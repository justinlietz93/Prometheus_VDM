# Runtime Physics Migration Directive v8 — FINAL CONSOLIDATED

**Author:** Justin K. Lietz  
**Date:** 2026-02-28  
**Status:** FINAL — Consolidated Patch Set Applied  
**Replaces:** ALL previous versions (v3, v4, v7, v8 draft)  
**Scope:** Complete migration from proxy heuristics to physics-derived runtime.  

**Rule:** No lookup tables. No artificial toggles. No wall-clock timestamps in the physics path. No hardcoded timescales, thresholds, patience counters, or spatial cutoffs. Every parameter is either a material constant of the lattice (τ, λ, D, kT, β, ε_bond) or emerges from the dynamics of those constants. Every instruction in this document is literal. If it says "delete," delete it. If it says "replace," replace every instance. If a function signature is specified, that is the exact signature. Codex must not invent parameters, add toggles, or introduce fallback paths.

**What changed from v3 and why:** v3 hardcoded seven non-emergent quantities: `TOPO_PERIOD=50` (cron timer), `TOPO_THRESHOLD=0.01` (eligibility gate), `TOPO_PATIENCE=100` (debounce counter), `tau_e=250` (eligibility decay), `R_NUCLEATION=4.0` (spatial cutoff), `debt_max=10.0` (ceiling clamp), `dt_physics_us=6324555` (pre-computed conversion). All seven violate the CF chain. CF01 §4.1 says `dF/dt = {F,H}_J + (F,S)_M` — both terms, every tick, for every degree of freedom. CF02 §4.1-4.3 says timescale separation comes from operator structure (coupling constants), not from scheduling. CF04 §4.2 says the causal cone grows from the dynamics. v8 replaces all seven with one new material constant `ε_bond = 200` (bond telegraph inertia from extended action) and a bond field `ψ_ij` that evolves under the same Klein-Gordon equation with heavier mass. Topology becomes a degree of freedom, not a cron job.

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
= D · (L_ψ φ)_{n,i} − V'(φ_{n,i})
```

Where:
- `φ_{n,i}` is the scalar field at node `i`, tick `n`. Range [0, 1].
- `τ_eff(i) = τ · exp(β · debt_i)` — debt-throttled relaxation time (per-node).
- `dt = 1.0` — one tick = one physics timestep (dimensionless).
- `D` — diffusion coefficient (= c²/γ, related to J and γ by CF-derived relationships).
- `(L_ψ φ)_i = Σ_{j ∈ adj(i)} ψ_ij · (φ_j − φ_i)` — bond-weighted graph Laplacian on the connectome topology. A fully formed bond (ψ=1) contributes full coupling. A dissolving bond (ψ→0) contributes decreasing coupling. This replaces the binary adjacency of v3. The Laplacian is defined on whatever adjacency structure the graph currently has — it does not require or assume a spatial embedding.
- `V(φ) = λ · φ²(1 − φ)²` — Ginzburg-Landau double-well on [0, 1].
- `V'(φ) = 2λ · φ(1 − φ)(1 − 2φ)` — potential derivative.
- No injected noise. The J-limb (telegraph inertia τ·φ̈) and M-limb (friction φ̇) fight on the same field. Their interaction with the tachyonic double-well and Laplacian coupling produces endogenous fluctuations from N coupled nonlinear oscillators on a self-modifying graph. kT is measured from these dynamics via equipartition (CF06 §4.3), not injected.

Rearranging for φ_{n+1} (implicit solve, dt = 1):

```
a_inertia(i) = τ_eff(i)
a_friction   = 1.0
rhs(i)       = D · (L_ψ φ)_i − V'(φ_i)

φ_new(i) = [ rhs(i) + (2·a_inertia(i) + a_friction)·φ_curr(i) − a_inertia(i)·φ_prev(i) ]
            / [ a_inertia(i) + a_friction ]

φ_new(i) = clip(φ_new(i), 0.0, 1.0)
```

#### Bond field equation — derived from extended action

The node field equation comes from varying VDM-AX-004 w.r.t. W_i.
The bond field equation comes from the same action with ψ_ij as a dynamical degree of freedom.

**Extended discrete action:**

    S(W, ψ) = Σ_n Δt Σ_i a^d [
        ½(Δ_t W_i)²
      - ½ Σ_{j∈N(i)} ψ_ij · (W_j - W_i)²
      - V(W_i)
    ] + Σ_n Δt Σ_{(i,j)} [
        ½ ε_bond · (Δ_t ψ_ij)²
      - U_bond(ψ_ij)
    ]

First three lines: VDM-E-011 with ψ_ij weighting the interaction.
Last two lines: bond kinetic + potential energy, ε_bond = bond inertia.

**Vary w.r.t. ψ_ij (Euler-Lagrange for bonds):**

    ε_bond · (ψ_{n+1} − 2ψ_n + ψ_{n-1}) / Δt²
        = −U'_bond(ψ_ij) + ½(W_j^n − W_i^n)²

The source term **½(φ_j − φ_i)²** falls out of the variation because ψ_ij multiplies (W_j − W_i)² in the action. Differentiating −½ψ(W_j−W_i)² w.r.t. ψ gives +½(W_j−W_i)².

**Physical meaning:** Bonds form where the field has large spatial gradients — at domain walls. Nodes in the same well have (φ_j−φ_i)² ≈ 0, exerting no force. Nodes straddling a domain wall have (φ_j−φ_i)² ≈ 1, pushing ψ→1. This is NOT Hebbian. The source is gradient (spatial difference), not correlation (temporal coincidence). The mechanism is self-limiting: once the bond condenses, Laplacian coupling D·ψ_ij(φ_j−φ_i) smooths the gradient, reducing the source that formed the bond. Equilibrium without external regulation.

**Add M-limb damping (CF01/CF02):**

    ε_bond · ψ̈_ij + ψ̇_ij = −U'_bond(ψ_ij) + ½(φ_j − φ_i)²

J-limb: ε_bond·ψ̈ (conservative inertia). M-limb: ψ̇ (friction).

**Bond potential:** U_bond(ψ) = λ_bond · ψ²(1−ψ)² (CF03 §1.1 applied to bond DOF). Bonds prefer ψ=0 or ψ=1. Barrier at ψ=0.5.

**Bond potential derivative:** U'(ψ) = 2·λ_bond · ψ(1−ψ)(1−2ψ)

**Full bond RHS:**

    rhs_bond(i,j) = −2·λ_bond · ψ(1−ψ)(1−2ψ) + ½(φ_j − φ_i)²

**Implicit solve (dt = 1):**

    ψ_new = [rhs_bond + (2·ε_bond + 1)·ψ_curr − ε_bond·ψ_prev]
             / [ε_bond + 1]
    ψ_new = clip(ψ_new, 0.0, 1.0)

**Why bonds form without noise:** At ψ=0, U'(0) = 0. The only force is +½(φ_j−φ_i)². Any nonzero gradient pushes ψ positive. Max barrier resistance ≈ 0.192·λ_bond (at ψ≈0.21). For λ_bond = 1.0, the source must exceed ~0.19, requiring |φ_j−φ_i| > 0.62. Domain walls provide this. Away from walls, gradients are small, bonds dissolve.

#### Bond field equation (derived from extended action, see §0.1b):

    ε_bond · (ψ_{n+1,ij} − 2ψ_{n,ij} + ψ_{n-1,ij}) / dt²
    + (ψ_{n+1,ij} − ψ_{n,ij}) / dt
    = −U'_bond(ψ_ij) + ½(φ_j − φ_i)²

