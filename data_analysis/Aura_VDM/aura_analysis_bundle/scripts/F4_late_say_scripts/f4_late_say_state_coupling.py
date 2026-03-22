#!/usr/bin/env python3
from __future__ import annotations
import argparse, io, gzip, zipfile, random
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

METRICS = [
    'active_edges',
    'active_synapses',
    'connectome_entropy',
    'vt_coverage',
    'vt_entropy',
    'b1_z',
    'sie_td_error',
    'sie_valence_01',
]
CORE_PROFILE_METRICS = ['active_edges','connectome_entropy','vt_coverage','vt_entropy','b1_z']

def load_tables(bundle_zip: Path) -> pd.DataFrame:
    with zipfile.ZipFile(bundle_zip) as z:
        with z.open('aura_analysis_bundle/tables/tick_table_full.csv.gz') as f:
            tick = pd.read_csv(io.BytesIO(gzip.decompress(f.read())))
        with z.open('aura_analysis_bundle/tables/utd_say_by_tick.csv') as f:
            say = pd.read_csv(f)
    m = tick.merge(say, on='t', how='left')
    for c in ['say_count','say_words','say_chars']:
        m[c] = m[c].fillna(0)
    return m

def baseline_delta(series: pd.Series, idx: int, start: int, end: int) -> float:
    base = series.iloc[idx-20:idx-5].mean()  # [-20, -6]
    target = series.iloc[idx+start:idx+end+1].mean()
    return float(target - base)

def build_event_table(m: pd.DataFrame):
    say_idx = m.index[(m['say_count'] > 0) | (m['did_say'] == 1)].tolist()
    rows = []
    valid_idx = []
    for idx in say_idx:
        if idx < 20 or idx + 5 >= len(m):
            continue
        valid_idx.append(idx)
        row = {
            't': int(m.at[idx, 't']),
            'phase': int(m.at[idx, 'phase']),
            'adc_territories': int(m.at[idx, 'adc_territories']),
            'say_count': float(m.at[idx, 'say_count']),
            'say_words': float(m.at[idx, 'say_words']),
            'say_chars': float(m.at[idx, 'say_chars']),
        }
        for metric in METRICS:
            s = m[metric]
            row[f'baseline_{metric}'] = float(s.iloc[idx-20:idx-5].mean())
            row[f'pre_{metric}'] = float(s.iloc[idx-5:idx].mean())
            row[f'at_{metric}'] = float(s.iloc[idx])
            row[f'post_{metric}'] = float(s.iloc[idx+1:idx+6].mean())
            row[f'pre_delta_{metric}'] = row[f'pre_{metric}'] - row[f'baseline_{metric}']
            row[f'at_delta_{metric}'] = row[f'at_{metric}'] - row[f'baseline_{metric}']
            row[f'post_delta_{metric}'] = row[f'post_{metric}'] - row[f'baseline_{metric}']
        rows.append(row)
    event_table = pd.DataFrame(rows)
    mask = np.ones(len(m), dtype=bool)
    for idx in valid_idx:
        mask[max(20, idx-20):min(len(m), idx+21)] = False
    controls = [i for i in np.where(mask)[0] if i >= 20 and i + 5 < len(m)]
    return event_table, valid_idx, controls

def period_summary(m: pd.DataFrame, say_idx, controls, n_boot=1000, seed=0) -> pd.DataFrame:
    periods = {'pre':(-5,-1),'at':(0,0),'post':(1,5)}
    rng = random.Random(seed)
    rows = []
    for period, (a,b) in periods.items():
        for metric in METRICS:
            obs_vals = [baseline_delta(m[metric], idx, a, b) for idx in say_idx]
            obs = float(np.mean(obs_vals))
            ctrl_means = []
            for _ in range(n_boot):
                samp = rng.sample(controls, len(say_idx))
                vals = [baseline_delta(m[metric], idx, a, b) for idx in samp]
                ctrl_means.append(float(np.mean(vals)))
            ctrl_means = np.array(ctrl_means, dtype=float)
            z = (obs - ctrl_means.mean()) / ctrl_means.std(ddof=0)
            p_emp = (np.sum(np.abs(ctrl_means - ctrl_means.mean()) >= abs(obs - ctrl_means.mean())) + 1) / (len(ctrl_means) + 1)
            rows.append({
                'period': period,
                'metric': metric,
                'observed_mean_delta': obs,
                'control_mean_delta': float(ctrl_means.mean()),
                'control_sd_delta': float(ctrl_means.std(ddof=0)),
                'z_score_vs_controls': float(z),
                'empirical_p': float(p_emp),
                'n_say_events': len(say_idx),
                'n_controls_available': len(controls),
            })
    return pd.DataFrame(rows)

