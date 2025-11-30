"""
FUM Frontend Styles (modular)

Exports:
- get_global_css(): concatenates base → layout → components CSS in a safe order
- get_base_css, get_layout_css, get_components_css: individual layers (advanced usage)

Layering contract:
1) base: variables, resets, typography, form controls, scrollbars (no layout)
2) layout: grids, cards, responsive rules, utilities (no component overrides)
3) components: dcc.Dropdown/react-select, rc-slider, and component-specific rules

Author: Justin K. Lietz
"""

from __future__ import annotations

from typing import Callable, List

# Individual layers
try:
    from .base import get_base_css
except Exception:  # pragma: no cover
    def get_base_css() -> str:  # type: ignore[no-redef]
        return ""

try:
    from .layout import get_layout_css
except Exception:  # pragma: no cover
    def get_layout_css() -> str:  # type: ignore[no-redef]
        return ""

try:
    from .components import get_components_css
except Exception:  # pragma: no cover
    def get_components_css() -> str:  # type: ignore[no-redef]
        return ""


def get_global_css() -> str:
    """
    Return the full CSS string for injection into Dash index.
    Concatenates in stable order: base → layout → components.
    Robust to partial availability (missing modules return empty string).
    """
    layers: List[Callable[[], str]] = [get_base_css, get_layout_css, get_components_css]
    parts: List[str] = []
    for layer in layers:
        try:
            css = layer()
            if css and isinstance(css, str):
                parts.append(css)
        except Exception:
            # Fail-soft: do not crash the app if one layer errors
            continue
    return "\n".join(parts)


__all__ = [
    "get_global_css",
    "get_base_css",
    "get_layout_css",
    "get_components_css",
]