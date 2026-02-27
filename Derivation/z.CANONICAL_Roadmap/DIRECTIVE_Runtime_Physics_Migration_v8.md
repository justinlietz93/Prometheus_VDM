# Runtime Physics Migration Directive v8

**Author:** Justin K. Lietz  
**Date:** 2026-02-25  
**Status:** DRAFT — supersedes v7  
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
- `(L_ψ φ)_i = Σ_{j ∈ adj(i)} ψ_ij · (φ_j − φ_i)` — bond-weighted graph Laplacian on the connectome topology. A fully formed bond (ψ=1) contributes full coupling. A dissolving bond (ψ→0) contributes decreasing coupling. This replaces the binary adjacency of v3. The Laplacian is defined on whatever adjacency structure the graph currently has — it does not require or assume a spatial embedding.
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

New edges can only be proposed between nodes within each other's causal cone, measured in graph distance (hops):

```
h_causal[i] += floor(c_eff(i))  each tick while |φ̇_i| > kT
```

where `c_eff(i) = √(D / τ_eff(i))` is the local propagation speed in hops per tick. Candidate edges require `graph_distance(i, j) ≤ h_causal[i]` AND `|φ̇_i| · |φ̇_j| > kT` AND (i,j) not already in adjacency.

There is no spatial embedding. The causal cone is defined on the graph topology itself. Graph distance is hop count along existing edges.

**Walker-assisted proposal (preferred implementation):** Rather than computing graph distance via BFS (which is O(k̄^h) per active node), candidate edges are drawn from the walker trail map. Nodes that walkers from node i have recently visited are natural bond candidates — they are within the causal cone by construction, since the walker traversed the path. This reduces proposal cost from O(N_active · k̄^h) to O(N_active · w) where w is the mean walker trail length per node.

### 0.2 Constants — Material Properties Only

| Name | Value | Role | Source | Type |
|------|-------|------|--------|------|
| `τ` | `2.0` | Base telegraph relaxation time | CF04 §2.1 | Material |
| `β` | `0.1` | Debt throttle exponent | CF03 §7.2 | Material |
| `λ` | `1.0` | Double-well barrier height | CF03 §1.1 | Material |
| `D` (= γ) | `0.05` | Diffusion coefficient | CF04 §6.1 | Material |
| `kT` | `0.001` | Effective temperature | CF06 §4.3 | Material |
| `ε_topo` | `0.01` | Structural coupling constant | CF02 §4.1 | Material |
| `WARM_THRESHOLD` | `0.05` | Trail heat below which a node is Zone 3 (cold) | TrailMap half-life + operational | Tuning |

Note: WARM_THRESHOLD is a tuning parameter, not a material constant. It
controls the boundary between "still evolving from last interaction" and
"effectively frozen." It can be adjusted without changing the physics.

### 0.3 Eliminated Constants (must not appear anywhere after migration)

`F_REF`, `PHASE_SENS`, `ALPHA` (as reaction rate), `BETA` (as separate decay rate in GDSP), `domain_modulation`, `use_time_dynamics`, `kappa` (as separate from D), `TOPO_PERIOD`, `TOPO_THRESHOLD`, `TOPO_PATIENCE`, `R_NUCLEATION`, `tau_e`, `debt_max`, `dt_physics_us`, `DEBT_MAX`, `PSI_DEATH`, `PSI_SEED`, `pos` (spatial embedding array), `r_causal` (Euclidean causal radius — replaced by `h_causal` in graph hops), `side` (cubic grid dimension), `_build_cubic_adjacency` (cubic lattice initialization — replaced by graph initialization).
`h_causal` (per-node causal horizon — replaced by walker trail reachability),
`_h_causal_frac` (fractional hop accumulator — eliminated with h_causal),
`MAX_BFS_DEPTH` (never needed — walkers replace BFS).

### 0.4 Compute, Memory, and Scaling

#### DEVICE NEUTRALITY CONSTRAINT

The fast path MUST NOT assume a single address space, a single execution device, or synchronous execution order between independent operations.

Specifically:

1. The bond-weighted Laplacian, the pointwise node solve, the bond solve, and the debt update are independent operations on the same tick's data. They MUST NOT be fused into a single function that requires all to execute on the same device.

2. All state arrays (phi_curr, phi_prev, debt, adj, psi_curr, psi_prev, h_causal) MUST be stored in standard contiguous array formats (numpy ndarray, or equivalent) that can be copied to any device buffer without reshaping or reinterpretation.

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

**Total: O(N · k̄) per tick** where k̄ is the emergent mean degree of the connectome. For k̄ = 20 and N = 1,000,000 this is ~40M operations per tick (Laplacian + bond update are each O(N·k̄)). For k̄ = 20 and N = 100,000,000 this is ~4B — still tractable with vectorized numpy or GPU dispatch.

**Candidate edge proposal: O(N_active · w)** where w is the mean walker trail length per node. Walker trails provide a natural candidate list of reachable nodes within the causal cone, eliminating the need for BFS graph-distance computation. Evaluated every tick but only for active nodes (|φ̇| > kT). Bounded by walker budget.

**Comparison to current architecture:**

| Architecture | Per-tick cost | Topology persistence | Causal structure |
|---|---|---|---|
| Current (global rebuild) | O(N · 64) | None — rebuilt from scratch | Violated |
| Physics-derived (bond field) | O(N · k̄), k̄ emergent | Persistent — bonds carry forward | Preserved — causal cone (graph distance) |

**The physics-derived architecture is ~10x cheaper per tick AND physically correct.**

#### Memory cost

| Array | Size | Dtype | Bytes (N=1M, k̄=20) |
|-------|------|-------|-------------------|
| `phi_curr` | N | float32 | 4 MB |
| `phi_prev` | N | float32 | 4 MB |
| `debt` | N | float64 | 8 MB |
| `h_causal` | N | int32 | 4 MB |
| `psi_curr` | N · k̄ | float32 | 80 MB |
| `psi_prev` | N · k̄ | float32 | 80 MB |
| `adj` | N · k̄ | int32 | 80 MB |
| `W` (alias to phi_curr) | 0 | — | 0 |

**Total: ~260 MB for N = 1,000,000 with k̄ = 20.**

Note: `pos` array is eliminated. There is no spatial embedding. Adjacency is defined by graph topology, not Euclidean coordinates.

#### Scaling law

```
T_tick = a · W · k̄
```

Where W is the size of the active + warm set, not N. Linear in the number of
nodes receiving attention this tick. The physics per node is unchanged — same
Klein-Gordon, same bond update. Only the count of nodes computed changes.

