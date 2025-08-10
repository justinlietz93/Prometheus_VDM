# fum_structural_homeostasis.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import numpy as np

# Rule reference (Blueprint)
# - Rule 4 / 4.1: EHTP + Global Directed Synaptic Plasticity (GDSP)
#   Stage‑1 cohesion repair and light, adaptive pruning. Subquadratic; act
#   only on loci/components provided by the runtime, not full graph scans.
#
# Time complexity:
# - O(N + M) to get component labels upstream (Connectome already computes count).
# - Bridging: O(B * k) where B is number of bridges (small), k is per‑node neighbor cap.
# - Pruning: O(M) over active edges via masked thresholding (vectorized).
#
# Formulae:
# - S_ij = ReLU(Δalpha_i) * ReLU(Δalpha_j) − λ * |Δomega_i − Δomega_j|
# - Prune if |E_ij| < prune_threshold (adaptive fraction of |E| mean)
#
# Parameters:
# - bundle_size: number of parallel edges to reinforce a bridge (encourages fusion)
# - lambda_omega: penalty weight in S_ij
# - prune_factor: fraction of mean(|E|) below which edges are removed


def _compute_affinity(a: np.ndarray, w: np.ndarray, lambda_omega: float) -> np.ndarray:
    """Compute void‑affinity matrix S_ij from Δalpha (a) and Δomega (w)."""
    a_relu = np.maximum(0.0, a.astype(np.float32))
    w = w.astype(np.float32)
    # S_ij = relu(a_i) * relu(a_j) − λ |Δω_i − Δω_j|
    S = a_relu[:, None] * a_relu[None, :] - lambda_omega * np.abs(w[:, None] - w[None, :])
    np.fill_diagonal(S, -np.inf)
    return S


def _select_bridge_pairs(labels: np.ndarray,
                         S: np.ndarray,
                         degrees: np.ndarray,
                         bundle_size: int = 3):
    """
    Choose bridge node pairs (u,v) across different components by maximizing S_ij.
    Tie‑break to prefer strong→weak: high degree u, low degree v.
    Returns a list of (u, v) pairs of length up to bundle_size per component pair.
    """
    pairs = []
    unique = np.unique(labels)
    if unique.size < 2:
        return pairs

    # Generate candidate component pairs (greedy: connect largest to others)
    # Rank components by size descending.
    comp_sizes = {c: int((labels == c).sum()) for c in unique}
    order = sorted(unique, key=lambda c: comp_sizes[c], reverse=True)
    root = order[0]
    others = order[1:]

    for tgt in others:
        idx_root = np.where(labels == root)[0]
        idx_tgt = np.where(labels == tgt)[0]
        if idx_root.size == 0 or idx_tgt.size == 0:
            continue

        # Submatrix of S over the boundary (root x tgt)
        S_block = S[np.ix_(idx_root, idx_tgt)]
        if np.all(~np.isfinite(S_block)):
            continue

        # For bundle, iteratively pick max, then suppress chosen rows/cols lightly
        local_pairs = []
        S_copy = S_block.copy()
        for _ in range(bundle_size):
            i_flat = np.nanargmax(S_copy)  # works since -inf stays < any finite
            r, c = divmod(i_flat, S_copy.shape[1])
            u = idx_root[r]
            v = idx_tgt[c]
            local_pairs.append((u, v))
            # soft suppression to diversify selection
            S_copy[r, :] = -np.inf
            S_copy[:, c] = -np.inf
            if not np.isfinite(S_copy).any():
                break

        # Apply strong→weak preference reordering (optional)
        local_pairs.sort(key=lambda p: (-degrees[p[0]], degrees[p[1]]))
        pairs.extend(local_pairs)

    return pairs


def perform_structural_homeostasis(connectome,
                                   labels: np.ndarray,
                                   d_alpha: np.ndarray,
                                   d_omega: np.ndarray,
                                   lambda_omega: float = 0.1,
                                   bundle_size: int = 3,
                                   prune_factor: float = 0.10):
    """
    Perform cohesion healing (bridging) and light pruning on the runtime connectome.

    Args:
        connectome: fum_rt.core.connectome.Connectome instance (current runtime).
        labels: np.ndarray of component labels per node for the ACTIVE subgraph.
        d_alpha: np.ndarray Δalpha (delta_re_vgsp) for current tick.
        d_omega: np.ndarray Δomega (delta_gdsp) for current tick.
        lambda_omega: float; S_ij penalty weight.
        bundle_size: int; number of parallel edges to reinforce each bridge.
        prune_factor: float; fraction of mean(|E|) used as adaptive pruning threshold.

    Effects:
        - Modifies connectome.A (adjacency) by adding symmetric bridge edges between
          components using S_ij max rule.
        - Updates connectome.E to follow nodes after topology change.
        - Prunes edges whose |E_ij| < prune_threshold (adaptive).
    """
    N = connectome.N
    if N <= 1:
        return

    # 1) Pruning (adaptive to current edge weights)
    E = connectome.E  # float32 N x N but sparse via threshold
    if E.size > 0:
        mean_w = float(np.mean(np.abs(E[E != 0]))) if np.any(E != 0) else 0.0
        prune_threshold = prune_factor * mean_w if mean_w > 0 else 0.0
        if prune_threshold > 0.0:
            mask_keep = np.abs(E) >= prune_threshold
            # keep symmetry shape
            connectome.A = np.where(mask_keep, connectome.A, 0).astype(np.int8)
            connectome.E = np.where(mask_keep, E, 0.0).astype(np.float32)

    # 2) Bridging if multiple components
    unique = np.unique(labels) if labels is not None else np.array([0], dtype=int)
    if unique.size > 1:
        # Compute S_ij over current nodes
        S = _compute_affinity(d_alpha, d_omega, lambda_omega=lambda_omega)

        # degrees for strong→weak preference
        degrees = connectome.A.sum(axis=1).astype(np.int32)

        bridge_pairs = _select_bridge_pairs(labels, S, degrees, bundle_size=bundle_size)

        # Add symmetric edges for selected pairs
        for u, v in bridge_pairs:
            if u == v:
                continue
            connectome.A[u, v] = 1
            connectome.A[v, u] = 1

        # Edge weights follow nodes (reuse existing vectorized function)
        connectome.E = (np.outer(connectome.W, connectome.W) * connectome.A).astype(np.float32)