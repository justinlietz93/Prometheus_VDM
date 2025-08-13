from __future__ import annotations

from typing import Dict, Any, List
from dash import html, dcc


def run_config_card(
    default_profile: Dict[str, Any],
    domain_options: List[Dict[str, str]],
    profile_options: List[Dict[str, str]],
):
    """
    Run configuration & process card.
    IDs preserved to match existing callbacks in fum_live.py.
    """
    return html.Div(
        [
            html.H4("Run configuration & process"),
            # Core
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
                                value=default_profile["domain"],
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
                                options=[{"label": " On", "value": "on"}],
                                value=["on"] if default_profile["use_time_dynamics"] else [],
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Sparse mode"),
                            dcc.Checklist(
                                id="cfg-sparse-mode",
                                options=[{"label": " On", "value": "on"}],
                                value=["on"] if default_profile["sparse_mode"] else [],
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
                                value=default_profile["threshold"],
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
                                value=default_profile["lambda_omega"],
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
                                value=default_profile["candidates"],
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
                                value=default_profile["bundle_size"],
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
                                value=default_profile["prune_factor"],
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
                                value=default_profile["status_interval"],
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
                                value=default_profile["stim_group_size"],
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
                                value=default_profile["stim_amp"],
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
                                value=default_profile["stim_decay"],
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
                                value=default_profile["stim_max_symbols"],
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
                                options=[{"label": " On", "value": "on"}],
                                value=["on"] if default_profile["speak_auto"] else [],
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Speak z"),
                            dcc.Input(
                                id="cfg-speak-z",
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
                                id="cfg-speak-hysteresis",
                                type="number",
                                value=default_profile["speak_hysteresis"],
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
                                value=default_profile["speak_cooldown_ticks"],
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
                                value=default_profile["speak_valence_thresh"],
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
                                value=default_profile["b1_half_life_ticks"],
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
                                value=default_profile["viz_every"],
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
                                value=default_profile["log_every"],
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
                                value=default_profile["checkpoint_every"],
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
                                value=default_profile["checkpoint_keep"],
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
                                value=default_profile["duration"],
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
                    html.Button("Save Profile", id="save-profile", n_clicks=0),
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
                        "Start New Run", id="start-run", n_clicks=0, className="btn-ok"
                    ),
                    html.Button("Resume Selected Run", id="resume-run", n_clicks=0),
                    html.Button(
                        "Stop Managed Run", id="stop-run", n_clicks=0, className="btn-danger"
                    ),
                ],
                className="row tight",
            ),
            html.Pre(id="proc-status", style={"fontSize": "12px", "whiteSpace": "pre-wrap"}),
            html.Button("Show Launcher Log", id="show-log", n_clicks=0),
            html.Pre(
                id="launch-log",
                style={"fontSize": "12px", "maxHeight": "240px", "overflowY": "auto"},
            ),
        ],
        className="card",
    )