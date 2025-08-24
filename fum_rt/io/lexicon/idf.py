"""
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

__all__ = ["idf", "compute_idf_scale"]