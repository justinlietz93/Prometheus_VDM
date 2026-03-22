from __future__ import annotations
import argparse, itertools
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import ensure_dir, parse_h5_snapshot


def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--h5_dir', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out = ensure_dir(args.out)
    paths = sorted(Path(args.h5_dir).glob('state_*.h5'))
    summaries=[]; raws=[]
    for p in paths:
        s, raw = parse_h5_snapshot(p)
        summaries.append(s); raws.append((s['tick'], raw))
    sm = pd.DataFrame(summaries).sort_values('tick')
    sm.to_csv(out/'snapshot_metrics.csv', index=False)
    sm[['file','bytes']].rename(columns={'bytes':'size_bytes'}).to_csv(out/'h5_file_sizes.csv', index=False)

    # territory masses long
    terr_rows=[]
    for tick, raw in raws:
        for terr in raw['territories']:
            terr_rows.append({'tick': tick, **terr})
    terr = pd.DataFrame(terr_rows).sort_values(['territory','tick'])
    terr.to_csv(out/'h5_territory_masses_long.csv', index=False)

    # overview figure
    fig, axes = plt.subplots(2,2, figsize=(12,8))
    axes[0,0].plot(sm['tick'], sm['nnz_edges'], marker='o'); axes[0,0].set_title('nnz_edges'); axes[0,0].grid(alpha=.25)
    axes[0,1].plot(sm['tick'], sm['mean_degree'], marker='o'); axes[0,1].set_title('mean_degree'); axes[0,1].grid(alpha=.25)
    axes[1,0].plot(sm['tick'], sm['mean_weight'], marker='o'); axes[1,0].set_title('mean_weight'); axes[1,0].grid(alpha=.25)
    axes[1,1].plot(sm['tick'], sm['std_weight'], marker='o'); axes[1,1].set_title('std_weight'); axes[1,1].grid(alpha=.25)
    fig.tight_layout(); fig.savefig(out/'h5_snapshot_structural_overview.png', dpi=180); plt.close(fig)

    # territory drift
    piv = terr.pivot(index='tick', columns='territory', values='mass')
    fig, ax = plt.subplots(figsize=(12,6))
    for c in piv.columns:
        ax.plot(piv.index, piv[c], marker='o', linewidth=1.0, label=f'T{c}')
    ax.set_xlabel('tick'); ax.set_ylabel('mass'); ax.grid(alpha=.25); ax.legend(ncol=3, fontsize=8)
    fig.tight_layout(); fig.savefig(out/'h5_territory_mass_drift.png', dpi=180); plt.close(fig)

    # drift vs distribution stability
    rows=[]
    for (tick_a, raw_a), (tick_b, raw_b) in zip(raws[:-1], raws[1:]):
        edge_a = set(zip(np.repeat(np.arange(len(raw_a['row_ptr'])-1), np.diff(raw_a['row_ptr'])), raw_a['col']))
        edge_b = set(zip(np.repeat(np.arange(len(raw_b['row_ptr'])-1), np.diff(raw_b['row_ptr'])), raw_b['col']))
        w_delta = float(np.mean(np.abs(raw_b['W'] - raw_a['W'])))
        masses_a = np.array([t['mass'] for t in raw_a['territories']], dtype=float)
        masses_b = np.array([t['mass'] for t in raw_b['territories']], dtype=float)
        msum_a, msum_b = masses_a.sum(), masses_b.sum()
        pa = masses_a / msum_a if msum_a else masses_a
        pb = masses_b / msum_b if msum_b else masses_b
        stability = 1.0 - 0.5 * float(np.abs(pa - pb).sum())
        rows.append({'tick_from':tick_a,'tick_to':tick_b,'mean_abs_w_delta':w_delta,'edge_jaccard':jaccard(edge_a, edge_b),'territory_distribution_stability':stability})
    drift = pd.DataFrame(rows)
    drift.to_csv(out/'h5_drift_summary.csv', index=False)
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(drift['mean_abs_w_delta'], drift['territory_distribution_stability'], s=60)
    for _, r in drift.iterrows():
        ax.annotate(f"{int(r['tick_from'])}->{int(r['tick_to'])}", (r['mean_abs_w_delta'], r['territory_distribution_stability']), fontsize=8)
    ax.set_xlabel('mean_abs_w_delta'); ax.set_ylabel('territory_distribution_stability'); ax.grid(alpha=.25)
    fig.tight_layout(); fig.savefig(out/'h5_drift_edge_turnover_vs_distribution_stability.png', dpi=180); plt.close(fig)

if __name__ == '__main__':
    main()
