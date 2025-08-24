"""
Runtime helper: autonomous speaking (composer + speaker gate + novelty IDF).

Behavior:
- Mirrors legacy Nexus logic for maybe_auto_speak() exactly.
- Pure runtime helper; safe fail-soft; no side-effects beyond UTD emissions and learned lexicon updates.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Set

from fum_rt.core import text_utils
from fum_rt.io.cognition.composer import compose_say_text as _compose_say_text_impl
from fum_rt.io.cognition.speaker import should_speak as _speak_gate, novelty_and_score as _novelty_and_score
from fum_rt.runtime.telemetry import macro_why_base as _telemetry_why_base


def maybe_auto_speak(
    nx: Any,
    m: Dict[str, Any],
    step: int,
    tick_tokens: Set[str],
    void_topic_symbols: Set[Any],
) -> None:
    """
    Behavior-preserving autonomous speaking based on topology spikes and valence.
    Mirrors the original Nexus block in full detail.
    """
    try:
        val_v2 = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
    except Exception:
        val_v2 = float(m.get("sie_valence_01", 0.0))
    spike = bool(m.get("b1_spike", False))

    if not getattr(nx, "speak_auto", False):
        return

    can_speak, reason = _speak_gate(val_v2, spike, float(getattr(nx, "speak_valence_thresh", 0.01)))
    if not can_speak:
        if reason == "low_valence":
            try:
                nx.logger.info(
                    "speak_suppressed",
                    extra={
                        "extra": {
                            "reason": "low_valence",
                            "val": val_v2,
                            "thresh": float(getattr(nx, "speak_valence_thresh", 0.01)),
                            "b1_z": float(m.get("b1_z", 0.0)),
                            "t": int(step),
                        }
                    },
                )
            except Exception:
                pass
        return

    # Compose; do not suppress due to lack of topic/tokens. Model controls content fully.
    seed_material = tick_tokens if tick_tokens else void_topic_symbols
    try:
        speech = _compose_say_text_impl(
            m or {},
            int(step),
            getattr(nx, "_lexicon", {}) or {},
            getattr(nx, "_ng2", {}) or {},
            getattr(nx, "_ng3", {}) or {},
            getattr(nx, "recent_text", []),
            templates=list(getattr(nx, "_phrase_templates", []) or []),
            seed_tokens=seed_material,
        ) or ""
    except Exception:
        speech = ""

    # Composer IDF gain (local to composer; does not affect dynamics)
    try:
        composer_k = float(getattr(nx, "_phase", {}).get("composer_idf_k", float(os.getenv("COMPOSER_IDF_K", "0.0"))))
    except Exception:
        composer_k = 0.0

    # Composer-local novelty IDF + score (telemetry/emitter only; does not affect dynamics)
    try:
        novelty_idf, score_out = _novelty_and_score(
            speech,
            getattr(nx, "_lexicon", {}) or {},
            int(getattr(nx, "_doc_count", 0)),
            text_utils.tokenize_text,
            float(composer_k),
            float(val_v2),
        )
    except Exception:
        novelty_idf, score_out = 0.0, float(val_v2)

    # Update learned lexicon after computing novelty (avoid self-bias in estimate)
    try:
        if not hasattr(nx, "_lexicon"):
            nx._lexicon = {}
        toks2 = text_utils.tokenize_text(speech)
        for w in set(toks2):
            nx._lexicon[w] = int(nx._lexicon.get(w, 0)) + 1
        # Ensure n-gram stores exist and update streaming n-grams
        try:
            nx._ng2
            nx._ng3
        except Exception:
            nx._ng2 = {}
            nx._ng3 = {}
        text_utils.update_ngrams(toks2, nx._ng2, nx._ng3)
    except Exception:
        pass

    # Emit macro
    try:
        why = _telemetry_why_base(nx, m, int(step))
        try:
            why["novelty_idf"] = float(novelty_idf)
            why["composer_idf_k"] = float(composer_k)
        except Exception:
            pass
        nx.utd.emit_macro(
            "say",
            {
                "text": speech,
                "why": why,
            },
            score=score_out,
        )
    except Exception:
        pass


__all__ = ["maybe_auto_speak"]