Replace the memory table — add:

| Array | Size | Dtype | Bytes (N=1M, k̄=20) |
|-------|------|-------|---------------------|
| `last_visit` | N | int32 | 4 MB |
| `frozen_phi` | N | float32 | 4 MB |

These are bookkeeping for the catch-up computation. Small overhead.

Linear in N for fixed k̄. The mean degree k̄ is determined by the dynamics, not fixed by geometry. In practice, mean degree has been observed to stabilize in the range 15–25 for runs from N=1,000 to N=10,000. Whether k̄ scales with N is an empirical question — if k̄ = O(1), scaling is linear; if k̄ = O(log N), scaling is O(N log N), still tractable.

### 0.5 Topology and Manifold Structure

The discrete manifold is the connectome graph itself. Nodes have no fixed spatial embedding. There is no coordinate grid, no position array, and no Euclidean distance metric. The adjacency structure IS the geometry. All notions of "distance," "locality," and "neighborhood" are defined in terms of graph hops along existing edges.

**Initial connectivity:** k-regular random graph or preferential attachment, matching the existing runtime initialization parameter `k_init`. The initial degree distribution and graph structure are initial conditions, analogous to the initial field configuration φ(t=0). The value of `k_init` is a free parameter (initial condition), not a material constant.

**N is unconstrained.** Any positive integer. No cube requirement, no grid constraint.

**No pos array.** Node spatial positions are not defined, not stored, and not referenced by any physics equation. The bond-weighted Laplacian, the Klein-Gordon solver, the bond field equation, the decoherence threshold, and the causal cone constraint are all defined on the graph topology and do not require spatial coordinates. If a spatial embedding is needed for visualization, it is computed from the graph Laplacian spectrum (Fiedler layout) at render time and is NOT stored as simulation state.

**Topology evolution.** The graph self-modifies through two mechanisms:
1. **Bond death (decoherence):** When ψ_ij drops below the thermal noise floor √(2 · ε_topo · kT), the edge is removed from the adjacency list (CF07).
2. **Bond birth (nucleation):** Candidate edges are proposed between co-active nodes within each other's causal cone (measured in graph hops via `h_causal`). New bonds are nucleated at ψ_ij = 0.0 and must be lifted by the metriplectic dynamics (CF07).

This produces a self-modifying scale-free topology with emergent degree heterogeneity, hub formation, hierarchical modularity, and territory structure — the phenomena documented in the Four Signatures paper and the Aura developmental run.

---

### 0.6 — Walker-Gated Computation

### The principlef

The field φ exists at every node. But the field only **evolves** at nodes where
gauge bosons (walkers) are present or have recently been present. A node with no
recent walker visit is in an analytically predictable state: exponential
relaxation toward whichever potential well it occupies. Computing this relaxation
tick-by-tick wastes arithmetic on a known answer.

This is not an optimization. It is what gauge theory says. Interactions between
nodes are mediated by gauge bosons (CF09). No boson → no interaction → no state
change beyond autonomous relaxation. The walkers are the carriers of interaction.
Where they go, the universe computes itself. Where they don't, nothing happens.

### Physical justification

1. **Telegraph finite speed (CF04):** Information propagates at c = √(D/τ)
   hops per tick. Walkers traverse the graph at bounded speed. A region not yet
   reached by any walker is causally disconnected from any stimulus.

2. **Thermal fluctuations are negligible (CF06):** With kT = 0.001 and barrier
   height λ = 1.0, the probability of a thermal kick moving a node from one
   well to another is ∝ exp(−ΔV/kT) = exp(−250) ≈ 0. Cold nodes don't
   spontaneously change state.

3. **Epistemic projection (CF07):** A fluctuation without an observer is not an
   event. A neuron spiking without a walker present to carry the signal cannot
   affect the global system. When a walker arrives and catches the node up, the
   spike becomes real — it enters the M-limb as a classical observable.

4. **Gauge boson mediation (CF09):** The berry connection's excitations (walkers)
   mediate the coupling between nodes. The bond-weighted Laplacian
   (L_ψ φ)_i = Σ ψ_ij(φ_j − φ_i) computes the interaction. But between two
   cold nodes deep in the same well, φ_j ≈ φ_i, so the Laplacian is ≈ 0.
   The interaction is zero without activity, and activity requires a walker
   to have brought or observed a signal.

### The three zones

Every node exists in one of three thermal zones, determined by walker trail
heat (from the existing TrailMap/HeatMap infrastructure):

**ZONE 1 — HOT (walker present this tick)**
Full metriplectic Klein-Gordon step: Laplacian coupling, bond potential,
fluctuation-dissipation noise, telegraph solve. Bond field ψ for all edges
of this node and its neighbors are updated. Edge proposals evaluated. Events
emitted to bus. This is where reality is being actively constructed.

Cost: O(k̄) per hot node (Laplacian + bond update for local neighborhood).

**ZONE 2 — WARM (walker trail decaying, above threshold)**
Reduced-frequency update. The node was recently visited; its state is still
evolving from the last interaction. Bond fields continue their telegraph
relaxation. Node field continues toward equilibrium. Update frequency scales
with trail heat: every tick while heat > WARM_HIGH, every Nth tick as heat
decays toward WARM_LOW.

Cost: O(k̄) per warm node, but executed less frequently.

**ZONE 3 — COLD (below threshold, no recent walker)**
No tick-by-tick computation. State is frozen at last computed value plus a
timestamp. When a walker arrives (cold → hot transition), the node is caught
up analytically before the full physics step runs.

Cost: O(1) at time of catch-up (exponential relaxation formula).

### Catch-up computation (cold → hot transition)

When a walker arrives at a cold node i at tick t_now, with last visit at
t_last:

```
Δt = t_now − t_last

# Node field: exponential relaxation toward nearest well
φ_well = round(φ_i(t_last))  # 0.0 or 1.0
φ_i(t_now) = φ_well + (φ_i(t_last) − φ_well) · exp(−Δt / τ_eff_i)

# φ_prev for telegraph history
φ_prev_i(t_now) = φ_well + (φ_prev_i(t_last) − φ_well) · exp(−(Δt−1) / τ_eff_i)

# Bond fields: each bond relaxes toward its own nearest well
for each edge (i, j):
    ψ_well = round(ψ_ij(t_last))  # 0.0 or 1.0
    ψ_ij(t_now) = ψ_well + (ψ_ij(t_last) − ψ_well) · exp(−Δt / τ_bond)
    # If ψ decayed below noise floor during gap → edge died
    if ψ_ij(t_now) < ETA_BOND_FLOOR:
        remove edge (i, j)

# Debt: exponential decay toward zero (no activity during gap)
debt_i(t_now) = debt_i(t_last) · (1 − β)^Δt
```

