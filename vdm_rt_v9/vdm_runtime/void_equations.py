"""
VDM Metriplectic Klein-Gordon Field Equations
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Two coupled telegraph equations derived from the discrete action.

Constants are organized in three categories:
  Category 1 — Free parameters of the action (VDM-AX-004).
               You choose them.  Different values = different physics.
  Category 2 — CF-derived quantities.  Computed FROM category 1.
               Never independently set.
  Category 3 — Engineering proxies.  ELIMINATED.  None exist.

Source: VDM-AX-004, CF01–CF04, CF06, CF11.
"""

from __future__ import annotations

import numpy as np
from typing import List, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: Free parameters of the discrete action (VDM-AX-004)
# These ARE the theory.  You choose them.
# ═══════════════════════════════════════════════════════════════════════════

J_COUPLING: float = 0.0125       # Nearest-neighbor coupling strength
LAMBDA: float = 1.0              # Node GL barrier: V(φ) = λ·φ²(1−φ)²
GAMMA_DAMP: float = 0.5          # M-limb damping coefficient
EPS_BOND: float = 200.0          # Bond telegraph inertia
LAMBDA_BOND: float = 1.0         # Bond GL barrier: U(ψ) = λ_bond·ψ²(1−ψ)²
BETA_DEBT: float = 0.1           # Debt throttle exponent


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: CF-derived quantities (computed, never independently set)
# ═══════════════════════════════════════════════════════════════════════════

A_LATTICE: float = 1.0           # Lattice spacing (= 1 hop)
DT: float = 1.0                  # Timestep (= 1 tick)

C_SQ     = 2.0 * J_COUPLING * A_LATTICE ** 2    # VDM-AX-C02
D_DIFF   = C_SQ / GAMMA_DAMP                     # CF04: D = c²/γ
TAU      = 1.0 / GAMMA_DAMP                      # CF04: τ = 1/γ
C_SIGNAL = float(np.sqrt(D_DIFF / TAU))           # CF04: c = √(D/τ)
TAU_BOND = EPS_BOND * DT ** 2                     # From action variation


# ═══════════════════════════════════════════════════════════════════════════
# Initial condition builders (computational lattice)
# ═══════════════════════════════════════════════════════════════════════════

def build_ring_lattice(N: int, k: int = 3) -> List[Tuple[int, int]]:
    """
    k-nearest-neighbor ring.  Each node connects to i±1, ..., i±k (mod N).
    This is the computational substrate, not the physical topology.
    """
    edges = set()
    for i in range(N):
        for offset in range(1, k + 1):
            j = (i + offset) % N
            edges.add((min(i, j), max(i, j)))
    return sorted(edges)


def build_grid_lattice(Nx: int, Ny: int, Nz: int = 1,
                       periodic: bool = True) -> List[Tuple[int, int]]:
    """
    2D or 3D grid.  Node index: i = x + y*Nx + z*Nx*Ny.
    6-connected in 3D, 4-connected in 2D.
    """
    edges = set()

    def idx(x, y, z):
        return x + y * Nx + z * Nx * Ny

    for z in range(Nz):
        for y in range(Ny):
            for x in range(Nx):
                i = idx(x, y, z)
                if x + 1 < Nx:
                    edges.add((i, idx(x+1, y, z)))
                elif periodic:
                    edges.add((min(i, idx(0, y, z)), max(i, idx(0, y, z))))
                if y + 1 < Ny:
                    edges.add((i, idx(x, y+1, z)))
                elif periodic:
                    edges.add((min(i, idx(x, 0, z)), max(i, idx(x, 0, z))))
                if Nz > 1:
                    if z + 1 < Nz:
                        edges.add((i, idx(x, y, z+1)))
                    elif periodic:
                        edges.add((min(i, idx(x, y, 0)), max(i, idx(x, y, 0))))
    return sorted(edges)


# ═══════════════════════════════════════════════════════════════════════════
# Physics functions
# ═══════════════════════════════════════════════════════════════════════════

def bond_decoherence_floor(kT: float) -> float:
    """η = √(2·kT/ε_bond).  CF07 §4.1."""
    if kT <= 0.0:
        return 0.0
    return float(np.sqrt(2.0 * kT / EPS_BOND))


def bond_weighted_laplacian(
    phi: np.ndarray,
    adj_lists: List[np.ndarray],
    psi: List[np.ndarray],
) -> np.ndarray:
    """(L_ψ φ)_i = Σ_{j∈adj(i)} ψ_ij·(φ_j − φ_i).  CF11 §2.3."""
    N = phi.shape[0]
    out = np.zeros(N, dtype=np.float64)
    for i in range(N):
        nbrs = adj_lists[i]
        if nbrs.size == 0:
            continue
        out[i] = np.sum(psi[i] * (phi[nbrs] - phi[i]))
    return out


def node_potential_derivative(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    """V'(φ) = 2λ·φ(1-φ)(1-2φ).  GL double-well, CF03 §1.1."""
    return 2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)


def node_potential(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    """V(φ) = λ·φ²(1-φ)².  CF03 §1.1."""
    return lam * phi**2 * (1.0 - phi)**2


def bond_potential_derivative(psi: np.ndarray, lam_bond: float = LAMBDA_BOND) -> np.ndarray:
    """U'(ψ) = 2·λ_bond·ψ(1-ψ)(1-2ψ).  CF03 §1.1."""
    return 2.0 * lam_bond * psi * (1.0 - psi) * (1.0 - 2.0 * psi)


def bond_gradient_source(phi_i: float, phi_j: np.ndarray) -> np.ndarray:
    """½(φ_j − φ_i)².  From action variation δS/δψ_ij."""
    return 0.5 * (phi_j - phi_i) ** 2


def get_constants() -> dict:
    """All constants for telemetry / checkpoint."""
    return {
        "J_COUPLING": J_COUPLING, "LAMBDA": LAMBDA,
        "GAMMA_DAMP": GAMMA_DAMP, "EPS_BOND": EPS_BOND,
        "LAMBDA_BOND": LAMBDA_BOND, "BETA_DEBT": BETA_DEBT,
        "TAU": TAU, "D_DIFF": D_DIFF, "C_SQ": C_SQ,
        "C_SIGNAL": C_SIGNAL, "TAU_BOND": TAU_BOND,
    }
