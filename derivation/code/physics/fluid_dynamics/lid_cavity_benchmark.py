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

import os, json, time, argparse, shutil
import numpy as np
import matplotlib.pyplot as plt

# Ensure repo root on sys.path for absolute import 'Prometheus_FUVDM.*'; else fall back to file import
import sys, pathlib, importlib.util, os
_P = pathlib.Path(__file__).resolve()
for _anc in [_P] + list(_P.parents):
    if _anc.name == "Prometheus_FUVDM":
        _ROOT = str(_anc.parent)
        if _ROOT not in sys.path:
            sys.path.insert(0, _ROOT)
        break

try:
    from Prometheus_FUVDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig  # noqa: E402
except Exception:
    # Fallback: load lbm2d.py directly by file path (no package/module requirement)
    _lbm_path = os.path.join(os.path.dirname(__file__), "fluids", "lbm2d.py")
    spec = importlib.util.spec_from_file_location("lbm2d_local", _lbm_path)
    _m = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(_m)
    LBM2D = _m.LBM2D
    LBMConfig = _m.LBMConfig

# Dimensionless helpers (LBM units)
try:
    from Prometheus_FUVDM.derivation.code.common.dimensionless_fuvdm import (
        lbm_viscosity_from_tau, reynolds_lbm, mach_lbm
    )