This is exact for isolated nodes (no external drive during gap). It is
approximate for nodes that had active neighbors during the gap — but those
neighbors would have been in Zones 1-2 (they had walkers), and the Laplacian
coupling from their direction was being computed on the neighbor's side
already. The cold node's contribution to that coupling was its frozen φ value,
which is correct because it wasn't changing.

### Walker trail as computation schedule

The existing `cortex/` walker system already provides the infrastructure:

| Component | Role in computation scheduling |
|-----------|-------------------------------|
| `TrailMap` (half-life 50 ticks) | Defines Zone 2 boundary. Nodes with trail score > WARM_THRESHOLD are in Zone 2. |
| `HeatMap` (half-life 200 ticks) | Provides longer-term activity memory for walker routing. |
| `ColdMap` | Tracks least-visited nodes. ColdScout routes walkers there, ensuring eventual coverage. |
| `VoidRayScout` | Routes along φ gradients — steers walkers toward active boundaries where computation matters most. |
| `run_scouts_once()` | Per-tick walker dispatch. Already bounded by time budget. |

The walker system is NOT new infrastructure to build. It exists and runs every
tick through `CoreEngine.step()`. The migration wires its output (trail heat
scores) into the connectome's computation scheduler.

### Active set construction

Each tick, the active set is built from walker events + trail decay:

```python
# After walker dispatch (existing cortex/ path):
active_set = set()     # Zone 1: full physics this tick
warm_set = set()       # Zone 2: reduced-frequency physics

# All nodes touched by walkers this tick → Zone 1
for event in walker_events:
    if event.kind == "vt_touch":
        active_set.add(event.token)
    elif event.kind == "edge_on":
        active_set.add(event.u)
        active_set.add(event.v)

# Include immediate neighbors of hot nodes (Laplacian coupling)
for i in list(active_set):
    for j in adj[i]:
        if j not in active_set:
            warm_set.add(j)

# Trail-warm nodes not already active → Zone 2
for node, score in trail_map.working_set():
    if score > WARM_THRESHOLD and node not in active_set:
        warm_set.add(node)
```

### Scaling

| Architecture | Per-tick cost | What drives it |
|---|---|---|
| v3 (global rebuild) | O(N · 64) | Every node, every tick, 64 candidates |
| v8 (full field update) | O(N · k̄) | Every node, every tick, k̄ neighbors |
| **v8.1 (walker-gated)** | **O(W · k̄)** | **W walker-visited nodes, k̄ neighbors** |

Where W = |active_set| + |warm_set|. For Aura at N=5000 with 256 walkers
doing 3 hops: W ≈ 768 hot + ~2000 warm neighbors ≈ 2800 nodes = 56% of N.
At N=100,000 with the same walker budget: W ≈ 3% of N.
At N=1,000,000: W ≈ 0.3% of N.

The walker budget is a tuning parameter (initial condition, not material
constant). More walkers → more of the graph is "conscious" per tick. Fewer
walkers → tighter attention, deeper focus on active regions.

### What this replaces

- **h_causal (causal horizon in hops):** Eliminated. The walkers ARE the causal
  cone. If a walker can reach node j from node i, j is within i's causal cone
  by construction — the walker traversed the path.

- **_propose_new_edges via BFS:** Eliminated. Walker trails provide the
  candidate set directly. No graph-distance computation needed.

- **O(N) per-tick loops in step():** Replaced by O(W) loops over active/warm
  sets.

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

    Defined on the connectome graph topology. No spatial embedding assumed.
    Works on any adjacency structure — cubic, scale-free, or self-modifying.

    Source: CF11 §2.3, CF03 §1.1.
    Complexity: O(N·k̄) where k̄ is mean degree.
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

# --- Walker-gated computation state ---
self.last_visit = np.zeros(self.N, dtype=np.int32)   # tick of last Zone 1 visit
self.last_visit[:] = -1  # mark all as never-visited (forces catch-up on first touch)

# Warm threshold for trail-heat gating (TODO NO HARDCODING, LET THE DYNAMICS MANAGE THIS)
self.WARM_THRESHOLD = 0.05

# --- Initial adjacency: from existing runtime graph initialization ---
# Uses k_init (constructor parameter) to build k-regular random graph
# or preferential attachment. This is an initial condition, not a
# lattice constraint. The topology will self-modify via bond dynamics.
# NOTE: self.adj must already be populated by the existing runtime
# initialization code (e.g., _build_initial_graph, or loaded from
# checkpoint). This directive does not change graph initialization —
# it changes graph EVOLUTION (bond field replaces global rebuild).

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

### 4.2 Graph initialization — No change from existing runtime

The existing runtime's graph initialization (k-regular random, preferential attachment,
or checkpoint load) is RETAINED. The migration does not change how the initial graph
is built — it changes how the graph EVOLVES after initialization.

The `_build_cubic_adjacency()` method from v7 is **deleted**. It must not exist in the
migrated codebase. If a cubic lattice is desired for controlled experiments, it can be
loaded as a checkpoint, not hardcoded as the only initialization path.

**Required invariant after initialization:**
- `self.adj` is a list of N numpy int32 arrays (variable length per node).
- `self.psi_curr[i].shape == self.adj[i].shape` for all i.
- `self.psi_prev[i].shape == self.adj[i].shape` for all i.
- All initial bonds have ψ = 1.0 (fully formed).

### 4.3 `step()` — New signature

OLD:
```python
def step(self, t: float, domain_modulation: float, sie_drive: float = 1.0, use_time_dynamics: bool = True):
```

NEW:
```python
def step(self, tick: int):
```

### **Delete the entire v8 step() body.** Replace with:

