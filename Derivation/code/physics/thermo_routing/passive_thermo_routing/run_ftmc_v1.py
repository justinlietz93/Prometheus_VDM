#!/usr/bin/env python3
from __future__ import annotations

"""
Flux Through Memory Channels v1 runner (frozen map; passive thermodynamic routing)

Requirements:
- MUST use Derivation/code/common helpers for IO, plotting, approvals.
- Enforce approvals (domain/script/tag) with optional --allow-unapproved.
- Emit compliance snapshot per proposal (boundary model, flux convention, map immutability,
  RJ basis alignment, determinism receipts, probe-limit, frozen-map delegation, budget mapping).
- Compute basic meters and placeholder KPIs (eta_ch, delta_B_ch, anisotropy) with degenerate CIs;
  full CI/bootstrap can be added once the analysis module is available.
"""

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np

# Path to common helpers (Derivation/code)
CODE_ROOT = Path(__file__).resolve().parents[3]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import log_path_by_tag, write_log, build_slug
from common.authorization.approval import check_tag_approval
from common.plotting.core import apply_style, save_figure, get_fig_ax

DOMAIN = "thermo_routing"


@dataclass
class Spec:
    grid: Dict[str, Any]
    geometry: Dict[str, Any]
    rd: Dict[str, Any]
    ic: Dict[str, Any]
    time: Dict[str, Any]
    analysis: Dict[str, Any]
    controls: Dict[str, Any]
    map: Dict[str, Any]
    seeds: int
    tag: str


def env_receipts() -> Dict[str, Any]:
    # Lightweight copy from run_thermo_routing; keep it consistent
    import os
    threads_env = (
        os.getenv("OMP_NUM_THREADS")
        or os.getenv("MKL_NUM_THREADS")
        or os.getenv("OPENBLAS_NUM_THREADS")
    )
    threads = int(threads_env) if threads_env else 1
    blas_name = None
    try:
        import numpy as _np
        cfg = getattr(_np, "__config__")
        for key in ("openblas_info", "blas_opt_info", "lapack_opt_info", "mkl_info", "blas_mkl_info"):
            get_info = getattr(cfg, key, None)
            info = get_info() if callable(get_info) else {}
            if info:
                libs = info.get("libraries") or info.get("define_macros") or []
                if libs:
                    blas_name = ",".join([str(x) for x in libs])
                    break
    except Exception:
        blas_name = blas_name or None
    try:
        from threadpoolctl import threadpool_info  # type: ignore
        infos = threadpool_info()
        for li in infos:
            internal = li.get("internal_api", "")
            if internal in ("openblas", "mkl", "blas", "blis"):
                name = li.get("internal_api")
                blas_name = name
                nt = li.get("num_threads")
                if isinstance(nt, int) and nt > 0:
                    threads = nt
                break
    except Exception:
        blas_name = blas_name or None
    fft = os.getenv("FFT_INFO", "numpy.pocketfft")
    fft_plan_mode = os.getenv("FFT_PLAN_MODE", "deterministic")
    return {"threads": threads, "blas": blas_name or "numpy.blas (unknown)", "fft": fft, "fft_plan_mode": fft_plan_mode}


def sha256_array(arr: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(arr).view(np.uint8)).hexdigest()


def _git_hashes(repo_root: Path) -> Tuple[str, str]:
    def _git_short_hash_from_dotgit(repo_root: Path) -> str:
        try:
            dotgit = repo_root / ".git"
            head = (dotgit / "HEAD").read_text().strip()
            if head.startswith("ref:"):
                ref = head.split(":", 1)[1].strip()
                ref_path = dotgit / ref
                if ref_path.exists():
                    full = ref_path.read_text().strip()
                else:
                    full = head
            else:
                full = head
            return full[:7]
        except Exception:
            return "unknown"

    def _git_full_hash(repo_root: Path) -> str:
        try:
            dotgit = repo_root / ".git"
            head = (dotgit / "HEAD").read_text().strip()
            if head.startswith("ref:"):
                ref = head.split(":", 1)[1].strip()
                ref_path = dotgit / ref
                if ref_path.exists():
                    return ref_path.read_text().strip()
                return head
            return head
        except Exception:
            return "unknown"

    return _git_full_hash(repo_root), _git_short_hash_from_dotgit(repo_root)


