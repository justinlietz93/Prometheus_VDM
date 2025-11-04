#!/usr/bin/env python3
"""
Reusable plotting helpers for the Metriplectic Assisted-Echo experiment.

This module reads the JSON/CSV artifacts emitted by assisted_echo.py and
produces white-paper-grade figures with gate overlays and captions.

Inputs:
- Run JSON (gate ledger, per-seed CEG, params/grid/spec)
- Telemetry CSV (per-step rows)
- CEG summary CSV

Outputs:
- PNG figures saved under figure_path("metriplectic", ...) per io_paths.py

Notes:
- Avoids pandas; uses stdlib csv/json + numpy/matplotlib for portability.
- Bootstrap CIs computed from per-seed CEG values in the JSON.
- Captions include commit/tag/seed info when available and draw a PASS/FAIL badge
  keyed to gate outcomes in the JSON ledger.

Usage:
  from common.plotting.assisted_echo_plots import (
      generate_core_pack,  # A-pack + B-pack
      plot_phase_portrait_H_isolines,
      plot_error_timeseries,
      plot_ceg_vs_lambda_with_CI,
      plot_energy_budget_parity,
      plot_entropy_production,
      plot_noether_drift_scalar,
      plot_strang_defect_from_sweep_csv,
      plot_endpoint_distance_violin,
      plot_assist_alignment_hist,
      plot_work_partition_panel,
      plot_telemetry_overlay,
      plot_seed_stability_envelope,
  )

"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

# Matplotlib is optional at import time (allow headless environments to import)
try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
except Exception:  # pragma: no cover
    plt = None  # type: ignore

# Code root discovery (Derivation/code/… on sys.path done by runners)
import sys
CODE_ROOT = Path(__file__).resolve().parents[3]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path  # type: ignore


# -------------------------------
# Utilities
# -------------------------------

def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def _read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def _as_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)

def _as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return int(default)

def _bootstrap_CI(vals: np.ndarray, fn, alpha: float = 0.05, draws: int = 2000, rng: Optional[np.random.Generator] = None) -> Tuple[float, float]:
    if vals.size == 0:
        return (np.nan, np.nan)
    rng = rng or np.random.default_rng(0)
    n = vals.size
    stats = []
    for _ in range(draws):
        sample = vals[rng.integers(0, n, size=n)]
        stats.append(fn(sample))
    lo = float(np.nanpercentile(stats, 100.0 * alpha / 2.0))
    hi = float(np.nanpercentile(stats, 100.0 * (1.0 - alpha / 2.0)))
    return lo, hi

def _badge(ax, text: str, color: str = "#2e7d32", loc: str = "upper right"):
    if plt is None:
        return
    x, y = (0.98, 0.98) if loc == "upper right" else (0.02, 0.98)
    bbox = dict(boxstyle="round,pad=0.3", fc=color, ec="none", alpha=0.8)
    ax.text(x, y, text, transform=ax.transAxes, fontsize=9, color="white", va="top", ha="right" if loc.endswith("right") else "left", bbox=bbox)

def _caption(fig, text: str):
    if plt is None:
        return
    fig.text(0.01, 0.01, text, fontsize=8, va="bottom", ha="left", wrap=True)

def _side_caption(fig, ax, text: str, width_frac: float = 0.26):
    """
    Place caption text to the right of the axes, off the plotting area so it never
    occludes the x-axis. Uses figure coordinates; expands the figure if needed.
    """
    if plt is None:
        return
    # Current axes box
    box = ax.get_position()
    # Compute right-column anchor in figure coords
    x_right = min(box.x1 + 0.02, 0.98)
    y_top = min(box.y1, 0.98)
    # If there is not enough room, gently expand right pad via constrained_layout pads
    try:
        fig.set_constrained_layout(True)
    except Exception:
        pass
    # Draw the caption with a light background for readability
    fig.text(
        x_right, y_top,
        text,
        transform=fig.transFigure,
        ha="left", va="top",
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.3", fc="#F5F5F5", ec="#BDBDBD", alpha=0.9),
        wrap=True,
    )

def _read_gate_decision(tj: Dict[str, Any], name: str) -> Dict[str, Any]:
    """Fetch a gate decision record from JSON summary; {} if missing."""
    return (tj.get("gate_ledger_summary", {}) or {}).get(name, {}) or {}

def _instrument_summary(tj: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Aggregate instrument gates (G1–G4). Returns (all_pass, text_summary).
    Uses 'meets_rate' as decision per gate.
    """
    gls = tj.get("gate_ledger_summary", {}) or {}
    names = ["G1_Noether_J", "G2_H_theorem_M", "G3_EnergyMatch", "G4_StrangDefect"]
    flags = []
    lines = []
    for nm in names:
        rec = gls.get(nm, {}) or {}
        ok = bool(rec.get("meets_rate", False) or rec.get("passed", False))
        flags.append(ok)
        pr = rec.get("pass_rate", None)
        lines.append(f"{nm}: {'PASS' if ok else 'FAIL'}" + (f" (pass_rate={pr:.2f})" if isinstance(pr, float) else ""))
    all_ok = all(flags) if flags else False
    summary = "Instrument (G1–G4): " + ("PASS" if all_ok else "FAIL") + "; " + " | ".join(lines)
    return all_ok, summary

