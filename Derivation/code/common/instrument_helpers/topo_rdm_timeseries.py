# -*- coding: utf-8 -*-
"""
Topo-RDM time-series → ridge skeleton helpers (instrument_helpers)

Provides minimal, dependency-light utilities to extract ridge points from raw
time-series without requiring an external DSI pipeline.

Exposed API
- read_timeseries_csv(path): read (t, h) from CSV with headers ["t","strain"] or ["time","h"].
- ridge_points_from_timeseries(t, h, params): return Nx2 array of [tau, f].

Notes
- Uses a Hann-window STFT and per-frame local maxima selection.
- Tunable via params["stft"]: {nperseg, noverlap, freq_max, top_k, power_quantile}.
- Keep usage lightweight; this is a meter helper, not a production TF toolkit.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

__all__ = ["read_timeseries_csv", "ridge_points_from_timeseries"]


def read_timeseries_csv(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    """
    Read raw time-series from CSV.
    Accept headers: ['t','strain'] or ['time','h'].
    Fallback: first two numeric columns.
    Returns (t, h) as 1D arrays of equal length.
    """
    tt: List[float] = []
    hh: List[float] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            raise RuntimeError("Empty CSV for time-series")
        h = [s.strip().lower() for s in headers]
        idx_t = None
        idx_h = None
        for i, name in enumerate(h):
            if name in ("t", "time", "sec", "seconds"):
                idx_t = i
            if name in ("h", "strain", "residual"):
                idx_h = i
        for row in reader:
            if not row:
                continue
            try:
                if idx_t is not None and idx_h is not None:
                    t = float(row[idx_t])
                    hv = float(row[idx_h])
                else:
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
                    t, hv = nums[0], nums[1]
                if np.isfinite(t) and np.isfinite(hv):
                    tt.append(t)
                    hh.append(hv)
            except Exception:
                continue
    if len(tt) < 4:
        raise RuntimeError("Too few time-series samples (<4)")
    t_arr = np.asarray(tt, dtype=float)
    h_arr = np.asarray(hh, dtype=float)
    # remove NaN/Inf
    mask = np.isfinite(t_arr) & np.isfinite(h_arr)
    t_arr = t_arr[mask]
    h_arr = h_arr[mask]
    # ensure strictly increasing time (stable STFT)
    order = np.argsort(t_arr)
    t_arr = t_arr[order]
    h_arr = h_arr[order]
    return t_arr, h_arr


def _hann_window(n: int) -> np.ndarray:
    if n <= 1:
        return np.ones(max(1, n), dtype=float)
    m = np.arange(n, dtype=float)
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * m / float(n - 1))


def _stft_frames(t: np.ndarray, x: np.ndarray, nperseg: int, noverlap: int) -> Tuple[List[np.ndarray], np.ndarray]:
    """
    Minimal STFT frame generator (real-valued).
    Returns list of frames (each length nperseg) and array of frame center times.
    """
    N = int(nperseg)
    S = int(max(0, min(noverlap, nperseg - 1)))
    step = N - S
    frames: List[np.ndarray] = []
    centers: List[float] = []
    i = 0
    L = len(x)
    while i + N <= L:
        seg = x[i : i + N]
        frames.append(seg.copy())
        tc = 0.5 * (t[i] + t[i + N - 1])
        centers.append(tc)
        i += step
    return frames, np.asarray(centers, dtype=float)


def ridge_points_from_timeseries(t: np.ndarray, h: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
    """
    Compute simple ridge points from raw time-series by:
    - detrending (mean subtraction)
    - STFT with Hann window
    - per-frame local maxima selection (top-k and/or power quantile)

    Returns Nx2 array [tau, f], with tau = ln((t_c - t_min + eps)/Tspan) (dimensionless).
    Config under params.get("stft", {}):
      nperseg (int, default 256)
      noverlap (int, default nperseg//2)
      freq_max (float, default +inf)
      top_k (int, default 3)
      power_quantile (float in [0,1], default 0.95)
    """
    t = np.asarray(t, dtype=float)
    x = np.asarray(h, dtype=float)
    if t.size != x.size:
        raise ValueError("t and h must have same length")
    if t.size < 8:
        raise RuntimeError("Too few samples for STFT (<8)")
    # Detrend (simple)
    x = x - float(np.mean(x))
    # Sampling interval
    dt = float(np.median(np.diff(t)))
    if not (np.isfinite(dt) and dt > 0):
        raise RuntimeError("Invalid or non-uniform time base")
    # STFT settings
    st = dict(params.get("stft", {}))
    nperseg = int(st.get("nperseg", 256))
    noverlap = int(st.get("noverlap", max(0, nperseg // 2)))
    freq_max = float(st.get("freq_max", np.inf))
    top_k = int(st.get("top_k", 3))
    power_quantile = float(st.get("power_quantile", 0.95))
    # Build frames and spectrum bins
    frames, centers = _stft_frames(t, x, nperseg=nperseg, noverlap=noverlap)
    if len(frames) == 0:
        raise RuntimeError("No STFT frames produced (check nperseg/noverlap vs series length)")
    win = _hann_window(nperseg)
    f_bins = np.fft.rfftfreq(nperseg, d=dt)
    use_idx = np.arange(f_bins.size)
    if np.isfinite(freq_max):
        use_idx = np.where(f_bins <= freq_max)[0]
        if use_idx.size == 0:
            use_idx = np.arange(f_bins.size)
    # Normalize time to dimensionless tau
    t0 = float(t[0])
    Tspan = float(max(t[-1] - t[0], 1e-9))
    eps_t = 1e-9
    pts_tau: List[float] = []
    pts_f: List[float] = []
    for frame, tc in zip(frames, centers):
        X = np.fft.rfft(frame * win, n=nperseg)
        A = np.abs(X)
        A = A[use_idx]
        if A.size < 3:
            continue
        # local maxima
        lm = (A[1:-1] > A[:-2]) & (A[1:-1] >= A[2:])
        pk_idx = np.where(lm)[0] + 1
        if pk_idx.size == 0:
            pk_idx = np.array([int(np.argmax(A))], dtype=int)
        # threshold by quantile
        try:
            thr = float(np.quantile(A[pk_idx], power_quantile)) if pk_idx.size > 0 else 0.0
        except Exception:
            thr = 0.0
        strong = pk_idx[A[pk_idx] >= thr] if pk_idx.size > 0 else pk_idx
        if strong.size == 0:
            strong = pk_idx
        # take top_k strongest
        order = np.argsort(A[strong])[::-1]
        keep = strong[order[: max(1, top_k)]]
        for ki in keep:
            f_val = float(f_bins[use_idx][int(ki)])
            tau_val = math.log(max((tc - t0), eps_t) / Tspan)
            pts_tau.append(tau_val)
            pts_f.append(f_val)
    if len(pts_tau) < 4:
        raise RuntimeError("Ridge extraction produced too few points (<4); adjust STFT/topology params")
    return np.column_stack([np.asarray(pts_tau, dtype=float), np.asarray(pts_f, dtype=float)])