from __future__ import annotations

"""
Reusable, themed file-picker component for Dash (no heavy scans, lazy-only).
- Compact display: shows selected basename + a "Choose file" button
- Modal overlay: navigable file tree rooted at a configured directory
- Bounded IO: lists one directory at a time; no recursive scans
- Integrates with existing callbacks via a target component id to receive the chosen path

Usage:
  In a component:
    from fum_rt.frontend.components.widgets.file_picker import file_picker

    # Place the compact picker UI where the dropdown used to be
    file_picker(prefix="feed", title="Select feed file", initial="", width="100%")

  In app initialization:
    from fum_rt.frontend.callbacks.file_picker import register_file_picker_instance
    register_file_picker_instance(
        app,
        prefix="feed",
        root=data_root_abs,
        exts=[".txt", ".jsonl", ".json", ".csv"],
        target_id="feed-path",  # the component id that should receive the chosen path (value property)
    )

IDs produced (all prefixed):
  - {prefix}-open-btn
  - {prefix}-modal (overlay container)
  - {prefix}-root (dcc.Store of absolute root)
  - {prefix}-cwd (dcc.Store of current working dir)
  - {prefix}-exts (dcc.Store of allowed extensions list or [])
  - {prefix}-dirs (dcc.Dropdown listing folders in cwd)
  - {prefix}-files (dcc.Dropdown listing files in cwd)
  - {prefix}-up-btn, {prefix}-root-btn
  - {prefix}-confirm-btn, {prefix}-cancel-btn
  - {prefix}-selected-label (compact label of chosen file)
  - {prefix}-selected-path (dcc.Store holding absolute path)
"""

import os
from dash import html, dcc


def _modal_styles() -> dict:
    # Fixed, full-viewport overlay that is independent of the app layout/grid.
    # Explicit width/height prevent reflow dependencies. No 'contain' or 'isolation'
    # to avoid creating unexpected containing blocks for fixed-position rendering.
    return {
        "position": "fixed",
        "top": 0,
        "right": 0,
        "bottom": 0,
        "left": 0,
        "width": "100vw",
        "height": "100vh",
        "boxSizing": "border-box",
        "backgroundColor": "rgba(10,14,19,0.66)",
        "display": "none",  # toggled by callbacks
        "alignItems": "center",
        "justifyContent": "center",
        "zIndex": 2147483000,  # above react-select menus (9999)
        "pointerEvents": "auto",
        # Prevent body scroll chaining while modal is open; scroll only inside overlay/panel
        "overflow": "auto",
        "overscrollBehavior": "contain",
        "touchAction": "none",
    }


def _panel_styles() -> dict:
    return {
        "position": "relative",
        "backgroundColor": "#0f141a",
        "color": "#cfd7e3",
        "border": "1px solid #233140",
        "borderRadius": "8px",
        "minWidth": "560px",
        "maxWidth": "90vw",
        "maxHeight": "90vh",
        "display": "grid",
        "gridTemplateRows": "auto auto 1fr auto",
        "gap": "8px",
        "padding": "12px",
        "boxShadow": "0 4px 16px rgba(0,0,0,0.4)",
        # Allow internal scrolling so content never spills outside the panel
        "overflow": "auto",
        "zIndex": 2147483001,              # ensure panel stacks above overlay
        "pointerEvents": "auto",           # interactive; background remains inert
        # Keep panel fully isolated from background layout as well
        "contain": "layout paint",
        "overscrollBehavior": "contain",   # prevent body scroll chaining
    }


def _row_styles() -> dict:
    return {"display": "flex", "gap": "8px", "alignItems": "center", "justifyContent": "flex-start"}


