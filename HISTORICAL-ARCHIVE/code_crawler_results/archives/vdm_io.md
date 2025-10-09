# vdm_io

Generated on: 2025-08-30 22:30:13

<?xml version="1.0" ?>
<vdm_io>
  <metadata>
    <global_stats>
      <total_files>27</total_files>
      <total_size_bytes>72058</total_size_bytes>
      <total_loc>1969</total_loc>
    </global_stats>
    <chunk_stats>
      <files_in_chunk>27</files_in_chunk>
      <size_in_chunk_bytes>72058</size_in_chunk_bytes>
      <loc_in_chunk>1969</loc_in_chunk>
    </chunk_stats>
  </metadata>
  <ascii_map><![CDATA[
io/
├── README.md
│   (LOC: 0, Size: 0 B)
├── __init__.py
│   (LOC: 0, Size: 0 B)
├── actuators/
│   ├── __init__.py
│   │   (LOC: 0, Size: 0 B)
│   ├── macros.py
│   │   (LOC: 133, Size: 4.9 KB)
│   ├── motor_control.py
│   │   (LOC: 9, Size: 383 B)
│   ├── symbols.py
│   │   (LOC: 7, Size: 348 B)
│   ├── thoughts.py
│   │   (LOC: 87, Size: 3.3 KB)
│   ├── visualize.py
│   │   (LOC: 7, Size: 348 B)
│   └── vocalizer.py
│       (LOC: 7, Size: 348 B)
├── cognition/
│   ├── composer.py
│   │   (LOC: 84, Size: 2.8 KB)
│   ├── speaker.py
│   │   (LOC: 98, Size: 2.5 KB)
│   └── stimulus.py
│       (LOC: 54, Size: 1.7 KB)
├── lexicon/
│   ├── idf.py
│   │   (LOC: 87, Size: 2.9 KB)
│   ├── phrase_bank_min.json
│   │   (LOC: 14, Size: 649 B)
│   └── store.py
│       (LOC: 160, Size: 5.6 KB)
├── logging/
│   └── rolling_jsonl.py
│       (LOC: 536, Size: 20.6 KB)
├── maps_ring.py
│   (LOC: 14, Size: 389 B)
├── sensors/
│   ├── __init__.py
│   │   (LOC: 0, Size: 0 B)
│   ├── auditory.py
│   │   (LOC: 7, Size: 348 B)
│   ├── somatosensory.py
│   │   (LOC: 7, Size: 348 B)
│   ├── symbols.py
│   │   (LOC: 7, Size: 348 B)
│   └── vision.py
│       (LOC: 7, Size: 348 B)
├── utd.py
│   (LOC: 115, Size: 4.5 KB)
├── ute.py
│   (LOC: 94, Size: 3.4 KB)
└── visualization/
    ├── __init__.py
    │   (LOC: 8, Size: 297 B)
    ├── maps_ring.py
    │   (LOC: 113, Size: 3.7 KB)
    └── websocket_server.py
        (LOC: 314, Size: 10.4 KB)]]></ascii_map>
  <files>
    <file>
      <path>README.md</path>
      <content/>
    </file>
    <file>
      <path>__init__.py</path>
      <content/>
    </file>
    <file>
      <path>actuators/__init__.py</path>
      <content/>
    </file>
    <file>
      <path>actuators/macros.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""


from __future__ import annotations
import json, os, threading, time
from typing import Any, Dict, Iterable, Optional
from fum_rt.io.logging.rolling_jsonl import RollingJsonlWriter
try:
    # Prefer zip spooler when available
    from fum_rt.io.logging.rolling_jsonl import RollingZipJsonlWriter  # type: ignore
except Exception:
    RollingZipJsonlWriter = None  # type: ignore

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
        # Prefer zip-spooled writer (bounded disk pressure); fallback to rolling JSONL
        use_zip = True
        try:
            use_zip = str(os.getenv("FUM_ZIP_SPOOL", "1")).strip().lower() in ("1", "true", "yes", "on", "y")
        except Exception:
            use_zip = True
        try:
            if use_zip and (RollingZipJsonlWriter is not None):  # type: ignore
                self._writer = RollingZipJsonlWriter(self.path)  # type: ignore
            else:
                self._writer = RollingJsonlWriter(self.path)
        except Exception:
            self._writer = RollingJsonlWriter(self.path)

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
        with self.lock:
            self._writer.write_line(line)

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
        self._emit("equation", flat, **kw)]]></content>
    </file>
    <file>
      <path>actuators/motor_control.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

