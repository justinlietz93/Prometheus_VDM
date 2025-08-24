from __future__ import annotations

from typing import Any, Dict, List
from dash import Input, Output  # noqa: F401


def _is_on(v: Any) -> bool:
    try:
        return isinstance(v, list) and ("on" in v)
    except Exception:
        return False


def _int_or(v: Any, dv: int) -> int:
    try:
        i = int(v)
        return i
    except Exception:
        return dv


def _float_or(v: Any, dv: float) -> float:
    try:
        f = float(v)
        return f
    except Exception:
        return dv


def _str_or(v: Any, dv: str) -> str:
    try:
        s = str(v).strip()
        return s if s else dv
    except Exception:
        return dv


def register_perf_callbacks(app):
    """
    Mirror UI Performance controls into dcc.Store(id="ui-state").
    No environment variables are required; settings apply immediately.
    """
    @app.callback(
        Output("ui-state", "data"),
        Input("ui-charts-http", "value"),
        Input("ui-update-ms", "value"),
        Input("ui-points-cap", "value"),
        Input("ui-series-cap", "value"),
        Input("ui-status-url", "value"),
        Input("ui-status-timeout", "value"),
        Input("ui-tail-chat", "value"),
        Input("ui-tail-launch", "value"),
        prevent_initial_call=False,
    )
    def on_perf_update(
        charts_http_v: List[str],
        update_ms_v: Any,
        points_cap_v: Any,
        series_cap_v: Any,
        status_url_v: Any,
        status_timeout_v: Any,
        tail_chat_v: List[str],
        tail_launch_v: List[str],
    ):
        charts_http = _is_on(charts_http_v)
        tail_chat = _is_on(tail_chat_v)
        tail_launch_log = _is_on(tail_launch_v)
        update_ms = _int_or(update_ms_v, 800)
        points_cap = _int_or(points_cap_v, 1200)
        series_cap = _int_or(series_cap_v, 6)
        status_url = _str_or(status_url_v, "http://127.0.0.1:8787/status/snapshot")
        status_timeout = _float_or(status_timeout_v, 0.2)

        # Provide keys consumed by charts controller (maxp/decimate)
        ui: Dict[str, Any] = {
            "charts_http_only": bool(charts_http),
            "update_ms": int(max(100, update_ms)),
            "points_cap": int(max(50, points_cap)),
            "series_cap": int(max(1, series_cap)),
            "tail_chat": bool(tail_chat),
            "tail_launch_log": bool(tail_launch_log),
            "status_url": status_url,
            "status_timeout": float(max(0.05, status_timeout)),
            # Charts controller knobs (no env):
            "maxp": int(max(50, points_cap)),
            "decimate": int(max(0, points_cap)),  # treat as target plotted points (0=off if caller wants)
        }
        return ui


__all__ = ["register_perf_callbacks"]