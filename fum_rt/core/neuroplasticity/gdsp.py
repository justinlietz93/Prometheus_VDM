from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Module: fum_rt.core.neuroplasticity.gdsp
Purpose: Organism-native GDSP structural actuator with budgeted, territory-scoped, sparse-masked operations.

Design constraints
- One class per file; pure core; no IO/logging; NumPy + SciPy only.
- Budgeted algorithms:
  - Repairs: component-bridging with node/pair caps (no global mask sweeps).
  - Growth: reinforcement within territory by eligibility percentile; exploratory via similarity+eligibility prefilter.
  - Pruning: timer-based over weak, non-persistent synapses with CSR-safe operations.
"""

from typing import Any
import numpy as np


class GDSPActuator:
    """
    Goal-Directed Structural Plasticity (GDSP) actuator.

    - Homeostatic repairs (fragmentation healing; locus pruning)
    - Performance-driven growth (reinforcement, exploratory)
    - Maintenance pruning (weak, non-persistent synapses over time)

    Budget controls:
      bridge_budget_nodes: sample cap per component for gap bridging
      bridge_budget_pairs: max candidate (u,v) eligibility checks per tick
    """

    class _AdaptiveThresholds:
        def __init__(self) -> None:
            self.reward_threshold = 0.8
            self.td_error_threshold = 0.5
            self.novelty_threshold = 0.7
            self.sustained_window_size = 10

            self.structural_activity_counter = 0
            self.timesteps_since_growth = 0

            self.min_reward_threshold = 0.3
            self.max_reward_threshold = 0.9
            self.min_td_threshold = 0.1
            self.max_td_threshold = 0.8
            self.min_novelty_threshold = 0.2
            self.max_novelty_threshold = 0.9

            self.reward_history: list[float] = []
            self.td_error_history: list[float] = []
            self.novelty_history: list[float] = []

        def update_and_adapt(self, sie_report: dict, b1_persistence: float) -> None:
            self.reward_history.append(float(sie_report.get("total_reward", 0.0)))
            self.td_error_history.append(float(sie_report.get("td_error", 0.0)))
            self.novelty_history.append(float(sie_report.get("novelty", 0.0)))

            # truncate
            if len(self.reward_history) > 100:
                self.reward_history = self.reward_history[-100:]
                self.td_error_history = self.td_error_history[-100:]
                self.novelty_history = self.novelty_history[-100:]

            self.timesteps_since_growth += 1

            # encourage growth when stagnant
            if self.timesteps_since_growth > 500 and float(b1_persistence) <= 0.001:
                self.reward_threshold = max(self.min_reward_threshold, self.reward_threshold * 0.95)
                self.td_error_threshold = max(self.min_td_threshold, self.td_error_threshold * 0.95)
                self.novelty_threshold = max(self.min_novelty_threshold, self.novelty_threshold * 0.95)

            # dampen when activity is high
            elif self.structural_activity_counter > 20:
                self.reward_threshold = min(self.max_reward_threshold, self.reward_threshold * 1.05)
                self.td_error_threshold = min(self.max_td_threshold, self.td_error_threshold * 1.05)
                self.novelty_threshold = min(self.max_novelty_threshold, self.novelty_threshold * 1.05)
                self.structural_activity_counter = 0

            # statistical adaptation
            if len(self.reward_history) >= 50:
                r75 = float(np.percentile(self.reward_history, 75))
                td90 = float(np.percentile(self.td_error_history, 90))
                n75 = float(np.percentile(self.novelty_history, 75))

                target_reward = max(self.min_reward_threshold, min(self.max_reward_threshold, r75))
                target_td = max(self.min_td_threshold, min(self.max_td_threshold, td90))
                target_nov = max(self.min_novelty_threshold, min(self.max_novelty_threshold, n75))

                self.reward_threshold = 0.95 * self.reward_threshold + 0.05 * target_reward
                self.td_error_threshold = 0.95 * self.td_error_threshold + 0.05 * target_td
                self.novelty_threshold = 0.95 * self.novelty_threshold + 0.05 * target_nov

        def record_structural_activity(self) -> None:
            self.structural_activity_counter += 1
            self.timesteps_since_growth = 0

    def __init__(self, bridge_budget_nodes: int = 128, bridge_budget_pairs: int = 2048, rng_seed: int = 0) -> None:
        self._thr = GDSPActuator._AdaptiveThresholds()
        # Per-territory histories (keyed by frozenset(indices))
        from collections import deque
        self._reward_hist: dict[frozenset, Any] = {}
        self._td_hist: dict[frozenset, Any] = {}
        self._deque = deque  # constructor for deques

        # Budgets for homeostatic repairs
        self._bridge_nodes = int(max(1, int(bridge_budget_nodes)))
        self._bridge_pairs = int(max(1, int(bridge_budget_pairs)))
        self._rng = np.random.default_rng(int(rng_seed))

    # ---------------- Homeostatic repairs ----------------

    def _grow_connection_across_gap(self, substrate: Any) -> Any:
        """
        Bridge a topological gap by adding a single best edge evaluated under strict budgets.
        - Compute connected components once (O(N+E)).
        - Sample up to _bridge_nodes from each of the two largest components.
        - Evaluate up to _bridge_pairs candidate pairs by reading eligibility_traces[u,v].
        """
        try:
            from scipy.sparse.csgraph import connected_components
        except Exception:
            return substrate

        try:
            W = substrate.synaptic_weights
            E = substrate.eligibility_traces
        except Exception:
            return substrate

        n_components, labels = connected_components(csgraph=W, directed=False, connection="weak")
        if n_components <= 1:
            return substrate

        component_ids, counts = np.unique(labels, return_counts=True)
        if len(counts) < 2:
            return substrate
        idx = np.argsort(counts)[-2:]
        comp1_id, comp2_id = component_ids[idx[0]], component_ids[idx[1]]
        comp1_nodes = np.where(labels == comp1_id)[0]
        comp2_nodes = np.where(labels == comp2_id)[0]

        # Sample bounded node sets
        k1 = min(len(comp1_nodes), self._bridge_nodes)
        k2 = min(len(comp2_nodes), self._bridge_nodes)
        if k1 == 0 or k2 == 0:
            return substrate

        try:
            s1_idx = self._rng.choice(len(comp1_nodes), size=k1, replace=False)
            s2_idx = self._rng.choice(len(comp2_nodes), size=k2, replace=False)
            S1 = comp1_nodes[s1_idx]
            S2 = comp2_nodes[s2_idx]
        except Exception:
            S1 = comp1_nodes[:k1]
            S2 = comp2_nodes[:k2]

        # Generate candidate pairs within cap
        pairs: list[tuple[int, int]] = []
        for u in S1:
            for v in S2:
                if len(pairs) >= self._bridge_pairs:
                    break
                pairs.append((int(u), int(v)))
            if len(pairs) >= self._bridge_pairs:
                break

        best_val = None
        best_pair: tuple[int, int] | None = None
        for (u, v) in pairs:
            try:
                if W[u, v] != 0:
                    continue
                val = float(E[u, v])
                if best_val is None or val > best_val:
                    best_val = val
                    best_pair = (u, v)
            except Exception:
                continue

        if best_pair is None:
            return substrate

        uu, vv = best_pair
        try:
            W_lil = W.tolil()
            P_lil = substrate.persistent_synapses.tolil()
            W_lil[uu, vv] = 0.01
            P_lil[uu, vv] = True
            substrate.synaptic_weights = W_lil.tocsr()
            substrate.persistent_synapses = P_lil.tocsr()
        except Exception:
            pass
        return substrate

    @staticmethod
    def _prune_connections_in_locus(substrate: Any, locus_indices: np.ndarray) -> Any:
        if locus_indices is None or len(locus_indices) == 0:
            return substrate
        try:
            locus_mask = np.ix_(locus_indices, locus_indices)
            locus_weights_csr = substrate.synaptic_weights[locus_mask]
            if locus_weights_csr.nnz == 0:
                return substrate
            min_idx = int(np.argmin(np.abs(locus_weights_csr.data)))
            rows, cols = locus_weights_csr.nonzero()
            global_row = int(locus_indices[rows[min_idx]])
            global_col = int(locus_indices[cols[min_idx]])

            W = substrate.synaptic_weights.tolil()
            W[global_row, global_col] = 0
            substrate.synaptic_weights = W.tocsr()
        except Exception:
            pass
        return substrate

    def trigger_homeostatic_repairs(self, substrate: Any, probe_analysis: dict) -> Any:
        comp_cnt = int(probe_analysis.get("component_count", 1))
        # Attempt a single budgeted bridge per tick to bound cost
        if comp_cnt > 1:
            before = int(getattr(substrate.synaptic_weights, "nnz", 0))
            substrate = self._grow_connection_across_gap(substrate)
            after = int(getattr(substrate.synaptic_weights, "nnz", 0))
            # subsequent ticks will try again if still fragmented

        if float(probe_analysis.get("b1_persistence", 0.0)) > 0.9:
            locus = probe_analysis.get("locus_indices")
            if locus is not None:
                substrate = self._prune_connections_in_locus(substrate, locus)
        return substrate

    # ---------------- Performance-based growth ----------------

    def trigger_performance_growth(self, substrate: Any, sie_report: dict, territory_indices: np.ndarray, b1_persistence: float = 0.0) -> Any:
        self._thr.update_and_adapt(sie_report, b1_persistence)

        if territory_indices is None or len(territory_indices) == 0:
            return substrate
        tid = frozenset(int(i) for i in territory_indices)

        if tid not in self._reward_hist:
            self._reward_hist[tid] = self._deque(maxlen=self._thr.sustained_window_size)
        if tid not in self._td_hist:
            self._td_hist[tid] = self._deque(maxlen=self._thr.sustained_window_size)

        self._reward_hist[tid].append(float(sie_report.get("total_reward", 0.0)))
        self._td_hist[tid].append(float(sie_report.get("td_error", 0.0)))
        novelty = float(sie_report.get("novelty", 0.0))

        # Reinforcement growth: strengthen existing connections with high eligibility
        if (len(self._reward_hist[tid]) == self._thr.sustained_window_size and
            all(r > self._thr.reward_threshold for r in self._reward_hist[tid])):
            substrate = self._execute_reinforcement_growth(substrate, territory_indices)
            self._thr.record_structural_activity()
            self._reward_hist[tid].clear()

        # Exploratory growth: persistent high error + novelty
        if (len(self._td_hist[tid]) == self._thr.sustained_window_size and
            all(e > self._thr.td_error_threshold for e in self._td_hist[tid]) and
            novelty > self._thr.novelty_threshold):
            substrate = self._execute_exploratory_growth(substrate, territory_indices)
            self._thr.record_structural_activity()
            self._td_hist[tid].clear()

        return substrate

    @staticmethod
    def _execute_reinforcement_growth(substrate: Any, territory_indices: np.ndarray) -> Any:
        if territory_indices is None or len(territory_indices) == 0:
            return substrate
        try:
            W_lil = substrate.synaptic_weights.tolil()
            E_lil = substrate.eligibility_traces.tolil()

            mask = np.ix_(territory_indices, territory_indices)
            E_sub = E_lil[mask].tocsr()
            if E_sub.nnz > 0:
                thr = float(np.percentile(E_sub.data, 75))
                for r in territory_indices:
                    for c in territory_indices:
                        try:
                            if W_lil[r, c] != 0 and float(E_lil[r, c]) > thr:
                                W_lil[r, c] = float(W_lil[r, c]) * 1.1
                        except Exception:
                            continue
            substrate.synaptic_weights = W_lil.tocsr()
        except Exception:
            pass
        return substrate

    @staticmethod
    def _execute_exploratory_growth(substrate: Any, territory_indices: np.ndarray) -> Any:
        """
        Exploratory growth (budgeted, territory-scoped, sparse-masked):
          - Prefilter external candidates by firing-rate similarity (cheap)
          - Blend with sparse eligibility hint from territory boundary
          - Pick a tiny top-M set and create bidirectional edges (capped)
        """
        if territory_indices is None or len(territory_indices) == 0:
            return substrate
        try:
            num_neurons = int(getattr(substrate.firing_rates, "shape", [0])[0]) if hasattr(substrate, "firing_rates") else 0
            if num_neurons <= len(territory_indices):
                return substrate

            all_neurons = np.arange(num_neurons, dtype=int)
            external = np.setdiff1d(all_neurons, territory_indices)
            if len(external) == 0:
                return substrate

            W_lil = substrate.synaptic_weights.tolil()
            P_lil = substrate.persistent_synapses.tolil()

            # 1) similarity prefilter
            terr_avg = float(np.mean(substrate.firing_rates[territory_indices])) if hasattr(substrate, "firing_rates") else 0.0
            ext_rates = substrate.firing_rates[external] if hasattr(substrate, "firing_rates") else np.zeros_like(external, dtype=float)
            diff = np.abs(ext_rates - terr_avg)

            prefilter_k = min(64, len(external))
            try:
                pf_idx = np.argpartition(diff, prefilter_k - 1)[:prefilter_k]
            except Exception:
                pf_idx = np.argsort(diff)[:prefilter_k]
            prefilter = external[pf_idx]
            diff_pf = diff[pf_idx]

            # 2) eligibility hint from territory boundary
            try:
                E_sub = substrate.eligibility_traces[territory_indices][:, prefilter]
                elig_hint = np.asarray(E_sub.max(axis=0)).ravel()
            except Exception:
                elig_hint = np.zeros_like(prefilter, dtype=float)

            # blend
            sim = 1.0 / (1.0 + diff_pf)
            try:
                emax = float(np.max(np.abs(elig_hint))) if elig_hint.size else 0.0
            except Exception:
                emax = 0.0
            elig_norm = (elig_hint / (emax + 1e-8)) if emax > 0.0 else np.zeros_like(elig_hint, dtype=float)
            score = 0.7 * sim + 0.3 * elig_norm

            # 3) top-M tiny set
            M = min(8, prefilter_k)
            try:
                chosen_idx = np.argpartition(score, -M)[-M:]
            except Exception:
                chosen_idx = np.argsort(score)[-M:]
            compat = prefilter[chosen_idx]

            # 4) add bidirectional edges under caps
            created = 0
            max_new = min(10, len(territory_indices) * max(1, len(compat)) // 4)
            for u in territory_indices[: min(3, len(territory_indices))]:
                for v in compat[: min(2, len(compat))]:
                    if created >= max_new:
                        break
                    try:
                        if W_lil[u, v] == 0:
                            W_lil[u, v] = 0.01
                            P_lil[u, v] = True
                            created += 1
                        if W_lil[v, u] == 0 and created < max_new:
                            W_lil[v, u] = 0.01
                            P_lil[v, u] = True
                            created += 1
                    except Exception:
                        continue

            substrate.synaptic_weights = W_lil.tocsr()
            substrate.persistent_synapses = P_lil.tocsr()
        except Exception:
            pass
        return substrate

    # ---------------- Maintenance pruning ----------------

    @staticmethod
    def trigger_maintenance_pruning(substrate: Any, T_prune: int, pruning_threshold: float = 0.01) -> Any:
        """
        Increment timers for weak, non-persistent synapses and prune when exceeding T_prune.
        """
        try:
            from scipy.sparse import csr_matrix
            W = substrate.synaptic_weights
            timers = substrate.synapse_pruning_timers.copy()
            P = substrate.persistent_synapses

            weak_mask = np.abs(W.data) < float(pruning_threshold)
            strong_mask = ~weak_mask

            persistent_bool = P.astype(bool)
            weak_mat = csr_matrix((weak_mask, W.nonzero()), shape=W.shape)
            eligible = weak_mat - weak_mat.multiply(persistent_bool)
            timers += eligible

            strong_mat = csr_matrix((strong_mask, W.nonzero()), shape=W.shape)
            timers = timers.multiply(strong_mat.astype(bool) == False)

            prune_mask = timers > int(T_prune)
            pruned = prune_mask.nnz
            if pruned > 0:
                W_lil = W.tolil()
                t_lil = timers.tolil()
                rows, cols = prune_mask.nonzero()
                if rows.size:
                    for r, c in zip(rows, cols):
                        try:
                            W_lil[r, c] = 0
                            t_lil[r, c] = 0
                        except Exception:
                            continue
                substrate.synaptic_weights = W_lil.tocsr()
                substrate.synapse_pruning_timers = t_lil.tocsr()
                substrate.synaptic_weights.eliminate_zeros()
            else:
                substrate.synapse_pruning_timers = timers
        except Exception:
            pass
        return substrate

    # ---------------- Orchestration ----------------

    def run(
        self,
        substrate: Any,
        introspection_report: dict | None = None,
        sie_report: dict | None = None,
        territory_indices: np.ndarray | None = None,
        T_prune: int = 100,
        pruning_threshold: float = 0.01,
    ) -> Any:
        b1_persistence = float(introspection_report.get("b1_persistence", 0.0)) if introspection_report else 0.0
        if introspection_report is not None and bool(introspection_report.get("repair_triggered", False)):
            substrate = self.trigger_homeostatic_repairs(substrate, introspection_report)
            self._thr.record_structural_activity()
            return substrate  # highest priority this tick

        if sie_report is not None and territory_indices is not None and len(territory_indices) > 0:
            substrate = self.trigger_performance_growth(substrate, sie_report, territory_indices, b1_persistence)

        substrate = self.trigger_maintenance_pruning(substrate, int(T_prune), float(pruning_threshold))
        return substrate

    @staticmethod
    def status_report(substrate: Any) -> dict:
        try:
            from scipy.sparse.csgraph import connected_components
            n_components, _ = connected_components(substrate.synaptic_weights, directed=False)
        except Exception:
            n_components = 1
        total_syn = int(getattr(substrate.synaptic_weights, "nnz", 0))
        total_neu = int(getattr(getattr(substrate, "firing_rates", None), "shape", [0])[0]) if hasattr(substrate, "firing_rates") else 0
        avg_deg = float(total_syn / total_neu) if total_neu > 0 else 0.0
        pers = int(getattr(substrate.persistent_synapses, "nnz", 0)) if hasattr(substrate, "persistent_synapses") else 0
        ratio = float(pers / total_syn) if total_syn > 0 else 0.0
        data = getattr(substrate.synaptic_weights, "data", np.array([], dtype=float))
        weight_stats = {
            "mean": float(np.mean(data)) if data.size > 0 else 0.0,
            "std": float(np.std(data)) if data.size > 0 else 0.0,
            "min": float(np.min(data)) if data.size > 0 else 0.0,
            "max": float(np.max(data)) if data.size > 0 else 0.0,
        }
        return {
            "total_neurons": int(total_neu),
            "total_synapses": int(total_syn),
            "persistent_synapses": int(pers),
            "persistent_ratio": float(ratio),
            "average_degree": float(avg_deg),
            "connected_components": int(n_components),
            "connectivity_health": "healthy" if n_components == 1 else "fragmented",
            "gdsp_operational": True,
        }


__all__ = ["GDSPActuator"]
