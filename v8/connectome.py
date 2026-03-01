"""
VDM v8 Connectome — Self-Modifying Graph with Metriplectic Klein-Gordon
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Graph state + step() implementing walker-gated metriplectic Klein-Gordon
on a self-modifying topology. Everything derived from the discrete action.

Source: CF01 (QGT→metriplectic), CF03 (tachyonic spinodal condensation),
CF07 (measurement/decoherence), CF09 (gauge emergence), Directive §0.1b, §0.6, §0.7.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

import numpy as np

from .void_equations import (
    D_DIFF,
    TAU,
    C_SIGNAL,
    EPS_BOND,
    LAMBDA,
    LAMBDA_BOND,
    BETA_DEBT,
    bond_decoherence_floor,
    bond_gradient_source,
    bond_potential_derivative,
    bond_weighted_laplacian,
    node_potential_derivative,
)
from .gauge import run_gauge_step, WalkerEvent, emit_counts


class Connectome:
    """
    Self-modifying graph with coupled node (φ) and bond (ψ) fields.

    Initial condition: ALL nodes at unstable vacuum φ=0.5, ZERO bonds.
    The tachyonic instability (V''(0.5) < 0) drives spinodal
    decomposition, forming domains. Walkers emit when |φ̇| > v_th.
    Bonds instantiate when walkers observe node pairs with gradients.
    Topology is emergent — not pinned.

    State:
        phi_curr, phi_prev — node field (second-order telegraph)
        adj — ragged adjacency (list of int32 arrays), initially empty
        psi_curr, psi_prev — bond field (parallel to adj), initially empty
        debt — per-node exponential throttle
        kT — measured effective temperature
    """

    def __init__(
        self,
        N: int,
        perturbation: np.ndarray,
        k_init: int = 10,
    ):
        """
        Initialize connectome with N nodes at unstable vacuum on substrate E0.

        Args:
            N: number of nodes
            perturbation: user-provided symmetry-breaking perturbation for φ
            k_init: initial computational substrate degree (ring lattice E0)
        """
        self.N = N

        # --- Node field: unstable vacuum φ = 0.5 + perturbation ---
        self.phi_curr = np.full(N, 0.5, dtype=np.float32) + perturbation.astype(np.float32)
        self.phi_prev = np.full(N, 0.5, dtype=np.float32)

        # --- Fixed computational substrate E0 ---
        # The true initial topology is the lattice. Physics (condensed bonds)
        # emerges on top of this.
        self.adj: List[np.ndarray] = []
        self.E0: List[np.ndarray] = []
        for i in range(N):
            nbrs = set()
            for dx in range(1, k_init // 2 + 1):
                nbrs.add((i + dx) % N)
                nbrs.add((i - dx) % N)
            arr = np.array(sorted(list(nbrs)), dtype=np.int32)
            self.adj.append(arr)
            self.E0.append(arr)

        # Bonds start at strict vacuum ψ = 0 on E0
        self.psi_curr: List[np.ndarray] = [
            np.zeros(len(self.adj[i]), dtype=np.float32) for i in range(N)
        ]
        self.psi_prev: List[np.ndarray] = [
            np.zeros(len(self.adj[i]), dtype=np.float32) for i in range(N)
        ]

        # --- Debt (self-limiting via exp(β·debt)) ---
        self.debt = np.zeros(N, dtype=np.float64)

        # --- Walker-gated state ---
        self.last_visit = np.full(N, -1, dtype=np.int32)
        
        # kT measured from ½·Var(φ̇) at every tick.
        phi_dot_init = perturbation.astype(np.float32)
        self.kT: float = max(0.5 * float(np.var(phi_dot_init)), 1e-30)
        self._tick: int = 0

        # --- External stimulus buffer ---
        self._stim = np.zeros(N, dtype=np.float32)

    # ------------------------------------------------------------------
    # Main physics step
    # ------------------------------------------------------------------

    def step(self, tick: int) -> Dict:
        """
        One tick of walker-gated metriplectic Klein-Gordon.

        The full physics: CF01 §4.1 (dF/dt = {F,H}_J + (F,S)_M).
        Both limbs, every tick, for every OBSERVED degree of freedom.
        Unobserved nodes are in superposition until measured (CF07).

        Bootstrap: until first walker emission, ALL nodes are in the
        compute set. This is required because at t=0 there are zero
        bonds → zero Laplacian coupling → each node evolves independently
        under V'(φ) alone. Once |φ̇| > v_th at some node, walkers appear,
        bonds instantiate where they observe gradients, and walker-gating
        takes over naturally.
        """
        self._tick = tick
        N = self.N

        # ---------------------------------------------------------------
        # Step 1: Compute φ̇ from current state
        # ---------------------------------------------------------------
        phi_dot = (self.phi_curr - self.phi_prev).astype(np.float32)

        # ---------------------------------------------------------------
        # Step 2: Gauge (Observer logic)
        emit_counts_arr = emit_counts(phi_dot, self.kT)
        
        # We process the gauge propagation in pure Python
        (
            all_events,
            active_set,
            warm_set,
            bond_pairs,
        ) = run_gauge_step(
            phi_dot=phi_dot,
            adj=self.adj,
            psi=self.psi_curr,
            kT=self.kT,
            c_signal=C_SIGNAL,
        )

        # Add stimulated nodes to active set
        stim_active = np.where(self._stim > 0.01)[0]
        for idx in stim_active:
            active_set.add(int(idx))
            for j in self.adj[int(idx)]:
                j_int = int(j)
                if j_int not in active_set:
                    warm_set.add(j_int)

        # Bootstrap: ALL nodes computed until first walker emission.
        # At t=0: zero bonds → zero Laplacian → each node evolves
        # independently under V'(φ). The tachyonic instability amplifies
        # the perturbation. Once φ̇ > v_th, walkers emit and begin
        # observing node pairs, creating the first bonds.
        has_walkers = all_events > 0
        if not has_walkers and sum(a.size for a in self.adj) == 0:
            # No walkers AND no bonds: bootstrap — compute all nodes
            active_set = set(range(N))
            warm_set = set()

        compute_set = active_set | warm_set
        compute_list = sorted(compute_set)

        # ---------------------------------------------------------------
        # Step 3: Measurement of cold→hot nodes (CF07)
        # When a walker arrives at an unobserved node, the state
        # coarse-grains from superposition to classical observation.
        # The analytical solution IS the measurement result.
        # ---------------------------------------------------------------
        for i in active_set:
            i_int = int(i)
            if self.last_visit[i_int] >= 0 and self.last_visit[i_int] < tick - 1:
                self._measure_cold_node(i_int, tick)
            self.last_visit[i_int] = tick

        # ---------------------------------------------------------------
        # Step 4: Node telegraph solve (compute set only)
        #   τ_eff·φ̈ + φ̇ = D·L_ψ(φ) − V'(φ)
        # ---------------------------------------------------------------
        phi_new = self.phi_curr.copy()

        if compute_list:
            lap_full = bond_weighted_laplacian(self.phi_curr, self.adj, self.psi_curr)
            dV = node_potential_derivative(self.phi_curr)

            for i in compute_list:
                tau_eff = float(TAU * np.exp(BETA_DEBT * self.debt[i]))
                rhs_i = float(D_DIFF * lap_full[i] - dV[i])
                rhs_i += float(self._stim[i])

                phi_new[i] = (
                    rhs_i + (2.0 * tau_eff + 1.0) * self.phi_curr[i]
                    - tau_eff * self.phi_prev[i]
                ) / (tau_eff + 1.0)

            phi_new[compute_list] = np.clip(phi_new[compute_list], 0.0, 1.0)

        # ---------------------------------------------------------------
        # Step 5: Bond telegraph solve (§0.1b, compute set only)
        #   ε_bond·ψ̈ + ψ̇ = −U'(ψ) + ½(φ_j − φ_i)²
        # ---------------------------------------------------------------
        for i in compute_list:
            nbrs = self.adj[i]
            if nbrs.size == 0:
                continue

            psi_c = self.psi_curr[i]
            psi_p = self.psi_prev[i]

            dU = bond_potential_derivative(psi_c, lam_bond=LAMBDA_BOND)
            grad_src = bond_gradient_source(self.phi_curr[i], self.phi_curr[nbrs])
            rhs_bond = -dU + grad_src

            psi_new = (
                rhs_bond + (2.0 * EPS_BOND + 1.0) * psi_c - EPS_BOND * psi_p
            ) / (EPS_BOND + 1.0)

            self.psi_prev[i] = psi_c.copy()
            self.psi_curr[i] = np.clip(psi_new, 0.0, 1.0).astype(np.float32)

        # ---------------------------------------------------------------
        # Step 6: Bond instantiation from walker observation
        # Walkers observe node pairs. If the pair is not yet connected,
        # a bond DOF is instantiated at ψ=0 (vacuum). The gradient
        # source ½(Δφ)² determines whether it condenses or decoheres.
        # ---------------------------------------------------------------
        instantiated = 0
        for u, v in bond_pairs:
            if v not in self.adj[u]:
                self._instantiate_bond(u, v)
                instantiated += 1

        # ---------------------------------------------------------------
        # Step 7: Decoherence sweep (CF07 — remove bonds below thermal floor)
        # ---------------------------------------------------------------
        removed = self._decohere_bonds(compute_list)

        # ---------------------------------------------------------------
        # Step 8: Measure kT from dynamics (CF06 §4.3, equipartition)
        #   kT = ½·Var(φ̇) over compute set. Always measured.
        # ---------------------------------------------------------------
        if len(compute_list) > 1:
            phi_dot_active = phi_new[compute_list] - self.phi_curr[compute_list]
            measured_kT = 0.5 * float(np.var(phi_dot_active))
            self.kT = max(measured_kT, 1e-30)

        # ---------------------------------------------------------------
        # Step 9: Debt update
        # ---------------------------------------------------------------
        if compute_list:
            phi_dot_new = np.abs(phi_new[compute_list] - self.phi_curr[compute_list])
            self.debt[compute_list] += phi_dot_new.astype(np.float64)
            self.debt[compute_list] *= (1.0 - 0.01)  # slow decay

        # ---------------------------------------------------------------
        # Step 10: State rotation
        # ---------------------------------------------------------------
        self.phi_prev = self.phi_curr.copy()
        self.phi_curr = phi_new

        # Decay stimulus
        self._stim *= 0.9

        # Telemetry
        total_edges = sum(a.size for a in self.adj)
        mean_degree = total_edges / N if N > 0 else 0.0

        return {
            "tick": tick,
            "n_walkers": all_events,
            "n_active": len(active_set),
            "n_warm": len(warm_set),
            "n_computed": len(compute_list),
            "bonds_instantiated": instantiated,
            "bonds_removed": removed,
            "kT": self.kT,
            "phi_mean": float(np.mean(self.phi_curr)),
            "phi_var": float(np.var(self.phi_curr)),
            "mean_degree": mean_degree,
        }

    # ------------------------------------------------------------------
    # Bond lifecycle
    # ------------------------------------------------------------------

    def stimulate_indices(self, idxs, amp: float = 0.05) -> None:
        """Deterministic stimulus injection into the field."""
        for i in idxs:
            if 0 <= i < self.N:
                self._stim[i] += amp

    def _instantiate_bond(self, u: int, v: int) -> None:
        """
        Instantiate bond DOF on edge (u,v) at ψ = 0 (vacuum).

        The gradient source ½(φ_j − φ_i)² from the action variation
        tilts the double-well. At domain walls the bond condenses via
        spinodal decomposition. Away from walls, it decoheres.
        Source: §0.1b (extended discrete action variation).
        """
        self.adj[u] = np.append(self.adj[u], np.int32(v))
        self.psi_curr[u] = np.append(self.psi_curr[u], np.float32(0.0))
        self.psi_prev[u] = np.append(self.psi_prev[u], np.float32(0.0))
        self.adj[v] = np.append(self.adj[v], np.int32(u))
        self.psi_curr[v] = np.append(self.psi_curr[v], np.float32(0.0))
        self.psi_prev[v] = np.append(self.psi_prev[v], np.float32(0.0))

    def _decohere_bonds(self, compute_nodes: List[int]) -> int:
        """
        Remove bonds below the dynamic decoherence floor (CF07).
        """
        eta_floor = bond_decoherence_floor(self.kT)
        bonds_removed = 0

        for i in compute_nodes:
            i = int(i)
            if self.adj[i].size == 0:
                continue

            # E0 substrate edges are fixed; they can drop to psi=0 but never
            # leave the adjacency list. Ephemeral edges are removed if below floor.
            in_e0 = np.isin(self.adj[i], self.E0[i])
            keep = (self.psi_curr[i] >= eta_floor) | in_e0
            if not np.all(keep):
                dead_nbrs = self.adj[i][~keep]
                bonds_removed += int((~keep).sum())
                
                self.adj[i] = self.adj[i][keep]
                self.psi_curr[i] = self.psi_curr[i][keep]
                self.psi_prev[i] = self.psi_prev[i][keep]

                for j in dead_nbrs:
                    j = int(j)
                    mask = self.adj[j] != i
                    self.adj[j] = self.adj[j][mask]
                    self.psi_curr[j] = self.psi_curr[j][mask]
                    self.psi_prev[j] = self.psi_prev[j][mask]

        return bonds_removed

    def _measure_cold_node(self, node: int, tick_now: int) -> None:
        """
        Measurement of an unobserved node upon walker arrival (CF07).

        The node was in superposition (unobserved). When the gauge boson
        (walker) arrives, the state coarse-grains into a classical
        measurement. The analytical exponential relaxation toward the
        nearest potential well IS the projection — it's what the
        measurement returns.
        """
        t_last = int(self.last_visit[node])
        if t_last < 0:
            t_last = 0
        dt_gap = tick_now - t_last
        if dt_gap <= 1:
            return

        tau_eff = float(TAU * np.exp(BETA_DEBT * self.debt[node]))

        # Node field: exponential relaxation toward nearest well
        phi_well = round(float(self.phi_curr[node]))  # 0.0 or 1.0
        decay = float(np.exp(-dt_gap / tau_eff))

        self.phi_curr[node] = phi_well + (self.phi_curr[node] - phi_well) * decay
        self.phi_prev[node] = phi_well + (self.phi_prev[node] - phi_well) * decay

        # Bond fields: each bond relaxes toward its nearest well
        for k in range(self.adj[node].size):
            psi_well = round(float(self.psi_curr[node][k]))
            bond_decay = float(np.exp(-dt_gap / float(EPS_BOND)))
            self.psi_curr[node][k] = psi_well + (
                self.psi_curr[node][k] - psi_well
            ) * bond_decay

        # Debt: exponential decay toward zero
        self.debt[node] *= (1.0 - BETA_DEBT) ** dt_gap