def _outcome_summary_g5(tj: Dict[str, Any], g5_threshold: float) -> Tuple[bool, str]:
    """Outcome (G5) summary with measured statistic vs threshold."""
    g5 = _read_gate_decision(tj, "G5_CEG_Positive")
    ok = bool(g5.get("passed", 0))
    medmax = g5.get("median_max", None)
    if medmax is None:
        # Fallback: derive from ceg_summary
        try:
            ceg_summary = tj.get("ceg_summary", {}) or {}
            medians = [float(v.get("median", 0.0)) for k, v in ceg_summary.items() if float(k) > 0.0]
            medmax = float(max(medians)) if medians else 0.0
        except Exception:
            medmax = 0.0
        ok = bool(medmax >= float(g5_threshold))
    text = f"G5 (outcome): {'PASS' if ok else 'FAIL'}; median_max={medmax:.4g} vs tol={float(g5_threshold):g}"
    return ok, text

def _apply_gate_badges(ax, tj: Dict[str, Any], g5_threshold: float):
    """Add instrument and outcome badges to the axes (top-left and top-right)."""
    inst_ok, _ = _instrument_summary(tj)
    _badge(ax, "G1–G4 PASS" if inst_ok else "G1–G4 FAIL", color=("#2e7d32" if inst_ok else "#c62828"), loc="upper left")
    g5_ok, _ = _outcome_summary_g5(tj, g5_threshold)
    _badge(ax, "G5 (outcome) PASS" if g5_ok else "G5 (outcome) FAIL", color=("#2e7d32" if g5_ok else "#c62828"), loc="upper right")

def _ensure_matplotlib():
    if plt is None:
        raise RuntimeError("matplotlib is not available; cannot generate figures")

def _first_mode_kphi(N: int, dx: float, c: float, m: float) -> float:
    L = float(N) * float(dx)
    k = 2.0 * math.pi / max(L, 1e-12)
    return float((c * c) * (k * k) + (m * m))


# -------------------------------
# Figure A1: Phase portrait with H-energy isolines
# -------------------------------

