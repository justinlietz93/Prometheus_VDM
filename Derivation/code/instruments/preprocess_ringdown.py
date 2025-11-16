#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic ringdown preprocessor → CSV (and optional ridges CSV).

Steps:
 - Window around t0: [t0 - t_pre, t0 + t_post]
 - Detrend (linear) and mean-remove
 - PSD (Welch) from pre-merger subwindow
 - Whiten via frequency-domain division by sqrt(Sn)
 - Zero-phase linear FIR band-pass (default 25–512 Hz)
 - Optional notch lines (not implemented by default)
 - Downsample after filtering (default 2048 Hz)
 - Emit CSV and JSON meta, optional ridges CSV from STFT maxima

Gating diagnostics (emitted in JSON):
 - whiteness_rho_max (max |ACF(τ)|, τ≠0 up to 1 s) and whiten_ok (≤ threshold)
 - band_ok (passband within [2/T, fs/2])
 - snr_ringdown = RMS_post / sigma_pre

Usage example:
  python preprocess_ringdown.py --in_csv data/gw150914_H1.csv --out_root outputs/gw150914_H1 \
    --fs 4096 --t0 1126259462.423 --t_pre 2.5 --t_post 2.5 --f_lo 25 --f_hi 512 \
    --psd_seg 1.0 --psd_olap 0.5 --down_fs 2048 --emit_ridges
"""

import argparse
import json
import math
import os
from typing import Tuple, Optional

import numpy as np
from numpy.fft import rfft, irfft, rfftfreq
from scipy import signal


def _ensure_parent(path: str) -> None:
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def welch_psd(x: np.ndarray, fs: float, seglen: float, overlap: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Welch PSD with fixed segment length and overlap (seconds).
    Returns (f, Pxx) one-sided density.
    """
    nperseg = max(8, int(round(seglen * fs)))
    noverlap = int(round(overlap * fs))
    f, Pxx = signal.welch(
        x,
        fs=fs,
        nperseg=nperseg,
        noverlap=noverlap,
        window="hann",
        detrend="constant",
        return_onesided=True,
        scaling="density",
    )
    return f, Pxx


def whiten(h: np.ndarray, fs: float, f_psd: np.ndarray, Pxx: np.ndarray, eps: float = 1e-24) -> np.ndarray:
    """
    Frequency-domain whitening: divide FFT by sqrt(PSD) interpolated to FFT bins.
    """
    H = rfft(h)
    freqs = rfftfreq(h.size, 1.0 / fs)
    Sn = np.interp(freqs, f_psd, Pxx, left=Pxx[0], right=Pxx[-1])
    Sn = np.maximum(Sn, eps)
    H_white = H / np.sqrt(Sn)
    # Ensure Hermitian symmetry via irfft (length preserved)
    return irfft(H_white, n=h.size)


def linear_fir_bandpass(x: np.ndarray, fs: float, f_lo: float, f_hi: float, numtaps: int = 1025) -> np.ndarray:
    """
    Zero-phase linear FIR band-pass with filtfilt to avoid phase distortion.
    """
    nyq = 0.5 * fs
    if not (0.0 < f_lo < f_hi < nyq):
        raise ValueError(f"Invalid band [{f_lo},{f_hi}] for fs={fs} (nyquist={nyq})")
    taps = signal.firwin(numtaps, [f_lo / nyq, f_hi / nyq], pass_zero=False, window="hann")
    # Zero-phase application
    y = signal.filtfilt(taps, [1.0], x, method="pad")
    return y


def _acf_max_abs(x: np.ndarray, fs: float, max_lag_s: float = 1.0) -> float:
    """
    Compute max absolute autocorrelation (excluding lag 0) up to max_lag_s.
    """
    n = x.size
    L = min(n - 1, int(round(max_lag_s * fs)))
    if L <= 0:
        return 0.0
    # Normalize to zero mean
    x0 = x - float(np.mean(x))
    # full correlation then extract positive lags [0..L]
    c = signal.correlate(x0, x0, mode="full", method="auto")
    mid = c.size // 2
    c_pos = c[mid : mid + L + 1]
    # Normalize by variance and sample count (biased)
    denom = c_pos[0] if c_pos[0] != 0 else 1.0
    rho = c_pos / denom
    if rho.size <= 1:
        return 0.0
    return float(np.max(np.abs(rho[1:])))


