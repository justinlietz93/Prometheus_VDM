#!/usr/bin/env python3
"""
VDM "Four Proofs" Analysis Pack
================================

This script reproduces the 4 analyses requested for the structurally-plastic VDM runs, using:
- snapshots_backup.zip (state_*.h5 snapshots, every 60 ticks)
- events slices for scalar telemetry (begin/mid/end) from:
    - 20260204_142311.zip   (ticks ~0-8247)
    - 20260204_144053.zip   (ticks ~8264-16504)
    - events.jsonl.zip      (ticks ~24910-29176)

Outputs:
- tables/*.csv
- figures/*.png

Notes:
- Offline-only. No runtime changes.
- Uses sparse CSR row_ptr/col_idx for degree-based metrics.

Run:
    python scripts/run_four_proofs.py --data_dir /mnt/data --out_dir /mnt/data/vdm_four_proofs_pack_repro
"""
from __future__ import annotations
import argparse, io, json, math, os, re, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KernelDensity

plt.rcParams["figure.dpi"] = 160

def gini(array: np.ndarray) -> float:
    x = np.array(array, dtype=np.float64)
    if np.any(x < 0):
        x = x - x.min()
    if np.allclose(x, 0):
        return 0.0
    x = np.sort(x)
    n = len(x)
    cumx = np.cumsum(x)
    return float((n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n)

def powerlaw_alpha_discrete(x: np.ndarray, xmin: int) -> tuple[float, int]:
    x = np.asarray(x)
    x = x[x >= xmin]
    n = len(x)
    if n == 0:
        return (float("nan"), 0)
    denom = np.sum(np.log(x / (xmin - 0.5)))
    if denom <= 0:
        return (float("nan"), n)
    alpha = 1 + n / denom
    return (float(alpha), int(n))

def hellinger(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    p = p / (p.sum() + eps)
    q = q / (q.sum() + eps)
    return float(np.linalg.norm(np.sqrt(p + eps) - np.sqrt(q + eps)) / math.sqrt(2))

def psd_loglog_slope(signal: np.ndarray, fs: float = 1.0, f_low: float = 1/500, f_high: float = 0.1):
    x = np.asarray(signal, dtype=np.float64)
    x = x - np.mean(x)
    N = len(x)
    w = np.hanning(N)
    xw = x * w
    X = np.fft.rfft(xw)
    psd = (np.abs(X) ** 2) / (fs * np.sum(w ** 2))
    freqs = np.fft.rfftfreq(N, d=1 / fs)
    mask = (freqs >= f_low) & (freqs <= f_high) & (psd > 0)
    if mask.sum() < 10:
        return float("nan"), (freqs, psd, mask, float("nan"), float("nan"))
    lf = np.log10(freqs[mask])
    lp = np.log10(psd[mask])
    slope, intercept = np.polyfit(lf, lp, 1)
    return float(slope), (freqs, psd, mask, float(slope), float(intercept))

def detect_avalanches(series: np.ndarray, threshold: float):
    x = np.asarray(series, dtype=np.float64)
    above = x > threshold
    sizes, durs = [], []
    i = 0
    N = len(x)
    while i < N:
        if not above[i]:
            i += 1
            continue
        j = i
        size = 0.0
        while j < N and above[j]:
            size += x[j] - threshold
            j += 1
        sizes.append(size)
        durs.append(j - i)
        i = j
    return np.array(sizes), np.array(durs)

def powerlaw_alpha_continuous(x: np.ndarray, xmin: float):
    x = np.asarray(x, dtype=np.float64)
    x = x[x > 0]
    x = x[x >= xmin]
    n = len(x)
    if n == 0:
        return float("nan"), 0
    alpha = 1 + n / np.sum(np.log(x / xmin))
    return float(alpha), int(n)

def size_duration_relation(sizes: np.ndarray, durs: np.ndarray) -> float:
    df = pd.DataFrame({"size": sizes, "dur": durs})
    grp = df.groupby("dur")["size"].mean()
    d = grp.index.values.astype(float)
    s = grp.values.astype(float)
    mask = (d > 0) & (s > 0)
    if mask.sum() < 3:
        return float("nan")
    slope, _ = np.polyfit(np.log10(d[mask]), np.log10(s[mask]), 1)
    return float(slope)

def rqa_metrics(R: np.ndarray, lmin: int = 2, vmin: int = 2) -> dict:
    N = R.shape[0]
    RR = (R.sum() - N) / (N * (N - 1))

    diag_lengths = []
    for k in range(-N + 1, N):
        if k == 0:
            continue
        diag = np.diagonal(R, offset=k)
        run = 0
        for val in diag:
            if val:
                run += 1
            else:
                if run > 0:
                    diag_lengths.append(run)
                    run = 0
        if run > 0:
            diag_lengths.append(run)
    diag_lengths = np.array(diag_lengths, dtype=int)
    if len(diag_lengths) == 0:
        DET = float("nan")
        Lmean = float("nan")
        Lent = float("nan")
    else:
        det_points = diag_lengths[diag_lengths >= lmin].sum()
        all_points = diag_lengths.sum()
        DET = det_points / all_points if all_points > 0 else float("nan")
        Lmean = diag_lengths[diag_lengths >= lmin].mean() if np.any(diag_lengths >= lmin) else float("nan")
        if np.any(diag_lengths >= lmin):
            lengths = diag_lengths[diag_lengths >= lmin]
            vals, counts = np.unique(lengths, return_counts=True)
            p = counts / counts.sum()
            Lent = float(-(p * np.log(p)).sum())
        else:
            Lent = float("nan")

    vert_lengths = []
    for j in range(N):
        col = R[:, j]
        run = 0
        for i, val in enumerate(col):
            if i == j:
                if run > 0:
                    vert_lengths.append(run)
                    run = 0
                continue
            if val:
                run += 1
            else:
                if run > 0:
                    vert_lengths.append(run)
                    run = 0
        if run > 0:
            vert_lengths.append(run)
    vert_lengths = np.array(vert_lengths, dtype=int)
    if len(vert_lengths) == 0:
        LAM = float("nan")
        TT = float("nan")
    else:
        lam_points = vert_lengths[vert_lengths >= vmin].sum()
        all_points = vert_lengths.sum()
        LAM = lam_points / all_points if all_points > 0 else float("nan")
        TT = vert_lengths[vert_lengths >= vmin].mean() if np.any(vert_lengths >= vmin) else float("nan")

    return {
        "RR": float(RR),
        "DET": float(DET),
        "Lmean": float(Lmean),
        "Lent": float(Lent),
        "LAM": float(LAM),
        "TT": float(TT),
        "n_diag_lines": int(len(diag_lengths)),
        "n_vert_lines": int(len(vert_lengths)),
    }

def build_regular_series(df: pd.DataFrame, value_col: str, fill_method: str = "ffill"):
    tmin = int(df["t"].min())
    tmax = int(df["t"].max())
    idx = np.arange(tmin, tmax + 1)
    s = pd.Series(df[value_col].values, index=df["t"].values)
    s = s.groupby(level=0).last()
    s = s.reindex(idx)
    if fill_method == "ffill":
        s = s.ffill().bfill()
    else:
        s = s.interpolate().bfill().ffill()
    return idx, s.values

def load_events_segment(zip_path: Path, inner_name: str, fields: tuple[str,...]):
    z = zipfile.ZipFile(zip_path, "r")
    rows = []
    with z.open(inner_name) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            t = obj.get("t")
            if t is None:
                continue
            row = {"t": t}
            for k in fields:
                if k == "t":
                    continue
                row[k] = obj.get(k)
            rows.append(row)
    df = pd.DataFrame(rows).sort_values("t").reset_index(drop=True)
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", type=str, required=True)
    ap.add_argument("--out_dir", type=str, required=True)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    (out_dir / "tables").mkdir(parents=True, exist_ok=True)
    (out_dir / "figures").mkdir(parents=True, exist_ok=True)

    # --- Load snapshots ---
    snap_zip = data_dir / "snapshots_backup.zip"
    zf = zipfile.ZipFile(snap_zip, "r")
    real = [n for n in zf.namelist() if n.startswith("snapshots_backup/state_") and n.endswith(".h5")]
    ticks = sorted([int(re.search(r"state_(\d+)\.h5", n).group(1)) for n in real])
    tick_to_name = {int(re.search(r"state_(\d+)\.h5", n).group(1)): n for n in real}

    rows = []
    topk = 20
    top_hubs = []
    prev_adc = None
    for tick in ticks:
        name = tick_to_name[tick]
        data = zf.open(name).read()
        with h5py.File(io.BytesIO(data), "r") as h5:
            W = h5["sparse/W"][:].astype(np.float64)
            row_ptr = h5["sparse/row_ptr"][:]
            col_idx = h5["sparse/col_idx"][:]
            out_deg = np.diff(row_ptr).astype(np.int32)
            nnz = len(col_idx)
            gin = gini(out_deg)
            alpha13, ntail13 = powerlaw_alpha_discrete(out_deg, xmin=13)

            hubs = np.argsort(out_deg)[-topk:][::-1]
            top_hubs.append(hubs)

            adc = json.loads(h5["adc_json"][()])
            terr = adc.get("territories", [])
            id_mass = {t["id"]: float(t.get("mass", 0.0)) for t in terr if "id" in t}
            vec = np.array([id_mass.get(i, 0.0) for i in range(1, 6)], dtype=np.float64)
            if vec.sum() <= 0:
                vec = np.ones_like(vec)
            vec = vec / vec.sum()
            if prev_adc is None:
                hw = float("nan")
            else:
                hw = hellinger(prev_adc, vec)
            prev_adc = vec

        rows.append({
            "tick": tick,
            "nnz": nnz,
            "gini_out": gin,
            "alpha_kmin13": alpha13,
            "n_tail_kmin13": ntail13,
            "out_deg_max": int(out_deg.max()),
            "hellinger_adc_mass_prev": hw,
            "top20_hubs": ";".join(map(str, hubs.tolist())),
        })

    df_snap = pd.DataFrame(rows)
    df_snap.to_csv(out_dir / "tables" / "snapshot_metrics.csv", index=False)

    # --- TRQA recurrence plot (hub occupancy) ---
    T = len(ticks); N = 1000
    M = np.zeros((T, N), dtype=np.uint8)
    for i, hubs in enumerate(top_hubs):
        M[i, hubs] = 1
    inter = M @ M.T
    union = 2 * topk - inter
    jaccard = inter / np.maximum(union, 1)

    # save recurrence figs
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(jaccard, origin="lower", aspect="auto", vmin=0, vmax=1)
    ax.set_title("TRQA Recurrence (Jaccard) of Top-20 Degree Hubs")
    ax.set_xlabel("snapshot index"); ax.set_ylabel("snapshot index")
    fig.colorbar(im, ax=ax, label="Jaccard overlap")
    fig.tight_layout()
    fig.savefig(out_dir / "figures" / "fig1a_hub_recursion_jaccard_heatmap.png")
    plt.close(fig)

    theta = 0.2
    R = (jaccard >= theta).astype(np.uint8)
    m = rqa_metrics(R)
    pd.DataFrame([{**m, "theta": theta}]).to_csv(out_dir / "tables" / "rqa_metrics_theta0p2.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(R, origin="lower", aspect="auto", vmin=0, vmax=1)
    ax.set_title(f"Recurrence Plot (threshold Jaccard ≥ {theta})")
    ax.set_xlabel("snapshot index"); ax.set_ylabel("snapshot index")
    fig.tight_layout()
    fig.savefig(out_dir / "figures" / "fig1b_hub_recursion_binary_theta0p2.png")
    plt.close(fig)

    # --- Free energy landscape (order parameters x=nnz, y=gini) ---
    x = df_snap["nnz"].values.astype(float)
    y = df_snap["gini_out"].values.astype(float)
    X = np.column_stack([x, y])
    sc = StandardScaler().fit(X)
    Xz = sc.transform(X)
    kde = KernelDensity(bandwidth=0.2, kernel="gaussian").fit(Xz)
    grid_x = np.linspace(x.min(), x.max(), 100)
    grid_y = np.linspace(y.min(), y.max(), 100)
    gx, gy = np.meshgrid(grid_x, grid_y, indexing="ij")
    grid = np.column_stack([gx.ravel(), gy.ravel()])
    log_dens = kde.score_samples(sc.transform(grid))
    dens = np.exp(log_dens).reshape(gx.shape)
    F = -np.log(dens + 1e-12)

    # 2-cluster macrostate
    km = KMeans(n_clusters=2, random_state=0, n_init=10).fit(sc.transform(X))
    centers = sc.inverse_transform(km.cluster_centers_)
    df_snap["state_cluster"] = km.labels_
    # label by higher gini = reading-like
    c0, c1 = centers[0], centers[1]
    if c0[1] > c1[1]:
        label_map = {0: "Reading-like", 1: "Dream/Integration-like"}
    else:
        label_map = {1: "Reading-like", 0: "Dream/Integration-like"}
    df_snap["state_label"] = df_snap["state_cluster"].map(label_map)
    df_snap.to_csv(out_dir / "tables" / "snapshot_metrics_with_states.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    levels = np.linspace(np.nanmin(F), np.nanpercentile(F, 95), 25)
    cs = ax.contourf(gx, gy, F, levels=levels)
    fig.colorbar(cs, ax=ax, label="F = -log P (KDE, arbitrary units)")
    for label, grp in df_snap.groupby("state_label"):
        ax.scatter(grp["nnz"], grp["gini_out"], s=10, alpha=0.6, label=label)
    for c in centers:
        ax.scatter(c[0], c[1], marker="x", s=80)
    ax.set_title("Empirical Free Energy Landscape (x=nnz edges, y=Gini)")
    ax.set_xlabel("nnz edges"); ax.set_ylabel("Gini")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "figures" / "fig3_free_energy_landscape.png")
    plt.close(fig)

    # --- PSD + avalanche scaling (requires events slices) ---
    fields = ("t","firing_var","active_edges","vt_entropy","vt_coverage","connectome_entropy")
    begin_zip = data_dir / "20260204_142311.zip"
    mid_zip = data_dir / "20260204_144053.zip"
    end_zip = data_dir / "events.jsonl.zip"
    df_begin = load_events_segment(begin_zip, "20260204_142311/events.jsonl", fields)
    df_mid   = load_events_segment(mid_zip,   "20260204_144053/events.jsonl", fields)
    df_end   = load_events_segment(end_zip,   "events.jsonl", fields)

    def do_psd(df, var):
        _, arr = build_regular_series(df, var)
        slope, data = psd_loglog_slope(arr)
        freqs, psd, mask, slope, intercept = data
        return slope, freqs, psd, mask, intercept, arr

    slope, freqs, psd, mask, intercept, arr = do_psd(df_mid, "firing_var")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(freqs[1:], psd[1:])
    fit_freq = freqs[mask]
    fit_line = 10 ** (intercept + slope * np.log10(fit_freq))
    ax.loglog(fit_freq, fit_line, linewidth=2, label=f"fit slope={slope:.2f} (β≈{-slope:.2f})")
    ax.set_title("PSD of firing_var (mid segment)")
    ax.set_xlabel("frequency (1/tick)"); ax.set_ylabel("PSD")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "figures" / "fig2_psd_firing_var_mid.png")
    plt.close(fig)

    # avalanche
    thr = float(np.quantile(arr, 0.75))
    sizes, durs = detect_avalanches(arr, thr)
    xmin_s = float(np.quantile(sizes, 0.5)) if len(sizes) else 0.0
    xmin_d = float(np.quantile(durs, 0.5)) if len(durs) else 0.0
    a_s, n_s = powerlaw_alpha_continuous(sizes, xmin_s) if xmin_s>0 else (float("nan"),0)
    a_d, n_d = powerlaw_alpha_continuous(durs.astype(float), xmin_d) if xmin_d>0 else (float("nan"),0)
    gamma = size_duration_relation(sizes, durs)
    pd.DataFrame([{
        "segment":"mid","var":"firing_var","threshold_q":0.75,"threshold":thr,"n_aval":int(len(sizes)),
        "size_alpha":a_s,"size_xmin":xmin_s,"size_n_tail":n_s,
        "dur_alpha":a_d,"dur_xmin":xmin_d,"dur_n_tail":n_d,
        "gamma_size_vs_dur":gamma,
    }]).to_csv(out_dir / "tables" / "avalanche_scaling_mid_firing_var.csv", index=False)

    sizes_sorted = np.sort(sizes[sizes > 0])
    ccdf = 1.0 - np.arange(1, len(sizes_sorted) + 1) / len(sizes_sorted)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(sizes_sorted, ccdf)
    ax.set_title("Avalanche size CCDF (firing_var, mid segment)")
    ax.set_xlabel("avalanche size"); ax.set_ylabel("CCDF")
    fig.tight_layout()
    fig.savefig(out_dir / "figures" / "fig2b_avalanche_size_ccdf_mid.png")
    plt.close(fig)

if __name__ == "__main__":
    main()
