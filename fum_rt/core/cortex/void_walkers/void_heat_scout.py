from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_heat_scout

HeatScout (read-only, void-faithful):
- Prefers neighbors whose node ids appear in HeatMap snapshot head ("heat_head").
- Emits only vt_touch and edge_on events (foldable by reducers).
- No scans of global structures; uses local neighbor reads and bounded TTL/budgets.
"""

from typing import Any, Dict, Optional, Set
from fum_rt.core.cortex.scouts.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent  # re-export type for hints


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


class HeatScout(BaseScout):
    """
    Activity-driven scout: routes toward nodes with higher recent activity (HeatMap).
    """

    __slots__ = ()

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer HeatMap head indices
        return _extract_head_nodes(maps, "heat_head", cap=max(64, self.budget_visits * 8))


__all__ = ["HeatScout"]
