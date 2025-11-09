#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VDM Stats helpers — τ_int estimation, auto-binning, and blocked resampling.

Canon anchors (reference-only; no formulas duplicated here):
- Equations: VDM-E-132 (τ_int), VDM-E-133 (binning adequacy)
  Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-132
  Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-133
- KPIs: kpi-tau-int, kpi-binning-adequacy, kpi-resample-ci-stability
  Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int
  Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-binning-adequacy
  Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-resample-ci-stability

IO policy: production runs must route artifacts via common.io_paths.
This module computes metrics and returns Python objects; calling code decides logging.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple, Sequence, List, Dict
import math
import numpy as np

# Optional IO helper import (soft dependency)
try:
    from common.io_paths import write_log  # type: ignore
except Exception:  # pragma: no cover
    write_log = None  # type: ignore

__all__ = [
    "TauIntResult",
    "BlockedSeries",
    "JackknifeResult",
    "BootstrapResult",
    "estimate_tau_int",
    "effective_sample_size",
    "auto_block_size",
    "block_reduce",
    "jackknife_block",
    "bootstrap_block",
    "ci_from_samples",
    "ci_stability_curve",
]

@dataclass
class TauIntResult:
    tau_int: float
    window_lag: int
    n: int
    method: str = "sokal-window"
    notes: str = ""


@dataclass
class BlockedSeries:
    block_size: int
    n_blocks: int
    means: np.ndarray
    stderr: float


@dataclass
class JackknifeResult:
    mean: float
    std: float
    ci: Tuple[float, float]
    block_size: int
    n_blocks: int


@dataclass
class BootstrapResult:
    mean: float
    std: float
    ci: Tuple[float, float]
    block_size: int
    n_blocks: int
    n_resamples: int
    seed: Optional[int] = None


def _next_pow_two(n: int) -> int:
    """Return next power of two ≥ n."""
    return 1 if n <= 1 else 2 ** (int(n - 1).bit_length())


def _acf_fft(x: np.ndarray, max_lag: Optional[int] = None) -> np.ndarray:
    """
    Fast normalized autocorrelation using FFT (unbiased at lag 0).
    Returns rho[0:K+1], where rho[0] = 1.0 and K = max_lag or N-1.
    """
    x = np.asarray(x, dtype=np.float64)
    n = x.size
    if n < 2:
        return np.array([1.0], dtype=np.float64)
    x = x - x.mean()
    m = _next_pow_two(2 * n)
    fx = np.fft.rfft(x, m)
    s = np.fft.irfft(fx * np.conjugate(fx), m)[:n]
    var0 = s[0]
    if var0 == 0.0:
        rho = np.zeros(n, dtype=np.float64)
        rho[0] = 1.0
    else:
        rho = s / var0
    if max_lag is None or max_lag >= n:
        K = n - 1
    else:
        K = int(max_lag)
    return rho[: K + 1]


def estimate_tau_int(x: Sequence[float], c: float = 5.0, max_lag: Optional[int] = None) -> TauIntResult:
    """
    Estimate integrated autocorrelation time τ_int using a Sokal-style window.

    Reference anchors:
      - VDM-E-132 (τ_int): see Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-132
      - KPI kpi-tau-int: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int

    Algorithm:
      - Compute normalized ACF ρ(t) via FFT.
      - Accumulate τ_int = 0.5 + sum_{t=1..W} ρ(t), with window W grown until t > c · τ_int or ρ(t) ≤ 0.
    """
    x_arr = np.asarray(x, dtype=np.float64)
    n = x_arr.size
    if n == 0:
        return TauIntResult(tau_int=0.0, window_lag=0, n=0, notes="empty series")
    rho = _acf_fft(x_arr, max_lag=max_lag)
    tau = 0.5
    W = 0
    for t in range(1, rho.size):
        if rho[t] <= 0.0:
            break
        tau += float(rho[t])
        W = t
        if t > c * tau:
            break
    return TauIntResult(tau_int=float(tau), window_lag=int(W), n=int(n))


def effective_sample_size(n: int, tau_int: float) -> float:
    """
    Effective sample size N_eff = N / (2 τ_int).
    See KPI: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int
    """
    if tau_int <= 0:
        return float(n)
    return float(n) / (2.0 * float(tau_int))


def auto_block_size(tau: float, min_factor: float = 2.0) -> int:
    """
    Minimum adequate block size B = ceil(min_factor · τ_int).
    Anchor: Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-133
    KPI: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-binning-adequacy
    """
    if tau <= 0:
        return 1
    return int(math.ceil(min_factor * float(tau)))


def block_reduce(x: Sequence[float], block_size: int) -> BlockedSeries:
    """
    Reduce a correlated series by non-overlapping block means.
    Returns BlockedSeries with per-block means and standard error of the mean.
    """
    x_arr = np.asarray(x, dtype=np.float64)
    n = x_arr.size
    if n == 0:
        return BlockedSeries(block_size=int(block_size), n_blocks=0, means=np.array([], dtype=np.float64), stderr=float("nan"))
    B = max(1, int(block_size))
    n_blocks = n // B
    if n_blocks == 0:
        # not enough data for a full block
        return BlockedSeries(block_size=B, n_blocks=0, means=np.array([], dtype=np.float64), stderr=float("nan"))
    x_trim = x_arr[: n_blocks * B]
    means = x_trim.reshape(n_blocks, B).mean(axis=1)
    stderr = float(means.std(ddof=1) / math.sqrt(n_blocks)) if n_blocks > 1 else float("nan")
    return BlockedSeries(block_size=B, n_blocks=int(n_blocks), means=means, stderr=stderr)


