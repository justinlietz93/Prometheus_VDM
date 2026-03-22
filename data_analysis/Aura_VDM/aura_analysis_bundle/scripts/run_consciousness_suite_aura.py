from __future__ import annotations
import json
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import zscore
from scipy.linalg import det
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.api import VAR
from sklearn.feature_selection import mutual_info_regression

ROOT = Path('/mnt/data/aura_suite_v1')
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
core = pd.read_csv(ROOT / 'timeseries_core_renamed_Aura.csv')
pca = pd.read_csv(ROOT / 'pca_state_space_Aura.csv')
df = core.merge(pca[['t','PC1','PC2','PC3','pca_speed','macro_state']], on='t', how='left')

plt.rcParams.update({'figure.dpi':160, 'savefig.dpi':200, 'font.size':11})

def savefig(name):
    plt.tight_layout()
    plt.savefig(OUT/name, bbox_inches='tight')
    plt.close()

def epoch_slices(df):
    return [(e, d.reset_index(drop=True)) for e,d in df.groupby('epoch', sort=False)]

def gaussian_mi_matrix(X):
    X=np.asarray(X)
    cov=np.cov(X, rowvar=False)
    if cov.ndim==0:
        return 0.0
    cov=np.atleast_2d(cov)+np.eye(cov.shape[0])*1e-9
    n=cov.shape[0]
    tc = 0.5*np.log(np.prod(np.diag(cov))/det(cov))
    dtc = 0.0
    for i in range(n):
        idx=[j for j in range(n) if j!=i]
        cov_wo=np.atleast_2d(np.cov(X[:,idx], rowvar=False))+np.eye(n-1)*1e-9
        dtc += 0.5*np.log(det(cov_wo)/det(cov))
    return tc, dtc, tc-dtc

def mi_gaussian_xy(x,y):
    xy=np.c_[x,y]
    cov=np.cov(xy, rowvar=False)+np.eye(xy.shape[1])*1e-9
    k=x.shape[1]
    covx=cov[:k,:k]; covy=cov[k:,k:]
    return 0.5*np.log(det(covx)*det(covy)/det(cov))

def lz_complexity(bits):
    s=''.join('1' if b else '0' for b in bits)
    i, l, k, c = 0,1,1,1
    n=len(s)
    if n==0: return 0
    while True:
        if i+k>n or l+k>n:
            c += 1; break
        if s[i+k-1]==s[l+k-1]:
            k += 1
        else:
            if k>1:
                i += 1
                if i==l:
                    c += 1
                    l += k
                    if l+1>n: break
                    i=0; k=1
            else:
                c += 1
                l += 1
                if l+1>n: break
                i=0; k=1
    return c

# 1. crosscorr
maxlag=200
for var,name in [('has_text','crosscorr_pca_speed_vs_has_text'), ('log_text_words','crosscorr_pca_speed_vs_log_text_words')]:
    a=zscore(df['pca_speed'].fillna(0).values)
    b=zscore(df[var].fillna(0).values)
    lags=np.arange(-maxlag,maxlag+1)
    cc=[]
    for lag in lags:
        if lag<0: x,y=a[:lag],b[-lag:]
        elif lag>0: x,y=a[lag:],b[:-lag]
        else: x,y=a,b
        if len(x)<10: cc.append(np.nan)
        else: cc.append(np.corrcoef(x,y)[0,1])
    pd.DataFrame({'lag':lags,'crosscorr':cc}).to_csv(OUT/f'{name}.csv', index=False)
    plt.figure(figsize=(8,4)); plt.plot(lags,cc); plt.axvline(0,color='k',lw=1); plt.xlabel('lag (ticks)'); plt.ylabel('corr'); plt.title(name.replace('_',' ')); savefig(f'{name}.png')

