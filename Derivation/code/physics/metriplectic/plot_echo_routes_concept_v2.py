#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def find_latest_run_json() -> Path:
    base = Path("Derivation/code/outputs/logs/metriplectic")
    pattern = re.compile(r"^\d{8}_\d{6}_assisted_echo__assisted-echo-t4-prereg-v1c\.json$")
    candidates: List[Path] = []
    if base.exists():
        for p in base.iterdir():
            if p.is_file() and pattern.match(p.name):
                candidates.append(p)
    if candidates:
        return sorted(candidates, key=lambda p: p.name)[-1]
    # Fallback to the known successful run path (from session)
    return base / "20251030_194555_assisted_echo__assisted-echo-t4-prereg-v1c.json"


def load_summary_ceg(run_json: Path) -> Tuple[float, float]:
    """
    Return (lambda_with_max_median, median_max_ceg) excluding lambda=0.
    """
    data = json.loads(run_json.read_text(encoding="utf-8"))
    ceg_summary = data.get("ceg_summary", {})
    lam_vals = []
    med_vals = []
    for k, v in ceg_summary.items():
        try:
            lam = float(k)
        except Exception:
            continue
        if abs(lam) < 1e-15:
            continue
        med = float(v.get("median", 0.0))
        lam_vals.append(lam)
        med_vals.append(med)
    if not lam_vals:
        return 0.0, 0.0
    idx = int(np.argmax(np.array(med_vals)))
    return float(lam_vals[idx]), float(med_vals[idx])


def bezier_curve(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, n: int = 300) -> np.ndarray:
    t = np.linspace(0.0, 1.0, n)[:, None]
    b0 = (1 - t) ** 3
    b1 = 3 * (1 - t) ** 2 * t
    b2 = 3 * (1 - t) * t ** 2
    b3 = t ** 3
    pts = b0 * p0 + b1 * p1 + b2 * p2 + b3 * p3
    return pts


def build_vector_field(ax, xlim=(-2.6, 2.6), ylim=(-2.0, 2.0), gamma=0.15, a=1.0, b=1.0) -> None:
    """
    Conceptual metriplectic field in 2D:
      H = 0.5 * ( (x/a)^2 + (y/b)^2 )
      J = [[0, 1], [-1, 0]]
      M ~ gamma * I with S = -H so M ∇S = -gamma ∇H
      v = J ∇H + M ∇S = [y/b^2, -x/a^2] - gamma [x/a^2, y/b^2]
    """
    nx, ny = 31, 25
    xs = np.linspace(xlim[0], xlim[1], nx)
    ys = np.linspace(ylim[0], ylim[1], ny)
    X, Y = np.meshgrid(xs, ys)
    # Gradient of H
    dHx = X / (a * a)
    dHy = Y / (b * b)
    # J∇H + M∇S (with S=-H) => [dHy, -dHx] - gamma [dHx, dHy]
    U = dHy - gamma * dHx
    V = -dHx - gamma * dHy
    # Normalize arrows for visual clarity
    Mv = np.hypot(U, V)
    U = np.where(Mv > 0, U / (Mv + 1e-12), 0.0)
    V = np.where(Mv > 0, V / (Mv + 1e-12), 0.0)
    ax.quiver(X, Y, U, V, color="#666666", alpha=0.5, width=0.0022, headwidth=3.5, headlength=4.0, minlength=0.0, scale=28)


def draw_hamiltonian_contours(ax, xlim=(-2.6, 2.6), ylim=(-2.0, 2.0), a=1.0, b=1.0) -> None:
    xs = np.linspace(xlim[0], xlim[1], 320)
    ys = np.linspace(ylim[0], ylim[1], 260)
    X, Y = np.meshgrid(xs, ys)
    H = 0.5 * ((X / a) ** 2 + (Y / b) ** 2)
    levels = np.linspace(0.1, 3.0, 17)
    cs = ax.contour(X, Y, H, levels=levels, cmap="viridis", alpha=0.9, linewidths=1.1)
    # optional: label a few contours lightly
    try:
        ax.clabel(cs, inline=True, fmt="%.1f", fontsize=7, inline_spacing=3)
    except Exception:
        pass


