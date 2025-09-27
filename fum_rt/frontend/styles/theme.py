"""
Deprecated shim for FUM Frontend Styles.

Old path (legacy):
  from fum_rt.frontend.styles.theme import get_global_css

New canonical path:
  from fum_rt.frontend.styles import get_global_css

This module delegates to the modular styles package to preserve backward compatibility.
"""

from __future__ import annotations

# Prefer aggregator in styles/__init__.py
try:
    from . import get_global_css as _get_global_css  # type: ignore[attr-defined]
except Exception:
    # Fail-soft: compute by concatenating available layers
    def _safe(layer):
        try:
            return layer()
        except Exception:
            return ""

    def _get_global_css() -> str:
        try:
            from .base import get_base_css  # type: ignore
        except Exception:
            def get_base_css() -> str:  # type: ignore[no-redef]
                return ""
        try:
            from .layout import get_layout_css  # type: ignore
        except Exception:
            def get_layout_css() -> str:  # type: ignore[no-redef]
                return ""
        try:
            from .components import get_components_css  # type: ignore
        except Exception:
            def get_components_css() -> str:  # type: ignore[no-redef]
                return ""
        return "\n".join([_safe(get_base_css), _safe(get_layout_css), _safe(get_components_css)])


def get_global_css() -> str:
    """
    Return full CSS string for injection.
    Prefer importing from fum_rt.frontend.styles instead of this legacy module.
    """
    return _get_global_css()


__all__ = ["get_global_css"]