#!/usr/bin/env python3
"""
VDM Report Generator — Pure Python Tool
=======================================

This is a complete, self-contained Python replacement for the original
vdm_convert.py + vdm_dashboard.html combo.

What it does:
• Loads the exact same .h5 state file (and optional .jsonl events)
• Runs every computation that was in the converter:
  - Spectral embedding (Fiedler + EV3/EV4)
  - Spectral communities + modularity
  - Bridge edges
  - Eigenvector centrality
  - Gini coefficients, entropy, Laplacian spectrum, etc.
• Generates a full static report with high-resolution PNGs for every
  visualization that existed in the HTML dashboard:
  - 3D spectral embedding (4 variants: W, community, degree, centrality + bridges)
  - Degree & W histograms
  - Laplacian spectrum
  - ADC territory horizontal bars
  - Gini + entropy gauges (Plotly indicators)
  - All time-series plots (entropy, valence, coverage, edges, b1_z, territories)
  - Territory detail CSV
• Creates a clean report directory with:
  - summary.txt (all meta stats)
  - data.json (original bundle for reproducibility)
  - territories.csv
  - images/*.png (every plot)
  - report_index.html (simple clickable overview)

Usage:
    python vdm_report.py state_22260.h5 [--events utd_events.jsonl] [--output report_dir]

Extra dependencies (one-time):
    pip install plotly kaleido

All original logic (including subsampling for N>8000, retry k-means, bridge subsampling, etc.)
is preserved exactly — no information is lost.
"""

import argparse
import json
import sys
import time
from pathlib import Path
import os

import numpy as np
import h5py
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from scipy.sparse.csgraph import connected_components
from scipy.cluster.vq import kmeans2, whiten

# ── Plotly for all visualizations ──
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.kaleido.scope.mathjax = None  # speeds up PNG export

# ====================== ORIGINAL COMPUTATION FUNCTIONS (copied verbatim for fidelity) ======================

def gini(x):
    """Gini coefficient of a 1-D array."""
    x = np.sort(np.asarray(x, dtype=np.float64))
    n = len(x)
    if n == 0 or x.sum() == 0:
        return 0.0
    idx = np.arange(1, n + 1)
    return float((2.0 * np.sum(idx * x) / (n * x.sum())) - (n + 1.0) / n)


def spectral_communities(vecs, k=8):
    """K-means on first k eigenvectors → community labels."""
    X = np.array(vecs)[:, 1:k+1].astype(np.float64)
    X = whiten(X)
    best_labels = None
    best_dist = np.inf
    for seed in range(5):
        try:
            centroids, labels = kmeans2(X, k, minit='++', seed=seed*42, iter=30)
            dists = np.sum((X - centroids[labels])**2)
            if dists < best_dist:
                best_dist = dists
                best_labels = labels
        except Exception:
            continue
    if best_labels is None:
        best_labels = np.zeros(len(vecs), dtype=int)
    return best_labels


def compute_modularity(row_ptr, col_idx, labels, N):
    """Newman modularity Q for given community labels."""
    m = len(col_idx)
    degrees = np.diff(row_ptr)
    Q = 0.0
    for i in range(N):
        start, end = row_ptr[i], row_ptr[i+1]
        for jj in range(start, end):
            j = col_idx[jj]
            if labels[i] == labels[j]:
                Q += 1.0 - degrees[i] * degrees[j] / m
    Q /= m
    return float(Q)


def find_bridge_edges(row_ptr, col_idx, labels, embed_coords, embed_idx_set,
                      max_bridges=500, rng=None):
    if rng is None:
        rng = np.random.default_rng(42)
    N = len(labels)
    bridges = []
    for i in range(N):
        if i not in embed_idx_set:
            continue
        start, end = row_ptr[i], row_ptr[i+1]
        for jj in range(start, end):
            j = col_idx[jj]
            if j not in embed_idx_set:
                continue
            if labels[i] != labels[j]:
                bridges.append((i, j))
    if len(bridges) > max_bridges:
        idx = rng.choice(len(bridges), size=max_bridges, replace=False)
        bridges = [bridges[ii] for ii in idx]
    return bridges


