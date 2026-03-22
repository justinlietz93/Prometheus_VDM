
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

base = Path("/mnt/data/work_aura/aura_analysis_bundle")
out = Path("/mnt/data/aura_research_deliverables_F7_pending")
for sub in ['tables','figures']:
    (out/sub).mkdir(parents=True, exist_ok=True)

# D7.2
E = pd.read_csv(base/'scalar_struct/tables/micro_transition_eigvals.csv')
E['mode_rank'] = np.arange(len(E))
E['implied_timescale_ticks'] = np.where(E['eigval'].abs() < 1, -1/np.log(E['eigval'].abs()), np.inf)
E['implied_timescale_minutes'] = E['implied_timescale_ticks'] * 2.58 / 60.0
P = pd.read_csv(base/'scalar_struct/tables/micro_transition_matrix_P.csv')
P = pd.DataFrame(P.values.astype(float))
row_summary = pd.DataFrame({
    'micro_state': np.arange(len(P)),
    'self_transition_prob': np.diag(P),
    'row_entropy_bits': -np.nansum(np.where(P.values>0, P.values*np.log2(P.values), 0), axis=1),
}).sort_values(['self_transition_prob','row_entropy_bits'], ascending=[False,True])
E.to_csv(out/'tables/d7_2_micro_transition_spectrum.csv', index=False)
row_summary.to_csv(out/'tables/d7_2_micro_transition_rows.csv', index=False)

# D7.4
pca_epoch = pd.read_csv(base/'tables/pca_state_space_Aura.csv')[['t','epoch']]
roll_summaries=[]; boundary_rows=[]
for name in ['entropy','pca_speed']:
    df = pd.read_csv(base/f'tables/rolling_var_autocorr_{name}.csv')
    m = df.merge(pca_epoch, on='t', how='left').dropna()
    summ = m.groupby('epoch')[['rolling_variance','rolling_autocorr_lag1']].agg(['mean','median','max','min']).reset_index()
    summ.columns = ['epoch'] + [f'{a}_{b}' for a,b in summ.columns.tolist()[1:]]
    summ['channel'] = name
    roll_summaries.append(summ)
    for b,label in [(10284,'E1_to_E2'),(11587,'E2_to_E3')]:
        pre = m[(m.t>=b-200)&(m.t<b)]
        post = m[(m.t>=b)&(m.t<b+200)]
        boundary_rows.append({
            'channel': name, 'boundary': label,
            'pre_var_mean': pre['rolling_variance'].mean(),
            'post_var_mean': post['rolling_variance'].mean(),
            'pre_ac_mean': pre['rolling_autocorr_lag1'].mean(),
            'post_ac_mean': post['rolling_autocorr_lag1'].mean(),
        })
pd.concat(roll_summaries, ignore_index=True).to_csv(out/'tables/d7_4_rolling_epoch_summary.csv', index=False)
pd.DataFrame(boundary_rows).to_csv(out/'tables/d7_4_boundary_window_summary.csv', index=False)

# D7.5
pm = pd.read_csv(base/'tables/predictive_MI_vs_lag_PCA.csv')
rows=[]
for ep,g in pm.groupby('epoch'):
    h = g[(g['lag']>=100)&(g['lag']<=600)].reset_index(drop=True)
    vals = h['predictive_mi'].values
    lags = h['lag'].values
    peaks=[]
    for i in range(1, len(vals)-1):
        if vals[i] > vals[i-1] and vals[i] >= vals[i+1]:
            peaks.append((int(lags[i]), float(vals[i])))
    peaks = sorted(peaks, key=lambda x:x[1], reverse=True)
    for rank,(lag,mi) in enumerate(peaks[:5], start=1):
        rows.append({'epoch':ep,'rank':rank,'lag':lag,'predictive_mi':mi})
pd.DataFrame(rows).to_csv(out/'tables/d7_5_predictive_mi_longlag_peaks.csv', index=False)
pm[(pm['lag']>=100)&(pm['lag']<=600)].to_csv(out/'tables/d7_5_predictive_mi_100_600.csv', index=False)

# D7.9
import glob, os
metric_rows=[]; effect_rows=[]
for f in sorted(glob.glob(str(base/'connectome_geom/results/node_embedding_metrics_state_*.csv'))):
    t = int(Path(f).stem.split('_')[-1])
    df = pd.read_csv(f)
    metric_rows.append({'snapshot_t': t, 'community_count': int(df['community'].nunique())})
    for mname in ['out_degree','participation','convergence_score','pagerank','row_weight_param']:
        grand = df[mname].mean(); ssb = sum(len(g)*(g[mname].mean()-grand)**2 for _,g in df.groupby('community')); sst = ((df[mname]-grand)**2).sum()
        effect_rows.append({'snapshot_t':t,'metric':mname,'eta_squared_by_community':ssb/sst})
pd.DataFrame(metric_rows).to_csv(out/'tables/d7_9_node_embedding_snapshot_summary.csv', index=False)
pd.DataFrame(effect_rows).to_csv(out/'tables/d7_9_node_embedding_effect_sizes.csv', index=False)
