#!/usr/bin/env python3
"""
D5.1 — Operator vs. Corpus Input Differentiation
==================================================
Tests whether the VDM runtime treated Justin's direct messages
as a statistically distinct causal class compared to ordinary
corpus input.

Analyses:
  A. Event-triggered state-change windows around operator messages
  B. Matched corpus-input control windows
  C. Permutation test (shuffle operator timestamps N times)
  D. Binary classifier: can local post-input changes predict
     whether the input was operator or corpus?
  E. Reply-lag and output-length comparison (D5.6)

Run:
    python d5_1_operator_differentiation.py \
        --data-dir ./Aura_Analysis_Tables \
        --exchange ./aura_justin_exchange.md \
        --out-dir ./d5_1_results

Requires: numpy, scipy.  Optional: sklearn (for classifier test).
"""

import argparse, csv, json, os, re, sys
from collections import defaultdict
from pathlib import Path
import numpy as np

# ---------------------------------------------------------------------------
# OPERATOR MESSAGE TICKS (extracted from aura_justin_exchange.md)
# If exchange file is provided, these are extracted automatically.
# Otherwise, this hardcoded list is used as fallback.
# ---------------------------------------------------------------------------
OPERATOR_TICKS_FALLBACK = [
    499, 3345, 3389, 3479, 3566, 4020, 4078, 4227,
    6819, 6823, 6828, 6832, 6836, 6841,
    10106, 10202, 10275, 11350, 12240, 12444, 12823, 12849,
    12991, 13237, 13415, 13726, 13791, 13866, 13967, 14009,
    14100, 14157, 14241, 14363, 14955, 15129, 15155, 15223,
    15300, 15301, 15400, 15730, 15880, 15992, 16169, 16185,
    16709, 16829, 17199,
]

# State variables to track
STATE_VARS = [
    "connectome_entropy", "b1_z", "active_edges",
    "firing_var", "vt_entropy", "vt_coverage",
    "sie_v2_valence_01",
]

# Window sizes (in ticks)
PRE_WINDOW = 5    # ticks before the event
POST_WINDOW = 20  # ticks after the event
N_PERMUTATIONS = 2000  # shuffle iterations


def safe_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


