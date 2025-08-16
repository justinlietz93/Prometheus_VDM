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
    * BaseScout (interface) via submodule "scouts.base"
    * GDSPActuator / RevGSP re-exported from core.neuroplasticity (for legacy imports)
- Additionally, this file makes itself behave like a package so that
  "from fum_rt.core.cortex.scouts.base import BaseScout" continues to work
  even though this file is a module. We achieve this by exposing __path__
  that points at "./scouts/".

Contract compliance:
- Scouts emit only foldable events: vt_touch, edge_on, and (optionally) spike(+/-)
- They do not mutate the connectome (read-only), no scans, no schedulers.
"""

import os as _os

# Make this module act like a package for submodules in ./scouts/
_pkg_dir = _os.path.join(_os.path.dirname(__file__), "scouts")
if _os.path.isdir(_pkg_dir):
    try:
        __path__  # type: ignore[name-defined]
    except NameError:
        __path__ = [_pkg_dir]  # type: ignore[assignment]
    else:
        try:
            if _pkg_dir not in __path__:  # type: ignore[operator]
                __path__.append(_pkg_dir)  # type: ignore[union-attr]
        except Exception:
            __path__ = [_pkg_dir]  # type: ignore[assignment]

# Prefer modular implementations
from .void_walkers.void_cold_scout import ColdScout as VoidColdScoutWalker
from .void_walkers.void_heat_scout import HeatScout
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
    from .scouts.base import BaseScout  # type: ignore
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
    "ColdMap",
    "BaseScout",
    "GDSPActuator",
    "RevGSP",
]