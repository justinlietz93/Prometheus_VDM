from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Cold-scout walkers (Phase D scaffolding).

Design:
- Pure core module under core/cortex. No IO/logging; read-only against connectome.
- Budgeted, uniform "cold" probes that do not depend on the announce bus.
- Emits existing core events for folding:
  - VTTouchEvent(kind="vt_touch") for visited nodes
  - EdgeOnEvent(kind="edge_on") for sampled neighbor edges (best-effort)

Behavior:
- Disabled by default (wired behind ENABLE_COLD_SCOUTS in runtime/Nexus).
- When enabled, keeps strict per-tick budgets.
- Uses only common, safe connectome attributes/methods (N, neighbors/get_neighbors, adj).

Rationale:
- Provides a tiny, constant-cost scout to surface coverage/cohesion signals without scans.
- Events fold into EventDrivenMetrics. This preserves void-dynamics and avoids hot-path scans.

Safety:
- All calls are best-effort with try/except and defensive fallbacks.
- If connectome APIs differ, scouts gracefully degrade to only VT touches or no-ops.
"""

from typing import Any, Iterable, List, Set, Sequence
import random
import math
import numpy as np

from fum_rt.core.proprioception.events import (
    BaseEvent,
    VTTouchEvent,
    EdgeOnEvent,
)


class VoidColdScoutWalker:
    """
    Budgeted, read-only cold-scout walker.

    Parameters:
      - budget_visits: max node visits per tick (emits vt_touch)
      - budget_edges: max neighbor edges sampled per tick (emits edge_on)
      - seed: RNG seed for reproducibility

    Methods:
      - step(connectome, tick) -> list[BaseEvent]
    """

    __slots__ = ("budget_visits", "budget_edges", "rng")

    def __init__(self, budget_visits: int = 0, budget_edges: int = 0, seed: int = 0) -> None:
        self.budget_visits = int(max(0, budget_visits))
        self.budget_edges = int(max(0, budget_edges))
        self.rng = random.Random(int(seed))

    # --------- helpers ---------

    @staticmethod
    def _get_N(C: Any) -> int:
        try:
            N = int(getattr(C, "N", 0))
            if N > 0:
                return N
        except Exception:
            pass
        # Try shape-based fallback (e.g., if C.W is an ndarray/sparse with shape)
        try:
            W = getattr(C, "W", None)
            if W is not None:
                shp = getattr(W, "shape", None)
                if isinstance(shp, (tuple, list)) and len(shp) >= 1:
                    n = int(shp[0])
                    return n if n > 0 else 0
        except Exception:
            pass
        return 0

    @staticmethod
    def _neighbors(C: Any, u: int) -> List[int]:
        # Prefer explicit neighbor methods
        try:
            for meth in ("neighbors", "get_neighbors"):
                fn = getattr(C, meth, None)
                if callable(fn):
                    neigh = fn(int(u))
                    if neigh:
                        try:
                            return [int(x) for x in list(neigh)]
                        except Exception:
                            return []
        except Exception:
            pass
        # Fallback: adjacency mapping
        try:
            adj = getattr(C, "adj", None)
            if isinstance(adj, dict):
                vals = adj.get(int(u), [])
                if isinstance(vals, dict):
                    return [int(x) for x in vals.keys()]
                return [int(x) for x in list(vals)]
        except Exception:
            pass
        return []

    # --------- main API ---------

    def step(self, connectome: Any, tick: int) -> List[BaseEvent]:
        """
        Execute one cold-scout pass with strict budgets, returning events to fold.
        """
        events: List[BaseEvent] = []
        N = self._get_N(connectome)
        if N <= 0:
            return events

        # Node visits - contribute to VT coverage/entropy
        bv = min(self.budget_visits, N)
        visited: Set[int] = set()
        if bv > 0:
            while len(visited) < bv:
                try:
                    visited.add(int(self.rng.randrange(N)))
                except Exception:
                    break
            for u in visited:
                events.append(VTTouchEvent(kind="vt_touch", t=int(tick), token=int(u), w=1.0))

        # Edge samples - contribute to cohesion via union-find
        be = self.budget_edges
        if be > 0:
            trials = 0
            emitted = 0
            max_trials = be * 4  # avoid long loops when degree is low/unavailable
            # Create a stable pool to bias toward visited nodes, else fall back to uniform
            pool: Sequence[int] = tuple(visited) if visited else tuple(range(N))
            while emitted < be and trials < max_trials and pool:
                trials += 1
                try:
                    u = int(self.rng.choice(pool))
                except Exception:
                    break
                neigh = self._neighbors(connectome, u)
                if not neigh:
                    continue
                try:
                    v = int(self.rng.choice(neigh))
                except Exception:
                    continue
                if v == u:
                    continue
                events.append(EdgeOnEvent(kind="edge_on", t=int(tick), u=int(u), v=int(v)))
                emitted += 1

        return events


# ---------------------------- Cold-map Reducer ----------------------------
class ColdMap:
    """
    Persistent, bounded coldness tracker keyed by node id.

    Coldness score (monotonic in idle time, bounded in [0,1)):
        age = max(0, t - last_seen[node])
        score = 1 - 2^(-age / half_life_ticks)

    Snapshot fields:
      - cold_head: top-16 [node_id, score] pairs (most cold first)
      - cold_p95, cold_p99, cold_max: distribution summaries across tracked nodes
    """
    __slots__ = ("head_k", "half_life", "keep_max", "rng", "_last_seen")

    def __init__(self, head_k: int = 256, half_life_ticks: int = 200, keep_max: int | None = None, seed: int = 0) -> None:
        self.head_k = int(max(8, head_k))
        self.half_life = int(max(1, half_life_ticks))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))
        self._last_seen: dict[int, int] = {}

    # ------------- updates -------------

    def touch(self, node: int, tick: int) -> None:
        """
        Record a touch for node at tick. Node ids must be non-negative ints.
        """
        try:
            n = int(node)
            t = int(tick)
        except Exception:
            return
        if n < 0:
            return
        self._last_seen[n] = t
        if len(self._last_seen) > self.keep_max:
            self._prune(t)

    def _prune(self, tick: int) -> None:
        """
        Reduce tracked set to keep_max entries, preferentially dropping the most recently seen nodes.
        Uses sampling to avoid O(N) passes.
        """
        try:
            size = len(self._last_seen)
            if size <= self.keep_max:
                return
            target = size - self.keep_max
            keys = list(self._last_seen.keys())
            sample_size = min(len(keys), max(256, target * 4))
            sample = self.rng.sample(keys, sample_size) if sample_size > 0 else keys
            # Sort sample by recency (most recent first) and drop up to target from this set.
            sample.sort(key=lambda k: self._last_seen.get(k, -10**12), reverse=True)
            to_remove = min(target, len(sample))
            for k in sample[:to_remove]:
                self._last_seen.pop(k, None)
        except Exception:
            # Conservative fallback: random removals until within bound
            while len(self._last_seen) > self.keep_max:
                try:
                    k = self.rng.choice(tuple(self._last_seen.keys()))
                    self._last_seen.pop(k, None)
                except Exception:
                    break

    # ------------- scoring -------------

    def _score(self, age: int) -> float:
        a = max(0, int(age))
        # score in [0, 1): 1 - 2^(-age / half_life)
        try:
            return float(1.0 - math.pow(0.5, float(a) / float(self.half_life)))
        except Exception:
            return 0.0

    # ------------- snapshot -------------

    def snapshot(self, tick: int, head_n: int = 16) -> dict:
        """
        Compute a coldness snapshot at tick.

        Returns:
          {
            "cold_head": list[[node_id, score], ...]           # top head_n by score
            "cold_p95": float,
            "cold_p99": float,
            "cold_max": float,
          }
        """
        try:
            t = int(tick)
        except Exception:
            t = 0

        if not self._last_seen:
            return {"cold_head": [], "cold_p95": 0.0, "cold_p99": 0.0, "cold_max": 0.0}

        # Compute scores for all tracked nodes (bounded by keep_max)
        pairs: List[tuple[int, float]] = []
        for node, ts in self._last_seen.items():
            try:
                age = t - int(ts)
            except Exception:
                age = 0
            s = self._score(age)
            pairs.append((int(node), float(s)))

        # Top head_n by score
        head_n = max(1, min(int(head_n), self.head_k))
        try:
            import heapq as _heapq
            head = _heapq.nlargest(head_n, pairs, key=lambda kv: kv[1])
        except Exception:
            head = sorted(pairs, key=lambda kv: kv[1], reverse=True)[:head_n]

        # Percentiles over full tracked set (bounded)
        vals = [s for _, s in pairs]
        vals.sort()

        def _pct(p: float) -> float:
            if not vals:
                return 0.0
            i = int(max(0, min(len(vals) - 1, round((len(vals) - 1) * p))))
            return float(vals[i])

        p95 = _pct(0.95)
        p99 = _pct(0.99)
        vmax = float(vals[-1]) if vals else 0.0

        head_out: List[List[float]] = [[int(n), float(s)] for n, s in head]
        return {
            "cold_head": head_out,
            "cold_p95": float(p95),
            "cold_p99": float(p99),
            "cold_max": float(vmax),
        }


# ---------------------------- Neuroplasticity (Organism-Native) ----------------------------
class RevGSP:
    """
    REV-GSP learner (class form, organism-native).
    - No IO/logging. Pure numeric state updates on a Substrate-like object.
    - Accepts any 'substrate' exposing:
        synaptic_weights (CSR), eligibility_traces (CSR), neuron_polarities (ndarray)
    """

    def __init__(
        self,
        reward_sigmoid_scale: float = 1.5,
        pi_params: dict | None = None,
        rng_seed: int | None = None,
        max_pairs: int = 2048,
        sample_spikes_cap: int | None = None,
    ) -> None:
        """
        Parameters:
          - reward_sigmoid_scale: gain for eta_effective sigmoid
          - pi_params: base params for PI kernel (a±, tau±)
          - rng_seed: deterministic sampling for budgets
          - max_pairs: hard cap on pre/post spike candidate evaluations per tick
          - sample_spikes_cap: optional cap on filtered spike list (down-sample before pairing)
        """
        self.reward_sigmoid_scale = float(reward_sigmoid_scale)
        self.pi_params = pi_params or {'a_plus_base': 0.1, 'a_minus_base': 0.1, 'tau_plus_base': 20.0, 'tau_minus_base': 20.0}
        self.rng = np.random.default_rng(rng_seed)
        self.max_pairs = int(max(1, int(max_pairs)))
        self.sample_spikes_cap = None if sample_spikes_cap is None else int(max(1, int(sample_spikes_cap)))

    # --- helpers ---
    def _clamped_normal(self, mu: float, sigma: float, lo: float, hi: float) -> float:
        try:
            val = float(self.rng.normal(mu, sigma))
        except Exception:
            val = float(mu)
        if val < lo:
            val = lo
        if val > hi:
            val = hi
        return float(val)

    def _base_pi(self, delta_t: float) -> float:
        a_plus = self._clamped_normal(self.pi_params['a_plus_base'], 0.01, 0.03, 0.07)
        a_minus = self._clamped_normal(self.pi_params['a_minus_base'], 0.01, 0.04, 0.08)
        tau_plus = self._clamped_normal(self.pi_params['tau_plus_base'], 2.0, 18.0, 22.0)
        tau_minus = self._clamped_normal(self.pi_params['tau_minus_base'], 2.0, 18.0, 22.0)
        if delta_t > 0:
            return float(a_plus * math.exp(-delta_t / tau_plus))
        return float(-a_minus * math.exp(delta_t / tau_minus))

    def _eta_effective(self, base_lr: float, total_reward: float) -> float:
        if abs(total_reward) < 1e-10:
            return float(base_lr)
        # 2*sigmoid(k*r)-1 in pure numpy
        k = self.reward_sigmoid_scale
        x = k * float(total_reward)
        mod = 2.0 / (1.0 + math.exp(-x)) - 1.0
        eta_mag = float(base_lr) * (1.0 + mod)
        return float(math.copysign(eta_mag, total_reward))

    @staticmethod
    def _gamma_from_plv(plv: float, base_decay: float = 0.95, sensitivity: float = 0.1) -> float:
        return float(base_decay + sensitivity * (float(plv) - 0.5))

    @staticmethod
    def _temporal_filter(spike_times: list[tuple[int, int]], window_size: int = 5) -> list[tuple[int, float]]:
        if len(spike_times) < window_size:
            return spike_times
        out: list[tuple[int, float]] = []
        for i in range(len(spike_times) - window_size + 1):
            window = spike_times[i : i + window_size]
            avg_time = sum(t for _, t in window) / float(window_size)
            neuron_idx = window[-1][0]
            out.append((neuron_idx, avg_time))
        return out

    @staticmethod
    def _adaptive_window(base_ms: int, max_latency: float) -> int:
        return int(base_ms + float(max_latency))

    @staticmethod
    def _latency_scale(pi_value: float, latency_error: float, max_latency: float) -> float:
        if float(max_latency) > 0.0:
            return float(pi_value) * (1.0 - float(latency_error) / float(max_latency))
        return float(pi_value)

    # --- main API ---
    def adapt(
        self,
        substrate: Any,
        spike_train: list[tuple[int, int]],
        spike_phases: dict,
        learning_rate: float,
        lambda_decay: float,
        total_reward: float,
        plv: float,
        network_latency_estimate: dict,
        time_window_ms: int = 20,
    ) -> tuple[Any, dict]:
        """
        Update substrate in-place using REV-GSP rule; returns (substrate, metrics).
        """
        try:
            from scipy.sparse import lil_matrix  # local import to avoid hard dependency at import-time
        except Exception as _:
            # Cannot operate without scipy
            return substrate, {"eta_effective": 0.0, "gamma": 0.0}

        filtered = self._temporal_filter(spike_train)
        win = self._adaptive_window(int(time_window_ms), float(network_latency_estimate.get('max', 0.0)))

        # Optional down-sample of filtered spikes to respect complexity cap
        if self.sample_spikes_cap is not None and len(filtered) > self.sample_spikes_cap:
            try:
                idx = self.rng.choice(len(filtered), size=self.sample_spikes_cap, replace=False)
                filtered = [filtered[int(i)] for i in idx]
            except Exception:
                # fallback: simple head slice
                filtered = filtered[: self.sample_spikes_cap]

        W = getattr(substrate, "synaptic_weights", None)
        E = getattr(substrate, "eligibility_traces", None)
        P = getattr(substrate, "neuron_polarities", None)
        if W is None or E is None or P is None:
            return substrate, {"eta_effective": 0.0, "gamma": 0.0}

        # Build PI sparsely
        try:
            shape = W.shape
        except Exception:
            shape = (0, 0)
        PI = lil_matrix(shape, dtype=np.float32)

        # Budgeted pair evaluation to ensure sub-quadratic behavior
        pairs_evaluated = 0
        break_outer = False
        for pre_neuron, pre_time in filtered:
            if break_outer:
                break
            for post_neuron, post_time in filtered:
                if pre_neuron == post_neuron:
                    continue
                try:
                    # Quick existence check (CSR O(1) average)
                    if W[pre_neuron, post_neuron] == 0:
                        continue
                    delta_t = float(post_time) - float(pre_time)
                    if 0.0 < abs(delta_t) < float(win):
                        base_pi = self._base_pi(delta_t)
                        phase_pre = float(spike_phases.get((pre_neuron, int(pre_time)), 0.0))
                        phase_post = float(spike_phases.get((post_neuron, int(post_time)), 0.0))
                        phase_mod = (1.0 + math.cos(phase_pre - phase_post)) * 0.5
                        pi_val = base_pi * phase_mod
                        pi_val = self._latency_scale(pi_val, float(network_latency_estimate.get('error', 0.0)), float(network_latency_estimate.get('max', 0.0)))
                        PI[pre_neuron, post_neuron] += float(pi_val)
                        pairs_evaluated += 1
                        if pairs_evaluated >= self.max_pairs:
                            break_outer = True
                            break
                except Exception:
                    continue

        PI_csr = PI.tocsr()

        # Eligibility update: E = gamma*E + PI
        gamma = self._gamma_from_plv(float(plv))
        try:
            E *= float(gamma)
        except Exception:
            # fallback reconstruct
            E = E.multiply(float(gamma))
        E += PI_csr

        # Row-scale by neuron polarity (CSR-friendly)
        try:
            indptr = E.indptr
            data = E.data
            for i in range(E.shape[0]):
                p = float(P[i])
                if p == 1.0:
                    continue
                start = indptr[i]
                end = indptr[i + 1]
                if end > start:
                    data[start:end] *= p
        except Exception:
            pass

        # Three-factor update
        eta = self._eta_effective(float(learning_rate), float(total_reward))
        try:
            trace_update = E * float(eta)
            decay_update = W * float(lambda_decay)
            dW = trace_update - decay_update
            W += dW
            # clip
            try:
                W.data = np.clip(W.data, -1.0, 1.0)
            except Exception:
                pass
        except Exception:
            pass

        return substrate, {"eta_effective": float(eta), "gamma": float(gamma)}


class GDSPActuator:
    """
    GDSP structural actuator (class form, organism-native).
    - No IO/logging; pure numeric structural modifications on Substrate-like object.
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

            # truncate history
            if len(self.reward_history) > 100:
                self.reward_history = self.reward_history[-100:]
                self.td_error_history = self.td_error_history[-100:]
                self.novelty_history = self.novelty_history[-100:]

            self.timesteps_since_growth += 1

            # encourage growth when topology is stagnant
            if self.timesteps_since_growth > 500 and float(b1_persistence) <= 0.001:
                self.reward_threshold = max(self.min_reward_threshold, self.reward_threshold * 0.95)
                self.td_error_threshold = max(self.min_td_threshold, self.td_error_threshold * 0.95)
                self.novelty_threshold = max(self.min_novelty_threshold, self.novelty_threshold * 0.95)

            # dampen when structural activity is high
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
                target_novelty = max(self.min_novelty_threshold, min(self.max_novelty_threshold, n75))

                self.reward_threshold = 0.95 * self.reward_threshold + 0.05 * target_reward
                self.td_error_threshold = 0.95 * self.td_error_threshold + 0.05 * target_td
                self.novelty_threshold = 0.95 * self.novelty_threshold + 0.05 * target_novelty

        def record_structural_activity(self) -> None:
            self.structural_activity_counter += 1
            self.timesteps_since_growth = 0

    def __init__(self, bridge_budget_nodes: int = 128, bridge_budget_pairs: int = 2048) -> None:
        """
        Parameters:
          - bridge_budget_nodes: max nodes sampled per component when bridging gaps
          - bridge_budget_pairs: max candidate pairs evaluated per repair attempt
        """
        self._thr = GDSPActuator._AdaptiveThresholds()
        # Per-territory histories (keyed by frozenset(indices))
        from collections import deque
        self._reward_hist: dict[frozenset, Any] = {}
        self._td_hist: dict[frozenset, Any] = {}
        self._deque = deque  # for construction
        # Budgets for homeostatic repairs
        self._bridge_nodes = int(max(1, int(bridge_budget_nodes)))
        self._bridge_pairs = int(max(1, int(bridge_budget_pairs)))
        self._rng = np.random.default_rng(0)

    # --- Homeostatic repairs ---
    def _grow_connection_across_gap(self, substrate: Any) -> Any:
        """
        Budgeted gap-bridging:
          - Connected components computed once (O(N+E))
          - Sample up to bridge_budget_nodes per of the two largest components
          - Evaluate up to bridge_budget_pairs candidate pairs by reading eligibility_traces[u,v]
          - Select argmax and connect; avoids O(n1*n2) mask construction
        """
        try:
            from scipy.sparse.csgraph import connected_components
        except Exception:
            return substrate

        n_components, labels = connected_components(csgraph=substrate.synaptic_weights, directed=False, connection='weak')
        if n_components <= 1:
            return substrate

        component_ids, counts = np.unique(labels, return_counts=True)
        if len(counts) < 2:
            return substrate
        idx = np.argsort(counts)[-2:]
        comp1_id, comp2_id = component_ids[idx[0]], component_ids[idx[1]]
        comp1_nodes = np.where(labels == comp1_id)[0]
        comp2_nodes = np.where(labels == comp2_id)[0]

        # Sample nodes to bound work
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

        # Generate candidate pairs (bounded)
        pairs: list[tuple[int, int]] = []
        for u in S1:
            for v in S2:
                if len(pairs) >= self._bridge_pairs:
                    break
                pairs.append((int(u), int(v)))
            if len(pairs) >= self._bridge_pairs:
                break

        # Evaluate eligibility values directly; skip existing edges
        E = substrate.eligibility_traces
        W = substrate.synaptic_weights
        best_val = None
        best_pair = None
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
        W_lil = W.tolil()
        P_lil = substrate.persistent_synapses.tolil()
        W_lil[uu, vv] = 0.01
        P_lil[uu, vv] = True
        substrate.synaptic_weights = W_lil.tocsr()
        substrate.persistent_synapses = P_lil.tocsr()
        return substrate

    @staticmethod
    def _prune_connections_in_locus(substrate: Any, locus_indices: np.ndarray) -> Any:
        try:
            from scipy.sparse import lil_matrix
        except Exception:
            return substrate
        if locus_indices is None or len(locus_indices) == 0:
            return substrate

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
        return substrate

    def trigger_homeostatic_repairs(self, substrate: Any, probe_analysis: dict) -> Any:
        comp_cnt = int(probe_analysis.get("component_count", 1))
        if comp_cnt > 1:
            # Attempt a single budgeted bridge per tick to bound cost
            before = int(substrate.synaptic_weights.nnz)
            substrate = self._grow_connection_across_gap(substrate)
            after = int(substrate.synaptic_weights.nnz)
            # no loop; try again on subsequent ticks if still fragmented

        if float(probe_analysis.get("b1_persistence", 0.0)) > 0.9:
            locus = probe_analysis.get("locus_indices")
            if locus is not None:
                substrate = self._prune_connections_in_locus(substrate, locus)
        return substrate

    # --- Performance-based growth ---
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

        # Reinforcement growth
        if (len(self._reward_hist[tid]) == self._thr.sustained_window_size and
            all(r > self._thr.reward_threshold for r in self._reward_hist[tid])):
            substrate = self._execute_reinforcement_growth(substrate, territory_indices)
            self._thr.record_structural_activity()
            self._reward_hist[tid].clear()

        # Exploratory growth
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
        from scipy.sparse import lil_matrix

        W_lil = substrate.synaptic_weights.tolil()
        E_lil = substrate.eligibility_traces.tolil()

        mask = np.ix_(territory_indices, territory_indices)
        E_sub = E_lil[mask].tocsr()
        if E_sub.nnz > 0:
            thr = float(np.percentile(E_sub.data, 75))
            for i, r in enumerate(territory_indices):
                for j, c in enumerate(territory_indices):
                    try:
                        if W_lil[r, c] != 0 and float(E_lil[r, c]) > thr:
                            W_lil[r, c] = float(W_lil[r, c]) * 1.1
                    except Exception:
                        continue

        substrate.synaptic_weights = W_lil.tocsr()
        return substrate

    @staticmethod
    def _execute_exploratory_growth(substrate: Any, territory_indices: np.ndarray) -> Any:
        if territory_indices is None or len(territory_indices) == 0:
            return substrate
        from scipy.sparse import lil_matrix

        num_neurons = int(getattr(substrate.firing_rates, "shape", [0])[0]) if hasattr(substrate, "firing_rates") else 0
        if num_neurons <= len(territory_indices):
            return substrate

        all_neurons = np.arange(num_neurons, dtype=int)
        external = np.setdiff1d(all_neurons, territory_indices)
        if len(external) == 0:
            return substrate

        W_lil = substrate.synaptic_weights.tolil()
        P_lil = substrate.persistent_synapses.tolil()

        terr_avg = float(np.mean(substrate.firing_rates[territory_indices])) if hasattr(substrate, "firing_rates") else 0.0
        ext_rates = substrate.firing_rates[external] if hasattr(substrate, "firing_rates") else np.zeros_like(external, dtype=float)
        diff = np.abs(ext_rates - terr_avg)
        compat_idx = np.argsort(diff)[: min(5, len(external))]
        compat = external[compat_idx]

        created = 0
        max_new = min(10, len(territory_indices) * max(1, len(compat)) // 4)
        for u in territory_indices[: min(3, len(territory_indices))]:
            for v in compat[: min(2, len(compat))]:
                if created >= max_new:
                    break
                if W_lil[u, v] == 0:
                    W_lil[u, v] = 0.01
                    P_lil[u, v] = True
                    created += 1
                if W_lil[v, u] == 0:
                    W_lil[v, u] = 0.01
                    P_lil[v, u] = True
                    created += 1

        substrate.synaptic_weights = W_lil.tocsr()
        substrate.persistent_synapses = P_lil.tocsr()
        return substrate

    @staticmethod
    def trigger_maintenance_pruning(substrate: Any, T_prune: int, pruning_threshold: float = 0.01) -> Any:
        try:
            from scipy.sparse import csr_matrix
        except Exception:
            return substrate
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
        return substrate

    # Orchestration
    def run(self, substrate: Any, introspection_report: dict | None = None, sie_report: dict | None = None, territory_indices: np.ndarray | None = None, T_prune: int = 100, pruning_threshold: float = 0.01) -> Any:
        b1_persistence = float(introspection_report.get("b1_persistence", 0.0)) if introspection_report else 0.0
        if introspection_report is not None and bool(introspection_report.get("repair_triggered", False)):
            substrate = self.trigger_homeostatic_repairs(substrate, introspection_report)
            self._thr.record_structural_activity()
            return substrate  # highest priority; skip other operations this tick

        if sie_report is not None and territory_indices is not None and len(territory_indices) > 0:
            substrate = self.trigger_performance_growth(substrate, sie_report, territory_indices, b1_persistence)

        substrate = self.trigger_maintenance_pruning(substrate, int(T_prune), float(pruning_threshold))
        return substrate

    @staticmethod
    def status_report(substrate: Any) -> dict:
        try:
            from scipy.sparse.csgraph import connected_components
        except Exception:
            n_components = 1
        else:
            n_components, _ = connected_components(substrate.synaptic_weights, directed=False)
        total_syn = int(substrate.synaptic_weights.nnz)
        total_neu = int(getattr(substrate.firing_rates, "shape", [0])[0]) if hasattr(substrate, "firing_rates") else 0
        avg_deg = float(total_syn / total_neu) if total_neu > 0 else 0.0
        pers = int(substrate.persistent_synapses.nnz) if hasattr(substrate, "persistent_synapses") else 0
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


__all__ = ["VoidColdScoutWalker", "ColdMap", "RevGSP", "GDSPActuator"]