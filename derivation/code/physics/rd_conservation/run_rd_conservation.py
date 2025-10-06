#!/usr/bin/env python3
"""
RD Conservation Harness (Obj-A/B/C scaffolding) — periodic BC default.

- Uses derivation/code/common/io_paths.py for logs/figures.
- Places artifacts under code/outputs/{logs,figures}/rd_conservation.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from dataclasses import dataclass
import argparse
from typing import List, Dict, Any

import numpy as np
import matplotlib.pyplot as plt

"""Adjust sys.path so 'common' imports resolve when run as a script."""
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from physics.reaction_diffusion.reaction_exact import logistic_invariant_Q


@dataclass
class StepSpec:
    bc: str
    scheme: str
    order_p: int
    expected_dt_slope: float
    grid: Dict[str, Any]
    params: Dict[str, Any]
    dt_sweep: List[float]
    seeds: int | List[int]
    safety: Dict[str, bool]
    cfl_used: bool
    adjacency: Dict[str, Any] | None = None
    notes: str | None = None


def laplacian_periodic_1d(u: np.ndarray, dx: float) -> np.ndarray:
    return (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx * dx)


def mass(u: np.ndarray, dx: float) -> float:
    return float(np.sum(u) * dx)


def diffusion_only_mass_check(N: int, dx: float, D: float, dt: float, steps: int, seed: int) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    u = rng.random(N).astype(float) * 0.1
    m0 = mass(u, dx)
    for _ in range(steps):
        lap = laplacian_periodic_1d(u, dx)
        u = u + dt * (D * lap)
    m1 = mass(u, dx)
    return {
        "N": N,
        "dx": dx,
        "D": D,
        "dt": dt,
        "steps": steps,
        "mass0": m0,
        "mass1": m1,
        "abs_delta_mass": abs(m1 - m0)
    }


def rk4_reaction_only_step(u: np.ndarray, r: float, ucoef: float, dt: float) -> np.ndarray:
    # du/dt = r u - ucoef u^2
    def f(x):
        return r * x - ucoef * x * x
    k1 = f(u)
    k2 = f(u + 0.5 * dt * k1)
    k3 = f(u + 0.5 * dt * k2)
    k4 = f(u + dt * k3)
    return u + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def reaction_only_q_invariant_convergence(r: float, ucoef: float, W0: float, dt_list: List[float], T: float) -> Dict[str, Any]:
    max_drifts: List[float] = []
    for dt in dt_list:
        steps = max(2, int(np.ceil(T / dt)))
        t = 0.0
        u = np.array([W0], dtype=float)
        q0 = float(logistic_invariant_Q(u, r, ucoef, t))
        max_drift = 0.0
        for _ in range(steps):
            u = rk4_reaction_only_step(u, r, ucoef, dt)
            t += dt
            q = float(logistic_invariant_Q(u, r, ucoef, t))
            max_drift = max(max_drift, abs(q - q0))
        max_drifts.append(max_drift)
    # Fit log-log slope
    eps = 1e-30
    x = np.log(np.array(dt_list, dtype=float))
    y = np.log(np.array(max_drifts, dtype=float) + eps)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    # Plot
    fig_path = figure_path("rd_conservation", "q_invariant_convergence", failed=False)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_list, max_drifts, "o-")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("dt")
    plt.ylabel("max |ΔQ|")
    plt.title(f"RK4 reaction-only: slope≈{slope:.3f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # Numeric caption sidecar json
    Path(str(fig_path).replace(".png", ".json")).write_text(json.dumps({
        "figure": str(fig_path),
        "slope": float(slope)
    }, indent=2))
    return {
        "dt": dt_list,
        "max_abs_Q_drift": max_drifts,
        "fit": {"slope": float(slope), "intercept": float(intercept)},
        "figure": str(fig_path)
    }


def energy_potential_Vhat(W: np.ndarray, r: float, ucoef: float) -> np.ndarray:
    # Vhat'(W) = -f(W) = -(r W - u W^2) => Vhat(W) = -(r/2) W^2 + (u/3) W^3 + C
    return -(r / 2.0) * (W ** 2) + (ucoef / 3.0) * (W ** 3)


def discrete_lyapunov_Lh(W: np.ndarray, dx: float, D: float, r: float, ucoef: float) -> float:
    # Edge-based gradient consistent with 3-point Laplacian
    diff = (np.roll(W, -1) - W) / dx
    grad_sq = diff * diff
    return float(np.sum(0.5 * D * grad_sq + energy_potential_Vhat(W, r, ucoef)) * dx)


def lyapunov_monitor(N: int, dx: float, D: float, r: float, ucoef: float, dt: float, steps: int, seed: int) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    W = rng.random(N).astype(float) * 0.1
    series = []
    L_prev = discrete_lyapunov_Lh(W, dx, D, r, ucoef)
    for k in range(steps):
        lap = laplacian_periodic_1d(W, dx)
        W = W + dt * (r * W - ucoef * W * W + D * lap)
        L_now = discrete_lyapunov_Lh(W, dx, D, r, ucoef)
        series.append({"step": k + 1, "delta_L": float(L_now - L_prev), "L": float(L_now)})
        L_prev = L_now
    fig_path = figure_path("rd_conservation", "lyapunov_delta_per_step", failed=False)
    plt.figure(figsize=(6, 4))
    plt.plot([s["step"] for s in series], [s["delta_L"] for s in series], "o-")
    plt.axhline(0.0, color='k', linewidth=0.8)
    plt.xlabel("step")
    plt.ylabel("ΔL_h")
    plt.title("Discrete Lyapunov per step (should be ≤ 0)")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    plt.close()
    return {"series": series, "figure": str(fig_path)}


def rd_euler_step(W: np.ndarray, dt: float, dx: float, D: float, r: float, ucoef: float) -> np.ndarray:
    lap = laplacian_periodic_1d(W, dx)
    return W + dt * (r * W - ucoef * W * W + D * lap)


def residuals_H0_Q_logistic(W0: np.ndarray, W1: np.ndarray, dt: float, r: float, ucoef: float, t0: float) -> np.ndarray:
    Q0 = logistic_invariant_Q(W0, r, ucoef, t0)
    Q1 = logistic_invariant_Q(W1, r, ucoef, t0 + dt)
    return (Q1 - Q0)


def objA_objB_sweeps(N: int, dx: float, D: float, r: float, ucoef: float, dt_list: List[float], seeds: List[int], scheme: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
    exact_samples = []
    dt_residual_max = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        W = rng.random(N).astype(float) * 0.1
        for dt in dt_list:
            W0 = W.copy()
            W1 = rd_euler_step(W0, dt, dx, D, r, ucoef) if scheme.lower() == "euler" else rd_euler_step(W0, dt, dx, D, r, ucoef)
            res = residuals_H0_Q_logistic(W0, W1, dt, r, ucoef, t0=0.0)
            max_abs = float(np.max(np.abs(res)))
            mean_abs = float(np.mean(np.abs(res)))
            exact_samples.append({"seed": int(seed), "dt": float(dt), "max_abs_residual": max_abs, "mean_abs_residual": mean_abs})
            dt_residual_max.append((dt, max_abs))
    dt_vals = sorted(set([d for d, _ in dt_residual_max]))
    dt_to_res = {d: [] for d in dt_vals}
    for d, rmax in dt_residual_max:
        dt_to_res[d].append(rmax)
    dt_max = [float(d) for d in dt_vals]
    res_max = [float(max(dt_to_res[d])) for d in dt_vals]
    x = np.log(np.array(dt_max, dtype=float))
    y = np.log(np.array(res_max, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T
    coeff, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, b = coeff
    y_pred = A @ coeff
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    sweep_exact = {
        "scheme": scheme,
        "bc": "periodic",
        "params": {"N": N, "dx": dx, "D": D, "r": r, "u": ucoef},
        "samples": exact_samples
    }
    write_log(log_path("rd_conservation", "sweep_exact", failed=False), sweep_exact)
    sweep_dt = {
        "scheme": scheme,
        "dt": dt_max,
        "max_abs_residual": res_max,
        "fit": {"slope": float(slope), "R2": float(R2)}
    }
    write_log(log_path("rd_conservation", "sweep_dt", failed=False), sweep_dt)
    fig_path = figure_path("rd_conservation", "residual_vs_dt", failed=False)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_max, res_max, "o-")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("dt")
    plt.ylabel("max |residual|")
    plt.title(f"Obj-A/B baseline H=0: slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    Path(str(fig_path).replace(".png", ".json")).write_text(json.dumps({"slope": float(slope), "R2": float(R2), "figure": str(fig_path)}, indent=2))
    return sweep_exact, sweep_dt


def main():
    parser = argparse.ArgumentParser(description="RD Conservation Harness")
    parser.add_argument("--spec", type=str, default=str(Path(__file__).resolve().parent / "step_spec.example.json"), help="Path to step_spec.json")
    args = parser.parse_args()
    spec_path = Path(args.spec)
    spec = StepSpec(**json.loads(spec_path.read_text()))

    # Controls — Diffusion-only mass conservation
    N = int(spec.grid["N"])
    dx = float(spec.grid["dx"])
    D = float(spec.params["D"])
    seed = 42
    dt = min(spec.dt_sweep)
    steps = 100
    ctrl_diff = diffusion_only_mass_check(N, dx, D, dt, steps, seed)
    ctrl_diff_log = {
        "control": "diffusion_only_mass",
        "spec": {
            "N": N, "dx": dx, "D": D, "dt": dt, "steps": steps,
            "bc": spec.bc, "scheme": spec.scheme
        },
        "metrics": ctrl_diff,
        "passes": {"machine_epsilon": ctrl_diff["abs_delta_mass"] < 1e-12}
    }
    write_log(log_path("rd_conservation", "controls_diffusion", failed=not ctrl_diff_log["passes"]["machine_epsilon"]), ctrl_diff_log)

    # Controls — Reaction-only Q invariant (RK4 expected order-4)
    q_T = 10.0
    q_dt_list = [0.02, 0.01, 0.005]
    q_ctrl = reaction_only_q_invariant_convergence(float(spec.params["r"]), float(spec.params["u"]), W0=0.12, dt_list=q_dt_list, T=q_T)
    ctrl_reac_log = {
        "control": "reaction_only_Q_invariant_rk4",
        "spec": {"r": spec.params["r"], "u": spec.params["u"], "dt_list": q_dt_list, "T": q_T},
        "metrics": q_ctrl,
        "passes": {"slope_ge_3.9": q_ctrl["fit"]["slope"] >= 3.9}
    }
    write_log(log_path("rd_conservation", "controls_reaction", failed=not ctrl_reac_log["passes"]["slope_ge_3.9"]), ctrl_reac_log)

    # Record step_spec for this run (as a convenience)
    cfl_thresh = (dx * dx) / (2.0 * D) if D > 0 else float("inf")
    cfl_ok = all(dt_i <= cfl_thresh for dt_i in spec.dt_sweep) if spec.scheme.lower() == "euler" else True
    spec_log = {
        "bc": spec.bc,
        "scheme": spec.scheme,
        "order_p": spec.order_p,
        "expected_dt_slope": spec.expected_dt_slope,
        "grid": spec.grid,
        "params": spec.params,
        "dt_sweep": spec.dt_sweep,
        "seeds": spec.seeds,
        "safety": spec.safety,
        "cfl_used": bool(cfl_ok),
        "cfl_threshold": None if not np.isfinite(cfl_thresh) else float(cfl_thresh),
        "adjacency": spec.adjacency,
        "notes": spec.notes
    }
    write_log(log_path("rd_conservation", "step_spec_snapshot", failed=False), spec_log)

    # Obj-A/B baseline
    seed_list = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    sweep_exact, sweep_dt = objA_objB_sweeps(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), [float(d) for d in spec.dt_sweep], seed_list, spec.scheme)

    # Obj-C Lyapunov
    lyap = lyapunov_monitor(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), min(spec.dt_sweep), steps=50, seed=123)
    write_log(log_path("rd_conservation", "lyapunov_series", failed=False), lyap)

    print(json.dumps({
        "controls_diffusion": ctrl_diff_log["passes"],
        "controls_reaction": ctrl_reac_log["passes"],
        "cfl_ok": bool(cfl_ok),
        "objA_samples": len(sweep_exact.get("samples", [])),
        "objB_fit_slope": sweep_dt.get("fit", {}).get("slope"),
        "objB_fit_R2": sweep_dt.get("fit", {}).get("R2"),
        "objC_series_len": len(lyap.get("series", []))
    }, indent=2))


if __name__ == "__main__":
    main()
