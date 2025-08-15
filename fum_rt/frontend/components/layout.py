from __future__ import annotations

import os
from typing import Any, Dict, List

from dash import html, dcc


def build_layout(
    runs_root: str,
    runs: List[str],
    default_run: str,
    repo_root: str,
    profiles_dir: str,
    default_profile: Dict[str, Any],
    domain_options: List[Dict[str, str]],
    data_files_options: List[Dict[str, str]],
    profile_options: List[Dict[str, str]],
) -> html.Div:
    """
    Construct the full dashboard layout (no callbacks).
    Keeps IDs identical to legacy UI to preserve callback wiring.
    """
    return html.Div(
        [
            html.H3("FUM Live Dashboard (external control)"),
            html.Div(
                [
                    # Left panel
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H4("Workspace"),
                                    html.Label("Runs root"),
                                    dcc.Input(
                                        id="runs-root",
                                        type="text",
                                        value=runs_root,
                                        style={"width": "100%"},
                                    ),
                                    html.Div(
                                        [
                                            html.Button(
                                                "Refresh Runs",
                                                id="refresh-runs",
                                                n_clicks=0,
                                            ),
                                            html.Button(
                                                "Use Current Run",
                                                id="use-current-run",
                                                n_clicks=0,
                                            ),
                                            html.Button(
                                                "Use Latest Run",
                                                id="use-latest-run",
                                                n_clicks=0,
                                            ),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Label("Run directory"),
                                    dcc.Dropdown(
                                        id="run-dir",
                                        options=[{"label": p, "value": p} for p in runs],
                                        value=default_run,
                                    ),
                                ],
                                className="card",
                            ),
                            html.Div(
                                [
                                    html.H4("Runtime Controls"),
                                    html.Label("Phase"),
                                    dcc.Slider(
                                        id="phase",
                                        min=0,
                                        max=4,
                                        step=1,
                                        value=0,
                                        marks={i: str(i) for i in range(5)},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Speak z"),
                                                    dcc.Input(
                                                        id="rc-speak-z",
                                                        type="number",
                                                        value=default_profile["speak_z"],
                                                        step=0.1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hysteresis"),
                                                    dcc.Input(
                                                        id="rc-speak-hysteresis",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_hysteresis"
                                                        ],
                                                        step=0.1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Cooldown (ticks)"),
                                                    dcc.Input(
                                                        id="rc-speak-cooldown",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_cooldown_ticks"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Valence thresh"),
                                                    dcc.Input(
                                                        id="rc-speak-valence",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_valence_thresh"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Walkers"),
                                                    dcc.Input(
                                                        id="rc-walkers",
                                                        type="number",
                                                        value=default_profile["walkers"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hops"),
                                                    dcc.Input(
                                                        id="rc-hops",
                                                        type="number",
                                                        value=default_profile["hops"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Bundle size"),
                                                    dcc.Input(
                                                        id="rc-bundle-size",
                                                        type="number",
                                                        value=default_profile[
                                                            "bundle_size"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Prune factor"),
                                                    dcc.Input(
                                                        id="rc-prune-factor",
                                                        type="number",
                                                        value=default_profile[
                                                            "prune_factor"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Threshold"),
                                            dcc.Input(
                                                id="rc-threshold",
                                                type="number",
                                                value=default_profile.get(
                                                    "threshold", 0.15
                                                ),
                                                step=0.01,
                                                min=0,
                                            ),
                                        ],
                                        className="tight",
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Lambda omega"),
                                            dcc.Input(
                                                id="rc-lambda-omega",
                                                type="number",
                                                value=default_profile.get(
                                                    "lambda_omega", 0.10
                                                ),
                                                step=0.01,
                                                min=0,
                                            ),
                                        ],
                                        className="tight",
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Candidates"),
                                            dcc.Input(
                                                id="rc-candidates",
                                                type="number",
                                                value=default_profile.get(
                                                    "candidates", 64
                                                ),
                                                step=1,
                                                min=1,
                                            ),
                                        ],
                                        className="tight",
                                    ),
                                    html.Div(
                                        [
                                            html.Label("SIE novelty IDF gain"),
                                            dcc.Input(
                                                id="rc-novelty-idf-gain",
                                                type="number",
                                                value=1.0,
                                                step=0.05,
                                                min=0,
                                            ),
                                        ],
                                        className="tight",
                                    ),
                                    html.Div(
                                        [
                                            html.Button(
                                                "Apply Runtime Settings",
                                                id="apply-phase",
                                                n_clicks=0,
                                                className="btn-ok",
                                            )
                                        ],
                                        className="tight",
                                    ),
                                    html.Pre(id="phase-status", style={"fontSize": "12px"}),
                                    html.Label("Load Engram (runtime, into selected Run)"),
                                    dcc.Input(
                                        id="rc-load-engram-input",
                                        type="text",
                                        placeholder="path to .h5/.npz (abs or under runs)",
                                        style={"width": "100%"},
                                    ),
                                    dcc.Dropdown(
                                        id="rc-load-engram-path",
                                        placeholder="select from runs...",
                                        style={"width": "100%", "marginTop": "4px"},
                                    ),
                                    html.Button(
                                        "Load Engram Now",
                                        id="rc-load-engram-btn",
                                        n_clicks=0,
                                        className="tight",
                                    ),
                                ],
                                className="card",
                            ),
                            html.Div(
                                [
                                    html.H4("Feed stdin (optional)"),
                                    dcc.Dropdown(
                                        id="feed-path",
                                        options=data_files_options,
                                        placeholder="select feed file...",
                                        style={"width": "100%"},
                                    ),
                                    dcc.Input(
                                        id="feed-rate",
                                        type="number",
                                        value=20,
                                        step=1,
                                        style={"width": "120px", "marginTop": "6px"},
                                    ),
                                    html.Div(
                                        [
                                            html.Button(
                                                "Start Feed",
                                                id="feed-start",
                                                n_clicks=0,
                                                className="btn-ok",
                                            ),
                                            html.Button(
                                                "Stop Feed",
                                                id="feed-stop",
                                                n_clicks=0,
                                                className="btn-danger",
                                            ),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(id="send-status", style={"fontSize": "12px"}),
                                ],
                                className="card",
                            ),
                        ],
                        style={"minWidth": "320px", "display": "grid", "gap": "16px"},
                    ),
                    # Right panel
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H4("Run configuration & process"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Neurons"),
                                                    dcc.Input(
                                                        id="cfg-neurons",
                                                        type="number",
                                                        value=default_profile["neurons"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("k"),
                                                    dcc.Input(
                                                        id="cfg-k",
                                                        type="number",
                                                        value=default_profile["k"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hz"),
                                                    dcc.Input(
                                                        id="cfg-hz",
                                                        type="number",
                                                        value=default_profile["hz"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Domain"),
                                                    dcc.Dropdown(
                                                        id="cfg-domain",
                                                        options=domain_options,
                                                        value=default_profile[
                                                            "domain"
                                                        ],
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Use time dynamics"),
                                                    dcc.Checklist(
                                                        id="cfg-use-time-dynamics",
                                                        options=[
                                                            {"label": " On", "value": "on"}
                                                        ],
                                                        value=[
                                                            "on"
                                                            if default_profile[
                                                                "use_time_dynamics"
                                                            ]
                                                            else ""
                                                        ]
                                                        if default_profile[
                                                            "use_time_dynamics"
                                                        ]
                                                        else [],
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Sparse mode"),
                                                    dcc.Checklist(
                                                        id="cfg-sparse-mode",
                                                        options=[
                                                            {"label": " On", "value": "on"}
                                                        ],
                                                        value=[
                                                            "on"
                                                            if default_profile[
                                                                "sparse_mode"
                                                            ]
                                                            else ""
                                                        ]
                                                        if default_profile["sparse_mode"]
                                                        else [],
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Structure & traversal"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Threshold"),
                                                    dcc.Input(
                                                        id="cfg-threshold",
                                                        type="number",
                                                        value=default_profile[
                                                            "threshold"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Lambda omega"),
                                                    dcc.Input(
                                                        id="cfg-lambda-omega",
                                                        type="number",
                                                        value=default_profile[
                                                            "lambda_omega"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Candidates"),
                                                    dcc.Input(
                                                        id="cfg-candidates",
                                                        type="number",
                                                        value=default_profile[
                                                            "candidates"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Walkers"),
                                                    dcc.Input(
                                                        id="cfg-walkers",
                                                        type="number",
                                                        value=default_profile[
                                                            "walkers"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hops"),
                                                    dcc.Input(
                                                        id="cfg-hops",
                                                        type="number",
                                                        value=default_profile["hops"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Bundle size"),
                                                    dcc.Input(
                                                        id="cfg-bundle-size",
                                                        type="number",
                                                        value=default_profile[
                                                            "bundle_size"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Prune factor"),
                                                    dcc.Input(
                                                        id="cfg-prune-factor",
                                                        type="number",
                                                        value=default_profile[
                                                            "prune_factor"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Status interval"),
                                                    dcc.Input(
                                                        id="cfg-status-interval",
                                                        type="number",
                                                        value=default_profile[
                                                            "status_interval"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Stimulus"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Group size"),
                                                    dcc.Input(
                                                        id="cfg-stim-group-size",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_group_size"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Amp"),
                                                    dcc.Input(
                                                        id="cfg-stim-amp",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_amp"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Decay"),
                                                    dcc.Input(
                                                        id="cfg-stim-decay",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_decay"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Max symbols"),
                                                    dcc.Input(
                                                        id="cfg-stim-max-symbols",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_max_symbols"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Speak / B1 spike detector"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Speak auto"),
                                                    dcc.Checklist(
                                                        id="cfg-speak-auto",
                                                        options=[
                                                            {"label": " On", "value": "on"}
                                                        ],
                                                        value=[
                                                            "on"
                                                            if default_profile[
                                                                "speak_auto"
                                                            ]
                                                            else ""
                                                        ]
                                                        if default_profile["speak_auto"]
                                                        else [],
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Speak z"),
                                                    dcc.Input(
                                                        id="cfg-speak-z",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_z"
                                                        ],
                                                        step=0.1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hysteresis"),
                                                    dcc.Input(
                                                        id="cfg-speak-hysteresis",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_hysteresis"
                                                        ],
                                                        step=0.1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Cooldown (ticks)"),
                                                    dcc.Input(
                                                        id="cfg-speak-cooldown-ticks",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_cooldown_ticks"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Valence thresh"),
                                                    dcc.Input(
                                                        id="cfg-speak-valence-thresh",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_valence_thresh"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("B1 half-life (ticks)"),
                                                    dcc.Input(
                                                        id="cfg-b1-half-life-ticks",
                                                        type="number",
                                                        value=default_profile[
                                                            "b1_half_life_ticks"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Viz / Logs / Checkpoints"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("viz_every"),
                                                    dcc.Input(
                                                        id="cfg-viz-every",
                                                        type="number",
                                                        value=default_profile[
                                                            "viz_every"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("log_every"),
                                                    dcc.Input(
                                                        id="cfg-log-every",
                                                        type="number",
                                                        value=default_profile[
                                                            "log_every"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("checkpoint_every"),
                                                    dcc.Input(
                                                        id="cfg-checkpoint-every",
                                                        type="number",
                                                        value=default_profile[
                                                            "checkpoint_every"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("checkpoint_keep"),
                                                    dcc.Input(
                                                        id="cfg-checkpoint-keep",
                                                        type="number",
                                                        value=default_profile[
                                                            "checkpoint_keep"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("duration (s)"),
                                                    dcc.Input(
                                                        id="cfg-duration",
                                                        type="number",
                                                        value=default_profile[
                                                            "duration"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Div(
                                        [
                                            dcc.Input(
                                                id="profile-name",
                                                type="text",
                                                placeholder="profile name",
                                                style={"width": "200px"},
                                            ),
                                            html.Button(
                                                "Save Profile", id="save-profile", n_clicks=0
                                            ),
                                            dcc.Dropdown(
                                                id="profile-path",
                                                options=profile_options,
                                                placeholder="load profile",
                                                style={"width": "50%"},
                                            ),
                                            html.Button("Load", id="load-profile", n_clicks=0),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(
                                        id="profile-save-status",
                                        style={"fontSize": "12px", "whiteSpace": "pre-wrap"},
                                    ),
                                    html.Div(
                                        [
                                            html.Button(
                                                "Start New Run",
                                                id="start-run",
                                                n_clicks=0,
                                                className="btn-ok",
                                            ),
                                            html.Button(
                                                "Resume Selected Run",
                                                id="resume-run",
                                                n_clicks=0,
                                            ),
                                            html.Button(
                                                "Stop Managed Run",
                                                id="stop-run",
                                                n_clicks=0,
                                                className="btn-danger",
                                            ),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(
                                        id="proc-status",
                                        style={"fontSize": "12px", "whiteSpace": "pre-wrap"},
                                    ),
                                    html.Button("Show Launcher Log", id="show-log", n_clicks=0),
                                    html.Pre(
                                        id="launch-log",
                                        style={
                                            "fontSize": "12px",
                                            "maxHeight": "240px",
                                            "overflowY": "auto",
                                        },
                                    ),
                                ],
                                className="card",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id="fig-dashboard",
                                        style={"height": "420px", "width": "100%"},
                                    ),
                                    dcc.Graph(
                                        id="fig-discovery",
                                        style={"height": "320px", "width": "100%"},
                                    ),
                                ],
                                className="card",
                            ),
                            html.Div(
                                [
                                    html.H4("Chat"),
                                    html.Pre(
                                        id="chat-view",
                                        style={
                                            "height": "220px",
                                            "overflowY": "auto",
                                            "overflowX": "hidden",
                                            "backgroundColor": "#0f141a",
                                            "color": "#e0e6ee",
                                            "padding": "8px",
                                            "whiteSpace": "pre-wrap",
                                            "wordBreak": "break-word",
                                            "overflowWrap": "anywhere",
                                            "hyphens": "none",
                                            "border": "1px solid #1d2733",
                                            "borderRadius": "8px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Chat filter"),
                                            dcc.RadioItems(
                                                id="chat-filter",
                                                options=[
                                                    {"label": "All Outputs", "value": "all"},
                                                    {"label": "'say' Macro Only", "value": "say"},
                                                    {
                                                        "label": "Self-Speak (Spike-Gated)",
                                                        "value": "spike",
                                                    },
                                                ],
                                                value="all",
                                                labelStyle={
                                                    "display": "inline-block",
                                                    "marginRight": "10px",
                                                },
                                            ),
                                        ],
                                        className="tight",
                                    ),
                                    html.Div(
                                        [
                                            dcc.Input(
                                                id="chat-input",
                                                type="text",
                                                placeholder="Type a message and click Send",
                                                style={"width": "80%"},
                                            ),
                                            html.Button("Send", id="chat-send", n_clicks=0),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(id="chat-status", style={"fontSize": "12px"}),
                                ],
                                className="card",
                            ),
                        ],
                        style={"minWidth": "400px", "display": "grid", "gap": "16px"},
                    ),
                ],
                className="grid",
            ),
            dcc.Interval(id="poll", interval=1500, n_intervals=0),
            dcc.Store(id="chat-state"),
            dcc.Store(id="ui-state"),
        ],
        style={"padding": "10px"},
    )                                                        ],
                                                        value=[
                                                            "on"
                                                            if default_profile[
                                                                "use_time_dynamics"
                                                            ]
                                                            else ""
                                                        ]
                                                        if default_profile[
                                                            "use_time_dynamics"
                                                        ]
                                                        else [],
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Sparse mode"),
                                                    dcc.Checklist(
                                                        id="cfg-sparse-mode",
                                                        options=[
                                                            {"label": " On", "value": "on"}
                                                        ],
                                                        value=[
                                                            "on"
                                                            if default_profile[
                                                                "sparse_mode"
                                                            ]
                                                            else ""
                                                        ]
                                                        if default_profile["sparse_mode"]
                                                        else [],
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Structure & traversal"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Threshold"),
                                                    dcc.Input(
                                                        id="cfg-threshold",
                                                        type="number",
                                                        value=default_profile[
                                                            "threshold"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Lambda omega"),
                                                    dcc.Input(
                                                        id="cfg-lambda-omega",
                                                        type="number",
                                                        value=default_profile[
                                                            "lambda_omega"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Candidates"),
                                                    dcc.Input(
                                                        id="cfg-candidates",
                                                        type="number",
                                                        value=default_profile[
                                                            "candidates"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Walkers"),
                                                    dcc.Input(
                                                        id="cfg-walkers",
                                                        type="number",
                                                        value=default_profile[
                                                            "walkers"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hops"),
                                                    dcc.Input(
                                                        id="cfg-hops",
                                                        type="number",
                                                        value=default_profile["hops"],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Bundle size"),
                                                    dcc.Input(
                                                        id="cfg-bundle-size",
                                                        type="number",
                                                        value=default_profile[
                                                            "bundle_size"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Prune factor"),
                                                    dcc.Input(
                                                        id="cfg-prune-factor",
                                                        type="number",
                                                        value=default_profile[
                                                            "prune_factor"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Status interval"),
                                                    dcc.Input(
                                                        id="cfg-status-interval",
                                                        type="number",
                                                        value=default_profile[
                                                            "status_interval"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Stimulus"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Group size"),
                                                    dcc.Input(
                                                        id="cfg-stim-group-size",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_group_size"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Amp"),
                                                    dcc.Input(
                                                        id="cfg-stim-amp",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_amp"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Decay"),
                                                    dcc.Input(
                                                        id="cfg-stim-decay",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_decay"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Max symbols"),
                                                    dcc.Input(
                                                        id="cfg-stim-max-symbols",
                                                        type="number",
                                                        value=default_profile[
                                                            "stim_max_symbols"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Speak / B1 spike detector"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("Speak auto"),
                                                    dcc.Checklist(
                                                        id="cfg-speak-auto",
                                                        options=[
                                                            {"label": " On", "value": "on"}
                                                        ],
                                                        value=[
                                                            "on"
                                                            if default_profile[
                                                                "speak_auto"
                                                            ]
                                                            else ""
                                                        ]
                                                        if default_profile["speak_auto"]
                                                        else [],
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Speak z"),
                                                    dcc.Input(
                                                        id="cfg-speak-z",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_z"
                                                        ],
                                                        step=0.1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Hysteresis"),
                                                    dcc.Input(
                                                        id="cfg-speak-hysteresis",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_hysteresis"
                                                        ],
                                                        step=0.1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Cooldown (ticks)"),
                                                    dcc.Input(
                                                        id="cfg-speak-cooldown-ticks",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_cooldown_ticks"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("Valence thresh"),
                                                    dcc.Input(
                                                        id="cfg-speak-valence-thresh",
                                                        type="number",
                                                        value=default_profile[
                                                            "speak_valence_thresh"
                                                        ],
                                                        step=0.01,
                                                        min=0,
                                                        max=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("B1 half-life (ticks)"),
                                                    dcc.Input(
                                                        id="cfg-b1-half-life-ticks",
                                                        type="number",
                                                        value=default_profile[
                                                            "b1_half_life_ticks"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Label("Viz / Logs / Checkpoints"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Label("viz_every"),
                                                    dcc.Input(
                                                        id="cfg-viz-every",
                                                        type="number",
                                                        value=default_profile[
                                                            "viz_every"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("log_every"),
                                                    dcc.Input(
                                                        id="cfg-log-every",
                                                        type="number",
                                                        value=default_profile[
                                                            "log_every"
                                                        ],
                                                        step=1,
                                                        min=1,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("checkpoint_every"),
                                                    dcc.Input(
                                                        id="cfg-checkpoint-every",
                                                        type="number",
                                                        value=default_profile[
                                                            "checkpoint_every"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("checkpoint_keep"),
                                                    dcc.Input(
                                                        id="cfg-checkpoint-keep",
                                                        type="number",
                                                        value=default_profile[
                                                            "checkpoint_keep"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Label("duration (s)"),
                                                    dcc.Input(
                                                        id="cfg-duration",
                                                        type="number",
                                                        value=default_profile[
                                                            "duration"
                                                        ],
                                                        step=1,
                                                        min=0,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="row",
                                    ),
                                    html.Div(
                                        [
                                            dcc.Input(
                                                id="profile-name",
                                                type="text",
                                                placeholder="profile name",
                                                style={"width": "200px"},
                                            ),
                                            html.Button(
                                                "Save Profile", id="save-profile", n_clicks=0
                                            ),
                                            dcc.Dropdown(
                                                id="profile-path",
                                                options=profile_options,
                                                placeholder="load profile",
                                                style={"width": "50%"},
                                            ),
                                            html.Button("Load", id="load-profile", n_clicks=0),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(
                                        id="profile-save-status",
                                        style={"fontSize": "12px", "whiteSpace": "pre-wrap"},
                                    ),
                                    html.Div(
                                        [
                                            html.Button(
                                                "Start New Run",
                                                id="start-run",
                                                n_clicks=0,
                                                className="btn-ok",
                                            ),
                                            html.Button(
                                                "Resume Selected Run",
                                                id="resume-run",
                                                n_clicks=0,
                                            ),
                                            html.Button(
                                                "Stop Managed Run",
                                                id="stop-run",
                                                n_clicks=0,
                                                className="btn-danger",
                                            ),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(
                                        id="proc-status",
                                        style={"fontSize": "12px", "whiteSpace": "pre-wrap"},
                                    ),
                                    html.Button("Show Launcher Log", id="show-log", n_clicks=0),
                                    html.Pre(
                                        id="launch-log",
                                        style={
                                            "fontSize": "12px",
                                            "maxHeight": "240px",
                                            "overflowY": "auto",
                                        },
                                    ),
                                ],
                                className="card",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id="fig-dashboard",
                                        style={"height": "420px", "width": "100%"},
                                    ),
                                    dcc.Graph(
                                        id="fig-discovery",
                                        style={"height": "320px", "width": "100%"},
                                    ),
                                ],
                                className="card",
                            ),
                            html.Div(
                                [
                                    html.H4("Chat"),
                                    html.Pre(
                                        id="chat-view",
                                        style={
                                            "height": "220px",
                                            "overflowY": "auto",
                                            "overflowX": "hidden",
                                            "backgroundColor": "#0f141a",
                                            "color": "#e0e6ee",
                                            "padding": "8px",
                                            "whiteSpace": "pre-wrap",
                                            "wordBreak": "break-word",
                                            "overflowWrap": "anywhere",
                                            "hyphens": "none",
                                            "border": "1px solid #1d2733",
                                            "borderRadius": "8px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Label("Chat filter"),
                                            dcc.RadioItems(
                                                id="chat-filter",
                                                options=[
                                                    {"label": "All Outputs", "value": "all"},
                                                    {"label": "'say' Macro Only", "value": "say"},
                                                    {
                                                        "label": "Self-Speak (Spike-Gated)",
                                                        "value": "spike",
                                                    },
                                                ],
                                                value="all",
                                                labelStyle={
                                                    "display": "inline-block",
                                                    "marginRight": "10px",
                                                },
                                            ),
                                        ],
                                        className="tight",
                                    ),
                                    html.Div(
                                        [
                                            dcc.Input(
                                                id="chat-input",
                                                type="text",
                                                placeholder="Type a message and click Send",
                                                style={"width": "80%"},
                                            ),
                                            html.Button("Send", id="chat-send", n_clicks=0),
                                        ],
                                        className="row tight",
                                    ),
                                    html.Pre(id="chat-status", style={"fontSize": "12px"}),
                                ],
                                className="card",
                            ),
                        ],
                        style={"minWidth": "400px", "display": "grid", "gap": "16px"},
                    ),
                ],
                className="grid",
            ),
            dcc.Interval(id="poll", interval=1500, n_intervals=0),
            dcc.Store(id="chat-state"),
            dcc.Store(id="ui-state"),
        ],
        style={"padding": "10px"},
    )