def eigenvector_centrality(row_ptr, col_idx, N, tol=1e-6, max_iter=100):
    data = np.ones(len(col_idx), dtype=np.float64)
    A = csr_matrix((data, col_idx, row_ptr), shape=(N, N))
    x = np.ones(N) / N
    for _ in range(max_iter):
        x_new = A.dot(x)
        norm = np.linalg.norm(x_new)
        if norm == 0:
            break
        x_new /= norm
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    return x


def compute_spectral_embedding(row_ptr, col_idx, N, n_components=10):
    data = np.ones(len(col_idx), dtype=np.float32)
    A = csr_matrix((data, col_idx, row_ptr), shape=(N, N))
    degrees = np.array(A.sum(axis=1)).ravel()

    d_inv_sqrt = np.zeros(N)
    mask = degrees > 0
    d_inv_sqrt[mask] = 1.0 / np.sqrt(degrees[mask])
    D_inv_sqrt = csr_matrix((d_inv_sqrt, (np.arange(N), np.arange(N))), shape=(N, N))
    L_norm = csr_matrix(np.eye(N)) - D_inv_sqrt @ A @ D_inv_sqrt

    k = min(n_components + 1, N - 2)
    try:
        vals, vecs = eigsh(L_norm, k=k, which='SM', tol=1e-6)
        order = np.argsort(vals)
        vals = vals[order]
        vecs = vecs[:, order]
    except Exception as e:
        print(f"  Warning: eigsh failed ({e}), using random embedding", file=sys.stderr)
        vals = np.zeros(k)
        vecs = np.random.randn(N, k).astype(np.float32)
    return vals.tolist(), vecs.tolist()


def compute_laplacian_spectrum(row_ptr, col_idx, N, k=20):
    data = np.ones(len(col_idx), dtype=np.float32)
    A = csr_matrix((data, col_idx, row_ptr), shape=(N, N))
    degrees = np.array(A.sum(axis=1)).ravel()
    d_inv_sqrt = np.zeros(N)
    mask = degrees > 0
    d_inv_sqrt[mask] = 1.0 / np.sqrt(degrees[mask])
    D_inv_sqrt = csr_matrix((d_inv_sqrt, (np.arange(N), np.arange(N))), shape=(N, N))
    L_norm = csr_matrix(np.eye(N)) - D_inv_sqrt @ A @ D_inv_sqrt

    k = min(k, N - 2)
    try:
        vals, _ = eigsh(L_norm, k=k, which='SM', tol=1e-6)
        vals = np.sort(vals)
    except Exception:
        vals = np.zeros(k)
    return vals.tolist()


