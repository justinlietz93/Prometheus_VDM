#!/usr/bin/env python3
"""
RD dispersion validation (linear regime) for Fisher-KPP:
    ∂t u = D ∂xx u + r u (1 - u)
Linearized about u≈0: u_t ≈ D u_xx + r u

Predictions:
  Continuum:  σ_c(k) = r − D k^2
  Discrete (periodic second-difference):  σ_d(m) = r − (4 D / dx^2) sin^2(π m / N)

Method:
  - Evolve the linearized PDE with periodic BCs from small random amplitude.
  - Record snapshots and fit log |Û_m(t)| vs t for selected modes m.
  - Compare measured growth rates to σ_d(m) (primary) and σ_c(k) (reference).

Outputs (defaults):
  - derivation/code/outputs/figures/<script>_<timestamp>.png
  - derivation/code/outputs/logs/<script>_<timestamp>.json

CLI example:
  python Prometheus_FUVDM/derivation/code/physics/rd_dispersion_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 10 --cfl 0.2 --seed 42
"""
import argparse
import json
import math
import os
import time
from typing import Tuple, List, Dict

import numpy as np
import matplotlib.pyplot as plt


def laplacian_periodic(u: np.ndarray, dx: float) -> np.ndarray:
    """1D Laplacian with periodic boundaries."""
    lap = (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx * dx)
    return lap


