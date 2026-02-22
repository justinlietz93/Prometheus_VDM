from __future__ import annotations

import numpy as np
import networkx as nx

from .announce import Observation
from .primitives.dsu import DSU as _DSU
from .void_dynamics_adapter import (
    TAU,
    BETA,
    LAMBDA,
    GAMMA,
    KT_EFF,
    EPS_TOPO,
    ETA_BOND_FLOOR,
    klein_gordon_rhs,
    bond_potential_derivative,
)


class SparseConnectome:
    def __init__(self, N: int, k: int, seed: int = 0, threshold: float = 0.15, lambda_omega: float = 0.1, **kwargs):
        n_req = int(N)
        side = max(1, int(round(float(n_req) ** (1.0 / 3.0))))
        self.N = int(side ** 3)
        self.k = int(k)
        self.rng = np.random.default_rng(seed)
        self.threshold = float(threshold)
        self.lambda_omega = float(lambda_omega)
        self.W = self.rng.uniform(0.0, 1.0, size=(self.N,)).astype(np.float32)

        self.tau = TAU
        self.beta = BETA
        self.lam = LAMBDA
        self.D = GAMMA
        self.kT = KT_EFF
        self.eps_topo = EPS_TOPO

        self.phi_curr = self.W.copy()
        self.phi_prev = self.W.copy()
        self.debt = np.zeros(self.N, dtype=np.float64)

        self._side = int(side)
        self.pos = np.zeros((self.N, 3), dtype=np.float32)
        for i in range(self.N):
            iz = i // (side * side)
            iy = (i // side) % side
            ix = i % side
            self.pos[i] = (ix, iy, iz)

        self.r_causal = np.zeros(self.N, dtype=np.float32)
        self._build_cubic_adjacency()
        self.psi_curr = [np.ones(self.adj[i].shape[0], dtype=np.float32) for i in range(self.N)]
        self.psi_prev = [p.copy() for p in self.psi_curr]

        self.findings = {}
        self._tick = 0
        self._stim = np.zeros(self.N, dtype=np.float32)
        self._stim_decay = 0.90
        self._frag_dsu = _DSU(self.N)
        self._frag_components_lb = self.N
        self._frag_dirty_since = None

        self._validation_events_enabled = False
        self._v_edge_births: list[tuple[int, int, float, float, float, int]] = []
        self._v_edge_deaths: list[tuple[int, int, int]] = []
        self._v_psi_up: list[tuple[int, int, int]] = []
        self._v_psi_down: list[tuple[int, int, int]] = []
        self._v_death_threshold = float(2.0 * self.eps_topo * self.kT)

    def enable_validation_events(self, enabled: bool = True) -> None:
        self._validation_events_enabled = bool(enabled)
        self._v_edge_births.clear()
        self._v_edge_deaths.clear()
        self._v_psi_up.clear()
        self._v_psi_down.clear()

    def _build_cubic_adjacency(self):
        side = self._side
        self.adj = [np.zeros(0, dtype=np.int32) for _ in range(self.N)]
        for i in range(self.N):
            iz = i // (side * side)
            iy = (i // side) % side
            ix = i % side
            nbrs = []
            if ix > 0:
                nbrs.append(i - 1)
            if ix < side - 1:
                nbrs.append(i + 1)
            if iy > 0:
                nbrs.append(i - side)
            if iy < side - 1:
                nbrs.append(i + side)
            if iz > 0:
                nbrs.append(i - side * side)
            if iz < side - 1:
                nbrs.append(i + side * side)
            self.adj[i] = np.array(sorted(nbrs), dtype=np.int32)

    def stimulate_indices(self, idxs, amp: float = 0.05):
        try:
            if idxs is None:
                return
            arr = np.asarray(list(set(int(i) % self.N for i in idxs)), dtype=np.int64)
            if arr.size == 0:
                return
            self.phi_curr[arr] = np.clip(self.phi_curr[arr] + float(amp), 0.0, 1.0).astype(np.float32)
            self.W = self.phi_curr
        except Exception:
            pass

    def _remove_dead_edges(self):
        for i in range(self.N):
            if self.adj[i].size == 0:
                continue
            alive = self.psi_curr[i] >= ETA_BOND_FLOOR
            if np.all(alive):
                continue
            dead_nbrs = self.adj[i][~alive]
            self.adj[i] = self.adj[i][alive]
            self.psi_curr[i] = self.psi_curr[i][alive]
            self.psi_prev[i] = self.psi_prev[i][alive]
            for j in dead_nbrs:
                j = int(j)
                if self._validation_events_enabled and i < j:
                    self._v_edge_deaths.append((i, j, int(self._tick)))
                mask = self.adj[j] != i
                self.adj[j] = self.adj[j][mask]
                self.psi_curr[j] = self.psi_curr[j][mask]
                self.psi_prev[j] = self.psi_prev[j][mask]

    def _propose_new_edges(self, phi_dot_abs: np.ndarray):
        side = self._side
        side2 = side * side
        for i in range(self.N):
            if phi_dot_abs[i] <= self.kT:
                continue
            r = float(self.r_causal[i])
            if r < 1.5:
                continue
            R = int(min(r, side // 2))
            if R < 2:
                continue
            r2 = r * r
            existing = set(self.adj[i].tolist())
            ix, iy, iz = map(int, self.pos[i])
            for dz in range(-R, R + 1):
                z = iz + dz
                if z < 0 or z >= side:
                    continue
                dz2 = dz * dz
                for dy in range(-R, R + 1):
                    y = iy + dy
                    if y < 0 or y >= side:
                        continue
                    dy2 = dy * dy
                    for dx in range(-R, R + 1):
                        x = ix + dx
                        if x < 0 or x >= side:
                            continue
                        if dx == 0 and dy == 0 and dz == 0:
                            continue
                        dist2 = float(dx * dx + dy2 + dz2)
                        if dist2 > r2 or dist2 < 2.25:
                            continue
                        j = x + y * side + z * side2
                        if j in existing or phi_dot_abs[j] <= self.kT:
                            continue

                        self.adj[i] = np.append(self.adj[i], np.int32(j))
                        self.psi_curr[i] = np.append(self.psi_curr[i], np.float32(0.0))
                        self.psi_prev[i] = np.append(self.psi_prev[i], np.float32(0.0))

                        self.adj[j] = np.append(self.adj[j], np.int32(i))
                        self.psi_curr[j] = np.append(self.psi_curr[j], np.float32(0.0))
                        self.psi_prev[j] = np.append(self.psi_prev[j], np.float32(0.0))

                        if self._validation_events_enabled:
                            a, b = (i, j) if i < j else (j, i)
                            self._v_edge_births.append((a, b, dist2, float(self.r_causal[a]), float(self.r_causal[b]), int(self._tick)))
                        existing.add(j)

    def _compute_physics_reward(self, dphi: np.ndarray):
        lap = 0.0
        for i in range(self.N):
            if self.adj[i].size:
                lap += float(np.sum((self.phi_curr[self.adj[i]] - self.phi_curr[i]) ** 2))
        H = 0.5 * self.D * lap + float(np.sum(self.lam * (self.phi_curr**2) * ((1.0 - self.phi_curr) ** 2)))
        dH_dt = float(H - float(getattr(self, "_reward_H", H)))
        fisher_speed = float(np.sqrt(np.mean(dphi * dphi)))
        S = float(np.mean(self.debt))
        dS_dt = float(S - float(getattr(self, "_reward_S", S)))
        boundary_flux = float(np.sum(np.abs(dphi)))
        self._reward_H = float(H)
        self._reward_dH_dt = float(dH_dt)
        self._reward_fisher_speed = float(fisher_speed)
        self._reward_S = float(S)
        self._reward_dS_dt = float(dS_dt)
        self._reward_boundary_flux = float(boundary_flux)
        raw = float(-dH_dt) + 0.1 * float(fisher_speed)
        self._last_sie2_valence = float(max(0.0, min(1.0, 0.5 + 0.5 * np.tanh(raw))))
        self._last_sie2_reward = float(raw)

    def _void_traverse(self, a: np.ndarray, om: np.ndarray):
        self.findings = {
            "vt_visits": int(np.count_nonzero(a > self.kT)),
            "vt_entropy": float(np.var(a)),
            "a_mean": float(np.mean(a)),
            "omega_mean": float(np.mean(om)),
        }
        bus = getattr(self, "bus", None)
        if bus is not None:
            try:
                bus.publish(Observation(tick=int(self._tick), kind="region_stat", nodes=[], w_mean=float(np.mean(self.phi_curr)), w_var=float(np.var(self.phi_curr)), s_mean=0.0, coverage_id=0, domain_hint=""))
            except Exception:
                pass

    def step(self, tick: int):
        self._tick = tick
        tau_eff = self.tau * np.exp(self.beta * self.debt)
        phi_dot = self.phi_curr - self.phi_prev
        rhs = klein_gordon_rhs(self.phi_curr, self.adj, self.psi_curr, lam=self.lam, D=self.D, kT=self.kT)
        a_inertia = tau_eff.astype(np.float32)
        numerator = rhs + (2.0 * a_inertia + 1.0) * self.phi_curr - a_inertia * self.phi_prev
        phi_new = np.clip(numerator / (a_inertia + 1.0), 0.0, 1.0).astype(np.float32)

        tau_bond = np.float32(self.tau / self.eps_topo)
        phi_dot_abs = np.abs(phi_dot).astype(np.float32)
        death_threshold = self._v_death_threshold
        for i in range(self.N):
            nbrs = self.adj[i]
            if nbrs.size == 0:
                continue
            psi_old = self.psi_curr[i]
            psi_prev_old = self.psi_prev[i]

            dU = bond_potential_derivative(psi_old, phi_dot_abs[i], phi_dot_abs[nbrs], lam=self.lam, eps=self.eps_topo)
            eta_bond = np.sqrt(2.0 * self.eps_topo * self.kT) * self.rng.standard_normal(nbrs.size).astype(np.float32)
            rhs_bond = -dU + eta_bond
            psi_new = (rhs_bond + (2.0 * tau_bond + 1.0) * psi_old - tau_bond * psi_prev_old) / (tau_bond + 1.0)
            psi_new = np.clip(psi_new, 0.0, 1.0).astype(np.float32)

            if self._validation_events_enabled:
                for idx, jv in enumerate(nbrs):
                    j = int(jv)
                    if i < j:
                        oldv = float(psi_old[idx])
                        newv = float(psi_new[idx])
                        if oldv <= 0.5 < newv:
                            self._v_psi_up.append((i, j, int(self._tick)))
                        if oldv >= death_threshold > newv:
                            self._v_psi_down.append((i, j, int(self._tick)))

            self.psi_prev[i] = psi_old.copy()
            self.psi_curr[i] = psi_new

        self._remove_dead_edges()
        self._propose_new_edges(phi_dot_abs)

        dphi = (phi_new - self.phi_curr).astype(np.float32)
        self.phi_prev = self.phi_curr.copy()
        self.phi_curr = phi_new
        self.W = self.phi_curr

        self.debt = (1.0 - self.beta) * self.debt + np.abs(dphi).astype(np.float64)
        c_eff = np.sqrt(self.D / tau_eff).astype(np.float32)
        active = phi_dot_abs > self.kT
        self.r_causal[active] += c_eff[active]

        try:
            self._stim *= getattr(self, "_stim_decay", 0.90)
        except Exception:
            pass

        self._compute_physics_reward(dphi)
        self._void_traverse(np.abs(dphi).astype(np.float32), (-self.beta * self.phi_curr).astype(np.float32))

    def _active_edge_iter(self):
        for i in range(self.N):
            nbrs = self.adj[i]
            psi = self.psi_curr[i]
            for idx in range(nbrs.size):
                j = int(nbrs[idx])
                if j <= i:
                    continue
                if float(psi[idx]) > ETA_BOND_FLOOR:
                    yield (i, j)

    def _weighted_edge_iter(self):
        for i in range(self.N):
            wi = float(self.W[i])
            for j in self.adj[i]:
                jj = int(j)
                if jj <= i:
                    continue
                if (wi * float(self.W[jj])) > self.threshold:
                    yield (i, jj)

    def _maybe_audit_frag(self, budget_edges: int) -> None:
        try:
            dsu = _DSU(self.N)
            seen: set[int] = set()
            processed = 0
            b = int(max(0, int(budget_edges)))
            for (i, j) in self._active_edge_iter():
                dsu.union(int(i), int(j))
                seen.add(int(i))
                seen.add(int(j))
                processed += 1
                if b > 0 and processed >= b:
                    break
            self._frag_dsu = dsu
            self._frag_components_lb = int(len(set(int(dsu.find(idx)) for idx in seen))) if seen else self.N
            if not (b > 0 and processed >= b):
                self._frag_dirty_since = None
        except Exception:
            pass

    def active_edge_count(self) -> int:
        return sum(1 for _ in self._active_edge_iter())

    def connected_components(self) -> int:
        dsu = _DSU(self.N)
        act_nodes = set()
        for i, j in self._active_edge_iter():
            dsu.union(i, j)
            act_nodes.add(int(i))
            act_nodes.add(int(j))
        return len(set(int(dsu.find(idx)) for idx in act_nodes)) if act_nodes else self.N

    def cyclomatic_complexity(self) -> int:
        e = 0
        dsu = _DSU(self.N)
        act_nodes = set()
        for i, j in self._active_edge_iter():
            e += 1
            dsu.union(i, j)
            act_nodes.add(int(i))
            act_nodes.add(int(j))
        c = len(set(int(dsu.find(idx)) for idx in act_nodes)) if act_nodes else self.N
        return int(max(0, e - self.N + c))

    def snapshot_graph(self):
        if self.N > 5000:
            return nx.Graph()
        G = nx.Graph()
        G.add_nodes_from(range(self.N))
        for i, j in self._active_edge_iter():
            G.add_edge(int(i), int(j))
        return G

    def connectome_entropy(self) -> float:
        deg = np.zeros(self.N, dtype=np.int64)
        for i, j in self._weighted_edge_iter():
            deg[i] += 1
            deg[j] += 1
        total = int(deg.sum())
        if total <= 0:
            return 0.0
        p = deg.astype(np.float64) / float(total)
        p = p[p > 0]
        return float(-(p * np.log(p)).sum())


Connectome = SparseConnectome
