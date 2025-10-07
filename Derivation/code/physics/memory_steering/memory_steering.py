"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Memory-driven steering on graphs: rigorous mapping to the FUM derivations + dimensionless implementation.

How this maps to your derivations (clickable refs):
- Fast φ-sector (propagation + mass gap): the continuum equation and invariants are already derived
  in [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:121-128), with vacuum
  v = 1 − β/α and excitation mass m_eff² = α − β. The kinetic normalization c² = 2 J a² comes
  from the discrete action in [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:121-128).
  This module does not alter those results. φ governs propagation/modes; “memory” M biases routing.

- Steering law (geometric optics/ray limit): documented and derived in
  [derivation/memory_steering.md](derivation/memory_steering.md:1) from Voxtrium’s note
  [derivation/voxtrium/voxtrium_message.txt](derivation/voxtrium/voxtrium_message.txt:1).
  Define an index n(x,t) = exp[η M(x,t)]; then rays bend toward memory gradients:
      r'' = ∇_⊥ ln n = η ∇_⊥ M.
  Here r'' is the curvature of the path, ∇_⊥ is the transverse gradient, and η is a coupling.

- Memory dynamics (slow field): the minimal causal PDE
      ∂_t M = γ R − δ M + κ ∇² M,
  where R is a usage/co-activation rate (e.g., STDP proxy), γ is write gain, δ decay, κ consolidation/spread.
  This produces stored structure that later steers dynamics via n=exp(η M).

- Dimensionless groups (scaling, not units) with chosen rulers L, T, M0, R0:
      Θ = η M0,    D_a = γ R0 T / M0,    Λ = δ T,    Γ = κ T / L².
  In [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:44-80) the φ-sector uses (a, τ);
  you can set L=a, T=τ for a shared ruler so this steering layer aligns with the φ units map.

- Predictions (used for the tests in utils):
  • Junction choice:     P(A) ≈ σ(Θ Δm)   (logistic in Θ Δm at a fork)
  • Curvature scaling:   κ_path ∝ Θ |∇_⊥ m|
  • Stability band:      robust memory when D_a ≳ Λ; Γ too low → brittle; Γ too high → washed out
  See [derivation/memory_steering.md](derivation/memory_steering.md:1) for the full statement.

Graph discretization used here (orthogonal to φ):
- We represent M on nodes (vector m), and use the unnormalized graph Laplacian L = D − A to discretize ∇².
- Memory PDE (Euler step):  m ← m + dt ( γ r − δ m − κ L m ), where r is an independently measured usage proxy.
- Steering at node i toward neighbor j is modeled by a softmax over neighbor memory:
      P(i→j) ∝ exp(Θ m_j).
  At a two-branch junction this reduces to the logistic P(A)=σ(Θ Δm), matching the prediction.

What this module provides:
- build_graph_laplacian(A): compute L = D − A (undirected).
- update_memory(m, r, L, gamma, delta, kappa, dt): Euler step for the memory PDE (slow M-dynamics).
- transition_probs(i, neighbors, m, theta): softmax steering P(i→j) ∝ exp(Θ m_j).
- transition_probs_temp(i, neighbors, m, theta, temperature=1.0): temperatured softmax (default T=1).
- sample_next_neighbor(...): sample a neighbor according to transition_probs.
- sample_next_neighbor_heading(i, neighbors, m, theta, pos, heading, heading_bias=2.0, temperature=1.0, rng=None):
  heading-aware sampler for graphs with coordinates pos[N,d]; score_j = Θ m_j + heading_bias cos∠(heading, step_ij), softmax at T.
- compute_dimensionless_groups(eta, M0, gamma, R0, T, delta, kappa, L_scale): (Θ, D_a, Λ, Γ).
- y_junction_adjacency(...), collect_junction_choices(...): helpers to generate the logistic junction dataset.

Use with the experiments runner:
- See [fum_rt/utils/memory_steering_experiments.py](fum_rt/utils/memory_steering_experiments.py:1), which generates three
  datasets/plots for the predictions above (junction logistic, curvature scaling, stability band).

Author: Justin K. Lietz
Date: 2025-08-09
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np


