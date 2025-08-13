from __future__ import annotations

from typing import List
from dash import Input, Output, State, no_update  # noqa: F401 (bound by Dash at runtime)
from fum_rt.frontend.utilities.fs_utils import list_runs


def register_workspace_callbacks(app, runs_root: str, manager):
    """
    Workspace-level callbacks:
      - Refresh run list (options + default selection)
      - Use current managed run
      - Use latest run under a root
    """

    @app.callback(
        Output("run-dir", "options"),
        Output("run-dir", "value", allow_duplicate=True),
        Input("refresh-runs", "n_clicks"),
        State("runs-root", "value"),
        prevent_initial_call=True,
    )
    def on_refresh_runs(_n, root):
        root = root or runs_root
        opts = [{"label": p, "value": p} for p in list_runs(root)]
        val = opts[0]["value"] if opts else ""
        return opts, val

    @app.callback(
        Output("run-dir", "value", allow_duplicate=True),
        Input("use-current-run", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_use_current(_n):
        return manager.current_run_dir or no_update

    @app.callback(
        Output("run-dir", "value", allow_duplicate=True),
        Input("use-latest-run", "n_clicks"),
        State("runs-root", "value"),
        prevent_initial_call=True,
    )
    def on_use_latest(_n, root):
        r = root or runs_root
        rs = list_runs(r)
        return rs[0] if rs else no_update