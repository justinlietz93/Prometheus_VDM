from __future__ import annotations

import os
from dash import Input, Output  # noqa: F401


def register_logs_callbacks(app, manager):
    """
    Launcher log viewer:
      - Streams the tail of the last launcher log written by ProcessManager.
    IDs preserved to match existing layout.
    """

    @app.callback(
        Output("launch-log", "children"),
        Input("poll", "n_intervals"),
        Input("show-log", "n_clicks"),
        Input("ui-state", "data"),
        prevent_initial_call=False,
    )
    def update_launch_log(_n, _clicks, ui_state):
        """
        Tail the launcher log efficiently without rereading entire file each tick.
        - UI-governed: only tails when ui_state['tail_launch_log'] is True (default OFF).
        - Bounds bytes via DASH_LOG_TAIL_BYTES (env) while staying purely UI-controlled for enable/disable.
        """
        # UI gating (default OFF). Also allow explicit one-shot via "Show Launcher Log" button.
        ui = ui_state or {}
        clicks = int(_clicks or 0)
        try:
            tail_enabled = bool(ui.get("tail_launch_log", False))
        except Exception:
            tail_enabled = False
        # If the user clicked "Show Launcher Log" at least once, show the log regardless of UI toggle.
        if clicks > 0:
            tail_enabled = True
        if not tail_enabled:
            return "Launcher log tail disabled (toggle in UI Performance or click Show Launcher Log)."

        try:
            path = getattr(manager, "launch_log", None)
            if not path or not os.path.exists(path):
                return "No launcher log yet."

            try:
                tail_bytes = int(os.getenv("DASH_LOG_TAIL_BYTES", "16384"))
            except Exception:
                tail_bytes = 16384

            st = os.stat(path)
            size = int(getattr(st, "st_size", 0))
            start = max(0, size - max(1024, tail_bytes))  # at least 1 KiB

            with open(path, "rb") as fh:
                fh.seek(start, os.SEEK_SET)
                data = fh.read()

            text = data.decode("utf-8", errors="ignore")
            # Keep a compact tail to avoid heavy DOM nodes
            return text[-4000:] if len(text) > 4000 else text
        except Exception as e:
            return f"Error reading launcher log: {e}"