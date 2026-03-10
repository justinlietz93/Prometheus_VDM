"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import json
from pathlib import Path

import numpy as np

# Import the real Connectome implementation (dense/validation mode)
from vdm_rt.core.sparse_connectome import Connectome


def Q_invariant(r: float, u: float, W: np.ndarray, t: float) -> np.ndarray:
    """Vectorized Q invariant from qfum_validate: ln|W| - ln|r - u W| - r t
    Numerically guarded to avoid division by zero.
    """
    eps = 1e-16
    W = np.asarray(W, dtype=np.float64)
    denom = (r - u * W)
    denom = np.where(np.abs(denom) < eps, np.copysign(eps, denom), denom)
    W_safe = np.where(np.abs(W) < eps, np.copysign(eps, W), W)
    return np.log(np.abs(W_safe)) - np.log(np.abs(denom)) - r * float(t)


def test_sum_Q_delta_records(tmp_path: Path) -> None:
    """Run one sparse Connectome.step on a small network, compute Δ(sum_i Q_i), and log results.

    This test is non-invasive: it uses the sparse-only runtime Connectome and does not modify any existing project source files.
    """
    # Small network for fast validation
    N = 32
    k = 4
    seed = 42

    # Physical mapping used in Q validator (documented in repo)
    r = 0.15
    u = 0.25
    t = 0.0

    # Construct connectome in sparse-only runtime mode
    conn = Connectome(N=N, k=k, seed=seed)

    # Snapshot initial node states
    W0 = conn.W.astype(np.float64).copy()
    Q0 = Q_invariant(r, u, W0, t)

    # Execute one update tick using the real runtime mapping
    conn.step(tick=int(t))

    # Snapshot after-step node states
    W1 = conn.W.astype(np.float64).copy()
    Q1 = Q_invariant(r, u, W1, t)

    # Aggregate diagnostics
    delta_vec = (Q1 - Q0)
    delta_sum = float(np.sum(delta_vec))

    payload = {
        "timestamp": int(t),
        "N": int(N),
        "k": int(k),
        "seed": int(seed),
        "r": float(r),
        "u": float(u),
        "t": float(t),
        "delta_sum_Q": delta_sum,
        "delta_max_abs": float(np.max(np.abs(delta_vec))),
        "W0_mean": float(np.mean(W0)),
        "W1_mean": float(np.mean(W1)),
        "W0_min": float(np.min(W0)),
        "W1_max": float(np.max(W1)),
    }

    # Write JSON log to derivation outputs (matches qfum_validate layout)
    # Determine repo root from this file's path
    repo_root = Path(__file__).resolve().parents[4]
    out_dir = repo_root / "derivation" / "code" / "outputs" / "logs" / "conservation_law"
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = out_dir / f"flux_test_{int(t)}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # Pass if we successfully wrote the log and computed the residual (non-invasive observation)
    assert fname.exists()