def plot_phase_portrait_H_isolines(
    telemetry_csv: Path,
    run_json: Path,
    out_png: Path,
    lambda_assisted: float = 0.5,
    title: str = "Phase portrait (first Fourier cosine mode)"
) -> None:
    """
    Plot phase trajectories (phi1, pi1) for forward, baseline(λ), assisted(λ),
    overlaid on H-energy isolines for the instrument metric.

    Fixes:
    - Break lines at seed boundaries to avoid long straight chords between seeds.
    - Place caption on the right, under the legend, to keep x-axis unobstructed.
    """
    _ensure_matplotlib()
    import textwrap

    tj = _read_json(run_json)
    rows = _read_csv_dicts(telemetry_csv)

    # Extract params for H isolines
    spec = {
        "N": _as_int(tj.get("grid", {}).get("N", 256)),
        "dx": _as_float(tj.get("grid", {}).get("dx", 1.0)),
        "c": _as_float(tj.get("params", {}).get("c", 1.0)),
        "m": _as_float(tj.get("params", {}).get("m", 0.0)),
    }
    k_phi = _first_mode_kphi(spec["N"], spec["dx"], spec["c"], spec["m"])

    # Collect trajectories PER SEED to prevent connecting different seeds with straight lines
    lam_key = float(lambda_assisted)
    traces = {
        "forward": {},   # seed -> (xs, ys)
        "baseline": {},  # seed -> (xs, ys) at selected λ
        "assisted": {},  # seed -> (xs, ys) at selected λ
    }
    H_vals: List[float] = []

    for r in rows:
        mode = r.get("mode", "")
        seed = _as_int(r.get("seed", -1))
        lam = _as_float(r.get("lambda", 0.0))
        phi1 = _as_float(r.get("phi1", 0.0))
        pi1 = _as_float(r.get("pi1", 0.0))
        H = _as_float(r.get("H_energy", 0.0))

        if mode == "forward":
            sel = True
            tgt = "forward"
        elif mode == "baseline":
            sel = math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12)
            tgt = "baseline"
        elif mode == "assisted":
            sel = math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12)
            tgt = "assisted"
        else:
            sel = False
            tgt = ""

        if sel:
            if seed not in traces[tgt]:
                traces[tgt][seed] = ([], [])
            traces[tgt][seed][0].append(phi1)
            traces[tgt][seed][1].append(pi1)

        if H > 0.0:
            H_vals.append(H)

    # Isoline levels from telemetry H (use forward telemetry percentiles)
    if len(H_vals) == 0:
        H_levels = [0.1, 0.5, 1.0]
    else:
        arr = np.array(H_vals, dtype=float)
        H_levels = list(np.nanpercentile(arr, [25, 50, 75]))
        H_levels = [float(max(h, 1e-6)) for h in H_levels]

    # Build isolines: H = 0.5 (k_phi phi1^2 + pi1^2)
    # => parameterize with angle t: phi1 = sqrt(2H/k_phi) cos t, pi1 = sqrt(2H) sin t
    fig, ax = plt.subplots(figsize=(8.5, 5.0), constrained_layout=True)
    t = np.linspace(0, 2.0 * np.pi, 512)
    for h in H_levels:
        a = math.sqrt(2.0 * h / max(k_phi, 1e-12))
        b = math.sqrt(2.0 * h)
        xx = a * np.cos(t)
        yy = b * np.sin(t)
        ax.plot(xx, yy, color="#cccccc", lw=1.0, alpha=0.5, zorder=1)

    # Helper to plot per-mode traces without connecting different seeds
    def _plot_mode(mode: str, color: str, lw: float, label: str) -> None:
        first = True
        for _seed, (xs, ys) in traces[mode].items():
            if xs:
                ax.plot(
                    xs, ys, "-", color=color, lw=lw,
                    alpha=(0.85 if first else 0.35),
                    label=(label if first else None),
                    zorder=2 if mode != "assisted" else 3
                )
                first = False

    # Trajectories per mode (label only once per mode)
    _plot_mode("forward",  "#455A64", 1.5, "forward (JMJ)")
    _plot_mode("baseline", "#9E9E9E", 1.5, f"reverse baseline (λ={lam_key:g})")
    _plot_mode("assisted", "#00796B", 2.0, f"reverse assisted (λ={lam_key:g})")

    ax.set_xlabel("phi_1 (first cosine mode)")
    ax.set_ylabel("pi_1 (first cosine mode)")
    ax.set_title(title)
    ax.grid(True, which="both", alpha=0.3)

    # Add legend outside to avoid overlap
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0, frameon=False)

    # Instrument + outcome badges and right-side caption (keep x-axis clear)
    try:
        g5_thr = float((tj.get("params", {}) or {}).get("ceg_gate_threshold", 0.05))
        _apply_gate_badges(ax, tj, g5_thr)
        inst_ok, inst_txt = _instrument_summary(tj)
        g5_ok, g5_txt = _outcome_summary_g5(tj, g5_thr)
        caption = _caption_text(tj, f"Phase portrait in (phi_1, pi_1). Showing forward, baseline, and assisted (λ={lam_key:g}). H-isolines (instrument metric) overlaid. ")
        cap_wrapped = textwrap.fill(caption, width=42)
        _side_caption(fig, ax, f"{cap_wrapped}\n{inst_txt}\n{g5_txt}")
    except Exception:
        pass

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


# (removed duplicate _read_gate_decision; canonical helper is defined above)


def _caption_text(run_json: Dict[str, Any], lead: str) -> str:
    grid = run_json.get("grid", {})
    params = run_json.get("params", {})
    tag = params.get("tag") or run_json.get("tag")
    N = grid.get("N"); dx = grid.get("dx"); dt = run_json.get("dt")
    seeds = run_json.get("seeds", [])
    commit = _guess_commit()
    return (
        f"{lead}"
        f"Figure generated from JSON: seed(s)={seeds}; grid N={N}, dx={dx}, dt={dt}; tag={tag}. "
        f"commit={commit}."
    )


def _guess_commit() -> str:
    """Best-effort commit hash from PROVENANCE_manifest.json; 'unknown' if missing."""
    try:
        prov = json.loads((CODE_ROOT / "PROVENANCE_manifest.json").read_text())
        return str(prov.get("commit", "unknown"))
    except Exception:
        return "unknown"


# -------------------------------
# Figure A2: Echo error vs time (H-norm)
# -------------------------------

