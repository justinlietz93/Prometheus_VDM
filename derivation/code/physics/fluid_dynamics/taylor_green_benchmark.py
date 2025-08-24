#!/usr/bin/env python3
"""
Taylor–Green vortex (2-D) viscosity recovery benchmark for the fluids sector.

CHANGE REASON:
- Relocated into derivation/code/physics/fluid_dynamics per repo rules (no Prometheus_FUVDM/bench/).
- Outputs follow RD harness: derivation/code/outputs/{figures,logs}.
- Ensures JSON uses native Python types (bool/float) to avoid numpy serialization issues.

Outputs (defaults):
- Figures → derivation/code/outputs/figures/<script>_<timestamp>.png
- Logs    → derivation/code/outputs/logs/<script>_<timestamp>.json
"""

import os, json, time, math, argparse
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

from Prometheus_FUVDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig, CS2  # noqa: E402


def init_taylor_green(sim: LBM2D, U0=0.05, k=2*math.pi):
    nx, ny = sim.nx, sim.ny
    x = (np.arange(nx) + 0.5) / nx
    y = (np.arange(ny) + 0.5) / ny
    X, Y = np.meshgrid(x, y)
    sim.ux[:, :] =  U0 * np.cos(k * X) * np.sin(k * Y)
    sim.uy[:, :] = -U0 * np.sin(k * X) * np.cos(k * Y)
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
    ap.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to derivation/code/outputs")
    args = ap.parse_args()

    cfg = LBMConfig(nx=args.nx, ny=args.ny, tau=args.tau, periodic_x=True, periodic_y=True)
    sim = LBM2D(cfg)
    init_taylor_green(sim, U0=args.U0, k=args.k)

    t0 = time.time()
    ts, Es = [], []
    # Adaptive sampling using correct lattice wavenumber scaling:
    # ln E(t) slope s = -2 ν k^2 (1/nx^2 + 1/ny^2)
    nu_th_est = float(sim.nu)
    nx_f = float(args.nx)
    ny_f = float(args.ny)
    k_sq = float(args.k) * float(args.k)
    lam = k_sq * ((1.0 / (nx_f * nx_f)) + (1.0 / (ny_f * ny_f)))
    rate = 2.0 * nu_th_est * lam
    se = 1 if rate > 0.5 else max(1, int(args.sample_every))
    for n in range(args.steps + 1):
        if n % se == 0:
            sim.moments()
            ts.append(float(n))
            Es.append(energy(sim.ux, sim.uy))
        sim.step(1)
    elapsed = time.time() - t0

    ts = np.asarray(ts, dtype=float)
    Es = np.asarray(Es, dtype=float)

    # Fit E(t) ~ E0 * exp(-2 ν k^2 (1/nx^2 + 1/ny^2) t) using early-time window to avoid underflow
    mask = Es > (float(Es.max()) * 1e-12)
    ts_fit = ts[mask] if np.any(mask) else ts
    Es_fit = Es[mask] if np.any(mask) else Es
    if ts_fit.size >= 3:
        slope, intercept = np.polyfit(ts_fit, np.log(Es_fit + 1e-300), 1)
    else:
        slope, intercept = np.polyfit(ts[:max(3, ts.size)], np.log(Es[:max(3, Es.size)] + 1e-300), 1)
    # Invert slope s = -2 ν k^2 (1/nx^2 + 1/ny^2) ⇒ ν_fit = -s / [2 k^2 (1/nx^2 + 1/ny^2)]
    inv = 2.0 * k_sq * ((1.0 / (nx_f * nx_f)) + (1.0 / (ny_f * ny_f)))
    nu_fit = float(-slope / inv)
    nu_th  = float(sim.nu)
    rel_err = float(abs(nu_fit - nu_th) / (abs(nu_th) + 1e-12))

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

    plt.figure(figsize=(7, 5))
    plt.semilogy(ts, Es, "o", ms=3, label="E(t) samples")
    plt.semilogy(ts, np.exp(intercept + slope * ts), "r--",
                 label=f"fit: nu_fit={nu_fit:.5f}, nu_th={nu_th:.5f}, rel_err={rel_err:.3%}")
    plt.xlabel("t (lattice)")
    plt.ylabel("E(t)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=140)
    plt.close()

# Acceptance and failed_runs routing
acceptance_rel_err = 0.05
passed = bool(rel_err <= acceptance_rel_err)
if not passed:
    # Route failing artifacts under failed_runs/
    fig_dir_failed = os.path.join(fig_dir, "failed_runs")
    log_dir_failed = os.path.join(log_dir, "failed_runs")
    os.makedirs(fig_dir_failed, exist_ok=True)
    os.makedirs(log_dir_failed, exist_ok=True)
    # Re-point output paths
    figure_path = os.path.join(fig_dir_failed, f"{script_name}_{tstamp}.png")
    log_path = os.path.join(log_dir_failed, f"{script_name}_{tstamp}.json")
    # Re-save figure into failed_runs path (generate fresh figure to ensure presence)
    plt.figure(figsize=(7, 5))
    plt.semilogy(ts, Es, "o", ms=3, label="E(t) samples")
    plt.semilogy(ts, np.exp(intercept + slope * ts), "r--",
                 label=f"fit: nu_fit={nu_fit:.5f}, nu_th={nu_th:.5f}, rel_err={rel_err:.3%}")
    plt.xlabel("t (lattice)")
    plt.ylabel("E(t)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=140)
    plt.close()
    payload = {
        "theory": "LBM→NS; Taylor–Green viscous decay E=E0 exp(-2 nu k^2 t)",
        "params": {
            "nx": int(args.nx), "ny": int(args.ny), "tau": float(args.tau), "nu_th": nu_th,
            "U0": float(args.U0), "k": float(args.k),
            "steps": int(args.steps), "sample_every": int(args.sample_every)
        },
        "metrics": {
            "nu_fit": nu_fit, "nu_th": nu_th, "rel_err": rel_err,
            "acceptance_rel_err": 0.05,
            "elapsed_sec": float(elapsed), "passed": bool(rel_err <= 0.05)
        },
        "outputs": {"figure": figure_path},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()