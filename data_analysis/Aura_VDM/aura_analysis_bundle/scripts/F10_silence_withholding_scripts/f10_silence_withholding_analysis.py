
#!/usr/bin/env python3
from pathlib import Path
import zipfile, io, gzip, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

ROOT = Path('/mnt/data/aura_research_deliverables')
ZIP_PATH = Path('/mnt/data/aura_analysis_bundle.zip')
OUT_TABLES = ROOT/'tables'
OUT_FIGS = ROOT/'figures'
OUT_DOCS = ROOT/'docs'
for p in [OUT_TABLES, OUT_FIGS, OUT_DOCS]:
    p.mkdir(parents=True, exist_ok=True)

WINDOW = 5
HI_GATE_QUANTILE = 0.95
HI_GATE_MIN_DIST = 5
METRICS = [
    'active_edges','active_synapses','connectome_entropy','vt_entropy',
    'vt_coverage','b1_z','sie_v2_valence_01','sie_td_error'
]


def rank_biserial_from_u(u, n1, n2):
    return (2*u)/(n1*n2) - 1

with zipfile.ZipFile(ZIP_PATH) as zf:
    tick = pd.read_csv(io.BytesIO(gzip.decompress(zf.read('aura_analysis_bundle/tables/tick_table_full.csv.gz'))))
    say = pd.read_csv(io.BytesIO(zf.read('aura_analysis_bundle/tables/utd_say_by_tick.csv')))

say_ticks = set(say[say['t'].isin(tick['t'])]['t'].astype(int).tolist())

# classify each tick
cats = []
for t in tick['t'].astype(int):
    if t in say_ticks:
        cats.append('say')
    elif any((t + d) in say_ticks for d in range(1, WINDOW+1)):
        cats.append('pre')
    elif any((t - d) in say_ticks for d in range(1, WINDOW+1)):
        cats.append('post')
    else:
        cats.append('silence')

tick = tick.copy()
tick['state_category'] = cats

# summary
summary = tick.groupby('state_category')[METRICS].agg(['mean','median','std'])
summary.columns = ['_'.join(col) for col in summary.columns]
summary = summary.reset_index()
summary.insert(1, 'n_ticks', tick.groupby('state_category').size().values)
summary.to_csv(OUT_TABLES/'f10_state_category_summary.csv', index=False)

# tests vs silence
rows = []
sil = tick[tick['state_category']=='silence']
for category in ['pre','say','post']:
    sub = tick[tick['state_category']==category]
    for metric in METRICS:
        x = sub[metric].dropna().values
        y = sil[metric].dropna().values
        u, p = mannwhitneyu(x, y, alternative='two-sided')
        rows.append({
            'comparison': f'{category}_vs_silence',
            'metric': metric,
            'n_category': len(x),
            'n_silence': len(y),
            'category_mean': float(np.mean(x)),
            'silence_mean': float(np.mean(y)),
            'delta': float(np.mean(x) - np.mean(y)),
            'u_stat': float(u),
            'p_value': float(p),
            'rank_biserial': float(rank_biserial_from_u(u, len(x), len(y))),
        })

tests = pd.DataFrame(rows).sort_values(['comparison','p_value','metric'])
tests.to_csv(OUT_TABLES/'f10_state_category_tests.csv', index=False)

# high-gate silent non-release analysis
silent = tick[tick['did_say']==0].copy()
q = silent['b1_z'].quantile(HI_GATE_QUANTILE)
nearest = []
for t in silent['t'].astype(int):
    nearest.append(min(abs(t-s) for s in say_ticks))
silent['nearest_say_dist'] = nearest
hi = silent[silent['b1_z'] >= q].copy()
hi_nonrelease = hi[hi['nearest_say_dist'] >= HI_GATE_MIN_DIST].copy()

