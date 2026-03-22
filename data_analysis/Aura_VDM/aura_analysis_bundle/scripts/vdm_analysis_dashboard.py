#!/usr/bin/env python3
"""
VDM Analysis Dashboard
======================
Unified analysis dashboard for Void Dynamics Model simulation data.

Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Usage:
    pip install dash plotly pandas numpy scipy scikit-learn statsmodels h5py
    python vdm_analysis_dashboard.py --port 8051

Data accepted:
    - utd_events.jsonl.zip  (primary: status + say events)
    - state_*.h5 snapshots  (optional: topology / graph metrics)
    - *.h5 scalar logs       (optional: continuous telemetry)
"""
from __future__ import annotations

import argparse
import base64
import io
import itertools
import json
import math
import re
import traceback
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import signal, stats as scipy_stats
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans, KMeans

import dash
from dash import dcc, html, Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc

# ─────────────────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────────────────
BG        = "#080c14"
PANEL     = "#0d1320"
SURFACE   = "#111827"
BORDER    = "#1e2d45"
GRID      = "rgba(255,255,255,0.06)"
FONT_COL  = "#c9d1e0"
ACCENT    = "#3b82f6"
ACCENT2   = "#06b6d4"
MUTED     = "#64748b"

PALETTE = [
    "#3b82f6", "#06b6d4", "#10b981", "#f59e0b",
    "#ec4899", "#8b5cf6", "#ef4444", "#84cc16",
    "#f97316", "#a78bfa", "#34d399", "#fbbf24",
]

LAYOUT_BASE = dict(
    paper_bgcolor=BG,
    plot_bgcolor=PANEL,
    font=dict(family="'JetBrains Mono', 'Fira Code', monospace", size=11, color=FONT_COL),
    title_font=dict(size=13, color="#e2e8f0"),
    margin=dict(l=50, r=20, t=44, b=44),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, borderwidth=1, font=dict(size=10)),
    xaxis=dict(gridcolor=GRID, linecolor=BORDER, tickcolor=MUTED, zeroline=False, showgrid=True),
    yaxis=dict(gridcolor=GRID, linecolor=BORDER, tickcolor=MUTED, zeroline=False, showgrid=True),
    colorway=PALETTE,
)

def sfig(title: str = "", height: int = 380, **kw) -> go.Figure:
    fig = go.Figure()
    layout = {**LAYOUT_BASE, **kw}
    if title:
        layout["title"] = dict(text=title, x=0.5, xanchor="center", font=dict(size=13))
    layout["height"] = height
    fig.update_layout(**layout)
    return fig

def _hm(z, x_labels, y_labels, title="", colorscale="Blues", height=380):
    fig = sfig(title, height=height)
    fig.add_trace(go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=colorscale,
        colorbar=dict(tickfont=dict(size=9, color=FONT_COL)),
    ))
    return fig


# ─────────────────────────────────────────────────────────
#  PARSING  (from run_all.py, deduped & cleaned)
# ─────────────────────────────────────────────────────────

