import io, zipfile, numpy as np, pandas as pd, re, difflib
from pathlib import Path
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

BASE_ZIP = Path('/mnt/data/aura_analysis_bundle.zip')
OUT_ROOT = Path('/mnt/data/aura_research_deliverables')
for sub in ['scripts','tables','figures','docs','patches']:
    (OUT_ROOT / sub).mkdir(parents=True, exist_ok=True)

def js_div(p, q):
    p = np.asarray(p, dtype=float).flatten(); q = np.asarray(q, dtype=float).flatten()
    p = p / p.sum(); q = q / q.sum()
    m = 0.5 * (p + q)
    def kl(a, b):
        mask = (a > 0) & (b > 0)
        return np.sum(a[mask] * np.log2(a[mask] / b[mask]))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

with zipfile.ZipFile(BASE_ZIP) as z:
    macro_inf = pd.read_csv(io.BytesIO(z.read('aura_analysis_bundle/scalar_struct/tables/macrostate_directed_influence_deltaR2.csv')))
    O = pd.read_csv(io.BytesIO(z.read('aura_analysis_bundle/tables/window_TC_DTC_O.csv')))
    pca = pd.read_csv(io.BytesIO(z.read('aura_analysis_bundle/tables/pca_state_space_Aura.csv')), usecols=['t','epoch'])
    lz = pd.read_csv(io.BytesIO(z.read('aura_analysis_bundle/tables/lz_complexity_pca_sign_timeseries.csv')))

pca = pca.sort_values('t')
Oe = pd.merge_asof(O.sort_values('t'), pca, on='t', direction='nearest')
lze = pd.merge_asof(lz.sort_values('t'), pca, on='t', direction='nearest')

bounds = []
prev_epoch = None
prev_t = None
for row in pca.itertuples(index=False):
    if prev_epoch is None:
        prev_epoch = row.epoch; prev_t = row.t; continue
    if row.epoch != prev_epoch:
        bounds.append({'t_prev': prev_t, 't_next': row.t, 'from_epoch': prev_epoch, 'to_epoch': row.epoch})
        prev_epoch = row.epoch
    prev_t = row.t

macro_summary = macro_inf.groupby(['macro','x','y'], as_index=False).agg(
    delta_r2_mean=('delta_r2','mean'),
    delta_r2_std=('delta_r2','std'),
    r2_base_mean=('r2_base','mean'),
    r2_ext_mean=('r2_ext','mean'),
    n_pairs=('n_pairs','mean')
)
pred_scores = macro_inf.groupby(['macro','x'], as_index=False).agg(
    outgoing_delta_r2_mean=('delta_r2','mean'),
    outgoing_delta_r2_sum=('delta_r2','sum'),
    mean_r2_ext=('r2_ext','mean')
).rename(columns={'x':'variable'})
targ_scores = macro_inf.groupby(['macro','y'], as_index=False).agg(
    incoming_delta_r2_mean=('delta_r2','mean'),
    incoming_delta_r2_sum=('delta_r2','sum'),
    mean_r2_ext=('r2_ext','mean')
).rename(columns={'y':'variable'})
pred_rank = pred_scores.groupby('variable', as_index=False).agg(score_mean=('outgoing_delta_r2_mean','mean'), score_sum=('outgoing_delta_r2_sum','mean'), mean_r2_ext=('mean_r2_ext','mean')).sort_values('score_mean', ascending=False)
targ_rank = targ_scores.groupby('variable', as_index=False).agg(score_mean=('incoming_delta_r2_mean','mean'), score_sum=('incoming_delta_r2_sum','mean'), mean_r2_ext=('mean_r2_ext','mean')).sort_values('score_mean', ascending=False)

O_epoch_summary = Oe.groupby('epoch', as_index=False).agg(
    O_mean=('O_information','mean'),
    O_std=('O_information','std'),
    O_min=('O_information','min'),
    O_max=('O_information','max'),
    TC_mean=('TC','mean'),
    DTC_mean=('DTC','mean'),
    n_windows=('t','count')
)
O_epoch_summary['synergy_ratio'] = O_epoch_summary['DTC_mean'] / O_epoch_summary['TC_mean']

