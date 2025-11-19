#!/usr/bin/env python3
"""
Topo-RDM v1 — Topological Ringdown Meter (add-on to DSI-RDM)

Purpose
- Consume time–frequency ridge skeleton points (tau, f) from the DSI ringdown pipeline
- Build a Vietoris–Rips 1-skeleton at radii ε and compute the Euler–rank proxy
  beta1(ε) = E(ε) - V + C(ε)
- Compute z-score B1z_max against a null suite (phase-shuffled skeletons; Kerr-only via imported ridges)
- Enforce gates: G1 (B1z_max ≥ z_gate_primary with FDR q ≤ fdr_q), G3 (null FP ≤ 5%)
- Emit artifacts via canonical io_paths: PNG + CSV + JSON with provenance

Canon anchors (do not duplicate canon content here; link-by-anchor in PROPOSAL/RESULTS):
- DSI proposal: [T2 DSI-RDM](../../../Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md)  # reference only
- Validation metrics: [VALIDATION_METRICS.md](../../../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
- Equations registry: [EQUATIONS.md](../../../z.CANONICAL_Equations/00_EQUATIONS.md)

Inputs
- Ridges CSV (recommended): comma-separated with headers including either:
  ["tau","f"] or ["tau","freq"], or fallback to first two numeric columns.
- OR raw time-series CSV (no external pipeline required): headers ["t","strain"] or ["time","h"]
  from which this runner computes a basic STFT scalogram and extracts ridge points internally.
- Spec JSON: Derivation/code/physics/black_holes/topo_rdm/dsi_topo_rdm.v1.json
  validated against schemas/topo_rdm.schema.json (lightweight runtime checks here)
 
Outputs (io_paths routes with domain="cosmology")
- PNG: panel with ridge scatter and β1(ε) with null bands
- CSV: ε, beta1_obs, beta1_null_mean, beta1_null_std, p, q
- JSON: gate decisions, metrics, seeds, commit hash, environment flags

Notes
- No heavy deps. Numpy and Matplotlib only.
- This runner expects ridge points; DSI integration should export them under a consistent tag.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
from datetime import datetime
# Optional SciPy for QNM fit in DSI branch (fallbacks if unavailable)
try:
    from scipy.optimize import curve_fit  # type: ignore
except Exception:
    curve_fit = None  # type: ignore

# Ensure code root on sys.path (robust to depth)
_THIS = Path(__file__).resolve()
_DERIVATION_DIR = None
for p in _THIS.parents:
    if p.name == "Derivation":
        _DERIVATION_DIR = p
        break
if _DERIVATION_DIR is None:
    # Fallback for non-standard layouts; expected depth is .../Derivation/code/...
    try:
        _DERIVATION_DIR = _THIS.parents[5]
    except Exception:
        _DERIVATION_DIR = _THIS.parent  # best effort

CODE_ROOT = _DERIVATION_DIR  # .../Derivation
CODE_CODE_ROOT = _DERIVATION_DIR / "code"  # .../Derivation/code
if str(CODE_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log  # type: ignore
from common.plotting.topo_rdm_plots import plot_topo_rdm_panel  # type: ignore
from common.instrument_helpers.topo_rdm_timeseries import read_timeseries_csv, ridge_points_from_timeseries, read_timeseries_gwpy  # type: ignore


# ---------- Utilities ----------

def _git_hash() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(CODE_ROOT))
        return out.decode("utf-8").strip()
    except Exception:
        return "unknown"

def _rng(seed: Optional[int]) -> np.random.Generator:
    if seed is None:
        return np.random.default_rng()
    return np.random.default_rng(int(seed))

def _read_json(p: Path) -> Dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def _ensure_points_array(points_like: np.ndarray) -> np.ndarray:
    A = np.asarray(points_like, dtype=float)
    if A.ndim != 2 or A.shape[1] != 2:
        raise ValueError("points must be an array of shape (N,2) with columns [tau, f]")
    return A

def _validate_parameters(params: Dict[str, Any]) -> None:
    # Lightweight checks mirroring schemas/topo_rdm.schema.json (no external jsonschema)
    required_top = ["omega0_ref", "window", "whitener", "taper", "K_QNM", "ridge", "filtration", "nulls", "b1z"]
    for k in required_top:
        if k not in params:
            raise ValueError(f"Missing required parameter: {k}")
    fil = params["filtration"]
    for k in ["radius_min", "radius_max", "num_scales"]:
        if k not in fil:
            raise ValueError(f"Missing filtration.{k}")
    if not (fil["radius_max"] > fil["radius_min"] > 0.0):
        raise ValueError("Require 0 < radius_min < radius_max")
    ns = int(params.get("nulls", {}).get("num_sim", 100))
    if ns < 10:
        raise ValueError("nulls.num_sim must be ≥ 10")

def _linspace(a: float, b: float, n: int) -> np.ndarray:
    return np.linspace(float(a), float(b), int(n), dtype=float)

# ---------- Data ingest ----------

def read_ridges_csv(path: Path) -> np.ndarray:
    """
    Read ridge points from CSV. Accept headers: ['tau','f'] or ['tau','freq'].
    Fallback: first two numeric columns of the file (skipping non-numeric).
    Returns Nx2 array [tau, f].
    """
    tau: List[float] = []
    ff: List[float] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            raise RuntimeError("Empty CSV for ridges")
        # normalize headers
        h = [s.strip().lower() for s in headers]
        idx_tau = None
        idx_f = None
        for i, name in enumerate(h):
            if name in ("tau", "log_time", "ln_theta"):
                idx_tau = i
            if name in ("f", "freq", "frequency"):
                idx_f = i
        for row in reader:
            if not row:
                continue
            try:
                if idx_tau is not None and idx_f is not None:
                    t = float(row[idx_tau])
                    fr = float(row[idx_f])
                else:
                    # fallback: take first two numeric cells
                    nums = []
                    for cell in row:
                        try:
                            nums.append(float(cell))
                        except Exception:
                            continue
                        if len(nums) == 2:
                            break
                    if len(nums) < 2:
                        continue
                    t, fr = nums[0], nums[1]
                if np.isfinite(t) and np.isfinite(fr):
                    tau.append(t)
                    ff.append(fr)
            except Exception:
                continue
    P = np.column_stack([np.asarray(tau, dtype=float), np.asarray(ff, dtype=float)])
    if P.shape[0] < 4:
        raise RuntimeError("Too few ridge points (<4) for topology analysis")
    return P
 
 
# (moved) time-series ingest and ridge extraction live in common.instrument_helpers.topo_rdm_timeseries
# Use: read_timeseries_csv, ridge_points_from_timeseries
# ---------- Graph/PH primitives ----------

class UnionFind:
    __slots__ = ("parent", "rank")

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

def pairwise_distances(X: np.ndarray) -> np.ndarray:
    """Compute Euclidean pairwise distances for Nx2 points. O(N^2)."""
    X = _ensure_points_array(X)
    # (x - y)^2 = x^2 + y^2 - 2 x⋅y
    G = X @ X.T
    sq = np.clip(np.diag(G)[:, None] + np.diag(G)[None, :] - 2.0 * G, a_min=0.0, a_max=None)
    D = np.sqrt(sq, dtype=float)
    return D

def mst_connectivity_radius(D: np.ndarray) -> float:
    """Max edge in a minimum spanning tree (single-linkage connectivity threshold)."""
    n = int(D.shape[0])
    if n <= 1:
        return 0.0
    # Extract upper-triangular edges
    iu, ju = np.triu_indices(n, k=1)
    w = D[iu, ju].astype(float)
    order = np.argsort(w)
    uf = UnionFind(n)
    used = 0
    r_max = 0.0
    for idx in order:
        wij = float(w[idx])
        a = int(iu[idx]); b = int(ju[idx])
        ra, rb = uf.find(a), uf.find(b)
        if ra != rb:
            uf.union(ra, rb)
            used += 1
            if wij > r_max:
                r_max = wij
            if used == n - 1:
                break
    return float(r_max)

def beta1_curve(points: np.ndarray, eps: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute beta1(ε) = E - V + C over a VR-graph filtration on points.
    Returns: beta1 (len eps), E (len eps), C (len eps)
    """
    P = _ensure_points_array(points)
    n = P.shape[0]
    if n < 2:
        return np.zeros_like(eps), np.zeros_like(eps), np.ones_like(eps)
    D = pairwise_distances(P)
    # zero diagonal
    np.fill_diagonal(D, np.inf)
    beta1 = np.zeros_like(eps, dtype=float)
    E_arr = np.zeros_like(eps, dtype=float)
    C_arr = np.zeros_like(eps, dtype=float)
    for k, thr in enumerate(eps):
        # adjacency where dist <= thr
        A = (D <= float(thr))
        # Count edges (undirected)
        E = float(np.count_nonzero(np.triu(A, k=1)))
        # Components via union-find
        uf = UnionFind(n)
        ii, jj = np.where(np.triu(A, k=1))
        for a, b in zip(ii.tolist(), jj.tolist()):
            uf.union(int(a), int(b))
        roots = {uf.find(i) for i in range(n)}
        C = float(len(roots))
        beta1[k] = E - n + C
        E_arr[k] = E
        C_arr[k] = C
    return beta1, E_arr, C_arr