except Exception:
    lbm_viscosity_from_tau = lambda tau: (float(tau) - 0.5) / 3.0
    def reynolds_lbm(U, L, tau):
        return float(U) * float(L) / (lbm_viscosity_from_tau(tau) + 1e-15)
    def mach_lbm(U):
        return float(U) / (1.0 / np.sqrt(3.0))


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
    # Void dynamics exposure
    ap.add_argument("--void_domain", type=str, default="standard_model", help="FUVDM domain modulation preset")
    ap.add_argument("--void_gain", type=float, default=0.5, help="gain for ω_eff = ω0/(1+g|ΔW|)")
    ap.add_argument("--void_enabled", action="store_true", help="enable FUVDM-stabilized collision")
    ap.add_argument("--u_clamp", type=float, default=0.05, help="max |u| clamp (Ma control); set small (e.g., 0.02) to suppress spikes")
    args = ap.parse_args()

    cfg = LBMConfig(
        nx=args.nx, ny=args.ny, tau=args.tau,
        periodic_x=False, periodic_y=False,
        void_enabled=bool(args.void_enabled),
        void_domain=str(args.void_domain),
        void_gain=float(args.void_gain),
        rho_floor=1e-9,
        u_clamp=float(args.u_clamp)
    )
    sim = LBM2D(cfg)
    # Use Zou/He velocity BC at the top (fluid), bounce-back on the other three walls
    sim.set_solid_box(top=False, bottom=True, left=True, right=True)

    # Report nondimensional numbers (LBM units)
    L_eff = max(1, int(args.ny) - 1)
    nu = float(lbm_viscosity_from_tau(args.tau))
    Re = float(reynolds_lbm(args.U_lid, L_eff, args.tau))
    Ma = float(mach_lbm(args.U_lid))
    print(f"[bench] L={L_eff}, nu={nu:.6f}, Re={Re:.2f}, Ma={Ma:.4f}")
    if Ma >= 0.1:
        print("[bench][warn] Ma >= 0.1; BGK low-Mach polynomial may be inaccurate/unstable.")

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
    # Precompute flow strength for gating
    sim.moments()
    _ux = np.nan_to_num(sim.ux, nan=0.0, posinf=0.0, neginf=0.0)
    _uy = np.nan_to_num(sim.uy, nan=0.0, posinf=0.0, neginf=0.0)
    _Vmag = np.hypot(_ux, _uy)
    u_max = float(np.nanmax(_Vmag)) if _Vmag.size else 0.0
    u_mean = float(np.nanmean(_Vmag)) if _Vmag.size else 0.0
    flow_gate = (np.isfinite(u_max) and (u_max >= max(1e-9, 0.05*abs(args.U_lid))))
    passed = bool(np.isfinite(div_max) and div_max <= 1e-6 and flow_gate)
    # Route outputs: failed runs go to .../failed_runs/, passes to base dirs
    out_fig_dir = fig_dir if passed else os.path.join(fig_dir, "failed_runs")
    out_log_dir = log_dir if passed else os.path.join(log_dir, "failed_runs")
    os.makedirs(out_fig_dir, exist_ok=True)
    os.makedirs(out_log_dir, exist_ok=True)
    figure_path = os.path.join(out_fig_dir, f"{script_name}_{tstamp}.png")
    log_path = os.path.join(out_log_dir, f"{script_name}_{tstamp}.json")

    # Figure: velocity magnitude and (optional) streamlines
    # Refresh macroscopic fields for plotting
    sim.moments()
    # Figure: velocity magnitude and (optional) streamlines
    X, Y = np.meshgrid(np.arange(args.nx), np.arange(args.ny))
    ux = np.nan_to_num(sim.ux, nan=0.0, posinf=0.0, neginf=0.0)
    uy = np.nan_to_num(sim.uy, nan=0.0, posinf=0.0, neginf=0.0)
    Vmag = np.hypot(ux, uy)
    vmax = np.nanpercentile(Vmag, 99.0)
    if (not np.isfinite(vmax)) or vmax <= 0.0:
        vmax = float(np.nanmax(Vmag)) if np.isfinite(np.nanmax(Vmag)) else 1e-12
    u_max = float(np.nanmax(Vmag)) if np.isfinite(np.nanmax(Vmag)) else 0.0
    u_mean = float(np.nanmean(Vmag)) if np.isfinite(np.nanmean(Vmag)) else 0.0
    if (not np.isfinite(u_max)) or u_max <= 1e-9:
        print("[warn] |u| too small or NaN; figure may look blank")
    plt.figure(figsize=(6, 5))
    im = plt.imshow(Vmag, origin="lower", cmap="viridis", vmin=0.0, vmax=vmax)
    plt.colorbar(im, label="|u|")
    try:
        # Streamplot on transposed fields to match coordinate orientation
        plt.streamplot(X.T, Y.T, ux.T, uy.T, density=1.0, color="w", linewidth=0.6)
    except Exception:
        pass
    plt.title(f"Lid-driven cavity (U_lid={args.U_lid}, tau={args.tau}, warmup={args.warmup}, div_max={div_max:.2e})")
    plt.tight_layout()
    plt.savefig(figure_path, dpi=140)
    plt.close()

    payload = {
        "theory": "LBM→NS; incompressible cavity with no-slip walls (bounce-back) + FUVDM ω_eff (optional)",
        "params": {
            "nx": int(args.nx), "ny": int(args.ny), "tau": float(args.tau), "U_lid": float(args.U_lid),
            "steps": int(args.steps), "sample_every": int(args.sample_every),
            "void_enabled": bool(args.void_enabled), "void_domain": str(args.void_domain), "void_gain": float(args.void_gain)
        },
        "metrics": {
            "div_max": float(div_max),
            "elapsed_sec": float(elapsed),
            "u_max": float(u_max),
            "u_mean": float(u_mean),
            "flow_gate": bool(flow_gate),
            "Re": float(Re),
            "Ma": float(Ma),
            "nu": float(nu),
            "passed": passed,
            # Void diagnostics (present even if disabled; fallback values reasonable)
            "void": {
                "dW_max": float(getattr(sim, "aggr_dW_max", 0.0)),
                "omega_min": float(getattr(sim, "aggr_omega_min", 0.0)),
                "omega_max": float(getattr(sim, "aggr_omega_max", 0.0)),
                "W_mean_last": float(getattr(sim, "last_W_mean", 0.0))
            }
        },
        "outputs": {"figure": figure_path},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()