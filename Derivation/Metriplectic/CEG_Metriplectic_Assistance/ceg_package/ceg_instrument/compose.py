#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Metriplectic composition utilities (self-contained, local imports only):
 - M-only: DG RD step
 - J-only: spectral advection J step
 - J ⊕ M (Strang): J(dt/2) → M(dt) → J(dt/2)
"""
from __future__ import annotations

from typing import Dict, Any, Tuple

import numpy as np

from .j_step import j_step_spectral_periodic
from .rd_solver import dg_rd_step_with_stats, discrete_lyapunov_Lh
from .kg_ops import spectral_grad


def m_step_dg(W: np.ndarray, dt: float, dx: float, D: float, r: float, u: float) -> np.ndarray:
    """DG RD dissipative step (wrapper)."""
    W1, _stats = dg_rd_step_with_stats(W, dt, dx, D, r, u)
    return W1


def j_only_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    return j_step_spectral_periodic(W, dt, dx, float(params.get("c", 1.0)))


def m_only_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    return m_step_dg(W, dt, dx, float(params["D"]), float(params["r"]), float(params["u"]))


def m_only_step_with_stats(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    tol = float(params.get("dg_tol", 1e-12))
    max_iter = int(params.get("dg_max_iter", 20))
    max_backtracks = int(params.get("dg_max_backtracks", 10))
    lap_operator = str(params.get("m_lap_operator", "stencil"))
    return dg_rd_step_with_stats(
        W, dt, dx,
        float(params["D"]), float(params["r"]), float(params["u"]),
        tol=tol, max_iter=max_iter, max_backtracks=max_backtracks,
        lap_operator=lap_operator,
    )


def jmj_strang_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    """Strang composition: J(dt/2) → M(dt) → J(dt/2)."""
    W1 = j_only_step(W, 0.5 * dt, dx, params)
    W2 = m_only_step(W1, dt, dx, params)
    W3 = j_only_step(W2, 0.5 * dt, dx, params)
    return W3


def jmj_strang_step_with_stats(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Strang composition with Newton stats."""
    W1 = j_only_step(W, 0.5 * dt, dx, params)
    W2, stats = m_only_step_with_stats(W1, dt, dx, params)
    W3 = j_only_step(W2, 0.5 * dt, dx, params)
    return W3, stats


def mjm_strang_step(W: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> np.ndarray:
    """Reverse Strang: M(dt/2) → J(dt) → M(dt/2)."""
    W1, _ = m_only_step_with_stats(W, 0.5 * dt, dx, params)
    W2 = j_only_step(W1, dt, dx, params)
    W3, _ = m_only_step_with_stats(W2, 0.5 * dt, dx, params)
    return W3


def lyapunov_values(W: np.ndarray, dx: float, D: float, r: float, u: float) -> float:
    return discrete_lyapunov_Lh(W, dx, D, r, u)


def lyapunov_values_consistent(W: np.ndarray, dx: float, D: float, r: float, u: float, lap_operator: str | None = None) -> float:
    """Lyapunov functional consistent with the chosen Laplacian."""
    mode = str(lap_operator or "stencil").lower()
    if mode == "spectral":
        g = spectral_grad(W, dx)
        Vhat = -(r / 2.0) * (W ** 2) + (u / 3.0) * (W ** 3)
        return float(np.sum(0.5 * D * (g * g) + Vhat) * dx)
    else:
        return discrete_lyapunov_Lh(W, dx, D, r, u)


__all__ = [
    "j_only_step", "m_only_step", "m_only_step_with_stats",
    "jmj_strang_step", "jmj_strang_step_with_stats", "mjm_strang_step",
    "lyapunov_values", "lyapunov_values_consistent",
]
