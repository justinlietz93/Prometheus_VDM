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
        Input("poll", "n_intervals"),
        Input("proc-status", "children"),
        State("run-dir", "value"),
        prevent_initial_call=False,
    )
    def on_runs_root_change(runs_root_dir, _n, _proc_status, run_dir):
        """
        Keep engram dropdown options fresh:
        - Rescan on runs-root changes
        - Rescan periodically (poll)
        - Rescan on process status transitions (Start/Resume)
        Also include current run_dir tree when it falls outside runs_root.
        """
        options = []
        seen = set()

        # 1) Scan runs_root recursively
        if runs_root_dir and os.path.isdir(runs_root_dir):
            try:
                engram_files = _list_files(runs_root_dir, exts=[".h5", ".npz"], recursive=True)
            except Exception:
                engram_files = []
            for rel_path in engram_files:
                full_path = os.path.join(runs_root_dir, rel_path)
                if full_path in seen:
                    continue
                seen.add(full_path)
                options.append({"label": rel_path.replace(os.path.sep, "/"), "value": full_path})

        # 2) Also scan active run_dir if provided and not already covered
        rd = (run_dir or "").strip()
        if rd and os.path.isdir(rd):
            try:
                rd_files = _list_files(rd, exts=[".h5", ".npz"], recursive=True)
            except Exception:
                rd_files = []
            # If rd lies under runs_root_dir, the above scan likely covered it; de-dup via 'seen'
            base = os.path.basename(rd.rstrip(os.path.sep))
            for rel_path in rd_files:
                full_path = os.path.join(rd, rel_path)
                if full_path in seen:
                    continue
                seen.add(full_path)
                label = f"{base}/{rel_path.replace(os.path.sep, '/')}"
                options.append({"label": label, "value": full_path})

        return options

    @app.callback(
        Output("rc-load-engram-input", "value", allow_duplicate=True),
        Input("rc-load-engram-path", "value"),
        prevent_initial_call=True,
    )
    def sync_engram_input_from_dropdown(val):
        return val