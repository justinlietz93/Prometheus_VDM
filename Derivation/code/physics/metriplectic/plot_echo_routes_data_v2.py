#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Ensure code root on path (mirror runner convention)
import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Import the same instruments used by the experiment logic (do not change core)
from physics.metriplectic.kg_ops import kg_verlet_step
from physics.metriplectic.compose import m_only_step_with_stats
from physics.metriplectic import assisted_echo as AE
from physics.metriplectic.echo_metrics import h_energy_norm_delta


@dataclass
class EchoSpecLite:
    grid: Dict[str, float]
    params: Dict[str, float]
    dt: float
    steps: int
    seeds: List[int]
    lambdas: List[float]
    budget: float


def load_spec(spec_path: Path) -> EchoSpecLite:
    raw = json.loads(spec_path.read_text(encoding="utf-8"))
    return EchoSpecLite(
        grid=raw["grid"],
        params=raw["params"],
        dt=float(raw["dt"]),
        steps=int(raw["steps"]),
        seeds=[int(s) for s in raw["seeds"]],
        lambdas=[float(l) for l in raw["lambdas"]],
        budget=float(raw["budget"]),
    )


def first_fourier_mode_real(x: np.ndarray) -> float:
    """
    Real part of first positive Fourier coefficient (k=1) with unitary-like scaling.
    This gives a consistent 1D scalar coordinate for plotting.
    """
    N = x.size
    # rfft returns length N//2+1, index 1 is k=1
    c1 = np.fft.rfft(x)[1] / N
    return float(np.real(c1))


def j_only_omega2_for_k1(N: int, dx: float, c: float, m: float) -> float:
    """
    Angular frequency squared for the first Fourier mode under J-only KG:
    H_mode = 1/2 (pi1^2 + omega1^2 * phi1^2).
    Use continuum wave number k=2π/(N*dx) for overlay.
    """
    k = 2.0 * np.pi / (N * dx)
    return float(m * m + (c * c) * (k * k))