```python
def step(self, tick: int, walker_events: list = None, trail_scores: dict = None):
    """
    One tick of walker-gated metriplectic Klein-Gordon.

    Only nodes in the active set (walker-visited) and warm set (recently visited
    neighbors) receive the full physics step. Cold nodes are analytically frozen.

    The walker system runs BEFORE this method. Walker events and trail scores
    are passed in from the engine layer.

    Source: CF01 §4.1 (dF/dt = {F,H}_J + (F,S)_M — both terms, every tick,
    for every OBSERVED degree of freedom).
    """
    self._tick = tick
    N = self.N
    from .void_dynamics_adapter import klein_gordon_rhs, bond_potential_derivative

    # --- Step 0: Build active and warm sets from walker data ---
    active_set = set()   # Zone 1: full physics
    warm_set = set()     # Zone 2: neighbor coupling

    if walker_events:
        for ev in walker_events:
            kind = getattr(ev, "kind", None)
            if kind == "vt_touch":
                node = int(getattr(ev, "token", -1))
                if 0 <= node < N:
                    active_set.add(node)
            elif kind == "edge_on":
                u = int(getattr(ev, "u", -1))
                v = int(getattr(ev, "v", -1))
                if 0 <= u < N:
                    active_set.add(u)
                if 0 <= v < N:
                    active_set.add(v)

    # Add external stimulation targets to active set
    if hasattr(self, '_stim'):
        stim_active = np.where(self._stim > 0.01)[0]
        for idx in stim_active:
            active_set.add(int(idx))

    # Neighbors of active nodes → warm set (Laplacian coupling boundary)
    for i in list(active_set):
        for j in self.adj[i]:
            j_int = int(j)
            if j_int not in active_set:
                warm_set.add(j_int)

    # Trail-warm nodes not already categorized
    if trail_scores:
        for node_str, score in trail_scores.items():
            node = int(node_str)
            if score > self.WARM_THRESHOLD and node not in active_set:
                warm_set.add(node)

    # Combined set for physics computation
    compute_set = active_set | warm_set

    if not compute_set:
        # Nothing to compute — all nodes cold. Just tick housekeeping.
        try:
            self._stim *= getattr(self, "_stim_decay", 0.90)
        except Exception:
            pass
        return

    # --- Step 1: Catch-up cold → hot/warm transitions ---
    for i in compute_set:
        t_last = int(self.last_visit[i])
        if t_last < 0:
            # Never visited — initial state is fine, just mark
            self.last_visit[i] = tick
            continue
        dt = tick - t_last
        if dt <= 1:
            continue  # visited last tick, no gap to close

        # Analytical relaxation during the gap
        tau_eff_i = float(self.tau * np.exp(self.beta * self.debt[i]))
        phi_well = round(float(self.phi_curr[i]))  # 0.0 or 1.0

        decay_phi = np.exp(-dt / tau_eff_i)
        self.phi_curr[i] = phi_well + (self.phi_curr[i] - phi_well) * decay_phi
        self.phi_prev[i] = phi_well + (self.phi_prev[i] - phi_well) * np.exp(-(dt - 1) / tau_eff_i)

        # Bond relaxation
        tau_bond = self.tau / self.eps_topo
        decay_psi = np.exp(-dt / tau_bond)
        for ki in range(self.adj[i].size):
            psi_well = round(float(self.psi_curr[i][ki]))
            self.psi_curr[i][ki] = psi_well + (self.psi_curr[i][ki] - psi_well) * decay_psi
            self.psi_prev[i][ki] = psi_well + (self.psi_prev[i][ki] - psi_well) * np.exp(-(dt - 1) / tau_bond)

        # Debt decay during gap (no activity)
        self.debt[i] *= (1.0 - self.beta) ** dt

    # Update visit timestamps for computed nodes
    for i in active_set:
        self.last_visit[i] = tick

    # --- Step 2: Node field computation (active + warm only) ---
    compute_list = np.array(sorted(compute_set), dtype=np.int32)
    tau_eff = self.tau * np.exp(self.beta * self.debt)
    phi_dot = self.phi_curr - self.phi_prev

    # Laplacian for computed nodes only
    rhs = np.zeros(N, dtype=np.float32)
    from .void_dynamics_adapter import LAMBDA as lam_val, GAMMA as D_val, KT_EFF as kT_val
    for i in compute_list:
        nbrs = self.adj[i]
        if nbrs.size == 0:
            continue
        # Bond-weighted Laplacian: Σ ψ_ij (φ_j − φ_i)
        lap = np.sum(self.psi_curr[i] * (self.phi_curr[nbrs] - self.phi_curr[i]))
        # Potential derivative: 2λ φ(1−φ)(1−2φ)
        phi_i = self.phi_curr[i]
        dV = 2.0 * self.lam * phi_i * (1.0 - phi_i) * (1.0 - 2.0 * phi_i)
        # Noise
        eta = np.sqrt(2.0 * self.D * self.kT) * self.rng.standard_normal()
        rhs[i] = self.D * lap - dV + eta

    # Telegraph solve for computed nodes
    phi_new = self.phi_curr.copy()
    for i in compute_list:
        a_inertia = float(tau_eff[i])
        numerator = rhs[i] + (2.0 * a_inertia + 1.0) * self.phi_curr[i] - a_inertia * self.phi_prev[i]
        denominator = a_inertia + 1.0
        phi_new[i] = np.clip(numerator / denominator, 0.0, 1.0)

    # --- Step 3: Bond field update (computed nodes only) ---
    tau_bond = np.float32(self.tau / self.eps_topo)
    phi_dot_abs = np.abs(phi_dot).astype(np.float32)

    for i in compute_list:
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

    # --- Step 4: Edge death (computed nodes only) ---
    self._remove_dead_edges(compute_list)

    # --- Step 5: Edge birth from walker trails ---
    self._propose_from_trails(walker_events, phi_dot_abs)

    # --- Step 6: Update node field history ---
    dphi = np.zeros(N, dtype=np.float32)
    for i in compute_list:
        dphi[i] = phi_new[i] - self.phi_curr[i]
    self.phi_prev[compute_list] = self.phi_curr[compute_list].copy()
    self.phi_curr[compute_list] = phi_new[compute_list]
    self.W = self.phi_curr  # backward compat alias

    # --- Step 7: Debt (computed nodes only) ---
    self.debt[compute_list] = (
        (1.0 - self.beta) * self.debt[compute_list]
        + np.abs(dphi[compute_list]).astype(np.float64)
    )

    # --- Step 8: External stimulation decay ---
    try:
        self._stim *= getattr(self, "_stim_decay", 0.90)
    except Exception:
        pass

    # --- Step 9: Physics-derived reward (active set only) ---
    self._compute_physics_reward(dphi, compute_list)

    # --- Step 10: Findings for telemetry ---
    self.findings.update({
        "active_count": len(active_set),
        "warm_count": len(warm_set),
        "cold_count": N - len(compute_set),
        "compute_fraction": len(compute_set) / max(1, N),
    })
```

### Notes on the new step():

1. **walker_events and trail_scores are passed in.** The walker system runs in
   CoreEngine.step() BEFORE connectome.step(). The engine passes walker output
   to the connectome. This preserves the existing separation of concerns —
   walkers are read-only against the connectome, connectome receives their
   reports.

