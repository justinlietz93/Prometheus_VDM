"""
Base CSS for FUM Live Dashboard.

Modularized: foundational variables, typography, resets, form controls, scrollbars.
Include this first; layer layout- and component-specific CSS on top.

Author: Justin K. Lietz
"""

from __future__ import annotations

def get_base_css() -> str:
    """
    Return core CSS variables and base elements without layout or component rules.
    Safe to include standalone; other style modules should be appended after this.
    """
    return """
    :root{
      --bg:#0b0f14; --panel:#10151c; --panel2:#0e141a; --text:#cfd7e3; --muted:#8699ac;
      --accent:#6aa0c2; --ok:#3a8f5c; --danger:#b3565c; --border:#1d2733; --grid:#233140;
      --plot:#0f141a; --paper:#10151c;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Ubuntu,Cantarell,Helvetica Neue,Arial,Noto Sans,sans-serif;line-height:1.35;margin:0}
    h1,h2,h3,h4{color:var(--text);font-weight:600;margin:0 0 8px 0}
    p{margin:0 0 8px 0}
    a{color:var(--accent);text-decoration:none}
    a:hover{text-decoration:underline}

    label{font-size:12px;color:var(--muted);margin-bottom:4px;display:block}

    button{cursor:pointer;border-radius:8px;border:1px solid var(--border);padding:6px 10px;background:var(--panel2);color:var(--text)}
    button:hover{filter:brightness(1.05)}
    .btn-ok{background:var(--ok);color:#fff;border:none}
    .btn-danger{background:var(--danger);color:#fff;border:none}

    pre{background:#0a0e13;border:1px solid var(--border);border-radius:8px;padding:8px;white-space:pre-wrap;color:#dfe7f1}
    input[type="text"],input[type="number"],textarea,select{
        width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--border);
        border-radius:8px;padding:6px 8px;outline:none;
    }
    input::placeholder,textarea::placeholder{color:var(--muted)}
    input:focus,textarea:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(106,160,194,0.15)}

    /* Scrollbars (WebKit) */
    *::-webkit-scrollbar{width:10px;height:10px}
    *::-webkit-scrollbar-track{background:var(--panel)}
    *::-webkit-scrollbar-thumb{
        background:#1d2733;
        border-radius:8px;
        border:1px solid var(--grid);
    }
    *::-webkit-scrollbar-thumb:hover{background:#273445}

    /* Scrollbars (Firefox) */
    *{scrollbar-color:#1d2733 var(--panel2);scrollbar-width:thin}
    """