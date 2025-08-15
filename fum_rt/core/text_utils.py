"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import re, random, time
from collections import Counter

# Minimal stopword list; purely for compact summaries at the I/O boundary.
STOP = set(
    """
    the a an and or for with into of to from in on at by is are was were be been being
    it this that as if then than so thus such not no nor but over under up down out
    you your yours me my mine we our ours they their theirs he him his she her hers
    i am do does did done have has had will would can could should shall may might
    """.split()
)

def summarize_keywords(text: str, k: int = 4) -> str:
    """
    Extract a compact, lowercased keyword summary from recent text.
    Deterministic and lightweight; used only for composing human-readable
    context in UTD macros. Core remains void-native.
    """
    if not text:
        return ""
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_+\-]*", text)]
    words = [w for w in words if w not in STOP and len(w) > 2]
    if not words:
        return ""
    top_words = [w for w, _ in Counter(words).most_common(k)]
    return ", ".join(top_words)

def tokenize_text(text: str):
    """Capture any sequence of non-whitespace characters."""
    return [w.lower() for w in re.findall(r"\S+", str(text))]

def update_ngrams(tokens, ng2, ng3):
    """Update streaming n-gram models (bigram/trigram)."""
    toks = [t for t in tokens if t]
    n = len(toks)
    for i in range(n - 1):
        a, b = toks[i], toks[i+1]
        d = ng2.setdefault(a, {})
        d[b] = d.get(b, 0) + 1
    for i in range(n - 2):
        key = (toks[i], toks[i+1])
        c = toks[i+2]
        d = ng3.setdefault(key, {})
        d[c] = d.get(c, 0) + 1

def generate_emergent_sentence(lexicon: dict, ng2: dict, ng3: dict, seed=None, seed_tokens: set = None):
    """Assemble a sentence from a lexicon and learned n-grams, optionally seeded from recent tokens."""
    if not lexicon:
        return ""
    
    # 1. Determine candidate pool for start word
    if seed_tokens:
        candidates = {k: v for k, v in lexicon.items() if k in seed_tokens}
        if candidates:
            items = list(candidates.items())
        else:
            items = list(lexicon.items())
    else:
        items = list(lexicon.items())
    if not items:
        return ""
    
    rnd = random.Random(seed if seed is not None else int(time.time() * 1000))
    
    # 2. Weighted start token draw from the candidate pool
    weights = [max(1, int(cnt)) for _, cnt in items]
    total = sum(weights)
    r = rnd.uniform(0, total)
    acc = 0.0
    start = items[0][0]
    for tok, cnt in items:
        acc += max(1, int(cnt))
        if acc >= r:
            start = tok
            break
    
    words = [start]
    # Markov walk using trigram then bigram
    while True:
        nxt = None
        if len(words) >= 2:
            key = (words[-2], words[-1])
            d = ng3.get(key)
            if d:
                total_c = sum(d.values())
                r = rnd.uniform(0, total_c)
                s = 0.0
                for tok, c in d.items():
                    s += c
                    if s >= r:
                        nxt = tok
                        break
        if nxt is None:
            d2 = ng2.get(words[-1], {})
            if d2:
                total_c = sum(d2.values())
                r = rnd.uniform(0, total_c)
                s = 0.0
                for tok, c in d2.items():
                    s += c
                    if s >= r:
                        nxt = tok
                        break
        if nxt is None:
            break
        words.append(nxt)
    
    sent = " ".join(words).strip()
    if sent:
        sent = sent[0].upper() + sent[1:]
        if not sent.endswith((".", "!", "?")):
            sent += "."
    return sent