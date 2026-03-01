"""
VDM v8 Physics Core — Metriplectic Klein-Gordon on Self-Modifying Graph
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Two coupled telegraph fields (node φ, bond ψ) + gauge excitations.
Everything derived from the discrete action via QGT decomposition.
"""
from .connectome import Connectome
from .void_equations import get_constants
from .connectome import Connectome
from .engram import save_engram, load_engram

__all__ = [
    "Connectome",
    "get_constants",
    "save_engram",
    "load_engram",
]
