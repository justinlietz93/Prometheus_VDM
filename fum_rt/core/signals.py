from __future__ import annotations

"""
Core signals seam (Phase B): stable function-level API for core numeric signals.

Intent:
- Define pure, numeric helpers that outside layers can depend on immediately.
- Initially forward to existing math/state (move-only). No logging/IO/emitters here.
- Safe defaults return 0.0/0 for unavailable signals to preserve behavior.

Rules:
- May import only fum_rt.core.* and numeric libs. Never import fum_rt.io.* or fum_rt.runtime.*.
- These helpers do not mutate external state; they read and derive scalars/dicts.

Migration path:
- Phase C will move incremental/event-driven implementations into core.{cortex,proprioception,neuroplasticity},
  and these wrappers will dispatch to the new implementations while preserving the same signatures.
"""

from typing import Any, Dict, Tuple
from fum_rt.core.metrics import compute_metrics


def _safe_getattr(obj: Any, name: str, default: float = 0.0) -> float:
    try:
        return float(getattr(obj, name))
    except Exception:
        return float(default)


def compute_b1_z(state: Any) -> float:
    """
    Derive b1_z scalar in a behavior-preserving way.

    Priority (non-mutating):
    1) Connectome intrinsic last b1_z if exposed by a detector cache (not guaranteed).
    2) Last computed runtime metrics if available on the 'state' (e.g., Nexus._emit_last_metrics).
    3) Recompute metrics via compute_metrics(connectome) and read 'b1_z' if exposed by runtime stack.
    4) Fallback to 0.0.

    Note: This is a seam; future implementations will obtain b1_z from event-driven reducers in core.
    """
    # 1) connectome-local cache (rare)
    try:
        cz = getattr(getattr(state, "connectome", None), "_last_b1_z", None)
        if cz is not None:
            return float(cz)
    except Exception:
        pass

    # 2) runtime snapshot cache
    try:
        m = getattr(state, "_emit_last_metrics", None)
        if isinstance(m, dict) and "b1_z" in m:
            return float(m.get("b1_z", 0.0))
    except Exception:
        pass

    # 3) recompute metrics and read b1_z if runtime contributes it
    try:
        C = getattr(state, "connectome", None)
        if C is not None:
            m2 = compute_metrics(C)
            return float(m2.get("b1_z", 0.0))
    except Exception:
        pass

    # 4) default
    return 0.0


def sie_valence(state: Any, dstate: Any = None) -> float:
    """
    Derive valence scalar in [0,1] using current prioritized sources:

    Priority:
    1) Connectome intrinsic SIE v2 snapshot (preferred): connectome._last_sie2_valence
    2) Runtime SieEngine legacy valence if exposed via last metrics or engine
    3) compute_metrics(connectome) field: 'sie_v2_valence_01' or 'sie_valence_01'
    4) Fallback 0.0

    This is read-only and does not alter SIE internals.
    """
    # 1) intrinsic v2
    try:
        v2 = getattr(getattr(state, "connectome", None), "_last_sie2_valence", None)
        if v2 is not None:
            return float(v2)
    except Exception:
        pass

    # 2) runtime last metrics cache
    try:
        m = getattr(state, "_emit_last_metrics", None)
        if isinstance(m, dict):
            if "sie_v2_valence_01" in m:
                return float(m.get("sie_v2_valence_01", 0.0))
            if "sie_valence_01" in m:
                return float(m.get("sie_valence_01", 0.0))
    except Exception:
        pass

    # 3) recompute metrics
    try:
        C = getattr(state, "connectome", None)
        if C is not None:
            m2 = compute_metrics(C)
            if "sie_v2_valence_01" in m2:
                return float(m2.get("sie_v2_valence_01", 0.0))
            return float(m2.get("sie_valence_01", 0.0))
    except Exception:
        pass

    return 0.0


def compute_cohesion(state: Any) -> int:
    """
    Compute/derive cohesion_components (approximate number of connected components
    in active subgraph, as defined by the current runtime metrics layer).

    Priority:
    1) Use last metrics cache when present.
    2) Recompute via compute_metrics(connectome).
    3) Fallback 0.
    """
    # 1) cache
    try:
        m = getattr(state, "_emit_last_metrics", None)
        if isinstance(m, dict) and "cohesion_components" in m:
            return int(m.get("cohesion_components", 0))
    except Exception:
        pass

    # 2) recompute
    try:
        C = getattr(state, "connectome", None)
        if C is not None:
            m2 = compute_metrics(C)
            return int(m2.get("cohesion_components", 0))
    except Exception:
        pass

    return 0


def compute_vt_metrics(state: Any) -> Tuple[float, float]:
    """
    Derive (vt_coverage, vt_entropy).

    Priority:
    1) Last metrics cache if present on state
    2) compute_metrics(connectome)
    3) Fallback (0.0, 0.0)
    """
    # 1) cache
    try:
        m = getattr(state, "_emit_last_metrics", None)
        if isinstance(m, dict):
            if "vt_coverage" in m or "vt_entropy" in m:
                cov = float(m.get("vt_coverage", 0.0))
                ent = float(m.get("vt_entropy", 0.0))
                return (cov, ent)
    except Exception:
        pass

    # 2) recompute
    try:
        C = getattr(state, "connectome", None)
        if C is not None:
            m2 = compute_metrics(C)
            cov = float(m2.get("vt_coverage", 0.0))
            ent = float(m2.get("vt_entropy", 0.0))
            return (cov, ent)
    except Exception:
        pass

    # 3) default
    return (0.0, 0.0)


def snapshot_numbers(state: Any) -> Dict[str, float]:
    """
    Convenience aggregator that composes the core snapshot dictionary expected
    by the runtime telemetry seam. Non-intrusive and read-only.

    Returns:
      {
        "b1_z": float, "vt_coverage": float, "vt_entropy": float,
        "cohesion_components": int, "sie_valence_01": float, "sie_v2_valence_01": float
      }
    """
    cov, ent = compute_vt_metrics(state)
    # Gather as many values as are cheaply available
    out: Dict[str, float] = {
        "b1_z": float(compute_b1_z(state)),
        "vt_coverage": float(cov),
        "vt_entropy": float(ent),
        "cohesion_components": float(compute_cohesion(state)),
        "sie_valence_01": 0.0,
        "sie_v2_valence_01": 0.0,
    }
    # attempt to fill valence fields
    try:
        v2 = sie_valence(state)
        out["sie_v2_valence_01"] = float(v2)
    except Exception:
        pass
    try:
        m = getattr(state, "_emit_last_metrics", None)
        if isinstance(m, dict) and "sie_valence_01" in m:
            out["sie_valence_01"] = float(m.get("sie_valence_01", 0.0))
    except Exception:
        pass
    return out


__all__ = [
    "compute_b1_z",
    "sie_valence",
    "compute_cohesion",
    "compute_vt_metrics",
    "snapshot_numbers",
]