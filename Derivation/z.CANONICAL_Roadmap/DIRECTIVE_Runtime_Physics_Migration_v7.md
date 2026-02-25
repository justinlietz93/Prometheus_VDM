# Runtime Physics Migration Directive v6

**Author:** Justin K. Lietz
**Date:** 2026-02-21
**Status:** DRAFT — supersedes v3
**Scope:** Complete migration from proxy heuristics to physics-derived runtime.

**Rule:** No lookup tables. No artificial toggles. No wall-clock timestamps in the physics path. No hardcoded timescales, thresholds, patience counters, or spatial cutoffs. Every parameter is either a material constant of the lattice (τ, λ, D, kT, β, ε_topo) or emerges from the dynamics of those constants. Every instruction in this document is literal. If it says "delete," delete it. If it says "replace," replace every instance. If a function signature is specified, that is the exact signature. Codex must not invent parameters, add toggles, or introduce fallback paths.

**What changed from v3 and why:** v3 hardcoded seven non-emergent quantities: `TOPO_PERIOD=50` (cron timer), `TOPO_THRESHOLD=0.01` (eligibility gate), `TOPO_PATIENCE=100` (debounce counter), `tau_e=250` (eligibility decay), `R_NUCLEATION=4.0` (spatial cutoff), `debt_max=10.0` (ceiling clamp), `dt_physics_us=6324555` (pre-computed conversion). All seven violate the CF chain. CF01 §4.1 says `dF/dt = {F,H}_J + (F,S)_M` — both terms, every tick, for every degree of freedom. CF02 §4.1-4.3 says timescale separation comes from operator structure (coupling constants), not from scheduling. CF04 §4.2 says the causal cone grows from the dynamics. v4 replaces all seven with one new material constant `ε_topo = 0.01` and a bond field `ψ_ij` that evolves under the same Klein-Gordon equation with heavier mass `τ_bond = τ/ε_topo`. Topology becomes a degree of freedom, not a cron job.

---

## 0. Notation, Constants, and Scaling

### 0.1 The Equation of Motion

The runtime executes one equation per tick per degree of freedom. There are two coupled degrees of freedom:

1. **φ_i (node field)** — scalar order parameter at node i, range [0, 1].
2. **ψ_ij (bond field)** — edge order parameter for each edge (i,j), range [0, 1].

Both evolve under the same metriplectic Klein-Gordon dynamics with different coupling constants. This is CF01 §4.1: `dF/dt = {F,H}_J + (F,S)_M` applied to all degrees of freedom simultaneously, every tick.

#### Node field equation (CF11 §2.3 + CF04 §3.1 + CF03 §1.1):

```
τ_eff(i) · (φ_{n+1,i} − 2φ_{n,i} + φ_{n-1,i}) / dt²
+ (φ_{n+1,i} − φ_{n,i}) / dt
= D · (L_ψ φ)_{n,i} − V'(φ_{n,i}) + η_{n,i}
```

Where:
- `φ_{n,i}` is the scalar field at node `i`, tick `n`. Range [0, 1].
- `τ_eff(i) = τ · exp(β · debt_i)` — debt-throttled relaxation time (per-node).
- `dt = 1.0` — one tick = one physics timestep (dimensionless).
- `D` — diffusion coefficient (= γ, since lattice spacing a = 1).
- `(L_ψ φ)_i = Σ_{j ∈ adj(i)} ψ_ij · (φ_j − φ_i)` — bond-weighted graph Laplacian. This is the finite-difference discretization of `∇²φ` on the spatial lattice defined in §0.5, weighted by bond strength. A fully formed bond (ψ=1) contributes full coupling. A dissolving bond (ψ→0) contributes decreasing coupling. This replaces the binary adjacency of v3.
- `V(φ) = λ · φ²(1 − φ)²` — Ginzburg-Landau double-well on [0, 1].
- `V'(φ) = 2λ · φ(1 − φ)(1 − 2φ)` — potential derivative.
- `η_i = √(2 · D · kT) · ξ_i` — fluctuation-dissipation noise, ξ ~ N(0,1).

Rearranging for φ_{n+1} (implicit solve, dt = 1):

```
a_inertia(i) = τ_eff(i)
a_friction   = 1.0
rhs(i)       = D · (L_ψ φ)_i − V'(φ_i) + η_i

φ_new(i) = [ rhs(i) + (2·a_inertia(i) + a_friction)·φ_curr(i) − a_inertia(i)·φ_prev(i) ]
            / [ a_inertia(i) + a_friction ]

φ_new(i) = clip(φ_new(i), 0.0, 1.0)
```

#### Bond field equation (CF03 §1.1 + CF02 §4.1 + CF04 §3.1):

Each edge (i,j) carries a bond field ψ_ij ∈ [0,1] that evolves under:

```
τ_bond · (ψ_{n+1,ij} − 2ψ_{n,ij} + ψ_{n-1,ij}) / dt²
+ (ψ_{n+1,ij} − ψ_{n,ij}) / dt
= −∂U_bond/∂ψ_ij + η_bond_ij
```

Where:
- `τ_bond = τ / ε_topo` — bond relaxation time. Since `ε_topo ≪ 1`, bonds are much slower than the field. This is how timescale separation emerges. CF02 §4.1: the M-limb coupling constant ε determines the dissipative timescale. Small ε → slow structural change. This is a physical mass, not a timer.
- `ε_topo = 0.01` — structural coupling constant. Material property of the lattice. The ratio `τ_bond / τ = 1/ε_topo = 100` means bonds are 100× slower than field oscillations. This is the ONLY source of timescale separation.
- `U_bond(ψ, φ̇_i, φ̇_j) = λ · ψ²(1−ψ)² − ε_topo · ψ · |φ̇_i| · |φ̇_j|`
  - First term: double-well in ψ. Bonds prefer ψ=0 (absent) or ψ=1 (present). Source: CF03 §1.1.
  - Second term: activity-driven nucleation. The product `|φ̇_i| · |φ̇_j|` means bonds form between co-active nodes. Source: CF06 §4.1 (gradient flow on Fisher metric).
