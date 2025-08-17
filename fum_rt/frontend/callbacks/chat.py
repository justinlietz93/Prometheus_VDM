from __future__ import annotations

import os
import json
from dash import Input, Output, State, no_update  # noqa: F401

from fum_rt.frontend.utilities.tail import tail_jsonl_bytes
from fum_rt.frontend.controllers.chat_controller import (
    items_from_utd_records,
    items_from_inbox_records,
    trim_items,
    render_chat_view,
)


def register_chat_callbacks(app):
    """
    Chat callbacks:
      - on_chat_send: append user text to chat_inbox.jsonl in the selected run
      - on_chat_update: stream UTD macro 'say' events + user inbox into a simple text view

    State shape stored in dcc.Store(id="chat-state"):
      {
        "run_dir": str,
        "utd_size": int,     # last read byte offset for utd_events.jsonl
        "inbox_size": int,   # last read byte offset for chat_inbox.jsonl
        "items": List[Dict]  # standardized chat items
      }
    """

    @app.callback(
        Output("chat-status", "children"),
        Output("chat-input", "value"),
        Input("chat-send", "n_clicks"),
        State("run-dir", "value"),
        State("chat-input", "value"),
        prevent_initial_call=True,
    )
    def on_chat_send(_n, run_dir, text):
        rd = (run_dir or "").strip()
        msg = (text or "").strip()
        if not rd:
            return "Select a run directory.", no_update
        if not msg:
            return "Type a message.", no_update
        try:
            inbox = os.path.join(rd, "chat_inbox.jsonl")
            os.makedirs(os.path.dirname(inbox), exist_ok=True)
            with open(inbox, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"type": "text", "msg": msg}, ensure_ascii=False) + "\n")
            return "Sent.", ""
        except Exception as e:
            return f"Error writing chat_inbox.jsonl: {e}", no_update

    @app.callback(
        Output("chat-view", "children"),
        Output("chat-state", "data"),
        Input("poll", "n_intervals"),
        Input("chat-filter", "value"),
        State("run-dir", "value"),
        State("chat-state", "data"),
        prevent_initial_call=False,
    )
    def on_chat_update(_n, filt, run_dir, data):
        rd = (run_dir or "").strip()
        if not rd:
            return "", {"run_dir": "", "utd_size": 0, "inbox_size": 0, "items": []}

        state = data or {}
        items = list(state.get("items", []))
        last_run = state.get("run_dir")
        utd_size = int(state.get("utd_size", 0)) if isinstance(state.get("utd_size"), int) else 0
        inbox_size = int(state.get("inbox_size", 0)) if isinstance(state.get("inbox_size"), int) else 0

        if last_run != rd:
            # Reset when switching runs
            items = []
            utd_size = 0
            inbox_size = 0

        # Strict zero-file-IO mode (for responsiveness): render from in-memory only
        _disable_io = str(os.getenv("DASH_DISABLE_FILE_IO", "1")).strip().lower() in ("1", "true", "yes", "on")
        if _disable_io:
            items = trim_items(items, limit=200)
            view = render_chat_view(items, filt=(filt or "all"))
            return view, {
                "run_dir": rd,
                "utd_size": int(utd_size),
                "inbox_size": int(inbox_size),
                "items": items,
            }

        # Stream UTD macro events
        utd_path = os.path.join(rd, "utd_events.jsonl")
        new_utd_recs, new_utd_size = tail_jsonl_bytes(utd_path, utd_size)
        items.extend(items_from_utd_records(new_utd_recs))

        # Stream user inbox
        inbox_path = os.path.join(rd, "chat_inbox.jsonl")
        new_inbox_recs, new_inbox_size = tail_jsonl_bytes(inbox_path, inbox_size)
        items.extend(items_from_inbox_records(new_inbox_recs))

        items = trim_items(items, limit=200)
        view = render_chat_view(items, filt=(filt or "all"))

        return view, {
            "run_dir": rd,
            "utd_size": int(new_utd_size),
            "inbox_size": int(new_inbox_size),
            "items": items,
        }