Where:
- `ε_bond` — bond telegraph inertia. Free parameter from extended action. Large ε_bond → slow topology.
- `U_bond(ψ) = λ_bond · ψ²(1−ψ)²` — double-well for bond bistability (CF03 §1.1 applied to bond DOF).
- `½(φ_j − φ_i)²` — gradient source from action variation. Bonds form at domain walls where the field has large spatial gradients. NOT activity coupling. NOT Hebbian.
- No noise term. Fluctuations in (φ_j − φ_i)² come from node dynamics.

Bond potential derivative:

    U'_bond(ψ) = 2·λ_bond · ψ(1−ψ)(1−2ψ)

Full RHS:

    rhs_bond(i,j) = −2·λ_bond · ψ(1−ψ)(1−2ψ) + ½(φ_j − φ_i)²

Implicit solve (dt = 1):

    ψ_new(i,j) = [rhs_bond + (2·ε_bond + 1)·ψ_curr − ε_bond·ψ_prev]
                  / [ε_bond + 1]
    ψ_new(i,j) = clip(ψ_new(i,j), 0.0, 1.0)

> **Bond Decoherence and Spinodal Condensation (CF07, §0.1b):**
> Structures physically cease to exist in the observable M-limb when they become indistinguishable from background thermal noise. When a bond's strength falls below the emergent decoherence floor (**$\psi_{ij} < \sqrt{2 \cdot kT / \varepsilon_{bond}}$**, where kT is measured from active-set φ̇ variance via equipartition), the edge is removed from the adjacency list. When a walker (gauge boson, CF09) encounters an unconnected pair with both endpoints observable (|φ̇| > 0, CF07 measurement condition), a bond DOF is instantiated at the unstable vacuum **$\psi_{ij} = 0.0$**. The gradient source ½(φ_j − φ_i)² from the action variation tilts the double-well. At domain walls where ½(Δφ)² exceeds the barrier (~0.192·λ_bond), the ψ=0 minimum ceases to exist and the bond condenses via spinodal decomposition toward ψ=1. Away from domain walls, the source is insufficient and ψ relaxes back to zero, where it is swept by the decoherence floor. No noise. No seeding. The gradient decides.

#### Bond DOF instantiation (replaces TOPO_PERIOD + 2-hop scan)

A bond DOF can only come into existence between nodes that a walker has connected through traversal. The walker IS the causal cone (CF09: gauge boson transport). If a walker has not traversed a path between nodes i and j, no bond DOF exists on edge (i,j).

**Conditions for bond DOF instantiation:**
- Walker has visited both i and j during the same traversal event
- Both endpoints are observable: |φ̇_i| > 0, |φ̇_j| > 0 (CF07 measurement condition — the gauge boson can only interact with nodes that have detectable dynamics)
- Edge (i,j) does not already carry a bond DOF

When all three conditions are met, the bond DOF is instantiated at ψ_ij = 0.0 (unstable vacuum). The telegraph integrator and gradient source ½(φ_j − φ_i)² determine whether the bond condenses or decoheres. There is no evaluation step, no scoring, no acceptance criterion. The walker observes; the dynamics decide.

**Observable ≠ co-active ≠ Hebbian.** The observability condition is a measurement prerequisite (can the gauge boson see this node?), not a force law. The force is the gradient source from the action variation. Nodes in the same state (both φ≈1) are observable but have zero gradient — no bond formation force. Nodes straddling a domain wall have maximum gradient — maximum force. Bonds form at structure boundaries, not between correlated oscillators.

**Cost:** O(N_walkers · h · k̄) per tick, where h is hops per walker and k̄ is mean degree. For W=768, h=3, k̄~20: ~46,000 pair checks. Only active-set nodes participate.

---

### 0.2 Parameters and CF Constraints

#### Free parameters (micro-parameters of the discrete action)

These are independent choices. Different values = different physics. They are constrained by CF-derived relationships but not determined by them. Analogous to choosing N and k_init — initial conditions for a specific run.

| Name | Symbol | Value | Role |
|------|--------|-------|------|
| Nearest-neighbor coupling | J | 0.0125 | Interaction strength in action (VDM-AX-004) |
| GL barrier height (nodes) | λ | 1.0 | Double-well depth: V(φ) = λ·φ²(1−φ)² |
| M-limb damping | γ | 0.5 | Friction coefficient from dissipative bracket |
| Bond telegraph inertia | ε_bond | 200.0 | Bond mass in extended action (sets timescale separation) |
| GL barrier height (bonds) | λ_bond | 1.0 | Bond double-well: U(ψ) = λ_bond·ψ²(1−ψ)² |
| Debt throttle exponent | β_debt | 0.1 | Exponential friction per unit debt |

#### CF-derived quantities (computed, not independently chosen)

Any valid parameter choice must satisfy these. You choose J and γ; everything else follows.

| Quantity | Expression | Value | Source |
|----------|-----------|-------|--------|
| Wave speed² | c² = 2Ja² | 0.025 | VDM-AX-C02, VDM-E-014 |
| Diffusion coefficient | D = c²/γ | 0.05 | VDM-E-050 |
| Telegraph relaxation | τ = 1/γ | 2.0 | CF04 §2.1 (Cattaneo) |
| Signal speed | c = √(D/τ) | 0.158 hops/tick | CF04 §3.1 |
| Bond relaxation | τ_bond = ε_bond·Δt² | 200 ticks | Extended action (§0.1b) |
| Effective temperature | kT = ½·Var(φ̇) | measured | CF06 §4.3 (equipartition) |
| Decoherence floor | η = √(2·kT/ε_bond) | measured (dynamic) | CF07 §4.1 |

Note: The old table listed `D (= γ) = 0.05`. D ≠ γ. D is diffusion (0.05), γ is damping (0.5). The relationship D = c²/γ = 2Ja²/γ connects them. Choosing J and γ determines D, τ, c, and everything else. They cannot be chosen independently.

#### Why these specific numbers

- τ = 2.0 → telegraph oscillations ring ~2 ticks before damping dominates (underdamped regime, interesting dynamics)
- c ≈ 0.16 hops/tick → information crosses 10 hops in ~63 ticks (walker budget of 3 hops/tick is ~19× faster, consistent with CF09)
- τ_bond = 200 → bonds change ~100× slower than field (timescale separation for topology vs activity)
- D = 0.05 → CFL number D·Δt/a² = 0.05 (stable, well within CFL < 0.5)

These are chosen for the N=1000 runtime. Different N or deployment target may need different values. The CF relationships must still hold.

### 0.3 Eliminated Constants (must not appear anywhere after migration)

`F_REF`, `PHASE_SENS`, `ALPHA` (as reaction rate), `BETA` (as separate decay rate in GDSP), `domain_modulation`, `use_time_dynamics`, `kappa` (as separate from D), `TOPO_PERIOD`, `TOPO_THRESHOLD`, `TOPO_PATIENCE`, `R_NUCLEATION`, `tau_e`, `debt_max`, `dt_physics_us`, `DEBT_MAX`, `PSI_DEATH`, `PSI_SEED`, `pos` (spatial embedding array), `r_causal` (Euclidean causal radius — replaced by walker trail reachability), `side` (cubic grid dimension), `_build_cubic_adjacency` (cubic lattice initialization — replaced by graph initialization).
`h_causal` (per-node causal horizon — replaced by walker trail reachability), `_h_causal_frac` (fractional hop accumulator — eliminated with h_causal), `MAX_BFS_DEPTH` (never needed — walkers replace BFS).

### 0.4 Compute, Memory, and Scaling

#### DEVICE NEUTRALITY CONSTRAINT

The fast path MUST NOT assume a single address space, a single execution device, or synchronous execution order between independent operations.

Specifically:

1. The bond-weighted Laplacian, the pointwise node solve, the bond solve, and the debt update are independent operations on the same tick's data. They MUST NOT be fused into a single function that requires all to execute on the same device.

2. All state arrays (phi_curr, phi_prev, debt, adj, psi_curr, psi_prev) MUST be stored in standard contiguous array formats (numpy ndarray, or equivalent) that can be copied to any device buffer without reshaping or reinterpretation.