def build_graph_laplacian(A: np.ndarray) -> np.ndarray:
    """
    Build the unnormalized graph Laplacian L = D − A (continuum analogue of −∇²).
    This is the standard discrete operator used in the memory PDE ∂_t m = γ r − δ m − κ L m,
    mapping directly to the ∇² term in [derivation/memory_steering.md](derivation/memory_steering.md:1).

    Args:
        A: np.ndarray (N x N). Nonzero → edge; diagonal should be zero. Ensure symmetry for undirected graphs.

    Returns:
        L: np.ndarray (N x N) Laplacian.

    Notes:
        - L = D − A is the unnormalized Laplacian (Dirichlet energy), which converges to −∇² under mesh refinement.
        - Self-loops are ignored (diagonal set to 0 in degree).
    """
    A = np.asarray(A)
    # Ensure zero diagonal in degree calculation
    deg = np.sum((A != 0) & (~np.eye(A.shape[0], dtype=bool)), axis=1).astype(np.float64)
    D = np.diag(deg)
    L = D - (A != 0).astype(np.float64)
    return L


def update_memory(
    m: np.ndarray,
    r: np.ndarray,
    L: np.ndarray,
    gamma: float,
    delta: float,
    kappa: float,
    dt: float,
) -> np.ndarray:
    """
    One explicit Euler step for the slow memory PDE (write–decay–spread),
        ∂_t m = γ r − δ m − κ L m,
    which is the graph-discretized form of ∂_t M = γ R − δ M + κ ∇² M in
    [derivation/memory_steering.md](derivation/memory_steering.md:1).

    Args:
        m: np.ndarray (N,). Memory field (dimensionless m = M/M0 if normalized to M0).
        r: np.ndarray (N,). Independent usage/co-activation proxy (dimensionless ρ = R/R0 if normalized to R0).
        L: np.ndarray (N x N). Graph Laplacian L = D − A.
        gamma, delta, kappa: PDE coefficients (map to D_a, Λ, Γ via compute_dimensionless_groups).
        dt: time step.

    Returns:
        m_next: updated memory field.

    Stability note:
        Explicit Euler requires dt small enough relative to (delta, kappa·λ_max(L)) for stability.
    """
    m = np.asarray(m, dtype=np.float64)
    r = np.asarray(r, dtype=np.float64)
    dm = gamma * r - delta * m - kappa * (L @ m)
    return m + dt * dm


def transition_probs(
    i: int,
    neighbors: Sequence[int],
    m: np.ndarray,
    theta: float,
) -> np.ndarray:
    """
    Softmax steering probabilities from node i toward its neighbors based on memory values:
        P(i→j) ∝ exp(Θ m_j),   Θ = η M0.
    At a 2-branch fork with memories (m_A, m_B) this reduces to the logistic
        P(A) = σ(Θ (m_A − m_B)),
    matching the prediction P(A) ≈ σ(Θ Δm) in [derivation/memory_steering.md](derivation/memory_steering.md:1).

    Args:
        i: current node index (unused; included for symmetry/extension).
        neighbors: iterable of neighbor node indices of i.
        m: np.ndarray (N,). Memory field (dimensionless).
        theta: dimensionless Θ (steering strength).

    Returns:
        probs: np.ndarray (len(neighbors),) summing to 1.0

    Notes:
        - Numerically stable softmax using max-subtraction.
        - If neighbors is empty, returns an empty array.
    """
    neigh = np.asarray(list(neighbors), dtype=int)
    if neigh.size == 0:
        return np.empty((0,), dtype=np.float64)

    z = theta * m[neigh]
    z = z - np.max(z)
    exps = np.exp(z)
    s = exps.sum()
    # Guard division by zero in pathological cases
    if s <= 0.0 or not np.isfinite(s):
        # fallback: uniform
        return np.ones_like(exps) / exps.size
    return exps / s