# ---------- Nulls and statistics ----------

def permute_f(points: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Phase-shuffle proxy at skeleton level: preserve tau and f marginals, destroy tau–f correlation."""
    P = _ensure_points_array(points)
    tau = P[:, 0].copy()
    f = P[:, 1].copy()
    rng.shuffle(f)
    return np.column_stack([tau, f])

def null_phase_shuffled_curves(points: np.ndarray, eps: np.ndarray, num_sim: int, seed: Optional[int]) -> np.ndarray:
    """
    Generate null beta1(ε) curves by permuting f across points.
    Returns array shape (num_sim, len(eps)).
    """
    rng = _rng(seed)
    curves = np.zeros((int(num_sim), len(eps)), dtype=float)
    for i in range(int(num_sim)):
        Pn = permute_f(points, rng)
        b1, _, _ = beta1_curve(Pn, eps)
        curves[i, :] = b1
    return curves

def bh_fdr(pvals: np.ndarray, alpha: float) -> Tuple[float, np.ndarray]:
    """
    Benjamini–Hochberg FDR control.
    Returns (threshold_p, mask_reject) where mask indicates q ≤ alpha.
    """
    m = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    thresh = (np.arange(1, m + 1) / float(m)) * float(alpha)
    below = ranked <= thresh
    if not np.any(below):
        return 0.0, np.zeros_like(pvals, dtype=bool)
    k_max = np.max(np.where(below)[0])
    p_thr = ranked[k_max]
    mask = pvals <= p_thr
    return float(p_thr), mask

def pvals_from_null(obs: np.ndarray, null_curves: np.ndarray) -> np.ndarray:
    """
    Empirical one-sided p-values per ε with mid-p correction for ties:
    Let F_n(x-) = Pr(null < x), T_n(x) = Pr(null = x); p = 1 - (F_n + 0.5 T_n).
    Guarantees p ∈ [1/(2K), 1] when all null_j are identical to obs[j] (prevents p=0 artifacts).
    """
    K = int(null_curves.shape[0])
    p = np.ones_like(obs, dtype=float)
    for j in range(len(obs)):
        null_j = null_curves[:, j]
        less = float(np.mean(null_j < obs[j]))
        eq = float(np.mean(null_j == obs[j]))
        pj = 1.0 - (less + 0.5 * eq)
        if not np.isfinite(pj):
            pj = 1.0
        # clip to [1/(2K), 1] for numerical safety
        lo = 1.0 / (2.0 * max(1, K))
        p[j] = float(np.clip(pj, lo, 1.0))
    return p

def zscore_of_max(obs: np.ndarray, null_curves: np.ndarray) -> Tuple[float, float, float]:
    """
    Compute z-score of the maximum beta1 across epsilons against null maxima distribution.
    Returns (z, mean_null_max, std_null_max).
    """
    max_obs = float(np.max(obs))
    null_max = np.max(null_curves, axis=1)
    mu = float(np.mean(null_max))
    sd = float(np.std(null_max, ddof=1)) if null_max.size > 1 else 0.0
    z = (max_obs - mu) / (sd + 1e-12)
    return float(z), mu, (sd if sd > 0 else 0.0)


# ---------- DSI-RDM helpers (log-time comb meter) ----------
def _qnm_model(t: np.ndarray, A: float, alpha: float, f0: float, phi: float, t0: float) -> np.ndarray:
    tt = np.maximum(0.0, np.asarray(t, dtype=float) - float(t0))
    return float(A) * np.exp(-float(alpha) * tt) * np.cos(2.0 * np.pi * float(f0) * tt + float(phi))

def _fit_qnm_damped_sinusoid(t: np.ndarray, h: np.ndarray, t0: float) -> Dict[str, float]:
    # Post-merger window for fit: up to 40% of available span
    t = np.asarray(t, dtype=float)
    h = np.asarray(h, dtype=float)
    span = float(t[-1] - t0)
    if span <= 0:
        return {"A": 0.0, "alpha": 0.0, "f0": 0.0, "phi": 0.0}
    t1 = t0 + 0.4 * span
    mask = (t >= t0) & (t <= t1)
    if not np.any(mask):
        mask = (t >= t0)
    tt = t[mask]
    yy = h[mask]
    if tt.size < 16:
        return {"A": 0.0, "alpha": 0.0, "f0": 0.0, "phi": 0.0}
    # Initial guesses
    A0 = float(np.std(yy)) * 2.0
    # crude FFT based freq guess
    dt = float(np.median(np.diff(tt))) if tt.size > 1 else 1e-3
    if dt <= 0:
        dt = 1e-3
    Y = np.fft.rfft(yy * np.hanning(len(yy)))
    freqs = np.fft.rfftfreq(len(yy), d=dt)
    if freqs.size > 1:
        idx = int(np.argmax(np.abs(Y)[1:])) + 1
        f0_guess = float(freqs[idx])
    else:
        f0_guess = 100.0
    alpha0 = 1.0 / max(1e-3, span)
    phi0 = 0.0
    if curve_fit is None:
        return {"A": 0.0, "alpha": 0.0, "f0": 0.0, "phi": 0.0}
    # Wrap model for curve_fit with fixed t0
    def _model_fit(t_in, A, alpha, f0, phi):
        return _qnm_model(t_in, A, alpha, f0, phi, t0)
    p0 = [A0, alpha0, max(1.0, min(1024.0, f0_guess)), phi0]
    bounds = ([0.0, 0.0, 1.0, -np.pi], [10.0 * max(1e-12, np.std(yy)), 200.0, 2048.0, np.pi])
    try:
        popt, _ = curve_fit(_model_fit, tt, yy, p0=p0, bounds=bounds, maxfev=20000)
        A, alpha, f0, phi = [float(x) for x in popt]
        return {"A": A, "alpha": alpha, "f0": f0, "phi": phi}
    except Exception:
        return {"A": 0.0, "alpha": 0.0, "f0": 0.0, "phi": 0.0}

def _residual_after_qnm(t: np.ndarray, h: np.ndarray, t0: float, params: Dict[str, float]) -> np.ndarray:
    if params.get("f0", 0.0) <= 0.0:
        return np.asarray(h, dtype=float)
    return np.asarray(h, dtype=float) - _qnm_model(t, params["A"], params["alpha"], params["f0"], params["phi"], t0)

def _uniform_tau_grid(t: np.ndarray, x: np.ndarray, t0: float, n_grid: int = 4096) -> Tuple[np.ndarray, np.ndarray]:
    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    dt_ref = float(np.median(np.diff(t))) if t.size > 1 else 1e-3
    # exclude t ≤ t0
    mask = t > (t0 + max(1e-12, 0.5 * dt_ref))
    if not np.any(mask):
        # fallback to last half
        idx = max(1, len(t) // 2)
        mask = np.zeros_like(t, dtype=bool); mask[idx:] = True
        t0 = float(t[idx])
    t_post = t[mask]
    x_post = x[mask]
    tau = np.log((t_post - t0) / max(1e-12, dt_ref))
    tau_min = float(np.min(tau))
    tau_max = float(np.max(tau))
    if not np.isfinite(tau_min) or not np.isfinite(tau_max) or tau_max - tau_min <= 1e-6:
        # trivial
        tau_u = np.linspace(0.0, 1.0, max(16, n_grid))
        x_u = np.interp(tau_u, tau_u, np.zeros_like(tau_u))
        return tau_u, x_u
    tau_u = np.linspace(tau_min, tau_max, int(n_grid))
    # resample x to uniform tau grid via linear interpolation
    x_u = np.interp(tau_u, tau, x_post)
    # apply Hann to reduce leakage
    win = 0.5 - 0.5 * np.cos(2.0 * np.pi * np.arange(len(x_u)) / max(1, len(x_u) - 1))
    return tau_u, x_u * win

def _dsi_periodogram(t: np.ndarray, r: np.ndarray, t0: float, n_grid: int = 4096) -> Tuple[np.ndarray, np.ndarray]:
    tau_u, r_u = _uniform_tau_grid(t, r, t0, n_grid=n_grid)
    d_tau = float(tau_u[1] - tau_u[0]) if len(tau_u) > 1 else 1.0
    R = np.fft.rfft(r_u)
    P = (np.abs(R) ** 2).astype(float)
    f_tau = np.fft.rfftfreq(len(r_u), d=d_tau)
    return f_tau, P

def _find_peaks_simple(P: np.ndarray, min_quantile: float = 0.98, k_max: int = 6) -> List[int]:
    P = np.asarray(P, dtype=float)
    if P.size < 5:
        return []
    thresh = float(np.quantile(P, min_quantile))
    idxs: List[int] = []
    for i in range(1, len(P) - 1):
        if P[i] > P[i - 1] and P[i] > P[i + 1] and P[i] >= thresh and i > 0:
            idxs.append(i)
    # sort by power descending, keep top k_max, skip DC (i==0 already excluded)
    idxs = sorted(idxs, key=lambda i: P[i], reverse=True)[:int(k_max)]
    return sorted(idxs)

def run_dsi(timeseries_csv_path: str, spec: "TopoSpec", t0_hint: Optional[float] = None) -> Dict[str, Any]:
    # Load time-series
    t_arr, h_arr = read_timeseries_csv(Path(timeseries_csv_path))
    # Try to infer t0 from paired meta JSON if available
    t0 = float(t_arr[0])
    if (t0_hint is not None) and np.isfinite(t0_hint):
        t0 = float(t0_hint)
    else:
        # If *_pre.csv, check *_pre.json
        if timeseries_csv_path.endswith("_pre.csv"):
            meta_path = timeseries_csv_path[:-8] + "_pre.json"
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        if "t0" in meta:
                            t0 = float(meta["t0"])
                except Exception:
                    pass
        # fallback: peak absolute as proxy
        try:
            t0 = float(t_arr[int(np.argmax(np.abs(h_arr)))])
        except Exception:
            t0 = float(t_arr[0])
    # QNM fit and residual
    qnm = _fit_qnm_damped_sinusoid(t_arr, h_arr, t0=t0)
    resid = _residual_after_qnm(t_arr, h_arr, t0=t0, params=qnm)
    # DSI spectrum on log-time
    f_tau, P = _dsi_periodogram(t_arr, resid, t0=t0, n_grid=4096)
    # Comb peaks
    peak_idx = _find_peaks_simple(P, min_quantile=0.98, k_max=6)
    f_peaks = [float(f_tau[i]) for i in peak_idx]
    f_peaks_sorted = sorted(f_peaks)
    deltas = np.diff(f_peaks_sorted) if len(f_peaks_sorted) >= 2 else np.asarray([], dtype=float)
    deltaOmega = float(np.mean(deltas)) if deltas.size > 0 else float("nan")
    C = float(1.0 - (np.std(deltas) / (np.mean(deltas) + 1e-12))) if deltas.size >= 1 else 0.0
    # Gate (within-run comb coherence proxy)
    G1 = bool((len(f_peaks_sorted) >= 3) and (C >= 0.60))
    # Artifacts
    domain = "cosmology"
    slug_base = f"dsi_rdm_v1__{spec.tag}"
    # Figure
    fig, ax = plt.subplots(2, 1, figsize=(8.0, 5.0), dpi=160, constrained_layout=True)
    # Panel 1: time series with QNM fit
    ax[0].plot(t_arr, h_arr, lw=0.8, color="#1f77b4", label="whitened+bandpassed")
    if qnm.get("f0", 0.0) > 0.0:
        ax[0].plot(t_arr, _qnm_model(t_arr, qnm["A"], qnm["alpha"], qnm["f0"], qnm["phi"], t0), lw=1.0, color="#d62728", label="QNM fit")
    ax[0].axvline(t0, color="k", ls="--", lw=0.8, alpha=0.7)
    ax[0].set_title("Ringdown (preprocessed) and QNM baseline")
    ax[0].set_xlabel("t [s]"); ax[0].set_ylabel("h (arb.)"); ax[0].legend(loc="upper right", fontsize=8)
    # Panel 2: log-time spectrum
    ax[1].plot(f_tau, P, lw=0.9, color="#2ca02c", label="P(Ω) in log-time")
    if f_peaks_sorted:
        ax[1].scatter(f_peaks_sorted, [P[np.argmin(np.abs(f_tau - fp))] for fp in f_peaks_sorted], color="#ff7f0e", s=14, zorder=5, label="peaks")
    ax[1].set_xlim(left=0.0)
    ax[1].set_xlabel("Ω (log-time frequency)"); ax[1].set_ylabel("Power")
    caption = f"Comb metric: C={C:.3f}; N_peaks={len(f_peaks_sorted)}; ΔΩ≈{(deltaOmega if np.isfinite(deltaOmega) else float('nan')):.4g}"
    ax[1].set_title(caption)
    figp = figure_path(domain, slug_base)
    fig.savefig(figp, dpi=160)
    plt.close(fig)
    # CSV spectrum
    csvp = log_path(domain, f"{slug_base}__spectrum", failed=not G1, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("f_tau,P\n")
        for ft, pv in zip(f_tau, P):
            f.write(f"{float(ft):.10g},{float(pv):.10g}\n")
    # JSON summary
    summary = {
        "instrument": "DSI-RDM v1 (log-time comb meter)",
        "timestamp": datetime.now().isoformat(),
        "tag": spec.tag,
        "git_hash": _git_hash(),
        "params": spec.parameters,
        "metrics": {
            "comb_coherence_C": float(C),
            "N_peaks": int(len(f_peaks_sorted)),
            "deltaOmega": (None if not np.isfinite(deltaOmega) else float(deltaOmega)),
            "f_tau_peaks": f_peaks_sorted,
            "t0_used": float(t0),
            "qnm_fit": qnm,
        },
        "gates": {
            "G1_comb_coherence": bool(G1),
            "overall_pass": bool(G1),
        },
        "artifacts": {
            "figure": str(figp),
            "csv_spectrum": str(csvp),
        },
    }
    jsonp = log_path(domain, f"{slug_base}__summary", failed=not G1, type="json")
    write_log(jsonp, summary)
    return summary

# ---------- Runner core ----------

@dataclass
class TopoSpec:
    parameters: Dict[str, Any]
    seeds: List[int]
    tag: str
    data: Optional[Dict[str, Any]] = None

def load_spec(spec_path: Optional[Path]) -> TopoSpec:
    if spec_path is None:
        # Minimal defaults if no spec passed (for ad-hoc testing)
        params = {
            "omega0_ref": "qnm220",
            "window": [0.0, 8.0],
            "whitener": "median-psd",
            "taper": "planck",
            "K_QNM": 3,
            "ridge": {"k_neighbors": 2, "max_gap": 2, "phase_coherence_min": 0.6},
            # Use quantile-bounded filtration by default to avoid complete-graph degeneracy of β1 max
            "filtration": {
                "kind": "vrips",
                "num_scales": 64,
                "radius_min": 0.01,
                "radius_max": 0.5,
                "use_quantile_bounds": True,
                "qmin": 0.05,
                "qmax": 0.60
            },
            "nulls": {"kerr_only": False, "phase_shuffled": True, "num_sim": 200},
            "b1z": {"fdr_q": 0.01, "z_gate_primary": 5.0, "z_gate_null": 3.0},
        }
        seeds = [1]
        tag = "dsi-topo-rdm-v1"
        data_field: Optional[Dict[str, Any]] = {"ridges_csv": None}
        return TopoSpec(parameters=params, seeds=seeds, tag=tag, data=data_field)
    data_json = _read_json(spec_path)
    params = data_json.get("parameters", {})
    _validate_parameters(params)
    seeds = data_json.get("seeds", [1])
    if isinstance(seeds, int):
        seeds = [int(seeds)]
    tag = str(data_json.get("tag", "dsi-topo-rdm-v1"))
    data_field = data_json.get("data", None)
    return TopoSpec(parameters=params, seeds=[int(s) for s in seeds], tag=tag, data=data_field)

def longest_true_run(mask: np.ndarray) -> int:
    m = 0
    cur = 0
    for v in mask:
        if v:
            cur += 1
            m = max(m, cur)
        else:
            cur = 0
    return m

def run_topo(points: np.ndarray, spec: TopoSpec, seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Main analysis: compute beta1 curve and statistics against nulls. Emit artifacts.
    """
    params = spec.parameters
    fil = params["filtration"]
    num_scales = int(fil.get("num_scales", 64))

    # Baseline bounds
    rmin = float(fil.get("radius_min", 0.01))
    rmax = float(fil.get("radius_max", 0.5))

    # Robust per-dimension scaling of [tau, f] into [0,1] to set a dimensionless geometry for ε
    Praw = _ensure_points_array(points)
    tau_raw = Praw[:, 0].astype(float)
    f_raw = Praw[:, 1].astype(float)
    # Percentile bounds (robust to outliers)
    try:
        lo_tau, hi_tau = np.percentile(tau_raw, [1.0, 99.0])
        lo_f, hi_f = np.percentile(f_raw, [1.0, 99.0])
    except Exception:
        lo_tau, hi_tau = float(np.min(tau_raw)), float(np.max(tau_raw))
        lo_f, hi_f = float(np.min(f_raw)), float(np.max(f_raw))
    # Avoid zero-width
    if not np.isfinite(hi_tau - lo_tau) or (hi_tau - lo_tau) <= 1e-9:
        hi_tau = lo_tau + 1.0
    if not np.isfinite(hi_f - lo_f) or (hi_f - lo_f) <= 1e-9:
        hi_f = lo_f + 1.0
    tau_s = np.clip((tau_raw - lo_tau) / (hi_tau - lo_tau), 0.0, 1.0)
    f_s = np.clip((f_raw - lo_f) / (hi_f - lo_f), 0.0, 1.0)
    points_s = np.column_stack([tau_s, f_s])

    # Pairwise distances (once) for adaptive bounds
    try:
        D_local = pairwise_distances(points_s)
        dvec = D_local[np.isfinite(D_local)].ravel()
        dvec = dvec[dvec > 0]
    except Exception:
        D_local = None
        dvec = np.asarray([], dtype=float)

    # Optional quantile-bounded filtration to avoid complete-graph degeneracy
    if bool(fil.get("use_quantile_bounds", False)) and dvec.size > 0:
        qmin = float(fil.get("qmin", 0.05))
        qmax = float(fil.get("qmax", 0.60))
        qmin = max(0.0, min(1.0, qmin))
        qmax = max(qmin + 1e-6, min(1.0, qmax))
        rmin = float(np.quantile(dvec, qmin))
        rmax = float(np.quantile(dvec, qmax))

    # Connectivity cap: keep rmax below the single-linkage connectivity threshold
    if D_local is not None:
        try:
            r_conn = mst_connectivity_radius(D_local)
        except Exception:
            r_conn = None
        cap_on = bool(fil.get("connectivity_cap", True))
        cap_pct = float(fil.get("cap_pct", 0.95))
        if cap_on and (r_conn is not None) and np.isfinite(r_conn) and (r_conn > 0):
            rmax = min(rmax, float(cap_pct) * float(r_conn))

    # Safety clamps for monotone bounds
    if not (np.isfinite(rmin) and np.isfinite(rmax)) or (rmin <= 0.0) or (rmax <= rmin):
        rmin = float(fil.get("radius_min", 0.01))
        rmax = float(fil.get("radius_max", 0.5))

    eps = _linspace(rmin, rmax, num_scales)

    # Observed curve
    b1_obs, E_obs, C_obs = beta1_curve(points_s, eps)

    # Phase-shuffled nulls
    null_cfg = params.get("nulls", {})
    do_phase = bool(null_cfg.get("phase_shuffled", True))
    num_sim = int(null_cfg.get("num_sim", 200))
    null_curves = np.empty((0, len(eps)), dtype=float)
    if do_phase:
        null_curves = null_phase_shuffled_curves(points_s, eps, num_sim=num_sim, seed=seed)
    # Kerr-only ridges (Null-A) provided as CSVs
    kerr_paths = null_cfg.get("kerr_only_ridges", [])
    if kerr_paths:
        curves_kerr = []
        for rp in kerr_paths:
            try:
                Pk = read_ridges_csv(Path(rp))
                b1k, _, _ = beta1_curve(Pk, eps)
                curves_kerr.append(b1k)
            except Exception:
                continue
        if len(curves_kerr) > 0:
            kerr_arr = np.vstack(curves_kerr).astype(float)
            null_curves = kerr_arr if null_curves.size == 0 else np.vstack([null_curves, kerr_arr])

    # Per-ε p-values and FDR q mask (use BH on p)
    if null_curves.shape[0] > 0:
        pvals = pvals_from_null(b1_obs, null_curves)
        p_thr, q_mask = bh_fdr(pvals, alpha=float(params["b1z"]["fdr_q"]))
    else:
        pvals = np.ones_like(b1_obs)
        p_thr, q_mask = 0.0, np.zeros_like(b1_obs, dtype=bool)

    # Z-score of max over ε using per-ε standardization (aligns with G1)
    if null_curves.shape[0] > 0:
        mu_per_eps_mx = np.mean(null_curves, axis=0)
        sd_per_eps_mx = np.std(null_curves, axis=0, ddof=1)
        z_per_eps_for_max = (b1_obs - mu_per_eps_mx) / (sd_per_eps_mx + 1e-12)
        z_max = float(np.max(z_per_eps_for_max))
        # Null maxima distribution in standardized units
        z_null_mx = (null_curves - mu_per_eps_mx[None, :]) / (sd_per_eps_mx[None, :] + 1e-12)
        z_null_max = np.max(z_null_mx, axis=1)
        mu_null_max = float(np.mean(z_null_max))
        sd_null_max = float(np.std(z_null_max, ddof=1)) if z_null_max.size > 1 else 0.0
    else:
        # No nulls: cannot compute z; set to 0
        z_max, mu_null_max, sd_null_max = 0.0, 0.0, 0.0

    # Gate G1: B1z_max ≥ z_gate_primary at any ε that survives FDR (require a small stable band: ≥2 consecutive)
    z_gate = float(params["b1z"]["z_gate_primary"])
    # For a rough per-ε z, compare to per-ε null μ/σ (fallback to overall if degenerate)
    if null_curves.shape[0] > 0:
        mu_per_eps = np.mean(null_curves, axis=0)
        sd_per_eps = np.std(null_curves, axis=0, ddof=1)
        z_per_eps = (b1_obs - mu_per_eps) / (sd_per_eps + 1e-12)
    else:
        z_per_eps = np.zeros_like(b1_obs)
    stable_mask = q_mask & (z_per_eps >= z_gate)
    stable_band_len = longest_true_run(stable_mask)
    G1 = bool((z_max >= z_gate) and (stable_band_len >= 2))

    # Gate G3: Null control — FP rate ≤ 0.05 based on null maxima exceeding muN + z_gate_null * sdN
    z_gate_null = float(params["b1z"]["z_gate_null"])
    if null_curves.shape[0] > 0:
        # Evaluate FP using raw null maxima distribution of beta1(ε)
        null_max = np.max(null_curves, axis=1)
        muN = float(np.mean(null_max))
        sdN = float(np.std(null_max, ddof=1)) if null_max.size > 1 else 0.0
        if sdN <= 0:
            fp_rate = 0.0
        else:
            thresh = muN + z_gate_null * sdN
            fp_rate = float(np.mean(null_max >= thresh))
    else:
        fp_rate = 1.0  # cannot verify → fail conservatively
    G3 = bool(fp_rate <= 0.05)

    # Gate G2: alignment with DSI comb spacing (optional alignment parameters)
    # Determine per-ε z peak location
    idx_peak = int(np.argmax(z_per_eps)) if z_per_eps.size > 0 else 0
    eps_at_peak = float(eps[idx_peak]) if len(eps) > 0 else None
    align_cfg = params.get("alignment", {})
    eps_target = None
    align_tol_pct = float(align_cfg.get("tol_pct", 5.0))
    require_align = bool(align_cfg.get("require_dsi_alignment", True))
    if "eps_target" in align_cfg:
        try:
            eps_target = float(align_cfg["eps_target"])
        except Exception:
            eps_target = None
    elif ("deltaOmega" in align_cfg) and ("eps_scale" in align_cfg):
        try:
            eps_target = float(align_cfg["deltaOmega"]) * float(align_cfg["eps_scale"])
        except Exception:
            eps_target = None
    if (eps_target is not None) and (eps_target > 0):
        align_delta_pct = abs(eps_at_peak - eps_target) / eps_target * 100.0
        G2 = bool(align_delta_pct <= align_tol_pct)
    else:
        align_delta_pct = None
        G2 = False
    # Alignment acceptance for overall pass
    alignment_ok = (not require_align) or (eps_target is None) or bool(G2)

    # Overall decision for artifact routing (fail if G1 or G3 fail)
    failed = not (G1 and G3)

    # ---------- Artifacts ----------
    domain = "cosmology"
    slug_base = f"topo_rdm_v1__{spec.tag}"
    # Use canonical plotting helper
    figp = plot_topo_rdm_panel(
        points=points,
        eps=eps,
        b1_obs=b1_obs,
        null_curves=(null_curves if null_curves.shape[0] > 0 else None),
        q_mask=q_mask,
        z_max=float(z_max),
        stable_band_len=int(stable_band_len),
        fp_rate=float(fp_rate),
        domain=domain,
        slug=slug_base,
        failed=failed,
    )

    # CSV: per-ε table
    csvp = log_path(domain, f"{slug_base}__betti_curve", failed=failed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("epsilon,beta1_obs,beta1_null_mean,beta1_null_std,p,q_mask\n")
        if null_curves.shape[0] > 0:
            mu = np.mean(null_curves, axis=0)
            sd = np.std(null_curves, axis=0, ddof=1)
        else:
            mu = np.zeros_like(b1_obs)
            sd = np.zeros_like(b1_obs)
        for e, b, m, s, p, q in zip(eps, b1_obs, mu, sd, (pvals if null_curves.shape[0] > 0 else np.ones_like(b1_obs)), q_mask):
            f.write(f"{e:.10g},{b:.10g},{m:.10g},{s:.10g},{float(p):.10g},{int(bool(q))}\n")

    # JSON: summary + gates + provenance
    require_approval = os.getenv("VDM_REQUIRE_APPROVAL", "1") == "1"
    approved_env = os.getenv("VDM_POLICY_APPROVED")
    approved = (approved_env == "1") if require_approval else (approved_env != "0")
    hard_block = os.getenv("VDM_POLICY_HARD_BLOCK", "0") == "1"
    env_info = {
        "python": platform.python_version(),
        "python_impl": platform.python_implementation(),
        "numpy": np.__version__,
        "matplotlib": mpl.__version__,
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "node": platform.node(),
    }

    summary = {
        "instrument": "Topological Ringdown Meter (Topo-RDM) v1",
        "timestamp": datetime.now().isoformat(),
        "tag": spec.tag,
        "git_hash": _git_hash(),
        "params": params,
        "seeds": list(spec.seeds),
        "seed_used": (None if seed is None else int(seed)),
        "policy": {
            "require_approval": bool(require_approval),
            "approved_env": (None if approved_env is None else str(approved_env)),
            "approved": bool(approved),
            "hard_block": bool(hard_block),
            "routed_failed": bool(failed),
        },
        "environment": env_info,
        "metrics": {
            "z_max": float(z_max),
            "mu_null_max": float(mu_null_max),
            "sd_null_max": float(sd_null_max),
            "stable_band_len": int(stable_band_len),
            "fp_rate": float(fp_rate),
            "p_threshold_bh": float(p_thr),
            "eps_at_peak": (None if eps_at_peak is None else float(eps_at_peak)),
            "eps_target": (None if eps_target is None else float(eps_target)),
            "align_delta_pct": (None if eps_target is None else float(align_delta_pct))
        },
        "gates": {
            "G1_topo_signal": bool(G1),
            "G2_dsi_alignment": bool(G2),
            "G3_null_control": bool(G3),
            "align_tol_pct": (None if eps_target is None else float(align_tol_pct)),
            "overall_pass": bool(G1 and G3 and alignment_ok),
        },
        "artifacts": {
            "figure": str(figp),
            "csv_betti": str(csvp),
        },
    }
    jsonp = log_path(domain, f"{slug_base}__summary", failed=failed, type="json")
    write_log(jsonp, summary)

    # Contradiction report on fail
    if failed:
        contra = {
            "gate": "Topo-RDM",
            "failed": {"G1": (not G1), "G3": (not G3)},
            "metrics": summary["metrics"],
            "artifacts": summary["artifacts"],
            "reason": "Topo gates not satisfied (see failed booleans).",
        }
        write_log(log_path(domain, f"CONTRADICTION_REPORT__{slug_base}", failed=True, type="json"), contra)

    return summary


# ---------- CLI ----------

def main() -> None:
    p = argparse.ArgumentParser(description="Topo-RDM v1: Topological Ringdown Meter")
    p.add_argument("--spec", type=str, default="", help="Path to dsi_topo_rdm.v1.json (optional)")
    p.add_argument("--mode", type=str, default="topo", choices=["topo", "dsi_only"], help="Analysis branch: 'topo' (β1) or 'dsi_only' (log-time comb)")
    p.add_argument(
        "--ridges_csv",
        type=str,
        default="",
        help="CSV of ridge points with columns [tau,f] or [tau,freq] (optional if provided in spec.data.ridges_csv)",
    )
    p.add_argument(
        "--timeseries_csv",
        type=str,
        default="",
        help="CSV of raw time-series with columns [t,strain] or [time,h] (no external pipeline required)",
    )
    p.add_argument("--t0", type=float, default=float("nan"), help="Reference time for post-merger (dsi_only mode). If NaN, infer from *_pre.json when available.")
    # Optional GWPy ingestion (network fetch from GWOSC or configured data source)
    p.add_argument("--gwpy_channel", type=str, default="", help='GWPy channel, e.g. "H1:GWOSC-4KHZ_R1_STRAIN"')
    p.add_argument("--gwpy_start", type=str, default="", help="GWPy start time (GPS seconds or ISO8601)")
    p.add_argument("--gwpy_end", type=str, default="", help="GWPy end time (GPS seconds or ISO8601)")
    p.add_argument("--tag", type=str, default="", help="Optional tag suffix for artifact slugs")
    p.add_argument("--seed", type=int, default=1, help="Seed for null generation")
    args = p.parse_args()
 
    spec = load_spec(Path(args.spec)) if args.spec else load_spec(None)
    if args.tag:
        spec.tag = f"{spec.tag}__{args.tag}"

    ridges_path = args.ridges_csv.strip()
    if not ridges_path:
        ridges_path = str(spec.data.get("ridges_csv", "")).strip() if getattr(spec, "data", None) else ""
    timeseries_path = args.timeseries_csv.strip()
    if not timeseries_path and getattr(spec, "data", None):
        timeseries_path = str(spec.data.get("timeseries_csv", "")).strip() if getattr(spec, "data", None) else ""

    # Optional GWPy parameters (CLI takes precedence; else check spec.data.gwpy)
    gwpy_channel = args.gwpy_channel.strip()
    gwpy_start = args.gwpy_start.strip()
    gwpy_end = args.gwpy_end.strip()
    if (not ridges_path) and (not timeseries_path) and getattr(spec, "data", None):
        gw_cfg = spec.data.get("gwpy", {}) if getattr(spec, "data", None) else {}
        if gw_cfg and not gwpy_channel:
            gwpy_channel = str(gw_cfg.get("channel", "")).strip()
            gwpy_start = str(gw_cfg.get("start", "")).strip()
            gwpy_end = str(gw_cfg.get("end", "")).strip()

    if ridges_path:
        points = read_ridges_csv(Path(ridges_path))
    elif timeseries_path:
        # Build ridge skeleton internally from raw time-series (CSV)
        t_arr, h_arr = read_timeseries_csv(Path(timeseries_path))
        points = ridge_points_from_timeseries(t_arr, h_arr, spec.parameters)
        # Save the derived ridge points for provenance
        domain = "cosmology"
        slug_base = f"topo_rdm_v1__{spec.tag}"
        ridges_out = log_path(domain, f"{slug_base}__ridges", failed=False, type="csv")
        with ridges_out.open("w", encoding="utf-8") as f:
            f.write("tau,f\n")
            for (tau_i, f_i) in points:
                f.write(f"{float(tau_i):.10g},{float(f_i):.10g}\n")
    elif gwpy_channel and gwpy_start and gwpy_end:
        # Build ridge skeleton by fetching from GWPy
        t_arr, h_arr = read_timeseries_gwpy(gwpy_channel, gwpy_start, gwpy_end)
        points = ridge_points_from_timeseries(t_arr, h_arr, spec.parameters)
        # Save the derived ridge points for provenance
        domain = "cosmology"
        slug_base = f"topo_rdm_v1__{spec.tag}"
        ridges_out = log_path(domain, f"{slug_base}__ridges", failed=False, type="csv")
        with ridges_out.open("w", encoding="utf-8") as f:
            f.write("tau,f\n")
            for (tau_i, f_i) in points:
                f.write(f"{float(tau_i):.10g},{float(f_i):.10g}\n")
    else:
        raise SystemExit("Provide --ridges_csv or --timeseries_csv or --gwpy_channel/--gwpy_start/--gwpy_end (or corresponding spec.data.* entries)")
 
    if args.mode.strip().lower() == "dsi_only":
        if not timeseries_path:
            raise SystemExit("dsi_only mode requires --timeseries_csv or spec.data.timeseries_csv (preprocessed CSV with header 't,h').")
        out = run_dsi(timeseries_path, spec, t0_hint=(None if not np.isfinite(args.t0) else float(args.t0)))
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        out = run_topo(points, spec, seed=int(args.seed))
        print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()