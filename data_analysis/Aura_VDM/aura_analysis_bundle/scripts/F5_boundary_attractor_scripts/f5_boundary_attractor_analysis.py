from pathlib import Path
import zipfile, io, json
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC_ZIP = Path("/mnt/data/batch1_results.zip")
OUT = Path("/mnt/data/aura_research_deliverables_F5")
for sub in ["scripts","tables","figures","docs","patches"]:
    (OUT/sub).mkdir(parents=True, exist_ok=True)

zf = zipfile.ZipFile(SRC_ZIP)
ts = pd.read_csv(io.BytesIO(zf.read('batch1_results/F5_boundary_motif_timeseries.csv')))
roll = pd.read_csv(io.BytesIO(zf.read('batch1_results/F5_boundary_motif_rolling.csv')))
book_tl = pd.read_csv(io.BytesIO(zf.read('batch1_results/book_feed_timeline.csv')))
master = json.loads(zf.read('batch1_results/batch1_fixed_master_results.json'))

ts['motif_hits'] = ts['motif_hits'].fillna(0)
ts['motif_density'] = ts['motif_density'].fillna(0)
ts['motif_nonzero'] = (ts['motif_hits'] > 0).astype(int)

by_epoch = pd.DataFrame(master['D5_boundary_motif_tracking']['by_epoch']).T.reset_index().rename(columns={'index':'epoch'})
by_epoch.to_csv(OUT/'tables/f5_boundary_motif_epoch_summary.csv', index=False)

by_book = ts.groupby('active_book').agg(
    n_events=('t','size'),
    nonzero_fraction=('motif_nonzero','mean'),
    mean_density=('motif_density','mean'),
    median_density=('motif_density','median'),
    total_motif_hits=('motif_hits','sum'),
    max_density=('motif_density','max')
).reset_index().sort_values('n_events', ascending=False)
by_book.to_csv(OUT/'tables/f5_boundary_motif_active_book_summary.csv', index=False)

runs=[]
mask = ts['motif_nonzero'].to_numpy()
start = 0
cur = int(mask[0])
for i,v in enumerate(mask[1:],1):
    if int(v) != cur:
        seg = ts.iloc[start:i]
        runs.append({
            'motif_nonzero':cur,'start_idx':start,'end_idx':i-1,'start_t':int(seg['t'].iloc[0]),'end_t':int(seg['t'].iloc[-1]),'n_events':len(seg),
            'book_start':seg['active_book'].iloc[0],'book_end':seg['active_book'].iloc[-1],'n_active_books':seg['active_book'].nunique(),
            'sum_motif_hits':float(seg['motif_hits'].sum()),'mean_motif_density':float(seg['motif_density'].mean())
        })
        start=i; cur=int(v)
seg = ts.iloc[start:]
runs.append({
    'motif_nonzero':cur,'start_idx':start,'end_idx':len(ts)-1,'start_t':int(seg['t'].iloc[0]),'end_t':int(seg['t'].iloc[-1]),'n_events':len(seg),
    'book_start':seg['active_book'].iloc[0],'book_end':seg['active_book'].iloc[-1],'n_active_books':seg['active_book'].nunique(),
    'sum_motif_hits':float(seg['motif_hits'].sum()),'mean_motif_density':float(seg['motif_density'].mean())
})
runs_df = pd.DataFrame(runs)
runs_df.to_csv(OUT/'tables/f5_boundary_motif_runs.csv', index=False)
run_summary = runs_df.groupby('motif_nonzero').agg(
    n_runs=('n_events','size'),
    mean_run_events=('n_events','mean'),
    median_run_events=('n_events','median'),
    max_run_events=('n_events','max'),
    cross_book_runs=('n_active_books', lambda s: int((s>1).sum()))
).reset_index()
run_summary.to_csv(OUT/'tables/f5_boundary_motif_run_summary.csv', index=False)

