from __future__ import annotations

"""
Snap-block infrastructure for modular, IDE-like layout.

Provides:
- block_container: grid-based snapping container with consistent gaps and collision-safe isolation/containment.
- block_panel: base panel with a compact header and collision borders; body clips content and enforces minWidth: 0.
- block_panel_tabs: panel variant with an internal tab-strip (dcc.Tabs) for tabbed views.
- file_picker_block: convenience wrapper to render the existing file_picker inside a block_panel (non-invasive).
- graph_tabs_panel: convenience to create a tabbed graph panel with one dcc.Graph per metric (one graph per tab).
- graph_tabs_single_graph_panel: convenience to create a tabbed panel with a single dcc.Graph; tabs filter series.
- set_blocks_debug: enable a global debug outline for all block panels.

This module is opt-in and does not modify any existing widget behavior or layouts.
"""

from typing import Optional, Union, List, Dict, Any
from dash import html, dcc

# Local widget; imported only for the convenience wrapper
from fum_rt.frontend.components.widgets.file_picker import file_picker

# -----------------------------------------------------------------------------
# Global debug outline toggle
# -----------------------------------------------------------------------------
_BLOCKS_DEBUG = False

def set_blocks_debug(enabled: bool = True) -> None:
    """
    Enable/disable a global debug outline for block panels.
    Note: Outline is applied at construction-time; re-render panels to see changes.
    """
    global _BLOCKS_DEBUG
    _BLOCKS_DEBUG = bool(enabled)


# -----------------------------------------------------------------------------
# Container: grid-based snapping
# -----------------------------------------------------------------------------
def block_container(
    children,
    min_col_px: int = 360,
    gap_px: int = 12,
    cols: Optional[int] = None,
    style: Optional[dict] = None,
    className: Optional[str] = None,
) -> html.Div:
    """
    Snap-block container using CSS Grid.

    - Panels flow into columns with consistent gap (no overlap).
    - Use 'cols' to fix the number of columns; otherwise auto-fit by width.
    - Non-invasive: use at page-level to wrap independent panels.
    """
    tpl = (
        f"repeat({cols}, minmax({min_col_px}px, 1fr))"
        if isinstance(cols, int) and cols > 0
        else f"repeat(auto-fit, minmax({min_col_px}px, 1fr))"
    )
    base = {
        "display": "grid",
        "gridTemplateColumns": tpl,
        "gap": f"{gap_px}px",
        "alignItems": "start",
        "justifyItems": "stretch",
        "width": "100%",
        "boxSizing": "border-box",
        # Isolation to keep panels from leaking stacking contexts/z-index
        "isolation": "isolate",
        # Prevent outside layout effects from interfering with measurement
        "contain": "layout paint",
    }
    if style:
        base.update(style)
    return html.Div(children=children, style=base, className=className or "fum-block-container")


# -----------------------------------------------------------------------------
# Base panel: header + collision borders
# -----------------------------------------------------------------------------
def block_panel(
    title: str,
    children,
    icon: Optional[str] = None,
    header_right: Optional[Union[list, html.Div]] = None,
    style: Optional[dict] = None,
    body_style: Optional[dict] = None,
    className: Optional[str] = None,
) -> html.Div:
    """
    Base snap-block panel with header + collision borders.

    - Visual 'collision' via border + subtle outline to show edges.
    - Body is overflow-hidden with minWidth: 0 to avoid content spill.
    - Non-invasive wrapper: place any widget in 'children'.
    """
    panel_style = {
        "position": "relative",
        "background": "var(--panel2)",
        "border": "1px solid var(--border)",
        "borderRadius": "8px",
        # Subtle outer edge to make boundaries obvious (overridden by debug flag)
        "outline": "1px solid rgba(255,255,255,0.06)",
        "boxSizing": "border-box",
        "display": "flex",
        "flexDirection": "column",
        "minWidth": 0,
        "minHeight": 0,
        "overflow": "hidden",
        "contain": "layout paint",
        "isolation": "isolate",
    }
    if _BLOCKS_DEBUG:
        panel_style["outline"] = "1px dashed rgba(255,0,0,0.6)"
    if style:
        panel_style.update(style)

    header_children: List = []
    if icon:
        header_children.append(html.Span(icon, style={"opacity": 0.8, "marginRight": "6px"}))
    header_children.append(html.Span(title, style={"fontWeight": 600}))

    header = html.Div(
        [
            html.Div(header_children, style={"display": "flex", "alignItems": "center", "gap": "6px", "minWidth": 0}),
            html.Div(header_right or [], style={"marginLeft": "auto", "display": "flex", "gap": "8px"}),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
            "padding": "6px 10px",
            "fontSize": "13px",
            "borderBottom": "1px solid var(--border)",
            "background": "var(--panel2)",
            "minWidth": 0,
        },
    )

    body_base = {
        "padding": "8px 10px",
        "minWidth": 0,
        "minHeight": 0,
        "overflow": "hidden",
    }
    if body_style:
        body_base.update(body_style)

    body = html.Div(children=children, style=body_base)

    return html.Div([header, body], style=panel_style, className=className or "fum-block-panel")


