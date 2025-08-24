"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Lexicon and phrase-bank utilities extracted from Nexus.

Goals:
- Preserve existing behavior exactly (paths, merge order, formats).
- Pure functions where possible; no logging side-effects.
- Robust to malformed files; fail-soft with safe defaults.
"""

import os
import json
from typing import Dict, Tuple, List, Mapping

# ---- Phrase templates -------------------------------------------------------

def load_phrase_templates(run_dir: str) -> List[str]:
    """
    Load phrase templates for the 'say' macro using the same precedence and shape handling
    Nexus used inline:
      1) runs/<ts>/macro_board.json under key: say.templates or say.phrases
      2) runs/<ts>/phrase_bank.json under key: say or templates (list)
      3) fallback: package file fum_rt/io/lexicon/phrase_bank_min.json under key: say or templates (list)
    Returns an ordered list of strings. Any missing/invalid sources are ignored.
    """
    templates: List[str] = []

    # 1) Per-run macro board metadata
    try:
        mb_path = os.path.join(run_dir, "macro_board.json")
        if os.path.exists(mb_path):
            with open(mb_path, "r", encoding="utf-8") as fh:
                _mb = json.load(fh)
            if isinstance(_mb, dict):
                _say_meta = _mb.get("say") or {}
                if isinstance(_say_meta, dict):
                    _tpls = _say_meta.get("templates") or _say_meta.get("phrases") or []
                    if isinstance(_tpls, list):
                        templates.extend([str(x) for x in _tpls if isinstance(x, (str,))])
    except Exception:
        pass

    # 2) Per-run phrase bank
    try:
        pb_run = os.path.join(run_dir, "phrase_bank.json")
        if os.path.exists(pb_run):
            with open(pb_run, "r", encoding="utf-8") as fh:
                obj = json.load(fh)
            if isinstance(obj, dict):
                _say = obj.get("say") or obj.get("templates") or []
                if isinstance(_say, list):
                    templates.extend([str(x) for x in _say if isinstance(x, (str,))])
            return templates
    except Exception:
        pass

    # 3) Fallback package phrase bank (minimum)
    try:
        pkg_dir = os.path.dirname(__file__)
        pb_pkg = os.path.join(pkg_dir, "phrase_bank_min.json")
        if os.path.exists(pb_pkg):
            with open(pb_pkg, "r", encoding="utf-8") as fh:
                obj = json.load(fh)
            if isinstance(obj, dict):
                _say = obj.get("say") or obj.get("templates") or []
                if isinstance(_say, list):
                    templates.extend([str(x) for x in _say if isinstance(x, (str,))])
    except Exception:
        pass

    return templates


# ---- Lexicon I/O ------------------------------------------------------------

def load_lexicon(run_dir: str) -> Tuple[Dict[str, int], int]:
    """
    Load DF-style lexicon and document count from runs/<ts>/lexicon.json.

    Supports:
      - {"tokens":[{"token":..., "count":...}], "doc_count": int}
      - {"doc_count": int, "word": count, ...}
      - Or a bare mapping without doc_count (defaults to 0)

    Returns: (lexicon_lowercased, doc_count_int)
    """
    path = os.path.join(run_dir, "lexicon.json")
    lex: Dict[str, int] = {}
    doc_count = 0
    try:
        if not os.path.exists(path):
            return lex, doc_count
        with open(path, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
        if not isinstance(obj, dict):
            return lex, doc_count

        # document count metadata
        try:
            dc = obj.get("doc_count", obj.get("documents", obj.get("docs", 0)))
            if dc is not None:
                doc_count = int(dc)
        except Exception:
            pass

        if "tokens" in obj and isinstance(obj["tokens"], list):
            for ent in obj["tokens"]:
                try:
                    lex[str(ent["token"]).lower()] = int(ent["count"])
                except Exception:
                    pass
        else:
            for k, v in obj.items():
                if str(k) in ("doc_count", "documents", "docs"):
                    continue
                try:
                    lex[str(k).lower()] = int(v)
                except Exception:
                    pass
    except Exception:
        # fail-soft: empty
        pass
    return lex, doc_count


def save_lexicon(run_dir: str, lexicon: Mapping[str, int], doc_count: int) -> None:
    """
    Persist lexicon to runs/<ts>/lexicon.json using the same normalized format Nexus used:
      {
        "doc_count": int,
        "tokens": [{"token": word, "count": n}, ...]  // sorted by (-count, token)
      }
    """
    try:
        toks = [
            {"token": str(k), "count": int(v)}
            for k, v in sorted(
                ((str(k), int(v)) for k, v in (lexicon or {}).items()),
                key=lambda kv: (-int(kv[1]), kv[0]),
            )
        ]
        obj = {"doc_count": int(max(0, int(doc_count))), "tokens": toks}
        path = os.path.join(run_dir, "lexicon.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
    except Exception:
        # fail-soft
        pass


__all__ = ["load_phrase_templates", "load_lexicon", "save_lexicon"]