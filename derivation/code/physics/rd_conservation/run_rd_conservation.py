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
from common.io_paths import figure_path, log_path, write_log
from physics.reaction_diffusion.reaction_exact import logistic_invariant_Q

import numpy as np
import matplotlib.pyplot as plt

# Adjust sys.path so 'common' imports resolve when run as a script
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))



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
    return u + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate_reaction_rk4(u0: np.ndarray, r: float, ucoef: float, dt: float, T: float) -> tuple[np.ndarray, int]:
    """Integrate reaction-only ODE du/dt = r u - ucoef u^2 with RK4 to time T using step dt."""
    steps = max(1, int(np.ceil(T / dt)))
    u = u0.copy()
    t = 0.0
    for _ in range(steps):
        u = rk4_reaction_only_step(u, r, ucoef, dt)
        t += dt
    return u, steps


def reaction_only_two_grid_convergence(r: float, ucoef: float, W0: float, dt_list: List[float], T: float, norm: str = "inf") -> Dict[str, Any]:
    """Global two-grid error at fixed T for RK4 reaction-only; expect slope ≈ 4.

    E(dt) = || U_T(dt) - U_T(dt/2) ||, where each U_T(·) integrates from 0 to T with RK4.
    """
    err: List[float] = []
    for dt in dt_list:
        u0 = np.array([W0], dtype=float)
        U_dt, n1 = integrate_reaction_rk4(u0, r, ucoef, float(dt), T)
        U_h1, _ = integrate_reaction_rk4(u0, r, ucoef, float(dt) / 2.0, T)
        # Compare final states at T
        if norm == "inf":
            e = float(np.linalg.norm(U_dt - U_h1, ord=np.inf))
        else:
            e = float(np.linalg.norm(U_dt - U_h1))
        err.append(e)
    # Fit slope
    eps = 1e-30
    x = np.log(np.array(dt_list, dtype=float))
    y = np.log(np.array(err, dtype=float) + eps)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, intercept])
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    # Gate and artifact routing
    expected_slope = 4.0
    failed_gate = bool((slope < 3.9) or (R2 < 0.999))
    fig_path = figure_path("rd_conservation", "reaction_two_grid_convergence", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_list, err, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("||U_T(dt) - U_T(dt/2)||_∞")
    plt.title(f"RK4 reaction-only (two-grid): slope≈{slope:.3f}, R2≈{R2:.4f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()

    # Logs
    tg_log = {
        "figure": str(fig_path),
        "slope": float(slope),
        "R2": float(R2),
        "expected_slope": float(expected_slope),
        "dt": [float(d) for d in dt_list],
        "two_grid_error": [float(e) for e in err],
        "metric": "global_two_grid_reaction_rk4",
        "failed": failed_gate
    }
    tg_log_path = log_path("rd_conservation", "reaction_two_grid_convergence", failed=failed_gate)
    write_log(tg_log_path, tg_log)
    csv_path = log_path("rd_conservation", "reaction_two_grid_convergence", failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error\n")
        for d, e in zip(dt_list, err):
            f.write(f"{d},{e}\n")
    return {
        "dt": dt_list,
        "two_grid_error": err,
        "fit": {"slope": float(slope), "intercept": float(intercept), "R2": float(R2)},
        "figure": str(fig_path),
        "failed": failed_gate
    }


def reaction_only_q_invariant_convergence(r: float, ucoef: float, W0: float, dt_list: List[float], T: float) -> Dict[str, Any]:
    max_drifts: List[float] = []
    domain_violations: List[int] = []
    for dt in dt_list:
        steps = max(2, int(np.ceil(T / dt)))
        t = 0.0
        u = np.array([W0], dtype=float)
        q0 = float(np.asarray(logistic_invariant_Q(u, r, ucoef, t)).reshape(-1)[0])
        max_drift = 0.0
        viol = 0
        for _ in range(steps):
            u = rk4_reaction_only_step(u, r, ucoef, dt)
            t += dt
            # Domain check: 0 < W < r/u for Q to remain real-valued
            upper = (r / ucoef) if ucoef != 0 else np.inf
            if not (0.0 < float(u[0]) < upper):
                viol += 1
            q = float(np.asarray(logistic_invariant_Q(u, r, ucoef, t)).reshape(-1)[0])
            max_drift = max(max_drift, abs(q - q0))
        max_drifts.append(max_drift)
        domain_violations.append(viol)
    # Fit log-log slope
    eps = 1e-30
    x = np.log(np.array(dt_list, dtype=float))
    y = np.log(np.array(max_drifts, dtype=float) + eps)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    # Determine control gate and route artifacts accordingly
    expected_slope = 4.0
    failed_gate = bool(slope < 3.9)
    # Plot (figures only go to figures/)
    fig_path = figure_path("rd_conservation", "q_invariant_convergence", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_list, max_drifts, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("max |ΔQ|")
    plt.title(f"RK4 reaction-only: slope≈{slope:.3f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # Write JSON/CSV under logs/
    qi_log = {
        "figure": str(fig_path),
        "slope": float(slope),
        "order_p": 4,
        "expected_slope": float(expected_slope),
        "dt": [float(d) for d in dt_list],
        "max_abs_Q_drift": [float(m) for m in max_drifts],
        "domain_violations": [int(v) for v in domain_violations],
        "failed": failed_gate
    }
    qi_log_path = log_path("rd_conservation", "q_invariant_convergence", failed=failed_gate)
    write_log(qi_log_path, qi_log)
    csv_path = log_path("rd_conservation", "q_invariant_convergence", failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,max_abs_Q_drift,domain_violations\n")
        for d, m, v in zip(dt_list, max_drifts, domain_violations):
            f.write(f"{d},{m},{v}\n")
    return {
        "dt": dt_list,
        "max_abs_Q_drift": max_drifts,
        "domain_violations": domain_violations,
        "fit": {"slope": float(slope), "intercept": float(intercept)},
        "figure": str(fig_path),
        "failed": failed_gate
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
    # Gate: Lyapunov should be non-increasing within a small tolerance
    tol_pos = 1e-12
    violations = int(sum(1 for s in series if s["delta_L"] > tol_pos))
    failed_gate = bool(violations > 0)
    fig_path = figure_path("rd_conservation", "lyapunov_delta_per_step", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot([s["step"] for s in series], [s["delta_L"] for s in series], "o-")
    plt.axhline(0.0, color='k', linewidth=0.8)
    plt.xlabel("step"); plt.ylabel("ΔL_h")
    plt.title("Discrete Lyapunov per step (should be ≤ 0)")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # CSV companion for ΔL series — write to logs directory
    csv_path3 = log_path("rd_conservation", "lyapunov_delta_per_step", failed=failed_gate, type="csv")
    with csv_path3.open("w", encoding="utf-8") as f:
        f.write("step,delta_L,L\n")
        for s in series:
            f.write(f"{s['step']},{s['delta_L']},{s['L']}\n")
    return {"series": series, "figure": str(fig_path), "failed": failed_gate, "violations": violations, "tol_pos": tol_pos}


def rd_euler_step(W: np.ndarray, dt: float, dx: float, D: float, r: float, ucoef: float) -> np.ndarray:
    lap = laplacian_periodic_1d(W, dx)
    return W + dt * (r * W - ucoef * W * W + D * lap)


def residuals_H0_Q_logistic(W0: np.ndarray, W1: np.ndarray, dt: float, r: float, ucoef: float, t0: float) -> np.ndarray:
    # Legacy metric (kept for reference): reaction-only invariant residual; not used in Obj-A/B
    Q0 = logistic_invariant_Q(W0, r, ucoef, t0)
    Q1 = logistic_invariant_Q(W1, r, ucoef, t0 + dt)
    return (Q1 - Q0)


def objA_objB_sweeps(N: int, dx: float, D: float, r: float, ucoef: float, dt_list: List[float], seeds: List[int], scheme: str, order_p: int, expected_dt_slope: float) -> tuple[Dict[str, Any], Dict[str, Any]]:
    # Richardson two-grid error on the same stepper under test
    def step_fn(W: np.ndarray, dt: float) -> np.ndarray:
        # TODO: extend for Strang, RK, etc. when added
        return rd_euler_step(W, dt, dx, D, r, ucoef) if scheme.lower() == "euler" else rd_euler_step(W, dt, dx, D, r, ucoef)

    def two_grid_error_inf(W0: np.ndarray, dt: float) -> float:
        W_big = step_fn(W0, dt)
        W_h1 = step_fn(W0, dt / 2.0)
        W_h2 = step_fn(W_h1, dt / 2.0)
        return float(np.linalg.norm(W_big - W_h2, ord=np.inf))

    exact_samples = []  # per-seed measurements for auditing
    dt_to_errs: Dict[float, List[float]] = {float(d): [] for d in dt_list}
    for seed in seeds:
        rng = np.random.default_rng(seed)
        W = rng.random(N).astype(float) * 0.1
        for dt in dt_list:
            W0 = W.copy()
            err = two_grid_error_inf(W0, float(dt))
            exact_samples.append({"seed": int(seed), "dt": float(dt), "two_grid_error_inf": float(err)})
            dt_to_errs[float(dt)].append(float(err))

    dt_vals = sorted(dt_to_errs.keys())
    # Aggregate with median across seeds to stabilize the fit
    err_med = [float(np.median(dt_to_errs[d])) for d in dt_vals]
    eps = 1e-30
    x = np.log(np.array(dt_vals, dtype=float))
    y = np.log(np.array(err_med, dtype=float) + eps)
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
        "metric": "two_grid_error_inf",
        "samples": exact_samples
    }
    # Gate for Obj-A/B: slope near expected and good linear fit
    expected = float(expected_dt_slope)
    # V3 gate: slope >= (expected - 0.1) and R2 >= 0.999
    slope_ok = float(slope) >= (expected - 0.1)
    R2_ok = float(R2) >= 0.999
    failed_gate = not (slope_ok and R2_ok)
    write_log(log_path("rd_conservation", "sweep_exact", failed=failed_gate), sweep_exact)
    sweep_dt = {
        "scheme": scheme,
        "dt": [float(d) for d in dt_vals],
        "two_grid_error_inf_med": err_med,
        "fit": {"slope": float(slope), "R2": float(R2)},
        "expected_slope": expected,
        "failed": failed_gate
    }
    write_log(log_path("rd_conservation", "sweep_dt", failed=failed_gate), sweep_dt)
    fig_path = figure_path("rd_conservation", "residual_vs_dt", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_vals, err_med, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("max |residual|")
    plt.ylabel("two-grid error ||Φ_dt - Φ_{dt/2}∘Φ_{dt/2}||_∞")
    plt.title(f"Obj-A/B (two-grid): slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # Numeric caption/log and CSV go to logs directory (not beside figures)
    caption = {
        "slope": float(slope),
        "R2": float(R2),
        "order_p": int(order_p),
        "expected_slope": expected,
        "metric": "two_grid_error_inf_median",
        "figure": str(fig_path),
        "dt": [float(d) for d in dt_vals],
        "two_grid_error_inf_med": err_med
    }
    cap_path = log_path("rd_conservation", "residual_vs_dt", failed=failed_gate)
    write_log(cap_path, caption)
    csv_path2 = log_path("rd_conservation", "residual_vs_dt", failed=failed_gate, type="csv")
    with csv_path2.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error_inf_median\n")
        for d, e in zip(dt_vals, err_med):
            f.write(f"{d},{e}\n")
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

    # Controls — Reaction-only RK4 two-grid (expected order-4)
    q_T = 10.0
    # Safer dt_list to sit in asymptotic regime
    q_dt_list = [0.05, 0.025, 0.0125, 0.00625]
    # Safe initial condition away from logistic barriers
    r_val = float(spec.params["r"]); u_val = float(spec.params["u"])
    W0_safe = 0.2 * (r_val / u_val) if u_val != 0 else 0.1
    q_ctrl = reaction_only_two_grid_convergence(r_val, u_val, W0=W0_safe, dt_list=q_dt_list, T=q_T)
    ctrl_reac_log = {
        "control": "reaction_only_two_grid_rk4",
        "spec": {"r": r_val, "u": u_val, "dt_list": q_dt_list, "T": q_T, "W0": float(W0_safe)},
        "metrics": q_ctrl,
        "passes": {"slope_ge_3.9_and_R2_ge_0.999": (q_ctrl["fit"]["slope"] >= 3.9 and q_ctrl["fit"].get("R2", 0.0) >= 0.999)}
    }
    write_log(log_path("rd_conservation", "controls_reaction", failed=not ctrl_reac_log["passes"]["slope_ge_3.9_and_R2_ge_0.999"]), ctrl_reac_log)

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
    sweep_exact, sweep_dt = objA_objB_sweeps(
        N, dx, D,
        float(spec.params["r"]), float(spec.params["u"]),
        [float(d) for d in spec.dt_sweep], seed_list, spec.scheme,
        int(spec.order_p), float(spec.expected_dt_slope)
    )
    # Log explicit Obj-A/B gate outcome for clarity
    objAB_failed = bool(sweep_dt.get("failed", False))
    objAB_gate_log = {
        "gate": "objAB_residual_vs_dt",
        "expected_slope": float(spec.expected_dt_slope),
        "fit": sweep_dt.get("fit", {}),
        "passes": {"slope_close_and_R2": (not objAB_failed)}
    }
    write_log(log_path("rd_conservation", "objAB_gate", failed=objAB_failed), objAB_gate_log)

    # Obj-C Lyapunov
    lyap = lyapunov_monitor(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), min(spec.dt_sweep), steps=50, seed=123)
    write_log(log_path("rd_conservation", "lyapunov_series", failed=bool(lyap.get("failed", False))), lyap)

    print(json.dumps({
        "controls_diffusion": ctrl_diff_log["passes"],
        "controls_reaction": ctrl_reac_log["passes"],
        "cfl_ok": bool(cfl_ok),
        "objA_samples": len(sweep_exact.get("samples", [])),
        "objB_fit_slope": sweep_dt.get("fit", {}).get("slope"),
        "objB_fit_R2": sweep_dt.get("fit", {}).get("R2"),
        "objB_pass": (not objAB_failed),
        "objC_series_len": len(lyap.get("series", []))
    }, indent=2))


if __name__ == "__main__":
    main()