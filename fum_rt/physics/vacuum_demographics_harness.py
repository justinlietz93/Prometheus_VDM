#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Vacuum demographics harness for the cosmology router vacuum channel.

This script mirrors the reproducibility pattern used by the other physics
runners.  It ingests a synthetic (or user-supplied) horizon activity tape,
propagates it through :class:`~fum_rt.core.cosmology.VacuumAccumulator`, and
compares the resulting equation-of-state residuals against the ΛCDM baseline.

The emitted JSON payload follows the RD runner schema: configuration snapshot,
metrics, per-sample timeline table, and artifact paths.  The figure plots the
w(z)+1 residual to make deviations from -1 immediately visible.

Usage example::

    python fum_rt/physics/vacuum_demographics_harness.py \
        --outdir /tmp/fum_vacuum \
        --eta 0.02 \
        --tape synthetic

The harness exits with status ``NEEDS_RECAL`` when the residual tolerance is
exceeded.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass
from typing import List, Sequence, Tuple

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from fum_rt.core.cosmology import (  # noqa: E402
    BudgetTick,
    HorizonActivityEvent,
    RetardedKernelSH,
    VacuumAccumulator,
)
from fum_rt.physics.harness_logging import (  # noqa: E402
    enrich_payload,
    hash_file,
    hash_jsonable,
)


@dataclass(frozen=True)
class TimelinePoint:
    """Evaluation sample consisting of cosmic time (Myr) and redshift."""

    t_myr: float
    redshift: float

    def as_tuple(self) -> Tuple[float, float]:
        return (float(self.t_myr), float(self.redshift))


@dataclass(frozen=True)
class HarnessConfig:
    """Immutable snapshot of the harness configuration."""

    epsilon: float
    local_radius: float
    max_events: int
    rho_lambda: float
    eta: float
    residual_tol: float
    position: Tuple[float, ...]
    budget: Tuple[int, int, int] | None

    def as_dict(self) -> dict:
        data = {
            "epsilon": self.epsilon,
            "local_radius": self.local_radius,
            "max_events": self.max_events,
            "rho_lambda": self.rho_lambda,
            "eta": self.eta,
            "residual_tol": self.residual_tol,
            "position": list(self.position),
        }
        if self.budget is not None:
            data["budget"] = {
                "max_ops": self.budget[0],
                "max_emits": self.budget[1],
                "ttl": self.budget[2],
            }
        else:
            data["budget"] = None
        return data


def _default_tape() -> Tuple[List[HorizonActivityEvent], List[TimelinePoint]]:
    """Return a reproducible synthetic BH activity tape and evaluation grid."""

    events = [
        HorizonActivityEvent(t=120, x=(0.0, 0.0, 0.0), dotA=6.5e-6, horizon_id="bh_000", dt_ret=40.0),
        HorizonActivityEvent(t=380, x=(0.5, 0.1, -0.2), dotA=-4.8e-6, horizon_id="bh_001", dt_ret=55.0),
        HorizonActivityEvent(t=610, x=(-0.3, 0.2, 0.15), dotA=5.1e-6, horizon_id="bh_002", dt_ret=60.0),
        HorizonActivityEvent(t=940, x=(0.15, -0.4, 0.25), dotA=-3.9e-6, horizon_id="bh_003", dt_ret=70.0),
        HorizonActivityEvent(t=1310, x=(-0.2, -0.15, -0.05), dotA=4.4e-6, horizon_id="bh_004", dt_ret=75.0),
        HorizonActivityEvent(t=1760, x=(0.05, 0.12, -0.18), dotA=-2.6e-6, horizon_id="bh_005", dt_ret=80.0),
        HorizonActivityEvent(t=2210, x=(-0.12, -0.07, 0.08), dotA=2.2e-6, horizon_id="bh_006", dt_ret=85.0),
        HorizonActivityEvent(t=2680, x=(0.02, 0.03, -0.05), dotA=-1.4e-6, horizon_id="bh_007", dt_ret=90.0),
        HorizonActivityEvent(t=3160, x=(0.0, 0.0, 0.0), dotA=1.1e-6, horizon_id="bh_008", dt_ret=95.0),
    ]
    timeline = [
        TimelinePoint(t_myr=200.0, redshift=6.5),
        TimelinePoint(t_myr=400.0, redshift=5.1),
        TimelinePoint(t_myr=700.0, redshift=4.0),
        TimelinePoint(t_myr=1100.0, redshift=3.0),
        TimelinePoint(t_myr=1600.0, redshift=2.4),
        TimelinePoint(t_myr=2100.0, redshift=1.8),
        TimelinePoint(t_myr=2600.0, redshift=1.2),
        TimelinePoint(t_myr=3100.0, redshift=0.8),
        TimelinePoint(t_myr=3600.0, redshift=0.4),
        TimelinePoint(t_myr=4100.0, redshift=0.1),
    ]
    return events, timeline


