#!/usr/bin/env python3
"""Compute the four 'proof' figures from tick + snapshot tables.

Inputs:
  - tick_table_full.csv.gz (from 00_build_tick_table.py)
  - snapshot_metrics.csv (from 01_compute_snapshot_metrics.py)

Outputs:
  figures/*.png and tables/*.csv in the output directory.

Proof 1: Hub recurrence plot (Jaccard of top-20 hubs across snapshots)
Proof 2: PSD + avalanche CCDFs for firing_var / active_edges
Proof 3: Free energy landscape F=-ln p(x,y) where x=mean_out_degree, y=gini_out_degree (KDE-smoothed)
Proof 4: Statistical speed (Hellinger distance between consecutive territory mass distributions)

Notes:
  - This is 'offline-only' analysis; no runtime instrumentation required.
"""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import gaussian_kde

def rqa_metrics(R: np.ndarray, l_min: int=2, v_min: int=2, exclude_main_diag: bool=True):
    n=R.shape[0]
    R2=R.copy()
    if exclude_main_diag:
        np.fill_diagonal(R2, False)
    rec_points=int(R2.sum())
    total_points=n*n - n if exclude_main_diag else n*n
    rr=rec_points/total_points if total_points>0 else np.nan

    diag_lengths=[]
    for k in range(1,n):
        diag=np.diag(R2, k=k)
        run=0
        for val in diag:
            if val: run+=1
            else:
                if run>0: diag_lengths.append(run); run=0
        if run>0: diag_lengths.append(run)
    det_points=sum(L for L in diag_lengths if L>=l_min)
    det=det_points/rec_points if rec_points>0 else np.nan
    L_max=max(diag_lengths) if diag_lengths else 0

    vert_lengths=[]
    for j in range(n):
        col=R2[:,j]
        run=0
        for val in col:
            if val: run+=1
            else:
                if run>0: vert_lengths.append(run); run=0
        if run>0: vert_lengths.append(run)
    lam_points=sum(L for L in vert_lengths if L>=v_min)
    lam=lam_points/rec_points if rec_points>0 else np.nan
    V_max=max(vert_lengths) if vert_lengths else 0

    return dict(rr=rr, det=det, lam=lam, L_max=L_max, V_max=V_max, rec_points=rec_points)

def compute_psd_and_beta(x: np.ndarray, fs: float, fmin: float, fmax: float):
    x=np.asarray(x, dtype=float)
    nans=np.isnan(x)
    if nans.any():
        idx=np.arange(len(x))
        x[nans]=np.interp(idx[nans], idx[~nans], x[~nans])
    x=signal.detrend(x)
    f,P=signal.welch(x, fs=fs, nperseg=2048, noverlap=1024)
    mask=(f>=fmin) & (f<=fmax) & (P>0)
    lf=np.log10(f[mask]); lP=np.log10(P[mask])
    if lf.size<10:
        beta=np.nan
    else:
        b,a=np.polyfit(lf,lP,1)
        beta=-b
    return f,P,float(beta)

def plot_psd(f,P,beta,out_path,title,fmin_fit,fmax_fit):
    fig=plt.figure(figsize=(7,5))
    ax=fig.add_subplot(111)
    mask=f>0
    ax.loglog(f[mask], P[mask])
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('PSD')
    ax.set_title(title + f"\nFit β≈{beta:.2f} over {fmin_fit}-{fmax_fit} Hz")
    f0=np.sqrt(fmin_fit*fmax_fit)
    logf=np.log10(f[mask]); logP=np.log10(P[mask])
    P0=10**np.interp(np.log10(f0), logf, logP)
    f_line=np.array([fmin_fit,fmax_fit])
    P_line=P0*(f_line/f0)**(-beta)
    ax.loglog(f_line, P_line, linestyle='--')
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

def compute_avalanches(activity: np.ndarray, thr: float):
    a=np.asarray(activity, dtype=float)
    above=a>thr
    sizes=[]; durs=[]
    size=0.0; dur=0; in_evt=False
    for ab,val in zip(above,a):
        if ab:
            in_evt=True
            size += (val-thr)
            dur += 1
        else:
            if in_evt:
                sizes.append(size); durs.append(dur)
                size=0.0; dur=0; in_evt=False
    if in_evt:
        sizes.append(size); durs.append(dur)
    return np.array(sizes), np.array(durs)

def plot_ccdf(data: np.ndarray, out_path, title):
    data=np.asarray(data, dtype=float)
    data=data[np.isfinite(data)]
    data=data[data>0]
    if data.size==0:
        return
    x=np.sort(data)
    n=x.size
    ccdf=1.0 - np.arange(n)/n
    fig=plt.figure(figsize=(6,4.5))
    ax=fig.add_subplot(111)
    ax.loglog(x, ccdf)
    ax.set_xlabel('Value')
    ax.set_ylabel('CCDF  P(X≥x)')
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

