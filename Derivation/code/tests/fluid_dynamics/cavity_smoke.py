#!/usr/bin/env python3
import os, sys, time, json
import numpy as np

# Ensure repo root on sys.path for absolute import 'Prometheus_VDM.*'
import pathlib
_P = pathlib.Path(__file__).resolve()
for _anc in [_P] + list(_P.parents):
    if _anc.name == "Prometheus_VDM":
        _ROOT = str(_anc.parent)
        if _ROOT not in sys.path:
            sys.path.insert(0, _ROOT)
        break

from Prometheus_VDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig, VOID_SOURCE, universal_void_dynamics

def run(nx=64, ny=64, tau=0.9, U=0.02, steps=1200, warmup=500, sample_every=200, void_enabled=True, void_gain=1.0, void_domain="standard_model"):
    cfg = LBMConfig(
        nx=nx, ny=ny, tau=tau,
        periodic_x=False, periodic_y=False,
        void_enabled=bool(void_enabled),
        void_gain=float(void_gain),
        void_domain=str(void_domain),
        rho_floor=1e-9,
        u_clamp=0.1
    )
    sim = LBM2D(cfg)
    # North/top is fluid row (y=0); other three walls are solid
    sim.set_solid_box(top=False, bottom=True, left=True, right=True)

    div_hist = []
    t0 = time.time()
    for n in range(steps + 1):
        sim.step(1)
        sim.set_lid_velocity(U)
        if (n >= warmup) and ((n - warmup) % sample_every == 0):
            sim.moments()
            d = sim.divergence()
            div_hist.append(float(d))
            print(f"step={n}, div={d:.3e}, W_mean={getattr(sim, 'last_W_mean', np.nan):.3f}, "
                  f"omega_min={getattr(sim, 'aggr_omega_min', np.nan):.3f}, omega_max={getattr(sim, 'aggr_omega_max', np.nan):.3f}", flush=True)

    elapsed = time.time() - t0
    div_max = float(np.max(div_hist)) if div_hist else float("nan")
    # pass/fail decision for routing (same threshold as benchmark)
    passed = (np.isfinite(div_max) and div_max <= 1e-6)

    payload = {
        "void_banner": {
            "loaded": bool(universal_void_dynamics is not None),
            "source": str(VOID_SOURCE)
        },
        "params": {
            "nx": nx, "ny": ny, "tau": tau, "U_lid": U,
            "steps": steps, "sample_every": sample_every,
            "void_enabled": bool(void_enabled), "void_gain": float(void_gain), "void_domain": str(void_domain)
        },
        "metrics": {
            "div_max": div_max,
            "elapsed_sec": float(elapsed),
            "passed": passed,
            "void": {
                "dW_max": float(getattr(sim, "aggr_dW_max", 0.0)),
                "omega_min": float(getattr(sim, "aggr_omega_min", 0.0)),
                "omega_max": float(getattr(sim, "aggr_omega_max", 0.0)),
                "W_mean_last": float(getattr(sim, "last_W_mean", 0.0))
            }
        }
    }
    print(json.dumps(payload, indent=2))
    # Persist under the fluids logs folder (failed → failed_runs/)
    base_outdir = os.path.join("Prometheus_VDM","derivation","code","outputs")
    base_log_dir = os.path.join(base_outdir, "logs", "fluid_dynamics")
    out_log_dir = base_log_dir if passed else os.path.join(base_log_dir, "failed_runs")
    os.makedirs(out_log_dir, exist_ok=True)
    fname = f"cavity_smoke_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
    with open(os.path.join(out_log_dir, fname), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

if __name__ == "__main__":
    run()