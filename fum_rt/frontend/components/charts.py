from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
import os


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
        className="fum-tabs small",
        children=[dcc.Tab(label="All", value="all")]
        + [dcc.Tab(label=lbl, value=lbl) for lbl in series_labels],
        style={"minWidth": 0},
        parent_style={"minWidth": 0},
        content_style={"minWidth": 0},
    )

    # Runtime customization: user-provided CSV list of series labels
    custom_row = html.Div(
        [
            dcc.Input(
                id="charts-series-input",
                type="text",
                placeholder="Series CSV (ex: Active synapses, Cycles, Avg W, B1 z, ...)",
                style={"width": "100%"},
            ),
            html.Button("Apply Tabs", id="charts-series-apply", n_clicks=0, className="btn-ok"),
        ],
        style={"display": "grid", "gridTemplateColumns": "1fr auto", "gap": "6px", "minWidth": 0},
    )

    return html.Div(
        [
            series_tabs,
            custom_row,
            dcc.Graph(id="fig-dashboard", figure=go.Figure(), style={"minHeight": "360px", "minWidth": 0}),
        ],
        className="card",
    )