def transition_probs_temp(
    i: int,
    neighbors: Sequence[int],
    m: np.ndarray,
    theta: float,
    temperature: float = 1.0,
) -> np.ndarray:
    """
    Temperatured softmax steering probabilities:
        P(i→j) ∝ exp((Θ m_j) / T) with T = temperature.

    Notes:
    - T → 0 narrows to argmax; T → ∞ flattens to uniform.
    - Numerically stabilized with max-subtraction.
    - Keeps the original transition_probs() unchanged for backward compatibility.

    Args:
        i: current node (unused; placeholder for symmetry/extension).
        neighbors: iterable of neighbor node indices of i.
        m: memory field (dimensionless).
        theta: Θ (steering strength).
        temperature: softmax temperature T (dimensionless), default 1.0.

    Returns:
        probs over neighbors (sums to 1), or empty if neighbors empty.
    """
    neigh = np.asarray(list(neighbors), dtype=int)
    if neigh.size == 0:
        return np.empty((0,), dtype=np.float64)

    T = float(temperature) if np.isfinite(temperature) and temperature > 0 else 1.0
    z = (theta * m[neigh]) / T
    z = z - np.max(z)
    exps = np.exp(z)
    s = exps.sum()
    if s <= 0.0 or not np.isfinite(s):
        return np.ones_like(exps) / exps.size
    return exps / s


def sample_next_neighbor_heading(
    i: int,
    neighbors: Sequence[int],
    m: np.ndarray,
    theta: float,
    pos: np.ndarray,
    heading: np.ndarray,
    heading_bias: float = 2.0,
    temperature: float = 1.0,
    rng: Optional[np.random.Generator] = None,
) -> Optional[int]:
    """
    Heading-aware neighbor sampler for graphs with coordinates.

    Score for each neighbor j:
        score_j = Θ m_j + heading_bias * cos(∠(heading, step_ij))
    with step_ij = pos[j] − pos[i] and softmax at temperature T.

    This approximates the ray-limit routing r'' ∝ Θ ∇_⊥ m with an inertial heading term,
    reducing grid-quantization artifacts seen with purely memory-driven argmax hopping.

    Args:
        i: current node index.
        neighbors: iterable of neighbor indices of i.
        m: memory field (dimensionless).
        theta: Θ (steering strength).
        pos: positions array of shape (N, d) giving coordinates for nodes.
        heading: current unit heading vector in R^d (will be renormalized defensively).
        heading_bias: ξ, weight of the heading alignment term.
        temperature: softmax temperature T.
        rng: optional numpy Generator.

    Returns:
        neighbor index sampled according to temperatured, heading-aware softmax; or None if no neighbors.

    Requirements:
        - pos must provide geometric coordinates for all nodes; otherwise, use transition_probs[_temp] instead.
    """
    neigh = np.asarray(list(neighbors), dtype=int)
    if neigh.size == 0:
        return None

    pos = np.asarray(pos, dtype=np.float64)
    if pos.ndim != 2 or i < 0 or i >= pos.shape[0]:
        # Fallback to temperatured memory-only softmax if no usable geometry
        p = transition_probs_temp(i, neigh, m, theta, temperature=temperature)
        if rng is None: rng = np.random.default_rng()
        idx = int(rng.choice(neigh.size, p=p))
        return int(neigh[idx])

    h = np.asarray(heading, dtype=np.float64)
    hn = np.linalg.norm(h)
    h = h / hn if (hn > 0 and np.isfinite(hn)) else np.zeros_like(pos[0])

    scores = []
    pi = pos[i]
    for j in neigh:
        # direction from i to j
        v = np.asarray(pos[j], dtype=np.float64) - pi
        nv = float(np.linalg.norm(v))
        if nv <= 0.0 or not np.isfinite(nv):
            cosang = 0.0
        else:
            u = v / nv
            cosang = float(np.clip(np.dot(u, h), -1.0, 1.0))
        scores.append(theta * float(m[j]) + float(heading_bias) * cosang)

    T = float(temperature) if np.isfinite(temperature) and temperature > 0 else 1.0
    z = np.asarray(scores, dtype=np.float64) / T
    z -= np.max(z)
    exps = np.exp(z)
    s = exps.sum()
    if s <= 0.0 or not np.isfinite(s):
        p = np.ones_like(exps) / exps.size
    else:
        p = exps / s

    if rng is None:
        rng = np.random.default_rng()
    idx = int(rng.choice(neigh.size, p=p))
    return int(neigh[idx])


