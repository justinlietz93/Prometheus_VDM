"""
Event-driven snapshot builder (core-local).

- Aggregates lightweight telemetry from:
  * EventDrivenMetrics.snapshot()
  * ColdMap.snapshot(t)
  * Heat/Excitation/Inhibition reducer snapshots
- Pure function; no IO, no scans, no side-effects outside returning a dict.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def _safe_merge(dst: Dict[str, Any], src: Optional[Dict[str, Any]]) -> None:
    if not isinstance(src, dict):
        return
    for k, v in src.items():
        try:
            dst[k] = v
        except Exception:
            continue


def build_evt_snapshot(
    *,
    evt_metrics: Optional[Any],
    cold_map: Optional[Any],
    heat_map: Optional[Any],
    exc_map: Optional[Any],
    inh_map: Optional[Any],
    memory_map: Optional[Any] = None,
    trail_map: Optional[Any] = None,
    latest_tick: int = 0,
    nx: Any = None,
) -> Dict[str, Any]:
    """
    Construct a consolidated event-driven snapshot without mutating model state.

    Parameters:
      evt_metrics: EventDrivenMetrics instance (or None)
      cold_map: ColdMap reducer (or None)
      heat_map/exc_map/inh_map: reducers exposing snapshot() -> dict
      latest_tick: integer tick associated with this fold/snapshot
      nx: nexus-like handle (unused; reserved for future keys)

    Returns:
      dict of event-driven fields (raw keys) to be prefixed by the caller when merging
      into the canonical telemetry map (e.g., "evt_*" in CoreEngine.snapshot()).
    """
    out: Dict[str, Any] = {}

    # 1) Base event-driven metrics
    try:
        if evt_metrics is not None:
            evs = evt_metrics.snapshot()
            if isinstance(evs, dict):
                _safe_merge(out, evs)
    except Exception:
        pass

    # 2) Cold map snapshot at the current tick (bounded head only; no scans)
    try:
        if cold_map is not None:
            cs = cold_map.snapshot(int(latest_tick))
            if isinstance(cs, dict):
                _safe_merge(out, cs)
    except Exception:
        pass

    # 3) Heat/Exc/Inh reducer snapshots (bounded heads; telemetry-only)
    try:
        if heat_map is not None:
            hs = heat_map.snapshot()
            if isinstance(hs, dict):
                _safe_merge(out, hs)
    except Exception:
        pass

    try:
        if exc_map is not None:
            es = exc_map.snapshot()
            if isinstance(es, dict):
                _safe_merge(out, es)
    except Exception:
        pass

    try:
        if inh_map is not None:
            ins = inh_map.snapshot()
            if isinstance(ins, dict):
                _safe_merge(out, ins)
    except Exception:
        pass

    # 4) Optional steering fields (views): memory/trail (bounded heads/dicts; no scans)
    try:
        if memory_map is not None:
            ms = memory_map.snapshot()
            if isinstance(ms, dict):
                _safe_merge(out, ms)
    except Exception:
        pass

    try:
        if trail_map is not None:
            ts = trail_map.snapshot()
            if isinstance(ts, dict):
                _safe_merge(out, ts)
    except Exception:
        pass

    return out


__all__ = ["build_evt_snapshot"]