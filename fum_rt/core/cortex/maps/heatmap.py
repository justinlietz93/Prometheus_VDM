from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.cortex.maps.heatmap
Purpose: Recency-weighted activity map (short half-life), event-driven only (no scans).
"""

from typing import Iterable
from .base_decay_map import BaseDecayMap
from fum_rt.core.proprioception.events import VTTouchEvent, SpikeEvent, DeltaWEvent


class HeatMap(BaseDecayMap):
    """
    Recency-weighted activity map (short half-life).
    Increments on vt_touch (small) and any spike/ΔW (scaled).

    Parameters:
      - half_life_ticks: decay half-life in ticks (e.g., 200)
      - vt_touch_gain: increment per vt_touch (e.g., 0.25)
      - spike_gain: multiplier * amp for SpikeEvent (e.g., 1.0)
      - dW_gain: multiplier * |dw| for DeltaWEvent (e.g., 0.5)

    Void-faithful: folds events only; never scans global structures.
    """
    __slots__ = ("vt_touch_gain", "spike_gain", "dW_gain")

    def __init__(
        self,
        head_k: int = 256,
        half_life_ticks: int = 200,
        keep_max: int | None = None,
        seed: int = 0,
        vt_touch_gain: float = 0.25,
        spike_gain: float = 1.0,
        dW_gain: float = 0.5,
    ):
        super().__init__(head_k, half_life_ticks, keep_max, seed)
        self.vt_touch_gain = float(vt_touch_gain)
        self.spike_gain = float(spike_gain)
        self.dW_gain = float(dW_gain)

    def fold(self, events: Iterable[object], tick: int) -> None:
        for e in events:
            k = getattr(e, "kind", None)
            if k == "vt_touch" and isinstance(e, VTTouchEvent):
                self.add(int(e.token), int(tick), self.vt_touch_gain * float(getattr(e, "w", 1.0)))
            elif k == "spike" and isinstance(e, SpikeEvent):
                self.add(int(e.node), int(tick), self.spike_gain * float(getattr(e, "amp", 1.0)))
            elif k == "delta_w" and isinstance(e, DeltaWEvent):
                self.add(int(e.node), int(tick), self.dW_gain * abs(float(e.dw)))

    def snapshot(self) -> dict:
        s = super().snapshot()
        return {
            "heat_head": s["head"],
            "heat_p95": s["p95"],
            "heat_p99": s["p99"],
            "heat_max": s["max"],
            "heat_count": s["count"],
        }


__all__ = ["HeatMap"]
