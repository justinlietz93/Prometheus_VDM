# Runtime Physics Migration Directive v2

**Author:** Justin K. Lietz
**Date:** 2026-02-21
**Status:** APPROVED — supersedes v1
**Scope:** Complete migration from proxy heuristics to physics-derived runtime.

**Rule:** No lookup tables. No artificial toggles. No wall-clock timestamps in the physics path. Every parameter either derived from the lattice or a universal constant from the CF chain. Every instruction in this document is literal. If it says "delete," delete it. If it says "replace," replace every instance. If a function signature is specified, that is the exact signature. Codex must not invent parameters, add toggles, or introduce fallback paths.

---

## 0. Notation, Constants, and Scaling

### 0.1 The Equation of Motion

The runtime executes one equation per tick per node. From CF11 §2.3 + CF04 §3.1 + CF03 §1.1:

```
τ_eff(i) · (φ_{n+1,i} − 2φ_{n,i} + φ_{n-1,i}) / dt²
+ (φ_{n+1,i} − φ_{n,i}) / dt
= D · (Lφ)_{n,i} − V'(φ_{n,i}) + η_{n,i}
```

Where:
- `φ_{n,i}` is the scalar field at node `i`, tick `n`. Range [0, 1].
- `τ_eff(i) = τ · exp(β · debt_i)` — debt-throttled relaxation time (per-node).
- `dt = 1.0` — one tick = one physics timestep (dimensionless).
- `D` — diffusion coefficient (= γ, since lattice spacing a = 1).
- `(Lφ)_i = Σ_{j ∈ adj(i)} (φ_j − φ_i)` — graph Laplacian.
- `V(φ) = λ · φ²(1 − φ)²` — Ginzburg-Landau double-well on [0, 1].
- `V'(φ) = 2λ · φ(1 − φ)(1 − 2φ)` — potential derivative.
- `η_i = √(2 · D · kT) · ξ_i` — fluctuation-dissipation noise, ξ ~ N(0,1).

Rearranging for φ_{n+1} (implicit solve, dt = 1):

```
a_inertia(i) = τ_eff(i)          # since dt = 1, τ/dt² = τ
a_friction   = 1.0               # since dt = 1, 1/dt = 1
rhs(i)       = D·(Lφ)_i − V'(φ_i) + η_i

φ_new(i) = [ rhs(i) + (2·a_inertia(i) + a_friction)·φ_curr(i) − a_inertia(i)·φ_prev(i) ]
            / [ a_inertia(i) + a_friction ]

φ_new(i) = clip(φ_new(i), 0.0, 1.0)
```

### 0.2 Constants

| Name | Value | Role | Source |
|------|-------|------|--------|
| `τ` | `2.0` | Base telegraph relaxation time | CF04 §2.1 |
| `β` | `0.1` | Debt decay rate and throttle coefficient | CF03 §7.2 |
| `λ` | `1.0` | Double-well barrier height | CF03 §1.1 |
| `γ` (= D) | `0.05` | Diffusion / transport coupling | CF04 §6.1 |
| `kT` | `0.001` | Effective temperature | CF06 §4.3 |
| `debt_max` | `10.0` | Debt clamp ceiling | Engineering |
| `tau_e` | `250` | Eligibility decay (ticks) | CF04 / Fix 3 |
| `TOPO_PERIOD` | `50` | Ticks between topology updates | §0.3 scaling |
| `TOPO_THRESHOLD` | `0.01` | Eligibility threshold for edge nucleation/dissolution | §0.3 scaling |
| `TOPO_PATIENCE` | `100` | Ticks below threshold before probabilistic edge death | §0.3 scaling |

Derived:
- Propagation speed: `c = √(γ/τ) = √(0.05/2.0) ≈ 0.158` hops/tick
- Physics timestep: `dt_physics_us = int(√(τ/γ) × 1_000_000) = 6_324_555` μs

### 0.3 Eliminated Constants (must not appear anywhere after migration)

`F_REF`, `PHASE_SENS`, `ALPHA` (as reaction rate), `BETA` (as separate decay rate in GDSP), `domain_modulation`, `use_time_dynamics`, `kappa` (as separate from D).

### 0.4 Compute, Memory, and Scaling

#### DEVICE NEUTRALITY CONSTRAINT

The fast path (Kernels 1-5 in §4.3) MUST NOT assume a single address
space, a single execution device, or synchronous execution order between
independent operations.

Specifically:

1. The graph Laplacian, the pointwise solve, and the eligibility
   computation are independent operations on the same tick's data.
   They MUST NOT be fused into a single function that requires all
   three to execute on the same device.