def stft_ridges(x: np.ndarray, fs: float, nperseg: int, noverlap: int, k_top: int = 3) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Top-k magnitude peaks per STFT frame as ridge samples (t,f,amp).
    """
    f, t, Z = signal.stft(
        x,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        detrend=False,
        return_onesided=True,
        boundary=None,
    )
    A = np.abs(Z)
    ridges = []
    for j in range(A.shape[1]):
        col = A[:, j]
        if k_top >= len(col):
            idx = np.argsort(col)[::-1]
        else:
            idx = np.argpartition(col, -k_top)[-k_top:]
            idx = idx[np.argsort(col[idx])[::-1]]
        for i in idx:
            ridges.append((t[j], f[i], float(col[i])))
    return np.asarray(ridges, dtype=float), (f, t, A)


def _downsample_poly(y: np.ndarray, fs: float, down_fs: float) -> Tuple[np.ndarray, float]:
    """
    Rational resampling via polyphase filtering, rebuild time grid linearly.
    """
    # Require integer ratio for resample_poly; approximate if necessary
    if down_fs >= fs:
        return y, fs
    # Compute integer ratio
    from math import gcd
    up = int(round(down_fs))
    down = int(round(fs))
    g = gcd(up, down)
    up //= g
    down //= g
    y2 = signal.resample_poly(y, up=up, down=down)
    N = y2.size
    return y2, down_fs


def _read_csv_t_h(path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Read CSV with header 't,h' or two-column numeric CSV (assumed t,h).
    """
    try:
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        if data.ndim == 1 and data.size >= 2:
            data = data.reshape(-1, 2)
    except Exception:
        data = np.loadtxt(path, delimiter=",")
        if data.ndim == 1 and data.size >= 2:
            data = data.reshape(-1, 2)
    t, h = data[:, 0].astype(float), data[:, 1].astype(float)
    return t, h


