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

Module: fum_rt.core.cortex.maps.excitationmap
Purpose: Excitatory-only activity map (short half-life), event-driven only (no scans).
"""

from typing import Iterable
from .base_decay_map import BaseDecayMap
from fum_rt.core.proprioception.events import SpikeEvent, DeltaWEvent


class ExcitationMap(BaseDecayMap):
    """
    Excitatory-only activity map.
    Filters by sign>0 (spikes) and dw>0 (ΔW).

    Parameters:
      - half_life_ticks: decay half-life in ticks (e.g., 200)
      - spike_gain: multiplier * amp for SpikeEvent (e.g., 1.0)
      - dW_gain: multiplier * dw for DeltaWEvent (dw > 0 only)
    """
    __slots__ = ("spike_gain", "dW_gain")

    def __init__(
        self,
        head_k: int = 256,
        half_life_ticks: int = 200,
        keep_max: int | None = None,
        seed: int = 0,
        spike_gain: float = 1.0,
        dW_gain: float = 0.5,
    ):
        super().__init__(head_k, half_life_ticks, keep_max, seed)
        self.spike_gain = float(spike_gain)
        self.dW_gain = float(dW_gain)

    def fold(self, events: Iterable[object], tick: int) -> None:
        for e in events:
            k = getattr(e, "kind", None)
            if k == "spike" and isinstance(e, SpikeEvent) and int(getattr(e, "sign", 0)) > 0:
                self.add(int(e.node), int(tick), self.spike_gain * float(getattr(e, "amp", 1.0)))
            elif k == "delta_w" and isinstance(e, DeltaWEvent):
                dw = float(getattr(e, "dw", 0.0))
                if dw > 0.0:
                    self.add(int(e.node), int(tick), self.dW_gain * dw)

    def snapshot(self) -> dict:
        s = super().snapshot()
        return {
            "exc_head": s["head"],
            "exc_p95": s["p95"],
            "exc_p99": s["p99"],
            "exc_max": s["max"],
            "exc_count": s["count"],
        }


__all__ = ["ExcitationMap"]