2. All state arrays (phi_curr, phi_prev, debt, adj, act_tick, elig)
   MUST be stored in standard contiguous array formats (numpy ndarray,
   or equivalent) that can be copied to any device buffer without
   reshaping or reinterpretation.

3. The step() function MUST NOT call time.time(), time.time_ns(),
   threading primitives, or device-specific APIs. It operates on
   arrays and returns arrays. Device dispatch is the caller's
   responsibility.

These constraints ensure that the physics implementation is portable
to CPU-only, GPU-assisted, multi-GPU, or distributed execution without
modifying the physics code.

#### Why this architecture scales

The current runtime rebuilds the **entire adjacency** from scratch every tick: allocate N empty sets, draw O(s) alias samples per node, score every candidate pair, symmetrize, prune, bridge, freeze into sorted arrays. Cost: **O(N · s) per tick** where s is the candidate count (default 64). For N = 256 this is fine. For N = 1,000,000 it is 64 million operations per tick just for topology, before the field update even runs.

This is also physically wrong. The universe does not globally recompute which particles are adjacent every Planck time. Topology (which nodes are coupled) is persistent state that evolves slowly and locally, driven by the field dynamics. The quantum world computes in superposition with unbounded parallelism, but the moment observation occurs, thermodynamics imposes a finite-speed dissipative wall. Global adjacency rebuild is the computational equivalent of omniscient instantaneous observation — it violates the causal structure that the telegraph equation is supposed to enforce.

The physics-derived architecture has three cost regimes:

**Fast path (every tick): field update only — O(N · k)**

| Operation | Cost | Why |
|-----------|------|-----|
| Graph Laplacian `(Lφ)_i = Σ_j (φ_j − φ_i)` | O(N · k) | One pass over adjacency; k = mean degree |
| Potential derivative `V'(φ)` | O(N) | Pointwise polynomial per node |
| Noise generation | O(N) | One `np.random.standard_normal(N)` call |
| Telegraph implicit solve | O(N) | Pointwise division per node |
| Debt update | O(N) | Pointwise |
| Activation timestamp update | O(N) worst case, typically O(N_active) | Only nodes with |dφ| > threshold |
| Eligibility computation | O(N · k) | One pass over adjacency for neighbor timing |

**Total fast path: O(N · k) per tick.** For k = 12 and N = 1,000,000 this is 12M operations per tick. For k = 12 and N = 100,000,000 this is 1.2B — still tractable on modern hardware with vectorized numpy.

**Slow path (every TOPO_PERIOD ticks): topology evolution — O(N · k²)**

| Operation | Cost | Why |
|-----------|------|-----|
| Edge nucleation: 2-hop scan per eligible node | O(N_eligible · k²) | For each eligible node, scan k neighbors' k neighbors |
| Edge dissolution: per-edge eligibility check | O(N · k) | One pass over all edges |

**Total slow path: O(N · k²) every TOPO_PERIOD ticks.** Amortized cost: **O(N · k² / TOPO_PERIOD) per tick.** For k = 12, TOPO_PERIOD = 50: amortized 2.88 · N per tick. This is less than 3x the cost of the fast path's Laplacian computation, and it runs 50x less often.

**Comparison to current architecture:**

| Architecture | Per-tick cost | Topology persistence | Causal structure |
|---|---|---|---|
| Current (global rebuild) | O(N · s) = O(N · 64) | None — rebuilt from scratch | Violated — edges appear/disappear globally |
| Physics-derived (persistent + local) | O(N · k) + O(N · k²/P) | Persistent — edges carry forward | Preserved — changes propagate locally |

For k = 12, s = 64, P = 50: current costs ~64N per tick, physics-derived costs ~12N + ~2.88N ≈ 15N per tick. **The physics-derived architecture is ~4x cheaper per tick AND physically correct.**

#### Memory cost

| Array | Size | Dtype | Bytes (N=1M) |
|-------|------|-------|-------------|
| `phi_curr` | N | float32 | 4 MB |
| `phi_prev` | N | float32 | 4 MB |
| `debt` | N | float32 | 4 MB |
| `last_activation_tick` | N | int64 | 8 MB |
| `eligibility` | N | float32 | 4 MB |
| `adj` (neighbor lists) | N · k avg | int32 | 48 MB (k=12) |
| `W` (alias to phi_curr) | 0 | — | 0 (pointer) |

**Total: ~72 MB for N = 1,000,000 with k = 12.** The current architecture has the same memory footprint plus the ephemeral `neigh_sets` allocation (N Python sets with ~k entries each) rebuilt every tick, which thrashes the garbage collector.

#### Scaling law

The physics-derived runtime scales as:

```
T_tick = a · N · k + b · N · k² / TOPO_PERIOD
```

