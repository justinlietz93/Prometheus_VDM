from __future__ import annotations

"""
Run Config modular sections.

Purpose:
- Break the large run_config_card into readable, maintainable sections
- Preserve ALL existing element IDs to avoid breaking callbacks
- No new callbacks introduced; purely structural/UX refactor

Sections:
- Core (neurons, k, hz, domain)
- Modes (use_time_dynamics, sparse_mode)
- Structure & Traversal (threshold, lambda_omega, candidates, walkers, hops, bundle_size, prune_factor, status_interval)
- Stimulus (stim_* fields)
- Speak / B1 (speak_* and b1_* fields)
- Viz / Logs / Checkpoints
- Profile I/O (profile-name, save/load, file picker + status)
- Process Actions (start/resume/stop + status + log)

Author: Justin K. Lietz
"""

from typing import Dict, Any, List
from dash import html, dcc

from fum_rt.frontend.components.widgets.file_picker import file_picker


def _num(id_: str, label: str, value: Any, step: float | int, min: Any | None = None, max: Any | None = None) -> html.Div:
    """Consistent number input with label. ID preserved."""
    return html.Div(
        [
            html.Label(label),
            dcc.Input(id=id_, type="number", value=value, step=step, min=min, max=max),
        ]
    )


def _toggle(id_: str, label: str, on: bool) -> html.Div:
    """Consistent On/Off checklist with label. ID preserved."""
    return html.Div(
        [
            html.Label(label),
            dcc.Checklist(id=id_, options=[{"label": " On", "value": "on"}], value=["on"] if on else []),
        ]
    )


def section_core_params(default_profile: Dict[str, Any], domain_options: List[Dict[str, str]]) -> html.Div:
    return html.Div(
        [
            html.H5("Core", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    _num("cfg-neurons", "Neurons", default_profile["neurons"], step=1, min=1),
                    _num("cfg-k", "k", default_profile["k"], step=1, min=1),
                    _num("cfg-hz", "Hz", default_profile["hz"], step=1, min=1),
                    html.Div(
                        [
                            html.Label("Domain"),
                            dcc.Dropdown(id="cfg-domain", options=domain_options, value=default_profile["domain"]),
                        ]
                    ),
                ],
                className="row",
            ),
        ],
        className="section",
    )


def section_modes(default_profile: Dict[str, Any]) -> html.Div:
    return html.Div(
        [
            html.H5("Modes", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    _toggle("cfg-use-time-dynamics", "Use time dynamics", bool(default_profile["use_time_dynamics"])),
                    _toggle("cfg-sparse-mode", "Sparse mode", bool(default_profile["sparse_mode"])),
                ],
                className="row",
            ),
        ],
        className="section",
    )


def section_structure_traversal(default_profile: Dict[str, Any]) -> html.Div:
    return html.Div(
        [
            html.H5("Structure & traversal", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    _num("cfg-threshold", "Threshold", default_profile["threshold"], step=0.01, min=0),
                    _num("cfg-lambda-omega", "Lambda omega", default_profile["lambda_omega"], step=0.01, min=0),
                    _num("cfg-candidates", "Candidates", default_profile["candidates"], step=1, min=1),
                    _num("cfg-walkers", "Walkers", default_profile["walkers"], step=1, min=1),
                    _num("cfg-hops", "Hops", default_profile["hops"], step=1, min=1),
                    _num("cfg-bundle-size", "Bundle size", default_profile["bundle_size"], step=1, min=1),
                    _num("cfg-prune-factor", "Prune factor", default_profile["prune_factor"], step=0.01, min=0, max=1),
                    _num("cfg-status-interval", "Status interval", default_profile["status_interval"], step=1, min=1),
                ],
                className="row",
            ),
        ],
        className="section",
    )


