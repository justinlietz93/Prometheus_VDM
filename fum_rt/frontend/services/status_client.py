from __future__ import annotations

"""
Lightweight HTTP status client (frontend-only; zero file IO).

- Purpose: fetch the latest runtime status snapshot from the in-process HTTP endpoint
  to drive live dashboard charts without scanning or tailing JSONL files.
- Endpoint (served by runtime.helpers.status_http.maybe_start_status_http):
  GET /status  -> 200 JSON (latest nx._emit_last_metrics) or 204 when not ready
  GET /health  -> 200 {"ok": true}

Environment
- STATUS_HTTP_URL (default "http://127.0.0.1:8787/status")
- STATUS_HTTP_TIMEOUT_MS (default 200)

Contracts
- Returns a Python dict on HTTP 200 with valid JSON; None on 204 or any error.
- No retries, no background threads; caller controls cadence (e.g., via dcc.Interval).
"""

import os
import json
from typing import Any, Optional
import urllib.request
import urllib.error


def get_status_snapshot() -> Optional[dict[str, Any]]:
    """
    Fetch the latest status snapshot from STATUS_HTTP_URL.

    Returns:
        dict[str, Any] on success (HTTP 200 JSON)
        None on 204 or any error/parse failure
    """
    try:
        url = os.getenv("STATUS_HTTP_URL", "http://127.0.0.1:8787/status").strip() or "http://127.0.0.1:8787/status"
    except Exception:
        url = "http://127.0.0.1:8787/status"

    try:
        tms = int(os.getenv("STATUS_HTTP_TIMEOUT_MS", "200"))
    except Exception:
        tms = 200
    timeout = max(0.05, float(tms) / 1000.0)

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310 (local loopback by default)
            code = getattr(resp, "status", 200)
            if code == 204:
                return None
            data = resp.read()
            if not data:
                return None
            try:
                return json.loads(data.decode("utf-8", "ignore"))
            except Exception:
                return None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    except Exception:
        return None


__all__ = ["get_status_snapshot"]