switch_rows=[]
active_list = ts['active_book'].tolist()
for i in range(1,len(active_list)):
    if active_list[i] != active_list[i-1]:
        before = ts.iloc[max(0, i-10):i]
        after = ts.iloc[i:min(len(ts), i+10)]
        switch_rows.append({
            'switch_event_index':i,'switch_tick':int(ts.iloc[i]['t']),'book_from':active_list[i-1],'book_to':active_list[i],
            'before_n':len(before),'after_n':len(after),
            'before_nonzero_fraction':float(before['motif_nonzero'].mean()) if len(before) else np.nan,
            'after_nonzero_fraction':float(after['motif_nonzero'].mean()) if len(after) else np.nan,
            'before_mean_density':float(before['motif_density'].mean()) if len(before) else np.nan,
            'after_mean_density':float(after['motif_density'].mean()) if len(after) else np.nan,
            'before_total_hits':float(before['motif_hits'].sum()) if len(before) else np.nan,
            'after_total_hits':float(after['motif_hits'].sum()) if len(after) else np.nan,
        })
pd.DataFrame(switch_rows).to_csv(OUT/'tables/f5_boundary_motif_source_switch_carryover.csv', index=False)

acf_rows=[]
for lag in range(1,51):
    acf_rows.append({'lag_events':lag,'acf_motif_nonzero':float(ts['motif_nonzero'].autocorr(lag=lag)),'acf_motif_density':float(ts['motif_density'].autocorr(lag=lag))})
pd.DataFrame(acf_rows).to_csv(OUT/'tables/f5_boundary_motif_autocorr.csv', index=False)

rolling_summary = pd.DataFrame([{
    'n_windows':len(roll),'mean_rolling_nonzero_fraction':float(roll['rolling_nonzero_fraction'].mean()),
    'median_rolling_nonzero_fraction':float(roll['rolling_nonzero_fraction'].median()),'min_rolling_nonzero_fraction':float(roll['rolling_nonzero_fraction'].min()),
    'max_rolling_nonzero_fraction':float(roll['rolling_nonzero_fraction'].max()),'fraction_windows_nonzero_gt_0_3':float((roll['rolling_nonzero_fraction']>0.3).mean()),
    'fraction_windows_nonzero_gt_0':float((roll['rolling_nonzero_fraction']>0).mean()),'spearman_rho_density_trend':master['D5_boundary_motif_tracking']['trend_test']['spearman_rho'],
    'trend_p_value':master['D5_boundary_motif_tracking']['trend_test']['p_value']
}])
rolling_summary.to_csv(OUT/'tables/f5_boundary_motif_rolling_summary.csv', index=False)

plt.figure(figsize=(10,4.8))
plt.plot(roll['t_center'], roll['rolling_nonzero_fraction'], label='Rolling nonzero fraction')
plt.plot(roll['t_center'], roll['rolling_motif_density'], label='Rolling motif density')
for _,r in book_tl.dropna().iterrows():
    plt.axvline(r['tick'], linestyle='--', linewidth=1)
plt.xlabel('tick center'); plt.ylabel('rolling value'); plt.title('Boundary-attractor rolling dynamics with source switches'); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'figures/f5_boundary_attractor_rolling.png', dpi=160); plt.close()

plt.figure(figsize=(9,4.8))
order = by_book.sort_values('nonzero_fraction', ascending=False)
plt.barh(order['active_book'], order['nonzero_fraction'])
plt.xlabel('fraction of events with boundary motif'); plt.title('Boundary motif persists across all active-book regimes'); plt.tight_layout(); plt.savefig(OUT/'figures/f5_boundary_attractor_by_book.png', dpi=160); plt.close()

plt.figure(figsize=(8,4.8))
acf_df = pd.read_csv(OUT/'tables/f5_boundary_motif_autocorr.csv')
plt.plot(acf_df['lag_events'], acf_df['acf_motif_nonzero'], label='binary motif presence')
plt.plot(acf_df['lag_events'], acf_df['acf_motif_density'], label='motif density')
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('lag (events)'); plt.ylabel('autocorrelation'); plt.title('Event-level motif autocorrelation'); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'figures/f5_boundary_attractor_autocorr.png', dpi=160); plt.close()
