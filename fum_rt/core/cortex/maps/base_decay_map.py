from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.cortex.maps.base_decay_map
Purpose: Shared bounded, exponential-decay event-driven map base for Heat/Exc/Inh reducers.

Void-faithful constraints:
- Event-driven folding only (no global scans over W or neighbors).
- Bounded working set via keep_max with sample-based pruning.
- O(#events) time per tick; snapshot is cheap and bounded by head_k/keep_max.
"""

from typing import Dict, Iterable, List
import math
import random


class BaseDecayMap:
    """
    Bounded, per-node exponentially decaying accumulator.
    Score_t(node) = Score_{t-Δ} * 2^(-Δ/half_life_ticks) + sum(increments at t)

    Snapshot:
      - head (top-16 [node, score] pairs by default; bounded by head_k)
      - p95, p99, max, count summaries

    Notes:
    - Subclasses must implement fold(events, tick) and call add(node, tick, inc).
    - No I/O/logging; pure core.
    """

    __slots__ = ("head_k", "half_life", "keep_max", "rng", "_val", "_last_tick")

    def __init__(self, head_k: int = 256, half_life_ticks: int = 200, keep_max: int | None = None, seed: int = 0) -> None:
        self.head_k = int(max(8, head_k))
        self.half_life = int(max(1, half_life_ticks))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))
        self._val: Dict[int, float] = {}
        self._last_tick: Dict[int, int] = {}

    # ------------- core updates -------------

    def _decay_to(self, node: int, tick: int) -> None:
        lt = self._last_tick.get(node)
        if lt is None:
            self._last_tick[node] = tick
            return
        dt = max(0, int(tick) - int(lt))
        if dt > 0:
            factor = 2.0 ** (-(dt / float(self.half_life)))
            try:
                self._val[node] *= factor
            except Exception:
                self._val[node] = float(self._val.get(node, 0.0)) * float(factor)
            self._last_tick[node] = tick

    def add(self, node: int, tick: int, inc: float) -> None:
        try:
            n = int(node)
            t = int(tick)
            dv = float(inc)
        except Exception:
            return
        if n < 0:
            return
        if n in self._val:
            self._decay_to(n, t)
            self._val[n] += dv
        else:
            self._val[n] = max(0.0, dv)
            self._last_tick[n] = t
        if len(self._val) > self.keep_max:
            self._prune()

    def _prune(self) -> None:
        # Drop a sampled set of the smallest entries (cheap; avoids full O(N) sort)
        size = len(self._val)
        target = size - self.keep_max
        if target <= 0:
            return
        keys = list(self._val.keys())
        sample_size = min(len(keys), max(256, target * 4))
        sample = self.rng.sample(keys, sample_size) if sample_size > 0 else keys
        sample.sort(key=lambda k: self._val.get(k, 0.0))  # ascending by score
        for k in sample[:target]:
            self._val.pop(k, None)
            self._last_tick.pop(k, None)

    # ------------- folding & snapshots -------------

    def fold(self, events: Iterable[object], tick: int) -> None:
        """
        Subclasses override and call add(node, tick, inc) appropriately.
        """
        raise NotImplementedError

    def snapshot(self, head_n: int = 16) -> dict:
        if not self._val:
            return {"head": [], "p95": 0.0, "p99": 0.0, "max": 0.0, "count": 0}
        # head top-k by score
        try:
            import heapq as _heapq
            head = _heapq.nlargest(int(min(self.head_k, max(1, head_n))), self._val.items(), key=lambda kv: kv[1])
        except Exception:
            head = sorted(self._val.items(), key=lambda kv: kv[1], reverse=True)[: int(min(self.head_k, max(1, head_n)))]
        # quick percentiles over working set
        vals = sorted(float(v) for v in self._val.values())
        def q(p: float) -> float:
            if not vals:
                return 0.0
            i = min(len(vals) - 1, max(0, int(math.floor(p * (len(vals) - 1)))))
            return float(vals[i])
        return {
            "head": [[int(k), float(v)] for k, v in head],
            "p95": q(0.95),
            "p99": q(0.99),
            "max": float(vals[-1]),
            "count": int(len(vals)),
        }


__all__ = ["BaseDecayMap"]