"""
Soft-dark theme for FUM Live Dashboard.
Provides a centralized CSS string to keep layout files minimal.
"""

def get_global_css() -> str:
    return """
    :root{
      --bg:#0b0f14; --panel:#10151c; --panel2:#0e141a; --text:#cfd7e3; --muted:#8699ac;
      --accent:#6aa0c2; --ok:#3a8f5c; --danger:#b3565c; --border:#1d2733; --grid:#233140;
      --plot:#0f141a; --paper:#10151c;
    }
    *{box-sizing:border-box}
    body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Ubuntu,Cantarell,Helvetica Neue,Arial,Noto Sans,sans-serif;}
    h1,h2,h3,h4{color:var(--text);font-weight:600}
    .grid{display:grid;grid-template-columns:360px 1fr;gap:16px}
    .card{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px}
    .card h4,.card h3{margin:0 0 8px 0}
    label{font-size:12px;color:var(--muted);margin-bottom:4px;display:block}
    .row{display:flex;gap:8px;flex-wrap:wrap}
    .row>div{flex:1;min-width:120px}
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
    /* dcc.Dropdown (react-select) */
    .Select-control{background:var(--panel2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px}
    .Select--single>.Select-control .Select-value{color:var(--text)!important}
    .Select-menu-outer{background:var(--panel2)!important;border:1px solid var(--border)!important;color:var(--text)!important}
    .Select-option{background:var(--panel2)!important;color:var(--text)!important}
    .Select-option.is-focused{background:#121a22!important}
    .Select-option.is-selected{background:#17222c!important}
    .VirtualizedSelectFocusedOption{background:#121a22!important}
    /* rc-slider */
    .rc-slider{padding:8px 0}
    .rc-slider-rail{background: #0d1218}
    .rc-slider-track{background: var(--accent)}
    .rc-slider-dot{border-color:#233140;background:#10151c}
    .rc-slider-handle{border:1px solid var(--border);background:var(--panel2)}
    .tight{margin-top:6px}
    """