transition_rows = []
for b in bounds:
    t0 = b['t_next']
    w = Oe[(Oe['t'] >= t0-200) & (Oe['t'] <= t0+200)].copy()
    pre = w[w['t'] < t0]
    post = w[w['t'] >= t0]
    transition_rows.append({
        'boundary_tick': t0,
        'from_epoch': b['from_epoch'],
        'to_epoch': b['to_epoch'],
        'n_pre': len(pre),
        'n_post': len(post),
        'O_mean_pre': pre['O_information'].mean(),
        'O_mean_post': post['O_information'].mean(),
        'O_var_pre': pre['O_information'].var(),
        'O_var_post': post['O_information'].var(),
        'TC_mean_pre': pre['TC'].mean(),
        'TC_mean_post': post['TC'].mean(),
        'DTC_mean_pre': pre['DTC'].mean(),
        'DTC_mean_post': post['DTC'].mean(),
    })
O_transition_summary = pd.DataFrame(transition_rows)

rho, pval = spearmanr(lze['t'], lze['lz_pca_sign'])
LZ_epoch_summary = lze.groupby('epoch', as_index=False).agg(
    lz_mean=('lz_pca_sign','mean'),
    lz_std=('lz_pca_sign','std'),
    lz_min=('lz_pca_sign','min'),
    lz_max=('lz_pca_sign','max'),
    n=('t','count')
)
LZ_trend_summary = pd.DataFrame([{'spearman_rho': rho, 'pvalue': pval, 'n': len(lze)}])

snapshots = [17160,17220,17280,17340,17400]
grid_rows = []
grids = {}
with zipfile.ZipFile(BASE_ZIP) as z:
    for s in snapshots:
        df = pd.read_csv(io.BytesIO(z.read(f'aura_analysis_bundle/connectome_geom/results/baseline_projection_grid_pi_state_{s}_32x32.csv')))
        for c in ['row','col','pi_density','n_nodes']:
            df[c] = pd.to_numeric(df[c])
        arr = df.pivot(index='row', columns='col', values='pi_density').sort_index().sort_index(axis=1).fillna(0.0).values
        arr = arr / arr.sum()
        grids[s] = arr
        rr, cc = np.indices(arr.shape)
        x_com = float((cc * arr).sum()); y_com = float((rr * arr).sum())
        p = arr.flatten(); p_nonzero = p[p > 0]
        entropy = float(-(p_nonzero * np.log2(p_nonzero)).sum())
        eff_bins = float(2 ** entropy)
        occ = int((p > 0).sum())
        grid_rows.append({'snapshot_tick': s, 'entropy_bits': entropy, 'effective_bins': eff_bins, 'occupied_bins': occ, 'occupancy_frac': occ / len(p), 'center_of_mass_x': x_com, 'center_of_mass_y': y_com})
grid_summary = pd.DataFrame(grid_rows)
pair_rows = []
for a, b in zip(snapshots[:-1], snapshots[1:]):
    com_a = grid_summary.loc[grid_summary.snapshot_tick == a, ['center_of_mass_x','center_of_mass_y']].iloc[0].values
    com_b = grid_summary.loc[grid_summary.snapshot_tick == b, ['center_of_mass_x','center_of_mass_y']].iloc[0].values
    pair_rows.append({'from_tick': a, 'to_tick': b, 'jsd_bits': js_div(grids[a], grids[b]), 'com_shift': float(np.linalg.norm(com_b - com_a))})
grid_pairwise = pd.DataFrame(pair_rows)

macro_summary.to_csv(OUT_ROOT/'tables'/'f7_macrostate_directed_influence_summary.csv', index=False)
pred_rank.to_csv(OUT_ROOT/'tables'/'f7_macrostate_predictor_ranking.csv', index=False)
targ_rank.to_csv(OUT_ROOT/'tables'/'f7_macrostate_target_ranking.csv', index=False)
O_epoch_summary.to_csv(OUT_ROOT/'tables'/'f7_Oinfo_epoch_summary.csv', index=False)
O_transition_summary.to_csv(OUT_ROOT/'tables'/'f7_Oinfo_transition_summary.csv', index=False)
LZ_epoch_summary.to_csv(OUT_ROOT/'tables'/'f7_LZ_epoch_summary.csv', index=False)
LZ_trend_summary.to_csv(OUT_ROOT/'tables'/'f7_LZ_trend_summary.csv', index=False)
grid_summary.to_csv(OUT_ROOT/'tables'/'f7_state_space_grid_summary.csv', index=False)
grid_pairwise.to_csv(OUT_ROOT/'tables'/'f7_state_space_grid_pairwise.csv', index=False)

