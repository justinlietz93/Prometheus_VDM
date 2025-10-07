"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Memory-Driven Steering (experiments): rigorous mapping to your derivations + three falsifiable tests

What this file does (experiments layer)
- Generates datasets (and prints CSV) to test the three predictions introduced in
  [derivation/memory_steering.md](derivation/memory_steering.md:1) from the Voxtrium note
  [derivation/voxtrium/voxtrium_message.txt](derivation/voxtrium/voxtrium_message.txt:1):
  1) Junction logistic collapse:  P(A) ≈ σ(Θ Δm)
  2) Curvature scaling:           ⟨κ_path⟩ ∝ Θ |∇m|
  3) Stability band:              robust memory for D_a ≳ Λ with intermediate Γ

How this maps to your φ‑EFT derivations (orthogonal layer)
- The fast φ‑sector continuum equation and invariants are already derived in
  [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:121-128):
      □φ + α φ² − (α − β) φ = 0,   v = 1 − β/α,   m_eff² = α − β.
- The kinetic normalization c² = 2 J a² is rigorously obtained from a discrete action in
  [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:121-128).
- The memory‑steering layer (M) is slow and biases routing only; it does not modify φ propagation,
  the vacuum/mass results, nor the on‑site invariant Q_FUM from [derivation/symmetry_analysis.md](derivation/symmetry_analysis.md:141-148).

Dimensionless groups used implicitly in the tests (see [derivation/memory_steering.md](derivation/memory_steering.md:1))
- Θ = η M0        (steering strength)
- D_a = γ R0 T / M0,   Λ = δ T,   Γ = κ T / L²
- We choose simple graph‑native rulers (L, T, M0, R0) inside each test to demonstrate collapse
  and leave the physical alignment to φ’s (a, τ) to [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:44-80).

Outputs (printed to stdout when run)
- Junction logistic:            “Theta*Delta_m, P(A)”
- Curvature scaling:            “Theta*|grad m|, mean(kappa_path)”
- Stability band:               “D_a, Lambda, Gamma, Retention, Fidelity_w, Fidelity_end, Fidelity_shuffle_end, Fidelity_edge_end, AUC_end, SNR_end”

