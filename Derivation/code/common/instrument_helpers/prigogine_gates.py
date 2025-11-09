"""
Compatibility shim for prigogine gate helpers

New location:
  Derivation/code/common/validation_gate_helpers/nonequilibrium/prigogine_gates.py

This module re-exports all public symbols to preserve existing imports:
  from instrument_helpers.prigogine_gates import ...
"""

from __future__ import annotations

import warnings
from importlib import import_module as _import_module

# Load new module
_new_mod = _import_module("validation_gate_helpers.nonequilibrium.prigogine_gates")

# Re-export public names
for _name in dir(_new_mod):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_new_mod, _name)

warnings.warn(
    "instrument_helpers.prigogine_gates has moved to "
    "validation_gate_helpers.nonequilibrium.prigogine_gates; "
    "update imports by 2025-12-01.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [n for n in dir(_new_mod) if not n.startswith("_")]
__doc__ = getattr(_new_mod, "__doc__", __doc__)