def robust_linear_fit(t: np.ndarray, y: np.ndarray, smooth_win: int = 5, mad_k: float = 3.0, max_iter: int = 3):
    """
    Robust linear fit y(t) ~ a * t + b with moving-average smoothing and MAD-based outlier rejection.
    Returns (a, R^2). If insufficient points, returns (nan, nan).
    """
    t = np.asarray(t, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    n = t.size
    if n < 2:
        return float("nan"), float("nan")

    if smooth_win % 2 == 0:
        smooth_win += 1
    if n >= smooth_win and smooth_win > 1:
        kernel = np.ones(smooth_win, dtype=float) / smooth_win
        y_s = np.convolve(y, kernel, mode="same")
    else:
        y_s = y.copy()

    mask = np.isfinite(y_s)
    if mask.sum() < 2:
        return float("nan"), float("nan")

    a = float("nan")
    b = float("nan")
    for _ in range(max_iter):
        tt = t[mask]
        yy = y_s[mask]
        if tt.size < 2:
            break
        coeffs = np.polyfit(tt, yy, 1)
        a = float(coeffs[0]); b = float(coeffs[1])
        pred = a * t + b
        resid = y_s - pred
        mad = float(np.median(np.abs(resid[mask])) + 1e-12)
        new_mask = np.isfinite(y_s) & (np.abs(resid) <= mad_k * mad)
        if new_mask.sum() < max(5, int(0.2 * n)):
            break
        if np.array_equal(new_mask, mask):
            break
        mask = new_mask

    tt = t[mask]
    yy = y_s[mask]
    if tt.size >= 2 and np.isfinite(a):
        pred = a * tt + b
        ss_res = float(np.sum((yy - pred) ** 2))
        ss_tot = float(np.sum((yy - np.mean(yy)) ** 2) + 1e-12)
        r2 = 1.0 - ss_res / ss_tot
    else:
        a, r2 = float("nan"), float("nan")
    return a, r2


def run_linear_sim(
    N: int,
    L: float,
    D: float,
    r: float,
    T: float,
    cfl: float,
    seed: int,
    amp0: float = 1e-6,
    record_slices: int = 60,
):
    """
    Explicit Euler on u_t = D u_xx + r u with periodic BCs. Start from small random noise.
    Returns dict with x, dx, dt, steps, snapshots, snapshot_times.
    """
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, L, N, endpoint=False)
    dx = x[1] - x[0]
    # time step from diffusion CFL (linear)
    dt_diff = cfl * dx * dx / (2.0 * D + 1e-12)
    dt_reac = 0.2 / r if r > 0 else dt_diff
    dt = min(dt_diff, dt_reac)
    steps = int(max(2, math.ceil(T / dt)))
    dt = T / steps

    u = amp0 * rng.standard_normal(size=N).astype(float)
    snapshots: List[np.ndarray] = []
    snapshot_times: List[float] = []
    out_every = max(1, steps // record_slices)

    for n in range(steps):
        lap = laplacian_periodic(u, dx)
        u += dt * (D * lap + r * u)
        if (n + 1) % out_every == 0:
            snapshots.append(u.copy())
            snapshot_times.append((n + 1) * dt)

    return {
        "x": x, "dx": dx, "dt": dt, "steps": steps,
        "snapshots": snapshots, "snapshot_times": snapshot_times,
    }


def analyze_dispersion(data: Dict, D: float, r: float, L: float, m_max: int, fit_frac: Tuple[float, float]):
    """
    Compute FFT of snapshots, fit growth rates for modes m=0..m_max, and compare to theory.
    Returns dict with arrays and summary metrics.
    """
    snaps = data["snapshots"]
    times = np.array(data["snapshot_times"], dtype=float)
    N = snaps[0].size
    dx = data["dx"]

    # Build 1-sided (non-negative) mode list
    m_vals = np.arange(0, min(m_max, N // 2) + 1, dtype=int)
    k_vals = 2.0 * np.pi * m_vals / L

    # Stack FFT amplitudes over time
    amps = []
    for u in snaps:
        U = np.fft.rfft(u)  # length N//2+1
        amps.append(np.abs(U))
    amps = np.array(amps)  # shape [T_s, M]

    f0, f1 = fit_frac
    i0 = int(max(0, min(len(times) - 2, round(f0 * len(times)))))
    i1 = int(max(i0 + 2, min(len(times), round(f1 * len(times)))))
    t_fit = times[i0:i1]

    sigma_meas = np.zeros_like(m_vals, dtype=float)
    r2_meas = np.zeros_like(m_vals, dtype=float)

    for j, m in enumerate(m_vals):
        a = amps[i0:i1, j]
        a = np.maximum(a, 1e-30)
        y = np.log(a)
        slope, r2 = robust_linear_fit(t_fit, y, smooth_win=5, mad_k=3.0, max_iter=3)
        sigma_meas[j] = slope
        r2_meas[j] = r2

    # Theoretical discrete and continuum rates
    sigma_disc = r - (4.0 * D / (dx * dx)) * (np.sin(np.pi * m_vals / N) ** 2)
    sigma_cont = r - D * (k_vals ** 2)

    # Compare only where growth/decay is measurable and fit quality decent
    good = np.isfinite(sigma_meas) & np.isfinite(r2_meas) & (r2_meas >= 0.95)
    rel_err = np.full_like(sigma_meas, np.nan, dtype=float)
    rel_err[good] = np.abs(sigma_meas[good] - sigma_disc[good]) / (np.abs(sigma_disc[good]) + 1e-12)

    # Summary metrics
    med_rel_err = float(np.nanmedian(rel_err))
    # R² between arrays (meas vs disc) on good subset
    if np.sum(good) >= 2:
        A = sigma_meas[good]
        B = sigma_disc[good]
        ss_res = float(np.sum((A - B) ** 2))
        ss_tot = float(np.sum((A - np.mean(A)) ** 2) + 1e-12)
        r2_array = 1.0 - ss_res / ss_tot
    else:
        r2_array = float("nan")

    return {
        "m_vals": m_vals.tolist(),
        "k_vals": k_vals.tolist(),
        "sigma_meas": sigma_meas.tolist(),
        "r2_meas": r2_meas.tolist(),
        "sigma_disc": sigma_disc.tolist(),
        "sigma_cont": sigma_cont.tolist(),
        "rel_err": rel_err.tolist(),
        "med_rel_err": med_rel_err,
        "r2_array": float(r2_array),
        "good_mask": good.tolist(),
    }


def plot_and_save_dispersion(analysis: Dict, figure_path: str, title: str = "RD dispersion (linear regime)"):
    m_vals = np.array(analysis["m_vals"], dtype=int)
    k_vals = np.array(analysis["k_vals"], dtype=float)
    sig_meas = np.array(analysis["sigma_meas"], dtype=float)
    sig_disc = np.array(analysis["sigma_disc"], dtype=float)
    sig_cont = np.array(analysis["sigma_cont"], dtype=float)
    good = np.array(analysis["good_mask"], dtype=bool)

    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.plot(k_vals, sig_disc, "k-", lw=2, label="theory σ_d (discrete)")
    ax.plot(k_vals, sig_cont, "k--", lw=1, alpha=0.6, label="theory σ_c (continuum)")
    ax.plot(k_vals[good], sig_meas[good], "o", ms=4, label="measured (fit on log|Û|)")
    if np.any(~good):
        ax.plot(k_vals[~good], sig_meas[~good], "o", ms=3, alpha=0.3, label="measured (low R²)")
    ax.set_xlabel("k = 2π m / L")
    ax.set_ylabel("σ(k)")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    plt.savefig(figure_path, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Validate RD linear dispersion σ(k) using periodic linearized evolution.")
    parser.add_argument("--N", type=int, default=1024)
    parser.add_argument("--L", type=float, default=200.0)
    parser.add_argument("--D", type=float, default=1.0)
    parser.add_argument("--r", type=float, default=0.25)
    parser.add_argument("--T", type=float, default=10.0)
    parser.add_argument("--cfl", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--amp0", type=float, default=1e-6, help="Initial noise amplitude (std dev).")
    parser.add_argument("--record", type=int, default=80, help="Number of snapshots to record.")
    parser.add_argument("--m_max", type=int, default=64, help="Max mode index m to fit (clamped by N//2).")
    parser.add_argument("--fit_start", type=float, default=0.1, help="fractional start of fit window")
    parser.add_argument("--fit_end", type=float, default=0.4, help="fractional end of fit window")
    parser.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to derivation/code/outputs next to this script")
    parser.add_argument("--figure", type=str, default=None, help="override figure path; otherwise script_name_timestamp.png in outdir/figures")
    parser.add_argument("--log", type=str, default=None, help="override log path; otherwise script_name_timestamp.json in outdir/logs")
    args = parser.parse_args()

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    tstamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    # Follow repo convention: write to derivation/code/outputs/{figures,logs}/reaction_diffusion
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures", "reaction_diffusion")
    log_dir = os.path.join(base_outdir, "logs", "reaction_diffusion")
    figure_path = args.figure if args.figure else os.path.join(fig_dir, f"{script_name}_{tstamp}.png")
    log_path = args.log if args.log else os.path.join(log_dir, f"{script_name}_{tstamp}.json")
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    t0 = time.time()
    sim = run_linear_sim(args.N, args.L, args.D, args.r, args.T, args.cfl, args.seed, amp0=args.amp0, record_slices=args.record)
    analysis = analyze_dispersion(sim, args.D, args.r, args.L, args.m_max, (args.fit_start, args.fit_end))
    elapsed = time.time() - t0

    # Acceptance criteria (conservative for multi-mode fit)
    acceptance = {
        "med_rel_err_max": 0.10,
        "r2_array_min": 0.98,
    }
    passed = (
        (math.isfinite(analysis["med_rel_err"]) and analysis["med_rel_err"] <= acceptance["med_rel_err_max"]) and
        (math.isfinite(analysis["r2_array"]) and analysis["r2_array"] >= acceptance["r2_array_min"])
    )
    if not passed:
        if args.figure is None:
            figure_path = os.path.join(fig_dir, "failed_runs", f"{script_name}_{tstamp}.png")
        if args.log is None:
            log_path = os.path.join(log_dir, "failed_runs", f"{script_name}_{tstamp}.json")
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    plot_and_save_dispersion(analysis, figure_path, title=f"RD dispersion (linear): D={args.D}, r={args.r}")

    # Acceptance criteria (conservative for multi-mode fit)
    acceptance = {
        "med_rel_err_max": 0.10,
        "r2_array_min": 0.98,
    }
    passed = (
        (math.isfinite(analysis["med_rel_err"]) and analysis["med_rel_err"] <= acceptance["med_rel_err_max"]) and
        (math.isfinite(analysis["r2_array"]) and analysis["r2_array"] >= acceptance["r2_array_min"])
    )

    payload = {
        "theory": {
            "continuum": "sigma_c(k) = r - D k^2",
            "discrete": "sigma_d(m) = r - (4 D / dx^2) sin^2(pi m / N)"
        },
        "params": {
            "N": args.N, "L": args.L, "D": args.D, "r": args.r, "T": args.T,
            "cfl": args.cfl, "seed": args.seed, "amp0": args.amp0,
            "record": args.record, "m_max": args.m_max,
            "fit_start": args.fit_start, "fit_end": args.fit_end,
        },
        "metrics": {
            "med_rel_err": analysis["med_rel_err"],
            "r2_array": analysis["r2_array"],
            "acceptance": acceptance,
            "passed": passed,
        },
        "series": {
            "m_vals": analysis["m_vals"],
            "k_vals": analysis["k_vals"],
            "sigma_meas": analysis["sigma_meas"],
            "sigma_disc": analysis["sigma_disc"],
            "sigma_cont": analysis["sigma_cont"],
            "r2_meas": analysis["r2_meas"],
            "rel_err": analysis["rel_err"],
            "good_mask": analysis["good_mask"],
        },
        "outputs": {
            "figure": figure_path
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_sec": elapsed,
    }

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps({
        "figure": figure_path,
        "log": log_path,
        "med_rel_err": payload["metrics"]["med_rel_err"],
        "r2_array": payload["metrics"]["r2_array"],
        "passed": payload["metrics"]["passed"],
    }, indent=2))


if __name__ == "__main__":
    main()