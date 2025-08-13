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
from fum_rt.frontend.utilities.fs_utils import list_runs, read_json_file, write_json_file, _list_files, latest_checkpoint

# ------- Tailing JSONL with offsets (modular) -------
from fum_rt.frontend.utilities.tail import tail_jsonl_bytes

# --------- Streaming ZEMA and series (modular) -------
from fum_rt.frontend.models.series import (
    StreamingZEMA,
    SeriesState,
    extract_tick,
    append_event,
    append_say,
    ffill,
)

# --------- Process manager (imported) -----
from fum_rt.frontend.services.process_manager import ProcessManager
from fum_rt.frontend.utilities.profiles import (
    get_default_profile,
    checklist_from_bool,
    bool_from_checklist,
    safe_int,
    safe_float,
)
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


# ------------- Live series state -------------
# Using modular imports for timeseries and chat helpers.
# (SeriesState, extract_tick, append_event, append_say, ffill) are imported above from fum_rt.frontend.models.series.

# -------- Helpers (delegated to utilities.profiles) --------
# Centralize conversions and checklist handling to avoid duplication.
_safe_int = safe_int
_safe_float = safe_float
_bool_from_checklist = bool_from_checklist
_checklist_from_bool = checklist_from_bool

# moved: latest_checkpoint imported from fum_rt.frontend.utilities.fs_utils

def assemble_profile(*args, **kwargs):
    """
    Delegation shim: use centralized assembler from utilities.profiles.
    Keeps local call sites unchanged while ensuring single source of truth.
    """
    from fum_rt.frontend.utilities.profiles import assemble_profile as _assemble
    return _assemble(*args, **kwargs)

