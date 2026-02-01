#!/usr/bin/env python3
"""
Reproducible scale-free / heavy-tail / Gini analysis for VDM 1000-neuron connectome.

This script re-generates:
- degree distributions (out/in/total)
- Gini coefficients
- Clauset-style discrete power-law tail fit (xmin, alpha, KS)
- bootstrap p-value for KS (tail-only)
- simple model comparisons via Vuong z (powerlaw vs lognormal / exponential), tail-only

Input:
- 1000_neurons_events.zip containing state_*.h5 with:
    sparse/row_ptr (n+1)
    sparse/col_idx (nnz)
    sparse/W (n)  [per-row weights; not used for degree fits]

Outputs:
- CSV/JSON + plots under --outdir

Notes:
- This is a *statistical signature* analysis (scale-free heavy tail); it does not claim causality.
"""
import argparse, zipfile, io, json, hashlib, datetime, math
from pathlib import Path

import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import optimize, special, stats

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def gini(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x)==0:
        return np.nan
    if np.min(x) < 0:
        x = x - np.min(x)
    if np.all(x==0):
        return 0.0
    x_sorted = np.sort(x)
    n = len(x_sorted)
    cumx = np.cumsum(x_sorted)
    return (n + 1 - 2*np.sum(cumx)/cumx[-1]) / n

def ccdf_int(x):
    x = np.asarray(x, dtype=int)
    x = x[np.isfinite(x)]
    x = x[x>=0]
    if len(x)==0:
        return pd.DataFrame({"k":[], "ccdf":[]})
    maxk = int(x.max())
    counts = np.bincount(x, minlength=maxk+1)
    tail = counts[::-1].cumsum()[::-1] / counts.sum()
    ks = np.arange(len(tail))
    return pd.DataFrame({"k": ks, "ccdf": tail})

def pl_loglik_discrete(alpha, x, xmin):
    x = np.asarray(x, dtype=int)
    x = x[x>=xmin]
    n = len(x)
    if n==0:
        return -np.inf
    z = special.zeta(alpha, xmin)  # Hurwitz zeta
    if not np.isfinite(z) or z<=0:
        return -np.inf
    return -alpha*np.sum(np.log(x)) - n*np.log(z)

def fit_powerlaw_discrete(x, xmin, alpha_bounds=(1.01, 6.0)):
    x = np.asarray(x, dtype=int)
    x = x[x>=xmin]
    if len(x) < 10:
        return None
    def nll(a):
        return -pl_loglik_discrete(a, x, xmin)
    res = optimize.minimize_scalar(nll, bounds=alpha_bounds, method="bounded")
    if not res.success:
        return None
    alpha = float(res.x)
    ll = -float(res.fun)
    return alpha, ll

def ks_distance_powerlaw_discrete(x, xmin, alpha):
    x = np.asarray(x, dtype=int)
    x = x[x>=xmin]
    if len(x)==0:
        return np.nan
    xs = np.sort(x)
    n = len(xs)
    uniq = np.unique(xs)
    emp = np.array([np.searchsorted(xs, k, side="right")/n for k in uniq], dtype=float)
    z_xmin = special.zeta(alpha, xmin)
    theo = 1.0 - (special.zeta(alpha, uniq+1) / z_xmin)
    return float(np.max(np.abs(emp - theo)))

def select_xmin_clauset_discrete(x, xmin_candidates=None, min_tail=50, alpha_bounds=(1.01, 6.0)):
    x = np.asarray(x, dtype=int)
    x = x[np.isfinite(x)]
    x = x[x>0]
    if xmin_candidates is None:
        xmin_candidates = np.unique(x)
    best = None
    rows=[]
    for xmin in xmin_candidates:
        tail = x[x>=xmin]
        n_tail = len(tail)
        if n_tail < min_tail:
            continue
        fit = fit_powerlaw_discrete(x, xmin, alpha_bounds=alpha_bounds)
        if fit is None:
            continue
        alpha, ll = fit
        ks = ks_distance_powerlaw_discrete(x, xmin, alpha)
        rows.append({"xmin": int(xmin), "alpha": alpha, "ks": ks, "n_tail": n_tail, "loglik": ll})
        if best is None or ks < best["ks"]:
            best = {"xmin": int(xmin), "alpha": alpha, "ks": ks, "n_tail": n_tail, "loglik": ll}
    return best, pd.DataFrame(rows).sort_values("ks")

