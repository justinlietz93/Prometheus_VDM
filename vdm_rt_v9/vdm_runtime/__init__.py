"""
VDM v9 Physics Core — Metriplectic Klein-Gordon on Self-Modifying Graph
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Two coupled telegraph fields (node φ, bond ψ) + gauge excitations.
Derived from the discrete action (VDM-AX-004) via CF01–CF11.

Runtime only.  CFN validation notebooks are separate.
"""
from .connectome import Connectome
from .void_equations import (
    LatticeDefinition,
    LatticeEdge,
    build_grid_lattice,
    build_grid_lattice_spec,
    build_ring_lattice,
    build_ring_lattice_spec,
    get_constants,
)

__all__ = [
    "Connectome",
    "LatticeDefinition",
    "LatticeEdge",
    "get_constants",
    "build_ring_lattice",
    "build_ring_lattice_spec",
    "build_grid_lattice",
    "build_grid_lattice_spec",
]
