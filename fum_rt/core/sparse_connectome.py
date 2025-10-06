# sparse_connectome.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Void-faithful sparse connectome for ultra-scale runs.

- Adjacency stored as neighbor lists (list[np.ndarray[int32]]) with symmetric edges
- No dense NxN matrices; all metrics computed by streaming over adjacency
- Traversal and measuring use void equations (Rule: use void equations for traversal/measuring)
- Stage-1 cohesion measured on topology-only adjacency (A_sparse)
- Active subgraph for cycle/entropy uses implicit edge weight W[i]*W[j] > threshold

API mirrors Connectome sufficiently for Nexus and metrics:
    - step(t, domain_modulation, sie_drive=1.0, use_time_dynamics=True)
    - active_edge_count()
    - connected_components()
    - cyclomatic_complexity()
    - snapshot_graph()  (safe for small N)
    - connectome_entropy()  (preferred by metrics if present)

Note: Stage‑1 healing/pruning here omits dense S_ij bridging to avoid NxN;
      bridging logic is already executed upstream in dense Connectome. For sparse,
      we rely on void‑guided rewiring each tick to fuse components (top‑k by S_ij).
"""

from __future__ import annotations
import numpy as np
import networkx as nx
from typing import List, Set
import os as _os
from .void_dynamics_adapter import universal_void_dynamics, delta_re_vgsp, delta_gdsp
from .announce import Observation


from .primitives.dsu import DSU as _DSU


class SparseConnectome:
    def __init__(self, N: int, k: int, seed: int = 0,
                 threshold: float = 0.15, lambda_omega: float = 0.1,
                 candidates: int = 64, structural_mode: str = "alias",
                 traversal_walkers: int = 256, traversal_hops: int = 3,
                 bundle_size: int = 3, prune_factor: float = 0.10):
        self.N = int(N)
        self.k = int(k)
        self.rng = np.random.default_rng(seed)
        self.threshold = float(threshold)
        self.lambda_omega = float(lambda_omega)
        self.candidates = int(max(1, candidates))
        self.structural_mode = structural_mode  # reserved; alias path used by default

        # Node state
        self.W = self.rng.uniform(0.0, 1.0, size=(self.N,)).astype(np.float32)

        # Sparse symmetric topology as neighbor lists (arrays of int32)
        self.adj: List[np.ndarray] = [np.zeros(0, dtype=np.int32) for _ in range(self.N)]

        # Traversal config
        self.traversal_walkers = int(max(1, traversal_walkers))
        self.traversal_hops = int(max(1, traversal_hops))

        # Findings each tick for Global System consumers (SIE/ADC)
        self.findings = {}
        # Homeostasis tuning (mirrors dense backend; currently stored for parity)
        self.bundle_size = int(max(1, bundle_size))
        self.prune_factor = float(max(0.0, prune_factor))
        # Local tick counter for announcement timestamps
        self._tick = 0
        # External stimulation buffer (deterministic symbol→group; decays each tick)
        self._stim = np.zeros(self.N, dtype=np.float32)
        self._stim_decay = 0.90

        # Sparse cohesion bridging budget and degree heterogeneity controls
        try:
            self.bridge_budget = int(_os.getenv("SPARSE_BRIDGE_BUDGET", "24"))
        except Exception:
            self.bridge_budget = 24
        try:
            self.min_k_frac = float(_os.getenv("MIN_K_FRAC", "0.5"))
        except Exception:
            self.min_k_frac = 0.5
        # Active-edge/fragment trackers (incremental; void-faithful)
        self._edges_active = 0
        self._vertices_active = 0
        self._last_edges_active = 0
        self._last_vertices_active = 0
        self._frag_dsu = _DSU(self.N)
        self._frag_components_lb = self.N
        self._frag_dirty_since = None

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

    def stimulate_indices(self, idxs, amp: float = 0.05):
        """
        Deterministic stimulus injection for sparse backend:
        - idxs: iterable of neuron indices to stimulate
        - amp: additive boost to the stimulus buffer (decays each tick)
        """
        try:
            if idxs is None:
                return
            arr = np.asarray(list(set(int(i) % self.N for i in idxs)), dtype=np.int64)
            if arr.size == 0:
                return
            self._stim[arr] = np.clip(self._stim[arr] + float(amp), 0.0, 1.0)
            # small immediate bump to W to seed associations
            self.W[arr] = np.clip(self.W[arr] + 0.01 * float(amp), 0.0, 1.0)
        except Exception:
            pass

    def _void_traverse(self, a: np.ndarray, om: np.ndarray):
        """
        Continuous void‑equation traversal on sparse graph (neighbor lists).
        Seeds ~ ReLU(Δalpha). Transition weight to neighbor j: max(0, a[i]*a[j] - λ*|ω_i-ω_j|).

        Also publishes compact Observation events to the ADC bus if present.
        """
        N = self.N
        walkers = self.traversal_walkers
        hops = self.traversal_hops

        prob, alias = self._build_alias(a)
        seeds = self._alias_draw(prob, alias, walkers)
        visit = np.zeros(N, dtype=np.int32)

        # Optional ADC bus and tick
        bus = getattr(self, "bus", None)
        tick = int(getattr(self, "_tick", 0))

        # Event accumulators
        sample_cap = 64
        sel_w_sum = 0.0
        sel_steps = 0
        sample_nodes = set()

        for s in seeds:
            cur = int(s)
            seen = {cur: 0}
            path = [cur]
            for step_idx in range(1, hops + 1):
                nbrs = self.adj[cur]
                if nbrs.size == 0:
                    break
                w = a[cur] * a[nbrs] - self.lambda_omega * np.abs(om[cur] - om[nbrs])
                w = np.clip(w, 0.0, None)
                if np.all(w <= 0):
                    break
                wp = w / (w.sum() + 1e-12)
                r = self.rng.random()
                cdf = np.cumsum(wp)
                idx = int(np.searchsorted(cdf, r, side="right"))
                nxt = int(nbrs[min(idx, nbrs.size - 1)])
                visit[nxt] += 1

                # accumulate simple local stats
                sel_w = float(w[min(idx, nbrs.size - 1)])
                sel_w_sum += max(0.0, sel_w)
                sel_steps += 1
                if len(sample_nodes) < sample_cap:
                    sample_nodes.add(nxt)

                # simple loop detection on this walk
                if nxt in seen:
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

        # publish a compact region_stat
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

    def step(self, t: float, domain_modulation: float, sie_drive: float = 1.0, use_time_dynamics: bool = True):
        """
        Sparse, void‑faithful tick:
        - Compute Δalpha/Δomega by void equations
        - Build per-node candidate list via alias sampler ~ ReLU(Δalpha)
        - Score candidates by S_ij = ReLU(Δα_i)·ReLU(Δα_j) − λ·|Δω_i − Δω_j|
        - Take symmetric top‑k neighbors (undirected)
        - Update node field with universal_void_dynamics gated by SIE valence
        - Run traversal to publish vt_* findings
        """
        # 1) Elemental deltas from void equations
        d_alpha = delta_re_vgsp(self.W, t, domain_modulation=domain_modulation, use_time_dynamics=use_time_dynamics)
        d_omega = delta_gdsp(self.W, t, domain_modulation=domain_modulation, use_time_dynamics=use_time_dynamics)
        a = np.maximum(0.0, d_alpha.astype(np.float32))
        om = d_omega.astype(np.float32)
        # External stimulation: add and decay deterministic symbol→group drive
        try:
            a = np.clip(a + self._stim, 0.0, None)
            self._stim *= getattr(self, "_stim_decay", 0.90)
        except Exception:
            pass

        # 2) Candidate sampler ~ a
        prob, alias = self._build_alias(a)

        # 3) Per-node top-k selection from candidates by void affinity S_ij
        N = self.N
        k_base = int(max(1, self.k))
        s = int(max(self.candidates, 2 * k_base))
        neigh_sets: List[Set[int]] = [set() for _ in range(N)]
        # Global activity scale for degree heterogeneity
        amax = float(np.max(a)) if a.size else 0.0
        _eps = 1e-12

        for i in range(N):
            js = self._alias_draw(prob, alias, s)
            if js.size == 0:
                continue
            js = js[js != i]
            if js.size == 0:
                continue
            js = np.unique(js)
            Si = a[i] * a[js] - self.lambda_omega * np.abs(om[i] - om[js])

            # Enforce positive void-affinity to avoid forced, non-supported edges (prevents ring-lattice collapse)
            pos_mask = Si > 0.0
            if not np.any(pos_mask):
                continue
            js_pos = js[pos_mask]
            Si_pos = Si[pos_mask]

            # Per-node target degree in [min_k_frac*k_base, k_base], proportional to activity a[i]
            if amax > _eps:
                frac = float(getattr(self, "min_k_frac", 0.5)) + (1.0 - float(getattr(self, "min_k_frac", 0.5))) * float(a[i]) / amax
            else:
                frac = 1.0
            k_i = int(max(1, round(frac * k_base)))

            take = min(k_i, Si_pos.size)
            if take <= 0:
                continue
            idx = np.argpartition(Si_pos, -take)[-take:]
            nbrs = js_pos[idx]
            for j in nbrs:
                neigh_sets[i].add(int(j))

        # Undirected symmetrization
        for i in range(N):
            for j in neigh_sets[i]:
                neigh_sets[j].add(i)

        # Sparse structural maintenance (adaptive pruning, lightweight)
        # Rationale:
        # - In sparse mode, adjacency is rebuilt each tick; to expose real pruning dynamics and
        #   avoid permanent over-connection, we drop edges whose implicit weight |W_i*W_j| is
        #   below prune_factor * mean(|W_i*W_j|) over current edges.
        # - This keeps complexity bounded and allows components to split when pathologies exist.
        try:
            # Collect undirected effective weights for current edges
            weights = []
            for i in range(N):
                wi = float(self.W[i])
                for j in neigh_sets[i]:
                    jj = int(j)
                    if jj <= i:
                        continue
                    weights.append(abs(wi * float(self.W[jj])))

            pruned_pairs = 0
            if weights:
                mean_w = float(np.mean(np.asarray(weights, dtype=np.float64)))
                prune_factor = float(getattr(self, "prune_factor", 0.10))
                prune_threshold = (prune_factor * mean_w) if mean_w > 0.0 else 0.0
                if prune_threshold > 0.0:
                    # Remove edges below adaptive threshold; maintain undirected symmetry
                    for i in range(N):
                        wi = float(self.W[i])
                        # collect first to avoid mutating set during iteration
                        to_remove = []
                        for j in neigh_sets[i]:
                            jj = int(j)
                            if jj <= i:
                                continue
                            wij = abs(wi * float(self.W[jj]))
                            if wij < prune_threshold:
                                to_remove.append(jj)
                        for jj in to_remove:
                            if jj in neigh_sets[i]:
                                neigh_sets[i].remove(jj)
                            if i in neigh_sets[jj]:
                                neigh_sets[jj].remove(i)
                                pruned_pairs += 1
            # Expose pruning stats for diagnostics (undirected pairs)
            try:
                setattr(self, "_last_pruned_count", int(pruned_pairs))
            except Exception:
                pass
            # No bridging in sparse maintenance (keep light); report zero bridged edges
            try:
                setattr(self, "_last_bridged_count", 0)
            except Exception:
                pass
        except Exception:
            # Fail-soft to preserve runtime continuity
            pass

        # --- Sparse cohesion bridging (event-driven, budgeted, no scans) ---
        # Goal: when multiple components exist, propose up to B symmetric bridges using the
        # same void-affinity sampler used for growth. This keeps dynamics lively (cycles/components)
        # without any NxN work. Budget defaults to 8 per tick; can be tuned via instance attribute.
        try:
            # Use frag tracker lower-bound components (active graph), avoid structural scans
            comp_count = int(getattr(self, "_frag_components_lb", 1))
            _dirty = getattr(self, "_frag_dirty_since", None)
            # Optionally early-audit with a small budget to refresh active components
            try:
                _budget = int(_os.getenv("FRAG_AUDIT_EDGES", "200000"))
            except Exception:
                _budget = 200000
            try:
                if _dirty is not None and _budget > 0:
                    # Best-effort refresh of active components (bounded)
                    # This calls an internal audit that streams over up to _budget active edges.
                    self._maybe_audit_frag(int(_budget))
                    comp_count = int(getattr(self, "_frag_components_lb", comp_count))
            except Exception:
                pass
            dsu = getattr(self, "_frag_dsu", _DSU(N))

            bridged_pairs = 0
            if comp_count > 1:
                B = int(getattr(self, "bridge_budget", 8))
                B = max(0, B)
                if B > 0:
                    # Use alias sampler (a) to pick candidate endpoints cheaply
                    attempts = 0
                    max_attempts = int(max(32, B * 64))
                    while bridged_pairs < B and attempts < max_attempts:
                        attempts += 1
                        ui = self._alias_draw(prob, alias, 1)
                        vi = self._alias_draw(prob, alias, 1)
                        if ui.size == 0 or vi.size == 0:
                            continue
                        u = int(ui[0]); v = int(vi[0])
                        if u == v:
                            continue
                        # Skip if already adjacent
                        if (v in neigh_sets[u]) or (u in neigh_sets[v]):
                            continue
                        # Bridge only across distinct components
                        if dsu.find(u) == dsu.find(v):
                            continue
                        # Score by void affinity; require positive support
                        s_uv = float(a[u] * a[v] - self.lambda_omega * abs(om[u] - om[v]))
                        if s_uv <= 0.0:
                            continue
                        # Add symmetric bridge and union components
                        neigh_sets[u].add(v)
                        neigh_sets[v].add(u)
                        dsu.union(u, v)
                        try:
                            self._frag_dsu = dsu
                            if int(getattr(self, "_frag_components_lb", 1)) > 1:
                                self._frag_components_lb = int(self._frag_components_lb) - 1
                            self._frag_dirty_since = None
                        except Exception:
                            pass
                        bridged_pairs += 1
            # Expose bridged count for diagnostics
            try:
                setattr(self, "_last_bridged_count", int(bridged_pairs))
            except Exception:
                pass
        except Exception:
            # Fail-soft for bridging; keep prior counters if present
            try:
                _ = int(getattr(self, "_last_bridged_count", 0))
            except Exception:
                pass

        # Freeze adjacency
        self.adj = [np.fromiter(sorted(s), dtype=np.int32) if s else np.zeros(0, dtype=np.int32) for s in neigh_sets]

        # 4) Node field update via universal void dynamics, gated by SIE valence in [0,1]
        dW = universal_void_dynamics(self.W, t, domain_modulation=domain_modulation, use_time_dynamics=use_time_dynamics)
        gate = float(max(0.0, min(1.0, sie_drive)))
        dW_eff = gate * dW
        self.W = np.clip(self.W + dW_eff, 0.0, 1.0).astype(np.float32)

        # 4.1) SIE v2 intrinsic reward/valence from W and dW (void-native)
        try:
            if not hasattr(self, "_sie2"):
                from .sie_v2 import SIECfg, SIEState
                self._sie2 = SIEState(self.N, SIECfg())
            from .sie_v2 import sie_step
            r_vec, v01 = sie_step(self._sie2, self.W, dW_eff)
            self._last_sie2_reward = float(np.mean(r_vec))
            self._last_sie2_valence = float(v01)
        except Exception:
            pass

        # 4.2) Active-edge counters and frag tracker (void-faithful, streaming)
        try:
            E_new = 0
            _seen = set()
            for (ii, jj) in self._active_edge_iter():
                E_new += 1
                _seen.add(int(ii)); _seen.add(int(jj))
            V_new = int(len(_seen))
            # mark dirty on edge-off (E decreased)
            try:
                if int(getattr(self, "_edges_active", 0)) > int(E_new):
                    if getattr(self, "_frag_dirty_since", None) is None:
                        self._frag_dirty_since = int(getattr(self, "_tick", 0))
            except Exception:
                pass
            self._last_edges_active = int(getattr(self, "_edges_active", 0))
            self._last_vertices_active = int(getattr(self, "_vertices_active", 0))
            self._edges_active = int(E_new)
            self._vertices_active = int(V_new)
            # optional budgeted audit
            try:
                _audit_every = int(_os.getenv("FRAG_AUDIT_EVERY", "50"))
            except Exception:
                _audit_every = 50
            try:
                _budget = int(_os.getenv("FRAG_AUDIT_EDGES", "200000"))
            except Exception:
                _budget = 200000
            if (getattr(self, "_frag_dirty_since", None) is not None or (int(getattr(self, "_tick", 0)) % max(1, _audit_every) == 0)) and _budget > 0:
                self._maybe_audit_frag(int(_budget))
            # cycles estimate
            try:
                comp_lb = int(getattr(self, "_frag_components_lb", 1))
            except Exception:
                comp_lb = 1
            cycles_est = int(max(0, int(E_new) - int(V_new) + int(comp_lb)))
            # augment findings
            try:
                self.findings.update({
                    "edges_active": int(E_new),
                    "vertices_active": int(V_new),
                    "components_lb": int(comp_lb),
                    "frag_dirty_age": int((int(getattr(self, "_tick", 0)) - int(getattr(self, "_frag_dirty_since", 0)))) if getattr(self, "_frag_dirty_since", None) is not None else 0,
                    "cycles_est": int(cycles_est),
                })
            except Exception:
                pass
        except Exception:
            pass

        # 5) Continuous traversal to emit vt_* findings
        try:
            self._void_traverse(a, om)
        except Exception:
            pass

        # increment local tick for announcement timestamps
        try:
            self._tick += 1
        except Exception:
            pass

    def _active_edge_iter(self):
        """Yield undirected edges (i, j) with i < j whose implicit weight is active."""
        th = self.threshold
        W = self.W
        for i in range(self.N):
            wi = float(W[i])
            nbrs = self.adj[i]
            if nbrs.size == 0:
                continue
            for j in nbrs:
                j = int(j)
                if j <= i:
                    continue
                if (wi * float(W[j])) > th:
                    yield (i, j)

    def _maybe_audit_frag(self, budget_edges: int) -> None:
        """
        Budgeted active-fragment audit (void-faithful):
        - Rebuild a DSU over ACTIVE edges only, streaming via _active_edge_iter().
        - Only processes up to 'budget_edges' edges; computes a lower-bound component count
          across the 'seen' active vertices.
        - Clears the dirty flag only when processing completes before budget exhaust.
        """
        try:
            N = int(self.N)
            dsu = _DSU(N)
            seen: set[int] = set()
            processed = 0
            b = int(max(0, int(budget_edges)))
            for (i, j) in self._active_edge_iter():
                ii = int(i); jj = int(j)
                dsu.union(ii, jj)
                seen.add(ii); seen.add(jj)
                processed += 1
                if b > 0 and processed >= b:
                    break
            if seen:
                roots = set(int(dsu.find(idx)) for idx in seen)
                comp_lb = int(len(roots))
            else:
                # No active vertices observed → treat as fully fragmented across N nodes
                comp_lb = N
            # Update trackers
            self._frag_dsu = dsu
            self._frag_components_lb = int(comp_lb)
            # Clear dirty flag only if we did not exhaust budget
            if not (b > 0 and processed >= b):
                self._frag_dirty_since = None
        except Exception:
            # Fail-soft: keep previous DSU/lower-bound
            pass

    def active_edge_count(self) -> int:
        return sum(1 for _ in self._active_edge_iter())

    def connected_components(self) -> int:
        """Active-subgraph components (Stage‑1 cohesion) over active edges only."""
        dsu = _DSU(self.N)
        e_active = 0
        act_nodes = set()
        for (i, j) in self._active_edge_iter():
            dsu.union(i, j)
            e_active += 1
            act_nodes.add(int(i))
            act_nodes.add(int(j))
        return (len(set(int(dsu.find(idx)) for idx in act_nodes)) if e_active > 0 else self.N)

    def cyclomatic_complexity(self) -> int:
        """
        Active-subgraph cyclomatic complexity: cycles = E_active - N + C_active
        where unions are formed only by active edges (W[i]*W[j] > threshold).
        """
        dsu = _DSU(self.N)
        e_active = 0
        act_nodes = set()
        for (i, j) in self._active_edge_iter():
            dsu.union(i, j)
            e_active += 1
            act_nodes.add(int(i))
            act_nodes.add(int(j))
        c_active = (len(set(int(dsu.find(idx)) for idx in act_nodes)) if e_active > 0 else self.N)
        cycles = e_active - self.N + c_active
        return int(max(0, cycles))

    def snapshot_graph(self):
        """
        Build a NetworkX graph of the active subgraph for visualization.
        Guarded for scale: returns empty graph if N is large.
        """
        if self.N > 5000:
            return nx.Graph()
        G = nx.Graph()
        G.add_nodes_from(range(self.N))
        for (i, j) in self._active_edge_iter():
            G.add_edge(int(i), int(j))
        return G

    def get_phi(self, i: int) -> float:
        """O(1) local read of fast field φ at node i; returns 0.0 when absent."""
        try:
            phi = getattr(self, "phi", None)
            if phi is None:
                return 0.0
            return float(phi[int(i)])
        except Exception:
            return 0.0

    def get_memory(self, i: int) -> float:
        """O(1) local read of slow memory m at node i via attached field/map when present."""
        # Prefer an attached MemoryField
        try:
            mf = getattr(self, "_memory_field", None)
            if mf is not None and hasattr(mf, "get_m"):
                return float(mf.get_m(int(i)))
        except Exception:
            pass
        # Fallback to attached MemoryMap adapter
        try:
            mm = getattr(self, "_memory_map", None)
            if mm is not None:
                fld = getattr(mm, "field", None)
                if fld is not None and hasattr(fld, "get_m"):
                    return float(fld.get_m(int(i)))
                dct = getattr(mm, "_m", None)
                if isinstance(dct, dict):
                    return float(dct.get(int(i), 0.0))
        except Exception:
            pass
        return 0.0

    def connectome_entropy(self) -> float:
        """
        Global pathological structure metric on the active subgraph.
        H = -Σ p_i log p_i where p_i proportional to degree(i) in active subgraph.
        """
        deg = np.zeros(self.N, dtype=np.int64)
        for i in range(self.N):
            wi = float(self.W[i])
            cnt = 0
            for j in self.adj[i]:
                j = int(j)
                if (wi * float(self.W[j])) > self.threshold:
                    cnt += 1
            deg[i] = cnt
        total = int(deg.sum())
        if total <= 0:
            return 0.0
        p = deg.astype(np.float64) / float(total)
        p = np.clip(p, 1e-12, 1.0)
        return float(-(p * np.log(p)).sum())