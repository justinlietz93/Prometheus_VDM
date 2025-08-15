"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Global System Components: Active Domain Cartography (ADC) and Self‑Improvement Engine (SIE)
Blueprint References:
- Rule 1: Core Architectural Principle (Parallel Local & Global Systems)
- Rule 3: The Self-Improvement Engine (SIE) and Its Components
- Rule 4.1: Pathology Detection Mechanisms (connectome_entropy input)
- Rule 7: Active Domain Cartography (ADC) with adaptive scheduling
Time Complexity:
- ADC (1D k-means over W): O(N * k * iters) with small k-range and few iterations (subquadratic)
- SIE (per tick updates): O(N + k_states) dominated by simple reductions (subquadratic)
Formulas: documented inline per method docstrings
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict
import numpy as np

# -------------------------------
# Active Domain Cartography (ADC)
# -------------------------------

@dataclass
class ADC:
    """
    Active Domain Cartography (Rule 7)
    - Maps neurons to territories (State S) using a bespoke, efficient process.
    - Scheduling: t_cartography = schedule_base * exp(-alpha * connectome_entropy)
    - Optimization: narrow k search [k_min, max_k]; 1D k-means on node field W
    - Complexity: O(N * k * iters) per trial k; k-range is small; iters small (default 5)
    Parameters:
        k_min: minimum number of territories to consider (>=2)
        max_k: maximum number of territories to consider
        alpha: decay constant for adaptive schedule
        schedule_base: base interval for cartography
        iters: k-means iterations (small constant)
        performance_threshold: cohesion score threshold for reactive adaptation
    """
    k_min: int = 2
    max_k: int = 16
    alpha: float = 0.30
    schedule_base: int = 100_000
    iters: int = 5
    performance_threshold: float = 1e-2
    next_t: int = 0
    last_k: int = 0

    def should_run(self, step: int, connectome_entropy: float) -> bool:
        """Blueprint Rule 7: scheduling. Returns True if step reached next_t."""
        if step >= self.next_t:
            # t_cartography = schedule_base * exp(-alpha * entropy)
            interval = int(max(1, round(self.schedule_base * np.exp(-self.alpha * float(connectome_entropy)))))
            self.next_t = step + interval
            return True
        return False

    @staticmethod
    def _kmeans_1d(x: np.ndarray, k: int, iters: int, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
        """
        1D k-means over x (shape (N,)), returns (centroids, labels)
        Complexity: O(N * k * iters)
        """
        N = x.size
        # Init centroids from quantiles (stable)
        qs = np.linspace(0.0, 1.0, num=k+2, endpoint=True)[1:-1]
        c = np.quantile(x, qs) if k > 1 else np.array([float(np.median(x))], dtype=np.float32)
        c = np.asarray(c, dtype=np.float32)
        labels = np.zeros(N, dtype=np.int32)
        for _ in range(max(1, iters)):
            # Assign
            dist = np.abs(x[:, None] - c[None, :])  # (N,k)
            labels = np.argmin(dist, axis=1).astype(np.int32)
            # Update
            for j in range(k):
                sel = (labels == j)
                if np.any(sel):
                    c[j] = float(np.mean(x[sel]))
        return c, labels

    @staticmethod
    def _cohesion_score(x: np.ndarray, labels: np.ndarray, k: int) -> float:
        """
        Blueprint Rule 7 ('The How'): overall cohesion = mean over territories of inverse intra-variance.
        We use a numerically stable version: mean(1 / (var + eps)).
        """
        eps = 1e-8
        score = 0.0
        for j in range(k):
            sel = (labels == j)
            if not np.any(sel):
                continue
            v = float(np.var(x[sel]))
            score += 1.0 / (v + eps)
        return score / float(max(1, k))

    def run(self, W: np.ndarray, rng: np.random.Generator) -> Tuple[np.ndarray, int, float]:
        """
        Perform cartography over 1D feature W (node field).
        Returns: (territory_ids, k_opt, cohesion_score)
        - Trials k in [k_min, max_k]; pick best by cohesion score (higher is better).
        - Reactive adaptation (Rule 7): if best cohesion below threshold, try k+1 once.
        """
        N = W.size
        k_min = max(2, int(self.k_min))
        k_max = max(k_min, int(self.max_k))
        best = (-np.inf, None, None)  # (score, labels, k)

        for k in range(k_min, min(k_max, N) + 1):
            _, lbl = self._kmeans_1d(W, k, self.iters, rng)
            s = self._cohesion_score(W, lbl, k)
            if s > best[0]:
                best = (s, lbl, k)

        score, labels, k_opt = best
        # Reactive adaptation (bifurcation)
        if score < self.performance_threshold and (k_opt + 1) <= min(k_max, N):
            _, lbl = self._kmeans_1d(W, k_opt + 1, self.iters, rng)
            s2 = self._cohesion_score(W, lbl, k_opt + 1)
            if s2 > score:
                score, labels, k_opt = s2, lbl, k_opt + 1

        self.last_k = int(k_opt)
        return labels.astype(np.int32), self.last_k, float(score)


# -----------------------------------
# Self‑Improvement Engine (SIE) Rule 3
# -----------------------------------

@dataclass
class SIE:
    """
    Self‑Improvement Engine (Rule 3)
    total_reward = w_td * TD_error_norm + w_nov * novelty_norm - w_hab * habituation_norm + w_hsi * hsi_norm
    State:
        V_states: value function per territory id (dense vector sized on demand)
        visit_counts: visitation counts per territory (for novelty/habituation)
    Complexity:
        Per tick: O(N) to aggregate territory stats (+ O(k_states) bookkeeping)
    """
    w_td: float = 0.35
    w_nov: float = 0.25
    w_hab: float = 0.15
    w_hsi: float = 0.25
    alpha: float = 0.10  # value function learning rate
    gamma: float = 0.95  # discount for TD
    target_var: float = 0.05  # target firing variance for HSI

    V_states: Dict[int, float] = field(default_factory=dict)
    visit_counts: Dict[int, int] = field(default_factory=dict)
    last_state: Optional[int] = None
    last_value: float = 0.0

    def _ensure_state(self, s: int):
        if s not in self.V_states:
            self.V_states[s] = 0.0
        if s not in self.visit_counts:
            self.visit_counts[s] = 0

    @staticmethod
    def _normalize(z: float) -> float:
        # Map arbitrary scalar to [-1, 1] with tanh
        return float(np.tanh(z))

    def _hsi_norm(self, W: np.ndarray) -> float:
        """
        Homeostatic Stability Index (proxy): 1 - |var(W) - target| / (target + eps), clipped to [-1,1]
        Cheap O(N) measure aligned with Rule 3 inputs.
        """
        eps = 1e-8
        v = float(np.var(W))
        diff = abs(v - self.target_var) / (self.target_var + eps)
        return float(np.clip(1.0 - diff, -1.0, 1.0))

    def compute(self, territories: Optional[np.ndarray], W: np.ndarray, external_R: Optional[float] = None) -> Dict[str, float]:
        """
        Compute SIE components and total_reward.
        Inputs:
            territories: array of length N with territory id per neuron (from ADC). If None, uses a single implicit state 0.
            W: node field (for HSI proxy)
            external_R: optional external reward R_t
        Returns dict with components and total_reward.
        """
        if territories is None or territories.size == 0:
            # Single territory fallback
            S_t = 0
            terr_ids = np.array([0], dtype=np.int32)
        else:
            # Choose current territory by majority (cheap proxy)
            # In future wire from UTE stream tagging
            vals, counts = np.unique(territories, return_counts=True)
            S_t = int(vals[np.argmax(counts)])
            terr_ids = vals.astype(np.int32)

        # Ensure state containers
        self._ensure_state(S_t)

        # Novelty/Habituation from visitation counts
        n_vis = self.visit_counts.get(S_t, 0)
        novelty_norm = self._normalize(1.0 / np.sqrt(max(1, n_vis)))
        habituation_norm = self._normalize(n_vis / (n_vis + 10.0))  # increases with repeated visits

        # HSI from W variance
        hsi_norm = self._hsi_norm(W)

        # TD error for current state (no external reward by default)
        R_t = 0.0 if external_R is None else float(external_R)
        V_s = self.V_states.get(S_t, 0.0)
        V_next = V_s  # single-state proxy unless territories change next tick

        # If previous state differs, approximate bootstrapping using its value
        if self.last_state is not None and self.last_state != S_t:
            V_next = self.V_states.get(self.last_state, 0.0)

        td_error = R_t + self.gamma * V_next - V_s
        # Normalize TD error to [-1,1] via tanh
        TD_error_norm = self._normalize(td_error)

        # Update value function
        self.V_states[S_t] = V_s + self.alpha * td_error

        # Update visit counts
        self.visit_counts[S_t] = n_vis + 1

        # Total reward per Rule 3
        total_reward = (
            self.w_td * TD_error_norm
            + self.w_nov * novelty_norm
            - self.w_hab * habituation_norm
            + self.w_hsi * hsi_norm
        )

        # Track last
        self.last_state = S_t
        self.last_value = self.V_states[S_t]

        return {
            "S_t": float(S_t),
            "TD_error_norm": float(TD_error_norm),
            "novelty_norm": float(novelty_norm),
            "habituation_norm": float(habituation_norm),
            "hsi_norm": float(hsi_norm),
            "total_reward": float(total_reward),
        }