where a and b are hardware-dependent constants. For fixed k and TOPO_PERIOD, this is **O(N) per tick** — linear in the number of nodes. The current architecture is also O(N) per tick (with a much larger constant factor and no causal correctness).

The critical insight: **k does not need to grow with N.** In a real lattice, each site has a fixed number of neighbors regardless of system size. A 3D cubic lattice has k = 6 whether there are 1,000 or 1,000,000,000 sites. The graph Laplacian is a local operator. The physics only couples adjacent nodes. This is why the metriplectic dynamics scale — they are fundamentally local, like real physics.

If you want denser connectivity (higher k), the cost grows as O(N · k) for the fast path. But k is a physics parameter (related to the lattice coordination number / dimensionality of the substrate), not something that should scale with N.

---

## 1. File Operations

### 1.1 Files to DELETE entirely

| File | Reason |
|------|--------|
| `vdm_rt/core/Void_Debt_Modulation.py` (if exists) | Lookup table proxy |

### 1.2 Files to REWRITE (replace entire contents)

| File | New purpose |
|------|-------------|
| `vdm_rt/core/Void_Equations.py` | Klein-Gordon RHS only |
| `vdm_rt/core/void_dynamics_adapter.py` | Thin import; no fallback |

### 1.3 Files to MODIFY (specific sections)

| File | What changes |
|------|-------------|
| `vdm_rt/core/sparse_connectome.py` | `__init__`, `step`, `stimulate_indices`, new topology methods |
| `vdm_rt/core/sie_v2.py` | Deprecated; no longer called from hot path |
| `vdm_rt/runtime/stepper.py` | Remove `domain_modulation`, `use_time_dynamics`; change `sie_drive` path |
| `vdm_rt/runtime/loop/main.py` | Remove `dom_mod` usage; use physics clock for `t` |
| `vdm_rt/nexus.py` | Remove `dom_mod`, `use_time_dynamics` from constructor and config |
| `vdm_rt/io/ute.py` | Physics-clock timestamps |
| `vdm_rt/io/utd.py` | Frame-based output |
| `vdm_rt/io/uted/ute_mux.py` | Physics-clock timestamps |
| `vdm_rt/io/uted/frames.py` | No change from v1 spec |
| `vdm_rt/io/uted/ports.py` | No change from v1 spec |
| `vdm_rt/io/uted/utd_demux.py` | No change from v1 spec |

### 1.4 Files to CREATE

| File | Purpose |
|------|---------|
| `vdm_rt/io/uted/__init__.py` | Package init (v1 spec) |
| `vdm_rt/io/uted/frames.py` | SensorFrame / ActuatorFrame (v1 spec) |
| `vdm_rt/io/uted/ports.py` | PortSpec (v1 spec) |
| `vdm_rt/io/uted/ute_mux.py` | UTEMux + adapters (v1 spec, physics timestamps) |
| `vdm_rt/io/uted/utd_demux.py` | UTDDemux (v1 spec) |

---

## 2. Void_Equations.py — Complete Replacement

Replace the entire file with:

