"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from dash import html, dcc


def chat_card():
    """
    Chat panel with log view, filter, input, and send button.
    IDs preserved to match existing callbacks in fum_live.py.
    """
    return html.Div(
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
                            {"label": "Self-Speak (Spike-Gated)", "value": "spike"},
                        ],
                        value="all",
                        labelStyle={"display": "inline-block", "marginRight": "10px"},
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
    )