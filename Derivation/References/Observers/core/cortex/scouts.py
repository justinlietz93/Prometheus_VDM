"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
fum_rt.core.cortex.scouts (facade)

This module is now a thin aggregator that re-exports modular scout classes and maps.
It preserves legacy import paths while enforcing void-faithful, read-only traversal.

Key points:
- No global scans; scouts only use local neighbor reads and bounded TTL/budgets.
- This facade exposes:
    * VoidColdScoutWalker (ColdScout)
    * HeatScout, ExcitationScout, InhibitionScout
    * ColdMap (from maps.coldmap)
    * BaseScout (interface) via void_walkers.base
    * GDSPActuator / RevGSP re-exported from core.neuroplasticity (for legacy imports)

Contract compliance:
- Scouts emit only foldable events: vt_touch, edge_on, and (optionally) spike(+/-)
- They do not mutate the connectome (read-only), no scans, no schedulers.
"""

# Prefer modular implementations
from .void_walkers.void_cold_scout import ColdScout as VoidColdScoutWalker
from .void_walkers.void_heat_scout import HeatScout
from .void_walkers.void_ray_scout import VoidRayScout
from .void_walkers.void_memory_ray_scout import MemoryRayScout
from .void_walkers.void_frontier_scout import FrontierScout
from .void_walkers.void_cycle_scout import CycleHunterScout
from .void_walkers.void_sentinel_scout import SentinelScout
try:
    from .void_walkers.void_excitation_scout import ExcitationScout
except Exception:  # pragma: no cover - optional during staged migration
    class ExcitationScout:  # type: ignore
        pass
try:
    from .void_walkers.void_inhibition_scout import InhibitionScout
except Exception:  # pragma: no cover - optional during staged migration
    class InhibitionScout:  # type: ignore
        pass

# Maps
try:
    from .maps.coldmap import ColdMap
except Exception:  # pragma: no cover
    ColdMap = None  # type: ignore

# Base interface (allow both "scouts.base" and "scouts: BaseScout" import styles)
try:
    from .void_walkers.base import BaseScout  # type: ignore
except Exception:  # pragma: no cover
    BaseScout = None  # type: ignore

# Neuroplasticity re-exports for legacy imports
try:
    from ..neuroplasticity.gdsp import GDSPActuator
except Exception:  # pragma: no cover
    GDSPActuator = None  # type: ignore
try:
    from ..neuroplasticity.revgsp import RevGSP
except Exception:  # pragma: no cover
    RevGSP = None  # type: ignore

__all__ = [
    "VoidColdScoutWalker",
    "HeatScout",
    "ExcitationScout",
    "InhibitionScout",
    "VoidRayScout",
    "MemoryRayScout",
    "FrontierScout",
    "CycleHunterScout",
    "SentinelScout",
    "ColdMap",
    "BaseScout",
    "GDSPActuator",
    "RevGSP",
]