```python
"""
VDM Metriplectic Klein-Gordon Field Equations
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Single equation of motion derived from:
  CF01 (QGT → metriplectic brackets)
  CF03 (double-well potential, Ginzburg-Landau)
  CF04 (telegraph-Fisher finite-speed transport)
  CF06 (fluctuation-dissipation from information geometry)
  CF11 (metriplectic damped Klein-Gordon)

There are no separate "RE-VGSP" and "GDSP" functions.
There is one RHS function. The J-limb and M-limb are terms within it.
"""

from __future__ import annotations
import numpy as np

# --- Universal constants (from CF chain) ---
TAU      = 2.0      # Telegraph relaxation time (CF04 §2.1)
BETA     = 0.1      # Debt decay / throttle coefficient (CF03 §7.2)
LAMBDA   = 1.0      # Double-well barrier height (CF03 §1.1)
GAMMA    = 0.05     # Diffusion coefficient D = γ (CF04 §6.1)
KT_EFF   = 0.001    # Effective temperature (CF06 §4.3)
DEBT_MAX = 10.0     # Debt clamp ceiling


def graph_laplacian(phi: np.ndarray, adj_lists: list[np.ndarray]) -> np.ndarray:
    """
    Discrete graph Laplacian: (Lφ)_i = Σ_{j ∈ adj(i)} (φ_j − φ_i)

    This is the spatial transport operator. Information propagates through
    edges at speed c = √(D/τ) hops per tick.

    Complexity: O(N·k) where k is mean degree.
    """
    N = phi.shape[0]
    out = np.zeros(N, dtype=np.float64)
    for i in range(N):
        nbrs = adj_lists[i]
        if nbrs.size == 0:
            continue
        out[i] = np.sum(phi[nbrs]) - nbrs.size * phi[i]
    return out.astype(np.float32)


def potential_derivative(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    """
    V(φ) = λ · φ²(1−φ)²  →  V'(φ) = 2λ · φ(1−φ)(1−2φ)

    Ginzburg-Landau double-well on [0,1]. Stable phases at φ=0 and φ=1.
    Unstable equilibrium at φ=0.5. Domain walls form at interfaces.
    Source: CF03 §1.1 (Modica-Mortola / phase-field energy functional).
    """
    return (2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)).astype(np.float32)


def klein_gordon_rhs(
    phi: np.ndarray,
    adj_lists: list[np.ndarray],
    lam: float = LAMBDA,
    D: float = GAMMA,
    kT: float = KT_EFF,
) -> np.ndarray:
    """
    Right-hand side of the metriplectic damped Klein-Gordon:

        rhs = D · Lφ − V'(φ) + η

    where η = √(2·D·kT) · ξ,  ξ ~ N(0,1)

    This contains both J-limb and M-limb contributions:
      J-limb: −V'(φ)  (reversible, from double-well potential)
      M-limb: D·Lφ + η  (irreversible, transport + fluctuation-dissipation)

    The inertial J-limb term (τ·∂²φ/∂t²) and friction M-limb term (∂φ/∂t)
    are handled by the telegraph timestepper in sparse_connectome.step(),
    not here. This function computes only the spatial + potential + noise RHS.

    Source: CF11 §2.3, CF04 §3.1, CF03 §1.1, CF06 §4.3.
    """
    transport = D * graph_laplacian(phi, adj_lists)
    dV = potential_derivative(phi, lam)
    noise = np.sqrt(2.0 * D * kT) * np.random.standard_normal(phi.shape).astype(np.float32)
    return transport - dV + noise


def get_constants() -> dict:
    """Return all physics constants for telemetry/checkpoint."""
    return {
        "TAU": TAU, "BETA": BETA, "LAMBDA": LAMBDA,
        "GAMMA": GAMMA, "KT_EFF": KT_EFF, "DEBT_MAX": DEBT_MAX,
    }
```

---

## 3. void_dynamics_adapter.py — Complete Replacement

```python
"""
Adapter layer for Void Equations. No fallbacks. No proxy code.
If Void_Equations.py cannot be imported, the runtime must crash.
"""
from vdm_rt.core.Void_Equations import (
    klein_gordon_rhs,
    graph_laplacian,
    potential_derivative,
    get_constants,
    TAU, BETA, LAMBDA, GAMMA, KT_EFF, DEBT_MAX,
)

__all__ = [
    "klein_gordon_rhs", "graph_laplacian", "potential_derivative",
    "get_constants",
    "TAU", "BETA", "LAMBDA", "GAMMA", "KT_EFF", "DEBT_MAX",
]
```

---

## 4. sparse_connectome.py — Modifications

### 4.1 `__init__` — New state variables

Add after `self.W = ...`:

```python
# --- Klein-Gordon field state ---
self.phi_curr = self.W.copy()
self.phi_prev = self.W.copy()
self.debt = np.zeros(self.N, dtype=np.float32)
self.last_activation_tick = np.zeros(self.N, dtype=np.int64)
self.eligibility = np.zeros(self.N, dtype=np.float32)

# Physics constants (imported, not hardcoded)
from .void_dynamics_adapter import TAU, BETA, LAMBDA, GAMMA, KT_EFF, DEBT_MAX
self.tau = TAU
self.beta = BETA
self.lam = LAMBDA
self.D = GAMMA
self.kT = KT_EFF
self.debt_max = DEBT_MAX

# Topology evolution constants
self.TOPO_PERIOD = 50
self.TOPO_THRESHOLD = 0.01
self.TOPO_PATIENCE = 100
```

Remove from `__init__`: any references to `telegraph_tau`, `gamma`, `kappa`, `W_prev`, `W_curr` from the round-2 patch.

The initial adjacency is constructed ONCE in `__init__` using the existing random sparse graph builder (the Erdős-Rényi or k-nearest construction already present). This is the initial lattice. It persists from tick 0 onward and is only modified by the local topology evolution in `_maybe_update_topology()`.

### 4.2 `step()` — New signature

OLD:
```python
def step(self, t: float, domain_modulation: float, sie_drive: float = 1.0, use_time_dynamics: bool = True):
```

NEW:
```python
def step(self, tick: int):
```

`tick` is the integer tick counter. No `domain_modulation`. No `sie_drive`. No `use_time_dynamics`.

### 4.3 `step()` — Complete tick sequence

**Delete the entire current body of step().** Replace with:

