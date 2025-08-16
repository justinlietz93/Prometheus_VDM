"""
Maps frames WebSocket forwarder (bounded, drop-oldest, void-faithful).

Canonical location: fum_rt.io.visualization.websocket_server

Purpose
- Serve UI consumers with the latest maps/frame payload from a bounded ring.
- Backpressure-safe: each client receives only the newest frame; old frames are dropped.
- Local-first: defaults to 127.0.0.1 binding; configurable via args/env.

Dependencies
- Optional: 'websockets' Python package (asyncio-based). If unavailable, this module is inert.

Env (defaults shown)
- MAPS_FPS=10                # broadcaster tick; sends at most this many frames per second
- WS_MAX_CONN=2              # maximum concurrent WebSocket clients
- WS_ALLOW_ORIGIN=           # comma-separated origins; if empty, all origins allowed

Transport format
- Two-message sequence per frame:
  1) Text frame: JSON dump of header dict (augmented with dtype/ver/quant/etc. by producer)
  2) Binary frame: raw payload bytes (u8 or f32 LE as dictated by header['dtype'])

Notes
- This module does not mutate frames; it forwards exactly what producers pushed to the ring.
- For RGB visualization, typical mapping is RGB = [exc, heat, inh] client-side.
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
from typing import Any, Dict, Optional, Set, Callable

try:
    import websockets  # type: ignore
    from websockets.server import WebSocketServerProtocol  # type: ignore
except Exception:  # pragma: no cover
    websockets = None
    WebSocketServerProtocol = object  # type: ignore

from fum_rt.io.visualization.maps_ring import MapsRing, MapsFrame


class MapsWebSocketServer:
    """
    Bounded WebSocket forwarder for maps frames.

    Usage:
      ring = MapsRing(capacity=3)
      ws = MapsWebSocketServer(ring, host="127.0.0.1", port=8888)
      ws.start()
      ...
      ws.stop()
    """

    __slots__ = (
        "ring",
        "host",
        "port",
        "max_conn",
        "allow_origins",
        "fps",
        "_running",
        "_thread",
        "_clients",
        "_loop",
        "_server",
        "_last_seq_sent",
        "_on_error",
    )

    def __init__(
        self,
        ring: MapsRing,
        host: str = "127.0.0.1",
        port: int = 8765,
        *,
        max_conn: Optional[int] = None,
        allow_origins: Optional[str] = None,
        fps: Optional[float] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.ring = ring
        self.host = str(host)
        self.port = int(port)
        try:
            self.max_conn = int(max_conn if max_conn is not None else os.getenv("WS_MAX_CONN", "2"))
        except Exception:
            self.max_conn = 2
        # Comma-separated origins string or None for any
        self.allow_origins = str(allow_origins) if allow_origins is not None else os.getenv("WS_ALLOW_ORIGIN", "")
        try:
            self.fps = float(fps if fps is not None else os.getenv("MAPS_FPS", "10"))
        except Exception:
            self.fps = 10.0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._clients: Set[WebSocketServerProtocol] = set()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._server = None
        self._last_seq_sent: int = 0
        self._on_error = on_error

    # ---- Public API ----

    def start(self) -> None:
        """
        Start the WebSocket server in a background thread. No-op if 'websockets' is missing.
        """
        if websockets is None:
            self._report_error("websocket_server_start_failed: websockets package not installed")
            return
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, name="maps_ws_server", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the server and wait for the background thread to exit.
        """
        if not self._running:
            return
        self._running = False
        try:
            if self._loop is not None:
                asyncio.run_coroutine_threadsafe(self._shutdown_async(), self._loop).result(timeout=2.0)
        except Exception:
            pass
        try:
            if self._thread is not None:
                self._thread.join(timeout=2.0)
        except Exception:
            pass
        self._thread = None

    # ---- Internal ----

    def _report_error(self, msg: str) -> None:
        try:
            if self._on_error:
                self._on_error(msg)
            else:
                print("[maps_ws] " + msg, flush=True)
        except Exception:
            pass

    def _run_loop(self) -> None:
        try:
            loop = asyncio.new_event_loop()
            self._loop = loop
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._start_async())
            loop.run_forever()
        except Exception as e:
            self._report_error(f"websocket_server_loop_error: {e}")
        finally:
            try:
                if self._server is not None:
                    loop = self._loop or asyncio.get_event_loop()
                    loop.run_until_complete(self._shutdown_async())
            except Exception:
                pass

    async def _start_async(self) -> None:
        assert websockets is not None
        origins = None
        if self.allow_origins:
            try:
                origins = [o.strip() for o in self.allow_origins.split(",") if o.strip()]
                if not origins:
                    origins = None
            except Exception:
                origins = None

        self._server = await websockets.serve(  # type: ignore
            self._ws_handler,
            self.host,
            self.port,
            max_size=2**20,  # 1 MiB per message should suffice for control
            max_queue=1,     # backpressure: queue at most one message per client
            ping_interval=20,
            ping_timeout=20,
            origins=origins,
        )

        # Broadcaster loop
        asyncio.create_task(self._broadcast_loop())

    async def _shutdown_async(self) -> None:
        try:
            # Close all clients
            for ws in list(self._clients):
                try:
                    await ws.close()
                except Exception:
                    pass
            self._clients.clear()
        except Exception:
            pass
        try:
            if self._server is not None:
                self._server.close()
                await self._server.wait_closed()
        except Exception:
            pass
        try:
            loop = asyncio.get_event_loop()
            loop.stop()
        except Exception:
            pass

    async def _ws_handler(self, websocket: WebSocketServerProtocol, path: str) -> None:  # type: ignore[override]
        # Enforce max connections
        try:
            if len(self._clients) >= max(1, self.max_conn):
                await websocket.close(code=1013, reason="server_overload")  # Try again later
                return
        except Exception:
            pass

        self._clients.add(websocket)
        try:
            # Initial latest send to prime client
            await self._send_latest(websocket)
            # Then just keep the connection alive until client disconnects; no per-client loop needed
            # since broadcast loop handles sending updates to all clients.
            await websocket.wait_closed()
        except Exception:
            pass
        finally:
            try:
                self._clients.remove(websocket)
            except Exception:
                pass

    async def _broadcast_loop(self) -> None:
        # Send at most one frame per fps interval; drop-oldest by only ever sending the latest frame
        interval = (1.0 / max(0.001, float(self.fps))) if self.fps > 0 else 0.0
        while self._running:
            try:
                if not self._clients:
                    # Avoid unnecessary ring access when there are no clients
                    await asyncio.sleep(interval if interval > 0 else 0.1)
                    continue
                fr = self.ring.latest()
                if fr is not None and fr.seq != self._last_seq_sent:
                    # Broadcast header (text) then payload (binary)
                    await self._broadcast_frame(fr)
                    self._last_seq_sent = fr.seq
                await asyncio.sleep(interval if interval > 0 else 0.0)
            except Exception:
                # Keep server resilient
                await asyncio.sleep(0.05)

    async def _broadcast_frame(self, fr: MapsFrame) -> None:
        dead: Set[WebSocketServerProtocol] = set()
        # Serialize header once
        try:
            hdr_text = json.dumps(fr.header, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            # Fallback minimal header
            hdr_text = json.dumps({"topic": "maps/frame", "tick": int(fr.tick)}, separators=(",", ":"))
        for ws in list(self._clients):
            try:
                await ws.send(hdr_text)     # text frame
                await ws.send(fr.payload)   # binary frame
            except Exception:
                dead.add(ws)
        # Purge disconnected clients
        for ws in dead:
            try:
                self._clients.remove(ws)
            except Exception:
                pass

    async def _send_latest(self, ws: WebSocketServerProtocol) -> None:
        fr = self.ring.latest()
        if fr is None:
            return
        try:
            hdr_text = json.dumps(fr.header, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            hdr_text = json.dumps({"topic": "maps/frame", "tick": int(fr.tick)}, separators=(",", ":"))
        try:
            await ws.send(hdr_text)
            await ws.send(fr.payload)
        except Exception:
            pass


__all__ = ["MapsWebSocketServer"]