3. The step() function MUST NOT call time.time(), time.time_ns(), threading primitives, or device-specific APIs. It operates on arrays and returns arrays. Device dispatch is the caller's responsibility.

#### Why this architecture scales

The current runtime rebuilds the **entire adjacency** from scratch every tick: allocate N empty sets, draw O(s) alias samples per node, score every pair, symmetrize, prune, bridge, freeze into sorted arrays. Cost: **O(N · s) per tick** where s is the sample count (default 64). For N = 256 this is fine. For N = 1,000,000 it is 64 million operations per tick just for topology, before the field update even runs.

This is also physically wrong. The universe does not globally recompute which particles are adjacent every Planck time. Topology (which nodes are coupled) is persistent state that evolves slowly and locally, driven by the field dynamics.

The physics-derived architecture has ONE cost regime — everything runs every tick with different coupling strengths:

**Every tick: field + bond update — O(N · k)**

| Operation | Cost | Why |
|-----------|------|-----|
| Bond-weighted Laplacian `Σ_j ψ_ij(φ_j − φ_i)` | O(N · k) | One pass over adjacency; k = mean degree |
| Potential derivative `V'(φ)` | O(N) | Pointwise polynomial per node |
| Telegraph solve (nodes) | O(N) | Pointwise division per node |
| Bond potential derivative `∂U_bond/∂ψ` | O(N · k) | One pass over edges |
| Bond telegraph solve | O(N · k) | Pointwise per edge |
| Activity `|φ̇|` computation | O(N) | Pointwise |
| Debt update | O(N) | Pointwise |
| Edge condensation/decoherence | O(N_events) | Sparse: only edges crossing the decoherence floor or newly instantiated bond DOFs |

**Total: O(N · k̄) per tick** where k̄ is the emergent mean degree of the connectome. For k̄ = 20 and N = 1,000,000 this is ~40M operations per tick (Laplacian + bond update are each O(N·k̄)). For k̄ = 20 and N = 100,000,000 this is ~4B — still tractable with vectorized numpy or GPU dispatch.

**Bond DOF instantiation: O(N_active · w)** where w is the mean walker trail length per node. Walker traversal histories define the set of reachable pairs within the causal cone, eliminating BFS graph-distance computation. Active-set nodes only (|φ̇| > 0). Bounded by walker budget.

**Comparison to current architecture:**

| Architecture | Per-tick cost | Topology persistence | Causal structure |
|---|---|---|---|
| Current (global rebuild) | O(N · 64) | None — rebuilt from scratch | Violated |
| Physics-derived (bond field) | O(N · k̄), k̄ emergent | Persistent — bonds carry forward | Preserved — causal cone (walker traversal) |

**The physics-derived architecture is ~10x cheaper per tick AND physically correct.**

#### Memory cost

| Array | Size | Dtype | Bytes (N=1M, k̄=20) |
|-------|------|-------|---------------------|
| `phi_curr` | N | float32 | 4 MB |
| `phi_prev` | N | float32 | 4 MB |
| `debt` | N | float64 | 8 MB |
| `psi_curr` | N · k̄ | float32 | 80 MB |
| `psi_prev` | N · k̄ | float32 | 80 MB |
| `adj` | N · k̄ | int32 | 80 MB |
| `W` (alias to phi_curr) | 0 | — | 0 |
| `last_visit` | N | int32 | 4 MB |
| `frozen_phi` | N | float32 | 4 MB |

**Total: ~264 MB for N = 1,000,000 with k̄ = 20.**

Note: `pos` array is eliminated. There is no spatial embedding. Adjacency is defined by graph topology, not Euclidean coordinates.

#### Scaling law

```
T_tick = a · W · k̄
```

Where W is the size of the active + warm set, not N. Linear in the number of nodes receiving attention this tick. The physics per node is unchanged — same Klein-Gordon, same bond update. Only the count of nodes computed changes.

Linear in N for fixed k̄. The mean degree k̄ is determined by the dynamics, not fixed by geometry. In practice, mean degree has been observed to stabilize in the range 15–25 for runs from N=1,000 to N=10,000. Whether k̄ scales with N is an empirical question — if k̄ = O(1), scaling is linear; if k̄ = O(log N), scaling is O(N log N), still tractable.

### 0.5 Topology and Manifold Structure

The discrete manifold is the connectome graph itself. Nodes have no fixed spatial embedding. There is no coordinate grid, no position array, and no Euclidean distance metric. The adjacency structure IS the geometry. All notions of "distance," "locality," and "neighborhood" are defined in terms of graph hops along existing edges.

**Initial connectivity:** k-regular random graph or preferential attachment, matching the existing runtime initialization parameter `k_init`. The initial degree distribution and graph structure are initial conditions, analogous to the initial field configuration φ(t=0). The value of `k_init` is a free parameter (initial condition), not a material constant.

**N is unconstrained.** Any positive integer. No cube requirement, no grid constraint.

**No pos array.** Node spatial positions are not defined, not stored, and not referenced by any physics equation. The bond-weighted Laplacian, the Klein-Gordon solver, the bond field equation, the decoherence threshold, and the causal cone constraint are all defined on the graph topology and do not require spatial coordinates. If a spatial embedding is needed for visualization, it is computed from the graph Laplacian spectrum (Fiedler layout) at render time and is NOT stored as simulation state.

**Topology evolution.** The graph self-modifies through two mechanisms:
1. **Bond decoherence:** When ψ_ij drops below the decoherence floor √(2 · kT / ε_bond), the edge is removed from the adjacency list (CF07).
2. **Bond condensation:** When a walker (gauge boson, CF09) encounters an unconnected pair with both endpoints observable (|φ̇| > 0), a bond DOF is instantiated at the unstable vacuum ψ = 0.0. The gradient source ½(φ_j − φ_i)² drives spinodal condensation at domain walls (§0.1b). Away from domain walls, the bond decoheres.

This produces a self-modifying scale-free topology with emergent degree heterogeneity, hub formation, hierarchical modularity, and territory structure — the phenomena documented in the Four Signatures paper and the Aura developmental run.

---

### 0.6 — Walker-Gated Computation

### The principle

The field φ exists at every node. But the field only **evolves** at nodes where gauge bosons (walkers) are present or have recently been present. A node with no recent walker visit is in an analytically predictable state: exponential relaxation toward whichever potential well it occupies. Computing this relaxation tick-by-tick wastes arithmetic on a known answer.

This is not an optimization. It is what gauge theory says. Interactions between nodes are mediated by gauge bosons (CF09). No boson → no interaction → no state change beyond autonomous relaxation. The walkers are the carriers of interaction. Where they go, the universe computes itself. Where they don't, nothing happens.

### Physical justification

1. **Telegraph finite speed (CF04):** Information propagates at c = √(D/τ) hops per tick. Walkers traverse the graph at bounded speed. A region not yet reached by any walker is causally disconnected from any stimulus.

2. **Thermal fluctuations are negligible (CF06):** With kT = 0.001 and barrier height λ = 1.0, the probability of a thermal kick moving a node from one well to another is ∝ exp(−ΔV/kT) = exp(−250) ≈ 0. Cold nodes don't spontaneously change state.

3. **Epistemic projection (CF07):** A fluctuation without an observer is not an event. A neuron spiking without a walker present to carry the signal cannot affect the global system. When a walker arrives and catches the node up, the spike becomes real — it enters the M-limb as a classical observable.

4. **Gauge boson mediation (CF09):** The berry connection's excitations (walkers) mediate the coupling between nodes. The bond-weighted Laplacian (L_ψ φ)_i = Σ ψ_ij(φ_j − φ_i) computes the interaction. But between two cold nodes deep in the same well, φ_j ≈ φ_i, so the Laplacian is ≈ 0. The interaction is zero without activity, and activity requires a walker to have brought or observed a signal.