2. **The catch-up in Step 1 uses analytical formulas.** For a node in a
   double-well with no external drive, exponential relaxation toward the
   nearest well is exact. For bonds, same. The `round()` to find the nearest
   well works because φ and ψ are both in double-wells on [0,1] with minima
   at 0 and 1.

3. **The node field computation in Step 2 uses per-node RNG calls** instead of
   the vectorized numpy call in v8. This is necessary because we're only
   computing a subset of nodes. Could be optimized with masked operations for
   the numpy path.

4. **The old _void_traverse (Step 11 in v8) is removed.** The walker system
   replaces it entirely. _void_traverse was a simplified walker embedded
   directly in the connectome. The cortex/ walker system is its replacement.

### 4.5 — `_remove_dead_edges()` — Modified for active set

```python
def _remove_dead_edges(self, compute_nodes: np.ndarray = None):
    """
    Remove edges whose bond field ψ has fallen below the emergent bond
    noise floor. Only checks nodes in compute_nodes (or all if None).
    """
    from .void_dynamics_adapter import ETA_BOND_FLOOR
    nodes = range(self.N) if compute_nodes is None else compute_nodes
    for i in nodes:
        i = int(i)
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

### 4.6 — `_propose_from_trails()` — Walker-trail edge proposal

This replaces `_propose_new_edges()` entirely. No BFS. No h_causal.
```python
def _propose_from_trails(self, walker_events: list, phi_dot_abs: np.ndarray):
    """
    Propose new edges between co-active nodes observed by the same walker.

    Two mechanisms, both bounded by what the walker can directly see:

    1. edge_on: Walker traverses existing edge (u, v). If u and v are both
       active and NOT already adjacent, propose u ↔ v. This is the only
       legitimate 2-hop mechanism — the walker physically traversed the
       path, so u and v are within each other's causal cone by construction.
       Cost: O(1) per edge_on event.

    2. vt_touch: Walker is at node i. It observes i and all of adj(i) —
       the 1-hop ego-network. Among those visible nodes, any co-active pair
       (j, k) that are neighbors of i but not neighbors of each other is a
       triangle-completion candidate. The walker revealed that j and k are
       both coupled to i and both active — a shortcut j ↔ k may be
       thermodynamically favored.
       Cost: O(k̄) per vt_touch event (one scan of i's neighbors).

    The walker does NOT see around corners. A node 2 hops away that the
    walker has not visited is outside its observation cone. Proposing bonds
    to unvisited nodes would violate CF09 (gauge boson mediates interaction).

    Source: CF09 (gauge boson mediates interaction), CF04 (causal cone from
    traversal), CF07 (nucleation at ψ = 0.0).

    Scaling: With W walkers × h hops = ~768 touches/tick and ~768 edge_on
    events/tick, total proposal cost is O(W·h·k̄) ≈ 768 × 20 = ~15,000
    pair checks per tick. Linear in k̄, not quadratic.
    """
    if not walker_events:
        return

    kT = self.kT
    proposed = set()

    for ev in walker_events:
        kind = getattr(ev, "kind", None)

        if kind == "edge_on":
            # Walker traversed from u to v — both in causal cone
            u = int(getattr(ev, "u", -1))
            v = int(getattr(ev, "v", -1))
            if u < 0 or v < 0 or u >= self.N or v >= self.N:
                continue
            if phi_dot_abs[u] <= kT or phi_dot_abs[v] <= kT:
                continue

            # Direct: u—v not connected?
            if v not in set(self.adj[u].tolist()):
                pair = (min(u, v), max(u, v))
                if pair not in proposed:
                    self._nucleate_bond(u, v)
                    proposed.add(pair)

        elif kind == "vt_touch":
            # Walker is at node i — can see i and adj(i), nothing further
            i = int(getattr(ev, "token", -1))
            if i < 0 or i >= self.N:
                continue
            if phi_dot_abs[i] <= kT:
                continue

            nbrs = self.adj[i]
            if nbrs.size < 2:
                continue

            # Triangle completion: find co-active neighbor pairs (j, k)
            # that are both neighbors of i but not neighbors of each other.
            # The walker can see both j and k from where it stands.
            active_nbrs = []
            for j in nbrs:
                j_int = int(j)
                if phi_dot_abs[j_int] > kT:
                    active_nbrs.append(j_int)

            if len(active_nbrs) < 2:
                continue

            # For each active neighbor j, check if other active neighbors
            # of i are in j's adjacency. If not → propose.
            # Build neighbor sets once per touch for the active subset.
            for idx_a in range(len(active_nbrs)):
                j = active_nbrs[idx_a]
                j_set = set(self.adj[j].tolist())
                for idx_b in range(idx_a + 1, len(active_nbrs)):
                    k = active_nbrs[idx_b]
                    if k not in j_set:
                        pair = (min(j, k), max(j, k))
                        if pair not in proposed:
                            self._nucleate_bond(j, k)
                            proposed.add(pair)
