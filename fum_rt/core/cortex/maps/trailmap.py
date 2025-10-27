"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.cortex.maps.trailmap
Purpose: Short half-life trail/repulsion map updated only by events (void-faithful, no scans).

Design:
- Event-driven only; folds vt_touch and edge_on into a fast-decaying accumulator.
- Intended as a light repulsion field to discourage immediate retracing (fan-out).
- Bounded working set via BaseDecayMap.keep_max (no global scans).

Snapshot keys:
- trail_head: top-k [[node, score], ...]
- trail_dict: bounded dict {node: score} over current working set (len ≤ keep_max)
"""

from typing import Iterable, Dict

from .base_decay_map import BaseDecayMap
from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent, SpikeEvent, DeltaWEvent


class TrailMap(BaseDecayMap):
    """
    Short half-life trail/repulsion map.

    Parameters:
      - half_life_ticks: decay half-life in ticks (defaults short, e.g., 50)
      - vt_touch_gain: increment for a node touch (small, e.g., 0.15)
      - edge_gain: increment applied to both endpoints of an edge_on (very small, e.g., 0.05)
      - spike_gain / dW_gain: optional small contributions to treat bursts as footprints
    """

    __slots__ = ("vt_touch_gain", "edge_gain", "spike_gain", "dW_gain")

    def __init__(
        self,
        head_k: int = 256,
        half_life_ticks: int = 50,
        keep_max: int | None = None,
        seed: int = 0,
        vt_touch_gain: float = 0.15,
        edge_gain: float = 0.05,
        spike_gain: float = 0.05,
        dW_gain: float = 0.02,
    ):
        super().__init__(head_k, half_life_ticks, keep_max, seed)
        self.vt_touch_gain = float(vt_touch_gain)
        self.edge_gain = float(edge_gain)
        self.spike_gain = float(spike_gain)
        self.dW_gain = float(dW_gain)

    def fold(self, events: Iterable[object], tick: int) -> None:
        """
        Fold a batch of events into the trail accumulator.

        Void-faithful:
        - Only uses provided events; no adjacency/weight scans.
        - Updates are strictly local to the nodes appearing in events.
        """
        t = int(tick)
        for e in events:
            k = getattr(e, "kind", None)
            if k == "vt_touch" and isinstance(e, VTTouchEvent):
                self.add(int(e.token), t, self.vt_touch_gain * float(getattr(e, "w", 1.0)))
            elif k == "edge_on" and isinstance(e, EdgeOnEvent):
                # Apply a small footprint on both endpoints
                u = int(getattr(e, "u", -1))
                v = int(getattr(e, "v", -1))
                if u >= 0:
                    self.add(u, t, self.edge_gain)
                if v >= 0:
                    self.add(v, t, self.edge_gain)
            elif k == "spike" and isinstance(e, SpikeEvent):
                self.add(int(e.node), t, self.spike_gain * float(getattr(e, "amp", 1.0)))
            elif k == "delta_w" and isinstance(e, DeltaWEvent):
                self.add(int(e.node), t, self.dW_gain * abs(float(e.dw)))

    def snapshot(self, head_n: int = 16) -> dict:
        """
        Export a bounded snapshot including both head list and the working-set dictionary.
        """
        s = super().snapshot(head_n=head_n)
        # Working-set dict is bounded by keep_max by construction
        d: Dict[int, float] = {int(k): float(v) for k, v in getattr(self, "_val", {}).items()}
        return {
            "trail_head": s["head"],
            "trail_p95": s["p95"],
            "trail_p99": s["p99"],
            "trail_max": s["max"],
            "trail_count": s["count"],
            "trail_dict": d,
        }


__all__ = ["TrailMap"]