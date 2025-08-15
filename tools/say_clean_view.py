#!/usr/bin/env python3
import argparse
import json
import sys
import re
import html
import os

def sanitize_text(s: str) -> str:
    """
    Non-invasive viewer cleanup:
    - HTML unescape
    - Drop <ref>...</ref> blocks and generic tags
    - Drop wiki templates {{...}}
    - Collapse [[link|label]] -> label, [[label]] -> label
    - Remove http/https links
    - Whitespace normalization
    This does NOT modify runtime output, only how it's displayed by this tool.
    """
    try:
        s = str(s or "")
        try:
            s = html.unescape(s)
        except Exception:
            pass
        # Remove <ref> blocks and tags
        s = re.sub(r"<ref[^>]*>.*?</ref>", " ", s, flags=re.IGNORECASE | re.DOTALL)
        s = re.sub(r"<[^>]+>", " ", s)
        # Remove actual HTML tags (if any slipped through)
        s = re.sub(r"<ref[^>]*>.*?</ref>", " ", s, flags=re.IGNORECASE | re.DOTALL)
        s = re.sub(r"<[^>]+>", " ", s)
        # Remove wiki templates and external link markup
        s = re.sub(r"\{\{[^}]+\}\}", " ", s)
        s = re.sub(r"\[http[^\s\]]+\]", " ", s, flags=re.IGNORECASE)
        s = re.sub(r"http[s]?://\S+", " ", s, flags=re.IGNORECASE)

        # Collapse wiki links: [[link|label]] or [[label]]
        def _collapse_wikilink(m):
            body = m.group(0)[2:-2]
            parts = body.split("|")
            return parts[-1] if parts else body
        s = re.sub(r"\[\[[^\]]+\]\]", _collapse_wikilink, s)

        # Normalize bars and whitespace
        s = s.replace("|", " ")
        s = re.sub(r"\s+", " ", s).strip()
        return s
    except Exception:
        return str(s or "")

def process(input_path: str, macro: str, include_text: bool, out_path: str, print_why: bool) -> int:
    n = 0
    out_fh = open(out_path, "w", encoding="utf-8") if out_path else None
    try:
        with open(input_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                ev_type = obj.get("type") or obj.get("event_type")

                if ev_type == "macro":
                    mname = obj.get("macro") or obj.get("name")
                    if macro and mname != macro:
                        continue
                    args = obj.get("args", {}) if isinstance(obj.get("args", {}), dict) else {}
                    text = args.get("text", "")
                    cleaned = sanitize_text(text)
                    rec = {
                        "macro": mname,
                        "text_raw": text,
                        "text_clean": cleaned,
                        "score": obj.get("score", None),
                    }
                    if print_why and "why" in args:
                        rec["why"] = args["why"]
                    n += 1
                    if out_fh:
                        out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    else:
                        sys.stdout.write(cleaned + "\n")

                elif include_text and ev_type == "text":
                    text = obj.get("msg") if "msg" in obj else obj.get("text", "")
                    cleaned = sanitize_text(text)
                    rec = {
                        "type": "text",
                        "text_raw": text,
                        "text_clean": cleaned,
                        "score": obj.get("score", None),
                    }
                    n += 1
                    if out_fh:
                        out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    else:
                        sys.stdout.write(cleaned + "\n")
    finally:
        if out_fh:
            out_fh.close()
    return n

def main():
    ap = argparse.ArgumentParser(description="Pretty view for UTD events (non-invasive, preserves runtime behavior).")
    ap.add_argument("--input", "-i", required=True, help="Path to runs/<timestamp>/utd_events.jsonl")
    ap.add_argument("--macro", "-m", default="say", help="Macro name to filter (default: say)")
    ap.add_argument("--include-text", action="store_true", help="Also include type=text events")
    ap.add_argument("--out", "-o", default=None, help="Optional output NDJSON path")
    ap.add_argument("--print-why", action="store_true", help="Include 'why' payload in output records")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        sys.stderr.write(f"Input not found: {args.input}\n")
        sys.exit(2)

    count = process(args.input, args.macro, args.include_text, args.out, args.print_why)
    if count == 0:
        sys.stderr.write("No events matched.\n")

if __name__ == "__main__":
    main()