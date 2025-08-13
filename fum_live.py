#!/usr/bin/env python3
"""
FUM Live Dashboard — Soft‑Dark UI
- Same imports and behavior as the original.
- De-duplicated logic (shared helpers + profile assembly).
- Soft, low-contrast dark theme; no bright whites.

Run:
  pip install dash plotly
  python fum_live.py --runs-root runs
"""
import argparse
import json
import os
import sys
import time
import threading
import subprocess
from typing import Any, Dict, List, Tuple

import plotly.graph_objs as go
import dash
from dash import Dash, dcc, html, Input, Output, State, no_update

# ---------------- CLI ----------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--runs-root", default="runs")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8050)
    p.add_argument("--debug", action="store_true")
    return p.parse_args()

# -------------- FS utils -------------
from fum_rt.frontend.utilities.fs_utils import list_runs, _list_files

# ------- Tailing JSONL with offsets (modular) -------

# --------- Streaming ZEMA and series (modular) -------

# --------- Process manager (imported) -----
from fum_rt.frontend.services.process_manager import ProcessManager
from fum_rt.frontend.utilities.profiles import get_default_profile
from fum_rt.frontend.styles.theme import get_global_css
from fum_rt.frontend.components.workspace import workspace_card
from fum_rt.frontend.components.runtime_controls import runtime_controls_card
from fum_rt.frontend.components.feed import feed_card
from fum_rt.frontend.components.run_config import run_config_card
from fum_rt.frontend.components.charts import charts_card
from fum_rt.frontend.components.chat import chat_card
from fum_rt.frontend.callbacks.workspace import register_workspace_callbacks
from fum_rt.frontend.callbacks.charts import register_chart_callbacks
from fum_rt.frontend.callbacks.runtime import register_runtime_callbacks
from fum_rt.frontend.callbacks.process import register_process_callbacks
from fum_rt.frontend.callbacks.feed import register_feed_callbacks
from fum_rt.frontend.callbacks.profile import register_profile_callbacks
from fum_rt.frontend.callbacks.logs import register_logs_callbacks
from fum_rt.frontend.callbacks.chat import register_chat_callbacks
from fum_rt.frontend.callbacks.engram import register_engram_callbacks


# ------------- Live series state -------------
# Using modular imports for timeseries and chat helpers.
# (SeriesState, extract_tick, append_event, append_say, ffill) are imported above from fum_rt.frontend.models.series.


# moved: latest_checkpoint imported from fum_rt.frontend.utilities.fs_utils


# ------------- Build Dash app ---------------
def build_app(runs_root: str) -> Dash:
    app = Dash(__name__)
    app.title = "Fully Unified Void Dynamics Model: Live Dashboard"

    # --- Soft‑dark theme (no bright whites) ---
    GLOBAL_CSS = get_global_css()
    app.index_string = app.index_string.replace("</head>", f"<style>{GLOBAL_CSS}</style></head>")

    runs = list_runs(runs_root)
    default_run = runs[0] if runs else ""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    PROFILES_DIR = os.path.join(repo_root, "run_profiles")
    os.makedirs(PROFILES_DIR, exist_ok=True)
    manager = ProcessManager(runs_root)

    default_profile = get_default_profile()

    def list_profiles() -> List[str]:
        return sorted([os.path.join(PROFILES_DIR, f) for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])

    domain_options = [
        {"label": n, "value": n}
        for n in ["math_physics", "quantum", "standard_model", "dark_matter", "biology_consciousness", "cosmogenesis", "higgs"]
    ]
    profile_options = [{"label": os.path.basename(p), "value": p} for p in list_profiles()]
    data_files_options = [{"label": p, "value": p} for p in _list_files(os.path.join(repo_root, "fum_rt", "data"), exts=None, recursive=True)]

    # -------- Layout (organized, soft-dark) --------
    app.layout = html.Div([
        html.H3("FUM Live Dashboard (external control)"),
        html.Div([
            # Left panel
            html.Div([
                workspace_card(runs_root, runs, default_run),
                runtime_controls_card(default_profile),
                feed_card(data_files_options),
            ], style={"minWidth": "320px", "display":"grid", "gap":"16px"}),

            # Right panel
            html.Div([
                run_config_card(default_profile, domain_options, profile_options),
                charts_card(),
                chat_card(),
            ], style={"minWidth": "400px", "display":"grid", "gap":"16px"}),
        ], className="grid"),
        dcc.Interval(id="poll", interval=1500, n_intervals=0),
        dcc.Store(id="chat-state"),
        dcc.Store(id="ui-state")
    ], style={"padding":"10px"})

    # ---------- Callbacks ----------
    register_workspace_callbacks(app, runs_root, manager)
    register_chart_callbacks(app)
    register_runtime_callbacks(app, default_profile)
    register_feed_callbacks(app, manager, repo_root)
    register_process_callbacks(app, runs_root, manager, default_profile)
    register_profile_callbacks(app, PROFILES_DIR, default_profile)
    register_logs_callbacks(app, manager)
    register_chat_callbacks(app)
    register_engram_callbacks(app)

    # moved to fum_rt.frontend.callbacks.runtime.register_runtime_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.feed.register_feed_callbacks

    # moved to fum_rt.frontend.callbacks.profile.register_profile_callbacks

    # moved to fum_rt.frontend.callbacks.profile.register_profile_callbacks

    # moved to fum_rt.frontend.callbacks.workspace.register_workspace_callbacks

    # moved to fum_rt.frontend.callbacks.workspace.register_workspace_callbacks

    # moved to fum_rt.frontend.callbacks.engram.register_engram_callbacks

    # moved to fum_rt.frontend.callbacks.engram.register_engram_callbacks

    # moved to fum_rt.frontend.callbacks.charts.register_chart_callbacks

    # moved to fum_rt.frontend.callbacks.logs.register_logs_callbacks

    # moved to fum_rt.frontend.callbacks.chat.register_chat_callbacks

    # moved to fum_rt.frontend.callbacks.chat.register_chat_callbacks
    return app

def main():
    args = parse_args()
    app = build_app(args.runs_root)
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
