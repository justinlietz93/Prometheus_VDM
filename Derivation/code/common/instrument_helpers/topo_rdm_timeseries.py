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
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

__all__ = ["read_timeseries_csv", "read_timeseries_gwpy", "ridge_points_from_timeseries"]


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


def read_timeseries_gwpy(channel: str, start: any, end: any) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load a time-series via GWPy and return (t, h) as float arrays.
    Preferred order:
      1) Attempt NDS/frames via TimeSeries.get(channel, start, end).
      2) Fallback to GWOSC open data via TimeSeries.fetch_open_data(ifo, start, end, tag=?).

    - channel: e.g., "H1:GWOSC-4KHZ_R1_STRAIN" or "H1:TEST-CHANNEL"
    - start, end: GPS seconds (float/int) or ISO8601 strings (GWPy/astropy-friendly)

    This import is optional; only done when using this helper.
    """
    try:
        from gwpy.timeseries import TimeSeries as _GWTimeSeries  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "GWPy is not available. Install 'gwpy' (pip install gwpy) or provide --timeseries_csv instead."
        ) from e

    # Helper: parse "IFO:GWOSC-4KHZ_R1_STRAIN" → (ifo, sample_rate, version)
    # sample_rate is mapped from the common GWOSC tags: 1,2,4,8,16,32 kHz → 1024,2048,4096,8192,16384,32768
    def _parse_ifo_sr_ver(s: str) -> Tuple[str, int | None, str | None]:
        ifo = "H1"
        sr: int | None = None
        ver: str | None = None

        if ":" in s:
            parts = s.split(":", 1)
            if parts[0] in ("H1", "L1", "V1", "K1"):
                ifo = parts[0]
            rest = parts[1]
        else:
            rest = s

        # Strip trailing "_STRAIN" if present
        if rest.endswith("_STRAIN"):
            rest = rest[:-7]

        # Only parse if GWOSC tag appears
        if "GWOSC" in rest:
            # Examples: "GWOSC-4KHZ_R1", "GWOSC-16KHZ_R1"
            # Extract KHZ code and release R#
            # KHZ mapping to power-of-two sample-rates
            KHZ_MAP = {
                "1": 1024, "2": 2048, "4": 4096, "8": 8192, "16": 16384, "32": 32768
            }
            # Find "<num>KHZ"
            m = re.search(r"(\d+)\s*KHZ", rest, flags=re.IGNORECASE)
            if m:
                num = m.group(1)
                sr = KHZ_MAP.get(num, None)
                if sr is None:
                    # Fallback if an uncommon tag is used
                    try:
                        sr = int(num) * 1000
                    except Exception:
                        sr = None
            # Find "_R\d+" release
            m2 = re.search(r"_R(\d+)", rest, flags=re.IGNORECASE)
            if m2:
                ver = f"R{m2.group(1)}".upper()

        return ifo, sr, ver

    # First try NDS/frames via .get (may require nds2)
    try:
        ts = _GWTimeSeries.get(channel, start, end)
    except ModuleNotFoundError as e:
        # nds2 missing or similar → try GWOSC open data
        if "nds2" not in str(e):
            raise
        ifo, sr, ver = _parse_ifo_sr_ver(channel)
        # Ensure numeric GPS where possible
        try:
            t0 = float(start)
            t1 = float(end)
        except Exception:
            raise RuntimeError("GWOSC fetch requires numeric GPS times for start/end") from e
        try:
            kw = {"cache": True}
            if sr is not None:
                kw["sample_rate"] = sr
            if ver is not None:
                kw["version"] = ver
            ts = _GWTimeSeries.fetch_open_data(ifo, t0, t1, **kw)
        except Exception as e2:
            raise RuntimeError(f"GWOSC fetch_open_data failed for {ifo} [{t0},{t1}] sample_rate={sr} version={ver}: {e2}") from e2
    except Exception:
        # Any other error from .get → attempt GWOSC as well
        ifo, sr, ver = _parse_ifo_sr_ver(channel)
        try:
            t0 = float(start); t1 = float(end)
        except Exception as e3:
            raise RuntimeError("GWOSC fetch requires numeric GPS times for start/end") from e3
        kw = {"cache": True}
        if sr is not None:
            kw["sample_rate"] = sr
        if ver is not None:
            kw["version"] = ver
        ts = _GWTimeSeries.fetch_open_data(ifo, t0, t1, **kw)

    # Convert to numpy arrays
    try:
        t = ts.times.value  # astropy.Time-like
    except Exception:
        # Fallback: reconstruct from t0 and dt/sample_rate if present
        try:
            dt = float(ts.dt.value) if hasattr(ts, "dt") else 1.0 / float(ts.sample_rate.value)
        except Exception:
            dt = 1.0
        t0 = float(ts.t0.value) if hasattr(ts, "t0") else 0.0
        t = t0 + np.arange(len(ts.value), dtype=float) * dt

    h = np.asarray(ts.value, dtype=float)
    t = np.asarray(t, dtype=float)

    # Clean non-finite and sort
    mask = np.isfinite(t) & np.isfinite(h)
    t = t[mask]
    h = h[mask]
    order = np.argsort(t)
    return t[order], h[order]


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

    # Optional time window cropping using params["window"] = [t_start_rel, t_end_rel] (seconds relative to t[0])
    t_ref = float(t[0])
    Tspan_ref = float(max(t[-1] - t[0], 1e-9))
    win_cfg = params.get("window", None)
    if isinstance(win_cfg, (list, tuple)) and len(win_cfg) == 2:
        try:
            w0 = float(win_cfg[0]); w1 = float(win_cfg[1])
            if np.isfinite(w0) and np.isfinite(w1) and (w1 > w0):
                tmin = float(t[0]) + w0
                tmax = float(t[0]) + w1
                sel = (centers >= tmin) & (centers <= tmax)
                if np.any(sel):
                    idx_sel = np.where(sel)[0]
                    frames = [frames[i] for i in idx_sel]
                    centers = centers[sel]
                    t_ref = tmin
                    Tspan_ref = float(max(min(t[-1], tmax) - tmin, 1e-9))
        except Exception:
            # non-fatal: ignore malformed window config
            pass

    if len(frames) == 0:
        raise RuntimeError("No STFT frames produced (check nperseg/noverlap vs series length and window)")

    win = _hann_window(nperseg)
    f_bins = np.fft.rfftfreq(nperseg, d=dt)
    use_idx = np.arange(f_bins.size)
    if np.isfinite(freq_max):
        use_idx = np.where(f_bins <= freq_max)[0]
        if use_idx.size == 0:
            use_idx = np.arange(f_bins.size)
    # Normalize time to dimensionless tau using reference window
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
            tau_val = math.log(max((tc - t_ref), eps_t) / Tspan_ref)
            pts_tau.append(tau_val)
            pts_f.append(f_val)
    if len(pts_tau) < 4:
        raise RuntimeError("Ridge extraction produced too few points (<4); adjust STFT/topology params or window")
    return np.column_stack([np.asarray(pts_tau, dtype=float), np.asarray(pts_f, dtype=float)])