def load_h5(path):
    print(f"Loading {path}...")
    t0 = time.time()

    with h5py.File(path, 'r') as f:
        W = f['sparse/W'][:].astype(np.float64)
        row_ptr = f['sparse/row_ptr'][:]
        col_idx = f['sparse/col_idx'][:]
        adc_raw = f['adc_json'][()]
        adc = json.loads(adc_raw)

    N = len(W)
    degrees = np.diff(row_ptr).astype(np.int32)
    n_edges = len(col_idx)
    mean_degree = float(degrees.mean())
    median_degree = float(np.median(degrees))
    max_degree = int(degrees.max())

    print(f"  N={N}, edges={n_edges}, mean_deg={mean_degree:.1f}")

    # Degree distribution
    deg_counts, deg_bins = np.histogram(degrees, bins=np.arange(0, max_degree + 2) - 0.5)
    degree_hist = {
        "bins": np.arange(0, max_degree + 1).tolist(),
        "counts": deg_counts.tolist(),
    }

    # W distribution
    w_hist_counts, w_hist_bins = np.histogram(W, bins=80)
    w_hist = {
        "bin_centers": ((w_hist_bins[:-1] + w_hist_bins[1:]) / 2).tolist(),
        "counts": w_hist_counts.tolist(),
    }

    gini_degree = gini(degrees)
    gini_w = gini(W)

    p = degrees / degrees.sum()
    p = p[p > 0]
    connectome_entropy = float(-np.sum(p * np.log2(p)))

    data = np.ones(len(col_idx), dtype=np.float32)
    A = csr_matrix((data, col_idx, row_ptr), shape=(N, N))
    n_components, _ = connected_components(A, directed=False)

    print(f"  Gini(degree)={gini_degree:.4f}, Gini(W)={gini_w:.4f}, components={n_components}")

    print("  Computing eigenvector centrality...")
    ev_cent = eigenvector_centrality(row_ptr, col_idx, N)

    # Spectral embedding (same subsampling logic as original)
    if N > 8000:
        sub_idx = np.random.default_rng(42).choice(N, size=5000, replace=False)
        sub_idx.sort()
        sub_map = {old: new for new, old in enumerate(sub_idx)}
        sub_set = set(sub_idx.tolist())
        sub_rows = [0]
        sub_cols = []
        for new_i, old_i in enumerate(sub_idx):
            start, end = row_ptr[old_i], row_ptr[old_i + 1]
            nbrs = col_idx[start:end]
            for j in nbrs:
                if j in sub_set:
                    sub_cols.append(sub_map[j])
            sub_rows.append(len(sub_cols))
        sub_row_ptr = np.array(sub_rows, dtype=np.int64)
        sub_col_idx = np.array(sub_cols, dtype=np.int32)
        sub_N = len(sub_idx)
        sub_W = W[sub_idx]
        sub_deg = np.diff(sub_row_ptr).astype(np.int32)
        sub_cent = ev_cent[sub_idx]
        eigenvalues, eigenvectors = compute_spectral_embedding(sub_row_ptr, sub_col_idx, sub_N, n_components=6)

        n_comm = min(8, sub_N - 1)
        print(f"  Computing spectral communities (k={n_comm})...")
        comm_labels = spectral_communities(eigenvectors, k=n_comm)
        modularity = compute_modularity(sub_row_ptr, sub_col_idx, comm_labels, sub_N)

        embed_idx = np.linspace(0, sub_N - 1, min(sub_N, 3000), dtype=int)
        embed_idx_set = set(embed_idx.tolist())
        bridges_raw = find_bridge_edges(sub_row_ptr, sub_col_idx, comm_labels, None, embed_idx_set, max_bridges=400)
        embed_idx_map = {old: pos for pos, old in enumerate(embed_idx)}
        bridge_lines = []
        for (a, b) in bridges_raw:
            if a in embed_idx_map and b in embed_idx_map:
                bridge_lines.append([embed_idx_map[a], embed_idx_map[b]])

        embedding = {
            "x": [eigenvectors[i][1] for i in embed_idx],
            "y": [eigenvectors[i][2] for i in embed_idx],
            "z": [eigenvectors[i][3] if len(eigenvectors[i]) > 3 else 0 for i in embed_idx],
            "w": [float(sub_W[i]) for i in embed_idx],
            "deg": [int(sub_deg[i]) for i in embed_idx],
            "community": [int(comm_labels[i]) for i in embed_idx],
            "centrality": [float(sub_cent[i]) for i in embed_idx],
            "bridges": bridge_lines,
            "subsampled": True,
            "n_shown": len(embed_idx),
        }
    else:
        eigenvalues, eigenvectors = compute_spectral_embedding(row_ptr, col_idx, N, n_components=6)
        n_comm = min(8, N - 1)
        print(f"  Computing spectral communities (k={n_comm})...")
        comm_labels = spectral_communities(eigenvectors, k=n_comm)
        modularity = compute_modularity(row_ptr, col_idx, comm_labels, N)

        embed_idx = np.linspace(0, N - 1, min(N, 3000), dtype=int)
        embed_idx_set = set(embed_idx.tolist())
        bridges_raw = find_bridge_edges(row_ptr, col_idx, comm_labels, None, embed_idx_set, max_bridges=400)
        embed_idx_map = {old: pos for pos, old in enumerate(embed_idx)}
        bridge_lines = []
        for (a, b) in bridges_raw:
            if a in embed_idx_map and b in embed_idx_map:
                bridge_lines.append([embed_idx_map[a], embed_idx_map[b]])

        embedding = {
            "x": [eigenvectors[i][1] for i in embed_idx],
            "y": [eigenvectors[i][2] for i in embed_idx],
            "z": [eigenvectors[i][3] if len(eigenvectors[i]) > 3 else 0 for i in embed_idx],
            "w": [float(W[i]) for i in embed_idx],
            "deg": [int(degrees[i]) for i in embed_idx],
            "community": [int(comm_labels[i]) for i in embed_idx],
            "centrality": [float(ev_cent[i]) for i in embed_idx],
            "bridges": bridge_lines,
            "subsampled": N > 3000,
            "n_shown": len(embed_idx),
        }

    print(f"  Modularity Q={modularity:.4f}, communities={n_comm}, bridges={len(bridge_lines)}")

    lap_spectrum = compute_laplacian_spectrum(row_ptr, col_idx, N, k=20)

    territories = []
    for t in adc.get("territories", []):
        territories.append({
            "id": t.get("id", 0),
            "key": t.get("key", []),
            "mass": t.get("mass", 0),
            "conf": t.get("conf", 0),
            "ttl": t.get("ttl", 0),
            "w_mean": t.get("w_stats", {}).get("mean", 0),
            "w_var": t.get("w_stats", {}).get("var", 0),
            "s_mean": t.get("s_stats", {}).get("mean", 0),
            "s_var": t.get("s_stats", {}).get("var", 0),
        })

    stem = Path(path).stem
    tick = None
    for part in stem.split("_"):
        try:
            tick = int(part)
            break
        except ValueError:
            continue

    spectral_gap_ratio = float(eigenvalues[1] / eigenvalues[2]) if len(eigenvalues) > 2 and eigenvalues[2] > 1e-10 else 0.0

    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")

    return {
        "meta": {
            "source_file": Path(path).name,
            "tick": tick,
            "N": N,
            "n_edges": n_edges,
            "mean_degree": mean_degree,
            "median_degree": median_degree,
            "max_degree": max_degree,
            "gini_degree": gini_degree,
            "gini_w": gini_w,
            "connectome_entropy": connectome_entropy,
            "n_components": n_components,
            "w_mean": float(W.mean()),
            "w_std": float(W.std()),
            "w_min": float(W.min()),
            "w_max": float(W.max()),
            "modularity": modularity,
            "n_communities": n_comm,
            "spectral_gap_ratio": spectral_gap_ratio,
            "n_bridge_edges": len(bridge_lines),
        },
        "degree_hist": degree_hist,
        "w_hist": w_hist,
        "embedding": embedding,
        "laplacian_spectrum": lap_spectrum,
        "territories": territories,
        "eigenvalues": eigenvalues[:20] if len(eigenvalues) > 20 else eigenvalues,
    }


