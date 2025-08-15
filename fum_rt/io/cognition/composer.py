from __future__ import annotations

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
        return ""