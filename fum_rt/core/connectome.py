"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import os as _os

# Dense backend is validation-only; forbid import unless FORCE_DENSE is explicitly set.
# This prevents accidental dense usage in runtime paths and enforces sparse-first policy.
if str(_os.getenv("FORCE_DENSE", "0")).strip().lower() not in ("1", "true", "yes", "on", "y", "t"):
    raise RuntimeError("Dense connectome is validation-only. Set FORCE_DENSE=1 to enable for tests.")

import numpy as np
import networkx as nx
from .void_dynamics_adapter import universal_void_dynamics, delta_re_vgsp, delta_gdsp
from .fum_structural_homeostasis import perform_structural_homeostasis
from .announce import Observation  # event schema for ADC bus

# TODO THIS ENTIRE FILE IS DEPRECATED AND WILL NEED TO BE REMOVED. USE /mnt/ironwolf/git/Void_Unity_Proofs/fum_rt/core/sparse_connectome.py
class Connectome:
    def __init__(self, N: int, k: int, seed: int = 0, threshold: float = 0.15, lambda_omega: float = 0.1, candidates: int = 64, structural_mode: str = "alias", traversal_walkers: int = 256, traversal_hops: int = 3, bundle_size: int = 3, prune_factor: float = 0.10):
        self.N = N
        self.k = k
        self.rng = np.random.default_rng(seed)
        self.threshold = threshold  # active synapse threshold on edge weights
        self.lambda_omega = lambda_omega  # penalty weight for structural plasticity (Ω)
        self.candidates = int(max(1, candidates))  # candidate samples per node for structure search
        self.structural_mode = structural_mode      # "alias" (default) | "dense"
        # Node state
        self.W = self.rng.uniform(0.0, 1.0, size=(N,)).astype(np.float32)
        # Start with empty topology; growth is dictated purely by Void Equations
        self.A = np.zeros((N, N), dtype=np.int8)
        # Graph objects are built on demand for visualization/metrics
        self.G = nx.Graph()
        # Edge weights derived from node states initially (zeros)
        self.E = self._edge_weights_from_W()
        # Void‑equation traversal configuration (Blueprint: "void equations for traversal and measuring")
        self.traversal_walkers = int(max(1, traversal_walkers))
        self.traversal_hops = int(max(1, traversal_hops))
        # Findings propagated each tick for Global System consumers (SIE/ADC)
        self.findings = {}
        # Void‑equation traversal configuration (Blueprint: "void equations for traversal and measuring")
        self.traversal_walkers = int(max(1, traversal_walkers))
        self.traversal_hops = int(max(1, traversal_hops))
        # Findings propagated each tick for Global System consumers (SIE/ADC)
        self.findings = {}
        # Local tick counter for announcements (incremented each step)
        self._tick = 0
        # Homeostasis tuning (Blueprint Rule 4/4.1)
        self.bundle_size = int(max(1, bundle_size))
        self.prune_factor = float(max(0.0, prune_factor))
        # External stimulation buffer (deterministic symbol→group)
        self._stim = np.zeros(N, dtype=np.float32)
        self._stim_decay = 0.90

    def _ring_lattice(self, N, k):
        # Each node connected to k nearest neighbors (k must be even)
        k = max(2, k + (k % 2))
        A = np.zeros((N, N), dtype=np.int8)
        for i in range(N):
            for d in range(1, k//2 + 1):
                j = (i + d) % N
                h = (i - d) % N
                A[i, j] = 1
                A[i, h] = 1
        return A

    def _edge_weights_from_W(self):
        # Symmetric edge weights derived from node states
        E = (np.outer(self.W, self.W) * self.A).astype(np.float32)
        return E

    def stimulate_indices(self, idxs, amp: float = 0.05):
        """
        Deterministic stimulus injection:
        - idxs: iterable of neuron indices to stimulate
        - amp: additive boost to the stimulus buffer (decays each tick)
        """
        try:
            if idxs is None:
                return
            idxs = np.asarray(list(set(int(i) % self.N for i in idxs)), dtype=np.int64)
            if idxs.size == 0:
                return
            # accumulate into a decaying stimulus buffer that feeds ReLU(Δalpha)
            self._stim[idxs] = np.clip(self._stim[idxs] + float(amp), 0.0, 1.0)
            # small immediate bump to W to seed associations
            self.W[idxs] = np.clip(self.W[idxs] + 0.01 * float(amp), 0.0, 1.0)
        except Exception:
            # maintain runtime continuity
            pass

    # --- Alias sampler (Vose) to sample candidates ~ ReLU(Δalpha) in O(N) build + O(1) draw ---
    def _build_alias(self, p: np.ndarray):
        n = p.size
        if n == 0:
            return np.array([], dtype=np.float32), np.array([], dtype=np.int32)
        p = p.astype(np.float64, copy=False)
        s = float(p.sum())
        if s <= 0:
            p = np.full(n, 1.0 / n, dtype=np.float64)
        else:
            p = p / s
        prob = np.zeros(n, dtype=np.float64)
        alias = np.zeros(n, dtype=np.int32)
        scaled = p * n
        small = [i for i, v in enumerate(scaled) if v < 1.0]
        large = [i for i, v in enumerate(scaled) if v >= 1.0]
        while small and large:
            s_idx = small.pop()
            l_idx = large.pop()
            prob[s_idx] = scaled[s_idx]
            alias[s_idx] = l_idx
            scaled[l_idx] = scaled[l_idx] - (1.0 - prob[s_idx])
            if scaled[l_idx] < 1.0:
                small.append(l_idx)
            else:
                large.append(l_idx)
        for i in large:
            prob[i] = 1.0
        for i in small:
            prob[i] = 1.0
        return prob.astype(np.float32), alias

    def _alias_draw(self, prob: np.ndarray, alias: np.ndarray, s: int):
        n = prob.size
        if n == 0 or s <= 0:
            return np.array([], dtype=np.int64)
        k = self.rng.integers(0, n, size=s, endpoint=False)
        u = self.rng.random(s)
        choose_alias = (u >= prob[k])
        out = k.copy()
        out[choose_alias] = alias[k[choose_alias]]
        return out.astype(np.int64)

    def _void_traverse(self, a: np.ndarray, om: np.ndarray):
        """
        Continuous void‑equation traversal (Blueprint mandate: use void equations for traversal/measuring)
        - Seeds walkers proportionally to ReLU(Δalpha)
        - Transition weight to neighbor j: max(0, a[i]*a[j] - λ*|ω_i-ω_j|)
        - Simulates small number of hops per walker; accumulates visit histogram
        Complexity: ~O(N*k + walkers*hops). k is current degree bound per node.
        Produces findings propagated to metrics/SIE/ADC: coverage, entropy, unique_nodes, mean_a/omega.
        Also publishes compact Observation events to the ADC bus if present.
        """
        N = self.N
        walkers = self.traversal_walkers
        hops = self.traversal_hops

        # Seed distribution ~ a (ReLU(Δalpha))
        prob, alias = self._build_alias(a)
        seeds = self._alias_draw(prob, alias, walkers)
        visit = np.zeros(N, dtype=np.int32)

        # Optional ADC bus
        bus = getattr(self, "bus", None)
        tick = int(getattr(self, "_tick", 0))

        # Event accumulators (kept small)
        sample_cap = 64
        sel_w_sum = 0.0
        sel_steps = 0
        cycle_events = 0
        sample_nodes = set()

        for s in seeds:
            i = int(s)
            cur = i
            seen = {cur: 0}  # for simple loop detection within this walk
            path = [cur]
            for step_idx in range(1, hops + 1):
                nbrs = np.nonzero(self.A[cur])[0]
                if nbrs.size == 0:
                    break
                # weights by void affinity
                w = a[cur] * a[nbrs] - self.lambda_omega * np.abs(om[cur] - om[nbrs])
                w = np.clip(w, 0.0, None)
                if np.all(w <= 0):
                    break
                # sample next neighbor proportional to w
                wp = w / (w.sum() + 1e-12)
                r = self.rng.random()
                cdf = np.cumsum(wp)
                idx = int(np.searchsorted(cdf, r, side="right"))
                nxt = int(nbrs[min(idx, nbrs.size - 1)])
                visit[nxt] += 1

                # Accumulate event stats
                sel_w = float(w[min(idx, nbrs.size - 1)])
                sel_w_sum += max(0.0, sel_w)
                sel_steps += 1
                if len(sample_nodes) < sample_cap:
                    sample_nodes.add(nxt)

                # Simple cycle detection: return to a previously visited node on this walk
                if nxt in seen:
                    cycle_events += 1
                    # Publish cycle_hit immediately if bus is present (use lightweight payload)
                    if bus is not None:
                        try:
                            obs = Observation(
                                tick=tick,
                                kind="cycle_hit",
                                nodes=[cur, nxt],
                                w_mean=float(a.mean()),
                                w_var=float(a.var()),
                                s_mean=0.0,
                                loop_len=int(len(path) - seen[nxt] + 1),
                                loop_gain=float(sel_w),
                                coverage_id=0,
                                domain_hint=""
                            )
                            bus.publish(obs)
                        except Exception:
                            pass
                else:
                    seen[nxt] = step_idx
                    path.append(nxt)

                cur = nxt

        total_visits = int(visit.sum())
        unique = int(np.count_nonzero(visit))
        coverage = float(unique) / float(max(1, N))
        if total_visits > 0:
            p = visit.astype(np.float64) / float(total_visits)
            p = p[p > 0]
            vt_entropy = float(-(p * np.log(p)).sum())
        else:
            vt_entropy = 0.0

        # Store findings for external consumers (Nexus metrics/SIE/ADC)
        self.findings = {
            "vt_visits": total_visits,
            "vt_unique": unique,
            "vt_coverage": coverage,
            "vt_entropy": vt_entropy,
            "vt_walkers": float(walkers),
            "vt_hops": float(hops),
            "a_mean": float(a.mean()),
            "omega_mean": float(om.mean()),
        }

        # Publish a compact region_stat at end of traversal
        if bus is not None:
            try:
                s_mean = float(sel_w_sum / max(1, sel_steps))
                cov_id = int(min(9, max(0, int(coverage * 10.0))))
                obs = Observation(
                    tick=tick,
                    kind="region_stat",
                    nodes=list(sample_nodes),
                    w_mean=float(self.W.mean()),
                    w_var=float(self.W.var()),
                    s_mean=s_mean,
                    coverage_id=cov_id,
                    domain_hint=""
                )
                bus.publish(obs)
            except Exception:
                pass
    
            # Increment local tick for announcement timestamps
            try:
                self._tick += 1
            except Exception:
                pass


    def step(self, t: float, domain_modulation: float, sie_drive: float = 1.0, use_time_dynamics: bool=True):
        """
        Apply one update tick driven entirely by Void Equations:
        - Structural growth/rewiring: candidates sampled via alias table built from ReLU(Δalpha)
        - Affinity S_ij = ReLU(Δalpha_i) * ReLU(Δalpha_j) − λ * |Δomega_i − Δomega_j|
        - Top‑k neighbors per node; symmetric adjacency
        - Node field update via universal_void_dynamics, multiplicatively gated by SIE valence (Rule 3)
        """
        # 1) Compute elemental deltas from your void equations
        d_alpha = delta_re_vgsp(self.W, t, domain_modulation=domain_modulation, use_time_dynamics=use_time_dynamics)
        d_omega = delta_gdsp(self.W, t, domain_modulation=domain_modulation, use_time_dynamics=use_time_dynamics)
        a = np.maximum(0.0, d_alpha.astype(np.float32))  # ReLU(Δalpha)
        om = d_omega.astype(np.float32)
        # External stimulation: add and decay deterministic symbol→group drive
        try:
            a = np.clip(a + self._stim, 0.0, None)
            self._stim *= getattr(self, "_stim_decay", 0.90)
        except Exception:
            pass

        # 2) Build candidate sampler ~ a (ReLU(Δalpha))
        prob, alias = self._build_alias(a)

        # 3) Per-node top-k neighbors by sampling; complexity ~ O(N * candidates)
        N = self.N
        k = int(max(1, self.k))
        s = int(max(self.candidates, 2 * k))
        A_new = np.zeros((N, N), dtype=np.int8)

        if self.structural_mode == "dense" and N <= 4096:
            # Exact affinity (validation/small N)
            S = a[:, None] * a[None, :] - self.lambda_omega * np.abs(om[:, None] - om[None, :])
            np.fill_diagonal(S, -np.inf)
            idx_topk = np.argpartition(S, -k, axis=1)[:, -k:]
            rows = np.repeat(np.arange(N), k)
            cols = idx_topk.reshape(-1)
            A_new[rows, cols] = 1
        else:
            # Alias sampling per node (default, efficient, void‑guided traversal)
            for i in range(N):
                js = self._alias_draw(prob, alias, s)
                # drop self and dupes
                js = js[js != i]
                if js.size == 0:
                    continue
                js = np.unique(js)  # s is small; set semantics OK
                # score by void affinity
                Si = a[i] * a[js] - self.lambda_omega * np.abs(om[i] - om[js])
                take = min(k, Si.size)
                idx = np.argpartition(Si, -take)[-take:]
                nbrs = js[idx]
                A_new[i, nbrs] = 1

        # Undirected symmetrization
        A_new = np.maximum(A_new, A_new.T)
        self.A = A_new

        # 4) Update node field with combined universal dynamics, gated by SIE valence (in [0,1])
        dW = universal_void_dynamics(self.W, t, domain_modulation=domain_modulation, use_time_dynamics=use_time_dynamics)
        dW = (float(max(0.0, min(1.0, sie_drive))) * dW).astype(np.float32)
        self.W = np.clip(self.W + dW, 0.0, 1.0)

        # 4.1) SIE v2 intrinsic reward/valence from W and dW (void-native)
        try:
            if not hasattr(self, "_sie2"):
                from .sie_v2 import SIECfg, SIEState
                self._sie2 = SIEState(self.N, SIECfg())
            from .sie_v2 import sie_step
            r_vec, v01 = sie_step(self._sie2, self.W, dW)
            self._last_sie2_reward = float(np.mean(r_vec))
            self._last_sie2_valence = float(v01)
        except Exception:
            pass

        # 5) Edge weights follow nodes on the updated topology
        self.E = self._edge_weights_from_W()

        # 5.1) Stage‑1 cohesion repair + pruning via structural homeostasis (void‑affinity)
        try:
            labels = self.component_labels()
            perform_structural_homeostasis(
                self,
                labels=labels,
                d_alpha=d_alpha,
                d_omega=d_omega,
                lambda_omega=self.lambda_omega,
                bundle_size=int(getattr(self, "bundle_size", 3)),
                prune_factor=float(getattr(self, "prune_factor", 0.10))
            )
        except Exception:
            # Keep runtime alive even if homeostasis step fails
            pass
        
        # 6) Continuous void‑equation traversal to propagate findings for Global System
        try:
            self._void_traverse(a, om)
        except Exception:
            # Keep system alive even if traversal fails; findings may be stale
            pass

    def active_edge_count(self):
        return int((self.E > self.threshold).sum() // 2)  # undirected

    def connected_components(self):
        # Cohesion via topology-only graph (Stage 1)
        G = nx.from_numpy_array(self.A.astype(int), create_using=nx.Graph)
        return nx.number_connected_components(G)
    
    def component_labels(self):
        # Labels for topology-only cohesion (Stage 1)
        G = nx.from_numpy_array(self.A.astype(int), create_using=nx.Graph)
        labels = np.zeros(self.N, dtype=int)
        for idx, comp in enumerate(nx.connected_components(G)):
            for n in comp:
                labels[int(n)] = idx
        return labels
    
    def cyclomatic_complexity(self):
        # For the active subgraph: cycles = E - N + C
        mask = (self.E > self.threshold)
        G_act = nx.from_numpy_array(mask.astype(int), create_using=nx.Graph)
        n = G_act.number_of_nodes()
        e = G_act.number_of_edges()
        c = nx.number_connected_components(G_act)
        return max(0, e - n + c)
    
    def snapshot_graph(self):
        # Return a NetworkX graph (active subgraph) for drawing
        mask = (self.E > self.threshold)
        G_act = nx.from_numpy_array(mask.astype(int), create_using=nx.Graph)
        return G_act