def hellinger(p: np.ndarray, q: np.ndarray):
    sp=np.sqrt(p); sq=np.sqrt(q)
    return np.linalg.norm(sp-sq)/np.sqrt(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tick_table', required=True)
    ap.add_argument('--snapshot_metrics', required=True)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--hz', type=float, default=10.0)
    ap.add_argument('--steady_start', type=int, default=500)
    args=ap.parse_args()

    out_dir=Path(args.out_dir)
    (out_dir/'figures').mkdir(parents=True, exist_ok=True)
    (out_dir/'tables').mkdir(parents=True, exist_ok=True)

    tick=pd.read_csv(args.tick_table)
    snap=pd.read_csv(args.snapshot_metrics)

    # ---------------- Proof 1: hub recurrence ----------------
    hubs=[set(json.loads(s)) for s in snap['top_hubs_json']]
    n=len(hubs)
    S=np.zeros((n,n), dtype=float)
    for i in range(n):
        A=hubs[i]
        for j in range(i,n):
            inter=len(A & hubs[j])
            union=40 - inter
            jac=inter/union if union>0 else 1.0
            S[i,j]=jac
            if j!=i: S[j,i]=jac

    fig=plt.figure(figsize=(8,7))
    ax=fig.add_subplot(111)
    im=ax.imshow(S, aspect='auto', origin='lower')
    ax.set_title('Proof 1: Hub Occupancy Recurrence (Jaccard, Top-20)')
    ax.set_xlabel('Snapshot index')
    ax.set_ylabel('Snapshot index')
    cbar=fig.colorbar(im, ax=ax); cbar.set_label('Jaccard similarity')
    fig.tight_layout()
    fig.savefig(out_dir/'figures'/'proof1_hub_recurrence_jaccard.png', dpi=200)
    plt.close(fig)

    # RQA metrics by threshold
    rows=[]
    for th in [0.2,0.25,0.3,0.35,0.4,0.45,0.5]:
        R=(S>=th)
        rows.append({'theta':th, **rqa_metrics(R)})
    pd.DataFrame(rows).to_csv(out_dir/'tables'/'proof1_rqa_metrics_by_threshold.csv', index=False)

    # ---------------- Proof 2: PSD + avalanches ---------------
    tick=tick.set_index('t').sort_index()
    for metric in ['firing_var','active_edges','active_synapses']:
        if metric not in tick.columns:
            continue
        series=tick.loc[args.steady_start:, metric].astype(float).values
        f,P,beta=compute_psd_and_beta(series, fs=args.hz, fmin=0.1, fmax=1.0)
        plot_psd(f,P,beta, out_dir/'figures'/f'proof2_psd_{metric}_steady.png',
                 title=f'Proof 2: PSD of {metric} (steady-state)',
                 fmin_fit=0.1, fmax_fit=1.0)

        # avalanches (q0.75 threshold)
        thr=float(np.nanquantile(series, 0.75))
        sizes,durs=compute_avalanches(series, thr)
        plot_ccdf(durs, out_dir/'figures'/f'proof2_avalanche_duration_ccdf_{metric}.png',
                  title=f'Proof 2: Avalanche durations ({metric}), thr=q0.75')
        plot_ccdf(sizes, out_dir/'figures'/f'proof2_avalanche_size_ccdf_{metric}.png',
                  title=f'Proof 2: Avalanche sizes ({metric}), thr=q0.75')

    # ---------------- Proof 3: Free energy landscape ----------
    x=snap['mean_out_degree'].values
    y=snap['gini_out_degree'].values
    X=np.vstack([x,y])
    kde=gaussian_kde(X)
    grid_x=np.linspace(x.min(), x.max(), 80)
    grid_y=np.linspace(y.min(), y.max(), 80)
    GX,GY=np.meshgrid(grid_x, grid_y, indexing='ij')
    points=np.vstack([GX.ravel(), GY.ravel()])
    P=kde(points).reshape(GX.shape)
    P=P/P.sum()
    F=-np.log(P + 1e-12)

    fig=plt.figure(figsize=(7,5.5))
    ax=fig.add_subplot(111)
    cs=ax.contourf(GX, GY, F, levels=30)
    cbar=fig.colorbar(cs, ax=ax); cbar.set_label('F=-ln p(x,y) (KDE)')
    ax.set_xlabel('Edge density (mean out-degree)')
    ax.set_ylabel('Hierarchy (Gini of out-degree)')
    ax.set_title('Proof 3: Free Energy Landscape (KDE-smoothed)')
    ax.scatter(x, y, s=6, alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_dir/'figures'/'proof3_free_energy_landscape_kde.png', dpi=200)
    plt.close(fig)

    # ---------------- Proof 4: statistical speed --------------
    masses=np.vstack([json.loads(s) for s in snap['territory_masses_json']])
    Pm=masses/(masses.sum(axis=1, keepdims=True)+1e-12)
    d=[]
    for i in range(len(Pm)-1):
        d.append(hellinger(Pm[i],Pm[i+1]))
    d=np.array(d)
    t_mid=snap['tick'].values[1:]
    pd.DataFrame({'tick':t_mid.astype(int),'hellinger_speed':d}).to_csv(out_dir/'tables'/'proof4_fisher_speed_hellinger.csv', index=False)

    fig=plt.figure(figsize=(7,5))
    ax=fig.add_subplot(111)
    ax.plot(t_mid, d, linewidth=1)
    ax.set_xlabel('Tick')
    ax.set_ylabel('Hellinger distance')
    ax.set_title('Proof 4: Statistical Speed (territory mass distributions)')
    fig.tight_layout()
    fig.savefig(out_dir/'figures'/'proof4_fisher_speed_hellinger.png', dpi=200)
    plt.close(fig)

    print('Done.')

if __name__=='__main__':
    main()