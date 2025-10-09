#!/usr/bin/env python3
import argparse, json, re, sys, html, unicodedata
from collections import deque

GLYPH_MAP = str.maketrans({
    "ƒ": "|", "ˆ": "^", "-": "-", "-": "-", "’": "'",
    "“": '"', "”": '"', "·": ".", "•": "-", "×": "x",
    "∣": "|", "⎪": "|"
})

LINK_PARAM_RX = re.compile(r"\|\s*[a-zA-Z0-9_-]+\s*=\s*[^|\]\s]+")
TEMPLATE_RX   = re.compile(r"\{\{.*?\}\}", flags=re.S)
REF_RX        = re.compile(r"<ref[^>]*>.*?</ref>", flags=re.I|re.S)
TAG_RX        = re.compile(r"<[^>]+>")
PIPE_RX       = re.compile(r'(\|\s*)+')
WIKI_LINK_RX  = re.compile(r"\[\[([^\]]+)\]\]")
WS_RX         = re.compile(r"\s+")
PUNCT_ONLY_RX = re.compile(r"^[\W_]+$")
ALNUM_RX      = re.compile(r"[A-Za-z0-9]")

def unescape_and_normalize(s: str) -> str:
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(GLYPH_MAP)
    return s

def strip_wikimarkup(s: str) -> str:
    # [[a|b|c]] -> keep last segment (display text); [[foo]] -> foo
    def repl_link(m):
        inner = m.group(1)
        parts = inner.split("|")
        return parts[-1].strip()
    s = WIKI_LINK_RX.sub(repl_link, s)
    s = TEMPLATE_RX.sub(" ", s)
    s = REF_RX.sub(" ", s)
    s = TAG_RX.sub(" ", s)
    s = LINK_PARAM_RX.sub(" ", s)
    s = PIPE_RX.sub(" ", s)
    return s

def basic_clean(s: str) -> str:
    s = unescape_and_normalize(s)
    s = strip_wikimarkup(s)
    s = WS_RX.sub(" ", s).strip()
    # Drop leading table residue like 'style="..."' that slipped through
    s = re.sub(r'^\s*style="[^"]*"\s*', "", s)
    # Trim trailing stray punctuation repetition
    s = re.sub(r"[.,;:]\s*$", lambda m: m.group(0)[0], s)
    return s

def is_noise(s: str, minlen: int) -> bool:
    if len(s) < minlen: return True
    if PUNCT_ONLY_RX.match(s): return True
    if not ALNUM_RX.search(s): return True
    # Heuristic: evaluator imperatives (prompt-echo)
    if re.match(r"(?i)^(state|provide|give|define|list|draw|construct|pose|ask|write|name)\b", s):
        return True
    return False

def classify(s: str) -> str:
    sl = s.lower()
    if "do(" in sl or "delete p(" in sl or re.search(r"\binterven", sl):
        return "intervention"
    if re.search(r"\b(⟂|independent|conditionally independent|d-?sep|collider|backdoor)\b", sl):
        return "CI"
    if re.search(r"\bP\s*\([^)]+", s) or re.search(r"\bPr\s*\(", s):
        return "probability"
    if re.search(r"=\s*f\(|=\s*β|=\\beta|=\s*alpha|=\s*gamma|=\s*\w+\(", sl):
        return "equation"
    if re.search(r"\b(therefore|thus|hence|it follows that)\b", sl):
        return "chain"
    return "text"

def main():
    ap = argparse.ArgumentParser(description="Clean and label UTD macro stream (NDJSON).")
    ap.add_argument("--in", dest="inp", required=True, help="Input NDJSON file (UTD events). Use - for stdin.")
    ap.add_argument("--out", dest="out_txt", required=True, help="Output cleaned text file.")
    ap.add_argument("--out-csv", dest="out_csv", default=None, help="Optional CSV with t,phase,macro,class,text")
    ap.add_argument("--channels", nargs="+", default=["say"], help="Macros to include (e.g., say status)")
    ap.add_argument("--minlen", type=int, default=8, help="Min cleaned line length.")
    ap.add_argument("--dedupe-window", type=int, default=200, help="Exact dedupe window size.")
    args = ap.parse_args()

    fin = sys.stdin if args.inp == "-" else open(args.inp, "r", encoding="utf-8")
    fout = open(args.out_txt, "w", encoding="utf-8")
    fcsv = open(args.out_csv, "w", encoding="utf-8") if args.out_csv else None
    if fcsv:
        fcsv.write("t,phase,macro,class,text\n")

    window = deque(maxlen=args.dedupe_window)
    window_set = set()

    def seen(snorm: str) -> bool:
        return snorm in window_set

    def push(snorm: str):
        if len(window) == window.maxlen:
            old = window.popleft()
            window_set.discard(old)
        window.append(snorm)
        window_set.add(snorm)

    kept = 0
    for line in fin:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "macro": continue
        macro = obj.get("macro")
        if macro not in args.channels: continue
        text = obj.get("args", {}).get("text", "")
        t = obj.get("args", {}).get("why", {}).get("t", "")
        phase = obj.get("args", {}).get("why", {}).get("phase", "")
        cleaned = basic_clean(text)
        if is_noise(cleaned, args.minlen):
            continue
        snorm = cleaned.lower()
        if seen(snorm):
            continue
        push(snorm)
        label = classify(cleaned)
        fout.write(f"[t={t}][{macro}][{label}] {cleaned}\n")
        if fcsv:
            # Escape double quotes
            ct = cleaned.replace('"', '""')
            fcsv.write(f"{t},{phase},{macro},{label},\"{ct}\"\n")
        kept += 1

    fout.close()
    if fcsv: fcsv.close()
    if fin is not sys.stdin: fin.close()

if __name__ == "__main__":
    main()
