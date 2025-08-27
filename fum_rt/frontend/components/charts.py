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
        children=[dcc.Tab(label="All", value="all", className="fum-tab", selected_className="fum-tab--selected")]
        + [
            dcc.Tab(label=lbl, value=lbl, className="fum-tab", selected_className="fum-tab--selected")
            for lbl in series_labels
        ]
        + [dcc.Tab(label="+", value="__add__", className="fum-tab add", selected_className="fum-tab--selected add")],
        style={"minWidth": 0},
        parent_style={"minWidth": 0},
        content_style={"minWidth": 0},
    )

    # '+' flow handled by callbacks; inline name/create controls appear only when + is selected

    return html.Div(
        [
            # Defaults and custom mappings for series tabs
            dcc.Store(id="charts-series-defaults", data=series_labels),
            dcc.Store(id="charts-series-custom-map", data={}),
            series_tabs,
            # Inline '+' controls (only visible when __add__ is selected)
            # '+' controls removed per UI directive; keep hidden placeholder container for compatibility
            html.Div(
                [],
                id="charts-add-controls",
                style={"display": "none"},
            ),
            # Series picker for custom tabs (visible for non-default tabs)
            html.Div(
                [
                    dcc.Dropdown(
                        id="charts-series-picker",
                        options=[{"label": l, "value": l} for l in series_labels],
                        multi=True,
                        placeholder="Select series for this tab",
                        className="dash-dropdown",
                        style={"minWidth": 0}
                    )
                ],
                id="charts-series-custom-controls",
                style={"display": "none", "minWidth": 0, "gap": "6px"},
            ),
            dcc.Graph(id="fig-dashboard", figure=go.Figure(), style={"minHeight": "360px", "minWidth": 0}),
        ],
        className="card",
    )