```

### Why 1-hop ego-network, not 2-hop scan:

The walker is the gauge boson (CF09). Its observation cone is the set of nodes
it has physically visited or can directly see from its current position. At node
i, the walker sees i and adj(i). It does NOT see adj(adj(i)) — those nodes are
behind a corner the walker hasn't turned.

The previous 2-hop scan (for each neighbor j, scan j's neighbors k) had the
walker proposing bonds to nodes it hadn't observed. This violated the causal
cone principle: if the walker didn't go to k, k is not in the walker's light
cone. The `edge_on` handler already covers the legitimate case where a walker
traverses a path and discovers unconnected endpoints.

Triangle completion within the 1-hop ego-network is the correct operation: the
walker observes that j and k are both active and both coupled to i, but not to
each other. The shortcut j ↔ k is a candidate that the dynamics will accept or
reject via the bond potential. Cost: O(k̄) per touch, linear in mean degree.

### 4.7 — `_compute_physics_reward()` — Active-set scoped

```python
def _compute_physics_reward(self, dphi: np.ndarray, compute_nodes: np.ndarray):
    """
    Physics-derived reward observables computed over the active set only.
    Cold nodes contribute nothing (their dphi = 0, their bonds are frozen).

    Source:
      Energy dissipation rate (−dH/dt): CF01 §4.2, CF02 §4.2
      Fisher speed: CF06 §4.3
      Entropy production rate: CF02 §4.2
    """
    # Energy: H[φ] = Σ_edges D·ψ_ij·(φ_i−φ_j)² + Σ_nodes V(φ_i)
    # Computed over active edges only (at least one endpoint in compute_set)
    compute_set = set(int(x) for x in compute_nodes)
    E_gradient = 0.0
    for i in compute_nodes:
        i = int(i)
        nbrs = self.adj[i]
        for ki, j in enumerate(nbrs):
            j = int(j)
            if j > i and j in compute_set:
                E_gradient += self.D * float(self.psi_curr[i][ki]) * \
                    (self.phi_curr[i] - self.phi_curr[j]) ** 2

    E_potential = float(np.sum(
        self.lam * self.phi_curr[compute_nodes]**2 *
        (1.0 - self.phi_curr[compute_nodes])**2
    ))
    H = E_gradient + E_potential

    H_prev = getattr(self, '_last_H', H)
    dH_dt = H - H_prev
    self._last_H = H

    # Fisher speed over active set
    eps = 1e-6
    active_dphi = dphi[compute_nodes]
    active_phi = self.phi_curr[compute_nodes]
    fisher_speed = float(np.sqrt(np.sum(
        active_dphi**2 / np.maximum(active_phi, eps)
    )))

    # Entropy over active set
    phi_c = np.clip(active_phi, eps, 1.0 - eps)
    S = float(-np.sum(phi_c * np.log(phi_c) + (1.0 - phi_c) * np.log(1.0 - phi_c)))
    S_prev = getattr(self, '_last_S', S)
    dS_dt = S - S_prev
    self._last_S = S

    boundary_flux = float(np.sum(np.abs(active_dphi)))

    # Store for telemetry
    self._reward_H = float(H)
    self._reward_dH_dt = float(dH_dt)
    self._reward_fisher_speed = float(fisher_speed)
    self._reward_S = float(S)
    self._reward_dS_dt = float(dS_dt)
    self._reward_boundary_flux = float(boundary_flux)

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

4.9 — Walker System Integration

### Existing infrastructure (preserved unchanged)

The `cortex/` directory contains a complete walker system that runs through
`CoreEngine.step()`. This system is NOT modified by the migration. It
continues to:

1. Dispatch scouts via `run_scouts_once()` with per-tick time budgets
2. Scouts traverse the connectome read-only, emitting vt_touch and edge_on events
3. Events fold into maps (HeatMap, ColdMap, TrailMap, ExcitationMap, etc.)
4. Map snapshots inform the global system and next tick's walker routing

### New integration point

The migration adds ONE new connection: walker events and trail scores are
passed from `CoreEngine.step()` into `connectome.step()`:

```
CoreEngine.step(dt_ms, ext_events):
    # 1. Run scouts (existing, unchanged)
    walker_events = run_scouts_once(connectome, scouts, maps, budget)

    # 2. Fold events into maps (existing, unchanged)
    for map in [heat_map, cold_map, trail_map, ...]:
        map.fold(walker_events, tick)

    # 3. Extract trail scores for computation gating (NEW)
    trail_snapshot = trail_map.snapshot()
    trail_scores = {node: score for node, score in trail_snapshot.get("trail_dict", {}).items()}

    # 4. Connectome step with walker data (MODIFIED call)
    connectome.step(tick=tick, walker_events=walker_events, trail_scores=trail_scores)
```

### What walkers observe

When a walker visits a node, it reads φ_curr (the node field) and reports what
it finds. If the node was cold and just got caught up, the walker observes the
post-catch-up state. If the node's φ changed significantly during the gap
(rare for cold nodes, but possible at boundaries), the walker's vt_touch
event carries that information to the bus.

The **global system** sees the shape of activity through the bus — which regions
are active, where boundaries are forming, what the territory structure looks
like. It derives meaning from the spatial pattern of walker reports, NOT from
direct inspection of the field. This is correct: the global system's knowledge
of the connectome is exactly what the walkers have reported. Unvisited regions
are invisible.

### Walker types and their roles post-migration

| Scout | Pre-migration role | Post-migration role |
|-------|-------------------|---------------------|
| VoidRayScout | Route along φ gradients | Same — φ gradients now include bond-weighted dynamics |
| HeatScout | Route toward recent activity | Same — now also drives computation allocation |
| ColdScout | Route toward unvisited regions | **Critical:** ensures eventual coverage of cold nodes |
| CycleHunterScout | Detect topological loops | Same — loops in persistent topology are more meaningful |
| FrontierScout | Explore graph boundary | Same — persistent topology has more stable boundaries |
| SentinelScout | Monitor structural integrity | Same — bond death/birth provides richer structural signal |
| MemoryRayScout | Route using slow memory field | Same |

**ColdScout is especially important post-migration.** With walker-gated
computation, cold regions are truly uncomputed. ColdScout ensures walkers
periodically visit neglected regions, preventing permanent blindspots. This is
the "what if something interesting happened there?" mechanism — biologically
analogous to spontaneous attention shifts, default-mode network activation, or
the mind wandering to check on unattended concerns.

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

```python
# walker_events and trail_scores populated from engine's cortex step
nx.connectome.step(
    tick=step,
    walker_events=walker_events,
    trail_scores=trail_scores,
)
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

```python
def step_connectome(self, tick: int, walker_events: list = None, trail_scores: dict = None) -> None:
    try:
        self._nx.connectome.step(
            tick=int(tick),
            walker_events=walker_events or [],
            trail_scores=trail_scores or {},
        )
    except Exception:
        pass
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
def step_connectome(self, tick: int, walker_events: list = None, trail_scores: dict = None) -> None:
    try:
        self._nx.connectome.step(
            tick=int(tick),
            walker_events=walker_events or [],
            trail_scores=trail_scores or {},
        )
    except Exception:
        pass
```

This must match the integration point in §4.9: the engine extracts walker events
and trail scores from the cortex system and passes them through to the connectome.
Without this passthrough, walker-gated computation (§0.6) is dead on arrival.

---

## 9. UTED — Output Boundary Transduction

### 9.1 Physics-Clock Timestamps

In `vdm_rt/io/uted/ute_mux.py`, all adapters:
```python
from vdm_rt.core.void_dynamics_adapter import TAU, GAMMA
import numpy as np

