from __future__ import annotations

import os
from dash import Input, Output, State, no_update  # noqa: F401


def register_feed_callbacks(app, manager, repo_root: str):
    """
    Feed controls:
      - Start feeding a file into the managed process stdin at a given rate
      - Stop feeding
    Uses the same IDs as the inline version in fum_live to preserve behavior.
    """

    @app.callback(
        Output("send-status", "children", allow_duplicate=True),
        Input("feed-start", "n_clicks"),
        State("feed-path", "value"),
        State("feed-rate", "value"),
        prevent_initial_call=True,
    )
    def on_feed_start(_n, path, rate):
        p = (path or "").strip()
        if not p:
            return "Provide a feed path (relative to fum_rt/data or absolute)."
        chosen = p
        try:
            if (not os.path.isabs(chosen)) or (not os.path.exists(chosen)):
                data_dir = os.path.join(repo_root, "fum_rt", "data")
                cand = os.path.join(data_dir, p)
                if os.path.exists(cand):
                    chosen = cand
        except Exception:
            pass
        ok = manager.feed_file(chosen, float(rate or 20.0))
        return f"Feeding from {chosen}." if ok else "Feed failed (check process running and path)."

    @app.callback(
        Output("send-status", "children", allow_duplicate=True),
        Input("feed-stop", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_feed_stop(_n):
        manager.stop_feed()
        return "Feed stopped."