def _load_tape(path: str | None) -> Tuple[List[HorizonActivityEvent], List[TimelinePoint]]:
    if path is None or path == "synthetic":
        return _default_tape()
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    raw_events = payload.get("events", [])
    if not isinstance(raw_events, list):
        raise ValueError("events must be provided as a list")
    events: List[HorizonActivityEvent] = []
    for idx, entry in enumerate(raw_events):
        if not isinstance(entry, dict):
            raise ValueError(f"event #{idx} must be a mapping")
        event = HorizonActivityEvent(
            t=int(entry["t"]),
            x=tuple(entry.get("x", (0.0, 0.0, 0.0))),
            dotA=float(entry["dotA"]),
            horizon_id=str(entry["horizon_id"]),
            dt_ret=float(entry.get("dt_ret", 50.0)),
        )
        events.append(event)
    raw_timeline = payload.get("timeline", [])
    if not raw_timeline:
        raise ValueError("timeline must contain at least one sample")
    timeline: List[TimelinePoint] = []
    for idx, entry in enumerate(raw_timeline):
        if not isinstance(entry, dict):
            raise ValueError(f"timeline entry #{idx} must be a mapping")
        timeline.append(
            TimelinePoint(
                t_myr=float(entry["t_myr"]),
                redshift=float(entry["redshift"]),
            )
        )
    timeline.sort(key=lambda p: p.t_myr)
    return events, timeline


def default_horizon_tape() -> Tuple[List[HorizonActivityEvent], List[TimelinePoint]]:
    """Public helper returning the synthetic tape used by the harnesses."""

    return _default_tape()


def load_horizon_tape(path: str | None) -> Tuple[List[HorizonActivityEvent], List[TimelinePoint]]:
    """Load a horizon activity tape from ``path`` or return the synthetic tape."""

    return _load_tape(path)


def _prepare_budget(budget: Tuple[int, int, int] | None) -> BudgetTick | None:
    if budget is None:
        return None
    max_ops, max_emits, ttl = budget
    return BudgetTick(tick=0, max_ops=max_ops, max_emits=max_emits, ttl=ttl)


def _compute_rho_series(
    accumulator: VacuumAccumulator,
    events: Sequence[HorizonActivityEvent],
    timeline: Sequence[TimelinePoint],
    *,
    position: Sequence[float],
    budget: BudgetTick | None,
) -> List[float]:
    rho_values: List[float] = []
    for point in timeline:
        rho = accumulator.evaluate(
            t=point.t_myr,
            position=position,
            events=events,
            budget=budget,
        )
        rho_values.append(rho)
    return rho_values


