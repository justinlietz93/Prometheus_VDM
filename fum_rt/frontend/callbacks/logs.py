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
        """
        Tail the launcher log efficiently without rereading entire file each tick.
        Reads only the last DASH_LOG_TAIL_BYTES (default 16 KiB) and returns the last 4000 chars.
        """
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