```python
def step(self, tick: int):
    """
    One tick of metriplectic Klein-Gordon on a persistent sparse graph.

    The adjacency self.adj persists from the previous tick. It is NOT rebuilt
    from scratch. Topology evolves locally and slowly via _maybe_update_topology().

    Tick sequence:
      1. Compute Klein-Gordon RHS: D·Lφ − V'(φ) + η       [O(N·k)]
      2. Implicit telegraph solve for φ_new (debt-throttled) [O(N)]
      3. Update debt, activation timestamps, eligibility     [O(N·k)]
      4. Maybe evolve topology (every TOPO_PERIOD ticks)     [O(N·k²) amortized O(N·k²/P)]
      5. Compute physics-derived reward observables           [O(N·k)]
      6. Traverse for telemetry                               [O(walkers·hops)]
    """
    from .void_dynamics_adapter import klein_gordon_rhs

    # --- Step 1: Klein-Gordon RHS ---
    rhs = klein_gordon_rhs(self.phi_curr, self.adj, lam=self.lam, D=self.D, kT=self.kT)

    # --- Step 2: Implicit telegraph solve ---
    tau_eff = self.tau * np.exp(self.beta * self.debt)  # per-node [O(N)]
    # With dt = 1:  a_inertia = tau_eff,  a_friction = 1.0
    numerator = (
        rhs
        + (2.0 * tau_eff + 1.0) * self.phi_curr
        - tau_eff * self.phi_prev
    )
    denominator = tau_eff + 1.0
    phi_new = np.clip(numerator / denominator, 0.0, 1.0).astype(np.float32)

    # Field displacement
    dphi = (phi_new - self.phi_curr).astype(np.float32)

    # Update field state
    self.phi_prev = self.phi_curr.copy()
    self.phi_curr = phi_new
    self.W = self.phi_curr  # backward compat alias

    # --- Step 3: Debt, activation, eligibility ---
    self.debt = np.clip(
        (1.0 - self.beta) * self.debt + np.abs(dphi),
        0.0, self.debt_max
    ).astype(np.float32)

    # Mark activations where |dφ| exceeds threshold
    activated = np.flatnonzero(np.abs(dphi) > 0.01)
    self.last_activation_tick[activated] = tick

    # Per-node eligibility from neighbor timing
    self.eligibility = self._compute_eligibility(tick)

    # External stimulation decay
    try:
        self._stim *= getattr(self, "_stim_decay", 0.90)
    except Exception:
        pass

    # --- Step 4: Local topology evolution (slow, periodic) ---
    self._maybe_update_topology(tick)

    # --- Step 5: Physics-derived reward ---
    self._compute_physics_reward(dphi)

    # --- Step 6: Traversal for telemetry ---
    a = np.abs(dphi).astype(np.float32)
    om = (-self.beta * self.phi_curr).astype(np.float32)
    try:
        self._void_traverse(a, om)
    except Exception:
        pass

    self._tick = tick
```

### 4.4 `_compute_eligibility()` — New method

```python
def _compute_eligibility(self, tick: int, tau_e: int = 250) -> np.ndarray:
    """
    Per-node eligibility from neighbor activation timing.
    Physics clock (tick counter), not wall clock.

    For each node i, eligibility = mean over neighbors j of:
      exp(−|Δt|/τ_e) · sign(Δt) · (φ_curr_i − φ_prev_i)

    where Δt = last_activation_tick[j] − last_activation_tick[i]

    Complexity: O(N·k)
    Source: DIRECTIVE v1 Fix 3, CF04 causal transport.
    """
    E = np.zeros(self.N, dtype=np.float32)
    for i, nbrs in enumerate(self.adj):
        if nbrs.size == 0:
            continue
        dt = self.last_activation_tick[nbrs] - self.last_activation_tick[i]
        causal = np.exp(-np.abs(dt) / float(tau_e)) * np.sign(dt)
        local_velocity = float(self.phi_curr[i] - self.phi_prev[i])
        E[i] = float(np.mean(causal)) * local_velocity
    return E
```

### 4.5 `_maybe_update_topology()` — New method (replaces global adjacency rebuild)

