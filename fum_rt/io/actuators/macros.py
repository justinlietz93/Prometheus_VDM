from __future__ import annotations
import json, os, threading, time
from typing import Any, Dict, Iterable, Optional

class MacroEmitter:
    """
    Thread-safe NDJSON macro emitter.
    Schema per event:
      {
        "type": "macro",
        "macro": <lowercase name>,
        "args": {
          "text": <flattened, human-readable line for classifiers>,
          "why": { ... metrics/context ... },
          ... macro-specific fields (optional) ...
        },
        "score": <float, optional>
      }
    """
    def __init__(self, path: str, why_provider=None):
        # Output path to NDJSON, e.g., runs/<ts>/utd_events.jsonl
        self.path = path or ""
        self.lock = threading.Lock()
        # why_provider: callable returning a dict with context (t, phase, etc.)
        self.why_provider = why_provider or (lambda: {"t": int(time.time() * 1000), "phase": 0})
        # ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)

    def _emit(self, macro: str, text: str, score: Optional[float] = None, **kwargs: Any):
        evt = {
            "type": "macro",
            "macro": str(macro).lower(),
            "args": {
                "text": str(text),
                "why": (self.why_provider() or {}),
            }
        }
        # attach any extra fields into args (vars, edges, etc.)
        for k, v in kwargs.items():
            evt["args"][k] = v
        if score is not None:
            try:
                evt["score"] = float(score)
            except Exception:
                pass
        line = json.dumps(evt, ensure_ascii=False)
        with self.lock, open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    # ---- basic channels ----
    def say(self, text: str, score: Optional[float] = None, **kw: Any):
        self._emit("say", text, score=score, **kw)

    def status(self, text: str, score: Optional[float] = None, **kw: Any):
        self._emit("status", text, score=score, **kw)

    def think(self, text: str, **kw: Any):
        self._emit("think", text, **kw)

    # ---- reasoning macros (flatten to readable text) ----
    def vars(self, mapping: Dict[str, str], **kw: Any):
        # VARS: N=neural; G=global_access; ...
        flat = "VARS: " + "; ".join(f"{k}={v}" for k, v in mapping.items())
        self._emit("vars", flat, vars=mapping, **kw)

    def edges(self, edges: Iterable[str], **kw: Any):
        # EDGES: N->G; G->B; E->B?
        flat = "EDGES: " + "; ".join(edges)
        self._emit("edges", flat, edges=list(edges), **kw)

    def assumptions(self, items: Iterable[str], **kw: Any):
        flat = "ASSUMPTIONS: " + "; ".join(items)
        self._emit("assumptions", flat, assumptions=list(items), **kw)

    def derivation(self, sentence: str, **kw: Any):
        """
        Expect at least one inference marker to trip 'chain' classifier:
        e.g., 'If A and B, therefore C.'
        """
        flat = "DERIVATION: " + sentence
        self._emit("derivation", flat, **kw)

    def target(self, text: str, **kw: Any):
        """
        Include 'do(' when applicable so 'intervention' classifier fires.
        e.g., 'TARGET: P(Y|do(X))'
        """
        flat = "TARGET: " + text
        self._emit("target", flat, **kw)

    def prediction_delta(self, text: str, **kw: Any):
        flat = "PREDICTION-DELTA: " + text
        self._emit("prediction-delta", flat, **kw)

    def transfer(self, text: str, **kw: Any):
        flat = "TRANSFER: " + text
        self._emit("transfer", flat, **kw)

    def equation(self, text: str, **kw: Any):
        """
        Encourage SEM/SCM form to trip 'equation' classifier:
        e.g., 'EQUATION: Y = β X + U_Y'
        """
        flat = "EQUATION: " + text
        self._emit("equation", flat, **kw)