# Motor control actuator interface]]></content>
    </file>
    <file>
      <path>actuators/symbols.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>actuators/thoughts.py</path>
      <content><![CDATA["""
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
        self._emit({"kind": "plan", "act": act, "vars": dict(vars or {}), "rationale": rationale, **kw})]]></content>
    </file>
    <file>
      <path>actuators/visualize.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>actuators/vocalizer.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>cognition/composer.py</path>
      <content><![CDATA[from __future__ import annotations

"""
Cognition - speech composer (Phase 3 move-only).

Behavior-preserving extraction of Nexus._compose_say_text:
- Prefer emergent sentence generation from streaming n-grams.
- Fallback to phrase templates with context formatting.
- Final fallback to keyword summary.
"""

from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

# Use absolute import to avoid relative package ambiguity
from fum_rt.core import text_utils


def compose_say_text(
    metrics: Dict[str, Any],
    step: int,
    lexicon: Dict[str, int],
    ng2: Dict[str, Dict[str, int]],
    ng3: Dict[Tuple[str, str], Dict[str, int]],
    recent_text: Iterable[str],
    templates: Optional[Sequence[str]] = None,
    seed_tokens: Optional[Set[str]] = None,
) -> str:
    """
    Compose a short sentence using emergent language or templates.

    Parameters:
        metrics: last tick metrics dict
        step: current tick number (used as seed)
        lexicon/ng2/ng3: emergent language state
        recent_text: iterable of recent inbound text strings
        templates: optional sequence of phrase templates with named fields
        seed_tokens: optional set of tokens influencing emergent generation

    Returns:
        A composed sentence string (non-empty). On failure, returns "".
    """
    try:
        # 1) Fully emergent sentence generation
        sent = text_utils.generate_emergent_sentence(
            lexicon=lexicon,
            ng2=ng2,
            ng3=ng3,
            seed=int(step),
            seed_tokens=seed_tokens,
        )
        if sent:
            return sent

        # 2) Template-based composition if n-grams are not mature
        #    Preserve original keyword summary behavior
        summary = text_utils.summarize_keywords(" ".join(str(s) for s in recent_text), k=6)
        words = [w.strip() for w in summary.split(",") if w.strip()]
        top1 = words[0] if len(words) > 0 else "frontier"
        top2 = words[1] if len(words) > 1 else "structure"

        ctx = {
            "keywords": (summary or "salient loop detected"),
            "top1": top1,
            "top2": top2,
            "vt_entropy": float(metrics.get("vt_entropy", 0.0)),
            "vt_coverage": float(metrics.get("vt_coverage", 0.0)),
            "b1_z": float(metrics.get("b1_z", 0.0)),
            "connectome_entropy": float(metrics.get("connectome_entropy", 0.0)),
            "valence": float(metrics.get("sie_v2_valence_01", 0.0)),
        }

        tpls: List[str] = list(templates or [])
        if tpls:
            tpl = tpls[int(step) % len(tpls)]
            try:
                return tpl.format(**ctx)
            except Exception:
                # fall through to final summary fallback
                pass

        # 3) Final fallback to keyword summary
        return (summary or "").strip() or "."
    except Exception:
        return ""]]></content>
    </file>
    <file>
      <path>cognition/speaker.py</path>
      <content><![CDATA[from __future__ import annotations

"""
Cognition - speaker gating and scoring (Phase 3 move-only).

Behavior-preserving helpers extracted from Nexus.run():
- Gating decision based on B1 spike and valence threshold.
- Novelty-IDF computation and emission score calculation.

No logging or IO; pure functions only.
"""

from typing import Callable, Dict, Iterable, Optional, Tuple


def should_speak(valence_v2: float, spike: bool, valence_thresh: float) -> Tuple[bool, Optional[str]]:
    """
    Decide whether to speak this tick.

    Mirrors Nexus policy:
    - Must have a topology spike (b1_spike == True).
    - Valence must be >= threshold.
    - Only logs suppression for low_valence; absence of spike is silent.

    Returns:
        (can_speak, reason)
        reason is "low_valence" when valence is below threshold, else None.
    """
    if not spike:
        return False, None
    if valence_v2 >= float(valence_thresh):
        return True, None
    return False, "low_valence"


def novelty_and_score(
    speech: str,
    lexicon: Dict[str, int],
    doc_count: int,
    tokenizer: Callable[[str], Iterable[str]],
    composer_k: float,
    valence_v2: float,
) -> Tuple[float, float]:
    """
    Compute composer-local novelty IDF factor and output score.

    Equivalent to inline Nexus logic:
      novelty_idf = IDF(emitted_tokens; lexicon, doc_count)
      score_out = valence_v2 * (novelty_idf ** composer_k)

    Robust to errors: falls back to (1.0, valence_v2) if anything fails.
    """
    novelty_idf = 1.0
    try:
        try:
            from fum_rt.io.lexicon.idf import compute_idf_scale as _compute_idf_scale
        except Exception:
            _compute_idf_scale = None

        tokens = []
        try:
            tokens = list(set(tokenizer(speech)))
        except Exception:
            tokens = []

        if _compute_idf_scale is not None:
            novelty_idf = float(
                _compute_idf_scale(
                    tokens,
                    dict(lexicon or {}),
                    int(doc_count or 0),
                    default=1.0,
                    min_scale=0.5,
                    max_scale=2.0,
                )
            )
    except Exception:
        novelty_idf = 1.0

    try:
        k = float(composer_k)
    except Exception:
        k = 0.0

    try:
        val = float(valence_v2)
    except Exception:
        val = 0.0

    try:
        score_out = float(val * (novelty_idf ** k))
    except Exception:
        score_out = float(val)

    return novelty_idf, score_out


__all__ = ["should_speak", "novelty_and_score"]]]></content>
    </file>
    <file>
      <path>cognition/stimulus.py</path>
      <content><![CDATA[from __future__ import annotations

"""
Cognition - stimulus mapping (Phase 3 move-only).

Deterministic, stateless symbol→group mapping used by Nexus ingestion.
Behavior preserved: identical arithmetic hash and iteration order.
"""

from typing import Dict, List, Optional


def symbols_to_indices(
    text: str,
    stim_group_size: int,
    stim_max_symbols: int,
    N: int,
    reverse_map: Optional[Dict[int, str]] = None,
) -> List[int]:
    """
    Deterministic mapping from input symbols to neuron indices.

    Parameters:
        text: source string to stimulate
        stim_group_size: number of neurons per unique symbol
        stim_max_symbols: max number of unique symbols to map per call
        N: total neuron count (bounds the index space)
        reverse_map: optional dict to populate with index->symbol for first-claiming symbols

    Returns:
        List of neuron indices (may contain duplicates if group_size overlaps across symbols).
    """
    try:
        g = int(max(1, int(stim_group_size)))
        max_syms = int(max(1, int(stim_max_symbols)))
        N_int = int(N)
        out: List[int] = []
        seen = set()
        for ch in str(text):
            if ch in seen:
                continue
            seen.add(ch)
            code = ord(ch)
            base = (code * 1315423911) % N_int
            for j in range(g):
                idx = int((base + j * 2654435761) % N_int)
                out.append(idx)
                if isinstance(reverse_map, dict) and idx not in reverse_map:
                    reverse_map[idx] = ch
            if len(seen) >= max_syms:
                break
        return out
    except Exception:
        return []]]></content>
    </file>
    <file>
      <path>lexicon/idf.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
IDF-based novelty scaling helpers for lexicon-driven runtime.

Design constraints:
- Pure functions, no side-effects. Safe to import anywhere.
- Stable under empty inputs: returns default scale (1.0) to preserve behavior.
- Bounded output: clamp to [min_scale, max_scale] for predictable gating.
- Mirrors Nexus expectations: caller multiplies by novelty_idf_gain and may clamp again.
"""

from typing import Iterable, Mapping
import math

def _safe_log(x: float) -> float:
    try:
        return math.log(x) if x > 0 else 0.0
    except Exception:
        return 0.0

def idf(df: int, doc_count: int) -> float:
    """
    Compute standard IDF with +1 smoothing:
        idf = 1 + ln( (doc_count + 1) / (df + 1) )
    Returns >= 0.0; equals 1.0 when df ≈ doc_count.
    """
    try:
        dc = max(0, int(doc_count))
        dfv = max(0, int(df))
        return 1.0 + _safe_log((dc + 1.0) / (dfv + 1.0))
    except Exception:
        return 1.0

def compute_idf_scale(tokens: Iterable[str], lexicon: Mapping[str, int], doc_count: int, default: float = 1.0, min_scale: float = 0.5, max_scale: float = 2.0) -> float:
    """
    Compute a bounded novelty scale from token set and a DF-style lexicon.

    Parameters:
    - tokens: Iterable of tokens observed this tick
    - lexicon: Mapping token -> document frequency (DF)
    - doc_count: Total number of documents/messages observed so far
    - default: Fallback scale when inputs are empty or invalid
    - min_scale, max_scale: Output clamp bounds

    Returns:
    - Scale in [min_scale, max_scale], or default if insufficient information
    """
    try:
        if tokens is None:
            return float(default)
        toks = {str(t).lower() for t in tokens if str(t).strip()}
        if not toks:
            return float(default)
        if not isinstance(lexicon, Mapping) or len(lexicon) == 0:
            return float(default)
        dc = max(0, int(doc_count))
        if dc <= 0:
            return float(default)
        # Compute mean IDF across unique tokens for a smooth, low-variance scale
        s = 0.0
        n = 0
        for w in toks:
            dfv = int(lexicon.get(w, 0))
            s += idf(dfv, dc)
            n += 1
        if n == 0:
            return float(default)
        mean_idf = s / float(n)
        # Bound per runtime expectations
        if mean_idf < float(min_scale):
            return float(min_scale)
        if mean_idf > float(max_scale):
            return float(max_scale)
        return float(mean_idf)
    except Exception:
        return float(default)

__all__ = ["idf", "compute_idf_scale"]]]></content>
    </file>
    <file>
      <path>lexicon/phrase_bank_min.json</path>
      <content><![CDATA[{
  "say": [
    "Topology discovery: {keywords}",
    "Observation: {top1}, {top2} (vt={vt_entropy:.2f}, v={valence:.2f})",
    "Emergent structure: {keywords} (b1_z={b1_z:.2f})",
    "Exploration reveals {top1} linked to {top2} (coverage={vt_coverage:.2f})",
    "Cohesion={cohesion_components}, entropy={connectome_entropy:.2f} - {keywords}",
    "Learning: {top1}, {top2}, coherence rising (v={valence:.2f})",
    "ADC map expanding near {top1} and {top2} (vt={vt_entropy:.2f})",
    "Novelty favored: {keywords} (valence={valence:.2f})",
    "Stability-window gain with {top1} ↔ {top2} (b1_z={b1_z:.2f})",
    "Self-speak: {keywords}"
  ]
}]]></content>
    </file>
    <file>
      <path>lexicon/store.py</path>
      <content><![CDATA["""
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


__all__ = ["load_phrase_templates", "load_lexicon", "save_lexicon"]]]></content>
    </file>
    <file>
      <path>logging/rolling_jsonl.py</path>
      <content><![CDATA["""
Rolling JSONL writer with bounded main file and archival segments.

- Maintains a capped "active" JSONL file (e.g., events.jsonl, utd_events.jsonl).
- When the active file exceeds the configured size or line cap, the oldest lines
  are streamed into an archive segment and the active file is rewritten to keep
  only the newest tail (rolling buffer).
- Archive segments live under: <run_dir>/archived/<YYYYMMDD_HHMMSS>/<base_name>
  Example: runs/<ts>/archived/20250815_120828/events.jsonl
- When the current archive segment exceeds its cap, a new timestamped segment
  directory is created and subsequent archival lines are appended there.

Configuration (env):
- For events.jsonl (category="EVENTS"):
    FUM_EVENTS_MAX_MB                  (default: 256)
    FUM_EVENTS_MAX_LINES               (default: unset; bytes cap used)
    FUM_EVENTS_ARCHIVE_SEGMENT_MB      (default: 512)
    FUM_EVENTS_ARCHIVE_SEGMENT_LINES   (default: unset; bytes cap used)
- For utd_events.jsonl (category="UTD"):
    FUM_UTD_MAX_MB                     (default: 256)
    FUM_UTD_MAX_LINES                  (default: unset; bytes cap used)
    FUM_UTD_ARCHIVE_SEGMENT_MB         (default: 512)
    FUM_UTD_ARCHIVE_SEGMENT_LINES      (default: unset; bytes cap used)
- Global:
    FUM_LOG_ROLL_CHECK_EVERY           (default: 200)  # enforce cadence (per write)

Notes:
- Uses a cross-process advisory lock via <base_path>.lock to serialize trimming with writers.
- Writers should not hold persistent file handles; always append per call (MacroEmitter, UTD updated).
"""

from __future__ import annotations

import io
import os
import time
import threading
from typing import Optional, Tuple

try:
    import fcntl as _fcntl
except Exception:  # non-posix fallback (no-op locks)
    _fcntl = None


def _now_ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _is_ts_dir(name: str) -> bool:
    # YYYYMMDD_HHMMSS
    if len(name) != 15:
        return False
    d, u = name.split("_", 1) if "_" in name else ("", "")
    return d.isdigit() and u.isdigit() and len(d) == 8 and len(u) == 6


class RollingJsonlWriter:
    """
    Append-only JSONL writer with rolling buffer and archival segments.

    Usage:
        w = RollingJsonlWriter("/path/to/events.jsonl")
        w.write_line('{"msg":"hello"}')
    """

    def __init__(
        self,
        base_path: str,
        *,
        max_main_bytes: Optional[int] = None,
        max_main_lines: Optional[int] = None,
        archive_dir: Optional[str] = None,
        archive_segment_max_bytes: Optional[int] = None,
        archive_segment_max_lines: Optional[int] = None,
        check_every: Optional[int] = None,
    ) -> None:
        self.base_path = os.path.abspath(base_path)
        _ensure_dir(os.path.dirname(self.base_path))
        self.lock_path = self.base_path + ".lock"
        self._local_lock = threading.Lock()

        base_name = os.path.basename(self.base_path).lower()
        if base_name == "events.jsonl":
            cat = "EVENTS"
        elif "utd" in base_name:
            cat = "UTD"
        else:
            cat = "LOG"

        # Defaults via env (prefer bytes caps unless specific line caps are set)
        def _env_int(name: str, default: Optional[int]) -> Optional[int]:
            v = os.environ.get(name, None)
            if v is None or str(v).strip() == "":
                return default
            try:
                return int(v)
            except Exception:
                return default

        if max_main_bytes is None:
            if cat == "EVENTS":
                max_main_bytes = _env_int("FUM_EVENTS_MAX_MB", 256)
            elif cat == "UTD":
                max_main_bytes = _env_int("FUM_UTD_MAX_MB", 256)
            else:
                max_main_bytes = _env_int("FUM_LOG_MAX_MB", 128)
            max_main_bytes = int(max_main_bytes) * 1024 * 1024 if max_main_bytes else None

        if max_main_lines is None:
            if cat == "EVENTS":
                max_main_lines = _env_int("FUM_EVENTS_MAX_LINES", None)
            elif cat == "UTD":
                max_main_lines = _env_int("FUM_UTD_MAX_LINES", None)
            else:
                max_main_lines = _env_int("FUM_LOG_MAX_LINES", None)

        if archive_dir is None:
            archive_dir = os.path.join(os.path.dirname(self.base_path), "archived")
        self.archive_dir = archive_dir

        if archive_segment_max_bytes is None:
            if cat == "EVENTS":
                archive_segment_max_bytes = _env_int("FUM_EVENTS_ARCHIVE_SEGMENT_MB", 512)
            elif cat == "UTD":
                archive_segment_max_bytes = _env_int("FUM_UTD_ARCHIVE_SEGMENT_MB", 512)
            else:
                archive_segment_max_bytes = _env_int("FUM_LOG_ARCHIVE_SEGMENT_MB", 256)
            archive_segment_max_bytes = (
                int(archive_segment_max_bytes) * 1024 * 1024 if archive_segment_max_bytes else None
            )

        if archive_segment_max_lines is None:
            if cat == "EVENTS":
                archive_segment_max_lines = _env_int("FUM_EVENTS_ARCHIVE_SEGMENT_LINES", None)
            elif cat == "UTD":
                archive_segment_max_lines = _env_int("FUM_UTD_ARCHIVE_SEGMENT_LINES", None)
            else:
                archive_segment_max_lines = _env_int("FUM_LOG_ARCHIVE_SEGMENT_LINES", None)

        self.max_main_bytes = max_main_bytes
        self.max_main_lines = max_main_lines
        self.archive_segment_max_bytes = archive_segment_max_bytes
        self.archive_segment_max_lines = archive_segment_max_lines

        if check_every is None:
            check_every = _env_int("FUM_LOG_ROLL_CHECK_EVERY", 200) or 200
        self._check_every = int(check_every)
        self._ops = 0

    # ------------- public -------------
    def write_line(self, line: str) -> None:
        data = (line.rstrip("\n") + "\n").encode("utf-8", errors="ignore")
        with self._local_lock:
            with self._acquire_lock():
                # append
                with open(self.base_path, "ab") as fh:
                    fh.write(data)
                self._ops += 1
                if (self._ops % self._check_every) == 0:
                    self._enforce()

    # ------------- internals -------------
    def _acquire_lock(self):
        class _Locker:
            def __init__(self, p: str) -> None:
                self.p = p
                self.fh = None

            def __enter__(self):
                _ensure_dir(os.path.dirname(self.p))
                self.fh = open(self.p, "a+")
                if _fcntl is not None:
                    _fcntl.flock(self.fh.fileno(), _fcntl.LOCK_EX)
                return self

            def __exit__(self, exc_type, exc, tb):
                try:
                    if _fcntl is not None and self.fh is not None:
                        _fcntl.flock(self.fh.fileno(), _fcntl.LOCK_UN)
                finally:
                    try:
                        if self.fh:
                            self.fh.close()
                    except Exception:
                        pass

        return _Locker(self.lock_path)

    def _enforce(self) -> None:
        """Trim oldest lines to keep main file under configured cap and move trimmed lines to archive."""
        try:
            size = os.path.getsize(self.base_path)
        except Exception:
            return

        # Prefer bytes cap unless a line cap is explicitly configured
        if self.max_main_lines and self.max_main_lines > 0:
            self._enforce_by_lines(self.max_main_lines)
        elif self.max_main_bytes and size > self.max_main_bytes:
            to_remove = size - self.max_main_bytes
            self._trim_oldest_bytes_to_archive(to_remove)

    def _enforce_by_lines(self, keep_last_lines: int) -> None:
        try:
            # Count lines
            total = 0
            with open(self.base_path, "rb") as fh:
                for _ in fh:
                    total += 1
            if total <= keep_last_lines:
                return
            to_remove = total - keep_last_lines

            # Stream: first 'to_remove' lines -> archive; remainder -> temp; then replace
            self._stream_archive_and_tail(to_remove_lines=to_remove)
        except Exception:
            return

    def _trim_oldest_bytes_to_archive(self, remove_bytes: int) -> None:
        if remove_bytes <= 0:
            return
        # Best-effort: move enough whole lines to cover remove_bytes
        moved = 0
        try:
            seg_fh, _ = self._open_archive_for_append()
            try:
                tmp_path = self.base_path + ".tmp"
                with open(self.base_path, "rb") as src, open(tmp_path, "wb") as dst:
                    for line in src:
                        if moved < remove_bytes:
                            # ensure we rotate segment if needed
                            self._seg_write(seg_fh, line)
                            moved += len(line)
                        else:
                            dst.write(line)
                # Replace atomically
                os.replace(tmp_path, self.base_path)
            finally:
                try:
                    if seg_fh:
                        seg_fh.close()
                except Exception:
                    pass
        except Exception:
            return

    def _stream_archive_and_tail(self, to_remove_lines: int) -> None:
        if to_remove_lines <= 0:
            return
        removed = 0
        try:
            seg_fh, _ = self._open_archive_for_append()
            try:
                tmp_path = self.base_path + ".tmp"
                with open(self.base_path, "rb") as src, open(tmp_path, "wb") as dst:
                    for line in src:
                        if removed < to_remove_lines:
                            self._seg_write(seg_fh, line)
                            removed += 1
                        else:
                            dst.write(line)
                os.replace(tmp_path, self.base_path)
            finally:
                try:
                    if seg_fh:
                        seg_fh.close()
                except Exception:
                    pass
        except Exception:
            return

    # ----- archive segment helpers -----
    def _open_archive_for_append(self) -> Tuple[io.BufferedWriter, str]:
        """
        Return a file handle opened for appending to the current archive segment and the segment dir.
        Creates archive dir/segment as needed.
        """
        _ensure_dir(self.archive_dir)
        # Select latest timestamp directory or create new
        try:
            dirs = [d for d in os.listdir(self.archive_dir) if _is_ts_dir(d)]
        except Exception:
            dirs = []
        if dirs:
            dirs.sort()
            seg_dir = os.path.join(self.archive_dir, dirs[-1])
        else:
            seg_dir = os.path.join(self.archive_dir, _now_ts())
            _ensure_dir(seg_dir)

        # Archive filename mirrors base filename inside the segment directory
        arch_file = os.path.join(seg_dir, os.path.basename(self.base_path))
        _ensure_dir(os.path.dirname(arch_file))

        # If current segment overflows max, rotate to a new segment directory
        if self._segment_full(arch_file):
            seg_dir = os.path.join(self.archive_dir, _now_ts())
            _ensure_dir(seg_dir)
            arch_file = os.path.join(seg_dir, os.path.basename(self.base_path))

        fh = open(arch_file, "ab")
        return fh, seg_dir

    def _segment_full(self, arch_file: str) -> bool:
        try:
            size = os.path.getsize(arch_file)
        except Exception:
            size = 0
        # bytes-based check first
        if self.archive_segment_max_bytes and self.archive_segment_max_bytes > 0:
            if size >= self.archive_segment_max_bytes:
                return True
        # optional lines-based check
        if self.archive_segment_max_lines and self.archive_segment_max_lines > 0:
            try:
                cnt = 0
                with open(arch_file, "rb") as fh:
                    for _ in fh:
                        cnt += 1
                if cnt >= self.archive_segment_max_lines:
                    return True
            except Exception:
                return False
        return False

    def _seg_write(self, seg_fh: io.BufferedWriter, line: bytes) -> None:
        # Append line to current segment, rotate if segment crosses cap
        try:
            seg_fh.write(line)
            seg_fh.flush()
        except Exception:
            return
        # If segment now full, open a new one for subsequent writes
        try:
            if self._segment_full(seg_fh.name):  # type: ignore[attr-defined]
                seg_fh.close()
                new_fh, _ = self._open_archive_for_append()
                seg_fh.__dict__.update(new_fh.__dict__)  # swap internals (best-effort)
        except Exception:
            pass


# ---------- Logging handler integration ----------

import logging


class RollingJsonlHandler(logging.Handler):
    """
    logging.Handler that writes formatted JSON lines to a bounded rolling JSONL file.
    """
    def __init__(self, path: str) -> None:
        super().__init__(level=logging.INFO)
        self._writer = RollingJsonlWriter(path)
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._writer.write_line(msg)
        except Exception:
            # Avoid crashing logging subsystem
            pass

class RollingZipJsonlHandler(logging.Handler):
    """
    logging.Handler that writes formatted JSON lines to a zip-spooled JSONL buffer.
    The buffer is truncated when it exceeds the configured threshold and compressed
    into a .zip archive adjacent to the buffer file (e.g., events.jsonl -> events.zip).
    """
    def __init__(self, path: str) -> None:
        super().__init__(level=logging.INFO)
        # Prefer zip spooler for bounded disk pressure
        self._writer = RollingZipJsonlWriter(path)  # type: ignore[name-defined]
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._writer.write_line(msg)
        except Exception:
            # Avoid crashing logging subsystem
            pass

__all__ = ["RollingJsonlWriter", "RollingJsonlHandler", "RollingZipJsonlWriter", "RollingZipJsonlHandler"]
# ---------- Zip spool writer (optional) ----------
# Lightweight, void-faithful spooler that compresses the active JSONL buffer into a growing .zip
# once it exceeds a bounded threshold, then truncates the buffer. Keeps a tiny in-process ring
# for quick peeks. Uses RollingJsonlWriter's advisory lock to coordinate with other writers.
import zipfile as _zipfile  # stdlib

class RollingZipJsonlWriter:
    """
    Zip spooler for JSONL:
    - Appends lines to a small active buffer file (base_path)
    - When buffer exceeds max_buffer_bytes, compresses it into <base_name>.zip (append mode)
      under the same directory and truncates the buffer to zero
    - Tracks coarse stats for UI/status reporting (entries, sizes)
    - Thread-safe; coordinates with other processes via RollingJsonlWriter's lock
    """

    def __init__(
        self,
        base_path: str,
        *,
        max_buffer_bytes: int | None = None,
        ring_bytes: int | None = None,
        zip_path: str | None = None,
    ) -> None:
        self.base_path = os.path.abspath(base_path)
        _ensure_dir(os.path.dirname(self.base_path))
        # Defaults (env-overridable)
        try:
            if max_buffer_bytes is None:
                max_buffer_bytes = int(os.getenv("FUM_ZIP_BUFFER_BYTES", "1048576"))  # 1 MiB
        except Exception:
            max_buffer_bytes = 1_048_576
        try:
            if ring_bytes is None:
                ring_bytes = int(os.getenv("FUM_ZIP_RING_BYTES", "65536"))  # 64 KiB
        except Exception:
            ring_bytes = 65_536
        self.max_buffer_bytes = int(max(32 * 1024, max_buffer_bytes or 1_048_576))
        self._ring_cap = int(max(1024, ring_bytes or 65_536))
        self._ring = bytearray()
        # Zip path next to base_path (events.jsonl -> events.zip)
        if not zip_path:
            stem = os.path.splitext(os.path.basename(self.base_path))[0]
            zip_path = os.path.join(os.path.dirname(self.base_path), f"{stem}.zip")
        self.zip_path = os.path.abspath(zip_path)

        # Use RollingJsonlWriter with huge caps to avoid its archival path interfering
        # (we rely on the zip spool rotation below)
        self._writer = RollingJsonlWriter(
            self.base_path,
            max_main_bytes=10**12,              # effectively disable
            max_main_lines=None,
            archive_dir=os.path.join(os.path.dirname(self.base_path), "archived"),
            archive_segment_max_bytes=None,
            archive_segment_max_lines=None,
            check_every=2_147_483_647,          # effectively disable
        )
        self._zip_entries_cache: int | None = None
        self._local_lock = threading.Lock()

    def write_line(self, line: str) -> None:
        # Append line (delegates to rolling writer for atomic append)
        self._writer.write_line(line)
        # Update in-process ring
        try:
            data = (line.rstrip("\n") + "\n").encode("utf-8", errors="ignore")
            self._ring.extend(data)
            if len(self._ring) > self._ring_cap:
                # keep last _ring_cap bytes
                self._ring[:] = self._ring[-self._ring_cap:]
        except Exception:
            pass

        # Rotate to zip if buffer exceeds threshold (guarded by advisory lock)
        try:
            with self._writer._acquire_lock():  # type: ignore[attr-defined]
                try:
                    size = os.path.getsize(self.base_path)
                except Exception:
                    size = 0
                if size >= self.max_buffer_bytes:
                    # Read buffer
                    try:
                        with open(self.base_path, "rb") as fh:
                            buf = fh.read()
                    except Exception:
                        buf = b""
                    if buf:
                        arcname = f"{os.path.basename(self.base_path)}.{_now_ts()}.jsonl"
                        try:
                            with _zipfile.ZipFile(self.zip_path, mode="a", compression=_zipfile.ZIP_DEFLATED) as zf:
                                zf.writestr(arcname, buf)
                                # Seed entries cache if unknown
                                try:
                                    if self._zip_entries_cache is None:
                                        self._zip_entries_cache = 0
                                    self._zip_entries_cache += 1
                                except Exception:
                                    pass
                        except Exception:
                            # best-effort: do not abort rotation
                            pass
                        # Truncate buffer
                        try:
                            with open(self.base_path, "wb") as fh2:
                                fh2.write(b"")
                        except Exception:
                            pass
        except Exception:
            # best-effort; avoid throwing on contentions
            pass

    def stats(self) -> dict:
        """
        Return coarse spool statistics for status reporting:
          - buffer_bytes: size of active JSONL buffer
          - zip_bytes: size of the zip archive file
          - zip_entries: count of archived segments (approximate)
          - ring_bytes: size of in-process ring buffer
        """
        try:
            buffer_bytes = os.path.getsize(self.base_path)
        except Exception:
            buffer_bytes = 0
        try:
            zip_bytes = os.path.getsize(self.zip_path)
        except Exception:
            zip_bytes = 0
        # If entries unknown, estimate by inspecting the zip once
        if self._zip_entries_cache is None:
            try:
                if os.path.exists(self.zip_path):
                    with _zipfile.ZipFile(self.zip_path, mode="r") as zf:
                        self._zip_entries_cache = len(zf.namelist())
                else:
                    self._zip_entries_cache = 0
            except Exception:
                self._zip_entries_cache = 0
        return {
            "buffer_bytes": int(buffer_bytes),
            "zip_bytes": int(zip_bytes),
            "zip_entries": int(self._zip_entries_cache or 0),
            "ring_bytes": int(len(self._ring)),
        }

# expose in module exports
try:
    __all__.append("RollingZipJsonlWriter")  # type: ignore[name-defined]
except Exception:
    __all__ = ["RollingJsonlWriter", "RollingJsonlHandler", "RollingZipJsonlWriter"]]]></content>
    </file>
    <file>
      <path>maps_ring.py</path>
      <content><![CDATA["""
Compatibility shim for visualization ring buffer.

Deprecated: import from 'fum_rt.io.visualization.maps_ring' instead.

Kept for transitional period to avoid breaking existing imports:
    from fum_rt.io.maps_ring import MapsRing, MapsFrame
"""

from __future__ import annotations

from fum_rt.io.visualization.maps_ring import MapsRing, MapsFrame

__all__ = ["MapsRing", "MapsFrame"]]]></content>
    </file>
    <file>
      <path>sensors/__init__.py</path>
      <content/>
    </file>
    <file>
      <path>sensors/auditory.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>sensors/somatosensory.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>sensors/symbols.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>sensors/vision.py</path>
      <content><![CDATA["""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
]]></content>
    </file>
    <file>
      <path>utd.py</path>
      <content><![CDATA[import sys, json, os
from fum_rt.io.logging.rolling_jsonl import RollingJsonlWriter
try:
    # Prefer zip spooler when available
    from fum_rt.io.logging.rolling_jsonl import RollingZipJsonlWriter  # type: ignore
except Exception:
    RollingZipJsonlWriter = None  # type: ignore

class UTD:
    """Universal Transduction Decoder.
    Emits opportunistic outputs (stdout + file sink) and supports a simple macro board.

    API
    - emit_text(payload: dict, score: float=1.0)
    - register_macro(name: str, meta: dict | None=None) -> bool
    - list_macros() -> list[str]
    - emit_macro(name: str, args: dict | None=None, score: float=1.0)
    """
    def __init__(self, run_dir: str):
        self.run_dir = run_dir
        os.makedirs(self.run_dir, exist_ok=True)
        self.path = os.path.join(self.run_dir, 'utd_events.jsonl')
        # Prefer zip-spooled writer to bound disk pressure; fallback to rolling JSONL
        use_zip = True
        try:
            # Allow explicit opt-out via env
            use_zip = str(os.getenv("FUM_ZIP_SPOOL", "1")).strip().lower() in ("1", "true", "yes", "on", "y")
        except Exception:
            use_zip = True
        try:
            if use_zip and RollingZipJsonlWriter is not None:  # type: ignore
                self._writer = RollingZipJsonlWriter(self.path)  # type: ignore
            else:
                self._writer = RollingJsonlWriter(self.path)
        except Exception:
            # Safe fallback
            self._writer = RollingJsonlWriter(self.path)
        # Macro registry and on-disk macro board for persistence
        self._macro_registry = {}
        self._macro_board_path = os.path.join(self.run_dir, 'macro_board.json')
        # Eager-load persisted macro board if present
        try:
            if os.path.exists(self._macro_board_path):
                with open(self._macro_board_path, 'r', encoding='utf-8') as fh:
                    reg = json.load(fh)
                    if isinstance(reg, dict):
                        for name, meta in reg.items():
                            self._macro_registry[str(name)] = meta if isinstance(meta, dict) else {}
        except Exception:
            # do not fail runtime if file is corrupt
            pass

    def register_macro(self, name: str, meta: dict | None=None) -> bool:
        """Register a macro key with optional metadata; idempotent. Persists to macro_board.json."""
        try:
            self._macro_registry[name] = meta or {}
            try:
                self._persist_macro_board()
            except Exception:
                pass
            return True
        except Exception:
            return False

    def list_macros(self):
        """List available macro keys."""
        try:
            return sorted(self._macro_registry.keys())
        except Exception:
            return []

    def _persist_macro_board(self):
        """Write macro registry to run_dir/macro_board.json."""
        try:
            with open(self._macro_board_path, 'w', encoding='utf-8') as fh:
                json.dump(self._macro_registry, fh, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def emit_text(self, payload: dict, score: float=1.0):
        rec = {'type': 'text', 'payload': payload, 'score': float(score)}
        print("[UTD] text:", payload, f"(score={score:.3f})")
        try:
            line = json.dumps(rec, ensure_ascii=False)
            self._writer.write_line(line)
        except Exception:
            # keep stdout emission even if file writing fails
            pass

    def emit_macro(self, name: str, args: dict | None=None, score: float=1.0):
        """
        Emit a macro event. If the macro key is not registered, auto-register it
        (and persist to macro_board.json) to avoid breaking the runtime.
        """
        if name not in self._macro_registry:
            # go through register path so persistence occurs
            self.register_macro(name, {})
        rec = {'type': 'macro', 'macro': name, 'args': (args or {}), 'score': float(score)}
        print(f"[UTD] macro:{name}", (args or {}), f"(score={score:.3f})")
        try:
            line = json.dumps(rec, ensure_ascii=False)
            self._writer.write_line(line)
        except Exception:
            # keep stdout emission even if file writing fails
            pass

    def close(self):
        try:
            try:
                self._persist_macro_board()
            except Exception:
                pass
            # RollingJsonlWriter does not keep a persistent file handle; nothing to close.
        except Exception:
            pass
]]></content>
    </file>
    <file>
      <path>ute.py</path>
      <content><![CDATA[
import sys, time, queue, threading, os, json

class UTE:
    """Universal Temporal Encoder.
    Feeds inbound messages into a queue the Nexus can poll every tick.
    Sources implemented: stdin (lines) and synthetic 'tick' generator.
    """
    def __init__(self, use_stdin=True, inbox_path=None):
        self.q = queue.Queue(maxsize=1024)
        self._stop = threading.Event()
        self.use_stdin = use_stdin
        self._threads = []
        # Optional run-local chat inbox (JSONL), e.g. runs/<ts>/chat_inbox.jsonl
        self.inbox_path = inbox_path
        self._inbox_size = 0

    def start(self):
        if self.use_stdin:
            t = threading.Thread(target=self._stdin_reader, daemon=True)
            t.start()
            self._threads.append(t)
        # Optional chat inbox tailer
        if self.inbox_path:
            t3 = threading.Thread(target=self._inbox_reader, daemon=True)
            t3.start()
            self._threads.append(t3)
        # Always run a synthetic ticker as a heartbeat
        t2 = threading.Thread(target=self._ticker, daemon=True)
        t2.start()
        self._threads.append(t2)

    def stop(self):
        self._stop.set()

    def _stdin_reader(self):
        for line in sys.stdin:
            if self._stop.is_set(): break
            line = line.strip()
            if line:
                self.q.put({'type': 'text', 'msg': line})

    def _inbox_reader(self):
        # Tail a JSONL chat inbox file (appended by dashboard/chat UI)
        while not self._stop.is_set():
            try:
                path = self.inbox_path
                if not path or not os.path.exists(path):
                    time.sleep(0.5)
                    continue
                size = os.path.getsize(path)
                # handle truncation/rotation
                if size < self._inbox_size:
                    self._inbox_size = 0
                if size == self._inbox_size:
                    time.sleep(0.5)
                    continue
                with open(path, "rb") as f:
                    f.seek(self._inbox_size)
                    data = f.read(size - self._inbox_size)
                self._inbox_size = size
                text = data.decode("utf-8", errors="ignore")
                for line in text.splitlines():
                    s = line.strip()
                    if not s:
                        continue
                    try:
                        rec = json.loads(s)
                    except Exception:
                        rec = {"type": "text", "msg": s}
                    if isinstance(rec, dict):
                        if rec.get("type") == "text" and "msg" in rec:
                            self.q.put({"type": "text", "msg": str(rec.get("msg"))})
                        else:
                            # Allow passthrough of structured events if provided
                            self.q.put(rec)
            except Exception:
                # Keep runtime alive on any error
                time.sleep(0.5)

    def _ticker(self):
        # 1 Hz ticker (used as heartbeat input)
        while not self._stop.is_set():
            self.q.put({'type':'tick', 'msg':'tick'})
            time.sleep(1.0)

    def poll(self, max_items=32):
        out = []
        while len(out) < max_items:
            try:
                out.append(self.q.get_nowait())
            except queue.Empty:
                break
        return out
]]></content>
    </file>
    <file>
      <path>visualization/__init__.py</path>
      <content><![CDATA["""
Visualization transport primitives.

- maps_ring: bounded, drop-oldest ring buffer for maps/frame payloads
- websocket_server: bounded WebSocket forwarder for maps frames
"""
from .maps_ring import MapsRing, MapsFrame  # re-export
from .websocket_server import MapsWebSocketServer  # re-export]]></content>
    </file>
    <file>
      <path>visualization/maps_ring.py</path>
      <content><![CDATA["""
Maps frames ring buffer (drop-oldest, thread-safe, void-faithful).

Canonical location: fum_rt.io.visualization.maps_ring

Purpose
- Provide a tiny, bounded ring for maps frames (header+payload) with drop-oldest semantics.
- Decouples producers (telemetry/core engine) from consumers (UI/websocket) without scans.
- O(1) amortized operations; no full-buffer copies; copies only payload bytes as provided.

Contract
- Frame header schema is producer-defined; commonly:
  {topic, ver?, tick, n, shape, channels, dtype, endianness, stats, ...}
- Payload is a bytes-like buffer; typically planar blocks (e.g., Float32 LE: heat|exc|inh).

Usage
- nx._maps_ring = MapsRing(capacity=int(os.getenv("MAPS_RING", 3)))
- Producer: nx._maps_ring.push(tick, header, payload)
- Consumer: ring.latest(), ring.drain(max_items)

Security / Backpressure
- Always drops the oldest on overflow.
- Readers can choose to read only latest() to avoid client backlog.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import threading


@dataclass(frozen=True)
class MapsFrame:
    tick: int
    header: Dict[str, Any]
    payload: bytes
    seq: int  # monotonically increasing sequence id


class MapsRing:
    """
    Bounded, thread-safe ring buffer for maps frames.

    - push(): appends a frame, dropping the oldest when at capacity.
    - latest(): returns the newest frame or None.
    - drain(max_items): returns up to max_items frames from oldest to newest.
      Use latest() if you only need the most recent frame to minimize bandwidth.
    """

    __slots__ = ("capacity", "_lock", "_buf", "_seq", "_drop_count")

    def __init__(self, capacity: int = 3) -> None:
        self.capacity = max(1, int(capacity))
        self._lock = threading.Lock()
        self._buf: List[MapsFrame] = []
        self._seq = 0
        self._drop_count = 0

    def push(self, tick: int, header: Dict[str, Any], payload: bytes) -> int:
        """
        Append a frame; drop oldest on overflow.
        Returns the sequence id assigned to the inserted frame.
        """
        if not isinstance(payload, (bytes, bytearray, memoryview)):
            # Normalize to bytes once (producers should pass bytes already)
            try:
                payload = bytes(payload)  # type: ignore[assignment]
            except Exception:
                payload = b""
        with self._lock:
            self._seq += 1
            f = MapsFrame(tick=int(tick), header=dict(header or {}), payload=bytes(payload), seq=self._seq)
            if len(self._buf) >= self.capacity:
                self._buf.pop(0)
                self._drop_count += 1
            self._buf.append(f)
            return f.seq

    def latest(self) -> Optional[MapsFrame]:
        with self._lock:
            if not self._buf:
                return None
            return self._buf[-1]

    def drain(self, max_items: Optional[int] = None) -> List[MapsFrame]:
        """
        Return up to max_items frames in order (oldest..newest).
        Does not mutate the ring (non-destructive view); consumers should track seq.
        """
        with self._lock:
            if not self._buf:
                return []
            if max_items is None or max_items <= 0:
                return list(self._buf)
            return list(self._buf[-int(max_items):])

    def size(self) -> int:
        with self._lock:
            return len(self._buf)

    def dropped(self) -> int:
        """
        Returns the number of frames dropped due to overflow since creation.
        """
        with self._lock:
            return int(self._drop_count)

    def __len__(self) -> int:
        return self.size()


__all__ = ["MapsRing", "MapsFrame"]]]></content>
    </file>
    <file>
      <path>visualization/websocket_server.py</path>
      <content><![CDATA["""
Maps frames WebSocket forwarder (bounded, drop-oldest, void-faithful).

Canonical location: fum_rt.io.visualization.websocket_server

Purpose
- Serve UI consumers with the latest maps/frame payload from a bounded ring.
- Backpressure-safe: each client receives only the newest frame; old frames are dropped.
- Local-first: defaults to 127.0.0.1 binding; configurable via args/env.

Dependencies
- Optional: 'websockets' Python package (asyncio-based). If unavailable, this module is inert.

Env (defaults shown)
- MAPS_FPS=10                # >0 = limit; 0 = off; <0 = unlimited (tests/bench); sends at most this many frames per second when >0
- WS_MAX_CONN=2              # maximum concurrent WebSocket clients
- WS_ALLOW_ORIGIN=           # comma-separated origins; if empty, all origins allowed

Transport format
- Two-message sequence per frame:
  1) Text frame: JSON dump of header dict (augmented with dtype/ver/quant/etc. by producer)
  2) Binary frame: raw payload bytes (u8 or f32 LE as dictated by header['dtype'])

Notes
- This module does not mutate frames; it forwards exactly what producers pushed to the ring.
- For RGB visualization, typical mapping is RGB = [exc, heat, inh] client-side.
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
from typing import Any, Dict, Optional, Set, Callable

try:
    import websockets  # type: ignore
    from websockets.server import WebSocketServerProtocol  # type: ignore
except Exception:  # pragma: no cover
    websockets = None
    WebSocketServerProtocol = object  # type: ignore

from fum_rt.io.visualization.maps_ring import MapsRing, MapsFrame


class MapsWebSocketServer:
    """
    Bounded WebSocket forwarder for maps frames.

    Usage:
      ring = MapsRing(capacity=3)
      ws = MapsWebSocketServer(ring, host="127.0.0.1", port=8888)
      ws.start()
      ...
      ws.stop()
    """

    __slots__ = (
        "ring",
        "host",
        "port",
        "max_conn",
        "allow_origins",
        "fps",
        "_running",
        "_thread",
        "_clients",
        "_loop",
        "_server",
        "_last_seq_sent",
        "_on_error",
    )

    def __init__(
        self,
        ring: MapsRing,
        host: str = "127.0.0.1",
        port: int = 8765,
        *,
        max_conn: Optional[int] = None,
        allow_origins: Optional[str] = None,
        fps: Optional[float] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.ring = ring
        self.host = str(host)
        self.port = int(port)
        try:
            self.max_conn = int(max_conn if max_conn is not None else os.getenv("WS_MAX_CONN", "2"))
        except Exception:
            self.max_conn = 2
        # Comma-separated origins string or None for any
        self.allow_origins = str(allow_origins) if allow_origins is not None else os.getenv("WS_ALLOW_ORIGIN", "")
        try:
            self.fps = float(fps if fps is not None else os.getenv("MAPS_FPS", "10"))
        except Exception:
            self.fps = 10.0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._clients: Set[WebSocketServerProtocol] = set()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._server = None
        self._last_seq_sent: int = 0
        self._on_error = on_error

    # ---- Public API ----

    def start(self) -> None:
        """
        Start the WebSocket server in a background thread. No-op if 'websockets' is missing.
        """
        if websockets is None:
            self._report_error("websocket_server_start_failed: websockets package not installed")
            return
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, name="maps_ws_server", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the server and wait for the background thread to exit.
        """
        if not self._running:
            return
        self._running = False
        try:
            if self._loop is not None:
                asyncio.run_coroutine_threadsafe(self._shutdown_async(), self._loop).result(timeout=2.0)
        except Exception:
            pass
        try:
            if self._thread is not None:
                self._thread.join(timeout=2.0)
        except Exception:
            pass
        self._thread = None

    # ---- Internal ----

    def _report_error(self, msg: str) -> None:
        try:
            if self._on_error:
                self._on_error(msg)
            else:
                print("[maps_ws] " + msg, flush=True)
        except Exception:
            pass

    def _run_loop(self) -> None:
        try:
            loop = asyncio.new_event_loop()
            self._loop = loop
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._start_async())
            loop.run_forever()
        except Exception as e:
            self._report_error(f"websocket_server_loop_error: {e}")
        finally:
            try:
                if self._server is not None:
                    loop = self._loop or asyncio.get_event_loop()
                    loop.run_until_complete(self._shutdown_async())
            except Exception:
                pass

    async def _start_async(self) -> None:
        assert websockets is not None
        origins = None
        if self.allow_origins:
            try:
                origins = [o.strip() for o in self.allow_origins.split(",") if o.strip()]
                if not origins:
                    origins = None
            except Exception:
                origins = None

        self._server = await websockets.serve(  # type: ignore
            self._ws_handler,
            self.host,
            self.port,
            max_size=2**20,  # 1 MiB per message should suffice for control
            max_queue=1,     # backpressure: queue at most one message per client
            ping_interval=20,
            ping_timeout=20,
            origins=origins,
        )

        # Broadcaster loop
        asyncio.create_task(self._broadcast_loop())

    async def _shutdown_async(self) -> None:
        try:
            # Close all clients
            for ws in list(self._clients):
                try:
                    await ws.close()
                except Exception:
                    pass
            self._clients.clear()
        except Exception:
            pass
        try:
            if self._server is not None:
                self._server.close()
                await self._server.wait_closed()
        except Exception:
            pass
        try:
            loop = asyncio.get_event_loop()
            loop.stop()
        except Exception:
            pass

    async def _ws_handler(self, websocket: WebSocketServerProtocol, path: str) -> None:  # type: ignore[override]
        # Enforce max connections
        try:
            if len(self._clients) >= max(1, self.max_conn):
                await websocket.close(code=1013, reason="server_overload")  # Try again later
                return
        except Exception:
            pass

        self._clients.add(websocket)
        try:
            # Initial latest send to prime client
            await self._send_latest(websocket)
            # Then just keep the connection alive until client disconnects; no per-client loop needed
            # since broadcast loop handles sending updates to all clients.
            await websocket.wait_closed()
        except Exception:
            pass
        finally:
            try:
                self._clients.remove(websocket)
            except Exception:
                pass

    async def _broadcast_loop(self) -> None:
        # Send at most one frame per fps interval; drop-oldest by only ever sending the latest frame
        try:
            fps = float(self.fps)
        except Exception:
            fps = 10.0
        if fps < 0:
            interval = 0.0  # unlimited
        elif fps == 0:
            interval = None  # disabled
        else:
            interval = 1.0 / max(0.001, fps)

        while self._running:
            try:
                if interval is None:
                    # Emission disabled: avoid spin
                    await asyncio.sleep(0.1)
                    continue
                if not self._clients:
                    # Avoid unnecessary ring access when there are no clients
                    await asyncio.sleep(interval if interval > 0 else 0.1)
                    continue
                fr = self.ring.latest()
                if fr is not None and fr.seq != self._last_seq_sent:
                    # Broadcast header (text) then payload (binary)
                    await self._broadcast_frame(fr)
                    self._last_seq_sent = fr.seq
                # For unlimited (interval==0), yield to event loop without sleeping
                if interval > 0:
                    await asyncio.sleep(interval)
                else:
                    await asyncio.sleep(0.0)
            except Exception:
                # Keep server resilient
                await asyncio.sleep(0.05)

    async def _broadcast_frame(self, fr: MapsFrame) -> None:
        dead: Set[WebSocketServerProtocol] = set()
        # Serialize header once
        try:
            hdr_text = json.dumps(fr.header, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            # Fallback minimal header
            hdr_text = json.dumps({"topic": "maps/frame", "tick": int(fr.tick)}, separators=(",", ":"))
        for ws in list(self._clients):
            try:
                await ws.send(hdr_text)     # text frame
                await ws.send(fr.payload)   # binary frame
            except Exception:
                dead.add(ws)
        # Purge disconnected clients
        for ws in dead:
            try:
                self._clients.remove(ws)
            except Exception:
                pass

    async def _send_latest(self, ws: WebSocketServerProtocol) -> None:
        fr = self.ring.latest()
        if fr is None:
            return
        try:
            hdr_text = json.dumps(fr.header, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            hdr_text = json.dumps({"topic": "maps/frame", "tick": int(fr.tick)}, separators=(",", ":"))
        try:
            await ws.send(hdr_text)
            await ws.send(fr.payload)
        except Exception:
            pass


__all__ = ["MapsWebSocketServer"]]]></content>
    </file>
  </files>
</vdm_io>