def parse_utd_zip(raw_bytes: bytes) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Parse utd_events.jsonl from a zip archive."""
    with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
        names = zf.namelist()
        jsonl_name = next((n for n in names if n.endswith("utd_events.jsonl")), None)
        if jsonl_name is None:
            jsonl_name = next((n for n in names if n.endswith(".jsonl")), None)
        if jsonl_name is None:
            raise ValueError("No .jsonl file found in zip")

        status_rows, say_rows, pending_texts = [], [], []
        with zf.open(jsonl_name) as f:
            for line in f:
                obj = json.loads(line)
                typ = obj.get("type")
                if typ == "text":
                    payload = obj.get("payload", {}) or {}
                    ptype = payload.get("type")
                    if ptype == "text":
                        pending_texts.append(payload.get("msg", ""))
                    elif ptype == "status":
                        row = dict(payload)
                        concat = "\n\n".join(t for t in pending_texts if isinstance(t, str))
                        row["input_text_concat"] = concat
                        row["input_text_words"] = len(re.findall(r"\w+", concat))
                        row["input_text_chars"] = len(concat)
                        row["has_input"] = int(len(pending_texts) > 0)
                        pending_texts = []
                        status_rows.append(row)
                elif typ == "macro" and obj.get("macro") == "say":
                    args = obj.get("args", {}) or {}
                    why = args.get("why", {}) or {}
                    say_rows.append({
                        "t": why.get("t"),
                        "phase": why.get("phase"),
                        "vt_coverage": why.get("vt_coverage"),
                        "vt_entropy": why.get("vt_entropy"),
                        "connectome_entropy": why.get("connectome_entropy"),
                        "b1_z": why.get("b1_z"),
                        "sie_v2_valence_01": why.get("sie_v2_valence_01"),
                        "text": args.get("text", ""),
                    })

    status_df = pd.DataFrame(status_rows)
    say_df = pd.DataFrame(say_rows)
    # numeric coerce
    for df in [status_df, say_df]:
        for c in df.select_dtypes(include="object").columns:
            try:
                df[c] = pd.to_numeric(df[c], errors="ignore")
            except Exception:
                pass
    if "t" in status_df.columns:
        status_df = status_df.sort_values("t").reset_index(drop=True)
    return status_df, say_df


def build_tick_df(status_df: pd.DataFrame, say_df: pd.DataFrame) -> pd.DataFrame:
    if status_df.empty:
        return pd.DataFrame()
    # pick largest neuron run if multiple
    if "neurons" in status_df.columns:
        n_counts = status_df["neurons"].value_counts()
        best_n = n_counts.index[0]
        df = status_df[status_df["neurons"] == best_n].copy()
    else:
        df = status_df.copy()

    df = df.sort_values("t").reset_index(drop=True)

    if not say_df.empty and "t" in say_df.columns:
        say_agg = say_df.dropna(subset=["t"]).groupby("t").agg(
            say_count=("text", "size"),
            say_words=("text", lambda s: sum(len(re.findall(r"\w+", x)) for x in s if isinstance(x, str))),
        ).reset_index()
        df = df.merge(say_agg, on="t", how="left")
    else:
        df["say_count"] = 0
        df["say_words"] = 0

    df["say_count"] = df.get("say_count", 0).fillna(0)
    df["say_words"] = df.get("say_words", 0).fillna(0)
    df["did_say"] = (df["say_count"] > 0).astype(int)
    if "has_input" not in df.columns:
        df["has_input"] = 0
    return df


# ─────────────────────────────────────────────────────────
#  UTILITY MATH
# ─────────────────────────────────────────────────────────

def safe_z(X: np.ndarray) -> np.ndarray:
    mu = np.nanmean(X, axis=0); sd = np.nanstd(X, axis=0)
    sd[sd == 0] = 1.0
    return (X - mu) / sd

def gini_coeff(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float); x = x[np.isfinite(x)]
    if x.size == 0: return float("nan")
    mn = x.min()
    if mn < 0: x = x - mn
    s = x.sum()
    if s <= 0: return 0.0
    x = np.sort(x); n = x.size
    i = np.arange(1, n + 1, dtype=float)
    return float(1.0 - (2.0 * np.sum((n + 1 - i) * x)) / (n * s))

def powerlaw_mle(data: np.ndarray, xmin: float) -> Tuple[float, float, int]:
    x = np.asarray(data, dtype=float); x = x[x >= xmin]
    n = len(x)
    if n < 5: return float("nan"), float("nan"), n
    alpha = 1 + n / np.sum(np.log(x / xmin))
    xs = np.sort(x); cdf_emp = np.arange(1, n + 1) / n
    cdf_pl = 1 - (xs / xmin) ** (1 - alpha)
    ks = float(np.max(np.abs(cdf_emp - cdf_pl)))
    return float(alpha), ks, n

def welch_slope(x: np.ndarray, fs: float = 1.0) -> float:
    x = np.asarray(x, dtype=float); x = x[np.isfinite(x)]
    if x.size < 64: return float("nan")
    nperseg = int(min(1024, max(64, 2 ** int(np.floor(np.log2(x.size))))))
    f, Pxx = signal.welch(x, fs=fs, nperseg=nperseg, detrend="constant")
    mask = f > 0; f = f[mask]; Pxx = Pxx[mask]
    if f.size < 8: return float("nan")
    b, _ = np.polyfit(np.log10(f), np.log10(Pxx + 1e-24), 1)
    return -float(b)

def perm_entropy(x: np.ndarray, m: int = 4, tau: int = 1) -> float:
    x = np.asarray(x, dtype=float).ravel()
    n = x.size - (m - 1) * tau
    if n <= 1: return float("nan")
    idx = np.arange(m, dtype=np.int64) * tau
    X = x[np.arange(n)[:, None] + idx[None, :]]
    patterns = np.argsort(X, axis=1).astype(np.int64)
    powers = (m ** np.arange(m, dtype=np.int64))
    ids = (patterns * powers[None, :]).sum(axis=1)
    counts = np.bincount(ids, minlength=m ** m).astype(float)
    counts = counts[counts > 0]; p = counts / counts.sum()
    H = float(-(p * np.log(p)).sum())
    Hmax = math.log(math.factorial(m))
    return H / Hmax if Hmax > 0 else float("nan")

def lz_complexity(x: np.ndarray, threshold: Optional[float] = None) -> float:
    x = np.asarray(x, dtype=float).ravel()
    if x.size < 4: return float("nan")
    thr = threshold if threshold is not None else float(np.median(x))
    s = "".join("1" if v >= thr else "0" for v in x)
    n = len(s); i = 0; c = 1; l = 1; k = 1; kmax = 1
    while True:
        if s[i + k - 1] in s[:i + kmax]:
            k += 1
            if i + k > n:
                c += 1; break
        else:
            kmax = max(k, kmax); i += kmax; k = 1
            if i + 1 > n:
                break
            else:
                kmax = 1
    b = n / math.log2(n + 1) if n > 1 else 1
    return c / b

def transfer_entropy(x: np.ndarray, y: np.ndarray, bins: int = 8, lag: int = 1) -> float:
    x = np.asarray(x).ravel(); y = np.asarray(y).ravel()
    n = min(x.size, y.size)
    if n <= lag + 10: return float("nan")
    x = x[:n]; y = y[:n]
    # quantile bin
    def qbin(v):
        qs = np.nanquantile(v, np.linspace(0, 1, bins + 1))
        qs = np.unique(qs)
        if qs.size <= 2: return np.zeros(v.size, dtype=np.int64)
        return np.digitize(v, qs[1:-1], right=False).astype(np.int64)
    xd = qbin(x); yd = qbin(y)
    K = bins
    y1 = yd[lag:]; y0 = yd[:-lag]; x0 = xd[:-lag]
    idx_y0x0 = y0 * K + x0
    idx_full = y1 * K * K + idx_y0x0
    C_full = np.bincount(idx_full, minlength=K**3).astype(float)
    C_y0x0 = np.bincount(idx_y0x0, minlength=K**2).astype(float)
    C_y1y0 = np.bincount(y1 * K + y0, minlength=K**2).astype(float)
    C_y0   = np.bincount(y0, minlength=K).astype(float)
    N = float(y1.size)
    P = C_full / N; Py0x0 = C_y0x0 / N; Py1y0 = C_y1y0 / N; Py0 = C_y0 / N
    te = 0.0
    nz = np.nonzero(P)[0]
    for idx in nz:
        p = P[idx]
        y1v = idx // (K * K); rem = idx % (K * K); y0v = rem // K; x0v = rem % K
        p_yx = Py0x0[y0v * K + x0v]; p_yy = Py1y0[y1v * K + y0v]; p_y = Py0[y0v]
        if p_yx <= 0 or p_y <= 0: continue
        te += p * np.log((p / p_yx) / max(p_yy / p_y, 1e-12))
    return float(te)

def tc_o_gaussian(X: np.ndarray) -> Tuple[float, float, float]:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[0] < 8 or X.shape[1] < 2:
        return float("nan"), float("nan"), float("nan")
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-12)
    cov = np.cov(Xs, rowvar=False)
    d = cov.shape[0]
    sign, logdet = np.linalg.slogdet(cov + 1e-10 * np.eye(d))
    hX = 0.5 * (d * math.log(2 * math.pi * math.e) + logdet) if sign > 0 else float("nan")
    var = np.diag(cov)
    h_marg = 0.5 * (math.log(2 * math.pi * math.e) + np.log(np.clip(var, 1e-12, None)))
    TC = float(np.sum(h_marg) - hX) if math.isfinite(hX) else float("nan")
    h_minus = []
    for i in range(d):
        keep = [j for j in range(d) if j != i]
        cm = cov[np.ix_(keep, keep)]
        s2, ld2 = np.linalg.slogdet(cm + 1e-10 * np.eye(len(keep)))
        hm = 0.5 * (len(keep) * math.log(2 * math.pi * math.e) + ld2) if s2 > 0 else float("nan")
        h_minus.append(hm)
    if any(not math.isfinite(h) for h in h_minus) or not math.isfinite(hX):
        return TC, float("nan"), float("nan")
    DTC = float(sum(h_minus) - (d - 1) * hX)
    O = float(TC - DTC)
    return TC, DTC, O

def avalanches(x: np.ndarray, q: float = 0.75) -> Tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float); x = x[np.isfinite(x)]
    if x.size < 16: return np.array([]), np.array([])
    thr = float(np.quantile(x, q))
    active = x > thr
    sizes, durs = [], []
    i = 0
    while i < len(active):
        if active[i]:
            j = i
            while j < len(active) and active[j]: j += 1
            sizes.append(float(np.sum(x[i:j] - thr)))
            durs.append(j - i)
            i = j
        else:
            i += 1
    return np.array(sizes), np.array(durs)


# ─────────────────────────────────────────────────────────
#  EPOCH ASSIGNMENT
# ─────────────────────────────────────────────────────────

def assign_epochs(df: pd.DataFrame, n_epochs: int = 3) -> pd.DataFrame:
    """Split df into n_epochs by connectome_entropy quantile."""
    df = df.copy()
    if "connectome_entropy" not in df.columns:
        df["epoch"] = "E1_full"
        return df
    ent = df["connectome_entropy"].astype(float)
    lo, hi = ent.quantile(0.33), ent.quantile(0.67)
    labels = []
    for v in ent:
        if v <= lo: labels.append("E1_low_entropy_baseline")
        elif v >= hi: labels.append("E2_high_entropy_plateau")
        else: labels.append("E3_mid")
    df["epoch"] = labels
    return df


# ─────────────────────────────────────────────────────────
#  FIGURE FACTORIES
# ─────────────────────────────────────────────────────────

# -- Cross-correlation --

def fig_crosscorr(df: pd.DataFrame, cols: List[str], max_lag: int = 80) -> go.Figure:
    fig = sfig("Cross-Correlation Matrix", height=420)
    valid = [c for c in cols if c in df.columns]
    if len(valid) < 2:
        return fig
    data = df[valid].astype(float).values
    data = (data - np.nanmean(data, 0)) / (np.nanstd(data, 0) + 1e-12)
    n = data.shape[1]
    lags = np.arange(-max_lag, max_lag + 1)
    for i in range(n):
        for j in range(n):
            if i >= j: continue
            xi = data[:, i]; xj = data[:, j]
            mask = np.isfinite(xi) & np.isfinite(xj)
            xi = xi[mask]; xj = xj[mask]
            cc = [float(np.corrcoef(xi[:len(xi)-abs(l)] if l >= 0 else xi[abs(l):],
                                    xj[abs(l):] if l >= 0 else xj[:len(xj)-abs(l)])[0, 1])
                  for l in lags]
            fig.add_trace(go.Scatter(x=lags, y=cc, mode="lines", name=f"{valid[i]}→{valid[j]}",
                                     line=dict(width=1.2)))
    fig.update_xaxes(title_text="Lag (ticks)")
    fig.update_yaxes(title_text="Cross-correlation")
    return fig

def fig_crosscorr_pca_speed(df: pd.DataFrame, text_col: str = "input_text_words", max_lag: int = 60) -> go.Figure:
    internal = ["active_edges","vt_coverage","vt_entropy","connectome_entropy",
                "sie_v2_valence_01","b1_z"]
    valid = [c for c in internal if c in df.columns]
    if len(valid) < 3 or text_col not in df.columns:
        return sfig("CrossCorr PCA Speed vs Text", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    X = safe_z(X)
    pca = PCA(n_components=2)
    Xp = pca.fit_transform(X)
    speed = np.linalg.norm(np.diff(Xp, axis=0), axis=1)
    speed = np.concatenate([[0], speed])
    tx = df[text_col].astype(float).fillna(0).values
    lags = np.arange(-max_lag, max_lag + 1)
    cc = []
    for l in lags:
        a = speed[:len(speed)-abs(l)] if l >= 0 else speed[abs(l):]
        b = tx[abs(l):] if l >= 0 else tx[:len(tx)-abs(l)]
        mask = np.isfinite(a) & np.isfinite(b)
        if mask.sum() < 10: cc.append(float("nan")); continue
        r = float(np.corrcoef(a[mask], b[mask])[0, 1])
        cc.append(r)
    fig = sfig(f"CrossCorr: PCA Speed vs {text_col}", height=380)
    fig.add_trace(go.Scatter(x=lags, y=cc, mode="lines+markers",
                             marker=dict(size=3), line=dict(color=ACCENT, width=1.5)))
    fig.update_xaxes(title_text="Lag")
    fig.update_yaxes(title_text="Pearson r")
    return fig

# -- Event-triggered --

def fig_event_triggered(df: pd.DataFrame, signal_col: str, window: int = 100) -> go.Figure:
    if signal_col not in df.columns or "did_say" not in df.columns:
        return sfig(f"Event-triggered: {signal_col}", height=380)
    sig = df[signal_col].astype(float).values
    events = np.where(df["did_say"].values > 0)[0]
    events = events[(events >= window) & (events < len(sig) - window)]
    if len(events) < 3:
        return sfig(f"Event-triggered: {signal_col} (insufficient events)", height=380)
    mat = np.vstack([sig[e - window:e + window + 1] for e in events])
    mean = mat.mean(0); sem = mat.std(0) / math.sqrt(len(events))
    t = np.arange(-window, window + 1)
    fig = sfig(f"Event-triggered avg: {signal_col}  (n={len(events)})", height=380)
    fig.add_trace(go.Scatter(x=t, y=mean + sem, mode="lines", line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=t, y=mean - sem, mode="lines",
                             fill="tonexty", fillcolor="rgba(59,130,246,0.15)",
                             line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=t, y=mean, mode="lines",
                             name=signal_col, line=dict(color=ACCENT, width=2)))
    fig.add_vline(x=0, line=dict(color="#ef4444", width=1, dash="dash"))
    fig.update_xaxes(title_text="Ticks relative to say event")
    return fig

# -- Granger --

def fig_granger_heatmap(df: pd.DataFrame, channels: List[str], title: str = "Granger sig", lag: int = 5) -> go.Figure:
    try:
        from statsmodels.tsa.stattools import grangercausalitytests
    except ImportError:
        return sfig(f"{title} (statsmodels not available)", height=380)
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2:
        return sfig(title, height=380)
    n = len(valid)
    mat = np.full((n, n), float("nan"))
    data = df[valid].astype(float).fillna(method="ffill").values
    data = (data - data.mean(0)) / (data.std(0) + 1e-12)
    for i in range(n):
        for j in range(n):
            if i == j: continue
            xy = np.column_stack([data[:, j], data[:, i]])
            try:
                res = grangercausalitytests(xy, maxlag=lag, verbose=False)
                pval = res[lag][0]["ssr_ftest"][1]
                mat[i, j] = -np.log10(max(pval, 1e-12))
            except Exception:
                pass
    return _hm(mat, valid, valid, title=title, colorscale="Viridis", height=380)

def fig_granger_causal_density(df: pd.DataFrame, channels: List[str]) -> go.Figure:
    try:
        from statsmodels.tsa.stattools import grangercausalitytests
    except ImportError:
        return sfig("Granger Causal Density (statsmodels unavailable)", height=320)
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2:
        return sfig("Granger Causal Density", height=320)
    data = df[valid].astype(float).fillna(method="ffill").values
    data = (data - data.mean(0)) / (data.std(0) + 1e-12)
    pairs, densities = [], []
    for i in range(len(valid)):
        for j in range(len(valid)):
            if i == j: continue
            xy = np.column_stack([data[:, j], data[:, i]])
            try:
                res = grangercausalitytests(xy, maxlag=3, verbose=False)
                pval = res[3][0]["ssr_ftest"][1]
                pairs.append(f"{valid[i]}→{valid[j]}")
                densities.append(-np.log10(max(pval, 1e-12)))
            except Exception:
                pass
    if not pairs:
        return sfig("Granger Causal Density", height=320)
    order = np.argsort(densities)[::-1][:20]
    fig = sfig("Granger Causal Density (-log10 p)", height=max(320, len(order) * 22 + 60))
    fig.add_trace(go.Bar(
        y=[pairs[i] for i in order], x=[densities[i] for i in order],
        orientation="h", marker_color=ACCENT2,
    ))
    fig.update_layout(margin=dict(l=180, r=20, t=44, b=44))
    return fig

# -- Macro state --

def fig_macrostate_over_time(df: pd.DataFrame, n_clusters: int = 4) -> go.Figure:
    internal = ["active_edges","vt_coverage","vt_entropy","connectome_entropy",
                "sie_v2_valence_01","b1_z","cohesion_components"]
    valid = [c for c in internal if c in df.columns]
    if len(valid) < 2:
        return sfig("Macrostate Over Time", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    Xz = safe_z(X)
    pca = PCA(n_components=min(5, len(valid)))
    Xp = pca.fit_transform(Xz)
    km = MiniBatchKMeans(n_clusters=n_clusters, random_state=0, n_init=10)
    labels = km.fit_predict(Xp)
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    fig = sfig("Macrostate Over Time  (k=4 spectral)", height=380)
    for k in range(n_clusters):
        mask = labels == k
        fig.add_trace(go.Scatter(x=t[mask], y=labels[mask], mode="markers",
                                 name=f"State {k}", marker=dict(size=3, color=PALETTE[k % len(PALETTE)]),
                                 opacity=0.7))
    fig.update_yaxes(title_text="Macrostate")
    fig.update_xaxes(title_text="Tick")
    return fig, labels

def fig_macrostate_stationary(df: pd.DataFrame, labels: np.ndarray, epoch_name: str = "") -> go.Figure:
    if labels is None or len(labels) == 0:
        return sfig(f"Stationary dist {epoch_name}", height=320)
    n_k = int(labels.max()) + 1
    pi = np.bincount(labels, minlength=n_k).astype(float)
    pi /= pi.sum()
    fig = sfig(f"Stationary Distribution {epoch_name}", height=320)
    fig.add_trace(go.Bar(x=[f"S{k}" for k in range(n_k)], y=pi,
                         marker_color=PALETTE[:n_k]))
    fig.update_yaxes(title_text="Fraction of time")
    return fig

# -- MIP / Integration --

def fig_integration_timeseries(df: pd.DataFrame, channels: List[str],
                                window: int = 256, stride: int = 64,
                                log_scale: bool = False) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2:
        return sfig("Integration (TC) Timeseries", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    TCs, DTCs, Os, ts = [], [], [], []
    for start in range(0, len(X) - window + 1, stride):
        end = start + window
        TC, DTC, O = tc_o_gaussian(X[start:end])
        TCs.append(TC); DTCs.append(DTC); Os.append(O)
        ts.append(int(t[start + window // 2]))
    title = "Integration Timeseries (TC/DTC/O)  —  log scale" if log_scale else "Integration Timeseries (TC/DTC/O)"
    fig = sfig(title, height=400)
    for arr, name, col in [(TCs, "TC", PALETTE[0]), (DTCs, "DTC", PALETTE[1]), (Os, "O-info", PALETTE[2])]:
        y = np.array(arr, dtype=float)
        if log_scale: y = np.log1p(np.abs(y)) * np.sign(y)
        fig.add_trace(go.Scatter(x=ts, y=y, mode="lines", name=name, line=dict(color=col, width=1.5)))
    fig.update_xaxes(title_text="Tick")
    fig.update_yaxes(title_text="nats (log1p)" if log_scale else "nats")
    return fig

def fig_mip_singleton_counts(df: pd.DataFrame, channels: List[str],
                              window: int = 512, stride: int = 64) -> go.Figure:
    import itertools as it
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 3:
        return sfig("MIP Singleton Variable Counts", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    counts = Counter()
    for start in range(0, len(X) - window + 1, stride):
        Xw = X[start:start + window]
        Xs = (Xw - Xw.mean(0)) / (Xw.std(0) + 1e-12)
        cov = np.cov(Xs, rowvar=False)
        d = len(valid)
        best_mi, best_i = float("inf"), 0
        for i in range(d):
            keep = [j for j in range(d) if j != i]
            cA = cov[np.ix_([i], [i])]
            cB = cov[np.ix_(keep, keep)]
            cAB = cov[np.ix_([i] + keep, [i] + keep)]
            s1, l1 = np.linalg.slogdet(cA + 1e-10)
            s2, l2 = np.linalg.slogdet(cB + 1e-10 * np.eye(len(keep)))
            s3, l3 = np.linalg.slogdet(cAB + 1e-10 * np.eye(d))
            mi = 0.5 * (l1 + l2 - l3) if s1 > 0 and s2 > 0 and s3 > 0 else float("inf")
            if mi < best_mi: best_mi, best_i = mi, i
        counts[valid[best_i]] += 1
    keys = sorted(counts.keys(), key=lambda k: -counts[k])
    fig = sfig("MIP: Most-Isolated Variable (singleton count)", height=380)
    fig.add_trace(go.Bar(x=keys, y=[counts[k] for k in keys],
                         marker_color=[PALETTE[i % len(PALETTE)] for i in range(len(keys))]))
    fig.update_yaxes(title_text="Count (windows where variable is MIP)")
    return fig

# -- Network --

def fig_degree_ccdf(degrees: np.ndarray, title: str = "CCDF degree", color: str = ACCENT) -> go.Figure:
    d = np.sort(degrees[np.isfinite(degrees) & (degrees > 0)])
    ccdf = 1 - np.arange(1, len(d) + 1) / len(d)
    xmin = max(1, int(np.quantile(d, 0.5)))
    alpha, ks, n_tail = powerlaw_mle(d, xmin)
    xfit = np.array([xmin, d.max()])
    fig = sfig(title, height=360)
    fig.add_trace(go.Scatter(x=d, y=ccdf, mode="markers",
                             marker=dict(size=3, color=color, opacity=0.7),
                             name="empirical"))
    if math.isfinite(alpha):
        ccdf_fit = (xfit / xmin) ** (1 - alpha)
        fig.add_trace(go.Scatter(x=xfit, y=ccdf_fit, mode="lines",
                                 line=dict(color="#ef4444", dash="dash", width=1.5),
                                 name=f"PL α≈{alpha:.2f}"))
    fig.update_xaxes(type="log", title_text="Degree")
    fig.update_yaxes(type="log", title_text="P(D ≥ d)")
    return fig

def fig_in_vs_out_scatter(df: pd.DataFrame) -> go.Figure:
    if "in_degree" not in df.columns or "out_degree" not in df.columns:
        return sfig("In vs Out Degree", height=360)
    fig = sfig("In-degree vs Out-degree", height=360)
    fig.add_trace(go.Scatter(x=df["in_degree"], y=df["out_degree"],
                             mode="markers", marker=dict(size=3, color=ACCENT, opacity=0.5)))
    fig.update_xaxes(title_text="In-degree"); fig.update_yaxes(title_text="Out-degree")
    return fig

def fig_jaccard_heatmap(df_snapshots: pd.DataFrame, top_k: int = 50) -> go.Figure:
    if df_snapshots.empty:
        return sfig("Jaccard Hub Recurrence", height=360)
    steps = df_snapshots["step"].unique()[:14]
    sets = {}
    for s in steps:
        sub = df_snapshots[df_snapshots["step"] == s]
        if "degree" in sub.columns:
            top = sub.nlargest(top_k, "degree")["node_id"].values
            sets[s] = set(top.tolist())
    labels = [str(s) for s in steps]
    n = len(labels)
    J = np.zeros((n, n))
    for i, si in enumerate(steps):
        for j, sj in enumerate(steps):
            if si not in sets or sj not in sets: continue
            inter = len(sets[si] & sets[sj]); union = len(sets[si] | sets[sj])
            J[i, j] = inter / union if union else 0
    return _hm(J, labels, labels, "Jaccard Hub Recurrence (top-k hubs)", colorscale="Cividis")

def fig_phase_portrait(df: pd.DataFrame) -> go.Figure:
    internal = ["active_edges","vt_coverage","vt_entropy","connectome_entropy","sie_v2_valence_01","b1_z"]
    valid = [c for c in internal if c in df.columns]
    if len(valid) < 2:
        return sfig("Phase Portrait (PC1 vs PC2)", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    Xz = safe_z(X)
    pca = PCA(n_components=2)
    Xp = pca.fit_transform(Xz)
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    n = min(1000, len(Xp))
    idx = np.linspace(0, len(Xp) - 1, n, dtype=int)
    fig = sfig("Phase Portrait  (PC1 × PC2)", height=400)
    fig.add_trace(go.Scatter(x=Xp[idx, 0], y=Xp[idx, 1], mode="markers",
                             marker=dict(size=3, color=t[idx], colorscale="Plasma", opacity=0.7,
                                         colorbar=dict(title="tick", tickfont=dict(size=8))),
                             name="trajectory"))
    fig.update_xaxes(title_text="PC1"); fig.update_yaxes(title_text="PC2")
    return fig

def fig_lz_complexity_pca(df: pd.DataFrame) -> go.Figure:
    internal = ["active_edges","vt_coverage","vt_entropy","connectome_entropy","sie_v2_valence_01","b1_z"]
    valid = [c for c in internal if c in df.columns]
    if len(valid) < 2:
        return sfig("LZ Complexity (PCA sign)", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    Xz = safe_z(X)
    pca = PCA(n_components=2)
    Xp = pca.fit_transform(Xz)
    win = 200; stride = 50
    ts, lzs = [], []
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    for s in range(0, len(Xp) - win, stride):
        ts.append(int(t[s + win // 2]))
        lzs.append(lz_complexity(Xp[s:s + win, 0]))
    fig = sfig("LZ Complexity — PCA sign timeseries", height=380)
    fig.add_trace(go.Scatter(x=ts, y=lzs, mode="lines",
                             line=dict(color=PALETTE[3], width=1.5), name="LZ(PC1)"))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="LZ complexity")
    return fig

def fig_sie_memory_vs_n(df: pd.DataFrame, full_status: pd.DataFrame) -> go.Figure:
    if "neurons" not in full_status.columns or "sie_v2_valence_01" not in full_status.columns:
        return sfig("SIE Memory vs N", height=360)
    groups = []
    for n, sub in full_status.groupby("neurons"):
        v = sub["sie_v2_valence_01"].astype(float).dropna()
        if v.size < 10: continue
        ac = float(pd.Series(v.values).autocorr(lag=1))
        groups.append({"neurons": n, "autocorr_lag1": ac, "n_ticks": len(v)})
    if not groups:
        return sfig("SIE Memory vs N", height=360)
    gdf = pd.DataFrame(groups).sort_values("neurons")
    fig = sfig("SIE Memory (autocorr lag-1) vs Neuron Count", height=360)
    fig.add_trace(go.Scatter(x=gdf["neurons"], y=gdf["autocorr_lag1"],
                             mode="markers+lines", marker=dict(size=8, color=ACCENT),
                             line=dict(width=1.5)))
    fig.update_xaxes(title_text="N neurons"); fig.update_yaxes(title_text="Autocorr lag-1")
    return fig

# -- PCI-like --

def fig_pci_like(df: pd.DataFrame, channels: List[str],
                 window: int = 512, stride: int = 128) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2:
        return sfig("PCI-like Timeseries", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    pci_vals, ts_out = [], []
    for s in range(0, len(X) - window, stride):
        Xw = X[s:s + window]
        # PCI-like = LZ(sign(PCA1 - median)) / entropy
        Xs = (Xw - Xw.mean(0)) / (Xw.std(0) + 1e-12)
        pca = PCA(n_components=1)
        pc1 = pca.fit_transform(Xs)[:, 0]
        lz = lz_complexity(pc1)
        pe = perm_entropy(pc1)
        pci_vals.append(lz * pe if math.isfinite(lz) and math.isfinite(pe) else float("nan"))
        ts_out.append(int(t[s + window // 2]))
    fig = sfig("PCI-like (LZ × PermEntropy)", height=380)
    fig.add_trace(go.Scatter(x=ts_out, y=pci_vals, mode="lines",
                             line=dict(color=ACCENT2, width=1.5), name="PCI-like"))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="PCI-like score")
    return fig

def fig_pci_by_epoch(df: pd.DataFrame, channels: List[str]) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2 or "epoch" not in df.columns:
        return sfig("PCI-like by Epoch (box)", height=360)
    X = df[valid].astype(float).fillna(method="ffill").values
    window = 256
    pci_by_epoch = defaultdict(list)
    t_arr = df["t"].values if "t" in df.columns else np.arange(len(df))
    epochs = df["epoch"].values
    for s in range(0, len(X) - window, 64):
        Xw = X[s:s + window]
        Xs = (Xw - Xw.mean(0)) / (Xw.std(0) + 1e-12)
        pca = PCA(n_components=1)
        pc1 = pca.fit_transform(Xs)[:, 0]
        lz = lz_complexity(pc1); pe = perm_entropy(pc1)
        score = lz * pe if math.isfinite(lz) and math.isfinite(pe) else float("nan")
        if math.isfinite(score):
            ep = epochs[s + window // 2]
            pci_by_epoch[ep].append(score)
    fig = sfig("PCI-like by Epoch", height=360)
    for ep, color in zip(sorted(pci_by_epoch.keys()), PALETTE):
        vals = pci_by_epoch[ep]
        fig.add_trace(go.Box(y=vals, name=ep, marker_color=color, boxmean=True))
    fig.update_yaxes(title_text="PCI-like")
    return fig

def fig_pci_events_vs_controls(df: pd.DataFrame, channels: List[str]) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2 or "did_say" not in df.columns:
        return sfig("PCI-like: Events vs Controls", height=360)
    X = df[valid].astype(float).fillna(method="ffill").values
    window = 128
    pci_event, pci_ctrl = [], []
    say = df["did_say"].values
    for s in range(window, len(X) - window, 32):
        Xw = X[s:s + window]
        Xs = (Xw - Xw.mean(0)) / (Xw.std(0) + 1e-12)
        pca = PCA(n_components=1)
        pc1 = pca.fit_transform(Xs)[:, 0]
        lz = lz_complexity(pc1); pe = perm_entropy(pc1)
        score = lz * pe if math.isfinite(lz) and math.isfinite(pe) else float("nan")
        if not math.isfinite(score): continue
        if say[s + window // 2] > 0:
            pci_event.append(score)
        else:
            pci_ctrl.append(score)
    fig = sfig("PCI-like: Say-events vs Controls", height=360)
    fig.add_trace(go.Box(y=pci_event, name="Say event", marker_color=PALETTE[2], boxmean=True))
    fig.add_trace(go.Box(y=pci_ctrl,  name="Control",   marker_color=PALETTE[4], boxmean=True))
    fig.update_yaxes(title_text="PCI-like")
    return fig

# -- Predictive MI --

def fig_predictive_mi(df: pd.DataFrame, channels: List[str], max_lag: int = 50) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2:
        return sfig("Predictive MI vs Lag", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    pca = PCA(n_components=2)
    Xp = pca.fit_transform((X - X.mean(0)) / (X.std(0) + 1e-12))
    pc1 = Xp[:, 0]
    lags = np.arange(1, max_lag + 1)
    mi_vals = []
    for l in lags:
        cov = np.cov(pc1[:-l], pc1[l:])
        r = cov[0, 1] / (math.sqrt(cov[0, 0] * cov[1, 1]) + 1e-12)
        mi_vals.append(max(0, -0.5 * math.log(max(1 - r ** 2, 1e-10))))
    fig = sfig("Predictive MI (Gaussian) vs Lag  —  PC1", height=380)
    fig.add_trace(go.Scatter(x=lags, y=mi_vals, mode="lines+markers",
                             marker=dict(size=4), line=dict(color=PALETTE[5], width=1.5)))
    fig.update_xaxes(title_text="Lag (ticks)"); fig.update_yaxes(title_text="MI (nats)")
    return fig

# -- Rolling --

def fig_rolling_autocorr(df: pd.DataFrame, col: str, lag: int = 1, window: int = 300) -> go.Figure:
    if col not in df.columns:
        return sfig(f"Rolling Autocorr {col}", height=340)
    x = df[col].astype(float).fillna(method="ffill")
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    ac = x.rolling(window, min_periods=window // 2).apply(
        lambda v: pd.Series(v).autocorr(lag=lag), raw=False)
    fig = sfig(f"Rolling Autocorr (lag={lag}) — {col}", height=340)
    fig.add_trace(go.Scatter(x=t, y=ac.values, mode="lines",
                             line=dict(color=ACCENT, width=1.2)))
    fig.add_hline(y=0, line=dict(color=MUTED, width=0.8, dash="dot"))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text=f"Autocorr lag-{lag}")
    return fig

def fig_rolling_variance(df: pd.DataFrame, col: str, window: int = 300) -> go.Figure:
    if col not in df.columns:
        return sfig(f"Rolling Variance {col}", height=340)
    x = df[col].astype(float).fillna(method="ffill")
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    rv = x.rolling(window, min_periods=window // 2).var()
    fig = sfig(f"Rolling Variance — {col}", height=340)
    fig.add_trace(go.Scatter(x=t, y=rv.values, mode="lines",
                             line=dict(color=PALETTE[1], width=1.2)))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="Variance")
    return fig

# -- Spectral --

def fig_spectral_slope(df: pd.DataFrame, cols: List[str]) -> go.Figure:
    valid = [c for c in cols if c in df.columns]
    slopes = {}
    for c in valid:
        x = df[c].astype(float).fillna(method="ffill").values
        slopes[c] = welch_slope(x)
    fig = sfig("Spectral Slope (1/f^β)  per signal", height=360)
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(valid))]
    fig.add_trace(go.Bar(x=valid, y=[slopes[c] for c in valid],
                         marker_color=colors))
    fig.add_hline(y=1.0, line=dict(color="#f59e0b", dash="dash", width=1),
                  annotation_text="1/f")
    fig.update_yaxes(title_text="β  (spectral slope)")
    return fig

def fig_spectral_fit_scatter(df: pd.DataFrame, col: str) -> go.Figure:
    if col not in df.columns:
        return sfig(f"Spectral fit — {col}", height=360)
    x = df[col].astype(float).fillna(method="ffill").values
    x = x[np.isfinite(x)]
    if x.size < 64:
        return sfig(f"Spectral fit — {col} (insufficient data)", height=360)
    nperseg = int(min(1024, max(64, 2 ** int(np.floor(np.log2(x.size))))))
    f, Pxx = signal.welch(x, fs=1.0, nperseg=nperseg, detrend="constant")
    mask = f > 0; f = f[mask]; Pxx = Pxx[mask]
    b, a = np.polyfit(np.log10(f), np.log10(Pxx + 1e-24), 1)
    fit = 10 ** (b * np.log10(f) + a)
    fig = sfig(f"Spectral fit — {col}  β≈{-b:.2f}", height=360)
    fig.add_trace(go.Scatter(x=f, y=Pxx, mode="markers",
                             marker=dict(size=3, color=ACCENT, opacity=0.6), name="PSD"))
    fig.add_trace(go.Scatter(x=f, y=fit, mode="lines",
                             line=dict(color="#ef4444", dash="dash", width=1.5),
                             name=f"fit β={-b:.2f}"))
    fig.update_xaxes(type="log", title_text="Frequency"); fig.update_yaxes(type="log", title_text="PSD")
    return fig

# -- TC/DTC/O --

def fig_o_information_ts(df: pd.DataFrame, channels: List[str], window: int = 256, stride: int = 64) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 3:
        return sfig("O-information Timeseries", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    Os, ts = [], []
    for s in range(0, len(X) - window, stride):
        _, _, O = tc_o_gaussian(X[s:s + window])
        Os.append(O); ts.append(int(t[s + window // 2]))
    fig = sfig("O-information Timeseries  (>0 = TC-dominant, <0 = synergy)", height=380)
    y = np.array(Os); colors = [PALETTE[0] if v >= 0 else PALETTE[6] for v in y]
    fig.add_trace(go.Bar(x=ts, y=y, marker_color=colors, name="O"))
    fig.add_hline(y=0, line=dict(color=MUTED, width=0.8))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="O-info (nats)")
    return fig

def fig_tc_timeseries(df: pd.DataFrame, channels: List[str], window: int = 256, stride: int = 64) -> go.Figure:
    valid = [c for c in channels if c in df.columns]
    if len(valid) < 2:
        return sfig("TC Timeseries", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    TCs, ts = [], []
    for s in range(0, len(X) - window, stride):
        TC, _, _ = tc_o_gaussian(X[s:s + window])
        TCs.append(TC); ts.append(int(t[s + window // 2]))
    fig = sfig("Total Correlation (TC) Timeseries", height=380)
    fig.add_trace(go.Scatter(x=ts, y=TCs, mode="lines",
                             line=dict(color=PALETTE[0], width=1.5), name="TC"))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="TC (nats)")
    return fig

# -- Biological neural comparison --

def fig_avalanche_ccdf(df: pd.DataFrame, col: str = "active_edges") -> go.Figure:
    if col not in df.columns:
        return sfig("Avalanche Size CCDF", height=360)
    x = df[col].astype(float).fillna(method="ffill").values
    sizes, durs = avalanches(x, q=0.75)
    if sizes.size < 10:
        return sfig("Avalanche Size CCDF (insufficient)", height=360)
    s_sorted = np.sort(sizes); ccdf = 1 - np.arange(1, len(s_sorted) + 1) / len(s_sorted)
    xmin = np.quantile(s_sorted, 0.3)
    alpha, _, _ = powerlaw_mle(s_sorted, xmin)
    fig = sfig(f"Avalanche Size CCDF  (α≈{alpha:.2f})", height=360)
    fig.add_trace(go.Scatter(x=s_sorted, y=ccdf, mode="markers",
                             marker=dict(size=3, color=ACCENT, opacity=0.6), name="data"))
    if math.isfinite(alpha):
        xfit = np.logspace(np.log10(max(xmin, 0.01)), np.log10(s_sorted.max()), 40)
        fit = (xfit / xmin) ** (1 - alpha)
        fig.add_trace(go.Scatter(x=xfit, y=fit, mode="lines",
                                 line=dict(color="#ef4444", dash="dash", width=1.5),
                                 name=f"PL α={alpha:.2f}"))
    fig.update_xaxes(type="log", title_text="Avalanche size")
    fig.update_yaxes(type="log", title_text="CCDF")
    return fig

def fig_psd_firing(df: pd.DataFrame, col: str) -> go.Figure:
    if col not in df.columns:
        return sfig(f"PSD — {col}", height=360)
    x = df[col].astype(float).fillna(method="ffill").values
    x = x[np.isfinite(x)]
    if x.size < 64:
        return sfig(f"PSD — {col}", height=360)
    nperseg = int(min(1024, max(64, 2 ** int(np.floor(np.log2(x.size))))))
    f, Pxx = signal.welch(x, fs=1.0, nperseg=nperseg, detrend="constant")
    mask = f > 0
    fig = sfig(f"PSD — {col}", height=360)
    fig.add_trace(go.Scatter(x=f[mask], y=Pxx[mask], mode="lines",
                             line=dict(color=PALETTE[3], width=1.2)))
    fig.update_xaxes(type="log", title_text="Frequency (1/tick)")
    fig.update_yaxes(type="log", title_text="Power")
    return fig

def fig_order_params(df: pd.DataFrame) -> go.Figure:
    cols = ["vt_coverage","connectome_entropy","sie_v2_valence_01","b1_z"]
    valid = [c for c in cols if c in df.columns]
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    fig = sfig("Order Parameters Timeseries", height=400)
    for i, c in enumerate(valid):
        x = df[c].astype(float).values
        x = (x - np.nanmean(x)) / (np.nanstd(x) + 1e-12)
        fig.add_trace(go.Scatter(x=t, y=x, mode="lines", name=c,
                                 line=dict(color=PALETTE[i], width=1.2)))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="z-score")
    return fig

def fig_fisher_speed(df: pd.DataFrame) -> go.Figure:
    internal = ["active_edges","vt_coverage","vt_entropy","connectome_entropy","sie_v2_valence_01","b1_z"]
    valid = [c for c in internal if c in df.columns]
    if len(valid) < 2:
        return sfig("Fisher Speed vs ADC Mass", height=380)
    X = df[valid].astype(float).fillna(method="ffill").values
    Xz = safe_z(X)
    dX = np.diff(Xz, axis=0)
    speed = np.linalg.norm(dX, axis=1)
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    fig = sfig("Fisher Information Speed  (||ΔΨ||₂)", height=380)
    fig.add_trace(go.Scatter(x=t[1:], y=speed, mode="lines",
                             line=dict(color=PALETTE[5], width=1.2), name="||ΔΨ||"))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="State-space speed")
    return fig

def fig_free_energy(df: pd.DataFrame) -> go.Figure:
    if "connectome_entropy" not in df.columns:
        return sfig("Free Energy Landscape", height=380)
    ent = df["connectome_entropy"].astype(float).dropna()
    nbins = 80
    counts, edges = np.histogram(ent, bins=nbins, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    F = -np.log(counts + 1e-12)
    F -= F.min()
    fig = sfig("Free Energy Landscape  F(H) = -log P(H)", height=380)
    fig.add_trace(go.Scatter(x=centers, y=F, mode="lines",
                             line=dict(color=PALETTE[2], width=2), fill="tozeroy",
                             fillcolor="rgba(16,185,129,0.12)"))
    fig.update_xaxes(title_text="Connectome entropy H")
    fig.update_yaxes(title_text="F (a.u.)")
    return fig

# -- Scale-free --

def fig_tail_fit_grid(degrees: np.ndarray, title_prefix: str = "") -> go.Figure:
    d = degrees[np.isfinite(degrees) & (degrees > 0)]
    xmins = np.percentile(d, [20, 40, 60, 80])
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=[f"xmin={int(xm)}" for xm in xmins],
                        shared_xaxes=False)
    fig.update_layout(**LAYOUT_BASE, height=500,
                      title=dict(text=f"{title_prefix} Tail Fit Grid", x=0.5))
    for idx, xm in enumerate(xmins):
        r, c = idx // 2 + 1, idx % 2 + 1
        xs = np.sort(d[d >= xm]); ccdf = 1 - np.arange(1, len(xs) + 1) / len(xs)
        alpha, ks, n = powerlaw_mle(d, xm)
        fig.add_trace(go.Scatter(x=xs, y=ccdf, mode="markers",
                                 marker=dict(size=3, color=ACCENT, opacity=0.6),
                                 name=f"data (n={n})", showlegend=(idx == 0)), row=r, col=c)
        if math.isfinite(alpha):
            xfit = np.logspace(np.log10(max(xm, 1)), np.log10(xs.max()), 40)
            fig.add_trace(go.Scatter(x=xfit, y=(xfit / xm) ** (1 - alpha),
                                     mode="lines", line=dict(color="#ef4444", dash="dash"),
                                     name=f"α={alpha:.2f}", showlegend=(idx == 0)), row=r, col=c)
        fig.update_xaxes(type="log", row=r, col=c)
        fig.update_yaxes(type="log", row=r, col=c)
    return fig

def fig_gini_metrics(df: pd.DataFrame) -> go.Figure:
    cols = ["active_edges","vt_coverage","vt_entropy","connectome_entropy",
            "sie_v2_valence_01","b1_z","cohesion_components"]
    valid = [c for c in cols if c in df.columns]
    ginis = {c: gini_coeff(df[c].astype(float).dropna().values) for c in valid}
    fig = sfig("Gini Coefficient per Metric", height=340)
    keys = [k for k in ginis if math.isfinite(ginis[k])]
    vals = [ginis[k] for k in keys]
    fig.add_trace(go.Bar(x=keys, y=vals,
                         marker_color=[PALETTE[i % len(PALETTE)] for i in range(len(keys))]))
    fig.update_yaxes(title_text="Gini")
    return fig

# -- Regime --

def fig_regime_all_ticks(df: pd.DataFrame, regime_col: str = "phase") -> go.Figure:
    if regime_col not in df.columns:
        return sfig("Regime All Ticks", height=380)
    t = df["t"].values if "t" in df.columns else np.arange(len(df))
    ent = df["connectome_entropy"].astype(float).values if "connectome_entropy" in df.columns else np.zeros(len(df))
    fig = sfig("Regime 3 — All Ticks  (entropy × phase)", height=380)
    fig.add_trace(go.Scatter(x=t, y=ent, mode="lines",
                             line=dict(color=PALETTE[0], width=1.0), name="connectome_entropy"))
    phases = df[regime_col].astype(float)
    for ph in sorted(phases.dropna().unique()):
        mask = (phases == ph).values
        if mask.sum() == 0: continue
        fig.add_trace(go.Scatter(x=t[mask], y=ent[mask], mode="markers",
                                 marker=dict(size=4, color=PALETTE[int(ph) % len(PALETTE)], opacity=0.6),
                                 name=f"phase {int(ph)}"))
    fig.update_xaxes(title_text="Tick"); fig.update_yaxes(title_text="Connectome entropy")
    return fig

def fig_emission_microstructure(df: pd.DataFrame) -> go.Figure:
    if "did_say" not in df.columns:
        return sfig("Emission Microstructure", height=380)
    say_ticks = df[df["did_say"] > 0]["t"].values if "t" in df.columns else np.where(df["did_say"] > 0)[0]
    if len(say_ticks) < 2:
        return sfig("Emission Microstructure (no events)", height=380)
    ipi = np.diff(np.sort(say_ticks))
    fig = sfig("Emission Microstructure  (inter-say intervals)", height=380)
    fig.add_trace(go.Histogram(x=ipi, nbinsx=60,
                               marker_color=ACCENT, opacity=0.8, name="IPI"))
    fig.update_xaxes(title_text="Inter-emission interval (ticks)")
    fig.update_yaxes(title_text="Count")
    return fig


# ─────────────────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────────────────

NAV_ITEMS = [
    ("overview",        "○  Overview"),
    ("crosscorr",       "↔  Cross-Correlation"),
    ("events",          "⚡  Event-Triggered"),
    ("granger",         "→  Granger"),
    ("macrostate",      "◉  Macrostate"),
    ("mip",             "∩  MIP / Integration"),
    ("network",         "⬡  Network"),
    ("pci",             "Φ  PCI-like"),
    ("predictive_mi",   "I  Predictive MI"),
    ("rolling",         "~  Rolling Stats"),
    ("spectral",        "♫  Spectral"),
    ("tc_o",            "Σ  TC / O-info"),
    ("bio_neural",      "🧠  Bio Neural"),
    ("scale_free",      "⚖  Scale-Free"),
    ("regimes",         "▦  Regimes"),
]

INTERNAL_CHANNELS = [
    "active_edges","vt_coverage","vt_entropy","connectome_entropy",
    "cohesion_components","b1_z","sie_v2_valence_01","sie_v2_reward_mean",
    "sie_total_reward","sie_valence_01","adc_territories",
]

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&display=swap",
        dbc.themes.BOOTSTRAP,
    ],
    suppress_callback_exceptions=True,
)
server = app.server

_NAV_STYLE = dict(
    background=BG,
    borderRight=f"1px solid {BORDER}",
    height="100vh",
    overflowY="auto",
    position="fixed",
    width="220px",
    padding="12px 0",
    zIndex=100,
)
_MAIN_STYLE = dict(marginLeft="220px", padding="20px 28px", background=BG, minHeight="100vh")

def nav_sidebar():
    items = []
    for key, label in NAV_ITEMS:
        items.append(html.A(
            label,
            id=f"nav-{key}",
            href=f"#{key}",
            style=dict(
                display="block", padding="7px 18px",
                color=MUTED, textDecoration="none",
                fontSize="12px", fontFamily="'JetBrains Mono', monospace",
                letterSpacing="0.3px",
                borderLeft="3px solid transparent",
                transition="all 0.15s",
            ),
        ))
    return html.Div(
        [
            html.Div("VDM ANALYSIS", style=dict(
                padding="14px 18px 10px", fontSize="10px", fontWeight="600",
                color=ACCENT, letterSpacing="2px",
                fontFamily="'JetBrains Mono', monospace",
            )),
            html.Hr(style=dict(borderColor=BORDER, margin="0 12px 8px")),
        ] + items,
        style=_NAV_STYLE,
    )

def upload_bar():
    return html.Div([
        html.Div([
            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    html.Span("▲ Drop utd_events.jsonl.zip  or click to browse",
                              style=dict(color=MUTED, fontSize="12px")),
                ]),
                style=dict(
                    padding="10px 20px", border=f"1px dashed {BORDER}",
                    borderRadius="6px", cursor="pointer",
                    background=SURFACE, color=FONT_COL,
                    fontFamily="'JetBrains Mono', monospace",
                    display="inline-block", minWidth="380px",
                ),
                multiple=False,
            ),
            html.Span(id="upload-status",
                      style=dict(marginLeft="16px", fontSize="11px",
                                 color=MUTED, fontFamily="'JetBrains Mono', monospace")),
        ], style=dict(display="flex", alignItems="center", gap="12px")),
        dcc.Loading(
            html.Div(id="loading-indicator"),
            type="circle", color=ACCENT,
            style=dict(marginLeft="12px"),
        ),
    ], style=dict(
        background=SURFACE, border=f"1px solid {BORDER}",
        borderRadius="8px", padding="14px 20px",
        marginBottom="20px", display="flex", alignItems="center",
        justifyContent="space-between",
    ))

def section(anchor_id: str, title: str, children) -> html.Div:
    return html.Div([
        html.H3(title, id=anchor_id, style=dict(
            color="#e2e8f0", fontSize="14px", fontWeight="600",
            fontFamily="'JetBrains Mono', monospace",
            borderBottom=f"1px solid {BORDER}",
            paddingBottom="8px", marginBottom="16px",
            letterSpacing="1px",
        )),
        *children,
    ], style=dict(marginBottom="36px"))

def fig_row(*figures) -> html.Div:
    cols = [dcc.Graph(figure=f, config=dict(displayModeBar=False))
            for f in figures if f is not None]
    cols_div = [html.Div(c, style=dict(flex="1", minWidth="0")) for c in cols]
    return html.Div(cols_div, style=dict(display="flex", gap="12px", flexWrap="wrap"))

app.layout = html.Div([
    dcc.Store(id="store-tick-df"),
    dcc.Store(id="store-status-df"),
    dcc.Store(id="store-say-df"),
    dcc.Store(id="store-labels"),
    nav_sidebar(),
    html.Div([
        html.Div("VDM Analysis Dashboard", style=dict(
            fontSize="22px", fontWeight="600", color="#e2e8f0",
            fontFamily="'JetBrains Mono', monospace",
            letterSpacing="1px", marginBottom="16px",
        )),
        upload_bar(),
        html.Div(id="dashboard-content", children=[
            html.Div("Upload a utd_events.jsonl.zip to begin analysis.",
                     style=dict(color=MUTED, fontFamily="'JetBrains Mono', monospace",
                                fontSize="12px", marginTop="40px"))
        ]),
    ], style=_MAIN_STYLE),
], style=dict(background=BG, minHeight="100vh"))


# ─────────────────────────────────────────────────────────
#  CALLBACKS
# ─────────────────────────────────────────────────────────

@app.callback(
    Output("store-tick-df", "data"),
    Output("store-status-df", "data"),
    Output("store-say-df", "data"),
    Output("upload-status", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
)
def process_upload(contents, filename):
    if contents is None:
        return no_update, no_update, no_update, ""
    try:
        _, b64 = contents.split(",", 1)
        raw = base64.b64decode(b64)
        status_df, say_df = parse_utd_zip(raw)
        tick_df = build_tick_df(status_df, say_df)
        tick_df = assign_epochs(tick_df)
        return (
            tick_df.to_json(orient="split", date_format="iso"),
            status_df.to_json(orient="split", date_format="iso"),
            say_df.to_json(orient="split", date_format="iso"),
            f"✓  {filename}  |  {len(tick_df):,} ticks  |  {int(tick_df.get('did_say', pd.Series([0])).sum())} say events",
        )
    except Exception as e:
        return no_update, no_update, no_update, f"✗ {str(e)[:80]}"


@app.callback(
    Output("dashboard-content", "children"),
    Input("store-tick-df", "data"),
    State("store-status-df", "data"),
    prevent_initial_call=True,
)
def render_dashboard(tick_json, status_json):
    if not tick_json:
        return html.Div("No data.", style=dict(color=MUTED))
    try:
        df = pd.read_json(io.StringIO(tick_json), orient="split")
        status_df = pd.read_json(io.StringIO(status_json), orient="split") if status_json else pd.DataFrame()
    except Exception as e:
        return html.Div(f"Parse error: {e}", style=dict(color="#ef4444"))

    ch = [c for c in INTERNAL_CHANNELS if c in df.columns]

    # -- OVERVIEW --
    n_ticks = len(df)
    t_range = f"{int(df['t'].min())} → {int(df['t'].max())}" if "t" in df.columns else "—"
    say_rate = float(df["did_say"].mean()) if "did_say" in df.columns else 0
    cards = []
    for k, v in [("Ticks", f"{n_ticks:,}"), ("Tick range", t_range),
                  ("Say rate", f"{say_rate:.4f}"), ("Channels", str(len(ch)))]:
        cards.append(html.Div([
            html.Div(k, style=dict(fontSize="10px", color=MUTED, marginBottom="4px")),
            html.Div(v, style=dict(fontSize="18px", fontWeight="600", color="#e2e8f0")),
        ], style=dict(background=SURFACE, border=f"1px solid {BORDER}", borderRadius="6px",
                      padding="14px 18px", flex="1")))

    overview_cards = html.Div(cards, style=dict(display="flex", gap="12px", marginBottom="20px"))

    timeseries_cols = ["connectome_entropy","vt_coverage","active_edges","sie_v2_valence_01","b1_z"]
    ts_valid = [c for c in timeseries_cols if c in df.columns]
    ts_fig = sfig("Raw Timeseries Overview", height=400)
    t_arr = df["t"].values if "t" in df.columns else np.arange(len(df))
    for i, c in enumerate(ts_valid):
        x = df[c].astype(float)
        x_z = (x - x.mean()) / (x.std() + 1e-12)
        ts_fig.add_trace(go.Scatter(x=t_arr, y=x_z, mode="lines", name=c,
                                    line=dict(color=PALETTE[i], width=1.0), opacity=0.85))
    ts_fig.update_xaxes(title_text="Tick"); ts_fig.update_yaxes(title_text="z-score")

    overview_sec = section("overview", "OVERVIEW", [
        overview_cards,
        dcc.Graph(figure=ts_fig, config=dict(displayModeBar=True)),
    ])

    # -- CROSSCORR --
    cc_fig = fig_crosscorr(df, ch[:6])
    cc_pca_words = fig_crosscorr_pca_speed(df, text_col="input_text_words")
    cc_pca_has = fig_crosscorr_pca_speed(df, text_col="has_input")
    cc_sec = section("crosscorr", "CROSS-CORRELATION", [
        fig_row(cc_fig),
        fig_row(cc_pca_words, cc_pca_has),
    ])

    # -- EVENT-TRIGGERED --
    ev_figs = [fig_event_triggered(df, c, window=80) for c in ["connectome_entropy","vt_coverage",
                                                                 "active_edges","sie_v2_valence_01"]
               if c in df.columns]
    ev_sec = section("events", "EVENT-TRIGGERED AVERAGES", [
        fig_row(*ev_figs[:2]),
        fig_row(*ev_figs[2:]),
    ])

    # -- GRANGER --
    gr_bar = fig_granger_causal_density(df, ch)
    epochs = df["epoch"].unique() if "epoch" in df.columns else ["full"]
    gr_heatmaps = []
    for ep in sorted(epochs)[:3]:
        sub = df[df["epoch"] == ep] if "epoch" in df.columns else df
        gr_heatmaps.append(fig_granger_heatmap(sub, ch[:6], title=f"Granger sig — {ep}"))
    gr_sec = section("granger", "GRANGER CAUSALITY", [
        dcc.Graph(figure=gr_bar, config=dict(displayModeBar=False)),
        fig_row(*gr_heatmaps),
    ])

    # -- MACROSTATE --
    ms_result = fig_macrostate_over_time(df)
    if isinstance(ms_result, tuple):
        ms_fig, labels = ms_result
    else:
        ms_fig, labels = ms_result, np.zeros(len(df), dtype=int)
    ms_stat_figs = []
    for ep in sorted(epochs)[:3]:
        mask = (df["epoch"] == ep).values if "epoch" in df.columns else np.ones(len(df), dtype=bool)
        ms_stat_figs.append(fig_macrostate_stationary(df[mask], labels[mask], epoch_name=ep))
    ms_sec = section("macrostate", "MACROSTATE", [
        dcc.Graph(figure=ms_fig, config=dict(displayModeBar=False)),
        fig_row(*ms_stat_figs),
    ])

    # -- MIP / INTEGRATION --
    integ_lin = fig_integration_timeseries(df, ch, window=256, stride=64, log_scale=False)
    integ_log = fig_integration_timeseries(df, ch, window=256, stride=64, log_scale=True)
    mip_sing = fig_mip_singleton_counts(df, ch, window=256, stride=64)
    mip_sec = section("mip", "MIP / INTEGRATION (TC · DTC · O)", [
        fig_row(integ_lin, integ_log),
        dcc.Graph(figure=mip_sing, config=dict(displayModeBar=False)),
    ])

    # -- NETWORK --
    ph_fig = fig_phase_portrait(df)
    lz_fig = fig_lz_complexity_pca(df)
    mem_fig = fig_sie_memory_vs_n(df, status_df)
    # degree distribution from active_edges proxy
    if "active_edges" in df.columns:
        deg_proxy = df["active_edges"].astype(float).dropna().values
        d_ccdf = fig_degree_ccdf(deg_proxy, "Degree Proxy CCDF (active_edges)")
    else:
        d_ccdf = sfig("Degree CCDF — no data", height=360)
    net_sec = section("network", "NETWORK", [
        fig_row(ph_fig, lz_fig),
        fig_row(d_ccdf, mem_fig),
    ])

    # -- PCI --
    pci_ts = fig_pci_like(df, ch)
    pci_ep = fig_pci_by_epoch(df, ch)
    pci_ev = fig_pci_events_vs_controls(df, ch)
    pci_sec = section("pci", "PCI-LIKE  (ΦLZ)", [
        dcc.Graph(figure=pci_ts, config=dict(displayModeBar=False)),
        fig_row(pci_ep, pci_ev),
    ])

    # -- PREDICTIVE MI --
    pmi_fig = fig_predictive_mi(df, ch)
    pmi_sec = section("predictive_mi", "PREDICTIVE MUTUAL INFORMATION", [
        dcc.Graph(figure=pmi_fig, config=dict(displayModeBar=False)),
    ])

    # -- ROLLING --
    ro_figs = []
    for c in ["connectome_entropy","sie_v2_valence_01","active_edges"]:
        ro_figs.append(fig_rolling_autocorr(df, c))
        ro_figs.append(fig_rolling_variance(df, c))
    ro_sec = section("rolling", "ROLLING STATISTICS", [
        fig_row(*ro_figs[:2]),
        fig_row(*ro_figs[2:4]),
        fig_row(*ro_figs[4:]),
    ])

    # -- SPECTRAL --
    sp_bar = fig_spectral_slope(df, ch)
    sp_ent = fig_spectral_fit_scatter(df, "connectome_entropy")
    sp_val = fig_spectral_fit_scatter(df, "sie_v2_valence_01")
    sp_sec = section("spectral", "SPECTRAL", [
        dcc.Graph(figure=sp_bar, config=dict(displayModeBar=False)),
        fig_row(sp_ent, sp_val),
    ])

    # -- TC / O --
    tc_ts = fig_tc_timeseries(df, ch)
    o_ts  = fig_o_information_ts(df, ch)
    tco_sec = section("tc_o", "TOTAL CORRELATION  /  O-INFORMATION", [
        fig_row(tc_ts, o_ts),
    ])

    # -- BIO NEURAL --
    av_fig = fig_avalanche_ccdf(df, "active_edges")
    psd_fig = fig_psd_firing(df, "connectome_entropy")
    fe_fig = fig_free_energy(df)
    ord_fig = fig_order_params(df)
    fish_fig = fig_fisher_speed(df)
    bio_sec = section("bio_neural", "BIOLOGICAL NEURAL  (avalanche · PSD · free energy · Fisher)", [
        fig_row(av_fig, psd_fig),
        fig_row(fe_fig, ord_fig),
        dcc.Graph(figure=fish_fig, config=dict(displayModeBar=False)),
    ])

    # -- SCALE FREE --
    g_fig = fig_gini_metrics(df)
    if "active_edges" in df.columns:
        deg_vals = df["active_edges"].astype(float).dropna().values
        tail_fig = fig_tail_fit_grid(deg_vals, title_prefix="active_edges")
    else:
        tail_fig = sfig("Tail Fit Grid — no degree data", height=500)
    sf_sec = section("scale_free", "SCALE-FREE / HEAVY TAIL", [
        dcc.Graph(figure=g_fig, config=dict(displayModeBar=False)),
        dcc.Graph(figure=tail_fig, config=dict(displayModeBar=False)),
    ])

    # -- REGIMES --
    rg_all = fig_regime_all_ticks(df)
    rg_emis = fig_emission_microstructure(df)
    rg_sec = section("regimes", "REGIMES", [
        fig_row(rg_all, rg_emis),
    ])

    return html.Div([
        overview_sec, cc_sec, ev_sec, gr_sec, ms_sec,
        mip_sec, net_sec, pci_sec, pmi_sec, ro_sec,
        sp_sec, tco_sec, bio_sec, sf_sec, rg_sec,
    ])


# ─────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="VDM Analysis Dashboard")
    ap.add_argument("--port", type=int, default=8051)
    ap.add_argument("--host", type=str, default="0.0.0.0")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()
    print(f"\n  VDM Analysis Dashboard  →  http://localhost:{args.port}\n")
    app.run(host=args.host, port=args.port, debug=args.debug)