- `η_bond = √(2 · ε_topo · kT) · ξ_ij` — thermal fluctuations for bonds. Source: CF06 §4.3.

Bond potential derivative:

```
∂U_bond/∂ψ = 2λ · ψ(1−ψ)(1−2ψ) − ε_topo · |φ̇_i| · |φ̇_j|
```

The implicit solve for ψ_{n+1} has the same structure as for φ_{n+1}:

```
a_bond_inertia = τ_bond        # = τ / ε_topo
a_bond_friction = 1.0
rhs_bond(i,j) = −∂U_bond/∂ψ_ij + η_bond_ij

ψ_new(i,j) = [ rhs_bond + (2·a_bond_inertia + a_bond_friction)·ψ_curr − a_bond_inertia·ψ_prev ]
              / [ a_bond_inertia + a_bond_friction ]

ψ_new(i,j) = clip(ψ_new(i,j), 0.0, 1.0)
```

> **Bond Decoherence and Nucleation (CF07):**
> Structures physically cease to exist in the observable M-limb when they become indistinguishable from background thermal noise. Therefore, when a bond's strength falls below the emergent thermal noise floor (**$\psi_{ij} < \sqrt{2 \cdot \varepsilon_{topo} \cdot kT}$**), the edge is lost to decoherence and removed from the adjacency list. When a candidate edge is proposed, it must be nucleated strictly at **$\psi_{ij} = 0.0$**. The continuous metriplectic integration and thermodynamic forces will naturally lift the bond out of the vacuum if favored, requiring no artificial numerical seeding.

#### Candidate edge proposal (replaces TOPO_PERIOD + 2-hop scan)

New edges can only be proposed between nodes within each other's causal cone:

```
r_causal(i) accumulates: r_causal[i] += c_eff(i) · dt  each tick while |φ̇_i| > kT
```

where `c_eff(i) = √(D / τ_eff(i))` is the local propagation speed. Candidate edges require `||pos[i] − pos[j]||₂ ≤ r_causal[i]` AND `|φ̇_i| · |φ̇_j| > kT` AND (i,j) not already in adjacency.

### 0.2 Constants — Material Properties Only

| Name | Value | Role | Source | Type |
|------|-------|------|--------|------|
| `τ` | `2.0` | Base telegraph relaxation time | CF04 §2.1 | Material |
| `β` | `0.1` | Debt throttle exponent | CF03 §7.2 | Material |
| `λ` | `1.0` | Double-well barrier height | CF03 §1.1 | Material |
| `D` (= γ) | `0.05` | Diffusion coefficient | CF04 §6.1 | Material |
| `kT` | `0.001` | Effective temperature | CF06 §4.3 | Material |
| `ε_topo` | `0.01` | Structural coupling constant | CF02 §4.1 | Material |


### 0.3 Eliminated Constants (must not appear anywhere after migration)

`F_REF`, `PHASE_SENS`, `ALPHA` (as reaction rate), `BETA` (as separate decay rate in GDSP), `domain_modulation`, `use_time_dynamics`, `kappa` (as separate from D), `TOPO_PERIOD`, `TOPO_THRESHOLD`, `TOPO_PATIENCE`, `R_NUCLEATION`, `tau_e`, `debt_max`, `dt_physics_us`, `DEBT_MAX`, `PSI_DEATH`, `PSI_SEED`.

### 0.4 Compute, Memory, and Scaling

#### DEVICE NEUTRALITY CONSTRAINT

The fast path MUST NOT assume a single address space, a single execution device, or synchronous execution order between independent operations.

Specifically:

1. The bond-weighted Laplacian, the pointwise node solve, the bond solve, and the debt update are independent operations on the same tick's data. They MUST NOT be fused into a single function that requires all to execute on the same device.

2. All state arrays (phi_curr, phi_prev, debt, adj, psi_curr, psi_prev, pos, r_causal) MUST be stored in standard contiguous array formats (numpy ndarray, or equivalent) that can be copied to any device buffer without reshaping or reinterpretation.

3. The step() function MUST NOT call time.time(), time.time_ns(), threading primitives, or device-specific APIs. It operates on arrays and returns arrays. Device dispatch is the caller's responsibility.

#### Why this architecture scales

The current runtime rebuilds the **entire adjacency** from scratch every tick: allocate N empty sets, draw O(s) alias samples per node, score every candidate pair, symmetrize, prune, bridge, freeze into sorted arrays. Cost: **O(N · s) per tick** where s is the candidate count (default 64). For N = 256 this is fine. For N = 1,000,000 it is 64 million operations per tick just for topology, before the field update even runs.

This is also physically wrong. The universe does not globally recompute which particles are adjacent every Planck time. Topology (which nodes are coupled) is persistent state that evolves slowly and locally, driven by the field dynamics.

The physics-derived architecture has ONE cost regime — everything runs every tick with different coupling strengths:

**Every tick: field + bond update — O(N · k)**

| Operation | Cost | Why |
|-----------|------|-----|
| Bond-weighted Laplacian `Σ_j ψ_ij(φ_j − φ_i)` | O(N · k) | One pass over adjacency; k = mean degree |
| Potential derivative `V'(φ)` | O(N) | Pointwise polynomial per node |
| Noise generation (nodes) | O(N) | One RNG call |
| Telegraph solve (nodes) | O(N) | Pointwise division per node |
| Bond potential derivative `∂U_bond/∂ψ` | O(N · k) | One pass over edges |
| Bond telegraph solve | O(N · k) | Pointwise per edge |
| Bond noise generation | O(N · k) | One RNG call |
| Activity `|φ̇|` computation | O(N) | Pointwise |
| Causal radius update | O(N) | One add per node |
| Debt update | O(N) | Pointwise |
| Edge birth/death bookkeeping | O(N_events) | Sparse: only edges crossing the emergent noise floor or new candidates |