def main() -> int:
    # Load current run summary
    run_json = find_latest_run_json()
    lam_star, ceg_star = load_summary_ceg(run_json)

    # Figure init
    fig, ax = plt.subplots(figsize=(7.8, 5.8), dpi=150)
    ax.set_aspect("equal", adjustable="box")
    xlim = (-2.6, 2.6)
    ylim = (-2.0, 2.0)

    # Background: Hamiltonian contours + metriplectic vector field
    draw_hamiltonian_contours(ax, xlim=xlim, ylim=ylim, a=1.0, b=1.0)
    build_vector_field(ax, xlim=xlim, ylim=ylim, gamma=0.15, a=1.0, b=1.0)

    # Key points
    z0 = np.array([0.0, 0.0])                  # initial state (origin in conceptual 2D projection)
    R_end = 2.35                                # endpoint radius for the forward pass
    theta = math.radians(40.0)
    e_base = np.array([R_end * math.cos(theta), R_end * math.sin(theta)])  # "E_baseline" point on contour

    # Residual distances after reverse phases (conceptual, proportional to gain)
    # Map CEG at max-lambda to a visible contraction relative to a nominal baseline miss radius
    miss_base = 0.70
    miss_asst = miss_base * (1.0 - float(ceg_star))  # slight improvement per measured CEG
    # Place residual points near origin along different bearings for clarity
    theta_b = math.radians(-20.0)
    theta_a = math.radians(-40.0)
    r_base_pt = np.array([miss_base * math.cos(theta_b), miss_base * math.sin(theta_b)])
    r_asst_pt = np.array([miss_asst * math.cos(theta_a), miss_asst * math.sin(theta_a)])

    # Forward route (orange): stylized JMJ arc from z0 to e_base
    p0 = z0
    p1 = np.array([0.6, -0.2])
    p2 = np.array([1.2, 0.9])
    p3 = e_base
    forward_pts = bezier_curve(p0, p1, p2, p3, n=600)
    ax.plot(forward_pts[:, 0], forward_pts[:, 1], color="#f4a300", lw=2.5, label="forward (JMJ)")

    # Baseline reverse (dashed blue): e_base to a miss near origin
    q0 = e_base
    q1 = e_base + np.array([-0.8, -0.2])
    q2 = np.array([0.8, -0.8])
    q3 = r_base_pt
    base_rev = bezier_curve(q0, q1, q2, q3, n=500)
    ax.plot(base_rev[:, 0], base_rev[:, 1], color="#1f77b4", lw=2.2, ls="--", label="reverse (baseline)")

    # Assisted reverse (dash-dot teal): e_base to closer point
    r0 = e_base
    r1 = e_base + np.array([-0.7, -0.4])
    r2 = np.array([0.5, -1.1])
    r3 = r_asst_pt
    asst_rev = bezier_curve(r0, r1, r2, r3, n=500)
    ax.plot(asst_rev[:, 0], asst_rev[:, 1], color="#1aa188", lw=2.6, ls="dashdot", label="reverse (assisted)")

    # Markers and annotations
    ax.scatter([z0[0]], [z0[1]], c="k", s=28, zorder=5)
    ax.annotate("z0", xy=z0, xytext=(6, 0), textcoords="offset points", fontsize=9)

    ax.scatter([e_base[0]], [e_base[1]], c="#000000", s=28, zorder=5)
    ax.annotate(r"$E_{\mathrm{baseline}}$", xy=e_base, xytext=(6, 2), textcoords="offset points", fontsize=9)

    ax.scatter([r_base_pt[0]], [r_base_pt[1]], c="#1f77b4", s=20, zorder=6)
    ax.annotate("baseline miss", xy=r_base_pt, xytext=(8, -12), textcoords="offset points", color="#1f77b4", fontsize=9)

    ax.scatter([r_asst_pt[0]], [r_asst_pt[1]], c="#1aa188", s=20, zorder=6)
    ax.annotate("assisted miss", xy=r_asst_pt, xytext=(8, -12), textcoords="offset points", color="#1aa188", fontsize=9)

    # Lambda/CEG callout box
    box_txt = f"λ* = {lam_star:.2f}\nmedian CEG(λ*) = {ceg_star:.3f}"
    ax.text(0.02, 0.98, box_txt, ha="left", va="top", transform=ax.transAxes, fontsize=9,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#333", alpha=0.9))

    # Aesthetics
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("state coordinate 1")
    ax.set_ylabel("state coordinate 2")
    ax.set_title("VDM echo with metriplectic split: baseline miss vs assisted rewind (conceptual)")
    ax.grid(True, ls="--", alpha=0.35)
    ax.legend(loc="upper right", frameon=True)

    # Save to requested conceptual path (overwrite previous)
    out_path = Path("Derivation/Metriplectic/vdm_echo_landscape_v2.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, facecolor="white")
    plt.close(fig)

    print(json.dumps({"figure": str(out_path), "run_json": str(run_json), "lambda_star": lam_star, "median_ceg_star": ceg_star}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())