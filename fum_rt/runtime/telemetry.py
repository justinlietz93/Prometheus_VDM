from __future__ import annotations

"""
Runtime telemetry packaging seam (Phase B).

Goals:
- Provide small, behavior-preserving builders for 'why' and 'status' payloads.
- Keep core numeric only; this module formats dicts but performs no logging or IO.
- Mirror existing Nexus packaging exactly to ensure byte-for-byte parity.

Policy:
- May import typing and stdlib only.
- No imports from io.* emitters; no file or JSON writes here.
"""

from typing import Any, Dict, Iterable, Set, Callable, Optional, Tuple, List


def macro_why_base(nx: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Build the base 'why' dict used for macro emissions (before any caller-specific fields).
    Mirrors the inline block in Nexus: uses current metrics with explicit numeric casts.

    Caller may extend with additional telemetry fields, e.g. novelty_idf, composer_idf_k.
    """
    m = metrics or {}
    try:
        phase = int(getattr(nx, "_phase", {}).get("phase", 0))
    except Exception:
        try:
            phase = int(m.get("phase", 0))
        except Exception:
            phase = 0

    return {
        "t": int(step),
        "phase": phase,
        "b1_z": float(m.get("b1_z", 0.0)),
        "cohesion_components": int(m.get("cohesion_components", 0)),
        "vt_coverage": float(m.get("vt_coverage", 0.0)),
        "vt_entropy": float(m.get("vt_entropy", 0.0)),
        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
        "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0))),
    }


def status_payload(nx: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Build the open UTD status payload.
    Mirrors the inline block from Nexus with identical keys and casts.
    """
    m = metrics or {}
    try:
        phase = int(m.get("phase", int(getattr(nx, "_phase", {}).get("phase", 0))))
    except Exception:
        phase = 0

    return {
        "type": "status",
        "t": int(step),
        "neurons": int(getattr(nx, "N", 0)),
        "phase": phase,
        "cohesion_components": int(m.get("cohesion_components", 0)),
        "vt_coverage": float(m.get("vt_coverage", 0.0)),
        "vt_entropy": float(m.get("vt_entropy", 0.0)),
        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
        "active_edges": int(m.get("active_edges", 0)),
        "homeostasis_pruned": int(m.get("homeostasis_pruned", 0)),
        "homeostasis_bridged": int(m.get("homeostasis_bridged", 0)),
        "b1_z": float(m.get("b1_z", 0.0)),
        "adc_territories": int(m.get("adc_territories", 0)),
        "adc_boundaries": int(m.get("adc_boundaries", 0)),
        "sie_total_reward": float(m.get("sie_total_reward", 0.0)),
        "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
        "sie_v2_reward_mean": float(m.get("sie_v2_reward_mean", 0.0)),
        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", 0.0)),
        "ute_in_count": int(m.get("ute_in_count", 0)),
        "ute_text_count": int(m.get("ute_text_count", 0)),
    }


# --- Tick Telemetry Fold (bus drain + ADC + optional event-driven metrics + B1) ---

class _DynObs:
    """
    Minimal observation object for publishing runtime 'delta' events to the bus
    without importing core.announce.Observation. Adapter reads via getattr().
    """
    __slots__ = ("tick", "kind", "nodes", "meta")

    def __init__(self, tick: int, kind: str, nodes: Optional[Iterable[int]] = None, meta: Optional[Dict[str, Any]] = None) -> None:
        self.tick = int(tick)
        self.kind = str(kind)
        self.nodes = list(nodes or [])
        self.meta = dict(meta or {})


def tick_fold(
    nx: Any,
    metrics: Dict[str, Any],
    drive: Dict[str, Any],
    td_signal: float,
    step: int,
    tick_rev_map: Optional[Dict[int, Any]] = None,
    *,
    obs_to_events: Optional[Callable[[Iterable[Any]], Iterable[Any]]] = None,
    adc_event: Optional[Callable[[Dict[str, Any], int], Any]] = None,
    apply_b1: Optional[Callable[[Any, Dict[str, Any], int], Dict[str, Any]]] = None,
) -> Tuple[Dict[str, Any], Set[Any]]:
    """
    Behavior-preserving fold of per-tick runtime telemetry:
      - Optionally publish a 'delta' event (feature-flagged) to the announce bus
      - Drain bus and derive void-topic symbols using tick_rev_map
      - Update ADC from drained observations; merge adc metrics
      - Optionally fold event-driven metrics (feature-flagged)
      - Update complexity proxy and apply B1 detector (via callback)
    Returns (metrics, void_topic_symbols)
    """
    m = metrics if isinstance(metrics, dict) else {}
    void_topic_symbols: Set[Any] = set()

    # 1) Optional delta event publish (telemetry-only; no dynamics change)
    try:
        if getattr(nx, "_evt_metrics", None) is not None:
            comps = {}
            try:
                comps = dict(drive.get("components", {}) or {})
            except Exception:
                comps = {}
            meta = {
                "b1": 0.0,  # cycle_hit provides primary b1 contributions; keep delta neutral
                "nov": float(comps.get("nov", 0.0)) if isinstance(comps, dict) else 0.0,
                "hab": float(comps.get("hab", 0.0)) if isinstance(comps, dict) else 0.0,
                "td": float(td_signal),
                "hsi": float(comps.get("hsi", 0.0)) if isinstance(comps, dict) else 0.0,
            }
            try:
                bus = getattr(nx, "bus", None)
                if bus is not None:
                    bus.publish(_DynObs(tick=int(step), kind="delta", nodes=[], meta=meta))
            except Exception:
                pass
    except Exception:
        pass

    # 2) Drain bus, derive topic symbols, update ADC, and fold event-driven metrics
    try:
        bus = getattr(nx, "bus", None)
        if bus is not None:
            obs_batch = bus.drain(max_items=int(getattr(nx, "bus_drain", 2048)))
            if obs_batch:
                # Map observed node indices back to symbols seen this tick
                try:
                    if isinstance(tick_rev_map, dict):
                        for obs in obs_batch:
                            try:
                                nodes = getattr(obs, "nodes", None)
                                if nodes:
                                    for idx in nodes:
                                        sym = tick_rev_map.get(int(idx))
                                        if sym is not None:
                                            void_topic_symbols.add(sym)
                            except Exception:
                                continue
                except Exception:
                    pass

                # Update ADC after extracting topic so we don't interfere with its logic
                try:
                    adc = getattr(nx, "adc", None)
                    if adc is not None:
                        adc.update_from(obs_batch)
                        adc_metrics = adc.get_metrics()
                    else:
                        adc_metrics = {}
                except Exception:
                    adc_metrics = {}

                # Optionally fold event-driven metrics telemetry
                try:
                    evtm = getattr(nx, "_evt_metrics", None)
                    if evtm is not None:
                        if obs_to_events is not None:
                            try:
                                for _ev in obs_to_events(obs_batch) or []:
                                    try:
                                        evtm.update(_ev)
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                        if adc_event is not None:
                            try:
                                evtm.update(adc_event(adc_metrics, t=int(step)))
                            except Exception:
                                pass
                        try:
                            evsnap = evtm.snapshot()
                            if isinstance(evsnap, dict):
                                # Do not override legacy scan-based metrics; prefix event-driven keys.
                                for _k, _v in evsnap.items():
                                    try:
                                        # Preserve existing B1 detector outputs from apply_b1
                                        if str(_k).startswith("b1_") and _k in m:
                                            continue
                                        m[f"evt_{_k}"] = _v
                                    except Exception:
                                        continue
                        except Exception:
                            pass
                except Exception:
                    pass

                # Fold ADC metrics and complexity proxy
                try:
                    if isinstance(adc_metrics, dict):
                        m.update(adc_metrics)
                        m["complexity_cycles"] = float(m.get("complexity_cycles", 0.0)) + float(adc_metrics.get("adc_cycle_hits", 0.0))
                except Exception:
                    pass
    except Exception:
        pass

    # 3) Apply B1 detector via provided seam (preserves detector parameters and gating)
    try:
        if apply_b1 is not None:
            m = apply_b1(nx, m, int(step))
    except Exception:
        pass

    return m, void_topic_symbols

__all__ = ["macro_why_base", "status_payload", "tick_fold"]