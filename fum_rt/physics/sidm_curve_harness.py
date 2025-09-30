#!/usr/bin/env python3
"""SIDM cross-section harness for the cosmology router grain shim.

This runner mirrors the FUM reproducibility pattern: it takes a velocity grid,
queries :class:`~fum_rt.core.cosmology.GrainScatteringShim`, evaluates the
monotonicity/acceptance gates, emits JSON logs, and produces a plot with the
pre-registered dwarf→cluster acceptance bands.

Usage (example)::

    python fum_rt/physics/sidm_curve_harness.py \
        --grid "10,20,30,50,80,120,200,350,600,900" \
        --outdir /tmp/fum_sidm

The JSON payload mirrors other physics runners: config snapshot, acceptance
summary, artifact paths, and timestamp. The acceptance status flips to
``NEEDS_RECAL`` if any velocity point leaves its band or if the curve ceases to
be monotone decreasing.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from fum_rt.core.cosmology import GrainScatteringShim
from fum_rt.physics.harness_logging import enrich_payload, hash_jsonable


DEFAULT_GRID = "10,20,30,50,80,120,200,350,600,900"


@dataclass(frozen=True)
class AcceptanceBand:
    """Acceptance envelope for a velocity interval."""

    label: str
    v_min: float
    v_max: float
    sigma_min: float
    sigma_max: float

    def contains(self, velocity: float) -> bool:
        v = float(velocity)
        if math.isclose(self.v_max, math.inf):
            return self.v_min <= v
        return self.v_min <= v <= self.v_max

    def as_dict(self) -> Dict[str, float | str]:
        return {
            "label": self.label,
            "v_min": self.v_min,
            "v_max": self.v_max,
            "sigma_min": self.sigma_min,
            "sigma_max": self.sigma_max,
        }


ACCEPTANCE_BANDS: Sequence[AcceptanceBand] = (
    AcceptanceBand(
        label="Dwarf spheroidal band",
        v_min=0.0,
        v_max=80.0,
        sigma_min=0.3,
        sigma_max=10.0,
    ),
    AcceptanceBand(
        label="Milky Way / LSB band",
        v_min=80.0,
        v_max=300.0,
        sigma_min=0.05,
        sigma_max=3.0,
    ),
    AcceptanceBand(
        label="Cluster band",
        v_min=300.0,
        v_max=math.inf,
        sigma_min=0.005,
        sigma_max=0.5,
    ),
)


def parse_velocity_grid(spec: str) -> List[float]:
    """Parse a comma-separated velocity list (km/s)."""

    parts = [chunk.strip() for chunk in spec.split(",") if chunk.strip()]
    if not parts:
        raise ValueError("velocity grid must contain at least one entry")
    values: List[float] = []
    for part in parts:
        try:
            val = abs(float(part))
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError(f"invalid velocity entry '{part}'") from exc
        if not math.isfinite(val):
            raise ValueError("velocity entries must be finite")
        values.append(val)
    return sorted(set(values))


def generate_curve(shim: GrainScatteringShim, velocities: Sequence[float]) -> List[Dict[str, float]]:
    """Compute the σ_T/m curve for the supplied velocity grid."""

    return shim.curve(velocities)


def evaluate_curve(
    curve: Sequence[Dict[str, float]],
    *,
    bands: Sequence[AcceptanceBand] = ACCEPTANCE_BANDS,
    monotone_tol: float = 1e-9,
) -> Dict[str, object]:
    """Return acceptance analysis for the supplied curve."""

    details: List[Dict[str, object]] = []
    within_bands = True
    monotone = True
    last_sigma = None

    for entry in curve:
        v = float(entry["v"])
        sigma = float(entry["sigmaT_over_m"])
        band = next((b for b in bands if b.contains(v)), None)
        if band is None:
            within = False
            within_bands = False
            band_label = None
            sigma_min = math.nan
            sigma_max = math.nan
        else:
            sigma_min = band.sigma_min
            sigma_max = band.sigma_max
            within = (sigma_min - monotone_tol) <= sigma <= (sigma_max + monotone_tol)
            if not within:
                within_bands = False
            band_label = band.label
        if last_sigma is not None and sigma > last_sigma + monotone_tol:
            monotone = False
        details.append(
            {
                "v": v,
                "sigmaT_over_m": sigma,
                "band": band_label,
                "sigma_min": sigma_min,
                "sigma_max": sigma_max,
                "within_band": within,
            }
        )
        last_sigma = sigma

    status = "PASS" if (within_bands and monotone) else "NEEDS_RECAL"
    return {
        "details": details,
        "within_bands": within_bands,
        "monotone": monotone,
        "status": status,
    }


def render_curve_figure(
    curve: Sequence[Dict[str, float]],
    figure_path: str,
    *,
    bands: Sequence[AcceptanceBand] = ACCEPTANCE_BANDS,
    status: str,
) -> None:
    """Render the SIDM curve with acceptance bands."""

    os.makedirs(os.path.dirname(os.path.abspath(figure_path)), exist_ok=True)
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt  # type: ignore

    velocities = [entry["v"] for entry in curve]
    sigmas = [entry["sigmaT_over_m"] for entry in curve]

    fig, ax = plt.subplots(figsize=(6, 4))
    for idx, band in enumerate(bands):
        v_bounds: Iterable[float]
        if math.isinf(band.v_max):
            v_bounds = [band.v_min, velocities[-1] if velocities else band.v_min]
        else:
            v_bounds = [band.v_min, band.v_max]
        ax.fill_between(
            v_bounds,
            [band.sigma_min, band.sigma_min],
            [band.sigma_max, band.sigma_max],
            alpha=0.15,
            label=f"{band.label} acceptance" if idx == 0 else None,
            color="#4C72B0",
        )
    ax.plot(velocities, sigmas, marker="o", color="#DD8452", label="σ_T/m curve")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Velocity [km/s]")
    ax.set_ylabel(r"σ_T / m [cm² / g]")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.set_title(f"SIDM curve status: {status}")
    handles, labels = ax.get_legend_handles_labels()
    if any(labels):
        ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)


def build_payload(
    *,
    shim: GrainScatteringShim,
    curve: Sequence[Dict[str, float]],
    analysis: Dict[str, object],
    figure_path: str,
    velocity_grid: Sequence[float],
    timestamp: str,
) -> Dict[str, object]:
    """Compose the JSON payload emitted by the runner."""

    return {
        "timestamp": timestamp,
        "shim_params": {
            "r_star": shim.r_star,
            "mass_scale": shim.mass_scale,
            "v_scale": shim.v_scale,
            "alpha": shim.alpha,
            "sigma_floor": shim.sigma_floor,
            "sigma_ceiling": shim.sigma_ceiling,
        },
        "velocity_grid_km_s": list(velocity_grid),
        "curve": list(curve),
        "acceptance_bands": [band.as_dict() for band in ACCEPTANCE_BANDS],
        "analysis": analysis,
        "outputs": {
            "figure": os.path.abspath(figure_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the SIDM σ_T/m curve for the cosmology grain shim with "
            "pre-registered dwarf→cluster acceptance bands."
        )
    )
    parser.add_argument(
        "--grid",
        type=str,
        default=DEFAULT_GRID,
        help="Comma-separated velocity grid in km/s (default: %(default)s)",
    )
    parser.add_argument(
        "--r_star",
        type=float,
        default=0.5,
        help="Grain effective radius R_* (same units as mass scale input).",
    )
    parser.add_argument(
        "--mass_scale",
        type=float,
        default=1.0,
        help="Mass scale used to convert geometric cross-section to σ_T/m.",
    )
    parser.add_argument(
        "--v_scale",
        type=float,
        default=150.0,
        help="Velocity scale (km/s) controlling where the curve turns over.",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=2.0,
        help="Power-law falloff exponent for σ_T/m(v).",
    )
    parser.add_argument(
        "--sigma_floor",
        type=float,
        default=1e-3,
        help="Lower hard floor for σ_T/m (cm²/g).",
    )
    parser.add_argument(
        "--sigma_ceiling",
        type=float,
        default=10.0,
        help="Upper hard ceiling for σ_T/m (cm²/g).",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=None,
        help="Base output directory (defaults to fum_rt/physics/outputs).",
    )
    parser.add_argument(
        "--figure",
        type=str,
        default=None,
        help="Optional override for figure path (png).",
    )
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="Optional override for JSON log path.",
    )
    args = parser.parse_args()

    velocities = parse_velocity_grid(args.grid)
    shim = GrainScatteringShim(
        r_star=args.r_star,
        mass_scale=args.mass_scale,
        v_scale=args.v_scale,
        alpha=args.alpha,
        sigma_floor=args.sigma_floor,
        sigma_ceiling=args.sigma_ceiling,
    )

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    tstamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures")
    log_dir = os.path.join(base_outdir, "logs")
    figure_path = (
        args.figure
        if args.figure
        else os.path.join(fig_dir, f"{script_name}_{tstamp}.png")
    )
    log_path = (
        args.log
        if args.log
        else os.path.join(log_dir, f"{script_name}_{tstamp}.json")
    )
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)

    curve = generate_curve(shim, velocities)
    analysis = evaluate_curve(curve)
    render_curve_figure(curve, figure_path, status=analysis["status"])

    payload = build_payload(
        shim=shim,
        curve=curve,
        analysis=analysis,
        figure_path=figure_path,
        velocity_grid=velocities,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )

    hashes = {
        "velocity_grid": hash_jsonable(velocities),
        "curve": hash_jsonable(curve),
        "shim_params": hash_jsonable(payload["shim_params"]),
    }
    gates = {
        "monotone_decreasing": bool(analysis.get("monotone", False)),
        "within_acceptance_bands": bool(analysis.get("within_bands", False)),
    }
    payload = enrich_payload(
        payload,
        script_name=script_name,
        gates=gates,
        seeds={"grid_points": len(velocities)},
        hashes=hashes,
        outputs={
            "figure": os.path.abspath(figure_path),
            "log": os.path.abspath(log_path),
        },
        inputs={"velocity_grid": velocities},
    )

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps({
        "log": payload["outputs"].get("log"),
        "figure": payload["outputs"].get("figure"),
        "status": analysis["status"],
        "gates": payload["gates"],
        "all_passed": payload["gate_summary"]["all_passed"],
    }, indent=2))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
