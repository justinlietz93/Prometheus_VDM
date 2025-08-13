"""
Plotting helper for memory-steering experiments.

- Parses outputs/memory_steering_results.csv (supports 4- or 5-column stability).
- Produces figures in outputs/.
- Prints a concise metrics summary that directly tests the three predictions:
  1) Junction logistic collapse
  2) Curvature scaling in the ray limit
  3) Stability band with write→decay protocol (Retention, Fidelity)

Usage:
- python3 -m fum_rt.utils.plot_memory_steering
  or
- python3 fum_rt/utils/plot_memory_steering.py   (if PYTHONPATH=. is set)
"""

import os
import math
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_results(src: str):
    lines = open(src, "r").read().splitlines()
    mode = 0
    Jx, Jp = [], []
    Cx, Cy = [], []
    # Extended stability rows: up to 10 columns:
    # (Da, Lam, Gam, Ret, Fid_w, Fid_end, Fid_shuffle_end, Fid_edge_end, AUC_end, SNR_end)
    SB = []
    # Signed curvature aggregates
    Sx, Smy, Sse, Sseed, Ssign = [], [], [], [], []
    for ln in lines:
        if ln.startswith("# Junction logistic"):
            mode = 1
            continue
        if ln.startswith("# Curvature scaling signed"):
            mode = 22
            continue
        if ln.startswith("# Curvature scaling"):
            mode = 2
            continue
        if ln.startswith("# Stability band"):
            mode = 3
            continue
        if not ln.strip() or ln.strip().startswith("#"):
            continue
        parts = [p.strip() for p in ln.split(",")]
        try:
            if mode == 1 and len(parts) >= 2:
                Jx.append(float(parts[0]))
                Jp.append(float(parts[1]))
            elif mode == 2 and len(parts) >= 2:
                Cx.append(float(parts[0]))
                Cy.append(float(parts[1]))
            elif mode == 22 and len(parts) >= 4:
                Sx.append(float(parts[0]))
                Smy.append(float(parts[1]))
                Sse.append(float(parts[2]))
                seed = float(parts[3]) if len(parts) >= 4 else float("nan")
                sign = float(parts[4]) if len(parts) >= 5 else float("nan")
                Sseed.append(seed)
                Ssign.append(sign)
            elif mode == 3:
                # Support 4..10 columns; pad with NaN
                vals = []
                for p in parts[:10]:
                    try:
                        vals.append(float(p))
                    except Exception:
                        vals.append(float("nan"))
                while len(vals) < 10:
                    vals.append(float("nan"))
                SB.append(tuple(vals[:10]))
        except Exception:
            # Skip malformed lines
            pass
    Jx = np.asarray(Jx, float)
    Jp = np.asarray(Jp, float)
    Cx = np.asarray(Cx, float)
    Cy = np.asarray(Cy, float)
    SB = np.asarray(SB, float) if len(SB) > 0 else np.zeros((0, 10), float)
    Sx = np.asarray(Sx, float)
    Smy = np.asarray(Smy, float)
    Sse = np.asarray(Sse, float)
    Sseed = np.asarray(Sseed, float)
    Ssign = np.asarray(Ssign, float)
    return Jx, Jp, Cx, Cy, SB, Sx, Smy, Sse, Sseed, Ssign


def fit_logistic(x: np.ndarray, p: np.ndarray):
    valid = (p > 0) & (p < 1) & np.isfinite(x) & np.isfinite(p)
    if valid.sum() < 2:
        return np.nan, np.nan, np.nan, None, None
    xv = x[valid]
    pv = p[valid]
    logit = np.log(pv / (1.0 - pv))
    X = np.vstack([xv, np.ones_like(xv)]).T
    k, b = np.linalg.lstsq(X, logit, rcond=None)[0]
    xgrid = np.linspace(np.nanmin(x), np.nanmax(x), 400)
    pred = 1.0 / (1.0 + np.exp(-(k * xgrid + b)))
    p_pred = 1.0 / (1.0 + np.exp(-(k * x + b)))
    p_mean = np.nanmean(p) if p.size else np.nan
    ss_res = np.nansum((p - p_pred) ** 2)
    ss_tot = np.nansum((p - p_mean) ** 2)
    R2 = 1.0 - (ss_res / ss_tot) if (ss_tot > 0) else np.nan
    return float(k), float(b), float(R2), xgrid, pred


