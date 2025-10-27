"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
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
import os as _os

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

    # Fairness: rotate starting scout by tick (round-robin) to avoid starvation
    start_idx = 0
    try:
        if isinstance(budget, dict):
            start_idx = int(budget.get("tick", 0))
    except Exception:
        start_idx = 0

    ordered: List[Any] = list(scouts or [])
    n_sc = len(ordered)
    if n_sc > 0 and start_idx:
        try:
            k = start_idx % n_sc
            ordered = ordered[k:] + ordered[:k]
        except Exception:
            # fallback: keep original order
            ordered = list(scouts or [])

    # Optional per-scout micro-slice (still one-shot runner; no schedulers)
    per_us = 0
    try:
        per_us = int(_os.getenv("SCOUTS_PER_SCOUT_US", "0"))
    except Exception:
        per_us = 0
    if per_us <= 0 and max_us > 0 and n_sc > 0:
        per_us = int(max_us // max(1, n_sc))

    for sc in ordered:
        # Global time guard (drop rest on over-budget)
        if max_us > 0:
            elapsed_us = (perf_counter_ns() - t0) // 1000
            if elapsed_us >= max_us:
                break

        sc_t0 = perf_counter_ns()
        try:
            out = sc.step(connectome=connectome, bus=None, maps=maps, budget=budget) or []
        except Exception:
            out = []
        if out:
            evs.extend(out)

        # Per-scout guard (best-effort; cannot preempt inside step)
        if per_us > 0:
            sc_elapsed_us = (perf_counter_ns() - sc_t0) // 1000
            if sc_elapsed_us > per_us:
                # soft-guard only: we don't penalize the scout, but this informs future tuning
                pass

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