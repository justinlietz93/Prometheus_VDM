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
from physics.reaction_diffusion.reaction_exact import logistic_invariant_Q, reaction_exact_step

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


def lyapunov_monitor(N: int, dx: float, D: float, r: float, ucoef: float, dt: float, steps: int, seed: int, stepper=None) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    W = rng.random(N).astype(float) * 0.1
    series = []
    L_prev = discrete_lyapunov_Lh(W, dx, D, r, ucoef)
    for k in range(steps):
        if stepper is None:
            lap = laplacian_periodic_1d(W, dx)
            W = W + dt * (r * W - ucoef * W * W + D * lap)
        else:
            W_prev = W.copy()
            W = stepper(W, dt, dx, D, r, ucoef)
            # If DG RD, compute identity residuals for certification
            if stepper is dg_rd_step:
                mid = 0.5 * (W + W_prev)
                over_f = r * (W_prev + 0.5 * (W - W_prev)) - ucoef * ((W_prev * W_prev + W_prev * W + W * W) / 3.0)
                G = D * laplacian_periodic_1d(mid, dx) + over_f
                # Energy identity residuals
                id_res_energy = (discrete_lyapunov_Lh(W, dx, D, r, ucoef) - L_prev) / dt + float(np.sum(G * G) * dx)
                id_res_dot = (discrete_lyapunov_Lh(W, dx, D, r, ucoef) - L_prev) - float(np.sum(G * (W - W_prev)) * dx)
                grad_norm_sq = float(np.sum(G * G) * dx)
            else:
                id_res_energy = None
                id_res_dot = None
                grad_norm_sq = None
        L_now = discrete_lyapunov_Lh(W, dx, D, r, ucoef)
        entry = {"step": k + 1, "delta_L": float(L_now - L_prev), "L": float(L_now)}
        if stepper is dg_rd_step:
            entry.update({"dg_identity_energy_res": id_res_energy, "dg_identity_dot_res": id_res_dot, "dg_grad_norm_sq": grad_norm_sq})
        series.append(entry)
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
        f.write("step,delta_L,L,dg_grad_norm_sq,dg_identity_energy_res,dg_identity_dot_res\n")
        for s in series:
            f.write(f"{s['step']},{s['delta_L']},{s['L']},{s.get('dg_grad_norm_sq','')},{s.get('dg_identity_energy_res','')},{s.get('dg_identity_dot_res','')}\n")
    return {"series": series, "figure": str(fig_path), "failed": failed_gate, "violations": violations, "tol_pos": tol_pos}


def rd_euler_step(W: np.ndarray, dt: float, dx: float, D: float, r: float, ucoef: float) -> np.ndarray:
    lap = laplacian_periodic_1d(W, dx)
    return W + dt * (r * W - ucoef * W * W + D * lap)


def diffusion_CN_step_periodic(W: np.ndarray, dt: float, dx: float, D: float) -> np.ndarray:
    """Crank–Nicolson diffusion half/whole step via spectral diagonalization (periodic)."""
    if D == 0.0 or dt == 0.0:
        return W.copy()
    N = W.size
    k = np.fft.fftfreq(N, d=dx)  # cycles per unit length
    # Symbol of discrete Laplacian: lambda = -4 sin^2(pi k dx)/(dx^2)
    theta = 2.0 * np.pi * k * dx
    lam = -4.0 * (np.sin(0.5 * theta) ** 2) / (dx * dx)
    alpha = 0.5 * dt * D
    G = (1.0 + alpha * lam) / (1.0 - alpha * lam)
    W_hat = np.fft.fft(W)
    Wn1_hat = G * W_hat
    Wn1 = np.fft.ifft(Wn1_hat).real
    return Wn1


