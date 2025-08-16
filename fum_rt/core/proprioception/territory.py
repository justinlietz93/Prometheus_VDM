"""
Void-faithful cohesion territories (incremental, event-folded; no scans).

- Maintains a union-find structure over observed edge_on-like events
  to approximate connected components ("territories").
- Keeps a bounded per-component head (reservoir) of member indices to serve
  territory_indices to actuators (e.g., GDSP) without graph scans.
- O(1) amortized per observation; no reads of W/CSR/adjacency.

API
- fold(observations): consumes Observation-like objects (kind/nodes fields)
  and unions endpoints found in cycle_hit (first two nodes) or edge_on(u,v).
- components_count(): number of current components (approximate).
- sample_indices(component_id, k): returns up to k indices from the requested
  component (component_id can be any node in the component).
- sample_any(k): returns up to k indices across largest components (by UF size).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set


class TerritoryUF:
    def __init__(self, head_k: int = 512) -> None:
        self.parent: Dict[int, int] = {}
        self.size: Dict[int, int] = {}
        # bounded head members per root (kept small; no scans)
        self._head: Dict[int, List[int]] = {}
        self._head_k = max(8, int(head_k))
        self._dirty = 0  # for future auditors

    # ------------- UF core -------------

    def _find(self, x: int) -> int:
        p = self.parent.get(x, x)
        if p != x:
            self.parent[x] = self._find(p)
        return self.parent.get(x, x)

    def _ensure(self, x: int) -> int:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            # seed head with the node itself
            self._head[x] = [x]
        return x

    def _merge_heads(self, r_to: int, r_from: int) -> None:
        """
        Merge bounded heads; keep uniqueness and cap to head_k.
        """
        h_to = self._head.get(r_to, [])
        h_from = self._head.get(r_from, [])
        if not h_from:
            self._head[r_to] = list(dict.fromkeys(h_to))[: self._head_k]
            return
        # Favor r_to contents then supplement with r_from
        merged: List[int] = []
        seen: Set[int] = set()
        for src in (h_to, h_from):
            for n in src:
                if n not in seen:
                    merged.append(n)
                    seen.add(n)
                    if len(merged) >= self._head_k:
                        break
            if len(merged) >= self._head_k:
                break
        self._head[r_to] = merged

    def _add_member(self, r: int, x: int) -> None:
        """
        Add a member to root r's head (bounded); no-ops on duplicates.
        """
        head = self._head.setdefault(r, [])
        if x in head:
            return
        if len(head) < self._head_k:
            head.append(x)
        # else: drop (bounded by design)

    def union(self, u: int, v: int) -> None:
        ru = self._find(self._ensure(u))
        rv = self._find(self._ensure(v))
        if ru == rv:
            return
        su = self.size.get(ru, 1)
        sv = self.size.get(rv, 1)
        # union by size
        if su < sv:
            ru, rv = rv, ru
            su, sv = sv, su
        self.parent[rv] = ru
        self.size[ru] = su + sv
        # merge bounded heads
        self._merge_heads(ru, rv)
        # cleanup from root moved
        try:
            if rv in self._head:
                del self._head[rv]
        except Exception:
            pass

    def mark_dirty(self, _u: int, _v: int) -> None:
        self._dirty += 1

    # ------------- public -------------

    def fold(self, observations: Iterable[Any]) -> None:
        """
        Fold Observation-like objects:
          - cycle_hit: if nodes has ≥ 2, union(nodes[0], nodes[1])
          - edge_on: union(u, v) if fields present
          - edge_off: mark_dirty (no reconciliation here)
        """
        if not observations:
            return
        for obs in observations:
            try:
                k = getattr(obs, "kind", None)
                if not k:
                    continue
                if k == "cycle_hit":
                    nodes = list(getattr(obs, "nodes", []) or [])
                    if len(nodes) >= 2:
                        u, v = int(nodes[0]), int(nodes[1])
                        self.union(u, v)
                        # seed members (bounded) for fast sampling
                        self._add_member(self._find(u), u)
                        self._add_member(self._find(v), v)
                elif k == "edge_on":
                    u = int(getattr(obs, "u", 0))
                    v = int(getattr(obs, "v", 0))
                    self.union(u, v)
                    self._add_member(self._find(u), u)
                    self._add_member(self._find(v), v)
                elif k == "edge_off":
                    u = int(getattr(obs, "u", 0))
                    v = int(getattr(obs, "v", 0))
                    self.mark_dirty(u, v)
            except Exception:
                continue

    def components_count(self) -> int:
        return sum(1 for n, p in self.parent.items() if n == p)

    def sample_indices(self, component_id: int, k: int) -> List[int]:
        """
        Sample up to k indices from the component containing 'component_id'.
        """
        if k <= 0:
            return []
        if component_id not in self.parent:
            return []
        r = self._find(int(component_id))
        head = self._head.get(r, [])
        return head[: int(k)]

    def sample_any(self, k: int) -> List[int]:
        """
        Sample up to k indices across largest components (bounded heads).
        """
        if k <= 0:
            return []
        # sort roots by UF size desc (bounded to number of heads)
        roots = list(self._head.keys())
        roots.sort(key=lambda r: self.size.get(r, len(self._head.get(r, []))), reverse=True)
        out: List[int] = []
        for r in roots:
            if len(out) >= k:
                break
            head = self._head.get(r, [])
            for n in head:
                out.append(n)
                if len(out) >= k:
                    break
        return out