hi_summary = pd.DataFrame([
    {
        'slice_t_min': int(tick['t'].min()),
        'slice_t_max': int(tick['t'].max()),
        'say_events_in_slice': int(len(say_ticks)),
        'silent_ticks': int(len(silent)),
        'hi_gate_quantile': HI_GATE_QUANTILE,
        'hi_gate_threshold_b1_z': float(q),
        'hi_gate_silent_ticks_total': int(len(hi)),
        'hi_gate_silent_ticks_nonrelease_min_dist': HI_GATE_MIN_DIST,
        'hi_gate_silent_ticks_nonrelease_count': int(len(hi_nonrelease)),
        'fraction_of_hi_gate_silent_nonrelease': float(len(hi_nonrelease)/len(hi) if len(hi) else np.nan),
        'mean_b1_z_hi_nonrelease': float(hi_nonrelease['b1_z'].mean()),
        'max_b1_z_hi_nonrelease': float(hi_nonrelease['b1_z'].max()),
        'mean_active_edges_hi_nonrelease': float(hi_nonrelease['active_edges'].mean()),
        'mean_vt_entropy_hi_nonrelease': float(hi_nonrelease['vt_entropy'].mean()),
        'mean_connectome_entropy_hi_nonrelease': float(hi_nonrelease['connectome_entropy'].mean()),
        'mean_vt_coverage_hi_nonrelease': float(hi_nonrelease['vt_coverage'].mean()),
        'has_input_fraction_hi_nonrelease': float(hi_nonrelease['has_input'].mean()),
        'phase_unique_hi_nonrelease': ';'.join(map(str, sorted(hi_nonrelease['phase'].dropna().unique().tolist()))),
        'territories_unique_hi_nonrelease': ';'.join(map(str, sorted(hi_nonrelease['adc_territories'].dropna().unique().tolist()))),
    }
])
hi_summary.to_csv(OUT_TABLES/'f10_high_gate_silence_summary.csv', index=False)

hi_nonrelease.sort_values(['b1_z','nearest_say_dist'], ascending=[False,True]).to_csv(
    OUT_TABLES/'f10_high_gate_silence_examples.csv', index=False
)

# figures
# 1: z-score style deltas vs silence using silence std
sil_stats = sil[METRICS].agg(['mean','std']).T.reset_index().rename(columns={'index':'metric','mean':'silence_mean','std':'silence_std'})
plot_rows = []
for category in ['pre','say','post']:
    sub = tick[tick['state_category']==category]
    means = sub[METRICS].mean()
    for metric in METRICS:
        std = sil_stats.loc[sil_stats['metric']==metric, 'silence_std'].iloc[0]
        base = sil_stats.loc[sil_stats['metric']==metric, 'silence_mean'].iloc[0]
        z = (means[metric] - base) / std if std and not np.isnan(std) else np.nan
        plot_rows.append({'category':category,'metric':metric,'z_vs_silence':z})
plot_df = pd.DataFrame(plot_rows)
plot_pivot = plot_df.pivot(index='metric', columns='category', values='z_vs_silence')[['pre','say','post']]
fig, ax = plt.subplots(figsize=(8,4.8))
plot_pivot.plot(kind='barh', ax=ax)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_title('F10 — State-category shifts vs silence (late slice)')
ax.set_xlabel('Difference vs silence (in silence SD units)')
ax.set_ylabel('Metric')
fig.tight_layout()
fig.savefig(OUT_FIGS/'f10_state_category_zscores.png', dpi=180)
plt.close(fig)

# 2: b1_z distributions
fig, ax = plt.subplots(figsize=(7.5,4.5))
data = [tick.loc[tick['state_category']==cat, 'b1_z'].dropna().values for cat in ['silence','pre','say','post']]
ax.boxplot(data, labels=['silence','pre','say','post'], showfliers=False)
ax.set_title('F10 — b1_z by state category (late slice)')
ax.set_ylabel('b1_z')
fig.tight_layout()
fig.savefig(OUT_FIGS/'f10_b1z_state_distributions.png', dpi=180)
plt.close(fig)

results = {
    'window_ticks': WINDOW,
    'hi_gate_quantile': HI_GATE_QUANTILE,
    'hi_gate_min_dist': HI_GATE_MIN_DIST,
    'say_ticks_in_slice': sorted(map(int, say_ticks)),
    'state_category_counts': tick['state_category'].value_counts().to_dict(),
}
(OUT_DOCS/'F10_results.json').write_text(json.dumps(results, indent=2))
print('F10 outputs written.')
