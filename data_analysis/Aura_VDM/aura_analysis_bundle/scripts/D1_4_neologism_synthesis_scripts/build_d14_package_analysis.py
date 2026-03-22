#!/usr/bin/env python3
"""Rebuild D1.4 tables and figures from package provenance inputs."""

import os, re, json
from collections import defaultdict, Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUTS = os.path.join(ROOT, "provenance", "inputs")
TABLES = os.path.join(ROOT, "tables")
FIGURES = os.path.join(ROOT, "figures")

def tokenize(text: str):
    text = text.lower().replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text)

def assign_book(t: int):
    if t < 3095:
        return "Germinal by Émile Zola"
    elif t < 7617:
        return "Germinal + War and Peace by Leo Tolstoy"
    elif t < 11367:
        return "Finnegans Wake by James Joyce"
    return "Introduction to Mathematical Philosophy by Bertrand Russell"

def max_contig_span_with_source(out_tokens, source_tokens, source_pos, max_positions=1500):
    best_len, best = 0, None
    for i, tok in enumerate(out_tokens):
        positions = source_pos.get(tok, [])
        if len(positions) > max_positions:
            step = max(1, len(positions)//max_positions)
            positions = positions[::step][:max_positions]
        for p in positions:
            l = 1
            while i+l < len(out_tokens) and p+l < len(source_tokens) and out_tokens[i+l] == source_tokens[p+l]:
                l += 1
            if l > best_len:
                best_len, best = l, (i,p,l)
    return best_len, best

def span_text(out_tokens, detail):
    if not detail:
        return ""
    i, p, l = detail
    return " ".join(out_tokens[i:i+l])

def main():
    say_df = pd.read_csv(os.path.join(INPUTS, "extracted_say_events.csv"))
    say_df["book_context"] = say_df["t"].apply(assign_book)
    say_df["tokens"] = say_df["text"].map(tokenize)
    say_df["output_token_count"] = say_df["tokens"].map(len)
    say_df["ticks_after_joyce_switch"] = say_df["t"] - 7617

    corpus_files = {
        "joyce":"FINNEGANS WAKE-JOYCE.txt",
        "zola":"GERMINAL-ZOLA.txt",
        "tolstoy":"WAR_AND_PEACE_TOLSTOY.txt",
        "russell":"INTRO_TO_MATH_PHILOSOPY-RUSSELL.txt",
        "schism":"SCHISM-TOOL.txt",
        "opeth":"WILL_O_THE_WISP-OPETH.txt"
    }
    corpus_tokens = {k: tokenize(open(os.path.join(INPUTS, v), encoding="utf-8", errors="ignore").read()) for k,v in corpus_files.items()}
    corpus_sets = {k:set(v) for k,v in corpus_tokens.items()}
    joyce_freq = Counter(corpus_tokens["joyce"])
    other_union = set().union(*(v for k,v in corpus_sets.items() if k != "joyce"))
    joyce_auto_marker_vocab = sorted(tok for tok in corpus_sets["joyce"] if tok not in other_union and (joyce_freq[tok] >= 2 or len(tok) >= 8 or "'" in tok))

    reviewed_markers = list(pd.read_csv(os.path.join(TABLES, "d14_reviewed_marker_lexicon.csv"))["token"])

    say_df["auto_marker_types"] = say_df["tokens"].map(lambda toks: sorted(set(tok for tok in toks if tok in joyce_auto_marker_vocab)))
    say_df["n_auto_marker_types"] = say_df["auto_marker_types"].map(len)
    say_df["reviewed_marker_types"] = say_df["tokens"].map(lambda toks: [tok for tok in reviewed_markers if tok in toks])
    say_df["n_reviewed_marker_types"] = say_df["reviewed_marker_types"].map(len)
    joyce_outputs = say_df[say_df["book_context"] == "Finnegans Wake by James Joyce"].copy()

    source_pos = {}
    for name, toks in corpus_tokens.items():
        pos = defaultdict(list)
        for i, t in enumerate(toks):
            pos[t].append(i)
        source_pos[name] = pos

    rows = []
    for _, r in joyce_outputs.iterrows():
        if r["n_reviewed_marker_types"] == 0:
            continue
        joyce_len, joyce_detail = max_contig_span_with_source(r["tokens"], corpus_tokens["joyce"], source_pos["joyce"])
        nonjoyce_best_src, nonjoyce_best_len, nonjoyce_best_detail = None, -1, None
        for src in [s for s in corpus_tokens if s != "joyce"]:
            l, detail = max_contig_span_with_source(r["tokens"], corpus_tokens[src], source_pos[src])
            if l > nonjoyce_best_len:
                nonjoyce_best_src, nonjoyce_best_len, nonjoyce_best_detail = src, l, detail
        rows.append({
            "t": r["t"],
            "ticks_after_joyce_switch": r["ticks_after_joyce_switch"],
            "output_token_count": r["output_token_count"],
            "reviewed_marker_types": " | ".join(r["reviewed_marker_types"]),
            "n_reviewed_marker_types": r["n_reviewed_marker_types"],
            "max_joyce_span_tokens": joyce_len,
            "max_joyce_span_text": span_text(r["tokens"], joyce_detail),
            "max_nonjoyce_span_tokens": nonjoyce_best_len,
            "max_nonjoyce_source": nonjoyce_best_src,
            "max_nonjoyce_span_text": span_text(r["tokens"], nonjoyce_best_detail),
            "text": r["text"],
        })
    reviewed_df = pd.DataFrame(rows).sort_values("t")
    reviewed_df.to_csv(os.path.join(TABLES, "d14_reviewed_marker_events_rebuilt.csv"), index=False)

    plt.figure(figsize=(10,5))
    plt.scatter(joyce_outputs["ticks_after_joyce_switch"], joyce_outputs["n_reviewed_marker_types"], s=np.maximum(20, joyce_outputs["output_token_count"]))
    plt.axvline(reviewed_df["ticks_after_joyce_switch"].min(), linestyle="--")
    plt.xlabel("Ticks after Joyce switch (t - 7617)")
    plt.ylabel("Reviewed Joyce marker types in output")
    plt.title("D1.4 Joyce-window outputs: reviewed marker uptake over time")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, "d14_reviewed_marker_timeline_rebuilt.png"), dpi=200)
    plt.close()

if __name__ == "__main__":
    main()
