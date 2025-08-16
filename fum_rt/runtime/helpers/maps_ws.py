"""
Runtime helper: maps/frame WebSocket bootstrap (bounded, drop-oldest).

- Safe no-op when ENABLE_MAPS_WS is not truthy or when 'websockets' package is missing.
- Ensures a bounded MapsRing exists on nx._maps_ring (capacity=MAPS_RING, default 3).
- Starts MapsWebSocketServer once and stores it on nx._maps_ws_server.

This file is part of the runtime helpers modularization under fum_rt.runtime.helpers.
"""

from __future__ import annotations

import os
from typing import Any


def _truthy(x) -> bool:
    try:
        if isinstance(x, (int, float)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False


def maybe_start_maps_ws(nx: Any) -> None:
    """
    Lazily start the maps/frame WebSocket forwarder if ENABLE_MAPS_WS is truthy.
    - Ensures a bounded MapsRing exists on nx._maps_ring (capacity=MAPS_RING, default 3)
    - Starts a background MapsWebSocketServer (host=MAPS_WS_HOST, port=MAPS_WS_PORT)
    - Safe no-op if websockets is not installed or any error occurs
    """
    try:
        if not _truthy(os.getenv("ENABLE_MAPS_WS", "0")):
            return

        # Ensure a ring exists (reuses ring created by telemetry tick_fold if present)
        ring = getattr(nx, "_maps_ring", None)
        if ring is None:
            try:
                from fum_rt.io.visualization.maps_ring import MapsRing  # allowed in runtime layer
                cap = 3
                try:
                    cap = int(os.getenv("MAPS_RING", "3"))
                except Exception:
                    cap = 3
                nx._maps_ring = MapsRing(capacity=max(1, cap))
                ring = nx._maps_ring
            except Exception:
                ring = None

        if ring is None:
            return

        # Start server once
        if getattr(nx, "_maps_ws_server", None) is None:
            try:
                from fum_rt.io.visualization.websocket_server import MapsWebSocketServer  # runtime-layer IO allowed
                host = os.getenv("MAPS_WS_HOST", "127.0.0.1")
                try:
                    port = int(os.getenv("MAPS_WS_PORT", "8765"))
                except Exception:
                    port = 8765

                def _err(msg: str) -> None:
                    try:
                        nx.logger.info("maps_ws_error", extra={"extra": {"err": str(msg)}})
                    except Exception:
                        try:
                            print("[maps_ws] " + str(msg), flush=True)
                        except Exception:
                            pass

                srv = MapsWebSocketServer(ring, host=host, port=port, on_error=_err)
                srv.start()
                nx._maps_ws_server = srv
            except Exception:
                # Missing websockets or other failure — safe no-op
                return
    except Exception:
        # Never disrupt runtime parity
        pass


__all__ = ["maybe_start_maps_ws"]