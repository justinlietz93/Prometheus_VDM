"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from typing import Any
from dash import Input, Output  # noqa: F401


def _int_or(v: Any, dv: int) -> int:
    try:
        return int(v)
    except Exception:
        return dv


def register_interval_callbacks(app):
    """
    Bind dcc.Interval(id="poll") cadence to UI Performance settings (ui-state).
    - update_ms <= 0 disables polling
    - update_ms > 0 sets the interval in milliseconds (min clamp = 100 ms)
    This replaces the env-only cadence for responsiveness control without restart.
    """
    @app.callback(
        Output("poll", "interval"),
        Output("poll", "disabled"),
        Input("ui-state", "data"),
        prevent_initial_call=False,
    )
    def on_ui_interval(ui_state: dict | None):
        ui = ui_state or {}
        update_ms = _int_or(ui.get("update_ms", 800), 800)
        if update_ms <= 0:
            # Disable polling entirely
            return 100, True  # Dash requires a valid interval even if disabled
        # Enforce a sane lower bound
        return int(max(100, update_ms)), False


__all__ = ["register_interval_callbacks"]