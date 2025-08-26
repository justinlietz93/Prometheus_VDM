"""
Layout CSS for FUM Live Dashboard.

Modularized: grid system, card container, responsive rules, utilities.
Include after styles.base.get_base_css().

Author: Justin K. Lietz
"""

from __future__ import annotations

def get_layout_css() -> str:
    """
    Return responsive layout rules (no component styling).
    """
    return """
    /* Layout hardening and responsive behavior */

    /* Constrain the app container to avoid full-width stretch on huge monitors */
    #react-entry-point, #_dash-app-content, #_dash-app-content > div{
      max-width: 1600px;
      margin: 0 auto;
      width: 100%;
    }

    /* Improve base grid: use a flexible left column and maintain gap consistency */
    .grid{
      display: grid;
      grid-template-columns: minmax(300px, 360px) 1fr;
      gap: 16px;
      align-items: start;
    }

    /* On mid-sized screens, ease the left column width to reduce crowding */
    @media (max-width: 1200px){
      .grid{
        grid-template-columns: minmax(260px, 320px) 1fr;
        gap: 14px;
      }
    }

    /* On narrow screens, stack to a single column to prevent overlap */
    @media (max-width: 900px){
      .grid{
        grid-template-columns: 1fr;
        gap: 12px;
      }
    }

    /* Cards: allow inner components to overflow (e.g., dropdown menus), add column flow */
    .card{
      position: relative;
      overflow: visible; /* prevent dropdown clipping */
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    /* Utility rows/columns for consistent spacing */
    .row{ display: flex; gap: 8px; flex-wrap: wrap }
    .row > div{ flex: 1; min-width: 140px }
    @media (max-width: 900px){
      .row{ gap: 6px }
      .row > div{ min-width: 120px }
    }

    /* Prevent horizontal scrolling from wide pre/code blocks or long text inputs */
    .card pre, .card code, .card textarea{
      max-width: 100%;
      overflow: auto;
    }

    /* Buttons spacing in cards */
    .card .btn-row{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    /* Guard against accidental absolute children overlap by default */
    .card > *{
      position: relative;
    }

    /* Optional helper: grid variant that auto-fits equal-width cards */
    .grid-auto{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      align-items: start;
    }

    .tight{ margin-top: 6px }

    /* Tweak focus ring thickness on small screens to reduce visual 'chunkiness' */
    @media (max-width: 900px){
      input:focus, textarea:focus, select:focus{
        box-shadow: 0 0 0 2px rgba(106,160,194,0.15);
      }
    }
    """