def main() -> None:
    ap = argparse.ArgumentParser(description="Deterministic ringdown preprocessor → CSV (+ optional ridges)")
    ap.add_argument("--in_csv", required=True, help="input CSV with columns t,h (seconds, strain)")
    ap.add_argument("--out_root", required=True, help="basename for outputs (directories created as needed)")
    ap.add_argument("--fs", type=float, required=True, help="sample rate [Hz]")
    ap.add_argument("--t0", type=float, required=True, help="peak or reference time [s] within the provided series timebase")
    ap.add_argument("--t_pre", type=float, default=4.0, help="seconds before t0")
    ap.add_argument("--t_post", type=float, default=4.0, help="seconds after t0")
    ap.add_argument("--f_lo", type=float, default=25.0, help="band-pass low cut [Hz]")
    ap.add_argument("--f_hi", type=float, default=512.0, help="band-pass high cut [Hz]")
    ap.add_argument("--psd_seg", type=float, default=1.0, help="Welch segment [s]")
    ap.add_argument("--psd_olap", type=float, default=0.5, help="Welch overlap [s]")
    ap.add_argument("--down_fs", type=float, default=2048.0, help="downsampled rate [Hz] after filtering")
    ap.add_argument("--emit_ridges", action="store_true", help="also compute ridges via STFT and write CSV")
    ap.add_argument("--ridges_top_k", type=int, default=3, help="top-k peaks per STFT frame")
    args = ap.parse_args()

    # IO
    t_raw, h_raw = _read_csv_t_h(args.in_csv)
    fs = float(args.fs)

    # Window selection around t0
    mask = (t_raw >= args.t0 - args.t_pre) & (t_raw <= args.t0 + args.t_post)
    if not np.any(mask):
        raise RuntimeError("Selected window contains no samples. Check t0 / t_pre / t_post.")
    t = t_raw[mask]
    h = h_raw[mask]

    # Detrend and mean-remove
    h = signal.detrend(h, type="linear")
    h -= float(np.mean(h))

    # PSD from pre-merger portion only
    pre_mask = (t < args.t0)
    h_pre_ref = h[pre_mask]
    if h_pre_ref.size < max(16, int(round(args.psd_seg * fs)) * 2):
        # Fallback: whole window if too short
        h_pre_ref = h
    f_psd, Pxx = welch_psd(h_pre_ref, fs=fs, seglen=args.psd_seg, overlap=args.psd_olap)

    # Whiten
    h_w = whiten(h, fs=fs, f_psd=f_psd, Pxx=Pxx, eps=1e-24)

    # Band-pass (zero-phase FIR)
    h_wbp = linear_fir_bandpass(h_w, fs=fs, f_lo=args.f_lo, f_hi=args.f_hi, numtaps=1025)

    # Downsample
    if args.down_fs and args.down_fs < fs:
        y_ds, fs_eff = _downsample_poly(h_wbp, fs=fs, down_fs=float(args.down_fs))
        # Rebuild time on uniform grid
        N = y_ds.size
        t_ds = np.linspace(t[0], t[-1], N, endpoint=True)
        t, h_wbp = t_ds, y_ds
    else:
        fs_eff = fs

    # Diagnostics
    Tspan = float(t[-1] - t[0])
    f_min_safe = 2.0 / Tspan if Tspan > 0 else 0.0
    f_nyq = 0.5 * fs_eff
    band_ok = (args.f_lo >= f_min_safe) and (args.f_hi <= f_nyq)
    rho_max = _acf_max_abs(h_wbp, fs=fs_eff, max_lag_s=1.0)
    whiten_ok = (rho_max <= 0.10)
    # SNR over post-t0 half vs sigma_pre of pre portion after filtering
    mid_mask = (t >= args.t0)
    if not np.any(mid_mask):
        # If t0 at right edge, fallback to second half
        half_idx = len(t) // 2
        mid_mask = np.zeros_like(t, dtype=bool)
        mid_mask[half_idx:] = True
    pre_mask_eff = ~mid_mask
    sigma_pre = float(np.std(h_wbp[pre_mask_eff])) if np.any(pre_mask_eff) else float(np.std(h_wbp))
    rms_post = float(np.sqrt(np.mean(h_wbp[mid_mask] ** 2))) if np.any(mid_mask) else float(np.sqrt(np.mean(h_wbp ** 2)))
    snr_ringdown = (rms_post / sigma_pre) if sigma_pre > 0 else float("inf")

    # Write preprocessed CSV (header 't,h' for Topo-RDM compatibility)
    out_csv = f"{args.out_root}_pre.csv"
    _ensure_parent(out_csv)
    np.savetxt(out_csv, np.column_stack([t, h_wbp]), delimiter=",", header="t,h", comments="")

    # Meta JSON
    meta = {
        "ok": True,
        "fs_in": fs,
        "fs_out": fs_eff,
        "t0": args.t0,
        "t_window": [float(t[0]), float(t[-1])],
        "band": [args.f_lo, args.f_hi],
        "psd": {"seg": args.psd_seg, "overlap": args.psd_olap},
        "diagnostics": {
            "whiteness_rho_max": rho_max,
            "whiten_ok": whiten_ok,
            "band_ok": band_ok,
            "f_min_safe": f_min_safe,
            "f_nyq": f_nyq,
            "snr_ringdown": snr_ringdown,
        },
        "notes": "detrend→Welch PSD (pre)→whiten→zero-phase FIR bandpass→downsample",
    }

    # Contradiction report on gating failure (do not stop emission; report for audit)
    contras = []
    if not band_ok:
        contras.append("Band safety violated: requested band outside [2/T, fs/2].")
    if not whiten_ok:
        contras.append("Whiteness check failed: max |ACF(τ)| > 0.10 beyond lag 0 within 1 s.")
    if contras:
        meta["ok"] = False
        meta["contradictions"] = contras
        with open(f"{args.out_root}_CONTRADICTION_REPORT.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "gate": "preprocess_hygiene",
                    "reasons": contras,
                    "t0": args.t0,
                    "band": [args.f_lo, args.f_hi],
                    "diagnostics": meta["diagnostics"],
                    "out_csv": out_csv,
                },
                f,
                indent=2,
                sort_keys=True,
            )

    meta_path = f"{args.out_root}_pre.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    # Optional ridges
    ridges_csv_path: Optional[str] = None
    if args.emit_ridges:
        nper = max(64, int(round(0.25 * fs_eff)))  # ≈250 ms
        nover = nper // 2
        ridges, _ = stft_ridges(h_wbp, fs=fs_eff, nperseg=nper, noverlap=nover, k_top=int(args.ridges_top_k))
        if ridges.size:
            ridges_csv_path = f"{args.out_root}_ridges.csv"
            _ensure_parent(ridges_csv_path)
            header = "t,f,amp"
            np.savetxt(ridges_csv_path, ridges, delimiter=",", header=header, comments="")

    # Final stdout for tooling
    print(
        json.dumps(
            {
                "ok": meta["ok"],
                "out_csv": out_csv,
                "meta": meta_path,
                "ridges_csv": ridges_csv_path,
                "fs_eff": fs_eff,
            }
        )
    )


if __name__ == "__main__":
    main()