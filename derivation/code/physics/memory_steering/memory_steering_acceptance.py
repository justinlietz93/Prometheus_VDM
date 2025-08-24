"""
Memory Steering Acceptance Harness

Implements a leaky first-order memory filter with saturation and runs:
- Step response: fit pole p and verify fixed point M*.
- Canonical void target: with g = 1.5 * lam and s ≡ 1, verify M_final ≈ 0.6 (multi-seed).
- Noise suppression: SNR_out improvement ≥ 3 dB.
- Boundedness: no post-clamp violations outside [0, 1].
- Lyapunov monotonicity for constant s (noise-free).
- Reproducibility: identical sequences for the same seed.

CLI:
  python -m Prometheus_FUVDM.derivation.code.physics.memory_steering.memory_steering_acceptance \
      --seed 0 --steps 512 --g 0.12 --lam 0.08 --noise_std 0.0

Outputs:
- JSON metrics: Prometheus_FUVDM/derivation/code/outputs/logs/memory_steering/memory_steering_acceptance_<timestamp>.json
- Figures (PNG): Prometheus_FUVDM/derivation/code/outputs/figures/memory_steering/
"""

import argparse
import json
import math
import os
import time
from datetime import datetime, timezone

import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless/CI safe
import matplotlib.pyplot as plt

# Paths
ROOT = os.path.join("Prometheus_FUVDM", "derivation")
LOG_DIR = os.path.join(ROOT, "code", "outputs", "logs", "memory_steering")
FIG_DIR = os.path.join(ROOT, "code", "outputs", "figures", "memory_steering")

def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

def iso_ts():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def memory_update(M, s, g, lam, rng=None, noise_std=0.0):
    """Single-step update for the memory variable with saturation to [0,1]."""
    eps = rng.normal(0.0, noise_std) if (rng is not None and noise_std > 0.0) else 0.0
    M_next = (1.0 - lam - g) * M + g * s + eps
    if M_next < 0.0:
        M_next = 0.0
    elif M_next > 1.0:
        M_next = 1.0
    return M_next

def run_filter(s, g, lam, M0=None, rng=None, noise_std=0.0):
    """Run the filter over an input sequence s."""
    T = len(s)
    M = np.zeros(T, dtype=float)
    if M0 is None:
        # If s is constant initially, set M0 to predicted fixed point for faster convergence in step test.
        s0 = float(s[0])
        M0 = g * s0 / (g + lam) if (g + lam) > 0 else s0
    M[0] = np.clip(M0, 0.0, 1.0)
    for t in range(T - 1):
        M[t+1] = memory_update(M[t], s[t], g, lam, rng=rng, noise_std=noise_std)
    return M

def fit_pole_from_step(M, s, g, lam, t_step):
    """Fit the discrete-time pole p from a post-step logarithmic residual."""
    s1 = float(s[-1])
    M_star = g * s1 / (g + lam) if (g + lam) > 0 else s1
    resid = M - M_star
    start = t_step + 2
    end = len(M) - 2
    if end <= start + 5:
        return np.nan, np.nan, np.nan, np.nan
    r = resid[start:end]
    mask = np.abs(r) > 1e-10
    t_idx = np.arange(start, end)[mask]
    y = np.log(np.abs(r[mask]))
    if len(y) < 5:
        return np.nan, M_star, np.nan, np.nan
    A = np.vstack([np.ones_like(t_idx, dtype=float), t_idx.astype(float)]).T
    coeff, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    b = coeff[1]
    p_fit = float(np.exp(b))
    p_pred = 1.0 - lam - g
    return p_fit, p_pred, M_star, resid

def snr_db(signal, noise):
    ps = np.var(signal)
    pn = np.var(noise)
    if pn <= 1e-20:
        return float('inf')
    return 10.0 * math.log10(ps / pn)

