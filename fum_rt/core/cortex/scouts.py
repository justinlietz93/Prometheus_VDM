from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

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
import math

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


# ---------------------------- Cold-map Reducer ----------------------------
class ColdMap:
    """
    Persistent, bounded coldness tracker keyed by node id.

    Coldness score (monotonic in idle time, bounded in [0,1)):
        age = max(0, t - last_seen[node])
        score = 1 - 2^(-age / half_life_ticks)

    Snapshot fields:
      - cold_head: top-16 [node_id, score] pairs (most cold first)
      - cold_p95, cold_p99, cold_max: distribution summaries across tracked nodes
    """
    __slots__ = ("head_k", "half_life", "keep_max", "rng", "_last_seen")

    def __init__(self, head_k: int = 256, half_life_ticks: int = 200, keep_max: int | None = None, seed: int = 0) -> None:
        self.head_k = int(max(8, head_k))
        self.half_life = int(max(1, half_life_ticks))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))
        self._last_seen: dict[int, int] = {}

    # ------------- updates -------------

    def touch(self, node: int, tick: int) -> None:
        """
        Record a touch for node at tick. Node ids must be non-negative ints.
        """
        try:
            n = int(node)
            t = int(tick)
        except Exception:
            return
        if n < 0:
            return
        self._last_seen[n] = t
        if len(self._last_seen) > self.keep_max:
            self._prune(t)

    def _prune(self, tick: int) -> None:
        """
        Reduce tracked set to keep_max entries, preferentially dropping the most recently seen nodes.
        Uses sampling to avoid O(N) passes.
        """
        try:
            size = len(self._last_seen)
            if size <= self.keep_max:
                return
            target = size - self.keep_max
            keys = list(self._last_seen.keys())
            sample_size = min(len(keys), max(256, target * 4))
            sample = self.rng.sample(keys, sample_size) if sample_size > 0 else keys
            # Sort sample by recency (most recent first) and drop up to target from this set.
            sample.sort(key=lambda k: self._last_seen.get(k, -10**12), reverse=True)
            to_remove = min(target, len(sample))
            for k in sample[:to_remove]:
                self._last_seen.pop(k, None)
        except Exception:
            # Conservative fallback: random removals until within bound
            while len(self._last_seen) > self.keep_max:
                try:
                    k = self.rng.choice(tuple(self._last_seen.keys()))
                    self._last_seen.pop(k, None)
                except Exception:
                    break

    # ------------- scoring -------------

    def _score(self, age: int) -> float:
        a = max(0, int(age))
        # score in [0, 1): 1 - 2^(-age / half_life)
        try:
            return float(1.0 - math.pow(0.5, float(a) / float(self.half_life)))
        except Exception:
            return 0.0

    # ------------- snapshot -------------

    def snapshot(self, tick: int, head_n: int = 16) -> dict:
        """
        Compute a coldness snapshot at tick.

        Returns:
          {
            "cold_head": list[[node_id, score], ...]           # top head_n by score
            "cold_p95": float,
            "cold_p99": float,
            "cold_max": float,
          }
        """
        try:
            t = int(tick)
        except Exception:
            t = 0

        if not self._last_seen:
            return {"cold_head": [], "cold_p95": 0.0, "cold_p99": 0.0, "cold_max": 0.0}

        # Compute scores for all tracked nodes (bounded by keep_max)
        pairs: List[tuple[int, float]] = []
        for node, ts in self._last_seen.items():
            try:
                age = t - int(ts)
            except Exception:
                age = 0
            s = self._score(age)
            pairs.append((int(node), float(s)))

        # Top head_n by score
        head_n = max(1, min(int(head_n), self.head_k))
        try:
            import heapq as _heapq
            head = _heapq.nlargest(head_n, pairs, key=lambda kv: kv[1])
        except Exception:
            head = sorted(pairs, key=lambda kv: kv[1], reverse=True)[:head_n]

        # Percentiles over full tracked set (bounded)
        vals = [s for _, s in pairs]
        vals.sort()

        def _pct(p: float) -> float:
            if not vals:
                return 0.0
            i = int(max(0, min(len(vals) - 1, round((len(vals) - 1) * p))))
            return float(vals[i])

        p95 = _pct(0.95)
        p99 = _pct(0.99)
        vmax = float(vals[-1]) if vals else 0.0

        head_out: List[List[float]] = [[int(n), float(s)] for n, s in head]
        return {
            "cold_head": head_out,
            "cold_p95": float(p95),
            "cold_p99": float(p99),
            "cold_max": float(vmax),
        }


__all__ = ["VoidColdScoutWalker", "ColdMap"]