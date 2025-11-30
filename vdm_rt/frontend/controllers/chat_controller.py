"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


def parse_utd_macro_record(rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Convert a single UTD macro record into a standardized chat item dict.
    Expected rec schema (best-effort):
      { "type": "macro", "macro": "...", "args": {...}, "why": {...} }
    """
    if not isinstance(rec, dict):
        return None
    if rec.get("type") != "macro":
        return None

    macro_name = rec.get("macro", "unknown")
    args = rec.get("args", {}) or {}
    if macro_name == "say":
        text = args.get("text", "")
    else:
        text = f"macro: {macro_name}"
        if args:
            try:
                arg_str = ", ".join(f"{k}={v}" for k, v in args.items())
                text += f" ({arg_str})"
            except Exception:
                text += f" (args: {args})"

    # Extract why.t and spike-like markers if present
    why = rec.get("why") or {}
    t = None
    try:
        t = int((why or {}).get("t"))
    except Exception:
        t = None

    spike = False
    if isinstance(why, dict):
        try:
            speak_ok = why.get("speak_ok")
            spike = bool(speak_ok) or bool((why or {}).get("spike"))
        except Exception:
            spike = False

    return {"kind": "model", "text": str(text), "t": t, "spike": bool(spike), "macro": macro_name}


def items_from_utd_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for rec in (records or []):
        try:
            item = parse_utd_macro_record(rec)
            if item:
                out.append(item)
        except Exception:
            # ignore malformed lines
            pass
    return out


def items_from_inbox_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert chat_inbox.jsonl records into standardized chat items.
    Supported entries (best-effort):
      - {"type": "text", "msg": "..."}  or {"type": "text", "text": "..."}
    """
    out: List[Dict[str, Any]] = []
    for rec in (records or []):
        try:
            if not isinstance(rec, dict):
                continue
            mtype = (rec.get("type") or "").lower()
            if mtype == "text":
                msg = rec.get("msg") or rec.get("text") or ""
                if msg:
                    out.append({"kind": "user", "text": str(msg), "t": None, "spike": False})
        except Exception:
            pass
    return out


def trim_items(items: List[Dict[str, Any]], limit: int = 200) -> List[Dict[str, Any]]:
    if not items:
        return []
    if len(items) <= limit:
        return items
    return items[-limit:]


def render_chat_view(items: List[Dict[str, Any]], filt: str = "all") -> str:
    """
    Render a plain-text view of chat items based on filter:
      - "all": show all
      - "say": only model items with macro == "say"
      - "spike": only model items with spike==True and macro == "say"
    """
    f = (filt or "all").lower()
    lines: List[str] = []

    for it in (items or []):
        if f == "say":
            if it.get("kind") != "model" or it.get("macro") != "say":
                continue
        elif f == "spike":
            if it.get("kind") != "model" or not it.get("spike", False) or it.get("macro") != "say":
                continue

        text = it.get("text") or ""
        if it.get("kind") == "user":
            lines.append(f"You: {text}")
        else:
            t = it.get("t")
            if t is not None:
                lines.append(f"[t={t}] {text}")
            else:
                lines.append(f"{text}")

    return "\n".join(lines)