### The three zones

Every node exists in one of three thermal zones, determined by walker trail heat (from the existing TrailMap/HeatMap infrastructure):

**ZONE 1 — HOT (walker present this tick)**
Full metriplectic Klein-Gordon step: Laplacian coupling, bond potential, telegraph solve. Bond field ψ for all edges of this node and its neighbors are updated. Walker-observed pairs checked for bond DOF instantiation. Events emitted to bus. This is where reality is being actively constructed.

Cost: O(k̄) per hot node (Laplacian + bond update for local neighborhood).

**ZONE 2 — WARM (neighbor of hot node, or trail score above decoherence floor)**
Full physics step, same equations as Zone 1. These nodes are in the compute set because the Laplacian coupling requires their neighbors' state to be current. The warm set is the boundary layer around the active set — it exists because physics is local, not because of a scheduling policy.

Cost: O(k̄) per warm node, every tick it remains in the compute set.

**ZONE 3 — COLD (below threshold, no recent walker)**
No tick-by-tick computation. State is frozen at last computed value plus a timestamp. When a walker arrives (cold → hot transition), the node is caught up analytically before the full physics step runs.

Cost: O(1) at time of catch-up (exponential relaxation formula).

### Catch-up computation (cold → hot transition)

When a walker arrives at a cold node i at tick t_now, with last visit at t_last:

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

This is exact for isolated nodes (no external drive during gap). It is approximate for nodes that had active neighbors during the gap — but those neighbors would have been in Zones 1-2 (they had walkers), and the Laplacian coupling from their direction was being computed on the neighbor's side already. The cold node's contribution to that coupling was its frozen φ value, which is correct because it wasn't changing.

### Walker source — gauge excitations from field dynamics

Walkers are gauge excitations radiated by nodes with kinetic energy above thermal equilibrium (§0.7). The walker system is NOT the existing `cortex/` infrastructure — it is derived from the field dynamics:

| Component | Physics source |
|-----------|---------------|
| Emission count per node | n_i = ⌊\|φ̇_i\|/v_th⌋ (Larmor radiation, §0.7) |
| Propagation direction | Bond-weighted CDF P(i→j) = ψ_ij/Σψ_ik, chaotic phase selection (§0.7) |
| TTL (hops per tick) | h_max = ⌊c/v_th⌋ where c = √(D/τ) is signal speed (§0.7) |
| Zone 1 boundary | Nodes visited by walkers this tick |
| Zone 2 boundary | Neighbors of Zone 1 nodes, or |φ̇| above decoherence floor |
| Zone 3 | All other nodes — analytically frozen |

The `cortex/` package (10 scout types, 6 map classes, ADC, runner, event system) is eliminated. Its functionality is replaced by the physics above. See `walker_system_complete_analysis.md` for the full analysis of why.

The walker system runs BEFORE the connectome step. Walker events and trail scores are passed into `step()` from the gauge emission/propagation loop.

### Active set construction

Each tick, the active set is built from walker events + trail decay:

```python
# After gauge emission/propagation (§0.7):
active_set = set()     # Zone 1: full physics this tick
warm_set = set()       # Zone 2: neighbor coupling

# All nodes visited by gauge excitations this tick → Zone 1
for event in walker_events:
    active_set.add(event.source)
    active_set.add(event.target)

# Include immediate neighbors of hot nodes (Laplacian coupling)
for i in list(active_set):
    for j in adj[i]:
        if j not in active_set:
            warm_set.add(j)

# Nodes with |φ̇| above decoherence floor but not walker-visited → Zone 2
for i in range(N):
    if abs(phi_dot[i]) > v_th and i not in active_set:
        warm_set.add(i)
```

### Scaling

| Architecture | Per-tick cost | What drives it |
|---|---|---|
| v3 (global rebuild) | O(N · 64) | Every node, every tick, 64 samples |
| v8 (full field update) | O(N · k̄) | Every node, every tick, k̄ neighbors |
| **v8.1 (walker-gated)** | **O(W · k̄)** | **W walker-visited nodes, k̄ neighbors** |

Where W = |active_set| + |warm_set|. For Aura at N=5000 with 256 walkers doing 3 hops: W ≈ 768 hot + ~2000 warm neighbors ≈ 2800 nodes = 56% of N. At N=100,000 with the same walker budget: W ≈ 3% of N. At N=1,000,000: W ≈ 0.3% of N.

The walker budget is a tuning parameter (initial condition, not material constant). More walkers → more of the graph is "conscious" per tick. Fewer walkers → tighter attention, deeper focus on active regions.

### What this replaces

- **_propose_new_edges via BFS:** Eliminated. Walker traversal history determines which pairs can instantiate bond DOFs. No graph-distance computation needed.

- **O(N) per-tick loops in step():** Replaced by O(W) loops over active/warm sets.

---

### 0.7 — Gauge Excitation Physics (Walker Emission and Propagation)

#### Physical origin

The coupling between the node field φ_i and the edge connection is through the covariant lattice derivative. When φ_i changes rapidly (|φ̇_i| is large), the local field configuration is evolving, which generates gauge field excitations on the edges emanating from node i. This is Larmor radiation: changing matter fields source gauge fields. It is not a design choice.

Walkers (gauge excitations) are radiated by nodes in proportion to their kinetic energy above thermal equilibrium.

#### Emission — Larmor radiation from the node field

**Thermal velocity** (from equipartition, CF06 §4.3):

    v_th = √(2·kT)

where kT = ½·Var(φ̇) is measured from the active set (§0.2).

**Emission count per node per tick:**

    n_i^emit = floor( |φ̇_i| / v_th )

This is deterministic. No np.random. The floor function converts continuous kinetic energy into discrete gauge quanta.

**Physical regimes:**

| |φ̇_i| | n_i | Physical meaning |
|--------|-----|------------------|
| 0 | 0 | Node at rest in vacuum. No radiation. Invisible to gauge sector (CF07 — thermally indistinguishable from empty space). |
| v_th | 1 | Thermal background. One walker, indistinguishable from noise. |
| 3·v_th | 3 | Genuinely excited. Three coherent gauge excitations propagate outward. |
| ≫ v_th | many | Domain wall or strong stimulus. Heavy radiation. |

**Total walker count per tick (emergent):**

    N_walkers(t) = Σ_i floor( |φ̇_i(t)| / v_th(t) )

This is entirely emergent:
- **t = 0:** Field starts at unstable vacuum φ = 0.5. φ̇ = 0 everywhere. Zero kinetic energy. Zero walkers. Nothing to radiate.
- **Tachyonic condensation:** Instability amplifies 10⁻¹⁶ differences. φ̇_i becomes nonzero at some nodes. Those nodes begin radiating gauge excitations along existing edges.
- **Domain formation:** Domain-wall nodes have large |φ̇|. These become strong emitters. Walkers propagate outward from excitation sites.
- **Steady state:** Thermal fluctuations. Every node has some φ̇_i from thermal motion. Only nodes with |φ̇_i| significantly above v_th produce coherent walkers.
- **Stimulus response:** Spikes at stimulus site, follows activity wavefront outward along bonds, dies back as field relaxes.

**The old cortex/ walker budget** (`traversal_walkers: int = 256`) is eliminated. The walker count is not a parameter — it is an observable of the field dynamics.

#### Propagation — bond-weighted gauge transport

A walker emitted at node i selects neighbor j with probability:

    P(i → j) = ψ_ij / Σ_{k ∈ N(i)} ψ_ik

This is the gauge boson transport: walkers preferentially travel along strong bonds. Condensed bonds (ψ ≈ 1) carry most gauge traffic. Weak bonds (ψ near decoherence floor) carry almost none. No bond (ψ = 0): no traversal possible.