def strang_step(W: np.ndarray, dt: float, dx: float, D: float, r: float, ucoef: float) -> np.ndarray:
    """Strang split: 1/2 diffusion (CN), exact reaction, 1/2 diffusion (CN)."""
    W_half = diffusion_CN_step_periodic(W, 0.5 * dt, dx, D)
    W_react = reaction_exact_step(W_half, r, ucoef, dt)
    W_out = diffusion_CN_step_periodic(W_react, 0.5 * dt, dx, D)
    return W_out


def dg_rd_step(Wn: np.ndarray, dt: float, dx: float, D: float, r: float, u: float, tol: float = 1e-12, max_iter: int = 20) -> np.ndarray:
    """Discrete-gradient RD implicit step (AVF for reaction, midpoint Laplacian), Newton solve (dense)."""
    N = Wn.size
    W1 = Wn.copy()
    def lap(x):
        return laplacian_periodic_1d(x, dx)
    for it in range(max_iter):
        mid = 0.5 * (W1 + Wn)
        # overline f (AVF) for logistic: r*(Wn + 0.5*(W1-Wn)) - u*((Wn^2 + Wn W1 + W1^2)/3)
        dW = (W1 - Wn)
        over_f = r * (Wn + 0.5 * dW) - u * ((Wn * Wn + Wn * W1 + W1 * W1) / 3.0)
        F = W1 - Wn - dt * (D * lap(mid) + over_f)
        res = np.linalg.norm(F, ord=np.inf)
        if res <= tol:
            break
        # Build dense Jacobian: I - dt*(0.5 D L + 0.5 r I - u*(Wn/3 + 2/3 W1) I)
        # Laplacian linear operator with periodic stencil
        J = np.eye(N)
        # Add - dt * 0.5 D L
        coeff = - dt * 0.5 * D / (dx * dx)
        for i in range(N):
            J[i, i] += - coeff * (-2.0)
            J[i, (i - 1) % N] += - coeff * (1.0)
            J[i, (i + 1) % N] += - coeff * (1.0)
        # Add - dt * (0.5 r I - u*(Wn/3 + 2/3 W1) I)
        diag_add = - dt * (0.5 * r - u * (Wn / 3.0 + (2.0 / 3.0) * W1))
        J[np.arange(N), np.arange(N)] += diag_add
        d = np.linalg.solve(J, -F)
        W1 = W1 + d
        if np.linalg.norm(d, ord=np.inf) <= tol * 0.1:
            break
    return W1


