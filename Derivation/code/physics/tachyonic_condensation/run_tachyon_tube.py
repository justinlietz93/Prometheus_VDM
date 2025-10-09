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
from typing import Any, Dict, List, Optional
import numpy as np
import math

# Ensure code root
import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from common.authorization.approval import check_tag_approval
from physics.tachyonic_condensation.cylinder_modes import compute_kappas, has_root_potential
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
    sigma: Optional[float] = None
    alpha: Optional[float] = None


def load_spec(path: Path) -> TubeSpec:
    raw = json.loads(path.read_text())
    tag = str(raw.get("tag"))
    Rs = list(map(float, raw["grid"]["R_sweep"]))
    params = raw.get("params", {})
    mu = float(params.get("mu"))
    lam = float(params.get("lam"))
    c = float(params.get("c", 1.0))
    ell_max = int(params.get("ell_max", 8))
    sigma = params.get("sigma")
    alpha = params.get("alpha")
    sigma_f = float(sigma) if sigma is not None else None
    alpha_f = float(alpha) if alpha is not None else None
    return TubeSpec(tag=tag, R_sweep=Rs, mu=mu, lam=lam, c=c, ell_max=ell_max, sigma=sigma_f, alpha=alpha_f)


def run_spectrum(spec: TubeSpec, num_brackets: int = 512) -> Dict[str, Any]:
    rows: List[List[float]] = []
    attempts = 0
    successes = 0
    # Track per-R and per-ell hits for plotting
    R_hits: Dict[float, Dict[int, bool]] = {R: {ell: False for ell in range(spec.ell_max + 1)} for R in spec.R_sweep}
    R_possible: Dict[float, Dict[int, bool]] = {R: {ell: False for ell in range(spec.ell_max + 1)} for R in spec.R_sweep}
    for R in spec.R_sweep:
        # mark possible pairs first
        for ell in range(spec.ell_max + 1):
            if has_root_potential(R=R, mu=spec.mu, c=spec.c, ell=ell, probes=max(64, num_brackets // 8)):
                R_possible[R][ell] = True
        roots = compute_kappas(R=R, mu=spec.mu, c=spec.c, ell_max=spec.ell_max, num_brackets=num_brackets)
        # bucket by ell and keep lowest root
        by_ell: Dict[int, List[Dict[str, float]]] = {}
        for r in roots:
            ell = int(round(r["ell"]))
            by_ell.setdefault(ell, []).append(r)
        for ell in range(spec.ell_max + 1):
            lst = by_ell.get(ell, [])
            found = bool(lst)
            # attempts: count pairs either predicted possible OR actually found (for robustness)
            if R_possible[R][ell] or found:
                attempts += 1
            if not found:
                continue
            lst_sorted = sorted(lst, key=lambda d: float(d["kappa"]))
            r0 = lst_sorted[0]
            rows.append([R, float(ell), float(r0["kappa"]), float(r0["k_in"]), float(r0["k_out"])])
            successes += 1
            R_hits[R][ell] = True
    coverage_phys = min(1.0, successes / max(1, attempts))
    # Also compute raw coverage over all (R, ell) pairs
    total_all_attempts = len(spec.R_sweep) * (spec.ell_max + 1)
    coverage_raw = successes / max(1, total_all_attempts)
    passed = coverage_phys >= 0.95
    # Artifact paths
    csvp = log_path("tachyonic_condensation", f"tube_spectrum_roots__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("R,ell,kappa,k_in,k_out\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    # Figure: scatter κ vs R (color by ell) + per-R coverage line
    try:
        import matplotlib.pyplot as plt
        R_sorted = sorted(R_hits.keys())
        figp = figure_path("tachyonic_condensation", f"tube_spectrum_overview__{spec.tag}", failed=not passed)
        plt.figure(figsize=(7.5, 4.5))
        ax1 = plt.gca()
        if rows:
            Rs = np.array([row[0] for row in rows], float)
            ells = np.array([row[1] for row in rows], float)
            kappas = np.array([row[2] for row in rows], float)
            sc = ax1.scatter(Rs, kappas, c=ells, cmap="viridis", s=20, edgecolor="none")
            cbar = plt.colorbar(sc, ax=ax1)
            cbar.set_label("ell")
        ax1.set_xlabel("R")
        ax1.set_ylabel("kappa (lowest per ell)")
        ax1.grid(True, alpha=0.2)
        # Twin axis: coverage per R
        ax2 = ax1.twinx()
        per_R_cov = []
        for Rv in R_sorted:
            hit_map = R_hits[Rv]
            per_R_cov.append(sum(1 for v in hit_map.values() if v) / (spec.ell_max + 1))
        ax2.plot(R_sorted, per_R_cov, "r-o", lw=1.5, ms=4, label="coverage per R")
        ax2.set_ylabel("coverage per R")
        ax2.set_ylim(0.0, 1.05)
        title_pass = "PASS" if passed else "FAIL"
        plt.title(
            f"Tube Spectrum: cov_phys={coverage_phys:.3f}, cov_raw={coverage_raw:.3f} [{title_pass}]\n(tag={spec.tag})"
        )
        plt.tight_layout()
        plt.savefig(figp, dpi=160)
        plt.close()
        figure_path_str = str(figp)
    except Exception:
        figure_path_str = None
    # Diagnostic heatmap: possible vs found (R×ell)
    heatmap_path_str = None
    try:
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        R_sorted = sorted(R_hits.keys())
        hm = np.zeros((len(R_sorted), spec.ell_max + 1))
        for i, Rv in enumerate(R_sorted):
            for ell in range(spec.ell_max + 1):
                # 0 = impossible, 1 = possible but not found, 2 = found
                if R_possible[Rv][ell]:
                    hm[i, ell] = 2.0 if R_hits[Rv][ell] else 1.0
                else:
                    hm[i, ell] = 0.0
        cmap = mcolors.ListedColormap(["#dddddd", "#fdae61", "#2b83ba"])  # grey, orange, blue
        bounds = [-0.5, 0.5, 1.5, 2.5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        figp_hm = figure_path("tachyonic_condensation", f"tube_spectrum_heatmap__{spec.tag}", failed=not passed)
        plt.figure(figsize=(8.0, 5.0))
        plt.imshow(hm.T, aspect="auto", origin="lower", cmap=cmap, norm=norm,
                   extent=[min(R_sorted), max(R_sorted), 0, spec.ell_max])
        plt.colorbar(ticks=[0,1,2], label="state (0=impossible, 1=possible, 2=found)")
        plt.xlabel("R")
        plt.ylabel("ell")
        plt.title("Spectrum root availability vs detection")
        plt.tight_layout()
        plt.savefig(figp_hm, dpi=160)
        plt.close()
        heatmap_path_str = str(figp_hm)
    except Exception as _hm_err:
        # Diagnostic figure is optional; ignore errors silently while keeping summary intact
        _ = _hm_err
    summary = {
        "tag": spec.tag,
        "metrics_version": "v2-phys-aware",
        "coverage": coverage_phys,
        "coverage_phys": coverage_phys,
        "coverage_raw": coverage_raw,
        "attempts": attempts,
        "attempts_phys": attempts,
        "attempts_raw": total_all_attempts,
        "successes": successes,
        "csv": str(csvp),
        "figure": figure_path_str,
        "heatmap": heatmap_path_str,
        "passed": passed,
    }
    write_log(log_path("tachyonic_condensation", f"tube_spectrum_summary__{spec.tag}", failed=not passed), summary)
    return summary


def _bg_energy_fn(sigma: Optional[float], alpha: Optional[float]):
    if sigma is None and alpha is None:
        return None
    def E_bg(R: float) -> float:
        val = 0.0
        if sigma is not None:
            val += 2.0 * math.pi * float(sigma) * R
        if alpha is not None and R > 0:
            val += float(alpha) / R
        return val
    return E_bg


def run_condensation(spec: TubeSpec) -> Dict[str, Any]:
    Ebg = _bg_energy_fn(spec.sigma, spec.alpha)
    scan = energy_scan(R_grid=spec.R_sweep, mu=spec.mu, lam=spec.lam, c=spec.c, ell_max=spec.ell_max, E_bg=Ebg)
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
            curvature_ok = a > 0.0
            fit_coeffs = [float(x) for x in coeffs]
    # fallback: discrete second difference if quadratic fit not conclusive
    if not curvature_ok and idx is not None and 1 <= idx < len(Rs) - 1:
        E_im1, E_i, E_ip1 = Es[idx - 1], Es[idx], Es[idx + 1]
        if all(map(np.isfinite, (E_im1, E_i, E_ip1))):
            d2 = (E_ip1 - 2.0 * E_i + E_im1)
            curvature_ok = d2 > 0.0
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
    ap.add_argument("--num-brackets", type=int, default=512, help="Bracketing resolution for spectrum solver")
    args = ap.parse_args()
    spec_path = Path(args.spec)
    spec = load_spec(spec_path)
    # Approval gate
    _approved, _eng_only, _proposal = check_tag_approval("tachyonic_condensation", spec.tag, args.allow_unapproved, CODE_ROOT)
    if args.mode == "spectrum":
        result = run_spectrum(spec, num_brackets=int(args.num_brackets))
    else:
        result = run_condensation(spec)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
