#!/usr/bin/env python3
"""
Scalar + sparse-structure analysis for VDM log slices.

Inputs:
  - events.jsonl         (tick telemetry; includes evt_trail_dict / evt_memory_dict)
  - utd_events.jsonl     (macro events; includes macro:say with tick in args.why.t)

Outputs:
  - tables/*.csv
  - figures/*.png

This is intentionally "offline-only": it does NOT require runtime changes.
"""
import argparse, json, os, math, hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score


def gini_coefficient(x):
    x = np.array(x, dtype=float)
    x = x[~np.isnan(x)]
    if x.size == 0:
        return np.nan
    if np.all(x == 0):
        return 0.0
    x = np.sort(x)
    n = x.size
    cumx = np.cumsum(x)
    g = (n + 1 - 2*np.sum(cumx)/cumx[-1]) / n
    return float(g)


def shannon_entropy_from_values(vals):
    vals = np.array(vals, dtype=float)
    vals = vals[vals > 0]
    if vals.size == 0:
        return 0.0
    p = vals / vals.sum()
    return float(-np.sum(p * np.log(p + 1e-12)))


def participation_ratio_from_values(vals):
    vals = np.array(vals, dtype=float)
    vals = vals[vals > 0]
    if vals.size == 0:
        return 0.0
    p = vals / vals.sum()
    return float(1.0 / np.sum(p*p))


def powerlaw_alpha_mle_continuous(vals, xmin):
    vals = np.array(vals, dtype=float)
    vals = vals[vals >= xmin]
    n = vals.size
    if n < 2 or xmin <= 0:
        return np.nan, int(n)
    alpha = 1.0 + n / np.sum(np.log(vals/xmin))
    return float(alpha), int(n)


def dict_stats(d, topk_jaccard=100, tail_quantile=0.90):
    if not d:
        return {
            'mass':0.0,'gini':np.nan,'entropy':0.0,'pr':0.0,
            'top1_frac':np.nan,'top10_frac':np.nan,'top100_frac':np.nan,
            'tail_xmin':np.nan,'tail_alpha':np.nan,'tail_n':0,
            'topk_set':set(), 'norm':0.0
        }
    vals = np.array(list(d.values()), dtype=float)
    mass = float(vals.sum())
    gini = gini_coefficient(vals)
    ent = shannon_entropy_from_values(vals)
    pr = participation_ratio_from_values(vals)

    sorted_vals = np.sort(vals)[::-1]
    top1_frac = float(sorted_vals[0]/mass) if mass>0 else np.nan
    top10_frac = float(sorted_vals[:min(10, len(sorted_vals))].sum()/mass) if mass>0 else np.nan
    top100_frac = float(sorted_vals[:min(100, len(sorted_vals))].sum()/mass) if mass>0 else np.nan

    xmin = float(np.quantile(vals, tail_quantile))
    alpha, n_tail = powerlaw_alpha_mle_continuous(vals, xmin)

    k = min(topk_jaccard, len(d))
    if k == len(d):
        top_items = sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:k]
        topk_set = set(int(k) for k,_ in top_items)
    else:
        keys = np.fromiter((int(k) for k in d.keys()), dtype=np.int64, count=len(d))
        vals2 = np.fromiter(d.values(), dtype=float, count=len(d))
        idx = np.argpartition(vals2, -k)[-k:]
        topk_set = set(int(keys[i]) for i in idx)

    norm = float(np.linalg.norm(vals))
    return {
        'mass':mass,'gini':gini,'entropy':ent,'pr':pr,
        'top1_frac':top1_frac,'top10_frac':top10_frac,'top100_frac':top100_frac,
        'tail_xmin':xmin,'tail_alpha':alpha,'tail_n':n_tail,
        'topk_set':topk_set, 'norm':norm
    }


def cosine_similarity_dict(d1, d2, norm1=None, norm2=None):
    if d1 is None or d2 is None or len(d1)==0 or len(d2)==0:
        return np.nan
    if norm1 is None:
        norm1 = math.sqrt(sum(v*v for v in d1.values()))
    if norm2 is None:
        norm2 = math.sqrt(sum(v*v for v in d2.values()))
    if norm1==0 or norm2==0:
        return np.nan
    dot = 0.0
    if len(d1) < len(d2):
        for k,v in d1.items():
            v2 = d2.get(k)
            if v2 is not None:
                dot += v*v2
    else:
        for k,v in d2.items():
            v1 = d1.get(k)
            if v1 is not None:
                dot += v*v1
    return float(dot/(norm1*norm2))


