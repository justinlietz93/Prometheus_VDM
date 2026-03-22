#!/usr/bin/env python3
"""
Offline node-correspondence matching between VDM state_*.h5 snapshots.

Goal:
- Estimate how much edge turnover is due to node reindexing/permutation vs true rewiring.

This is intentionally sparse:
- CSR ops (A @ v, A @ A)
- sparse eigensolver for Laplacian embedding (eigsh)
- Hungarian assignment on 1000x1000 cost matrix (OK for N~1k; for larger N, see TODO notes)

Outputs:
- tables/*.csv
- figures/*.png
"""

import os, glob, argparse
import numpy as np
import pandas as pd
import h5py
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
from itertools import combinations

def load_snapshot(path):
    name=os.path.basename(path).replace(".h5","")
    with h5py.File(path,'r') as f:
        W=f['sparse/W'][()].astype(np.float64)
        col_idx=f['sparse/col_idx'][()].astype(np.int32)
        row_ptr=f['sparse/row_ptr'][()].astype(np.int64)
    N=len(W)
    E=len(col_idx)
    data=np.ones(E, dtype=np.int8)
    A=sp.csr_matrix((data, col_idx, row_ptr), shape=(N,N), dtype=np.int8)
    out_deg=np.diff(row_ptr).astype(np.int64)
    in_deg=np.bincount(col_idx, minlength=N).astype(np.int64)
    A_und = ((A + A.T) > 0).astype(np.int8).tocsr()
    return dict(name=name, path=path, N=N, E=E, row_ptr=row_ptr, col_idx=col_idx, W=W,
                A=A, A_und=A_und, out_deg=out_deg, in_deg=in_deg)

def compute_spectral_coords(A_und, k=8):
    N=A_und.shape[0]
    deg=np.array(A_und.sum(axis=1)).ravel().astype(float)
    inv_sqrt=np.zeros_like(deg)
    mask=deg>0
    inv_sqrt[mask]=1.0/np.sqrt(deg[mask])
    Dinv=sp.diags(inv_sqrt)
    L = sp.eye(N, format='csr') - Dinv @ A_und @ Dinv

    k_compute=min(N-2, k+6)
    vals, vecs = spla.eigsh(L, k=k_compute, which='SM')
    idx=np.argsort(vals)
    vals=vals[idx]
    vecs=vecs[:,idx]

    nontriv = np.where(vals>1e-6)[0]
    start = int(nontriv[0]) if len(nontriv)>0 else 0
    take = vecs[:, start:start+k]

    for j in range(take.shape[1]):
        if take[:,j].sum() < 0:
            take[:,j] *= -1
    return take

def compute_node_features(snap, k_spec=8, include_twohop=True):
    A = snap["A"].astype(np.int32)
    out_deg = snap["out_deg"].astype(float)
    in_deg  = snap["in_deg"].astype(float)
    W = snap["W"].astype(float)

    # 1-hop neighbor sums
    nbr_outdeg_sum = A.dot(out_deg)
    nbr_indeg_sum  = A.dot(in_deg)
    nbr_W_sum      = A.dot(W)

    # 2-hop features via sparse multiply
    if include_twohop:
        B = A.dot(A)  # counts of length-2 paths
        twohop_paths      = np.array(B.sum(axis=1)).ravel().astype(float)
        twohop_outdeg_sum = B.dot(out_deg)
        twohop_W_sum      = B.dot(W)
    else:
        twohop_paths      = np.zeros(snap["N"])
        twohop_outdeg_sum = np.zeros(snap["N"])
        twohop_W_sum      = np.zeros(snap["N"])

    # spectral coords (undirected Laplacian)
    spec = compute_spectral_coords(snap["A_und"], k=k_spec)

    feats = np.column_stack([
        out_deg, in_deg, W,
        nbr_outdeg_sum, nbr_indeg_sum, nbr_W_sum,
        twohop_paths, twohop_outdeg_sum, twohop_W_sum,
        spec
    ])
    return feats

def zscore_pair(X, Y):
    Z=np.vstack([X,Y])
    mu=Z.mean(axis=0)
    sd=Z.std(axis=0)
    sd[sd==0]=1.0
    return (X-mu)/sd, (Y-mu)/sd

