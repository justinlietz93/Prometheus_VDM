import os
from typing import Dict, Any

import numpy as np

from fum_rt.core.engine.maps_frame import stage_maps_frame
from fum_rt.runtime.telemetry import tick_fold


class _DummyMap:
    def __init__(self, d: Dict[int, float]) -> None:
        self._val = dict(d)


class _StubNx:
    def __init__(self, N: int) -> None:
        self.N = int(N)
        self._emit_step = 0
        # no bus, ring will be lazy-initialized by tick_fold


def _set_env(k: str, v: str):
    prev = os.environ.get(k)
    os.environ[k] = v
    return prev


def _restore_env(k: str, prev):
    if prev is None:
        os.environ.pop(k, None)
    else:
        os.environ[k] = prev


def test_frame_v2_u8_tiles_and_ring_capacity():
    # Configure telemetry for u8 + tiles + bounded ring and disable FPS limiter
    prev_mode = _set_env("MAPS_MODE", "u8")
    prev_tile = _set_env("MAPS_TILE", "4x4")
    prev_ring = _set_env("MAPS_RING", "2")
    prev_fps = _set_env("MAPS_FPS", "0")

    try:
        n = 64  # 8x8 square
        nx = _StubNx(n)
        heat = _DummyMap({5: 1.0})
        exc = _DummyMap({7: 0.7})
        inh = _DummyMap({9: 0.9})

        # Stage float32 frame (v1)
        stage_maps_frame(nx, heat, exc, inh, fold_tick=1)

        # Telemetry fold quantizes to u8 (v2) and pushes to ring
        _m, _syms = tick_fold(nx, metrics={}, drive={}, td_signal=0.0, step=1)

        ring = getattr(nx, "_maps_ring", None)
        assert ring is not None, "MapsRing was not initialized"
        fr = ring.latest()
        assert fr is not None, "No frame pushed to MapsRing"
        hdr = fr.header

        # Header assertions
        assert hdr.get("dtype") == "u8"
        assert hdr.get("ver") == "v2"
        assert hdr.get("quant") == "u8"
        assert "tiles" in hdr, "Tile metadata missing from header"
        tiles = hdr["tiles"]
        # 8x8 frame tiled into 4x4 should yield 2x2 grid
        assert tiles.get("size") == [4, 4]
        assert tiles.get("grid") == [2, 2]
        assert tiles.get("shape") == [8, 8]
        # payload_len hint matches payload bytes
        assert hdr.get("payload_len") == 3 * n
        assert len(fr.payload) == 3 * n

        # Capacity behavior: push 2 more frames and ensure ring stays at capacity=2
        stage_maps_frame(nx, heat, exc, inh, fold_tick=2)
        tick_fold(nx, metrics={}, drive={}, td_signal=0.0, step=2)
        assert ring.size() == 2
        stage_maps_frame(nx, heat, exc, inh, fold_tick=3)
        tick_fold(nx, metrics={}, drive={}, td_signal=0.0, step=3)
        assert ring.size() == 2
        assert ring.dropped() >= 1
    finally:
        _restore_env("MAPS_MODE", prev_mode)
        _restore_env("MAPS_TILE", prev_tile)
        _restore_env("MAPS_RING", prev_ring)
        _restore_env("MAPS_FPS", prev_fps)