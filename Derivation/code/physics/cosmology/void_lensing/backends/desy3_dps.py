from __future__ import annotations

"""
Backends for DES-Y3 diffusion-prior (DPS) convergence (κ) maps — scaffold stub.

This module defines a minimal, import-safe interface for loading DPS-based
kappa maps for the T2 Void Lensing Cross-Correlation Meter v1.

In the scaffold phase:
- no real I/O is performed;
- no external dependencies are imported; and
- the loader returns (None, metadata) placeholders only.

The upstream DES-Y3 DPS mass-mapping pipeline is treated as a black box at T2;
see the Void Lensing T2 proposal and external references for details.
"""

from typing import Any, Dict, Tuple


def load_kappa_map(source: str = "DESY3_DPS") -> Tuple[None, Dict[str, Any]]:
    """
    Placeholder loader for DES-Y3 DPS convergence (κ) maps.

    Parameters
    ----------
    source:
        Identifier for the upstream DPS map source. Kept as a string to
        allow future variants (e.g. different data releases).

    Returns
    -------
    kappa_map, metadata:
        In the scaffold, kappa_map is always None and metadata is a small
        dictionary describing the backend and implementation status.

    Notes
    -----
    - This function performs no disk or network I/O.
    - It is intended only to document the expected interface for DPS-based
      backends; real implementations will be added in later sessions.
    """
    metadata: Dict[str, Any] = {
        "backend": source,
        "status": "PENDING_IMPLEMENTATION",
        "description": "DES-Y3 DPS κ-map loader stub (no I/O performed).",
    }
    return None, metadata