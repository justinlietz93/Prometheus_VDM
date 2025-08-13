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
from fum_rt.frontend.utilities.fs_utils import list_runs, read_json_file, write_json_file, _list_files

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


# ------------- Live series state -------------
# Using modular imports for timeseries and chat helpers.
# (SeriesState, extract_tick, append_event, append_say, ffill) are imported above from fum_rt.frontend.models.series.

# -------- Helpers --------
def _safe_int(x, default=None):
    try:
        return int(x)
    except Exception:
        return default

def _safe_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default

def _bool_from_checklist(val) -> bool:
    if isinstance(val, list):
        return 'on' in val
    return bool(val)

def _checklist_from_bool(b: bool):
    return ['on'] if bool(b) else []

def latest_checkpoint(run_dir: str) -> str | None:
    try:
        files = []
        for fn in os.listdir(run_dir):
            if fn.startswith("state_") and (fn.endswith(".h5") or fn.endswith(".npz")):
                ext = ".h5" if fn.endswith(".h5") else ".npz"
                step_str = fn[6:-len(ext)]
                try:
                    s = int(step_str)
                    files.append((s, os.path.join(run_dir, fn)))
                except Exception:
                    pass
        if files:
            files.sort(key=lambda x: x[0], reverse=True)
            return files[0][1]
    except Exception:
        return None
    return None

def assemble_profile(
    neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
    walkers, hops, status_interval, bundle_size, prune_factor,
    stim_group_size, stim_amp, stim_decay, stim_max_symbols,
    speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
    viz_every, log_every, checkpoint_every, checkpoint_keep, duration,
    default_profile: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "neurons": int(_safe_int(neurons, default_profile["neurons"])),
        "k": int(_safe_int(k, default_profile["k"])),
        "hz": int(_safe_int(hz, default_profile["hz"])),
        "domain": str(domain or default_profile["domain"]),
        "use_time_dynamics": _bool_from_checklist(use_td) if use_td is not None else default_profile["use_time_dynamics"],
        "sparse_mode": _bool_from_checklist(sparse_mode) if sparse_mode is not None else default_profile["sparse_mode"],
        "threshold": float(_safe_float(threshold, default_profile["threshold"])),
        "lambda_omega": float(_safe_float(lambda_omega, default_profile["lambda_omega"])),
        "candidates": int(_safe_int(candidates, default_profile["candidates"])),
        "walkers": int(_safe_int(walkers, default_profile["walkers"])),
        "hops": int(_safe_int(hops, default_profile["hops"])),
        "status_interval": int(_safe_int(status_interval, default_profile["status_interval"])),
        "bundle_size": int(_safe_int(bundle_size, default_profile["bundle_size"])),
        "prune_factor": float(_safe_float(prune_factor, default_profile["prune_factor"])),
        "stim_group_size": int(_safe_int(stim_group_size, default_profile["stim_group_size"])),
        "stim_amp": float(_safe_float(stim_amp, default_profile["stim_amp"])),
        "stim_decay": float(_safe_float(stim_decay, default_profile["stim_decay"])),
        "stim_max_symbols": int(_safe_int(stim_max_symbols, default_profile["stim_max_symbols"])),
        "speak_auto": _bool_from_checklist(speak_auto) if speak_auto is not None else default_profile["speak_auto"],
        "speak_z": float(_safe_float(speak_z, default_profile["speak_z"])),
        "speak_hysteresis": float(_safe_float(speak_hyst, default_profile["speak_hysteresis"])),
        "speak_cooldown_ticks": int(_safe_int(speak_cd, default_profile["speak_cooldown_ticks"])),
        "speak_valence_thresh": float(_safe_float(speak_val, default_profile["speak_valence_thresh"])),
        "b1_half_life_ticks": int(_safe_int(b1_hl, default_profile["b1_half_life_ticks"])),
        "viz_every": int(_safe_int(viz_every, default_profile["viz_every"])),
        "log_every": int(_safe_int(log_every, default_profile["log_every"])),
        "checkpoint_every": int(_safe_int(checkpoint_every, default_profile["checkpoint_every"])),
        "checkpoint_keep": int(_safe_int(checkpoint_keep, default_profile["checkpoint_keep"])),
        "duration": None if duration in (None, "", "None") else int(_safe_int(duration, 0)),
    }