def dg_rd_step_with_stats(Wn: np.ndarray, dt: float, dx: float, D: float, r: float, u: float,
                          tol: float = 1e-12, max_iter: int = 20, max_backtracks: int = 10,
                          lap_operator: str = "stencil") -> tuple[np.ndarray, Dict[str, Any]]:
    """DG RD step with Newton iteration stats and simple backtracking line search.

    lap_operator: 'stencil' (3-pt periodic) or 'spectral' (FFT-based circulant). Default 'stencil'.
    """
    N = Wn.size
    W1 = Wn.copy()
    stats = {"iters": 0, "final_residual_inf": None, "backtracks": 0, "converged": False}
    # Prepare Laplacian operator according to mode
    lap_mode = str(lap_operator or "stencil").lower()
    if lap_mode == "spectral":
        N = Wn.size
        k_cyc = np.fft.fftfreq(N, d=dx)
        omega_sq = (2.0 * np.pi) ** 2 * (k_cyc ** 2)
        lam_spec = - omega_sq  # symbol for ∂xx
        # Dense circulant matrix of spectral Laplacian (real)
        kernel = np.fft.ifft(lam_spec).real
        C_spec = np.empty((N, N), dtype=float)
        for i in range(N):
            C_spec[i, :] = np.roll(kernel, i)
        def lap(x):
            # Use dense circulant for consistency with Jacobian
            return C_spec @ x
    else:
        C_spec = None
        def lap(x):
            return laplacian_periodic_1d(x, dx)
    prev_res = None
    for it in range(1, max_iter + 1):
        mid = 0.5 * (W1 + Wn)
        dW = (W1 - Wn)
        over_f = r * (Wn + 0.5 * dW) - u * ((Wn * Wn + Wn * W1 + W1 * W1) / 3.0)
        F = W1 - Wn - dt * (D * lap(mid) + over_f)
        res = float(np.linalg.norm(F, ord=np.inf))
        if res <= tol:
            stats.update({"iters": it, "final_residual_inf": res, "converged": True})
            break
        # Build dense Jacobian
        J = np.eye(N)
        if lap_mode == "spectral":
            # Add - dt * 0.5 * D * L_spec
            J += (- dt * 0.5 * D) * C_spec
        else:
            coeff = - dt * 0.5 * D / (dx * dx)
            for i in range(N):
                J[i, i] += - coeff * (-2.0)
                J[i, (i - 1) % N] += - coeff * (1.0)
                J[i, (i + 1) % N] += - coeff * (1.0)
        diag_add = - dt * (0.5 * r - u * (Wn / 3.0 + (2.0 / 3.0) * W1))
        J[np.arange(N), np.arange(N)] += diag_add
        d = np.linalg.solve(J, -F)
        # Backtracking line search to ensure residual decrease
        step = 1.0
        W_trial = W1 + step * d
        # Evaluate residual at trial
        mid_t = 0.5 * (W_trial + Wn)
        over_f_t = r * (Wn + 0.5 * (W_trial - Wn)) - u * ((Wn * Wn + Wn * W_trial + W_trial * W_trial) / 3.0)
        F_t = W_trial - Wn - dt * (D * lap(mid_t) + over_f_t)
        res_t = float(np.linalg.norm(F_t, ord=np.inf))
        bt = 0
        while res_t > res and bt < max_backtracks:
            step *= 0.5
            W_trial = W1 + step * d
            mid_t = 0.5 * (W_trial + Wn)
            over_f_t = r * (Wn + 0.5 * (W_trial - Wn)) - u * ((Wn * Wn + Wn * W_trial + W_trial * W_trial) / 3.0)
            F_t = W_trial - Wn - dt * (D * lap(mid_t) + over_f_t)
            res_t = float(np.linalg.norm(F_t, ord=np.inf))
            bt += 1
        if bt > 0:
            stats["backtracks"] = stats.get("backtracks", 0) + bt
        W1 = W_trial
        prev_res = res
        stats.update({"iters": it, "final_residual_inf": res_t})
        if np.linalg.norm(step * d, ord=np.inf) <= tol * 0.1:
            # Step small enough
            stats["converged"] = True
            break
    return W1, stats