def fit_linear(x: np.ndarray, y: np.ndarray):
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 2:
        return np.nan, np.nan, np.nan, np.nan
    A = np.vstack([x[mask], np.ones(mask.sum())]).T
    a, c = np.linalg.lstsq(A, y[mask], rcond=None)[0]
    y_pred = a * x + c
    y_mean = np.nanmean(y)
    ss_res = np.nansum((y - y_pred) ** 2)
    ss_tot = np.nansum((y - y_mean) ** 2)
    R2 = 1.0 - (ss_res / ss_tot) if (ss_tot > 0) else np.nan
    xm = np.nanmean(x)
    ym = np.nanmean(y)
    rden = math.sqrt(np.nansum((x - xm) ** 2) * np.nansum((y - ym) ** 2))
    r = np.nan if (rden == 0) else float(np.nansum((x - xm) * (y - ym)) / rden)
    return float(a), float(c), float(R2), r


def pivot_heatmap(SB: np.ndarray, value_index: int = 3):
    # value_index:
    #   3 = Retention
    #   5 = Fidelity_end
    #   6 = Fidelity_shuffle_end
    if SB.size == 0:
        return None
    Da = SB[:, 0]
    Lam = SB[:, 1]
    Val = SB[:, value_index]
    uDa = np.unique(Da)
    uLam = np.unique(Lam)
    H = np.full((uLam.size, uDa.size), np.nan, float)
    for i, lam in enumerate(uLam):
        for j, da in enumerate(uDa):
            mask = (Lam == lam) & (Da == da)
            if np.any(mask):
                H[i, j] = np.nanmean(Val[mask])
    extent = [uDa.min(), uDa.max(), uLam.min(), uLam.max()]
    return H, uDa, uLam, extent