# -----------------------------------------------------------------------------
# Tabs panel: header + tab-strip (dcc.Tabs) + tab content (one graph per tab)
# -----------------------------------------------------------------------------
def block_panel_tabs(
    title: str,
    tabs: List[Dict[str, Any]],
    value: Optional[str] = None,
    icon: Optional[str] = None,
    header_right: Optional[Union[list, html.Div]] = None,
    style: Optional[dict] = None,
    tabs_style: Optional[dict] = None,
    content_style: Optional[dict] = None,
    className: Optional[str] = None,
    tabs_id: Optional[str] = None,
) -> html.Div:
    """
    Panel variant with a tab-strip inside the body (no callbacks required).

    Args:
      title: panel header title text
      tabs: list of dicts: {"label": str, "value": str, "content": Component}
      value: optional selected tab value (defaults to first tab)
      icon: optional leading icon text in header
      header_right: optional header-right controls
      style: outer panel style
      tabs_style: style dict applied to dcc.Tabs
      content_style: style dict applied to the tab content wrapper
      className: optional CSS class
      tabs_id: optional id to assign to dcc.Tabs (useful for callbacks)

    Returns:
      html.Div panel with header and dcc.Tabs.
    """
    # Panel chrome (similar to block_panel)
    panel_style = {
        "position": "relative",
        "background": "var(--panel2)",
        "border": "1px solid var(--border)",
        "borderRadius": "8px",
        "outline": "1px solid rgba(255,255,255,0.06)",
        "boxSizing": "border-box",
        "display": "flex",
        "flexDirection": "column",
        "minWidth": 0,
        "minHeight": 0,
        "overflow": "hidden",
        "contain": "layout paint",
        "isolation": "isolate",
    }
    if _BLOCKS_DEBUG:
        panel_style["outline"] = "1px dashed rgba(255,0,0,0.6)"
    if style:
        panel_style.update(style)

    header_children: list = []
    if icon:
        header_children.append(html.Span(icon, style={"opacity": 0.8, "marginRight": "6px"}))
    header_children.append(html.Span(title, style={"fontWeight": 600}))

    header = html.Div(
        [
            html.Div(header_children, style={"display": "flex", "alignItems": "center", "gap": "6px", "minWidth": 0}),
            html.Div(header_right or [], style={"marginLeft": "auto", "display": "flex", "gap": "8px"}),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
            "padding": "6px 10px",
            "fontSize": "13px",
            "borderBottom": "1px solid var(--border)",
            "background": "var(--panel2)",
            "minWidth": 0,
        },
    )

    # Tabs + content: each tab embeds content directly; no callbacks needed
    value_default = value if isinstance(value, str) else (tabs[0]["value"] if tabs else "tab-0")
    tab_children = [
        dcc.Tab(
            label=t.get("label", f"Tab {i+1}"),
            value=t.get("value", f"tab-{i}"),
            children=html.Div(t.get("content"), style={"padding": "8px 10px", **(content_style or {})}),
        )
        for i, t in enumerate(tabs or [])
    ]

    # Build Tabs kwargs without injecting an id=None (Dash disallows id=None)
    _tabs_kwargs = dict(
        value=value_default,
        children=tab_children,
        style={"minWidth": 0, "overflow": "hidden", **(tabs_style or {})},
        parent_style={"minWidth": 0},  # ensure shrinking works inside flex/grid
        content_style={"minWidth": 0, "minHeight": 0, "overflow": "hidden"},
    )
    if isinstance(tabs_id, str) and tabs_id.strip():
        _tabs_kwargs["id"] = tabs_id

    tabs_comp = dcc.Tabs(**_tabs_kwargs)

    body = html.Div(
        children=[tabs_comp],
        style={"minWidth": 0, "minHeight": 0, "overflow": "hidden"},
    )

    return html.Div([header, body], style=panel_style, className=className or "fum-block-panel tabs")


