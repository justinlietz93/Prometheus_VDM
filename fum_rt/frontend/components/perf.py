from __future__ import annotations

from dash import html, dcc


def perf_card():
    """
    UI Performance card (no env vars required).
    Writes settings into dcc.Store(id="ui-state") via callbacks/perf.register_perf_callbacks.
    """
    return html.Div(
        [
            html.H4("UI Performance"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Allow file I/O (tail JSONL)"),
                            dcc.Checklist(
                                id="ui-file-io",
                                options=[{"label": " On", "value": "on"}],
                                value=["on"],  # default ON, but bounded by caps below
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Tail cap bytes (initial/rotation window)"),
                            dcc.Input(id="ui-tail-cap", type="number", value=1048576, min=1024, step=1024),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Max delta bytes per tick"),
                            dcc.Input(id="ui-tail-delta", type="number", value=65536, min=4096, step=4096),
                        ]
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Max lines parsed per tick"),
                            dcc.Input(id="ui-tail-lines", type="number", value=200, min=10, step=10),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Max points plotted"),
                            dcc.Input(id="ui-maxp", type="number", value=1200, min=100, step=50),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Decimate to N points (0=off)"),
                            dcc.Input(id="ui-decimate", type="number", value=600, min=0, step=50),
                        ]
                    ),
                ],
                className="row",
            ),
            html.Small(
                "These settings apply immediately; no restart or env variables are needed.",
                style={"color": "#8699ac"},
            ),
        ],
        className="card",
    )


__all__ = ["perf_card"]