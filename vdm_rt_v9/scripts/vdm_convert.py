#!/usr/bin/env python3
"""
VDM State → Dashboard JSON Converter
=====================================
Converts H5 state files + optional JSONL event logs into a single JSON
bundle that the VDM Dashboard HTML viewer can consume.

Usage:
    python vdm_convert.py state_22260.h5 [--events utd_events.jsonl] [-o dashboard_data.json]

Requires: numpy, scipy, h5py
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import h5py
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import eigsh
from scipy.sparse.csgraph import connected_components


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
    from scipy.cluster.vq import kmeans2, whiten
    X = np.array(vecs)[:, 1:k+1].astype(np.float64)
    X = whiten(X)
    # Retry k-means a few times for stability
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
    m = len(col_idx)  # total edges (directed count)
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
    """Find cross-community edges, subsampled, with 3D coordinates."""
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
    # Subsample if too many
    if len(bridges) > max_bridges:
        idx = rng.choice(len(bridges), size=max_bridges, replace=False)
        bridges = [bridges[ii] for ii in idx]
    return bridges


def eigenvector_centrality(row_ptr, col_idx, N, tol=1e-6, max_iter=100):
    """Power-iteration eigenvector centrality (cheap approximation)."""
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
    """Compute spectral embedding from graph Laplacian."""
    data = np.ones(len(col_idx), dtype=np.float32)
    A = csr_matrix((data, col_idx, row_ptr), shape=(N, N))
    degrees = np.array(A.sum(axis=1)).ravel()

    # Normalized Laplacian: L_norm = I - D^{-1/2} A D^{-1/2}
    d_inv_sqrt = np.zeros(N)
    mask = degrees > 0
    d_inv_sqrt[mask] = 1.0 / np.sqrt(degrees[mask])
    D_inv_sqrt = csr_matrix((d_inv_sqrt, (np.arange(N), np.arange(N))), shape=(N, N))
    L_norm = csr_matrix(np.eye(N)) - D_inv_sqrt @ A @ D_inv_sqrt

    k = min(n_components + 1, N - 2)
    try:
        vals, vecs = eigsh(L_norm, k=k, which='SM', tol=1e-6)
        # Sort by eigenvalue
        order = np.argsort(vals)
        vals = vals[order]
        vecs = vecs[:, order]
    except Exception as e:
        print(f"  Warning: eigsh failed ({e}), using random embedding", file=sys.stderr)
        vals = np.zeros(k)
        vecs = np.random.randn(N, k).astype(np.float32)

    return vals.tolist(), vecs.tolist()


def compute_laplacian_spectrum(row_ptr, col_idx, N, k=20):
    """First k eigenvalues of the normalized Laplacian."""
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
    """Load H5 state file and compute all derived quantities."""
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

    # Degree distribution (histogram)
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

    # Gini coefficient
    gini_degree = gini(degrees)
    gini_w = gini(W)

    # Connectome entropy
    p = degrees / degrees.sum()
    p = p[p > 0]
    connectome_entropy = float(-np.sum(p * np.log2(p)))

    # Connected components
    data = np.ones(len(col_idx), dtype=np.float32)
    A = csr_matrix((data, col_idx, row_ptr), shape=(N, N))
    n_components, _ = connected_components(A, directed=False)

    print(f"  Gini(degree)={gini_degree:.4f}, Gini(W)={gini_w:.4f}, components={n_components}")

    # Spectral embedding (subsample for performance if N > 5000)
    print("  Computing spectral embedding...")

    # Eigenvector centrality on full graph
    print("  Computing eigenvector centrality...")
    ev_cent = eigenvector_centrality(row_ptr, col_idx, N)

    if N > 8000:
        # Subsample for embedding visualization
        sub_idx = np.random.default_rng(42).choice(N, size=5000, replace=False)
        sub_idx.sort()
        # Build subgraph
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

        # Communities from eigenvectors
        n_comm = min(8, sub_N - 1)
        print(f"  Computing spectral communities (k={n_comm})...")
        comm_labels = spectral_communities(eigenvectors, k=n_comm)

        # Modularity
        print("  Computing modularity...")
        modularity = compute_modularity(sub_row_ptr, sub_col_idx, comm_labels, sub_N)

        # Subsample the eigenvectors further for JSON size
        embed_idx = np.linspace(0, sub_N - 1, min(sub_N, 3000), dtype=int)
        embed_idx_set = set(embed_idx.tolist())

        # Bridge edges
        print("  Finding bridge edges...")
        bridges_raw = find_bridge_edges(sub_row_ptr, sub_col_idx, comm_labels,
                                         None, embed_idx_set, max_bridges=400)
        # Convert bridge endpoints to embed_idx positions for coordinate lookup
        embed_idx_map = {old: pos for pos, old in enumerate(embed_idx)}
        bridge_lines = []
        for (a, b) in bridges_raw:
            if a in embed_idx_map and b in embed_idx_map:
                ia, ib = embed_idx_map[a], embed_idx_map[b]
                bridge_lines.append([ia, ib])

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

        # Communities
        n_comm = min(8, N - 1)
        print(f"  Computing spectral communities (k={n_comm})...")
        comm_labels = spectral_communities(eigenvectors, k=n_comm)

        # Modularity
        print("  Computing modularity...")
        modularity = compute_modularity(row_ptr, col_idx, comm_labels, N)

        embed_idx = np.linspace(0, N - 1, min(N, 3000), dtype=int)
        embed_idx_set = set(embed_idx.tolist())

        # Bridge edges
        print("  Finding bridge edges...")
        bridges_raw = find_bridge_edges(row_ptr, col_idx, comm_labels,
                                         None, embed_idx_set, max_bridges=400)
        embed_idx_map = {old: pos for pos, old in enumerate(embed_idx)}
        bridge_lines = []
        for (a, b) in bridges_raw:
            if a in embed_idx_map and b in embed_idx_map:
                ia, ib = embed_idx_map[a], embed_idx_map[b]
                bridge_lines.append([ia, ib])

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

    # Laplacian spectrum
    print("  Computing Laplacian spectrum...")
    lap_spectrum = compute_laplacian_spectrum(row_ptr, col_idx, N, k=20)

    # ADC territories
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

    # Extract tick from filename if possible
    stem = Path(path).stem
    tick = None
    for part in stem.split("_"):
        try:
            tick = int(part)
            break
        except ValueError:
            continue

    # Spectral gap ratio
    if len(eigenvalues) > 2 and eigenvalues[2] > 1e-10:
        spectral_gap_ratio = float(eigenvalues[1] / eigenvalues[2])
    else:
        spectral_gap_ratio = 0.0

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
    """Load JSONL event log and extract time series."""
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
                    for key in [
                        "neurons", "phase", "cohesion_components",
                        "vt_coverage", "vt_entropy", "connectome_entropy",
                        "active_edges", "b1_z", "adc_territories",
                        "sie_valence_01", "sie_v2_valence_01",
                        "sie_v2_reward_mean", "sie_total_reward",
                        "ute_in_count", "ute_text_count",
                        "homeostasis_pruned", "homeostasis_bridged",
                    ]:
                        if key in p:
                            entry[key] = p[key]
                    statuses.append(entry)

                elif p.get("type") == "say":
                    say_events.append({
                        "t": p.get("t", obj.get("t", 0)),
                        "text": p.get("msg", p.get("text", ""))[:200],
                    })

            elif obj.get("type") == "macro" and obj.get("macro") == "status":
                args = obj.get("args", {})
                if "t" in args:
                    entry = {"t": args["t"]}
                    for key in [
                        "neurons", "cohesion_components", "vt_coverage",
                        "vt_entropy", "connectome_entropy", "active_edges",
                        "ute_in_count", "ute_text_count",
                    ]:
                        if key in args:
                            entry[key] = args[key]
                    statuses.append(entry)

    # Deduplicate by tick — prefer the entry with more fields
    by_tick = {}
    for s in statuses:
        t = s["t"]
        if t not in by_tick or len(s) > len(by_tick[t]):
            by_tick[t] = s
    unique = list(by_tick.values())
    unique.sort(key=lambda x: x["t"])

    print(f"  {len(unique)} status events, {len(say_events)} say events")
    return {"statuses": unique, "say_events": say_events}


def main():
    parser = argparse.ArgumentParser(description="VDM State → Dashboard JSON")
    parser.add_argument("h5_file", help="Path to H5 state file")
    parser.add_argument("--events", "-e", help="Path to JSONL event log", default=None)
    parser.add_argument("--output", "-o", help="Output JSON path", default=None)
    args = parser.parse_args()

    bundle = {"version": 1, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")}

    # Load H5
    bundle["state"] = load_h5(args.h5_file)

    # Load events if provided
    if args.events:
        bundle["events"] = load_events(args.events)
    else:
        bundle["events"] = {"statuses": [], "say_events": []}

    # Output path
    if args.output:
        out_path = args.output
    else:
        stem = Path(args.h5_file).stem
        out_path = f"vdm_dashboard_{stem}.json"

    print(f"Writing {out_path}...")
    with open(out_path, "w") as f:
        json.dump(bundle, f)

    size_mb = Path(out_path).stat().st_size / 1024 / 1024
    print(f"Done. Output: {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
