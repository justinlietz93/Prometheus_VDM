"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
from dash import Input, Output, State, no_update  # noqa: F401
from fum_rt.frontend.utilities.pdf_utils import convert_pdf_to_text_file


def register_feed_callbacks(app, manager, repo_root: str):
    """
    Feed controls:
      - Start feeding a file into the managed process stdin at a given rate
      - Stop feeding
    Uses the same IDs as the inline version in fum_live to preserve behavior.
    """

    @app.callback(
        Output("send-status", "children", allow_duplicate=True),
        Input("feed-start", "n_clicks"),
        State("feed-path", "value"),
        State("feed-rate", "value"),
        prevent_initial_call=True,
    )
    def on_feed_start(_n, path, rate):
        p = (path or "").strip()
        if not p:
            return "Provide a feed path (relative to fum_rt/data or absolute)."
        chosen = p
        try:
            if (not os.path.isabs(chosen)) or (not os.path.exists(chosen)):
                data_dir = os.path.join(repo_root, "fum_rt", "data")
                cand = os.path.join(data_dir, p)
                if os.path.exists(cand):
                    chosen = cand
        except Exception:
            pass

        # If a PDF is selected, convert to text (best-effort with graceful fallback) before feeding
        status_prefix = ""
        try:
            if chosen.lower().endswith(".pdf"):
                out_dir = os.path.join(repo_root, "outputs", "pdf_text")
                os.makedirs(out_dir, exist_ok=True)
                txt_path, method = convert_pdf_to_text_file(chosen, out_dir)
                if txt_path:
                    status_prefix = f"Converted PDF via {method}; "
                    chosen = txt_path
                else:
                    return "PDF conversion failed (install PyMuPDF/pdfminer.six/PyPDF2 or pytesseract+pdf2image)."
        except Exception:
            return "PDF conversion failed."

        ok = manager.feed_file(chosen, float(rate or 20.0))
        return f"{status_prefix}Feeding from {chosen}." if ok else "Feed failed (check process running and path)."

    @app.callback(
        Output("send-status", "children", allow_duplicate=True),
        Input("feed-stop", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_feed_stop(_n):
        manager.stop_feed()
        return "Feed stopped."