from __future__ import annotations

"""
Optional in-process HTTP status endpoint (void-faithful; no schedulers).

- Purpose: serve the latest status payload to UI without any file reads.
- Behavior: starts a tiny HTTP server in a background thread (event-driven, no timers).
- Endpoint:
    GET /status  -> 200 JSON of nx._emit_last_metrics (latest per-tick status) or 204 if not yet available
    GET /health  -> 200 {"ok": true}
- Enable via:
    ENABLE_STATUS_HTTP=1
    STATUS_HTTP_HOST=127.0.0.1
    STATUS_HTTP_PORT=8787
- Safety:
    - If any error occurs (port busy, etc.), remain a no-op.
    - Never mutates core dynamics; purely IO.
"""

import os
import json
import threading
from typing import Any, Optional


def _truthy(x: Any) -> bool:
    try:
        if isinstance(x, (int, float, bool)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False


def maybe_start_status_http(nx: Any) -> None:
    """
    Idempotently start the status HTTP server if ENABLE_STATUS_HTTP is truthy.
    Stores references on nx as:
      nx._status_http_server (HTTPServer)
      nx._status_http_thread (threading.Thread)
    """
    try:
        if not _truthy(os.getenv("ENABLE_STATUS_HTTP", "0")):
            return
    except Exception:
        return

    # Already running
    try:
        if getattr(nx, "_status_http_server", None) is not None:
            return
    except Exception:
        pass

    # Lazy import from stdlib; avoid global import side effects
    try:
        from http.server import BaseHTTPRequestHandler, HTTPServer  # type: ignore
    except Exception:
        return

    # Configuration
    try:
        host = os.getenv("STATUS_HTTP_HOST", "127.0.0.1").strip() or "127.0.0.1"
    except Exception:
        host = "127.0.0.1"
    try:
        port = int(os.getenv("STATUS_HTTP_PORT", "8787"))
    except Exception:
        port = 8787

    # Bind Nexus reference in a closure for the handler
    nexus_ref = nx

    class _Handler(BaseHTTPRequestHandler):  # type: ignore
        # Silence default logging
        def log_message(self, format: str, *args) -> None:  # noqa: A003 (shadow builtins name)
            try:
                if getattr(nexus_ref, "logger", None) is not None:
                    # Keep this extremely low-cost; skip formatting expansions
                    pass
            except Exception:
                pass

        def _send_json(self, code: int, payload: Optional[dict]) -> None:
            try:
                body = b""
                if payload is not None:
                    try:
                        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                    except Exception:
                        body = b"{}"
                self.send_response(code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if body:
                    self.wfile.write(body)
            except Exception:
                # Best-effort: avoid crashing the server
                try:
                    self.send_response(500)
                    self.end_headers()
                except Exception:
                    pass

        def do_GET(self) -> None:  # type: ignore
            try:
                path = self.path or "/"
                if path == "/health":
                    return self._send_json(200, {"ok": True})
                if path == "/status":
                    # Serve latest status payload captured by the runtime loop
                    try:
                        m = getattr(nexus_ref, "_emit_last_metrics", None)
                    except Exception:
                        m = None
                    if isinstance(m, dict) and m:
                        # Minimal filtering: ensure JSON-serializable scalars
                        safe = {}
                        for k, v in m.items():
                            try:
                                if isinstance(v, (int, float, str, bool)) or v is None:
                                    safe[k] = v
                                else:
                                    # fallback to float or string
                                    try:
                                        safe[k] = float(v)  # type: ignore
                                    except Exception:
                                        safe[k] = str(v)
                            except Exception:
                                continue
                        return self._send_json(200, safe)
                    return self._send_json(204, None)
                # Not found
                self.send_response(404)
                self.end_headers()
            except Exception:
                try:
                    self.send_response(500)
                    self.end_headers()
                except Exception:
                    pass

    # Create and start the HTTP server
    try:
        server = HTTPServer((host, port), _Handler)  # type: ignore
    except Exception:
        return

    def _run() -> None:
        try:
            server.serve_forever(poll_interval=0.5)
        except Exception:
            pass
        finally:
            try:
                server.server_close()
            except Exception:
                pass

    try:
        th = threading.Thread(target=_run, name="status_http", daemon=True)
        th.start()
        setattr(nx, "_status_http_server", server)
        setattr(nx, "_status_http_thread", th)
    except Exception:
        try:
            server.server_close()
        except Exception:
            pass
        return


__all__ = ["maybe_start_status_http"]