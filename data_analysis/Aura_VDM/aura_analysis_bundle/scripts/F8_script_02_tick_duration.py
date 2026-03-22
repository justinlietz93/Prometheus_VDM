#!/usr/bin/env python3
"""
FAMILY 8 — Temporal Microstructure
Script 2: Tick-Duration (Endogenous Clock) Analysis

PURPOSE:
  Each tick has a wall-clock duration (ts[i+1] - ts[i]). If the
  endogenous clock were constant, dt would be ~uniform. If the
  system is doing variable-depth processing, dt will show structure:
    - Heavy-tailed dt distribution → some ticks take much longer
    - dt correlated with internal state → processing depth varies
    - dt changes by epoch → the clock itself reorganizes

  This is the temporal equivalent of asking: does the system
  think at different speeds depending on what it's doing?

INPUTS:
  - events_slim2.csv (columns: t, ts, connectome_entropy, active_edges, b1_z, ...)

OUTPUTS:
  - F8_02_tick_duration_analysis.json
  - F8_02_tick_durations.csv
"""

import csv
import json
import math
import os
import statistics

TABLE_DIR = "../tables"
OUT_PREFIX = "F8_02"

# ── LOAD ──
rows = []
with open(os.path.join(TABLE_DIR, "events_slim2.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"Loaded {len(rows)} ticks")

# ── COMPUTE TICK DURATIONS ──
durations = []
for i in range(1, len(rows)):
    t_prev = int(rows[i - 1]["t"])
    t_curr = int(rows[i]["t"])
    ts_prev = float(rows[i - 1]["ts"])
    ts_curr = float(rows[i]["ts"])
    dt_sec = ts_curr - ts_prev
    dt_tick = t_curr - t_prev

    # Only include dt > 0 and dt < 120 (filter extreme gaps like pauses)
    if 0 < dt_sec < 120 and dt_tick == 1:
        durations.append({
            "t": t_curr,
            "dt_sec": dt_sec,
            "entropy": float(rows[i]["connectome_entropy"]),
            "active_edges": float(rows[i]["active_edges"]),
            "b1_z": float(rows[i]["b1_z"]),
            "firing_var": float(rows[i]["firing_var"]) if rows[i].get("firing_var") else None,
        })

print(f"Valid single-tick durations: {len(durations)}")

dt_vals = [d["dt_sec"] for d in durations]

# ── STATISTICS ──
def basic_stats(vals):
    n = len(vals)
    mu = statistics.mean(vals)
    sd = statistics.stdev(vals)
    med = statistics.median(vals)
    cv = sd / mu if mu > 0 else 0
    sorted_v = sorted(vals)
    return {
        "n": n,
        "mean": round(mu, 4),
        "std": round(sd, 4),
        "median": round(med, 4),
        "cv": round(cv, 4),
        "min": round(min(vals), 4),
        "max": round(max(vals), 4),
        "p5": round(sorted_v[int(0.05 * n)], 4),
        "p25": round(sorted_v[int(0.25 * n)], 4),
        "p75": round(sorted_v[int(0.75 * n)], 4),
        "p95": round(sorted_v[int(0.95 * n)], 4),
        "p99": round(sorted_v[int(0.99 * n)], 4),
    }

overall = basic_stats(dt_vals)

# ── EPOCH SPLIT ──
def epoch_of(t):
    if t < 10500: return "E1"
    elif t < 11600: return "E2"
    else: return "E3"

epoch_dts = {"E1": [], "E2": [], "E3": []}
for d in durations:
    ep = epoch_of(d["t"])
    epoch_dts[ep].append(d["dt_sec"])

epoch_stats = {}
for ep in ["E1", "E2", "E3"]:
    if len(epoch_dts[ep]) >= 10:
        epoch_stats[ep] = basic_stats(epoch_dts[ep])
    else:
        epoch_stats[ep] = {"n": len(epoch_dts[ep]), "error": "too few"}

# ── CORRELATION: dt vs internal state ──
def pearson_r(x, y):
    n = len(x)
    if n < 3:
        return None
    mx = statistics.mean(x)
    my = statistics.mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    dx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    dy = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if dx * dy == 0:
        return None
    return num / (dx * dy)

correlations = {}
for field in ["entropy", "active_edges", "b1_z"]:
    vals_field = [d[field] for d in durations if d[field] is not None]
    vals_dt = [d["dt_sec"] for d in durations if d[field] is not None]
    r = pearson_r(vals_dt, vals_field)
    if r is not None:
        correlations[f"dt_vs_{field}"] = round(r, 4)

# ── AUTOCORRELATION of dt series ──
def autocorr_lag(vals, lag):
    n = len(vals)
    if n <= lag:
        return None
    mu = statistics.mean(vals)
    var = statistics.variance(vals)
    if var == 0:
        return None
    num = sum((vals[i] - mu) * (vals[i + lag] - mu) for i in range(n - lag))
    return num / ((n - lag) * var)

dt_autocorr = {}
for lag in [1, 2, 3, 5, 10, 20, 50]:
    ac = autocorr_lag(dt_vals, lag)
    if ac is not None:
        dt_autocorr[f"lag_{lag}"] = round(ac, 4)

# ── WRITE ──
result = {
    "description": "Tick-duration (endogenous clock) analysis",
    "overall": overall,
    "by_epoch": epoch_stats,
    "correlations_with_state": correlations,
    "dt_autocorrelation": dt_autocorr,
    "interpretation": {
        "cv_meaning": "CV >> 0 means tick durations are highly variable = processing depth varies.",
        "autocorr_meaning": "Positive autocorr at lag 1 = slow ticks cluster together (sustained deep processing).",
        "correlation_meaning": "Nonzero r(dt, entropy) = the clock speed depends on internal disorder level.",
    },
}

with open(f"{OUT_PREFIX}_tick_duration_analysis.json", "w") as f:
    json.dump(result, f, indent=2, sort_keys=True)

with open(f"{OUT_PREFIX}_tick_durations.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["t", "dt_sec", "entropy", "active_edges", "b1_z", "epoch"])
    writer.writeheader()
    for d in durations:
        writer.writerow({
            "t": d["t"],
            "dt_sec": round(d["dt_sec"], 6),
            "entropy": round(d["entropy"], 6),
            "active_edges": d["active_edges"],
            "b1_z": round(d["b1_z"], 6),
            "epoch": epoch_of(d["t"]),
        })

print(f"\n=== RESULTS ===")
print(f"Overall dt: mean={overall['mean']}s, median={overall['median']}s, CV={overall['cv']}")
print(f"Autocorrelation: {dt_autocorr}")
print(f"Correlations: {correlations}")
print(f"\nBy epoch:")
for ep in ["E1", "E2", "E3"]:
    s = epoch_stats[ep]
    if "error" not in s:
        print(f"  {ep}: mean={s['mean']}s, median={s['median']}s, CV={s['cv']}")
    else:
        print(f"  {ep}: {s}")

print(f"\nWrote: {OUT_PREFIX}_tick_duration_analysis.json, {OUT_PREFIX}_tick_durations.csv")
