from __future__ import annotations

from typing import List, Dict
from dash import html, dcc


def feed_card(data_files_options: List[Dict[str, str]]):
    """
    Feed stdin (optional) card.
    IDs preserved to match existing callbacks.
    """
    return html.Div(
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
                    html.Button("Start Feed", id="feed-start", n_clicks=0, className="btn-ok"),
                    html.Button("Stop Feed", id="feed-stop", n_clicks=0, className="btn-danger"),
                ],
                className="row tight",
            ),
            html.Pre(id="send-status", style={"fontSize": "12px"}),
        ],
        className="card",
    )