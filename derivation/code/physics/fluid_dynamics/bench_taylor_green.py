#!/usr/bin/env python3
"""
Taylor–Green vortex (2-D) viscosity recovery benchmark for the fluids sector.

CHANGE REASON:
- Implements benchmark from TODO_up_next plan to certify LBM→NS reduction.
- Writes figure + JSON metrics with 'passed' gate, mirroring RD harness style.

Outputs:
- Figures → assets/figures/taylor_green.png
- Logs    → logs/fluids/taylor_green.json
"""

import os, json, time, math, argparse
import numpy as np
import matplotlib.pyplot as plt

# Ensure repo root on sys.path for direct script execution
import sys, pathlib
ROOT = str(pathlib.Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Prometheus_FUVDM.fluids.lbm2d import LBM2D, LBMConfig, CS2  # CS2 not used directly here


def init_taylor_green(sim: LBM2D, U0=0.05, k=2*math.pi):
    nx, ny = sim.nx, sim.ny
    x = (np.arange(nx)+0.5)/nx
    y = (np.arange(ny)+0.5)/ny
    X, Y = np.meshgrid(x, y)
    sim.ux[:, :] =  U0 * np.cos(k*X) * np.sin(k*Y)
    sim.uy[:, :] = -U0 * np.sin(k*X) * np.cos(k*Y)
    sim._set_equilibrium()


def energy(ux, uy):
    return 0.5 * float(np.mean(ux**2 + uy**2))


def main():
    ap = argparse.ArgumentParser(description="Taylor–Green vortex viscosity recovery (LBM→NS).")
    ap.add_argument("--nx", type=int, default=256)
    ap.add_argument("--ny", type=int, default=256)
    ap.add_argument("--tau", type=float, default=0.8, help="Relaxation time (nu = cs^2*(tau-0.5))")
    ap.add_argument("--U0", type=float, default=0.05)
    ap.add_argument("--k", type=float, default=2*math.pi)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--sample_every", type=int, default=50)
    ap.add_argument("--outdir", type=str, default="Prometheus_FUVDM")
    args = ap.parse_args()

    cfg = LBMConfig(nx=args.nx, ny=args.ny, tau=args.tau, periodic_x=True, periodic_y=True)
    sim = LBM2D(cfg)
    init_taylor_green(sim, U0=args.U0, k=args.k)

    t0 = time.time()
    ts, Es = [], []
    for n in range(args.steps + 1):
        if n % args.sample_every == 0:
            sim.moments()
            ts.append(n)
            Es.append(energy(sim.ux, sim.uy))
        sim.step(1)
    elapsed = time.time() - t0

    ts = np.asarray(ts, float)
    Es = np.asarray(Es, float)

    # Fit E(t) ~ E0 * exp(-2 nu k^2 t)
    slope, intercept = np.polyfit(ts, np.log(Es + 1e-20), 1)
    nu_fit = -slope / (2 * args.k * args.k)
    nu_th  = sim.nu
    rel_err = abs(nu_fit - nu_th) / (abs(nu_th) + 1e-12)

    figdir = os.path.join(args.outdir, "assets/figures")
    logdir = os.path.join(args.outdir, "logs/fluids")
    os.makedirs(figdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)
    figpath = os.path.join(figdir, "taylor_green.png")
    logpath = os.path.join(logdir, "taylor_green.json")

    plt.figure(figsize=(7, 5))
    plt.semilogy(ts, Es, "o", ms=3, label="E(t) samples")
    plt.semilogy(ts, np.exp(intercept + slope * ts), "r--",
                 label=f"fit: nu_fit={nu_fit:.5f}, nu_th={nu_th:.5f}, rel_err={rel_err:.3%}")
    plt.xlabel("t (lattice)")
    plt.ylabel("E(t)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figpath, dpi=140)
    plt.close()

    payload = {
        "theory": "LBM→NS; Taylor–Green viscous decay E=E0 exp(-2 nu k^2 t)",
        "params": {
            "nx": args.nx, "ny": args.ny, "tau": args.tau, "nu_th": nu_th,
            "U0": args.U0, "k": args.k,
            "steps": args.steps, "sample_every": args.sample_every
        },
        "metrics": {
            "nu_fit": nu_fit, "nu_th": nu_th, "rel_err": rel_err,
            "elapsed_sec": elapsed, "passed": rel_err <= 0.05
        },
        "outputs": {"figure": figpath},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(logpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()