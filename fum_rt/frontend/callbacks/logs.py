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
        prevent_initial_call=False,
    )
    def update_launch_log(_n, _clicks):
        try:
            path = getattr(manager, "launch_log", None)
            if not path or not os.path.exists(path):
                return "No launcher log yet."
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                data = fh.read()
            return data[-4000:]
        except Exception as e:
            return f"Error reading launcher log: {e}"