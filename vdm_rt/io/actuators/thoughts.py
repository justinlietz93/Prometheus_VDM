"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Any, Dict, Iterable, Optional


class ThoughtEmitter:
    """
    Introspection Ledger (emit-only).
    Thread-safe NDJSON writer for typed "thought events" that are never ingested back.

    Event shape (one JSON per line):
    {
      "type": "thought",
      "why": { ... context from why_provider ... },
      "kind": "<observation|motif|hypothesis|test|derivation|revision|plan>",
      ... kind-specific fields ...
    }
    """

    def __init__(self, path: str, why: Optional[callable] = None):
        """
        Args:
            path: Output NDJSON path (e.g., runs/<ts>/thoughts.ndjson)
            why:  Callable returning a dict of read-only context (t, phase, b1_z, etc.)
        """
        self.path = path
        self._why = why or (lambda: {"t": int(time.time() * 1000), "phase": 0})
        self._lock = threading.Lock()
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    # -------------- core --------------

    def _emit(self, payload: Dict[str, Any]) -> None:
        evt = {"type": "thought", "why": (self._why() or {})}
        evt.update(payload or {})
        line = json.dumps(evt, ensure_ascii=False)
        with self._lock, open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    # -------------- typed helpers --------------

    def observation(self, key: str, value: Any, **kw: Any) -> None:
        self._emit({"kind": "observation", "key": key, "value": value, **kw})

    def motif(self, motif_id: str, nodes: Optional[Iterable[Any]] = None, **kw: Any) -> None:
        self._emit({"kind": "motif", "motif_id": motif_id, "nodes": list(nodes or []), **kw})

    def hypothesis(
        self,
        hid: str,
        claim: str,
        status: str = "tentative",
        conf: Optional[float] = None,
        **kw: Any,
    ) -> None:
        self._emit({"kind": "hypothesis", "id": hid, "claim": claim, "status": status, "conf": conf, **kw})

    def test(self, kind: str, result: bool, vars: Optional[Dict[str, Any]] = None, **kw: Any) -> None:
        self._emit({"kind": "test", "test_kind": kind, "result": bool(result), "vars": dict(vars or {}), **kw})

    def derivation(
        self,
        premises: Iterable[str],
        therefore: str,
        conf: Optional[float] = None,
        **kw: Any,
    ) -> None:
        self._emit({"kind": "derivation", "premises": list(premises or []), "therefore": therefore, "conf": conf, **kw})

    def revision(self, hyp: str, new_status: str, because: Optional[Iterable[str]] = None, **kw: Any) -> None:
        self._emit({"kind": "revision", "hyp": hyp, "new_status": new_status, "because": list(because or []), **kw})

    def plan(self, act: str, vars: Optional[Dict[str, Any]] = None, rationale: Optional[str] = None, **kw: Any) -> None:
        self._emit({"kind": "plan", "act": act, "vars": dict(vars or {}), "rationale": rationale, **kw})