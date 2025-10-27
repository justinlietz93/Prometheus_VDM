"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import numpy as np

from fum_rt.core.engine import CoreEngine
from fum_rt.core.proprioception.events import VTTouchEvent, SpikeEvent, DeltaWEvent


class _StubNx:
    """
    Minimal nexus-like stub for CoreEngine:
    - Provides only the attributes CoreEngine.step() actually touches in this test
    """
    def __init__(self, N: int = 64, seed: int = 0) -> None:
        self.N = int(N)
        self.seed = int(seed)
        self._emit_step = 0  # for fold tick hint
        # optional params used by _ensure_evt_init() with safe fallbacks:
        self.b1_half_life_ticks = 50
        self.cold_head_k = 256
        self.cold_half_life_ticks = 200
        # No bus needed here (we assert _maps_frame_ready before telemetry publishes)


def test_maps_frame_smoke_builds_arrays_without_scans():
    nx = _StubNx(N=64, seed=0)
    eng = CoreEngine(nx)

    # Simulate a small batch of events hitting distinct nodes
    events = [
        VTTouchEvent(kind="vt_touch", t=1, token=42, w=1.0),            # -> HeatMap
        SpikeEvent(kind="spike", t=1, node=7, amp=0.8, sign=+1),        # -> ExcitationMap
        SpikeEvent(kind="spike", t=1, node=9, amp=0.5, sign=-1),        # -> InhibitionMap
        DeltaWEvent(kind="delta_w", t=1, node=9, dw=-0.2),              # -> InhibitionMap (abs)
    ]

    # Fold events and build maps/frame
    eng.step(10, events)

    # Engine should stage a maps frame for telemetry to publish later
    assert hasattr(nx, "_maps_frame_ready"), "maps/frame not staged by CoreEngine"
    header, payload = getattr(nx, "_maps_frame_ready")

    # Validate header contract
    assert isinstance(header, dict)
    assert header.get("channels") == ["heat", "exc", "inh"]
    n = header.get("n")
    assert isinstance(n, int) and n == nx.N
    shape = header.get("shape")
    assert isinstance(shape, list) and len(shape) == 2
    stats = header.get("stats")
    assert isinstance(stats, dict) and set(stats.keys()) == {"heat", "exc", "inh"}
    for ch in ("heat", "exc", "inh"):
        assert "min" in stats[ch] and "max" in stats[ch]
        # min is fixed to 0.0 by construction
        assert stats[ch]["min"] == 0.0

    # Validate payload: 3 * n float32 (little-endian) blocks
    assert isinstance(payload, (bytes, bytearray))
    assert len(payload) == 3 * n * 4  # float32 bytes

    f32 = np.frombuffer(payload, dtype="<f4", count=3 * n)
    heat = f32[:n]
    exc = f32[n : 2 * n]
    inh = f32[2 * n : 3 * n]

    # Only working-set indices should be nonzero (42 for heat, 7 for exc, 9 for inh)
    nonzero_idx = set(np.nonzero(heat)[0]) | set(np.nonzero(exc)[0]) | set(np.nonzero(inh)[0])
    assert nonzero_idx.issubset({42, 7, 9}), f"Unexpected nonzero indices: {sorted(nonzero_idx)}"

    # Ensure we didn't accidentally scan/normalize across full arrays (max from working-set is fine)
    # i.e., stats max should be >= the observed nonzero values and min stays 0.0
    for arr_name, arr in (("heat", heat), ("exc", exc), ("inh", inh)):
        observed_max = float(arr.max(initial=0.0))
        assert stats[arr_name]["max"] >= observed_max