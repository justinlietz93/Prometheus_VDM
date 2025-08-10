"""
Physics-informed diagnostics for the FUM runtime.

This module provides:
- Mass-gap estimation from two-point correlations on the runtime graph
- Pulse-speed (group velocity) estimation from time-resolved activity

References:
- [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:125-193)
- [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:117-134)
- [derivation/finite_tube_mode_analysis.md](derivation/finite_tube_mode_analysis.md:1)
- [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:44-121)

Conventions:
- We treat graph shortest-path distance (in hops) as the discrete spatial metric r
  when geometric embedding is unavailable. This is a standard surrogate on networks.
- The continuum prediction for the static two-point correlator is
  C(r) ~ exp(-r / xi) with mass gap m_eff = 1 / xi (dimensionless units).
- The wave speed c enters the EOM via c^2 = 2 J a^2 (per-site convention), see
  [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:117-134).
  We estimate an effective group velocity v_g from an expanding activity front.

Author: Justin K. Lietz
Date: 2025-08-09
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import numpy as np


def _ensure_adjacency(connectome) -> np.ndarray:
    """
    Extract a dense binary adjacency matrix A (int8) from the runtime connectome.

    Expected connectome interface (from fum_rt.core.*):
      - connectome.A : np.ndarray (N x N), int8, 0/1
      - connectome.N : int, number of nodes

    Returns:
      A : np.ndarray (N x N) int8 in {0,1}
    """
    if not hasattr(connectome, "A"):
        raise AttributeError("connectome must expose .A (adjacency)")

    A = connectome.A
    if not isinstance(A, np.ndarray):
        A = np.asarray(A)
    # Ensure binary
    A = (A != 0).astype(np.int8)
    return A


def _shortest_path_distances(A: np.ndarray, seeds: np.ndarray, max_d: int) -> Dict[int, List[Tuple[int, int, int]]]:
    """
    Compute shortest-path distances from a subset of seed nodes using BFS.

    Args:
      A: binary adjacency (N x N)
      seeds: array of seed node indices
      max_d: maximum distance to consider

    Returns:
      distances_by_d: mapping d -> list of (src, dst, d) pairs observed with shortest-path distance d,
                      with 1 <= d <= max_d
    """
    N = A.shape[0]
    neighbors = [np.where(A[i] != 0)[0] for i in range(N)]
    distances_by_d: Dict[int, List[Tuple[int, int, int]]] = {d: [] for d in range(1, max_d + 1)}

    for s in seeds:
        dist = np.full(N, -1, dtype=np.int32)
        dist[s] = 0
        q = [s]
        head = 0
        while head < len(q):
            u = q[head]
            head += 1
            du = dist[u]
            if du >= max_d:
                continue
            for v in neighbors[u]:
                if dist[v] == -1:
                    dist[v] = du + 1
                    q.append(v)
                    if 1 <= dist[v] <= max_d:
                        distances_by_d[dist[v]].append((s, v, dist[v]))
    return distances_by_d


def estimate_mass_gap_from_phi(
    connectome,
    phi: Optional[np.ndarray] = None,
    sample_fraction: float = 0.1,
    max_d: int = 10,
    min_counts_per_d: int = 50,
) -> Dict[str, float]:
    """
    Estimate the correlation length xi (in graph hops) and mass gap m_eff = 1/xi
    from a static snapshot of a scalar field on the graph.

    Inputs:
      connectome: runtime connectome with fields .A (binary adjacency) and .N
      phi: optional np.ndarray (N,) scalar field per node. If None, use a weight-derived proxy:
           phi_i := sum_j |E_ij| if connectome.E available, else degree (sum of A_i*).
      sample_fraction: fraction of nodes to use as BFS seeds (subsamples for speed)
      max_d: maximum graph distance to consider
      min_counts_per_d: require at least this many pairs per distance bin for inclusion

    Outputs (in a dict):
      {
        "xi": correlation length (hops),
        "m_eff": 1/xi,
        "r_values": number of bins used,
        "fit_slope": slope of log C(d) vs d,
        "fit_intercept": intercept,
      }

    Notes:
      - Two-point connected correlator defined as C(d) = mean_{pairs at dist d}[ (phi_i - mu)(phi_j - mu) ],
        normalized by var to reduce scale dependence. We then fit log C(d) ~ -d/xi + const.
      - If no sufficient bins, returns NaNs.
    """
    A = _ensure_adjacency(connectome)
    N = A.shape[0]

    # Field proxy if none provided
    if phi is None:
        if hasattr(connectome, "E") and isinstance(connectome.E, np.ndarray):
            # node scalar = L1 sum of incident weights (absolute)
            phi = np.sum(np.abs(connectome.E), axis=1).astype(np.float64)
        else:
            # fallback: degree
            phi = np.sum(A, axis=1).astype(np.float64)

    phi = np.asarray(phi, dtype=np.float64)
    if phi.shape[0] != N:
        raise ValueError("phi length must equal connectome.N")

    mu = float(np.mean(phi))
    var = float(np.var(phi))
    if var <= 1e-18:
        return {"xi": float("nan"), "m_eff": float("nan"), "r_values": 0, "fit_slope": float("nan"), "fit_intercept": float("nan")}

    # Subsample seeds
    rng = np.random.default_rng(12345)
    seeds = np.arange(N)
    rng.shuffle(seeds)
    keep = max(1, int(sample_fraction * N))
    seeds = seeds[:keep]

    distances_by_d = _shortest_path_distances(A, seeds, max_d=max_d)

    # Compute correlator per distance
    C_vals = []
    d_vals = []
    for d in range(1, max_d + 1):
        pairs = distances_by_d[d]
        if len(pairs) < min_counts_per_d:
            continue
        # average over pairs: connected correlator normalized by var
        num = 0.0
        for (i, j, _) in pairs:
            num += (phi[i] - mu) * (phi[j] - mu)
        C_d = (num / len(pairs)) / var
        if C_d > 1e-12:
            C_vals.append(max(C_d, 1e-12))
            d_vals.append(d)

    if len(d_vals) < 2:
        return {"xi": float("nan"), "m_eff": float("nan"), "r_values": 0, "fit_slope": float("nan"), "fit_intercept": float("nan")}

    # Fit log C(d) ~ - d/xi + const
    y = np.log(np.asarray(C_vals))
    x = np.asarray(d_vals, dtype=np.float64)
    # Least squares fit
    A_fit = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A_fit, y, rcond=None)[0]  # y = slope*x + intercept
    # slope should be negative: slope = -1/xi
    if slope >= -1e-12:
        xi = float("inf")
    else:
        xi = -1.0 / slope
    m_eff = 1.0 / xi if xi != float("inf") else 0.0

    return {
        "xi": float(xi),
        "m_eff": float(m_eff),
        "r_values": int(len(d_vals)),
        "fit_slope": float(slope),
        "fit_intercept": float(intercept),
    }


class PulseSpeedEstimator:
    """
    Online estimator for a pulse (activity front) group velocity on a graph.

    Usage:
      pse = PulseSpeedEstimator(connectome)
      pse.begin(center_node=some_index, tick=t0)
      for each tick t:
          pse.observe(tick=t, active_mask=spikes or thresholded field)
      result = pse.finalize()

    The estimator computes the mean geodesic radius of active nodes relative to the chosen center,
    then fits a linear model radius(t) ~ v_g * (t - t0) + const to recover v_g.
    """

    def __init__(self, connectome, max_radius: Optional[int] = None):
        self.A = _ensure_adjacency(connectome)
        self.N = self.A.shape[0]
        self.max_radius = max_radius if max_radius is not None else max(10, self.N // 10)
        self._dist_cache_center: Optional[int] = None
        self._dist_from_center: Optional[np.ndarray] = None
        self._t0: Optional[float] = None
        self._ts: List[float] = []
        self._radii: List[float] = []

    def _bfs_from_center(self, c: int) -> np.ndarray:
        dist = np.full(self.N, -1, dtype=np.int32)
        dist[c] = 0
        q = [c]
        head = 0
        rows = self.A
        neighbors = [np.where(rows[i] != 0)[0] for i in range(self.N)]
        while head < len(q):
            u = q[head]
            head += 1
            du = dist[u]
            if du >= self.max_radius:
                continue
            for v in neighbors[u]:
                if dist[v] == -1:
                    dist[v] = du + 1
                    q.append(v)
        return dist

    def begin(self, center_node: int, tick: float):
        self._dist_cache_center = int(center_node)
        self._dist_from_center = self._bfs_from_center(self._dist_cache_center)
        self._t0 = float(tick)
        self._ts.clear()
        self._radii.clear()

    def observe(self, tick: float, active_mask: np.ndarray):
        """
        Record the mean radius of currently active nodes.

        Args:
          tick: current time (integer tick or float time)
          active_mask: boolean array shape (N,) marking active nodes at this tick
                       (e.g., spikes, or |delta phi| > threshold)
        """
        if self._dist_from_center is None or self._t0 is None:
            raise RuntimeError("PulseSpeedEstimator.begin(...) must be called before observe(...)")

        active_mask = np.asarray(active_mask, dtype=bool)
        if active_mask.shape[0] != self.N:
            raise ValueError("active_mask length must equal number of nodes")

        idx = np.where(active_mask)[0]
        if idx.size == 0:
            return  # skip empty frames
        d = self._dist_from_center[idx]
        d = d[d >= 0]  # ignore unreachable or -1
        if d.size == 0:
            return
        mean_r = float(np.mean(d))
        self._ts.append(float(tick) - self._t0)
        self._radii.append(mean_r)

    def finalize(self) -> Dict[str, float]:
        """
        Fit radius(t) ~ v_g * (t - t0) + const. Return v_g and fit diagnostics.
        """
        if len(self._ts) < 2:
            return {"v_g": float("nan"), "frame_count": int(len(self._ts)), "slope": float("nan"), "intercept": float("nan")}
        x = np.asarray(self._ts, dtype=np.float64)
        y = np.asarray(self._radii, dtype=np.float64)
        A_fit = np.vstack([x, np.ones_like(x)]).T
        slope, intercept = np.linalg.lstsq(A_fit, y, rcond=None)[0]
        return {"v_g": float(max(0.0, slope)), "frame_count": int(len(self._ts)), "slope": float(slope), "intercept": float(intercept)}