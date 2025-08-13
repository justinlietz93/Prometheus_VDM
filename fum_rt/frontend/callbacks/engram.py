from __future__ import annotations

import os
from dash import Input, Output  # noqa: F401
from fum_rt.frontend.utilities.fs_utils import _list_files


def register_engram_callbacks(app):
    """
    Engram path helpers:
      - Populate dropdown options by scanning runs-root for .h5/.npz
      - Keep the free-text input in sync with dropdown selection
    """

    @app.callback(
        Output("rc-load-engram-path", "options"),
        Input("runs-root", "value"),
        prevent_initial_call=False,
    )
    def on_runs_root_change(runs_root_dir):
        if not runs_root_dir or not os.path.isdir(runs_root_dir):
            return []
        engram_files = _list_files(runs_root_dir, exts=[".h5", ".npz"], recursive=True)
        options = []
        for rel_path in engram_files:
            full_path = os.path.join(runs_root_dir, rel_path)
            options.append({"label": rel_path.replace(os.path.sep, "/"), "value": full_path})
        return options

    @app.callback(
        Output("rc-load-engram-input", "value", allow_duplicate=True),
        Input("rc-load-engram-path", "value"),
        prevent_initial_call=True,
    )
    def sync_engram_input_from_dropdown(val):
        return val