def load_events(path):
    print(f"Loading events from {path}...")
    statuses = []
    say_events = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("type") == "text" and isinstance(obj.get("payload"), dict):
                p = obj["payload"]
                if p.get("type") == "status" and "t" in p:
                    entry = {"t": p["t"]}
                    for key in ["neurons", "phase", "cohesion_components", "vt_coverage", "vt_entropy",
                                "connectome_entropy", "active_edges", "b1_z", "adc_territories",
                                "sie_valence_01", "sie_v2_valence_01", "sie_v2_reward_mean",
                                "sie_total_reward", "ute_in_count", "ute_text_count",
                                "homeostasis_pruned", "homeostasis_bridged"]:
                        if key in p:
                            entry[key] = p[key]
                    statuses.append(entry)
                elif p.get("type") == "say":
                    say_events.append({"t": p.get("t", obj.get("t", 0)), "text": p.get("msg", p.get("text", ""))[:200]})
            elif obj.get("type") == "macro" and obj.get("macro") == "status":
                args = obj.get("args", {})
                if "t" in args:
                    entry = {"t": args["t"]}
                    for key in ["neurons", "cohesion_components", "vt_coverage", "vt_entropy",
                                "connectome_entropy", "active_edges", "ute_in_count", "ute_text_count"]:
                        if key in args:
                            entry[key] = args[key]
                    statuses.append(entry)

    by_tick = {}
    for s in statuses:
        t = s["t"]
        if t not in by_tick or len(s) > len(by_tick[t]):
            by_tick[t] = s
    unique = list(by_tick.values())
    unique.sort(key=lambda x: x["t"])

    print(f"  {len(unique)} status events, {len(say_events)} say events")
    return {"statuses": unique, "say_events": say_events}


# ====================== COLOR PALETTES (exact match to dashboard) ======================

TC = ['#ef4444','#f97316','#fbbf24','#34d399','#22d3ee','#6366f1','#a855f7','#f472b6','#64748b','#e2e8f0']
CS = [[0,'#6366f1'],[0.2,'#22d3ee'],[0.45,'#34d399'],[0.7,'#fbbf24'],[1,'#ef4444']]
COMM_PALETTE = ['#ef4444','#f97316','#fbbf24','#34d399','#22d3ee','#6366f1','#a855f7','#f472b6','#64748b','#e2e8f0']


