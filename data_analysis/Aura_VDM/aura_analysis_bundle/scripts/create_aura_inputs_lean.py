from __future__ import annotations
import json, re
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT=Path('/mnt/data')
AURA=ROOT/'_aura_pkg'
EVENTS_PARTS=ROOT/'_events_parts'
OUT=ROOT/'aura_suite_v1'
OUT.mkdir(exist_ok=True)
WORD_RE=re.compile(r"\b\w+\b", re.UNICODE)

# Parse UTD shards, keep only needed information
status_rows=[]; text_stats={}; say_rows=[]; cur_t=0
for p in sorted((AURA/'utd_events').glob('*.txt')):
    with p.open('r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            if not line.startswith('{'): continue
            rec=json.loads(line)
            typ=rec.get('type')
            if typ=='text':
                payload=rec.get('payload',{}) or {}
                ptype=payload.get('type')
                if ptype=='status':
                    cur_t=int(payload['t'])
                    status_rows.append({
                        't':cur_t,
                        'phase':payload.get('phase'),
                        'cohesion_components':payload.get('cohesion_components'),
                        'vt_coverage':payload.get('vt_coverage'),
                        'vt_entropy':payload.get('vt_entropy'),
                        'connectome_entropy_status':payload.get('connectome_entropy'),
                        'active_edges_status':payload.get('active_edges'),
                        'homeostasis_pruned_status':payload.get('homeostasis_pruned'),
                        'homeostasis_bridged_status':payload.get('homeostasis_bridged'),
                        'b1_z_status':payload.get('b1_z'),
                        'adc_territories':payload.get('adc_territories'),
                        'adc_boundaries':payload.get('adc_boundaries'),
                        'sie_total_reward_status':payload.get('sie_total_reward'),
                        'sie_valence_01_status':payload.get('sie_valence_01'),
                        'sie_v2_reward_mean_status':payload.get('sie_v2_reward_mean'),
                        'sie_v2_valence_01_status':payload.get('sie_v2_valence_01'),
                        'ute_in_count':payload.get('ute_in_count'),
                        'ute_text_count':payload.get('ute_text_count'),
                    })
                elif ptype=='text':
                    msg=payload.get('msg','')
                    d=text_stats.setdefault(cur_t, {'text_events':0,'text_words':0,'text_chars':0})
                    d['text_events'] += 1
                    d['text_words'] += len(WORD_RE.findall(msg))
                    d['text_chars'] += len(msg)
            elif typ=='macro' and rec.get('macro')=='say':
                args=rec.get('args',{}) or {}
                why=args.get('why',{}) or {}
                txt=args.get('text','')
                t=int(why.get('t',cur_t))
                say_rows.append({'t':t,'say_count':1,'say_words':len(WORD_RE.findall(txt)),'say_chars':len(txt)})

status_df=pd.DataFrame(status_rows).drop_duplicates(subset=['t']).sort_values('t')
text_df=pd.DataFrame([{'t':t,**v} for t,v in text_stats.items()]).sort_values('t')
say_df=pd.DataFrame(say_rows)
if not say_df.empty:
    say_df=say_df.groupby('t',as_index=False).sum()
else:
    say_df=pd.DataFrame(columns=['t','say_count','say_words','say_chars'])

# Parse raw events with only needed fields
need = ['t','ts','connectome_entropy','complexity_cycles','firing_var','sie_total_reward','sie_v2_valence_01','sie_valence_01','sie_novelty','sie_td_error','vt_unique','vt_visits','vt_coverage','vt_entropy','active_edges','active_synapses','cohesion_components','homeostasis_pruned','homeostasis_bridged','omega_mean','a_mean','b1_z','b1_spike','phase']
raw_rows=[]
for p in sorted(EVENTS_PARTS.glob('*.txt'))+[AURA/'events.jsonl']:
    with p.open('r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            if not line.startswith('{'): continue
            rec=json.loads(line)
            if rec.get('msg')!='tick' or 't' not in rec: continue
            raw_rows.append({k:rec.get(k) for k in need})
raw_df=pd.DataFrame(raw_rows).drop_duplicates(subset=['t']).sort_values('t')

# Merge
core=raw_df.merge(text_df,on='t',how='left').merge(say_df,on='t',how='left').merge(status_df[['t','ute_in_count','ute_text_count']],on='t',how='left')
for c in ['text_events','text_words','text_chars','say_count','say_words','say_chars','ute_in_count','ute_text_count']:
    if c in core.columns:
        core[c]=core[c].fillna(0)
core.rename(columns={'connectome_entropy':'entropy','complexity_cycles':'complexity','vt_coverage':'coverage'}, inplace=True)
core['firing_var_log']=np.log1p(np.clip(core['firing_var'].astype(float),0,None))
core['reward_mean']=core['sie_total_reward']
core['valence_01']=core['sie_v2_valence_01']
core['valence_legacy_01']=core['sie_valence_01']
core['novelty']=core['sie_novelty']
core['td_error']=core['sie_td_error']
core['void_unique']=core['vt_unique']
core['void_unique_log']=np.log1p(np.clip(core['vt_unique'].astype(float),0,None))
core['void_visits']=core['vt_visits']
core['has_text']=(core['text_words']>0).astype(int)
core['log_text_words']=np.log1p(core['text_words'])
core['has_say']=(core['say_count']>0).astype(int)
core['dt_wall']=core['ts'].diff()
for col in ['entropy','complexity','firing_var_log','reward_mean','valence_01','novelty','td_error','void_unique_log','coverage','active_edges','omega_mean','a_mean','b1_z']:
    core[f'd_{col}']=core[col].diff().fillna(0)
# epochs from entropy longest high segment
x=core[['entropy']].values
if len(core)>=10:
    gmm=GaussianMixture(n_components=2,random_state=0).fit(x)
    hi=np.argmax(gmm.means_.ravel())
    is_high=(gmm.predict(x)==hi).astype(int)
    best=(0,-1,-1); start=None
    for i,v in enumerate(is_high):
        if v==1 and start is None: start=i
        if (v==0 or i==len(is_high)-1) and start is not None:
            end=i-1 if v==0 else i
            L=end-start+1
            if L>best[0]: best=(L,start,end)
            start=None
    _,s,e=best
else:
    s=e=-1
epoch=np.array(['E1_low_entropy_baseline_1']*len(core),dtype=object)
if s>=0:
    epoch[s:e+1]='E2_high_entropy_plateau'
    if e+1<len(core): epoch[e+1:]='E3_low_entropy_baseline_2'
core['epoch']=epoch
# keep ordered cols
ordered=['t','ts','epoch','phase','entropy','complexity','firing_var','firing_var_log','reward_mean','valence_01','valence_legacy_01','novelty','td_error','void_unique','void_unique_log','void_visits','coverage','vt_entropy','active_edges','active_synapses','cohesion_components','homeostasis_pruned','homeostasis_bridged','omega_mean','a_mean','b1_z','b1_spike','text_events','text_words','log_text_words','has_text','say_count','say_words','has_say','ute_in_count','ute_text_count','dt_wall'] + [c for c in core.columns if c.startswith('d_')]
core=core[ordered]
core.to_csv(OUT/'timeseries_core_renamed_Aura.csv', index=False)
# pca state
features=['entropy','complexity','firing_var_log','reward_mean','valence_01','novelty','td_error','void_unique_log','log_text_words','active_edges','coverage','b1_z']
X=core[features].replace([np.inf,-np.inf],np.nan).ffill().bfill().fillna(0)
Xs=StandardScaler().fit_transform(X)
pca=PCA(n_components=3,random_state=0)
PC=pca.fit_transform(Xs)
pca_df=pd.DataFrame({'t':core['t'],'epoch':core['epoch'],'PC1':PC[:,0],'PC2':PC[:,1],'PC3':PC[:,2]})
pca_df['pca_speed']=np.sqrt(np.sum(np.diff(PC,axis=0,prepend=PC[[0],:])**2,axis=1))
for c in ['PC1','PC2','PC3']:
    pca_df[f'{c}_sign']=(pca_df[c]>=0).astype(int)
pca_df['macro_state']=pca_df['PC1_sign']*4+pca_df['PC2_sign']*2+pca_df['PC3_sign']
pca_df.to_csv(OUT/'pca_state_space_Aura.csv', index=False)
meta={'tick_start':int(core['t'].min()),'tick_end':int(core['t'].max()),'n_ticks':int(len(core)),'epoch_counts':core['epoch'].value_counts().to_dict(),'epoch_high_start_tick':int(core.loc[core['epoch']=='E2_high_entropy_plateau','t'].min()) if (core['epoch']=='E2_high_entropy_plateau').any() else None,'epoch_high_end_tick':int(core.loc[core['epoch']=='E2_high_entropy_plateau','t'].max()) if (core['epoch']=='E2_high_entropy_plateau').any() else None,'pca_explained_variance_ratio':pca.explained_variance_ratio_.tolist(),'features':features}
(OUT/'aura_suite_metadata.json').write_text(json.dumps(meta, indent=2))
print(json.dumps(meta,indent=2))