def parse_utd_say(path):
    recs=[]
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            obj=json.loads(line)
            if obj.get('type')=='macro' and obj.get('macro')=='say':
                args=obj.get('args',{})
                why=args.get('why',{})
                t=why.get('t')
                text=args.get('text','')
                rec={'t':t,'say_len':len(text)}
                recs.append(rec)
    if not recs:
        return pd.DataFrame(columns=['t','say_len'])
    return pd.DataFrame(recs)


def build_input_episodes(has_input, gap_close=2, min_len=3):
    has_input = np.asarray(has_input, dtype=bool)
    n = len(has_input)
    closed = has_input.copy()
    i=0
    while i<n:
        if not closed[i]:
            j=i
            while j<n and not closed[j]:
                j+=1
            gap_len = j-i
            left = i-1>=0 and closed[i-1]
            right = j<n and closed[j]
            if left and right and gap_len<=gap_close:
                closed[i:j]=True
            i=j
        else:
            i+=1

    episode_id = np.zeros(n, dtype=int)
    eid=0
    segments=[]
    i=0
    while i<n:
        if closed[i]:
            eid+=1
            j=i
            while j<n and closed[j]:
                j+=1
            segments.append((eid,i,j))
            episode_id[i:j]=eid
            i=j
        else:
            i+=1

    if min_len>1:
        for eid,i,j in segments:
            if (j-i)<min_len:
                episode_id[i:j]=0

    unique = sorted([e for e in np.unique(episode_id) if e!=0])
    mapping={old:new for new,old in enumerate(unique, start=1)}
    for old,new in mapping.items():
        episode_id[episode_id==old]=new
    return closed.astype(int), episode_id


def event_triggered_average(series, event_idx, window=20):
    n=len(series)
    offsets=np.arange(-window, window+1)
    mats=[]
    for idx in event_idx:
        if idx-window<0 or idx+window>=n:
            continue
        mats.append(series[idx-window:idx+window+1])
    if len(mats)==0:
        return offsets, np.full(len(offsets), np.nan), 0
    mat=np.vstack(mats)
    return offsets, mat.mean(axis=0), mat.shape[0]


def fit_micro_macro_states_fast(df, feature_cols, n_micro=25, n_macro_max=6, n_pc=10, n_pc_use=6, kmeans_iter=30, random_state=0):
    X = df[feature_cols].values.astype(np.float32)
    if np.isnan(X).any():
        col_med = np.nanmedian(X, axis=0)
        inds = np.where(np.isnan(X))
        X[inds] = np.take(col_med, inds[1])
    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0)
    Xz = (X - X_mean) / (X_std + 1e-6)

    U,S,Vt = np.linalg.svd(Xz, full_matrices=False)
    n_pc = min(n_pc, U.shape[1])
    PCs = U[:,:n_pc] * S[:n_pc]
    n_pc_use = min(n_pc_use, n_pc)

    centroids, micro = kmeans2(PCs[:,:n_pc_use], n_micro, minit='points', iter=kmeans_iter)
    micro = micro.astype(int)

    n = n_micro
    counts = np.zeros((n,n), dtype=np.float64)
    for i in range(len(micro)-1):
        counts[micro[i], micro[i+1]] += 1.0
    counts += 1e-6
    P = counts / counts.sum(axis=1, keepdims=True)

    vals, vecs = np.linalg.eig(P.T)
    vals = np.real(vals); vecs=np.real(vecs)
    order = np.argsort(-vals)
    vals=vals[order]; vecs=vecs[:,order]
    k = min(n_macro_max, len(vals))
    vals_k = vals[:k]; vecs_k=vecs[:,:k]

    gaps = vals_k[:-1] - vals_k[1:]
    m_guess = int(np.argmax(gaps[:min(5,len(gaps))]) + 1) if len(gaps)>0 else 2
    m_guess = max(2, min(m_guess, n_macro_max))

    feats = vecs_k[:,1:m_guess]
    if feats.shape[1]==0:
        macro_micro = np.zeros(n, dtype=int)
    else:
        _, macro_micro = kmeans2(feats, m_guess, minit='points', iter=50)
        macro_micro = macro_micro.astype(int)

    macro_tick = np.array([macro_micro[m] for m in micro], dtype=int)
    return micro, macro_micro, macro_tick, P, vals_k