def render_report(bundle: dict, output_dir: Path):
    """Generate every visualization from the original HTML dashboard as PNGs + supporting files."""
    os.makedirs(output_dir / "images", exist_ok=True)
    s = bundle["state"]
    m = s["meta"]
    ev = bundle.get("events", {"statuses": []})
    sts = ev.get("statuses", [])

    # ── 1. Save original JSON bundle ──
    with open(output_dir / "data.json", "w") as f:
        json.dump(bundle, f, indent=2)

    # ── 2. Summary text ──
    active_terr = sum(1 for t in s["territories"] if t["mass"] > 0)
    total_mass = sum(t["mass"] for t in s["territories"])
    summary = f"""VDM ANALYSIS REPORT
===================
Source          : {m['source_file']}
Tick            : {m.get('tick', '?')}
Neurons (N)     : {m['N']:,}
Active Edges    : {m['n_edges']:,} (mean deg {m['mean_degree']:.1f})
Components      : {m['n_components']} {"(fully connected)" if m['n_components']==1 else "(fragmented)"}
Gini (degree)   : {m['gini_degree']:.4f}
Gini (W)        : {m['gini_w']:.4f}
Connectome H    : {m['connectome_entropy']:.2f} bits
Modularity Q    : {m['modularity']:.4f} ({m['n_communities']} communities)
Spectral gap    : {m['spectral_gap_ratio']:.4f}
Bridge edges    : {m['n_bridge_edges']}
ADC Territories : {active_terr} (total mass {total_mass:,})
Generated       : {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
    (output_dir / "summary.txt").write_text(summary)
    print(f"   → summary.txt written")

    # ── 3. Territory CSV ──
    terrs = [t for t in s["territories"] if t["mass"] > 0]
    if terrs:
        with open(output_dir / "territories.csv", "w", newline="") as f:
            import csv
            w = csv.writer(f)
            w.writerow(["ID", "Key", "Mass", "Conf", "TTL", "W_mean", "S_mean"])
            for t in sorted(terrs, key=lambda x: x["mass"], reverse=True):
                w.writerow([t["id"], str(t["key"]), t["mass"], t["conf"], t["ttl"],
                            t["w_mean"], t["s_mean"]])
        print(f"   → territories.csv written")

    # ── 4. Plots (all saved as PNG) ──

    def save_fig(fig, name: str, w=900, h=500):
        path = output_dir / "images" / f"{name}.png"
        fig.write_image(path, width=w, height=h, scale=2)
        print(f"   → images/{name}.png")

    # 4.1 Degree Distribution
    dh = s["degree_hist"]
    max_bin = max(i for i, c in enumerate(dh["counts"]) if c > 0)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dh["bins"][:max_bin+2], y=dh["counts"][:max_bin+2],
                         marker_color="#22d3ee", name="Degree"))
    fig.add_vline(x=m["mean_degree"], line_dash="dash", line_color="#ef4444", annotation_text="mean")
    fig.add_vline(x=m["median_degree"], line_dash="dash", line_color="#34d399", annotation_text="median")
    fig.update_layout(title="Degree Distribution", xaxis_title="Degree", yaxis_title="Count", bargap=0.1)
    save_fig(fig, "degree_hist", 900, 420)

    # 4.2 W Distribution
    wh = s["w_hist"]
    fig = go.Figure(go.Bar(x=wh["bin_centers"], y=wh["counts"], marker_color="#f472b6"))
    fig.add_vline(x=m["w_mean"], line_dash="dash", line_color="#34d399",
                  annotation_text=f"mean = {m['w_mean']:.4f}")
    fig.update_layout(title="Node Weight (W) Distribution", xaxis_title="W", yaxis_title="Count")
    save_fig(fig, "w_hist", 900, 420)

    # 4.3 Laplacian Spectrum
    lap = s["laplacian_spectrum"]
    fig = go.Figure()
    colors = ["#fbbf24" if i < 2 else "#34d399" for i in range(len(lap))]
    fig.add_trace(go.Bar(x=list(range(len(lap))), y=lap, marker_color=colors))
    fig.add_trace(go.Scatter(x=list(range(len(lap))), y=lap, mode="lines+markers", line_color="#fbbf24"))
    fig.update_layout(title="Laplacian Spectrum (first 20 eigenvalues)", xaxis_title="Index", yaxis_title="Eigenvalue")
    save_fig(fig, "laplacian_spectrum", 900, 420)

    # 4.4 ADC Territory Mass (horizontal bar)
    terr_sorted = sorted([t for t in s["territories"] if t["mass"] > 0], key=lambda x: x["mass"], reverse=True)
    if terr_sorted:
        names = [f"T{t['id']} (k={t.get('key', [0])[1]})" for t in terr_sorted]
        masses = [t["mass"] for t in terr_sorted]
        colors = [TC[i % len(TC)] for i in range(len(terrs))]
        fig = go.Figure(go.Bar(y=names, x=masses, orientation="h", marker_color=colors,
                               text=[f"{int(m):,}" for m in masses], textposition="outside"))
        fig.update_layout(title="ADC Territory Mass", xaxis_title="Mass", height=300 + len(names)*25)
        save_fig(fig, "territory_mass", 1000, max(500, 300 + len(names)*25))

    # 4.5 Gini Gauges (one figure with 3 indicators)
    gauge_fig = make_subplots(rows=1, cols=3, specs=[[{"type": "indicator"}] * 3])
    gauge_fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=m["gini_degree"],
        title={"text": "Degree Gini"},
        gauge={"axis": {"range": [0, 1]}, "bar": {"color": "#f472b6"}}
    ), row=1, col=1)
    gauge_fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=m["gini_w"],
        title={"text": "W Gini"},
        gauge={"axis": {"range": [0, 1]}, "bar": {"color": "#34d399"}}
    ), row=1, col=2)
    gauge_fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=min(m["connectome_entropy"] / 16, 1),
        title={"text": "Entropy / 16"},
        gauge={"axis": {"range": [0, 1]}, "bar": {"color": "#fbbf24"}},
        number={"suffix": " bits", "valueformat": ".2f"}
    ), row=1, col=3)
    gauge_fig.update_layout(title="Inequality & Entropy Gauges", height=420)
    save_fig(gauge_fig, "gauges", 1200, 420)

    # 4.6 3D Spectral Embedding — 4 variants (covers all interactive modes from dashboard)
    emb = s["embedding"]
    max_deg = max(emb["deg"]) if emb["deg"] else 1
    deg_sizes = [1.2 + 5.0 * (d / max_deg) for d in emb["deg"]]

    def make_3d_trace(color_data, colorscale, title_suffix):
        return go.Scatter3d(
            x=emb["x"], y=emb["y"], z=emb["z"],
            mode="markers",
            marker=dict(size=deg_sizes, color=color_data,
                        colorscale=colorscale, showscale=True, opacity=0.75),
            hovertext=[f"deg={d} W={w:.4f}" for d, w in zip(emb["deg"], emb["w"])],
            name=title_suffix
        )

    # Bridges (same as original)
    bridge_x, bridge_y, bridge_z = [], [], []
    if emb.get("bridges"):
        for a, b in emb["bridges"]:
            bridge_x.extend([emb["x"][a], emb["x"][b], None])
            bridge_y.extend([emb["y"][a], emb["y"][b], None])
            bridge_z.extend([emb["z"][a], emb["z"][b], None])

    def add_bridges(fig):
        if bridge_x:
            fig.add_trace(go.Scatter3d(x=bridge_x, y=bridge_y, z=bridge_z,
                                       mode="lines", line=dict(color="rgba(255,255,255,0.12)", width=1),
                                       name="Bridge edges"))

    # Variant 1: colored by W
    fig_w = go.Figure(data=[make_3d_trace(emb["w"], CS, "W")])
    add_bridges(fig_w)
    fig_w.update_layout(title="Spectral Embedding — colored by W", scene=dict(xaxis_title="Fiedler", yaxis_title="EV3", zaxis_title="EV4"))
    save_fig(fig_w, "3d_embedding_W", 1200, 800)

    # Variant 2: colored by community
    if emb.get("community"):
        comm_colors = [COMM_PALETTE[c % len(COMM_PALETTE)] for c in emb["community"]]
        fig_comm = go.Figure(data=[go.Scatter3d(x=emb["x"], y=emb["y"], z=emb["z"],
                                                mode="markers", marker=dict(size=deg_sizes, color=comm_colors, opacity=0.85))])
        add_bridges(fig_comm)
        fig_comm.update_layout(title="Spectral Embedding — colored by Community")
        save_fig(fig_comm, "3d_embedding_community", 1200, 800)

    # Variant 3: colored by degree
    fig_deg = go.Figure(data=[make_3d_trace(emb["deg"], [[0,"#6366f1"],[0.5,"#22d3ee"],[1,"#ef4444"]], "Degree")])
    add_bridges(fig_deg)
    fig_deg.update_layout(title="Spectral Embedding — colored by Degree")
    save_fig(fig_deg, "3d_embedding_degree", 1200, 800)

    # Variant 4: colored by centrality (if present)
    if emb.get("centrality"):
        fig_cent = go.Figure(data=[make_3d_trace(emb["centrality"],
                                                 [[0,"#080810"],[0.3,"#6366f1"],[0.6,"#f472b6"],[1,"#fbbf24"]], "Centrality")])
        add_bridges(fig_cent)
        fig_cent.update_layout(title="Spectral Embedding — colored by Centrality")
        save_fig(fig_cent, "3d_embedding_centrality", 1200, 800)

    # ── 4.7 Time Series Plots (if events present) ──
    if len(sts) > 3:
        ticks = [s["t"] for s in sts]

        def ts_plot(key, title, color, filename):
            y = [s.get(key) for s in sts if key in s]
            if not y:
                return
            fig = go.Figure(go.Scatter(x=ticks[:len(y)], y=y, mode="lines", line_color=color, fill="tozeroy"))
            fig.update_layout(title=title, xaxis_title="Tick")
            save_fig(fig, filename, 900, 380)

        ts_plot("connectome_entropy", "Connectome Entropy", "#22d3ee", "ts_entropy")
        ts_plot("sie_v2_valence_01", "SIE v2 Valence", "#fbbf24", "ts_valence")
        ts_plot("vt_coverage", "VT Coverage", "#34d399", "ts_coverage")
        ts_plot("active_edges", "Active Edges", "#22d3ee", "ts_edges")
        ts_plot("b1_z", "Boundary Pulse (b1_z)", "#6366f1", "ts_b1z")
        ts_plot("adc_territories", "ADC Territory Count", "#f472b6", "ts_territories")

    # ── 5. Simple index HTML for easy browsing ──
    index_html = f"""<!DOCTYPE html><html><head><title>VDM Report — tick {m.get('tick','?')}</title>
    <style>body{{font-family:JetBrains Mono,sans-serif;background:#080810;color:#b8b8cc;padding:20px}}
    img{{max-width:100%;margin:20px 0;border:1px solid #1a1a2e;border-radius:8px}}</style></head><body>
    <h1>VDM Report — {m['source_file']}</h1>
    <pre>{summary}</pre>
    <h2>3D Embeddings</h2>
    <img src="images/3d_embedding_W.png"><br>
    <img src="images/3d_embedding_community.png"><br>
    <img src="images/3d_embedding_degree.png"><br>
    <h2>Other Plots</h2>
    <img src="images/degree_hist.png"><br>
    <img src="images/w_hist.png"><br>
    <img src="images/laplacian_spectrum.png"><br>
    <img src="images/territory_mass.png"><br>
    <img src="images/gauges.png"><br>
    </body></html>"""
    (output_dir / "report_index.html").write_text(index_html)
    print(f"   → report_index.html written (open in browser)")

    print(f"\n✅ FULL REPORT COMPLETE: {output_dir.resolve()}")
    print(f"   Open report_index.html or explore the images/ folder.")


# ====================== MAIN ======================

def main():
    parser = argparse.ArgumentParser(description="VDM Report Generator — Python-only dashboard replacement")
    parser.add_argument("h5_file", help="Path to .h5 state file")
    parser.add_argument("--events", "-e", help="Path to .jsonl event log", default=None)
    parser.add_argument("--output", "-o", help="Output directory (default: auto)", default=None)
    args = parser.parse_args()

    bundle = {"version": 1, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")}

    # Load data (exact same logic as original converter)
    bundle["state"] = load_h5(args.h5_file)
    if args.events:
        bundle["events"] = load_events(args.events)
    else:
        bundle["events"] = {"statuses": [], "say_events": []}

    # Output directory
    stem = Path(args.h5_file).stem
    if args.output:
        out_dir = Path(args.output)
    else:
        out_dir = Path(f"vdm_report_{stem}")
    out_dir.mkdir(parents=True, exist_ok=True)

    render_report(bundle, out_dir)


if __name__ == "__main__":
    main()