**Deterministic sampling (no np.random):** The probability distribution P(i → j) is sampled deterministically using the fractional part of the emitting node's velocity as a phase selector:

    u = frac( |φ̇_i| · (1 + emit_index) )    # ∈ [0, 1), deterministic
    CDF = cumsum( ψ_i / sum(ψ_i) )
    j = first k where CDF[k] ≥ u

where `emit_index` is which of the n_i walkers this is (0, 1, 2, ...). Different walkers from the same node select different neighbors because `emit_index` shifts the phase. The fractional velocity is deterministic chaos from the nonlinear field dynamics — it IS the randomness, emergent from the J/M split and tachyonic instability.

**TTL-bounded propagation (locality):** A walker propagates for at most `h_max` hops per tick. This is the finite speed of gauge boson transport (CF04 — causal horizon grows from dynamics). A walker cannot traverse the entire graph in one tick; that would violate locality (A2). At each hop, the same bond-weighted CDF selection applies, with a new phase from the local velocity at each visited node.

    h_max = floor( c / v_th )

where c = √(D/τ) is the signal speed (§0.2). The TTL is physics-derived, not a tuning parameter.

**At each visited node, the walker observes the local configuration (CF07).** If it encounters an unconnected pair where both endpoints are observable (|φ̇| > v_th) and have a gradient between them, a bond DOF is instantiated at ψ = 0.0 (§0.1b, §4.6).

#### The full gauge excitation chain (zero engineering language)

1. **Radiation:** Node i emits ⌊|φ̇_i|/v_th⌋ gauge excitations per tick
2. **Propagation:** Each excitation traverses edges with probability ∝ ψ_ij, TTL-bounded, deterministically sampled via chaotic phase
3. **Observation:** At each visited node, walker observes local configuration (CF07)
4. **Instantiation:** If unconnected observable pair with gradient exists, bond DOF created at ψ = 0.0
5. **Condensation/decoherence:** Bond dynamics determine outcome (gradient source vs double-well barrier, §0.1b)

#### Implementation requirement: φ̇ as first-class state variable

The telegraph integrator already tracks `phi_curr` and `phi_prev` as second-order state. The velocity:

    φ̇_i = (phi_curr[i] - phi_prev[i]) / dt

is available each tick. However, the walker emission mechanism requires explicit access to φ̇. After the v8 migration, φ̇ is a **first-class state variable** that persists alongside φ:

```python
# Computed once per tick, after telegraph solve (Step 2), before walker emission
phi_dot = (phi_new - self.phi_curr).astype(np.float32)  # φ̇ = Δφ/dt, dt=1
v_th = np.sqrt(2.0 * max(self.kT, 1e-15))

# Walker emission (Step 4, replaces old cortex/ dispatch)
n_emit = np.floor(np.abs(phi_dot) / v_th).astype(np.int32)
# n_emit[i] = number of gauge excitations emitted by node i this tick
```

#### What this replaces in §0.6

§0.6 (Walker-Gated Computation) described the walker system as existing `cortex/` infrastructure to wire in. That section's **zone definitions** and **active set construction** logic remain valid — but the **walker source** changes:

| Old (cortex/) | New (§0.7) |
|---------------|------------|
| Fixed budget: `traversal_walkers = 256` | Emergent: N_walkers = Σ ⌊\|φ̇_i\|/v_th⌋ |
| Probabilistic emission via `np.random` | Deterministic: floor function on kinetic energy |
| 10 scout types with heuristic routing | Bond-weighted CDF, chaotic phase selection |
| Heuristic trail maps drive zone boundaries | φ̇ magnitude directly defines zones |
| Engineering parameter per scout class | Zero parameters — everything from field state |

The §0.6 active set construction pseudocode (lines 375–398) is updated: instead of `walker_events` coming from `cortex/run_scouts_once()`, they come from the gauge emission/propagation loop described above. The zone definitions (Zone 1 = walker-visited, Zone 2 = neighbors, Zone 3 = cold) remain unchanged — they are correct physics regardless of how walkers are sourced.

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

# --- Free parameters (micro-parameters of the discrete action) ---
# These instantiate VDM-AX-004. Different values = different physics.
# CF relationships (below) must hold for any valid choice.
J_COUPLING  = 0.0125   # Nearest-neighbor coupling in action
LAMBDA      = 1.0      # Node GL barrier: V(φ) = λ·φ²(1−φ)²
GAMMA_DAMP  = 0.5      # M-limb damping coefficient
EPS_BOND    = 200.0    # Bond telegraph inertia (from extended action)
LAMBDA_BOND = 1.0      # Bond GL barrier: U(ψ) = λ_bond·ψ²(1−ψ)²
BETA_DEBT   = 0.1      # Debt throttle exponent

# --- CF-derived quantities (computed, not assigned) ---
A_LATTICE = 1.0                                         # Lattice spacing
DT        = 1.0                                         # Timestep
C_SQ      = 2.0 * J_COUPLING * A_LATTICE**2             # VDM-AX-C02
D_DIFF    = C_SQ / GAMMA_DAMP                           # VDM-E-050
TAU       = 1.0 / GAMMA_DAMP                            # CF04 §2.1
C_SIGNAL  = float(np.sqrt(D_DIFF / TAU))                # CF04 §3.1
TAU_BOND  = EPS_BOND * DT**2                            # From action variation

# kT is measured, not set. Bootstrap for first ticks.
KT_EFF_INIT = 0.001

def bond_decoherence_floor(kT: float) -> float:
    """
    Bond decoherence threshold: √(2·kT/ε_bond).
    Bonds below this are thermally indistinguishable from vacuum.
    Source: CF07 §4.1.
    """
    return float(np.sqrt(2.0 * max(kT, 1e-15) / EPS_BOND))

# Bootstrap (overwritten by measured kT after first ticks)
ETA_BOND_FLOOR = bond_decoherence_floor(KT_EFF_INIT)


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
    lam_bond: float = LAMBDA_BOND,
) -> np.ndarray:
    """
    U_bond(ψ) = λ_bond · ψ²(1−ψ)²
    U'_bond(ψ) = 2·λ_bond · ψ(1−ψ)(1−2ψ)
    Source: CF03 §1.1 (double-well applied to bond DOF).
    """
    return (2.0 * lam_bond * psi_ij * (1.0 - psi_ij) * (1.0 - 2.0 * psi_ij)).astype(np.float32)


def bond_gradient_source(
    phi_i: float,
    phi_j: np.ndarray,
) -> np.ndarray:
    """
    Source term from action variation: ½(φ_j − φ_i)²

    Bonds form where the field has large spatial gradients (domain walls).
    This is NOT activity coupling and NOT Hebbian. Nodes in the same state
    produce zero source. Nodes straddling a domain wall produce maximum source.
    Source: extended action (§0.1b), variation δS/δψ_ij.
    """
    return (0.5 * (phi_j - phi_i)**2).astype(np.float32)


def klein_gordon_rhs(
    phi: np.ndarray,
    adj_lists: list[np.ndarray],
    psi: list[np.ndarray],
    lam: float = LAMBDA,
    D: float = D_DIFF,
) -> np.ndarray:
    """
    Node field RHS: rhs = D · L_ψ(φ) − V'(φ)

    No injected noise. Endogenous fluctuations from J/M split,
    tachyonic instability, Laplacian coupling on self-modifying graph.
    Source: VDM-AX-004, CF01 §4.1, CF11 §2.3, CF04 §3.1, CF03 §1.1.
    """
    transport = D * bond_weighted_laplacian(phi, adj_lists, psi)
    dV = node_potential_derivative(phi, lam)
    return transport - dV


