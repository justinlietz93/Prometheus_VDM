from __future__ import annotations

"""
fum_rt.core.cortex.void_walkers.runner

Stateless, per-tick scout executor (void-faithful, no schedulers).
- Runs a bounded list of read-only scouts exactly once per tick.
- Enforces a micro time budget (microseconds) across all scouts.
- Accepts optional seeds (e.g., recent UTE indices) and map heads (heat/exc/inh/cold).
- Emits only foldable events (vt_touch, edge_on, optional spike/delta_w); no writes.

Usage (in runtime loop per tick):
    from fum_rt.core.cortex.void_walkers.runner import run_scouts_once as _run_scouts_once
    evs = _run_scouts_once(connectome, scouts, maps, budget, bus, max_us)

Notes:
- No timers, no cadence, no background threads. This is a pure function called once per tick.
- Drop-oldest behavior is delegated to the downstream bus implementation when publish_many is used.
"""

from typing import Any, Dict, Iterable, List, Optional, Sequence
from time import perf_counter_ns

from fum_rt.core.proprioception.events import BaseEvent


def _truthy(x: Any) -> bool:
    try:
        if isinstance(x, (int, float, bool)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False


def run_scouts_once(
    connectome: Any,
    scouts: Sequence[Any],
    maps: Optional[Dict[str, Any]] = None,
    budget: Optional[Dict[str, int]] = None,
    bus: Any = None,
    max_us: int = 2000,
) -> List[BaseEvent]:
    """
    Execute a bounded batch of scouts exactly once for this tick.

    Parameters:
      - connectome: object exposing read-only neighbor access (N, neighbors/get_neighbors or adj mapping)
      - scouts: sequence of instantiated scout objects with .step(connectome, bus, maps, budget) -> list[BaseEvent]
      - maps: optional dict of map heads: {"heat_head": [[node,score],...], "exc_head": [...], "inh_head": [...], "cold_head": [...]}
      - budget: {"visits": int, "edges": int, "ttl": int, "tick": int, "seeds": list[int]} (any subset)
      - bus: optional announce bus; when present, publish_many(evs) is invoked once at end
      - max_us: total per-tick microsecond budget across all scouts

    Returns:
      - list of BaseEvent emitted by all scouts within budget
    """
    evs: List[BaseEvent] = []
    if not scouts:
        return evs

    # Ensure safe numeric bounds
    try:
        max_us = int(max(0, int(max_us)))
    except Exception:
        max_us = 0  # 0 → gather but still permit at least the first scout call if desired

    t0 = perf_counter_ns()
    for sc in scouts:
        # Time guard (drop rest on over-budget)
        if max_us > 0:
            elapsed_us = (perf_counter_ns() - t0) // 1000
            if elapsed_us >= max_us:
                break

        # Execute one scout with the common budget
        try:
            out = sc.step(connectome=connectome, bus=None, maps=maps, budget=budget) or []
        except Exception:
            out = []
        if out:
            evs.extend(out)

    # Publish once (drop-oldest semantics live in bus implementation)
    if evs and bus is not None:
        try:
            if hasattr(bus, "publish_many"):
                bus.publish_many(evs)
            else:
                # bounded fallback
                for e in evs:
                    try:
                        bus.publish(e)  # type: ignore[attr-defined]
                    except Exception:
                        break
        except Exception:
            pass

    return evs


__all__ = ["run_scouts_once"]