# ------------- Build Dash app ---------------
def build_app(runs_root: str) -> Dash:
    app = Dash(__name__)
    app.title = "FUM Live Dashboard"

    # --- Soft‑dark theme (no bright whites) ---
    GLOBAL_CSS = """
    :root{
      --bg:#0b0f14; --panel:#10151c; --panel2:#0e141a; --text:#cfd7e3; --muted:#8699ac;
      --accent:#6aa0c2; --ok:#3a8f5c; --danger:#b3565c; --border:#1d2733; --grid:#233140;
      --plot:#0f141a; --paper:#10151c;
    }
    *{box-sizing:border-box}
    body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Ubuntu,Cantarell,Helvetica Neue,Arial,Noto Sans,sans-serif;}
    h1,h2,h3,h4{color:var(--text);font-weight:600}
    .grid{display:grid;grid-template-columns:360px 1fr;gap:16px}
    .card{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px}
    .card h4,.card h3{margin:0 0 8px 0}
    label{font-size:12px;color:var(--muted);margin-bottom:4px;display:block}
    .row{display:flex;gap:8px;flex-wrap:wrap}
    .row>div{flex:1;min-width:120px}
    button{cursor:pointer;border-radius:8px;border:1px solid var(--border);padding:6px 10px;background:var(--panel2);color:var(--text)}
    button:hover{filter:brightness(1.05)}
    .btn-ok{background:var(--ok);color:#fff;border:none}
    .btn-danger{background:var(--danger);color:#fff;border:none}
    pre{background:#0a0e13;border:1px solid var(--border);border-radius:8px;padding:8px;white-space:pre-wrap;color:#dfe7f1}
    input[type="text"],input[type="number"],textarea,select{
        width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--border);
        border-radius:8px;padding:6px 8px;outline:none;
    }
    input::placeholder,textarea::placeholder{color:var(--muted)}
    input:focus,textarea:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(106,160,194,0.15)}
    /* dcc.Dropdown (react-select) */
    .Select-control{background:var(--panel2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px}
    .Select--single>.Select-control .Select-value{color:var(--text)!important}
    .Select-menu-outer{background:var(--panel2)!important;border:1px solid var(--border)!important;color:var(--text)!important}
    .Select-option{background:var(--panel2)!important;color:var(--text)!important}
    .Select-option.is-focused{background:#121a22!important}
    .Select-option.is-selected{background:#17222c!important}
    .VirtualizedSelectFocusedOption{background:#121a22!important}
    /* rc-slider */
    .rc-slider{padding:8px 0}
    .rc-slider-rail{background: #0d1218}
    .rc-slider-track{background: var(--accent)}
    .rc-slider-dot{border-color:#233140;background:#10151c}
    .rc-slider-handle{border:1px solid var(--border);background:var(--panel2)}
    .tight{margin-top:6px}
    """
    app.index_string = app.index_string.replace("</head>", f"<style>{GLOBAL_CSS}</style></head>")

    runs = list_runs(runs_root)
    default_run = runs[0] if runs else ""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    PROFILES_DIR = os.path.join(repo_root, "run_profiles")
    os.makedirs(PROFILES_DIR, exist_ok=True)
    manager = ProcessManager(runs_root)

    default_profile = {
        "neurons": 1000, "k": 12, "hz": 10, "domain": "math_physics",
        "use_time_dynamics": True,
        "sparse_mode": False, "threshold": 0.15, "lambda_omega": 0.10, "candidates": 64,
        "walkers": 256, "hops": 3, "bundle_size": 3, "prune_factor": 0.10, "status_interval": 1,
        "viz_every": 0, "log_every": 1,
        "speak_auto": True, "speak_z": 3.0, "speak_hysteresis": 0.5, "speak_cooldown_ticks": 10, "speak_valence_thresh": 0.55,
        "b1_half_life_ticks": 50,
        "stim_group_size": 8, "stim_amp": 0.08, "stim_decay": 0.92, "stim_max_symbols": 128,
        "checkpoint_every": 60, "checkpoint_keep": 5, "duration": None
    }

    def list_profiles() -> List[str]:
        return sorted([os.path.join(PROFILES_DIR, f) for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])

    domain_options = [
        {"label": n, "value": n}
        for n in ["math_physics", "quantum", "standard_model", "dark_matter", "biology_consciousness", "cosmogenesis", "higgs"]
    ]

    # -------- Layout (organized, soft-dark) --------
    app.layout = html.Div([
        html.H3("FUM Live Dashboard (external control)"),
        html.Div([
            # Left panel
            html.Div([
                html.Div([
                    html.H4("Workspace"),
                    html.Label("Runs root"),
                    dcc.Input(id="runs-root", type="text", value=runs_root, style={"width":"100%"}),
                    html.Div([
                        html.Button("Refresh Runs", id="refresh-runs", n_clicks=0),
                        html.Button("Use Current Run", id="use-current-run", n_clicks=0),
                        html.Button("Use Latest Run", id="use-latest-run", n_clicks=0),
                    ], className="row tight"),
                    html.Label("Run directory"),
                    dcc.Dropdown(id="run-dir", options=[{"label": p, "value": p} for p in runs], value=default_run),
                ], className="card"),

                html.Div([
                    html.H4("Runtime Controls"),
                    html.Label("Phase"),
                    dcc.Slider(id="phase", min=0, max=4, step=1, value=0, marks={i:str(i) for i in range(5)}),

                    html.Div([
                        html.Div([html.Label("Speak z"), dcc.Input(id="rc-speak-z", type="number", value=default_profile["speak_z"], step=0.1, min=0)]),
                        html.Div([html.Label("Hysteresis"), dcc.Input(id="rc-speak-hysteresis", type="number", value=default_profile["speak_hysteresis"], step=0.1, min=0)]),
                        html.Div([html.Label("Cooldown (ticks)"), dcc.Input(id="rc-speak-cooldown", type="number", value=default_profile["speak_cooldown_ticks"], step=1, min=1)]),
                        html.Div([html.Label("Valence thresh"), dcc.Input(id="rc-speak-valence", type="number", value=default_profile["speak_valence_thresh"], step=0.01, min=0, max=1)]),
                    ], className="row tight"),

                    html.Div([
                        html.Div([html.Label("Walkers"), dcc.Input(id="rc-walkers", type="number", value=default_profile["walkers"], step=1, min=1)]),
                        html.Div([html.Label("Hops"), dcc.Input(id="rc-hops", type="number", value=default_profile["hops"], step=1, min=1)]),
                        html.Div([html.Label("Bundle size"), dcc.Input(id="rc-bundle-size", type="number", value=default_profile["bundle_size"], step=1, min=1)]),
                        html.Div([html.Label("Prune factor"), dcc.Input(id="rc-prune-factor", type="number", value=default_profile["prune_factor"], step=0.01, min=0, max=1)]),
                    ], className="row tight"),

                    html.Div([
                        html.Div([html.Label("Threshold"), dcc.Input(id="rc-threshold", type="number", value=default_profile.get("threshold", 0.15), step=0.01, min=0)]),
                        html.Div([html.Label("Lambda omega"), dcc.Input(id="rc-lambda-omega", type="number", value=default_profile.get("lambda_omega", 0.10), step=0.01, min=0)]),
                        html.Div([html.Label("Candidates"), dcc.Input(id="rc-candidates", type="number", value=default_profile.get("candidates", 64), step=1, min=1)]),
                    ], className="row tight"),

                    html.Div([html.Label("SIE novelty IDF gain"), dcc.Input(id="rc-novelty-idf-gain", type="number", value=1.0, step=0.05, min=0)], className="tight"),
                    html.Div([html.Button("Apply Runtime Settings", id="apply-phase", n_clicks=0, className="btn-ok")], className="tight"),
                    html.Pre(id="phase-status", style={"fontSize":"12px"}),

                    html.Label("Load Engram (runtime, into selected Run)"),
                    dcc.Input(id="rc-load-engram-input", type="text", placeholder="path to .h5/.npz (abs or under runs)", style={"width":"100%"}),
                    dcc.Dropdown(id="rc-load-engram-path", placeholder="select from runs...", style={"width":"100%","marginTop":"4px"}),
                    html.Button("Load Engram Now", id="rc-load-engram-btn", n_clicks=0, className="tight"),
                ], className="card"),

                html.Div([
                    html.H4("Feed stdin (optional)"),
                    dcc.Dropdown(id="feed-path",
                                 options=[{"label": p, "value": p} for p in _list_files(os.path.join(repo_root, "fum_rt", "data"), exts=None, recursive=True)],
                                 placeholder="select feed file...", style={"width":"100%"}),
                    dcc.Input(id="feed-rate", type="number", value=20, step=1, style={"width":"120px", "marginTop":"6px"}),
                    html.Div([
                        html.Button("Start Feed", id="feed-start", n_clicks=0, className="btn-ok"),
                        html.Button("Stop Feed", id="feed-stop", n_clicks=0, className="btn-danger"),
                    ], className="row tight"),
                    html.Pre(id="send-status", style={"fontSize":"12px"}),
                ], className="card"),
            ], style={"minWidth": "320px", "display":"grid", "gap":"16px"}),

            # Right panel
            html.Div([
                html.Div([
                    html.H4("Run configuration & process"),
                    # Core
                    html.Div([
                        html.Div([html.Label("Neurons"), dcc.Input(id="cfg-neurons", type="number", value=default_profile["neurons"], step=1, min=1)]),
                        html.Div([html.Label("k"), dcc.Input(id="cfg-k", type="number", value=default_profile["k"], step=1, min=1)]),
                        html.Div([html.Label("Hz"), dcc.Input(id="cfg-hz", type="number", value=default_profile["hz"], step=1, min=1)]),
                        html.Div([html.Label("Domain"), dcc.Dropdown(id="cfg-domain", options=domain_options, value=default_profile["domain"])]),
                    ], className="row"),

                    html.Div([
                        html.Div([html.Label("Use time dynamics"), dcc.Checklist(id="cfg-use-time-dynamics", options=[{"label":" On","value":"on"}], value=_checklist_from_bool(default_profile["use_time_dynamics"]))]),
                        html.Div([html.Label("Sparse mode"), dcc.Checklist(id="cfg-sparse-mode", options=[{"label":" On","value":"on"}], value=_checklist_from_bool(default_profile["sparse_mode"]))]),
                    ], className="row"),

                    html.Label("Structure & traversal"),
                    html.Div([
                        html.Div([html.Label("Threshold"), dcc.Input(id="cfg-threshold", type="number", value=default_profile["threshold"], step=0.01, min=0)]),
                        html.Div([html.Label("Lambda omega"), dcc.Input(id="cfg-lambda-omega", type="number", value=default_profile["lambda_omega"], step=0.01, min=0)]),
                        html.Div([html.Label("Candidates"), dcc.Input(id="cfg-candidates", type="number", value=default_profile["candidates"], step=1, min=1)]),
                        html.Div([html.Label("Walkers"), dcc.Input(id="cfg-walkers", type="number", value=default_profile["walkers"], step=1, min=1)]),
                        html.Div([html.Label("Hops"), dcc.Input(id="cfg-hops", type="number", value=default_profile["hops"], step=1, min=1)]),
                        html.Div([html.Label("Bundle size"), dcc.Input(id="cfg-bundle-size", type="number", value=default_profile["bundle_size"], step=1, min=1)]),
                        html.Div([html.Label("Prune factor"), dcc.Input(id="cfg-prune-factor", type="number", value=default_profile["prune_factor"], step=0.01, min=0, max=1)]),
                        html.Div([html.Label("Status interval"), dcc.Input(id="cfg-status-interval", type="number", value=default_profile["status_interval"], step=1, min=1)]),
                    ], className="row"),

                    html.Label("Stimulus"),
                    html.Div([
                        html.Div([html.Label("Group size"), dcc.Input(id="cfg-stim-group-size", type="number", value=default_profile["stim_group_size"], step=1, min=1)]),
                        html.Div([html.Label("Amp"), dcc.Input(id="cfg-stim-amp", type="number", value=default_profile["stim_amp"], step=0.01, min=0)]),
                        html.Div([html.Label("Decay"), dcc.Input(id="cfg-stim-decay", type="number", value=default_profile["stim_decay"], step=0.01, min=0, max=1)]),
                        html.Div([html.Label("Max symbols"), dcc.Input(id="cfg-stim-max-symbols", type="number", value=default_profile["stim_max_symbols"], step=1, min=1)]),
                    ], className="row"),

                    html.Label("Speak / B1 spike detector"),
                    html.Div([
                        html.Div([html.Label("Speak auto"), dcc.Checklist(id="cfg-speak-auto", options=[{"label":" On","value":"on"}], value=_checklist_from_bool(default_profile["speak_auto"]))]),
                        html.Div([html.Label("Speak z"), dcc.Input(id="cfg-speak-z", type="number", value=default_profile["speak_z"], step=0.1, min=0)]),
                        html.Div([html.Label("Hysteresis"), dcc.Input(id="cfg-speak-hysteresis", type="number", value=default_profile["speak_hysteresis"], step=0.1, min=0)]),
                        html.Div([html.Label("Cooldown (ticks)"), dcc.Input(id="cfg-speak-cooldown-ticks", type="number", value=default_profile["speak_cooldown_ticks"], step=1, min=1)]),
                        html.Div([html.Label("Valence thresh"), dcc.Input(id="cfg-speak-valence-thresh", type="number", value=default_profile["speak_valence_thresh"], step=0.01, min=0, max=1)]),
                        html.Div([html.Label("B1 half-life (ticks)"), dcc.Input(id="cfg-b1-half-life-ticks", type="number", value=default_profile["b1_half_life_ticks"], step=1, min=1)]),
                    ], className="row"),

                    html.Label("Viz / Logs / Checkpoints"),
                    html.Div([
                        html.Div([html.Label("viz_every"), dcc.Input(id="cfg-viz-every", type="number", value=default_profile["viz_every"], step=1, min=0)]),
                        html.Div([html.Label("log_every"), dcc.Input(id="cfg-log-every", type="number", value=default_profile["log_every"], step=1, min=1)]),
                        html.Div([html.Label("checkpoint_every"), dcc.Input(id="cfg-checkpoint-every", type="number", value=default_profile["checkpoint_every"], step=1, min=0)]),
                        html.Div([html.Label("checkpoint_keep"), dcc.Input(id="cfg-checkpoint-keep", type="number", value=default_profile["checkpoint_keep"], step=1, min=0)]),
                        html.Div([html.Label("duration (s)"), dcc.Input(id="cfg-duration", type="number", value=default_profile["duration"], step=1, min=0)]),
                    ], className="row"),

                    html.Div([
                        dcc.Input(id="profile-name", type="text", placeholder="profile name", style={"width":"200px"}),
                        html.Button("Save Profile", id="save-profile", n_clicks=0),
                        dcc.Dropdown(id="profile-path", options=[{"label": os.path.basename(p), "value": p} for p in list_profiles()], placeholder="load profile", style={"width":"50%"}),
                        html.Button("Load", id="load-profile", n_clicks=0),
                    ], className="row tight"),
                    html.Pre(id="profile-save-status", style={"fontSize":"12px","whiteSpace":"pre-wrap"}),

                    html.Div([
                        html.Button("Start New Run", id="start-run", n_clicks=0, className="btn-ok"),
                        html.Button("Resume Selected Run", id="resume-run", n_clicks=0),
                        html.Button("Stop Managed Run", id="stop-run", n_clicks=0, className="btn-danger"),
                    ], className="row tight"),
                    html.Pre(id="proc-status", style={"fontSize":"12px","whiteSpace":"pre-wrap"}),
                    html.Button("Show Launcher Log", id="show-log", n_clicks=0),
                    html.Pre(id="launch-log", style={"fontSize":"12px","maxHeight":"240px","overflowY":"auto"}),
                ], className="card"),

                html.Div([
                    dcc.Graph(id="fig-dashboard", style={"height":"420px","width":"100%"}),
                    dcc.Graph(id="fig-discovery", style={"height":"320px","width":"100%"}),
                ], className="card"),

                html.Div([
                    html.H4("Chat"),
                    html.Pre(
                        id="chat-view",
                        style={
                            "height":"220px",
                            "overflowY":"auto",
                            "overflowX":"hidden",
                            "backgroundColor":"#0f141a",
                            "color":"#e0e6ee",
                            "padding":"8px",
                            "whiteSpace":"pre-wrap",
                            "wordBreak":"break-word",
                            "overflowWrap":"anywhere",
                            "hyphens":"none",
                            "border":"1px solid #1d2733",
                            "borderRadius":"8px"
                        }
                    ),
                    html.Div([
                        html.Label("Chat filter"),
                        dcc.RadioItems(
                            id="chat-filter",
                            options=[
                                {"label": "All Outputs", "value": "all"},
                                {"label": "'say' Macro Only", "value": "say"},
                                {"label": "Self-Speak (Spike-Gated)", "value": "spike"}
                            ],
                            value="all",
                            labelStyle={"display":"inline-block","marginRight":"10px"}
                        ),
                    ], className="tight"),
                    html.Div([
                        dcc.Input(id="chat-input", type="text", placeholder="Type a message and click Send", style={"width":"80%"}),
                        html.Button("Send", id="chat-send", n_clicks=0),
                    ], className="row tight"),
                    html.Pre(id="chat-status", style={"fontSize":"12px"}),
                ], className="card"),
            ], style={"minWidth": "400px", "display":"grid", "gap":"16px"}),
        ], className="grid"),
        dcc.Interval(id="poll", interval=1500, n_intervals=0),
        dcc.Store(id="chat-state"),
        dcc.Store(id="ui-state")
    ], style={"padding":"10px"})

    # ---------- Callbacks ----------
    @app.callback(
        Output("run-dir","options"),
        Output("run-dir","value", allow_duplicate=True),
        Input("refresh-runs","n_clicks"),
        State("runs-root","value"),
        prevent_initial_call=True
    )
    def on_refresh_runs(_n, root):
        root = root or runs_root
        opts = [{"label": p, "value": p} for p in list_runs(root)]
        val = opts[0]["value"] if opts else ""
        return opts, val

    @app.callback(
        Output("phase-status","children"),
        Input("apply-phase","n_clicks"),
        State("run-dir","value"),
        State("phase","value"),
        State("rc-speak-z","value"),
        State("rc-speak-hysteresis","value"),
        State("rc-speak-cooldown","value"),
        State("rc-speak-valence","value"),
        State("rc-walkers","value"),
        State("rc-hops","value"),
        State("rc-bundle-size","value"),
        State("rc-prune-factor","value"),
        State("rc-threshold","value"),
        State("rc-lambda-omega","value"),
        State("rc-candidates","value"),
        State("rc-novelty-idf-gain","value"),
        prevent_initial_call=True
    )
    def on_apply_phase(_n, run_dir, phase,
                       s_z, s_h, s_cd, s_vt,
                       c_w, c_h, c_b, c_pf, c_thr, c_lw, c_cand, s_idf):
        if not run_dir:
            return "Select a run directory."
        prof = {
            "phase": int(_safe_int(phase, 0)),
            "speak": {
                "speak_z": float(_safe_float(s_z, default_profile["speak_z"])),
                "speak_hysteresis": float(_safe_float(s_h, default_profile["speak_hysteresis"])),
                "speak_cooldown_ticks": int(_safe_int(s_cd, default_profile["speak_cooldown_ticks"])),
                "speak_valence_thresh": float(_safe_float(s_vt, default_profile["speak_valence_thresh"])),
            },
            "connectome": {
                "walkers": int(_safe_int(c_w, default_profile["walkers"])),
                "hops": int(_safe_int(c_h, default_profile["hops"])),
                "bundle_size": int(_safe_int(c_b, default_profile["bundle_size"])),
                "prune_factor": float(_safe_float(c_pf, default_profile["prune_factor"])),
                "threshold": float(_safe_float(c_thr, default_profile.get("threshold", 0.15))),
                "lambda_omega": float(_safe_float(c_lw, default_profile.get("lambda_omega", 0.10))),
                "candidates": int(_safe_int(c_cand, default_profile.get("candidates", 64))),
            },
            "sie": {"novelty_idf_gain": float(_safe_float(s_idf, 1.0))}
        }
        ok = write_json_file(os.path.join(run_dir,"phase.json"), prof)
        return "Applied" if ok else "Error writing phase.json"

    @app.callback(
        Output("phase-status","children", allow_duplicate=True),
        Input("rc-load-engram-btn","n_clicks"),
        State("run-dir","value"),
        State("rc-load-engram-path","value"),
        State("rc-load-engram-input","value"),
        prevent_initial_call=True
    )
    def on_load_engram_now(_n, run_dir, path, path_text):
        rd = (run_dir or "").strip()
        if not rd:
            return "Select a run directory."
        p = ((path or path_text) or "").strip()
        if not p:
            return "Enter engram path."
        try:
            obj = read_json_file(os.path.join(rd, "phase.json")) or {}
            if not isinstance(obj, dict):
                obj = {}
            obj["load_engram"] = p
            ok = write_json_file(os.path.join(rd, "phase.json"), obj)
            return f"Queued load_engram: {p}" if ok else "Error writing phase.json"
        except Exception as e:
            return f"Error: {e}"

    @app.callback(
        Output("phase-status","children", allow_duplicate=True),
        Input("poll","n_intervals"),
        State("run-dir","value"),
        prevent_initial_call=True
    )
    def notify_engram_events(_n, run_dir):
        rd = (run_dir or "").strip()
        if not rd:
            return no_update
        state = getattr(notify_engram_events, "_state", None)
        if state is None or state.get("run_dir") != rd:
            state = {"run_dir": rd, "events_size": 0}
            setattr(notify_engram_events, "_state", state)
        ev_path = os.path.join(rd, "events.jsonl")
        recs, new_size = tail_jsonl_bytes(ev_path, state["events_size"])
        state["events_size"] = new_size
        msg = None
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            name = str(rec.get("event_type") or rec.get("event") or rec.get("message") or rec.get("msg") or rec.get("name") or "").lower()
            extra = rec.get("extra") or rec.get("meta") or {}
            if name == "engram_loaded":
                engram_path = extra.get("path") or extra.get("engram") or rec.get("path")
                msg = f"Engram loaded: {engram_path}" if engram_path else "Engram loaded."
            elif name == "engram_load_error":
                err = extra.get("err") or extra.get("error") or rec.get("error")
                engram_path = extra.get("path") or extra.get("engram") or rec.get("path")
                if err and engram_path:
                    msg = f"Engram load error: {err} ({engram_path})"
                elif err:
                    msg = f"Engram load error: {err}"
                else:
                    msg = "Engram load error."
        return (msg if msg else no_update)

    # ----- Start / Resume -----
    def start_or_resume(profile: Dict[str, Any]):
        ok, msg = manager.start(profile)
        if not ok:
            return f"Start failed:\\n{msg}", no_update
        rd = profile.get("run_dir") or msg
        cmd_echo = " ".join(manager.last_cmd or [])
        return (f"Started.\\nrun_dir={rd}\\n"
                f"checkpoint_every={profile.get('checkpoint_every')} keep={profile.get('checkpoint_keep')}\\n"
                f"cmd: {cmd_echo}\\n"
                f"launch_log: {manager.launch_log}"), rd or no_update

    @app.callback(
        Output("proc-status","children", allow_duplicate=True),
        Output("run-dir","value", allow_duplicate=True),
        Input("start-run","n_clicks"),
        State("runs-root","value"),
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
        State("rc-load-engram-path", "value"),
        State("rc-load-engram-input", "value"),
        prevent_initial_call=True
    )
    def on_start_run(n_start, root,
                     neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
                     walkers, hops, status_interval, bundle_size, prune_factor,
                     stim_group_size, stim_amp, stim_decay, stim_max_symbols,
                     speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
                     viz_every, log_every, checkpoint_every, checkpoint_keep, duration, load_engram_path, load_engram_input):
        if not n_start:
            raise dash.exceptions.PreventUpdate
        if root:
            try:
                manager.set_runs_root(root)
            except Exception:
                pass
        profile = assemble_profile(
            neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
            walkers, hops, status_interval, bundle_size, prune_factor,
            stim_group_size, stim_amp, stim_decay, stim_max_symbols,
            speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
            viz_every, log_every, checkpoint_every, checkpoint_keep, duration,
            default_profile
        )
        lep = (load_engram_input or load_engram_path)
        if lep:
            profile['load_engram'] = lep
            # Adopt the folder as run_dir so the whole bundle (events, lexicon, macro board) is reused.
            try:
                p = str(lep).strip()
                if p:
                    adopt_dir = p if os.path.isdir(p) else os.path.dirname(p)
                    if adopt_dir:
                        profile['run_dir'] = adopt_dir
            except Exception:
                pass
        return start_or_resume(profile)

    @app.callback(
        Output("proc-status","children", allow_duplicate=True),
        Output("run-dir","value", allow_duplicate=True),
        Input("resume-run","n_clicks"),
        State("runs-root","value"),
        State("run-dir","value"),
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
        State("rc-load-engram-path", "value"),
        State("rc-load-engram-input", "value"),
        prevent_initial_call=True
    )
    def on_resume_run(n_resume, root, run_dir,
                      neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
                      walkers, hops, status_interval, bundle_size, prune_factor,
                      stim_group_size, stim_amp, stim_decay, stim_max_symbols,
                      speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
                      viz_every, log_every, checkpoint_every, checkpoint_keep, duration, load_engram_path, load_engram_input):
        if not n_resume:
            raise dash.exceptions.PreventUpdate
        if root:
            try:
                manager.set_runs_root(root)
            except Exception:
                pass
        rd = (run_dir or "").strip()
        if not rd or not os.path.isdir(rd):
            return "Select an existing run directory to resume.", no_update

        profile = assemble_profile(
            neurons, k, hz, domain, use_td, sparse_mode, threshold, lambda_omega, candidates,
            walkers, hops, status_interval, bundle_size, prune_factor,
            stim_group_size, stim_amp, stim_decay, stim_max_symbols,
            speak_auto, speak_z, speak_hyst, speak_cd, speak_val, b1_hl,
            viz_every, log_every, checkpoint_every, checkpoint_keep, duration,
            default_profile
        )
        profile["run_dir"] = rd

        lep = (load_engram_input or load_engram_path)
        if not lep:
            lep = latest_checkpoint(rd)
        if lep:
            profile["load_engram"] = lep

        ok, msg = manager.start(profile)
        if not ok:
            return f"Resume failed:\\n{msg}", no_update

        cmd_echo = " ".join(manager.last_cmd or [])
        return (f"Resumed.\\nrun_dir={rd}\\n"
                f"load_engram={profile.get('load_engram','')}\\n"
                f"cmd: {cmd_echo}\\n"
                f"launch_log: {manager.launch_log}"), rd

    @app.callback(
        Output("proc-status","children", allow_duplicate=True),
        Input("stop-run","n_clicks"),
        prevent_initial_call=True
    )
    def on_stop_run(n_stop):
        if not n_stop:
            raise dash.exceptions.PreventUpdate
        ok, msg = manager.stop()
        return ("Stopped." if ok else msg)

    @app.callback(
        Output("send-status","children", allow_duplicate=True),
        Input("feed-start","n_clicks"),
        State("feed-path","value"),
        State("feed-rate","value"),
        prevent_initial_call=True
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
        return (f"Feeding from {chosen}." if ok else "Feed failed (check process running and path).")

    @app.callback(
        Output("send-status","children", allow_duplicate=True),
        Input("feed-stop","n_clicks"),
        prevent_initial_call=True
    )
    def on_feed_stop(_n):
        manager.stop_feed()
        return "Feed stopped."

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

    @app.callback(
        Output("run-dir","value", allow_duplicate=True),
        Input("use-current-run","n_clicks"),
        prevent_initial_call=True
    )
    def on_use_current(_n):
        return (manager.current_run_dir or no_update)

    @app.callback(
        Output("run-dir","value", allow_duplicate=True),
        Input("use-latest-run","n_clicks"),
        State("runs-root","value"),
        prevent_initial_call=True
    )
    def on_use_latest(_n, root):
        r = (root or runs_root)
        rs = list_runs(r)
        return (rs[0] if rs else no_update)

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

    @app.callback(
        Output("fig-dashboard","figure"),
        Output("fig-discovery","figure"),
        Input("poll","n_intervals"),
        Input("run-dir","value"),
        prevent_initial_call=False
    )
    def update_figs(_n, run_dir):
        if not run_dir:
            return go.Figure(), go.Figure()
        state = getattr(update_figs, "_state", None)
        if state is None or state.run_dir != run_dir:
            state = SeriesState(run_dir)
            setattr(update_figs, "_state", state)
        new_events, esize = tail_jsonl_bytes(state.events_path, state.events_size)
        state.events_size = esize
        for rec in new_events:
            append_event(state, rec)
        new_utd, usize = tail_jsonl_bytes(state.utd_path, state.utd_size)
        state.utd_size = usize
        for rec in new_utd:
            append_say(state, rec)
        MAXP = 2000
        if len(state.t) > MAXP:
            state.t = state.t[-MAXP:]
            state.active = state.active[-MAXP:]
            state.avgw = state.avgw[-MAXP:]
            state.coh = state.coh[-MAXP:]
            state.comp = state.comp[-MAXP:]
            state.b1z = state.b1z[-MAXP:]
            state.val = state.val[-MAXP:]
            state.val2 = state.val2[-MAXP:]
            state.entro = state.entro[-MAXP:]
        if len(state.speak_ticks) > 800:
            state.speak_ticks = state.speak_ticks[-800:]
        t = state.t
        active = ffill(state.active)
        avgw = ffill(state.avgw)
        coh = ffill(state.coh)
        comp = ffill(state.comp)
        b1z = ffill(state.b1z)
        val = ffill(state.val)
        val2 = ffill(state.val2)
        entro = ffill(state.entro)

        # Muted palette
        C = {
            "synapses": "#7aa2c7",
            "avgw": "#9ab8d1",
            "valence": "#c39b70",
            "valence2": "#8bb995",
            "components": "#b68484",
            "cycles": "#a08878",
            "b1z": "#76b0a7",
            "entropy": "#a495c7",
            "speak_line": "rgba(120,180,120,0.45)",
        }

        # fig1
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t, y=active, name="Active synapses", line=dict(width=1, color=C["synapses"])))
        fig1.add_trace(go.Scatter(x=t, y=avgw, name="Avg W", yaxis="y2", line=dict(width=1, color=C["avgw"])))
        if any(v is not None for v in val):
            fig1.add_trace(go.Scatter(x=t, y=val, name="SIE valence", yaxis="y2", line=dict(width=1, dash="dot", color=C["valence"])))
        if any(v is not None for v in val2):
            fig1.add_trace(go.Scatter(x=t, y=val2, name="SIE v2 valence", yaxis="y2", line=dict(width=1, dash="dash", color=C["valence2"])))
        fig1.add_trace(go.Scatter(x=t, y=coh, name="Components", yaxis="y3", line=dict(width=1, color=C["components"])))
        fig1.add_trace(go.Scatter(x=t, y=comp, name="Cycles", yaxis="y4", line=dict(width=1, color=C["cycles"])))
        fig1.add_trace(go.Scatter(x=t, y=b1z, name="B1 z", yaxis="y5", line=dict(width=1, color=C["b1z"])))
        if any(v is not None for v in entro):
            fig1.add_trace(go.Scatter(x=t, y=entro, name="Connectome entropy", yaxis="y6", line=dict(width=1, color=C["entropy"])))
        fig1.update_layout(
            title=f"Dashboard — {os.path.basename(run_dir)}",
            paper_bgcolor="#10151c",
            plot_bgcolor="#0f141a",
            font=dict(color="#cfd7e3"),
            xaxis=dict(domain=[0.05,0.95], title="Tick", gridcolor="#233140", zerolinecolor="#233140"),
            yaxis=dict(title="Active synapses", side="left", gridcolor="#233140", zerolinecolor="#233140"),
            yaxis2=dict(overlaying="y", side="right", title="Avg W / Valence", showgrid=False, zeroline=False),
            yaxis3=dict(overlaying="y", side="left", position=0.02, showticklabels=False, showgrid=False, zeroline=False),
            yaxis4=dict(overlaying="y", side="right", position=0.98, showticklabels=False, showgrid=False, zeroline=False),
            yaxis5=dict(overlaying="y", side="right", position=0.96, showticklabels=False, showgrid=False, zeroline=False),
            yaxis6=dict(overlaying="y", side="left", position=0.04, showticklabels=False, showgrid=False, zeroline=False),
            legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=40,r=20,t=40,b=40),
        )

        # fig2
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=t, y=comp, name="Cycle hits", line=dict(width=1, color=C["cycles"])))
        for tk in state.speak_ticks[-200:]:
            fig2.add_vline(x=tk, line_width=1, line_dash="dash", line_color=C["speak_line"])
        fig2.add_trace(go.Scatter(x=t, y=b1z, name="B1 z", yaxis="y2", line=dict(width=1, color=C["b1z"])))
        fig2.update_layout(
            title="Discovery & Self‑Speak",
            paper_bgcolor="#10151c",
            plot_bgcolor="#0f141a",
            font=dict(color="#cfd7e3"),
            xaxis=dict(title="Tick", gridcolor="#233140", zerolinecolor="#233140"),
            yaxis=dict(title="Cycle hits", gridcolor="#233140", zerolinecolor="#233140"),
            yaxis2=dict(overlaying="y", side="right", title="B1 z", showgrid=False, zeroline=False),
            legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=40,r=20,t=40,b=40),
        )
        return fig1, fig2

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
