"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Physics solvers and harnesses for the FUM scalar EFT stack."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "compute_kappas",
    "mode_functions",
    "ModeEntry",
    "compute_modes_for_R",
    "build_quartic_diagonal",
    "find_condensate_diagonal",
    "mass_matrix_diagonal",
    "energy_scan",
]

_MODULE_ATTRS = {
    "compute_kappas": (".cylinder_modes", "compute_kappas"),
    "mode_functions": (".cylinder_modes", "mode_functions"),
    "ModeEntry": (".condense_tube", "ModeEntry"),
    "compute_modes_for_R": (".condense_tube", "compute_modes_for_R"),
    "build_quartic_diagonal": (".condense_tube", "build_quartic_diagonal"),
    "find_condensate_diagonal": (".condense_tube", "find_condensate_diagonal"),
    "mass_matrix_diagonal": (".condense_tube", "mass_matrix_diagonal"),
    "energy_scan": (".condense_tube", "energy_scan"),
}

if TYPE_CHECKING:  # pragma: no cover - type checkers resolve eagerly
    from .cylinder_modes import compute_kappas, mode_functions  # noqa: F401
    from .condense_tube import (  # noqa: F401
        ModeEntry,
        compute_modes_for_R,
        build_quartic_diagonal,
        find_condensate_diagonal,
        mass_matrix_diagonal,
        energy_scan,
    )


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _MODULE_ATTRS[name]
    except KeyError as exc:  # pragma: no cover - defensive fallback
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(list(globals().keys()) + list(_MODULE_ATTRS.keys())))