def jackknife_block(x: Sequence[float], block_size: int, confidence: float = 0.95) -> JackknifeResult:
    """
    Blocked jackknife over non-overlapping blocks (J ≥ τ_int recommended).
    KPI: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-resample-ci-stability
    """
    bs = block_reduce(x, block_size)
    if bs.n_blocks <= 1:
        m = float(np.asarray(x, dtype=np.float64).mean()) if len(x) else float("nan")
        return JackknifeResult(mean=m, std=float("nan"), ci=(float("nan"), float("nan")), block_size=bs.block_size, n_blocks=bs.n_blocks)
    theta_i = bs.means
    theta_bar = float(theta_i.mean())
    m = bs.n_blocks
    # variance of jackknife pseudo-values
    var = (m - 1) * float(((theta_i - theta_bar) ** 2).mean())
    std = float(math.sqrt(var))
    z = _z_from_confidence(confidence)
    ci = (theta_bar - z * std, theta_bar + z * std)
    return JackknifeResult(mean=theta_bar, std=std, ci=ci, block_size=bs.block_size, n_blocks=bs.n_blocks)


def bootstrap_block(x: Sequence[float], block_size: int, n_resamples: int = 1000, seed: Optional[int] = None, confidence: float = 0.95) -> BootstrapResult:
    """
    Block bootstrap by resampling block means with replacement.
    KPI: Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-resample-ci-stability
    """
    bs = block_reduce(x, block_size)
    if bs.n_blocks == 0:
        m = float(np.asarray(x, dtype=np.float64).mean()) if len(x) else float("nan")
        return BootstrapResult(mean=m, std=float("nan"), ci=(float("nan"), float("nan")), block_size=bs.block_size, n_blocks=bs.n_blocks, n_resamples=int(n_resamples), seed=seed)
    rng = np.random.default_rng(seed)
    samples = np.empty(int(n_resamples), dtype=np.float64)
    for i in range(int(n_resamples)):
        idx = rng.integers(0, bs.n_blocks, size=bs.n_blocks)
        samples[i] = float(bs.means[idx].mean())
    mean = float(samples.mean())
    std = float(samples.std(ddof=1))
    ci = ci_from_samples(samples, confidence)
    return BootstrapResult(mean=mean, std=std, ci=ci, block_size=bs.block_size, n_blocks=bs.n_blocks, n_resamples=int(n_resamples), seed=seed)


def ci_from_samples(samples: Sequence[float], confidence: float = 0.95) -> Tuple[float, float]:
    """
    Percentile confidence interval (two-sided) for bootstrap samples.
    """
    lo = (1.0 - confidence) / 2.0
    hi = 1.0 - lo
    arr = np.asarray(samples, dtype=np.float64)
    return (float(np.quantile(arr, lo)), float(np.quantile(arr, hi)))


def ci_stability_curve(x: Sequence[float], block_sizes: Sequence[int], method: str = "jackknife", confidence: float = 0.95) -> List[Dict[str, float]]:
    """
    Compute CI width vs block size to support KPI stability windows.
    Returns a list of dict rows: {"block": B, "ci_lo": lo, "ci_hi": hi, "ci_width": w}.
    """
    rows: List[Dict[str, float]] = []
    for B in block_sizes:
        if method == "jackknife":
            r = jackknife_block(x, B, confidence=confidence)
            lo, hi = r.ci
        elif method == "bootstrap":
            r = bootstrap_block(x, B, n_resamples=1000, confidence=confidence)
            lo, hi = r.ci
        else:
            raise ValueError(f"unknown method: {method}")
        rows.append({"block": float(B), "ci_lo": float(lo), "ci_hi": float(hi), "ci_width": float(hi - lo)})
    return rows


def _z_from_confidence(confidence: float) -> float:
    """Two-sided normal critical value for common confidence levels."""
    # common quantiles (approximate to 1e-4); avoids SciPy dependency
    table = {0.90: 1.64485363, 0.95: 1.95996398, 0.975: 2.24140273, 0.99: 2.57582930}
    if confidence in table:
        return table[confidence]
    # fallback: inverse error function approximation
    # uses Winitzki approximation for erfinv (sufficient for CI guidance)
    y = (confidence + 1.0) / 2.0  # target CDF for standard normal via erf
    # map to erf argument
    from math import sqrt, log
    # approximate inverse erf: erfinv(y) ≈ sign(y) * sqrt( sqrt(a + b*ln(1-y^2)) - (a + b*ln(1-y^2)) )
    # Not exact; used only when uncommon confidence requested.
    a = 0.147
    s = 2.0 * y - 1.0
    sgn = 1.0 if s >= 0 else -1.0
    s = abs(s)
    term = (2/(math.pi * a) + math.log(1 - s*s)/2.0)
    erfinv = sgn * math.sqrt(math.sqrt(term*term - math.log(1 - s*s)/a) - term)
    return math.sqrt(2.0) * erfinv


# End of module