def _compute_w_residuals(
    timeline: Sequence[TimelinePoint],
    rho_values: Sequence[float],
) -> List[float]:
    if len(timeline) != len(rho_values):
        raise ValueError("timeline and rho_values length mismatch")
    if not timeline:
        return []
    ln_a = [math.log(1.0 / (1.0 + p.redshift)) for p in timeline]
    ln_rho = [math.log(max(r, 1e-30)) for r in rho_values]
    residuals: List[float] = []
    n = len(timeline)
    for i in range(n):
        if n == 1:
            deriv = 0.0
        elif i == 0:
            deriv = (ln_rho[1] - ln_rho[0]) / max(1e-12, (ln_a[1] - ln_a[0]))
        elif i == n - 1:
            deriv = (ln_rho[-1] - ln_rho[-2]) / max(1e-12, (ln_a[-1] - ln_a[-2]))
        else:
            da = ln_a[i + 1] - ln_a[i - 1]
            dr = ln_rho[i + 1] - ln_rho[i - 1]
            deriv = dr / max(1e-12, da)
        w = -1.0 - (1.0 / 3.0) * deriv
        residuals.append(w + 1.0)
    return residuals


def _aggregate_metrics(residuals: Sequence[float], tol: float) -> Tuple[str, dict]:
    if not residuals:
        return "PASS", {"max_abs": 0.0, "rms": 0.0}
    max_abs = max(abs(r) for r in residuals)
    rms = math.sqrt(sum(r * r for r in residuals) / len(residuals))
    status = "PASS" if max_abs <= tol else "NEEDS_RECAL"
    metrics = {
        "max_abs": max_abs,
        "rms": rms,
        "tol": tol,
        "status": status,
    }
    return status, metrics


def _render_residuals(
    timeline: Sequence[TimelinePoint],
    residuals: Sequence[float],
    figure_path: str,
    status: str,
) -> None:
    if not figure_path:
        return
    os.makedirs(os.path.dirname(os.path.abspath(figure_path)), exist_ok=True)
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt  # type: ignore

    zs = [p.redshift for p in timeline]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(zs, residuals, marker="o", linestyle="-", color="tab:blue", label="w(z)+1")
    ax.axhline(0.0, color="black", linewidth=1.0, linestyle="--", label="ΛCDM baseline")
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("w(z) + 1")
    ax.set_title(f"Vacuum demographics residuals ({status})")
    ax.invert_xaxis()
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)


