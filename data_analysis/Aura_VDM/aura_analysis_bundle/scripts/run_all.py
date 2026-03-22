#!/usr/bin/env python3
"""
VDM High-Impact Scalar Telemetry Analysis (pre-locality logs)

Reproduces:
- Motor-gate / decoder readout model
- Macrostate (metastable) model + dwell times + transition-triggered averages
- Goal-drive atlas (windowed transfer entropy)
- Input->internal coupling (ΔR²) + internal->output gating check
- Candidate coherent episode ranking (integration/differentiation/persistence/endogeneity)
- Scaling dashboard across neuron counts present in utd_events

Usage:
  python run_all.py --input_zip /path/to/1000_neurons_events.zip --out_dir ./vdm_high_impact_scalar_analysis_v1

Notes:
  - This script intentionally avoids any locality/geometry reconstruction: old logs are scalar telemetry.
  - Outputs are written as CSV + PNG into out_dir/{tables,figures,logs}
"""
import argparse, json, re, zipfile, os, math, hashlib
from collections import defaultdict, Counter
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score, average_precision_score, precision_recall_curve, r2_score
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

import matplotlib.pyplot as plt


def safe_zscore(X: np.ndarray) -> np.ndarray:
    mu = np.nanmean(X, axis=0)
    sd = np.nanstd(X, axis=0)
    sd[sd == 0] = 1.0
    return (X - mu) / sd


def implied_timescale(lam: float) -> float:
    if lam <= 0 or lam >= 1:
        return float("inf")
    return -1.0 / math.log(lam)


def discretize_quantiles(x, n_bins=8):
    x = np.asarray(x)
    qs = np.linspace(0, 1, n_bins + 1)
    edges = np.quantile(x, qs)
    edges = np.unique(edges)
    if len(edges) <= 2:
        return np.zeros_like(x, dtype=int), edges
    bins = np.digitize(x, edges[1:-1], right=False)
    return bins.astype(int), edges


def transfer_entropy_discrete(x, y, lag=1, n_bins=8) -> float:
    """
    TE(X->Y) = I(X_{t-lag}; Y_t | Y_{t-lag}) in bits, using quantile discretization.
    """
    x_b, _ = discretize_quantiles(x, n_bins)
    y_b, _ = discretize_quantiles(y, n_bins)

    x_prev = x_b[:-lag]
    y_prev = y_b[:-lag]
    y_t = y_b[lag:]

    bx = max(x_b.max() + 1, n_bins)
    by = max(y_b.max() + 1, n_bins)

    triple = y_t + by * (y_prev + by * x_prev)
    pair_yx = y_prev + by * x_prev
    pair_yy = y_t + by * y_prev

    ct_triple = Counter(triple)
    ct_pair_yx = Counter(pair_yx)
    ct_pair_yy = Counter(pair_yy)
    ct_y_prev = Counter(y_prev)

    n = len(y_t)
    te = 0.0
    for key, c in ct_triple.items():
        p_xyz = c / n
        y_t_val = key % by
        tmp = key // by
        y_prev_val = tmp % by
        x_prev_val = tmp // by

        denom_yx = ct_pair_yx[y_prev_val + by * x_prev_val]
        p_y_given_yx = c / denom_yx if denom_yx else 0.0

        denom_y = ct_y_prev[y_prev_val]
        p_y_given_y = (ct_pair_yy[y_t_val + by * y_prev_val] / denom_y) if denom_y else 0.0

        te += p_xyz * math.log((p_y_given_yx + 1e-12) / (p_y_given_y + 1e-12))
    return te / math.log(2)


def powerlaw_mle_continuous(data, xmin):
    x = np.asarray(data)
    x = x[x >= xmin]
    n = len(x)
    if n < 5:
        return float("nan"), float("nan"), n
    alpha = 1 + n / np.sum(np.log(x / xmin))
    x_sorted = np.sort(x)
    cdf_emp = np.arange(1, n + 1) / n
    cdf_pl = 1 - (x_sorted / xmin) ** (1 - alpha)
    ks = np.max(np.abs(cdf_emp - cdf_pl))
    return float(alpha), float(ks), int(n)


