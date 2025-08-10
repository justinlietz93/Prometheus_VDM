import re
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

def summarize_tokens(text: str, k: int = 4) -> str:
    """
    Extract a compact, lowercased keyword summary from recent text.
    Deterministic and lightweight; used only for composing human-readable
    context in UTD macros. Core remains void-native.

    Args:
        text: input text to scan
        k: number of top keywords to return

    Returns:
        A comma-separated string of up to k keywords. Empty string if none.
    """
    if not text:
        return ""
    # alnum with simple token chars; hyphen and plus allowed inside words
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_+\-]*", text)]
    words = [w for w in words if w not in STOP and len(w) > 2]
    if not words:
        return ""
    top = [w for w, _ in Counter(words).most_common(max(1, int(k)))]
    return ", ".join(top[: max(1, int(k))])