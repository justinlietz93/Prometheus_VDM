"""
Adapter layer for Void Equations. No fallbacks. No proxy code.
If Void_Equations.py cannot be imported, the runtime must crash.
"""
from vdm_rt.core.Void_Equations import (
    klein_gordon_rhs,
    bond_weighted_laplacian,
    node_potential_derivative,
    bond_potential_derivative,
    get_constants,
    TAU, BETA, LAMBDA, GAMMA, KT_EFF, EPS_TOPO,
    ETA_BOND_FLOOR,
)

__all__ = [
    "klein_gordon_rhs",
    "bond_weighted_laplacian",
    "node_potential_derivative",
    "bond_potential_derivative",
    "get_constants",
    "TAU", "BETA", "LAMBDA", "GAMMA", "KT_EFF", "EPS_TOPO",
    "ETA_BOND_FLOOR",
]