def sample_next_neighbor(
    i: int,
    neighbors: Sequence[int],
    m: np.ndarray,
    theta: float,
    rng: Optional[np.random.Generator] = None,
) -> Optional[int]:
    """
    Sample the next neighbor for a hop from node i using the softmax steering distribution.
    This is the discrete analogue of “rays bend toward ∇M” via n=exp(η M) (see derivation).

    Args:
        i: current node index.
        neighbors: neighbor indices of i.
        m: memory field (dimensionless).
        theta: steering strength Θ.
        rng: optional numpy Generator; if None, uses default.

    Returns:
        neighbor index or None if no neighbors.
    """
    neigh = np.asarray(list(neighbors), dtype=int)
    if neigh.size == 0:
        return None
    p = transition_probs(i, neigh, m, theta)
    if rng is None:
        rng = np.random.default_rng()
    idx = int(rng.choice(neigh.size, p=p))
    return int(neigh[idx])


def compute_dimensionless_groups(
    eta: float,
    M0: float,
    gamma: float,
    R0: float,
    T: float,
    delta: float,
    kappa: float,
    L_scale: float,
) -> Tuple[float, float, float, float]:
    """
    Compute the four dimensionless groups (Θ, D_a, Λ, Γ) that control the steering+memory dynamics.

    Definitions (see [derivation/memory_steering.md](derivation/memory_steering.md:1)):
        Θ = η M0,   D_a = γ R0 T / M0,   Λ = δ T,   Γ = κ T / L².

    Args:
        eta, M0: coupling and memory scale (produce Θ).
        gamma, R0, T, delta, kappa: PDE parameters and scales (produce D_a, Λ, Γ).
        L_scale: spatial length scale L (use a for φ-map alignment).

    Returns:
        (Theta, D_a, Lambda, Gamma)
    """
    Theta = eta * float(M0)
    Da = (gamma * R0 * T) / float(M0) if M0 != 0 else np.inf
    Lam = delta * T
    Gam = (kappa * T) / (L_scale ** 2) if L_scale != 0 else np.inf
    return (float(Theta), float(Da), float(Lam), float(Gam))


def y_junction_adjacency(
    len_in: int = 5,
    len_a: int = 5,
    len_b: int = 5,
) -> Tuple[np.ndarray, int, int, int]:
    """
    Construct a simple undirected Y-junction adjacency (for P(A)=σ(Θ Δm) tests).

    Topology:
      chain_in (0 ... len_in-1) feeds into a junction node J,
      which then splits into branch A (JA_1 ... JA_len_a)
      and branch B (JB_1 ... JB_len_b).

    Returns:
        A: adjacency (N x N) dense binary
        j: junction node index
        a0: first node on branch A
        b0: first node on branch B
    """
    # index layout: in: 0..len_in-1, J: len_in, A: len_in+1..+len_a, B: subsequent
    J = len_in
    a_start = J + 1
    b_start = J + 1 + len_a
    N = len_in + 1 + len_a + len_b
    A = np.zeros((N, N), dtype=np.int8)

    # inbound chain
    for t in range(1, len_in):
        A[t - 1, t] = 1
        A[t, t - 1] = 1
    # connect inbound tail to junction
    if len_in > 0:
        A[len_in - 1, J] = 1
        A[J, len_in - 1] = 1

    # branch A
    last = J
    for k in range(len_a):
        n = a_start + k
        A[last, n] = 1
        A[n, last] = 1
        last = n

    # branch B
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
    """
    Collect Bernoulli choices at a Y-junction under softmax steering to empirically test
    P(A) ≈ σ(Θ Δm). This function is used by the experiment runner to produce the logistic
    collapse plot and fit.

    Args:
        A: adjacency (dense binary)
        m: memory field (dimensionless)
        J: junction node index
        a_next: first node on branch A
        b_next: first node on branch B
        theta: Θ
        trials: number of samples
        rng: optional RNG

    Returns:
        (count_A, count_B)
    """
    if rng is None:
        rng = np.random.default_rng()
    # neighbors of junction (exclude inbound if present by user’s choice; here include all)
    neighbors = np.where(A[J] != 0)[0]
    # restrict to branches if explicitly provided
    neighbors = [n for n in neighbors if n in (a_next, b_next)]
    if len(neighbors) != 2:
        # Fallback: use two highest-m_j neighbors if not a clean Y
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
    # Map to (A,B) order if possible
    ca = counts.get(a_next, 0)
    cb = counts.get(b_next, 0)
    return (int(ca), int(cb))