def get_constants() -> dict:
    """Return all material constants for telemetry/checkpoint."""
    return {
        "J_COUPLING": J_COUPLING, "LAMBDA": LAMBDA, "GAMMA_DAMP": GAMMA_DAMP,
        "EPS_BOND": EPS_BOND, "LAMBDA_BOND": LAMBDA_BOND, "BETA_DEBT": BETA_DEBT,
        "TAU": TAU, "D_DIFF": D_DIFF, "C_SQ": C_SQ, "C_SIGNAL": C_SIGNAL,
        "TAU_BOND": TAU_BOND, "KT_EFF_INIT": KT_EFF_INIT,
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
    bond_gradient_source,
    get_constants,
    J_COUPLING, LAMBDA, GAMMA_DAMP, EPS_BOND, LAMBDA_BOND, BETA_DEBT,
    TAU, D_DIFF, C_SQ, C_SIGNAL, TAU_BOND, KT_EFF_INIT,
    bond_decoherence_floor, ETA_BOND_FLOOR,
)

__all__ = [
    "klein_gordon_rhs",
    "bond_weighted_laplacian",
    "node_potential_derivative",
    "bond_potential_derivative",
    "bond_gradient_source",
    "get_constants",
    "J_COUPLING", "LAMBDA", "GAMMA_DAMP", "EPS_BOND", "LAMBDA_BOND", "BETA_DEBT",
    "TAU", "D_DIFF", "C_SQ", "C_SIGNAL", "TAU_BOND", "KT_EFF_INIT",
    "bond_decoherence_floor", "ETA_BOND_FLOOR",
]
```

---

## 4. sparse_connectome.py — Modifications

### 4.1 `__init__` — Complete new state

Remove from `__init__`: all references to `telegraph_tau`, `gamma`, `kappa`, `W_prev`, `W_curr`, `last_activation_tick`, `eligibility`, `TOPO_PERIOD`, `TOPO_THRESHOLD`, `TOPO_PATIENCE`.

Add after `self.W = ...`:

```python
# --- Parameters (free choices constrained by CF relationships) ---
from .void_dynamics_adapter import (
    J_COUPLING, LAMBDA, GAMMA_DAMP, EPS_BOND, LAMBDA_BOND, BETA_DEBT,
    TAU, D_DIFF, C_SQ, TAU_BOND, KT_EFF_INIT,
    bond_decoherence_floor,
)
self.J = J_COUPLING
self.lam = LAMBDA               # Node GL barrier (unchanged name for compat)
self.gamma_damp = GAMMA_DAMP
self.eps_bond = EPS_BOND
self.lam_bond = LAMBDA_BOND
self.beta_debt = BETA_DEBT

# CF-derived
self.tau = TAU
self.D = D_DIFF
self.c_sq = C_SQ
self.tau_bond = TAU_BOND
self.kT = KT_EFF_INIT           # Overwritten by measurement after first ticks

# --- Node field state ---
self.phi_curr = self.W.copy()
self.phi_prev = self.W.copy()

# --- Debt (no ceiling — self-limits via exp(β·debt) asymptotic freeze) ---
self.debt = np.zeros(self.N, dtype=np.float64)

# --- Walker-gated computation state ---
self.last_visit = np.zeros(self.N, dtype=np.int32)   # tick of last Zone 1 visit
self.last_visit[:] = -1  # mark all as never-visited (forces catch-up on first touch)

# Zone 2→3 boundary: same decoherence floor as bonds (CF07).
self.WARM_THRESHOLD = float(bond_decoherence_floor(self.kT))

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

# Deterministic seed for initial conditions (NOT for physics noise).
self._seed = getattr(self, '_seed', 42)
```

### 4.2 Graph initialization — No change from existing runtime

The existing runtime's graph initialization (k-regular random, preferential attachment, or checkpoint load) is RETAINED. The migration does not change how the initial graph is built — it changes how the graph EVOLVES after initialization.

The `_build_cubic_adjacency()` method from v7 is **deleted**. It must not exist in the migrated codebase. If a cubic lattice is desired for controlled experiments, it can be loaded as a checkpoint, not hardcoded as the only initialization path.

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
def step(self, tick: int, walker_events: list = None, trail_scores: dict = None):
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
    from .void_dynamics_adapter import bond_potential_derivative, bond_gradient_source

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
            # Stimulus decays at telegraph rate: exp(−1/τ). CF04 §2.1.
            self._stim *= getattr(self, "_stim_decay", float(np.exp(-1.0 / self.tau)))
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
        tau_eff_i = float(self.tau * np.exp(self.beta_debt * self.debt[i]))
        phi_well = round(float(self.phi_curr[i]))  # 0.0 or 1.0

        decay_phi = np.exp(-dt / tau_eff_i)
        self.phi_curr[i] = phi_well + (self.phi_curr[i] - phi_well) * decay_phi
        self.phi_prev[i] = phi_well + (self.phi_prev[i] - phi_well) * np.exp(-(dt - 1) / tau_eff_i)

        # Bond relaxation
        tau_bond = self.tau_bond
        decay_psi = np.exp(-dt / tau_bond)
        for ki in range(self.adj[i].size):
            psi_well = round(float(self.psi_curr[i][ki]))
            self.psi_curr[i][ki] = psi_well + (self.psi_curr[i][ki] - psi_well) * decay_psi
            self.psi_prev[i][ki] = psi_well + (self.psi_prev[i][ki] - psi_well) * np.exp(-(dt - 1) / tau_bond)

        # Debt decay during gap (no activity)
        self.debt[i] *= (1.0 - self.beta_debt) ** dt

    # Update visit timestamps for computed nodes
    for i in active_set:
        self.last_visit[i] = tick

    # --- Step 2: Node field computation (active + warm only) ---
    compute_list = np.array(sorted(compute_set), dtype=np.int32)
    tau_eff = self.tau * np.exp(self.beta_debt * self.debt)
    phi_dot = self.phi_curr - self.phi_prev

    # Laplacian for computed nodes only
    rhs = np.zeros(N, dtype=np.float32)
    for i in compute_list:
        nbrs = self.adj[i]
        if nbrs.size == 0:
            continue
        # Bond-weighted Laplacian: Σ ψ_ij (φ_j − φ_i)
        lap = np.sum(self.psi_curr[i] * (self.phi_curr[nbrs] - self.phi_curr[i]))
        # Potential derivative: 2λ φ(1−φ)(1−2φ)
        phi_i = self.phi_curr[i]
        dV = 2.0 * self.lam * phi_i * (1.0 - phi_i) * (1.0 - 2.0 * phi_i)
        rhs[i] = self.D * lap - dV

    # Telegraph solve for computed nodes
    phi_new = self.phi_curr.copy()
    for i in compute_list:
        a_inertia = float(tau_eff[i])
        numerator = rhs[i] + (2.0 * a_inertia + 1.0) * self.phi_curr[i] - a_inertia * self.phi_prev[i]
        denominator = a_inertia + 1.0
        phi_new[i] = np.clip(numerator / denominator, 0.0, 1.0)

    # --- Step 3: Bond field update (computed nodes only) ---
    # Bond telegraph: ε_bond·ψ̈ + ψ̇ = −U'(ψ) + ½(φ_j − φ_i)²
    # Source term from action variation (§0.1b). No noise.

    for i in compute_list:
        nbrs = self.adj[i]
        if nbrs.size == 0:
            continue
        psi_c = self.psi_curr[i]
        psi_p = self.psi_prev[i]

        dU = bond_potential_derivative(psi_c, lam_bond=self.lam_bond)
        grad_source = bond_gradient_source(self.phi_curr[i], self.phi_curr[nbrs])
        rhs_bond = -dU + grad_source

        psi_new = (
            rhs_bond + (2.0 * self.eps_bond + 1.0) * psi_c
            - self.eps_bond * psi_p
        ) / (self.eps_bond + 1.0)
        self.psi_prev[i] = psi_c.copy()
        self.psi_curr[i] = np.clip(psi_new, 0.0, 1.0).astype(np.float32)

    # --- Step 4: Edge death (computed nodes only) ---
    self._remove_dead_edges(compute_list)

    # --- Step 5: Bond DOF instantiation from walker observation ---
    phi_dot_abs = np.abs(phi_dot).astype(np.float32)
    self._instantiate_walker_observed_bonds(walker_events, phi_dot_abs)

    # --- Step 6: Update node field history ---
    dphi = np.zeros(N, dtype=np.float32)
    for i in compute_list:
        dphi[i] = phi_new[i] - self.phi_curr[i]
    self.phi_prev[compute_list] = self.phi_curr[compute_list].copy()
    self.phi_curr[compute_list] = phi_new[compute_list]
    self.W = self.phi_curr  # backward compat alias

    # --- Step 6b: Measure effective temperature from dynamics ---
    # Equipartition: kT = ½·Var(φ̇) over the active set.
    # The system's own temperature, not a forcing parameter.
    if len(compute_list) > 10:
        phi_dot_active = phi_new[compute_list] - self.phi_curr[compute_list]
        measured_kT = 0.5 * float(np.var(phi_dot_active))
        self.kT = max(measured_kT, 1e-15)

    # --- Step 7: Debt (computed nodes only) ---
    self.debt[compute_list] = (
        (1.0 - self.beta_debt) * self.debt[compute_list]
        + np.abs(dphi[compute_list]).astype(np.float64)
    )

    # --- Step 8: External stimulation decay ---
    try:
        # Stimulus decays at telegraph rate: exp(−1/τ). CF04 §2.1.
        self._stim *= getattr(self, "_stim_decay", float(np.exp(-1.0 / self.tau)))
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

1. **walker_events and trail_scores are passed in.** The walker system runs in CoreEngine.step() BEFORE connectome.step(). The engine passes walker output to the connectome. This preserves the existing separation of concerns — walkers are read-only against the connectome, connectome receives their reports.

2. **The catch-up in Step 1 uses analytical formulas.** For a node in a double-well with no external drive, exponential relaxation toward the nearest well is exact. For bonds, same. The `round()` to find the nearest well works because φ and ψ are both in double-wells on [0,1] with minima at 0 and 1.

3. **The old _void_traverse (Step 11 in v8) is removed.** The walker system replaces it entirely. _void_traverse was a simplified walker embedded directly in the connectome. The cortex/ walker system is its replacement.

### 4.5 — `_remove_dead_edges()` — Modified for active set

```python
def _remove_dead_edges(self, compute_nodes: np.ndarray = None):
    """
    Remove edges whose bond field ψ has fallen below the emergent bond
    decoherence floor. Only checks nodes in compute_nodes (or all if None).
    """
    from .void_dynamics_adapter import bond_decoherence_floor
    eta_floor = bond_decoherence_floor(self.kT)
    nodes = range(self.N) if compute_nodes is None else compute_nodes
    for i in nodes:
        i = int(i)
        if self.adj[i].size == 0:
            continue
        alive = self.psi_curr[i] >= eta_floor
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