# -----------------------------------------------------------------------------
# Single-graph tabs panel: header + tab-strip + single dcc.Graph (tabs filter series)
# -----------------------------------------------------------------------------
def graph_tabs_single_graph_panel(
    prefix: str,
    title: str,
    metrics: List[str],
    icon: Optional[str] = None,
    header_right: Optional[Union[list, html.Div]] = None,
    style: Optional[dict] = None,
    tabs_style: Optional[dict] = None,
    className: Optional[str] = None,
    include_store: bool = True,
) -> html.Div:
    """
    Tabbed panel with a single Graph; tabs select which series to display.

    Generates:
      - dcc.Tabs(id=f"{prefix}-tabs") with an "All" tab plus one per metric.
      - dcc.Graph(id=f"{prefix}-graph") that should be updated by a callback based on tabs + data.
      - Optional dcc.Store(id=f"{prefix}-data") to hold incoming series data:
            {"series": {"metricA": {"x": [...], "y": [...]}, "metricB": {...}}}

    Use the registrar in callbacks (graph_tabs/single_graph.py) to wire up the figure update.
    """
    # Tabs: "All" + one per metric
    tab_list = [{"label": "All", "value": "all"}] + [{"label": m, "value": m} for m in (metrics or [])]
    tabs = dcc.Tabs(
        id=f"{prefix}-tabs",
        value="all",
        children=[dcc.Tab(label=t["label"], value=t["value"]) for t in tab_list],
        style={"minWidth": 0, "overflow": "hidden", **(tabs_style or {})},
        parent_style={"minWidth": 0},
        content_style={"display": "none"},  # single graph; no per-tab body
    )
    graph = dcc.Graph(id=f"{prefix}-graph", style={"minWidth": 0, "width": "100%"})
    parts = [tabs, graph]
    if include_store:
        parts.insert(0, dcc.Store(id=f"{prefix}-data"))
    body = html.Div(parts, style={"minWidth": 0, "minHeight": 0, "overflow": "hidden"})
    return block_panel(
        title=title,
        children=body,
        icon=icon,
        header_right=header_right,
        style=style,
        className=className,
    )


# -----------------------------------------------------------------------------
# Convenience wrappers
# -----------------------------------------------------------------------------
def file_picker_block(prefix: str, title: str, initial: str = "", width: str = "100%") -> html.Div:
    """
    Optional convenience: wrap the existing file_picker in a BlockPanel.
    This does NOT change the file picker itself, only provides panel chrome.
    """
    return block_panel(title=title, children=file_picker(prefix, title, initial, width))


def graph_tabs_panel(
    prefix: str,
    title: str,
    metrics: List[str],
    icon: Optional[str] = None,
    header_right: Optional[Union[list, html.Div]] = None,
    style: Optional[dict] = None,
    tabs_style: Optional[dict] = None,
    content_style: Optional[dict] = None,
    className: Optional[str] = None,
) -> html.Div:
    """
    Convenience: create a tabbed graph panel with one dcc.Graph per metric.

    Each tab contains a dcc.Graph(id=f"{prefix}-graph-{metric}"). The real-time update
    callbacks in your app can target these IDs to update figures based on the selected metric.
    """
    tabs: List[Dict[str, Any]] = []
    for m in metrics or []:
        graph_id = f"{prefix}-graph-{m}"
        tabs.append(
            {
                "label": m,
                "value": m,
                "content": dcc.Graph(id=graph_id, style={"minWidth": 0}),
            }
        )
    # Default to first metric if any
    default_value = metrics[0] if metrics else None
    return block_panel_tabs(
        title=title,
        tabs=tabs,
        value=default_value,
        icon=icon,
        header_right=header_right,
        style=style,
        tabs_style=tabs_style,
        content_style=content_style,
        className=className,
        tabs_id=f"{prefix}-tabs",
    )


__all__ = [
    "set_blocks_debug",
    "block_container",
    "block_panel",
    "block_panel_tabs",
    "graph_tabs_single_graph_panel",
    "file_picker_block",
    "graph_tabs_panel",
]