def plot_error_timeseries(
    telemetry_csv: Path,
    out_png: Path,
    lambda_assisted: float = 0.5,
    title: str = "Echo error vs. time (H-norm)"
) -> None:
    # Plot per-seed traces to avoid chords between seeds; mirrors per-seed logic in
    # plot_phase_portrait_H_isolines() for seed-bounded polylines.
    _ensure_matplotlib()
    rows = _read_csv_dicts(telemetry_csv)

    lam_key = float(lambda_assisted)
    # seed -> (steps, errs) per mode
    f_tr: Dict[int, Tuple[List[int], List[float]]] = {}
    b_tr: Dict[int, Tuple[List[int], List[float]]] = {}
    a_tr: Dict[int, Tuple[List[int], List[float]]] = {}

    for r in rows:
        mode = r.get("mode", "")
        lam = _as_float(r.get("lambda", 0.0))
        seed = _as_int(r.get("seed", -1))
        step = _as_int(r.get("step", 0))
        e = _as_float(r.get("err_to_ref", 0.0))

        if mode == "forward":
            f_tr.setdefault(seed, ([], []))
            f_tr[seed][0].append(step); f_tr[seed][1].append(e)
        elif mode == "baseline" and math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12):
            b_tr.setdefault(seed, ([], []))
            b_tr[seed][0].append(step); b_tr[seed][1].append(e)
        elif mode == "assisted" and math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12):
            a_tr.setdefault(seed, ([], []))
            a_tr[seed][0].append(step); a_tr[seed][1].append(e)

    def _sorted_items(tr: Dict[int, Tuple[List[int], List[float]]]):
        for sd, (xs, ys) in tr.items():
            if xs:
                order = np.argsort(np.array(xs, dtype=float))
                tr[sd] = ([int(xs[i]) for i in order], [float(ys[i]) for i in order])
        return tr.items()

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

    first = True
    for _, (xs, ys) in _sorted_items(f_tr):
        ax.plot(xs, ys, "-", color="#455A64", lw=1.5, alpha=(0.85 if first else 0.35), label=("forward (JMJ)" if first else None))
        first = False

    first = True
    for _, (xs, ys) in _sorted_items(b_tr):
        ax.plot(xs, ys, "-", color="#9E9E9E", lw=1.5, alpha=(0.85 if first else 0.35), label=(f"reverse baseline (λ={lam_key:g})" if first else None))
        first = False

    first = True
    for _, (xs, ys) in _sorted_items(a_tr):
        ax.plot(xs, ys, "-", color="#00796B", lw=2.0, alpha=(0.9 if first else 0.45), label=(f"reverse assisted (λ={lam_key:g})" if first else None))
        first = False

    ax.set_xlabel("step")
    ax.set_ylabel("|z - z*|_H")
    ax.set_title(title)
    ax.legend(loc="best")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)

# -------------------------------
# Figure A3: CEG vs λ with bootstrap CI
# -------------------------------

def plot_ceg_vs_lambda_with_CI(
    run_json: Path,
    ceg_csv: Path,
    out_png: Path,
    g5_threshold: float = 0.05,
    title: str = "CEG vs λ with 95% bootstrap CI (median across seeds)"
) -> None:
    _ensure_matplotlib()
    tj = _read_json(run_json)
    ceg_rows = _read_csv_dicts(ceg_csv)

    # Build lambda list from CSV
    lambdas: List[float] = []
    medians_csv: Dict[float, float] = {}
    for r in ceg_rows:
        lam = _as_float(r.get("lambda", 0.0))
        med = _as_float(r.get("median_ceg", 0.0))
        lambdas.append(lam)
        medians_csv[lam] = med
    lambdas = sorted(set(lambdas))

    # Compute per-seed CEG values from JSON for CI
    per_seed = tj.get("per_seed", [])
    ci_low: List[float] = []
    ci_high: List[float] = []
    meds: List[float] = []

    for lam in lambdas:
        k = f"{float(lam):.12g}"
        vals: List[float] = []
        for s in per_seed:
            if "ceg" in s and k in s["ceg"]:
                try:
                    vals.append(float(s["ceg"][k]))
                except Exception:
                    pass
        arr = np.array(vals, dtype=float) if vals else np.array([], dtype=float)
        lo, hi = _bootstrap_CI(arr, np.nanmedian, alpha=0.05) if arr.size > 0 else (np.nan, np.nan)
        ci_low.append(lo); ci_high.append(hi)
        meds.append(medians_csv.get(lam, float(np.nan)))

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.plot(lambdas, meds, "o-", color="#1565C0", lw=2.0, label="median CEG")
    # CI ribbon
    if all([not math.isnan(x) for x in ci_low + ci_high]):
        ax.fill_between(lambdas, ci_low, ci_high, color="#90CAF9", alpha=0.4, label="95% CI (bootstrap)")

    # Threshold line and badges (instrument + outcome)
    ax.axhline(y=float(g5_threshold), color="#C62828", lw=1.0, ls="--", label=f"G5 threshold = {g5_threshold:g}")
    _apply_gate_badges(ax, tj, g5_threshold)

    ax.set_xlabel("λ")
    ax.set_ylabel("CEG (Δ error per unit work)")
    ax.set_title(title)
    ax.legend(loc="best")

    # Right-side caption: expectations + decisions
    try:
        inst_ok, inst_txt = _instrument_summary(tj)
        g5_ok, g5_txt = _outcome_summary_g5(tj, g5_threshold)
        _side_caption(fig, ax, f"{inst_txt}\n{g5_txt}\nDashed line = prereg threshold.")
    except Exception:
        pass

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


