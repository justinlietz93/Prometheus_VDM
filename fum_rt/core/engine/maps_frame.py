"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Telemetry maps/frame builder (core-local, no IO).

- Builds Float32 LE arrays for heat/excitation/inhibition from bounded reducer working sets.
- Computes header with contract:
  {topic:'maps/frame', tick, n, shape, channels:['heat','exc','inh'], dtype:'f32', endianness:'LE', stats}
- Stages result onto nx._maps_frame_ready for runtime telemetry emitters to publish.
- Strictly avoids any W/CSR/adjacency scans; operates only on small reducer dictionaries.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as _np


def _max_from(d: Dict[int, float]) -> float:
    try:
        if not d:
            return 0.0
        # Mirror payload dtype (float32 LE): cast values to float32 before max to ensure
        # header['stats']['max'] ≥ observed max from the serialized payload.
        return float(max((_np.float32(v) for v in d.values())))
    except Exception:
        return 0.0


def _fill_array_from_map(arr: _np.ndarray, d: Dict[int, float]) -> None:
    try:
        n = int(arr.shape[0])
    except Exception:
        n = len(arr)
    try:
        for k, v in (d or {}).items():
            try:
                ik = int(k)
                if 0 <= ik < n:
                    arr[ik] = float(v)
            except Exception:
                continue
    except Exception:
        pass


def stage_maps_frame(
    nx: Any,
    heat_map: Optional[Any],
    exc_map: Optional[Any],
    inh_map: Optional[Any],
    fold_tick: int,
) -> None:
    """
    Construct and stage the maps/frame payload on nx._maps_frame_ready.

    Parameters:
      nx: nexus-like object, must provide integer attribute N (<= few 10^6) for shape.
      heat_map/exc_map/inh_map: reducers exposing a _val: Dict[int,float] working set (bounded).
      fold_tick: integer tick associated to this fold (monotonic).
    """
    try:
        N = int(getattr(nx, "N", 0))
    except Exception:
        N = 0
    if N <= 0:
        return

    # Allocate arrays (Float32 LE by frombuffer/tobytes contract downstream)
    heat_arr = _np.zeros(N, dtype=_np.float32)
    exc_arr = _np.zeros(N, dtype=_np.float32)
    inh_arr = _np.zeros(N, dtype=_np.float32)

    # Fill from bounded dictionaries (no global scans)
    try:
        _fill_array_from_map(heat_arr, getattr(heat_map, "_val", {}))
    except Exception:
        pass
    try:
        _fill_array_from_map(exc_arr, getattr(exc_map, "_val", {}))
    except Exception:
        pass
    try:
        _fill_array_from_map(inh_arr, getattr(inh_map, "_val", {}))
    except Exception:
        pass

    # Sanitize non-finite
    for arr in (heat_arr, exc_arr, inh_arr):
        try:
            _np.nan_to_num(arr, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
        except Exception:
            pass

    # Square-ish shape heuristic
    try:
        side = int(max(1, int(_np.ceil(_np.sqrt(N)))))
    except Exception:
        side = int(max(1, int((N or 1) ** 0.5)))
    shape = [side, side]

    # Stats from bounded dictionaries (min fixed to 0.0 by construction)
    stats = {
        "heat": {"min": 0.0, "max": _max_from(getattr(heat_map, "_val", {}))},
        "exc": {"min": 0.0, "max": _max_from(getattr(exc_map, "_val", {}))},
        "inh": {"min": 0.0, "max": _max_from(getattr(inh_map, "_val", {}))},
    }

    header = {
        "topic": "maps/frame",
        "tick": int(fold_tick),
        "n": int(N),
        "shape": shape,
        "channels": ["heat", "exc", "inh"],
        "dtype": "f32",
        "endianness": "LE",
        "stats": stats,
    }

    payload = heat_arr.tobytes() + exc_arr.tobytes() + inh_arr.tobytes()

    try:
        setattr(nx, "_maps_frame_ready", (header, payload))
    except Exception:
        pass