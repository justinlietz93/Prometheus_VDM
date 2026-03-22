#!/usr/bin/env python3
from pathlib import Path
import pandas as pd, json
import matplotlib.pyplot as plt

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch1-dir', required=True)
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args()
    base = Path(args.batch1_dir)
    out = Path(args.out_dir)
    for sub in ['tables','figures','docs']:
        (out/sub).mkdir(parents=True, exist_ok=True)

    f11 = pd.read_csv(base/'F11_cross_source_motif_origins.csv')
    with open(base/'batch1_fixed_master_results.json') as f:
        master = json.load(f)

    origin_summary = f11['origin'].value_counts().rename_axis('origin').reset_index(name='count')
    origin_summary['fraction'] = origin_summary['count']/len(f11)
    origin_summary['percent'] = origin_summary['fraction']*100
    origin_summary.to_csv(out/'tables/f11_direct_origin_summary.csv', index=False)

    by_epoch = pd.crosstab(f11['epoch'], f11['origin'])
    by_epoch = by_epoch.reindex(columns=['could_be_source_continuation','cross_source_transfer','endogenous'], fill_value=0)
    by_epoch_frac = by_epoch.div(by_epoch.sum(axis=1), axis=0).fillna(0)
    by_epoch_long = by_epoch.reset_index().melt(id_vars='epoch', var_name='origin', value_name='count')
    by_epoch_long['fraction'] = by_epoch_long.apply(lambda r: by_epoch_frac.loc[r['epoch'], r['origin']], axis=1)
    by_epoch_long['percent'] = by_epoch_long['fraction']*100
    by_epoch_long.to_csv(out/'tables/f11_direct_origin_by_epoch.csv', index=False)

    by_book = pd.crosstab(f11['active_book'], f11['origin'])
    by_book = by_book.reindex(columns=['could_be_source_continuation','cross_source_transfer','endogenous'], fill_value=0)
    by_book_frac = by_book.div(by_book.sum(axis=1), axis=0).fillna(0)
    by_book_long = by_book.reset_index().melt(id_vars='active_book', var_name='origin', value_name='count')
    by_book_long['fraction'] = by_book_long.apply(lambda r: by_book_frac.loc[r['active_book'], r['origin']], axis=1)
    by_book_long['percent'] = by_book_long['fraction']*100
    by_book_long.to_csv(out/'tables/f11_direct_origin_by_active_book.csv', index=False)

    motif_counts = f11['motif_words'].value_counts().rename_axis('motif_words').reset_index(name='count')
    motif_counts['fraction'] = motif_counts['count']/len(f11)
    motif_counts.to_csv(out/'tables/f11_direct_motif_word_counts.csv', index=False)
    f11.to_csv(out/'tables/f11_direct_motif_events_full.csv', index=False)

    color_map = {'could_be_source_continuation':'#999999','cross_source_transfer':'#4C78A8','endogenous':'#F58518'}
    origins = ['could_be_source_continuation','cross_source_transfer','endogenous']
    labels = ['source continuation','cross-source transfer','endogenous']

    fig, ax = plt.subplots(figsize=(9,5))
    left = None
    for origin,label in zip(origins,labels):
        vals = by_epoch_frac[origin].values
        ax.barh(range(len(by_epoch_frac.index)), vals, left=left, color=color_map[origin], label=label)
        left = vals.copy() if left is None else left + vals
    ax.set_yticks(range(len(by_epoch_frac.index)))
    ax.set_yticklabels([s.replace('_',' ') for s in by_epoch_frac.index])
    ax.set_xlim(0,1)
    ax.set_xlabel('Fraction of motif events')
    ax.set_title('F11 direct: motif-origin fractions by epoch')
    ax.legend(frameon=False, loc='lower right')
    plt.tight_layout(); fig.savefig(out/'figures/f11_direct_origin_by_epoch.png', dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10,5))
    left = None
    for origin,label in zip(origins,labels):
        vals = by_book_frac[origin].values
        ax.barh(range(len(by_book_frac.index)), vals, left=left, color=color_map[origin], label=label)
        left = vals.copy() if left is None else left + vals
    ax.set_yticks(range(len(by_book_frac.index)))
    ax.set_yticklabels(by_book_frac.index)
    ax.set_xlim(0,1)
    ax.set_xlabel('Fraction of motif events')
    ax.set_title('F11 direct: motif-origin fractions by active source')
    ax.legend(frameon=False, loc='lower right')
    plt.tight_layout(); fig.savefig(out/'figures/f11_direct_origin_by_active_book.png', dpi=180); plt.close(fig)

    with open(out/'docs/f11_direct_master_extract.json','w') as f:
        json.dump(master.get('F11_cross_source_transfer',{}), f, indent=2)

if __name__ == '__main__':
    main()