def event_triggered_profile(m: pd.DataFrame, say_idx) -> pd.DataFrame:
    offsets = list(range(-20, 21))
    rows = []
    for metric in CORE_PROFILE_METRICS:
        for off in offsets:
            vals = []
            for idx in say_idx:
                base = m[metric].iloc[idx-20:idx-5].mean()
                vals.append(float(m[metric].iloc[idx+off] - base))
            arr = np.array(vals, dtype=float)
            rows.append({
                'metric': metric,
                'offset': off,
                'mean_delta_from_baseline': float(arr.mean()),
                'sem_delta_from_baseline': float(arr.std(ddof=1) / np.sqrt(len(arr))) if len(arr) > 1 else 0.0,
            })
    return pd.DataFrame(rows)

def make_figures(profile: pd.DataFrame, summary: pd.DataFrame, outdir: Path) -> None:
    metrics = ['active_edges','connectome_entropy','vt_coverage','vt_entropy','b1_z']
    titles = {
        'active_edges':'Active edges',
        'connectome_entropy':'Connectome entropy',
        'vt_coverage':'Traversal coverage',
        'vt_entropy':'Traversal entropy',
        'b1_z':'b1_z',
    }
    fig, axes = plt.subplots(len(metrics), 1, figsize=(9,13), sharex=True)
    for ax, metric in zip(axes, metrics):
        d = profile[profile['metric'] == metric].sort_values('offset')
        x = d['offset'].to_numpy()
        y = d['mean_delta_from_baseline'].to_numpy()
        se = d['sem_delta_from_baseline'].to_numpy()
        ax.plot(x, y, linewidth=2)
        ax.fill_between(x, y-se, y+se, alpha=0.2)
        ax.axvline(0, linestyle='--', linewidth=1)
        ax.axhline(0, linestyle=':', linewidth=1)
        ax.set_title(titles[metric])
    axes[-1].set_xlabel('Ticks relative to say onset')
    fig.suptitle('Late say events: event-triggered state profiles relative to local baseline')
    fig.tight_layout(rect=[0,0,1,0.98])
    fig.savefig(outdir / 'f4_late_say_event_triggered_profiles.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(10,11), sharex=True)
    periods = ['pre','at','post']
    for ax, period in zip(axes, periods):
        d = summary[summary['period'] == period].copy().set_index('metric').loc[metrics].reset_index()
        ax.bar(d['metric'], d['z_score_vs_controls'])
        ax.axhline(0, linestyle=':', linewidth=1)
        ax.set_ylabel('z vs matched controls')
        ax.set_title(f'{period} window')
        ax.tick_params(axis='x', rotation=30)
    fig.suptitle('Late say events: deviation from matched non-say controls')
    fig.tight_layout(rect=[0,0,1,0.98])
    fig.savefig(outdir / 'f4_late_say_period_zscores.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle-zip', type=Path, default=Path('/mnt/data/aura_analysis_bundle.zip'))
    ap.add_argument('--outdir', type=Path, default=Path('/mnt/data/aura_research_deliverables'))
    args = ap.parse_args()
    m = load_tables(args.bundle_zip)
    out_tables = args.outdir / 'tables'
    out_figs = args.outdir / 'figures'
    out_tables.mkdir(parents=True, exist_ok=True)
    out_figs.mkdir(parents=True, exist_ok=True)
    event_table, say_idx, controls = build_event_table(m)
    summary = period_summary(m, say_idx, controls)
    profile = event_triggered_profile(m, say_idx)
    event_table.to_csv(out_tables / 'f4_late_say_event_windows.csv', index=False)
    summary.to_csv(out_tables / 'f4_late_say_period_summary.csv', index=False)
    profile.to_csv(out_tables / 'f4_late_say_event_triggered_profile.csv', index=False)
    make_figures(profile, summary, out_figs)

if __name__ == '__main__':
    main()
