from __future__ import annotations

"""
Registrar for single-graph tabbed panels.

Wires up a single dcc.Graph to a tab-strip (dcc.Tabs) produced by
graph_tabs_single_graph_panel(prefix, ...).

Contract:
- The panel creates:
    - dcc.Store(id=f"{prefix}-data") with expected shape:
        {"series": {"metric_name": {"x": [...], "y": [...]}, ...}}
      (x is optional; if missing, range(len(y)) is used.)
    - dcc.Tabs(id=f"{prefix}-tabs")
    - dcc.Graph(id=f"{prefix}-graph")

- This registrar updates the figure when either the tabs value or the data changes.

Usage:
    from fum_rt.frontend.callbacks.graph_tabs.single_graph import register_graph_tabs_single_graph

    register_graph_tabs_single_graph(
        app,
        prefix="rt",
        metrics=["loss", "accuracy", "latency_ms"],
        title="Real-time Metrics",
        yaxis_title="Value",
    )

Notes:
- This callback only formats data already available in the Store. You must populate
  f"{prefix}-data" from your existing data pipeline (interval ticks, web sockets, etc).
"""

from typing import List, Dict, Any, Optional

import dash
from dash import Output, Input, State, no_update
import plotly.graph_objects as go


def _empty_fig(message: str = "No data") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        template=None,
        margin=dict(l=16, r=12, t=28, b=24),
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=True),
        annotations=[
            dict(
                text=message,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=12, color="#9098a0"),
            )
        ],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def register_graph_tabs_single_graph(
    app,
    prefix: str,
    metrics: List[str],
    title: Optional[str] = None,
    yaxis_title: Optional[str] = None,
    template: Optional[str] = None,
) -> None:
    """
    Register a single-graph update callback for a tabbed panel.

    Args:
      app: Dash app
      prefix: id prefix used by graph_tabs_single_graph_panel
      metrics: list of metric keys that may exist in the data store
      title: optional layout title for the figure
      yaxis_title: optional y axis title
      template: optional plotly template name (e.g., "plotly_dark")
    """
    tabs_id = f"{prefix}-tabs"
    data_id = f"{prefix}-data"
    graph_id = f"{prefix}-graph"

    @app.callback(
        Output(graph_id, "figure"),
        Input(tabs_id, "value"),
        Input(data_id, "data"),
        prevent_initial_call=True,
    )
    def _on_update(selected_tab, data):
        try:
            store = data if isinstance(data, dict) else {}
            series_obj: Dict[str, Any] = store.get("series", {}) or {}
        except Exception:
            series_obj = {}

        # Build the figure
        if not series_obj:
            # No data yet
            return _empty_fig()

        fig = go.Figure()

        def _append_trace(mkey: str):
            s = series_obj.get(mkey) or {}
            y = s.get("y")
            if y is None:
                return
            x = s.get("x") or list(range(len(y)))
            fig.add_trace(go.Scatter(x=x, y=y, name=mkey, mode="lines"))

        # If "all" selected, draw all available metrics (in user-declared order where possible)
        if selected_tab in (None, "all"):
            # Keep user-provided order, append any extras we don't know about
            chosen = list(metrics or [])
            for k in series_obj.keys():
                if k not in chosen:
                    chosen.append(k)
            for m in chosen:
                _append_trace(m)
        else:
            # Only the selected metric
            _append_trace(str(selected_tab))

        # Layout
        fig.update_layout(
            template=template,
            title=title,
            margin=dict(l=16, r=12, t=28 if title else 8, b=24),
            xaxis=dict(showgrid=True, zeroline=False),
            yaxis=dict(showgrid=True, zeroline=True, title=yaxis_title),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        # Avoid returning an entirely empty fig if no traces got added for some reason
        if not fig.data:
            return _empty_fig("No series available for selection")
        return fig