def parse_utd_events(input_zip: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      status_df: one row per status payload (includes input_text_concat derived from preceding text events)
      say_df: macro say events with t and text
    """
    with zipfile.ZipFile(input_zip, "r") as zf:
        status_rows = []
        pending_texts = []
        pending_scores = []
        say_rows = []

        with zf.open("utd_events.jsonl") as f:
            for line in f:
                obj = json.loads(line)
                typ = obj.get("type")
                if typ == "text":
                    payload = obj.get("payload", {}) or {}
                    ptype = payload.get("type")
                    if ptype == "text":
                        pending_texts.append(payload.get("msg", ""))
                        pending_scores.append(obj.get("score", float("nan")))
                    elif ptype == "status":
                        p = payload
                        row = dict(p)
                        row["input_texts"] = pending_texts
                        row["input_text_concat"] = "\n\n".join([t for t in pending_texts if isinstance(t, str)])
                        row["input_text_n"] = len(pending_texts)
                        concat = row["input_text_concat"]
                        row["input_text_chars"] = len(concat)
                        row["input_text_words"] = len(re.findall(r"\w+", concat))
                        pending_texts = []
                        pending_scores = []
                        status_rows.append(row)
                elif typ == "macro" and obj.get("macro") == "say":
                    args = obj.get("args", {}) or {}
                    why = args.get("why", {}) or {}
                    say_rows.append({
                        "t": why.get("t"),
                        "phase": why.get("phase"),
                        "vt_coverage": why.get("vt_coverage"),
                        "vt_entropy": why.get("vt_entropy"),
                        "connectome_entropy": why.get("connectome_entropy"),
                        "cohesion_components": why.get("cohesion_components"),
                        "b1_z": why.get("b1_z"),
                        "sie_v2_valence_01": why.get("sie_v2_valence_01"),
                        "text": args.get("text", ""),
                    })

    status_df = pd.DataFrame(status_rows)
    say_df = pd.DataFrame(say_rows)
    return status_df, say_df


def assign_say_to_neurons(status_df: pd.DataFrame, say_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign macro say events to neuron runs by matching on t, choosing closest status row if overlaps.
    """
    status_df = status_df.copy()
    # dedup status by (neurons,t)
    status_df = status_df.sort_values(["neurons", "t"]).drop_duplicates(["neurons", "t"], keep="last").reset_index(drop=True)

    # index status rows by t
    status_by_t = defaultdict(list)
    for idx, t in enumerate(status_df["t"].values):
        status_by_t[int(t)].append(idx)

    # precompute std for distance normalization
    stds = status_df[["vt_coverage","vt_entropy","connectome_entropy","cohesion_components","phase"]].std()

    assigned = []
    for _, sr in say_df.iterrows():
        t = sr.get("t")
        if pd.isna(t):
            assigned.append(float("nan"))
            continue
        t = int(t)
        idxs = status_by_t.get(t, [])
        if not idxs:
            assigned.append(float("nan"))
            continue
        if len(idxs) == 1:
            assigned.append(int(status_df.loc[idxs[0], "neurons"]))
            continue

        best = None
        best_d = float("inf")
        for idx in idxs:
            d = 0.0
            count = 0
            for col in ["vt_coverage","vt_entropy","connectome_entropy","cohesion_components","phase"]:
                sv = sr.get(col)
                tv = status_df.loc[idx, col]
                if pd.isna(sv) or pd.isna(tv):
                    continue
                sd = stds[col] if stds[col] else 1.0
                d += ((sv - tv) / sd) ** 2
                count += 1
            if count and d < best_d:
                best_d = d
                best = int(status_df.loc[idx, "neurons"])
        assigned.append(best if best is not None else int(status_df.loc[idxs[0], "neurons"]))

    say_df = say_df.copy()
    say_df["neurons"] = assigned
    say_df["say_words"] = say_df["text"].fillna("").astype(str).apply(lambda s: len(re.findall(r"\w+", s)))
    say_df["say_chars"] = say_df["text"].fillna("").astype(str).apply(len)
    return status_df, say_df


def build_tick_table(status_df: pd.DataFrame, say_df: pd.DataFrame) -> pd.DataFrame:
    say_agg = say_df.dropna(subset=["neurons","t"]).groupby(["neurons","t"]).agg(
        say_count=("text","size"),
        say_words=("say_words","sum"),
        say_chars=("say_chars","sum"),
    ).reset_index()
    df = status_df.merge(say_agg, on=["neurons","t"], how="left")
    for c in ["say_count","say_words","say_chars"]:
        df[c] = df[c].fillna(0)
    df["did_say"] = (df["say_count"] > 0).astype(int)
    df["has_input"] = (df["ute_text_count"] > 0).astype(int)
    return df.sort_values(["neurons","t"]).reset_index(drop=True)


def rolling_any(arr, window):
    s = pd.Series(arr)
    return s.rolling(window, min_periods=1).max().shift(1).fillna(0).astype(int).values


def event_triggered_average(series, event_idxs, window):
    n = len(series)
    w = window
    valid = [idx for idx in event_idxs if idx - w >= 0 and idx + w < n]
    if not valid:
        return None, 0
    mat = np.vstack([series[idx - w: idx + w + 1] for idx in valid])
    return mat.mean(axis=0), len(valid)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_zip", required=True, type=str)
    ap.add_argument("--out_dir", required=True, type=str)
    args = ap.parse_args()

    input_zip = Path(args.input_zip)
    out_dir = Path(args.out_dir)
    (out_dir / "tables").mkdir(parents=True, exist_ok=True)
    (out_dir / "figures").mkdir(parents=True, exist_ok=True)
    (out_dir / "logs").mkdir(parents=True, exist_ok=True)

    status_df, say_df = parse_utd_events(input_zip)
    status_df, say_df = assign_say_to_neurons(status_df, say_df)
    tick_df = build_tick_table(status_df, say_df)

    # Save raw tick table (compressed)
    tick_df.to_csv(out_dir / "tables" / "tick_table_all_runs.csv.gz", index=False, compression="gzip")

    # ---- Focus analysis on 1k run (neurons==1000) ----
    df1k = tick_df[tick_df["neurons"] == 1000].sort_values("t").reset_index(drop=True)
    # Derived features
    df1k["recent_input_any_W50"] = rolling_any(df1k["has_input"].values, 50)

    # reconfig_score as norm of standardized deltas on a small metric subset
    metrics_for_delta = ["active_edges","vt_coverage","vt_entropy","connectome_entropy","b1_z","sie_total_reward","sie_v2_reward_mean"]
    Xraw = df1k[metrics_for_delta].astype(float).values
    Xz = safe_zscore(Xraw)
    delta = np.vstack([np.zeros(Xz.shape[1]), np.diff(Xz, axis=0)])
    df1k["reconfig_score"] = np.linalg.norm(delta, axis=1)
    thr = np.quantile(df1k["reconfig_score"], 0.99)
    df1k["reconfig_spike"] = (df1k["reconfig_score"] >= thr).astype(int)
    df1k["b1_spike"] = (df1k["b1_z"] >= 3.0).astype(int)

    # ---- Motor gate model ----
    features_gate = ["b1_z","vt_coverage","active_edges","connectome_entropy","has_input","recent_input_any_W50","phase"]
    X = df1k[features_gate].astype(float).values
    y = df1k["did_say"].astype(int).values
    split = int(len(df1k) * 0.7)

    gate = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", solver="liblinear")),
    ])
    gate.fit(X[:split], y[:split])
    p_test = gate.predict_proba(X[split:])[:, 1]
    auc = roc_auc_score(y[split:], p_test)
    ap_score = average_precision_score(y[split:], p_test)

    coef = gate.named_steps["clf"].coef_[0]
    spec = pd.DataFrame({
        "feature": features_gate,
        "coef_std": coef,
        "abs_coef": np.abs(coef),
        "auc_univariate": [roc_auc_score(y, df1k[f]) for f in features_gate],
    }).sort_values("abs_coef", ascending=False)
    spec.to_csv(out_dir / "tables" / "decoder_readout_spec.csv", index=False)
    pd.DataFrame([{"auc_test": auc, "avg_precision_test": ap_score, "features": ",".join(features_gate)}]).to_csv(
        out_dir / "tables" / "motor_gate_model_performance.csv", index=False
    )

    # PR curve
    prec, rec, _ = precision_recall_curve(y[split:], p_test)
    plt.figure(figsize=(5.2, 4.2))
    plt.plot(rec, prec)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Motor gate model PR curve (time split test)")
    plt.tight_layout()
    plt.savefig(out_dir / "figures" / "motor_gate_pr_curve.png", dpi=200)
    plt.close()

    # Coeff bar
    spec2 = spec.sort_values("abs_coef", ascending=True)
    plt.figure(figsize=(8, 4.5))
    plt.barh(spec2["feature"], spec2["coef_std"])
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Motor gate model: standardized logistic coefficients")
    plt.tight_layout()
    plt.savefig(out_dir / "figures" / "motor_gate_logit_coefficients.png", dpi=200)
    plt.close()

    # ---- Macrostate model (metastable) ----
    internal_features = ['active_edges','vt_coverage','vt_entropy','connectome_entropy',
                         'cohesion_components','b1_z','adc_territories',
                         'sie_total_reward','sie_v2_reward_mean','sie_valence_01','sie_v2_valence_01']
    Xint = df1k[internal_features].astype(float).values
    Xint_z = safe_zscore(Xint)
    pca = PCA(n_components=6, random_state=0)
    Xp = pca.fit_transform(Xint_z)

    K_micro = 60
    km_micro = MiniBatchKMeans(n_clusters=K_micro, random_state=0, batch_size=2048, n_init=10)
    micro = km_micro.fit_predict(Xp[:, :5])

    C = np.zeros((K_micro, K_micro), dtype=np.int64)
    for a, b in zip(micro[:-1], micro[1:]):
        C[a, b] += 1
    row = C.sum(axis=1, keepdims=True)
    P = np.divide(C, row, out=np.zeros_like(C, dtype=float), where=row != 0)
    eigvals = np.linalg.eigvals(P.T)
    eigvals = np.sort(np.real(eigvals))[::-1]
    eig_df = pd.DataFrame({"rank": np.arange(1, 16), "eigval": eigvals[:15]})
    eig_df.to_csv(out_dir / "tables" / "microstate_eigenspectrum_top15.csv", index=False)

    # choose k_macro=4 (spectral gap)
    eigvals_full, eigvecs = np.linalg.eig(P.T)
    idx_sort = np.argsort(np.real(eigvals_full))[::-1]
    eigvecs_sorted = np.real(eigvecs[:, idx_sort])
    k_macro = 4
    V = eigvecs_sorted[:, 1:k_macro]
    km_macro = MiniBatchKMeans(n_clusters=k_macro, random_state=0, batch_size=256, n_init=10)
    macro_labels_micro = km_macro.fit_predict(V)
    macro = macro_labels_micro[micro]
    df1k["microstate"] = micro
    df1k["macrostate"] = macro

    # segments + transitions
    t_series = df1k["t"].values
    segs = []
    start_idx = 0
    for i in range(1, len(macro)):
        if macro[i] != macro[i-1]:
            segs.append({"macro": int(macro[i-1]), "t_start": int(t_series[start_idx]), "t_end": int(t_series[i-1]),
                         "idx_start": start_idx, "idx_end": i-1, "duration_ticks": i-start_idx})
            start_idx = i
    segs.append({"macro": int(macro[-1]), "t_start": int(t_series[start_idx]), "t_end": int(t_series[-1]),
                 "idx_start": start_idx, "idx_end": len(macro)-1, "duration_ticks": len(macro)-start_idx})
    seg_df = pd.DataFrame(segs)
    seg_df.to_csv(out_dir / "tables" / "macrostate_segments_k4.csv", index=False)

    trans_idxs = np.where(macro[1:] != macro[:-1])[0] + 1
    trans = pd.DataFrame({
        "idx": trans_idxs.astype(int),
        "t": t_series[trans_idxs].astype(int),
        "from_macro": macro[trans_idxs-1].astype(int),
        "to_macro": macro[trans_idxs].astype(int),
        "did_say": df1k["did_say"].values[trans_idxs].astype(int),
        "b1_spike": df1k["b1_spike"].values[trans_idxs].astype(int),
        "reconfig_spike": df1k["reconfig_spike"].values[trans_idxs].astype(int),
        "has_input": df1k["has_input"].values[trans_idxs].astype(int),
    })
    trans.to_csv(out_dir / "tables" / "macrostate_transitions_k4.csv", index=False)

    # Dwell CCDF + power-law fit
    durs = seg_df["duration_ticks"].values
    xmin = 200
    alpha, ks, n_tail = powerlaw_mle_continuous(durs, xmin)
    pd.DataFrame([{"xmin": xmin, "alpha": alpha, "ks": ks, "n_tail": n_tail}]).to_csv(
        out_dir / "tables" / "macrostate_dwell_powerlaw_fit.csv", index=False
    )

    durs_sorted = np.sort(durs)
    ccdf = 1 - np.arange(1, len(durs_sorted) + 1) / len(durs_sorted)
    plt.figure(figsize=(6.0, 4.5))
    plt.loglog(durs_sorted, ccdf, marker=".", linestyle="none")
    xfit = np.array([xmin, durs_sorted.max()])
    ccdf_fit = (xfit / xmin) ** (1 - alpha) if not math.isnan(alpha) else np.array([np.nan, np.nan])
    plt.loglog(xfit, ccdf_fit, linestyle="-")
    plt.xlabel("Dwell duration (ticks)")
    plt.ylabel("CCDF P(T>=t)")
    plt.title(f"Macrostate dwell times CCDF (xmin={xmin}, alpha≈{alpha:.2f})")
    plt.tight_layout()
    plt.savefig(out_dir / "figures" / "macrostate_dwell_ccdf_powerlaw.png", dpi=200)
    plt.close()

    # Event-triggered averages around transitions
    W = 200
    eta = {"dt": np.arange(-W, W + 1)}
    for col in ["b1_z","reconfig_score","did_say","has_input","active_edges","connectome_entropy"]:
        m, nv = event_triggered_average(df1k[col].astype(float).values, trans_idxs, W)
        eta[col] = m
    eta_df = pd.DataFrame(eta)
    eta_df.to_csv(out_dir / "tables" / "event_triggered_means_around_macro_transitions.csv", index=False)

    # ---- Goal-drive atlas (windowed TE) ----
    win = 5000
    step = 1000
    rows = []
    for start in range(0, len(df1k) - win + 1, step):
        end = start + win
        sub = df1k.iloc[start:end]
        te_r = transfer_entropy_discrete(sub["sie_v2_reward_mean"].values, sub["vt_coverage"].values, lag=1, n_bins=8)
        te_e = transfer_entropy_discrete(sub["connectome_entropy"].values, sub["vt_coverage"].values, lag=1, n_bins=8)
        rows.append({
            "t_start": int(sub["t"].iloc[0]),
            "t_end": int(sub["t"].iloc[-1]),
            "say_rate": float(sub["did_say"].mean()),
            "input_rate": float(sub["has_input"].mean()),
            "macro_mode": int(pd.Series(sub["macrostate"]).mode().iloc[0]),
            "te_rewardmean_to_cov": te_r,
            "te_entropy_to_cov": te_e,
            "goal_drive_cov": te_r - te_e,
        })
    atlas = pd.DataFrame(rows).sort_values("goal_drive_cov", ascending=False)
    atlas.to_csv(out_dir / "tables" / "goal_drive_atlas_ranked.csv", index=False)

    # ---- Input -> internal coupling (ΔR²) using TF-IDF SVD topics ----
    docs = df1k["input_text_concat"].fillna("").astype(str).apply(lambda s: s[:2000])
    tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
    X_tfidf = tfidf.fit_transform(docs)
    svd = TruncatedSVD(n_components=12, random_state=0)
    X_text = svd.fit_transform(X_tfidf)

    PC = Xp[:, :3]

    def delta_r2_for_h(h):
        X_base = PC[:-h]
        X_plus = np.hstack([PC[:-h], X_text[:-h]])
        Y = PC[h:]
        n = len(Y)
        split2 = int(n * 0.7)
        out = []
        for k in range(Y.shape[1]):
            yk = Y[:, k]
            mb = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X_base[:split2], yk[:split2])
            mp = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X_plus[:split2], yk[:split2])
            r2b = r2_score(yk[split2:], mb.predict(X_base[split2:]))
            r2p = r2_score(yk[split2:], mp.predict(X_plus[split2:]))
            out.append({"horizon": h, "pc": k + 1, "r2_base": r2b, "r2_plus": r2p, "delta_r2": r2p - r2b})
        return out

    coupling_rows = []
    for h in [1,2,5,10,20,50]:
        coupling_rows.extend(delta_r2_for_h(h))
    coupling = pd.DataFrame(coupling_rows)
    coupling.to_csv(out_dir / "tables" / "coupling_input_to_internal_deltaR2.csv", index=False)

    # ---- Internal -> output gating: adding text should not help much ----
    gate_int_features = ["b1_z","active_edges","vt_coverage","connectome_entropy","vt_entropy","phase","sie_v2_reward_mean","sie_v2_valence_01"]
    X_int = df1k[gate_int_features].astype(float).values
    X_int_text = np.hstack([X_int, X_text])
    y = df1k["did_say"].values
    split3 = int(len(y) * 0.7)

    def fit_auc(Xmat):
        model = Pipeline([("scaler", StandardScaler()),
                          ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", solver="liblinear"))])
        model.fit(Xmat[:split3], y[:split3])
        p = model.predict_proba(Xmat[split3:])[:, 1]
        return roc_auc_score(y[split3:], p), average_precision_score(y[split3:], p)

    auc_int, ap_int = fit_auc(X_int)
    auc_int_text, ap_int_text = fit_auc(X_int_text)
    pd.DataFrame([
        {"model": "internal_only", "auc": auc_int, "avg_precision": ap_int, "n_features": X_int.shape[1]},
        {"model": "internal_plus_text", "auc": auc_int_text, "avg_precision": ap_int_text, "n_features": X_int_text.shape[1]},
    ]).to_csv(out_dir / "tables" / "coupling_internal_to_output_gate.csv", index=False)

    # ---- Consciousness-adjacent window metrics + ranking ----
    # Integration: Gaussian total correlation on correlation matrix
    Xch = df1k[internal_features].astype(float).values
    Xch_z = safe_zscore(Xch)
    pc1 = Xp[:, 0]
    pc2 = Xp[:, 1]

    def window_stats(start, end):
        sub = Xch_z[start:end]
        R = np.corrcoef(sub, rowvar=False)
        R = np.nan_to_num(R, nan=0.0)
        sign, logdet = np.linalg.slogdet(R + 1e-6*np.eye(R.shape[0]))
        tc = float(-0.5*logdet) if sign > 0 else float("nan")
        eigv = np.linalg.eigvalsh(R)
        eigv = np.clip(eigv, 1e-8, None)
        pr = float((eigv.sum()**2)/np.sum(eigv**2))
        w_pc1 = pc1[start:end]
        corr20 = float(np.corrcoef(w_pc1[:-20], w_pc1[20:])[0,1]) if len(w_pc1) > 21 else float("nan")
        # endogeneity proxy: delta R² from adding has_input and one text comp to AR(1) for delta pc2
        idx = np.arange(start, end-1)
        y = pc2[idx+1] - pc2[idx]
        Xb = pc2[idx].reshape(-1, 1)
        Xx = np.column_stack([pc2[idx], df1k["has_input"].values[idx], X_text[idx, 0]])
        splitw = int(len(y)*0.7)
        rb = Ridge(alpha=1.0).fit(Xb[:splitw], y[:splitw])
        rx = Ridge(alpha=1.0).fit(Xx[:splitw], y[:splitw])
        r2b = r2_score(y[splitw:], rb.predict(Xb[splitw:])) if len(y)-splitw > 10 else float("nan")
        r2x = r2_score(y[splitw:], rx.predict(Xx[splitw:])) if len(y)-splitw > 10 else float("nan")
        endog = float(-(r2x - r2b)) if (not math.isnan(r2b) and not math.isnan(r2x)) else float("nan")
        say_rate = float(df1k["did_say"].iloc[start:end].mean())
        input_rate = float(df1k["has_input"].iloc[start:end].mean())
        return tc, pr, corr20, endog, say_rate, input_rate, R

    win = 2000
    step = 500
    rows = []
    prev_R = None
    for start in range(0, len(df1k) - win + 1, step):
        end = start + win
        tc, pr, corr20, endog, say_rate, input_rate, R = window_stats(start, end)
        if prev_R is None:
            turnover = float("nan")
        else:
            triu = np.triu_indices_from(R, k=1)
            v1 = prev_R[triu]; v2 = R[triu]
            sim = float(np.corrcoef(v1, v2)[0,1]) if np.std(v1) and np.std(v2) else float("nan")
            turnover = 1 - sim if not math.isnan(sim) else float("nan")
        prev_R = R
        rows.append({"t_start": int(df1k["t"].iloc[start]), "t_end": int(df1k["t"].iloc[end-1]),
                     "tc_integration": tc, "pr_differentiation": pr, "pc1_corr20": corr20,
                     "endogeneity_index": endog, "say_rate": say_rate, "input_rate": input_rate,
                     "backbone_turnover": turnover})
    wm = pd.DataFrame(rows)
    # z-score composite
    def z(s):
        s = s.astype(float)
        m = np.nanmean(s); sd = np.nanstd(s)
        sd = sd if sd else 1.0
        return (s - m) / sd
    wm["turnover_filled"] = wm["backbone_turnover"].fillna(wm["backbone_turnover"].median())
    wm["coherence_score"] = z(wm["tc_integration"]) + z(wm["pr_differentiation"]) + z(wm["pc1_corr20"]) + z(wm["endogeneity_index"]) \
                            - z(wm["turnover_filled"]) - 0.5*z(wm["say_rate"]) - 0.5*z(wm["input_rate"])
    wm.to_csv(out_dir / "tables" / "consciousness_proxy_window_metrics.csv", index=False)
    wm.sort_values("coherence_score", ascending=False).head(20).to_csv(out_dir / "tables" / "candidate_coherent_episodes_top20.csv", index=False)

    plt.figure(figsize=(9.5, 4.2))
    plt.plot(wm["t_start"], wm["coherence_score"], marker="o", linewidth=0.8)
    plt.xlabel("t_start (window)")
    plt.ylabel("Coherence score (composite)")
    plt.title("Consciousness-adjacent composite score over time")
    plt.tight_layout()
    plt.savefig(out_dir / "figures" / "coherence_score_over_time.png", dpi=200)
    plt.close()

    # ---- Scaling dashboard across neuron counts in this file ----
    # (Keep it simple; avoid expensive clustering on huge runs)
    runs = []
    for n in sorted(tick_df["neurons"].unique()):
        sub = tick_df[tick_df["neurons"] == n].sort_values("t").reset_index(drop=True)
        X = sub[internal_features].astype(float).values
        sd = X.std(axis=0); keep = sd > 0
        Xz = safe_zscore(X[:, keep])
        R = np.corrcoef(Xz, rowvar=False)
        R = np.nan_to_num(R, nan=0.0)
        sign, logdet = np.linalg.slogdet(R + 1e-6*np.eye(R.shape[0]))
        tc = float(-0.5*logdet) if sign > 0 else float("nan")
        eigv = np.linalg.eigvalsh(R)
        eigv = np.clip(eigv, 1e-8, None)
        pr = float((eigv.sum()**2)/np.sum(eigv**2))
        te_r = transfer_entropy_discrete(sub["sie_v2_reward_mean"].values, sub["vt_coverage"].values, lag=1, n_bins=6) if len(sub) > 200 else float("nan")
        te_e = transfer_entropy_discrete(sub["connectome_entropy"].values, sub["vt_coverage"].values, lag=1, n_bins=6) if len(sub) > 200 else float("nan")
        runs.append({
            "neurons": int(n),
            "ticks": int(len(sub)),
            "t_start": int(sub["t"].min()),
            "t_end": int(sub["t"].max()),
            "say_rate": float(sub["did_say"].mean()),
            "input_rate": float((sub["ute_text_count"]>0).mean()),
            "b1_spike_rate": float((sub["b1_z"]>=3).mean()),
            "tc_integration": tc,
            "pr_differentiation": pr,
            "goal_drive_cov": float(te_r - te_e) if (not math.isnan(te_r) and not math.isnan(te_e)) else float("nan"),
        })
    scale = pd.DataFrame(runs)
    scale.to_csv(out_dir / "tables" / "scaling_risk_dashboard.csv", index=False)

    # ---- Hash index ----
    rows = []
    for path in sorted(out_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(out_dir)
            rows.append({"path": str(rel), "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    pd.DataFrame(rows).to_csv(out_dir / "SHA256SUMS.csv", index=False)

    # Short summary log
    with open(out_dir / "logs" / "analysis_summary.txt", "w") as f:
        f.write(f"1k ticks: {len(df1k)}  say ticks: {int(df1k['did_say'].sum())}  say_rate: {df1k['did_say'].mean():.6f}\n")
        f.write(f"Motor gate AUC (test): {auc:.4f}  AP: {ap_score:.4f}\n")
        f.write(f"Macro transitions: {len(trans_idxs)}  dwell tail alpha(xmin=200): {alpha:.2f}\n")
        f.write("\nDecoder readout spec:\n")
        f.write(spec.to_string(index=False))
        f.write("\n\nScaling dashboard:\n")
        f.write(scale.to_string(index=False))

    print("DONE. Outputs:", out_dir)


if __name__ == "__main__":
    main()
