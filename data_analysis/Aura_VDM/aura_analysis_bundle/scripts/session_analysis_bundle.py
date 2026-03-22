#!/usr/bin/env python3
"""
Aura Distinction Inventory — Session Analysis Bundle
=====================================================
Reproduces ALL analyses from the 2026-03-16 session that produced
new distinction findings. Every number reported in the inventory
traces back to this script.

Run:
    python session_analysis_bundle.py \
        --data-dir ./Aura_Analysis_Tables \
        --exchange ./aura_justin_exchange.md \
        --out-dir ./session_analysis_results

Requires: numpy, scipy
Optional: scikit-learn (for D5.1 classifier)

Produces:
    results/master_results.json          — All numerical findings
    results/statistical_tests.csv        — Every test in one table
    results/D5_1_signed_permutation.json — Full permutation output
    results/D5_1_operator_deltas.csv     — Per-message state changes
    results/F10_silence_comparison.csv   — Pre-speech vs silence
    results/F10_inter_say_intervals.csv  — Full interval distribution
    results/D12_territory_timeline.csv   — Territory emergence sequence
    results/D12_homeostasis_events.csv   — Pruning/bridging by epoch
    results/F14_composer_audit.json      — Decoder masking metrics
    results/D2_state_space_geometry.json — PCA trajectory analysis
    results/D8_rolling_variance.json     — Change-points and CSD
    results/D3_neuron_analysis.json      — Per-neuron specialization
    results/D2_11_landscape_migration.json — 32x32 grid JSD
    results/D7_7_lz_complexity.json      — LZ by epoch
    results/D4_6_mip_dynamics.json       — MIP integration details
    logs/execution_log.txt               — Full stdout capture
    logs/metadata.json                   — Provenance
"""

import argparse, csv, json, os, re, sys, time, hashlib
from collections import Counter, defaultdict
from datetime import datetime
from io import StringIO
import numpy as np

