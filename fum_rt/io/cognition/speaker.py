from __future__ import annotations

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


__all__ = ["should_speak", "novelty_and_score"]