def plot_all(src: str = os.path.join("outputs", "memory_steering_results.csv"),
             outdir: str = "outputs"):
    if not os.path.exists(src):
        raise SystemExit(f"[error] Missing {src}. Generate it first with: python3 -m fum_rt.utils.memory_steering_experiments > {src}")
    os.makedirs(outdir, exist_ok=True)

    Jx, Jp, Cx, Cy, SB, Sx, Smy, Sse, Sseed, Ssign = parse_results(src)

    # ---------- Plot 1: Junction logistic ----------
    k, b, R2_log, xgrid, pred = fit_logistic(Jx, Jp)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.scatter(Jx, Jp, s=24, color="#1f77b4", label="data")
    if xgrid is not None:
        ax1.plot(xgrid, pred, color="#d62728", lw=2,
                 label=f"fit: k={k:.3f}, b={b:.3f}, R2={R2_log:.3f}")
    ax1.set_xlabel("Theta * Delta m")
    ax1.set_ylabel("P(A)")
    ax1.set_title("Junction logistic collapse")
    ax1.legend(loc="lower right")
    fig1.tight_layout()
    p1 = os.path.join(outdir, "junction_logistic.png")
    fig1.savefig(p1, dpi=160)

    # ---------- Plot 2: Curvature scaling ----------
    a, c, R2_lin, pearson = fit_linear(Cx, Cy)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.scatter(Cx, Cy, s=18, color="#2ca02c", alpha=0.8, label="data")
    if np.isfinite(a):
        xline = np.linspace(np.nanmin(Cx), np.nanmax(Cx), 100) if Cx.size else np.array([0, 1])
        ax2.plot(xline, a * xline + c, color="#9467bd", lw=2,
                 label=f"fit: a={a:.3f}, c={c:.3f}\nR2={R2_lin:.3f}, r={pearson:.3f}")
    ax2.set_xlabel("Theta * |grad m|")
    ax2.set_ylabel("mean(kappa_path)")
    ax2.set_title("Curvature scaling")
    ax2.legend(loc="upper left")
    fig2.tight_layout()
    p2 = os.path.join(outdir, "curvature_scaling.png")
    fig2.savefig(p2, dpi=160)

    # ---------- Plot 2b: Curvature scaling (signed) ----------
    p_signed = os.path.join(outdir, "curvature_scaling_signed.png")
    if Sx.size > 0:
        fig2b, ax2b = plt.subplots(figsize=(6, 4))
        sign_labels = {0: "baseline", 1: "flip_grad", 2: "flip_theta"}
        colors = {0: "#1f77b4", 1: "#ff7f0e", 2: "#2ca02c"}
        valid_signs = np.unique(Ssign[np.isfinite(Ssign)]).astype(int) if np.any(np.isfinite(Ssign)) else []
        for sid in sorted(valid_signs.tolist()):
            mask = (Ssign == sid)
            if not np.any(mask):
                continue
            ax2b.errorbar(Sx[mask], Smy[mask], yerr=Sse[mask], fmt="o", ms=4,
                          color=colors.get(sid, "#7f7f7f"),
                          label=sign_labels.get(sid, f"sign={sid}"), alpha=0.9)
        ax2b.set_xlabel("X = Theta * |grad m|")
        ax2b.set_ylabel("mean(kappa_path)")
        ax2b.set_title("Curvature scaling (signed invariance)")
        ax2b.legend(loc="upper left", fontsize=8)
        fig2b.tight_layout()
        fig2b.savefig(p_signed, dpi=160)
    else:
        # No signed data present; do not create a figure
        pass

    # ---------- Plot 3: Stability band heatmaps ----------
    fig3, ax3 = plt.subplots(1, 2, figsize=(11, 4))
    if SB.size > 0:
        Hret = pivot_heatmap(SB, 3)
        Hfid = pivot_heatmap(SB, 5)  # Fidelity_end
        if Hret is not None:
            H, uDa, uLam, extent = Hret
            im = ax3[0].imshow(H, origin="lower", aspect="auto", extent=extent, cmap="viridis")
            ax3[0].set_xlabel("D_a")
            ax3[0].set_ylabel("Lambda")
            ax3[0].set_title("Retention (avg over Gamma)")
            cbar = fig3.colorbar(im, ax=ax3[0])
            cbar.set_label("Retention")
        if Hfid is not None:
            Hf, uDa, uLam, extent = Hfid
            im2 = ax3[1].imshow(Hf, origin="lower", aspect="auto", extent=extent, cmap="magma")
            ax3[1].set_xlabel("D_a")
            ax3[1].set_ylabel("Lambda")
            ax3[1].set_title("Fidelity_end (avg over Gamma)")
            cbar2 = fig3.colorbar(im2, ax=ax3[1])
            cbar2.set_label("Fidelity_end")
    else:
        ax3[0].text(0.5, 0.5, "No stability data", ha="center", va="center")
        ax3[1].axis("off")
    fig3.tight_layout()
    p3 = os.path.join(outdir, "stability_band.png")
    fig3.savefig(p3, dpi=160)

    # ---------- Plot 3b: Stability band heatmaps per Gamma (slices) ----------
    p3_ret_by_gamma = p3_fid_by_gamma = p3_auc_by_gamma = p3_snr_by_gamma = None
    if SB.size > 0:
        def _slice_by_gamma(value_index: int, label: str, cmap: str, out_name: str):
            Da = SB[:, 0]; Lam = SB[:, 1]; Gam = SB[:, 2]; Val = SB[:, value_index]
            mask = np.isfinite(Da) & np.isfinite(Lam) & np.isfinite(Gam) & np.isfinite(Val)
            if not np.any(mask):
                return None
            Da = Da[mask]; Lam = Lam[mask]; Gam = Gam[mask]; Val = Val[mask]
            uDa = np.unique(Da); uLam = np.unique(Lam); uGam = np.unique(Gam)

            # Build per-Gamma heatmaps and collect global color limits for consistent scaling
            Hs = {}
            vmin, vmax = float("inf"), float("-inf")
            for g in uGam:
                m = (Gam == g)
                H = np.full((uLam.size, uDa.size), np.nan, float)
                for i, lam in enumerate(uLam):
                    for j, da in enumerate(uDa):
                        mm = m & (Lam == lam) & (Da == da)
                        if np.any(mm):
                            v = float(np.nanmean(Val[mm]))
                            H[i, j] = v
                Hs[float(g)] = H
                finite_vals = H[np.isfinite(H)]
                if finite_vals.size > 0:
                    vmin = min(vmin, float(np.nanmin(finite_vals)))
                    vmax = max(vmax, float(np.nanmax(finite_vals)))
            if not np.isfinite(vmin) or not np.isfinite(vmax):
                vmin = vmax = None

            # Layout panels
            nGam = uGam.size
            ncol = int(np.ceil(np.sqrt(nGam)))
            nrow = int(np.ceil(nGam / ncol))
            fig_g, axes_g = plt.subplots(nrow, ncol, figsize=(4.0 * ncol, 3.2 * nrow))
            axes_g = np.atleast_2d(axes_g).reshape(-1)
            im_last = None
            extent = [uDa.min(), uDa.max(), uLam.min(), uLam.max()]
            for k, g in enumerate(uGam):
                axg = axes_g[k]
                H = Hs[float(g)]
                im = axg.imshow(H, origin="lower", aspect="auto", extent=extent, cmap=cmap, vmin=vmin, vmax=vmax)
                axg.set_title(f"Gamma={g:.3f}")
                axg.set_xlabel("D_a")
                axg.set_ylabel("Lambda")
                im_last = im
            for k in range(uGam.size, len(axes_g)):
                axes_g[k].axis("off")
            fig_g.tight_layout(rect=[0, 0, 0.92, 1])
            if im_last is not None:
                cbar = fig_g.colorbar(im_last, ax=axes_g[:nGam].tolist(), fraction=0.02, pad=0.02)
                cbar.set_label(label)
            path = os.path.join(outdir, out_name)
            fig_g.savefig(path, dpi=160)
            return path

        # Generate per-Gamma panels for key metrics
        p3_ret_by_gamma = _slice_by_gamma(3, "Retention", "viridis", "stability_retention_by_gamma.png")
        p3_fid_by_gamma = _slice_by_gamma(5, "Fidelity_end", "magma", "stability_fidelity_by_gamma.png")
        if SB.shape[1] > 8:
            tmp = _slice_by_gamma(8, "AUC_end", "plasma", "stability_auc_by_gamma.png")
            if tmp:
                p3_auc_by_gamma = tmp
        if SB.shape[1] > 9:
            tmp = _slice_by_gamma(9, "SNR_end", "cividis", "stability_snr_by_gamma.png")
            if tmp:
                p3_snr_by_gamma = tmp

    # ---------- Combined summary panel ----------
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    # Panel A (logistic)
    axes[0].scatter(Jx, Jp, s=20, color="#1f77b4")
    if xgrid is not None:
        axes[0].plot(xgrid, pred, color="#d62728", lw=2)
    axes[0].set_xlabel("Theta * Delta m")
    axes[0].set_ylabel("P(A)")
    axes[0].set_title(f"Junction (R2={R2_log:.3f})")
    # Panel B (curvature)
    axes[1].scatter(Cx, Cy, s=16, color="#2ca02c", alpha=0.8)
    if np.isfinite(a):
        xline = np.linspace(np.nanmin(Cx), np.nanmax(Cx), 100) if Cx.size else np.array([0, 1])
        axes[1].plot(xline, a * xline + c, color="#9467bd", lw=2)
    axes[1].set_xlabel("Theta * |grad m|")
    axes[1].set_ylabel("mean(kappa_path)")
    axes[1].set_title(f"Curvature (R2={R2_lin:.3f}, r={pearson:.3f})")
    # Panel C (stability: retention heatmap)
    if SB.size > 0:
        Hret = pivot_heatmap(SB, 3)
        if Hret is not None:
            H, uDa, uLam, extent = Hret
            axes[2].imshow(H, origin="lower", aspect="auto", extent=extent, cmap="viridis")
            axes[2].set_xlabel("D_a")
            axes[2].set_ylabel("Lambda")
            axes[2].set_title("Retention (avg Γ)")
    else:
        axes[2].text(0.5, 0.5, "No stability data", ha="center", va="center")
    fig.tight_layout()
    p4 = os.path.join(outdir, "memory_steering_summary.png")
    fig.savefig(p4, dpi=160)

    # ---------- Metrics summary (text) ----------
    print("=== METRICS SUMMARY ===")
    if np.isfinite(k):
        print(f"[JUNCTION] k={k:.3f}, b={b:.3f}, R2={R2_log:.3f}")
    else:
        print("[JUNCTION] insufficient data")

    if np.isfinite(a):
        print(f"[CURVATURE] a={a:.3f}, c={c:.3f}, R2={R2_lin:.3f}, r={pearson:.3f}")
    else:
        print("[CURVATURE] insufficient data")

    # Signed curvature invariance summary
    if 'Sx' in locals() and np.size(Sx) > 0:
        passes_grad, total_grad = 0, 0
        passes_theta, total_theta = 0, 0
        tol = 1e-9

        def _get_mu_se(sign_id, xval):
            m = (Ssign == sign_id)
            if not np.any(m):
                return None, None
            m = m & np.isfinite(Sx) & np.isfinite(Smy) & np.isfinite(Sse) & np.isclose(Sx, xval, atol=tol, rtol=0.0)
            if not np.any(m):
                return None, None
            idx = np.where(m)[0][0]
            return float(Smy[idx]), float(Sse[idx])

        for x0 in np.unique(Sx[Ssign == 0]):
            mu0, se0 = _get_mu_se(0, x0)
            if mu0 is None:
                continue
            mu1, se1 = _get_mu_se(1, x0)
            if mu1 is not None:
                z = abs(mu1 - mu0) / max(1e-12, math.sqrt(se1 * se1 + se0 * se0))
                total_grad += 1
                if z <= 2.0:
                    passes_grad += 1
            mu2, se2 = _get_mu_se(2, x0)
            if mu2 is not None:
                z = abs(mu2 - mu0) / max(1e-12, math.sqrt(se2 * se2 + se0 * se0))
                total_theta += 1
                if z <= 2.0:
                    passes_theta += 1
        rate_g = (passes_grad / total_grad) if total_grad > 0 else float("nan")
        rate_t = (passes_theta / total_theta) if total_theta > 0 else float("nan")
        print(f"[CURVATURE|signed] invariance pass (|Δ| ≤ 2σ): flip_grad={rate_g:.2%} over {total_grad} pairs, "
              f"flip_theta={rate_t:.2%} over {total_theta} pairs")
    else:
        print("[CURVATURE|signed] no signed data")

    if SB.size > 0:
        Da = SB[:, 0]; Lam = SB[:, 1]; Gam = SB[:, 2]
        Ret = SB[:, 3]
        Fid_w = SB[:, 4] if SB.shape[1] > 4 else np.full_like(Ret, np.nan)
        Fid_e = SB[:, 5] if SB.shape[1] > 5 else np.full_like(Ret, np.nan)
        Fid_shuf = SB[:, 6] if SB.shape[1] > 6 else np.full_like(Ret, np.nan)
        Fid_edge = SB[:, 7] if SB.shape[1] > 7 else np.full_like(Ret, np.nan)
        AUC_e = SB[:, 8] if SB.shape[1] > 8 else np.full_like(Ret, np.nan)
        SNR_e = SB[:, 9] if SB.shape[1] > 9 else np.full_like(Ret, np.nan)

        robust = Da >= Lam
        mean_ret_rob = float(np.nanmean(Ret[robust])) if robust.any() else float("nan")
        mean_ret_non = float(np.nanmean(Ret[~robust])) if (~robust).any() else float("nan")
        mean_fid_e_rob = float(np.nanmean(Fid_e[robust])) if robust.any() else float("nan")
        mean_fid_e_non = float(np.nanmean(Fid_e[~robust])) if (~robust).any() else float("nan")
        mean_fid_shuf = float(np.nanmean(np.abs(Fid_shuf))) if np.any(np.isfinite(Fid_shuf)) else float("nan")
        mean_auc_rob = float(np.nanmean(AUC_e[robust])) if robust.any() else float("nan")
        mean_auc_non = float(np.nanmean(AUC_e[~robust])) if (~robust).any() else float("nan")
        mean_snr_rob = float(np.nanmean(SNR_e[robust])) if robust.any() else float("nan")
        mean_snr_non = float(np.nanmean(SNR_e[~robust])) if (~robust).any() else float("nan")

        print(f"[STABILITY] Retention mean: robust={mean_ret_rob:.3f}, non={mean_ret_non:.3f}")
        print(f"[STABILITY] Fidelity_end mean: robust={mean_fid_e_rob:.3f}, non={mean_fid_e_non:.3f}")
        print(f"[STABILITY] Fidelity_shuffle_end |mean|: {mean_fid_shuf:.3f}")
        if np.any(np.isfinite(AUC_e)):
            print(f"[STABILITY] AUC_end mean: robust={mean_auc_rob:.3f}, non={mean_auc_non:.3f}")
        if np.any(np.isfinite(SNR_e)):
            print(f"[STABILITY] SNR_end mean: robust={mean_snr_rob:.3f}, non={mean_snr_non:.3f}")

        # ---- Per-Gamma analysis (band visibility without averaging it away) ----
        uGam = np.unique(Gam[np.isfinite(Gam)])
        best = None  # track Gamma with largest fidelity_end separation
        for g in uGam:
            mask_g = np.isfinite(Gam) & (Gam == g)
            if not np.any(mask_g):
                continue
            rob_g = robust & mask_g
            non_g = (~robust) & mask_g
            ret_rob_g = float(np.nanmean(Ret[rob_g])) if np.any(rob_g) else float("nan")
            ret_non_g = float(np.nanmean(Ret[non_g])) if np.any(non_g) else float("nan")
            fid_rob_g = float(np.nanmean(Fid_e[rob_g])) if np.any(rob_g) else float("nan")
            fid_non_g = float(np.nanmean(Fid_e[non_g])) if np.any(non_g) else float("nan")
            d_ret = (ret_rob_g - ret_non_g) if (np.isfinite(ret_rob_g) and np.isfinite(ret_non_g)) else float("nan")
            d_fid = (fid_rob_g - fid_non_g) if (np.isfinite(fid_rob_g) and np.isfinite(fid_non_g)) else float("nan")
            print(f"[STABILITY|Gamma] Gam={g:.3f} Ret: rob={ret_rob_g:.3f}, non={ret_non_g:.3f}, Δ={d_ret:.3f} | "
                  f"Fid_end: rob={fid_rob_g:.3f}, non={fid_non_g:.3f}, Δ={d_fid:.3f}")
            if np.isfinite(d_fid):
                if best is None or abs(d_fid) > abs(best[1]):
                    best = (g, d_fid)
        if best is not None:
            print(f"[STABILITY|Gamma] Max |Δ Fidelity_end| at Gam={best[0]:.3f}: Δ={best[1]:.3f}")
    else:
        print("[STABILITY] no data")

    # Report saved plot paths (signed plot may be absent if no data)
    saved = [p1, p2, p3, p4]
    if 'p_signed' in locals():
        saved.append(p_signed)
    # Add per-Gamma heatmaps if created
    for extra_name in ("p3_ret_by_gamma", "p3_fid_by_gamma", "p3_auc_by_gamma", "p3_snr_by_gamma"):
        if extra_name in locals():
            extra_val = locals()[extra_name]
            if extra_val:
                saved.append(extra_val)
    print("Saved plots:", *saved)


if __name__ == "__main__":
    src = os.environ.get("FUM_RESULTS_CSV", os.path.join("outputs", "memory_steering_results.csv"))
    outdir = os.environ.get("FUM_RESULTS_OUT", "outputs")
    plot_all(src, outdir)