```python
def _maybe_update_topology(self, tick: int):
    """
    Local, eligibility-driven topology evolution.
    Runs every TOPO_PERIOD ticks, NOT every tick.

    The adjacency self.adj persists tick-to-tick. This method makes
    small local modifications based on accumulated eligibility traces.

    Physics justification:
    - CF04 §4.1: Causal cone requires stable lattice over propagation timescale.
      Propagation speed c = √(γ/τ) ≈ 0.158 hops/tick. A signal traverses ~8 hops
      in TOPO_PERIOD=50 ticks. Topology must be stable over this window.
    - CF03 §1.1: Domain walls form at persistent interfaces. Global rebuild every
      tick prevents interfaces from stabilizing.
    - The J/M timescale separation: field dynamics (J, fast) explore many states
      before topology (M, slow) commits to structural change.

    Edge nucleation: For each eligible node, scan 2-hop neighborhood for
    non-adjacent nodes with correlated eligibility. Propose edge with
    probability proportional to eligibility product.

    Edge dissolution: For each existing edge, if eligibility product is
    below threshold, dissolve with probability 1/TOPO_PATIENCE per check.
    Edges must be consistently low-eligibility across multiple checks to die.

    Complexity: O(N_eligible · k²) for nucleation + O(N · k) for dissolution.
    Amortized per tick: O(N · k² / TOPO_PERIOD).
    """
    if tick % self.TOPO_PERIOD != 0:
        return

    N = self.N
    elig = self.eligibility
    threshold = self.TOPO_THRESHOLD
    patience = self.TOPO_PATIENCE

    # Build adjacency set view for O(1) membership test
    adj_sets = [set(self.adj[i].tolist()) for i in range(N)]

    # --- Edge nucleation (local, 2-hop) ---
    for i in range(N):
        if abs(elig[i]) < threshold:
            continue
        # 2-hop neighborhood: reachable in 2 hops but not currently adjacent
        two_hop = set()
        for j in self.adj[i]:
            j = int(j)
            for k_node in self.adj[j]:
                k_node = int(k_node)
                if k_node != i and k_node not in adj_sets[i]:
                    two_hop.add(k_node)
        for k_node in two_hop:
            if abs(elig[k_node]) < threshold:
                continue
            # Probability proportional to eligibility product
            p = min(1.0, abs(elig[i] * elig[k_node]) * 100.0)
            if self.rng.random() < p:
                adj_sets[i].add(k_node)
                adj_sets[k_node].add(i)

    # --- Edge dissolution (local, per-edge) ---
    for i in range(N):
        if not adj_sets[i]:
            continue
        to_remove = []
        for j in adj_sets[i]:
            if j <= i:
                continue  # process each undirected edge once
            edge_elig = abs(elig[i]) * abs(elig[j])
            if edge_elig < threshold:
                # Probabilistic dissolution: 1/patience chance per check
                if self.rng.random() < (1.0 / patience):
                    to_remove.append(j)
        for j in to_remove:
            adj_sets[i].discard(j)
            adj_sets[j].discard(i)

    # --- Freeze adjacency ---
    self.adj = [
        np.array(sorted(adj_sets[i]), dtype=np.int32) if adj_sets[i]
        else np.zeros(0, dtype=np.int32)
        for i in range(N)
    ]

    # --- Connectivity maintenance ---
    # If the graph has fragmented into isolated components, do minimal
    # bridging (same as existing bridge_budget logic but only during
    # topology updates, not every tick).
    try:
        from .primitives.dsu import DSU as _DSU
        dsu = _DSU(N)
        for i in range(N):
            for j in self.adj[i]:
                dsu.union(i, int(j))
        # Count components among nodes that have ANY edges
        active_nodes = [i for i in range(N) if self.adj[i].size > 0]
        if active_nodes:
            roots = set(dsu.find(i) for i in active_nodes)
            n_components = len(roots)
        else:
            n_components = N

        if n_components > 1:
            B = min(int(getattr(self, "bridge_budget", 8)), n_components - 1)
            bridged = 0
            attempts = 0
            max_attempts = B * 64
            while bridged < B and attempts < max_attempts:
                attempts += 1
                u = self.rng.integers(0, N)
                v = self.rng.integers(0, N)
                if u == v or dsu.find(u) == dsu.find(v):
                    continue
                # Bridge: add symmetric edge
                self.adj[u] = np.append(self.adj[u], np.int32(v))
                self.adj[v] = np.append(self.adj[v], np.int32(u))
                self.adj[u] = np.sort(self.adj[u])
                self.adj[v] = np.sort(self.adj[v])
                dsu.union(u, v)
                bridged += 1
        self._frag_components_lb = n_components
    except Exception:
        pass
```

### 4.6 `_compute_physics_reward()` — New method (replaces SIE v2)

