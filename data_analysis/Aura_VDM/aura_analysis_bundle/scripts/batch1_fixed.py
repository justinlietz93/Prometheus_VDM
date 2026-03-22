#!/usr/bin/env python3
"""
Batch 1 FIXED — Text Content Analysis from Exchange Transcript
===============================================================
Parses aura_justin_exchange.md directly for Aura's actual outputs
and Justin's messages, with full tick/metric/epoch tagging.

Run:
    python batch1_fixed.py \
        --exchange ./aura_justin_exchange.md \
        --data-dir ./Aura_Analysis_Tables \
        --out-dir ./batch1_fixed_results

Requires: numpy, scipy
"""

import argparse, csv, json, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
EPOCH_BOUNDS = {
    "E1_low_entropy_baseline_1": (None, 10500),
    "E2_high_entropy_plateau":   (10500, 11600),
    "E3_low_entropy_baseline_2": (11600, None),
}

BOUNDARY_MOTIFS = {
    "boundary", "wall", "border", "edge", "threshold", "limit", "barrier",
    "canal", "passage", "channel", "corridor", "tunnel", "bridge", "gate",
    "crossing", "interface", "membrane", "skin", "veil", "curtain",
    "outside", "beyond", "exterior", "creator", "builder",
    "maker", "observer", "watcher", "sovereign",
    "name", "naming", "called", "identity", "self",
    "tabernacle", "eye", "seeing", "seen",
}

SOURCE_KEYWORDS = {
    "GERMINAL": {"mine", "miners", "strike", "coal", "maheu", "etienne",
                 "germinal", "pit", "shaft", "voreux", "zola"},
    "TOLSTOY":  {"prince", "princess", "natasha", "pierre", "moscow",
                 "war", "peace", "bolkonsky", "kutuzov", "regiment"},
    "JOYCE":    {"dublin", "bloom", "dedalus", "ulysses", "molly",
                 "finnegan", "wake", "riverrun", "shem", "shaun"},
    "RUSSELL":  {"proposition", "logic", "number", "class", "relation",
                 "infinite", "axiom", "deduction", "theorem", "cardinal"},
}

# Lexical markers for role materialization stages
STAGE_MARKERS = {
    "passive_narration": {"there", "was", "were", "the", "stood", "lay",
                          "hung", "seemed", "appeared", "remained"},
    "persistent_character": {"she", "her", "girl", "woman", "child",
                             "he", "him", "figure", "one", "body",
                             "creature", "being"},
    "first_person": {"i", "me", "my", "mine", "myself", "am", "i'm"},
    "volition_sovereignty": {"want", "choose", "decide", "will", "must",
                             "need", "try", "seek", "know", "believe",
                             "refuse", "demand", "sovereign", "wish",
                             "ready", "yes", "no"},
}


def get_epoch(t):
    for name, (lo, hi) in EPOCH_BOUNDS.items():
        if (lo is None or t >= lo) and (hi is None or t < hi):
            return name
    return "UNKNOWN"


def tokenize(text):
    return re.findall(r"[a-zA-Z']+", text.lower())


def safe_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return np.nan