# ------------- Build Dash app ---------------
def build_app(runs_root: str) -> Dash:
    app = Dash(__name__)
    app.title = "FUM Live Dashboard"

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

    # moved to fum_rt.frontend.callbacks.runtime.register_runtime_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.process.register_process_callbacks

    # moved to fum_rt.frontend.callbacks.feed.register_feed_callbacks

    @app.callback(
        Output("profile-path","options"),
        Output("profile-save-status","children"),
        Input("save-profile","n_clicks"),
        State("profile-name","value"),
        State("cfg-neurons","value"),
        State("cfg-k","value"),
        State("cfg-hz","value"),
        State("cfg-domain","value"),
        State("cfg-use-time-dynamics","value"),
        State("cfg-sparse-mode","value"),
        State("cfg-threshold","value"),
        State("cfg-lambda-omega","value"),
        State("cfg-candidates","value"),
        State("cfg-walkers","value"),
        State("cfg-hops","value"),
        State("cfg-status-interval","value"),
        State("cfg-bundle-size","value"),
        State("cfg-prune-factor","value"),
        State("cfg-stim-group-size","value"),
        State("cfg-stim-amp","value"),
        State("cfg-stim-decay","value"),
        State("cfg-stim-max-symbols","value"),
        State("cfg-speak-auto","value"),
        State("cfg-speak-z","value"),
        State("cfg-speak-hysteresis","value"),
        State("cfg-speak-cooldown-ticks","value"),
        State("cfg-speak-valence-thresh","value"),
        State("cfg-b1-half-life-ticks","value"),
        State("cfg-viz-every","value"),
        State("cfg-log-every","value"),
        State("cfg-checkpoint-every","value"),
        State("cfg-checkpoint-keep","value"),
        State("cfg-duration","value"),
        prevent_initial_call=True
    )
    def on_save_profile(_n, name,
                        neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
                        walkers, hops, status_interval, bundle_size, prune_factor,
                        stim_group_size, stim_amp, stim_decay, stim_max_symbols,
                        speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
                        viz_every, log_every, checkpoint_every, checkpoint_keep, duration):
        name = (name or "").strip()
        if not name:
            return [{"label": os.path.basename(p), "value": p} for p in list_profiles()], "Provide a profile name."
        data = assemble_profile(
            neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
            walkers, hops, status_interval, bundle_size, prune_factor,
            stim_group_size, stim_amp, stim_decay, stim_max_symbols,
            speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
            viz_every, log_every, checkpoint_every, checkpoint_keep, duration,
            default_profile
        )
        path = os.path.join(PROFILES_DIR, f"{name}.json")
        ok = write_json_file(path, data)
        status = f"Saved profile to {path}" if ok else f"Error writing {path}"
        return [{"label": os.path.basename(p), "value": p} for p in list_profiles()], status

    @app.callback(
        Output("cfg-neurons","value"),
        Output("cfg-k","value"),
        Output("cfg-hz","value"),
        Output("cfg-domain","value"),
        Output("cfg-use-time-dynamics","value"),
        Output("cfg-sparse-mode","value"),
        Output("cfg-threshold","value"),
        Output("cfg-lambda-omega","value"),
        Output("cfg-candidates","value"),
        Output("cfg-walkers","value"),
        Output("cfg-hops","value"),
        Output("cfg-status-interval","value"),
        Output("cfg-bundle-size","value"),
        Output("cfg-prune-factor","value"),
        Output("cfg-stim-group-size","value"),
        Output("cfg-stim-amp","value"),
        Output("cfg-stim-decay","value"),
        Output("cfg-stim-max-symbols","value"),
        Output("cfg-speak-auto","value"),
        Output("cfg-speak-z","value"),
        Output("cfg-speak-hysteresis","value"),
        Output("cfg-speak-cooldown-ticks","value"),
        Output("cfg-speak-valence-thresh","value"),
        Output("cfg-b1-half-life-ticks","value"),
        Output("cfg-viz-every","value"),
        Output("cfg-log-every","value"),
        Output("cfg-checkpoint-every","value"),
        Output("cfg-checkpoint-keep","value"),
        Output("cfg-duration","value"),
        Input("load-profile","n_clicks"),
        State("profile-path","value"),
        prevent_initial_call=True
    )
    def on_load_profile(_n, path):
        if not path:
            raise dash.exceptions.PreventUpdate
        data = read_json_file(path) or {}
        def g(k, dv):
            v = data.get(k, dv)
            return v if v is not None else dv
        return (
            g("neurons", default_profile["neurons"]),
            g("k", default_profile["k"]),
            g("hz", default_profile["hz"]),
            g("domain", default_profile["domain"]),
            _checklist_from_bool(bool(g("use_time_dynamics", default_profile["use_time_dynamics"]))),
            _checklist_from_bool(bool(g("sparse_mode", default_profile["sparse_mode"]))),
            g("threshold", default_profile["threshold"]),
            g("lambda_omega", default_profile["lambda_omega"]),
            g("candidates", default_profile["candidates"]),
            g("walkers", default_profile["walkers"]),
            g("hops", default_profile["hops"]),
            g("status_interval", default_profile["status_interval"]),
            g("bundle_size", default_profile["bundle_size"]),
            g("prune_factor", default_profile["prune_factor"]),
            g("stim_group_size", default_profile["stim_group_size"]),
            g("stim_amp", default_profile["stim_amp"]),
            g("stim_decay", default_profile["stim_decay"]),
            g("stim_max_symbols", default_profile["stim_max_symbols"]),
            _checklist_from_bool(bool(g("speak_auto", default_profile["speak_auto"]))),
            g("speak_z", default_profile["speak_z"]),
            g("speak_hysteresis", default_profile["speak_hysteresis"]),
            g("speak_cooldown_ticks", default_profile["speak_cooldown_ticks"]),
            g("speak_valence_thresh", default_profile["speak_valence_thresh"]),
            g("b1_half_life_ticks", default_profile["b1_half_life_ticks"]),
            g("viz_every", default_profile["viz_every"]),
            g("log_every", default_profile["log_every"]),
            g("checkpoint_every", default_profile["checkpoint_every"]),
            g("checkpoint_keep", default_profile["checkpoint_keep"]),
            g("duration", default_profile["duration"])
        )

    # moved to fum_rt.frontend.callbacks.workspace.register_workspace_callbacks

    # moved to fum_rt.frontend.callbacks.workspace.register_workspace_callbacks

    @app.callback(
        Output("rc-load-engram-path", "options"),
        Input("runs-root", "value"),
        prevent_initial_call=False
    )
    def on_runs_root_change(runs_root_dir):
        if not runs_root_dir or not os.path.isdir(runs_root_dir):
            return []
        engram_files = _list_files(runs_root_dir, exts=[".h5", ".npz"], recursive=True)
        options = []
        for rel_path in engram_files:
            full_path = os.path.join(runs_root_dir, rel_path)
            options.append({"label": rel_path.replace(os.path.sep, '/'), "value": full_path})
        return options

    @app.callback(
        Output("rc-load-engram-input","value", allow_duplicate=True),
        Input("rc-load-engram-path","value"),
        prevent_initial_call=True
    )
    def sync_engram_input_from_dropdown(val):
        return val

    # moved to fum_rt.frontend.callbacks.charts.register_chart_callbacks

    @app.callback(
        Output("launch-log","children"),
        Input("poll","n_intervals"),
        Input("show-log","n_clicks"),
        prevent_initial_call=False,
    )
    def update_launch_log(_n, _clicks):
        try:
            path = manager.launch_log
            if not path or not os.path.exists(path):
                return "No launcher log yet."
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                data = fh.read()
            return data[-4000:]
        except Exception as e:
            return f"Error reading launcher log: {e}"

    @app.callback(
        Output("chat-status","children"),
        Output("chat-input","value"),
        Input("chat-send","n_clicks"),
        State("run-dir","value"),
        State("chat-input","value"),
        prevent_initial_call=True
    )
    def on_chat_send(_n, run_dir, text):
        rd = (run_dir or "").strip()
        msg = (text or "").strip()
        if not rd:
            return "Select a run directory.", no_update
        if not msg:
            return "Type a message.", no_update
        try:
            inbox = os.path.join(rd, "chat_inbox.jsonl")
            os.makedirs(os.path.dirname(inbox), exist_ok=True)
            with open(inbox, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"type":"text","msg": msg}, ensure_ascii=False) + "\\n")
            return "Sent.", ""
        except Exception as e:
            return f"Error writing chat_inbox.jsonl: {e}", no_update

    @app.callback(
        Output("chat-view","children"),
        Output("chat-state","data"),
        Input("poll","n_intervals"),
        Input("chat-filter","value"),
        State("run-dir","value"),
        State("chat-state","data"),
        prevent_initial_call=False
    )
    def on_chat_update(_n, filt, run_dir, data):
        rd = (run_dir or "").strip()
        if not rd:
            return "", {"run_dir":"", "utd_size":0, "inbox_size":0, "items":[]}

        state = data or {}
        items = list(state.get("items", []))
        last_run = state.get("run_dir")
        utd_size = int(state.get("utd_size", 0)) if isinstance(state.get("utd_size"), int) else 0
        inbox_size = int(state.get("inbox_size", 0)) if isinstance(state.get("inbox_size"), int) else 0

        if last_run != rd:
            items = []
            utd_size = 0
            inbox_size = 0

        utd_path = os.path.join(rd, "utd_events.jsonl")
        new_utd_recs, new_utd_size = tail_jsonl_bytes(utd_path, utd_size)
        for rec in new_utd_recs:
            try:
                if isinstance(rec, dict) and (rec.get("type") == "macro"):
                    macro_name = rec.get("macro", "unknown")
                    args = rec.get("args", {})
                    if macro_name == "say":
                        text = args.get("text", "")
                    else:
                        text = f"macro: {macro_name}"
                        if args:
                            try:
                                arg_str = ", ".join(f"{k}={v}" for k,v in args.items())
                                text += f" ({arg_str})"
                            except:
                                text += f" (args: {args})"
                    why = rec.get("why") or {}
                    t = None
                    try:
                        t = int((why or {}).get("t"))
                    except Exception:
                        t = None
                    spike = False
                    if isinstance(why, dict):
                        try:
                            speak_ok = why.get("speak_ok")
                            spike = bool(speak_ok) or bool((why or {}).get('spike'))
                        except Exception:
                            spike = False
                    items.append({"kind":"model", "text": str(text), "t": t, "spike": bool(spike), "macro": macro_name})
            except Exception:
                pass

        inbox_path = os.path.join(rd, "chat_inbox.jsonl")
        new_inbox_recs, new_inbox_size = tail_jsonl_bytes(inbox_path, inbox_size)
        for rec in new_inbox_recs:
            try:
                if isinstance(rec, dict):
                    mtype = (rec.get("type") or "").lower()
                    if mtype == "text":
                        msg = rec.get("msg") or rec.get("text") or ""
                        if msg:
                            items.append({"kind":"user", "text": str(msg), "t": None, "spike": False})
            except Exception:
                pass

        if len(items) > 200:
            items = items[-200:]

        filt = (filt or "all").lower()
        view_lines = []
        for it in items:
            if filt == "say":
                if it.get("kind") != "model" or it.get("macro") != "say":
                    continue
            elif filt == "spike":
                if it.get("kind") != "model" or not it.get("spike", False) or it.get("macro") != "say":
                    continue
            t = it.get("t")
            text = it.get("text") or ""
            if it.get("kind") == "user":
                view_lines.append(f"You: {text}")
            else:
                if t is not None:
                    view_lines.append(f"[t={t}] {text}")
                else:
                    view_lines.append(f"{text}")
        view = "\\n".join(view_lines)
        return view, {"run_dir": rd, "utd_size": int(new_utd_size), "inbox_size": int(new_inbox_size), "items": items}

    return app

def main():
    args = parse_args()
    app = build_app(args.runs_root)
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