def sample_discrete_powerlaw(alpha, xmin, n, rng):
    z = special.zeta(alpha, xmin)
    xmax = int(min(max(xmin+500, xmin * (n**(1/(alpha-1)))), 20000))
    xs = np.arange(xmin, xmax+1)
    pmf = xs**(-alpha) / z
    cdf = np.cumsum(pmf)
    cdf = cdf / cdf[-1]
    u = rng.random(n)
    idx = np.searchsorted(cdf, u, side="left")
    return xs[idx]

def bootstrap_p_value_ks(x, xmin, alpha, ks_obs, n_boot=200, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=int)
    tail = x[x>=xmin]
    n_tail = len(tail)
    if n_tail==0:
        return np.nan
    ks_synth=[]
    for _ in range(n_boot):
        synth = sample_discrete_powerlaw(alpha, xmin, n_tail, rng)
        fit = fit_powerlaw_discrete(synth, xmin)
        if fit is None:
            continue
        a_hat, _ = fit
        ks_b = ks_distance_powerlaw_discrete(synth, xmin, a_hat)
        ks_synth.append(ks_b)
    if len(ks_synth)==0:
        return np.nan
    ks_synth = np.array(ks_synth)
    return float(np.mean(ks_synth >= ks_obs))

def exp_fit_geometric_ll_i(tail, xmin):
    y = tail - xmin
    mean_y = y.mean()
    if mean_y <= 0:
        q = 1e-12
    else:
        q = mean_y/(mean_y+1.0)
    q = min(max(q, 1e-12), 1-1e-12)
    lam = -math.log(q)
    ll_i = math.log(1-q) + y*np.log(q)
    return lam, ll_i

def lognormal_trunc_ll_i(tail, xmin):
    lx = np.log(tail.astype(float))
    mu = float(lx.mean())
    sigma = float(lx.std(ddof=0))
    sigma = max(sigma, 1e-9)
    ll_i = -np.log(tail.astype(float)) - math.log(sigma) - 0.5*math.log(2*math.pi) - ((lx-mu)**2)/(2*sigma**2)
    a = (math.log(xmin) - mu)/sigma
    Z = 1.0 - stats.norm.cdf(a)
    Z = max(Z, 1e-12)
    ll_i = ll_i - math.log(Z)
    return mu, sigma, ll_i

def vuong_test(ll1, ll2):
    d = ll1 - ll2
    n = len(d)
    if n<10:
        return np.nan, np.nan
    sd = d.std(ddof=1)
    if sd==0:
        return np.sign(d.mean())*np.inf, 0.0
    z = d.sum() / (sd * math.sqrt(n))
    p = 2*(1-stats.norm.cdf(abs(z)))
    return float(z), float(p)

