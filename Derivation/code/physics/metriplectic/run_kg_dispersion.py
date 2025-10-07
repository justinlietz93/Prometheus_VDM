#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np
import sys

# Ensure common helpers on path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from common.approval import check_tag_approval
from physics.metriplectic.kg_ops import kg_verlet_step


@dataclass
class DispersionSpec:
    N: int = 512
    L: float = 2.0 * np.pi
    c: float = 1.0
    m: float = 1.0
    A: float = 1e-6
    dt: float = 0.01
    steps: int = 8000
    modes: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8, 10)
    tag: str = "KG-dispersion-v1"


def _grid(spec: DispersionSpec) -> Tuple[np.ndarray, float]:
    x = np.linspace(0.0, spec.L, spec.N, endpoint=False)
    dx = spec.L / spec.N
    return x, dx


def _project_sin(x: np.ndarray, y: np.ndarray, k: float) -> float:
    # a_k = 2/L ∫ y(x) sin(kx) dx (Riemann sum)
    L = float(x[-1] - x[0] + (x[1] - x[0]))
    dx = x[1] - x[0]
    return (2.0 / L) * float(np.sum(y * np.sin(k * x)) * dx)


def _measure_omega_from_zero_crossings(t: np.ndarray, y: np.ndarray) -> float:
    # Positive-going zero crossings with linear interpolation
    crossings: List[float] = []
    for i in range(len(y) - 1):
        if y[i] < 0.0 and y[i + 1] >= 0.0:
            dy = y[i + 1] - y[i]
            if abs(dy) < 1e-30:
                continue
            frac = -y[i] / dy
            t_cross = t[i] + frac * (t[i + 1] - t[i])
            crossings.append(t_cross)
    if len(crossings) < 2:
        return float("nan")
    periods = np.diff(np.array(crossings))
    T_mean = float(np.mean(periods))
    if T_mean <= 0:
        return float("nan")
    return 2.0 * np.pi / T_mean


def run_dispersion(spec: DispersionSpec, approved: bool = False, engineering_only: bool = False, proposal: str | None = None) -> Dict[str, Any]:
    x, dx = _grid(spec)
    results: List[Tuple[int, float, float]] = []  # (mode, k, omega)
    t = np.arange(spec.steps + 1, dtype=float) * spec.dt

    for m_idx in spec.modes:
        k = 2.0 * np.pi * (m_idx / spec.L)  # k = 2π m / L
        # Initial conditions: single sine mode in phi, zero momentum
        phi = spec.A * np.sin(k * x)
        pi = np.zeros_like(phi)
        # Record modal coefficient over time
        y = np.empty_like(t)
        y[0] = _project_sin(x, phi, k)
        cur_phi, cur_pi = phi.copy(), pi.copy()
        for n in range(1, spec.steps + 1):
            cur_phi, cur_pi = kg_verlet_step(cur_phi, cur_pi, spec.dt, dx, spec.c, spec.m)
            y[n] = _project_sin(x, cur_phi, k)

        omega = _measure_omega_from_zero_crossings(t, y)
        results.append((m_idx, k, omega))

    # Build regression data: y = omega^2, x = k^2
    k_arr = np.array([r[1] for r in results])
    w_arr = np.array([r[2] for r in results])
    k2 = k_arr * k_arr
    w2 = w_arr * w_arr

    # Linear regression w2 = slope * k2 + intercept
    slope, intercept = np.polyfit(k2, w2, 1)
    y_pred = slope * k2 + intercept
    ss_res = float(np.sum((w2 - y_pred) ** 2))
    ss_tot = float(np.sum((w2 - float(np.mean(w2))) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    # Gates
    rel_slope = abs(slope - spec.c * spec.c) / max(spec.c * spec.c, 1e-30)
    rel_intercept = abs(intercept - spec.m * spec.m) / max(spec.m * spec.m, 1e-30)
    passed = bool((R2 >= 0.999) and (rel_slope <= 0.01) and (rel_intercept <= 0.01))

    # Artifacts
    import matplotlib.pyplot as plt
    quarantine = engineering_only or (not approved)
    figp = figure_path("metriplectic", f"kg_dispersion_fit__{spec.tag}", failed=(not passed) or quarantine)
    xmin, xmax = float(np.min(k2)), float(np.max(k2))
    xs = np.linspace(xmin, xmax, 200)
    plt.figure(figsize=(6.2, 4.2))
    plt.plot(k2, w2, "o", label="modes")
    plt.plot(xs, slope * xs + intercept, "-", label=f"fit: R^2={R2:.6f}")
    plt.plot(xs, (spec.c * spec.c) * xs + (spec.m * spec.m), "--", label="theory")
    plt.xlabel(r"$k^2$")
    plt.ylabel(r"$\omega^2$")
    plt.title("KG dispersion fit")
    plt.legend(loc="best", fontsize=8)
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()

    # CSV
    csvp = log_path("metriplectic", f"kg_dispersion_fit__{spec.tag}", failed=(not passed) or quarantine, type="csv")
    with csvp.open("w", encoding="utf-8") as fcsv:
        fcsv.write("mode,k,k2,omega,omega2\n")
        for (m_idx, kk, ww) in results:
            fcsv.write(f"{m_idx},{kk},{kk*kk},{ww},{ww*ww}\n")

    # JSON log
    logj = {
        "params": {
            "N": spec.N, "L": spec.L, "c": spec.c, "m": spec.m,
            "A": spec.A, "dt": spec.dt, "steps": spec.steps,
            "modes": list(spec.modes)
        },
        "fit": {
            "slope": float(slope), "intercept": float(intercept), "R2": float(R2),
            "rel_slope": float(rel_slope), "rel_intercept": float(rel_intercept)
        },
        "gate": {"passed": passed, "R2_min": 0.999, "rel_tol": 0.01},
        "policy": {"approved": bool(approved), "engineering_only": bool(engineering_only), "quarantined": bool(quarantine), "tag": spec.tag, "proposal": proposal},
        "table": {"k": k_arr.tolist(), "omega": w_arr.tolist()},
        "figure": str(figp), "csv": str(csvp)
    }
    write_log(log_path("metriplectic", f"kg_dispersion_fit__{spec.tag}", failed=(not passed) or quarantine), logj)
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="KG dispersion: single-mode sweep and linear fit of omega^2 vs k^2")
    p.add_argument("--N", type=int, default=512)
    p.add_argument("--L", type=float, default=2.0 * np.pi)
    p.add_argument("--c", type=float, default=1.0)
    p.add_argument("--m", type=float, default=1.0)
    p.add_argument("--A", type=float, default=1e-6)
    p.add_argument("--dt", type=float, default=0.01)
    p.add_argument("--steps", type=int, default=8000)
    p.add_argument("--modes", type=str, default="1,2,3,4,5,6,8,10")
    p.add_argument("--tag", type=str, default="KG-dispersion-v1")
    p.add_argument("--allow-unapproved", action="store_true", help="Allow running with an unapproved tag (engineering-only; artifacts quarantined)")
    args = p.parse_args()
    modes = tuple(int(s) for s in args.modes.split(",") if s.strip())
    # Tag approval (shared utility)
    approved, engineering_only, proposal = check_tag_approval("metriplectic", args.tag, args.allow_unapproved, CODE_ROOT)
    spec = DispersionSpec(N=args.N, L=args.L, c=args.c, m=args.m, A=args.A, dt=args.dt, steps=args.steps, modes=modes, tag=args.tag)
    out = run_dispersion(spec, approved=approved, engineering_only=engineering_only, proposal=proposal)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
