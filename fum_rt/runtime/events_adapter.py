"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime adapter: Convert connectome Observation events into core event-driven metrics inputs.

Design:
- Pure adapter: no logging/IO; small and deterministic.
- Safe: returns an empty list for unknown/unsupported events.
- Behavior-preserving by default: only used when ENABLE_EVENT_METRICS=1.
"""

from typing import Any, Dict, Iterable, List
from fum_rt.core.proprioception.events import (
    BaseEvent,
    DeltaEvent,
    VTTouchEvent,
    SpikeEvent,
    DeltaWEvent,
    EdgeOnEvent,
    ADCEvent,
)


def observations_to_events(observations: Iterable[Any]) -> List[BaseEvent]:
    """
    Map connectome Observation objects to EventDrivenMetrics events.
    Supported kinds:
      - "cycle_hit":   -> DeltaEvent (b1 from loop_gain if available) + EdgeOnEvent(u,v) when nodes include two ids
                         Also synthesizes bounded excitatory SpikeEvent for the touched endpoints.
      - "region_stat": -> VTTouchEvent per node (weight 1.0) and bounded excitatory SpikeEvent per node (amp from s_mean or 1.0)
      - "delta_w":     -> DeltaWEvent per node (bounded fan-out).
                         Additionally, when dw < 0, synthesize bounded inhibitory SpikeEvent (sign=-1, amp=|dw| clipped)
                         to provide an inhibition source without scans.

    Unknown kinds are ignored.
    """
    out: List[BaseEvent] = []
    if not observations:
        return out

    for obs in observations:
        try:
            kind = getattr(obs, "kind", None)
            tick = int(getattr(obs, "tick", 0))
        except Exception:
            continue

        if kind == "cycle_hit":
            try:
                loop_gain = float(getattr(obs, "loop_gain", 0.0))
            except Exception:
                loop_gain = 0.0
            # Use non-negative contribution to the b1 accumulator
            b1_contrib = loop_gain if loop_gain > 0.0 else 1.0
            out.append(DeltaEvent(kind="delta", t=tick, b1=float(b1_contrib)))
            try:
                nodes = list(getattr(obs, "nodes", []) or [])
                if len(nodes) >= 2:
                    u, v = int(nodes[0]), int(nodes[1])
                    out.append(EdgeOnEvent(kind="edge_on", t=tick, u=u, v=v))
                # Also synthesize excitatory SpikeEvents for the endpoints (bounded, event-driven)
                try:
                    amp = loop_gain if loop_gain > 0.0 else 1.0
                except Exception:
                    amp = 1.0
                for idx in nodes[:2]:
                    try:
                        out.append(SpikeEvent(kind="spike", t=tick, node=int(idx), amp=float(amp), sign=+1))
                    except Exception:
                        continue
            except Exception:
                pass

        elif kind == "region_stat":
            try:
                nodes = list(getattr(obs, "nodes", []) or [])
                for node in nodes:
                    out.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(node), w=1.0))
                # Synthesize excitatory SpikeEvent per node using s_mean as amplitude when available
                try:
                    s_mean = float(getattr(obs, "s_mean", 0.0))
                except Exception:
                    s_mean = 0.0
                amp = s_mean if s_mean > 0.0 else 1.0
                for node in nodes:
                    out.append(SpikeEvent(kind="spike", t=tick, node=int(node), amp=float(amp), sign=+1))
            except Exception:
                pass

        elif kind == "delta":
            # Generic learning delta event; fields are expected in obs.meta
            try:
                meta = getattr(obs, "meta", {}) or {}
                b1 = float(meta.get("b1", 0.0))
                nov = float(meta.get("nov", 0.0))
                hab = float(meta.get("hab", 0.0))
                tdv = float(meta.get("td", 0.0))
                hsi = float(meta.get("hsi", 0.0))
                out.append(
                    DeltaEvent(
                        kind="delta",
                        t=tick,
                        b1=b1,
                        novelty=nov,
                        hab=hab,
                        td=tdv,
                        hsi=hsi,
                    )
                )
            except Exception:
                pass

        elif kind == "delta_w":
            # Map Observation(kind='delta_w') -> one or more DeltaWEvent(s)
            # Also synthesize inhibitory SpikeEvent when dw < 0 (bounded fan-out) to drive InhibitionMap without scans.
            try:
                nodes = list(getattr(obs, "nodes", []) or [])
                meta = dict(getattr(obs, "meta", {}) or {})
                dwv = float(meta.get("dw", 0.0))
                # Determine inhibitory synthesis parameters
                is_inh = dwv < 0.0
                inh_amp = float(min(1.0, abs(dwv))) if is_inh else 0.0
                # Bound fan-out defensively
                for node in nodes[:16]:
                    ni = int(node)
                    out.append(DeltaWEvent(kind="delta_w", t=tick, node=ni, dw=float(dwv)))
                    # Provide an explicit inhibitory spike source when dw is negative
                    if is_inh and inh_amp > 0.0:
                        out.append(SpikeEvent(kind="spike", t=tick, node=ni, amp=inh_amp, sign=-1))
            except Exception:
                pass

        else:
            # ignore unknown kinds
            pass

    return out


def adc_metrics_to_event(metrics: Dict[str, Any], t: int) -> ADCEvent:
    """
    Convert ADC metrics dict into a single ADCEvent for folding.
    Expected keys (optional):
      - adc_territories
      - adc_boundaries
      - adc_cycle_hits
    """
    try:
        terr = metrics.get("adc_territories", None)
        bnd = metrics.get("adc_boundaries", None)
        cyc = metrics.get("adc_cycle_hits", None)
    except Exception:
        terr = bnd = cyc = None

    try:
        terr_i = None if terr is None else int(terr)
    except Exception:
        terr_i = None
    try:
        bnd_i = None if bnd is None else int(bnd)
    except Exception:
        bnd_i = None
    try:
        cyc_f = None if cyc is None else float(cyc)
    except Exception:
        cyc_f = None

    return ADCEvent(kind="adc", t=int(t), adc_territories=terr_i, adc_boundaries=bnd_i, adc_cycle_hits=cyc_f)