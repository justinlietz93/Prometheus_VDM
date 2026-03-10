"""
VDM Metriplectic Klein-Gordon Field Equations
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Two coupled equations of motion derived from:
  CF01 (QGT → metriplectic brackets)
  CF02 (GENERIC two-generator structure — J and M simultaneous)
  CF03 (double-well potential, Ginzburg-Landau, for both φ and ψ)
  CF04 (telegraph-Fisher finite-speed transport, causal cone)
  CF06 (fluctuation-dissipation from information geometry)
  CF11 (metriplectic damped Klein-Gordon)

There are no separate "RE-VGSP" and "GDSP" functions.
There are no topology timers, thresholds, or patience counters.
There are two coupled Klein-Gordon fields (node + bond) with different masses.
"""

from __future__ import annotations
import numpy as np

TAU = 2.0
BETA = 0.1
LAMBDA = 1.0
GAMMA = 0.05
KT_EFF = 0.001
EPS_TOPO = 0.01
ETA_BOND_FLOOR = float(np.sqrt(2.0 * EPS_TOPO * KT_EFF))


def bond_weighted_laplacian(phi: np.ndarray, adj_lists: list[np.ndarray], psi: list[np.ndarray]) -> np.ndarray:
    N = phi.shape[0]
    out = np.zeros(N, dtype=np.float64)
    for i in range(N):
        nbrs = adj_lists[i]
        if nbrs.size == 0:
            continue
        out[i] = np.sum(psi[i] * (phi[nbrs] - phi[i]))
    return out.astype(np.float32)


def node_potential_derivative(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    return (2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)).astype(np.float32)


def bond_potential_derivative(
    psi_ij: np.ndarray,
    phi_dot_i: float,
    phi_dot_j: np.ndarray,
    lam: float = LAMBDA,
    eps: float = EPS_TOPO,
) -> np.ndarray:
    dwell = 2.0 * lam * psi_ij * (1.0 - psi_ij) * (1.0 - 2.0 * psi_ij)
    activity = eps * np.abs(phi_dot_i) * np.abs(phi_dot_j)
    return (dwell - activity).astype(np.float32)


def klein_gordon_rhs(
    phi: np.ndarray,
    adj_lists: list[np.ndarray],
    psi: list[np.ndarray],
    lam: float = LAMBDA,
    D: float = GAMMA,
    kT: float = KT_EFF,
) -> np.ndarray:
    transport = D * bond_weighted_laplacian(phi, adj_lists, psi)
    dV = node_potential_derivative(phi, lam)
    noise = np.sqrt(2.0 * D * kT) * np.random.standard_normal(phi.shape).astype(np.float32)
    return transport - dV + noise


def get_constants() -> dict:
    return {
        "TAU": TAU,
        "BETA": BETA,
        "LAMBDA": LAMBDA,
        "GAMMA": GAMMA,
        "KT_EFF": KT_EFF,
        "EPS_TOPO": EPS_TOPO,
    }