Usage
- python3 fum_rt/utils/memory_steering_experiments.py  > outputs/memory_steering_results.csv
- The plotting helper (separate) converts the combined CSV into figures saved in outputs/.
"""

from __future__ import annotations

import math
import sys
import os
import contextlib
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np

# Steering primitives (robust import: module or script)
try:
    from fum_rt.core.memory_steering import (
        build_graph_laplacian,
        update_memory,
        transition_probs,
        sample_next_neighbor,
        compute_dimensionless_groups,
        y_junction_adjacency,
        collect_junction_choices,
    )
except Exception as e1:
    # Second-chance import: add repo root to sys.path if running as a script
    try:
        import os as _os, sys as _sys
        _repo_root = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), _os.pardir, _os.pardir))
        if _repo_root not in _sys.path:
            _sys.path.insert(0, _repo_root)
        from fum_rt.core.memory_steering import (
            build_graph_laplacian,
            update_memory,
            transition_probs,
            sample_next_neighbor,
            compute_dimensionless_groups,
            y_junction_adjacency,
            collect_junction_choices,
        )
    except Exception as e2:
        print("[warn] falling back to local copies of simple helpers:", e2, file=sys.stderr)

        def build_graph_laplacian(A: np.ndarray) -> np.ndarray:
            A = np.asarray(A)
            deg = np.sum((A != 0) & (~np.eye(A.shape[0], dtype=bool)), axis=1).astype(np.float64)
            return np.diag(deg) - (A != 0).astype(np.float64)

        def transition_probs(i: int, neighbors: Sequence[int], m: np.ndarray, theta: float) -> np.ndarray:
            neigh = np.asarray(list(neighbors), dtype=int)
            if neigh.size == 0:
                return np.empty((0,), dtype=np.float64)
            z = theta * m[neigh]
            z = z - np.max(z)
            exps = np.exp(z)
            s = exps.sum()
            if s <= 0.0 or not np.isfinite(s):
                return np.ones_like(exps) / exps.size
            return exps / s

        def sample_next_neighbor(
            i: int, neighbors: Sequence[int], m: np.ndarray, theta: float, rng: Optional[np.random.Generator] = None
        ) -> Optional[int]:
            neigh = np.asarray(list(neighbors), dtype=int)
            if neigh.size == 0:
                return None
            p = transition_probs(i, neigh, m, theta)
            if rng is None:
                rng = np.random.default_rng()
            idx = int(rng.choice(neigh.size, p=p))
            return int(neigh[idx])

        def y_junction_adjacency(len_in: int = 5, len_a: int = 5, len_b: int = 5) -> Tuple[np.ndarray, int, int, int]:
            J = len_in
            a_start = J + 1
            b_start = J + 1 + len_a
            N = len_in + 1 + len_a + len_b
            A = np.zeros((N, N), dtype=np.int8)
            for t in range(1, len_in):
                A[t - 1, t] = 1
                A[t, t - 1] = 1
            if len_in > 0:
                A[len_in - 1, J] = 1
                A[J, len_in - 1] = 1
            last = J
            for k in range(len_a):
                n = a_start + k
                A[last, n] = 1
                A[n, last] = 1
                last = n
            last = J
            for k in range(len_b):
                n = b_start + k
                A[last, n] = 1
                A[n, last] = 1
                last = n
            return A, J, a_start, b_start

        def collect_junction_choices(
            A: np.ndarray,
            m: np.ndarray,
            J: int,
            a_next: int,
            b_next: int,
            theta: float,
            trials: int = 1000,
            rng: Optional[np.random.Generator] = None,
        ) -> Tuple[int, int]:
            if rng is None:
                rng = np.random.default_rng()
            neighbors = np.where(A[J] != 0)[0]
            neighbors = [n for n in neighbors if n in (a_next, b_next)]
            if len(neighbors) != 2:
                neigh = np.where(A[J] != 0)[0]
                if neigh.size < 2:
                    return (0, 0)
                order = np.argsort(m[neigh])[::-1]
                neighbors = [int(neigh[order[0]]), int(neigh[order[1]])]
            counts = {neighbors[0]: 0, neighbors[1]: 0}
            for _ in range(int(trials)):
                p = transition_probs(J, neighbors, m, theta)
                idx = int(rng.choice(2, p=p))
                counts[neighbors[idx]] += 1
            ca = counts.get(a_next, 0)
            cb = counts.get(b_next, 0)
            return (int(ca), int(cb))

        def update_memory(m, r, L, gamma, delta, kappa, dt):
            m = np.asarray(m, dtype=np.float64)
            r = np.asarray(r, dtype=np.float64)
            return m + dt * (gamma * r - delta * m - kappa * (L @ m))

        def compute_dimensionless_groups(eta, M0, gamma, R0, T, delta, kappa, L_scale):
            Theta = eta * float(M0)
            Da = (gamma * R0 * T) / float(M0) if M0 != 0 else np.inf
            Lam = delta * T
            Gam = (kappa * T) / (L_scale ** 2) if L_scale != 0 else np.inf
            return (float(Theta), float(Da), float(Lam), float(Gam))


# ---------------------------
# Utilities for grid graphs
# ---------------------------

def grid_adjacency(nx: int, ny: int) -> np.ndarray:
    """4-neighbor undirected grid adjacency (no wrap). Nodes indexed row-major: i = y*nx + x."""
    N = nx * ny
    A = np.zeros((N, N), dtype=np.int8)
    for y in range(ny):
        for x in range(nx):
            i = y * nx + x
            if x + 1 < nx:
                j = y * nx + (x + 1)
                A[i, j] = 1
                A[j, i] = 1
            if y + 1 < ny:
                j = (y + 1) * nx + x
                A[i, j] = 1
                A[j, i] = 1
    return A


def grid_neighbors(nx: int, ny: int, i: int) -> List[int]:
    y, x = divmod(i, nx)
    out = []
    if x > 0:
        out.append(i - 1)
    if x + 1 < nx:
        out.append(i + 1)
    if y > 0:
        out.append(i - nx)
    if y + 1 < ny:
        out.append(i + nx)
    return out


# ---------------------------
# 1) Junction logistic collapse
# ---------------------------

def run_junction_logistic(theta: float = 2.0, delta_m_values: Sequence[float] = None, trials: int = 2000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Junction logistic collapse: P(A) ≈ σ(Θ Δm)

    Why this maps to the derivation:
    - In [derivation/memory_steering.md](derivation/memory_steering.md:1) the steering index is n=exp(η M).
      At a fork, the two outgoing neighbors (A,B) inherit memory values (m_A, m_B). The softmax routing
      P(i→j) ∝ exp(Θ m_j) reduces to a binary logistic:
          P(A) = σ(Θ (m_A − m_B)) = σ(Θ Δm).
      Hence plotting P(A) vs Θ Δm should overlay across graph sizes/speeds, demonstrating a
      dimensionless collapse (Θ is the only slope).

    Args:
        theta: Θ (dimensionless steering strength)
        delta_m_values: sweep of Δm values in m‑units (dimensionless)
        trials: Bernoulli samples for P(A) estimation

    Returns:
        x: array of Θ Δm (abscissa of the collapse)
        pA: measured P(A)
    """
    if delta_m_values is None:
        delta_m_values = np.linspace(-2.0, 2.0, 17)  # symmetric sweep in m-units
    A, J, a0, b0 = y_junction_adjacency(5, 5, 5)
    N = A.shape[0]
    rng = np.random.default_rng(123)
    m = np.zeros(N, dtype=np.float64)
    xvals, pvals = [], []
    for d in delta_m_values:
        m[:] = 0.0
        m[a0] = +0.5 * d
        m[b0] = -0.5 * d
        ca, cb = collect_junction_choices(A, m, J, a0, b0, theta=theta, trials=trials, rng=rng)
        pA = ca / max(1, (ca + cb))
        xvals.append(theta * d)
        pvals.append(pA)
    return np.asarray(xvals), np.asarray(pvals)


# ---------------------------
# 2) Curvature scaling
# ---------------------------