```python
def _compute_physics_reward(self, dphi: np.ndarray):
    """
    Physics-derived reward observables. Replaces heuristic SIE.

    All quantities computed from φ_prev, φ_curr, adj, and the
    energy/entropy functionals. No lookup tables. No weights.

    Complexity: O(N·k) for energy, O(N) for everything else.

    Source:
      Energy dissipation rate (−dH/dt): CF01 §4.2, CF02 §4.2
      Fisher speed: CF06 §4.3
      Entropy production rate: CF02 §4.2
    """
    # Energy: H[φ] = Σ_edges D(φ_i−φ_j)² + Σ_nodes V(φ_i)
    E_gradient = 0.0
    for i, nbrs in enumerate(self.adj):
        for j in nbrs:
            if int(j) > i:
                E_gradient += self.D * (self.phi_curr[i] - self.phi_curr[int(j)]) ** 2
    E_potential = float(np.sum(self.lam * self.phi_curr**2 * (1.0 - self.phi_curr)**2))
    H = E_gradient + E_potential

    # dH/dt ≈ H_curr − H_prev
    H_prev = getattr(self, '_last_H', H)
    dH_dt = H - H_prev
    self._last_H = H

    # Fisher speed: v_F = √(Σ (1/max(φ,ε)) · dφ²)
    eps = 1e-6
    fisher_speed = float(np.sqrt(np.sum(dphi**2 / np.maximum(self.phi_curr, eps))))

    # Entropy: S = −Σ [φ·log(φ) + (1−φ)·log(1−φ)]
    phi_c = np.clip(self.phi_curr, eps, 1.0 - eps)
    S = float(-np.sum(phi_c * np.log(phi_c) + (1.0 - phi_c) * np.log(1.0 - phi_c)))
    S_prev = getattr(self, '_last_S', S)
    dS_dt = S - S_prev
    self._last_S = S

    # Boundary flux (for speak gating)
    boundary_flux = float(np.sum(np.abs(dphi)))

    # Store for telemetry
    self._reward_H = float(H)
    self._reward_dH_dt = float(dH_dt)
    self._reward_fisher_speed = float(fisher_speed)
    self._reward_S = float(S)
    self._reward_dS_dt = float(dS_dt)
    self._reward_boundary_flux = float(boundary_flux)

    # Composite valence (physics-derived, backward compat for speak gating)
    raw = float(-dH_dt) + 0.1 * float(fisher_speed)
    self._last_sie2_valence = float(max(0.0, min(1.0, 0.5 + 0.5 * np.tanh(raw))))
    self._last_sie2_reward = float(raw)
```

### 4.7 `stimulate_indices()` — Modified

```python
def stimulate_indices(self, idxs, amp: float = 0.05):
    """Inject external stimulus. Updates phi_curr and activation timestamps."""
    try:
        if idxs is None:
            return
        arr = np.asarray(list(set(int(i) % self.N for i in idxs)), dtype=np.int64)
        if arr.size == 0:
            return
        self.phi_curr[arr] = np.clip(self.phi_curr[arr] + float(amp), 0.0, 1.0)
        self.W = self.phi_curr
        self.last_activation_tick[arr] = self._tick
    except Exception:
        pass
```

---

## 5. stepper.py — Modifications

### 5.1 Connectome step call

OLD:
```python
nx.connectome.step(t, domain_modulation=float(getattr(nx, "dom_mod", 1.0)),
                   sie_drive=sie_gate, use_time_dynamics=nx.use_time_dynamics)
```

NEW:
```python
nx.connectome.step(tick=step)
```

Remove all code that computes `sie_gate`, `sie_drive`, `dom_mod`, `domain_modulation`, `idf_scale`.

### 5.2 Metrics from physics reward

After the step call, read physics observables:
```python
m["H"] = float(getattr(nx.connectome, "_reward_H", 0.0))
m["dH_dt"] = float(getattr(nx.connectome, "_reward_dH_dt", 0.0))
m["fisher_speed"] = float(getattr(nx.connectome, "_reward_fisher_speed", 0.0))
m["S"] = float(getattr(nx.connectome, "_reward_S", 0.0))
m["dS_dt"] = float(getattr(nx.connectome, "_reward_dS_dt", 0.0))
m["boundary_flux"] = float(getattr(nx.connectome, "_reward_boundary_flux", 0.0))
m["sie_v2_valence_01"] = float(getattr(nx.connectome, "_last_sie2_valence", 0.0))
```

### 5.3 Time variable

OLD:
```python
t = time.time() - t0
```

NEW:
```python
t_wall = time.time() - t0  # wall clock for diagnostics only
```

The integer `step` passed to `connectome.step(tick=step)` IS the physics time.

---

## 6. main.py (loop) — Modifications

Remove `dom_mod` from all `getattr(nx, "dom_mod", ...)` paths. Remove `use_time_dynamics` from all paths. The loop increments `step` and calls the stepper with `step` as the tick counter.

---

## 7. nexus.py — Modifications

Remove from `__init__`:
- `self.dom_mod`
- `self.use_time_dynamics`
- `self.domain` (as a modulation parameter; may be retained as a descriptive label)