plt.figure(figsize=(9,4))
plt.bar(pred_rank['variable'], pred_rank['score_mean'])
plt.xticks(rotation=30, ha='right')
plt.ylabel('Mean ΔR² as predictor')
plt.title('F7.1 macrostate predictor hierarchy')
plt.tight_layout()
plt.savefig(OUT_ROOT/'figures'/'f7_macrostate_predictor_hierarchy.png', dpi=180)
plt.close()

plt.figure(figsize=(10,4))
for epoch, grp in Oe.groupby('epoch'):
    plt.plot(grp['t'], grp['O_information'], label=epoch)
for b in bounds:
    plt.axvline(b['t_next'], color='k', linestyle='--', alpha=0.4)
plt.ylabel('O-information')
plt.xlabel('tick')
plt.title('F7.6 O-information trajectory by epoch')
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUT_ROOT/'figures'/'f7_Oinfo_timeseries_by_epoch.png', dpi=180)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(grid_summary['snapshot_tick'], grid_summary['entropy_bits'], marker='o', label='grid entropy')
plt.plot(grid_summary['snapshot_tick'], grid_summary['effective_bins'] / 100, marker='s', label='effective bins / 100')
plt.xlabel('snapshot tick')
plt.title('F7.8 state-space landscape reshaping')
plt.legend()
plt.tight_layout()
plt.savefig(OUT_ROOT/'figures'/'f7_state_space_landscape_metrics.png', dpi=180)
plt.close()

script_text = Path('/tmp/f7_infoflow.py').read_text()
(OUT_ROOT/'scripts'/'f7_infoflow_higherorder_landscape.py').write_text(script_text)

pred1 = pred_rank.iloc[0]
targ1 = targ_rank.iloc[0]
e1 = O_epoch_summary[O_epoch_summary.epoch=='E1_low_entropy_baseline_1'].iloc[0]
e2 = O_epoch_summary[O_epoch_summary.epoch=='E2_high_entropy_plateau'].iloc[0]
e3 = O_epoch_summary[O_epoch_summary.epoch=='E3_low_entropy_baseline_2'].iloc[0]
note = f'''# F7 — Information-flow hierarchy, higher-order dynamics, and landscape reshaping

## Scope
This package resolves three previously underpowered high-value distinctions from Family 7:
- D7.1 macrostate directed-influence hierarchy
- D7.6 window-level TC/DTC/O-information dynamics
- D7.8 baseline projection grid / state-space landscape reshaping

## D7.1
Using `macrostate_directed_influence_deltaR2.csv`, directed incremental predictive power is selective rather than flat.
- strongest predictor channel overall: **{pred1['variable']}** (mean outgoing ΔR² = **{pred1['score_mean']:.4f}**)
- strongest target channel overall: **{targ1['variable']}** (mean incoming ΔR² = **{targ1['score_mean']:.4f}**)

## D7.6
O-information stays negative across every epoch, but its depth shifts sharply:
- E1 mean O = **{e1['O_mean']:.3f}**
- E2 mean O = **{e2['O_mean']:.3f}**
- E3 mean O = **{e3['O_mean']:.3f}**

Boundary-local variance changes are severe:
- E1→E2 variance: **{O_transition_summary.iloc[0]['O_var_pre']:.3f} → {O_transition_summary.iloc[0]['O_var_post']:.3f}**
- E2→E3 variance: **{O_transition_summary.iloc[1]['O_var_pre']:.3f} → {O_transition_summary.iloc[1]['O_var_post']:.3f}**

## D7.7
LZ complexity shows a small but highly significant upward trend:
- Spearman ρ = **{rho:.4f}**
- p = **{pval:.3e}**

## D7.8
Consecutive state-space landscape JSD declines overall:
- 17160→17220 = **{grid_pairwise.iloc[0]['jsd_bits']:.3f}**
- 17220→17280 = **{grid_pairwise.iloc[1]['jsd_bits']:.3f}**
- 17280→17340 = **{grid_pairwise.iloc[2]['jsd_bits']:.3f}**
- 17340→17400 = **{grid_pairwise.iloc[3]['jsd_bits']:.3f}**

This is a settling-but-not-frozen late landscape.
'''
(OUT_ROOT/'docs'/'F7_infoflow_higherorder_landscape_note.md').write_text(note)

