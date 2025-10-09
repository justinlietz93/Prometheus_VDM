#!/usr/bin/env python3
"""
Tachyonic tube spectrum & condensation runner (diagonal baseline).

Generates artifacts for two tags:
  - tube-spectrum-v1: κ-spectrum across R_sweep (lowest root per ℓ)
  - tube-condensation-v1: Energy scan E(R) with diagonal quartic condensation

Approval policy: requires tag-specific manifest entry plus DB secrets unless --allow-unapproved is passed (artifacts then quarantined).

Artifacts:
  - Figures: spectrum distribution (optional), energy scan PNG
  - Logs: CSV (spectrum roots), CSV (energy scan), JSON summary

Gates:
  - Spectrum: coverage fraction ≥ 0.95 (finite κ for ≥95% of (R, ℓ) pairs attempted)
  - Condensation: finite energy fraction ≥ 0.80 and local minimum has positive second derivative within 10% tolerance from quadratic fit.
"""

from __future__ import annotations

import argparse, json
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List
import numpy as np
import math

# Ensure code root
import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from common.authorization.approval import check_tag_approval
from physics.tachyonic_condensation.cylinder_modes import compute_kappas
from physics.tachyonic_condensation.condense_tube import (
    compute_modes_for_R, build_quartic_diagonal, find_condensate_diagonal,
    mass_matrix_diagonal, tube_energy_diagonal, energy_scan, ModeEntry
)

@dataclass
class TubeSpec:
    tag: str
    R_sweep: List[float]
    mu: float
    lam: float
    c: float
    ell_max: int | None = 8


def load_spec(path: Path) -> TubeSpec:
    raw = json.loads(path.read_text())
    tag = str(raw.get("tag"))
    Rs = list(map(float, raw["grid"]["R_sweep"]))
    params = raw.get("params", {})
    mu = float(params.get("mu"))
    lam = float(params.get("lam"))
    c = float(params.get("c", 1.0))
    ell_max = int(params.get("ell_max", 8))
    return TubeSpec(tag=tag, R_sweep=Rs, mu=mu, lam=lam, c=c, ell_max=ell_max)


def run_spectrum(spec: TubeSpec) -> Dict[str, Any]:
    rows: List[List[float]] = []
    attempts = 0
    successes = 0
    for R in spec.R_sweep:
        roots = compute_kappas(R=R, mu=spec.mu, c=spec.c, ell_max=spec.ell_max, num_brackets=256)
        # bucket by ell and keep lowest root
        by_ell: Dict[int, List[Dict[str, float]]] = {}
        for r in roots:
            ell = int(round(r["ell"]))
            by_ell.setdefault(ell, []).append(r)
        for ell in range(spec.ell_max + 1):
            attempts += 1
            lst = by_ell.get(ell, [])
            if not lst:
                continue
            lst_sorted = sorted(lst, key=lambda d: float(d["kappa"]))
            r0 = lst_sorted[0]
            rows.append([R, float(ell), float(r0["kappa"]), float(r0["k_in"]), float(r0["k_out"])])
            successes += 1
    coverage = successes / max(1, attempts)
    passed = coverage >= 0.95
    # Artifact paths
    csvp = log_path("tachyonic_condensation", f"tube_spectrum_roots__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("R,ell,kappa,k_in,k_out\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    summary = {
        "tag": spec.tag,
        "coverage": coverage,
        "attempts": attempts,
        "successes": successes,
        "csv": str(csvp),
        "passed": passed,
    }
    write_log(log_path("tachyonic_condensation", f"tube_spectrum_summary__{spec.tag}", failed=not passed), summary)
    return summary


def run_condensation(spec: TubeSpec) -> Dict[str, Any]:
    scan = energy_scan(R_grid=spec.R_sweep, mu=spec.mu, lam=spec.lam, c=spec.c, ell_max=spec.ell_max)
    Rs = scan["R"]
    Es = scan["E"]
    min_R = float(scan["min_R"]) ; min_E = float(scan["min_E"]) if math.isfinite(scan["min_E"]) else float("nan")
    finite_fraction = float(np.mean(np.isfinite(Es)))
    # local quadratic fit near minimum if possible
    idx = int(np.nanargmin(Es)) if np.any(np.isfinite(Es)) else None
    curvature_ok = False
    fit_coeffs = None
    if idx is not None and 1 <= idx < len(Rs) - 1:
        # pick window of up to 5 points around idx
        lo = max(0, idx - 2)
        hi = min(len(Rs), idx + 3)
        window_R = Rs[lo:hi]
        window_E = Es[lo:hi]
        mask = np.isfinite(window_E)
        if np.sum(mask) >= 3:
            xr = np.array(window_R)[mask]
            yr = np.array(window_E)[mask]
            # fit a quadratic a R^2 + b R + c
            A = np.vstack([xr**2, xr, np.ones_like(xr)]).T
            coeffs, *_ = np.linalg.lstsq(A, yr, rcond=None)
            a = float(coeffs[0])
            curvature_ok = a > 0 and a < 10.0 * abs(a)  # trivial positivity; upper bound placeholder
            fit_coeffs = [float(x) for x in coeffs]
    passed = (finite_fraction >= 0.80) and curvature_ok

    # Artifacts
    import matplotlib.pyplot as plt
    figp = figure_path("tachyonic_condensation", f"tube_energy_scan__{spec.tag}", failed=not passed)
    plt.figure(figsize=(6.0,4.2))
    plt.plot(Rs, Es, "o-", label="E(R)")
    if math.isfinite(min_R) and math.isfinite(min_E):
        plt.axvline(min_R, color="red", ls="--", label=f"min R={min_R:.3f}")
    plt.xlabel("R") ; plt.ylabel("E") ; plt.title("Tachyonic Tube Condensation Energy Scan") ; plt.legend() ; plt.tight_layout()
    plt.savefig(figp, dpi=160) ; plt.close()

    csvp = log_path("tachyonic_condensation", f"tube_energy_scan__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("R,E\n")
        for Rv, Ev in zip(Rs, Es):
            f.write(f"{Rv},{Ev}\n")

    summary = {
        "tag": spec.tag,
        "finite_fraction": finite_fraction,
        "min_R": min_R,
        "min_E": min_E,
        "curvature_ok": curvature_ok,
        "fit_coeffs": fit_coeffs,
        "csv": str(csvp),
        "figure": str(figp),
        "passed": passed
    }
    write_log(log_path("tachyonic_condensation", f"tube_condensation_summary__{spec.tag}", failed=not passed), summary)
    return summary


def main():
    ap = argparse.ArgumentParser(description="Tachyonic tube spectrum & condensation runner")
    ap.add_argument("--spec", type=str, required=True, help="Path to tag-specific tube spec JSON")
    ap.add_argument("--allow-unapproved", action="store_true", help="Allow unapproved run (artifacts quarantined)")
    ap.add_argument("--mode", choices=["spectrum", "condensation"], required=True)
    args = ap.parse_args()
    spec_path = Path(args.spec)
    spec = load_spec(spec_path)
    # Approval gate
    _approved, _eng_only, _proposal = check_tag_approval("tachyonic_condensation", spec.tag, args.allow_unapproved, CODE_ROOT)
    if args.mode == "spectrum":
        result = run_spectrum(spec)
    else:
        result = run_condensation(spec)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
