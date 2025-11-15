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
from common.instrument_helpers.topo_rdm_timeseries import read_timeseries_csv, ridge_points_from_timeseries  # type: ignore


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
    Empirical one-sided p-values per ε: p = 1 - ECDF(B1_null <= B1_obs).
    """
    K = null_curves.shape[0]
    p = np.ones_like(obs, dtype=float)
    for j in range(len(obs)):
        null_j = null_curves[:, j]
        # fraction of null ≤ observed
        ecdf = np.mean(null_j <= obs[j])
        p[j] = 1.0 - ecdf
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
    # Optionally cap filtration by pairwise-distance quantiles to avoid complete-graph degeneracy
    rmin = float(fil.get("radius_min", 0.01))
    rmax = float(fil.get("radius_max", 0.5))
    if bool(fil.get("use_quantile_bounds", False)):
        try:
            D_local = pairwise_distances(points)
            dvec = D_local[np.isfinite(D_local)].ravel()
            dvec = dvec[dvec > 0]
            if dvec.size > 0:
                qmin = float(fil.get("qmin", 0.05))
                qmax = float(fil.get("qmax", 0.60))
                # clamp and ensure qmax > qmin
                qmin = max(0.0, min(1.0, qmin))
                qmax = max(qmin + 1e-6, min(1.0, qmax))
                rmin = float(np.quantile(dvec, qmin))
                rmax = float(np.quantile(dvec, qmax))
        except Exception:
            # fall back to explicit radii if quantile computation fails
            pass
    # safety: ensure sane monotone bounds
    if not (np.isfinite(rmin) and np.isfinite(rmax)) or (rmin <= 0.0) or (rmax <= rmin):
        rmin = float(fil.get("radius_min", 0.01))
        rmax = float(fil.get("radius_max", 0.5))
    eps = _linspace(rmin, rmax, num_scales)
    # Observed curve
    b1_obs, E_obs, C_obs = beta1_curve(points, eps)

    # Phase-shuffled nulls
    null_cfg = params.get("nulls", {})
    do_phase = bool(null_cfg.get("phase_shuffled", True))
    num_sim = int(null_cfg.get("num_sim", 200))
    null_curves = np.empty((0, len(eps)), dtype=float)
    if do_phase:
        null_curves = null_phase_shuffled_curves(points, eps, num_sim=num_sim, seed=seed)
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

    # Z-score of max against null maxima
    if null_curves.shape[0] > 0:
        z_max, mu_null_max, sd_null_max = zscore_of_max(b1_obs, null_curves)
    else:
        # No nulls: cannot compute z; set to 0
        z_max, mu_null_max, sd_null_max = 0.0, float(np.max(b1_obs)), 0.0

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

    # Gate G3: Null control — FP rate ≤ 0.05 based on null maxima exceeding z_gate_null
    z_gate_null = float(params["b1z"]["z_gate_null"])
    if null_curves.shape[0] > 0:
        # Evaluate z vs null maxima distribution (compute null z under leave-one-out? pragmatic: use μ/σ of null maxima once)
        null_max = np.max(null_curves, axis=1)
        muN = float(np.mean(null_max))
        sdN = float(np.std(null_max, ddof=1)) if null_max.size > 1 else 0.0
        if sdN <= 0:
            fp_rate = 0.0
        else:
            # Equivalent FP rate: fraction exceeding muN + z_gate_null * sdN
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

    # JSON: summary + gates
    summary = {
        "instrument": "Topological Ringdown Meter (Topo-RDM) v1",
        "tag": spec.tag,
        "git_hash": _git_hash(),
        "params": params,
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
            "overall_pass": bool(G1 and G3 and (G2 or eps_target is None)),
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
 
    if ridges_path:
        points = read_ridges_csv(Path(ridges_path))
    elif timeseries_path:
        # Build ridge skeleton internally from raw time-series
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
    else:
        raise SystemExit("Provide --ridges_csv or --timeseries_csv (or spec.data.ridges_csv/spec.data.timeseries_csv)")
 
    out = run_topo(points, spec, seed=int(args.seed))
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()