from __future__ import annotations

from typing import List
from dash import html, dcc


def workspace_card(runs_root: str, runs: List[str], default_run: str):
    """
    Workspace card with runs root controls and run selector.
    IDs preserved to match existing callbacks.
    """
    return html.Div(
        [
            html.H4("Workspace"),
            html.Label("Runs root"),
            dcc.Input(id="runs-root", type="text", value=runs_root, style={"width": "100%"}),
            html.Div(
                [
                    html.Button("Refresh Runs", id="refresh-runs", n_clicks=0),
                    html.Button("Use Current Run", id="use-current-run", n_clicks=0),
                    html.Button("Use Latest Run", id="use-latest-run", n_clicks=0),
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
    )