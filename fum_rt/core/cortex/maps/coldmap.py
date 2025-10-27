"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.cortex.maps.coldmap
Purpose: Persistent, bounded coldness tracker keyed by node id (telemetry-only, read-only).
Design: Pure core module; no IO/logging; compatible with existing CoreEngine usage.
"""

from typing import List
import random
import math


class ColdMap:
    """
    Persistent, bounded coldness tracker keyed by node id.

    Coldness score (monotonic in idle time, bounded in [0,1)):
        age = max(0, t - last_seen[node])
        score = 1 - 2^(-age / half_life_ticks)

    Snapshot fields:
      - cold_head: top-16 [node_id, score] pairs (most cold first)
      - cold_p95, cold_p99, cold_max: distribution summaries across tracked nodes

    Notes:
    - API-compatible with existing CoreEngine usage:
        * touch(node: int, tick: int) to record activity
        * snapshot(tick: int, head_n: int = 16) -> dict with fields listed above
    - Constructor accepts (head_k, half_life_ticks, keep_max, seed) to match current wiring.
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


__all__ = ["ColdMap"]
