"""
VDM v9 Connectome — Self-Modifying Graph with Metriplectic Klein-Gordon
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Two coupled telegraph fields (node φ, bond ψ) on a self-modifying graph.

INITIAL STATE — DERIVED, not a design choice:

  φ_i(0) = 0.5    All nodes in superposition (unstable vacuum)
  φ̇_i(0) = 0      Field at rest
  ψ_ij(0) = 0.5   All bonds in superposition on computational lattice

  DERIVATION of ψ(0) = 0.5 from A0 (Closure):

    A0 states: "Only objects defined inside the framework are allowed;
    no external primitives as foundations."

    The discrete action (VDM-AX-004) treats both fields symmetrically.
    Both have Ginzburg-Landau double-well potentials:
      V(φ)  = λ      · φ²(1−φ)²     minima at 0, 1; maximum at 0.5
      U(ψ)  = λ_bond · ψ²(1−ψ)²     minima at 0, 1; maximum at 0.5

    φ = 0.5 is the maximum-symmetry state for nodes: equal distance
    from both wells, maximum uncertainty about which well the node
    belongs to.  This is "superposition" — no observation has selected
    a well.

    By action symmetry, ψ = 0.5 is the identical state for bonds:
    maximum uncertainty about whether the bond is condensed (ψ = 1)
    or decohered (ψ = 0).

    Any other choice for ψ(0) — say ψ = 0.0 — injects information
    about which well the bond should be near.  Where does this
    information come from?  There is no source inside the framework.
    This violates A0: it introduces an external primitive (the
    assertion "bonds start decohered") with no derivation chain.

    Therefore: the unique A0-compliant IC for a GL field with no
    prior observation is the unstable vacuum of its potential.
    ψ(0) = 0.5 is forced, not chosen.

The system is inert until it receives external stimulus.
Stimulus = first observation = symmetry breaking.

Source: VDM-AX-001, VDM-AX-004, A0, A4, A5,
        CF01/CF02, CF04, CF07, CF09.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

import numpy as np

from .void_equations import (
    D_DIFF, TAU, C_SIGNAL, EPS_BOND,
    LAMBDA, LAMBDA_BOND, BETA_DEBT,
    bond_decoherence_floor,
    bond_gradient_source,
    bond_potential_derivative,
    bond_weighted_laplacian,
    node_potential_derivative,
)
from .gauge import run_gauge_step


class Connectome:
    """
    Self-modifying graph with coupled node (φ) and bond (ψ) fields.

    State:
        phi_curr, phi_prev  — node field (second-order telegraph)
        adj                 — ragged adjacency (list of int32 arrays)
        psi_curr, psi_prev  — bond field (parallel to adj)
        debt                — per-node exponential throttle
        kT                  — measured effective temperature
    """

    def __init__(
        self,
        N: int,
        initial_edges: List[Tuple[int, int]],
    ):
        """
        Initialize connectome in superposition.

        Args:
            N: number of nodes.
            initial_edges: computational lattice — list of (i, j) pairs.
                Provides spatial coupling so the Laplacian is nonzero
                when stimulus breaks the symmetry.  The PHYSICAL bond
                pattern (which edges survive) emerges from dynamics.
        """
        self.N = N

        # ── Node field IC: superposition (A0 + action symmetry) ──
        # V(φ) has unstable vacuum at φ = 0.5.  V'(0.5) = 0.
        # Maximum symmetry, zero information about well membership.
        # φ̇(0) = 0: field at rest.  Waiting for first observation.
        self.phi_curr = np.full(N, 0.5, dtype=np.float64)
        self.phi_prev = np.full(N, 0.5, dtype=np.float64)

        # ── Bond field IC: superposition (A0 + action symmetry) ──
        # U(ψ) has unstable vacuum at ψ = 0.5.  U'(0.5) = 0.
        # Maximum symmetry, zero information about condensation.
        # Derivation in module docstring.
        self.adj: List[np.ndarray] = [
            np.array([], dtype=np.int32) for _ in range(N)
        ]
        self.psi_curr: List[np.ndarray] = [
            np.array([], dtype=np.float64) for _ in range(N)
        ]
        self.psi_prev: List[np.ndarray] = [
            np.array([], dtype=np.float64) for _ in range(N)
        ]

        for u, v in initial_edges:
            if u != v and v not in self.adj[u]:
                self._add_bond(u, v, psi_init=0.5)

        # ── Auxiliary state ──
        self.debt = np.zeros(N, dtype=np.float64)
        self.last_visit = np.full(N, -1, dtype=np.int32)

        # kT = 0: no thermal energy, no walkers, superposition.
        self.kT: float = 0.0
        self._tick: int = 0

        # External source coupling J_ext(x,t).
        # Set each tick by the external observer via stimulate().
        # Read by the integrator, then zeroed.  No internal decay —
        # the field response persists in {φ, φ̇} and decays through
        # M-limb damping (γ·φ̇) already in the telegraph equation.
        self._J_ext = np.zeros(N, dtype=np.float64)

    # ══════════════════════════════════════════════════════════════════════
    # Stimulus — the first observation
    # ══════════════════════════════════════════════════════════════════════

    def stimulate(self, indices: List[int], amplitudes: np.ndarray) -> None:
        """
        Set external source coupling J_ext(x,t) for this tick.

        Enters the invariant functional as:
            I[φ,Π] = ∫ [½Π² + ½|∇φ|² + V(φ) − J_ext·φ] dx

        The J-limb variation then gives:
            Π̇ = ∇²φ − V'(φ) + J_ext(x,t)

        The source modifies the energy landscape, not the dynamics.
        A0 is satisfied: the formalism (J, M, degeneracy) is unchanged.
        The external source is a boundary condition, not a foundation.

        Source: standard linear source coupling in field theory.

        Args:
            indices: which nodes receive source coupling
            amplitudes: J_ext value per node (any modality mapped to scalar)
        """
        for i, amp in zip(indices, amplitudes):
            if 0 <= i < self.N:
                self._J_ext[i] = float(amp)

    def stimulate_indices(self, idxs: List[int], amp: float = 0.05) -> None:
        """Convenience: uniform source coupling."""
        for i in idxs:
            if 0 <= i < self.N:
                self._J_ext[i] = float(amp)

    # ══════════════════════════════════════════════════════════════════════
    # Main physics step
    # ══════════════════════════════════════════════════════════════════════

    def step(self, tick: int) -> Dict:
        """
        One tick of metriplectic Klein-Gordon on self-modifying graph.

        Before stimulus: φ = 0.5, φ̇ = 0, kT = 0.  Nothing moves.
        After stimulus: tachyonic instability amplifies broken symmetry.
        Domains form.  Bonds reorganize.  Walkers emit.  Topology extends.
        """
        self._tick = tick
        N = self.N

        # ─── 1. Compute φ̇ from state ───
        phi_dot = self.phi_curr - self.phi_prev

        # ─── 2. Gauge emission + propagation (CF09, CF06, CF07) ───
        events, active_set, warm_set, bond_pairs = run_gauge_step(
            phi_dot=phi_dot,
            adj=self.adj,
            psi=self.psi_curr,
            kT=self.kT,
            c_signal=C_SIGNAL,
        )

        # Nodes with external source coupling are active (source = observation)
        stim_nodes = np.where(np.abs(self._J_ext) > 1e-15)[0]
        for idx in stim_nodes:
            active_set.add(int(idx))
            for j in self.adj[int(idx)]:
                if int(j) not in active_set:
                    warm_set.add(int(j))

        # Compute set with LOCAL CAUSALITY (three zones):
        #
        # Zone 1 (Active): Walker-visited + stimulated this tick.
        # Zone 2 (Warm):   Neighbors of active — Laplacian boundary.
        # Zone 3 (Unsettled): Previously observed, still rolling toward
        #                     a well.  Has definite state but hasn't
        #                     reached equilibrium.  Needs telegraph update.
        #
        # NOT computed: Superposition (never observed, last_visit = -1)
        #               Settled (in well, φ̇ ≈ 0 — analytical mode,
        #                        _measure_cold_node handles re-entry)
        #
        # The compute set is a MOVING SHELL, not a growing sphere.
        # Observation propagates at c_signal (CF04, A2 locality).

        # Mark stimulus as observation
        for i in stim_nodes:
            self.last_visit[int(i)] = tick

        # Warm set neighbors become observed by Laplacian coupling
        for i in warm_set:
            if self.last_visit[int(i)] < 0:
                self.last_visit[int(i)] = tick

        # Zone 3: observed + unsettled (still moving toward well)
        # A node is "settled" when:
        #   - Position: V(φ) - V(well) < kT → within thermal fluctuation
        #     of well minimum.  Near well: V(φ) ≈ λ·φ², so settled when
        #     |φ - well| < √(kT/λ).  Source: CF06 equipartition.
        #   - Velocity: |φ̇| < v_th = √(2kT).  Below thermal velocity,
        #     motion is indistinguishable from thermal background (CF07).
        #
        # When kT = 0 (pre-thermal): thresholds are 0, so ALL observed
        # nodes are unsettled.  Correct — without thermal background,
        # you can't distinguish "almost at well" from "at well."
        pos_thresh = float(np.sqrt(max(self.kT, 0.0) / LAMBDA))
        vel_thresh = float(np.sqrt(2.0 * max(self.kT, 0.0)))
        unsettled = set()
        for i in range(N):
            if self.last_visit[i] < 0:
                continue  # superposition, skip
            nearest_well = round(float(self.phi_curr[i]))
            if (abs(self.phi_curr[i] - nearest_well) > pos_thresh
                    or abs(float(phi_dot[i])) > vel_thresh):
                unsettled.add(i)

        compute_set = active_set | warm_set | unsettled
        compute_list = sorted(compute_set)

        # ─── 3. Cold-node measurement (CF07) ───
        for i in active_set:
            i_int = int(i)
            if (self.last_visit[i_int] >= 0
                    and self.last_visit[i_int] < tick - 1):
                self._measure_cold_node(i_int, tick)
            self.last_visit[i_int] = tick

        # ─── 4. Node telegraph solve (CF04, CF11) ───
        #   τ_eff·φ̈ + φ̇ = D·L_ψ(φ) − V'(φ) + stimulus
        phi_new = self.phi_curr.copy()

        if compute_list:
            lap = bond_weighted_laplacian(
                self.phi_curr, self.adj, self.psi_curr)
            dV = node_potential_derivative(self.phi_curr)

            for i in compute_list:
                tau_eff = TAU * np.exp(BETA_DEBT * self.debt[i])
                rhs = D_DIFF * lap[i] - dV[i] + self._J_ext[i]

                phi_new[i] = (
                    rhs + (2.0 * tau_eff + 1.0) * self.phi_curr[i]
                    - tau_eff * self.phi_prev[i]
                ) / (tau_eff + 1.0)

            phi_new[compute_list] = np.clip(
                phi_new[compute_list], 0.0, 1.0)

        # ─── 5. Bond telegraph solve (extended action) ───
        #   ε_bond·ψ̈ + ψ̇ = −U'(ψ) + ½(φ_j − φ_i)²
        for i in compute_list:
            nbrs = self.adj[i]
            if nbrs.size == 0:
                continue

            psi_c = self.psi_curr[i]
            psi_p = self.psi_prev[i]

            dU = bond_potential_derivative(psi_c, lam_bond=LAMBDA_BOND)
            grad_src = bond_gradient_source(
                self.phi_curr[i], self.phi_curr[nbrs])
            rhs_bond = -dU + grad_src

            psi_new = (
                rhs_bond + (2.0 * EPS_BOND + 1.0) * psi_c
                - EPS_BOND * psi_p
            ) / (EPS_BOND + 1.0)

            self.psi_prev[i] = psi_c.copy()
            self.psi_curr[i] = np.clip(psi_new, 0.0, 1.0)

        # ─── 6. Bond instantiation from walker observation (CF09) ───
        instantiated = 0
        for u, v in bond_pairs:
            if v not in self.adj[u]:
                # Walker-observed new edges start at ψ = 0.0 (vacuum).
                # NOT 0.5.  Difference: initial lattice edges have never
                # been observed — they're in superposition (0.5).
                # Walker-created edges are the RESULT of an observation:
                # the walker arrived, measured the pair, found a gradient.
                # The measurement collapses the bond to a definite state.
                # ψ = 0.0 is the vacuum from which spinodal condensation
                # proceeds if the gradient source is sufficient.
                self._add_bond(u, v, psi_init=0.0)
                instantiated += 1

        # ─── 7. Decoherence sweep (CF07) ───
        removed = self._decohere_bonds(compute_list)

        # ─── 8. Measure kT (CF06 §4.3, equipartition) ───
        if len(compute_list) > 1:
            phi_dot_new = phi_new[compute_list] - self.phi_curr[compute_list]
            self.kT = max(0.5 * float(np.var(phi_dot_new)), 0.0)

        # ─── 9. Debt update (CF11) ───
        #   Accumulate: debt += |φ̇| (integrated activity)
        #   Decay: M-limb relaxation on timescale τ_eff
        #     debt *= exp(−Δt/τ_eff_i)  where  τ_eff_i = τ·exp(β·debt_i)
        #   Self-consistent: high debt → slow recovery.  Low debt → fast.
        #   Uses only category 1 parameters (γ through τ, β_debt).
        if compute_list:
            speed = np.abs(phi_new[compute_list] - self.phi_curr[compute_list])
            self.debt[compute_list] += speed
            # M-limb relaxation of debt
            for idx in compute_list:
                tau_eff_i = TAU * np.exp(BETA_DEBT * self.debt[idx])
                self.debt[idx] *= np.exp(-1.0 / tau_eff_i)

        # ─── 10. State rotation ───
        self.phi_prev = self.phi_curr.copy()
        self.phi_curr = phi_new

        # Zero external source after integrator has read it.
        # The field response persists in {φ, φ̇}.
        # M-limb damping handles the rest.  No decay constant.
        self._J_ext[:] = 0.0

        # Telemetry
        total_edges = sum(a.size for a in self.adj)

        return {
            "tick": tick,
            "n_walkers": len(events),
            "n_active": len(active_set),
            "n_warm": len(warm_set),
            "n_computed": len(compute_list),
            "bonds_instantiated": instantiated,
            "bonds_removed": removed,
            "bonds_total": total_edges // 2,
            "kT": self.kT,
            "phi_mean": float(np.mean(self.phi_curr)),
            "phi_var": float(np.var(self.phi_curr)),
            "phi_dot_max": float(np.max(np.abs(phi_dot))),
            "mean_degree": total_edges / N if N > 0 else 0.0,
            "stimulus_active": len(stim_nodes),
        }

    # ══════════════════════════════════════════════════════════════════════
    # Bond lifecycle
    # ══════════════════════════════════════════════════════════════════════

    def _add_bond(self, u: int, v: int, psi_init: float = 0.0) -> None:
        """Add bond DOF at specified ψ value."""
        self.adj[u] = np.append(self.adj[u], np.int32(v))
        self.psi_curr[u] = np.append(self.psi_curr[u], psi_init)
        self.psi_prev[u] = np.append(self.psi_prev[u], psi_init)

        self.adj[v] = np.append(self.adj[v], np.int32(u))
        self.psi_curr[v] = np.append(self.psi_curr[v], psi_init)
        self.psi_prev[v] = np.append(self.psi_prev[v], psi_init)

    def _decohere_bonds(self, compute_nodes: list) -> int:
        """Remove bonds below thermal floor (CF07 §4.1)."""
        if self.kT <= 0.0:
            return 0

        eta_floor = bond_decoherence_floor(self.kT)
        removed = 0

        for i in compute_nodes:
            i = int(i)
            if self.adj[i].size == 0:
                continue

            alive = self.psi_curr[i] >= eta_floor
            if alive.all():
                continue

            dead_nbrs = self.adj[i][~alive]
            removed += int((~alive).sum())

            self.adj[i] = self.adj[i][alive]
            self.psi_curr[i] = self.psi_curr[i][alive]
            self.psi_prev[i] = self.psi_prev[i][alive]

            for j in dead_nbrs:
                j = int(j)
                mask = self.adj[j] != i
                self.adj[j] = self.adj[j][mask]
                self.psi_curr[j] = self.psi_curr[j][mask]
                self.psi_prev[j] = self.psi_prev[j][mask]

        return removed

    def _measure_cold_node(self, node: int, tick_now: int) -> None:
        """
        Measurement of unobserved node upon walker arrival (CF07).

        Exponential relaxation toward nearest potential well
        IS the measurement projection.
        """
        t_last = max(int(self.last_visit[node]), 0)
        dt_gap = tick_now - t_last
        if dt_gap <= 1:
            return

        tau_eff = TAU * np.exp(BETA_DEBT * self.debt[node])

        phi_well = round(float(self.phi_curr[node]))
        decay = np.exp(-dt_gap / tau_eff)

        self.phi_curr[node] = (
            phi_well + (self.phi_curr[node] - phi_well) * decay)
        self.phi_prev[node] = (
            phi_well + (self.phi_prev[node] - phi_well) * decay)

        for k in range(self.adj[node].size):
            psi_well = round(float(self.psi_curr[node][k]))
            bond_decay = np.exp(-dt_gap / EPS_BOND)
            self.psi_curr[node][k] = (
                psi_well + (self.psi_curr[node][k] - psi_well) * bond_decay)

        tau_eff_debt = TAU * np.exp(BETA_DEBT * self.debt[node])
        self.debt[node] *= np.exp(-dt_gap / tau_eff_debt)

    # ══════════════════════════════════════════════════════════════════════
    # State access
    # ══════════════════════════════════════════════════════════════════════

    def get_state(self) -> Dict:
        """Full state snapshot for logging."""
        return {
            "phi": self.phi_curr.copy(),
            "phi_prev": self.phi_prev.copy(),
            "debt": self.debt.copy(),
            "kT": self.kT,
            "tick": self._tick,
            "bonds_total": sum(a.size for a in self.adj) // 2,
        }