### 4.6 — `_instantiate_walker_observed_bonds()` — Bond DOF instantiation

This replaces `_propose_new_edges()` entirely. No BFS. No h_causal.
Walker traversal IS the causal cone. When a walker encounters an
unconnected pair with both endpoints observable, a bond DOF is
instantiated at the unstable vacuum ψ = 0.0. The telegraph integrator
and gradient source determine whether the bond condenses or decoheres.

```python
def _instantiate_walker_observed_bonds(
    self, walker_events: list, phi_dot_abs: np.ndarray,
):
    """
    Instantiate bond DOFs at ψ = 0.0 for unconnected pairs with
    observable endpoints encountered during walker traversal.

    Two observation geometries:

    1. **Direct observation:** Walker steps i → j. Both endpoints
       observable (|φ̇| > 0), not connected. Bond DOF instantiated
       on edge (i,j) at unstable vacuum ψ = 0.0.

    2. **Transitive observation:** Walker at j (arrived from i).
       Node j has neighbor k. If i and k are both observable and not
       connected, the walker has observed a path i—j—k. Bond DOF
       instantiated on edge (i,k) at ψ = 0.0. The shortcut is within
       the observed causal cone because the walker traversed both legs.

    Both geometries respect causality: no bond DOF exists between
    nodes outside the walker's observation cone (CF04: causal horizon
    from dynamics; CF09: walker = gauge boson transport).

    The observability condition (|φ̇| > 0) is the CF07 measurement
    prerequisite: the gauge boson can only interact with nodes that
    have detectable dynamics. It is NOT the driving force. The driving
    force is the gradient source ½(φ_j − φ_i)² from the action
    variation, which the telegraph integrator evaluates after
    instantiation. The gradient decides; the walker mediates.

    Cost: O(W·h·k̄) per tick. For W=768, h=3, k̄~20: ~46,000 pair
    checks. Negligible vs field update.
    """
    if not walker_events:
        return

    instantiated = set()

    for event in walker_events:
        i = event.get("from")
        j = event.get("to")
        if i is None or j is None:
            continue

        # --- Direct observation: walker stepped i → j ---
        if phi_dot_abs[i] > 0 and phi_dot_abs[j] > 0:
            if j not in self.adj[i]:
                pair = (min(i, j), max(i, j))
                if pair not in instantiated:
                    self._condense_spinodal_bond(i, j)
                    instantiated.add(pair)

        # --- Transitive observation: walker at j, check j's neighbors ---
        if phi_dot_abs[i] > 0:
            for k_idx in range(self.adj[j].size):
                k = int(self.adj[j][k_idx])
                if k == i:
                    continue
                if phi_dot_abs[k] > 0 and k not in self.adj[i]:
                    pair = (min(i, k), max(i, k))
                    if pair not in instantiated:
                        self._condense_spinodal_bond(i, k)
                        instantiated.add(pair)
```

### Why 1-hop ego-network, not 2-hop scan:

The walker is the gauge boson (CF09). Its observation cone is the set of nodes it has physically visited or can directly see from its current position. At node i, the walker sees i and adj(i). It does NOT see adj(adj(i)) — those nodes are behind a corner the walker hasn't turned.

Triangle completion within the 1-hop ego-network is the correct operation: the walker observes that j and k are both observable and both coupled to i, but not to each other. The shortcut j ↔ k is a bond DOF placed at the unstable vacuum. The gradient source and telegraph integrator determine whether it condenses or decoheres. Cost: O(k̄) per touch, linear in mean degree.

```python
def _condense_spinodal_bond(self, u: int, v: int):
    """
    Instantiate bond DOF on edge (u,v) at the unstable vacuum ψ = 0.0
    for spinodal condensation.

    The gradient source ½(φ_j − φ_i)² from the action variation tilts
    the bond double-well. At domain walls where ½(Δφ)² exceeds the
    barrier maximum (~0.192·λ_bond), the ψ=0 minimum ceases to exist
    — the bond is in the spinodal region and condenses deterministically
    toward ψ=1 via the telegraph integrator. Away from domain walls,
    the source is too weak to destabilize ψ=0, and the bond decoheres
    below the thermal floor √(2·kT/ε_bond).

    Same tachyonic condensation mechanism as the node field: unstable
    vacuum drives spontaneous symmetry breaking. No noise, no barrier
    crossing, no thermal nucleation, no engineering selection.

    Source: extended action (§0.1b), spinodal regime analysis.
    """
    self.adj[u] = np.append(self.adj[u], np.int32(v))
    self.psi_curr[u] = np.append(self.psi_curr[u], np.float32(0.0))
    self.psi_prev[u] = np.append(self.psi_prev[u], np.float32(0.0))

    self.adj[v] = np.append(self.adj[v], np.int32(u))
    self.psi_curr[v] = np.append(self.psi_curr[v], np.float32(0.0))
    self.psi_prev[v] = np.append(self.psi_prev[v], np.float32(0.0))
```