Remove from constructor parameters:
- `domain_modulation`, `use_time_dynamics`, `dom_mod`

Remove the call to `get_domain_modulation()` and any import of `Void_Debt_Modulation`.

---

## 8. UTED — Physics-Clock Timestamps

In `vdm_rt/io/uted/ute_mux.py`, all adapters:

```python
from vdm_rt.core.void_dynamics_adapter import TAU, GAMMA
import numpy as np

DT_PHYSICS_US = int(np.sqrt(TAU / GAMMA) * 1_000_000)  # ≈ 6_324_555 μs

# In every adapter's poll_frames():
timestamp_us = tick * DT_PHYSICS_US
# NOT time.time_ns() // 1000
```

`HeartbeatAdapter` emits one frame per tick. No wall-clock rate limiting.

Wall-clock time may be stored in a separate `wall_us` field for debugging but must NOT be in `timestamp_us`.

---

## 9. sie_v2.py — Deprecation

`sie_v2.py` continues to exist but `sie_step()` is no longer called from the hot path. The physics-derived reward in `sparse_connectome._compute_physics_reward()` replaces it. `sie_v2.py` may be retained for comparison but must not be imported by `sparse_connectome.py` or `stepper.py`.

---

## 10. Eliminated Proxies Checklist

After migration, `grep -rn` for each of these in `vdm_rt/` must return ZERO hits (comments explaining retirement are allowed, production code is not):

- [ ] `F_REF`
- [ ] `PHASE_SENS`
- [ ] `ALPHA` as `= 0.25` in a non-comment line
- [ ] `sin(2 * np.pi * f_ref`
- [ ] `domain_modulation` as a parameter name
- [ ] `get_domain_modulation`
- [ ] `Void_Debt_Modulation`
- [ ] `use_time_dynamics` as a parameter name
- [ ] `time.time_ns()` in any file under `vdm_rt/core/` or `vdm_rt/io/uted/`
- [ ] `np.random.uniform(-0.02, 0.02`
- [ ] `alpha * W * (1 - W)` or `alpha * W * (1.0 - W)` (logistic reaction)
- [ ] `-beta * W` as a standalone decay term
- [ ] `delta_re_vgsp` as a function definition
- [ ] `delta_gdsp` as a function definition
- [ ] `universal_void_dynamics` as a function definition
- [ ] `neigh_sets: List[Set[int]] = [set() for _ in range(N)]` in `step()` (global rebuild)
- [ ] `self._build_alias` called from within `step()` (alias sampling in hot path)

---

## 11. Validation Gates (run 50,000 ticks, N=256, k=12)

All must pass or the migration is rejected:

1. **No NaN:** `np.any(np.isnan(phi_curr))` is never True.
2. **Field bounded:** `phi_curr ∈ [0.0, 1.0]` every tick.
3. **Bimodal distribution:** At tick 50000, histogram of `phi_curr` has two peaks: `count(φ < 0.2) > 0.2·N` AND `count(φ > 0.8) > 0.2·N`.
4. **Causal propagation:** Inject stimulus at node i at tick T. Measure first activation tick at node j (graph distance d). Delay ≥ `d / c` where `c = √(γ/τ)`. Test 10 random pairs with d ∈ [3, 10].
5. **Energy non-increase:** Compute H every 100 ticks. Over any 1000-tick window, H must not increase by more than 5% of its starting value.
6. **Gini coefficient:** At tick 50000, Gini of `phi_curr` ≥ 0.45.
7. **Topology persistence:** Mean edge lifetime (ticks an edge persists before dissolution) > 500 ticks.
8. **Topology locality:** No edge is ever created between nodes more than 2 hops apart in the current graph.
9. **Eliminated proxies:** grep check (Section 10) passes with zero hits.
10. **Eligibility non-zero:** At tick 50000, `count(|eligibility| > 1e-4) > 0.1·N`.
11. **Per-tick cost:** Mean wall-clock time per tick ≤ 2x the time for a single `klein_gordon_rhs()` call (topology update amortization is working).

---

## 12. Implementation Order

1. **Void_Equations.py** — rewrite (Section 2)
2. **void_dynamics_adapter.py** — rewrite (Section 3)
3. **sparse_connectome.py** — modify `__init__`, replace `step()`, add new methods (Section 4)
4. **stepper.py** — modify (Section 5)
5. **main.py** — modify (Section 6)
6. **nexus.py** — modify (Section 7)
7. **UTED** — create/modify (Section 8)
8. **Validation** — run all gates (Section 11)

Each step must pass `python -m pytest` before proceeding. If existing tests reference eliminated parameters (`domain_modulation`, `use_time_dynamics`, `sie_drive`, etc.), update the tests to match the new signatures FIRST.
