from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_sentinel_scout

SentinelScout (read-only, void-faithful):
- Blue-noise reseeder / de-trample walker.
- Purpose: prevent path lock-in by sampling uniformly across space and announcing coverage.
- Emits vt_touch for coverage and opportunistic edge_on (one hop) when neighbors exist.

Behavior:
- Seeds = budget["seeds"] when provided (e.g., recent UTE indices) else uniform random nodes.
- TTL kept minimal (default 1) to avoid trampling and keep cost bounded.
- Local reads only (neighbors of the current node); no scans; no writes.

Optional inputs (maps):
- "visit_head" or "cold_head" can bias seeds slightly when present; still bounded heads.
"""

from typing import Any, Dict, Optional, Sequence, Set, List
from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent, VTTouchEvent, EdgeOnEvent


def _head_to_set(maps: Optional[Dict[str, Any]], keys: Sequence[str], cap: int = 512) -> Set[int]:
    out: Set[int] = set()
    if not isinstance(maps, dict):
        return out
    for key in keys:
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
            continue
    return out


class SentinelScout(BaseScout):
    """
    Blue-noise reseeding walker with minimal TTL to refresh coverage.
    """

    __slots__ = ()

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 1,   # one hop per seed by default
        seed: int = 0,
    ) -> None:
        super().__init__(budget_visits=budget_visits, budget_edges=budget_edges, ttl=ttl, seed=seed)

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Prefer low-visit or cold heads when available; bounded and read-only
        return _head_to_set(maps, keys=("visit_head", "cold_head"), cap=max(64, self.budget_visits * 8))

    def step(
        self,
        connectome: Any,
        bus: Any = None,  # unused
        maps: Optional[Dict[str, Any]] = None,
        budget: Optional[Dict[str, int]] = None,
    ) -> List[BaseEvent]:
        events: List[BaseEvent] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events

        b_vis = self.budget_visits
        b_edg = self.budget_edges
        ttl = self.ttl
        tick = 0
        seeds = None
        if isinstance(budget, dict):
            try:
                b_vis = int(budget.get("visits", b_vis))
            except Exception:
                pass
            try:
                b_edg = int(budget.get("edges", b_edg))
            except Exception:
                pass
            try:
                # Sentinel is intentionally shallow; cap TTL to 1 even if provided larger
                ttl = max(1, min(1, int(budget.get("ttl", ttl))))
            except Exception:
                ttl = 1
            try:
                tick = int(budget.get("tick", 0))
            except Exception:
                tick = 0
            try:
                seeds = list(budget.get("seeds", []))
            except Exception:
                seeds = None

        b_vis = max(0, min(b_vis, N))
        b_edg = max(0, b_edg)
        ttl = 1  # enforce single-step walks to reduce trampling

        # Seeds: prefer explicit seeds; else priority; else uniform domain
        priority: Set[int] = set()
        try:
            priority = self._priority_set(maps)
        except Exception:
            priority = set()

        if seeds:
            try:
                pool: Sequence[int] = tuple(int(s) for s in seeds if 0 <= int(s) < N) or tuple(priority) or tuple(range(N))
            except Exception:
                pool = tuple(priority) or tuple(range(N))
        else:
            pool = tuple(priority) or tuple(range(N))

        edges_emitted = 0
        visits_done = 0

        while visits_done < b_vis and pool:
            try:
                u = int(self.rng.choice(pool))
            except Exception:
                break

            cur = u
            depth = 0
            while depth < ttl:
                # Announce coverage
                events.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(cur), w=1.0))
                visits_done += 1
                if visits_done >= b_vis:
                    break

                # Opportunistic single hop
                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if neigh:
                        try:
                            v = int(self.rng.choice(tuple(neigh)))
                        except Exception:
                            break
                        if v != cur:
                            events.append(EdgeOnEvent(kind="edge_on", t=tick, u=int(cur), v=int(v)))
                            edges_emitted += 1
                            cur = int(v)
                        else:
                            break
                    else:
                        break
                else:
                    break

                depth += 1

        return events


__all__ = ["SentinelScout"]