---

## 4.7 — Reward formula

```python
# Scale Fisher speed using measured kT as energy-information bridge.
raw = float(-dH_dt) + self.kT * float(fisher_speed)
```

---

## 6.1 Time variable

DELETE: `t = float(step) * dt_physics` and any float time computation.
The integer `step` counter IS the physics time. No conversion needed.

---

## 9.3 — Output nodes

**Disjointness constraint:** Output node indices MUST NOT overlap with UTE input node indices. Sensory cortex and motor cortex are anatomically disjoint. Enforced at init:

```python
assert set(output_nodes).isdisjoint(set(ute_input_nodes)), \
    "Output and input regions must not overlap (disjoint anatomy)."
```

### SpeechOutputAdapter

```python
        if not np.any(active_mask):
            return None  # silence — no node above thermal noise floor
```

---

## 11 — Eliminated Proxies Checklist

- [ ] `TOPO_PERIOD` as a cron timer (replaced by bond telegraph inertia ε_bond)
- [ ] `TOPO_THRESHOLD` as an eligibility gate (replaced by decoherence floor)
- [ ] `TOPO_PATIENCE` as a debounce counter (replaced by telegraph inertia)
- [ ] `tau_e` as an eligibility trace (replaced by |φ̇| as velocity state)
- [ ] `R_NUCLEATION` as a fixed spatial cutoff (replaced by walker trail reachability)
- [ ] `debt_max` as a ceiling clamp (replaced by exp(β_debt·debt) asymptotic freeze)
- [ ] `dt_physics_us` as pre-computed conversion (replaced by √(τ/D) at I/O boundary)
- [ ] `PSI_DEATH` as arbitrary threshold (replaced by dynamic decoherence floor)
- [ ] `PSI_SEED` as arbitrary spawn (replaced by ψ=0.0 with gradient-driven spinodal condensation)
- [ ] `r_causal` as a float Euclidean radius (replaced by walker trail reachability)
- [ ] `h_causal` as a stored state array
- [ ] `pos` array as spatial embedding
- [ ] `_build_cubic_adjacency` method
- [ ] Injected noise in node/bond equations

---

## 12 — Validation Gates

| Gate | Test | Pass Criterion |
|------|------|----------------|
| 1 | Import Void_Equations | No fallback path; crash on import failure |
| 2 | Constants are CF-derived | D = c²/γ, τ = 1/γ, c = √(D/τ) |
| 3 | No hardcoded timescales | All timescales from τ, ε_bond, or measured kT |
| 4 | Bond field persists | ψ_curr, ψ_prev arrays exist and evolve |
| 5 | Topology evolves | Adjacency changes over runtime (bonds condense/decoherence) |
| 6 | No global rebuild | `step()` does not allocate new adjacency structures |
| 7 | Walker-gated computation | Active set size < N for most ticks |
| 8 | Bond locality | Every bond DOF instantiated during the run was observed by a walker traversal event |
| 9 | No spatial embedding | `pos` array does not exist |
| 10 | Debt self-limits | debt_i grows but τ_eff = τ·exp(β·debt) asymptotically freezes node |
| 11 | No noise injection | No np.random calls in physics path |
| 12 | kT measured | kT = ½·Var(φ̇) over active set, updated each tick |
| 13 | CFL stable | D·Δt/a² < 0.5 (D = 0.05, Δt = 1, a = 1 → 0.05) |
| 14 | Memory O(N·k̄) | Total memory ~260 MB for N=1M, k̄=20 |
| 15 | Developmental silence | At tick 0 with randomized initial bonds, the speech adapter returns None for ≥ 90% of the first 1000 ticks. Coherent output must be earned through bond development. |
| 16 | Bond condensation from gradients | With noise removed and source term = ½(φ_j − φ_i)², bonds must condense at domain walls. At tick 50000, count(ψ > 0.5) > 0. If zero bonds survive, the ratio λ_bond / max((φ_j−φ_i)²) is too high — domain wall gradients are not overcoming the barrier. |

---

## Appendix — CF Traceability Table

| v3 Mechanism | v8 Replacement | Source |
|---|---|---|
| `TOPO_PERIOD = 50` (cron timer) | Bond telegraph inertia ε_bond = 200 (from extended action) | VDM-AX-004 extended; bond EL equation |
| `TOPO_THRESHOLD = 0.01` (eligibility gate) | Decoherence floor √(2·kT/ε_bond), kT measured | CF07 §4.1 + CF06 §4.3 (equipartition) |
| `TOPO_PATIENCE = 100` (debounce counter) | Telegraph inertia in bond equation (bonds resist sudden change) | CF04 §2.1: τ_bond from action variation |
| `tau_e = 250` (eligibility trace) | |φ̇| = field velocity (no separate trace) | CF11 §2.3: velocity is state variable |
| `R_NUCLEATION = 4.0` (fixed spatial cutoff) | Walker trail reachability (walkers ARE the causal cone) | CF04 §4.2 + CF09: gauge boson transport |
| `debt_max = 10.0` (ceiling clamp) | Self-limiting via exp(β_debt·debt) asymptotic freeze | CF03 §7.2: exponential throttling |
| `dt_physics_us = 6324555` (pre-computed) | √(τ/D) computed symbolically at I/O boundary | CF04: dimensional analysis |
| `PSI_DEATH = 1e-6` (arbitrary threshold) | Dynamic decoherence floor √(2·kT/ε_bond) | CF07 §4.1: epistemic projection |
| `PSI_SEED = 0.01` (arbitrary spawn) | ψ = 0.0; gradient source ½(φ_j−φ_i)² drives spinodal condensation | VDM-AX-004 extended action variation |

---

## Summary of Patches Applied (35 Total)

| Section | Patches | What changed |
|---------|---------|-------------|
| §0.1 EOM | 01–07 | Noise removed, bond derived from action, gradient source replaces activity coupling, engineering language eliminated |
| §0.2 Constants | 08 | Free params + CF constraints, D ≠ γ, honest labeling |
| §0.4 Scaling | 09–15 | Terminology fixes, h_causal removed |
| §0.5 Topology | 16–17 | Decoherence/condensation language |
| §0.6 Zones | 18–20 | Typo, Zone 1/2 fixes |
| §2 Void_Equations | 21–23 | Constants, functions, noise removal |
| §4.1 __init__ | 24–26 | Imports, WARM_THRESHOLD, no RNG |
| §4.3 step() | 27–31 | Signature, noise removal, bond update, kT measurement, method call |
| §4.5 dead edges | 32 | Dynamic decoherence floor |
| §4.6 bond instantiation | 33 | Complete method rewrite + _condense_spinodal_bond |
| §6–§9 remaining | 34a–34e | Time variable, reward, stimulus, output nodes |
| §11–§12 validation | 34f–35a | Checklist fixes, testable gates |
| Appendix | 35b | CF traceability table |

---

## The Three Key Physics Corrections

1. **Bond source ½(φ_j − φ_i)²** replaces the invented `ε·|φ̇_i|·|φ̇_j|`. Falls out of the action. Bonds form at domain walls (spatial gradients), not between correlated oscillators (Hebbian). Self-limiting: bond enables Laplacian coupling → gradient relaxes → source decreases.

2. **No injected noise.** The metriplectic split IS the noise source. kT is measured from what the dynamics produce, not injected.

3. **No engineering-choice language.** The walker observes. The bond DOF is instantiated at the unstable vacuum. The gradient source and telegraph integrator determine condensation or decoherence. There is nothing to propose, evaluate, accept, or reject.

---

**END OF DIRECTIVE v8 FINAL CONSOLIDATED**