def polyline_curvature(pts: np.ndarray) -> np.ndarray:
    """
    Discrete curvature estimate along a polyline:

    - We approximate the continuous curvature κ by the local turning angle Δθ and mean edge length ℓ:
          κ ≈ 2 sin(Δθ/2) / ℓ
      (endpoints are set to 0). This delivers a robust, grid‑agnostic estimator of path bending.

    - In the derivation [derivation/memory_steering.md](derivation/memory_steering.md:1), rays obey r'' = ∇_⊥ ln n = Θ ∇_⊥ m
      (with n=exp(Θ m)). The magnitude of r'' along a path is proportional to |∇m| with a slope ∝ Θ. This function
      yields the ⟨κ_path⟩ metric used in the curvature scaling test ⟨κ_path⟩ ∝ Θ |∇m|.
    """
    n = pts.shape[0]
    if n < 3:
        return np.zeros(n, dtype=np.float64)
    kappa = np.zeros(n, dtype=np.float64)
    for i in range(1, n - 1):
        p0 = pts[i - 1]
        p1 = pts[i]
        p2 = pts[i + 1]
        v1 = p1 - p0
        v2 = p2 - p1
        # normalize
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        if n1 == 0 or n2 == 0:
            kappa[i] = 0.0
            continue
        v1n = v1 / n1
        v2n = v2 / n2
        cosang = np.clip(np.dot(v1n, v2n), -1.0, 1.0)
        dtheta = math.acos(cosang)
        ell = 0.5 * (n1 + n2)
        if ell == 0:
            kappa[i] = 0.0
        else:
            kappa[i] = 2.0 * math.sin(0.5 * dtheta) / ell
    return kappa

def polyline_curvature_signed(pts: np.ndarray) -> np.ndarray:
    """
    Discrete signed curvature estimate along a polyline.

    - Uses the same magnitude estimator as polyline_curvature:
          |κ| ≈ 2 sin(Δθ/2) / ℓ
      but multiplies by the sign sgn = sign( (v1 × v2)_z ) where v1 = p1−p0, v2 = p2−p1.
      In 2D, (v1 × v2)_z = v1_x v2_y − v1_y v2_x.

    - This returns the signed bending, suitable for falsification via gradient/Θ sign flips:
          ⟨κ_signed⟩ ∝ Θ (∇m · n_⊥)
    """
    n = pts.shape[0]
    if n < 3:
        return np.zeros(n, dtype=np.float64)
    kappa = np.zeros(n, dtype=np.float64)
    for i in range(1, n - 1):
        p0 = pts[i - 1]
        p1 = pts[i]
        p2 = pts[i + 1]
        v1 = p1 - p0
        v2 = p2 - p1
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        if n1 == 0 or n2 == 0:
            kappa[i] = 0.0
            continue
        v1n = v1 / n1
        v2n = v2 / n2
        # turning angle
        cosang = float(np.clip(np.dot(v1n, v2n), -1.0, 1.0))
        dtheta = math.acos(cosang)
        ell = 0.5 * (n1 + n2)
        if ell == 0:
            kmag = 0.0
        else:
            kmag = 2.0 * math.sin(0.5 * dtheta) / ell
        # orientation sign from 2D cross product z-component
        cross_z = float(v1n[0] * v2n[1] - v1n[1] * v2n[0])
        sgn = 0.0
        if cross_z > 0:
            sgn = +1.0
        elif cross_z < 0:
            sgn = -1.0
        kappa[i] = sgn * kmag
    return kappa