def analyze_discrete_heavytail(x, label, min_tail=50, seed=0, n_boot=200):
    x = np.asarray(x, dtype=int)
    x = x[x>0]
    best, grid = select_xmin_clauset_discrete(x, min_tail=min_tail)
    grid.to_csv(outdir/f"tail_fit_grid_{label}.csv", index=False)
    if best is None:
        return None
    xmin = best["xmin"]
    alpha = best["alpha"]
    ks = best["ks"]
    n_tail = best["n_tail"]
    pval = bootstrap_p_value_ks(x, xmin, alpha, ks, n_boot=n_boot, seed=seed)
    xmax = int(x.max())
    decades = math.log10(xmax/xmin) if xmax>xmin else 0.0

    tail = x[x>=xmin].astype(int)
    z = special.zeta(alpha, xmin)
    ll_pl_i = -alpha*np.log(tail) - np.log(z)

    lam, ll_exp_i = exp_fit_geometric_ll_i(tail, xmin)
    mu, sigma, ll_ln_i = lognormal_trunc_ll_i(tail, xmin)

    z_pl_ln, p_pl_ln = vuong_test(ll_pl_i, ll_ln_i)
    z_pl_exp, p_pl_exp = vuong_test(ll_pl_i, ll_exp_i)

    # CCDF overlay
    cc = ccdf_int(x)
    plt.figure(figsize=(6,4))
    plt.loglog(cc["k"][1:], cc["ccdf"][1:], marker='.', linestyle='none', label="empirical")
    k = cc["k"].to_numpy()
    k_tail = k[k>=xmin]
    ccdf_theo = special.zeta(alpha, k_tail) / special.zeta(alpha, xmin)
    plt.loglog(k_tail, ccdf_theo, linestyle='-', label=f"fit xmin={xmin}, alpha={alpha:.3f}")
    plt.xlabel("k"); plt.ylabel("P(K>=k)")
    plt.title(f"{label}: CCDF with tail fit")
    plt.legend(); plt.tight_layout()
    plt.savefig(outdir/f"{label}_ccdf_with_fit.png", dpi=200)
    plt.close()

    return {
        "label": label,
        "xmin": int(xmin),
        "alpha": float(alpha),
        "ks": float(ks),
        "p_boot_ks": float(pval),
        "n_tail": int(n_tail),
        "xmax": int(xmax),
        "tail_decades_log10": float(decades),
        "gini": float(gini(x)),
        "loglik_powerlaw": float(ll_pl_i.sum()),
        "exp_lambda_hat": float(lam),
        "loglik_exponential": float(ll_exp_i.sum()),
        "lognormal_mu_hat": float(mu),
        "lognormal_sigma_hat": float(sigma),
        "loglik_lognormal": float(ll_ln_i.sum()),
        "vuong_z_pl_vs_lognormal": float(z_pl_ln),
        "vuong_p_pl_vs_lognormal": float(p_pl_ln),
        "vuong_z_pl_vs_exponential": float(z_pl_exp),
        "vuong_p_pl_vs_exponential": float(p_pl_exp),
    }

def main():
    global outdir
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True, help="path to 1000_neurons_events.zip")
    ap.add_argument("--state", default="state_394860.h5", help="H5 state file inside zip")
    ap.add_argument("--outdir", default="vdm_scale_free_1k_analysis_out", help="output directory")
    ap.add_argument("--min_tail", type=int, default=50)
    ap.add_argument("--n_boot", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    zip_path = Path(args.zip)
    with zipfile.ZipFile(zip_path,'r') as zf:
        h5_bytes = zf.read(args.state)
        events_bytes = zf.read("events.jsonl")
        utd_bytes = zf.read("utd_events.jsonl")

    prov = {
        "source_zip": zip_path.name,
        "zip_sha256": sha256_bytes(zip_path.read_bytes()),
        "state_h5": args.state,
        "state_h5_sha256": sha256_bytes(h5_bytes),
        "events_jsonl_sha256": sha256_bytes(events_bytes),
        "utd_events_jsonl_sha256": sha256_bytes(utd_bytes),
    }

    ts=[]
    for ln in events_bytes.decode("utf-8", errors="ignore").splitlines():
        try:
            obj=json.loads(ln)
        except:
            continue
        if "ts" in obj:
            ts.append(float(obj["ts"]))
    if ts:
        prov["events_ts_utc_min"] = datetime.datetime.utcfromtimestamp(min(ts)).isoformat()+"Z"
        prov["events_ts_utc_max"] = datetime.datetime.utcfromtimestamp(max(ts)).isoformat()+"Z"

    with h5py.File(io.BytesIO(h5_bytes), 'r') as h5:
        row_ptr = h5["sparse/row_ptr"][:]
        col_idx = h5["sparse/col_idx"][:]

    n_nodes = len(row_ptr)-1
    out_deg = np.diff(row_ptr).astype(int)
    in_deg = np.bincount(col_idx, minlength=n_nodes).astype(int)
    tot_deg = out_deg + in_deg

    pd.DataFrame({
        "node": np.arange(n_nodes),
        "out_degree": out_deg,
        "in_degree": in_deg,
        "total_degree": tot_deg,
    }).to_csv(outdir/"connectome_node_degrees.csv", index=False)

    (outdir/"provenance.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")

    results=[]
    for arr,label in [(out_deg,"out_degree"), (in_deg,"in_degree"), (tot_deg,"total_degree")]:
        r = analyze_discrete_heavytail(arr, label, min_tail=args.min_tail, seed=args.seed, n_boot=args.n_boot)
        results.append(r)
    pd.DataFrame(results).to_csv(outdir/"tail_fit_summary_degrees.csv", index=False)

if __name__ == "__main__":
    main()
