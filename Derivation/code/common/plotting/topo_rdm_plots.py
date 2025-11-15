# -*- coding: utf-8 -*-
"""
Topo-RDM plotting helpers (canonical plotting location)

Purpose
- Provide reusable plotting utilities for the Topological Ringdown Meter (Topo-RDM)
- Keep all plotting under Derivation/code/common/plotting and import from runners
- Save artifacts via io_paths through the common plotting package

Anchors (reference only; do not duplicate canon content)
- DSI proposal: Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md
- Validation metrics: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md
- Equations: Derivation/z.CANONICAL_Equations/00_EQUATIONS.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt

from .helpers import plot_multi_panel  # canonical multi-panel plotting and io routing
from .types import PlotSpec


def plot_topo_rdm_panel(
    points: np.ndarray,
    eps: np.ndarray,
    b1_obs: np.ndarray,
    null_curves: Optional[np.ndarray],
    q_mask: np.ndarray,
    z_max: float,
    stable_band_len: int,
    fp_rate: float,
    domain: str = "cosmology",
    slug: str = "topo_rdm_panel",
    failed: bool = False,
) -> Path:
    """
    Render a two-panel Topo-RDM figure and save via canonical routing.

    Left: ridge skeleton scatter (tau vs f)
    Right: beta1(eps) with optional null bands and FDR-kept points overlay

    Parameters
    - points: (N,2) array of [tau, f]
    - eps: (M,) filtration radii
    - b1_obs: (M,) observed beta1 curve
    - null_curves: (S, M) null beta1 curves (optional). When provided,
      draws mean ± 2σ band and mean line.
    - q_mask: (M,) boolean mask where FDR keeps the point (q ≤ α)
    - z_max: scalar z-score of max beta1 against null maxima
    - stable_band_len: length of longest consecutive FDR-kept segment with z ≥ gate
    - fp_rate: empirical false positive rate from null maxima (≈ fraction over threshold)
    - domain: artifact domain (default "cosmology")
    - slug: artifact slug (basename without timestamp)
    - failed: whether to route under failed_runs/

    Returns
    - Path to the saved PNG figure
    """
    # Build panel functions to be rendered by the common plotting helpers
    def _panel_left(ax: plt.Axes) -> None:
        ax.scatter(points[:, 0], points[:, 1], s=8, alpha=0.7, c="k")
        ax.set_xlabel("τ = ln(θ/θ0)")
        ax.set_ylabel("frequency f (arb)")
        ax.set_title("Ridge skeleton")

    def _panel_right(ax: plt.Axes) -> None:
        ax.plot(eps, b1_obs, label="β1(obs)", color="#1f77b4")
        if null_curves is not None and getattr(null_curves, "size", 0) > 0:
            mu = np.mean(null_curves, axis=0)
            sd = np.std(null_curves, axis=0, ddof=1)
            ax.fill_between(eps, mu - 2 * sd, mu + 2 * sd, color="#ff7f0e", alpha=0.2, label="null ±2σ")
            ax.plot(eps, mu, color="#ff7f0e", lw=1.0, alpha=0.9, label="null mean")
        if q_mask is not None and q_mask.size == b1_obs.size:
            ax.plot(eps[q_mask], b1_obs[q_mask], "o", ms=3.0, color="#2ca02c", label="FDR-kept")
        ax.set_xlabel("ε (filtration radius)")
        ax.set_ylabel("β1")
        title2 = f"β1(ε), z_max≈{float(z_max):.2f}, stable_band_len={int(stable_band_len)}, FP≈{float(fp_rate):.3f}"
        ax.set_title(title2)
        ax.legend(loc="best", fontsize=8)

    spec = PlotSpec(
        domain=domain,
        name=slug,  # keep slug exact for artifact naming
        title=None,
        size=(7.8, 4.2),
        tight=True,
        legend=False,
        style="light",
        meta={"z_max": float(z_max), "stable_band_len": int(stable_band_len), "fp_rate": float(fp_rate)},
    )

    path, _ = plot_multi_panel([_panel_left, _panel_right], spec, failed=failed, ncols=2)
    return path