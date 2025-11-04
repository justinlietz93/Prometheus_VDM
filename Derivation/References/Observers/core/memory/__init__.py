"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
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