def delta_r2_x_to_y(df, idx_pairs, x_col, y_col, ridge_alpha=1e-3):
    idx_pairs = np.array(idx_pairs, dtype=int)
    y_target = df[y_col].values[idx_pairs+1]

    X_base = df[[y_col]].values[idx_pairs]  # y_t
    X_ext = np.column_stack([X_base, df[[x_col]].values[idx_pairs]])  # y_t, x_t

    n=len(idx_pairs)
    if n < 50:
        model_base=Ridge(alpha=ridge_alpha).fit(X_base, y_target)
        model_ext=Ridge(alpha=ridge_alpha).fit(X_ext, y_target)
        r2_base=r2_score(y_target, model_base.predict(X_base))
        r2_ext=r2_score(y_target, model_ext.predict(X_ext))
        return float(r2_ext-r2_base), float(r2_base), float(r2_ext), int(n), True

    split=int(n*0.7)
    Xb_tr,Xb_te=X_base[:split],X_base[split:]
    Xe_tr,Xe_te=X_ext[:split],X_ext[split:]
    y_tr,y_te=y_target[:split],y_target[split:]

    model_base=Ridge(alpha=ridge_alpha).fit(Xb_tr,y_tr)
    model_ext=Ridge(alpha=ridge_alpha).fit(Xe_tr,y_tr)
    r2_base=r2_score(y_te, model_base.predict(Xb_te))
    r2_ext=r2_score(y_te, model_ext.predict(Xe_te))
    return float(r2_ext-r2_base), float(r2_base), float(r2_ext), int(n), False


def lead_time_last_true_before(say_idx, hot_mask, window=50):
    lead=[]
    for idx in say_idx:
        start=max(0, idx-window)
        segment = hot_mask[start:idx]  # exclude idx
        true_idx = np.where(segment)[0]
        if true_idx.size==0:
            lead.append(np.nan)
        else:
            last = start + true_idx[-1]
            lead.append(idx-last)
    return np.array(lead, dtype=float)


