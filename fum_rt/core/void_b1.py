# void_b1.py
"""
Void-faithful, streaming B1 surrogate and Euler-rank estimate.

Design goals
- No dense NxN; use adjacency lists or the connectome's active-edge iterator
- O(E_active) for sparse; sampling to keep per-tick cost bounded
- Outputs:
  - void_b1: [0,1] scalar capturing cyclic structure density with smoothing
  - euler_rank: E_active - V_active + C_active (graph-level Betti-1 proxy)
  - triangles_per_edge: local triangle frequency around sampled active edges
  - active_node_ratio: V_active / N
  - active_edges_est: estimated or exact count of active undirected edges

Notes
- For SparseConnectome we rely on connectome._active_edge_iter() to enumerate
  active edges without scanning non-active neighbors.
- For dense Connectome this module only executes for small N where mask ops
  are acceptable; large-N runs auto-sparse in Nexus.
"""

from __future__ import annotations
import math
from typing import Iterable, List, Tuple, Dict, Any, Optional

import numpy as np


def _count_intersection_sorted(a: np.ndarray, b: np.ndarray) -> int:
    """
    Count |a ∩ b| given two ascending-sorted int arrays.
    """
    i = j = 0
    na, nb = a.size, b.size
    cnt = 0
    while i < na and j < nb:
        ai = int(a[i]); bj = int(b[j])
        if ai == bj:
            cnt += 1
            i += 1; j += 1
        elif ai < bj:
            i += 1
        else:
            j += 1
    return cnt


def _alpha_from_half_life(half_life_ticks: int) -> float:
    hl = max(1, int(half_life_ticks))
    return 1.0 - math.exp(math.log(0.5) / float(hl))


class _Reservoir:
    """
    Fixed-size reservoir sampler for a stream of unknown-length items.
    Items are small tuples (i,j).
    """
    def __init__(self, k: int, rng: np.random.Generator):
        self.k = int(max(1, k))
        self.rng = rng
        self.buf: List[Tuple[int, int]] = []
        self.seen = 0

    def push(self, item: Tuple[int, int]):
        self.seen += 1
        if len(self.buf) < self.k:
            self.buf.append(item)
            return
        # Replace with probability k/seen
        if self.rng.random() < (float(self.k) / float(self.seen)):
            idx = int(self.rng.integers(0, self.k))
            self.buf[idx] = item

    def items(self) -> List[Tuple[int, int]]:
        return self.buf

    def count(self) -> int:
        return self.seen