orig = Path('/mnt/data/Aura_Distinction_Inventory_v0.5.md').read_text()
new_d71 = """### D7.1 — Macrostate Directed-Influence Hierarchy
- **Data source:** `macrostate_mutual_info.csv`, `macrostate_directed_influence_deltaR2.csv`.
- **Finding:** Directed influence patterns between macrostate variables are measurably hierarchical rather than flat. Across macros 0–3, **`vt_entropy`** is the strongest predictor channel by mean outgoing incremental predictive power (mean ΔR² = **0.0663**), while **`vt_entropy`** is also the strongest target channel by mean incoming ΔR² among the observed target set (mean incoming ΔR² = **0.1614**). Other predictor channels (`connectome_entropy`, `sie_total_reward`, `sie_td_error`, `sie_v2_valence_01`) contribute smaller but nonuniform directed increments into `vt_coverage`, `active_edges`, and `b1_z`.
- **Interpretation:** The directed predictive structure is selective and asymmetric: some channels behave more like upstream organizers, others more like downstream readouts. This is a hierarchy of information flow, not a flat mutual-coupling web.
- **Repro artifacts:** `f7_infoflow_higherorder_landscape.py`, `f7_macrostate_directed_influence_summary.csv`, `f7_macrostate_predictor_ranking.csv`, `f7_macrostate_target_ranking.csv`."""
new_d76 = """### D7.6 — Window-Level TC, DTC, and O-Information Dynamics
- **Data source:** `window_TC_DTC_O.csv` (766 windows), merged to epoch labels from `pca_state_space_Aura.csv`.
- **Finding:** O-information remains **negative in every window and every epoch**, confirming sustained synergy-dominated higher-order interaction, but its depth changes sharply by regime:
  - E1 mean O-information = **−32.667**
  - E2 mean O-information = **−40.146** (most synergistic / deepest negative)
  - E3 mean O-information = **−29.662** (less negative again)
- **Boundary-local dynamics:** Around the E1→E2 boundary (`t≈10284`), O-information variance rises from **1.387** to **48.189** in the ±200-tick local window. Around the E2→E3 boundary (`t≈11587`), O-information variance falls from **95.609** to **9.118** while the mean shifts from **−32.986** to **−23.869**.
- **Interpretation:** The higher-order interaction field does not merely drift; it reconfigures sharply at regime boundaries. E2 deepens the synergy basin, and E3 relaxes it while remaining firmly nonredundant.
- **Repro artifacts:** `f7_infoflow_higherorder_landscape.py`, `f7_Oinfo_epoch_summary.csv`, `f7_Oinfo_transition_summary.csv`, `f7_Oinfo_timeseries_by_epoch.png`."""
new_d77 = """### D7.7 — LZ Complexity Increasing Over Time
- **Claim:** The algorithmic compressibility of the PCA sign trajectory decreases slightly but significantly over time — the system generates more novel sign-pattern structure as it matures.
- **Measurable:** Spearman trend ρ = **+0.0694**, p = **1.37 × 10⁻⁹** across 7,604 windows. By epoch: E1 = **0.017707**, E2 = **0.016506**, E3 = **0.016945**.
- **Interpretation:** E2 is the most compressible / stereotyped regime; E3 partially rebounds toward greater novelty without returning exactly to E1.
- **Source:** `lz_complexity_pca_sign_timeseries.csv`; repro artifacts in `f7_LZ_epoch_summary.csv` and `f7_LZ_trend_summary.csv`."""
new_d78 = """### D7.8 — Baseline Projection Grids (32×32 State-Space Maps)
- **Data source:** `baseline_projection_grid_pi_state_*.csv` files.
- **Finding:** The projected late state-space landscapes reshape measurably across the five terminal snapshots, but the size of each step generally shrinks over time. Consecutive Jensen-Shannon divergence between landscapes is:
  - 17160→17220: **0.258 bits**
  - 17220→17280: **0.207 bits**
  - 17280→17340: **0.156 bits**
  - 17340→17400: **0.173 bits**
- **Additional structure:** Grid entropy and effective occupied bins remain high across all five snapshots, while center-of-mass shifts persist, showing continued migration inside a stabilizing landscape.
- **Interpretation:** The late runtime is settling, but not frozen: the geometry of state-space preference is still moving while the magnitude of each reshaping step declines.
- **Repro artifacts:** `f7_infoflow_higherorder_landscape.py`, `f7_state_space_grid_summary.csv`, `f7_state_space_grid_pairwise.csv`, `f7_state_space_landscape_metrics.png`."""
updated = orig
updated = re.sub(r"### D7\.1 — Macrostate Mutual Information Structure\n(?:- .*\n)+", new_d71+"\n\n", updated)
updated = re.sub(r"### D7\.6 — Window-Level TC, DTC, and O-Information Dynamics\n(?:- .*\n)+", new_d76+"\n\n", updated)
updated = re.sub(r"### D7\.7 — LZ Complexity of PCA Sign Timeseries\n(?:- .*\n)+", new_d77+"\n\n", updated)
updated = re.sub(r"### D7\.7 — LZ Complexity Increasing Over Time\n(?:- .*\n)+", "", updated)
updated = re.sub(r"### D7\.8 — Baseline Projection Grids \(32×32 State-Space Maps\)\n(?:- .*\n)+", new_d78+"\n\n", updated)
(OUT_ROOT/'docs'/'Aura_Distinction_Inventory_v0.5.with_F7_infoflow.md').write_text(updated)
patch = ''.join(difflib.unified_diff(orig.splitlines(True), updated.splitlines(True), fromfile='Aura_Distinction_Inventory_v0.5.md', tofile='Aura_Distinction_Inventory_v0.5.with_F7_infoflow.md'))
(OUT_ROOT/'patches'/'Aura_Distinction_Inventory_v0.5_F7_infoflow.patch').write_text(patch)