**Total: O(N · k) per tick.** For k = 6 and N = 1,000,000 this is ~12M operations per tick (Laplacian + bond update are each O(N·k)). For k = 6 and N = 100,000,000 this is ~1.2B — still tractable with vectorized numpy.

**Candidate edge proposal: O(N_active · s²)** where s = floor(r_causal). Evaluated every tick but only for active nodes (|φ̇| > kT), and s grows as O(√t · c_eff). For early ticks s ≈ 1 and cost is negligible. Bounded by causal cone finiteness.

**Comparison to current architecture:**

| Architecture | Per-tick cost | Topology persistence | Causal structure |
|---|---|---|---|
| Current (global rebuild) | O(N · 64) | None — rebuilt from scratch | Violated |
| Physics-derived (bond field) | O(N · k) ≈ O(N · 6) | Persistent — bonds carry forward | Preserved — causal cone |

**The physics-derived architecture is ~10x cheaper per tick AND physically correct.**

#### Memory cost

| Array | Size | Dtype | Bytes (N=1M, k=6) |
|-------|------|-------|-------------------|
| `phi_curr` | N | float32 | 4 MB |
| `phi_prev` | N | float32 | 4 MB |
| `debt` | N | float64 | 8 MB |
| `r_causal` | N | float32 | 4 MB |
| `pos` | N × 3 | float32 | 12 MB |
| `psi_curr` | N · k | float32 | 24 MB |
| `psi_prev` | N · k | float32 | 24 MB |
| `adj` | N · k | int32 | 24 MB |
| `W` (alias to phi_curr) | 0 | — | 0 |

**Total: ~104 MB for N = 1,000,000 with k = 6.**

#### Scaling law

```
T_tick = a · N · k
```

Linear in N for fixed k. k does not grow with N (cubic lattice: k = 6 regardless of N).

### 0.5 Topology and Manifold Structure

The discrete manifold is the connectome graph itself. Nodes have no fixed spatial embedding. There is no coordinate grid. The adjacency structure IS the geometry.

**Initial connectivity:** k-regular random graph or preferential attachment, matching the existing runtime initialization parameter `k`. The initial degree distribution and graph structure are initial conditions, analogous to the initial field configuration φ(t=0).

**Edge proposal constraint:** Candidate edges require graph distance (hop count) between nodes i and j ≤ `h_causal(i)`, where `h_causal` accumulates from local dynamics:

```
h_causal[i] += 1  each tick while |φ̇_i| > kT
```

This replaces the Euclidean `r_causal`. Co-activity condition `|φ̇_i|·|φ̇_j| > kT` is unchanged.

**N is unconstrained.** Any positive integer. No cube requirement.

**No pos array.** Node positions are not defined, not stored, not used in physics. If a spatial embedding is needed for visualization, it is computed from the graph spectrum (Fiedler layout) at render time, not stored as state.

---

## 1. File Operations

### 1.1 Files to DELETE entirely

| File | Reason |
|------|--------|
| `vdm_rt/core/Void_Debt_Modulation.py` (if exists) | Lookup table proxy |

### 1.2 Files to REWRITE (replace entire contents)

| File | New purpose |
|------|-------------|
| `vdm_rt/core/Void_Equations.py` | Bond-weighted Klein-Gordon RHS + bond potential |
| `vdm_rt/core/void_dynamics_adapter.py` | Thin import; no fallback |

### 1.3 Files to MODIFY (specific sections)

| File | What changes |
|------|-------------|
| `vdm_rt/core/sparse_connectome.py` | `__init__`, `step`, `stimulate_indices`, bond field methods |
| `vdm_rt/core/sie_v2.py` | Deprecated; no longer called from hot path |
| `vdm_rt/core/engine/core_engine.py` | `step_connectome` signature: remove `domain_modulation`, `use_time_dynamics`, `sie_gate`; pass `tick` only |
| `vdm_rt/runtime/stepper.py` | Remove `domain_modulation`, `use_time_dynamics`, `sie_drive`, `idf_scale`; pass `tick=step` |
| `vdm_rt/runtime/loop/main.py` | Remove `dom_mod` usage; use integer tick for `t` |
| `vdm_rt/nexus.py` | Remove `dom_mod`, `use_time_dynamics`, `get_domain_modulation` import |
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

Two coupled equations of motion derived from:
  CF01 (QGT → metriplectic brackets)
  CF02 (GENERIC two-generator structure — J and M simultaneous)
  CF03 (double-well potential, Ginzburg-Landau, for both φ and ψ)
  CF04 (telegraph-Fisher finite-speed transport, causal cone)
  CF06 (fluctuation-dissipation from information geometry)
  CF11 (metriplectic damped Klein-Gordon)

