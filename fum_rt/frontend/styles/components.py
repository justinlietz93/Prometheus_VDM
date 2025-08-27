"""
Component CSS for FUM Live Dashboard.

Modularized: dcc.Dropdown (react-select), rc-slider, and component-level utilities.
Include after styles.layout.get_layout_css().

Author: Justin K. Lietz
"""

from __future__ import annotations


def get_components_css() -> str:
    """
    Return component-specific rules for dropdowns, sliders, tabs, etc.
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

    /* dcc.Tabs (fum-tabs) — dark theme styling */
    .fum-tabs{
      border-bottom:1px solid var(--border);
      margin: 0;
      padding: 0 6px 0 0;
    }
    .fum-tabs .tab{
      background: var(--panel2);
      color: var(--text);
      border: 1px solid var(--border);
      border-bottom: none;
      padding: 6px 10px;
      margin: 0 6px 0 0;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      font-size: 13px;
      line-height: 1.2;
      opacity: 0.9;
      transition: filter 120ms ease, box-shadow 120ms ease, opacity 120ms ease;
    }
    .fum-tabs .tab:hover{
      filter: brightness(1.05);
      opacity: 1;
    }
    .fum-tabs .tab--selected{
      background: var(--panel);
      color: var(--text);
      border-color: var(--accent);
      box-shadow: inset 0 -2px 0 var(--accent);
      opacity: 1;
    }

    /* Compact variant */
    .fum-tabs.small{ padding: 0 4px 0 0; }
    .fum-tabs.small .tab{
      padding: 3px 8px;
      font-size: 12px;
      margin: 0 4px 0 0;
    }
    .fum-tabs.small .tab--selected{
      box-shadow: inset 0 -1px 0 var(--accent);
    }

    /* Tabs content wrapper inside our panels */
    .fum-tabs .tab-content{
      background: var(--panel);
      color: var(--text);
    }
    """