def pairwise_cost(X, Y):
    X2=np.sum(X*X, axis=1)[:,None]
    Y2=np.sum(Y*Y, axis=1)[None,:]
    XY=X @ Y.T
    d2=X2 + Y2 - 2*XY
    d2[d2<0]=0
    return np.sqrt(d2)

def match_nodes_features(feats_a, feats_b):
    Xa,Xb=zscore_pair(feats_a,feats_b)
    C=pairwise_cost(Xa,Xb)
    row_ind,col_ind=linear_sum_assignment(C)
    perm=np.empty_like(col_ind)
    perm[row_ind]=col_ind
    return perm, C

def csr_edge_ids(row_ptr, col_idx, N):
    row_idx = np.repeat(np.arange(N, dtype=np.int64), np.diff(row_ptr))
    ids = row_idx * N + col_idx.astype(np.int64)
    return np.unique(ids)

def permute_edge_ids(ids_B, inv_perm, N):
    row = (ids_B // N).astype(np.int64)
    col = (ids_B % N).astype(np.int64)
    row2 = inv_perm[row]
    col2 = inv_perm[col]
    return np.unique(row2 * N + col2)

def edge_jaccard(ids1, ids2):
    inter=np.intersect1d(ids1, ids2, assume_unique=True)
    union=ids1.size + ids2.size - inter.size
    return inter.size/union if union>0 else 1.0, int(inter.size), int(union)

def corr(a,b):
    a=np.asarray(a); b=np.asarray(b)
    if a.std()==0 or b.std()==0:
        return float("nan")
    return float(np.corrcoef(a,b)[0,1])

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--h5_dir", required=True, help="Directory containing state_*.h5 checkpoints")
    ap.add_argument("--out_dir", required=True, help="Output directory")
    ap.add_argument("--k_spec", type=int, default=8, help="Spectral embedding dimensions")
    args=ap.parse_args()

    out_dir=args.out_dir
    ensure_dir(out_dir)
    ensure_dir(os.path.join(out_dir,"tables"))
    ensure_dir(os.path.join(out_dir,"figures"))

    paths=sorted(glob.glob(os.path.join(args.h5_dir,"state_*.h5")))
    if not paths:
        raise SystemExit("No state_*.h5 found in --h5_dir")
    snaps=[load_snapshot(p) for p in paths]
    N=snaps[0]["N"]

    # precompute edge ids and features
    edge_ids={s["name"]: csr_edge_ids(s["row_ptr"], s["col_idx"], N) for s in snaps}
    feats={s["name"]: compute_node_features(s, k_spec=args.k_spec, include_twohop=True) for s in snaps}

    # consecutive pair metrics
    rows=[]
    pair_labels=[]
    for i in range(len(snaps)-1):
        a=snaps[i]; b=snaps[i+1]
        ids_a=edge_ids[a["name"]]; ids_b=edge_ids[b["name"]]
        jac_raw, inter_raw, union_raw = edge_jaccard(ids_a, ids_b)

        perm, C = match_nodes_features(feats[a["name"]], feats[b["name"]])
        inv=np.empty_like(perm); inv[perm]=np.arange(N)
        ids_b_al = permute_edge_ids(ids_b, inv, N)
        jac_gs, inter_gs, union_gs = edge_jaccard(ids_a, ids_b_al)

        costs=C[np.arange(N), perm]
        rows.append(dict(
            snap_a=a["name"], snap_b=b["name"],
            edge_jaccard_raw=jac_raw, edge_inter_raw=inter_raw, edge_union_raw=union_raw,
            edge_jaccard_graphsig=jac_gs, edge_inter_graphsig=inter_gs, edge_union_graphsig=union_gs,
            edge_persist_frac_of_A=inter_gs/a["E"], edge_persist_frac_of_B=inter_gs/b["E"],
            W_corr_raw=corr(a["W"], b["W"]),
            W_corr_graphsig=corr(a["W"], b["W"][perm]),
            outdeg_corr_raw=corr(a["out_deg"], b["out_deg"]),
            outdeg_corr_graphsig=corr(a["out_deg"], b["out_deg"][perm]),
            match_cost_mean=float(np.mean(costs)),
            match_cost_p50=float(np.percentile(costs,50)),
            match_cost_p90=float(np.percentile(costs,90)),
        ))
        pair_labels.append(f"{a['name'].split('_')[1]}→{b['name'].split('_')[1]}")

        # save mapping
        map_df=pd.DataFrame({"node_a":np.arange(N), "node_b":perm.astype(int), "match_cost":costs})
        map_df.to_csv(os.path.join(out_dir,"tables",f"mapping_graphsig_{a['name']}_to_{b['name']}.csv.gz"),
                      index=False, compression="gzip")

    df_pairs=pd.DataFrame(rows)
    df_pairs.to_csv(os.path.join(out_dir,"tables","pair_matching_metrics_consecutive.csv"), index=False)

    # all-pairs raw vs graphsig
    rows=[]
    for i,j in combinations(range(len(snaps)),2):
        a=snaps[i]; b=snaps[j]
        ids_a=edge_ids[a["name"]]; ids_b=edge_ids[b["name"]]
        jac_raw, _, _ = edge_jaccard(ids_a, ids_b)
        perm,_ = match_nodes_features(feats[a["name"]], feats[b["name"]])
        inv=np.empty_like(perm); inv[perm]=np.arange(N)
        ids_b_al=permute_edge_ids(ids_b, inv, N)
        jac_gs, _, _ = edge_jaccard(ids_a, ids_b_al)
        rows.append(dict(snap_a=a["name"], snap_b=b["name"], edge_jaccard_raw=jac_raw, edge_jaccard_graphsig=jac_gs))
    pd.DataFrame(rows).to_csv(os.path.join(out_dir,"tables","pair_matching_metrics_allpairs_raw_vs_graphsig.csv"), index=False)

    # transitivity (triple consistency)
    perms={}
    for i,j in combinations(range(len(snaps)),2):
        a=snaps[i]["name"]; b=snaps[j]["name"]
        perm,_=match_nodes_features(feats[a], feats[b])
        perms[(a,b)]=perm
    triples=[]
    for i,j,k in combinations(range(len(snaps)),3):
        a=snaps[i]["name"]; b=snaps[j]["name"]; c=snaps[k]["name"]
        p_ab=perms[(a,b)]
        p_bc=perms[(b,c)]
        p_ac=perms[(a,c)]
        comp=p_bc[p_ab]
        triples.append(dict(snap_a=a,snap_b=b,snap_c=c,composition_consistency=float(np.mean(comp==p_ac))))
    pd.DataFrame(triples).to_csv(os.path.join(out_dir,"tables","matching_transitivity_triples.csv"), index=False)

    # Figures: edge jaccard bars
    x=np.arange(len(pair_labels))
    width=0.35
    fig,ax=plt.subplots(figsize=(10,4))
    ax.bar(x-width/2, df_pairs["edge_jaccard_raw"], width, label="raw")
    ax.bar(x+width/2, df_pairs["edge_jaccard_graphsig"], width, label="graph-signature")
    ax.set_xticks(x); ax.set_xticklabels(pair_labels)
    ax.set_ylabel("Directed edge Jaccard")
    ax.set_title("Edge overlap: raw vs graph-signature alignment")
    ax.legend(frameon=False)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir,"figures","edge_jaccard_raw_vs_graphsig.png"), dpi=200)
    plt.close(fig)

    # Figures: W correlation bars
    fig,ax=plt.subplots(figsize=(10,4))
    ax.bar(x-width/2, df_pairs["W_corr_raw"], width, label="raw")
    ax.bar(x+width/2, df_pairs["W_corr_graphsig"], width, label="graph-signature")
    ax.set_xticks(x); ax.set_xticklabels(pair_labels)
    ax.set_ylabel("Pearson r")
    ax.set_title("Per-node W correlation: raw vs aligned")
    ax.legend(frameon=False)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir,"figures","W_corr_raw_vs_graphsig.png"), dpi=200)
    plt.close(fig)

    print("Done. Outputs written to:", out_dir)

if __name__ == "__main__":
    main()