There are no separate "RE-VGSP" and "GDSP" functions.
There are no topology timers, thresholds, or patience counters.
There are two coupled Klein-Gordon fields (node + bond) with different masses.
"""

from __future__ import annotations
import numpy as np

# --- Material constants (from CF chain) ---
TAU       = 2.0      # Telegraph relaxation time (CF04 §2.1)
BETA      = 0.1      # Debt throttle exponent (CF03 §7.2)
LAMBDA    = 1.0      # Double-well barrier height (CF03 §1.1)
GAMMA     = 0.05     # Diffusion coefficient D = γ (CF04 §6.1)
KT_EFF    = 0.001    # Effective temperature (CF06 §4.3)
EPS_TOPO  = 0.01     # Structural coupling constant (CF02 §4.1)

# Emergent bond noise floor (CF07)
ETA_BOND_FLOOR = float(np.sqrt(2.0 * EPS_TOPO * KT_EFF))  # sqrt(2·ε_topo·kT)


def bond_weighted_laplacian(
    phi: np.ndarray,
    adj_lists: list[np.ndarray],
    psi: list[np.ndarray],
) -> np.ndarray:
    """
    Bond-weighted discrete Laplacian: (L_ψ φ)_i = Σ_{j ∈ adj(i)} ψ_ij · (φ_j − φ_i)

    On the cubic spatial lattice (§0.5), this is the standard finite-difference
    stencil weighted by bond strength.

    Source: CF11 §2.3, CF03 §1.1.
    Complexity: O(N·k).
    """
    N = phi.shape[0]
    out = np.zeros(N, dtype=np.float64)
    for i in range(N):
        nbrs = adj_lists[i]
        if nbrs.size == 0:
            continue
        out[i] = np.sum(psi[i] * (phi[nbrs] - phi[i]))
    return out.astype(np.float32)


def node_potential_derivative(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    """
    V(φ) = λ · φ²(1−φ)²  →  V'(φ) = 2λ · φ(1−φ)(1−2φ)
    Source: CF03 §1.1.
    """
    return (2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)).astype(np.float32)


def bond_potential_derivative(
    psi_ij: np.ndarray,
    phi_dot_i: float,
    phi_dot_j: np.ndarray,
    lam: float = LAMBDA,
    eps: float = EPS_TOPO,
) -> np.ndarray:
    """
    U_bond(ψ) = λ · ψ²(1−ψ)² − ε · ψ · |φ̇_i| · |φ̇_j|

    ∂U/∂ψ = 2λ · ψ(1−ψ)(1−2ψ) − ε · |φ̇_i| · |φ̇_j|

    Source: CF03 §1.1, CF06 §4.1.
    """
    dwell = 2.0 * lam * psi_ij * (1.0 - psi_ij) * (1.0 - 2.0 * psi_ij)
    activity = eps * np.abs(phi_dot_i) * np.abs(phi_dot_j)
    return (dwell - activity).astype(np.float32)


def klein_gordon_rhs(
    phi: np.ndarray,
    adj_lists: list[np.ndarray],
    psi: list[np.ndarray],
    lam: float = LAMBDA,
    D: float = GAMMA,
    kT: float = KT_EFF,
) -> np.ndarray:
    """
    Node field RHS: rhs = D · L_ψ(φ) − V'(φ) + η

    Source: CF11 §2.3, CF04 §3.1, CF03 §1.1, CF06 §4.3.
    """
    transport = D * bond_weighted_laplacian(phi, adj_lists, psi)
    dV = node_potential_derivative(phi, lam)
    noise = np.sqrt(2.0 * D * kT) * np.random.standard_normal(phi.shape).astype(np.float32)
    return transport - dV + noise


def get_constants() -> dict:
    """Return all material constants for telemetry/checkpoint."""
    return {
        "TAU": TAU, "BETA": BETA, "LAMBDA": LAMBDA,
        "GAMMA": GAMMA, "KT_EFF": KT_EFF, "EPS_TOPO": EPS_TOPO,
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
    bond_weighted_laplacian,
    node_potential_derivative,
    bond_potential_derivative,
    get_constants,
    TAU, BETA, LAMBDA, GAMMA, KT_EFF, EPS_TOPO,
    ETA_BOND_FLOOR,
)

__all__ = [
    "klein_gordon_rhs",
    "bond_weighted_laplacian",
    "node_potential_derivative",
    "bond_potential_derivative",
    "get_constants",
    "TAU", "BETA", "LAMBDA", "GAMMA", "KT_EFF", "EPS_TOPO",
    "ETA_BOND_FLOOR",
]
```

---

## 4. sparse_connectome.py — Modifications

### 4.1 `__init__` — Complete new state

Remove from `__init__`: all references to `telegraph_tau`, `gamma`, `kappa`, `W_prev`, `W_curr`, `last_activation_tick`, `eligibility`, `TOPO_PERIOD`, `TOPO_THRESHOLD`, `TOPO_PATIENCE`.

Add after `self.W = ...`:

```python
# --- Material constants (from CF chain, not tuning knobs) ---
from .void_dynamics_adapter import TAU, BETA, LAMBDA, GAMMA, KT_EFF, EPS_TOPO, ETA_BOND_FLOOR
self.tau = TAU
self.beta = BETA
self.lam = LAMBDA
self.D = GAMMA
self.kT = KT_EFF
self.eps_topo = EPS_TOPO

# --- Node field state ---
self.phi_curr = self.W.copy()
self.phi_prev = self.W.copy()

# --- Debt (no ceiling — self-limits via exp(β·debt) asymptotic freeze) ---
self.debt = np.zeros(self.N, dtype=np.float64)

# --- Spatial positions (immutable, cubic lattice) ---
side = round(self.N ** (1/3))
assert side ** 3 == self.N, f"N={self.N} is not a perfect cube"
self._side = side
self.pos = np.zeros((self.N, 3), dtype=np.float32)
for i in range(self.N):
    iz = i // (side * side)
    iy = (i // side) % side
    ix = i % side
    self.pos[i] = (ix, iy, iz)

# --- Causal radius (per-node, accumulated while active) ---
self.r_causal = np.zeros(self.N, dtype=np.float32)

# --- Initial adjacency: 6 face-adjacent neighbors on cubic lattice ---
self._build_cubic_adjacency()

# --- Bond field state (parallel to adj, initial bonds fully formed) ---
self.psi_curr: list[np.ndarray] = [
    np.ones(self.adj[i].shape[0], dtype=np.float32)
    for i in range(self.N)
]
self.psi_prev: list[np.ndarray] = [
    psi.copy() for psi in self.psi_curr
]

# Tick counter
self._tick = 0
```

### 4.2 `_build_cubic_adjacency()` — New method

```python
def _build_cubic_adjacency(self):
    """Build 6-connected face-adjacent cubic lattice. No periodic boundary."""
    side = self._side
    self.adj = [np.zeros(0, dtype=np.int32) for _ in range(self.N)]
    for i in range(self.N):
        iz = i // (side * side)
        iy = (i // side) % side
        ix = i % side
        nbrs = []
        if ix > 0:        nbrs.append(i - 1)
        if ix < side - 1: nbrs.append(i + 1)
        if iy > 0:        nbrs.append(i - side)
        if iy < side - 1: nbrs.append(i + side)
        if iz > 0:        nbrs.append(i - side * side)
        if iz < side - 1: nbrs.append(i + side * side)
        self.adj[i] = np.array(sorted(nbrs), dtype=np.int32)
```

### 4.3 `step()` — New signature

OLD:
```python
def step(self, t: float, domain_modulation: float, sie_drive: float = 1.0, use_time_dynamics: bool = True):
```

NEW:
```python
def step(self, tick: int):
```

### 4.4 `step()` — Complete tick sequence

**Delete the entire current body of step().** Replace with:

```python
def step(self, tick: int):
    """
    One tick of coupled metriplectic Klein-Gordon (node field + bond field).
    Both fields evolve every tick. There is no topology update period.

    Source: CF01 §4.1 (dF/dt = {F,H}_J + (F,S)_M — both terms, every tick).
    """
    self._tick = tick
    N = self.N
    from .void_dynamics_adapter import klein_gordon_rhs, bond_potential_derivative

    # --- Per-node derived quantities ---
    tau_eff = self.tau * np.exp(self.beta * self.debt)  # no clamp
    phi_dot = self.phi_curr - self.phi_prev              # field velocity

    # --- Step 1: Node field Klein-Gordon RHS ---
    rhs = klein_gordon_rhs(
        self.phi_curr, self.adj, self.psi_curr,
        lam=self.lam, D=self.D, kT=self.kT,
    )

    # --- Step 2: Node field telegraph solve ---
    a_inertia = tau_eff.astype(np.float32)
    a_friction = np.float32(1.0)
    numerator = rhs + (2.0 * a_inertia + a_friction) * self.phi_curr - a_inertia * self.phi_prev
    denominator = a_inertia + a_friction
    phi_new = np.clip(numerator / denominator, 0.0, 1.0).astype(np.float32)

    # --- Step 3: Bond field update (every tick, heavier mass τ/ε_topo) ---
    tau_bond = np.float32(self.tau / self.eps_topo)
    phi_dot_abs = np.abs(phi_dot).astype(np.float32)

    for i in range(N):
        nbrs = self.adj[i]
        if nbrs.size == 0:
            continue
        psi_c = self.psi_curr[i]
        psi_p = self.psi_prev[i]

        dU = bond_potential_derivative(
            psi_c, phi_dot_abs[i], phi_dot_abs[nbrs],
            lam=self.lam, eps=self.eps_topo,
        )
        eta_bond = np.sqrt(2.0 * self.eps_topo * self.kT) * \
                   self.rng.standard_normal(nbrs.size).astype(np.float32)
        rhs_bond = -dU + eta_bond

        psi_new = (
            rhs_bond + (2.0 * tau_bond + 1.0) * psi_c - tau_bond * psi_p
        ) / (tau_bond + 1.0)
        self.psi_prev[i] = psi_c.copy()
        self.psi_curr[i] = np.clip(psi_new, 0.0, 1.0).astype(np.float32)

    # --- Step 4: Edge death (ψ < η_bond floor) ---
    self._remove_dead_edges()

    # --- Step 5: Edge birth (causal cone + co-activity) ---
    self._propose_new_edges(phi_dot_abs)

    # --- Step 6: Update node field history ---
    dphi = (phi_new - self.phi_curr).astype(np.float32)
    self.phi_prev = self.phi_curr.copy()
    self.phi_curr = phi_new
    self.W = self.phi_curr  # backward compat alias

    # --- Step 7: Debt (no ceiling — self-limits via exp) ---
    self.debt = (1.0 - self.beta) * self.debt + np.abs(dphi).astype(np.float64)

    # --- Step 8: Causal radius (only for active nodes) ---
    c_eff = np.sqrt(self.D / tau_eff).astype(np.float32)
    active = phi_dot_abs > self.kT
    self.r_causal[active] += c_eff[active]

    # --- Step 9: External stimulation decay ---
    try:
        self._stim *= getattr(self, "_stim_decay", 0.90)
    except Exception:
        pass

    # --- Step 10: Physics-derived reward ---
    self._compute_physics_reward(dphi)

    # --- Step 11: Traversal for telemetry ---
    a = np.abs(dphi).astype(np.float32)
    om = (-self.beta * self.phi_curr).astype(np.float32)
    try:
        self._void_traverse(a, om)
    except Exception:
        pass
```

### 4.5 `_remove_dead_edges()` — New method

```python
def _remove_dead_edges(self):
    """Remove edges whose bond field ψ has fallen below the emergent bond noise floor."""
    from .void_dynamics_adapter import ETA_BOND_FLOOR
    for i in range(self.N):
        if self.adj[i].size == 0:
            continue
        alive = self.psi_curr[i] >= ETA_BOND_FLOOR
        if not np.all(alive):
            dead_nbrs = self.adj[i][~alive]
            self.adj[i] = self.adj[i][alive]
            self.psi_curr[i] = self.psi_curr[i][alive]
            self.psi_prev[i] = self.psi_prev[i][alive]
            for j in dead_nbrs:
                j = int(j)
                mask = self.adj[j] != i
                self.adj[j] = self.adj[j][mask]
                self.psi_curr[j] = self.psi_curr[j][mask]
                self.psi_prev[j] = self.psi_prev[j][mask]
```

### 4.6 `_propose_new_edges()` — New method

```python
def _propose_new_edges(self, phi_dot_abs: np.ndarray):
    """
    Propose new edges based on causal cone and co-activity.
    Source: CF04 §4.2 (causal cone), CF06 §4.1 (co-activity).

    SCALING RULE: This method MUST NOT scan all nodes (no `for j in range(self.N)`).
    Candidates must be enumerated locally from the cubic lattice coordinates inside the
    causal radius r_causal(i).
    """
    kT = self.kT
    side = self._side
    side2 = side * side

    for i in range(self.N):
        if phi_dot_abs[i] <= kT:
            continue

        r = float(self.r_causal[i])
        if r < 1.5:
            continue

        R = int(min(r, side // 2))
        if R < 2:
            continue

        existing = set(self.adj[i].tolist())
        ix, iy, iz = map(int, self.pos[i])

        # Enumerate lattice sites in the local cube [-R, R]^3, then filter by Euclidean radius.
        for dz in range(-R, R + 1):
            z = iz + dz
            if z < 0 or z >= side:
                continue
            for dy in range(-R, R + 1):
                y = iy + dy
                if y < 0 or y >= side:
                    continue
                for dx in range(-R, R + 1):
                    x = ix + dx
                    if x < 0 or x >= side:
                        continue

                    # skip self
                    if dx == 0 and dy == 0 and dz == 0:
                        continue

                    # Euclidean filter (causal cone)
                    dist = float(np.sqrt(dx * dx + dy * dy + dz * dz))
                    if dist > r or dist < 1.5:
                        continue

                    j = x + y * side + z * side2
                    if j in existing:
                        continue
                    if phi_dot_abs[j] <= kT:
                        continue

                    # Nucleate strictly at psi = 0.0 (no PSI_SEED)
                    self.adj[i] = np.append(self.adj[i], np.int32(j))
                    self.psi_curr[i] = np.append(self.psi_curr[i], np.float32(0.0))
                    self.psi_prev[i] = np.append(self.psi_prev[i], np.float32(0.0))

                    self.adj[j] = np.append(self.adj[j], np.int32(i))
                    self.psi_curr[j] = np.append(self.psi_curr[j], np.float32(0.0))
                    self.psi_prev[j] = np.append(self.psi_prev[j], np.float32(0.0))

                    existing.add(j)
```

### 4.7 `_compute_physics_reward()` — New method (replaces SIE v2)

```python
def _compute_physics_reward(self, dphi: np.ndarray):
    """
    Physics-derived reward observables. Replaces heuristic SIE.
    All quantities from φ, ψ, adj, energy/entropy functionals.
    No lookup tables. No weights.

    Source:
      Energy dissipation rate (−dH/dt): CF01 §4.2, CF02 §4.2
      Fisher speed: CF06 §4.3
      Entropy production rate: CF02 §4.2
    """
    # Energy: H[φ] = Σ_edges D·ψ_ij·(φ_i−φ_j)² + Σ_nodes V(φ_i)
    E_gradient = 0.0
    for i, nbrs in enumerate(self.adj):
        for ki, j in enumerate(nbrs):
            if int(j) > i:
                E_gradient += self.D * float(self.psi_curr[i][ki]) * (self.phi_curr[i] - self.phi_curr[int(j)]) ** 2
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

### 4.8 `stimulate_indices()` — Modified

```python
def stimulate_indices(self, idxs, amp: float = 0.05):
    """Inject external stimulus. Updates phi_curr."""
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
```

---

## 5. stepper.py — Modifications

### 5.1 Function signature

OLD:
```python
def compute_step_and_metrics(nx: Any, t: float, step: int, idf_scale: float = 1.0) -> Tuple[Dict[str, Any], Dict[str, Any]]:
```

NEW:
```python
def compute_step_and_metrics(nx: Any, step: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
```

Remove the `t` and `idf_scale` parameters.

### 5.2 Remove SIE drive computation (CONTROL PATH ONLY)

DELETE all code that computes or uses `sie_drive`, `sie_gate`, `dom_mod`, `domain_modulation`, and `idf_scale` as **control inputs** to the physics step. DELETE the entire block from "1) density from active edges" through "4) SIE drive" inclusive.

**Important distinction:** This section deletes **drivers**, not **meters**.

**Logging policy (must improve, not wipe):**
- You are NOT required to preserve legacy meter names just for compatibility.
- You MUST ensure the new logging is **strictly richer in information content** (by storing physics-native primitive state + a compact signature vector).
- Any meter that remains must be there because it helps diagnose cognition (criticality, regimes, metastability, structure, sensorimotor coupling), not because the old code used it.

**Instrumentation flags are allowed** (they are not physics): you may gate expensive meter computation behind `LOG_LEVEL` / `LOG_FULL`, but these flags must not affect physics state evolution.



### 5.3 Connectome step call

OLD:
```python
nx.connectome.step(
    t,
    domain_modulation=float(getattr(nx, "dom_mod", 1.0)),
    sie_drive=sie_gate,
    use_time_dynamics=bool(getattr(nx, "use_time_dynamics", True)),
)
```

NEW:
```python
nx.connectome.step(tick=step)
```

### 5.4 Metrics: physics-native signature logging (append-only)

After the step call, construct a **physics-native signature vector** from the current state. Do not keep "zombie" legacy meters unless they are explicitly redefined as cognition-relevant readouts from the physics state.

Per-tick logging MUST be **O(N) or O(N·k)** (no dense scans). Anything heavier (Granger, TC/O-info/MIP, PCA, etc.) is OFFLINE analysis on the dumped logs/snapshots.

```python
# 6) metrics (physics-native signature vector; bounded cost)
m = {}

# --- Core physics observables from connectome (new) ---
m["H"] = float(getattr(nx.connectome, "_reward_H", 0.0))
m["dH_dt"] = float(getattr(nx.connectome, "_reward_dH_dt", 0.0))
m["S"] = float(getattr(nx.connectome, "_reward_S", 0.0))
m["dS_dt"] = float(getattr(nx.connectome, "_reward_dS_dt", 0.0))
m["fisher_speed"] = float(getattr(nx.connectome, "_reward_fisher_speed", 0.0))
m["boundary_flux"] = float(getattr(nx.connectome, "_reward_boundary_flux", 0.0))

# --- Minimal activity/structure meters derived from primitive fields (cognition-relevant) ---
phi_curr = nx.connectome.phi_curr
phi_prev = nx.connectome.phi_prev
phi_dot  = (phi_curr - phi_prev)

# Activity scalars (used for PSD / avalanches / regime clustering)
m["phi_dot_rms"] = float(np.sqrt(np.mean(phi_dot * phi_dot)))
m["phi_dot_var"] = float(np.var(phi_dot))
m["phi_mean"]    = float(np.mean(phi_curr))
m["phi_var"]     = float(np.var(phi_curr))

# Structure scalars (weighted topology; emergent threshold)
eta_bond = float(np.sqrt(2.0 * nx.connectome.eps_topo * nx.connectome.kT))
# Count bonds above noise floor (O(N·k))
active_edges = 0
psi_sum = 0.0
psi_sq_sum = 0.0
for i in range(nx.connectome.N):
    psi = nx.connectome.psi_curr[i]
    if psi.size:
        active_edges += int(np.sum(psi > eta_bond))
        psi_sum += float(np.sum(psi))
        psi_sq_sum += float(np.sum(psi * psi))
m["active_edges"] = int(active_edges)
m["psi_mean"] = float(psi_sum / max(1, sum(len(nx.connectome.psi_curr[i]) for i in range(nx.connectome.N))))
m["psi_rms"]  = float(np.sqrt(psi_sq_sum / max(1, sum(len(nx.connectome.psi_curr[i]) for i in range(nx.connectome.N)))))

# --- Traversal findings (if present; meters only) ---
try:
    findings = getattr(nx.connectome, "findings", None)
    if findings:
        m.update(findings)
except Exception:
    pass

# Drive is physics-derived only (no SIE)
m["valence_01"] = float(getattr(nx.connectome, "_last_sie2_valence", 0.0))
drive = {"valence_01": m["valence_01"]}

return m, drive
```

Notes:
- If you want to retain a legacy meter name like `firing_var`, you may redefine it explicitly as `phi_dot_var` (or a documented function of `phi_dot`) and log it — but only if it serves a cognition analysis use-case.
- Full-state dumps (H5 engram / snapshots) are the primary path for deep analysis; per-tick scalars are a compact index.

---



## 6. main.py (loop) — Modifications

### 6.1 Time variable

OLD:
```python
t = time.time() - t0
```

NEW:
```python
t_wall = time.time() - t0  # wall clock for diagnostics only
```

The integer `step` passed to the stepper IS the physics time.

### 6.2 Stepper call

OLD:
```python
m, drive = _compute_step_and_metrics(nx, t, step, idf_scale=idf_scale)
```

NEW:
```python
m, drive = _compute_step_and_metrics(nx, step)
```

### 6.3 Remove dom_mod

DELETE: `idf_scale = 1.0` and any code that reads `getattr(nx, "dom_mod", ...)`.

---

## 7. nexus.py — Modifications

### 7.1 Remove from imports

DELETE this line:
```python
from .core.void_dynamics_adapter import get_domain_modulation
```

### 7.2 Remove from `__init__` constructor parameters

DELETE: `use_time_dynamics` parameter and `domain` as a modulation parameter.

### 7.3 Remove from `__init__` body

DELETE:
```python
self.use_time_dynamics = use_time_dynamics
```

DELETE:
```python
self.dom_mod = float(get_domain_modulation(self.domain))
```

### 7.4 Remove from `run()`

OLD:
```python
self.logger.info("nexus_started", extra={"extra": {"N": self.N, "k": self.k, "hz": self.hz, "domain": self.domain, "dom_mod": self.dom_mod}})
```

NEW:
```python
self.logger.info("nexus_started", extra={"extra": {"N": self.N, "k": self.k, "hz": self.hz, "domain": self.domain}})
```

---

## 8. engine/core_engine.py — Modifications

### 8.1 step_connectome signature

OLD:
```python
def step_connectome(self, t: float, domain_modulation: float = 1.0, sie_gate: float = 0.0, use_time_dynamics: bool = True) -> None:
    try:
        self._nx.connectome.step(t, domain_modulation=float(domain_modulation), sie_drive=float(sie_gate), use_time_dynamics=bool(use_time_dynamics))
    except Exception:
        pass
```

NEW:
```python
def step_connectome(self, tick: int) -> None:
    try:
        self._nx.connectome.step(tick=int(tick))
    except Exception:
        pass
```

---

## 9. UTED — Physics-Clock Timestamps

In `vdm_rt/io/uted/ute_mux.py`, all adapters:

```python
from vdm_rt.core.void_dynamics_adapter import TAU, GAMMA
import numpy as np

# In every adapter's poll_frames():
# Compute conversion symbolically, never as a pre-computed integer
dt_physical = float(np.sqrt(TAU / GAMMA))  # dimensionless ticks → seconds-equivalent
timestamp_us = int(tick * dt_physical * 1_000_000)
# NOT time.time_ns() // 1000
```

`HeartbeatAdapter` emits one frame per tick. No wall-clock rate limiting.

Wall-clock time may be stored in a separate `wall_us` field for debugging but must NOT be in `timestamp_us`.

---

## 10. sie_v2.py — Deprecation

`sie_v2.py` continues to exist but `sie_step()` is no longer called from the hot path. The physics-derived reward in `sparse_connectome._compute_physics_reward()` replaces it. `sie_v2.py` must not be imported by `sparse_connectome.py` or `stepper.py`.

---

## 11. Eliminated Proxies Checklist

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
- [ ] `TOPO_PERIOD` as a constant or attribute
- [ ] `TOPO_THRESHOLD` as a constant or attribute
- [ ] `TOPO_PATIENCE` as a constant or attribute
- [ ] `R_NUCLEATION` as a constant or attribute
- [ ] `tau_e` as a constant (the variable `tau_eff` computed from `τ·exp(β·debt)` is allowed)
- [ ] `DEBT_MAX` or `debt_max` as a constant
- [ ] `dt_physics_us` as a constant
- [ ] `PSI_DEATH`
- [ ] `PSI_SEED`
- [ ] `_maybe_update_topology` as a method definition
- [ ] `_compute_eligibility` as a method definition
- [ ] `eligibility` as a stored array (field velocity `|φ̇|` computed inline is allowed)
- [ ] `last_activation_tick` as a stored array

---

## 12. Validation Gates (run 50,000 ticks, N=216 (6³), k_init=6)

All must pass or the migration is rejected:

1. **No NaN:** `np.any(np.isnan(phi_curr))` is never True at any tick.
2. **Field bounded:** `phi_curr ∈ [0.0, 1.0]` every tick.
3. **Bimodal distribution:** At tick 50000, histogram of `phi_curr` has two peaks: `count(φ < 0.2) > 0.2·N` AND `count(φ > 0.8) > 0.2·N`.
4. **Causal propagation:** Inject stimulus at node i at tick T. Measure first activation tick at node j (graph distance d). Delay ≥ `d / c` where `c = √(γ/τ)`. Test 10 random pairs with d ∈ [3, 10].
5. **Energy non-increase:** Compute H every 100 ticks. Over any 1000-tick window, H must not increase by more than 5% of its starting value.
6. **Gini coefficient:** At tick 50000, Gini of `phi_curr` ≥ 0.45.
7. **Bond persistence:** Mean bond lifetime (ticks a bond persists with ψ > 0.5 before dropping below the bond noise floor $\sqrt{2 \cdot \varepsilon_{topo} \cdot kT}$) > 500 ticks. The telegraph inertia τ_bond = τ/ε_topo = 200 provides this naturally.
8. **Bond locality:** No bond is ever created between nodes with `||pos[i] − pos[j]|| > max(r_causal[i], r_causal[j])`.
9. **Eliminated proxies:** grep check (Section 11) passes with zero hits.
10. **Bond field non-trivial:** At tick 50000, `count(ψ > 0.5) > 0.5 · total_edges` AND `count(ψ < 0.1) > 0`.
11. **Per-tick cost:** Mean wall-clock time per tick ≤ 3x the time for a single `klein_gordon_rhs()` call (bond update overhead is bounded).
12. **No debt overflow:** `np.any(np.isinf(self.debt))` is never True. `np.max(self.debt) < 500` at tick 50000 (self-limiting via exponential friction).

---

## 13. Implementation Order

1. **Void_Equations.py** — rewrite (Section 2)
2. **void_dynamics_adapter.py** — rewrite (Section 3)
3. **sparse_connectome.py** — modify `__init__`, replace `step()`, add new methods (Section 4)
4. **stepper.py** — modify (Section 5)
5. **main.py** — modify (Section 6)
6. **nexus.py** — modify (Section 7)
7. **core_engine.py** — modify (Section 8)
8. **UTED** — create/modify (Section 9)
9. **Validation** — run all gates (Section 12)

Each step must pass `python -m pytest` before proceeding. If existing tests reference eliminated parameters (`domain_modulation`, `use_time_dynamics`, `sie_drive`, `t` as float, etc.), update the tests to match the new signatures FIRST.

---

## Appendix: CF Chain Traceability

| v3 Mechanism | v4 Replacement | CF Source |
|---|---|---|
| `TOPO_PERIOD = 50` (cron timer) | Bond field ψ with τ_bond = τ/ε_topo ≈ 200 (natural timescale) | CF02 §4.1: M-limb coupling ε sets dissipative timescale |
| `TOPO_THRESHOLD = 0.01` (eligibility gate) | Bond energy vs kT (thermal activation) | CF06 §4.3: fluctuation-dissipation gives natural threshold |
| `TOPO_PATIENCE = 100` (debounce counter) | Telegraph inertia τ_bond (bonds resist sudden change) | CF04 §2.1: relaxation time = memory of previous state |
| `tau_e = 250` (eligibility trace) | `|φ̇|` = field velocity (no separate trace) | CF11 §2.3: velocity is a state variable of the telegraph eq |
| `R_NUCLEATION = 4.0` (fixed spatial cutoff) | Causal cone r_causal(i) grows from dynamics | CF04 §4.2: finite propagation speed → causal cone structure |
| `debt_max = 10.0` (ceiling clamp) | Self-limiting via exp(β·debt) asymptotic freeze | CF03 §7.2: throttling is exponential, not clamped |
| `dt_physics_us = 6324555` (pre-computed integer) | `√(τ/D)` computed symbolically at I/O boundary | CF04 §7.1: dimensional analysis, not magic numbers |
| **`PSI_DEATH = 1e-6`** (arbitrary float threshold) | Dynamic thermal noise floor **$\eta_{bond} = \sqrt{2 \cdot \varepsilon_{topo} \cdot kT}$** | **CF07 §4.1 & §4.2**: Epistemic projection; classical reality is bounded by finite resolution limits. |
| **`PSI_SEED = 0.01`** (arbitrary spawn value) | Natural nucleation from **$\psi = 0.0$** via metriplectic integration | **CF07 §4.1**: Classical boundaries emerge from natural forces, forbidding artificial state injection. |

---

**END OF DIRECTIVE v4**
