from __future__ import annotations

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
        return []