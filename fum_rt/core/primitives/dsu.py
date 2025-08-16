"""
Disjoint Set Union (Union-Find) primitive with O(1) component counting
and optional masked counting for rare telemetry.

Void-faithful: event-folded unions only; no global scans in hot path.
Copyright © 2025 Justin K. Lietz, Neuroca, Inc.
"""
from __future__ import annotations

from typing import Optional
import numpy as np


class DSU:
    """
    Path-compressed, union-by-rank disjoint set with size tracking and
    O(1) component counting.

    Hot-path methods:
      - find(x) -> int
      - union(a, b) -> bool            # True if merged (reduced components)
      - same_set(a, b) -> bool
      - count_sets() -> int            # O(1)

    Rare/telemetry method:
      - count_sets(mask: Optional[np.ndarray]) -> int
        When mask is provided, counts sets only across masked indices
        via a local scan of the mask (not for per-tick use).
    """
    __slots__ = ("parent", "rank", "size", "components")

    def __init__(self, n: int):
        n = int(n)
        self.parent = np.arange(n, dtype=np.int32)
        self.rank = np.zeros(n, dtype=np.int8)
        self.size = np.ones(n, dtype=np.int32)
        self.components = n

    def find(self, x: int) -> int:
        p = self.parent
        x = int(x)
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return int(x)

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # attach lower-rank to higher-rank
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] = self.rank[ra] + 1
        self.components -= 1
        return True

    def grow_to(self, n: int) -> None:
        """
        Grow DSU to cover indices [0, n), preserving existing sets.
        O(n - old_n) initialization; does not scan existing structure.
        """
        n = int(n)
        cur = int(self.parent.size)
        if n <= cur:
            return
        add = n - cur
        self.parent = np.concatenate([self.parent, np.arange(cur, n, dtype=np.int32)])
        self.rank = np.concatenate([self.rank, np.zeros(add, dtype=np.int8)])
        self.size = np.concatenate([self.size, np.ones(add, dtype=np.int32)])
        self.components += add

    def same_set(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)
 
    def count_sets(self, mask: Optional[np.ndarray] = None) -> int:
        if mask is None:
            return int(self.components)
        m = np.asarray(mask)
        if m.dtype != np.bool_:
            m = m.astype(bool, copy=False)
        if m.shape[0] != self.parent.size:
            raise ValueError("mask length must equal DSU size")
        idx = np.nonzero(m)[0]
        if idx.size == 0:
            return 0
        roots = set(self.find(int(i)) for i in idx)
        return len(roots)
 
 
 
__all__ = ["DSU"]