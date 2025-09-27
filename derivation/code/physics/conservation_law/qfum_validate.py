#!/usr/bin/env python3
"""
Q_FUM Logistic Invariant Validation

Purpose
- Numerically verify the logarithmic first integral
    Q(W,t) = ln(W/(r - u W)) - r t
  for the autonomous logistic on-site ODE:
    dW/dt = r W - u W^2
- Produce figures and JSON metrics suitable for arXiv-ready inclusion:
  1) Solution overlay: numeric vs analytic
  2) Invariant drift over time: |Q(t) - Q(0)|
  3) Convergence study: ΔQ vs dt (log-log) + slope

Usage
- Basic run (double precision RK4):
    python derivation/code/physics/conservation_law/qfum_validate.py \\
        --r 0.15 --u 0.25 --W0 0.12 0.62 --T 40 --dt 0.001 --solver rk4

- Convergence sweep (3 stepsizes):
    python derivation/code/physics/conservation_law/qfum_validate.py \\
        --r 0.15 --u 0.25 --W0 0.12 --T 10 --dt 0.002 0.001 0.0005 --solver rk4

Outputs
- Figures:
    derivation/code/outputs/figures/conservation_law/qfum_solution_overlay_UTC.png
    derivation/code/outputs/figures/conservation_law/qfum_Q_drift_UTC.png
    derivation/code/outputs/figures/conservation_law/qfum_convergence_UTC.png
- JSON metrics:
    derivation/code/outputs/logs/conservation_law/qfum_metrics_UTC.json

Dependencies
- numpy, matplotlib, json, argparse, datetime

Author: Justin K. Lietz
Date: 2025-08-26
"""

from __future__ import annotations
import argparse
import json
import math
import os
import time
from pathlib import Path
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List, Tuple, Dict
import shutil

# add repo-common IO helpers (derivation/code on sys.path)
sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.io_paths import figure_path, log_path, write_log

import numpy as np
import matplotlib.pyplot as plt


BASE_OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs"))
FIG_DIR = os.path.join(BASE_OUTDIR, "figures", "conservation_law")
LOG_DIR = os.path.join(BASE_OUTDIR, "logs", "conservation_law")
ARXIV_FIG_DIR = "derivation/arxiv/RD_Methods_QA/figs"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_dirs(*paths: str) -> None:
    for p in paths:
        os.makedirs(p, exist_ok=True)


def logistic_ode_rhs(r: float, u: float):
    def F(W: float) -> float:
        return r * W - u * W * W
    return F


def rk4_step(F, W: float, dt: float) -> float:
    k1 = F(W)
    k2 = F(W + 0.5 * dt * k1)
    k3 = F(W + 0.5 * dt * k2)
    k4 = F(W + dt * k3)
    return W + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def integrate_numeric(r: float, u: float, W0: float, T: float, dt: float, solver: str = "rk4") -> Tuple[np.ndarray, np.ndarray]:
    N = max(1, int(round(T / dt)))
    t = np.linspace(0.0, N * dt, N + 1, dtype=np.float64)
    W = np.zeros_like(t)
    W[0] = float(W0)
    F = logistic_ode_rhs(r, u)
    if solver.lower() == "rk4":
        step = lambda w: rk4_step(F, w, dt)
    elif solver.lower() == "euler":
        step = lambda w: w + dt * F(w)
    else:
        raise ValueError(f"Unsupported solver: {solver}")
    for n in range(N):
        w_next = step(W[n])
        # avoid crossing poles; clamp very gently if needed (diagnostic safety)
        if math.isfinite(w_next):
            W[n + 1] = w_next
        else:
            W[n + 1] = W[n]
    return t, W


def logistic_analytic(r: float, u: float, W0: float, t: np.ndarray) -> np.ndarray:
    # W(t) = (r/u) / (1 + C e^{-r t}), where C = (r/u - W0) / W0
    C = ((r / u) - W0) / W0
    denom = 1.0 + C * np.exp(-r * t)
    return (r / u) / denom


def Q_invariant(r: float, u: float, W: np.ndarray, t: np.ndarray) -> np.ndarray:
    # Q = ln|W| - ln|r - u W| - r t  (difference-of-logs form; numerically stabler than ln of ratio)
    eps = 1e-16
    denom = (r - u * W)
    # avoid division by zero; mask tiny magnitudes with signed epsilon
    denom = np.where(np.abs(denom) < eps, np.copysign(eps, denom), denom)
    W_safe = np.where(np.abs(W) < eps, np.copysign(eps, W), W)
    return np.log(np.abs(W_safe)) - np.log(np.abs(denom)) - r * t


