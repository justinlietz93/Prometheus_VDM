#!/usr/bin/env python3
"""
RD front-speed validation for Fisher-KPP:
    ∂t u = D ∂xx u + r u (1 - u)

Theory:
    Minimal pulled-front speed c_th = 2 * sqrt(D * r)

Outputs (defaults):
    - derivation/code/outputs/figures/<script>_<timestamp>.png
    - derivation/code/outputs/logs/<script>_<timestamp>.json

CLI example:
  python Prometheus_FUVDM/derivation/code/physics/rd_front_speed_experiment.py \
    --N 1024 --L 200 --D 1.0 --r 0.25 --T 80 --cfl 0.2 --seed 42 --x0 -60 --level 0.1 --fit_start 0.6 --fit_end 0.9
"""
import argparse
import json
import math
import os
import time
from typing import Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt


def laplacian_neumann(u: np.ndarray, dx: float) -> np.ndarray:
    """1D Laplacian with zero-gradient (Neumann) boundaries."""
    lap = np.empty_like(u)
    # interior
    lap[1:-1] = (u[2:] - 2*u[1:-1] + u[:-2]) / (dx*dx)
    # Neumann at boundaries: ghost = mirror interior point
    lap[0] = (u[1] - 2*u[0] + u[1]) / (dx*dx)          # 2*(u1 - u0)/dx^2
    lap[-1] = (u[-2] - 2*u[-1] + u[-2]) / (dx*dx)      # 2*(u_{N-2} - u_{N-1})/dx^2
    return lap


def front_position(x: np.ndarray, u: np.ndarray, level: float = 0.5) -> float:
    """Find x where u crosses 'level' via linear interpolation."""
    crossed = np.where((u[:-1] - level) * (u[1:] - level) <= 0)[0]
    if crossed.size == 0:
        # fallback: argmin |u - level|
        i = int(np.argmin(np.abs(u - level)))
        return float(x[i])
    i = int(crossed[0])
    u0, u1 = u[i], u[i+1]
    if u1 == u0:
        return float(x[i])
    frac = (level - u0) / (u1 - u0)
    return float(x[i] + frac * (x[i+1] - x[i]))


def front_position_near(x: np.ndarray, u: np.ndarray, level: float, x_guess: float) -> float:
    """
    Find a level crossing near a previous position x_guess.
    This stabilizes tracking (avoids picking a different crossing due to noise).
    """
    dif = u - level
    idx = np.where(dif[:-1] * dif[1:] <= 0)[0]
    if idx.size == 0:
        j = int(np.argmin(np.abs(dif)))
        return float(x[j])
    xs = []
    for i in idx:
        u0, u1 = u[i], u[i+1]
        if u1 == u0:
            xs.append(float(x[i]))
        else:
            frac = (level - u0) / (u1 - u0)
            xs.append(float(x[i] + frac * (x[i+1] - x[i])))
    xs = np.array(xs, dtype=float)
    j = int(np.argmin(np.abs(xs - x_guess)))
    return float(xs[j])


def robust_linear_fit(t: np.ndarray, x: np.ndarray, smooth_win: int = 7, mad_k: float = 3.0, max_iter: int = 3):
    """
    Robust linear fit x(t) ~ a * t + b with simple moving-average smoothing and MAD-based outlier rejection.
    Returns (a, R^2). If insufficient points, returns (nan, nan).
    """
    t = np.asarray(t, dtype=float).ravel()
    x = np.asarray(x, dtype=float).ravel()
    n = t.size
    if n < 2:
        return float("nan"), float("nan")

    # Smooth x with moving average (odd window)
    if smooth_win % 2 == 0:
        smooth_win += 1
    if n >= smooth_win and smooth_win > 1:
        kernel = np.ones(smooth_win, dtype=float) / smooth_win
        x_s = np.convolve(x, kernel, mode="same")
    else:
        x_s = x.copy()

    mask = np.ones(n, dtype=bool)
    a = float("nan")
    b = float("nan")

    for _ in range(max_iter):
        tt = t[mask]
        xx = x_s[mask]
        if tt.size < 2:
            break
        coeffs = np.polyfit(tt, xx, 1)
        a = float(coeffs[0])
        b = float(coeffs[1])
        pred = a * t + b
        resid = x_s - pred
        mad = float(np.median(np.abs(resid[mask])) + 1e-12)
        new_mask = np.abs(resid) <= mad_k * mad
        # Ensure we keep enough points
        if new_mask.sum() < max(5, int(0.2 * n)):
            break
        # If mask stabilizes, stop
        if np.array_equal(new_mask, mask):
            break
        mask = new_mask

    # Final R^2 on kept points
    tt = t[mask]
    xx = x_s[mask]
    if tt.size >= 2 and np.isfinite(a):
        pred = a * tt + b
        ss_res = float(np.sum((xx - pred) ** 2))
        ss_tot = float(np.sum((xx - np.mean(xx)) ** 2) + 1e-12)
        r2 = 1.0 - ss_res / ss_tot
    else:
        a, r2 = float("nan"), float("nan")
    return a, r2


