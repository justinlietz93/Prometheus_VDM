"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.void_cycle_scout

CycleHunterScout (read-only, void-faithful):
- Seeks short cycles (3-6 hops) using a TTL-limited walk with a tiny path window.
- Purely local: only neighbor lists are read; no global scans or dense conversions.
- Emits vt_touch and edge_on events; reducers can infer cycle hits from returned edge traces.

Heuristic:
- Maintain a small deque of the recent path (window ~ 5).
- Prefer stepping to a neighbor that is already in the recent window (closes a short cycle).
- Otherwise, hop randomly (blue-noise) among neighbors.

Guardrails:
- No schedulers; executes once per tick under the runner.
- Bounded budgets: visits, edges, ttl.
- No writes; events only.
"""

from typing import Any, Dict, Optional, Sequence, Set, List, Deque
from collections import deque
import random

from fum_rt.core.cortex.void_walkers.base import BaseScout
from fum_rt.core.proprioception.events import BaseEvent, VTTouchEvent, EdgeOnEvent


class CycleHunterScout(BaseScout):
    """
    Short-cycle finder with tiny path memory.
    """

    __slots__ = ("window",)

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 64,
        seed: int = 0,
        *,
        window: int = 5,
    ) -> None:
        super().__init__(budget_visits=budget_visits, budget_edges=budget_edges, ttl=ttl, seed=seed)
        self.window = int(max(2, window))

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        # Neutral: let runner seeds drive locality; no external heads required.
        return set()

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
                ttl = int(budget.get("ttl", ttl))
            except Exception:
                pass
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
        ttl = max(1, ttl)

        # Seed pool: prefer runner-provided seeds; else uniform
        if seeds:
            try:
                pool: Sequence[int] = tuple(int(s) for s in seeds if 0 <= int(s) < N) or tuple(range(N))
            except Exception:
                pool = tuple(range(N))
        else:
            pool = tuple(range(N))

        edges_emitted = 0
        visits_done = 0

        while visits_done < b_vis and pool:
            try:
                u = int(self.rng.choice(pool))
            except Exception:
                break

            cur = u
            depth = 0
            path: Deque[int] = deque(maxlen=self.window)

            while depth < ttl:
                # Touch current node
                events.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(cur), w=1.0))
                path.append(int(cur))
                visits_done += 1
                if visits_done >= b_vis:
                    break

                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if not neigh:
                        break

                    # Prefer neighbors that are in the recent path window (cycle closure)
                    try:
                        path_set = set(path)
                    except Exception:
                        path_set = set(int(x) for x in path) if path else set()

                    pref = [int(v) for v in neigh if int(v) in path_set and int(v) != int(cur)]
                    if pref:
                        v = int(self.rng.choice(pref))
                    else:
                        # Blue-noise hop
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

                depth += 1

        return events


__all__ = ["CycleHunterScout"]