def evaluate_vacuum_demographics(
    events: Sequence[HorizonActivityEvent],
    timeline: Sequence[TimelinePoint],
    config: HarnessConfig,
    *,
    figure_path: str | None = None,
) -> dict:
    kernel = RetardedKernelSH(
        epsilon=config.epsilon,
        local_radius=config.local_radius,
        max_events=config.max_events,
    )
    accumulator = VacuumAccumulator(
        kernel=kernel,
        rho_lambda=config.rho_lambda,
        eta=config.eta,
    )
    budget_obj = _prepare_budget(config.budget)
    rho_values = _compute_rho_series(
        accumulator,
        events,
        timeline,
        position=config.position,
        budget=budget_obj,
    )
    residuals = _compute_w_residuals(timeline, rho_values)
    status, metrics = _aggregate_metrics(residuals, config.residual_tol)
    table = []
    for point, rho, resid in zip(timeline, rho_values, residuals):
        table.append(
            {
                "t_myr": point.t_myr,
                "redshift": point.redshift,
                "rho_vac": rho,
                "w_residual": resid,
            }
        )
    if figure_path:
        _render_residuals(timeline, residuals, figure_path, status)
    payload = {
        "config": config.as_dict(),
        "timeline": table,
        "metrics": metrics,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return payload


def _parse_position(spec: str | None) -> Tuple[float, ...]:
    if spec is None:
        return (0.0, 0.0, 0.0)
    parts = [chunk.strip() for chunk in spec.split(",") if chunk.strip()]
    if not parts:
        raise ValueError("position specification must contain coordinates")
    coords = tuple(float(p) for p in parts)
    if len(coords) > 4:
        raise ValueError("position must be local (≤4 coordinates)")
    return coords


def main() -> None:
    parser = argparse.ArgumentParser(description="Vacuum demographics harness for the cosmology router")
    parser.add_argument("--tape", type=str, default="synthetic", help="path to JSON tape payload or 'synthetic'")
    parser.add_argument("--epsilon", type=float, default=5e-3, help="retarded kernel coupling strength")
    parser.add_argument("--local-radius", type=float, default=1.0, help="locality radius for the kernel evaluation")
    parser.add_argument("--max-events", type=int, default=64, help="maximum horizon events per evaluation")
    parser.add_argument("--rho-lambda", type=float, default=6.0e-27, help="baseline vacuum energy density (kg/m^3)")
    parser.add_argument("--eta", type=float, default=0.01, help="router coupling coefficient η")
    parser.add_argument("--residual-tol", type=float, default=5e-4, help="ΛCDM residual tolerance for |w(z)+1|")
    parser.add_argument("--position", type=str, default=None, help="evaluation position as comma-separated coordinates")
    parser.add_argument("--budget", type=str, default=None, help="optional budget triple max_ops,max_emits,ttl")
    parser.add_argument("--outdir", type=str, default=None, help="base output directory")
    parser.add_argument("--figure", type=str, default=None, help="override figure path")
    parser.add_argument("--log", type=str, default=None, help="override JSON log path")
    args = parser.parse_args()

    events, timeline = load_horizon_tape(args.tape)
    position = _parse_position(args.position)
    budget_tuple: Tuple[int, int, int] | None
    if args.budget:
        parts = [int(chunk.strip()) for chunk in args.budget.split(",") if chunk.strip()]
        if len(parts) != 3:
            raise ValueError("budget must be 'max_ops,max_emits,ttl'")
        budget_tuple = (parts[0], parts[1], parts[2])
    else:
        budget_tuple = None

    config = HarnessConfig(
        epsilon=args.epsilon,
        local_radius=args.local_radius,
        max_events=args.max_events,
        rho_lambda=args.rho_lambda,
        eta=args.eta,
        residual_tol=args.residual_tol,
        position=position,
        budget=budget_tuple,
    )

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures")
    log_dir = os.path.join(base_outdir, "logs")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    figure_path = args.figure if args.figure else os.path.join(fig_dir, f"{script_name}_{timestamp}.png")
    log_path = args.log if args.log else os.path.join(log_dir, f"{script_name}_{timestamp}.json")

    payload = evaluate_vacuum_demographics(
        events,
        timeline,
        config,
        figure_path=figure_path,
    )

    tape_descriptor = {
        "events": [
            {
                "t": event.t,
                "x": list(event.x),
                "dotA": event.dotA,
                "horizon_id": event.horizon_id,
                "dt_ret": event.dt_ret,
            }
            for event in events
        ],
        "timeline": [
            {"t_myr": point.t_myr, "redshift": point.redshift}
            for point in timeline
        ],
    }
    hashes = {"horizon_tape": hash_jsonable(tape_descriptor)}
    if args.tape and args.tape != "synthetic":
        hashes["tape_file"] = hash_file(os.path.abspath(args.tape))

    gates = {
        "lcdm_residual_within_tol": payload["metrics"].get("status") == "PASS",
        "timeline_nonempty": bool(payload.get("timeline")),
    }
    budgets_meta = None
    if config.budget is not None:
        budgets_meta = {
            "max_ops": config.budget[0],
            "max_emits": config.budget[1],
            "ttl": config.budget[2],
        }
    seeds = {
        "tape": "synthetic_fixed"
        if not args.tape or args.tape == "synthetic"
        else "external",
    }

    payload = enrich_payload(
        payload,
        script_name=script_name,
        gates=gates,
        seeds=seeds,
        budgets=budgets_meta,
        hashes=hashes,
        outputs={
            "figure": os.path.abspath(figure_path),
            "log": os.path.abspath(log_path),
        },
        inputs={
            "tape": args.tape or "synthetic",
            "position": position,
        },
    )

    with open(log_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(json.dumps({
        "log": payload["outputs"].get("log"),
        "figure": payload["outputs"].get("figure"),
        "status": payload["metrics"]["status"],
        "gates": payload["gates"],
        "all_passed": payload["gate_summary"]["all_passed"],
    }, indent=2))


if __name__ == "__main__":
    main()
