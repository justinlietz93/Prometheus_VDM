"""
Gauge Excitation Physics — Emission and Propagation
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Walkers are gauge excitations (CF09) radiated by nodes whose kinetic
energy exceeds thermal equilibrium.  They propagate along bond-weighted
edges.

ZERO OPEN DESIGN CHOICES.  Every formula derived below:

  Emission count — energy conservation + equipartition (CF06)
  Hop selection  — ergodic theory on chaotic dynamics (A4 + CF04)
  Bond IC        — A0 closure (see connectome.py)

No np.random calls in dynamics.  No engineering parameters.

Source: CF09 (gauge boson transport), CF04 (causal cone),
        CF07 (observability/measurement), CF06 (equipartition).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Tuple

import numpy as np


# ═══════════════════════════════════════════════════════════════════════════
# Data structures
# ═══════════════════════════════════════════════════════════════════════════

@dataclass(slots=True)
class WalkerEvent:
    """One hop of a gauge excitation."""
    source: int
    target: int
    emit_index: int


# ═══════════════════════════════════════════════════════════════════════════
# Thermal physics (CF06)
# ═══════════════════════════════════════════════════════════════════════════

def thermal_velocity(kT: float) -> float:
    """v_th = √(2·kT).  Equipartition, CF06 §4.3."""
    if kT <= 0.0:
        return 0.0
    return float(np.sqrt(2.0 * kT))


# ═══════════════════════════════════════════════════════════════════════════
# Gauge excitation emission — DERIVED, not a design choice
#
# DERIVATION (energy conservation + equipartition):
#
#   A node has kinetic energy E_k = ½ φ̇_i².
#   Thermal equilibrium contributes kT per mode (CF06 §4.3, equipartition).
#   Excess kinetic energy above thermal:
#
#       ΔE = max(½ φ̇_i² − kT, 0)
#
#   Each gauge quantum carries energy kT.  Below kT it is thermally
#   indistinguishable from vacuum fluctuations (CF07 §4.1).
#   Number of distinguishable quanta the excess can produce:
#
#       n_i = floor(ΔE / kT)
#           = floor(φ̇_i² / (2·kT) − 1)
#
#   Using v_th² = 2·kT:
#
#       n_i = floor((φ̇_i / v_th)² − 1)
#
#   Properties:
#     |φ̇| = v_th  →  n = 0   (thermal equilibrium, no emission)
#     |φ̇| = 0     →  n = 0   (at rest, no emission)
#     |φ̇| < v_th  →  n = 0   (below thermal, no emission)
#     |φ̇| = 2·v_th → n = 3   (excess = 3·kT → 3 quanta)
#
#   No free parameters.  Floor because you can't emit a fraction
#   of a quantum.  The −1 is because the first kT of kinetic energy
#   IS thermal — it doesn't produce a distinguishable excitation.
#
#   Source: CF06 §4.3 (equipartition), CF07 §4.1 (observability
#           threshold), CF09 (gauge excitations exist).
# ═══════════════════════════════════════════════════════════════════════════

def emit_counts(phi_dot: np.ndarray, kT: float) -> np.ndarray:
    """
    Per-node gauge excitation count from energy conservation.

    n_i = floor(φ̇_i² / (2·kT) − 1)  when |φ̇_i| > v_th, else 0.

    Derived above.  Source: CF06, CF07, CF09.
    """
    if kT <= 0.0:
        return np.zeros(phi_dot.shape[0], dtype=np.int32)

    two_kT = 2.0 * kT
    ratio = phi_dot ** 2 / two_kT - 1.0   # ΔE/kT
    ratio = np.maximum(ratio, 0.0)         # no negative emission
    return np.floor(ratio).astype(np.int32)


# ═══════════════════════════════════════════════════════════════════════════
# Hop selection — DERIVED, not a design choice
#
# DERIVATION (ergodic theory on deterministic chaos):
#
#   The hop distribution is P(i→j) = ψ_ij / Σ_k ψ_ik.
#   Source: CF09 — gauge field propagates along connection, connection
#   strength IS the bond field.  Stronger bonds carry more gauge traffic.
#   This distribution is parameter-free: normalized bond weight.
#
#   To SAMPLE this distribution without np.random, we need a uniform
#   variate u ∈ [0, 1) to walk the CDF.  The field state provides it:
#
#   N coupled nonlinear oscillators with tachyonic instability and
#   self-modifying topology have positive Lyapunov exponents for N ≫ 1.
#   (Standard result: nonlinear coupling + double-well → chaotic
#   trajectories.  See Strogatz, "Nonlinear Dynamics and Chaos", ch. 9;
#   Pikovsky et al., "Synchronization", ch. 5.)
#
#   Positive Lyapunov → mixing → Weyl equidistribution theorem:
#   For any sufficiently smooth function f of the state,
#
#       frac(f(φ_i, φ̇_i, ψ_ij, ...))
#
#   is uniformly distributed on [0, 1) after sufficient mixing time.
#
#   A uniform variate on [0, 1) is exactly what CDF inversion requires.
#   The specific function f is irrelevant — ANY smooth nonlinear function
#   of the chaotic state works — because the Lyapunov mixing guarantees
#   the fractional parts explore [0, 1) uniformly.
#
#   We use f = |φ̇_i| · (1 + emit_index).  The emit_index ensures
#   different quanta from the same node get different phases.
#
#   Interpretation (VDM): the hop outcome is determined by the full
#   J-limb state, which includes sub-representational structure that
#   appears uniformly distributed when projected through any finite-
#   precision observable.  The M-limb shadow of J-limb determinism
#   IS the probability distribution.
#
#   Source: A4 (metriplectic split — J-limb deterministic),
#           CF04 (nonlinear telegraph → chaotic trajectories),
#           Weyl equidistribution (standard, 1916).
# ═══════════════════════════════════════════════════════════════════════════

def _select_neighbor(
    node: int,
    adj: List[np.ndarray],
    psi: List[np.ndarray],
    phi_dot: np.ndarray,
    emit_index: int,
) -> int:
    """
    Bond-weighted neighbor selection via deterministic field state.

    P(i→j) ∝ ψ_ij (CF09: gauge propagates along connection strength).
    CDF sampled by u = frac(|φ̇_i|·(1 + emit_index)) (Weyl/ergodic).

    Derived above.  Source: CF09, A4, CF04, Weyl (1916).
    """
    nbrs = adj[node]
    if nbrs.size == 0:
        return -1

    weights = psi[node]
    w_sum = float(np.sum(weights))
    if w_sum < 1e-30:
        return -1

    # Deterministic phase from chaotic field state (Weyl equidistribution)
    u = abs(float(phi_dot[node])) * (1.0 + emit_index)
    u = u - int(u)  # frac()

    # CDF inversion
    cdf = 0.0
    for k in range(nbrs.size):
        cdf += float(weights[k]) / w_sum
        if cdf >= u:
            return int(nbrs[k])

    return int(nbrs[-1])


# ═══════════════════════════════════════════════════════════════════════════
# Single walker propagation
# ═══════════════════════════════════════════════════════════════════════════

def propagate_one(
    source: int,
    adj: List[np.ndarray],
    psi: List[np.ndarray],
    phi_dot: np.ndarray,
    emit_index: int,
    v_th: float,
    h_max: int,
) -> Tuple[List[WalkerEvent], List[Tuple[int, int]]]:
    """
    Propagate a single gauge excitation from source.

    Decoherence (CF07 §4.1): walker stops when it arrives at a node
    where |φ̇| ≤ v_th — thermally indistinguishable from vacuum.
    Propagation range = spatial extent of the excited region.
    No TTL.  Physics determines range.

    Bond candidates: unconnected pairs where both endpoints are
    observable (|φ̇| > v_th, CF07) and gradient exists.
    """
    events: List[WalkerEvent] = []
    bond_candidates: List[Tuple[int, int]] = []
    current = source

    for hop in range(h_max):
        # Decoherence: current node at thermal equilibrium? (CF07)
        if hop > 0 and abs(float(phi_dot[current])) <= v_th:
            break

        target = _select_neighbor(current, adj, psi, phi_dot, emit_index + hop)
        if target < 0:
            break

        events.append(WalkerEvent(
            source=current, target=target, emit_index=emit_index))

        # Bond candidate: both endpoints observable and not connected
        if (abs(float(phi_dot[current])) > v_th
                and abs(float(phi_dot[target])) > v_th):
            if target not in adj[current]:
                bond_candidates.append(
                    (min(current, target), max(current, target)))

        # Transitive observation: target's neighbors visible to walker
        if abs(float(phi_dot[current])) > v_th:
            for k in adj[target]:
                k_int = int(k)
                if k_int != current and abs(float(phi_dot[k_int])) > v_th:
                    if k_int not in adj[current]:
                        bond_candidates.append(
                            (min(current, k_int), max(current, k_int)))

        current = target

    return events, bond_candidates


# ═══════════════════════════════════════════════════════════════════════════
# Full gauge step
# ═══════════════════════════════════════════════════════════════════════════

def run_gauge_step(
    phi_dot: np.ndarray,
    adj: List[np.ndarray],
    psi: List[np.ndarray],
    kT: float,
    c_signal: float,
) -> Tuple[List[WalkerEvent], Set[int], Set[int], Set[Tuple[int, int]]]:
    """
    Full gauge emission + propagation for one tick.

    When kT = 0 (superposition, pre-stimulus): zero walkers, empty sets.
    Once stimulus creates field velocities → kT > 0 → walkers emit.
    """
    N = phi_dot.shape[0]
    v_th = thermal_velocity(kT)

    all_events: List[WalkerEvent] = []
    active_set: Set[int] = set()
    warm_set: Set[int] = set()
    bond_pairs: Set[Tuple[int, int]] = set()

    if v_th <= 0.0:
        return all_events, active_set, warm_set, bond_pairs

    # Max hops from causal cone: h_max = floor(c / v_th) (CF04)
    h_max = max(1, int(np.floor(c_signal / v_th)))

    # Emission counts from energy conservation (derived above)
    n_emit = emit_counts(phi_dot, kT)

    for i in range(N):
        count = int(n_emit[i])
        if count <= 0:
            continue

        active_set.add(i)

        for ei in range(count):
            events, candidates = propagate_one(
                source=i, adj=adj, psi=psi, phi_dot=phi_dot,
                emit_index=ei, v_th=v_th, h_max=h_max,
            )
            all_events.extend(events)
            for ev in events:
                active_set.add(ev.source)
                active_set.add(ev.target)
            for pair in candidates:
                bond_pairs.add(pair)

    # Warm set: neighbors of active (Laplacian boundary layer)
    for i in active_set:
        for j in adj[i]:
            j_int = int(j)
            if j_int not in active_set:
                warm_set.add(j_int)

    return all_events, active_set, warm_set, bond_pairs
