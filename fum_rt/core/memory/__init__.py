from __future__ import annotations

"""
fum_rt.core.memory package

Exports:
- MemoryField: event-driven memory field owner (from .field)
- load_engram, save_checkpoint: engram IO (from .engram_io)

This resolves the prior module/package name conflict by making
fum_rt.core.memory a proper package namespace with explicit re-exports.
"""

from .field import MemoryField
from .engram_io import load_engram, save_checkpoint

__all__ = ["MemoryField", "load_engram", "save_checkpoint"]