"""
Runtime helper: message ingestion and per-tick symbol/index extraction.

Provides:
- process_messages(): Mirrors legacy Nexus/runtime behavior while keeping the runtime layer modular.

Policy:
- Runtime helpers may import fum_rt.io.* and fum_rt.core.*.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Set, Tuple

from fum_rt.core import text_utils
from fum_rt.io.cognition.stimulus import symbols_to_indices as _stim_symbols_to_indices


def process_messages(nx: Any, msgs: Iterable[Dict[str, Any]]) -> Tuple[int, Set[int], Set[str], Dict[int, Any]]:
    """
    Process UTE messages:
      - Count text messages
      - Update recent_text, lexicon/ngrams, and document count
      - Build per-tick token set for IDF computations and seed selection
      - Map symbols to connectome indices via nx._symbols_to_indices (deterministic)
      - Emit each message to UTD (mirrors original timing)

    Returns: (ute_text_count, stim_idxs, tick_tokens, tick_rev_map)
    """
    ute_text_count = 0
    stim_idxs: Set[int] = set()
    tick_tokens: Set[str] = set()
    tick_rev_map: Dict[int, Any] = {}

    for m in msgs:
        try:
            if m.get("type") != "text":
                # Non-text messages are emitted to UTD as-is
                try:
                    nx.utd.emit_text(m)
                except Exception:
                    pass
                continue

            ute_text_count += 1
            # Append to rolling recent_text
            try:
                text = str(m.get("msg", ""))
                try:
                    nx.recent_text.append(text)
                except Exception:
                    pass
                # Update lexicon/ngrams and token set for this tick (behavior-preserving)
                try:
                    if not hasattr(nx, "_lexicon"):
                        nx._lexicon = {}
                    toks = text_utils.tokenize_text(text)
                    for w in set(toks):
                        nx._lexicon[w] = int(nx._lexicon.get(w, 0)) + 1
                        tick_tokens.add(w)
                    # Ensure n-gram stores exist and update streaming n-grams for emergent composition
                    try:
                        nx._ng2
                        nx._ng3
                    except Exception:
                        nx._ng2 = {}
                        nx._ng3 = {}
                    text_utils.update_ngrams(toks, nx._ng2, nx._ng3)
                    # Increment document counter once per inbound text message
                    nx._doc_count = int(getattr(nx, "_doc_count", 0)) + 1
                except Exception:
                    pass
                # Symbol → indices mapping (deterministic)
                try:
                    group_size = int(getattr(nx, "stim_group_size", 4))
                    max_symbols = int(getattr(nx, "stim_max_symbols", 64))
                    idxs = _stim_symbols_to_indices(
                        text, group_size, max_symbols, int(getattr(nx, "N", 0)), reverse_map=tick_rev_map
                    )
                    for i in idxs:
                        stim_idxs.add(int(i))
                except Exception:
                    pass
            except Exception:
                pass

            # Emit original message
            try:
                nx.utd.emit_text(m)
            except Exception:
                pass
        except Exception:
            # Fail-soft per message
            pass

    return ute_text_count, stim_idxs, tick_tokens, tick_rev_map


__all__ = ["process_messages"]