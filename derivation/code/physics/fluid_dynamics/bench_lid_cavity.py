#!/usr/bin/env python3
"""
Lid-driven cavity (2-D) incompressibility benchmark for the fluids sector.

CHANGE REASON:
- Implements benchmark from TODO_up_next plan to certify LBM→NS reduction.
- Writes figure + JSON metrics with 'passed' gate, mirroring RD harness style.

Outputs:
- Figures → assets/figures/lid_cavity.png
- Logs    → logs/fluids/lid_cavity.json
"""

import os, json, time, argparse
import numpy as np
import matplotlib.pyplot as plt

# Ensure repo root on sys.path for direct script execution
import sys, pathlib
ROOT = str(pathlib.Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Prometheus_FUVDM.fluids.lbm2d import LBM2D, LBMConfig


def main():
    ap = argparse.ArgumentParser(description="Lid-driven cavity incompressibility (LBM→NS).")
    ap.add_argument("--nx", type=int, default=128)
    ap.add_argument("--ny", type=int, default=128)
    ap.add_argument("--tau", type=float, default=0.7, help="Relaxation time (nu = cs^2*(tau-0.5))")
    ap.add_argument("--U_lid", type=float, default=0.1)
    ap.add_argument("--steps", type=int, default=15000)
    ap.add_argument("--sample_every", type=int, default=200)
    ap.add_argument("--outdir", type=str, default="Prometheus_FUVDM")
    args = ap.parse_args()

    cfg = LBMConfig(nx=args.nx, ny=args.ny, tau=args.tau, periodic_x=False, periodic_y=False)
    sim = LBM2D(cfg)
    sim.set_solid_box(top=True, bottom=True, left=True, right=True)

    figdir = os.path.join(args.outdir, "assets/figures")
    logdir = os.path.join(args.outdir, "logs/fluids")
    os.makedirs(figdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)
    figpath = os.path.join(figdir, "lid_cavity.png")
    logpath = os.path.join(logdir, "lid_cavity.json")

    t0 = time.time()
    div_hist = []
    for n in range(args.steps + 1):
        # apply moving lid velocity at the top boundary (approx Zou/He) after streaming/collision cycles
        sim.set_lid_velocity(args.U_lid)
        sim.step(1)
        if n % args.sample_every == 0:
            sim.moments()
            div_hist.append(sim.divergence())

    elapsed = time.time() - t0
    div_hist = np.asarray(div_hist, float)
    div_max  = float(np.max(div_hist))
    passed = (div_max <= 1e-6)  # threshold for double precision; tune as needed

    # Figure (velocity magnitude and streamlines)
    X, Y = np.meshgrid(np.arange(args.nx), np.arange(args.ny))
    Vmag = np.sqrt(sim.ux**2 + sim.uy**2)
    plt.figure(figsize=(6, 5))
    im = plt.imshow(Vmag, origin="lower", cmap="viridis")
    plt.colorbar(im, label="|u|")
    try:
        plt.streamplot(X.T, Y.T, sim.ux.T, sim.uy.T, density=1.2, color="w", linewidth=0.6)
    except Exception:
        # matplotlib streamplot can fail on degenerate fields; ignore streamlines if so
        pass
    plt.title(f"Lid-driven cavity (U_lid={args.U_lid}, tau={args.tau}, div_max={div_max:.2e})")
    plt.tight_layout()
    plt.savefig(figpath, dpi=140)
    plt.close()

    payload = {
        "theory": "LBM→NS; incompressible cavity with no-slip walls (bounce-back)",
        "params": {
            "nx": args.nx, "ny": args.ny, "tau": args.tau, "U_lid": args.U_lid,
            "steps": args.steps, "sample_every": args.sample_every
        },
        "metrics": {"div_max": div_max, "elapsed_sec": elapsed, "passed": passed},
        "outputs": {"figure": figpath},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(logpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()