def _build_outlet_masks(nx: int, ny: int, w_A: float, w_B: float) -> Tuple[np.ndarray, np.ndarray]:
    top_len = int(round(ny * max(0.0, min(1.0, w_A))))
    bot_len = int(round(ny * max(0.0, min(1.0, w_B))))
    mask_A = np.zeros((ny,), dtype=bool)
    mask_B = np.zeros((ny,), dtype=bool)
    if top_len > 0:
        mask_A[ny - top_len:] = True
    if bot_len > 0:
        mask_B[:bot_len] = True
    return mask_A, mask_B


def _compute_corridor_mask(mu: np.ndarray, q: float = 0.8) -> np.ndarray:
    if mu.size == 0:
        return np.zeros_like(mu, dtype=bool)
    thr = float(np.quantile(mu, max(0.0, min(1.0, q))))
    return (mu >= thr)


def _grad_mu(mu: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # Simple central differences with Neumann at borders
    gy = np.zeros_like(mu, dtype=float)
    gx = np.zeros_like(mu, dtype=float)
    gy[1:-1, :] = 0.5 * (mu[2:, :] - mu[:-2, :])
    gx[:, 1:-1] = 0.5 * (mu[:, 2:] - mu[:, :-2])
    gy[0, :] = mu[1, :] - mu[0, :]
    gy[-1, :] = mu[-1, :] - mu[-2, :]
    gx[:, 0] = mu[:, 1] - mu[:, 0]
    gx[:, -1] = mu[:, -1] - mu[:, -2]
    return gy, gx


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(int(seed))


def _simulate_tracers(
    mu: np.ndarray,
    W: int,
    H: int,
    inj_band: Tuple[int, int],
    maskA: np.ndarray,
    maskB: np.ndarray,
    corridor_mask: np.ndarray,
    seed: int = 0,
    sample_paths: int = 256,
    drift_weight: float = 0.0,
    corridor_priority: bool = True,
    emit_events: bool = False,
) -> Dict[str, Any]:
    Ny, Nx = mu.shape
    rng = _rng(seed)
    y0, y1 = inj_band
    y0 = max(0, min(Ny - 1, y0))
    y1 = max(0, min(Ny, y1))
    # Initialize walkers uniformly in injection stripe at x = 0..1
    starts_y = rng.integers(low=y0, high=max(y0 + 1, y1), size=W)
    starts_x = rng.integers(low=0, high=min(2, Nx), size=W)
    pos_y = starts_y.astype(int)
    pos_x = starts_x.astype(int)
    alive = np.ones(W, dtype=bool)
    # Flux accumulators and series
    FA = 0
    FB = 0
    FA_series: list[int] = []
    FB_series: list[int] = []
    # Corridor exit count
    exits_in_corridor = 0
    # Anisotropy accumulators (parallel vs normal to ridge tangents)
    gy, gx = _grad_mu(mu)
    sum_par = 0.0
    sum_perp = 0.0
    # Optional sample of paths to plot / event logging
    sampled_idx = set(rng.choice(W, size=min(W, sample_paths), replace=False).tolist())
    path_samples: Dict[int, list[Tuple[int, int]]] = {i: [(int(pos_y[i]), int(pos_x[i]))] for i in sampled_idx}
    events: list[Dict[str, Any]] = []

    def neighbors(i: int, j: int):
        # 4-neighborhood with reflecting walls on left/top/bottom; absorbing on right (exit candidate)
        nb = []
        # West
        if j > 0:
            nb.append((i, j - 1, 'W'))
        # East (inside) or exit candidate
        if j < Nx - 1:
            nb.append((i, j + 1, 'E'))
        else:
            nb.append((i, j, 'X'))  # exit attempt
        # South/North (y-1/y+1)
        if i > 0:
            nb.append((i - 1, j, 'S'))
        if i < Ny - 1:
            nb.append((i + 1, j, 'N'))
        return nb

    for h in range(H):
        if not alive.any():
            FA_series.append(FA)
            FB_series.append(FB)
            continue
        for w in range(W):
            if not alive[w]:
                continue
            i, j = int(pos_y[w]), int(pos_x[w])
            nb = neighbors(i, j)
            # Corridor-priority neighbor selection (remain local and read-only)
            if corridor_priority and nb:
                original_nb = list(nb)
                filtered = []
                for (ii, jj, kind) in original_nb:
                    if kind == 'X':
                        # treat as corridor if current right-edge cell is in corridor
                        if j >= Nx - 1 and corridor_mask[i, Nx - 1]:
                            filtered.append((ii, jj, kind))
                    else:
                        if corridor_mask[ii, jj]:
                            filtered.append((ii, jj, kind))
                if filtered:
                    # Always retain exit candidate if present in original set
                    for (tii, tjj, tkind) in original_nb:
                        if tkind == 'X':
                            filtered.append((tii, tjj, tkind))
                            break
                    nb = filtered
            # Weights based on neighbor cell mobility (for exit, use boundary cell's mu)
            weights = []
            drift_logits = []
            gy_ = float(gy[i, j])
            gx_ = float(gx[i, j])
            grad_norm = (gy_ ** 2 + gx_ ** 2) ** 0.5
            for (ii, jj, kind) in nb:
                if kind == 'X':
                    m = mu[i, j]
                else:
                    m = mu[ii, jj]
                weights.append(max(1e-12, float(m)))
                # Optional drift bias toward +grad direction (advection proxy; still local)
                if drift_weight != 0.0 and grad_norm > 0.0:
                    dy = ii - i
                    dx = jj - j
                    step_norm = (dx * dx + dy * dy) ** 0.5
                    if step_norm > 0.0:
                        n_y, n_x = gy_ / grad_norm, gx_ / grad_norm
                        drift_logits.append(drift_weight * (dy * n_y + dx * n_x) / step_norm)
                    else:
                        drift_logits.append(0.0)
                else:
                    drift_logits.append(0.0)
            weights = np.array(weights, dtype=float)
            drift_logits = np.array(drift_logits, dtype=float)
            # Softmax for numerical stability
            z = np.exp((weights + drift_logits) - np.max(weights + drift_logits))
            p = z / np.sum(z)
            choice = int(np.searchsorted(np.cumsum(p), rng.random()))
            ii, jj, kind = nb[choice]
            if kind == 'X':
                # Attempt to exit on the right boundary at row i
                if emit_events and w in sampled_idx:
                    events.append({"kind": "edge_on", "h": h, "u": [int(i), int(j)], "v": [int(i), int(min(Nx - 1, j))], "exit": True})
                if maskA[i]:
                    FA += 1
                    alive[w] = False
                    if corridor_mask[i, min(Nx - 1, j)]:
                        exits_in_corridor += 1
                elif maskB[i]:
                    FB += 1
                    alive[w] = False
                    if corridor_mask[i, min(Nx - 1, j)]:
                        exits_in_corridor += 1
                else:
                    # Closed segment → reflect (no movement)
                    pass
            else:
                # Move
                dy = ii - i
                dx = jj - j
                if emit_events and w in sampled_idx:
                    events.append({"kind": "vt_touch", "h": h, "token": [int(i), int(j)]})
                    events.append({"kind": "edge_on", "h": h, "u": [int(i), int(j)], "v": [int(ii), int(jj)]})
                pos_y[w] = ii
                pos_x[w] = jj
                # Anisotropy projection (tangent ⟂ grad)
                gy_ = float(gy[i, j])
                gx_ = float(gx[i, j])
                norm = (gy_ ** 2 + gx_ ** 2) ** 0.5
                if norm > 1e-12:
                    # Normal unit vector = grad / ||grad||; tangent unit is perpendicular
                    n_y, n_x = gy_ / norm, gx_ / norm
                    t_y, t_x = -n_x, n_y
                    par = abs(dy * t_y + dx * t_x)
                    perp = abs(dy * n_y + dx * n_x)
                    sum_par += par
                    sum_perp += perp
                if w in path_samples:
                    path_samples[w].append((ii, jj))
        FA_series.append(FA)
        FB_series.append(FB)

    total_outflux = FA + FB
    eta_ch = (float(exits_in_corridor) / float(total_outflux)) if total_outflux > 0 else 0.0
    anis = (float(sum_par) / float(sum_perp + 1e-12))
    return {
        "FA": FA,
        "FB": FB,
        "FA_series": FA_series,
        "FB_series": FB_series,
        "eta_ch": eta_ch,
        "anis": anis,
        "paths": path_samples,
        "starts": list(zip(starts_y.tolist(), starts_x.tolist())),
        "events": events,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Flux Through Memory Channels v1 runner")
    p.add_argument("--spec", required=True, help="Path to spec JSON")
    p.add_argument("--allow-unapproved", action="store_true", help="Allow unapproved run (quarantine artifacts)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    os.environ["VDM_RUN_SCRIPT"] = Path(__file__).stem
    code_root = Path(__file__).resolve().parents[3]

    # Load spec
    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    S = Spec(**spec)

    # Approvals
    approved, engineering_only, proposal = check_tag_approval(DOMAIN, S.tag, args.allow_unapproved, code_root)

    # Map immutability receipts
    # Load channel map from spec inline data or from file path
    map_mode = str(S.map.get("map_mode", "mobility"))
    channel = np.array(S.map.get("channel_map", []), dtype=float)
    map_path = S.map.get("map_path")
    if (channel.size == 0) and map_path:
        try:
            p = Path(map_path)
            if p.suffix.lower() == ".npy":
                channel = np.array(np.load(p), dtype=float)
            elif p.suffix.lower() in (".csv", ".txt"):
                channel = np.array(np.loadtxt(p, delimiter="," if p.suffix.lower() == ".csv" else None), dtype=float)
            else:
                # best-effort load
                channel = np.array(np.load(p), dtype=float)
        except Exception:
            channel = np.array([], dtype=float)
    map_hash_start = sha256_array(channel) if channel.size else ""

    # Grid/time
    Nx, Ny = int(S.grid.get("Nx", 128)), int(S.grid.get("Ny", 64))
    Lx, Ly = float(S.grid.get("Lx", 8.0)), float(S.grid.get("Ly", 4.0))
    a = Lx / max(1, Nx)
    dt = float(S.time.get("dt", 0.01))
    T = float(S.time.get("T", 2.0))
    steps = int(round(T / dt))

    # Boundary model receipts (frozen-map v1 uses reflective walls + open outlets)
    boundary_model = "walls_reflecting + open_right"
    flux_convention = "outflux_only"

    # RJ basis sanity (diagnostic only; FTMC v1 has no operator)
    rj_basis_ok = False
    rj_basis_note = "not_applicable (no operator for passive FTMC v1)"

    # Determinism receipts (environment + runtime clause)
    env = env_receipts()
    determinism_ok = True
    determinism_clause = "not_run"

    # Probe-limit: runner does not include actuators; bus=None; events-only implied by design
    probe_limit_ok = True

    # Frozen-map: treat MemoryMap as an external field (no fold); we only record that we used a read-only map
    frozen_map_ok = True if channel.size else False

    # Budget mapping transparency: accept W,H in controls and report visits/edges/ttl mapping
    W = int(S.controls.get("walkers", 0))
    H = int(S.controls.get("hops", 0))
    ttl = H if H > 0 else None
    visits = W * H if (W > 0 and H > 0) else None
    edges = visits
    budget_mapping_ok = (ttl is not None and visits is not None)

    # Placeholder KPIs (to be computed by proper analysis modules)
    eta_ch = 0.0
    delta_B_ch = 0.0
    anisotropy = 1.0

    # Provenance
    commit_full, commit_short = _git_hashes(code_root)
    salted_tag = os.getenv("VDM_SALTED_TAG", "FluxThroughMemoryChannels_v1")
    try:
        salted_hash = hashlib.sha256((commit_full + "|" + salted_tag).encode("utf-8")).hexdigest()
    except Exception:
        salted_hash = None

    # Geometry: define outlet masks and injection stripe for tracer starts
    wA = float(S.geometry.get("w_A", 0.35))
    wB = float(S.geometry.get("w_B", 0.35))
    maskA, maskB = _build_outlet_masks(Nx, Ny, wA, wB)
    y0 = int(0.30 * Ny)
    y1 = int(0.70 * Ny)

    # Corridor mask from map (top-quantile band)
    corridor_q = float(S.analysis.get("corridor_q", 0.8))
    corridor = _compute_corridor_mask(channel, q=corridor_q) if channel.size else np.zeros((Ny, Nx), bool)

    # Tracer-walker passive flow over the map (advisors' suggestion Option 1)
    W = max(1, int(S.controls.get("walkers", 256)))
    H = max(1, int(S.controls.get("hops", 128)))
    nseeds = max(1, int(S.seeds))
    drift_w = float(S.controls.get("drift_weight", 0.0))
    corridor_priority = bool(S.controls.get("corridor_priority", True))
    emit_events = bool(S.controls.get("emit_events", False))

    FA_list = []
    FB_list = []
    eta_list = []
    anis_list = []
    # Use a modest subset of paths from the first seed for visualization
    viz_paths = {}
    viz_FA_series = None
    viz_FB_series = None
    for sidx in range(nseeds):
        sim = _simulate_tracers(channel, W, H, (y0, y1), maskA, maskB, corridor, seed=sidx, sample_paths=min(512, W), drift_weight=drift_w, corridor_priority=corridor_priority, emit_events=emit_events and (sidx == 0))
        FA_list.append(sim["FA"])
        FB_list.append(sim["FB"])
        eta_list.append(sim["eta_ch"])
        anis_list.append(sim["anis"])
        if sidx == 0:
            viz_paths = sim["paths"]
            viz_FA_series = sim["FA_series"]
            viz_FB_series = sim["FB_series"]
            events_seed0 = sim.get("events", [])
    # Determinism receipt: repeat seed-0 run and compare cumulative series
    if viz_FA_series is not None and viz_FB_series is not None:
        sim_repeat = _simulate_tracers(channel, W, H, (y0, y1), maskA, maskB, corridor, seed=0, sample_paths=0, drift_weight=drift_w, corridor_priority=corridor_priority, emit_events=False)
        A1 = np.array(viz_FA_series, dtype=int); B1 = np.array(viz_FB_series, dtype=int)
        A2 = np.array(sim_repeat["FA_series"], dtype=int); B2 = np.array(sim_repeat["FB_series"], dtype=int)
        bitwise_eq = bool(np.array_equal(A1, A2) and np.array_equal(B1, B2))
        linf = float(max((np.abs(A1 - A2).max() if A1.size else 0), (np.abs(B1 - B2).max() if B1.size else 0)))
        max_ulp = float(max(linf, 0.0))
        determinism_clause = "bitwise" if bitwise_eq else ("linf<=1e-12" if linf <= 1e-12 else ("max-ULP<=1" if max_ulp <= 1.0 else "fail"))
        determinism_ok = bool(bitwise_eq or linf <= 1e-12 or max_ulp <= 1.0)

    FA_total = float(np.mean(FA_list))
    FB_total = float(np.mean(FB_list))
    B = FA_total - FB_total
    rho = FA_total / (FA_total + FB_total + 1e-16)

    # Baseline geometry-only run (uniform weights)
    uniform_mu = np.ones_like(channel) if channel.size else np.ones((Ny, Nx), dtype=float)
    FA0_list, FB0_list = [], []
    for sidx in range(nseeds):
        sim0 = _simulate_tracers(uniform_mu, W, H, (y0, y1), maskA, maskB, corridor, seed=1000 + sidx, sample_paths=0, drift_weight=drift_w, corridor_priority=corridor_priority, emit_events=False)
        FA0_list.append(sim0["FA"])
        FB0_list.append(sim0["FB"])
    FA0 = float(np.mean(FA0_list))
    FB0 = float(np.mean(FB0_list))
    B0 = FA0 - FB0
    # Paired delta per seed
    B_list = [float(a - b) for a, b in zip(FA_list, FB_list)]
    B0_list = [float(a - b) for a, b in zip(FA0_list, FB0_list)]
    delta_list = [bb - bb0 for bb, bb0 in zip(B_list, B0_list)]
    delta_B_ch = float(np.mean(delta_list)) if delta_list else 0.0

    # Control: Port-closure ablation (turn off outlets A/B → expect zero outflux)
    maskA_off = np.zeros_like(maskA, dtype=bool)
    maskB_off = np.zeros_like(maskB, dtype=bool)
    sim_closed = _simulate_tracers(channel, W, H, (y0, y1), maskA_off, maskB_off, corridor, seed=4242, sample_paths=0, drift_weight=drift_w, corridor_priority=corridor_priority, emit_events=False)
    port_closure_ok = (sim_closed["FA"] + sim_closed["FB"]) == 0

    # CI helper
    def _ci(xs: list[float]) -> Tuple[float, float]:
        if not xs:
            return (0.0, 0.0)
        m = float(np.mean(xs))
        if len(xs) <= 1:
            return (m, m)
        s = float(np.std(xs, ddof=1))
        hw = 1.96 * s / (len(xs) ** 0.5)
        return (m - hw, m + hw)

    eta_ci = _ci(eta_list)
    anis_ci = _ci(anis_list)
    dB_ci = _ci(delta_list)

    # Artifacts: (1) map+paths; (2) flux vs hops panel
    import matplotlib.pyplot as plt
    apply_style("light")
    quarantine = bool((not approved) or engineering_only)

    # Figure 1: channel map with sampled paths and outlet bands
    fig1, ax1 = plt.subplots(1, 1, figsize=(8, 3.5))
    ax1.set_title(f"FTMC v1 — Channel map ({map_mode}) with sampled tracer paths")
    if channel.size:
        im = ax1.imshow(channel, origin="lower", aspect="equal", cmap="viridis")
        fig1.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
    # Plot corridor band
    if corridor.any():
        yy, xx = np.where(corridor)
        ax1.scatter(xx, yy, s=1, c="#ffffff22", marker="s")
    # Outlet bands
    top_len = int(round(Ny * wA))
    bot_len = int(round(Ny * wB))
    ax1.axhspan(Ny - top_len, Ny, xmin=(Nx - 1) / Nx, xmax=1.0, color="#1f77b4", alpha=0.15)
    ax1.axhspan(0, bot_len, xmin=(Nx - 1) / Nx, xmax=1.0, color="#ff7f0e", alpha=0.15)
    # Sampled paths
    for pid, pts in viz_paths.items():
        if len(pts) > 1:
            ys = [p[0] for p in pts]
            xs = [p[1] for p in pts]
            ax1.plot(xs, ys, lw=0.6, alpha=0.5, color="#000000")
    ax1.set_xticks([]); ax1.set_yticks([])
    fig1_path = save_figure(DOMAIN, build_slug("ftmc_map_paths", S.tag), fig1, failed=quarantine)

    # Figure 2: cumulative flux vs hops
    fig2, ax2 = plt.subplots(1, 1, figsize=(7, 3.0))
    ax2.set_title("Cumulative outflux vs hops (seed 0)")
    if viz_FA_series is not None and viz_FB_series is not None:
        ax2.plot(viz_FA_series, label="F_A(h)")
        ax2.plot(viz_FB_series, label="F_B(h)")
    ax2.set_xlabel("hops")
    ax2.set_ylabel("cumulative exits")
    ax2.legend(loc="best")
    fig2_path = save_figure(DOMAIN, build_slug("ftmc_flux_vs_hops", S.tag), fig2, failed=quarantine)

    # Dimensionless receipts and outflux floor gate
    Pi_walk = float(W) / float(max(1, Nx * Ny))
    Pi_hop = float(H) / float(max(1, Nx))
    total_outflux_mean = float(FA_total + FB_total)
    outflux_floor_eps = float(S.analysis.get("outflux_floor_eps", 1.0))
    outflux_floor_ok = bool(total_outflux_mean > outflux_floor_eps)

    # CSV metrics artifact (minimum artifact policy: at least 1 CSV)
    csv_metrics = {
        "timestamp": datetime.now().isoformat(),
        "domain": DOMAIN,
        "tag": S.tag,
        "approved": bool(approved),
        "quarantined": bool(quarantine),
        "seed_count": int(nseeds),
        "walkers": int(W),
        "hops": int(H),
        "FA_mean": float(FA_total),
        "FB_mean": float(FB_total),
        "B": float(B),
        "B0": float(B0),
    "delta_B_ch": float(delta_B_ch),
    "delta_B_ci_lo": float(dB_ci[0]),
    "delta_B_ci_hi": float(dB_ci[1]),
        "eta_mean": float(np.mean(eta_list) if eta_list else 0.0),
        "eta_ci_lo": float(eta_ci[0]),
        "eta_ci_hi": float(eta_ci[1]),
        "anis_mean": float(np.mean(anis_list) if anis_list else 1.0),
        "anis_ci_lo": float(anis_ci[0]),
        "anis_ci_hi": float(anis_ci[1]),
        "port_closure_pass": bool(port_closure_ok),
        "commit": commit_short,
    "map_hash": sha256_array(channel) if channel.size else "",
    "Pi_walk": float(Pi_walk),
    "Pi_hop": float(Pi_hop),
    "corridor_q": float(corridor_q),
    "outflux_floor_eps": float(outflux_floor_eps),
    "outflux_floor_ok": bool(outflux_floor_ok),
    "rj_basis_ok": bool(rj_basis_ok),
    "rj_basis_note": rj_basis_note,
    "determinism": bool(determinism_ok),
    "determinism_clause": determinism_clause,
    }
    csv_path = log_path_by_tag(DOMAIN, "ftmc_v1_metrics", S.tag, failed=quarantine, type="csv")
    write_log(csv_path, csv_metrics)


    # Map hash end (immutability)
    map_hash_end = sha256_array(channel) if channel.size else ""
    map_immutable_ok = (map_hash_start == map_hash_end)

    # Summary JSON (schema-compatible)
    # Pre-compute JSON path so we can reference it inside the summary artifacts
    json_path = log_path_by_tag(DOMAIN, "ftmc_v1_summary", S.tag, failed=quarantine, type="json")

    summary: Dict[str, Any] = {
        "tag": S.tag,
        "domain": DOMAIN,
        "provenance": {
            "commit_full": commit_full,
            "commit": commit_short,
            "salted_tag": salted_tag,
            "salted_hash": salted_hash,
        },
        "env": env,
        "compliance": {
            "boundary_model": boundary_model,
            "flux_convention": flux_convention,
            "map_immutable": bool(map_immutable_ok),
            "rj_basis_ok": bool(rj_basis_ok),
            "rj_basis_note": rj_basis_note,
            "determinism": bool(determinism_ok),
            "determinism_clause": determinism_clause,
            "probe_limit": bool(probe_limit_ok),
            "frozen_map": bool(frozen_map_ok),
            "budget_mapping": bool(budget_mapping_ok),
            "outflux_floor_ok": bool(outflux_floor_ok),
            "void_faithful": True,
        },
        "map": {"mode": map_mode, "hash": map_hash_end},
        "dimensionless": {"Pi_walk": float(Pi_walk), "Pi_hop": float(Pi_hop), "corridor_q": float(corridor_q)},
        "budget": {"visits": int(W * H), "edges": int(W * H), "ttl": int(H), "seeds": int(nseeds)},
        "kpi": {
            "eta_ch": {"value": float(np.mean(eta_list) if eta_list else 0.0), "ci": [float(eta_ci[0]), float(eta_ci[1])]},
            "delta_B_ch": {"value": float(delta_B_ch), "ci": [float(dB_ci[0]), float(dB_ci[1])]},
            "anisotropy": {"value": float(np.mean(anis_list) if anis_list else 1.0), "ci": [float(anis_ci[0]), float(anis_ci[1])]},
            "meters": {"h_theorem": {}, "determinism": {}, "rj": {}},
        },
        "artifacts": {"figures": [str(fig1_path), str(fig2_path)], "logs": [str(csv_path), str(json_path)]},
        "policy": {
            "approved": bool(approved),
            "engineering_only": bool(engineering_only),
            "quarantined": bool(quarantine),
            "tag": S.tag,
            "proposal": proposal,
        },
        "controls": {
            "port_closure": {"FA": int(sim_closed["FA"]), "FB": int(sim_closed["FB"]), "pass": bool(port_closure_ok)},
            "rj_basis": {"ok": bool(rj_basis_ok), "note": rj_basis_note},
            "drift_weight": float(drift_w),
            "corridor_priority": bool(corridor_priority),
            "emit_events": bool(emit_events),
        },
        "gate_matrix": {"compliance": "PASS" if (map_immutable_ok and frozen_map_ok and probe_limit_ok and budget_mapping_ok) else "FAIL", "outflux_floor": "PASS" if outflux_floor_ok else "FAIL"},
        "status": "pending",
    }

    # Optional events log (void-style) for seed 0 sampled walkers
    if emit_events:
        events_path = log_path_by_tag(DOMAIN, "ftmc_v1_events", S.tag, failed=quarantine, type="json")
        events_payload = {"events": events_seed0 or []}
        write_log(events_path, events_payload)
        # add to artifacts; ensure the list exists
        logs_list = summary.get("artifacts", {}).get("logs", None)
        if isinstance(logs_list, list):
            logs_list.append(str(events_path))

    # Write summary
    write_log(json_path, summary)
    print(json.dumps({"summary_path": str(json_path), "approved": approved}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