class VoidB1Meter:
    """
    Streaming surrogate for B1 with Euler-rank estimate.

    - Maintains EMA of b1_raw to produce void_b1 in [0,1]
    - Computes euler_rank = E_active - V_active + C_active (cycles count)
    - Estimates triangles_per_edge over a bounded reservoir of active edges

    Parameters
    - sample_edges: maximum number of active edges sampled per tick
    - half_life_ticks: EMA half-life for void_b1 smoothing
    """
    def __init__(self, sample_edges: int = 4096, half_life_ticks: int = 50):
        self.sample_edges = int(max(32, sample_edges))
        self.alpha = _alpha_from_half_life(half_life_ticks)
        self._ema_b1: Optional[float] = None

    # ---------------- Sparse path (preferred) ----------------

    def _update_sparse(
        self,
        adj: List[np.ndarray],
        W: np.ndarray,
        threshold: float,
        rng: np.random.Generator,
        active_edge_iter: Iterable[Tuple[int, int]],
        N: int,
    ) -> Dict[str, Any]:
        """
        O(E_active) with bounded sampling for triangles.
        """
        N = int(N)
        W = np.asarray(W, dtype=np.float32)
        th = float(threshold)

        # Reservoir over active edges, and visit-tracking for V_active and C_active
        res = _Reservoir(self.sample_edges, rng)
        visited = np.zeros(N, dtype=np.bool_)
        E_active = 0

        # We also compute active-subgraph components via DSU over active edges
        parent = np.arange(N, dtype=np.int32)
        rank = np.zeros(N, dtype=np.int8)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int):
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[rb] < rank[ra]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] = rank[ra] + 1

        for (i, j) in active_edge_iter:
            i = int(i); j = int(j)
            # Active edge guaranteed by iterator contract
            E_active += 1
            visited[i] = True
            visited[j] = True
            union(i, j)
            res.push((i, j))

        V_active = int(visited.sum())
        if E_active == 0:
            C_active = N  # no active edges: every node is isolated (V_active may be 0)
        else:
            # Count unique roots only over nodes that are active (visited==True)
            roots = set(int(find(int(idx))) for idx in np.nonzero(visited)[0])
            C_active = len(roots)

        # Triangles-per-edge over the reservoir
        tri = 0
        m = len(res.items())
        if m > 0:
            for (i, j) in res.items():
                ai = adj[i]; aj = adj[j]
                # Intersect active neighbors only: W[i]*W[k] > th and W[j]*W[k] > th
                # Fast path: build filtered lists then intersect
                if ai.size == 0 or aj.size == 0:
                    continue
                # Filter by active threshold
                ai_act = ai[(W[i] * W[ai]) > th]
                if ai_act.size == 0:
                    continue
                aj_act = aj[(W[j] * W[aj]) > th]
                if aj_act.size == 0:
                    continue
                tri += _count_intersection_sorted(ai_act, aj_act)

        triangles_per_edge = (float(tri) / float(m)) if m > 0 else 0.0

        # Cycles (Euler-rank for graphs)
        cycles = max(0, int(E_active - V_active + C_active))

        # Node activity ratio
        active_node_ratio = (float(V_active) / float(max(1, N)))

        return {
            "E_active": int(E_active),
            "V_active": int(V_active),
            "C_active": int(C_active),
            "cycles": int(cycles),
            "triangles_per_edge": float(triangles_per_edge),
            "active_node_ratio": float(active_node_ratio),
            "reservoir_seen": int(res.count()),
            "reservoir_used": int(m),
        }

    # ---------------- Dense path (small-N only) ----------------

    def _update_dense(
        self,
        A: np.ndarray,
        E: np.ndarray,
        W: np.ndarray,
        threshold: float,
        rng: np.random.Generator,
    ) -> Dict[str, Any]:
        """
        Small-N fallback using masks; cost is acceptable only for validation runs.
        """
        N = int(A.shape[0])
        th = float(threshold)

        # Active mask, undirected, upper triangle to avoid double counting
        mask = (E > th) & (A == 1)
        # Degrees and active vertices
        deg = mask.sum(axis=1).astype(np.int64)
        V_active = int((deg > 0).sum())

        # Active edge list (upper triangle)
        iu, ju = np.where(np.triu(mask, k=1))
        edges = np.stack([iu, ju], axis=1).astype(np.int32, copy=False)
        E_active = int(edges.shape[0])

        # DSU for active components (restricted to active vertices)
        parent = np.arange(N, dtype=np.int32)
        rank = np.zeros(N, dtype=np.int8)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int):
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[rb] < rank[ra]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] = rank[ra] + 1

        for i, j in edges:
            union(int(i), int(j))

        if E_active == 0:
            C_active = N
        else:
            act_idx = np.nonzero(deg > 0)[0]
            roots = set(int(find(int(idx))) for idx in act_idx)
            C_active = len(roots)

        # Reservoir over edges
        k = min(self.sample_edges, E_active)
        triangles_per_edge = 0.0
        if k > 0:
            sel = rng.choice(E_active, size=k, replace=False)
            sel_edges = edges[sel]
            # Build neighbor lists once (sorted)
            # For small N, extracting sorted neighbor arrays is fine
            nbrs = [np.where(A[i] > 0)[0].astype(np.int32) for i in range(N)]
            # Intersect with active condition using threshold
            tri = 0
            for (i, j) in sel_edges:
                ai = nbrs[int(i)]; aj = nbrs[int(j)]
                if ai.size == 0 or aj.size == 0:
                    continue
                ai_act = ai[(W[int(i)] * W[ai]) > th]
                if ai_act.size == 0:
                    continue
                aj_act = aj[(W[int(j)] * W[aj]) > th]
                if aj_act.size == 0:
                    continue
                tri += _count_intersection_sorted(ai_act, aj_act)
            triangles_per_edge = float(tri) / float(k)

        cycles = max(0, int(E_active - V_active + C_active))
        active_node_ratio = float(V_active) / float(max(1, N))

        return {
            "E_active": int(E_active),
            "V_active": int(V_active),
            "C_active": int(C_active),
            "cycles": int(cycles),
            "triangles_per_edge": float(triangles_per_edge),
            "active_node_ratio": float(active_node_ratio),
            "reservoir_seen": int(E_active),
            "reservoir_used": int(k),
        }

    # ---------------- Public API ----------------

    def update(self, connectome) -> Dict[str, Any]:
        """
        Compute a void-faithful topology packet and return:
        {
          'void_b1': [0,1],
          'euler_rank': int,
          'cycles': int,
          'triangles_per_edge': float,
          'active_node_ratio': float,
          'active_edges_est': int
        }

        The method chooses sparse vs dense automatically.
        """
        rng = getattr(connectome, "rng", np.random.default_rng(0))

        if hasattr(connectome, "_active_edge_iter"):
            # Sparse path
            adj = getattr(connectome, "adj", None)
            if adj is None:
                raise RuntimeError("Sparse path requires 'adj' on connectome")
            W = np.asarray(connectome.W, dtype=np.float32)
            th = float(getattr(connectome, "threshold", 0.0))
            N = int(getattr(connectome, "N", W.shape[0]))
            pkt = self._update_sparse(
                adj=adj,
                W=W,
                threshold=th,
                rng=rng,
                active_edge_iter=getattr(connectome, "_active_edge_iter")(),
                N=N,
            )
        else:
            # Dense path
            A = np.asarray(connectome.A, dtype=np.int8)
            E = np.asarray(connectome.E, dtype=np.float32)
            W = np.asarray(connectome.W, dtype=np.float32)
            th = float(getattr(connectome, "threshold", 0.0))
            pkt = self._update_dense(A=A, E=E, W=W, threshold=th, rng=rng)

        # Compose a normalized void_b1 score with EMA smoothing.
        # Mix cycles density and triangles per edge; both emphasize local cyclic structure.
        E_act = max(1, int(pkt["E_active"]))
        cycles_density = float(pkt["cycles"]) / float(E_act)  # [0, +]
        # Heuristic normalization: triangles_per_edge is usually small (0..few)
        tri_norm = min(1.0, float(pkt["triangles_per_edge"]) / 4.0)

        b1_raw = 0.6 * cycles_density + 0.4 * tri_norm
        b1_raw = max(0.0, min(1.0, b1_raw))  # clamp to [0,1]

        if self._ema_b1 is None:
            self._ema_b1 = b1_raw
        else:
            a = self.alpha
            self._ema_b1 = (1.0 - a) * float(self._ema_b1) + a * float(b1_raw)

        out = {
            "void_b1": float(self._ema_b1),
            "euler_rank": int(pkt["cycles"]),  # Graph Euler-rank equals cycles for 1D complexes
            "cycles": int(pkt["cycles"]),
            "triangles_per_edge": float(pkt["triangles_per_edge"]),
            "active_node_ratio": float(pkt["active_node_ratio"]),
            "active_edges_est": int(pkt["E_active"]),
            "active_vertices_est": int(pkt["V_active"]),
            "active_components_est": int(pkt["C_active"]),
            "reservoir_seen": int(pkt["reservoir_seen"]),
            "reservoir_used": int(pkt["reservoir_used"]),
        }
        return out


# Convenience singleton for quick integration
_GLOBAL_B1_METER: Optional[VoidB1Meter] = None


def update_void_b1(connectome, sample_edges: int = 4096, half_life_ticks: int = 50) -> Dict[str, Any]:
    """
    Module-level helper to update and return the topology packet.
    Lazily initializes a process-local meter.
    """
    global _GLOBAL_B1_METER
    if _GLOBAL_B1_METER is None:
        _GLOBAL_B1_METER = VoidB1Meter(sample_edges=sample_edges, half_life_ticks=half_life_ticks)
    return _GLOBAL_B1_METER.update(connectome)