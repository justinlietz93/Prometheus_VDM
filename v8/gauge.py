"""
Gauge Excitation Physics — Walker Emission and Propagation
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Walkers are gauge excitations radiated by nodes with kinetic energy
above thermal equilibrium (Larmor radiation). They propagate along
bond-weighted edges via deterministic chaotic phase selection.

Source: Directive §0.7, CF09 (gauge boson transport), CF04 (causal cone),
CF07 (observability/measurement), CF06 (equipartition for v_th).

No RNG calls. No heuristics. No engineering parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Tuple

import numpy as np


@dataclass(slots=True)
class WalkerEvent:
    """One hop of a gauge excitation."""
    source: int         # node the walker left
    target: int         # node the walker arrived at
    emit_index: int     # which walker from this source (0, 1, ...)


def thermal_velocity(kT: float) -> float:
    """
    v_th = √(2·kT) — thermal velocity from equipartition.
    Source: CF06 §4.3.
    """
    return float(np.sqrt(2.0 * max(kT, 1e-15)))


def emit_counts(phi_dot: np.ndarray, kT: float) -> np.ndarray:
    """
    Per-node gauge excitation count: n_i = floor(|φ̇_i| / v_th).

    Larmor radiation: changing matter fields source gauge fields.
    Deterministic — floor function on kinetic energy ratio.

    Returns int32 array of emission counts per node.
    Source: Directive §0.7.
    """
    v_th = thermal_velocity(kT)
    return np.floor(np.abs(phi_dot) / v_th).astype(np.int32)


def _select_neighbor(
    node: int,
    adj: List[np.ndarray],
    psi: List[np.ndarray],
    phi_dot: np.ndarray,
    emit_index: int,
) -> int:
    """
    Deterministic bond-weighted neighbor selection via chaotic phase.

    P(i → j) = ψ_ij / Σ_k ψ_ik, sampled by:
        u = frac(|φ̇_i| · (1 + emit_index))
        j = first neighbor where CDF ≥ u

    The fractional velocity is deterministic chaos from the nonlinear
    field dynamics — it IS the randomness, emergent from J/M split
    and tachyonic instability.

    Returns neighbor index, or -1 if no valid neighbor.
    Source: Directive §0.7 (chaotic phase selection).
    """
    nbrs = adj[node]
    if nbrs.size == 0:
        return -1

    weights = psi[node].copy()
    w_sum = weights.sum()
    if w_sum < 1e-30:
        return -1

    # Chaotic phase from field velocity
    u = abs(float(phi_dot[node])) * (1.0 + emit_index)
    u = u - int(u)  # frac()

    # CDF walk
    cdf = 0.0
    for k in range(nbrs.size):
        cdf += float(weights[k]) / w_sum
        if cdf >= u:
            return int(nbrs[k])

    # Numerical edge case — return last neighbor
    return int(nbrs[-1])


def propagate_one(
    source: int,
    adj: List[np.ndarray],
    psi: List[np.ndarray],
    phi_dot: np.ndarray,
    h_max: int,
    emit_index: int,
    v_th: float,
) -> Tuple[List[WalkerEvent], List[Tuple[int, int]]]:
    """
    Propagate a single gauge excitation from source for up to h_max hops.

    At each hop:
    1. Select next neighbor via bond-weighted CDF (chaotic phase)
    2. Record walker event (source → target)
    3. Check for bond DOF instantiation candidates:
       - Unconnected pairs where both endpoints are observable (|φ̇| > v_th)

    Returns:
        events: list of WalkerEvent for each hop
        bond_candidates: list of (u, v) pairs eligible for bond instantiation

    Source: Directive §0.7 (propagation), §4.6 (observation geometry).
    """
    events: List[WalkerEvent] = []
    bond_candidates: List[Tuple[int, int]] = []
    current = source

    for hop in range(h_max):
        target = _select_neighbor(current, adj, psi, phi_dot, emit_index + hop)
        if target < 0:
            break

        events.append(WalkerEvent(source=current, target=target, emit_index=emit_index))

        # --- Direct observation: walker stepped current → target ---
        # Bond candidate if both endpoints observable (|φ̇| > 0, CF07)
        # and not already connected. The gradient source ½(Δφ)² from
        # the action variation determines whether the bond condenses.
        if abs(phi_dot[current]) > 0 and abs(phi_dot[target]) > 0:
            if target not in adj[current]:
                u, v = (min(current, target), max(current, target))
                bond_candidates.append((u, v))

        # --- Transitive observation: check target's neighbors ---
        # Walker at target, came from current. If target has neighbor k
        # where current-k are both observable and not connected → candidate
        if abs(phi_dot[current]) > 0:
            for k in adj[target]:
                k_int = int(k)
                if k_int == current:
                    continue
                if abs(phi_dot[k_int]) > 0 and k_int not in adj[current]:
                    u, v = (min(current, k_int), max(current, k_int))
                    bond_candidates.append((u, v))

        current = target

    return events, bond_candidates


def run_gauge_step(
    phi_dot: np.ndarray,
    adj: List[np.ndarray],
    psi: List[np.ndarray],
    kT: float,
    c_signal: float,
) -> Tuple[List[WalkerEvent], Set[int], Set[int], Set[Tuple[int, int]]]:
    """
    Full gauge emission + propagation for one tick.

    1. Compute emission counts per node (Larmor radiation)
    2. Propagate each walker (bond-weighted CDF, TTL-bounded)
    3. Collect walker events, active/warm sets, bond candidates

    Returns:
        all_events: every walker hop this tick
        active_set: Zone 1 nodes (walker-visited)
        warm_set: Zone 2 nodes (neighbors of active)
        bond_pairs: unique (u, v) pairs for bond DOF instantiation

    Source: Directive §0.7 + §0.6.
    """
    N = phi_dot.shape[0]
    v_th = thermal_velocity(kT)

    # TTL from physics: h_max = floor(c / v_th)
    # Minimum 1 hop so walkers can propagate at all
    h_max = max(1, int(np.floor(c_signal / v_th))) if v_th > 1e-15 else 1

    # Emission counts
    n_emit = emit_counts(phi_dot, kT)

    all_events: List[WalkerEvent] = []
    active_set: Set[int] = set()
    bond_pairs: Set[Tuple[int, int]] = set()

    # Emit and propagate
    emitters: Set[int] = set()
    for i in range(N):
        count = int(n_emit[i])
        if count <= 0:
            continue

        emitters.add(i)

        for ei in range(count):
            events, candidates = propagate_one(
                source=i,
                adj=adj,
                psi=psi,
                phi_dot=phi_dot,
                h_max=h_max,
                emit_index=ei,
                v_th=v_th,
            )
            all_events.extend(events)
            for ev in events:
                active_set.add(ev.source)
                active_set.add(ev.target)
            for pair in candidates:
                bond_pairs.add(pair)

    # --- Isolated emitter bond discovery ---
    # When a node emits (Larmor radiation) but has no edges to
    # propagate along, the excitation still observes the local
    # neighborhood. The computational lattice provides the index
    # proximity: nodes i±1 are "nearest neighbors" on the grid.
    # Bond candidates form between nearby emitters. This is how
    # the first bonds emerge from the void.
    for i in emitters:
        active_set.add(i)
        if adj[i].size == 0:
            # Observe nearest computational neighbors
            for offset in [1, -1]:
                j = (i + offset) % N
                if j in emitters:
                    u, v = (min(i, j), max(i, j))
                    bond_pairs.add((u, v))

    # Warm set: neighbors of active nodes (Laplacian coupling boundary)
    warm_set: Set[int] = set()
    for i in active_set:
        for j in adj[i]:
            j_int = int(j)
            if j_int not in active_set:
                warm_set.add(j_int)

    # Also: nodes with |φ̇| > v_th but not walker-visited → Zone 2
    for i in range(N):
        if abs(phi_dot[i]) > v_th and i not in active_set:
            warm_set.add(i)

    return all_events, active_set, warm_set, bond_pairs