def fixed_dt_deltaS_comparison(N: int, dx: float, D: float, r: float, u: float, dt: float, seeds: List[int], coeffs: Dict[str, float]) -> Dict[str, Any]:
    """Produce a 1x3 panel figure comparing |ΔS| histograms at fixed dt for Euler, Strang, DG."""
    schemes = ["euler", "strang", "dg_rd"]
    steppers = {
        "euler": None,
        "strang": lambda W, dt_, dx_, D_, r_, u_: strang_step(W, dt_, dx_, D_, r_, u_),
        "dg_rd": lambda W, dt_, dx_, D_, r_, u_: dg_rd_step(W, dt_, dx_, D_, r_, u_),
    }
    summaries = {}
    combined_rows = []
    fig_path = figure_path("rd_conservation", "fixed_dt_deltaS_compare", failed=False)
    plt.figure(figsize=(12, 4))
    for idx, sch in enumerate(schemes, start=1):
        summ = objA_fixed_dt_sweep(N, dx, D, r, u, dt, seeds, coeffs, stepper=steppers[sch], scheme_label=sch)
        summaries[sch] = summ["stats"]
        for row in summ["samples"]:
            combined_rows.append({"scheme": sch, "seed": row["seed"], "abs_delta_S": abs(row["delta_S"])})
        plt.subplot(1, 3, idx)
        vals = [abs(x["delta_S"]) for x in summ["samples"]]
        plt.hist(vals, bins=20)
        plt.xlabel("|ΔS|")
        if idx == 1:
            plt.ylabel("count")
        plt.title(f"{sch} (dt={dt})")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # Logs
    logj = {"figure": str(fig_path), "dt": float(dt), "summaries": summaries}
    write_log(log_path("rd_conservation", "fixed_dt_deltaS_compare", failed=False), logj)
    csv_path = log_path("rd_conservation", "fixed_dt_deltaS_compare", failed=False, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("scheme,seed,abs_delta_S\n")
        for rrow in combined_rows:
            f.write(f"{rrow['scheme']},{rrow['seed']},{rrow['abs_delta_S']}\n")
    return logj


def residuals_H0_Q_logistic(W0: np.ndarray, W1: np.ndarray, dt: float, r: float, ucoef: float, t0: float) -> np.ndarray:
    # Legacy metric (kept for reference): reaction-only invariant residual; not used in Obj-A/B
    Q0 = logistic_invariant_Q(W0, r, ucoef, t0)
    Q1 = logistic_invariant_Q(W1, r, ucoef, t0 + dt)
    return (Q1 - Q0)


def objA_objB_sweeps(N: int, dx: float, D: float, r: float, ucoef: float, dt_list: List[float], seeds: List[int], scheme: str, order_p: int, expected_dt_slope: float) -> tuple[Dict[str, Any], Dict[str, Any]]:
    # Richardson two-grid error on the same stepper under test
    def step_fn(W: np.ndarray, dt: float) -> np.ndarray:
        s = scheme.lower()
        if s == "euler":
            return rd_euler_step(W, dt, dx, D, r, ucoef)
        elif s == "strang":
            return strang_step(W, dt, dx, D, r, ucoef)
        elif s == "dg_rd":
            return dg_rd_step(W, dt, dx, D, r, ucoef)
        else:
            return rd_euler_step(W, dt, dx, D, r, ucoef)

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
    # Determine expected slope by scheme if not explicitly provided
    if scheme.lower() == "strang":
        expected = 3.0
    elif scheme.lower() == "dg_rd":
        expected = 3.0
    else:
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


# =========================
# Obj-A CAS attempt helpers
# =========================
def _cas_build_row(Wm: float, Wi: float, Wp: float, dx: float, D: float, r: float, u: float) -> np.ndarray:
    """Build one linear equation row for unknowns [a0,a1,a2,b1,b2,b4] in L - R = 0.
    Q'(Wi) = a0 + a1 Wi + a2 Wi^2
    H_{i+1/2}(Wi,Wp) = (b1*(Wp - Wi) + b2*(Wp**2 - Wi**2) + b4*(Wi*Wp*(Wp - Wi)))
    Equation: Q'(Wi)*(r Wi - u Wi^2 + D*(Wp - 2Wi + Wm)/dx^2) = (1/dx)*(H_{i+1/2} - H_{i-1/2})
    Rearranged to coeffs dot x = 0.
    """
    lap = (Wp - 2.0 * Wi + Wm) / (dx * dx)
    Fi = (r * Wi - u * Wi * Wi) + D * lap
    # Coeffs for a0,a1,a2 from left side
    c_a0 = Fi
    c_a1 = Wi * Fi
    c_a2 = (Wi * Wi) * Fi
    # Right side terms contribute with negative sign to bring to LHS
    # H_{i+1/2}
    d1_p = (Wp - Wi)
    d2_p = (Wp * Wp - Wi * Wi)
    d4_p = (Wi * Wp * (Wp - Wi))
    # H_{i-1/2} with (Wm,Wi)
    d1_m = (Wi - Wm)
    d2_m = (Wi * Wi - Wm * Wm)
    d4_m = (Wm * Wi * (Wi - Wm))
    flux_diff = np.array([d1_p - d1_m, d2_p - d2_m, d4_p - d4_m], dtype=float) / dx
    # Move RHS to LHS: coefficients for b's are -flux_diff components
    c_b1, c_b2, c_b4 = -flux_diff[0], -flux_diff[1], -flux_diff[2]
    return np.array([c_a0, c_a1, c_a2, c_b1, c_b2, c_b4], dtype=float)


def cas_solve_linear_balance(dx: float, D: float, r: float, u: float, samples: int = 2000, seed: int = 0) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    # Sample Wi triplets well inside (0, r/u) to avoid logistic barriers
    upper = (r / u) if u != 0 else 1.0
    lo = 0.01 * upper
    hi = 0.99 * upper
    rows = []
    for _ in range(samples):
        Wm, Wi, Wp = rng.uniform(lo, hi, size=3)
        rows.append(_cas_build_row(Wm, Wi, Wp, dx, float(D), float(r), float(u)))
    A = np.vstack(rows)
    # Solve for nullspace vector minimizing ||A x|| subject to ||x||=1 via SVD
    U, s, VT = np.linalg.svd(A, full_matrices=False)
    x = VT[-1, :]
    resid = float(s[-1])
    cond = float(s[0] / (s[-1] + 1e-30)) if s[-1] > 0 else np.inf
    sol = {
        "coeffs": {"a0": float(x[0]), "a1": float(x[1]), "a2": float(x[2]), "b1": float(x[3]), "b2": float(x[4]), "b4": float(x[5])},
        "sv_min": resid,
        "sv_max": float(s[0]),
        "cond_est": cond,
        "singular_values": [float(si) for si in s.tolist()]
    }
    return sol


def Q_from_coeffs(W: np.ndarray, a0: float, a1: float, a2: float) -> np.ndarray:
    # Integrate Q'(W) = a0 + a1 W + a2 W^2 → Q(W) = a0 W + 0.5 a1 W^2 + (1/3) a2 W^3 (constant irrelevant)
    return a0 * W + 0.5 * a1 * (W ** 2) + (a2 / 3.0) * (W ** 3)


def objA_fixed_dt_sweep(N: int, dx: float, D: float, r: float, u: float, dt: float, seeds: List[int], coeffs: Dict[str, float], stepper=None, scheme_label: str = "euler") -> Dict[str, Any]:
    a0, a1, a2 = coeffs["a0"], coeffs["a1"], coeffs["a2"]
    rng = np.random.default_rng(12345)
    res = []
    for seed in seeds:
        W = np.array(np.random.default_rng(seed).random(N) * 0.1, dtype=float)
        S0 = float(np.sum(Q_from_coeffs(W, a0, a1, a2)) * dx)
        if stepper is None:
            W1 = rd_euler_step(W, dt, dx, D, r, u)
        else:
            W1 = stepper(W, dt, dx, D, r, u)
        S1 = float(np.sum(Q_from_coeffs(W1, a0, a1, a2)) * dx)
        res.append({"seed": int(seed), "delta_S": float(S1 - S0)})
    deltas = [abs(x["delta_S"]) for x in res]
    stats = {
        "dt": float(dt),
        "max_abs_delta_S": float(np.max(deltas)),
        "median_abs_delta_S": float(np.median(deltas)),
        "mean_abs_delta_S": float(np.mean(deltas)),
        "N": N,
        "dx": dx,
        "D": D,
        "r": r,
        "u": u
    }
    # Figure: histogram of |ΔS|
    failed_gate = bool(stats["max_abs_delta_S"] > 1e-12)
    fig_path = figure_path("rd_conservation", "objA_fixed_dt_abs_deltaS_hist", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.hist(deltas, bins=20)
    plt.xlabel("|ΔS|"); plt.ylabel("count")
    plt.title(f"Obj-A fixed-dt |ΔS| (dt={dt}, scheme={scheme_label})")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # Logs
    summary = {"figure": str(fig_path), "stats": stats, "samples": res, "failed": failed_gate, "scheme": scheme_label}
    write_log(log_path("rd_conservation", "objA_fixed_dt_summary", failed=failed_gate), summary)
    csv_path = log_path("rd_conservation", "objA_fixed_dt_abs_deltaS", failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("seed,abs_delta_S\n")
        for x in res:
            f.write(f"{x['seed']},{abs(x['delta_S'])}\n")
    return summary


def euler_Q_drift_scaling_vs_dt(N: int, dx: float, D: float, r: float, u: float, dt_list: List[float], seeds: List[int], coeffs: Dict[str, float]) -> Dict[str, Any]:
    """Measure |ΔS| vs dt under one Euler RD step using CAS-derived Q; aggregate by median across seeds.

    Expect slope ≈ 2 for Euler (O(dt^2) change of nonlinear invariants at one step).
    """
    a0, a1, a2 = coeffs["a0"], coeffs["a1"], coeffs["a2"]
    def S_of(W: np.ndarray) -> float:
        return float(np.sum(Q_from_coeffs(W, a0, a1, a2)) * dx)

    dt_vals = [float(d) for d in dt_list]
    med_abs_dS: List[float] = []
    for dt in dt_vals:
        per_seed: List[float] = []
        for seed in seeds:
            rng = np.random.default_rng(seed)
            W = rng.random(N).astype(float) * 0.1
            S0 = S_of(W)
            W1 = rd_euler_step(W, dt, dx, D, r, u)
            S1 = S_of(W1)
            per_seed.append(abs(S1 - S0))
        med_abs_dS.append(float(np.median(per_seed)))

    # Fit slope on log-log
    eps = 1e-30
    x = np.log(np.array(dt_vals, dtype=float))
    y = np.log(np.array(med_abs_dS, dtype=float) + eps)
    A = np.vstack([x, np.ones_like(x)]).T
    coeff, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, b = coeff
    y_pred = A @ coeff
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    # Gate and routing
    expected = 2.0
    slope_ok = float(slope) >= (expected - 0.1)
    R2_ok = float(R2) >= 0.999
    failed_gate = not (slope_ok and R2_ok)

    fig_path = figure_path("rd_conservation", "euler_deltaS_vs_dt", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_vals, med_abs_dS, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("median |ΔS| (one Euler step)")
    plt.title(f"Euler RD: |ΔS| vs dt (slope≈{float(slope):.3f}, R2≈{float(R2):.4f})")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()

    caption = {
        "figure": str(fig_path),
        "dt": dt_vals,
        "median_abs_deltaS": med_abs_dS,
        "fit": {"slope": float(slope), "R2": float(R2)},
        "expected_slope": expected,
        "failed": failed_gate
    }
    write_log(log_path("rd_conservation", "euler_deltaS_vs_dt", failed=failed_gate), caption)
    csv_path = log_path("rd_conservation", "euler_deltaS_vs_dt", failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,median_abs_deltaS\n")
        for d, s in zip(dt_vals, med_abs_dS):
            f.write(f"{d},{s}\n")
    return caption


def main():
    parser = argparse.ArgumentParser(description="RD Conservation Harness")
    parser.add_argument("--spec", type=str, default=str(Path(__file__).resolve().parent / "step_spec.example.json"), help="Path to step_spec.json")
    parser.add_argument("--scheme", type=str, default=None, help="Override scheme in spec: euler|strang|dg_rd")
    args = parser.parse_args()
    spec_path = Path(args.spec)
    spec = StepSpec(**json.loads(spec_path.read_text()))
    if args.scheme:
        spec.scheme = args.scheme

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
    # Choose stepper for Lyapunov if non-Euler
    stepper = None
    if spec.scheme.lower() == "strang":
        stepper = lambda W, dt, dx_, D_, r_, u_: strang_step(W, dt, dx_, D_, r_, u_)
    elif spec.scheme.lower() == "dg_rd":
        stepper = lambda W, dt, dx_, D_, r_, u_: dg_rd_step_with_stats(W, dt, dx_, D_, r_, u_)[0]
    lyap = lyapunov_monitor(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), min(spec.dt_sweep), steps=50, seed=123, stepper=stepper)
    write_log(log_path("rd_conservation", "lyapunov_series", failed=bool(lyap.get("failed", False))), lyap)

    # Obj-A CAS attempt: linear balance class, then fixed-dt numeric sweep
    cas = cas_solve_linear_balance(dx, D, float(spec.params["r"]), float(spec.params["u"]), samples=4000, seed=7)
    # Log CAS singular values and candidate coefficients
    rel_sv = (cas["sv_min"] / cas["sv_max"]) if cas.get("sv_max", 0.0) else float("inf")
    cas_log = {"cas": cas, "relative_sigma": float(rel_sv)}
    write_log(log_path("rd_conservation", "objA_cas_linear_balance", failed=False), cas_log)

    # Numeric fixed-dt certification using the CAS-derived Q' coefficients
    coeffs = cas["coeffs"]
    dt_fixed = float(min(spec.dt_sweep))
    objA_summary = objA_fixed_dt_sweep(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), dt_fixed, seed_list, coeffs, stepper=stepper, scheme_label=spec.scheme)
    objA_pass = bool(objA_summary["stats"]["max_abs_delta_S"] <= 1e-12)
    # Emit contradiction report if Obj-A fails for this class & scheme
    if not objA_pass:
        contradiction = {
            "claim": "Exact conservation for Euler RD with polynomial Q' (≤ quadratic) and antisymmetric polynomial flux basis",
            "scheme": spec.scheme,
            "bc": spec.bc,
            "class": {
                "Q_prime": "a0 + a1 W + a2 W^2",
                "flux": "b1*(Wp-Wi)+b2*(Wp^2-Wi^2)+b4*(Wi*Wp*(Wp-Wi))"
            },
            "cas": cas,
            "relative_sigma": float(rel_sv),
            "fixed_dt_summary": objA_summary,
            "controls": {
                "diffusion_only_mass": ctrl_diff_log["passes"],
                "reaction_only_two_grid_rk4": ctrl_reac_log["passes"],
                "objB_two_grid": {"slope": sweep_dt.get("fit", {}).get("slope"), "R2": sweep_dt.get("fit", {}).get("R2"), "pass": not sweep_dt.get("failed", True)},
                "lyapunov": {"violations": lyap.get("violations", 0), "pass": not lyap.get("failed", False)}
            },
            "step_spec": spec_log,
            "timestamp": None
        }
        write_log(log_path("rd_conservation", "CONTRADICTION_REPORT", failed=True), contradiction)

    # Euler |ΔS| vs dt scaling to confirm method-induced O(dt^2) drift
    euler_scaling = euler_Q_drift_scaling_vs_dt(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), [float(d) for d in spec.dt_sweep], seed_list, coeffs)
    # Fixed-dt |ΔS| comparison across Euler/Strang/DG
    fixed_dt_compare = fixed_dt_deltaS_comparison(N, dx, D, float(spec.params["r"]), float(spec.params["u"]), dt_fixed, seed_list, coeffs)

    print(json.dumps({
        "controls_diffusion": ctrl_diff_log["passes"],
        "controls_reaction": ctrl_reac_log["passes"],
        "cfl_ok": bool(cfl_ok),
        "objA_samples": len(sweep_exact.get("samples", [])),
        "objB_fit_slope": sweep_dt.get("fit", {}).get("slope"),
        "objB_fit_R2": sweep_dt.get("fit", {}).get("R2"),
        "objB_pass": (not objAB_failed),
        "objC_series_len": len(lyap.get("series", [])),
        "objA_pass": objA_pass
    }, indent=2))


if __name__ == "__main__":
    main()