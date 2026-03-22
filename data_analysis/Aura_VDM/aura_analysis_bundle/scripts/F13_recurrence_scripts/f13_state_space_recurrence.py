#!/usr/bin/env python3
from __future__ import annotations
import argparse, io, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

EPOCHS = [
    'E1_low_entropy_baseline_1',
    'E2_high_entropy_plateau',
    'E3_low_entropy_baseline_2',
]

def load_pca(bundle_zip: Path | None = None, csv_path: Path | None = None) -> pd.DataFrame:
    if csv_path is not None:
        return pd.read_csv(csv_path)
    if bundle_zip is None:
        raise ValueError('Provide either --bundle-zip or --csv-path')
    with zipfile.ZipFile(bundle_zip) as z:
        data = z.read('aura_analysis_bundle/tables/pca_state_space_Aura.csv')
    return pd.read_csv(io.BytesIO(data))

def compute_tables(df: pd.DataFrame, eps: float = 0.5, max_lag: int = 600):
    X = df[['PC1','PC2','PC3']].to_numpy()
    Xz = (X - X.mean(axis=0)) / X.std(axis=0)
    df = df.copy()
    lag_rows, peak_rows, epoch_rows = [], [], []

    # global linear grid for hotspot maps
    pc12 = df[['PC1','PC2']].to_numpy()
    xb = np.linspace(pc12[:,0].min(), pc12[:,0].max(), 33)
    yb = np.linspace(pc12[:,1].min(), pc12[:,1].max(), 33)
    xid = np.clip(np.searchsorted(xb, pc12[:,0], side='right') - 1, 0, len(xb)-2)
    yid = np.clip(np.searchsorted(yb, pc12[:,1], side='right') - 1, 0, len(yb)-2)
    df['cell_x'] = xid
    df['cell_y'] = yid
    df['cell'] = xid * (len(yb)-1) + yid
    hotspot_rows = []

    for epoch in EPOCHS:
        mask = (df['epoch'].to_numpy() == epoch)
        Xe = Xz[mask]
        de = df.loc[mask].copy()
        n = len(de)
        if n < 50:
            continue
        rng = np.random.default_rng(0)
        idx1 = rng.integers(0, n, 50000)
        idx2 = rng.integers(0, n, 50000)
        baseline = (np.linalg.norm(Xe[idx1] - Xe[idx2], axis=1) <= eps).mean()

        rr = []
        upper = min(max_lag, n-1)
        for lag in range(1, upper + 1):
            rec = (np.linalg.norm(Xe[:-lag] - Xe[lag:], axis=1) <= eps).mean()
            rr.append(rec)
            lag_rows.append((epoch, lag, rec, baseline, rec - baseline))
        rr = np.asarray(rr)
        peaks, props = find_peaks(rr[9:], prominence=0.01, distance=8)  # lags >= 10
        lags = peaks + 10
        prominences = props.get('prominences', np.zeros_like(lags, dtype=float))
        peak_df = pd.DataFrame({
            'lag': lags,
            'rr': rr[lags-1],
            'prominence': prominences,
        }).sort_values(['rr','prominence'], ascending=False)
        for _, row in peak_df.head(15).iterrows():
            peak_rows.append((epoch, int(row['lag']), float(row['rr']), float(row['prominence']), float(baseline), float(row['rr'] - baseline)))

        # hotspot summary: long-lag revisits in same PC1/PC2 grid cell
        cells = de['cell'].to_numpy()
        counts = {}
        total = 0
        for lag in range(20, min(200, n-1) + 1):
            match = (cells[:-lag] == cells[lag:])
            total += int(match.sum())
            if match.any():
                vals, cts = np.unique(cells[:-lag][match], return_counts=True)
                for c, ct in zip(vals, cts):
                    counts[int(c)] = counts.get(int(c), 0) + int(ct)
        items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        top10_return_share = (sum(v for _, v in items[:10]) / total) if total else np.nan
        top10_occupancy_share = de['cell'].value_counts().head(10).sum() / len(de)
        epoch_rows.append((
            epoch, n, baseline, float(rr.mean()), float(rr[9:].max()),
            int((rr[9:] > baseline + 0.05).sum()), int((rr[9:] > baseline + 0.1).sum()),
            int(len(peak_df)), total, int(len(counts)), float(top10_return_share), float(top10_occupancy_share)
        ))
        for rank, (cell, count) in enumerate(items[:20], start=1):
            cx, cy = divmod(cell, len(yb)-1)
            hotspot_rows.append((epoch, rank, int(cx), int(cy), int(count), float(count / total) if total else np.nan))

    lag_df = pd.DataFrame(lag_rows, columns=['epoch','lag','recurrence_rate','baseline_random_pair_rr','excess_over_baseline'])
    peak_df = pd.DataFrame(peak_rows, columns=['epoch','lag','recurrence_rate','prominence','baseline_random_pair_rr','excess_over_baseline'])
    epoch_df = pd.DataFrame(epoch_rows, columns=[
        'epoch','n_ticks','baseline_random_pair_rr','mean_rr_lag1_600','max_rr_lag10_600',
        'lags_above_base_plus_0.05','lags_above_base_plus_0.1','peak_count',
        'total_longlag_returns_20_200','active_return_cells','top10_return_cell_share','top10_occupancy_share'
    ])
    hotspot_df = pd.DataFrame(hotspot_rows, columns=['epoch','rank','cell_x','cell_y','longlag_return_count','share_of_epoch_returns'])
    return lag_df, peak_df, epoch_df, hotspot_df, df