def step_response_experiment(seed, steps, g, lam):
    rng = np.random.default_rng(seed)
    t_step = 64 if steps > 100 else max(4, steps // 4)
    s0, s1 = 0.2, 0.8
    s = np.ones(steps) * s0
    s[t_step:] = s1
    # Choose M0 at initial fixed point
    M0 = g * s0 / (g + lam) if (g + lam) > 0 else s0
    M = run_filter(s, g, lam, M0=M0, rng=rng, noise_std=0.0)
    p_fit, p_pred, M_star, resid = fit_pole_from_step(M, s, g, lam, t_step)
    # Final value and overshoot
    tail = M[int(0.9 * steps):]
    M_final = float(np.mean(tail))
    step_amp = abs((g * s1 / (g + lam)) - (g * s0 / (g + lam))) if (g + lam) > 0 else abs(s1 - s0)
    overshoot = float(max(0.0, np.max(M) - max(M_star, M0))) / (step_amp + 1e-12)
    # Plot
    ts = np.arange(steps)
    plt.figure(figsize=(7, 4))
    plt.plot(ts, s, 'k--', label='s(t)')
    plt.plot(ts, M, 'b-', label='M(t)')
    plt.axvline(t_step, color='gray', alpha=0.3)
    plt.hlines([M_star], 0, steps-1, colors='r', linestyles=':', label='M* (pred)')
    plt.title(f"Step Response (g={g:.3f}, λ={lam:.3f}) | p_fit={p_fit:.3f}, p_pred={p_pred:.3f}")
    plt.xlabel('t'); plt.ylabel('value'); plt.legend(loc='best')
    fname = os.path.join(FIG_DIR, f"step_response_{iso_ts()}_g{g:.3f}_lam{lam:.3f}.png")
    plt.tight_layout(); plt.savefig(fname, dpi=150); plt.close()
    return {
        "p_fit": p_fit,
        "p_pred": p_pred,
        "M_star_pred": M_star,
        "M_final": M_final,
        "overshoot": overshoot,
        "figure": fname,
        "pass_pole": (not np.isnan(p_fit)) and (abs(p_fit - p_pred) <= 0.02),
        "pass_Mstar": abs(M_final - M_star) <= 1e-2,
        "pass_overshoot": overshoot <= 0.02
    }

def canonical_void_experiment_multi(steps):
    """Test the 0.6 target for seeds {0,1,2}; deterministic here (no noise)."""
    results = []
    lam = 0.1
    g = 1.5 * lam
    for seed in [0, 1, 2]:
        rng = np.random.default_rng(seed)
        s = np.ones(steps)
        M = run_filter(s, g, lam, M0=0.0, rng=rng, noise_std=0.0)
        M_final = float(np.mean(M[int(0.9 * steps):]))
        # Plot each seed lightly; last one will be representative
        ts = np.arange(steps)
        plt.figure(figsize=(7, 3.5))
        plt.plot(ts, M, 'b-', label='M(t)')
        plt.hlines([0.6], 0, steps-1, colors='r', linestyles=':', label='0.6 target')
        plt.title(f"Canonical Void Target | g=1.5λ, λ={lam:.3f}, g={g:.3f}, seed={seed}, M_final={M_final:.3f}")
        plt.xlabel('t'); plt.ylabel('M'); plt.legend(loc='best')
        fname = os.path.join(FIG_DIR, f"canonical_void_{iso_ts()}_lam{lam:.3f}_seed{seed}.png")
        plt.tight_layout(); plt.savefig(fname, dpi=150); plt.close()
        results.append({
            "seed": seed, "lam": lam, "g": g, "target": 0.6, "M_final": M_final,
            "figure": fname,
            "pass_target": abs(M_final - 0.6) <= 0.02
        })
    overall_pass = all(r["pass_target"] for r in results)
    return {"seeds": [0,1,2], "results": results, "overall_pass": overall_pass, "lam": lam, "g": g}

def noise_suppression_experiment(seed, steps, g, lam, noise_std=0.05):
    rng = np.random.default_rng(seed)
    t = np.arange(steps)
    # Base signal around 0.5 with amplitude 0.3, clipped to [0,1]
    s_signal = 0.5 + 0.3 * np.sin(2 * np.pi * t / 128.0)
    noise_in = rng.normal(0.0, noise_std, size=steps)
    s = np.clip(s_signal + noise_in, 0.0, 1.0)
    # Filter outputs
    M_full = run_filter(s, g, lam, M0=None, rng=rng, noise_std=0.0)
    M_signal = run_filter(s_signal, g, lam, M0=None, rng=rng, noise_std=0.0)
    noise_out = M_full - M_signal
    snr_in = snr_db(s_signal, np.clip(s - s_signal, -1e6, 1e6))
    snr_out = snr_db(M_signal, noise_out)
    # Plot
    plt.figure(figsize=(7, 4))
    plt.plot(t, s, color='gray', alpha=0.5, label='s = signal + noise')
    plt.plot(t, M_full, 'b-', label='M(s)')
    plt.plot(t, M_signal, 'g--', label='M(signal)')
    plt.title(f"Noise Suppression (ΔSNR={snr_out - snr_in:.2f} dB)")
    plt.xlabel('t'); plt.ylabel('value'); plt.legend(loc='best')
    fname = os.path.join(FIG_DIR, f"noise_suppression_{iso_ts()}_g{g:.3f}_lam{lam:.3f}.png")
    plt.tight_layout(); plt.savefig(fname, dpi=150); plt.close()
    return {
        "snr_in_db": snr_in,
        "snr_out_db": snr_out,
        "delta_snr_db": snr_out - snr_in,
        "figure": fname,
        "pass_snr": (snr_out - snr_in) >= 3.0
    }

def boundedness_experiment(seed, steps, g, lam):
    rng = np.random.default_rng(seed)
    s = rng.uniform(0.0, 1.0, size=steps)
    M = run_filter(s, g, lam, M0=None, rng=rng, noise_std=0.0)
    violations = int(np.sum((M < -1e-12) | (M > 1.0 + 1e-12)))
    return {
        "violations": violations,
        "pass_bounded": violations == 0
    }

def lyapunov_experiment(seed, steps, g, lam):
    rng = np.random.default_rng(seed)
    s = np.ones(steps) * 0.7
    M_star = g * 0.7 / (g + lam) if (g + lam) > 0 else 0.7
    M = run_filter(s, g, lam, M0=0.0, rng=rng, noise_std=0.0)
    F = 0.5 * (M - M_star) ** 2
    dF = np.diff(F)
    # Allow tiny numerical ups due to float
    frac_positive = float(np.mean(dF > 1e-15))
    median_dF = float(np.median(dF))
    # Plot
    t = np.arange(1, steps)
    plt.figure(figsize=(7, 3.5))
    plt.plot(t, dF, 'm-', alpha=0.7)
    plt.axhline(0.0, color='k', linewidth=0.8)
    plt.title(f"Lyapunov ΔF (frac>0 = {frac_positive:.3f}, median={median_dF:.3e})")
    plt.xlabel('t'); plt.ylabel('ΔF')
    fname = os.path.join(FIG_DIR, f"lyapunov_{iso_ts()}_g{g:.3f}_lam{lam:.3f}.png")
    plt.tight_layout(); plt.savefig(fname, dpi=150); plt.close()
    return {
        "frac_positive": frac_positive,
        "median_dF": median_dF,
        "figure": fname,
        "pass_lyapunov": frac_positive <= 0.01 and median_dF < 0.0
    }

def reproducibility_check(seed, steps, g, lam, noise_std=0.0):
    rng1 = np.random.default_rng(seed)
    rng2 = np.random.default_rng(seed)
    s1 = np.ones(steps) * 0.3
    s2 = np.ones(steps) * 0.3
    M1 = run_filter(s1, g, lam, M0=None, rng=rng1, noise_std=noise_std)
    M2 = run_filter(s2, g, lam, M0=None, rng=rng2, noise_std=noise_std)
    max_abs_diff = float(np.max(np.abs(M1 - M2)))
    return {
        "max_abs_diff": max_abs_diff,
        "pass_repro": max_abs_diff <= 1e-12
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--steps", type=int, default=512)
    parser.add_argument("--g", type=float, default=0.12)
    parser.add_argument("--lam", type=float, default=0.08)
    parser.add_argument("--noise_std", type=float, default=0.0)
    args = parser.parse_args()

    ensure_dirs()
    t0 = time.time()

    # Run experiments
    step_res = step_response_experiment(args.seed, args.steps, args.g, args.lam)
    canon = canonical_void_experiment_multi(args.steps)
    noise_res = noise_suppression_experiment(args.seed, args.steps, args.g, args.lam, noise_std=0.05)
    bound_res = boundedness_experiment(args.seed, args.steps, args.g, args.lam)
    lyap_res = lyapunov_experiment(args.seed, args.steps, args.g, args.lam)
    repro_res = reproducibility_check(args.seed, args.steps, args.g, args.lam, noise_std=args.noise_std)

    runtime = time.time() - t0
    p_pred = 1.0 - args.lam - args.g
    metrics = {
        "timestamp": iso_ts(),
        "params": {"seed": args.seed, "steps": args.steps, "g": args.g, "lam": args.lam, "noise_std": args.noise_std},
        "predictions": {
            "pole_pred": p_pred,
            "tau_discrete_pred": (float('inf') if p_pred <= 0 else -1.0 / math.log(max(1e-12, p_pred))),
        },
        "step_response": step_res,
        "canonical_void": canon,
        "noise_suppression": noise_res,
        "boundedness": bound_res,
        "lyapunov": lyap_res,
        "reproducibility": repro_res,
        "performance": {"runtime_s": runtime}
    }

    # Acceptance booleans
    passes = [
        step_res["pass_pole"], step_res["pass_Mstar"], step_res["pass_overshoot"],
        canon["overall_pass"],
        noise_res["pass_snr"],
        bound_res["pass_bounded"],
        lyap_res["pass_lyapunov"],
        repro_res["pass_repro"]
    ]
    metrics["acceptance"] = {
        "checks": {
            "step_pole": step_res["pass_pole"],
            "step_fixed_point": step_res["pass_Mstar"],
            "step_overshoot": step_res["pass_overshoot"],
            "canonical_void_target": canon["overall_pass"],
            "noise_snr_improvement": noise_res["pass_snr"],
            "boundedness": bound_res["pass_bounded"],
            "lyapunov": lyap_res["pass_lyapunov"],
            "reproducibility": repro_res["pass_repro"],
        },
        "overall_pass": all(passes)
    }

    # Save JSON
    out_json = os.path.join(LOG_DIR, f"memory_steering_acceptance_{metrics['timestamp']}.json")
    with open(out_json, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[memory_steering] Acceptance {'PASS' if metrics['acceptance']['overall_pass'] else 'FAIL'}")
    print(f"Log saved: {out_json}")

if __name__ == "__main__":
    main()