# In every adapter's poll_frames():
dt_physical = float(np.sqrt(TAU / GAMMA))  # dimensionless ticks → seconds-equivalent
timestamp_us = int(tick * dt_physical * 1_000_000)
# NOT time.time_ns() // 1000
```

`HeartbeatAdapter` emits one frame per tick. No wall-clock rate limiting.
Wall-clock time may be stored in a separate `wall_us` field for debugging
but must NOT be in `timestamp_us`.

### 9.2 Principle: Output Nodes as Neuromuscular Junction

The UTD does not observe the connectome globally. It observes a
designated set of **output nodes** — a fixed region of the graph that
serves as the motor boundary. This is an initial condition (anatomy),
not a learned behavior.

The mapping is:
```
[territory dynamics] → [walker-mediated bond routes] → [output nodes] → [UTD adapter] → [actuator]
     (emergent)              (emergent)                 (fixed IC)       (fixed wiring)    (external)
```

The output nodes do not change position, meaning, or connectivity rules.
They participate in the same Klein-Gordon + bond field dynamics as every
other node. What makes them "output" is solely that the UTD adapter
reads their state. This is analogous to motor neurons: they obey the
same electrochemistry as every other neuron; what makes them "motor" is
that their axons terminate on muscle fibers.

The model does not know what the output nodes do. It does not know what
language the actuator speaks. It discovers through reinforcement that
certain activation patterns at the output boundary correlate with
environmental responses that propagate back through the UTE. Over time,
walker routes and bond strengths develop between internal territories and
the output region, producing coherent, territory-specific output.

### 9.3 Output Node Specification

Output nodes are designated at initialization, analogous to how input
nodes are designated by the UTE lexicon-to-index mapping.
```python
# In sparse_connectome.__init__, after graph initialization:

# Output region: fixed set of node indices for each actuator channel.
# These are initial conditions (anatomy), not tuning parameters.
# Size is configurable at init like k_init and N.
self.output_regions: dict[str, np.ndarray] = {}

# Example: speech output = first n_speech nodes
# Motor output = next n_motor nodes
# Visual output = next n_visual nodes
# The specific allocation is set by the UTED port configuration.
```

Port configuration in UTED:
```python
# In ute_mux.py or port config:
PORTS = {
    "speech": PortSpec(
        output_nodes=range(0, 64),       # which nodes this adapter reads
        poll_interval=1,                   # every tick
        pattern_decoder="token_softmax",   # how to decode activation → tokens
    ),
    # Future actuators:
    # "motor": PortSpec(output_nodes=range(64, 128), ...),
    # "visual": PortSpec(output_nodes=range(128, 192), ...),
}
```

### 9.4 UTD Readout: Local Observation Only

The UTD speech adapter reads the field state at its designated output
nodes and decodes it into tokens. It does NOT:

- Drain the global bus
- Access `void_topic_symbols` from all territories
- Read `tick_rev_map` for the full graph
- Inspect territory structure or walker reports

It reads `phi_curr[output_nodes]` and the symbol mappings for those
specific nodes. That is all.
```python
class SpeechOutputAdapter:
    """
    Reads output node activation patterns and decodes to token sequences.

    The adapter is a fixed transduction boundary. It converts whatever
    activation pattern appears at its output nodes into the actuator's
    native format (text tokens). It has no knowledge of territories,
    walkers, or internal dynamics.
    """

    def __init__(self, output_nodes: np.ndarray, index_to_symbol: dict):
        self.output_nodes = output_nodes
        self.index_to_symbol = index_to_symbol  # node index → token/symbol

    def read(self, phi_curr: np.ndarray, phi_prev: np.ndarray,
             kT: float) -> str | None:
        """
        Read the output region and decode to text if the pattern is
        above thermal noise.

        Returns None if output nodes are quiescent (nothing to say).
        Returns a token string if a coherent pattern is present.
        """
        phi_out = phi_curr[self.output_nodes]
        phi_dot = np.abs(phi_curr[self.output_nodes] - phi_prev[self.output_nodes])

        # Are the output nodes active? (above thermal noise floor)
        active_mask = phi_dot > kT
        if np.sum(active_mask) < 2:
            return None  # silence — default state

        # Which output nodes are driven toward φ=1 (activated)?
        # Nodes near well φ=1 with recent activity are "firing"
        firing = active_mask & (phi_out > 0.5)
        if np.sum(firing) == 0:
            return None

        # Decode: map firing output nodes to their symbols
        # Ordered by activation strength (strongest first)
        firing_indices = self.output_nodes[firing]
        strengths = phi_out[firing]
        order = np.argsort(-strengths)

        tokens = []
        for idx in firing_indices[order]:
            sym = self.index_to_symbol.get(int(idx))
            if sym is not None:
                tokens.append(sym)

        if not tokens:
            return None

        return " ".join(tokens)
