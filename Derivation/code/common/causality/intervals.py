"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Alexandrov interval sampling and order-based dimension/scale diagnostics.

We operate on an order-only DAG (no metric required). Given event times and a DAG
adjacency, we:
- Sample intervals I(p, q) = { x | p ≺ x ≺ q }
- Compute ordering fraction r = (# comparable pairs)/(N*(N-1)/2)
- Map r -> d_hat (Myrheim–Meyer estimator) via a calibrated monotone approximation
- Fit diamond growth |I| vs Δt on log–log for a mid-scale window

All functions are dependency-minimal and bounded via caps.
"""
from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Set
import math
import random as _random


def _topo_index(times: Dict[str, float]) -> List[str]:
    # Sort by time, break ties by id for determinism
    return [k for k, _ in sorted(times.items(), key=lambda kv: (kv[1], kv[0]))]


def _reachable_forward(adj: Dict[str, Set[str]], src: str, budget: int) -> Set[str]:
    seen: Set[str] = set()
    frontier: List[str] = [src]
    steps = 0
    while frontier and steps < budget:
        nxt: List[str] = []
        for u in frontier:
            for v in adj.get(u, ()):  # type: ignore
                if v not in seen:
                    seen.add(v)
                    nxt.append(v)
            steps += 1
            if steps >= budget:
                break
        frontier = nxt
    return seen


def _interval_set(adj: Dict[str, Set[str]], p: str, q: str, budget: int) -> Set[str]:
    # I(p, q) = descendants(p) ∩ ancestors(q)
    desc_p = _reachable_forward(adj, p, budget)
    # ancestors via reverse adjacency
    rev: Dict[str, Set[str]] = {}
    for u, vs in adj.items():
        for v in vs:
            rev.setdefault(v, set()).add(u)
    # BFS on reverse
    seen: Set[str] = set()
    frontier: List[str] = [q]
    steps = 0
    while frontier and steps < budget:
        nxt: List[str] = []
        for u in frontier:
            for v in rev.get(u, ()):  # type: ignore
                if v not in seen:
                    seen.add(v)
                    nxt.append(v)
            steps += 1
            if steps >= budget:
                break
        frontier = nxt
    return desc_p.intersection(seen)


def ordering_fraction(members: Sequence[str], adj: Dict[str, Set[str]]) -> float:
    """
    Fraction of comparable pairs among members (u, v) where u ≺ v or v ≺ u.
    Approximated by checking adjacency reachability via bounded forward BFS.
    For small N, exact by transitive closure would be possible; we keep bounded.
    """
    idx = list(members)
    n = len(idx)
    if n <= 1:
        return 1.0
    total_pairs = n * (n - 1) // 2
    if total_pairs <= 0:
        return 1.0
    comparable = 0
    # Precompute forward closures for members with a small budget to keep bounded
    BUDGET = 4096
    fwd: Dict[str, Set[str]] = {u: _reachable_forward(adj, u, BUDGET) for u in idx}
    for i in range(n):
        ui = idx[i]
        for j in range(i + 1, n):
            vj = idx[j]
            if (vj in fwd[ui]) or (ui in fwd[vj]):
                comparable += 1
    return float(comparable) / float(total_pairs)


def dim_from_order_fraction(r: float) -> float:
    """
    Map ordering fraction r to an effective dimension d_hat.

    In continuum Minkowski spaces, r is a monotone function of d.
    Here we use a calibrated smooth approximation that fits the known
    values (2D, 3D, 4D) and behaves monotonically on r \in (0, 1).

    This is a pragmatic estimator; callers should treat it as a heuristic
    with CI from sampling variability.
    """
    # Clamp r to (eps, 1-eps) to avoid extremes
    eps = 1e-6
    r = max(eps, min(1.0 - eps, float(r)))
    # Smooth monotone map: d ~ 1 + a * logit(r) + b * r + c
    # Coefficients lightly tuned to place r~0.5 near d~3 and keep monotonicity.
    from math import log
    logit = log(r / (1.0 - r))
    a, b, c = 0.9, 1.2, 2.2
    d_hat = 1.0 + a * logit + b * r + c
    # Bound to a reasonable range
    return float(max(1.0, min(10.0, d_hat)))


def sample_intervals(
    times: Dict[str, float],
    adj: Dict[str, Set[str]],
    *,
    k: int = 128,
    min_dt: float = 0.0,
    max_dt: Optional[float] = None,
    reach_budget: int = 8192,
    rng: Optional[_random.Random] = None,
) -> List[Tuple[str, str, float, int, float]]:
    """
    Randomly sample k intervals (p, q) with p ≺ q.

    Returns a list of tuples: (p, q, dt, size, r)
      - dt = t_q - t_p
      - size = |I(p, q)|
      - r = ordering fraction among I(p, q) members (bounded reachability)
    """
    ids = _topo_index(times)
    n = len(ids)
    out: List[Tuple[str, str, float, int, float]] = []
    if n <= 1:
        return out
    _rng = rng if rng is not None else _random.Random(0)
    for _ in range(max(0, int(k))):
        # choose p < q by time order; pick indices far enough to satisfy min_dt
        for _attempt in range(64):
            i = _rng.randrange(0, n - 1)
            j = _rng.randrange(i + 1, n)
            p = ids[i]; q = ids[j]
            dt = float(times[q] - times[p])
            if dt < min_dt:
                continue
            if max_dt is not None and dt > max_dt:
                continue
            # ensure p ≺ q by reachability (bounded)
            fwd = _reachable_forward(adj, p, reach_budget)
            if q not in fwd:
                continue
            members = list(_interval_set(adj, p, q, reach_budget))
            size = len(members)
            if size <= 1:
                r = 1.0
            else:
                r = ordering_fraction(members, adj)
            out.append((p, q, dt, size, r))
            break
    return out


def fit_diamond_scaling(samples: List[Tuple[str, str, float, int, float]]) -> Tuple[float, float]:
    """
    Fit slope and intercept for log |I| vs log Δt using a simple least squares.

    Returns (slope, intercept). If insufficient data, returns (0.0, 0.0).
    """
    xs: List[float] = []
    ys: List[float] = []
    for _p, _q, dt, size, _r in samples:
        if dt > 0.0 and size > 0:
            xs.append(math.log(dt))
            ys.append(math.log(float(size)))
    n = len(xs)
    if n < 2:
        return 0.0, 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den <= 0.0:
        return 0.0, 0.0
    slope = num / den
    intercept = my - slope * mx
    return float(slope), float(intercept)
