"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
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


def apply_b1_detector(state: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Behavior-preserving B1 detector update using state.b1_detector.
    Mutates metrics in place; returns metrics for convenience.

    This seam delegates to the existing StreamingZEMA instance configured in runtime (Nexus.b1_detector),
    avoiding any duplication of detector parameters and preserving gating behavior.
    """
    m = metrics if isinstance(metrics, dict) else {}
    try:
        b1_value = float(m.get("complexity_cycles", 0.0))
    except Exception:
        b1_value = 0.0
    try:
        det = getattr(state, "b1_detector", None)
        if det is not None:
            z = det.update(b1_value, tick=int(step))
            m["b1_value"] = float(z.get("value", 0.0))
            m["b1_delta"] = float(z.get("delta", 0.0))
            m["b1_z"] = float(z.get("z", 0.0))
            m["b1_spike"] = bool(z.get("spike", False))
    except Exception:
        # Leave metrics unchanged on failure
        pass
    return m


def compute_active_edge_density(connectome: Any, N: int) -> Tuple[int, float]:
    """
    Compute undirected active-edge density and return (E, density).

    Mirrors Nexus logic (behavior-preserving):
      E = max(0, active_edge_count)
      N = max(1, N)
      density = 2*E / (N*(N-1)) if denom > 0 else 0
    """
    try:
        E = max(0, int(connectome.active_edge_count()))
        Nn = max(1, int(N))
        denom = float(Nn * (Nn - 1))
        density = (2.0 * E / denom) if denom > 0.0 else 0.0
        return int(E), float(density)
    except Exception:
        return 0, 0.0


def compute_td_signal(prev_E: int | None, E: int, vt_prev: float | None = None, vt_last: float | None = None) -> float:
    """
    Compute TD-like signal combining structural change (delta_e) and traversal entropy change (vt_delta).

    Behavior-preserving mapping from Nexus:
      delta_e  = (E - prev_E) / max(1, E)                  # prev_E defaults to E on first use → 0
      vt_delta = 0.0 if missing else (vt_last - vt_prev)
      td_raw   = 4.0*delta_e + 1.5*vt_delta
      td       = clip(td_raw, -2.0,  2.0)
    """
    try:
        E_int = int(E)
        pE = E_int if prev_E is None else int(prev_E)
        delta_e = float(E_int - pE) / float(max(1, E_int))
    except Exception:
        delta_e = 0.0

    try:
        if vt_prev is None or vt_last is None:
            vt_delta = 0.0
        else:
            vt_delta = float(vt_last) - float(vt_prev)
    except Exception:
        vt_delta = 0.0

    td_raw = 4.0 * float(delta_e) + 1.5 * float(vt_delta)
    if td_raw > 2.0:
        return 2.0
    if td_raw < -2.0:
        return -2.0
    return float(td_raw)


def compute_firing_var(connectome: Any) -> float | None:
    """
    Compute variance of the field W; None on failure.
    """
    try:
        return float(connectome.W.var())
    except Exception:
        return None


__all__ = [
    "compute_b1_z",
    "sie_valence",
    "compute_cohesion",
    "compute_vt_metrics",
    "snapshot_numbers",
    "apply_b1_detector",
    "compute_active_edge_density",
    "compute_td_signal",
    "compute_firing_var",
]