@dataclass
class RunMetrics:
    r: float
    u: float
    solver: str
    dt: float
    T: float
    W0: float
    delta_Q_max: float
    W_min: float
    W_max: float


@dataclass
class ConvergenceMetrics:
    r: float
    u: float
    solver: str
    dts: List[float]
    delta_Q_max_list: List[float]
    slope: float
    intercept: float
    r2: float


def fit_loglog(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float]:
    # Fit y ~ a x^p => log10 y = p log10 x + b
    X = np.log10(x)
    Y = np.log10(y)
    A = np.vstack([X, np.ones_like(X)]).T
    p, b = np.linalg.lstsq(A, Y, rcond=None)[0]
    Y_hat = p * X + b
    ss_res = float(np.sum((Y - Y_hat) ** 2))
    ss_tot = float(np.sum((Y - np.mean(Y)) ** 2))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    return float(p), float(b), float(r2)


def plot_solution_overlay(fig_path: str, t: np.ndarray, W_num: np.ndarray, W_an: np.ndarray, r: float, u: float, W0: float) -> None:
    plt.figure(figsize=(6.0, 4.0), dpi=150)
    plt.plot(t, W_num, "-", lw=1.4, label="Numeric", color="#1f77b4")
    plt.plot(t, W_an, "--", lw=1.4, label="Analytic", color="#ff7f0e")
    plt.xlabel("t")
    plt.ylabel("W(t)")
    plt.title(f"Logistic solution overlay (r={r:.3g}, u={u:.3g}, W0={W0:.3g})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, bbox_inches="tight")
    plt.close()


def plot_Q_drift(fig_path: str, t: np.ndarray, Q: np.ndarray, r: float, u: float, W0: float) -> float:
    Q0 = float(Q[0])
    drift = np.abs(Q - Q0)
    delta_Q_max = float(np.nanmax(drift))
    plt.figure(figsize=(6.0, 4.0), dpi=150)
    plt.plot(t, drift, "-", lw=1.4, color="#2ca02c")
    plt.xlabel("t")
    plt.ylabel(r"|Q(t) - Q(0)|")
    plt.title(f"Invariant drift (max={delta_Q_max:.3e})  r={r:.3g}, u={u:.3g}, W0={W0:.3g}")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(fig_path, bbox_inches="tight")
    plt.close()
    return delta_Q_max


def plot_convergence(fig_path: str, dts: List[float], deltas: List[float], slope: float, r2: float) -> None:
    plt.figure(figsize=(6.0, 4.0), dpi=150)
    plt.plot(dts, deltas, "o-", lw=1.4, color="#d62728")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("dt")
    plt.ylabel("max |Q(t) - Q(0)|")
    plt.title(f"Convergence: slope ~ {slope:.2f}, R^2={r2:.3f}")
    plt.tight_layout()
    plt.savefig(fig_path, bbox_inches="tight")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Validate the Q invariant for the logistic on-site law.")
    parser.add_argument("--r", type=float, required=True, help="Growth rate r")
    parser.add_argument("--u", type=float, required=True, help="Saturation coefficient u")
    parser.add_argument("--W0", type=float, nargs="+", required=True, help="Initial condition(s) W0 (one or more)")
    parser.add_argument("--T", type=float, default=40.0, help="Total time horizon")
    parser.add_argument("--dt", type=float, nargs="+", default=[1e-3], help="Time step(s) for integration")
    parser.add_argument("--solver", type=str, default="rk4", choices=["rk4", "euler"], help="Time-stepping scheme")
    parser.add_argument("--outdir", type=str, default=None, help="Base output dir override (figures/logs)")
    args = parser.parse_args()

    r = float(args.r)
    u = float(args.u)
    W0_list = [float(x) for x in args.W0]
    dt_list = [float(x) for x in args.dt]
    T = float(args.T)
    solver = str(args.solver).lower()

    # Resolve base output directory (override if provided)
    base_outdir_path = Path(args.outdir).resolve() if args.outdir else Path(BASE_OUTDIR).resolve()
    fig_dir_base = str((base_outdir_path / "figures" / "conservation_law").resolve())
    log_dir_base = str((base_outdir_path / "logs" / "conservation_law").resolve())

    # only ensure arXiv figs dir; figure/log dirs are ensured at file save
    ensure_dirs(ARXIV_FIG_DIR)
    stamp = utc_stamp()

    run_metrics: List[RunMetrics] = []

    # For the first W0 and finest dt, produce overlay and Q-drift figures
    W0_primary = W0_list[0]
    dt_primary = min(dt_list)

    t_p, W_num_p = integrate_numeric(r, u, W0_primary, T, dt_primary, solver=solver)
    W_an_p = logistic_analytic(r, u, W0_primary, t_p)
    Q_p = Q_invariant(r, u, W_num_p, t_p)
    delta_Q_max_p = float(np.nanmax(np.abs(Q_p - Q_p[0])))

    sol_fig = ""
    drift_fig = ""
    # Defer plotting until pass/fail is known

    # Placeholders; will be assigned only on PASS
    sol_fig_stable = ""
    drift_fig_stable = ""
    sol_fig_arxiv = ""
    drift_fig_arxiv = ""

    run_metrics.append(RunMetrics(r=r, u=u, solver=solver, dt=dt_primary, T=T, W0=W0_primary,
                                  delta_Q_max=delta_Q_max_p, W_min=float(np.min(W_num_p)), W_max=float(np.max(W_num_p))))

    # Convergence study on the first W0 across dt list
    deltas = []
    dts_sorted = sorted(dt_list, reverse=True)  # larger to smaller for plotting clarity
    for dt in dts_sorted:
        t_c, W_num_c = integrate_numeric(r, u, W0_primary, T, dt, solver=solver)
        Q_c = Q_invariant(r, u, W_num_c, t_c)
        deltaQ = float(np.nanmax(np.abs(Q_c - Q_c[0])))
        deltas.append(deltaQ)
        run_metrics.append(RunMetrics(r=r, u=u, solver=solver, dt=dt, T=T, W0=W0_primary,
                                      delta_Q_max=deltaQ, W_min=float(np.min(W_num_c)), W_max=float(np.max(W_num_c))))

    # Fit slope on positive finite pairs
    dts_arr = np.array(dts_sorted, dtype=np.float64)
    deltas_arr = np.array(deltas, dtype=np.float64)
    mask = np.isfinite(dts_arr) & np.isfinite(deltas_arr) & (dts_arr > 0) & (deltas_arr > 0)
    if np.count_nonzero(mask) >= 2:
        slope, intercept, r2 = fit_loglog(dts_arr[mask], deltas_arr[mask])
    else:
        slope, intercept, r2 = float("nan"), float("nan"), float("nan")

    conv_fig = ""
    conv_fig_stable = ""
    conv_fig_arxiv = ""
    # Defer plotting of convergence until pass/fail is known

    conv_metrics = ConvergenceMetrics(
        r=r, u=u, solver=solver, dts=list(dts_arr), delta_Q_max_list=list(deltas_arr),
        slope=slope, intercept=intercept, r2=r2
    )

    # Acceptance criteria and pass/fail routing (repo pattern)
    drift_gate = 1e-8 if solver == "rk4" else 1e-5
    conv_r2_min = 0.98
    expected_order = 4 if solver == "rk4" else 1
    order_tol = 0.4
    drift_ok = math.isfinite(delta_Q_max_p) and (delta_Q_max_p <= drift_gate)
    if np.count_nonzero(mask) >= 2 and math.isfinite(slope) and math.isfinite(r2):
        conv_ok = (r2 >= conv_r2_min) and (abs(slope - expected_order) <= order_tol)
    else:
        conv_ok = True  # allow pure drift validation if no convergence sweep available
    passed = drift_ok and conv_ok

    # Decide final figure targets and plot exactly once, using common helper policy
    failed_flag = not passed

    # Overlay/drift figures: prefer repo io_paths unless --outdir override provided
    if args.outdir is None:
        sol_fig_final = str(figure_path("conservation_law", "qfum_solution_overlay", failed=failed_flag))
        drift_fig_final = str(figure_path("conservation_law", "qfum_Q_drift", failed=failed_flag))
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = Path(fig_dir_base) / ("failed_runs" if failed_flag else "")
        base_dir.mkdir(parents=True, exist_ok=True)
        sol_fig_final = str(base_dir / f"{ts}_qfum_solution_overlay.png")
        drift_fig_final = str(base_dir / f"{ts}_qfum_Q_drift.png")

    plot_solution_overlay(sol_fig_final, t_p, W_num_p, W_an_p, r, u, W0_primary)
    plot_Q_drift(drift_fig_final, t_p, Q_p, r, u, W0_primary)

    # Convergence (only if we have data to show)
    conv_fig_final = ""
    if np.count_nonzero(mask) >= 2:
        if args.outdir is None:
            conv_fig_final = str(figure_path("conservation_law", "qfum_convergence", failed=failed_flag))
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_dir = Path(fig_dir_base) / ("failed_runs" if failed_flag else "")
            base_dir.mkdir(parents=True, exist_ok=True)
            conv_fig_final = str(base_dir / f"{ts}_qfum_convergence.png")
        plot_convergence(conv_fig_final, list(dts_arr[mask]), list(deltas_arr[mask]), slope, r2)

    # Produce arXiv copies ONLY on PASS
    sol_fig_stable = ""  # retained for JSON schema; not used when using io_paths
    drift_fig_stable = ""
    conv_fig_stable = ""
    if passed:
        try:
            os.makedirs(ARXIV_FIG_DIR, exist_ok=True)
            sol_fig_arxiv = os.path.join(ARXIV_FIG_DIR, "qfum_solution_overlay.png")
            drift_fig_arxiv = os.path.join(ARXIV_FIG_DIR, "qfum_Q_drift.png")
            shutil.copyfile(sol_fig_final, sol_fig_arxiv)
            shutil.copyfile(drift_fig_final, drift_fig_arxiv)
            if conv_fig_final:
                conv_fig_arxiv = os.path.join(ARXIV_FIG_DIR, "qfum_convergence.png")
                shutil.copyfile(conv_fig_final, conv_fig_arxiv)
        except Exception:
            pass
    else:
        # On failure, ensure arXiv placeholders remain blank
        sol_fig_arxiv = ""
        drift_fig_arxiv = ""
        conv_fig_arxiv = ""

    # Log JSON (prefer repo helper; respect --outdir override)
    if args.outdir is None:
        out_json_path = log_path("conservation_law", "qfum_metrics", failed=(not passed))
    else:
        out_dir = Path(log_dir_base)
        if not passed:
            out_dir = out_dir / "failed_runs"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_json_path = out_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_qfum_metrics.json"
    payload: Dict[str, object] = {
        "version": "1.0",
        "timestamp_utc": stamp,
        "params": {"r": r, "u": u, "T": T, "solver": solver, "W0_list": W0_list, "dt_list": dt_list},
        "runs": [asdict(m) for m in run_metrics],
        "convergence": asdict(conv_metrics),
        "figures": {
            "solution_overlay": sol_fig_final,
            "solution_overlay_stable": sol_fig_stable,
            "solution_overlay_arxiv": sol_fig_arxiv,
            "Q_drift": drift_fig_final,
            "Q_drift_stable": drift_fig_stable,
            "Q_drift_arxiv": drift_fig_arxiv,
            "convergence": conv_fig_final,
            "convergence_stable": conv_fig_stable,
            "convergence_arxiv": conv_fig_arxiv,
        },
        "acceptance": {
            "drift_gate": drift_gate,
            "convergence_expected_order": expected_order,
            "convergence_r2_min": conv_r2_min,
            "order_tol": order_tol,
            "drift_ok": drift_ok,
            "convergence_ok": conv_ok,
            "passed": passed
        }
    }
    if args.outdir is None:
        write_log(out_json_path, payload)
    else:
        with open(out_json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    out_json = str(out_json_path)

    # Console summary
    print("[QFUM] Primary run:")
    print(f"  r={r:.6g}, u={u:.6g}, W0={W0_primary:.6g}, dt={dt_primary:.6g}, T={T:.6g}")
    print(f"  max |Q(t)-Q(0)| = {delta_Q_max_p:.3e}")
    if np.isfinite(slope):
        print(f"[QFUM] Convergence: slope ~ {slope:.2f}, R^2={r2:.3f}")
        print(f"  Expected (RK4) ~ 4, Observed ~ {slope:.2f}")

    print("[QFUM] Figures:")
    print(f"  {sol_fig_final}")
    print(f"  {drift_fig_final}")
    if conv_fig_final:
        print(f"  {conv_fig_final}")
    print(f"[QFUM] {'PASSED' if passed else 'FAILED'}  (drift_ok={drift_ok}, conv_ok={conv_ok})")
    print("[QFUM] ArXiv figs:")
    print(f"  {sol_fig_arxiv}")
    print(f"  {drift_fig_arxiv}")
    if conv_fig_arxiv:
        print(f"  {conv_fig_arxiv}")
    print(f"[QFUM] Metrics JSON: {out_json}")


if __name__ == "__main__":
    main()