def section_stimulus(default_profile: Dict[str, Any]) -> html.Div:
    return html.Div(
        [
            html.H5("Stimulus", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    _num("cfg-stim-group-size", "Group size", default_profile["stim_group_size"], step=1, min=1),
                    _num("cfg-stim-amp", "Amp", default_profile["stim_amp"], step=0.01, min=0),
                    _num("cfg-stim-decay", "Decay", default_profile["stim_decay"], step=0.01, min=0, max=1),
                    _num("cfg-stim-max-symbols", "Max symbols", default_profile["stim_max_symbols"], step=1, min=1),
                ],
                className="row",
            ),
        ],
        className="section",
    )


def section_speak_b1(default_profile: Dict[str, Any]) -> html.Div:
    return html.Div(
        [
            html.H5("Speak / B1 spike detector", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    _toggle("cfg-speak-auto", "Speak auto", bool(default_profile["speak_auto"])),
                    _num("cfg-speak-z", "Speak z", default_profile["speak_z"], step=0.1, min=0),
                    _num("cfg-speak-hysteresis", "Hysteresis", default_profile["speak_hysteresis"], step=0.1, min=0),
                    _num("cfg-speak-cooldown-ticks", "Cooldown (ticks)", default_profile["speak_cooldown_ticks"], step=1, min=1),
                    _num("cfg-speak-valence-thresh", "Valence thresh", default_profile["speak_valence_thresh"], step=0.01, min=0, max=1),
                    _num("cfg-b1-half-life-ticks", "B1 half-life (ticks)", default_profile["b1_half_life_ticks"], step=1, min=1),
                ],
                className="row",
            ),
        ],
        className="section",
    )


def section_viz_logs_checkpoints(default_profile: Dict[str, Any]) -> html.Div:
    return html.Div(
        [
            html.H5("Viz / Logs / Checkpoints", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    _num("cfg-viz-every", "viz_every", default_profile["viz_every"], step=1, min=0),
                    _num("cfg-log-every", "log_every", default_profile["log_every"], step=1, min=1),
                    _num("cfg-checkpoint-every", "checkpoint_every", default_profile["checkpoint_every"], step=1, min=0),
                    _num("cfg-checkpoint-keep", "checkpoint_keep", default_profile["checkpoint_keep"], step=1, min=0),
                    _num("cfg-duration", "duration (s)", default_profile["duration"], step=1, min=0),
                ],
                className="row",
            ),
        ],
        className="section",
    )


def section_profile_io(profile_options: List[Dict[str, str]]) -> html.Div:
    """Save/Load profile, with file picker; includes profile-save-status."""
    return html.Div(
        [
            html.H5("Profile I/O", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    dcc.Input(id="profile-name", type="text", placeholder="profile name", style={"width": "200px"}),
                    html.Button("Save Profile", id="save-profile", n_clicks=0),
                    file_picker(prefix="profile-file", title="Select profile (.json)", initial="", width="50%"),
                    dcc.Dropdown(
                        id="profile-path",
                        options=profile_options,
                        placeholder="load profile",
                        style={"width": "50%", "display": "none"},
                    ),
                    html.Button("Load", id="load-profile", n_clicks=0),
                ],
                className="row tight",
            ),
            html.Pre(id="profile-save-status", style={"fontSize": "12px", "whiteSpace": "pre-wrap"}),
        ],
        className="section",
    )


def section_process_actions() -> html.Div:
    """Start/Resume/Stop + proc-status + launcher log."""
    return html.Div(
        [
            html.H5("Process actions", style={"margin": "6px 0 4px 0", "opacity": 0.9}),
            html.Div(
                [
                    html.Button("Start New Run", id="start-run", n_clicks=0, className="btn-ok"),
                    html.Button("Resume Selected Run", id="resume-run", n_clicks=0),
                    html.Button("Stop Managed Run", id="stop-run", n_clicks=0, className="btn-danger"),
                ],
                className="row tight",
            ),
            html.Pre(id="proc-status", style={"fontSize": "12px", "whiteSpace": "pre-wrap"}),
            html.Button("Show Launcher Log", id="show-log", n_clicks=0),
            html.Pre(id="launch-log", style={"fontSize": "12px", "maxHeight": "240px", "overflowY": "auto"}),
        ],
        className="section",
    )