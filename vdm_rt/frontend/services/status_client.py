"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
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


def get_status_snapshot(url: Optional[str] = None, timeout_s: Optional[float] = None) -> Optional[dict[str, Any]]:
    """
    Fetch the latest status snapshot.

    Args:
        url: Optional override for status URL (e.g., "http://127.0.0.1:8787/status/snapshot").
             If None, use env STATUS_HTTP_URL or default "http://127.0.0.1:8787/status".
        timeout_s: Optional override for request timeout in seconds. If None, use env
                   STATUS_HTTP_TIMEOUT_MS (default 0.2s).

    Returns:
        dict[str, Any] on success (HTTP 200 JSON)
        None on 204 or any error/parse failure
    """
    # URL
    if url is None:
        try:
            url = os.getenv("STATUS_HTTP_URL", "http://127.0.0.1:8787/status").strip() or "http://127.0.0.1:8787/status"
        except Exception:
            url = "http://127.0.0.1:8787/status"
    # Prefer /status/snapshot if caller passed base /status
    try:
        if url.endswith("/status"):
            url = url + "/snapshot"
    except Exception:
        pass

    # Timeout
    if timeout_s is None:
        try:
            tms = int(os.getenv("STATUS_HTTP_TIMEOUT_MS", "200"))
        except Exception:
            tms = 200
        timeout_s = max(0.05, float(tms) / 1000.0)
    else:
        try:
            timeout_s = max(0.05, float(timeout_s))
        except Exception:
            timeout_s = 0.2

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # nosec B310 (local loopback by default)
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