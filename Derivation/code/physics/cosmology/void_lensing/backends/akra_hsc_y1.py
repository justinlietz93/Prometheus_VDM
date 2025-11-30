from __future__ import annotations

"""
Backends for AKRA 2.0 HSC-Y1 convergence (κ) maps — scaffold stub.

This module defines a minimal, import-safe interface for loading AKRA-based
kappa maps for the T2 Void Lensing Cross-Correlation Meter v1.

In the scaffold phase:
- no real I/O is performed;
- no external dependencies are imported; and
- the loader returns (None, metadata) placeholders only.

The upstream AKRA 2.0 pipeline is treated as a black box at T2; see the
Void Lensing T2 proposal and external references for details.
"""

from typing import Any, Dict, Tuple


def load_kappa_map(source: str = "AKRA_HSC_Y1") -> Tuple[None, Dict[str, Any]]:
    """
    Placeholder loader for AKRA HSC-Y1 convergence (κ) maps.

    Parameters
    ----------
    source:
        Identifier for the upstream AKRA map source. Kept as a string to
        allow future variants (e.g. different data releases).

    Returns
    -------
    kappa_map, metadata:
        In the scaffold, kappa_map is always None and metadata is a small
        dictionary describing the backend and implementation status.

    Notes
    -----
    - This function performs no disk or network I/O.
    - It is intended only to document the expected interface for AKRA-based
      backends; real implementations will be added in later sessions.
    """
    metadata: Dict[str, Any] = {
        "backend": source,
        "status": "PENDING_IMPLEMENTATION",
        "description": "AKRA HSC-Y1 κ-map loader stub (no I/O performed).",
    }
    return None, metadata