# -------------------------------
# Figure A4: Energy-match budget parity (assisted vs baseline)
# -------------------------------

def plot_energy_budget_parity(
    telemetry_csv: Path,
    out_png: Path,
    lambda_assisted: float = 0.5,
    rel_tol_band: float = 1e-4,
    title: str = "Energy budget parity (H-work)"
) -> None:
    _ensure_matplotlib()
    rows = _read_csv_dicts(telemetry_csv)

    lam_key = float(lambda_assisted)
    steps, cum_bl, cum_as = [], [], []

    # Use cum_work column added by runner
    for r in rows:
        lam = _as_float(r.get("lambda", 0.0))
        step = _as_int(r.get("step", 0))
        mode = r.get("mode", "")
        if not math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12):
            continue
        if mode == "baseline":
            steps.append(step); cum_bl.append(_as_float(r.get("cum_work", 0.0)))
        elif mode == "assisted":
            cum_as.append(_as_float(r.get("cum_work", 0.0)))

    # Align lengths
    n = min(len(steps), len(cum_bl), len(cum_as))
    steps = steps[:n]; cum_bl = cum_bl[:n]; cum_as = cum_as[:n]

    rel_diff = []
    for i in range(n):
        denom = max(abs(cum_bl[i]), 1e-12)
        rel_diff.append((cum_as[i] - cum_bl[i]) / denom)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), sharex=True, constrained_layout=True)
    ax1.plot(steps, cum_bl, "-", color="#9E9E9E", lw=1.5, label="baseline cumulative work")
    ax1.plot(steps, cum_as, "-", color="#00796B", lw=1.5, label="assisted cumulative work")
    ax1.set_ylabel("cumulative H-work")
    ax1.legend(loc="best")
    ax1.set_title(title)

    ax2.plot(steps, rel_diff, "-", color="#6A1B9A", lw=1.5, label="relative difference")
    ax2.axhline(y=rel_tol_band, color="#C62828", lw=1.0, ls="--", label=f"tolerance ±{rel_tol_band:g}")
    ax2.axhline(y=-rel_tol_band, color="#C62828", lw=1.0, ls="--")
    ax2.set_xlabel("step")
    ax2.set_ylabel("rel diff")
    ax2.legend(loc="best")

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# Figure A5: Per-step entropy production (ΔΣ)
# -------------------------------

def plot_entropy_production(
    telemetry_csv: Path,
    out_png: Path,
    title: str = "Entropy production ΔΣ on M-leg (forward JMJ)"
) -> None:
    """
    Plot forward ΔΣ per-seed traces to avoid straight-line chords between seeds.
    Also report the histogram of per-seed minima (instrument gate diagnostic).
    """
    _ensure_matplotlib()
    rows = _read_csv_dicts(telemetry_csv)

    # Group forward-mode rows by seed
    seed_traces: Dict[int, Tuple[List[int], List[float]]] = {}
    for r in rows:
        if r.get("mode", "") != "forward":
            continue
        sd = _as_int(r.get("seed", -1))
        step = _as_int(r.get("step", 0))
        ds = _as_float(r.get("delta_sigma", 0.0))
        seed_traces.setdefault(sd, ([], []))
        seed_traces[sd][0].append(step)
        seed_traces[sd][1].append(ds)

    # Compute minima per seed (over steps)
    min_per_seed: Dict[int, float] = {}
    for sd, (xs, ys) in seed_traces.items():
        if ys:
            min_per_seed[sd] = float(np.nanmin(np.asarray(ys, dtype=float)))

    # Time series (per-seed) + histogram of minima across seeds
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

    first = True
    for sd, (xs, ys) in seed_traces.items():
        if not xs:
            continue
        order = np.argsort(np.asarray(xs, dtype=float))
        xs_sorted = [int(xs[i]) for i in order]
        ys_sorted = [float(ys[i]) for i in order]
        ax1.plot(
            xs_sorted,
            ys_sorted,
            "-",
            color="#3949AB",
            lw=1.2,
            alpha=(0.9 if first else 0.4),
            label=("forward ΔΣ (per-seed)" if first else None),
        )
        first = False

    ax1.axhline(y=0.0, color="#C62828", lw=1.0, ls="--")
    ax1.set_xlabel("step")
    ax1.set_ylabel("ΔΣ")
    ax1.set_title(title)
    if not first:
        ax1.legend(loc="best")

    mins = np.array(list(min_per_seed.values()), dtype=float) if min_per_seed else np.array([], dtype=float)
    if mins.size > 0:
        ax2.hist(mins, bins=20, color="#90A4AE", edgecolor="#455A64")
    ax2.axvline(x=0.0, color="#C62828", lw=1.0, ls="--")
    ax2.set_xlabel("min ΔΣ (per seed)")
    ax2.set_ylabel("count")
    ax2.set_title("Min ΔΣ over steps (by seed)")

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


