from __future__ import annotations
import json, gzip, re
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

ROOT = Path('/mnt/data')
AURA = ROOT / '_aura_pkg'
EVENTS_PARTS = ROOT / '_events_parts'
OUT = ROOT / 'aura_suite_v1'
INTER = OUT / 'intermediate'
INTER.mkdir(parents=True, exist_ok=True)
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


def iter_json_lines(path: Path):
    open_fn = gzip.open if path.suffix == '.gz' else open
    with open_fn(path, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line=line.strip()
            if not line or not line.startswith('{'):
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def parse_raw_event_file(path: Path) -> pd.DataFrame:
    rows=[]
    for rec in iter_json_lines(path):
        if rec.get('msg')!='tick' or 'ts' not in rec:
            continue
        row=dict(rec)
        row['source_file']=path.name
        rows.append(row)
    if not rows:
        return pd.DataFrame()
    df=pd.DataFrame(rows)
    # create tick if absent by sequence within file; but Aura files have t mostly only later? infer continuous sequence if missing
    if 't' not in df.columns or df['t'].isna().all():
        df['t']=np.arange(len(df))
    return df


def save_both(df: pd.DataFrame, base: Path):
    df.to_csv(base, index=False)
    with gzip.open(str(base)+'.gz','wt',encoding='utf-8') as gz:
        df.to_csv(gz,index=False)


def build_utd_tables():
    status_rows=[]
    text_rows=[]
    say_rows=[]
    cur_t=None
    shards=sorted((AURA/'utd_events').glob('*.txt'))
    for p in shards:
        for rec in iter_json_lines(p):
            typ=rec.get('type')
            if typ=='text':
                payload=rec.get('payload',{}) or {}
                ptype=payload.get('type')
                if ptype=='status' and 't' in payload:
                    cur_t=int(payload.get('t'))
                    status_rows.append({
                        't':cur_t,
                        'phase':payload.get('phase'),
                        'cohesion_components':payload.get('cohesion_components'),
                        'vt_coverage':payload.get('vt_coverage'),
                        'vt_entropy':payload.get('vt_entropy'),
                        'connectome_entropy':payload.get('connectome_entropy'),
                        'active_edges':payload.get('active_edges'),
                        'homeostasis_pruned':payload.get('homeostasis_pruned'),
                        'homeostasis_bridged':payload.get('homeostasis_bridged'),
                        'b1_z':payload.get('b1_z'),
                        'adc_territories':payload.get('adc_territories'),
                        'adc_boundaries':payload.get('adc_boundaries'),
                        'sie_total_reward':payload.get('sie_total_reward'),
                        'sie_valence_01':payload.get('sie_valence_01'),
                        'sie_v2_reward_mean':payload.get('sie_v2_reward_mean'),
                        'sie_v2_valence_01':payload.get('sie_v2_valence_01'),
                        'ute_in_count':payload.get('ute_in_count'),
                        'ute_text_count':payload.get('ute_text_count'),
                        'source_file':p.name,
                    })
                elif ptype=='text':
                    msg=payload.get('msg','') or ''
                    text_rows.append({
                        't':cur_t,
                        'msg':msg,
                        'text_words':len(WORD_RE.findall(msg)),
                        'text_chars':len(msg),
                        'source_file':p.name,
                    })
            elif typ=='macro' and rec.get('macro')=='say':
                args=rec.get('args',{}) or {}
                why=args.get('why',{}) or {}
                txt=args.get('text','') or ''
                t = why.get('t', cur_t)
                say_rows.append({
                    't':t,
                    'text':txt,
                    'say_words':len(WORD_RE.findall(txt)),
                    'say_chars':len(txt),
                    'phase':why.get('phase'),
                    'cohesion_components':why.get('cohesion_components'),
                    'vt_coverage':why.get('vt_coverage'),
                    'vt_entropy':why.get('vt_entropy'),
                    'connectome_entropy':why.get('connectome_entropy'),
                    'b1_z':why.get('b1_z'),
                    'sie_valence_01':why.get('sie_valence_01'),
                    'sie_v2_valence_01':why.get('sie_v2_valence_01'),
                    'novelty_idf':why.get('novelty_idf'),
                    'composer_idf_k':why.get('composer_idf_k'),
                    'source_file':p.name,
                })
    status_df=pd.DataFrame(status_rows)
    if not status_df.empty:
        status_df=status_df.sort_values(['t','source_file']).drop_duplicates(subset=['t'], keep='last')
    text_df=pd.DataFrame(text_rows)
    say_df=pd.DataFrame(say_rows)
    if not text_df.empty:
        text_by_tick=text_df.groupby('t',dropna=False,as_index=False).agg(
            text_events=('msg','count'),
            text_words=('text_words','sum'),
            text_chars=('text_chars','sum')
        )
    else:
        text_by_tick=pd.DataFrame(columns=['t','text_events','text_words','text_chars'])
    if not say_df.empty:
        say_by_tick=say_df.groupby('t',dropna=False,as_index=False).agg(
            say_count=('text','count'),
            say_words=('say_words','sum'),
            say_chars=('say_chars','sum')
        )
    else:
        say_by_tick=pd.DataFrame(columns=['t','say_count','say_words','say_chars'])

    status_df.to_csv(INTER/'utd_status_full.csv', index=False)
    text_by_tick.to_csv(INTER/'utd_text_by_tick.csv', index=False)
    say_by_tick.to_csv(INTER/'utd_say_by_tick.csv', index=False)
    return status_df, text_by_tick, say_by_tick


def build_raw_event_tables():
    dfs=[]
    for p in sorted(EVENTS_PARTS.glob('*.txt')):
        df=parse_raw_event_file(p)
        if not df.empty:
            dfs.append(df)
            # save per-file parsed
            save_both(df, INTER/f'{p.stem}_parsed.csv')
    # aura events.jsonl late segment
    late=parse_raw_event_file(AURA/'events.jsonl')
    if not late.empty:
        dfs.append(late)
    merged=pd.concat(dfs, ignore_index=True, sort=False) if dfs else pd.DataFrame()
    if merged.empty:
        raise RuntimeError('No raw tick events parsed')
    # sort and dedupe
    merged=merged.sort_values(['ts']).reset_index(drop=True)
    # try preserve t if present; create seq too
    merged['row_idx']=np.arange(len(merged))
    merged.to_csv(INTER/'raw_events_merged.csv', index=False)
    # richer parsed with normalized columns
    parsed=merged.copy()
    parsed['has_b1_spike']=parsed.get('b1_spike',0).fillna(0).astype(int) if 'b1_spike' in parsed.columns else 0
    parsed['log_active_edges']=np.log1p(pd.to_numeric(parsed.get('active_edges',0), errors='coerce').fillna(0))
    parsed['log_text_words']=0.0
    parsed.to_csv(INTER/'events_parsed.csv', index=False)
    # slims
    slim_cols=[c for c in ['t','ts','phase','connectome_entropy','complexity_cycles','firing_var','sie_total_reward','sie_valence_01','sie_v2_valence_01','sie_novelty','sie_td_error','vt_unique','vt_visits','vt_coverage','vt_entropy','active_edges','active_synapses','cohesion_components','homeostasis_pruned','homeostasis_bridged','omega_mean','a_mean','b1_z','b1_spike','source_file'] if c in parsed.columns]
    parsed[slim_cols].to_csv(INTER/'events_parsed_slim.csv', index=False)
    slim2_cols=[c for c in ['t','ts','connectome_entropy','complexity_cycles','firing_var','active_edges','omega_mean','a_mean','b1_z','phase'] if c in parsed.columns]
    parsed[slim2_cols].to_csv(INTER/'events_slim2.csv', index=False)
    return merged, parsed


def build_core_and_pca(status_df, text_by_tick, say_by_tick, merged):
    core=merged.copy()
    # merge text/say/status by t where available; fallback nearest by ts not implemented
    if 't' not in core.columns:
        core['t']=np.arange(len(core))
    core=core.merge(text_by_tick,on='t',how='left').merge(say_by_tick,on='t',how='left')
    status_merge_cols=['t','ute_in_count','ute_text_count']
    if not status_df.empty:
        avail=[c for c in status_merge_cols if c in status_df.columns]
        core=core.merge(status_df[avail], on='t', how='left')
    for c in ['text_events','text_words','text_chars','say_count','say_words','say_chars','ute_in_count','ute_text_count']:
        if c in core.columns:
            core[c]=core[c].fillna(0)
    rename={
        'connectome_entropy':'entropy',
        'complexity_cycles':'complexity',
        'vt_coverage':'coverage',
        'sie_total_reward':'reward_mean',
        'sie_v2_valence_01':'valence_01',
        'sie_valence_01':'valence_legacy_01',
        'sie_novelty':'novelty',
        'sie_td_error':'td_error',
        'vt_unique':'void_unique',
        'vt_visits':'void_visits',
    }
    core=core.rename(columns={k:v for k,v in rename.items() if k in core.columns})
    if 'firing_var' in core.columns:
        core['firing_var_log']=np.log1p(np.clip(pd.to_numeric(core['firing_var'], errors='coerce').fillna(0),0,None))
    core['log_text_words']=np.log1p(pd.to_numeric(core.get('text_words',0), errors='coerce').fillna(0))
    core['has_text']=(pd.to_numeric(core.get('text_words',0), errors='coerce').fillna(0)>0).astype(int)
    core['has_say']=(pd.to_numeric(core.get('say_count',0), errors='coerce').fillna(0)>0).astype(int)
    core['void_unique_log']=np.log1p(pd.to_numeric(core.get('void_unique',0), errors='coerce').fillna(0))
    core['dt_wall']=pd.to_numeric(core['ts'], errors='coerce').diff()
    for col in ['entropy','complexity','firing_var_log','reward_mean','valence_01','novelty','td_error','void_unique_log','coverage','active_edges','omega_mean','a_mean','b1_z']:
        if col in core.columns:
            core[f'd_{col}']=pd.to_numeric(core[col], errors='coerce').diff().fillna(0)
    # epochs using entropy GMM if present
    if 'entropy' in core.columns and len(core)>=10:
        x=pd.to_numeric(core['entropy'], errors='coerce').fillna(method='ffill').fillna(method='bfill').to_numpy().reshape(-1,1)
        gmm=GaussianMixture(n_components=2, random_state=0).fit(x)
        hi=np.argmax(gmm.means_.ravel())
        is_high=(gmm.predict(x)==hi).astype(int)
        best=(0,-1,-1); start=None
        for i,v in enumerate(is_high):
            if v==1 and start is None:
                start=i
            if (v==0 or i==len(is_high)-1) and start is not None:
                end=i-1 if v==0 else i
                L=end-start+1
                if L>best[0]: best=(L,start,end)
                start=None
        _,s,e=best
        epoch=np.array(['E1_low_entropy_baseline_1']*len(core),dtype=object)
        if s>=0:
            epoch[s:e+1]='E2_high_entropy_plateau'
            if e+1<len(core):
                epoch[e+1:]='E3_low_entropy_baseline_2'
        core['epoch']=epoch
    else:
        core['epoch']='E1_low_entropy_baseline_1'

    core.to_csv(OUT/'timeseries_core_renamed_Aura.csv', index=False)
    # pca state
    features=[c for c in ['entropy','complexity','firing_var_log','reward_mean','valence_01','novelty','td_error','void_unique_log','log_text_words','active_edges','coverage','b1_z'] if c in core.columns]
    X=core[features].replace([np.inf,-np.inf],np.nan).ffill().bfill().fillna(0)
    Xs=StandardScaler().fit_transform(X)
    pca=PCA(n_components=min(3, Xs.shape[1]), random_state=0)
    PC=pca.fit_transform(Xs)
    pca_df=pd.DataFrame({'t':core['t'],'epoch':core['epoch']})
    for i,name in enumerate(['PC1','PC2','PC3'][:PC.shape[1]]):
        pca_df[name]=PC[:,i]
        pca_df[f'{name}_sign']=(pca_df[name]>=0).astype(int)
    while 'PC3' not in pca_df.columns:
        missing='PC'+str(len([c for c in pca_df.columns if c.startswith('PC') and len(c)==3])+1)
        if missing in ['PC1','PC2','PC3']:
            pca_df[missing]=0.0
            pca_df[f'{missing}_sign']=0
    arr=pca_df[['PC1','PC2','PC3']].to_numpy()
    pca_df['pca_speed']=np.sqrt(np.sum(np.diff(arr, axis=0, prepend=arr[[0],:])**2, axis=1))
    pca_df['macro_state']=pca_df['PC1_sign']*4+pca_df['PC2_sign']*2+pca_df['PC3_sign']
    pca_df.to_csv(OUT/'pca_state_space_Aura.csv', index=False)
    return core, pca_df


def main():
    status_df, text_by_tick, say_by_tick = build_utd_tables()
    merged, parsed = build_raw_event_tables()
    build_core_and_pca(status_df, text_by_tick, say_by_tick, merged)
    print('Rebuilt intermediate and derived Aura inputs')

if __name__=='__main__':
    main()
