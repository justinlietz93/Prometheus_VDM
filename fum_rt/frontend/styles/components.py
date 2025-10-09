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

    /* dcc.Tabs (fum-tabs) - dark theme styling */
    .fum-tabs{
      background: transparent;
      border: none;
      margin: 0 0 6px 0;
      padding: 0;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    /* Base tab - minimal underline style to match dark theme */
    .fum-tabs .tab,
    .fum-tabs button.tab,
    .fum-tabs .fum-tab{
      background: transparent !important;
      color: var(--muted) !important;
      border: none !important;
      border-bottom: 2px solid transparent !important;
      padding: 4px 8px;
      margin: 0 8px 0 0;
      border-radius: 0;
      font-size: 13px;
      line-height: 1.2;
      opacity: 0.95;
      transition: color 120ms ease, border-color 120ms ease, filter 120ms ease;
    }

    .fum-tabs .tab:hover,
    .fum-tabs button.tab:hover,
    .fum-tabs .fum-tab:hover{
      filter: brightness(1.04);
      opacity: 1;
      color: var(--text) !important;
      border-bottom-color: var(--border) !important;
    }

    /* Selected tab (robust: match class and aria-selected) - accent underline */
    .fum-tabs .tab--selected,
    .fum-tabs .tab[aria-selected="true"],
    .fum-tabs button.tab[aria-selected="true"],
    .fum-tabs .fum-tab--selected{
      background: transparent !important;
      color: var(--text) !important;
      border: none !important;
      border-bottom: 2px solid var(--accent) !important;
      box-shadow: none !important;
      opacity: 1;
    }

    /* Compact variant */
    .fum-tabs.small{ padding: 0 2px 0 0; gap: 4px; }
    .fum-tabs.small .tab,
    .fum-tabs.small button.tab,
    .fum-tabs.small .fum-tab{
      padding: 2px 6px;
      font-size: 12px;
      margin: 0 6px 0 0;
    }
    .fum-tabs.small .tab--selected,
    .fum-tabs.small .tab[aria-selected="true"],
    .fum-tabs.small button.tab[aria-selected="true"],
    .fum-tabs.small .fum-tab--selected{
      border-bottom-width: 1px !important;
    }

    /* '+' add tab subtle style */
    .fum-tabs .fum-tab.add{
      color: var(--muted) !important;
      border-bottom-color: transparent !important;
      opacity: 0.8;
    }
    .fum-tabs .fum-tab.add:hover{
      color: var(--text) !important;
      opacity: 1;
    }

    /* Tabs content wrapper (when used) */
    .fum-tabs .tab-content{
      background: var(--panel);
      color: var(--text);
      border: 1px solid var(--border);
      border-top: none;
      border-bottom-left-radius: 8px;
      border-bottom-right-radius: 8px;
    }
    """