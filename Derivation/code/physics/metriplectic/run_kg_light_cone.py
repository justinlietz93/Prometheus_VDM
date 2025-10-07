#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import sys

CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from physics.metriplectic.kg_ops import kg_verlet_step


@dataclass
class ConeSpec:
    N: int = 512
    L: float = 2.0 * np.pi
    c: float = 1.0
    m: float = 1.0
    A: float = 1e-4
    sigma: float = 0.05  # Gaussian width in fraction of L
    dt: float = 0.005
    steps: int = 4000
    thresh_frac: float = 1e-6
    tag: str = "KG-cone-v1"


def _grid(spec: ConeSpec) -> Tuple[np.ndarray, float]:
    x = np.linspace(0.0, spec.L, spec.N, endpoint=False)
    dx = spec.L / spec.N
    return x, dx


def _initial_gaussian(spec: ConeSpec, x: np.ndarray) -> np.ndarray:
    x0 = 0.5 * spec.L
    sig = spec.sigma * spec.L
    return spec.A * np.exp(-0.5 * ((x - x0) / sig) ** 2)


def _radius_at_threshold(phi: np.ndarray, x: np.ndarray, x0: float, thresh: float) -> float:
    # smallest radius R such that max(|phi| in [x0-R, x0+R]) >= thresh (periodic domain)
    N = x.size
    L = x[-1] - x[0] + (x[1] - x[0])
    dx = x[1] - x[0]
    # distances with periodic wrap
    dxs = np.abs(((x - x0 + 0.5 * L) % L) - 0.5 * L)
    # monotone search over unique radii set
    order = np.argsort(dxs)
    max_abs = 0.0
    R = 0.0
    for idx in order:
        max_abs = max(max_abs, abs(phi[idx]))
        R = dxs[idx]
        if max_abs >= thresh:
            return float(R)
    return float(R)


def run_light_cone(spec: ConeSpec) -> Dict[str, Any]:
    x, dx = _grid(spec)
    x0 = 0.5 * spec.L
    phi0 = _initial_gaussian(spec, x)
    pi0 = np.zeros_like(phi0)
    peak0 = float(np.max(np.abs(phi0)))
    thresh = spec.thresh_frac * max(peak0, 1e-30)

    t = np.arange(spec.steps + 1, dtype=float) * spec.dt
    R = np.empty_like(t)
    cur_phi, cur_pi = phi0.copy(), pi0.copy()
    R[0] = _radius_at_threshold(cur_phi, x, x0, thresh)
    for n in range(1, spec.steps + 1):
        cur_phi, cur_pi = kg_verlet_step(cur_phi, cur_pi, spec.dt, dx, spec.c, spec.m)
        R[n] = _radius_at_threshold(cur_phi, x, x0, thresh)

    # Linear fit: R(t) ~ v * t + b
    A = np.vstack([t, np.ones_like(t)]).T
    v, b = np.linalg.lstsq(A, R, rcond=None)[0]
    R_pred = v * t + b
    ss_res = float(np.sum((R - R_pred) ** 2))
    ss_tot = float(np.sum((R - float(np.mean(R))) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    passed = bool(v <= spec.c * (1.0 + 0.02) + 1e-15)

    # Artifacts
    import matplotlib.pyplot as plt
    # spacetime image (optional but helpful): show |phi| with light-cone overlay
    figp = figure_path("metriplectic", f"kg_light_cone__{spec.tag}", failed=not passed)
    plt.figure(figsize=(6.4, 4.4))
    # downsample for visualization
    # create a small spacetime image by sampling every N//256
    stride = max(1, spec.N // 256)
    im = []
    cur_phi, cur_pi = phi0.copy(), pi0.copy()
    for n in range(spec.steps + 1):
        if n > 0:
            cur_phi, cur_pi = kg_verlet_step(cur_phi, cur_pi, spec.dt, dx, spec.c, spec.m)
        im.append(np.abs(cur_phi[::stride]))
    im_arr = np.array(im)
    extent = [0, spec.L, spec.steps * spec.dt, 0]
    plt.imshow(im_arr, aspect='auto', extent=extent, cmap='magma')
    # overlay measured R(t)
    plt.plot(x0 + R, t, 'c-', lw=1.0, label='R(t)')
    plt.plot(x0 - R, t, 'c-', lw=1.0)
    # overlay fitted slope lines (x0 ± v t)
    plt.plot(x0 + (v * t + b), t, 'w--', lw=1.0, label=f'fit v={v:.4f}, R^2={R2:.5f}')
    plt.plot(x0 - (v * t + b), t, 'w--', lw=1.0)
    plt.colorbar(label='|phi|')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.title('KG locality cone')
    plt.legend(loc='upper right', fontsize=8)
    plt.tight_layout(); plt.savefig(figp, dpi=140); plt.close()

    # CSV
    csvp = log_path("metriplectic", f"kg_light_cone__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as fcsv:
        fcsv.write("t,R\n")
        for ti, Ri in zip(t, R):
            fcsv.write(f"{ti},{Ri}\n")

    # JSON
    logj = {
        "params": {
            "N": spec.N, "L": spec.L, "c": spec.c, "m": spec.m,
            "A": spec.A, "sigma": spec.sigma, "dt": spec.dt, "steps": spec.steps,
            "thresh_frac": spec.thresh_frac
        },
        "fit": {"v": float(v), "b": float(b), "R2": float(R2)},
    "gate": {"passed": passed, "v_max": spec.c * (1.0 + 0.02)},
        "figure": str(figp), "csv": str(csvp)
    }
    write_log(log_path("metriplectic", f"kg_light_cone__{spec.tag}", failed=not passed), logj)
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="KG locality cone: front speed estimate from threshold radius")
    p.add_argument("--N", type=int, default=512)
    p.add_argument("--L", type=float, default=2.0 * np.pi)
    p.add_argument("--c", type=float, default=1.0)
    p.add_argument("--m", type=float, default=1.0)
    p.add_argument("--A", type=float, default=1e-4)
    p.add_argument("--sigma", type=float, default=0.05)
    p.add_argument("--dt", type=float, default=0.005)
    p.add_argument("--steps", type=int, default=4000)
    p.add_argument("--thresh_frac", type=float, default=1e-6)
    p.add_argument("--tag", type=str, default="KG-cone-v1")
    args = p.parse_args()
    spec = ConeSpec(N=args.N, L=args.L, c=args.c, m=args.m, A=args.A, sigma=args.sigma, dt=args.dt, steps=args.steps, thresh_frac=args.thresh_frac, tag=args.tag)
    out = run_light_cone(spec)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