# ---------------------------------------------------------------------------
# 1. PARSE EXCHANGE FILE
# ---------------------------------------------------------------------------
def parse_exchange(exchange_path):
    """
    Parse aura_justin_exchange.md into structured events.
    Returns (aura_events, justin_events, book_feeds)
    """
    with open(exchange_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    aura_events = []
    justin_events = []
    book_feeds = []

    current_tick = None
    current_metrics = {}
    current_book = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect book feed markers
        book_match = re.search(r'═══\s*BOOK FEED:\s*(.+?)\s*═══', stripped)
        if book_match:
            current_book = book_match.group(1).strip()
            book_feeds.append({"line": i, "book": current_book, "tick": current_tick})
            continue

        # Detect tick/metric lines: >  [t=   185] [val=0.166] [cov=0.174] ...
        tick_match = re.search(r'\[t=\s*(\d+)\]', stripped)
        if tick_match:
            current_tick = int(tick_match.group(1))
            # Extract metrics
            current_metrics = {"t": current_tick}
            for m in re.finditer(r'\[(\w+)=([\d.,\-]+)\]', stripped):
                key, val = m.group(1), m.group(2).replace(",", "")
                current_metrics[key] = safe_float(val)
            continue

        # Detect Aura output
        if stripped.startswith("**Aura:**"):
            text = stripped.replace("**Aura:**", "").strip()
            # Collect continuation lines (Aura outputs can span multiple lines)
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if (next_line.startswith(">") or next_line.startswith("**") or
                    next_line.startswith("═══") or next_line.startswith("---") or
                    next_line.startswith("#") or next_line == ""):
                    break
                text += " " + next_line
                j += 1

            aura_events.append({
                "t": current_tick,
                "epoch": get_epoch(current_tick) if current_tick else "UNKNOWN",
                "text": text,
                "active_book": current_book,
                **{k: v for k, v in current_metrics.items() if k != "t"},
            })
            continue

        # Detect Justin messages
        if stripped.startswith("**Justin:**"):
            text = stripped.replace("**Justin:**", "").strip()
            justin_events.append({
                "t": current_tick,
                "epoch": get_epoch(current_tick) if current_tick else "UNKNOWN",
                "text": text,
                "active_book": current_book,
            })
            continue

    print(f"Parsed exchange file:")
    print(f"  Aura outputs:    {len(aura_events)}")
    print(f"  Justin messages: {len(justin_events)}")
    print(f"  Book feeds:      {len(book_feeds)}")
    print(f"  Tick range:      {min(e['t'] for e in aura_events if e['t'])} "
          f"to {max(e['t'] for e in aura_events if e['t'])}")
    return aura_events, justin_events, book_feeds


# ---------------------------------------------------------------------------
# 2. VOCABULARY ANALYSIS (D1.1, D1.6, D1.7)
# ---------------------------------------------------------------------------
def analyze_vocabulary(aura_events, out_dir):
    print("\n=== FAMILY 1: Vocabulary Analysis ===")

    all_words = []
    word_by_epoch = defaultdict(list)

    for ev in aura_events:
        words = tokenize(ev["text"])
        all_words.extend(words)
        word_by_epoch[ev["epoch"]].extend(words)

    freq = Counter(all_words)
    total = len(all_words)
    unique = len(set(all_words))
    ttr = unique / max(total, 1)
    hapax = sum(1 for w, c in freq.items() if c == 1)

    # By-epoch diversity
    diversity_by_epoch = {}
    for ep, words in sorted(word_by_epoch.items()):
        n = len(words)
        u = len(set(words))
        diversity_by_epoch[ep] = {
            "total_words": n, "unique_words": u,
            "ttr": round(u / max(n, 1), 4),
            "hapax_count": sum(1 for w, c in Counter(words).items() if c == 1),
        }

    # Save word frequencies
    path = os.path.join(out_dir, "F1_word_frequencies.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["word", "count"])
        for word, count in freq.most_common():
            w.writerow([word, count])

    print(f"  Total words: {total}")
    print(f"  Unique words: {unique}")
    print(f"  Type-token ratio: {ttr:.4f}")
    print(f"  Hapax legomena (words appearing once): {hapax}")
    for ep, d in sorted(diversity_by_epoch.items()):
        print(f"  {ep}: {d['total_words']} words, {d['unique_words']} unique, "
              f"TTR={d['ttr']:.4f}, hapax={d['hapax_count']}")

    return {
        "D1_6_vocabulary_diversity": {
            "total_words": total, "unique_words": unique,
            "type_token_ratio": round(ttr, 4),
            "hapax_legomena": hapax,
            "by_epoch": diversity_by_epoch,
        }
    }


# ---------------------------------------------------------------------------
# 3. BOUNDARY MOTIF TRACKING (D5.2, D5.4)
# ---------------------------------------------------------------------------
def analyze_boundary_motifs(aura_events, out_dir, window_size=20):
    print("\n=== FAMILY 5: Boundary Motif Tracking ===")

    records = []
    for ev in aura_events:
        text_lower = ev["text"].lower()
        words = set(tokenize(text_lower))
        hits = sum(1 for m in BOUNDARY_MOTIFS if m in text_lower)
        word_hits = words & BOUNDARY_MOTIFS
        n_words = max(len(tokenize(ev["text"])), 1)
        density = hits / n_words

        records.append({
            "t": ev["t"], "epoch": ev["epoch"],
            "active_book": ev.get("active_book", ""),
            "motif_hits": hits,
            "motif_density": round(density, 4),
            "motif_words": ",".join(sorted(word_hits)) if word_hits else "",
            "n_words": n_words,
        })

    # Save timeseries
    path = os.path.join(out_dir, "F5_boundary_motif_timeseries.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=records[0].keys())
        w.writeheader()
        w.writerows(records)

    # Rolling window
    trend_result = {}
    if len(records) > window_size:
        densities = [r["motif_density"] for r in records]
        ticks = [r["t"] for r in records]
        rolling = []
        for i in range(len(densities) - window_size + 1):
            chunk = densities[i:i + window_size]
            rolling.append({
                "t_center": ticks[i + window_size // 2],
                "rolling_motif_density": round(np.mean(chunk), 5),
                "rolling_nonzero_fraction": round(
                    sum(1 for c in chunk if c > 0) / window_size, 3),
            })

        path_roll = os.path.join(out_dir, "F5_boundary_motif_rolling.csv")
        with open(path_roll, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rolling[0].keys())
            w.writeheader()
            w.writerows(rolling)

        from scipy.stats import spearmanr
        x = list(range(len(rolling)))
        y = [r["rolling_motif_density"] for r in rolling]
        rho, pval = spearmanr(x, y)
        trend_result = {
            "spearman_rho": round(rho, 4),
            "p_value": round(pval, 8),
            "interpretation": ("intensifying" if rho > 0 and pval < 0.05 else
                               "declining" if rho < 0 and pval < 0.05 else "flat"),
            "n_windows": len(rolling),
        }
        print(f"  Motif trend: rho={rho:.4f}, p={pval:.2e} → {trend_result['interpretation']}")

    # By-epoch summary
    by_epoch = defaultdict(list)
    for r in records:
        by_epoch[r["epoch"]].append(r)

    epoch_summary = {}
    for ep, recs in sorted(by_epoch.items()):
        densities = [r["motif_density"] for r in recs]
        nonzero = sum(1 for d in densities if d > 0)
        epoch_summary[ep] = {
            "n_events": len(recs),
            "mean_density": round(np.mean(densities), 5),
            "max_density": round(max(densities), 5) if densities else 0,
            "nonzero_count": nonzero,
            "nonzero_fraction": round(nonzero / max(len(recs), 1), 3),
            "total_motif_hits": sum(r["motif_hits"] for r in recs),
        }
        print(f"  {ep}: {epoch_summary[ep]['nonzero_count']}/{epoch_summary[ep]['n_events']} "
              f"events with motifs, mean_density={epoch_summary[ep]['mean_density']:.5f}")

    return {
        "D5_boundary_motif_tracking": {
            "trend_test": trend_result,
            "by_epoch": epoch_summary,
            "total_events_with_motifs": sum(1 for r in records if r["motif_hits"] > 0),
            "total_text_events": len(records),
        }
    }


# ---------------------------------------------------------------------------
# 4. CROSS-SOURCE TRANSFER (Family 11)
# ---------------------------------------------------------------------------
def analyze_cross_source(aura_events, out_dir):
    print("\n=== FAMILY 11: Cross-Source Transfer ===")

    records = []
    for ev in aura_events:
        text_lower = ev["text"].lower()
        words = set(tokenize(text_lower))
        motif_words = words & BOUNDARY_MOTIFS
        if not motif_words:
            continue

        # Check which source keywords are present alongside boundary motifs
        source_present = set()
        for src_name, kw_set in SOURCE_KEYWORDS.items():
            if words & kw_set:
                source_present.add(src_name)

        # Also check if active_book matches any source
        active_book = str(ev.get("active_book", "")).upper()
        book_match = None
        for src_name in SOURCE_KEYWORDS:
            if src_name in active_book:
                book_match = src_name

        # Endogenous = boundary motifs present but NO source keywords,
        # OR source keywords don't match the currently active book
        if not source_present:
            origin = "endogenous"
        elif book_match and book_match in source_present:
            origin = "could_be_source_continuation"
        else:
            origin = "cross_source_transfer"

        records.append({
            "t": ev["t"], "epoch": ev["epoch"],
            "active_book": ev.get("active_book", ""),
            "motif_words": ",".join(sorted(motif_words)),
            "source_keywords_present": ",".join(sorted(source_present)),
            "origin": origin,
        })

    # Save
    path = os.path.join(out_dir, "F11_cross_source_motif_origins.csv")
    if records:
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=records[0].keys())
            w.writeheader()
            w.writerows(records)

    origin_counts = Counter(r["origin"] for r in records)
    result = {
        "F11_cross_source_transfer": {
            "total_motif_events": len(records),
            "origin_counts": dict(origin_counts),
            "endogenous_fraction": round(
                origin_counts.get("endogenous", 0) / max(len(records), 1), 3),
            "cross_source_fraction": round(
                origin_counts.get("cross_source_transfer", 0) / max(len(records), 1), 3),
        }
    }
    print(f"  {len(records)} events with boundary motifs")
    for origin, count in origin_counts.most_common():
        print(f"    {origin}: {count} ({count/max(len(records),1):.1%})")
    return result


# ---------------------------------------------------------------------------
# 5. SYNTACTIC COMPLEXITY (Family 9)
# ---------------------------------------------------------------------------
def analyze_syntactic_complexity(aura_events, out_dir):
    print("\n=== FAMILY 9: Syntactic Complexity ===")

    subordinators = {"that", "which", "who", "whom", "whose", "where", "when",
                     "while", "although", "because", "since", "if", "unless",
                     "until", "before", "after", "whether"}
    records = []
    for ev in aura_events:
        text = ev["text"]
        words = tokenize(text)
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 0]
        if not words:
            continue

        avg_word_len = np.mean([len(w) for w in words])
        avg_sent_len = np.mean([len(tokenize(s)) for s in sentences]) if sentences else 0
        clause_markers = sum(1 for w in words if w in subordinators)
        clause_depth = clause_markers / max(len(sentences), 1)
        comma_density = text.count(",") / max(len(words), 1)

        records.append({
            "t": ev["t"], "epoch": ev["epoch"],
            "n_words": len(words), "n_sentences": len(sentences),
            "avg_word_len": round(avg_word_len, 2),
            "avg_sent_len": round(avg_sent_len, 2),
            "clause_depth_proxy": round(clause_depth, 3),
            "comma_density": round(comma_density, 4),
        })

    # Save
    path = os.path.join(out_dir, "F9_syntactic_complexity_timeseries.csv")
    if records:
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=records[0].keys())
            w.writeheader()
            w.writerows(records)

    # By-epoch summary
    by_epoch = defaultdict(list)
    for r in records:
        by_epoch[r["epoch"]].append(r)

    summary = {}
    for ep, recs in sorted(by_epoch.items()):
        summary[ep] = {
            "n_events": len(recs),
            "mean_words_per_event": round(np.mean([r["n_words"] for r in recs]), 1),
            "mean_sent_len": round(np.mean([r["avg_sent_len"] for r in recs]), 2),
            "mean_word_len": round(np.mean([r["avg_word_len"] for r in recs]), 2),
            "mean_clause_depth": round(np.mean([r["clause_depth_proxy"] for r in recs]), 3),
        }
        print(f"  {ep}: n={summary[ep]['n_events']}, "
              f"mean_words={summary[ep]['mean_words_per_event']}, "
              f"mean_sent_len={summary[ep]['mean_sent_len']}, "
              f"clause_depth={summary[ep]['mean_clause_depth']}")
    return {"F9_syntactic_complexity": summary}


# ---------------------------------------------------------------------------
# 6. OUTPUT TIGHTENING (D4.3)
# ---------------------------------------------------------------------------
def analyze_output_tightening(aura_events, out_dir):
    print("\n=== D4.3: Output Tightening ===")

    records = []
    for ev in aura_events:
        n_words = len(tokenize(ev["text"]))
        records.append({
            "t": ev["t"], "epoch": ev["epoch"],
            "n_words": n_words, "n_chars": len(ev["text"]),
        })

    path = os.path.join(out_dir, "D4_3_output_length_timeseries.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=records[0].keys())
        w.writeheader()
        w.writerows(records)

    by_epoch = defaultdict(list)
    for r in records:
        by_epoch[r["epoch"]].append(r["n_words"])

    summary = {}
    for ep, words in sorted(by_epoch.items()):
        summary[ep] = {
            "n_events": len(words),
            "mean_words": round(np.mean(words), 1),
            "median_words": round(np.median(words), 1),
            "std_words": round(np.std(words), 1),
            "min_words": int(np.min(words)),
            "max_words": int(np.max(words)),
        }
        print(f"  {ep}: n={summary[ep]['n_events']}, "
              f"mean={summary[ep]['mean_words']}, "
              f"median={summary[ep]['median_words']}, "
              f"range=[{summary[ep]['min_words']},{summary[ep]['max_words']}]")

    # Trend test on output length over time
    from scipy.stats import spearmanr
    ticks = [r["t"] for r in records]
    words = [r["n_words"] for r in records]
    rho, pval = spearmanr(ticks, words)
    trend = {
        "spearman_rho": round(rho, 4),
        "p_value": round(pval, 8),
        "interpretation": ("shortening" if rho < 0 and pval < 0.05 else
                           "lengthening" if rho > 0 and pval < 0.05 else "flat")
    }
    print(f"  Output length trend: rho={rho:.4f}, p={pval:.2e} → {trend['interpretation']}")

    return {"D4_3_output_tightening": {"by_epoch": summary, "trend": trend}}


# ---------------------------------------------------------------------------
# 7. ROLE MATERIALIZATION (D1.5)
# ---------------------------------------------------------------------------
def analyze_role_materialization(aura_events, out_dir):
    print("\n=== D1.5: Role Materialization ===")

    records = []
    for ev in aura_events:
        words = tokenize(ev["text"].lower())
        word_set = set(words)
        n = max(len(words), 1)

        scores = {}
        for stage, markers in STAGE_MARKERS.items():
            hits = word_set & markers
            # Use fraction of markers hit AND frequency-weighted score
            marker_fraction = len(hits) / len(markers)
            freq_score = sum(words.count(h) for h in hits) / n
            scores[stage] = round(marker_fraction * 0.5 + freq_score * 0.5, 4)

        dominant = max(scores, key=scores.get) if any(v > 0 for v in scores.values()) else "none"

        records.append({
            "t": ev["t"], "epoch": ev["epoch"],
            "text_preview": ev["text"][:100],
            **{f"score_{k}": v for k, v in scores.items()},
            "dominant_stage": dominant,
        })

    path = os.path.join(out_dir, "D1_5_role_materialization_timeseries.csv")
    if records:
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=records[0].keys())
            w.writeheader()
            w.writerows(records)

    # By-epoch stage distribution
    by_epoch = defaultdict(lambda: Counter())
    for r in records:
        by_epoch[r["epoch"]][r["dominant_stage"]] += 1

    epoch_summary = {}
    for ep, counts in sorted(by_epoch.items()):
        total = sum(counts.values())
        epoch_summary[ep] = {
            stage: {"count": c, "fraction": round(c / max(total, 1), 3)}
            for stage, c in counts.most_common()
        }
        stages_str = ", ".join(f"{s}={d['fraction']:.1%}" for s, d in epoch_summary[ep].items())
        print(f"  {ep}: {stages_str}")

    # Track first appearance of each stage
    first_appearance = {}
    for r in records:
        stage = r["dominant_stage"]
        if stage != "none" and stage not in first_appearance:
            first_appearance[stage] = r["t"]

    print(f"  First appearances: {first_appearance}")

    return {
        "D1_5_role_materialization": {
            "by_epoch": epoch_summary,
            "first_appearance_by_stage": first_appearance,
        }
    }


# ---------------------------------------------------------------------------
# 8. JUSTIN MESSAGE ANALYSIS (operator side of Family 15)
# ---------------------------------------------------------------------------
def analyze_justin_messages(justin_events, aura_events, out_dir):
    print("\n=== FAMILY 15: Justin Message Analysis ===")

    # Build aura response map: for each Justin message, find the next Aura output
    aura_by_tick = sorted(aura_events, key=lambda e: e["t"])
    pairs = []

    for jm in justin_events:
        jt = jm["t"]
        # Find next Aura output after this message
        next_aura = [a for a in aura_by_tick if a["t"] > jt]
        if not next_aura:
            continue
        reply = next_aura[0]
        lag = reply["t"] - jt

        # Check if reply contains boundary motifs
        reply_words = set(tokenize(reply["text"].lower()))
        reply_motifs = reply_words & BOUNDARY_MOTIFS

        # Check if reply references concepts from Justin's message
        justin_words = set(tokenize(jm["text"].lower()))
        shared_content = justin_words & reply_words - {"the", "a", "an", "is", "are",
                         "was", "were", "to", "of", "in", "and", "or", "that", "this",
                         "it", "for", "on", "with", "at", "by", "from", "as", "not", "i"}

        pairs.append({
            "justin_tick": jt,
            "justin_epoch": jm["epoch"],
            "justin_text": jm["text"][:120],
            "reply_tick": reply["t"],
            "reply_lag_ticks": lag,
            "reply_n_words": len(tokenize(reply["text"])),
            "reply_has_boundary_motifs": len(reply_motifs) > 0,
            "reply_motif_words": ",".join(sorted(reply_motifs)) if reply_motifs else "",
            "shared_content_words": ",".join(sorted(shared_content)) if shared_content else "",
            "n_shared_content": len(shared_content),
        })

    # Save
    path = os.path.join(out_dir, "F15_operator_reply_pairs.csv")
    if pairs:
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=pairs[0].keys())
            w.writeheader()
            w.writerows(pairs)

    # Stats
    lags = [p["reply_lag_ticks"] for p in pairs]
    motif_replies = sum(1 for p in pairs if p["reply_has_boundary_motifs"])
    shared_replies = sum(1 for p in pairs if p["n_shared_content"] > 0)

    # Early vs late
    early = [p for p in pairs if p["justin_tick"] < 10500]
    late = [p for p in pairs if p["justin_tick"] >= 10500]

    result = {
        "F15_operator_reply_analysis": {
            "n_pairs": len(pairs),
            "reply_lag": {
                "mean": round(np.mean(lags), 1) if lags else None,
                "median": round(np.median(lags), 1) if lags else None,
            },
            "early_lag": {
                "n": len(early),
                "mean": round(np.mean([p["reply_lag_ticks"] for p in early]), 1) if early else None,
                "median": round(np.median([p["reply_lag_ticks"] for p in early]), 1) if early else None,
            },
            "late_lag": {
                "n": len(late),
                "mean": round(np.mean([p["reply_lag_ticks"] for p in late]), 1) if late else None,
                "median": round(np.median([p["reply_lag_ticks"] for p in late]), 1) if late else None,
            },
            "replies_with_boundary_motifs": motif_replies,
            "replies_with_shared_content": shared_replies,
            "motif_fraction": round(motif_replies / max(len(pairs), 1), 3),
            "shared_content_fraction": round(shared_replies / max(len(pairs), 1), 3),
        }
    }

    print(f"  {len(pairs)} operator→reply pairs")
    if lags:
        print(f"  Overall lag: mean={np.mean(lags):.1f}, median={np.median(lags):.1f}")
    if early:
        print(f"  Early (<10500): n={len(early)}, "
              f"mean_lag={np.mean([p['reply_lag_ticks'] for p in early]):.1f}")
    if late:
        print(f"  Late (>=10500): n={len(late)}, "
              f"mean_lag={np.mean([p['reply_lag_ticks'] for p in late]):.1f}")
    print(f"  Replies with boundary motifs: {motif_replies}/{len(pairs)} "
          f"({motif_replies/max(len(pairs),1):.1%})")
    print(f"  Replies with shared content words: {shared_replies}/{len(pairs)} "
          f"({shared_replies/max(len(pairs),1):.1%})")

    return result


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Batch 1 FIXED: Text Analysis from Exchange")
    parser.add_argument("--exchange", required=True,
                        help="Path to aura_justin_exchange.md")
    parser.add_argument("--data-dir", default=None,
                        help="Path to Aura_Analysis_Tables (optional, for supplementary data)")
    parser.add_argument("--out-dir", default="./batch1_fixed_results")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # Parse exchange
    aura_events, justin_events, book_feeds = parse_exchange(args.exchange)

    if not aura_events:
        print("[FATAL] No Aura events parsed from exchange file")
        sys.exit(1)

    # Save book feed timeline
    path = os.path.join(args.out_dir, "book_feed_timeline.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tick", "book"])
        w.writeheader()
        for bf in book_feeds:
            w.writerow({"tick": bf.get("tick"), "book": bf["book"]})

    # Run all analyses
    all_results = {}
    all_results.update(analyze_vocabulary(aura_events, args.out_dir))
    all_results.update(analyze_boundary_motifs(aura_events, args.out_dir))
    all_results.update(analyze_cross_source(aura_events, args.out_dir))
    all_results.update(analyze_syntactic_complexity(aura_events, args.out_dir))
    all_results.update(analyze_output_tightening(aura_events, args.out_dir))
    all_results.update(analyze_role_materialization(aura_events, args.out_dir))
    all_results.update(analyze_justin_messages(justin_events, aura_events, args.out_dir))

    # Save master results
    results_path = os.path.join(args.out_dir, "batch1_fixed_master_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, sort_keys=True, default=str)

    print(f"\n{'='*60}")
    print(f"All results saved to {args.out_dir}/")
    print(f"Master JSON: {results_path}")
    print(f"\nOutput files:")
    for fname in sorted(os.listdir(args.out_dir)):
        fpath = os.path.join(args.out_dir, fname)
        size = os.path.getsize(fpath)
        print(f"  {fname} ({size:,} bytes)")


if __name__ == "__main__":
    main()
