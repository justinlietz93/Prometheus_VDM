from __future__ import annotations

from dash import html
from fum_rt.frontend.components.widgets.graph import graph


def charts_card():
    """
    Charts card composed from graph primitives (widgets).
    IDs preserved to match existing callbacks in fum_live.py.
    """
    return html.Div(
        [
            graph("fig-dashboard", height=420),
            graph("fig-discovery", height=320),
        ],
        className="card",
    )