def run_curvature_scaling(
    nx: int = 21,
    ny: int = 21,
    theta_values: Sequence[float] = (1.0, 2.0, 3.0),
    pulses: int = 50,
    heading_bias: float = 2.0,
    temperature: float = 0.3,
    mode: str = "graph",
    dt: float = 0.2,
    nsteps: int = 80,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Curvature scaling: ⟨κ_path⟩ ∝ Θ |∇m|

    Protocol and mapping:
    - Create a smooth, constant gradient in m across the grid: m(y) increases linearly with y.
      This fixes |∇m| uniformly (up to grid effects).
    - Two implementations:
      (graph) 8‑neighbor with heading inertia (score_j = Θ m_j + ξ cos(∠(h, step_j))).
      (ray)   Continuous 2‑D “ray” stepper: ẋ = ĥ, ḣ = Π_⊥(Θ ∇m), with ĥ renormalized each step.
    - Return pairs (X = Θ |∇m|, Y = ⟨κ_path⟩). The derivation predicts linear scaling.

    Args:
        nx, ny: grid size for graph mode (also sets the m-gradient scale).
        theta_values: Θ values to test.
        pulses: number of paths to average per Θ (seeds).
        heading_bias: ξ in the graph sampler’s heading term.
        mode: "graph" (default) or "ray".
        dt:   step size for the ray integrator.
        nsteps: number of steps for the ray integrator.

    Returns:
        X: array of Θ |∇m|
        Y: array of mean curvature per path
    """
    # Memory gradient: m(y) = y/(ny-1) ∈ [0,1], so |∇m| = 1/(ny-1)
    grad_mag = 1.0 / max(1, ny - 1)

    rng = np.random.default_rng(7)
    X_all, Y_all = [], []

    if mode == "graph":
        # Build discrete m on the grid
        m = np.zeros(nx * ny, dtype=np.float64)
        for y in range(ny):
            m[y * nx:(y + 1) * nx] = (y / max(1, ny - 1))

        # 8-neighbor helper (no wrap)
        def neighbors8(i: int) -> List[int]:
            y, x = divmod(i, nx)
            out = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < nx and 0 <= yy < ny:
                        out.append(yy * nx + xx)
            return out

        def dir_unit(i: int, j: int) -> np.ndarray:
            yi, xi = divmod(i, nx)
            yj, xj = divmod(j, nx)
            v = np.array([xj - xi, yj - yi], dtype=np.float64)
            n = np.linalg.norm(v)
            return v / n if n > 0 else np.zeros(2, dtype=np.float64)

        # Sources along a central row; initial heading along +x so ∇m is transverse
        src_y = ny // 2
        src_nodes = [src_y * nx + x for x in range(1, nx - 1)]  # avoid borders
        for theta in theta_values:
            for s in rng.choice(src_nodes, size=min(pulses, len(src_nodes)), replace=False):
                path_nodes = [s]
                last = -1
                cur = s
                h = np.array([1.0, 0.0], dtype=np.float64)  # initial heading (+x)
                steps = nx // 2
                for _ in range(steps):
                    neigh = neighbors8(cur)
                    if len(neigh) == 0:
                        break
                    # Heading-aware softmax: score = Θ m_j + heading_bias * cos(∠(h, step))
                    scores = []
                    for j in neigh:
                        u = dir_unit(cur, j)
                        cosang = float(np.clip(np.dot(u, h), -1.0, 1.0))
                        scores.append(theta * m[j] + heading_bias * cosang)
                    z = np.asarray(scores, dtype=np.float64) / max(temperature, 1e-6)
                    z -= np.max(z)
                    p = np.exp(z)
                    ssum = p.sum()
                    if not np.isfinite(ssum) or ssum <= 0:
                        p = np.ones_like(p) / len(p)
                    else:
                        p /= ssum
                    idx = int(rng.choice(len(neigh), p=p))
                    nxt = int(neigh[idx])
                    if nxt == cur:
                        break
                    last, cur = cur, nxt
                    h = dir_unit(last, cur)
                    path_nodes.append(cur)

                # Compute curvature along the polyline
                pts = np.array([[n % nx, n // nx] for n in path_nodes], dtype=np.float64)
                if pts.shape[0] >= 3:
                    kappa = polyline_curvature(pts)
                    if kappa.size > 0:
                        X_all.append(theta * grad_mag)
                        Y_all.append(float(np.mean(kappa)))

    else:
        # Continuous ray integrator in a domain of size (nx, ny)
        g = np.array([0.0, grad_mag], dtype=np.float64)  # ∇m constant and vertical
        # Seeds: choose start positions along mid-height, avoid borders
        y0 = (ny - 1) * 0.5
        xs = rng.uniform(1.0, nx - 2.0, size=pulses)
        for theta in theta_values:
            for x0 in xs:
                # Initialize position and heading
                x = np.array([x0, y0], dtype=np.float64)
                h = np.array([1.0, 0.0], dtype=np.float64)
                pts = [x.copy()]
                for _ in range(int(nsteps)):
                    # ḣ = Π_⊥(Θ ∇m) = Θ(∇m - (∇m·h) h)
                    dv = theta * (g - np.dot(g, h) * h)
                    h = h + dt * dv
                    nrm = float(np.linalg.norm(h))
                    if nrm == 0 or not np.isfinite(nrm):
                        break
                    h = h / nrm
                    # ẋ = ĥ (unit speed)
                    x = x + dt * h
                    pts.append(x.copy())
                pts = np.asarray(pts, dtype=np.float64)
                if pts.shape[0] >= 3:
                    kappa = polyline_curvature(pts)
                    if kappa.size > 0:
                        X_all.append(theta * grad_mag)
                        Y_all.append(float(np.mean(kappa)))

    return np.asarray(X_all), np.asarray(Y_all)
# ---------------------------
# 2b) Curvature: calibration and signed-test helpers
# ---------------------------

def calibrate_curvature_on_arcs(R_values=(20.0, 40.0, 80.0), n_points=200, noise=0.0, out_png="outputs/curvature_calibration.png"):
    """
    Synthetic calibration: draw circular arcs of radius R and verify the polyline_curvature
    estimator returns kappa ≈ 1/R (±20%).

    Args:
        R_values: iterable radii to test
        n_points: samples per arc
        noise: optional Gaussian jitter to add to points
        out_png: path to save the calibration plot

    Returns:
        results: list of (R, kappa_mean, kappa_std, frac_error)
    """
    import os
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    import matplotlib.pyplot as plt
    res = []
    fig, ax = plt.subplots(figsize=(6,4))
    for R in R_values:
        theta = np.linspace(0.0, np.pi/3.0, n_points)  # 60-degree arc
        x = R * np.cos(theta)
        y = R * np.sin(theta)
        pts = np.stack([x, y], axis=1)
        if noise > 0.0:
            pts = pts + np.random.default_rng(123).normal(scale=noise, size=pts.shape)
        kappa = polyline_curvature(pts)
        if kappa.size == 0:
            kappa_mean, kappa_std = np.nan, np.nan
        else:
            kappa_mean = float(np.mean(kappa[1:-1]))  # ignore endpoints
            kappa_std = float(np.std(kappa[1:-1]))
        target = 1.0/float(R)
        frac_err = (kappa_mean/target - 1.0) if (target>0 and np.isfinite(target) and np.isfinite(kappa_mean)) else np.nan
        res.append((float(R), kappa_mean, kappa_std, frac_err))
        ax.errorbar([1.0/R], [kappa_mean], yerr=[kappa_std], fmt="o", label=f"R={R:g}")
    ax.axline((0,0),(1,1), color="#d62728", linestyle="--", label="ideal: kappa=1/R")
    ax.set_xlabel("1/R (ideal)")
    ax.set_ylabel("estimated kappa")
    ax.set_title("Curvature estimator calibration on circular arcs")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    return res


def run_curvature_scaling_signed(
    nx: int = 41,
    ny: int = 41,
    x_values: Optional[Sequence[float]] = None,   # desired X = Theta*|grad m|
    pulses_per_x: int = 64,
    dt: float = 0.10,
    nsteps: int = 600,
    signed_check_mids: int = 3,
    rng: Optional[np.random.Generator] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Curvature scaling with ray-limit integrator + signed falsification and SE estimates.

    - Domain: continuous rays in a box of size (nx, ny), with constant gradient in m along +y.
    - For each target X = Theta*|grad m|, pick Theta = X/|grad m| and average path curvature over many seeds.
    - Signed test: for ~3 midpoints of X, repeat runs with (1) gradient flipped (|∇m|→−|∇m|) and (2) Theta→−Theta.

    Returns:
        X_all: array of X = Theta*|grad m|
        Y_mean: mean kappa per X/sign bucket
        Y_se: standard error per X/sign bucket
        sign_id: integer tags {0: baseline, 1: flip_grad, 2: flip_theta}
    """
    if rng is None:
        rng = np.random.default_rng(77)

    # Gradient magnitude based on grid
    grad_mag = 1.0 / max(1, ny - 1)
    if x_values is None:
        # default: 10 log-spaced values in [0.02, 0.45]
        x_values = np.geomspace(0.02, 0.45, 10)
    x_values = np.asarray(x_values, dtype=float)

    # Seeds: choose start x positions along mid-height, avoid borders
    y0 = (ny - 1) * 0.5
    xs_all = rng.uniform(1.0, nx - 2.0, size=pulses_per_x)

    def ray_batch(theta_val: float, grad_sign: float = 1.0) -> Tuple[float, float]:
        # Constant gradient vector (vertical), allow sign flip for falsification
        g = np.array([0.0, grad_sign * grad_mag], dtype=np.float64)
        kappas = []
        for x0 in xs_all:
            x = np.array([x0, y0], dtype=np.float64)
            h = np.array([1.0, 0.0], dtype=np.float64)  # initial heading +x
            pts = [x.copy()]
            for _ in range(int(nsteps)):
                dv = theta_val * (g - np.dot(g, h) * h)     # h' = Theta (g - (g·h)h)
                h = h + dt * dv
                nrm = float(np.linalg.norm(h))
                if nrm == 0 or not np.isfinite(nrm):
                    break
                h = h / nrm
                x = x + dt * h
                pts.append(x.copy())
            pts = np.asarray(pts, dtype=np.float64)
            if pts.shape[0] >= 3:
                kappa = polyline_curvature(pts)
                if kappa.size > 0:
                    kappas.append(float(np.mean(kappa)))
        if len(kappas) == 0:
            return (np.nan, np.nan)
        arr = np.asarray(kappas, dtype=float)
        return (float(np.mean(arr)), float(np.std(arr)/np.sqrt(max(1, arr.size))))

    # Baseline (sign_id=0)
    X_base, Y_mean_base, Y_se_base, sign_base = [], [], [], []
    for X in x_values:
        theta = X / max(grad_mag, 1e-12)
        mu, se = ray_batch(theta, grad_sign=+1.0)
        X_base.append(X); Y_mean_base.append(mu); Y_se_base.append(se); sign_base.append(0)

    # Signed falsification on ~3 midpoints
    mid_idx = np.linspace(0, len(x_values)-1, signed_check_mids, dtype=int)
    X_flip, Y_mean_flip, Y_se_flip, sign_flip = [], [], [], []
    for idx in mid_idx:
        Xmid = float(x_values[idx])
        theta_mid = Xmid / max(grad_mag, 1e-12)

        # flip gradient (sign_id=1)
        mu1, se1 = ray_batch(theta_mid, grad_sign=-1.0)
        X_flip.append(Xmid); Y_mean_flip.append(mu1); Y_se_flip.append(se1); sign_flip.append(1)

        # flip Theta (sign_id=2)
        mu2, se2 = ray_batch(-theta_mid, grad_sign=+1.0)
        X_flip.append(Xmid); Y_mean_flip.append(mu2); Y_se_flip.append(se2); sign_flip.append(2)

    # Concatenate
    X_all = np.asarray(list(X_base) + list(X_flip), dtype=float)
    Y_mean = np.asarray(list(Y_mean_base) + list(Y_mean_flip), dtype=float)
    Y_se = np.asarray(list(Y_se_base) + list(Y_se_flip), dtype=float)
    sign_id = np.asarray(list(sign_base) + list(sign_flip), dtype=int)
    return X_all, Y_mean, Y_se, sign_id


# ---------------------------
# 3) Stability band
# ---------------------------

def run_stability_band(
    nx: int = 21,
    ny: int = 21,
    T_write: float = 5.0,
    T_decay: float = 5.0,
    dt: float = 0.1,
    gamma_values: Sequence[float] = (0.5,),           # used only if da_values is None
    delta_values: Sequence[float] = (0.05, 0.1, 0.2),
    kappa_values: Sequence[float] = (0.2, 0.5, 1.0),
    da_values: Optional[Sequence[float]] = None,       # if provided, dose-controlled write using scale_R
    gamma_fixed: float = 1.0,
    dose_model: str = "scale_R",
    topk_frac: float = 0.05,
    cfl_limit: float = 0.9,
) -> List[Tuple[float, float, float, float, float, float, float, float, float, float, float, float]]:
    """
    Stability band in (D_a, Λ, Γ) with dose control and discriminative metrics.

    PDE: ∂_t m = γ r − δ m − κ L m
    Dimensionless: D_a = γ R_0 T / M_0, Λ = δ T, Γ = κ T / L²

    Protocol (two‑phase):
      - Write (duration T_write): r = R_amp * R_mask, evolve → m_w
      - Decay (duration T_decay): r = 0, evolve → m_end

    Dose control (when da_values is provided):
      Enforce ∫_0^{T_write} γ R_0 dt = D_a M_0 via R_amp = (D_a*M0)/(γ_fixed*T_write).
      We set γ = gamma_fixed during both phases.

    Metrics:
      - Retention         = ||m_end|| / ||m_w||                (||·|| = mean |·|)
      - Fidelity_w        = corr(m_w, R_mask)
      - Fidelity_end      = corr(m_end, R_mask)
      - Fidelity_shuffle  = corr(m_end, shuffle(R_mask))
      - Fidelity_edge     = corr(L m_end, L R_mask)
      - AUC_end           = ROC AUC for score=m_end vs mask
      - SNR_end           = (μ_in − μ_out) / σ_out
      - AUPRC_topk        = truncated AP using top k=floor(topk_frac*N) predictions
      - BPER              = band‑pass energy ratio = ||L_norm m_end|| / ||m_end||

    Returns rows:
      (D_a, Λ, Γ, Ret, Fid_w, Fid_end, Fid_shuffle, Fid_edge, AUC_end, SNR_end, AUPRC_topk, BPER)

    Notes:
      - L is the combinatorial Laplacian; L_norm = I − D^{-1/2} A D^{-1/2}
      - We clamp κ by a CFL condition: dt * κ * λ_max(L) ≤ cfl_limit with λ_max(L) ≈ 2 * deg_max
    """
    N = nx * ny
    A = grid_adjacency(nx, ny)
    L = build_graph_laplacian(A)

    # Degree-normalized Laplacian for BPER
    deg = np.sum((A != 0) & (~np.eye(A.shape[0], dtype=bool)), axis=1).astype(np.float64)
    with np.errstate(divide="ignore"):
        dinv2 = 1.0 / np.sqrt(np.maximum(deg, 1e-12))
    Dinv2 = np.diag(dinv2)
    L_norm = np.eye(N, dtype=np.float64) - (Dinv2 @ (A != 0).astype(np.float64) @ Dinv2)

    # Localized usage R_mask: small central disk
    R_mask = np.zeros(N, dtype=np.float64)
    cx, cy = (nx - 1) / 2.0, (ny - 1) / 2.0
    for y in range(ny):
        for x in range(nx):
            r2 = (x - cx) ** 2 + (y - cy) ** 2
            if r2 <= (min(nx, ny) * 0.15) ** 2:
                R_mask[y * nx + x] = 1.0

    # Scales for dimensionless groups (simple choice)
    L_scale = 1.0
    M0 = 1.0
    R0 = 1.0
    rng = np.random.default_rng(12345)

    # Helpers
    def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
        a = np.asarray(a, float).ravel()
        b = np.asarray(b, float).ravel()
        am = a.mean(); bm = b.mean()
        av = a - am; bv = b - bm
        num = float(np.dot(av, bv))
        den = float(np.linalg.norm(av) * np.linalg.norm(bv))
        if den == 0.0 or not np.isfinite(den):
            return float("nan")
        return num / den

    def average_ranks(x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, float)
        order = np.argsort(x, kind="mergesort")
        ranks = np.empty_like(order, dtype=float)
        ranks[order] = np.arange(1, x.size + 1, dtype=float)
        i = 0
        while i < x.size:
            j = i + 1
            while j < x.size and x[order[j]] == x[order[i]]:
                j += 1
            if j - i > 1:
                avg = 0.5 * (i + 1 + j)
                ranks[order[i:j]] = avg
            i = j
        return ranks

    def auc_binary(scores: np.ndarray, labels: np.ndarray) -> float:
        scores = np.asarray(scores, float).ravel()
        labels = (np.asarray(labels).ravel() > 0.0).astype(int)
        n_pos = int(labels.sum()); n_neg = int(labels.size - n_pos)
        if n_pos == 0 or n_neg == 0:
            return float("nan")
        r = average_ranks(scores)
        R_pos = float(r[labels == 1].sum())
        U = R_pos - n_pos * (n_pos + 1) / 2.0
        return max(0.0, min(1.0, U / (n_pos * n_neg)))

    def average_precision_topk(scores: np.ndarray, labels: np.ndarray, topk: int) -> float:
        scores = np.asarray(scores, float).ravel()
        labels = (np.asarray(labels).ravel() > 0.0).astype(int)
        n_pos = int(labels.sum())
        if n_pos == 0 or topk <= 0:
            return float("nan")
        order = np.argsort(scores)[::-1]
        order = order[:min(topk, scores.size)]
        tp = 0
        ap_sum = 0.0
        for i, idx in enumerate(order, start=1):
            if labels[idx] == 1:
                tp += 1
                ap_sum += tp / i  # precision at this positive
        return float(ap_sum / max(1, n_pos))

    # CFL estimate for κ
    deg_max = int(np.max(deg)) if deg.size else 0
    lam_max = 2.0 * float(deg_max)  # rough bound for combinatorial Laplacian
    kappa_cfl = cfl_limit / max(1e-12, dt * lam_max)

    rows: List[Tuple[float, float, float, float, float, float, float, float, float, float, float, float]] = []

    if da_values is not None and len(da_values) > 0 and dose_model == "scale_R":
        # Dose-controlled path: use gamma_fixed and scale R amplitude to hit desired D_a
        for da_target in da_values:
            gamma = float(gamma_fixed)
            for delta in delta_values:
                for kappa in kappa_values:
                    kappa_eff = min(float(kappa), float(kappa_cfl))
                    # Write phase with amplitude scaling
                    R_amp = (da_target * M0) / max(1e-12, gamma * T_write)
                    m = np.zeros(N, dtype=np.float64)
                    steps_w = int(math.ceil(T_write / dt))
                    for _ in range(steps_w):
                        m = update_memory(m, R_amp * R_mask, L, gamma=gamma, delta=delta, kappa=kappa_eff, dt=dt)
                    m_w = m.copy()
                    # Decay
                    steps_d = int(math.ceil(T_decay / dt))
                    zero_R = np.zeros_like(R_mask)
                    for _ in range(steps_d):
                        m = update_memory(m, zero_R, L, gamma=gamma, delta=delta, kappa=kappa_eff, dt=dt)
                    m_end = m
                    # Metrics
                    denom = float(np.mean(np.abs(m_w))) if np.any(m_w != 0) else 1.0
                    Ret = float(np.mean(np.abs(m_end))) / max(denom, 1e-9)
                    Fid_w = pearson_corr(m_w, R_mask)
                    Fid_e = pearson_corr(m_end, R_mask)
                    # Controls
                    R_shuf = rng.permutation(R_mask)
                    Fid_s = pearson_corr(m_end, R_shuf)
                    LR = L @ R_mask
                    L_end = L @ m_end
                    Fid_edge = pearson_corr(L_end, LR)
                    mask_in = (R_mask > 0.0)
                    scores = m_end
                    auc = auc_binary(scores, mask_in.astype(int))
                    if np.any(~mask_in):
                        mu_in = float(np.mean(scores[mask_in])) if np.any(mask_in) else float("nan")
                        mu_out = float(np.mean(scores[~mask_in]))
                        sd_out = float(np.std(scores[~mask_in])) + 1e-9
                        snr = (mu_in - mu_out) / sd_out
                    else:
                        snr = float("nan")
                    # AUPRC top-k and BPER
                    k_top = max(1, int(round(topk_frac * N)))
                    ap_k = average_precision_topk(scores, mask_in.astype(int), k_top)
                    bper = float(np.linalg.norm(L_norm @ m_end) / max(1e-12, np.linalg.norm(m_end)))

                    # Dimensionless groups (record the target D_a explicitly)
                    Da = float(da_target)
                    Lam = float(delta * T_decay)
                    Gam = float((kappa_eff * T_write) / (L_scale ** 2))

                    rows.append((Da, Lam, Gam, Ret, Fid_w, Fid_e, Fid_s, Fid_edge, float(auc), float(snr), float(ap_k), float(bper)))
    else:
        # Legacy path (no explicit dose control): iterate gamma_values with unit-amplitude R
        for gamma in gamma_values:
            for delta in delta_values:
                for kappa in kappa_values:
                    kappa_eff = min(float(kappa), float(kappa_cfl))
                    # Write with unit amplitude
                    m = np.zeros(N, dtype=np.float64)
                    steps_w = int(math.ceil(T_write / dt))
                    for _ in range(steps_w):
                        m = update_memory(m, R_mask, L, gamma=float(gamma), delta=delta, kappa=kappa_eff, dt=dt)
                    m_w = m.copy()
                    # Decay
                    steps_d = int(math.ceil(T_decay / dt))
                    zero_R = np.zeros_like(R_mask)
                    for _ in range(steps_d):
                        m = update_memory(m, zero_R, L, gamma=float(gamma), delta=delta, kappa=kappa_eff, dt=dt)
                    m_end = m
                    # Metrics
                    denom = float(np.mean(np.abs(m_w))) if np.any(m_w != 0) else 1.0
                    Ret = float(np.mean(np.abs(m_end))) / max(denom, 1e-9)
                    Fid_w = pearson_corr(m_w, R_mask)
                    Fid_e = pearson_corr(m_end, R_mask)
                    R_shuf = rng.permutation(R_mask)
                    Fid_s = pearson_corr(m_end, R_shuf)
                    LR = L @ R_mask
                    L_end = L @ m_end
                    Fid_edge = pearson_corr(L_end, LR)
                    mask_in = (R_mask > 0.0)
                    scores = m_end
                    auc = auc_binary(scores, mask_in.astype(int))
                    if np.any(~mask_in):
                        mu_in = float(np.mean(scores[mask_in])) if np.any(mask_in) else float("nan")
                        mu_out = float(np.mean(scores[~mask_in]))
                        sd_out = float(np.std(scores[~mask_in])) + 1e-9
                        snr = (mu_in - mu_out) / sd_out
                    else:
                        snr = float("nan")
                    k_top = max(1, int(round(topk_frac * N)))
                    ap_k = average_precision_topk(scores, mask_in.astype(int), k_top)
                    bper = float(np.linalg.norm(L_norm @ m_end) / max(1e-12, np.linalg.norm(m_end)))

                    # Dimensionless groups from gamma, delta, kappa
                    Theta, Da, Lam_w, Gam = compute_dimensionless_groups(
                        eta=1.0, M0=M0, gamma=float(gamma), R0=R0, T=T_write, delta=delta, kappa=kappa_eff, L_scale=L_scale
                    )
                    Lam = float(delta * T_decay)
                    rows.append((float(Da), Lam, float(Gam), Ret, Fid_w, Fid_e, Fid_s, Fid_edge, float(auc), float(snr), float(ap_k), float(bper)))
    return rows


# ---------------------------
# Entry point
# ---------------------------

def main():
    # Optional CSV sink: if FUM_RESULTS_CSV_OUT is set, tee stdout into that file.
    csv_out = os.environ.get("FUM_RESULTS_CSV_OUT", "").strip()

    def _produce():
        # 1) Junction logistic
        theta = 2.0
        delta_m = np.linspace(-2.0, 2.0, 17)
        X, P = run_junction_logistic(theta=theta, delta_m_values=delta_m, trials=2000)
        print("# Junction logistic (CSV): Theta*Delta_m, P(A)")
        for x, p in zip(X, P):
            print(f"{x:.6f},{p:.6f}")

        # 2) Curvature scaling (unsigned overview; small-bend regime)
        Xc, Yc = run_curvature_scaling(
            nx=21, ny=21,
            theta_values=(0.5, 1.0, 2.0, 3.0, 4.0),
            pulses=160, mode="ray", dt=0.10, nsteps=200
        )
        print("\n# Curvature scaling (CSV): Theta*|grad m|, mean(kappa_path)")
        for x, y in zip(Xc, Yc):
            print(f"{x:.6f},{y:.8f}")

        # 2b) Curvature: calibration unit test + signed falsification (12 X values)
        cal_res = calibrate_curvature_on_arcs(
            R_values=(20.0, 40.0, 80.0), n_points=200, noise=0.0, out_png="outputs/curvature_calibration.png"
        )
        print("\n# Curvature calibration test (CSV): R, kappa_mean, kappa_std, frac_error")
        for (R, km, ks, fe) in cal_res:
            print(f"{R:.6f},{km:.8f},{ks:.8f},{fe:.6f}")

        Xs, Ys, Yse, sign_id = run_curvature_scaling_signed(
            nx=41, ny=41,
            x_values=np.linspace(0.02, 0.30, 12),  # avoid heading saturation
            pulses_per_x=96, dt=0.08, nsteps=400, signed_check_mids=3
        )
        print("\n# Curvature scaling signed (CSV): X, mean_kappa, se_kappa, seed, sign_id")
        seed_val = 77
        for x, mu, se, sgn in zip(Xs, Ys, Yse, sign_id):
            print(f"{x:.6f},{mu:.8f},{se:.8f},{seed_val:d},{int(sgn)}")

        # 3) Stability band (dose-controlled write→decay with discriminative metrics)
        rows = run_stability_band(
            nx=21, ny=21, T_write=5.0, T_decay=5.0, dt=0.2,
            da_values=(0.5, 1.0, 1.5, 2.0), gamma_fixed=1.0, dose_model="scale_R",
            delta_values=(0.05, 0.1, 0.2, 0.3),
            kappa_values=(0.1, 0.3, 0.6, 1.0),
            topk_frac=0.05, cfl_limit=0.9
        )
        print("\n# Stability band (CSV|dose_model=scale_R): D_a, Lambda, Gamma, Retention, Fidelity_w, Fidelity_end, Fidelity_shuffle_end, Fidelity_edge_end, AUC_end, SNR_end, AUPRC_topk, BPER")
        for (Da, Lam, Gam, Ret, Fid_w, Fid_e, Fid_s, Fid_edge, AUC_e, SNR_e, APk, BPER) in rows:
            print(f"{Da:.6f},{Lam:.6f},{Gam:.6f},{Ret:.6f},{Fid_w:.6f},{Fid_e:.6f},{Fid_s:.6f},{Fid_edge:.6f},{AUC_e:.6f},{SNR_e:.6f},{APk:.6f},{BPER:.6f}")

    if csv_out:
        os.makedirs(os.path.dirname(csv_out), exist_ok=True)

        class Tee:
            def __init__(self, *streams):
                self.streams = streams
            def write(self, data):
                for s in self.streams:
                    try:
                        s.write(data)
                    except Exception:
                        pass
            def flush(self):
                for s in self.streams:
                    try:
                        s.flush()
                    except Exception:
                        pass

        with open(csv_out, "w") as f:
            tee = Tee(sys.stdout, f)
            with contextlib.redirect_stdout(tee):
                _produce()
    else:
        _produce()


if __name__ == "__main__":
    main()