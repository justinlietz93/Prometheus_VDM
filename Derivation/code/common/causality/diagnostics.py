"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Convenience diagnostics that compose event_dag and intervals helpers.

These are pure functions that consume in-memory structures and return dicts.
No IO, no approvals-safe for CI and unit tests.
"""
from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Set

from .event_dag import build_event_dag, is_acyclic, transitive_reduction
from .intervals import sample_intervals, dim_from_order_fraction, fit_diamond_scaling


def dag_summary(
    events: Sequence[Tuple[str, float]],
    edges: Optional[Iterable[Tuple[str, str]]] = None,
    *,
    infer_by_time: bool = False,
    max_successors: int = 0,
    time_tolerance: float = 0.0,
    tr_edge_cap: int = 200_000,
) -> Dict[str, float | int | bool]:
    times, adj = build_event_dag(
        events,
        edges,
        infer_by_time=infer_by_time,
        max_successors=max_successors,
        time_tolerance=time_tolerance,
    )
    m = sum(len(v) for v in adj.values())
    acyclic = is_acyclic(adj)
    # TR size (best-effort)
    tr = transitive_reduction(adj, max_edges=tr_edge_cap)
    m_tr = sum(len(v) for v in tr.values())
    return {
        "n": len(times),
        "m": int(m),
        "acyclic": bool(acyclic),
        "m_tr": int(m_tr),
    }


def interval_summary(
    times: Dict[str, float],
    adj: Dict[str, Set[str]],
    *,
    k: int = 128,
    min_dt: float = 0.0,
    max_dt: Optional[float] = None,
    reach_budget: int = 8192,
) -> Dict[str, float | int]:
    samples = sample_intervals(
        times,
        adj,
        k=k,
        min_dt=min_dt,
        max_dt=max_dt,
        reach_budget=reach_budget,
    )
    n_samp = len(samples)
    if n_samp == 0:
        return {"samples": 0}
    # Dimension estimates per-sample
    ds = [dim_from_order_fraction(r) for (_p, _q, _dt, _sz, r) in samples]
    # Aggregate r as well
    rs = [r for (_p, _q, _dt, _sz, r) in samples]
    d_mean = float(sum(ds) / n_samp)
    d_min = float(min(ds)); d_max = float(max(ds))
    r_mean = float(sum(rs) / n_samp)
    # Diamond scaling slope
    slope, intercept = fit_diamond_scaling(samples)
    return {
        "samples": int(n_samp),
        "d_mean": d_mean,
        "d_min": d_min,
        "d_max": d_max,
        "r_mean": r_mean,
        "slope_logI_logDt": float(slope),
        "intercept_logI_logDt": float(intercept),
    }


def full_causality_summary(
    events: Sequence[Tuple[str, float]],
    edges: Optional[Iterable[Tuple[str, str]]] = None,
    *,
    infer_by_time: bool = False,
    max_successors: int = 0,
    time_tolerance: float = 0.0,
    k_intervals: int = 128,
    min_dt: float = 0.0,
    max_dt: Optional[float] = None,
    reach_budget: int = 8192,
    tr_edge_cap: int = 200_000,
) -> Dict[str, float | int | bool]:
    """
    One-shot combined summary: { DAG stats, interval stats, slope }.
    """
    times, adj = build_event_dag(
        events,
        edges,
        infer_by_time=infer_by_time,
        max_successors=max_successors,
        time_tolerance=time_tolerance,
    )
    dag = dag_summary(
        events,
        edges,
        infer_by_time=infer_by_time,
        max_successors=max_successors,
        time_tolerance=time_tolerance,
        tr_edge_cap=tr_edge_cap,
    )
    inter = interval_summary(
        times,
        adj,
        k=k_intervals,
        min_dt=min_dt,
        max_dt=max_dt,
        reach_budget=reach_budget,
    )
    out: Dict[str, float | int | bool] = {}
    out.update(dag)
    out.update(inter)
    return out
