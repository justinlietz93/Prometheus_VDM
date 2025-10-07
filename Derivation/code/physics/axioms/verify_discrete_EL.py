#!/usr/bin/env python3
"""
Verify the 2J coefficient in the discrete Euler-Lagrange equation arising from the
spatial interaction term in the discrete action:

  S_spatial = - (J/2) ∑_i ∑_{j∈N(i)} (W_j - W_i)^2

By direct variation, one obtains
  ∂(S_spatial)/∂W_i = + 2 J ∑_{j∈N(i)} (W_j - W_i)

Equivalently, for the spatial "potential" (positive) energy
  U_int(W) := (J/2) ∑_i ∑_{j∈N(i)} (W_j - W_i)^2,

the gradient satisfies
  ∂U_int/∂W_i = - 2 J ∑_{j∈N(i)} (W_j - W_i).

This script numerically checks the gradient identity above in 1D and 2D on
periodic lattices by finite differences and compares to the analytic formula.

Author: Justin K. Lietz
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def neighbor_sum_1d(W: np.ndarray) -> np.ndarray:
    """
    ∑_{j∈N(i)} (W_j - W_i) on a 1D ring (periodic).
    N(i) = {i-1, i+1}.
    """
    right = np.roll(W, -1)
    left  = np.roll(W,  1)
    return (right - W) + (left - W)  # = right + left - 2W


def neighbor_sum_2d(W: np.ndarray) -> np.ndarray:
    """
    ∑_{j∈N(i)} (W_j - W_i) on a 2D torus (periodic).
    N(i) = von Neumann (north,south,east,west).
    """
    north = np.roll(W, -1, axis=0)
    south = np.roll(W,  1, axis=0)
    east  = np.roll(W, -1, axis=1)
    west  = np.roll(W,  1, axis=1)
    return (north - W) + (south - W) + (east - W) + (west - W)  # = sum(neigh) - 4W


def U_int_1d(W: np.ndarray, J: float) -> float:
    """
    U_int = (J/2) ∑_i ∑_{j∈N(i)} (W_j - W_i)^2, with 1D periodic neighbors.
    """
    right = np.roll(W, -1)
    left  = np.roll(W,  1)
    E = 0.5 * J * (np.sum((right - W)**2) + np.sum((left - W)**2))
    return float(E)


def U_int_2d(W: np.ndarray, J: float) -> float:
    """
    U_int = (J/2) ∑_i ∑_{j∈N(i)} (W_j - W_i)^2, with 2D periodic neighbors (4-neighborhood).
    """
    north = np.roll(W, -1, axis=0)
    south = np.roll(W,  1, axis=0)
    east  = np.roll(W, -1, axis=1)
    west  = np.roll(W,  1, axis=1)
    E = 0.5 * J * (
        np.sum((north - W)**2) + np.sum((south - W)**2) +
        np.sum((east  - W)**2) + np.sum((west  - W)**2)
    )
    return float(E)


def numeric_grad(U_fn, W: np.ndarray, J: float, eps: float = 1e-6) -> np.ndarray:
    """
    Central finite-difference gradient of U wrt W.
    """
    g = np.zeros_like(W, dtype=float)
    it = np.nditer(W, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        idx = it.multi_index
        orig = W[idx]
        W[idx] = orig + eps
        Up = U_fn(W, J)
        W[idx] = orig - eps
        Um = U_fn(W, J)
        W[idx] = orig
        g[idx] = (Up - Um) / (2*eps)
        it.iternext()
    return g


def verify_1d(N: int = 31, J: float = 0.7, seed: int = 0) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    W = rng.standard_normal(N)
    # Analytic gradient: ∂U/∂W = -2J ∑_{j∈N(i)} (W_j - W_i)
    g_ana = -2.0 * J * neighbor_sum_1d(W)
    g_num = numeric_grad(U_int_1d, W.copy(), J)
    max_abs = float(np.max(np.abs(g_ana - g_num)))
    rel = float(max_abs / (np.max(np.abs(g_num)) + 1e-12))
    return max_abs, rel


def verify_2d(Ny: int = 17, Nx: int = 23, J: float = 0.7, seed: int = 1) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((Ny, Nx))
    g_ana = -2.0 * J * neighbor_sum_2d(W)
    g_num = numeric_grad(U_int_2d, W.copy(), J)
    max_abs = float(np.max(np.abs(g_ana - g_num)))
    rel = float(max_abs / (np.max(np.abs(g_num)) + 1e-12))
    return max_abs, rel


if __name__ == "__main__":
    max_abs_1d, rel_1d = verify_1d()
    print("1D: max_abs =", max_abs_1d, "rel =", rel_1d)
    assert max_abs_1d < 1e-6

    max_abs_2d, rel_2d = verify_2d()
    print("2D: max_abs =", max_abs_2d, "rel =", rel_2d)
    assert max_abs_2d < 1e-6

    print("verify_discrete_EL: 2J coefficient check PASSED")