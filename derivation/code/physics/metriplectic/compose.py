#!/usr/bin/env python3
"""
Metriplectic composition utilities:
 - M-only: reuse DG RD step from RD harness
 - J-only: spectral advection J step
 - J ⊕ M (Strang): J(dt/2) → M(dt) → J(dt/2)
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict, Any
import numpy as np

# Ensure code root on path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Local imports
from physics.metriplectic.j_step import j_step_spectral_periodic
from physics.rd_conservation.run_rd_conservation import dg_rd_step, laplacian_periodic_1d, discrete_lyapunov_Lh


def m_step_dg(W: np.ndarray, dt: float, dx: float, D: float, r: float, u: float) -> np.ndarray:
    """DG RD dissipative step (wrapper)."""
    return dg_rd_step(W, dt, dx, D, r, u)


def j_only_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    return j_step_spectral_periodic(W, dt, dx, float(params.get("c", 1.0)))


def m_only_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    return m_step_dg(W, dt, dx, float(params["D"]), float(params["r"]), float(params["u"]))


def jmj_strang_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    """Strang composition: J(dt/2) → M(dt) → J(dt/2)."""
    W1 = j_only_step(W, 0.5 * dt, dx, params)
    W2 = m_only_step(W1, dt, dx, params)
    W3 = j_only_step(W2, 0.5 * dt, dx, params)
    return W3


def two_grid_error_inf(step_fn, W0: np.ndarray, dt: float) -> float:
    W_big = step_fn(W0, dt)
    W_h1 = step_fn(W0, 0.5 * dt)
    W_h2 = step_fn(W_h1, 0.5 * dt)
    return float(np.linalg.norm(W_big - W_h2, ord=np.inf))


def lyapunov_values(W: np.ndarray, dx: float, D: float, r: float, u: float) -> float:
    return discrete_lyapunov_Lh(W, dx, D, r, u)


__all__ = [
    "j_only_step", "m_only_step", "jmj_strang_step", "two_grid_error_inf", "lyapunov_values"
]