# ---------------------------------------------------------------------------
# 1. EXTRACT OPERATOR TICKS FROM EXCHANGE FILE
# ---------------------------------------------------------------------------
def extract_operator_ticks(exchange_path):
    """Parse aura_justin_exchange.md and extract tick numbers for Justin's messages."""
    if not os.path.exists(exchange_path):
        print(f"[WARN] Exchange file not found: {exchange_path}")
        return OPERATOR_TICKS_FALLBACK

    with open(exchange_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    ticks = []
    current_tick = None
    for i, line in enumerate(lines):
        tick_match = re.search(r'\[t=\s*(\d+)\]', line)
        if tick_match:
            current_tick = int(tick_match.group(1))
        if '**Justin:**' in line and current_tick is not None:
            ticks.append(current_tick)

    if not ticks:
        print("[WARN] No operator ticks extracted, using fallback list")
        return OPERATOR_TICKS_FALLBACK

    print(f"Extracted {len(ticks)} operator message ticks from exchange file")
    print(f"  Range: t={min(ticks)} to t={max(ticks)}")
    return sorted(set(ticks))


# ---------------------------------------------------------------------------
# 2. LOAD TICK-LEVEL STATE DATA
# ---------------------------------------------------------------------------
def load_tick_states(data_dir):
    """Load utd_status_full.csv for tick-level state."""
    path = os.path.join(data_dir, "utd_status_full.csv")
    if not os.path.exists(path):
        print("[FATAL] utd_status_full.csv not found")
        sys.exit(1)
    print(f"Loading tick states from utd_status_full.csv...")
    states = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            t = int(r.get("t", 0))
            state = {}
            for var in STATE_VARS:
                state[var] = safe_float(r.get(var))
            states[t] = state
    print(f"  Loaded {len(states)} ticks, range {min(states)}..{max(states)}")
    return states


def load_say_events(data_dir):
    """Load say events with their ticks."""
    path = os.path.join(data_dir, "utd_say_by_tick.csv")
    if not os.path.exists(path):
        return set()
    say_ticks = set()
    with open(path, "r") as f:
        for r in csv.DictReader(f):
            say_ticks.add(int(r["t"]))
    return say_ticks


# ---------------------------------------------------------------------------
# 3. EVENT-TRIGGERED ANALYSIS
# ---------------------------------------------------------------------------
def compute_event_triggered_response(tick_states, event_ticks, pre=PRE_WINDOW, post=POST_WINDOW):
    """
    For each event tick, extract the state-change vector in the post-window
    relative to the pre-window baseline.

    Returns dict: {variable_name: [delta_values_per_event]}
    """
    all_ticks = sorted(tick_states.keys())
    tick_set = set(all_ticks)
    deltas = defaultdict(list)
    raw_responses = []

    for et in event_ticks:
        # Find pre-window ticks
        pre_ticks = [t for t in all_ticks if et - pre <= t < et]
        # Find post-window ticks
        post_ticks = [t for t in all_ticks if et < t <= et + post]

        if len(pre_ticks) < 2 or len(post_ticks) < 2:
            continue

        response = {"event_tick": et}
        for var in STATE_VARS:
            pre_vals = [tick_states[t][var] for t in pre_ticks if np.isfinite(tick_states[t][var])]
            post_vals = [tick_states[t][var] for t in post_ticks if np.isfinite(tick_states[t][var])]
            if pre_vals and post_vals:
                pre_mean = np.mean(pre_vals)
                post_mean = np.mean(post_vals)
                delta = post_mean - pre_mean
                deltas[var].append(delta)
                response[f"{var}_pre_mean"] = pre_mean
                response[f"{var}_post_mean"] = post_mean
                response[f"{var}_delta"] = delta

                # Also compute post-window max absolute deviation
                post_max_dev = max(abs(v - pre_mean) for v in post_vals)
                response[f"{var}_max_dev"] = post_max_dev

        raw_responses.append(response)

    return deltas, raw_responses


# ---------------------------------------------------------------------------
# 4. MATCHED CORPUS CONTROL WINDOWS
# ---------------------------------------------------------------------------
def generate_corpus_controls(tick_states, operator_ticks, n_controls_per_event=5, rng_seed=42):
    """
    For each operator event, sample n matched control ticks from the same
    epoch range that are NOT near any operator message.
    """
    rng = np.random.RandomState(rng_seed)
    all_ticks = sorted(tick_states.keys())

    # Define exclusion zones around operator messages (± 30 ticks)
    exclusion = set()
    for ot in operator_ticks:
        for dt in range(-30, 31):
            exclusion.add(ot + dt)

    # Available control ticks
    control_pool = [t for t in all_ticks if t not in exclusion]

    if len(control_pool) < len(operator_ticks) * n_controls_per_event:
        print(f"[WARN] Limited control pool: {len(control_pool)} available")
        n_controls_per_event = max(1, len(control_pool) // max(len(operator_ticks), 1))

    control_ticks = sorted(rng.choice(
        control_pool,
        size=min(len(operator_ticks) * n_controls_per_event, len(control_pool)),
        replace=False
    ))

    return list(control_ticks)


# ---------------------------------------------------------------------------
# 5. PERMUTATION TEST
# ---------------------------------------------------------------------------
def permutation_test(tick_states, operator_ticks, n_perms=N_PERMUTATIONS, rng_seed=42):
    """
    Shuffle operator timestamps among all available ticks.
    Recompute mean |delta| for each variable.
    Compare real operator response to shuffled distribution.
    """
    rng = np.random.RandomState(rng_seed)
    all_ticks = sorted(tick_states.keys())
    n_op = len(operator_ticks)

    # Real operator response
    real_deltas, _ = compute_event_triggered_response(tick_states, operator_ticks)
    real_mean_abs = {}
    for var in STATE_VARS:
        if real_deltas[var]:
            real_mean_abs[var] = np.mean(np.abs(real_deltas[var]))

    # Null distribution
    null_dist = defaultdict(list)
    print(f"  Running {n_perms} permutations...")
    for i in range(n_perms):
        if (i + 1) % 500 == 0:
            print(f"    permutation {i+1}/{n_perms}")
        # Sample random ticks
        shuffled = sorted(rng.choice(all_ticks, size=n_op, replace=False))
        shuf_deltas, _ = compute_event_triggered_response(tick_states, shuffled)
        for var in STATE_VARS:
            if shuf_deltas[var]:
                null_dist[var].append(np.mean(np.abs(shuf_deltas[var])))

    # Compute p-values
    results = {}
    for var in STATE_VARS:
        if var in real_mean_abs and null_dist[var]:
            real_val = real_mean_abs[var]
            null_vals = np.array(null_dist[var])
            p_value = np.mean(null_vals >= real_val)
            results[var] = {
                "real_mean_abs_delta": round(float(real_val), 8),
                "null_mean": round(float(np.mean(null_vals)), 8),
                "null_std": round(float(np.std(null_vals)), 8),
                "z_score": round(float((real_val - np.mean(null_vals)) / max(np.std(null_vals), 1e-12)), 3),
                "p_value": round(float(p_value), 6),
                "n_permutations": n_perms,
                "significant_at_005": p_value < 0.05,
                "significant_at_001": p_value < 0.01,
            }

    return results


# ---------------------------------------------------------------------------
# 6. REPLY LAG AND OUTPUT CHARACTERISTICS (D5.6)
# ---------------------------------------------------------------------------
def analyze_reply_dynamics(tick_states, operator_ticks, say_ticks, out_dir):
    """
    D5.6 — For each operator message, find the next say event.
    Measure lag, output characteristics, silence duration after.
    """
    say_sorted = sorted(say_ticks)
    all_ticks = sorted(tick_states.keys())

    records = []
    for ot in operator_ticks:
        # Find next say event after this operator message
        next_says = [s for s in say_sorted if s > ot]
        if not next_says:
            continue
        next_say = next_says[0]
        reply_lag = next_say - ot

        # Find say event AFTER the reply (to measure silence duration)
        subsequent_says = [s for s in say_sorted if s > next_say]
        post_silence = subsequent_says[0] - next_say if subsequent_says else None

        # State at operator message time
        op_state = tick_states.get(ot, {})

        records.append({
            "operator_tick": ot,
            "reply_tick": next_say,
            "reply_lag_ticks": reply_lag,
            "post_reply_silence_ticks": post_silence,
            "b1_z_at_operator_msg": round(op_state.get("b1_z", np.nan), 4),
            "entropy_at_operator_msg": round(op_state.get("connectome_entropy", np.nan), 4),
        })

    if not records:
        return {"D5_6_reply_dynamics": {"error": "no matched operator→reply pairs"}}

    # Save
    path = os.path.join(out_dir, "D5_6_reply_lag_per_operator_message.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=records[0].keys())
        w.writeheader()
        w.writerows(records)

    lags = [r["reply_lag_ticks"] for r in records]
    silences = [r["post_reply_silence_ticks"] for r in records if r["post_reply_silence_ticks"] is not None]

    # Split by run phase (early vs late)
    early_lags = [r["reply_lag_ticks"] for r in records if r["operator_tick"] < 10500]
    late_lags = [r["reply_lag_ticks"] for r in records if r["operator_tick"] >= 10500]

    result = {
        "D5_6_reply_dynamics": {
            "n_operator_messages": len(records),
            "overall_lag": {
                "mean": round(np.mean(lags), 1),
                "median": round(np.median(lags), 1),
                "std": round(np.std(lags), 1),
                "min": int(np.min(lags)),
                "max": int(np.max(lags)),
            },
            "early_run_lag": {
                "n": len(early_lags),
                "mean": round(np.mean(early_lags), 1) if early_lags else None,
                "median": round(np.median(early_lags), 1) if early_lags else None,
            },
            "late_run_lag": {
                "n": len(late_lags),
                "mean": round(np.mean(late_lags), 1) if late_lags else None,
                "median": round(np.median(late_lags), 1) if late_lags else None,
            },
            "post_reply_silence": {
                "mean": round(np.mean(silences), 1) if silences else None,
                "median": round(np.median(silences), 1) if silences else None,
            },
        }
    }

    print(f"\n  Reply dynamics: {len(records)} operator→reply pairs")
    print(f"  Overall lag: mean={result['D5_6_reply_dynamics']['overall_lag']['mean']}, "
          f"median={result['D5_6_reply_dynamics']['overall_lag']['median']}")
    if early_lags:
        print(f"  Early (<10500): mean={result['D5_6_reply_dynamics']['early_run_lag']['mean']}")
    if late_lags:
        print(f"  Late (>=10500): mean={result['D5_6_reply_dynamics']['late_run_lag']['mean']}")

    return result


# ---------------------------------------------------------------------------
# 7. SIMPLE BINARY CLASSIFIER (D5.1 strongest test)
# ---------------------------------------------------------------------------
def classification_test(tick_states, operator_ticks, control_ticks, out_dir):
    """
    Can local post-input state changes predict whether the input was
    from the operator or from the corpus?

    Uses a simple logistic regression on delta features.
    Falls back to Mann-Whitney per-variable if sklearn unavailable.
    """
    print("\n=== D5.1: Classification Test ===")

    # Compute deltas for both classes
    op_deltas, op_raw = compute_event_triggered_response(tick_states, operator_ticks)
    ctrl_deltas, ctrl_raw = compute_event_triggered_response(tick_states, control_ticks)

    # Per-variable Mann-Whitney comparison
    from scipy.stats import mannwhitneyu
    mw_results = {}
    for var in STATE_VARS:
        op_vals = op_deltas.get(var, [])
        ctrl_vals = ctrl_deltas.get(var, [])
        if len(op_vals) >= 5 and len(ctrl_vals) >= 5:
            u, p = mannwhitneyu(op_vals, ctrl_vals, alternative="two-sided")
            mw_results[var] = {
                "operator_mean_delta": round(np.mean(op_vals), 6),
                "operator_std_delta": round(np.std(op_vals), 6),
                "control_mean_delta": round(np.mean(ctrl_vals), 6),
                "control_std_delta": round(np.std(ctrl_vals), 6),
                "mann_whitney_U": round(float(u), 1),
                "p_value": round(float(p), 6),
                "n_operator": len(op_vals),
                "n_control": len(ctrl_vals),
                "significant_at_005": p < 0.05,
                "effect_size_r": round(float(u / (len(op_vals) * len(ctrl_vals))) - 0.5, 4)
                    if len(op_vals) > 0 and len(ctrl_vals) > 0 else None,
            }

    # Try sklearn classifier
    classifier_result = None
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_score
        from sklearn.preprocessing import StandardScaler

        # Build feature matrix
        features_op = []
        for resp in op_raw:
            row = [resp.get(f"{var}_delta", 0) for var in STATE_VARS]
            if not any(np.isnan(row)):
                features_op.append(row)

        features_ctrl = []
        for resp in ctrl_raw:
            row = [resp.get(f"{var}_delta", 0) for var in STATE_VARS]
            if not any(np.isnan(row)):
                features_ctrl.append(row)

        if len(features_op) >= 10 and len(features_ctrl) >= 10:
            X = np.array(features_op + features_ctrl)
            y = np.array([1] * len(features_op) + [0] * len(features_ctrl))

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            clf = LogisticRegression(max_iter=1000, random_state=42)
            # 5-fold cross-validation
            scores = cross_val_score(clf, X_scaled, y, cv=5, scoring="accuracy")

            classifier_result = {
                "method": "LogisticRegression_5fold_CV",
                "mean_accuracy": round(float(np.mean(scores)), 4),
                "std_accuracy": round(float(np.std(scores)), 4),
                "fold_scores": [round(float(s), 4) for s in scores],
                "chance_level": 0.5,
                "n_operator": len(features_op),
                "n_control": len(features_ctrl),
                "above_chance": float(np.mean(scores)) > 0.55,
            }
            print(f"  Classifier accuracy: {np.mean(scores):.3f} ± {np.std(scores):.3f} "
                  f"(chance=0.50)")
        else:
            classifier_result = {"error": "too few valid feature vectors",
                                 "n_op": len(features_op), "n_ctrl": len(features_ctrl)}

    except ImportError:
        classifier_result = {
            "error": "sklearn not available — install with pip install scikit-learn",
            "note": "Mann-Whitney tests still ran successfully"
        }

    return {
        "D5_1_classification": {
            "mann_whitney_per_variable": mw_results,
            "classifier": classifier_result,
        }
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="D5.1: Operator Differentiation")
    parser.add_argument("--data-dir", required=True,
                        help="Path to Aura_Analysis_Tables directory")
    parser.add_argument("--exchange", default=None,
                        help="Path to aura_justin_exchange.md")
    parser.add_argument("--out-dir", default="./d5_1_results")
    parser.add_argument("--n-perms", type=int, default=N_PERMUTATIONS,
                        help="Number of permutations for shuffle test")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # 1. Get operator ticks
    if args.exchange:
        operator_ticks = extract_operator_ticks(args.exchange)
    else:
        operator_ticks = OPERATOR_TICKS_FALLBACK
        print(f"Using {len(operator_ticks)} hardcoded operator ticks")

    # Save operator ticks for reproducibility
    with open(os.path.join(args.out_dir, "operator_ticks.json"), "w") as f:
        json.dump({"operator_ticks": operator_ticks, "n": len(operator_ticks)}, f, indent=2)

    # 2. Load data
    tick_states = load_tick_states(args.data_dir)
    say_ticks = load_say_events(args.data_dir)

    all_results = {}

    # 3. Event-triggered response for operator messages
    print("\n=== A. Operator Event-Triggered Response ===")
    op_deltas, op_raw = compute_event_triggered_response(tick_states, operator_ticks)
    op_summary = {}
    for var in STATE_VARS:
        vals = op_deltas.get(var, [])
        if vals:
            op_summary[var] = {
                "mean_delta": round(np.mean(vals), 6),
                "std_delta": round(np.std(vals), 6),
                "median_delta": round(np.median(vals), 6),
                "n_events": len(vals),
            }
            print(f"  {var}: mean_delta={op_summary[var]['mean_delta']:.6f}, "
                  f"n={op_summary[var]['n_events']}")

    # Save raw responses
    if op_raw:
        path = os.path.join(args.out_dir, "operator_event_triggered_responses.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=op_raw[0].keys())
            w.writeheader()
            w.writerows(op_raw)

    all_results["operator_event_triggered"] = op_summary

    # 4. Matched corpus controls
    print("\n=== B. Corpus Control Windows ===")
    control_ticks = generate_corpus_controls(tick_states, operator_ticks)
    ctrl_deltas, ctrl_raw = compute_event_triggered_response(tick_states, control_ticks)
    ctrl_summary = {}
    for var in STATE_VARS:
        vals = ctrl_deltas.get(var, [])
        if vals:
            ctrl_summary[var] = {
                "mean_delta": round(np.mean(vals), 6),
                "std_delta": round(np.std(vals), 6),
                "n_events": len(vals),
            }
            print(f"  {var}: mean_delta={ctrl_summary[var]['mean_delta']:.6f}, "
                  f"n={ctrl_summary[var]['n_events']}")
    all_results["corpus_control_event_triggered"] = ctrl_summary

    # 5. Classification test (D5.1)
    all_results.update(classification_test(tick_states, operator_ticks, control_ticks, args.out_dir))

    # 6. Permutation test
    print("\n=== C. Permutation Test ===")
    perm_results = permutation_test(tick_states, operator_ticks, n_perms=args.n_perms)
    for var, res in perm_results.items():
        sig = "***" if res["significant_at_001"] else ("*" if res["significant_at_005"] else "")
        print(f"  {var}: z={res['z_score']:.2f}, p={res['p_value']:.4f} {sig}")
    all_results["permutation_test"] = perm_results

    # 7. Reply dynamics (D5.6)
    print("\n=== D. Reply Dynamics (D5.6) ===")
    all_results.update(analyze_reply_dynamics(tick_states, operator_ticks, say_ticks, args.out_dir))

    # Save master results
    results_path = os.path.join(args.out_dir, "d5_1_master_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, sort_keys=True, default=str)

    print(f"\n=== All results saved to {args.out_dir}/ ===")
    print(f"Master JSON: {results_path}")

    # Output manifest
    print("\nOutput files:")
    for fname in sorted(os.listdir(args.out_dir)):
        fpath = os.path.join(args.out_dir, fname)
        size = os.path.getsize(fpath)
        print(f"  {fname} ({size:,} bytes)")

    # Quick verdict
    print("\n" + "=" * 60)
    print("QUICK VERDICT:")
    sig_vars = [v for v, r in perm_results.items() if r.get("significant_at_005")]
    if sig_vars:
        print(f"  {len(sig_vars)}/{len(perm_results)} variables show SIGNIFICANT "
              f"operator-specific response (p<0.05):")
        for v in sig_vars:
            r = perm_results[v]
            print(f"    {v}: z={r['z_score']:.2f}, p={r['p_value']:.4f}")
        print("  → The runtime treated operator messages as a distinct causal class.")
    else:
        print("  No variables reached significance in the permutation test.")
        print("  This does NOT mean differentiation didn't happen — it may require")
        print("  finer-grained analysis (e.g., motif-specific, phase-specific).")
    print("=" * 60)


if __name__ == "__main__":
    main()
