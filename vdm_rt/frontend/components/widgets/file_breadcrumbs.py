"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Breadcrumbs widget for the File Picker component.

Pure UI builder. No IO, no state. Pattern-matching friendly IDs.
"""

from dash import html


def breadcrumbs(prefix: str, base: str | None, selected: str | None):
    """
    Build breadcrumbs from base (root) to selected directory.

    Args:
      prefix: file picker instance prefix
      base: absolute root directory
      selected: absolute selected directory (within base)
    """
    try:
        base = (base or "").strip()
        selected = (selected or "").strip()
        if not base:
            return []
        root_label = base.rstrip("/").split("/")[-1] or base
        out = [
            html.Button(
                root_label,
                id={"role": f"{prefix}-crumb", "path": base},
                n_clicks=0,
                style={"background": "transparent", "border": "none", "color": "#9ab8d1", "cursor": "pointer", "padding": "2px 4px"},
            )
        ]
        if selected and selected != base:
            # Render each path segment from base -> selected
            rel = selected[len(base) + 1 :] if selected.startswith(base + "/") else selected
            for part in [p for p in rel.split("/") if p]:
                base = f"{base}/{part}"
                out.append(html.Span("›", style={"opacity": 0.6, "padding": "0 2px"}))
                out.append(
                    html.Button(
                        part,
                        id={"role": f"{prefix}-crumb", "path": base},
                        n_clicks=0,
                        style={"background": "transparent", "border": "none", "color": "#9ab8d1", "cursor": "pointer", "padding": "2px 4px"},
                    )
                )
        return out
    except Exception:
        return []