# -------------------------------
# Figure A6: Noether-J drift (scalar, current runner)
# -------------------------------

def plot_noether_drift_scalar(
    run_json: Path,
    out_png: Path,
    title: str = "J-only round-trip drift (instrument meter)"
) -> None:
    """Plot the scalar time-reversal drift per seed (current runner emits scalar)."""
    _ensure_matplotlib()
    tj = _read_json(run_json)
    per_seed = tj.get("per_seed", [])
    vals: List[float] = []
    for s in per_seed:
        diag = s.get("gates_diag", {})
        v = _as_float(diag.get("time_rev_drift", 0.0))
        vals.append(v)
    seeds = list(range(1, len(vals) + 1))
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.semilogy(seeds, vals, "o", color="#6D4C41")
    ax.axhline(y=1e-12, color="#C62828", ls="--", lw=1.0, label="tol 1e-12")
    ax.set_xlabel("seed index")
    ax.set_ylabel("drift (|z_rev - z_0|_H)")
    ax.set_title(title)
    ax.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# Figure A7: Strang-defect slope (from sweep CSV)
# -------------------------------

def plot_strang_defect_from_sweep_csv(
    sweep_csv: Path,
    out_png: Path,
    title: str = "Strang defect vs Δt (two-grid, H-norm)"
) -> None:
    """
    Expect sweep CSV with columns: dt,e (and optionally fit_slope, R2)
    This is produced by separate sweep runners (e.g., run_metriplectic.py).
    """
    _ensure_matplotlib()
    rows = _read_csv_dicts(sweep_csv)
    dts, es = [], []
    for r in rows:
        if "dt" in r and "e" in r:
            dts.append(_as_float(r["dt"]))
            es.append(_as_float(r["e"]))
    if len(dts) == 0:
        # Nothing to plot
        return
    x = np.array(dts, dtype=float); y = np.array(es, dtype=float)
    lx = np.log(x); ly = np.log(y + 1e-300)  # guard zero
    A = np.vstack([lx, np.ones_like(lx)]).T
    slope, b = np.linalg.lstsq(A, ly, rcond=None)[0]
    y_pred = A @ np.array([slope, b])
    ss_res = float(np.sum((ly - y_pred) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.loglog(x, y, "o", color="#283593", label="defect e(h)")
    xfit = np.linspace(min(x), max(x), 100)
    yfit = np.exp(b) * (xfit ** slope)
    ax.loglog(xfit, yfit, "-", color="#FF6F00", lw=1.5, label=f"fit slope={slope:.3f}, R²={R2:.4f}")
    ax.set_xlabel("Δt")
    ax.set_ylabel("e(h)")
    ax.set_title(title)
    ax.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# Figure A8: Endpoint distance vs λ (violin/box)
# -------------------------------

def plot_endpoint_distance_violin(
    run_json: Path,
    out_png: Path,
    use_violin: bool = True,
    title: str = "Endpoint distance vs λ (H-norm, assisted)"
) -> None:
    _ensure_matplotlib()
    tj = _read_json(run_json)
    per_seed = tj.get("per_seed", [])
    # Collect per-seed assisted_err per lambda
    lam_to_vals: Dict[float, List[float]] = {}
    for s in per_seed:
        errs = s.get("assisted_err", {})
        for k, v in errs.items():
            lam = float(k)
            lam_to_vals.setdefault(lam, []).append(_as_float(v))
    lambdas = sorted(lam_to_vals.keys())
    data = [lam_to_vals[lam] for lam in lambdas]

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    if use_violin:
        parts = ax.violinplot(data, showmeans=True, showextrema=True, showmedians=True)
        for pc in parts["bodies"]:
            pc.set_facecolor("#80CBC4"); pc.set_edgecolor("#004D40"); pc.set_alpha(0.7)
    else:
        ax.boxplot(data, showmeans=True)
    ax.set_xticks(range(1, len(lambdas) + 1))
    ax.set_xticklabels([f"{lam:g}" for lam in lambdas])
    ax.set_xlabel("λ")
    ax.set_ylabel("|z_T - z_0|_H (assisted)")
    ax.set_title(title)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# B9: Assistance alignment distribution
# -------------------------------

def plot_assist_alignment_hist(
    telemetry_csv: Path,
    out_png: Path,
    lambda_assisted: float = 0.5,
    title: str = "Assistance direction alignment with -∇_H (cos θ)"
) -> None:
    _ensure_matplotlib()
    rows = _read_csv_dicts(telemetry_csv)
    lam_key = float(lambda_assisted)
    vals: List[float] = []
    for r in rows:
        if r.get("mode", "") != "assisted":
            continue
        lam = _as_float(r.get("lambda", 0.0))
        if not math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12):
            continue
        vals.append(_as_float(r.get("align_cos", 0.0)))
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    if len(vals) > 0:
        ax.hist(vals, bins=30, color="#B39DDB", edgecolor="#4527A0")
        ax.axvline(x=np.median(vals), color="#311B92", lw=1.2, ls="--", label=f"median {np.median(vals):.3f}")
        ax.legend()
    ax.set_xlabel("cos θ")
    ax.set_ylabel("count")
    ax.set_title(title)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# B10: Work/heat decomposition panel
# -------------------------------

def plot_work_partition_panel(
    telemetry_csv: Path,
    out_png: Path,
    lambda_assisted: float = 0.5,
    title: str = "Work partition across channels (H-energy metric)"
) -> None:
    _ensure_matplotlib()
    rows = _read_csv_dicts(telemetry_csv)
    lam_key = float(lambda_assisted)
    # Sum components for baseline vs assisted
    sums = {"baseline": {"phi": 0.0, "pi": 0.0}, "assisted": {"phi": 0.0, "pi": 0.0}}
    for r in rows:
        mode = r.get("mode", "")
        lam = _as_float(r.get("lambda", 0.0))
        if mode not in ("baseline", "assisted"):
            continue
        if not math.isclose(lam, lam_key, rel_tol=0, abs_tol=1e-12):
            continue
        sums[mode]["phi"] += _as_float(r.get("work_e_phi", 0.0))
        sums[mode]["pi"] += _as_float(r.get("work_e_pi", 0.0))
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    labels = ["baseline", "assisted"]
    phi = [sums["baseline"]["phi"], sums["assisted"]["phi"]]
    pi = [sums["baseline"]["pi"], sums["assisted"]["pi"]]
    idx = np.arange(len(labels))
    ax.bar(idx, phi, color="#64B5F6", label="phi-channel")
    ax.bar(idx, pi, bottom=phi, color="#4DB6AC", label="pi-channel")
    ax.set_xticks(idx)
    ax.set_xticklabels(labels)
    ax.set_ylabel("total H-work components")
    ax.set_title(title)
    ax.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# B11: λ-sweep telemetry overlay (err_to_ref)
# -------------------------------

def plot_telemetry_overlay(
    telemetry_csv: Path,
    out_png: Path,
    lambdas: Optional[Sequence[float]] = None,
    title: str = "Telemetry overlay across λ (err_to_ref)"
) -> None:
    """
    Overlay assisted err_to_ref traces across up to 4 λ values.
    Plot per-seed lines to avoid straight-line chords between seeds.
    """
    _ensure_matplotlib()
    rows = _read_csv_dicts(telemetry_csv)
    # If no explicit list, select up to 4 distinct nonzero λ observed in assisted mode
    if not lambdas:
        lam_set = sorted({_as_float(r.get("lambda", 0.0)) for r in rows if r.get("mode", "") == "assisted"})
        lambdas = [lam for lam in lam_set if lam > 0.0][:4]

    # Build traces per (λ, seed)
    lam_seed_traces: Dict[float, Dict[int, Tuple[List[int], List[float]]]] = {}
    for r in rows:
        if r.get("mode", "") != "assisted":
            continue
        lam = _as_float(r.get("lambda", 0.0))
        if lambdas and lam not in set(lambdas):
            continue
        sd = _as_int(r.get("seed", -1))
        step = _as_int(r.get("step", 0))
        val = _as_float(r.get("err_to_ref", 0.0))
        lam_seed_traces.setdefault(lam, {})
        lam_seed_traces[lam].setdefault(sd, ([], []))
        lam_seed_traces[lam][sd][0].append(step)
        lam_seed_traces[lam][sd][1].append(val)

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    colors = ["#00695C", "#0277BD", "#8E24AA", "#EF6C00", "#C62828"]

    for j, lam in enumerate(lambdas or []):
        color = colors[j % len(colors)]
        first = True
        for sd, (xs, ys) in (lam_seed_traces.get(float(lam), {}) or {}).items():
            if not xs:
                continue
            order = np.argsort(np.asarray(xs, dtype=float))
            xs_sorted = [int(xs[i]) for i in order]
            ys_sorted = [float(ys[i]) for i in order]
            ax.plot(
                xs_sorted,
                ys_sorted,
                "-",
                color=color,
                lw=1.3,
                alpha=(0.9 if first else 0.4),
                label=(f"λ={float(lam):g}" if first else None),
            )
            first = False

    ax.set_xlabel("step")
    ax.set_ylabel("|z - z*|_H")
    ax.set_title(title)
    if ax.get_legend_handles_labels()[0]:
        ax.legend(loc="best")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


# -------------------------------
# B12: Seed stability envelope (quantiles over seeds)
# -------------------------------

def plot_seed_stability_envelope(
    run_json: Path,
    out_png: Path,
    lambda_focus: float = 0.5,
    title: str = "Seed stability (P50/P95/P99) at fixed λ"
) -> None:
    _ensure_matplotlib()
    tj = _read_json(run_json)
    per_seed = tj.get("per_seed", [])
    lam_key = f"{float(lambda_focus):.12g}"
    vals: List[float] = []
    for s in per_seed:
        ceg_map = s.get("ceg", {})
        if lam_key in ceg_map:
            vals.append(_as_float(ceg_map[lam_key], 0.0))
    if len(vals) == 0:
        return
    arr = np.array(vals, dtype=float)
    q50, q95, q99 = np.nanpercentile(arr, [50, 95, 99])

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.bar(["P50","P95","P99"], [q50, q95, q99], color=["#4CAF50","#FFB300","#E53935"])
    ax.set_ylabel("CEG")
    ax.set_title(title + f" (λ={float(lambda_focus):g})")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


# -------------------------------
# Core pack generator (A + B essential)
# -------------------------------

def generate_core_pack(
    domain: str,
    tag: str,
    timestamp_stem: str,
    run_json: Path,
    telemetry_csv: Path,
    ceg_csv: Path,
    lambda_assisted: float = 0.5,
    g5_threshold: Optional[float] = None
) -> Dict[str, str]:
    """
    Emit the A-pack (1–8) and B-pack (9–12) essentials for a single run.

    Returns a dict of figure labels → file paths.
    """
    # Discover threshold from JSON if not provided
    tj = _read_json(run_json)
    if g5_threshold is None:
        g5_threshold = float(tj.get("params", {}).get("ceg_gate_threshold", 0.05))

    figs: Dict[str, str] = {}

    def _fig(stem: str) -> Path:
        # Use canonical stem naming from the caller
        return figure_path(domain, f"{timestamp_stem}_{stem}__{tag}")

    # A1
    p = _fig("assisted_echo_phase"); plot_phase_portrait_H_isolines(telemetry_csv, run_json, p, lambda_assisted=lambda_assisted); figs["A1_phase"] = str(p)
    # A2
    p = _fig("assisted_echo_error_timeseries"); plot_error_timeseries(telemetry_csv, p, lambda_assisted=lambda_assisted); figs["A2_error_ts"] = str(p)
    # A3
    p = _fig("assisted_echo_ceg_vs_lambda"); plot_ceg_vs_lambda_with_CI(run_json, ceg_csv, p, g5_threshold=g5_threshold); figs["A3_ceg_vs_lambda"] = str(p)
    # A4
    p = _fig("assisted_echo_energy_budget"); plot_energy_budget_parity(telemetry_csv, p, lambda_assisted=lambda_assisted); figs["A4_budget"] = str(p)
    # A5
    p = _fig("assisted_echo_entropy_production"); plot_entropy_production(telemetry_csv, p); figs["A5_entropy"] = str(p)
    # A6
    p = _fig("assisted_echo_noether_drift"); plot_noether_drift_scalar(run_json, p); figs["A6_noether"] = str(p)
    # A7 requires sweep CSV from separate diagnostic; caller can invoke plot_strang_defect_from_sweep_csv
    # A8
    p = _fig("assisted_echo_endpoint_distance"); plot_endpoint_distance_violin(run_json, p, use_violin=True); figs["A8_endpoint"] = str(p)

    # B9
    p = _fig("assisted_echo_assist_alignment"); plot_assist_alignment_hist(telemetry_csv, p, lambda_assisted=lambda_assisted); figs["B9_align"] = str(p)
    # B10
    p = _fig("assisted_echo_work_partition"); plot_work_partition_panel(telemetry_csv, p, lambda_assisted=lambda_assisted); figs["B10_work_part"] = str(p)
    # B11
    p = _fig("assisted_echo_telemetry_overlay"); plot_telemetry_overlay(telemetry_csv, p); figs["B11_overlay"] = str(p)
    # B12
    p = _fig("assisted_echo_seed_stability"); plot_seed_stability_envelope(run_json, p, lambda_focus=lambda_assisted); figs["B12_seed_env"] = str(p)

    return figs