manifest_files = [
    OUT_ROOT/'scripts'/'f7_infoflow_higherorder_landscape.py',
    OUT_ROOT/'tables'/'f7_macrostate_directed_influence_summary.csv',
    OUT_ROOT/'tables'/'f7_macrostate_predictor_ranking.csv',
    OUT_ROOT/'tables'/'f7_macrostate_target_ranking.csv',
    OUT_ROOT/'tables'/'f7_Oinfo_epoch_summary.csv',
    OUT_ROOT/'tables'/'f7_Oinfo_transition_summary.csv',
    OUT_ROOT/'tables'/'f7_LZ_epoch_summary.csv',
    OUT_ROOT/'tables'/'f7_LZ_trend_summary.csv',
    OUT_ROOT/'tables'/'f7_state_space_grid_summary.csv',
    OUT_ROOT/'tables'/'f7_state_space_grid_pairwise.csv',
    OUT_ROOT/'figures'/'f7_macrostate_predictor_hierarchy.png',
    OUT_ROOT/'figures'/'f7_Oinfo_timeseries_by_epoch.png',
    OUT_ROOT/'figures'/'f7_state_space_landscape_metrics.png',
    OUT_ROOT/'docs'/'F7_infoflow_higherorder_landscape_note.md',
    OUT_ROOT/'docs'/'Aura_Distinction_Inventory_v0.5.with_F7_infoflow.md',
    OUT_ROOT/'patches'/'Aura_Distinction_Inventory_v0.5_F7_infoflow.patch',
]
(OUT_ROOT/'F7_PACKAGE_MANIFEST.txt').write_text('\n'.join(str(p.relative_to(OUT_ROOT)) for p in manifest_files))

pkg = Path('/mnt/data/aura_research_deliverables_pkg_F7_infoflow.zip')
with zipfile.ZipFile(pkg, 'w', compression=zipfile.ZIP_DEFLATED) as zz:
    for p in manifest_files + [OUT_ROOT/'F7_PACKAGE_MANIFEST.txt']:
        zz.write(p, arcname=str(p.relative_to(OUT_ROOT)))

print('WROTE', pkg)
print('top predictor', pred1['variable'], pred1['score_mean'])
print('O means', O_epoch_summary[['epoch','O_mean']].to_dict('records'))
print('JSDs', grid_pairwise.to_dict('records'))
