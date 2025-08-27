from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
from fum_rt.frontend.components.widgets.blocks import block_panel_tabs


def charts_card():
    """
    Charts card — two graphs placed into tabs to preserve existing callbacks and IDs.
    Tabs:
      - Dashboard (fig-dashboard)
      - Discovery (fig-discovery)
    """
    tabs = [
        {
            "label": "Dashboard",
            "value": "dashboard",
            "content": dcc.Graph(
                id="fig-dashboard",
                figure=go.Figure(),
                style={"minHeight": "360px", "minWidth": 0},
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
    )
    return html.Div([panel], className="card")