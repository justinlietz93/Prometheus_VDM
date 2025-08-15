from __future__ import annotations

from typing import Dict, Any
from dash import html, dcc


def runtime_controls_card(default_profile: Dict[str, Any]):
    """
    Runtime tuning + load-engram controls.
    IDs preserved to match existing callbacks in fum_live.
    """
    return html.Div(
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
                                id="rc-speak-cooldown",
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
                                id="rc-speak-valence",
                                type="number",
                                value=default_profile["speak_valence_thresh"],
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
                                id="rc-prune-factor",
                                type="number",
                                value=default_profile["prune_factor"],
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
                            html.Label("Threshold"),
                            dcc.Input(
                                id="rc-threshold",
                                type="number",
                                value=default_profile.get("threshold", 0.15),
                                step=0.01,
                                min=0,
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Lambda omega"),
                            dcc.Input(
                                id="rc-lambda-omega",
                                type="number",
                                value=default_profile.get("lambda_omega", 0.10),
                                step=0.01,
                                min=0,
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Candidates"),
                            dcc.Input(
                                id="rc-candidates",
                                type="number",
                                value=default_profile.get("candidates", 64),
                                step=1,
                                min=1,
                            ),
                        ]
                    ),
                ],
                className="row tight",
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
    )