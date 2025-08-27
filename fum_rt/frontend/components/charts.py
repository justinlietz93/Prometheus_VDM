from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
import os
from fum_rt.frontend.components.widgets.blocks import block_panel_tabs


def charts_card():
    """
    Charts card — two graphs placed into tabs to preserve existing callbacks and IDs.
    Tabs:
      - Dashboard (fig-dashboard)
      - Discovery (fig-discovery)

    Dashboard tab also includes a series filter (tabs) with one tab per series.
    """
    # Series tabs reflect traces constructed in charts_controller.compute_dashboard_figures
    labels_env = os.getenv("DASH_SERIES_TABS", "")
    if isinstance(labels_env, str) and labels_env.strip():
        series_labels = [s.strip() for s in labels_env.split(",") if s.strip()]
    else:
        series_labels = [
            "Active synapses",
            "Cycles",
            "Avg W",
            "B1 z",
            "Components",
            "SIE valence",
            "SIE v2 valence",
            "Connectome entropy",
        ]
    series_tabs = dcc.Tabs(
        id="charts-series-tabs",
        value="all",
        className="fum-tabs",
        children=[dcc.Tab(label="All", value="all")]
        + [dcc.Tab(label=lbl, value=lbl) for lbl in series_labels],
        style={"minWidth": 0},
        parent_style={"minWidth": 0},
        content_style={"minWidth": 0},
    )

    tabs = [
        {
            "label": "Dashboard",
            "value": "dashboard",
            "content": html.Div(
                [
                    series_tabs,
                    dcc.Graph(
                        id="fig-dashboard",
                        figure=go.Figure(),
                        style={"minHeight": "360px", "minWidth": 0},
                    ),
                ],
                style={"display": "grid", "gap": "8px", "minWidth": 0},
            ),
        },
        {
            "label": "Discovery",
            "value": "discovery",
            "content": dcc.Graph(
                id="fig-discovery",
                figure=go.Figure(),
                style={"minHeight": "300px", "minWidth": 0},
            ),
        },
    ]

    panel = block_panel_tabs(
        title="Charts",
        tabs=tabs,
        value="dashboard",
        tabs_style={"minWidth": 0},
        content_style={"minWidth": 0},
        tabs_id="charts-tabs",
    )
    return html.Div([panel], className="card")