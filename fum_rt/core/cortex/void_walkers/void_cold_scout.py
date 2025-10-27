"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_cold_scout

ColdScout (read-only, void-faithful):
- Prefers neighbors whose node ids appear in ColdMap snapshot head ("cold_head").
- Emits only vt_touch and edge_on events.
- No scans of global structures; uses local neighbor reads and bounded TTL/budgets.

Compatibility:
- Provides alias VoidColdScoutWalker for existing imports in legacy code paths.
"""

from typing import Any, Dict, List, Optional, Sequence, Set
from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent


def _extract_head_nodes(maps: Optional[Dict[str, Any]], key: str, cap: int = 512) -> Set[int]:
    """
    Extract bounded head nodes from map snapshot structure: [[node, score], ...]
    """
    out: Set[int] = set()
    if not isinstance(maps, dict):
        return out
    try:
        head = maps.get(key, []) or []
        for pair in head[: cap]:
            try:
                n = int(pair[0])
            except Exception:
                continue
            if n >= 0:
                out.add(n)
    except Exception:
        return out
    return out


class ColdScout(BaseScout):
    """
    Coldness-driven scout: routes toward nodes with higher coldness (less recently seen).
    """

    __slots__ = ()

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        return _extract_head_nodes(maps, "cold_head", cap=max(64, self.budget_visits * 8))


# Back-compat alias used by runtime/engine wiring in existing code
VoidColdScoutWalker = ColdScout

__all__ = ["ColdScout", "VoidColdScoutWalker"]
