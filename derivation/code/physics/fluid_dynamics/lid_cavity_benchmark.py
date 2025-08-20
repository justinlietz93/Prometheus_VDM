#!/usr/bin/env python3
"""
Lid-driven cavity (2-D) incompressibility benchmark for the fluids sector.

CHANGE REASON:
- Relocated into derivation/code/physics/fluid_dynamics per repo rules (no Prometheus_FUVDM/bench/).
- Outputs follow RD harness: derivation/code/outputs/{figures,logs}.
- Ensures JSON uses native Python types to avoid numpy serialization issues.

Outputs (defaults):
- Figures → derivation/code/outputs/figures/<script>_<timestamp>.png
- Logs    → derivation/code/outputs/logs/<script>_<timestamp>.json
"""

import os, json, time, argparse
import numpy as np
import matplotlib.pyplot as plt

# Ensure repo root on sys.path for absolute import 'Prometheus_FUVDM.*'
import sys, pathlib
_P = pathlib.Path(__file__).resolve()
for _anc in [_P] + list(_P.parents):
    if _anc.name == "Prometheus_FUVDM":
        _ROOT = str(_anc.parent)
        if _ROOT not in sys.path:
            sys.path.insert(0, _ROOT)
        break

from Prometheus_FUVDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Lid-driven cavity incompressibility (LBM→NS).")
    ap.add_argument("--nx", type=int, default=128)
    ap.add_argument("--ny", type=int, default=128)
    ap.add_argument("--tau", type=float, default=0.7, help="Relaxation time (nu = cs^2*(tau-0.5))")
    ap.add_argument("--U_lid", type=float, default=0.1)
    ap.add_argument("--steps", type=int, default=15000)
    ap.add_argument("--sample_every", type=int, default=200)
    ap.add_argument("--warmup", type=int, default=2000, help="steps to run before sampling (allow flow to settle)")
    ap.add_argument("--progress_every", type=int, default=None, help="print progress every N samples (default: sample_every)")
    ap.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to derivation/code/outputs")
    args = ap.parse_args()

    cfg = LBMConfig(nx=args.nx, ny=args.ny, tau=args.tau, periodic_x=False, periodic_y=False)
    sim = LBM2D(cfg)
    # Use Zou/He velocity BC at the top (fluid), bounce-back on the other three walls
    sim.set_solid_box(top=False, bottom=True, left=True, right=True)

    # Output routing (match RD harness)
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    tstamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures", "fluid_dynamics")
    log_dir = os.path.join(base_outdir, "logs", "fluid_dynamics")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    figure_path = os.path.join(fig_dir, f"{script_name}_{tstamp}.png")
    log_path = os.path.join(log_dir, f"{script_name}_{tstamp}.json")

    t0 = time.time()
    div_hist = []
    for n in range(args.steps + 1):
        # Collide+stream step first, then impose lid velocity on the streamed distributions (Zou/He-style)
        sim.step(1)
        sim.set_lid_velocity(float(args.U_lid))
        # Sample after warmup
        if (n >= args.warmup) and ((n - args.warmup) % args.sample_every == 0):
            sim.moments()
            d = sim.divergence()
            div_hist.append(d)
            # Console progress (prints each sample; set --progress_every to control frequency)
            progN = args.progress_every if args.progress_every is not None else args.sample_every
            if ((n - args.warmup) % max(1, int(progN))) == 0:
                print(f"step={n}, div={d:.3e}", flush=True)

    elapsed = time.time() - t0
    div_hist = np.asarray(div_hist, dtype=float)
    div_max = float(np.max(div_hist)) if div_hist.size else 0.0
    passed = bool(div_max <= 1e-6)

    # Figure: velocity magnitude and (optional) streamlines
    X, Y = np.meshgrid(np.arange(args.nx), np.arange(args.ny))
    Vmag = np.sqrt(sim.ux**2 + sim.uy**2)
    plt.figure(figsize=(6, 5))
    im = plt.imshow(Vmag, origin="lower", cmap="viridis")
    plt.colorbar(im, label="|u|")
    try:
        plt.streamplot(X, Y, sim.ux, sim.uy, density=1.0, color="w", linewidth=0.6)
    except Exception:
        pass
    plt.title(f"Lid-driven cavity (U_lid={args.U_lid}, tau={args.tau}, warmup={args.warmup}, div_max={div_max:.2e})")
    plt.tight_layout()
    plt.savefig(figure_path, dpi=140)
    plt.close()

    payload = {
        "theory": "LBM→NS; incompressible cavity with no-slip walls (bounce-back)",
        "params": {
            "nx": int(args.nx), "ny": int(args.ny), "tau": float(args.tau), "U_lid": float(args.U_lid),
            "steps": int(args.steps), "sample_every": int(args.sample_every),
        },
        "metrics": {"div_max": float(div_max), "elapsed_sec": float(elapsed), "passed": passed},
        "outputs": {"figure": figure_path},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()