def run_sim(
    N: int,
    L: float,
    D: float,
    r: float,
    T: float,
    cfl: float,
    seed: int,
    level: float = 0.5,
    x0: Optional[float] = None,
    fit_frac: Tuple[float, float] = (0.2, 0.9),
    noise_amp: float = 0.0,
):
    rng = np.random.default_rng(seed)
    x = np.linspace(-L/2, L/2, N, endpoint=False)
    dx = x[1] - x[0]
    # stability-limited timestep (explicit Euler)
    dt_diff = cfl * dx*dx / (2.0*D + 1e-12)
    dt_reac = 0.2 / r if r > 0 else dt_diff
    dt = min(dt_diff, dt_reac)
    steps = int(max(2, math.ceil(T / dt)))
    dt = T / steps

    # Smooth step IC: left ~1, right ~0; place interface well inside domain
    w = 2.0  # interface width
    if x0 is None:
        x0 = -L / 4.0
    u = 0.5 * (1.0 - np.tanh((x - x0) / w))
    # keep far-ahead region identically zero to avoid uniform logistic growth
    region_edge = x0 + 6.0 * w
    u[x > region_edge] = 0.0
    # optional: gated noise only on the left side of the interface
    if noise_amp > 0.0:
        noise = noise_amp * rng.standard_normal(size=N)
        noise[x > region_edge] = 0.0
        u += noise
    u = np.clip(u, 0.0, 1.0)

    rec_t = []
    rec_xf = []
    rec_xg = []
    snapshot_times = []
    snapshots = []

    out_every = max(1, steps // 400)
    snap_every = max(1, steps // 6)
    last_xf = None

    for n in range(steps):
        lap = laplacian_neumann(u, dx)
        u += dt * (D * lap + r * u * (1.0 - u))
        u = np.clip(u, 0.0, 1.0)

        if n % out_every == 0:
            t = (n+1) * dt
            # real level crossing?
            dif = u - level
            has_cross = np.any(dif[:-1] * dif[1:] <= 0)
            if has_cross:
                if last_xf is None:
                    xf = front_position(x, u, level)
                else:
                    xf = front_position_near(x, u, level, last_xf)
                last_xf = xf
                rec_t.append(t)
                rec_xf.append(xf)
                # gradient-peak tracker (cross-check)
                grad = np.empty_like(u)
                grad[1:-1] = (u[2:] - u[:-2]) / (2.0 * dx)
                grad[0] = (u[1] - u[0]) / dx
                grad[-1] = (u[-1] - u[-2]) / dx
                xg = float(x[np.argmax(np.abs(grad))])
                rec_xg.append(xg)
            else:
                # front has passed; if domain is fully invaded (> level), stop tracking
                if float(np.min(u)) > level:
                    break
        if n % snap_every == 0:
            snapshot_times.append((n+1) * dt)
            snapshots.append(u.copy())

    rec_t = np.array(rec_t)
    rec_xf = np.array(rec_xf)

    # Fit speed from late-time window
    f0, f1 = fit_frac
    i0 = int(max(0, min(len(rec_t)-2, round(f0 * len(rec_t)))))
    i1 = int(max(i0+2, min(len(rec_t), round(f1 * len(rec_t)))))
    t_fit = rec_t[i0:i1]
    x_fit = rec_xf[i0:i1]

    if t_fit.size >= 5:
        c_meas, r2 = robust_linear_fit(t_fit, x_fit, smooth_win=7, mad_k=3.0, max_iter=3)
        # Fallback if robustness failed
        if (not math.isfinite(c_meas)) or (not math.isfinite(r2)) or (r2 < 0.6):
            half = len(t_fit) // 2
            if half >= 1:
                dx_med = float(np.median(x_fit[half:]) - np.median(x_fit[:half]))
                dt_med = float(np.median(t_fit[half:]) - np.median(t_fit[:half]) + 1e-12)
                c_meas = dx_med / dt_med
                # Simple R^2 estimate with this slope
                b0 = float(np.median(x_fit) - c_meas * np.median(t_fit))
                x_pred = c_meas * t_fit + b0
                ss_res = float(np.sum((x_fit - x_pred) ** 2))
                ss_tot = float(np.sum((x_fit - np.mean(x_fit)) ** 2) + 1e-12)
                r2 = 1.0 - ss_res / ss_tot
            else:
                c_meas, r2 = float("nan"), float("nan")
    else:
        c_meas, r2 = float("nan"), float("nan")

    # Final metrics after fit
    c_th = 2.0 * math.sqrt(D * r)
    c_abs = abs(c_meas) if math.isfinite(c_meas) else float("nan")
    rel_err = abs(c_abs - c_th) / (abs(c_th) + 1e-12)

    # Determine sign via slope between medians if fit unreliable
    if not math.isfinite(c_meas) or not math.isfinite(r2) or r2 < 0.5:
        half = len(rec_t) // 2
        if half >= 2:
            dx_med = float(np.median(rec_xf[half:]) - np.median(rec_xf[:half]))
            dt_med = float(np.median(rec_t[half:]) - np.median(rec_t[:half]) + 1e-12)
            c_meas = dx_med / dt_med
            # Update derived metrics after fallback
            c_abs = abs(c_meas) if math.isfinite(c_meas) else float("nan")
            rel_err = abs(c_abs - c_th) / (abs(c_th) + 1e-12)

    # Gradient-based front speed (optional cross-check)
    if len(rec_xg) == len(rec_t) and len(rec_t) >= 5:
        tg = rec_t[i0:i1]
        xg = np.array(rec_xg[i0:i1], dtype=float)
        if tg.size >= 5:
            c_meas_grad, r2_grad = robust_linear_fit(tg, xg, smooth_win=7, mad_k=3.0, max_iter=3)
            c_abs_grad = abs(c_meas_grad) if math.isfinite(c_meas_grad) else float("nan")
            rel_err_grad = abs(c_abs_grad - c_th) / (abs(c_th) + 1e-12)
        else:
            c_meas_grad = float("nan"); r2_grad = float("nan"); c_abs_grad = float("nan"); rel_err_grad = float("nan")
    else:
        c_meas_grad = float("nan"); r2_grad = float("nan"); c_abs_grad = float("nan"); rel_err_grad = float("nan")

    return {
        "x": x,
        "snapshots": snapshots,
        "snapshot_times": snapshot_times,
        "rec_t": rec_t,
        "rec_xf": rec_xf,
        "rec_xg": rec_xg,
        "c_meas": c_meas,
        "c_abs": c_abs,
        "c_th": c_th,
        "rel_err": rel_err,
        "r2": r2,
        "c_meas_grad": c_meas_grad,
        "c_abs_grad": c_abs_grad,
        "rel_err_grad": rel_err_grad,
        "r2_grad": r2_grad,
        "dx": dx,
        "dt": dt,
        "steps": steps,
        "level": level,
        "fit_frac": [f0, f1],
    }


def plot_and_save(data: dict, figure_path: str):
    x = data["x"]
    snapshots = data["snapshots"]
    snapshot_times = data["snapshot_times"]
    rec_t = data["rec_t"]
    rec_xf = data["rec_xf"]
    c_meas = data["c_meas"]
    c_abs = data["c_abs"]
    c_th = data["c_th"]
    r2 = data["r2"]

    plt.figure(figsize=(10, 7))
    # Top: snapshots
    ax1 = plt.subplot(2, 1, 1)
    for u, t in zip(snapshots, snapshot_times):
        ax1.plot(x, u, lw=1, label=f"t={t:.1f}")
    ax1.set_title("RD Fisher-KPP front evolution")
    ax1.set_xlabel("x")
    ax1.set_ylabel("u")
    if len(snapshot_times) <= 8 and len(snapshot_times) > 0:
        ax1.legend(ncol=2, fontsize=8)

    # Bottom: front position vs time
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(rec_t, rec_xf, ".", ms=3, label="x_front(t)")
    # optional gradient-peak tracker overlay
    if len(data.get("rec_xg", [])) == len(rec_t) and len(rec_t) > 0:
        ax2.plot(rec_t, data["rec_xg"], "g.", ms=3, alpha=0.6, label="x_grad(t)")
    if np.isfinite(c_meas):
        t_line = np.array([rec_t.min(), rec_t.max()])
        ax2.plot(t_line, c_meas * t_line + (rec_xf[0] - c_meas * rec_t[0]), "r--",
                 label=f"fit c={c_meas:.3f}, |c|={c_abs:.3f}, R2={r2:.3f}")
        ax2.plot(t_line, c_th * t_line + (rec_xf[0] - c_th * rec_t[0]), "k-.",
                 label=f"theory c=2√(Dr)={c_th:.3f}")
    ax2.set_xlabel("t")
    ax2.set_ylabel("x_front")
    ax2.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    plt.savefig(figure_path, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Validate Fisher-KPP front speed c=2√(Dr).")
    parser.add_argument("--N", type=int, default=1024)
    parser.add_argument("--L", type=float, default=200.0)
    parser.add_argument("--D", type=float, default=1.0)
    parser.add_argument("--r", type=float, default=0.25)
    parser.add_argument("--T", type=float, default=80.0)
    parser.add_argument("--cfl", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--level", type=float, default=0.1)
    parser.add_argument("--x0", type=float, default=-60.0)
    parser.add_argument("--fit_start", type=float, default=0.6, help="fractional start of fit window")
    parser.add_argument("--fit_end", type=float, default=0.9, help="fractional end of fit window")
    parser.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to derivation/code/outputs next to this script")
    parser.add_argument("--figure", type=str, default=None, help="override figure path; otherwise script_name_timestamp.png in outdir/figures")
    parser.add_argument("--log", type=str, default=None, help="override log path; otherwise script_name_timestamp.json in outdir/logs")
    parser.add_argument("--noise_amp", type=float, default=0.0, help="optional gated noise amplitude (applied only left of the front)")
    args = parser.parse_args()

    # Compute output paths based on script name and UTC timestamp
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
    data = run_sim(
        args.N, args.L, args.D, args.r, args.T, args.cfl, args.seed,
        level=args.level,
        x0=args.x0,
        fit_frac=(args.fit_start, args.fit_end),
        noise_amp=args.noise_amp,
    )
    elapsed = time.time() - t0

    acceptance_rel_err = 0.05
    acceptance_r2 = 0.98
    passed = (data["rel_err"] <= acceptance_rel_err) and (np.isfinite(data["r2"]) and data["r2"] >= acceptance_r2)
    if not passed:
        if args.figure is None:
            figure_path = os.path.join(fig_dir, "failed_runs", f"{script_name}_{tstamp}.png")
        if args.log is None:
            log_path = os.path.join(log_dir, "failed_runs", f"{script_name}_{tstamp}.json")
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    plot_and_save(data, figure_path)

    payload = {
        "theory": "Fisher-KPP front speed c=2*sqrt(D*r)",
        "params": {
            "N": args.N, "L": args.L, "D": args.D, "r": args.r, "T": args.T,
            "cfl": args.cfl, "seed": args.seed, "level": args.level,
            "x0": args.x0, "fit_start": args.fit_start, "fit_end": args.fit_end,
            "noise_amp": args.noise_amp
        },
        "metrics": {
            "c_meas": data["c_meas"],
            "c_abs": data["c_abs"],
            "c_sign": (1.0 if (np.isfinite(data['c_meas']) and data['c_meas'] >= 0) else -1.0),
            "c_th": data["c_th"],
            "rel_err": data["rel_err"],
            "r2": data["r2"],
            "dx": data["dx"],
            "dt": data["dt"],
            "steps": data["steps"],
            "elapsed_sec": elapsed,
            "acceptance_rel_err": 0.05,
            "passed": (data["rel_err"] <= 0.05) and (np.isfinite(data["r2"]) and data["r2"] >= 0.98),
            "c_meas_grad": data.get("c_meas_grad", float("nan")),
            "c_abs_grad": data.get("c_abs_grad", float("nan")),
            "rel_err_grad": data.get("rel_err_grad", float("nan")),
            "r2_grad": data.get("r2_grad", float("nan"))
        },
        "outputs": {
            "figure": figure_path
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps({
        "figure": figure_path,
        "log": log_path,
        "c_meas": data["c_meas"],
        "c_abs": data["c_abs"],
        "c_th": data["c_th"],
        "rel_err": data["rel_err"],
        "r2": data["r2"],
        "c_meas_grad": data.get("c_meas_grad"),
        "c_abs_grad": data.get("c_abs_grad"),
        "rel_err_grad": data.get("rel_err_grad"),
        "r2_grad": data.get("r2_grad")
    }, indent=2))


if __name__ == "__main__":
    main()