def forward_trajectory_phi1_pi1(phi0: np.ndarray, pi0: np.ndarray, dt: float, dx: float, steps: int, params: Dict[str, float]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Reproduce the forward JMJ integration used by the runner and record (phi1, pi1) at each step.
    """
    ph, pr = phi0.copy(), pi0.copy()
    N = ph.size
    xs: List[float] = []
    ys: List[float] = []
    for _ in range(steps):
        # Use the exact helper from the experiment for forward Strang step
        ph, pr = AE._jmj_step(ph, pr, dt, dx, params)
        xs.append(first_fourier_mode_real(ph))
        ys.append(first_fourier_mode_real(pr))
    return np.array(xs, dtype=float), np.array(ys, dtype=float)


def reverse_path_phi1_pi1_baseline(phiF: np.ndarray, piF: np.ndarray, dt: float, dx: float, steps: int, params: Dict[str, float], rng: np.random.Generator, work_per_step: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Baseline reverse phase (random corrections) exactly matching experiment sequence,
    while recording a dense path in (phi1, pi1).
    """
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    ph, pr = phiF.copy(), piF.copy()
    xs: List[float] = []
    ys: List[float] = []

    work_sum = 0.0
    for _ in range(steps):
        # J half backward
        ph, pr = kg_verlet_step(ph, pr, -0.5 * dt, dx, c, m)
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

        # Clamp remaining budget and draw random H-norm-scaled correction
        remaining = float(steps * work_per_step - work_sum)
        target = float(max(0.0, min(work_per_step, remaining)))
        dphi, dpi = AE._random_correction_pair(rng, ph, pr, dx, target, c, m)
        # Account work based on the same H-norm metric
        zph = np.zeros_like(dphi); zpi = np.zeros_like(dpi)
        work_sum += float(h_energy_norm_delta(dphi, dpi, zph, zpi, dx, c, m))
        # Apply assistance
        ph = ph + dphi; pr = pr + dpi
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

        # Reverse-phase M forward dt on phi only (same as experiment)
        ph, _ = m_only_step_with_stats(ph, dt, dx, params)
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

        # J half backward
        ph, pr = kg_verlet_step(ph, pr, -0.5 * dt, dx, c, m)
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

    return np.array(xs, dtype=float), np.array(ys, dtype=float)


def reverse_path_phi1_pi1_assisted(phiF: np.ndarray, piF: np.ndarray, dt: float, dx: float, steps: int, params: Dict[str, float], phi_ref: np.ndarray, pi_ref: np.ndarray, work_per_step: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Assisted reverse phase (model-aware corrections) exactly matching experiment sequence,
    while recording a dense path in (phi1, pi1).
    """
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    ph, pr = phiF.copy(), piF.copy()
    xs: List[float] = []
    ys: List[float] = []

    work_sum = 0.0
    for _ in range(steps):
        # J half backward
        ph, pr = kg_verlet_step(ph, pr, -0.5 * dt, dx, c, m)
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

        # Clamp remaining and apply model-aware assistance
        remaining = float(steps * work_per_step - work_sum)
        target = float(max(0.0, min(work_per_step, remaining)))
        dphi, dpi = AE._assist_correction_pair(ph, pr, phi_ref, pi_ref, dx, params, work=target, c=c, m=m)
        # Account work
        zph = np.zeros_like(dphi); zpi = np.zeros_like(dpi)
        work_sum += float(h_energy_norm_delta(dphi, dpi, zph, zpi, dx, c, m))
        ph = ph + dphi; pr = pr + dpi
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

        # Reverse-phase M forward dt on phi only
        ph, _ = m_only_step_with_stats(ph, dt, dx, params)
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

        # J half backward
        ph, pr = kg_verlet_step(ph, pr, -0.5 * dt, dx, c, m)
        xs.append(first_fourier_mode_real(ph)); ys.append(first_fourier_mode_real(pr))

    return np.array(xs, dtype=float), np.array(ys, dtype=float)


def main() -> int:
    # Load the same spec used by the run
    spec_path = Path("Derivation/code/physics/metriplectic/specs/assisted_echo.v1c.json")
    spec = load_spec(spec_path)
    N = int(spec.grid["N"]); dx = float(spec.grid["dx"]); dt = float(spec.dt)
    c = float(spec.params.get("c", 1.0)); m = float(spec.params.get("m", 0.0))
    steps = int(spec.steps)

    # Choose λ* as the max lambda in the v1c sweep (as in summary pass)
    lam_star = max(spec.lambdas)
    work_per_step = float(lam_star) * float(spec.budget)

    # Use the first seed in the prereg seeds list (representative trajectory)
    seed = int(spec.seeds[0])
    rng = np.random.default_rng(seed)

    # Reconstruct initial condition exactly as the runner does
    phi0 = rng.random(N).astype(float) * 0.1
    pi0  = rng.random(N).astype(float) * 0.1

    # Forward trajectory (JMJ)
    f_x, f_y = forward_trajectory_phi1_pi1(phi0, pi0, dt, dx, steps, spec.params)
    # Final state after forward pass (for reverse start)
    # Recompute deterministically using the same loop to get phiF, piF
    ph, pr = phi0.copy(), pi0.copy()
    for _ in range(steps):
        ph, pr = AE._jmj_step(ph, pr, dt, dx, spec.params)
    phiF, piF = ph, pr

    # Reverse baseline trajectory (dense)
    rb_x, rb_y = reverse_path_phi1_pi1_baseline(phiF, piF, dt, dx, steps, spec.params, rng, work_per_step)

    # Reverse assisted trajectory (dense), using phi0,pi0 as reference as in experiment
    ra_x, ra_y = reverse_path_phi1_pi1_assisted(phiF, piF, dt, dx, steps, spec.params, phi0, pi0, work_per_step)

    # Build J-only Hamiltonian contours in (phi1, pi1) plane
    w2 = j_only_omega2_for_k1(N, dx, c, m)

    # Determine plotting extents from data
    all_x = np.concatenate([f_x, rb_x, ra_x])
    all_y = np.concatenate([f_y, rb_y, ra_y])
    x_min, x_max = float(all_x.min()), float(all_x.max())
    y_min, y_max = float(all_y.min()), float(all_y.max())
    xr = x_max - x_min if x_max > x_min else 1.0
    yr = y_max - y_min if y_max > y_min else 1.0
    pad_x = 0.08 * xr
    pad_y = 0.08 * yr

    xs = np.linspace(x_min - pad_x, x_max + pad_x, 240)
    ys = np.linspace(y_min - pad_y, y_max + pad_y, 220)
    X, Y = np.meshgrid(xs, ys)
    H = 0.5 * (Y * Y + w2 * X * X)

    # Plot
    fig, ax = plt.subplots(figsize=(7.8, 5.8), dpi=150)
    cs = ax.contour(X, Y, H, levels=16, cmap="viridis", alpha=0.9, linewidths=1.0)
    try:
        ax.clabel(cs, inline=True, fmt="%.2f", fontsize=7, inline_spacing=3)
    except Exception:
        pass

    # Trajectories
    ax.plot(f_x, f_y, color="#f4a300", lw=2.4, label="forward (JMJ)")
    ax.plot(rb_x, rb_y, color="#1f77b4", lw=2.0, ls="--", label=f"reverse baseline (λ={lam_star:g})")
    ax.plot(ra_x, ra_y, color="#1aa188", lw=2.2, ls="dashdot", label=f"reverse assisted (λ={lam_star:g})")

    # Key points
    ax.scatter([f_x[-1]], [f_y[-1]], c="k", s=22, zorder=5)
    ax.annotate(r"$E_{\mathrm{baseline}}$", xy=(f_x[-1], f_y[-1]), xytext=(6, 2), textcoords="offset points", fontsize=9)
    ax.scatter([f_x[0]], [f_y[0]], c="k", s=22, zorder=5)
    ax.annotate("z0", xy=(f_x[0], f_y[0]), xytext=(6, 0), textcoords="offset points", fontsize=9)

    # Aesthetics
    ax.set_xlabel(r"first Fourier mode $\,\phi_1\,$")
    ax.set_ylabel(r"first Fourier mode $\,\pi_1\,$")
    ax.set_title("VDM echo (data-driven): baseline miss vs assisted rewind in ($\\phi_1,\\pi_1$)")
    ax.grid(True, ls="--", alpha=0.35)
    ax.legend(loc="upper right", frameon=True)

    ax.set_xlim(xs.min(), xs.max()); ax.set_ylim(ys.min(), ys.max())
    fig.tight_layout()

    out_path = Path("Derivation/Metriplectic/vdm_echo_landscape_v2.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor="white")
    plt.close(fig)

    print(json.dumps({"figure": str(out_path), "seed": seed, "lambda": lam_star, "omega2_k1": w2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())