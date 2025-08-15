from __future__ import annotations

"""
Cold-scout walkers (Phase D scaffolding).

Design:
- Pure core module under core/cortex. No IO/logging; read-only against connectome.
- Budgeted, uniform "cold" probes that do not depend on the announce bus.
- Emits existing core events for folding:
  - VTTouchEvent(kind="vt_touch") for visited nodes
  - EdgeOnEvent(kind="edge_on") for sampled neighbor edges (best-effort)

Behavior:
- Disabled by default (wired behind ENABLE_COLD_SCOUTS in runtime/Nexus).
- When enabled, keeps strict per-tick budgets.
- Uses only common, safe connectome attributes/methods (N, neighbors/get_neighbors, adj).

Rationale:
- Provides a tiny, constant-cost scout to surface coverage/cohesion signals without scans.
- Events fold into EventDrivenMetrics. This preserves void-dynamics and avoids hot-path scans.

Safety:
- All calls are best-effort with try/except and defensive fallbacks.
- If connectome APIs differ, scouts gracefully degrade to only VT touches or no-ops.
"""

from typing import Any, Iterable, List, Set, Sequence
import random

from fum_rt.core.proprioception.events import (
    BaseEvent,
    VTTouchEvent,
    EdgeOnEvent,
)


class VoidColdScoutWalker:
    """
    Budgeted, read-only cold-scout walker.

    Parameters:
      - budget_visits: max node visits per tick (emits vt_touch)
      - budget_edges: max neighbor edges sampled per tick (emits edge_on)
      - seed: RNG seed for reproducibility

    Methods:
      - step(connectome, tick) -> list[BaseEvent]
    """

    __slots__ = ("budget_visits", "budget_edges", "rng")

    def __init__(self, budget_visits: int = 0, budget_edges: int = 0, seed: int = 0) -> None:
        self.budget_visits = int(max(0, budget_visits))
        self.budget_edges = int(max(0, budget_edges))
        self.rng = random.Random(int(seed))

    # --------- helpers ---------

    @staticmethod
    def _get_N(C: Any) -> int:
        try:
            N = int(getattr(C, "N", 0))
            if N > 0:
                return N
        except Exception:
            pass
        # Try shape-based fallback (e.g., if C.W is an ndarray/sparse with shape)
        try:
            W = getattr(C, "W", None)
            if W is not None:
                shp = getattr(W, "shape", None)
                if isinstance(shp, (tuple, list)) and len(shp) >= 1:
                    n = int(shp[0])
                    return n if n > 0 else 0
        except Exception:
            pass
        return 0

    @staticmethod
    def _neighbors(C: Any, u: int) -> List[int]:
        # Prefer explicit neighbor methods
        try:
            for meth in ("neighbors", "get_neighbors"):
                fn = getattr(C, meth, None)
                if callable(fn):
                    neigh = fn(int(u))
                    if neigh:
                        try:
                            return [int(x) for x in list(neigh)]
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

    # --------- main API ---------

    def step(self, connectome: Any, tick: int) -> List[BaseEvent]:
        """
        Execute one cold-scout pass with strict budgets, returning events to fold.
        """
        events: List[BaseEvent] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events

        # Node visits - contribute to VT coverage/entropy
        bv = min(self.budget_visits, N)
        visited: Set[int] = set()
        if bv > 0:
            while len(visited) < bv:
                try:
                    visited.add(int(self.rng.randrange(N)))
                except Exception:
                    break
            for u in visited:
                events.append(VTTouchEvent(kind="vt_touch", t=int(tick), token=int(u), w=1.0))

        # Edge samples - contribute to cohesion via union-find
        be = self.budget_edges
        if be > 0:
            trials = 0
            emitted = 0
            max_trials = be * 4  # avoid long loops when degree is low/unavailable
            # Create a stable pool to bias toward visited nodes, else fall back to uniform
            pool: Sequence[int] = tuple(visited) if visited else tuple(range(N))
            while emitted < be and trials < max_trials and pool:
                trials += 1
                try:
                    u = int(self.rng.choice(pool))
                except Exception:
                    break
                neigh = self._neighbors(connectome, u)
                if not neigh:
                    continue
                try:
                    v = int(self.rng.choice(neigh))
                except Exception:
                    continue
                if v == u:
                    continue
                events.append(EdgeOnEvent(kind="edge_on", t=int(tick), u=int(u), v=int(v)))
                emitted += 1

        return events


__all__ = ["VoidColdScoutWalker"]