def make_figures(lag_df, peak_df, hotspot_df, df, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    # Figure 1: recurrence by lag
    fig, axes = plt.subplots(3, 1, figsize=(10, 11), sharex=True, constrained_layout=True)
    title_map = {
        'E1_low_entropy_baseline_1': 'E1 — low-entropy baseline 1',
        'E2_high_entropy_plateau': 'E2 — high-entropy plateau',
        'E3_low_entropy_baseline_2': 'E3 — low-entropy baseline 2',
    }
    for ax, epoch in zip(axes, EPOCHS):
        sub = lag_df[lag_df['epoch'] == epoch]
        peaks = peak_df[peak_df['epoch'] == epoch].sort_values('recurrence_rate', ascending=False).head(5)
        ax.plot(sub['lag'], sub['recurrence_rate'], lw=2)
        ax.axhline(float(sub['baseline_random_pair_rr'].iloc[0]), ls='--', lw=1.4)
        ax.set_ylabel('Return probability')
        ax.set_title(title_map[epoch], loc='left', fontsize=12, fontweight='bold')
        for _, row in peaks.iterrows():
            ax.scatter(row['lag'], row['recurrence_rate'], s=28, zorder=3)
            ax.annotate(f"{int(row['lag'])}", (row['lag'], row['recurrence_rate']), textcoords='offset points', xytext=(3,4), fontsize=8)
        ax.text(0.99, 0.04, f"baseline = {float(sub['baseline_random_pair_rr'].iloc[0]):.3f}", transform=ax.transAxes,
                ha='right', va='bottom', fontsize=9, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='0.8'))
        ax.grid(alpha=0.2)
    axes[-1].set_xlabel('Lag (ticks)')
    fig.suptitle('Family 13 — Return probability to a nearby PCA state vs lag\n3D PCA trajectory, recurrence threshold ε = 0.5 z-units', fontsize=14, fontweight='bold')
    fig.savefig(outdir/'f13_recurrence_by_lag_epoch.png', dpi=220)
    plt.close(fig)

    # Figure 2: hotspot heatmaps
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), constrained_layout=True)
    for ax, epoch in zip(axes, EPOCHS):
        hs = hotspot_df[hotspot_df['epoch'] == epoch]
        grid = np.zeros((32, 32), dtype=float)
        for _, row in hs.iterrows():
            grid[int(row['cell_x']), int(row['cell_y'])] = row['longlag_return_count']
        im = ax.imshow(grid.T, origin='lower', aspect='auto')
        ax.set_title(title_map[epoch], fontsize=11, fontweight='bold')
        ax.set_xlabel('PC1 grid cell')
        ax.set_ylabel('PC2 grid cell')
        if not hs.empty:
            top10 = hs.nsmallest(10, 'rank')['share_of_epoch_returns'].sum()
            ax.text(0.98, 0.02, f"top-10 cells = {top10:.1%}\nof epoch returns", transform=ax.transAxes,
                    ha='right', va='bottom', fontsize=9, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='0.8'))
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    fig.suptitle('Family 13 — Where long-lag revisits happen in PCA space\nCounts of same-cell returns over lags 20–200 ticks', fontsize=14, fontweight='bold')
    fig.savefig(outdir/'f13_recurrence_hotspots_epoch.png', dpi=220)
    plt.close(fig)

    # Figure 3: compact epoch summary
    es = lag_df.groupby('epoch').first().reset_index()[['epoch']].copy()
    tmp = peak_df.sort_values(['epoch','recurrence_rate'], ascending=[True,False]).groupby('epoch').head(1)[['epoch','lag','recurrence_rate']]
    es = es.merge(tmp, on='epoch', how='left')
    # Add active return cells and occupancy share from hotspot-based summary
    # (computed externally in epoch table by caller; read from hotspot_df surrogate below not possible)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle-zip', type=Path, default=Path('/mnt/data/aura_analysis_bundle.zip'))
    ap.add_argument('--csv-path', type=Path, default=None)
    ap.add_argument('--out-dir', type=Path, default=Path('/mnt/data/aura_research_deliverables_F13'))
    ap.add_argument('--epsilon', type=float, default=0.5)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir/'tables').mkdir(exist_ok=True)
    (args.out_dir/'figures').mkdir(exist_ok=True)
    df = load_pca(args.bundle_zip if args.csv_path is None else None, args.csv_path)
    lag_df, peak_df, epoch_df, hotspot_df, df2 = compute_tables(df, eps=args.epsilon)
    lag_df.to_csv(args.out_dir/'tables'/'f13_recurrence_lag_by_epoch.csv', index=False)
    peak_df.to_csv(args.out_dir/'tables'/'f13_recurrence_peak_table.csv', index=False)
    epoch_df.to_csv(args.out_dir/'tables'/'f13_recurrence_epoch_summary.csv', index=False)
    hotspot_df.to_csv(args.out_dir/'tables'/'f13_longlag_hotspots.csv', index=False)
    make_figures(lag_df, peak_df, hotspot_df, df2, args.out_dir/'figures')
    print('Wrote F13 outputs to', args.out_dir)

if __name__ == '__main__':
    main()
