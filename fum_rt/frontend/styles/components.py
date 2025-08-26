"""
Component CSS for FUM Live Dashboard.

Modularized: dcc.Dropdown (react-select), rc-slider, and component-level utilities.
Include after styles.layout.get_layout_css().

Author: Justin K. Lietz
"""

from __future__ import annotations


def get_components_css() -> str:
    """
    Return component-specific rules for dropdowns, sliders, etc.
    """
    return """
    /* dcc.Dropdown (react-select) */
    .Select-control{
      background:var(--panel2)!important;
      border:1px solid var(--border)!important;
      color:var(--text)!important;
      border-radius:8px;
      min-height: 34px;
    }
    .Select--single>.Select-control .Select-value{
      color:var(--text)!important;
    }
    .Select-menu-outer{
      background:var(--panel2)!important;
      border:1px solid var(--border)!important;
      color:var(--text)!important;
      z-index: 9999 !important; /* ensure above neighbors */
    }
    .Select-option{
      background:var(--panel2)!important;
      color:var(--text)!important;
    }
    .Select-option.is-focused{background:#121a22!important}
    .Select-option.is-selected{background:#17222c!important}
    .VirtualizedSelectFocusedOption{background:#121a22!important}

    /* Prevent clipping of dropdown menus by container overflow */
    .dash-dropdown, .Select, .Select-menu-outer{
      overflow: visible !important;
    }

    /* Ensure focus rings render above adjacent inputs */
    .Select-control{ z-index: 2 }

    /* rc-slider */
    .rc-slider{padding:8px 0; z-index: 1}
    .rc-slider-rail{background:#0d1218}
    .rc-slider-track{background:var(--accent)}
    .rc-slider-dot{border-color:#233140;background:#10151c}
    .rc-slider-handle{border:1px solid var(--border);background:var(--panel2)}
    """