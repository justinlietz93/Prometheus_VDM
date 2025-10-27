"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from dash import html, dcc


def perf_card():
    """
    UI Performance card (no environment variables required).
    Publishes settings into dcc.Store(id="ui-state") via callbacks/perf.register_perf_callbacks.
    """
    return html.Div(
        [
            html.H4("UI Performance"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Charts: HTTP snapshot only"),
                            dcc.Checklist(
                                id="ui-charts-http",
                                options=[{"label": " On", "value": "on"}],
                                value=[],  # default OFF - falls back to bounded file tails if HTTP not ready
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Update interval (ms)"),
                            dcc.Input(id="ui-update-ms", type="number", value=800, min=250, step=50),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Points per series cap"),
                            dcc.Input(id="ui-points-cap", type="number", value=1200, min=100, step=50),
                        ]
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Series count cap"),
                            dcc.Input(id="ui-series-cap", type="number", value=6, min=1, step=1),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Status URL"),
                            dcc.Input(
                                id="ui-status-url",
                                type="text",
                                value="http://127.0.0.1:8787/status/snapshot",
                                style={"width": "100%"},
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Status timeout (s)"),
                            dcc.Input(id="ui-status-timeout", type="number", value=0.2, min=0.05, step=0.05),
                        ]
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Tail Chat file"),
                            dcc.Checklist(id="ui-tail-chat", options=[{"label": " On", "value": "on"}], value=[]),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Tail Launcher log"),
                            dcc.Checklist(id="ui-tail-launch", options=[{"label": " On", "value": "on"}], value=[]),
                        ]
                    ),
                ],
                className="row",
            ),
            html.Small(
                "Settings apply immediately; no env vars or restart required.",
                style={"color": "#8699ac"},
            ),
        ],
        className="card",
    )


__all__ = ["perf_card"]