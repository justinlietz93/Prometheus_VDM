#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Self-contained RD solver for the CEG package.

Provides:
- ``reaction_exact_step``: exact logistic ODE update (no imports needed)
- ``laplacian_periodic_1d``: periodic 3-point stencil Laplacian
- ``discrete_lyapunov_Lh``: discrete Lyapunov functional
- ``dg_rd_step_with_stats``: discrete-gradient RD implicit Newton step

These are extracted from Derivation/code/physics/rd_conservation and
physics/reaction_diffusion with all external imports removed so the
package is self-contained.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

import numpy as np

ArrayLike = Union[float, np.ndarray]


# ---------------------------------------------------------------------------
# Exact logistic reaction step
# ---------------------------------------------------------------------------

def reaction_exact_step(
    W: ArrayLike,
    r: ArrayLike,
    u: ArrayLike,
    dt: ArrayLike,
    clip_eps: float = 1e-12,
    dtype: Optional[np.dtype] = None,
) -> np.ndarray:
    """Exact logistic reaction step: dW/dt = r W - u W²."""
    x = np.array(W, dtype=dtype if dtype is not None else np.float64)
    r_arr = np.array(r, dtype=x.dtype)
    u_arr = np.array(u, dtype=x.dtype)
    dt_arr = np.array(dt, dtype=x.dtype)

    s = np.expm1(r_arr * dt_arr)
    e = s + 1.0

    u_zero = np.isclose(u_arr, 0.0)

    denom = u_arr * x * s + r_arr
    if np.isscalar(denom):
        if abs(denom) < clip_eps:
            denom = np.sign(denom) * clip_eps if denom != 0 else clip_eps
    else:
        zero_mask = np.isclose(denom, 0.0, atol=clip_eps, rtol=0.0)
        denom = np.where(zero_mask, np.where(denom > 0, clip_eps, -clip_eps), denom)

    num = r_arr * x * e
    W_next = num / denom

    if np.any(u_zero):
        W_lin = x * e
        mask = u_zero
        if not np.array(mask).shape == x.shape:
            mask = np.broadcast_to(mask, x.shape)
        W_next = np.where(mask, W_lin, W_next)

    return W_next


# ---------------------------------------------------------------------------
# Periodic Laplacian (3-point stencil)
# ---------------------------------------------------------------------------

def laplacian_periodic_1d(u: np.ndarray, dx: float) -> np.ndarray:
    """3-point periodic finite-difference Laplacian."""
    return (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx * dx)


# ---------------------------------------------------------------------------
# Discrete Lyapunov functional
# ---------------------------------------------------------------------------

def _energy_potential_Vhat(W: np.ndarray, r: float, ucoef: float) -> np.ndarray:
    """Potential energy density for RD Lyapunov functional."""
    return -(r / 2.0) * (W * W) + (ucoef / 3.0) * (W * W * W)


def discrete_lyapunov_Lh(W: np.ndarray, dx: float, D: float, r: float, ucoef: float) -> float:
    """Edge-based discrete Lyapunov functional consistent with 3-point Laplacian."""
    diff = (np.roll(W, -1) - W) / dx
    grad_sq = diff * diff
    return float(np.sum(0.5 * D * grad_sq + _energy_potential_Vhat(W, r, ucoef)) * dx)


# ---------------------------------------------------------------------------
# DG RD step (Newton + backtracking)
# ---------------------------------------------------------------------------

def dg_rd_step_with_stats(
    Wn: np.ndarray,
    dt: float,
    dx: float,
    D: float,
    r: float,
    u: float,
    tol: float = 1e-12,
    max_iter: int = 20,
    max_backtracks: int = 10,
    lap_operator: str = "stencil",
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Discrete-gradient RD implicit step (AVF reaction, midpoint Laplacian), Newton solve.

    Parameters
    ----------
    Wn : ndarray
        Current state (shape: (N,)).
    dt : float
        Time step.
    dx : float
        Grid spacing.
    D : float
        Diffusion coefficient.
    r : float
        Reaction rate.
    u : float
        Saturation coefficient.
    tol : float
        Newton convergence tolerance (inf-norm of residual).
    max_iter : int
        Maximum Newton iterations.
    max_backtracks : int
        Maximum backtracking steps per Newton iteration.
    lap_operator : str
        ``'stencil'`` (3-pt periodic) or ``'spectral'`` (FFT circulant).

    Returns
    -------
    (W1, stats) where W1 is the updated state and stats is a diagnostic dict.
    """
    N = Wn.size
    W1 = Wn.copy()
    stats: Dict[str, Any] = {"iters": 0, "final_residual_inf": None, "backtracks": 0, "converged": False}

    lap_mode = str(lap_operator or "stencil").lower()
    if lap_mode == "spectral":
        k_cyc = np.fft.fftfreq(N, d=dx)
        omega_sq = (2.0 * np.pi) ** 2 * (k_cyc ** 2)
        lam_spec = -omega_sq
        kernel = np.fft.ifft(lam_spec).real
        C_spec = np.empty((N, N), dtype=float)
        for i in range(N):
            C_spec[i, :] = np.roll(kernel, i)

        def lap(x: np.ndarray) -> np.ndarray:
            return C_spec @ x
    else:
        C_spec = None

        def lap(x: np.ndarray) -> np.ndarray:
            return laplacian_periodic_1d(x, dx)

    for it in range(1, max_iter + 1):
        mid = 0.5 * (W1 + Wn)
        dW = W1 - Wn
        over_f = r * (Wn + 0.5 * dW) - u * ((Wn * Wn + Wn * W1 + W1 * W1) / 3.0)
        F = W1 - Wn - dt * (D * lap(mid) + over_f)
        res = float(np.linalg.norm(F, ord=np.inf))
        if res <= tol:
            stats.update({"iters": it, "final_residual_inf": res, "converged": True})
            break

        # Build dense Jacobian
        J = np.eye(N)
        if lap_mode == "spectral":
            J += (-dt * 0.5 * D) * C_spec
        else:
            coeff = -dt * 0.5 * D / (dx * dx)
            for i in range(N):
                J[i, i] += -coeff * (-2.0)
                J[i, (i - 1) % N] += -coeff * 1.0
                J[i, (i + 1) % N] += -coeff * 1.0
        diag_add = -dt * (0.5 * r - u * (Wn / 3.0 + (2.0 / 3.0) * W1))
        J[np.arange(N), np.arange(N)] += diag_add

        d = np.linalg.solve(J, -F)

        # Backtracking line search
        step = 1.0
        W_trial = W1 + step * d
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
        stats.update({"iters": it, "final_residual_inf": res_t})
        if np.linalg.norm(step * d, ord=np.inf) <= tol * 0.1:
            stats["converged"] = True
            break

    return W1, stats


__all__ = [
    "reaction_exact_step",
    "laplacian_periodic_1d",
    "discrete_lyapunov_Lh",
    "dg_rd_step_with_stats",
]