```

### 9.5 What Emerges (Not Engineered)

The following behaviors are NOT specified by this section. They must
emerge from the Klein-Gordon + bond field + walker dynamics:

1. **Selective output routing.** Which territory develops strong bonds
   to the output region is determined by reinforcement. Territories
   whose output patterns correlate with rewarding UTE input develop
   stronger walker routes and bond strengths to output nodes.

2. **Gating / serialization.** When two territories compete for the
   output nodes, the bond-weighted Laplacian coupling and double-well
   potential naturally resolve the competition. The territory with
   stronger bonds and more coherent drive wins — the output nodes
   settle into that territory's pattern. The other territory's signal
   is attenuated by weaker bonds. This is competitive disinhibition
   via circuit dynamics, not an engineered gate.

3. **Developmental progression.** Early in training:
   - Output nodes receive diffuse, incoherent drive (crying/noise)
   - Occasional coherent fragments appear (babbling)
   - Reinforced pathways strengthen (first words)
   - Multiple territory→output routes mature (vocabulary)
   - Competitive dynamics at output nodes produce clean serialized
     output (sentences)

4. **Silence as default.** If no territory is driving the output nodes
   above thermal noise, the adapter returns None. Silence is not a
   gate closing — it is the absence of coherent drive reaching the
   output boundary. The model must actively drive the output to speak.

5. **Modal universality.** The same mechanism works for any actuator.
   Wire a motor adapter to a different output region. The model
   discovers what that region does through exploration and
   reinforcement. The internal representations are modality-agnostic
   — the model develops whatever encoding works for driving each
   output region effectively.

### 9.6 Eliminated Mechanisms

After this migration, the following are removed from the speech path:

| Eliminated | Reason |
|---|---|
| Global bus drain for speech composition | UTD reads output nodes only |
| `void_topic_symbols` aggregation | Symbols come from output node mappings only |
| `b1_spike` as speech gate | Gating emerges from bond dynamics at output boundary |
| `should_speak(valence, spike, thresh)` | No engineered gate; silence = no coherent drive |
| `speak_valence_thresh` | No threshold; thermal noise floor is the only cutoff |
| `maybe_auto_speak()` as global aperture | Replaced by `SpeechOutputAdapter.read()` |
| `compose_say_text()` with global symbol set | Composer receives only output-node symbols |

The `StreamingZEMA` b1 detector may be retained as a telemetry-only
observable. It must not gate any actuator output.

### 9.7 What Remains for Engineering vs. Emergence

| Aspect | Specified (IC/anatomy) | Emergent |
|---|---|---|
| Which nodes are output nodes | ✓ (port config) | |
| How many output nodes per actuator | ✓ (port config) | |
| Pattern → token decoding | ✓ (adapter wiring) | |
| Which territories connect to output | | ✓ (bond dynamics) |
| When the model speaks | | ✓ (output node activation) |
| What the model says | | ✓ (territory→output patterns) |
| Speech timing and rhythm | | ✓ (walker route dynamics) |
| Vocabulary development | | ✓ (reinforcement of output pathways) |
| Gating / turn-taking | | ✓ (competitive dynamics at output nodes) |
| Internal→output encoding | | ✓ (model develops its own language) |

### 9.8 Integration with Walker-Gated Computation

Output nodes follow the same Zone 1/2/3 rules as all other nodes
(Section 0.6). A walker must visit the output region for those nodes
to be computed. If no walker visits the output nodes, they are cold,
the adapter reads quiescent state, and the model is silent.

This means the model must learn to route walkers to the output region
as part of learning to speak. ColdScout will occasionally visit
neglected output nodes (ensuring the model doesn't permanently forget
the output exists), but sustained, coherent output requires the model
to develop intentional walker routing — which is exactly the
attention-to-articulation pathway.

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
- [ ] `pos` as a stored state array (no spatial embedding exists)
- [ ] `self.pos` in any file under `vdm_rt/core/`
- [ ] `self._side` or `side` as a grid dimension attribute
- [ ] `_build_cubic_adjacency` as a method definition
- [ ] `||pos[i]` or `np.linalg.norm(self.pos` (Euclidean distance on node positions)
- [ ] `r_causal` as a float Euclidean radius (replaced by `h_causal` integer hops)
- [ ] `side * side` or `side2` as cubic index arithmetic
- [ ] - [ ] `h_causal` as a stored state array
- [ ] `_h_causal_frac` as a stored accumulator
- [ ] `_void_traverse` as a method in sparse_connectome (replaced by cortex/ walkers)
- [ ] `_build_alias` called from within `step()` (alias sampling was for _void_traverse and global topology rebuild)

---

## 12. Validation Gates (run 50,000 ticks, N=1000, k_init=12)

All must pass or the migration is rejected:

1. **No NaN:** `np.any(np.isnan(phi_curr))` is never True at any tick.
2. **Field bounded:** `phi_curr ∈ [0.0, 1.0]` every tick.
3. **Bimodal distribution:** At tick 50000, histogram of `phi_curr` has two peaks: `count(φ < 0.2) > 0.2·N` AND `count(φ > 0.8) > 0.2·N`.
4. **Causal propagation:** Inject stimulus at node i at tick T. Measure first tick at which
   a walker reports φ_j > threshold at node j (graph distance d hops from i). Delay ≥
   `d / max_walker_speed` where max_walker_speed is bounded by the walker hop budget per
   tick. Test 10 random pairs with graph distance d ∈ [3, 10]. Note: information cannot
   propagate faster than walkers can carry it.
5. **Energy non-increase:** Compute H every 100 ticks. Over any 1000-tick window, H must not increase by more than 5% of its starting value.
6. **Gini coefficient:** At tick 50000, Gini of `phi_curr` ≥ 0.45.
7. **Bond persistence:** Mean bond lifetime (ticks a bond persists with ψ > 0.5 before dropping below the bond noise floor $\sqrt{2 \cdot \varepsilon_{topo} \cdot kT}$) > 500 ticks. The telegraph inertia τ_bond = τ/ε_topo = 200 provides this naturally.
8. **Bond locality:** Every bond created during the run was proposed by a walker event
   (edge_on or 2-hop from vt_touch). No bond exists between nodes that no walker has
   connected via traversal. Verify by logging all bond creation events with their
   originating walker event.
9. **Eliminated proxies:** grep check (Section 11) passes with zero hits.
10. **Bond field non-trivial:** At tick 50000, `count(ψ > 0.5) > 0.5 · total_edges` AND `count(ψ < 0.1) > 0`.
11. **Per-tick cost:** Mean wall-clock time per tick ≤ 3x the time for a single `klein_gordon_rhs()` call (bond update overhead is bounded).
12. **No debt overflow:** `np.any(np.isinf(self.debt))` is never True. `np.max(self.debt) < 500` at tick 50000 (self-limiting via exponential friction).
13. **Computation sparsity:** At tick 50000, the mean compute_fraction (|compute_set|/N)
    over the last 1000 ticks is < 0.5. The walker-gated model should not be computing
    the entire graph — if it is, the gating is not working.
14. **Output locality:** The `SpeechOutputAdapter.read()` function
    accesses ONLY `phi_curr[output_nodes]` and `phi_prev[output_nodes]`.
    Grep confirms no reference to global bus drain, void_topic_symbols,
    or tick_rev_map in the speech output path.
15. **Developmental silence:** At tick 0 with randomized initial bonds,
    the output nodes are not yet coherently driven but should be left for the model to route signal to in order to learn.

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
| `R_NUCLEATION = 4.0` (fixed spatial cutoff) | Causal horizon h_causal(i) grows from dynamics in graph hops | CF04 §4.2: finite propagation speed → causal cone on graph topology |
| `debt_max = 10.0` (ceiling clamp) | Self-limiting via exp(β·debt) asymptotic freeze | CF03 §7.2: throttling is exponential, not clamped |
| `dt_physics_us = 6324555` (pre-computed integer) | `√(τ/D)` computed symbolically at I/O boundary | CF04 §7.1: dimensional analysis, not magic numbers |
| **`PSI_DEATH = 1e-6`** (arbitrary float threshold) | Dynamic thermal noise floor **$\eta_{bond} = \sqrt{2 \cdot \varepsilon_{topo} \cdot kT}$** | **CF07 §4.1 & §4.2**: Epistemic projection; classical reality is bounded by finite resolution limits. |
| **`PSI_SEED = 0.01`** (arbitrary spawn value) | Natural nucleation from **$\psi = 0.0$** via metriplectic integration | **CF07 §4.1**: Classical boundaries emerge from natural forces, forbidding artificial state injection. |

---

**END OF DIRECTIVE v8**