# 2. event-triggered
win=120
for var,name in [('has_text','event_triggered_has_text'), ('log_text_words','event_triggered_log_text_words')]:
    events=np.where(df[var].fillna(0).values>0)[0]
    # de-cluster
    sel=[]; last=-10**9
    for idx in events:
        if idx-last>=30:
            sel.append(idx); last=idx
    mats=[]
    for idx in sel:
        if idx-win<0 or idx+win>=len(df): continue
        mats.append(df['pca_speed'].iloc[idx-win:idx+win+1].values)
    if mats:
        avg=np.mean(mats,axis=0); xs=np.arange(-win,win+1)
        plt.figure(figsize=(8,4)); plt.plot(xs,avg); plt.axvline(0,color='k',lw=1); plt.xlabel('ticks from event'); plt.ylabel('mean PCA speed'); plt.title(name.replace('_',' ')); savefig(f'{name}.png')

# 3. LZ complexity pca sign timeseries
sign_state=((pca[['PC1','PC2','PC3']].values>=0).astype(int)).reshape(len(pca),3)
W=200
lz_vals=[]; centers=[]
for i in range(0,len(sign_state)-W+1):
    bits=sign_state[i:i+W].ravel().tolist()
    lz_vals.append(lz_complexity(bits)/len(bits))
    centers.append(int(pca['t'].iloc[i+W//2]))
pd.DataFrame({'t':centers,'lz_pca_sign':lz_vals}).to_csv(OUT/'lz_complexity_pca_sign_timeseries.csv', index=False)
plt.figure(figsize=(10,4)); plt.plot(centers,lz_vals); plt.xlabel('tick'); plt.ylabel('normalized LZ'); plt.title('LZ complexity of PCA sign state'); savefig('lz_complexity_pca_sign_timeseries.png')

# 4. TC/DTC/O in windows
vars_tc=['entropy','complexity','firing_var_log','reward_mean','valence_01','novelty','td_error','void_unique_log','log_text_words']
rows=[]; win=150
for i in range(0,len(df)-win+1,10):
    X=df[vars_tc].iloc[i:i+win].fillna(method='ffill').fillna(method='bfill').fillna(0).values
    tc,dtc,o=gaussian_mi_matrix(X)
    rows.append({'t':int(df['t'].iloc[i+win//2]),'TC':tc,'DTC':dtc,'O_information':o})
wd=pd.DataFrame(rows); wd.to_csv(OUT/'window_TC_DTC_O.csv', index=False)
for col,name in [('TC','TC_timeseries'),('O_information','O_information_timeseries')]:
    plt.figure(figsize=(10,4)); plt.plot(wd['t'],wd[col]); plt.xlabel('tick'); plt.ylabel(col); plt.title(name.replace('_',' ')); savefig(f'{name}.png')

# 5. MIP proxy using singleton minimum cut variable
mip_rows=[]; counts=[]
vars_mip=vars_tc
for i in range(0,len(df)-win+1,10):
    Wd=df[vars_mip].iloc[i:i+win].fillna(method='ffill').fillna(method='bfill').fillna(0)
    X=Wd.values
    cov=np.cov(X,rowvar=False)+np.eye(X.shape[1])*1e-9
    best=None
    for j,var in enumerate(vars_mip):
        x=X[:,[j]]; y=np.delete(X,j,axis=1)
        mi=mi_gaussian_xy(x,y)
        if best is None or mi<best[0]: best=(mi,var)
    mip_rows.append({'t':int(df['t'].iloc[i+win//2]),'mip_integration':best[0],'singleton_variable':best[1]})
    counts.append(best[1])
mip=pd.DataFrame(mip_rows); mip.to_csv(OUT/'mip_integration_timeseries.csv',index=False)
for yscale,name in [('linear','mip_integration_timeseries_linear'),('log','mip_integration_timeseries_log')]:
    plt.figure(figsize=(10,4)); plt.plot(mip['t'],mip['mip_integration']); plt.xlabel('tick'); plt.ylabel('MIP integration proxy'); plt.yscale(yscale); plt.title(name.replace('_',' ')); savefig(f'{name}.png')
count_df=pd.Series(counts).value_counts().rename_axis('variable').reset_index(name='count')
count_df.to_csv(OUT/'mip_singleton_counts_by_epoch.csv', index=False)
plt.figure(figsize=(8,4)); plt.bar(count_df['variable'],count_df['count']); plt.xticks(rotation=45,ha='right'); plt.ylabel('count'); plt.title('MIP singleton variable counts'); savefig('mip_singleton_variable_counts.png')

# 6. predictive MI vs lag PCA by epoch
lags=range(1,1001,10)
mi_rows=[]
for epoch,sub in epoch_slices(pca):
    arr=sub[['PC1','PC2','PC3']].values
    for lag in lags:
        if len(arr)<=lag+10: continue
        mi=mi_gaussian_xy(arr[:-lag], arr[lag:])
        mi_rows.append({'epoch':epoch,'lag':lag,'predictive_mi':mi})
mi_df=pd.DataFrame(mi_rows); mi_df.to_csv(OUT/'predictive_MI_vs_lag_PCA.csv', index=False)
plt.figure(figsize=(9,5))
for epoch,sub in mi_df.groupby('epoch'):
    plt.plot(sub['lag'], sub['predictive_mi'], label=epoch)
plt.legend(fontsize=8); plt.xlabel('lag'); plt.ylabel('Gaussian MI'); plt.title('Predictive MI vs lag (PCA)'); savefig('predictive_MI_vs_lag_PCA_epochs.png')
auc=mi_df.groupby('epoch').apply(lambda g: np.trapz(g['predictive_mi'], g['lag'])).reset_index(name='auc')
peaks=mi_df.loc[mi_df.groupby('epoch')['predictive_mi'].idxmax()][['epoch','lag','predictive_mi']]
auc.to_csv(OUT/'predictive_MI_auc_summary.csv', index=False); peaks.to_csv(OUT/'predictive_MI_top_peaks_PCA_by_epoch.csv', index=False)

# 7. rolling variance/autocorr
for signal_col,prefix in [('entropy','entropy'),('pca_speed','pca_speed')]:
    s=df[signal_col] if signal_col in df.columns else pca[signal_col]
    rv=s.rolling(500,min_periods=100).var()
    ra=s.rolling(500,min_periods=100).apply(lambda x: pd.Series(x).autocorr(lag=1), raw=False)
    pd.DataFrame({'t':df['t'] if signal_col in df.columns else pca['t'],'rolling_variance':rv,'rolling_autocorr_lag1':ra}).to_csv(OUT/f'rolling_var_autocorr_{prefix}.csv',index=False)
    plt.figure(figsize=(10,4)); plt.plot(df['t'] if signal_col in df.columns else pca['t'], rv); plt.xlabel('tick'); plt.ylabel('variance'); plt.title(f'Rolling variance {prefix}'); savefig(f'rolling_variance_{prefix}.png')
    plt.figure(figsize=(10,4)); plt.plot(df['t'] if signal_col in df.columns else pca['t'], ra); plt.xlabel('tick'); plt.ylabel('lag1 autocorr'); plt.title(f'Rolling autocorr {prefix} lag1'); savefig(f'rolling_autocorr_{prefix}_lag1.png')

# 8. spectral slopes
spec_rows=[]
for col,name in [('PC1','PC1'),('entropy','entropy'),('firing_var_log','firing_var_log')]:
    s=(pca[col] if col=='PC1' else df[col]).fillna(method='ffill').fillna(method='bfill').values
    f,P=signal.welch(s, fs=1.0, nperseg=min(1024,len(s)))
    mask=(f>=0.002) & (f<=0.1) & (P>0)
    x=np.log10(f[mask]); y=np.log10(P[mask])
    slope,intercept=np.polyfit(x,y,1)
    spec_rows.append({'signal':col,'slope':slope,'intercept':intercept})
    plt.figure(figsize=(6,4)); plt.scatter(x,y,s=8,alpha=0.6); plt.plot(x,slope*x+intercept,color='r'); plt.xlabel('log10 f'); plt.ylabel('log10 PSD'); plt.title(f'Spectral slope {name}'); savefig(f'spectral_slope_{name}.png')
spec=pd.DataFrame(spec_rows); spec.to_csv(OUT/'spectral_exponent_slopes.csv', index=False)
plt.figure(figsize=(6,4)); plt.scatter(spec['signal'], spec['slope']); plt.ylabel('slope'); plt.title('Spectral slope fit scatter'); savefig('spectral_slope_fit_scatter.png')

# 9. granger fast and standard on core subset by epoch
vars_g=['entropy','complexity','firing_var_log','reward_mean','td_error','void_unique_log']
cd_rows=[]
for epoch,sub in epoch_slices(df):
    sub=sub[vars_g].fillna(method='ffill').fillna(method='bfill').dropna()
    sig=np.zeros((len(vars_g),len(vars_g)),dtype=int)
    pvals=np.ones((len(vars_g),len(vars_g)))
    for i,target in enumerate(vars_g):
        for j,source in enumerate(vars_g):
            if i==j: continue
            try:
                arr=sub[[target,source]]
                res=grangercausalitytests(arr,maxlag=5,verbose=False)
                p=min(res[k][0]['ssr_ftest'][1] for k in res)
            except Exception:
                p=np.nan
            pvals[j,i]=p
            sig[j,i]=int((p<0.05) if np.isfinite(p) else 0)
    pd.DataFrame(pvals,index=vars_g,columns=vars_g).to_csv(OUT/f'granger_fast_pvals_{epoch}.csv')
    pd.DataFrame(sig,index=vars_g,columns=vars_g).to_csv(OUT/f'granger_fast_sig_{epoch}.csv')
    plt.figure(figsize=(6,5)); plt.imshow(sig, cmap='viridis', aspect='auto'); plt.xticks(range(len(vars_g)),vars_g,rotation=45,ha='right'); plt.yticks(range(len(vars_g)),vars_g); plt.title(f'Granger fast sig {epoch}'); plt.colorbar(); savefig(f'granger_fast_sig_heatmap_{epoch}.png')
    cd_rows.append({'epoch':epoch,'causal_density':sig.sum()/(len(vars_g)*(len(vars_g)-1))})
# standard (maxlag 10) only E1 and E2 to save time
for epoch in ['E1_low_entropy_baseline_1','E2_high_entropy_plateau']:
    sub=df[df['epoch']==epoch][vars_g].fillna(method='ffill').fillna(method='bfill').dropna()
    sig=np.zeros((len(vars_g),len(vars_g)),dtype=int); pvals=np.ones((len(vars_g),len(vars_g)))
    for i,target in enumerate(vars_g):
        for j,source in enumerate(vars_g):
            if i==j: continue
            try:
                arr=sub[[target,source]]
                res=grangercausalitytests(arr,maxlag=10,verbose=False)
                p=min(res[k][0]['ssr_ftest'][1] for k in res)
            except Exception:
                p=np.nan
            pvals[j,i]=p; sig[j,i]=int((p<0.05) if np.isfinite(p) else 0)
    pd.DataFrame(pvals,index=vars_g,columns=vars_g).to_csv(OUT/f'granger_pvals_{epoch}.csv')
    pd.DataFrame(sig,index=vars_g,columns=vars_g).to_csv(OUT/f'granger_sig_{epoch}.csv')
    plt.figure(figsize=(6,5)); plt.imshow(sig, cmap='viridis', aspect='auto'); plt.xticks(range(len(vars_g)),vars_g,rotation=45,ha='right'); plt.yticks(range(len(vars_g)),vars_g); plt.title(f'Granger sig {epoch}'); plt.colorbar(); savefig(f'granger_sig_heatmap_{epoch}.png')
cd=pd.DataFrame(cd_rows); cd.to_csv(OUT/'granger_fast_causal_density_by_epoch.csv', index=False)
plt.figure(figsize=(6,4)); plt.bar(cd['epoch'], cd['causal_density']); plt.xticks(rotation=20,ha='right'); plt.ylabel('density'); plt.title('Granger fast causal density'); savefig('granger_fast_causal_density_bar.png')

# 10. macro-state stationary per epoch
markov_rows=[]
for epoch,sub in epoch_slices(pca):
    states=sub['macro_state'].astype(int).values
    K=8
    counts=np.zeros((K,K),dtype=float)
    for a,b in zip(states[:-1],states[1:]): counts[a,b]+=1
    P=np.divide(counts, counts.sum(axis=1,keepdims=True), out=np.zeros_like(counts), where=counts.sum(axis=1,keepdims=True)!=0)
    # stationary approx by eig
    w,v=np.linalg.eig(P.T)
    idx=np.argmin(np.abs(w-1))
    stat=np.real(v[:,idx]); stat=np.maximum(stat,0); stat=stat/stat.sum() if stat.sum()>0 else np.ones(K)/K
    pd.DataFrame({'state':range(K),'stationary_prob':stat}).to_csv(OUT/f'macro_state_stationary_{epoch}.csv', index=False)
    plt.figure(figsize=(7,4)); plt.bar(range(K), stat); plt.xlabel('macro state'); plt.ylabel('stationary prob'); plt.title(f'Macro state stationary {epoch}'); savefig(f'macro_state_stationary_{epoch}.png')
    ent=-(stat*np.log2(np.clip(stat,1e-12,None))).sum()
    markov_rows.append({'epoch':epoch,'stationary_entropy':ent})
pd.DataFrame(markov_rows).to_csv(OUT/'macro_state_markov_entropy_metrics.csv', index=False)

# 11. PCI-like
signals = ['entropy','complexity','firing_var_log','reward_mean','td_error','void_unique_log','coverage','active_edges','omega_mean','a_mean','b1_z','pca_speed']
Z = pd.DataFrame({c:zscore(df[c].fillna(method='ffill').fillna(method='bfill')) if c in df.columns else zscore(pca[c]) for c in signals})
score = (np.abs(Z['td_error']) + np.abs(Z['d_entropy'] if 'd_entropy' in Z.columns else zscore(df['d_entropy'])) if False else 0)
# custom salient score
score = np.abs(zscore(df['td_error'].fillna(0))) + np.abs(zscore(df['d_entropy'].fillna(0))) + np.abs(zscore(pca['pca_speed'].fillna(0))) + np.abs(zscore(df['d_void_unique_log'].fillna(0)))
# select top spaced events
order=np.argsort(-score.values)
events=[]
for idx in order:
    if len(events)>=30: break
    if all(abs(idx-e)>=200 for e in events): events.append(idx)
events=sorted(events)
controls=[]
for idx in np.linspace(200,len(df)-201,30,dtype=int):
    if all(abs(idx-e)>=100 for e in events): controls.append(int(idx))
controls=controls[:30]
def pci_like_at(idx, halfwin=50):
    if idx-halfwin<0 or idx+halfwin>=len(Z): return np.nan, np.nan
    W=Z.iloc[idx-halfwin:idx+halfwin+1].values
    dev=(np.abs(W)>2).astype(int).ravel().tolist()
    lz=lz_complexity(dev)/len(dev)
    density=np.mean(np.abs(W)>2)
    return lz*density, density
pci_e=[]; pci_c=[]
for idx in events:
    v,d=pci_like_at(idx)
    pci_e.append({'t':int(df.iloc[idx]['t']),'pci_like':v,'density':d,'cohesion_components':int(df.iloc[idx]['cohesion_components'])})
for idx in controls:
    v,d=pci_like_at(idx)
    pci_c.append({'t':int(df.iloc[idx]['t']),'pci_like':v,'density':d,'cohesion_components':int(df.iloc[idx]['cohesion_components'])})
pci_e=pd.DataFrame(pci_e); pci_c=pd.DataFrame(pci_c)
pci_e.to_csv(OUT/'pci_like_events.csv', index=False); pci_c.to_csv(OUT/'pci_like_controls.csv', index=False)
pci_epoch=df[['t','epoch']].merge(pci_e[['t','pci_like']],on='t',how='right'); pci_epoch.to_csv(OUT/'pci_like_by_epoch_summary.csv', index=False)
plt.figure(figsize=(6,4)); plt.boxplot([pci_e['pci_like'].dropna(), pci_c['pci_like'].dropna()], labels=['events','controls']); plt.ylabel('PCI-like'); plt.title('PCI-like events vs controls'); savefig('pci_like_events_vs_controls_box.png')
vals=[pci_epoch[pci_epoch['epoch']==e]['pci_like'].dropna() for e in pci_epoch['epoch'].dropna().unique()]
labels=[e for e in pci_epoch['epoch'].dropna().unique()]
plt.figure(figsize=(7,4)); plt.boxplot(vals, labels=labels); plt.xticks(rotation=20,ha='right'); plt.ylabel('PCI-like'); plt.title('PCI-like by epoch'); savefig('pci_like_by_epoch_box.png')
plt.figure(figsize=(6,4)); plt.scatter(pci_e['density'], pci_e['pci_like'], c=pci_e['cohesion_components']); plt.xlabel('active density'); plt.ylabel('PCI-like'); plt.title('PCI components scatter'); savefig('pci_components_scatter.png')

# 12. dashboard heatmap v2 by epoch
# summarize metrics per epoch and zscore across epochs
summary = []
for epoch,sub in df.groupby('epoch',sort=False):
    summary.append({
        'epoch':epoch,
        'LZ_PCA_sign_mean': pd.read_csv(OUT/'lz_complexity_pca_sign_timeseries.csv')['lz_pca_sign'].mean() if True else np.nan,
        'TC_mean': wd[wd['t'].between(sub['t'].min(), sub['t'].max())]['TC'].mean(),
        'O_mean': wd[wd['t'].between(sub['t'].min(), sub['t'].max())]['O_information'].mean(),
        'I_mip_mean': mip[mip['t'].between(sub['t'].min(), sub['t'].max())]['mip_integration'].mean(),
        'macro_eff_states': pca[pca['epoch']==epoch]['macro_state'].nunique(),
        'predMI_auc_1_1000': auc.loc[auc['epoch']==epoch,'auc'].iloc[0] if (auc['epoch']==epoch).any() else np.nan,
        'predMI_lag315': mi_df[(mi_df['epoch']==epoch) & (mi_df['lag'].between(311,319))]['predictive_mi'].mean(),
        'PCI_like_events_mean': pci_epoch[pci_epoch['epoch']==epoch]['pci_like'].mean(),
        'causal_density_alpha0.01': cd.loc[cd['epoch']==epoch,'causal_density'].iloc[0] if (cd['epoch']==epoch).any() else np.nan,
    })
summary_df=pd.DataFrame(summary)
summary_df.to_csv(OUT/'consciousness_metrics_dashboard_by_epoch_v2.csv', index=False)
Zsum=summary_df.copy()
for c in summary_df.columns[1:]:
    vals=summary_df[c].values.astype(float)
    Zsum[c]=(vals-np.nanmean(vals))/ (np.nanstd(vals)+1e-9)
plt.figure(figsize=(12,2.6))
plt.imshow(Zsum.iloc[:,1:].values, aspect='auto', cmap='viridis')
plt.yticks(range(len(Zsum)), Zsum['epoch'])
plt.xticks(range(len(Zsum.columns)-1), Zsum.columns[1:], rotation=45, ha='right')
plt.colorbar(label='z-score across epochs')
plt.title('Consciousness-metric dashboard (relative, z-scored) v2')
savefig('consciousness_metrics_dashboard_heatmap_v2.png')

# 13. Network/H5 figures
import h5py
from collections import Counter
h5_files=sorted(Path('/mnt/data/_aura_pkg').glob('state_*.h5'))
# Use final snapshot for degree distributions and phase portrait from PCA
with h5py.File(h5_files[-1],'r') as hf:
    row_ptr=np.array(hf['sparse/row_ptr']); col_idx=np.array(hf['sparse/col_idx']); W=np.array(hf['sparse/W'])
out_deg=np.diff(row_ptr)
in_deg=np.bincount(col_idx, minlength=len(out_deg))
for deg,name in [(in_deg,'in'),(out_deg,'out')]:
    vals=np.bincount(deg)
    xs=np.arange(len(vals)); pmf=vals/vals.sum(); ccdf=1-np.cumsum(pmf)+pmf
    plt.figure(figsize=(6,4)); plt.bar(xs, pmf); plt.xlim(0, min(len(xs)-1,150)); plt.xlabel(f'{name}-degree'); plt.ylabel('PMF'); plt.title(f'PMF {name}-degree'); savefig(f'pmf_{name}_degree.png')
    plt.figure(figsize=(6,4)); plt.plot(xs[1:], ccdf[1:]); plt.yscale('log'); plt.xscale('log'); plt.xlabel(f'{name}-degree'); plt.ylabel('CCDF'); plt.title(f'CCDF {name}-degree'); savefig(f'ccdf_{name}_degree.png')
plt.figure(figsize=(5,5)); plt.scatter(in_deg,out_deg,s=5,alpha=0.4); plt.xlabel('in-degree'); plt.ylabel('out-degree'); plt.title('In vs out degree'); savefig('in_vs_out_scatter.png')
# jaccard prev tick across H5s
import itertools
sets=[]
for p in h5_files:
    with h5py.File(p,'r') as hf:
        row=np.array(hf['sparse/row_ptr']); col=np.array(hf['sparse/col_idx'])
    es=set()
    for i in range(len(row)-1):
        for j in col[row[i]:row[i+1]]: es.add((i,int(j)))
    sets.append(es)
js=[]; labels=[]
for a,b,p1,p2 in zip(sets[:-1],sets[1:],h5_files[:-1],h5_files[1:]):
    inter=len(a&b); uni=len(a|b); js.append(inter/uni if uni else np.nan); labels.append(f'{p1.stem}->{p2.stem}')
plt.figure(figsize=(8,4)); plt.bar(labels,js); plt.xticks(rotation=30,ha='right'); plt.ylabel('Jaccard'); plt.title('Prev-tick snapshot edge Jaccard'); savefig('14_jaccard_prev_tick.png')
# phase portrait and sie_memory_vs_N proxy using reward/novelty scatter? single N placeholder with late H5 masses not meaningful -> use cumulative say memory vs active edges
plt.figure(figsize=(6,5)); plt.scatter(pca['PC1'], pca['PC2'], c=pd.factorize(pca['epoch'])[0], s=6, alpha=0.5); plt.xlabel('PC1'); plt.ylabel('PC2'); plt.title('Aura phase portrait'); savefig('plot_1k_phase_portrait.png')
plt.figure(figsize=(6,4)); plt.plot(df['t'], np.cumsum(df['say_words'].fillna(0))); plt.xlabel('tick'); plt.ylabel('cumulative say words'); plt.title('SIE memory vs N proxy'); savefig('sie_memory_vs_N.png')

# artifact manifest
manifest=[]
for p in sorted(OUT.glob('*')):
    if p.is_file(): manifest.append({'path':p.name,'bytes':p.stat().st_size})
pd.DataFrame(manifest).to_csv(OUT/'aura_suite_artifact_manifest.csv', index=False)
print('suite complete', len(manifest), 'artifacts')
