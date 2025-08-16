from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.base

Void-faithful, read-only scout base class.
- No global scans or dense conversions; no direct access to raw weight arrays or external graph libraries.
- Operates only on local neighbor reads provided by the active graph.
- Emits only small, foldable events for reducers and telemetry.

Contract:
- step(connectome, bus, maps, budget) - returns a list[BaseEvent]
  * connectome: object exposing N and neighbors/get_neighbors or adj mapping
  * bus: opaque (optional) announce bus; NOT used for writes here (read-only scouts emit events to return)
  * maps: optional dict-like snapshots; subclasses may consult e.g. {"heat_head":[[n,score],...]}
  * budget: optional dict with keys:
      - "visits": int (node touches to attempt)
      - "edges": int (edge probes to attempt)
      - "ttl":   int (max walk depth per seed)
      - "tick":  int (current tick for event timestamps)

Returned events use only core event types:
- VTTouchEvent(kind="vt_touch", t, token=node, w=1.0)
- EdgeOnEvent(kind="edge_on", t, u, v)
- Subclasses may add SpikeEvent with sign bias (still event-only).

This module defines the common, safe scaffolding. Heuristics live in subclasses.
"""

from typing import Any, Iterable, List, Optional, Sequence, Set, Dict
import random

from fum_rt.core.proprioception.events import (
    BaseEvent,
    VTTouchEvent,
    EdgeOnEvent,
    SpikeEvent,  # subclasses may use; base does not emit spikes
)


class BaseScout:
    __slots__ = ("budget_visits", "budget_edges", "ttl", "rng")

    def __init__(
        self,
        budget_visits: int = 16,
        budget_edges: int = 8,
        ttl: int = 64,
        seed: int = 0,
    ) -> None:
        self.budget_visits = int(max(0, budget_visits))
        self.budget_edges = int(max(0, budget_edges))
        self.ttl = int(max(1, ttl))
        self.rng = random.Random(int(seed))

    # ---------------------- connectome helpers (read-only) ----------------------

    @staticmethod
    def _get_N(C: Any) -> int:
        try:
            N = int(getattr(C, "N", 0))
            if N > 0:
                return N
        except Exception:
            pass
        try:
            W = getattr(C, "W", None)
            shp = getattr(W, "shape", None)
            if shp and isinstance(shp, (tuple, list)) and len(shp) >= 1:
                n = int(shp[0])
                return n if n > 0 else 0
        except Exception:
            pass
        return 0

    @staticmethod
    def _neighbors(C: Any, u: int) -> List[int]:
        # Prefer explicit methods
        try:
            for meth in ("neighbors", "get_neighbors"):
                fn = getattr(C, meth, None)
                if callable(fn):
                    xs = fn(int(u))
                    if xs:
                        try:
                            return [int(x) for x in list(xs)]
                        except Exception:
                            return []
        except Exception:
            pass
        # Fallback: adjacency mapping
        try:
            adj = getattr(C, "adj", None)
            if isinstance(adj, dict):
                vals = adj.get(int(u), [])
                if isinstance(vals, dict):
                    return [int(x) for x in vals.keys()]
                return [int(x) for x in list(vals)]
        except Exception:
            pass
        return []

    # --------------------------- heuristic hooks --------------------------------

    def _priority_set(self, maps: Optional[Dict[str, Any]]) -> Set[int]:
        """
        Subclasses may override to bias routing locally using heads from reducers.
        Returns a bounded set of node indices to prefer when available.
        """
        return set()

    # ------------------------------ main API ------------------------------------

    def step(
        self,
        connectome: Any,
        bus: Any = None,  # unused (read-only)
        maps: Optional[Dict[str, Any]] = None,
        budget: Optional[Dict[str, int]] = None,
    ) -> List[BaseEvent]:
        """
        Bounded, TTL-limited local exploration that returns foldable events.
        Default strategy:
        - Touch up to 'visits' seeds (uniform from [0..N) if no priority).
        - For each, walk up to TTL steps, emitting vt_touch on the current node
          and best-effort edge_on to a locally chosen neighbor (biased by priority set).
        - Edge probes total bounded by 'edges'.
        """
        events: List[BaseEvent] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events

        b_vis = self.budget_visits
        b_edg = self.budget_edges
        ttl = self.ttl
        tick = 0
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

        b_vis = max(0, min(b_vis, N))
        b_edg = max(0, b_edg)
        ttl = max(1, ttl)

        # Seed pool: prefer priority nodes when available
        priority: Set[int] = set()
        try:
            priority = self._priority_set(maps)
        except Exception:
            priority = set()
        pool: Sequence[int] = tuple(priority) if priority else tuple(range(N))

        edges_emitted = 0
        visits_done = 0

        while visits_done < b_vis and pool:
            try:
                u = int(self.rng.choice(pool))
            except Exception:
                break

            # TTL-limited micro-walk starting at u
            cur = u
            depth = 0
            while depth < ttl:
                # Touch current node (coverage)
                events.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(cur), w=1.0))
                visits_done += 1
                if visits_done >= b_vis:
                    break

                # Probe one neighbor edge if budget remains
                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if neigh:
                        v = self._pick_neighbor(neigh, priority)
                        if v is not None and v != cur:
                            events.append(EdgeOnEvent(kind="edge_on", t=tick, u=int(cur), v=int(v)))
                            edges_emitted += 1
                            cur = int(v)
                        else:
                            # random hop when no preference applies
                            try:
                                cur = int(self.rng.choice(tuple(neigh)))
                            except Exception:
                                break
                    else:
                        break
                else:
                    break

                depth += 1

        return events

    # -------------------------- local routing policy ----------------------------

    def _pick_neighbor(self, neigh: Sequence[int], priority: Set[int]) -> Optional[int]:
        """
        Choose a neighbor biased toward 'priority' set when available, else blue-noise hop.
        """
        try:
            # Filter by priority first
            pref = [int(x) for x in neigh if int(x) in priority]
            if pref:
                return int(self.rng.choice(pref))
            # Blue-noise hop (random choice)
            return int(self.rng.choice(tuple(neigh)))
        except Exception:
            return None