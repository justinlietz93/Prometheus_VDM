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

There are no separate RE-VGSP and GDSP functions.
There are no topology timers, thresholds, or patience counters.
There are two coupled Klein-Gordon fields (node + bond) with different masses.
No injected noise. kT is measured, not set.
"""

from __future__ import annotations

import numpy as np
from typing import List


# ---------------------------------------------------------------------------
# Free parameters (micro-parameters of the discrete action)
# These instantiate VDM-AX-004. Different values = different physics.
# CF relationships (below) must hold for any valid choice.
# ---------------------------------------------------------------------------
J_COUPLING: float = 0.0125       # Nearest-neighbor coupling in action
LAMBDA: float = 1.0              # Node GL barrier: V(φ) = λ·φ²(1−φ)²
GAMMA_DAMP: float = 0.5          # M-limb damping coefficient
EPS_BOND: float = 200.0          # Bond telegraph inertia (from extended action)
LAMBDA_BOND: float = 1.0         # Bond GL barrier: U(ψ) = λ_bond·ψ²(1−ψ)²
BETA_DEBT: float = 0.1           # Debt throttle exponent

# ---------------------------------------------------------------------------
# CF-derived quantities (computed, not independently chosen)
# You choose J and γ; everything else follows.
# ---------------------------------------------------------------------------
A_LATTICE: float = 1.0
DT: float = 1.0
C_SQ: float = 2.0 * J_COUPLING * A_LATTICE ** 2         # VDM-AX-C02
D_DIFF: float = C_SQ / GAMMA_DAMP                        # VDM-E-050
TAU: float = 1.0 / GAMMA_DAMP                            # CF04 §2.1
C_SIGNAL: float = float(np.sqrt(D_DIFF / TAU))           # CF04 §3.1
TAU_BOND: float = EPS_BOND * DT ** 2                     # From action variation


def bond_decoherence_floor(kT: float) -> float:
    """
    Bond decoherence threshold: √(2·kT/ε_bond).
    Bonds below this are thermally indistinguishable from vacuum.
    Source: CF07 §4.1.
    """
    return float(np.sqrt(2.0 * max(kT, 1e-15) / EPS_BOND))


# ---------------------------------------------------------------------------
# Physics functions
# ---------------------------------------------------------------------------

def bond_weighted_laplacian(
    phi: np.ndarray,
    adj_lists: List[np.ndarray],
    psi: List[np.ndarray],
) -> np.ndarray:
    """
    Bond-weighted discrete Laplacian: (L_ψ φ)_i = Σ_{j∈adj(i)} ψ_ij·(φ_j − φ_i)

    Defined on the connectome graph topology. No spatial embedding assumed.
    Works on any adjacency structure — cubic, scale-free, or self-modifying.

    Source: CF11 §2.3, CF03 §1.1.
    Complexity: O(N·k̄) where k̄ is mean degree.
    """
    N = phi.shape[0]
    out = np.zeros(N, dtype=np.float64)
    for i in range(N):
        nbrs = adj_lists[i]
        if nbrs.size == 0:
            continue
        out[i] = np.sum(psi[i] * (phi[nbrs] - phi[i]))
    return out.astype(np.float32)


def node_potential_derivative(
    phi: np.ndarray,
    lam: float = LAMBDA,
) -> np.ndarray:
    """
    V(φ) = λ·φ²(1−φ)²  →  V'(φ) = 2λ·φ(1−φ)(1−2φ)
    Source: CF03 §1.1.
    """
    return (2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)).astype(np.float32)


def bond_potential_derivative(
    psi_ij: np.ndarray,
    lam_bond: float = LAMBDA_BOND,
) -> np.ndarray:
    """
    U_bond(ψ) = λ_bond·ψ²(1−ψ)²
    U'_bond(ψ) = 2·λ_bond·ψ(1−ψ)(1−2ψ)
    Source: CF03 §1.1 (double-well applied to bond DOF).
    """
    return (
        2.0 * lam_bond * psi_ij * (1.0 - psi_ij) * (1.0 - 2.0 * psi_ij)
    ).astype(np.float32)


def bond_gradient_source(
    phi_i: float,
    phi_j: np.ndarray,
) -> np.ndarray:
    """
    Source term from action variation: ½(φ_j − φ_i)²

    Bonds form where the field has large spatial gradients (domain walls).
    NOT activity coupling. NOT Hebbian. Nodes in the same state produce
    zero source. Nodes straddling a domain wall produce maximum source.
    Source: extended action (§0.1b), variation δS/δψ_ij.
    """
    return (0.5 * (phi_j - phi_i) ** 2).astype(np.float32)


def klein_gordon_rhs(
    phi: np.ndarray,
    adj_lists: List[np.ndarray],
    psi: List[np.ndarray],
    lam: float = LAMBDA,
    D: float = D_DIFF,
) -> np.ndarray:
    """
    Node field RHS: rhs = D·L_ψ(φ) − V'(φ)

    No injected noise. Endogenous fluctuations from J/M split,
    tachyonic instability, Laplacian coupling on self-modifying graph.
    Source: VDM-AX-004, CF01 §4.1, CF11 §2.3, CF04 §3.1, CF03 §1.1.
    """
    transport = D * bond_weighted_laplacian(phi, adj_lists, psi)
    dV = node_potential_derivative(phi, lam)
    return transport - dV


def get_constants() -> dict:
    """Return all constants for telemetry / checkpoint."""
    return {
        "J_COUPLING": J_COUPLING,
        "LAMBDA": LAMBDA,
        "GAMMA_DAMP": GAMMA_DAMP,
        "EPS_BOND": EPS_BOND,
        "LAMBDA_BOND": LAMBDA_BOND,
        "BETA_DEBT": BETA_DEBT,
        "TAU": TAU,
        "D_DIFF": D_DIFF,
        "C_SQ": C_SQ,
        "C_SIGNAL": C_SIGNAL,
        "TAU_BOND": TAU_BOND,
    }