def file_picker_overlay(prefix: str, title: str) -> html.Div:
    """
    Top-level modal overlay (portal) for a given file-picker prefix.
    This makes the overlay independent from the layout container.
    """
    return html.Div(
        [
            html.Div(
                [
                    # Title bar
                    html.Div(
                        [
                            html.H4(title, style={"margin": "0", "fontSize": "16px"}),
                            html.Button("×", id=f"{prefix}-cancel-btn", n_clicks=0, title="Close"),
                        ],
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                    ),
                    # Toolbar
                    html.Div(
                        [
                            html.Button("Root", id=f"{prefix}-root-btn", n_clicks=0),
                            html.Button("Up", id=f"{prefix}-up-btn", n_clicks=0),
                            html.Div(id=f"{prefix}-cwd-label", style={"marginLeft": "10px", "opacity": 0.8}),
                        ],
                        style=_row_styles(),
                    ),
                    # Breadcrumbs
                    html.Div(
                        id=f"{prefix}-crumbs",
                        style={"display": "flex", "gap": "6px", "flexWrap": "wrap", "fontSize": "12px", "opacity": 0.9},
                    ),
                    # Body: single explorer (folders + files)
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Explorer"),
                                    html.Div(
                                        id=f"{prefix}-dirs-list",
                                        style={
                                            "border": "1px solid var(--border)",
                                            "borderRadius": "8px",
                                            "background": "var(--panel2)",
                                            "maxHeight": "60vh",
                                            "overflowY": "auto",
                                            "padding": "4px",
                                        },
                                    ),
                                    dcc.Dropdown(
                                        id=f"{prefix}-dirs",
                                        options=[],
                                        placeholder="(no subfolders)",
                                        clearable=False,
                                        style={"display": "none"},
                                    ),
                                    html.Button("Open folder", id=f"{prefix}-open-dir-btn", n_clicks=0, style={"display": "none"}),
                                ],
                                style={"display": "grid", "gap": "6px"},
                            ),
                        ],
                        style={
                            "overflow": "auto",
                            "maxHeight": "60vh",
                        },
                    ),
                    # Action row
                    html.Div(
                        [
                            html.Button("Confirm", id=f"{prefix}-confirm-btn", n_clicks=0, className="btn-ok"),
                            html.Div(id=f"{prefix}-status", style={"marginLeft": "12px", "opacity": 0.8, "fontSize": "12px"}),
                        ],
                        style=_row_styles(),
                    ),
                ],
                style=_panel_styles(),
            )
        ],
        id=f"{prefix}-modal",
        className="fum-modal",
        style=_modal_styles(),
    )


def file_picker(prefix: str, title: str, initial: str = "", width: str = "100%") -> html.Div:
    """
    Build the compact file-picker UI with modal overlay.

    Args:
      prefix: unique prefix for component IDs
      title: title to show in the modal
      initial: initial selected path (optional)
      width: width style for compact strip

    Returns:
      html.Div node
    """
    # Respect the caller-provided width (percent or pixels)
    try:
        w = str(width).strip() if width else "100%"
    except Exception:
        w = "100%"
    return html.Div(
        [
            # Compact strip: responsive filename area + right-aligned button
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                "Selected: ",
                                style={"opacity": 0.8, "fontSize": "13px", "flex": "0 0 auto"},
                            ),
                            html.Span(
                                children=[
                                    html.Span(
                                        (os.path.splitext(os.path.basename(initial))[0] if initial else "(none)"),
                                        style={
                                            "minWidth": 0,
                                            "overflow": "hidden",
                                            "textOverflow": "ellipsis",
                                            "whiteSpace": "nowrap",
                                            "display": "block",
                                            "flex": 1,
                                        },
                                    ),
                                    html.Span(
                                        (os.path.splitext(os.path.basename(initial))[1] if initial else ""),
                                        style={"flex": "0 0 auto"},
                                    ),
                                ],
                                id=f"{prefix}-selected-label",
                                style={
                                    "fontWeight": 500,
                                    "fontSize": "13px",
                                    "display": "flex",
                                    "alignItems": "baseline",
                                    "flex": 1,
                                    "minWidth": 0,
                                    "overflow": "hidden"
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "6px",
                            "flex": 1,
                            "minWidth": 0,
                        },
                    ),
                    html.Button(
                        "Choose file",
                        id=f"{prefix}-open-btn",
                        n_clicks=0,
                        className="btn-ok",
                        style={"marginLeft": "auto", "flex": "0 0 auto"},
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "width": "100%",
                    "gap": "8px",
                    "flexWrap": "nowrap",
                    "justifyContent": "flex-start",
                    "background": "var(--panel2)",
                    "border": "1px solid var(--border)",
                    "borderRadius": "8px",
                    "padding": "6px 8px",
                    "minHeight": "36px",
                    "overflow": "hidden"
                },
            ),
            # Persistent stores for this instance
            dcc.Store(id=f"{prefix}-root"),
            dcc.Store(id=f"{prefix}-cwd"),
            dcc.Store(id=f"{prefix}-exts"),
            dcc.Store(id=f"{prefix}-selected-path", data=initial),
            dcc.Store(id=f"{prefix}-file-sel"),
            dcc.Store(id=f"{prefix}-dir-sel"),
            dcc.Store(id=f"{prefix}-selected-dir"),
            dcc.Store(id=f"{prefix}-tree-store"),
            dcc.Store(id=f"{prefix}-last-action"),
            # Modal overlay moved to top-level portal; see components/layout.py (modals-root)
        ],
        style={
            "width": w,
            "display": "block",
            "boxSizing": "border-box",
            "overflow": "hidden",
        },
    )