# ───────────────────────────────────────────────────────────────
# UTILITIES
# ───────────────────────────────────────────────────────────────
def sf(v):
    """Safe float conversion."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan

EPOCH_BOUNDS = {
    "E1": (None, 10500),
    "E2": (10500, 11600),
    "E3": (11600, None),
}

def get_epoch(t):
    for name, (lo, hi) in EPOCH_BOUNDS.items():
        if (lo is None or t >= lo) and (hi is None or t < hi):
            return name
    return "UNK"

STATE_VARS = [
    "connectome_entropy", "b1_z", "active_edges",
    "vt_coverage", "vt_entropy", "sie_v2_valence_01",
]

OPERATOR_TICKS = [
    499, 3345, 3389, 3479, 3566, 4020, 4078, 4227,
    6819, 6823, 6828, 6832, 6836, 6841,
    10106, 10202, 10275, 11350, 12240, 12444, 12823, 12849,
    12991, 13237, 13415, 13726, 13791, 13866, 13967, 14009,
    14100, 14157, 14241, 14363, 14955, 15129, 15155, 15223,
    15300, 15301, 15400, 15730, 15880, 15992, 16169, 16185,
    16709, 16829, 17199,
]

class Logger:
    """Tee stdout to file and console."""
    def __init__(self, path):
        self.terminal = sys.stdout
        self.log = open(path, "w")
    def write(self, msg):
        self.terminal.write(msg)
        self.log.write(msg)
    def flush(self):
        self.terminal.flush()
        self.log.flush()
    def close(self):
        self.log.close()

def load_csv(path, encoding="utf-8"):
    with open(path, "r", encoding=encoding, errors="replace") as f:
        return list(csv.DictReader(f))

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True, default=str)

def save_csv(rows, path):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ───────────────────────────────────────────────────────────────
# DATA LOADERS
# ───────────────────────────────────────────────────────────────
def load_tick_states(data_dir):
    """Load utd_status_full.csv into numpy arrays."""
    path = os.path.join(data_dir, "utd_status_full.csv")
    rows = load_csv(path)
    ticks = np.array([int(sf(r["t"])) for r in rows])
    arrays = {}
    for var in STATE_VARS:
        arrays[var] = np.array([sf(r.get(var, 0)) for r in rows])
    # Extra columns
    for extra in ["adc_territories", "cohesion_components",
                  "homeostasis_pruned", "homeostasis_bridged",
                  "phase", "ute_in_count", "ute_text_count"]:
        arrays[extra] = np.array([sf(r.get(extra, 0)) for r in rows])
    print(f"  utd_status_full: {len(ticks)} ticks, range {ticks[0]}..{ticks[-1]}")
    return ticks, arrays, rows

def load_say_ticks(data_dir):
    rows = load_csv(os.path.join(data_dir, "utd_say_by_tick.csv"))
    return sorted(int(r["t"]) for r in rows)

def extract_operator_ticks(exchange_path):
    if not exchange_path or not os.path.exists(exchange_path):
        return OPERATOR_TICKS
    with open(exchange_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    ticks, current_tick = [], None
    msg_lengths = {}
    for line in lines:
        m = re.search(r'\[t=\s*(\d+)\]', line)
        if m:
            current_tick = int(m.group(1))
        if '**Justin:**' in line and current_tick is not None:
            ticks.append(current_tick)
            msg = line.split('**Justin:**')[1].strip()
            msg_lengths[current_tick] = len(msg.split())
    return sorted(set(ticks)), msg_lengths


# ───────────────────────────────────────────────────────────────
# ANALYSIS: D5.1 — Signed Permutation Test
# ───────────────────────────────────────────────────────────────
def run_d5_1(ticks_arr, arrays, operator_ticks, msg_lengths, out_dir):
    from scipy.stats import mannwhitneyu, spearmanr
    print("\n" + "=" * 60)
    print("D5.1: Operator Differentiation — Signed Permutation Test")
    print("=" * 60)

    PRE, POST = 5, 20
    N_PERMS = 500
    rng = np.random.RandomState(42)

    def get_deltas(event_ticks):
        deltas = {var: [] for var in STATE_VARS}
        event_data = []
        for et in event_ticks:
            pre_mask = (ticks_arr >= et - PRE) & (ticks_arr < et)
            post_mask = (ticks_arr > et) & (ticks_arr <= et + POST)
            if pre_mask.sum() < 2 or post_mask.sum() < 2:
                continue
            row = {"event_tick": et, "epoch": get_epoch(et)}
            for var in STATE_VARS:
                arr = arrays[var]
                pre = arr[pre_mask]; pre = pre[np.isfinite(pre)]
                post = arr[post_mask]; post = post[np.isfinite(post)]
                if len(pre) > 0 and len(post) > 0:
                    d = float(np.mean(post) - np.mean(pre))
                    deltas[var].append(d)
                    row[f"{var}_delta"] = round(d, 6)
                    row[f"{var}_pre_mean"] = round(float(np.mean(pre)), 6)
                    row[f"{var}_post_mean"] = round(float(np.mean(post)), 6)
            event_data.append(row)
        return {v: np.array(d) if d else np.array([]) for v, d in deltas.items()}, event_data

    # Real operator deltas
    real_deltas, op_event_data = get_deltas(operator_ticks)
    save_csv(op_event_data, os.path.join(out_dir, "results", "D5_1_operator_deltas.csv"))

    real_signed = {v: float(np.mean(d)) for v, d in real_deltas.items() if len(d) > 0}
    print("Real operator signed mean deltas:")
    for var, val in real_signed.items():
        print(f"  {var}: {val:+.6f} (n={len(real_deltas[var])})")

    # Corpus controls
    exclusion = set()
    for ot in operator_ticks:
        for dt in range(-30, 31):
            exclusion.add(ot + dt)
    control_pool = [int(t) for t in ticks_arr if int(t) not in exclusion]
    control_ticks = sorted(rng.choice(control_pool,
        size=min(len(operator_ticks) * 5, len(control_pool)), replace=False))
    ctrl_deltas, _ = get_deltas(control_ticks)

    # Mann-Whitney
    mw_results = {}
    for var in STATE_VARS:
        op = real_deltas.get(var, np.array([]))
        ct = ctrl_deltas.get(var, np.array([]))
        if len(op) >= 5 and len(ct) >= 5:
            u, p = mannwhitneyu(op, ct, alternative="two-sided")
            r_eff = float(u / (len(op) * len(ct))) - 0.5
            mw_results[var] = {
                "operator_mean": round(float(np.mean(op)), 6),
                "control_mean": round(float(np.mean(ct)), 6),
                "U": round(float(u), 1), "p": round(float(p), 6),
                "effect_r": round(r_eff, 4),
                "n_op": len(op), "n_ctrl": len(ct),
                "sig_005": p < 0.05, "sig_001": p < 0.001,
            }

    # Signed permutation test
    null_signed = {var: [] for var in STATE_VARS}
    print(f"\nRunning {N_PERMS} signed permutation shuffles...")
    for i in range(N_PERMS):
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{N_PERMS}...")
        shuf = sorted(rng.choice(ticks_arr, size=len(operator_ticks), replace=False))
        shuf_d, _ = get_deltas(shuf)
        for var in STATE_VARS:
            if len(shuf_d[var]) > 0:
                null_signed[var].append(float(np.mean(shuf_d[var])))

    perm_results = {}
    print("\nSIGNED PERMUTATION RESULTS:")
    for var in STATE_VARS:
        if var in real_signed and null_signed[var]:
            rv = real_signed[var]
            nv = np.array(null_signed[var])
            p_lo = float(np.mean(nv <= rv))
            p_hi = float(np.mean(nv >= rv))
            p_two = min(2 * min(p_lo, p_hi), 1.0)
            z = float((rv - np.mean(nv)) / max(np.std(nv), 1e-15))
            perm_results[var] = {
                "real_signed_mean": round(rv, 8),
                "null_mean": round(float(np.mean(nv)), 8),
                "null_std": round(float(np.std(nv)), 8),
                "z": round(z, 3), "p_two": round(p_two, 6),
                "n_perms": N_PERMS,
                "sig_005": p_two < 0.05, "sig_001": p_two < 0.001,
                "direction": "CONTRACTS" if rv < 0 else "EXPANDS",
            }
            sig = "***" if p_two < 0.001 else "**" if p_two < 0.01 else "*" if p_two < 0.05 else ""
            print(f"  {var:25s}  z={z:+6.2f}  p={p_two:.4f}  {sig}  [{perm_results[var]['direction']}]")

    # D5.1c: entropy response intensification
    ent_deltas_by_time = [(d["event_tick"], d.get("connectome_entropy_delta", np.nan))
                          for d in op_event_data if "connectome_entropy_delta" in d]
    if len(ent_deltas_by_time) > 10:
        t_vals = [x[0] for x in ent_deltas_by_time]
        d_vals = [x[1] for x in ent_deltas_by_time]
        rho_t, p_t = spearmanr(t_vals, d_vals)
        intensification = {
            "variable": "connectome_entropy",
            "rho": round(rho_t, 4), "p": round(p_t, 6),
            "interpretation": "INTENSIFIES" if rho_t < 0 and p_t < 0.05 else "no trend"
        }
    else:
        intensification = {"error": "too few data points"}

    # D5.1d: dose-response
    paired = [(d["event_tick"], d.get("active_edges_delta", np.nan))
              for d in op_event_data if "active_edges_delta" in d]
    dose_response = {}
    if len(paired) > 10:
        msg_w = [msg_lengths.get(t, 0) for t, _ in paired]
        edge_d = [d for _, d in paired]
        rho_dr, p_dr = spearmanr(msg_w, edge_d)
        short = [d for w, d in zip(msg_w, edge_d) if w < 10]
        long = [d for w, d in zip(msg_w, edge_d) if w >= 10]
        dose_response = {
            "rho": round(rho_dr, 4), "p": round(p_dr, 6),
            "short_msg_mean_delta": round(float(np.mean(short)), 0) if short else None,
            "long_msg_mean_delta": round(float(np.mean(long)), 0) if long else None,
            "interpretation": "no dose-response" if p_dr > 0.05 else "dose-response present",
        }

    result = {
        "signed_permutation": perm_results,
        "mann_whitney": mw_results,
        "intensification": intensification,
        "dose_response": dose_response,
        "config": {"PRE": PRE, "POST": POST, "N_PERMS": N_PERMS, "seed": 42},
    }
    save_json(result, os.path.join(out_dir, "results", "D5_1_signed_permutation.json"))
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: Family 10 — Silence + D8.6 Inter-Say Intervals
# ───────────────────────────────────────────────────────────────
def run_family_10(ticks_arr, arrays, say_ticks, out_dir):
    from scipy.stats import mannwhitneyu, kstest
    print("\n" + "=" * 60)
    print("FAMILY 10: Silence Analysis + D8.6 Inter-Say Intervals")
    print("=" * 60)

    say_set = set(say_ticks)
    n = len(ticks_arr)

    pre_speech = {v: [] for v in STATE_VARS}
    silence = {v: [] for v in STATE_VARS}
    post_speech = {v: [] for v in STATE_VARS}

    for i in range(n):
        t = int(ticks_arr[i])
        is_pre = any((st - 5 <= t < st) for st in say_ticks if abs(st - t) < 10)
        is_post = any((st < t <= st + 5) for st in say_ticks if abs(st - t) < 10)
        is_say = t in say_set
        for var in STATE_VARS:
            v = arrays[var][i]
            if np.isfinite(v):
                if is_pre:
                    pre_speech[var].append(v)
                elif is_post:
                    post_speech[var].append(v)
                elif not is_say:
                    silence[var].append(v)

    # Pre-speech vs silence
    silence_results = {"pre_vs_silence": {}, "post_vs_silence": {}}
    comparison_rows = []
    for label, group in [("pre_vs_silence", pre_speech), ("post_vs_silence", post_speech)]:
        for var in STATE_VARS:
            g = np.array(group[var])
            s = np.array(silence[var])
            if len(g) > 10 and len(s) > 10:
                u, p = mannwhitneyu(g, s, alternative="two-sided")
                sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
                res = {
                    "group_mean": round(float(np.mean(g)), 6),
                    "silence_mean": round(float(np.mean(s)), 6),
                    "diff": round(float(np.mean(g) - np.mean(s)), 6),
                    "U": round(float(u), 1), "p": round(float(p), 6),
                    "n_group": len(g), "n_silence": len(s),
                    "sig_001": p < 0.001,
                }
                silence_results[label][var] = res
                comparison_rows.append({
                    "comparison": label, "variable": var, **res
                })
                print(f"  {label} {var:25s}  diff={res['diff']:+.4f}  p={p:.6f} {sig}")

    save_csv(comparison_rows, os.path.join(out_dir, "results", "F10_silence_comparison.csv"))

    # Inter-say intervals
    intervals = np.diff(say_ticks)
    _, p_exp = kstest(intervals, 'expon', args=(0, np.mean(intervals)))
    med = float(np.median(intervals))

    interval_rows = [{"say_tick": say_ticks[i], "interval": int(intervals[i]),
                       "epoch": get_epoch(say_ticks[i])}
                     for i in range(len(intervals))]
    save_csv(interval_rows, os.path.join(out_dir, "results", "F10_inter_say_intervals.csv"))

    # By epoch
    epoch_intervals = {}
    for ep in ["E1", "E2", "E3"]:
        ep_iv = [int(intervals[i]) for i in range(len(intervals)) if get_epoch(say_ticks[i]) == ep]
        if ep_iv:
            epoch_intervals[ep] = {
                "n": len(ep_iv), "mean": round(float(np.mean(ep_iv)), 1),
                "median": round(float(np.median(ep_iv)), 1),
                "CV": round(float(np.std(ep_iv) / np.mean(ep_iv)), 3),
            }

    # Burst detection
    short_thresh = float(np.percentile(intervals, 25))
    burst_lens = []
    current = 0
    for iv in intervals:
        if iv <= short_thresh:
            current += 1
        else:
            if current > 0:
                burst_lens.append(current)
            current = 0
    if current > 0:
        burst_lens.append(current)

    interval_result = {
        "n_intervals": len(intervals),
        "mean": round(float(np.mean(intervals)), 1),
        "median": round(float(np.median(intervals)), 1),
        "std": round(float(np.std(intervals)), 1),
        "CV": round(float(np.std(intervals) / np.mean(intervals)), 3),
        "min": int(np.min(intervals)), "max": int(np.max(intervals)),
        "exponential_test_p": round(float(p_exp), 8),
        "reject_exponential": p_exp < 0.05,
        "gt_2x_median_pct": round(float(np.sum(intervals > 2 * med) / len(intervals) * 100), 1),
        "gt_5x_median_pct": round(float(np.sum(intervals > 5 * med) / len(intervals) * 100), 1),
        "by_epoch": epoch_intervals,
        "n_bursts": len(burst_lens),
        "mean_burst_len": round(float(np.mean(burst_lens)), 1) if burst_lens else 0,
        "max_burst_len": max(burst_lens) if burst_lens else 0,
    }

    print(f"\n  D8.6: {len(intervals)} intervals, CV={interval_result['CV']:.3f}")
    print(f"    Exponential test: p={p_exp:.2e} → {'REJECT' if p_exp < 0.05 else 'cannot reject'}")
    print(f"    {len(burst_lens)} bursts, max length {max(burst_lens) if burst_lens else 0}")

    result = {"silence_analysis": silence_results, "inter_say_intervals": interval_result}
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: Family 12 — Developmental Ontogeny
# ───────────────────────────────────────────────────────────────
def run_family_12(ticks_arr, arrays, status_rows, out_dir):
    from scipy.stats import spearmanr
    print("\n" + "=" * 60)
    print("FAMILY 12: Developmental Ontogeny")
    print("=" * 60)

    terr = arrays["adc_territories"]
    n = len(ticks_arr)

    # Territory emergence
    first_appearance = {}
    transitions = []
    prev = None
    timeline_rows = []
    for i in range(n):
        t = int(ticks_arr[i])
        tv = int(terr[i]) if np.isfinite(terr[i]) else 0
        if tv not in first_appearance:
            first_appearance[tv] = t
        if prev is not None and tv != prev:
            transitions.append({"t": t, "from": prev, "to": tv, "epoch": get_epoch(t)})
        prev = tv
        timeline_rows.append({"t": t, "territories": tv, "epoch": get_epoch(t)})

    save_csv(timeline_rows[::100], os.path.join(out_dir, "results", "D12_territory_timeline.csv"))  # subsample

    print(f"  Territory emergence:")
    emergence = {}
    for tv in sorted(first_appearance.keys()):
        t = first_appearance[tv]
        emergence[str(tv)] = {"first_tick": t, "epoch": get_epoch(t)}
        print(f"    {tv} territories: t={t} ({get_epoch(t)})")

    # Time at each count
    durations = defaultdict(int)
    for i in range(n - 1):
        tv = int(terr[i]) if np.isfinite(terr[i]) else 0
        dt = int(ticks_arr[i + 1] - ticks_arr[i])
        durations[tv] += dt
    total_time = sum(durations.values())

    # Correlations
    correlations = {}
    for var in ["connectome_entropy", "active_edges", "vt_entropy", "vt_coverage",
                "sie_v2_valence_01", "b1_z"]:
        valid = np.isfinite(terr) & np.isfinite(arrays[var])
        if valid.sum() > 100:
            rho, p = spearmanr(terr[valid], arrays[var][valid])
            correlations[var] = {"rho": round(rho, 4), "p": float(p)}

    # Cohesion
    coh = arrays["cohesion_components"]
    frag_count = int(np.sum(coh > 1))

    # Homeostasis
    pruned = arrays["homeostasis_pruned"]
    bridged = arrays["homeostasis_bridged"]
    homeo_rows = []
    for ep in ["E1", "E2", "E3"]:
        mask = np.array([get_epoch(int(t)) == ep for t in ticks_arr])
        ep_p = pruned[mask]
        ep_b = bridged[mask]
        nz_p = int(np.sum(ep_p > 0))
        nz_b = int(np.sum(ep_b > 0))
        homeo_rows.append({
            "epoch": ep, "n_ticks": int(mask.sum()),
            "pruning_events": nz_p,
            "pruning_mean_when_active": round(float(np.mean(ep_p[ep_p > 0])), 1) if nz_p > 0 else 0,
            "bridging_events": nz_b,
            "bridging_mean_when_active": round(float(np.mean(ep_b[ep_b > 0])), 1) if nz_b > 0 else 0,
        })
        print(f"  {ep}: pruning={nz_p}, bridging={nz_b}")

    save_csv(homeo_rows, os.path.join(out_dir, "results", "D12_homeostasis_events.csv"))

    result = {
        "territory_emergence": emergence,
        "transitions": transitions,
        "time_at_count": {str(k): {"ticks": v, "pct": round(v / total_time * 100, 1)}
                          for k, v in sorted(durations.items())},
        "correlations": correlations,
        "cohesion": {"fragmented_ticks": frag_count, "total": n,
                     "pct": round(frag_count / n * 100, 3)},
        "homeostasis": homeo_rows,
    }
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: Family 14 — Composer/Decoder Masking
# ───────────────────────────────────────────────────────────────
def run_family_14(data_dir, out_dir):
    from scipy.stats import spearmanr
    print("\n" + "=" * 60)
    print("FAMILY 14: Composer/Decoder Masking")
    print("=" * 60)

    rows = load_csv(os.path.join(data_dir, "say_event_composer_audit_metrics.csv"))
    print(f"  {len(rows)} say events")

    def get_vals(col):
        return [sf(r[col]) for r in rows if np.isfinite(sf(r[col]))]

    tri = get_vals("tri_frac_in_corpus")
    lcs = get_vals("lcs_frac_say")
    jac = get_vals("best_all_jaccard")
    imm = get_vals("imm_jaccard")

    # Unique ratio
    uniq = []
    for r in rows:
        slen = sf(r["say_len_tokens"])
        suniq = sf(r["say_unique_tokens"])
        if slen > 0:
            uniq.append(suniq / slen)

    # Self-reference
    past_sim = get_vals("past_tfidf_top1_sim")
    past_lag = get_vals("past_tfidf_top1_lag")

    # Trend
    ticks = [int(sf(r["t"])) for r in rows if np.isfinite(sf(r["tri_frac_in_corpus"]))]
    tri_vals = [sf(r["tri_frac_in_corpus"]) for r in rows if np.isfinite(sf(r["tri_frac_in_corpus"]))]
    rho, pval = spearmanr(ticks, tri_vals) if len(ticks) > 10 else (np.nan, np.nan)

    # By epoch
    by_epoch = {}
    for ep in ["E1", "E2", "E3"]:
        ep_tri = [sf(r["tri_frac_in_corpus"]) for r in rows
                  if get_epoch(int(sf(r["t"]))) == ep and np.isfinite(sf(r["tri_frac_in_corpus"]))]
        if ep_tri:
            zero = sum(1 for v in ep_tri if v == 0)
            by_epoch[ep] = {
                "n": len(ep_tri), "mean_tri": round(np.mean(ep_tri), 4),
                "zero_overlap": zero, "zero_pct": round(zero / len(ep_tri) * 100, 1),
            }

    result = {
        "D14_1_trigram": {"mean": round(np.mean(tri), 4), "median": round(np.median(tri), 4),
                          "zero_count": sum(1 for v in tri if v == 0),
                          "zero_pct": round(sum(1 for v in tri if v == 0) / len(tri) * 100, 1)},
        "D14_2_lcs": {"mean": round(np.mean(lcs), 4),
                      "lt30_pct": round(sum(1 for v in lcs if v < 0.3) / len(lcs) * 100, 1)},
        "D14_3_jaccard": {"mean": round(np.mean(jac), 4),
                          "lt30_pct": round(sum(1 for v in jac if v < 0.3) / len(jac) * 100, 1)},
        "D14_4_immediate": {"mean": round(np.mean(imm), 4)},
        "D14_5_uniqueness": {"mean": round(np.mean(uniq), 4)},
        "D14_6_self_ref": {"mean_sim": round(np.mean(past_sim), 4) if past_sim else None,
                           "median_lag": round(np.median(past_lag), 0) if past_lag else None},
        "trend": {"rho": round(rho, 4), "p": round(pval, 6)},
        "by_epoch": by_epoch,
    }
    save_json(result, os.path.join(out_dir, "results", "F14_composer_audit.json"))
    for k, v in result.items():
        if isinstance(v, dict) and "mean" in v:
            print(f"  {k}: {v}")
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: State-Space Geometry (PCA)
# ───────────────────────────────────────────────────────────────
def run_state_space(data_dir, out_dir):
    from scipy.spatial.distance import cdist
    from scipy.stats import entropy as sp_entropy
    print("\n" + "=" * 60)
    print("D2.8–2.11: State-Space Geometry")
    print("=" * 60)

    rows = load_csv(os.path.join(data_dir, "pca_state_space_Aura.csv"))
    ticks = np.array([int(sf(r["t"])) for r in rows])
    pc_cols = ["PC1", "PC2", "PC3"]
    pc = np.array([[sf(r[c]) for c in pc_cols] for r in rows])
    print(f"  {len(rows)} rows, PCs: {pc_cols}")

    # Speed
    speeds = np.sqrt(np.sum(np.diff(pc, axis=0) ** 2, axis=1))
    speed_by_epoch = {}
    for ep in ["E1", "E2", "E3"]:
        mask = np.array([get_epoch(int(t)) == ep for t in ticks[1:]])
        if mask.sum() > 0:
            speed_by_epoch[ep] = {"mean": round(float(np.mean(speeds[mask])), 4),
                                   "std": round(float(np.std(speeds[mask])), 4),
                                   "n": int(mask.sum())}

    # Occupancy entropy
    occ = {}
    for ep in ["E1", "E2", "E3"]:
        mask = np.array([get_epoch(int(t)) == ep for t in ticks])
        if mask.sum() > 10:
            ep_pc = pc[mask, :2]
            h, _, _ = np.histogram2d(ep_pc[:, 0], ep_pc[:, 1], bins=20,
                                      range=[[pc[:, 0].min(), pc[:, 0].max()],
                                             [pc[:, 1].min(), pc[:, 1].max()]])
            h_flat = h.flatten()
            h_prob = h_flat / h_flat.sum()
            h_prob = h_prob[h_prob > 0]
            occ[ep] = {
                "entropy_bits": round(float(sp_entropy(h_prob)), 4),
                "occupied_pct": round(float(np.sum(h_flat > 0) / 400 * 100), 1),
            }

    # Recurrence (subsampled)
    sub_idx = np.arange(0, len(pc), 10)
    sub_pc = pc[sub_idx]
    sub_ticks = ticks[sub_idx]
    D = cdist(sub_pc, sub_pc, metric='euclidean')
    recurrence_dists = []
    for i in range(len(sub_pc)):
        candidates = np.where(np.abs(sub_ticks - sub_ticks[i]) > 100)[0]
        if len(candidates) > 0:
            recurrence_dists.append(float(np.min(D[i, candidates])))

    # Centroid drift
    window = 200
    centroids = []
    for i in range(0, len(pc) - window, window // 2):
        centroids.append(np.mean(pc[i:i + window, :3], axis=0))
    drifts = [float(np.linalg.norm(centroids[i + 1] - centroids[i]))
              for i in range(len(centroids) - 1)] if len(centroids) > 1 else []

    result = {
        "D2_8_occupancy": occ,
        "D2_9_recurrence": {
            "median_dist": round(float(np.median(recurrence_dists)), 4),
            "mean_dist": round(float(np.mean(recurrence_dists)), 4),
        },
        "D2_10_centroid_drift": {
            "total_displacement": round(float(np.linalg.norm(centroids[-1] - centroids[0])), 4) if len(centroids) > 1 else None,
            "mean_drift": round(float(np.mean(drifts)), 4) if drifts else None,
        },
        "D3_speed_by_epoch": speed_by_epoch,
    }
    save_json(result, os.path.join(out_dir, "results", "D2_state_space_geometry.json"))
    for k, v in result.items():
        print(f"  {k}: {v}")
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: Family 8 — Rolling Variance + CSD
# ───────────────────────────────────────────────────────────────
def run_family_8(data_dir, out_dir):
    print("\n" + "=" * 60)
    print("FAMILY 8: Rolling Variance, CSD, Change-Points")
    print("=" * 60)

    rows = load_csv(os.path.join(data_dir, "rolling_var_autocorr_entropy.csv"))
    ticks = np.array([int(sf(r["t"])) for r in rows])
    var_v = np.array([sf(r["rolling_variance"]) for r in rows])
    ac_v = np.array([sf(r["rolling_autocorr_lag1"]) for r in rows])
    valid = np.isfinite(var_v) & np.isfinite(ac_v)
    ticks, var_v, ac_v = ticks[valid], var_v[valid], ac_v[valid]

    # By epoch
    epoch_stats = {}
    for ep in ["E1", "E2", "E3"]:
        mask = np.array([get_epoch(int(t)) == ep for t in ticks])
        if mask.sum() > 0:
            epoch_stats[ep] = {
                "var_mean": round(float(np.mean(var_v[mask])), 6),
                "var_std": round(float(np.std(var_v[mask])), 6),
                "ac_mean": round(float(np.mean(ac_v[mask])), 4),
                "ac_std": round(float(np.std(ac_v[mask])), 4),
                "n": int(mask.sum()),
            }

    # Change-points
    half = 50
    diffs = []
    for i in range(half, len(var_v) - half):
        left = float(np.mean(var_v[i - half:i]))
        right = float(np.mean(var_v[i:i + half]))
        diffs.append(abs(right - left))
    diffs = np.array(diffs)
    top5 = np.argsort(diffs)[-5:][::-1]
    change_points = [{"rank": rank + 1, "t": int(ticks[idx + half]),
                      "epoch": get_epoch(int(ticks[idx + half])),
                      "magnitude": round(float(diffs[idx]), 6)}
                     for rank, idx in enumerate(top5)]

    # CSD at boundaries
    csd = {}
    for b in [10500, 11600]:
        pre = (ticks >= b - 300) & (ticks < b)
        post = (ticks >= b) & (ticks < b + 300)
        if pre.sum() > 10 and post.sum() > 10:
            csd[str(b)] = {
                "pre_ac": round(float(np.mean(ac_v[pre])), 4),
                "post_ac": round(float(np.mean(ac_v[post])), 4),
                "pre_var": round(float(np.mean(var_v[pre])), 6),
                "post_var": round(float(np.mean(var_v[post])), 6),
                "ac_increase": bool(np.mean(ac_v[post]) > np.mean(ac_v[pre])),
                "var_increase": bool(np.mean(var_v[post]) > np.mean(var_v[pre])),
                "var_ratio": round(float(np.mean(var_v[post]) / max(np.mean(var_v[pre]), 1e-12)), 1),
            }

    result = {"by_epoch": epoch_stats, "change_points": change_points, "CSD": csd}
    save_json(result, os.path.join(out_dir, "results", "D8_rolling_variance.json"))
    for k, v in result.items():
        print(f"  {k}: {v}")
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: Batch 2 — Per-Neuron
# ───────────────────────────────────────────────────────────────
def run_per_neuron(data_dir, out_dir):
    from scipy.stats import spearmanr
    print("\n" + "=" * 60)
    print("BATCH 2: Per-Neuron Specialization & Hub Analysis")
    print("=" * 60)

    snapshots = [17160, 17220, 17280, 17340, 17400]
    snap_data = {}
    for tick in snapshots:
        fname = os.path.join(data_dir, f"node_embedding_metrics_state_{tick}.csv")
        if os.path.exists(fname):
            snap_data[tick] = load_csv(fname)

    if not snap_data:
        return {"error": "no node_embedding files found"}

    cols = list(snap_data[snapshots[0]][0].keys())
    metric_cols = [c for c in cols if c not in ("node", "node_id", "id", "territory", "community")]
    test_row = snap_data[snapshots[0]][0]
    metric_cols = [c for c in metric_cols if np.isfinite(sf(test_row.get(c)))]

    # D3.9: Cross-neuron variance trend
    specialization = {}
    for col in metric_cols[:8]:
        variances = []
        for tick in snapshots:
            if tick in snap_data:
                vals = [sf(r.get(col)) for r in snap_data[tick]]
                vals = [v for v in vals if np.isfinite(v)]
                if vals:
                    variances.append(float(np.var(vals)))
        if len(variances) >= 3:
            rho, p = spearmanr(range(len(variances)), variances)
            specialization[col] = {
                "variances": [round(v, 4) for v in variances],
                "rho": round(rho, 3), "p": round(p, 4),
            }

    # D3.10: Plasticity Gini
    plasticity = {}
    for col in metric_cols[:5]:
        n_neurons = len(snap_data[snapshots[0]])
        neuron_vars = []
        for i in range(min(n_neurons, 5000)):
            vals = []
            for tick in snapshots:
                if tick in snap_data and i < len(snap_data[tick]):
                    v = sf(snap_data[tick][i].get(col))
                    if np.isfinite(v):
                        vals.append(v)
            if len(vals) >= 3:
                neuron_vars.append(float(np.var(vals)))
        if neuron_vars:
            nv = np.sort(neuron_vars)
            n = len(nv)
            gini = float((2 * np.sum(np.arange(1, n + 1) * nv) / (n * np.sum(nv))) - (n + 1) / n)
            cumsum = np.cumsum(nv[::-1]) / np.sum(nv)
            n_80 = int(np.searchsorted(cumsum, 0.8) + 1)
            plasticity[col] = {
                "gini": round(gini, 4),
                "top_pct_for_80": round(n_80 / n * 100, 1),
            }

    # D3.11: Hub turnover
    K = 50
    hub_sets = {}
    for tick in snapshots:
        if tick in snap_data:
            vals = [(i, sf(r.get("out_degree", 0))) for i, r in enumerate(snap_data[tick])]
            vals = [(i, v) for i, v in vals if np.isfinite(v)]
            vals.sort(key=lambda x: -x[1])
            hub_sets[tick] = set(i for i, _ in vals[:K])

    hub_jaccards = {}
    for i in range(len(snapshots) - 1):
        t1, t2 = snapshots[i], snapshots[i + 1]
        if t1 in hub_sets and t2 in hub_sets:
            inter = len(hub_sets[t1] & hub_sets[t2])
            union = len(hub_sets[t1] | hub_sets[t2])
            hub_jaccards[f"{t1}_{t2}"] = {"jaccard": round(inter / union, 3) if union > 0 else 0,
                                            "shared": inter}

    persistent = set.intersection(*hub_sets.values()) if len(hub_sets) >= 3 else set()
    ever_hub = set.union(*hub_sets.values()) if hub_sets else set()

    result = {
        "D3_9_specialization": specialization,
        "D3_10_plasticity": plasticity,
        "D3_11_hub_turnover": {
            "K": K, "consecutive_jaccards": hub_jaccards,
            "persistent_hubs": len(persistent),
            "total_ever_hub": len(ever_hub),
            "turnover_ratio": round(1 - len(persistent) / K, 3),
        },
    }
    save_json(result, os.path.join(out_dir, "results", "D3_neuron_analysis.json"))
    print(f"  Hub turnover: {len(persistent)} persistent / {K} (turnover={1 - len(persistent)/K:.2f})")
    return result


# ───────────────────────────────────────────────────────────────
# ANALYSIS: D2.11 Landscape Migration + D7.7 LZ + D4.6 MIP
# ───────────────────────────────────────────────────────────────
def run_remaining(data_dir, out_dir):
    from scipy.spatial.distance import jensenshannon
    from scipy.stats import spearmanr
    print("\n" + "=" * 60)
    print("D2.11 + D7.7 + D4.6: Landscape, LZ, MIP")
    print("=" * 60)

    # Landscape migration
    snapshots = [17160, 17220, 17280, 17340, 17400]
    grids = {}
    for tick in snapshots:
        fname = os.path.join(data_dir, f"baseline_projection_grid_pi_state_{tick}_32x32.csv")
        try:
            with open(fname) as f:
                reader = csv.reader(f)
                raw = [row for row in reader]
            grid = np.array([[sf(v) for v in row[1:]] for row in raw[1:]])
            grid[grid < 0] = 0
            total = grid.sum()
            if total > 0:
                grids[tick] = grid / total
        except:
            pass

    landscape = {}
    if len(grids) >= 2:
        for i in range(len(snapshots) - 1):
            t1, t2 = snapshots[i], snapshots[i + 1]
            if t1 in grids and t2 in grids:
                p = grids[t1].flatten() + 1e-12
                q = grids[t2].flatten() + 1e-12
                p, q = p / p.sum(), q / q.sum()
                landscape[f"{t1}_{t2}"] = round(float(jensenshannon(p, q)), 4)

    # LZ complexity
    lz_rows = load_csv(os.path.join(data_dir, "lz_complexity_pca_sign_timeseries.csv"))
    lz_by_epoch = {}
    for ep in ["E1", "E2", "E3"]:
        vals = [sf(r["lz_pca_sign"]) for r in lz_rows
                if get_epoch(int(sf(r["t"]))) == ep and np.isfinite(sf(r["lz_pca_sign"]))]
        if vals:
            lz_by_epoch[ep] = {"n": len(vals), "mean": round(np.mean(vals), 6),
                                "std": round(np.std(vals), 6)}
    all_t = [int(sf(r["t"])) for r in lz_rows if np.isfinite(sf(r["lz_pca_sign"]))]
    all_lz = [sf(r["lz_pca_sign"]) for r in lz_rows if np.isfinite(sf(r["lz_pca_sign"]))]
    lz_rho, lz_p = spearmanr(all_t, all_lz)

    # MIP
    mip_rows = load_csv(os.path.join(data_dir, "mip_integration_timeseries.csv"))
    mip_by_epoch = {}
    for ep in ["E1", "E2", "E3"]:
        vals = [sf(r["mip_integration"]) for r in mip_rows
                if get_epoch(int(sf(r["t"]))) == ep and np.isfinite(sf(r["mip_integration"]))]
        if vals:
            nz = sum(1 for v in vals if v > 0.001)
            mip_by_epoch[ep] = {"n": len(vals), "mean": round(np.mean(vals), 6),
                                 "max": round(max(vals), 6),
                                 "nonzero_pct": round(nz / len(vals) * 100, 1)}

    singleton_by_epoch = defaultdict(lambda: defaultdict(int))
    for r in mip_rows:
        ep = get_epoch(int(sf(r["t"])))
        sv = r.get("singleton_variable", "")
        if sv:
            singleton_by_epoch[ep][sv] += 1

    result = {
        "D2_11_landscape_JSD": landscape,
        "D7_7_lz_complexity": {"by_epoch": lz_by_epoch, "trend_rho": round(lz_rho, 4),
                                "trend_p": float(lz_p)},
        "D4_6_mip": {"by_epoch": mip_by_epoch,
                      "singleton_dist": {ep: dict(v) for ep, v in singleton_by_epoch.items()}},
    }
    save_json(result, os.path.join(out_dir, "results", "D2_11_D7_7_D4_6.json"))
    for k, v in result.items():
        print(f"  {k}: {v}")
    return result


# ───────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Aura Session Analysis Bundle")
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--exchange", default=None)
    parser.add_argument("--out-dir", default="./session_analysis_results")
    args = parser.parse_args()

    # Setup directories
    for subdir in ["results", "logs"]:
        os.makedirs(os.path.join(args.out_dir, subdir), exist_ok=True)

    # Logging
    log_path = os.path.join(args.out_dir, "logs", "execution_log.txt")
    logger = Logger(log_path)
    sys.stdout = logger

    start_time = time.time()
    print(f"Aura Session Analysis Bundle")
    print(f"Started: {datetime.now().isoformat()}")
    print(f"Data dir: {args.data_dir}")
    print(f"Exchange: {args.exchange}")
    print(f"Output: {args.out_dir}")

    # Load core data
    print("\n" + "=" * 60)
    print("LOADING DATA")
    print("=" * 60)
    ticks_arr, arrays, status_rows = load_tick_states(args.data_dir)
    say_ticks = load_say_ticks(args.data_dir)
    print(f"  Say events: {len(say_ticks)}")

    if args.exchange:
        operator_ticks, msg_lengths = extract_operator_ticks(args.exchange)
    else:
        operator_ticks, msg_lengths = OPERATOR_TICKS, {}
    print(f"  Operator ticks: {len(operator_ticks)}")

    # Run all analyses
    all_results = {}
    stat_rows = []  # Unified statistical test table

    # D5.1
    d5_1 = run_d5_1(ticks_arr, arrays, operator_ticks, msg_lengths, args.out_dir)
    all_results["D5_1"] = d5_1
    for var, res in d5_1.get("signed_permutation", {}).items():
        stat_rows.append({"test": "D5.1_signed_perm", "variable": var,
                          "statistic": f"z={res['z']}", "p_value": res["p_two"],
                          "significant": res["sig_001"], "notes": res["direction"]})
    for var, res in d5_1.get("mann_whitney", {}).items():
        stat_rows.append({"test": "D5.1_mann_whitney", "variable": var,
                          "statistic": f"U={res['U']}", "p_value": res["p"],
                          "significant": res["sig_001"], "notes": f"r={res['effect_r']}"})

    # Family 10 + D8.6
    f10 = run_family_10(ticks_arr, arrays, say_ticks, args.out_dir)
    all_results["F10_D8_6"] = f10
    for comp in ["pre_vs_silence", "post_vs_silence"]:
        for var, res in f10.get("silence_analysis", {}).get(comp, {}).items():
            stat_rows.append({"test": f"F10_{comp}", "variable": var,
                              "statistic": f"U={res['U']}", "p_value": res["p"],
                              "significant": res["sig_001"], "notes": f"diff={res['diff']}"})

    # Family 12
    f12 = run_family_12(ticks_arr, arrays, status_rows, args.out_dir)
    all_results["F12"] = f12

    # Family 14
    f14 = run_family_14(args.data_dir, args.out_dir)
    all_results["F14"] = f14

    # State-space geometry
    ss = run_state_space(args.data_dir, args.out_dir)
    all_results["state_space"] = ss

    # Family 8
    f8 = run_family_8(args.data_dir, args.out_dir)
    all_results["F8"] = f8

    # Per-neuron
    pn = run_per_neuron(args.data_dir, args.out_dir)
    all_results["per_neuron"] = pn

    # Remaining (landscape, LZ, MIP)
    rem = run_remaining(args.data_dir, args.out_dir)
    all_results["remaining"] = rem

    # Save master results
    save_json(all_results, os.path.join(args.out_dir, "results", "master_results.json"))

    # Save unified statistical tests table
    save_csv(stat_rows, os.path.join(args.out_dir, "results", "statistical_tests.csv"))

    # Metadata
    elapsed = time.time() - start_time
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "data_dir": args.data_dir,
        "exchange_file": args.exchange,
        "n_ticks": len(ticks_arr),
        "n_say_events": len(say_ticks),
        "n_operator_messages": len(operator_ticks),
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "input_hashes": {},
    }
    # Hash key input files
    for fname in ["utd_status_full.csv", "utd_say_by_tick.csv",
                  "say_event_composer_audit_metrics.csv", "pca_state_space_Aura.csv",
                  "rolling_var_autocorr_entropy.csv"]:
        fpath = os.path.join(args.data_dir, fname)
        if os.path.exists(fpath):
            metadata["input_hashes"][fname] = file_sha256(fpath)
    save_json(metadata, os.path.join(args.out_dir, "logs", "metadata.json"))

    # Print manifest
    print(f"\n{'='*60}")
    print(f"COMPLETE — {elapsed:.1f} seconds")
    print(f"{'='*60}")
    print(f"\nOutput files:")
    for root, dirs, files in os.walk(args.out_dir):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, args.out_dir)
            size = os.path.getsize(fpath)
            print(f"  {rel} ({size:,} bytes)")

    sys.stdout = logger.terminal
    logger.close()
    print(f"\nDone. Results in {args.out_dir}/")
    print(f"Execution log: {log_path}")


if __name__ == "__main__":
    main()
