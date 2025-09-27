from __future__ import annotations

"""
File tree row widgets for the File Picker component.

Pure UI builders (no IO, no state). IDs are pattern-matching friendly.
"""

from dash import html

# Truncate helper: preserves extension, uses middle ellipsis
def _truncate_middle(name: str, max_len: int = 48) -> str:
    try:
        s = str(name)
    except Exception:
        return name
    if len(s) <= max_len:
        return s
    # Separate extension (keep dot + ext)
    import os as _os
    base, ext = _os.path.splitext(s)
    # Reserve 1 for ellipsis
    reserve = 1 + len(ext)
    if max_len <= reserve + 2:
        # Extreme constraint fallback
        head_len = max(1, max_len - len(ext) - 1)
        return s[:head_len] + "…" + ext
    remain = max_len - reserve
    left = remain // 2
    right = remain - left
    return base[:left] + "…" + base[-right:] + ext


def dir_row(prefix: str, path: str, name: str, depth: int, expanded: bool, is_selected: bool):
    """
    Build a single directory row with chevron and folder icon.

    Args:
      prefix: file picker instance prefix
      path: absolute directory path this row represents
      name: label to display
      depth: nesting depth for left indent
      expanded: whether the directory is expanded
      is_selected: whether this directory is the currently selected one
    """
    chevron = "▾" if expanded else "▸"
    icon = "📁"
    return html.Div(
        html.Button(
            [
                html.Span(chevron, style={"width": "1em"}),
                html.Span(icon, style={"width": "1.2em"}),
                html.Span(
                    _truncate_middle(name, max_len=48),
                    title=name,
                    style={"overflow": "hidden", "textOverflow": "ellipsis"},
                ),
            ],
            id={"role": f"{prefix}-tree-dir", "path": path},
            n_clicks=0,
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "6px",
                "padding": "4px 6px",
                "borderRadius": "6px",
                "cursor": "pointer",
                "width": "100%",
                "textAlign": "left",
                "background": "rgba(106,160,194,0.18)" if is_selected else "transparent",
                "border": "1px solid var(--border)" if is_selected else "1px solid rgba(35,49,64,0.0)",
                "marginLeft": f"{depth * 12}px",
            },
        )
    )


def file_row(prefix: str, file_path: str, depth: int, selected: bool):
    """
    Build a single file row with bullet and page icon.

    Args:
      prefix: file picker instance prefix
      file_path: absolute file path this row represents
      depth: nesting depth (aligned as child of its directory)
      selected: whether this file is currently selected
    """
    fname = file_path.split("/")[-1]
    display = _truncate_middle(fname, max_len=48)
    return html.Div(
        html.Button(
            [
                html.Span("•", style={"width": "1em", "opacity": 0.7}),
                html.Span("📄", style={"width": "1.2em"}),
                html.Span(display, title=fname, style={"overflow": "hidden", "textOverflow": "ellipsis"}),
            ],
            id={"role": f"{prefix}-file", "path": file_path},
            n_clicks=0,
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "6px",
                "padding": "4px 6px",
                "borderRadius": "6px",
                "cursor": "pointer",
                "width": "100%",
                "textAlign": "left",
                "background": "rgba(106,160,194,0.18)" if selected else "transparent",
                "border": "1px solid var(--border)" if selected else "1px solid rgba(35,49,64,0.0)",
                "marginLeft": f"{(depth + 1) * 12}px",
            },
        )
    )