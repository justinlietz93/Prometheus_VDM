from __future__ import annotations

"""
Mock backends for void-lensing κ maps and void catalogues — scaffold stub.

This module defines minimal, import-safe interfaces for loading synthetic
kappa maps and void catalogues for the T2 Void Lensing Cross-Correlation
Meter v1.

In the scaffold phase:
- no real I/O is performed;
- no external dependencies are imported; and
- all loaders return (None, metadata) placeholders only.

Upstream mock suites (e.g. PyTwinPeaks tunnel-void catalogues,
morphology-weighted SBI, DESI n(z) calibrations) are treated as black
boxes at T2; this module only documents expected interfaces.
"""

from typing import Any, Dict, Tuple


def load_mock_suite(suite_name: str = "void_lensing_meter-mocks-v1") -> Tuple[None, Dict[str, Any]]:
    """
    Placeholder loader for a suite of synthetic void-lensing mocks.

    Parameters
    ----------
    suite_name:
        Identifier for the mock suite configuration (e.g. matches the
        spec file name under `specs/void_lensing_meter-mocks-v1.json`).

    Returns
    -------
    mock_bundle, metadata:
        In the scaffold, `mock_bundle` is always None and `metadata` is a
        small dictionary describing the backend and implementation status.

    Notes
    -----
    - This function performs no disk or network I/O.
    - Real implementations will hook into upstream mock generators and
      catalogues once those are integrated.
    """
    metadata: Dict[str, Any] = {
        "backend": "mocks",
        "suite_name": suite_name,
        "status": "PENDING_IMPLEMENTATION",
        "description": "Void-lensing mock suite loader stub (no I/O performed).",
    }
    return None, metadata


def load_kappa_map(mock_id: str = "mock_000") -> Tuple[None, Dict[str, Any]]:
    """
    Placeholder loader for an individual synthetic convergence (κ) map.

    Parameters
    ----------
    mock_id:
        Identifier of the mock realisation within a suite.

    Returns
    -------
    kappa_map, metadata:
        In the scaffold, `kappa_map` is always None and `metadata` is a
        small dictionary describing the backend and implementation status.

    Notes
    -----
    - This function performs no disk or network I/O.
    - Intended only to document the expected interface for mock κ-map
      loaders; real implementations will be added later.
    """
    metadata: Dict[str, Any] = {
        "backend": "mocks",
        "mock_id": mock_id,
        "status": "PENDING_IMPLEMENTATION",
        "description": "Void-lensing mock κ-map loader stub (no I/O performed).",
    }
    return None, metadata