def save_line_plot(x, y, path, title, xlabel='t', ylabel='', vlines=None, scatter_points=None):
    plt.figure(figsize=(10,4))
    plt.plot(x, y, linewidth=1.0)
    if vlines is not None and len(vlines)>0:
        for xv in vlines:
            plt.axvline(x=xv, linewidth=0.5, alpha=0.3)
    if scatter_points is not None:
        xs, ys = scatter_points
        plt.scatter(xs, ys, s=20)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def save_eta_plot(offsets, mean, path, title, ylabel):
    plt.figure(figsize=(6,4))
    plt.plot(offsets, mean, linewidth=1.5)
    plt.axvline(0, linewidth=0.8)
    plt.title(title)
    plt.xlabel("offset (ticks)")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(1<<20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--events", required=True, help="events.jsonl")
    ap.add_argument("--utd", required=True, help="utd_events.jsonl")
    ap.add_argument("--out", required=True, help="output directory")
    args=ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    tables=os.path.join(args.out,"tables"); figs=os.path.join(args.out,"figures")
    os.makedirs(tables, exist_ok=True); os.makedirs(figs, exist_ok=True)

    rows=[]
    prev_trail=None; prev_mem=None
    prev_trail_top=set(); prev_mem_top=set()
    prev_trail_norm=None; prev_mem_norm=None

    with open(args.events,'r',encoding='utf-8') as f:
        for line in f:
            obj=json.loads(line)
            if obj.get('msg')!='tick':
                continue
            trail=obj.get('evt_trail_dict',{})
            mem=obj.get('evt_memory_dict',{})
            trail_stats=dict_stats(trail, topk_jaccard=100, tail_quantile=0.90)
            mem_stats=dict_stats(mem, topk_jaccard=100, tail_quantile=0.90)

            if prev_trail is None:
                trail_cos=np.nan; trail_jac=np.nan
            else:
                trail_cos=cosine_similarity_dict(trail, prev_trail, norm1=trail_stats['norm'], norm2=prev_trail_norm)
                inter=len(trail_stats['topk_set'] & prev_trail_top); union=len(trail_stats['topk_set'] | prev_trail_top)
                trail_jac=inter/union if union>0 else np.nan

            if prev_mem is None:
                mem_cos=np.nan; mem_jac=np.nan
            else:
                mem_cos=cosine_similarity_dict(mem, prev_mem, norm1=mem_stats['norm'], norm2=prev_mem_norm)
                inter=len(mem_stats['topk_set'] & prev_mem_top); union=len(mem_stats['topk_set'] | prev_mem_top)
                mem_jac=inter/union if union>0 else np.nan

            scalar={k:v for k,v in obj.items() if not isinstance(v,(dict,list))}
            for prefix,stats_ in [('trail',trail_stats),('memory',mem_stats)]:
                for key,val in stats_.items():
                    if key in ('topk_set','norm'):
                        continue
                    scalar[f'{prefix}_{key}']=val
            scalar['trail_cos_prev']=trail_cos
            scalar['trail_jaccard_topk_prev']=trail_jac
            scalar['memory_cos_prev']=mem_cos
            scalar['memory_jaccard_topk_prev']=mem_jac
            rows.append(scalar)

            prev_trail=trail; prev_mem=mem
            prev_trail_top=trail_stats['topk_set']; prev_mem_top=mem_stats['topk_set']
            prev_trail_norm=trail_stats['norm']; prev_mem_norm=mem_stats['norm']

    df=pd.DataFrame(rows)

    # Merge say events
    say_df=parse_utd_say(args.utd)
    if len(say_df):
        say_agg=say_df.groupby('t').agg(
            say_count=('say_len','size'),
            say_len_sum=('say_len','sum'),
            say_len_mean=('say_len','mean')
        ).reset_index()
        df=df.merge(say_agg, on='t', how='left')
    else:
        df['say_count']=0; df['say_len_sum']=0; df['say_len_mean']=0.0
    df['say_count']=df['say_count'].fillna(0).astype(int)
    df['say_len_sum']=df['say_len_sum'].fillna(0).astype(int)
    df['say_len_mean']=df['say_len_mean'].fillna(0.0)
    df['did_say']=(df['say_count']>0).astype(int)

    # Input episodes (use ute_text_count>0 as input present)
    df['has_input_raw']=(df['ute_text_count']>0).astype(int)
    closed, ep_id = build_input_episodes(df['has_input_raw'].values, gap_close=2, min_len=3)
    df['has_input']=closed
    df['input_episode_id']=ep_id

    # Macrostate refit using internal-only scalar channels (exclude UTD/UTE + exclude our struct summaries)
    base_features = [
        'avg_weight','active_synapses','active_edges','cohesion_components','complexity_cycles','connectome_entropy','firing_var',
        'vt_visits','vt_unique','vt_coverage','vt_entropy','vt_hops','vt_walkers','td_signal','novelty_idf_scale','omega_mean','a_mean',
        'homeostasis_pruned','homeostasis_bridged',
        'adc_territories','adc_boundaries','adc_cycle_hits',
        'b1_value','b1_delta','b1_z','b1_spike',
        'sie_total_reward','sie_valence_01','sie_td_error','sie_novelty','sie_habituation_mean','sie_self_benefit','sie_hsi_norm','sie_density',
        'sie_novelty_scale','sie_v2_reward_mean','sie_v2_valence_01','sie_gate',
        'phase'
    ]
    head_features = [
        'evt_cold_p95','evt_cold_p99','evt_cold_max',
        'evt_heat_p95','evt_heat_p99','evt_heat_max','evt_heat_count',
        'evt_exc_p95','evt_exc_p99','evt_exc_max','evt_exc_count',
        'evt_inh_p95','evt_inh_p99','evt_inh_max','evt_inh_count',
        'evt_memory_p95','evt_memory_p99','evt_memory_max','evt_memory_count',
        'evt_trail_p95','evt_trail_p99','evt_trail_max','evt_trail_count'
    ]
    macro_features=[c for c in base_features+head_features if c in df.columns]
    micro, macro_micro, macro_tick, P, eigvals = fit_micro_macro_states_fast(df, macro_features, n_micro=25, n_macro_max=6)
    df['micro_refit']=micro
    df['macro_refit']=macro_tick

    # Save core tables
    df.to_csv(os.path.join(tables,"tick_table_full.csv.gz"), index=False, compression="gzip")
    pd.DataFrame({'micro':np.arange(len(macro_micro)),'macro':macro_micro}).to_csv(os.path.join(tables,"micro_to_macro_map.csv"), index=False)
    pd.DataFrame(P).to_csv(os.path.join(tables,"micro_transition_matrix_P.csv"), index=False)
    pd.DataFrame({'eigval':eigvals}).to_csv(os.path.join(tables,"micro_transition_eigvals.csv"), index=False)

    # Mutual information sanity check
    mi_in = mutual_info_score(df['macro_refit'], df['has_input'])
    mi_say = mutual_info_score(df['macro_refit'], df['did_say'])
    nmi_in = normalized_mutual_info_score(df['macro_refit'], df['has_input'])
    nmi_say = normalized_mutual_info_score(df['macro_refit'], df['did_say'])
    pd.DataFrame([{
        'mi_macro_has_input':mi_in,
        'mi_macro_did_say':mi_say,
        'nmi_macro_has_input':nmi_in,
        'nmi_macro_did_say':nmi_say
    }]).to_csv(os.path.join(tables,"macrostate_mutual_info.csv"), index=False)

    # Directed influence (delta R2) within each macrostate
    drive_rows=[]
    for m in sorted(df['macro_refit'].unique()):
        macro = df['macro_refit'].values
        idx_pairs = np.where((macro[:-1]==m) & (macro[1:]==m))[0]
        for x_col in ['connectome_entropy','vt_entropy','sie_v2_valence_01','sie_total_reward','sie_td_error']:
            for y_col in ['vt_coverage','vt_entropy','active_edges','b1_z']:
                dr2,r2b,r2e,n,insamp = delta_r2_x_to_y(df, idx_pairs, x_col, y_col)
                drive_rows.append({'macro':m,'x':x_col,'y':y_col,'delta_r2':dr2,'r2_base':r2b,'r2_ext':r2e,'n_pairs':n,'in_sample':insamp})
    pd.DataFrame(drive_rows).to_csv(os.path.join(tables,"macrostate_directed_influence_deltaR2.csv"), index=False)

    # Lead-time distribution for a simple comm detector
    say_idx = df.index[df['did_say']==1].to_numpy()
    thresholds=[0.3,0.5,0.7,0.9,1.1]
    lead_records=[]
    for thr in thresholds:
        hot=(df['macro_refit']==0) & (df['has_input']==1) & (df['b1_z']>thr)
        lead=lead_time_last_true_before(say_idx, hot.values, window=50)
        for event_i, idx in enumerate(say_idx):
            lead_records.append({'thr':thr,'say_event_idx':event_i,'t':int(df.loc[idx,'t']), 'lead_ticks':float(lead[event_i])})
    pd.DataFrame(lead_records).to_csv(os.path.join(tables,"comm_detector_lead_times_by_threshold.csv"), index=False)

    # Plots
    t_vals=df['t'].values
    b1_spike_t = df.loc[df['b1_spike']==1,'t'].values
    say_t = df.loc[df['did_say']==1,'t'].values

    save_line_plot(t_vals, df['b1_z'].values, os.path.join(figs,"b1_z_with_spikes_and_say.png"),
                   title="b1_z over time (vertical lines=b1_spike; dots=did_say)", ylabel="b1_z",
                   vlines=b1_spike_t, scatter_points=(say_t, df.loc[df['did_say']==1,'b1_z'].values))

    plt.figure(figsize=(10,4))
    plt.step(t_vals, df['macro_refit'].values, where='post', linewidth=1.0, label='macro_refit')
    plt.plot(t_vals, df['has_input'].values*0.2, linewidth=1.0, label='has_input (scaled)')
    plt.scatter(say_t, df.loc[df['did_say']==1,'macro_refit'].values, s=30, label='did_say')
    plt.title("Macrostate, input presence, and did_say")
    plt.xlabel("t"); plt.ylabel("state / scaled input")
    plt.legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(figs,"macro_input_say.png"), dpi=150)
    plt.close()

    # Simple ETA plots
    def save_eta(name, event_idx, window, fname, ylabel):
        offsets, mean, n_events = event_triggered_average(df[name].values.astype(float), event_idx, window=window)
        save_eta_plot(offsets, mean, os.path.join(figs,fname), title=f"ETA around events (n={n_events})", ylabel=ylabel)

    # macro transitions
    macro = df['macro_refit'].values
    trans_idx = np.where(macro[1:] != macro[:-1])[0]+1
    save_eta('b1_z', trans_idx, 20, "eta_macrotrans_b1_z.png", "b1_z")
    save_eta('trail_entropy', trans_idx, 20, "eta_macrotrans_trail_entropy.png", "trail_entropy")
    save_eta('active_edges', trans_idx, 20, "eta_macrotrans_active_edges.png", "active_edges")
    save_eta('has_input', trans_idx, 20, "eta_macrotrans_has_input.png", "has_input")
    save_eta('did_say', trans_idx, 20, "eta_macrotrans_did_say.png", "did_say")

    # say events
    save_eta('b1_z', say_idx, 50, "eta_say_b1_z.png", "b1_z")
    save_eta('trail_entropy', say_idx, 50, "eta_say_trail_entropy.png", "trail_entropy")
    save_eta('active_edges', say_idx, 50, "eta_say_active_edges.png", "active_edges")

    # SHA256 sums
    sums=[]
    for root,_,files in os.walk(args.out):
        for fn in files:
            if fn=="SHA256SUMS.csv":
                continue
            p=os.path.join(root,fn)
            rel=os.path.relpath(p,args.out)
            sums.append({'path':rel.replace("\\","/"), 'sha256':sha256_file(p)})
    pd.DataFrame(sums).sort_values('path').to_csv(os.path.join(args.out,"SHA256SUMS.csv"), index=False)

    print("Done. Output:", args.out)


if __name__=="__main__":
    main()
