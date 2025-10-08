#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, Any, List

import numpy as np
import sys

# Ensure common helpers on path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from common.data.results_db import (
    begin_run,
    add_artifacts,
    log_metrics,
    end_run_success,
    end_run_failed,
)
from common.authorization.approval import check_tag_approval
from physics.metriplectic.kg_ops import kg_verlet_step


@dataclass
class ConeSpec:
    N: int = 512
    L: float = 2.0 * np.pi
    c: float = 1.0
    m: float = 1.0
    A: float = 1e-4  # slightly larger than dispersion to clear threshold cleanly
    dt: float = 0.0025
    steps: int = 4000
    sigma_frac: float = 0.01  # sigma = sigma_frac * L
    threshold_rel: float = 1e-6  # threshold = threshold_rel * A
    tag: str = "KG-cone-v1"


def _grid(spec: ConeSpec) -> Tuple[np.ndarray, float]:
    x = np.linspace(0.0, spec.L, spec.N, endpoint=False)
    dx = spec.L / spec.N
    return x, dx


def _periodic_distance(x: np.ndarray, x0: float, L: float) -> np.ndarray:
    # minimal periodic distance on a ring [0,L)
    d = np.abs(x - x0)
    return np.minimum(d, L - d)


def _initial_gaussian(spec: ConeSpec, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    x0 = 0.5 * spec.L
    sigma = spec.sigma_frac * spec.L
    phi0 = spec.A * np.exp(-0.5 * ((x - x0) / sigma) ** 2)
    pi0 = np.zeros_like(phi0)
    return phi0, pi0, x0


def _front_radius(x: np.ndarray, x0: float, L: float, phi: np.ndarray, thresh: float) -> float:
    mask = np.abs(phi) >= thresh
    if not np.any(mask):
        return 0.0
    d = _periodic_distance(x, x0, L)
    return float(np.max(d[mask]))


def run_cone(spec: ConeSpec, approved: bool = False, engineering_only: bool = False, proposal: str | None = None) -> Dict[str, Any]:
    x, dx = _grid(spec)
    t = np.arange(spec.steps + 1, dtype=float) * spec.dt
    phi, pi, x0 = _initial_gaussian(spec, x)
    thresh = spec.threshold_rel * spec.A

    # Optional space-time for visualization: store |phi| at a stride to limit memory
    stride_t = max(1, int(spec.steps // 400))  # at most ~400 time slices
    st_slices: List[np.ndarray] = []
    st_times: List[float] = []

    R: np.ndarray = np.zeros_like(t)
    R[0] = _front_radius(x, x0, spec.L, phi, thresh)
    if 0 % stride_t == 0:
        st_slices.append(np.abs(phi).copy())
        st_times.append(t[0])

    cur_phi, cur_pi = phi.copy(), pi.copy()
    for n in range(1, spec.steps + 1):
        cur_phi, cur_pi = kg_verlet_step(cur_phi, cur_pi, spec.dt, dx, spec.c, spec.m)
        R[n] = _front_radius(x, x0, spec.L, cur_phi, thresh)
        if n % stride_t == 0:
            st_slices.append(np.abs(cur_phi).copy())
            st_times.append(t[n])

    # Fit R(t) = v * t + b
    coeffs = np.polyfit(t, R, 1)
    v = float(coeffs[0])
    b = float(coeffs[1])
    R_pred = v * t + b
    ss_res = float(np.sum((R - R_pred) ** 2))
    ss_tot = float(np.sum((R - float(np.mean(R))) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    # Gate: speed <= c*(1+eps)
    eps = 0.02
    passed = bool(v <= spec.c * (1.0 + eps))

    # Artifacts
    import matplotlib.pyplot as plt
    quarantine = engineering_only or (not approved)
    figp = figure_path("metriplectic", f"kg_light_cone__{spec.tag}", failed=(not passed) or quarantine)

    # Build space-time image
    if st_slices:
        ST = np.stack(st_slices, axis=0)  # [T, X]
        extent = [0.0, spec.L, st_times[0], st_times[-1]]  # x from 0..L, t from 0..T
        plt.figure(figsize=(6.4, 4.2))
        plt.imshow(ST, aspect='auto', origin='lower', extent=extent, cmap='magma')
        # Overlay measured front as R(t) around x0 -> draw both +/- branches (unwrapped in [0,L])
        tt = np.array(st_times)
        Rt = np.interp(tt, t, R)
        x_plus = (x0 + Rt)
        x_minus = (x0 - Rt)
        # Clip into [0,L]
        x_plus = np.mod(x_plus, spec.L)
        x_minus = np.mod(x_minus, spec.L)
        plt.plot(x_plus, tt, 'c-', lw=1.2, label='front +R(t)')
        plt.plot(x_minus, tt, 'c--', lw=1.0, label='front -R(t)')
        # Reference light cone lines at slope c
        t_line = np.linspace(tt[0], tt[-1], 200)
        ref_plus = (x0 + spec.c * t_line)
        ref_minus = (x0 - spec.c * t_line)
        plt.plot(np.mod(ref_plus, spec.L), t_line, 'w:', lw=1.0, label='|dx/dt|=c')
        plt.plot(np.mod(ref_minus, spec.L), t_line, 'w:', lw=1.0)
        plt.colorbar(label='|phi|')
        plt.xlabel('x')
        plt.ylabel('t')
        plt.title('KG local causality cone')
        plt.legend(loc='upper right', fontsize=7)
        plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()

    # CSV of R(t)
    csvp = log_path("metriplectic", f"kg_light_cone__{spec.tag}", failed=(not passed) or quarantine, type="csv")
    with csvp.open("w", encoding="utf-8") as fcsv:
        fcsv.write("t,R\n")
        for ti, Ri in zip(t, R):
            fcsv.write(f"{ti},{Ri}\n")

    # JSON log
    logj = {
        "params": {
            "N": spec.N, "L": spec.L, "c": spec.c, "m": spec.m,
            "A": spec.A, "dt": spec.dt, "steps": spec.steps,
            "sigma_frac": spec.sigma_frac, "threshold_rel": spec.threshold_rel
        },
        "fit": {"speed": v, "intercept": b, "R2": R2},
        "gate": {"passed": passed, "speed_max": spec.c * (1.0 + eps), "eps": eps},
        "policy": {"approved": bool(approved), "engineering_only": bool(engineering_only), "quarantined": bool(quarantine), "tag": spec.tag, "proposal": proposal},
        "figure": str(figp),
        "csv": str(csvp),
    }
    write_log(log_path("metriplectic", f"kg_light_cone__{spec.tag}", failed=(not passed) or quarantine), logj)

    # Results DB logging
    try:
        handle = begin_run(
            domain="metriplectic",
            experiment=str(Path(__file__).resolve()),
            tag=spec.tag,
            params={
                "N": spec.N, "L": spec.L, "c": spec.c, "m": spec.m,
                "A": spec.A, "dt": spec.dt, "steps": spec.steps,
                "sigma_frac": spec.sigma_frac, "threshold_rel": spec.threshold_rel,
            },
            engineering_only=bool(quarantine),
        )
        add_artifacts(handle, {"figure": str(figp), "csv": str(csvp)})
        log_metrics(handle, {"speed": float(v), "intercept": float(b), "R2": float(R2), "passed": bool(passed)})
        if passed:
            end_run_success(handle)
        else:
            end_run_failed(handle, metrics={"passed": False})
    except Exception as _e:
        _ = _e

    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="KG locality cone: Gaussian packet front speed and space–time plot")
    p.add_argument("--N", type=int, default=512)
    p.add_argument("--L", type=float, default=2.0 * np.pi)
    p.add_argument("--c", type=float, default=1.0)
    p.add_argument("--m", type=float, default=1.0)
    p.add_argument("--A", type=float, default=1e-4)
    p.add_argument("--dt", type=float, default=0.0025)
    p.add_argument("--steps", type=int, default=4000)
    p.add_argument("--sigma-frac", dest="sigma_frac", type=float, default=0.01)
    p.add_argument("--threshold-rel", dest="threshold_rel", type=float, default=1e-6)
    p.add_argument("--tag", type=str, default="KG-cone-v1")
    p.add_argument("--allow-unapproved", action="store_true", help="Allow running with an unapproved tag (engineering-only; artifacts quarantined)")
    args = p.parse_args()

    # Approval check
    approved, engineering_only, proposal = check_tag_approval("metriplectic", args.tag, args.allow_unapproved, CODE_ROOT)

    spec = ConeSpec(N=args.N, L=args.L, c=args.c, m=args.m, A=args.A, dt=args.dt, steps=args.steps,
                    sigma_frac=args.sigma_frac, threshold_rel=args.threshold_rel, tag=args.tag)
    out = run_cone(spec, approved=approved, engineering_only=engineering_only, proposal=proposal)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
