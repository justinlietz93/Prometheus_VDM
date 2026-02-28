# Directive v8 — Consolidated Patch Set (FINAL)

**Date:** 2026-02-28
**Replaces:** ALL previous patch files. This is the only document.
**Patch count:** 35 patches, applied in directive section order.

---

## Confidence Assessment

### HIGH CONFIDENCE — mathematically derived

1. **Bond source term ½(φ_j − φ_i)² from action variation.** Extend
   VDM-AX-004 to include ψ_ij as dynamical DOF. Variation gives
   +½(W_j−W_i)² as the driving force. This is algebra. The directive's
   original `ε·|φ̇_i|·|φ̇_j|` was invented — it doesn't come from any
   action, and it implies Hebbian "fire together, wire together" which
   would cause runaway without external regulation. The correct source
   drives bond formation at spatial gradients (domain walls), not
   temporal correlations. Self-limiting: once the bond enables Laplacian
   coupling, the gradient relaxes, reducing the source that created it.

2. **Noise injection violates metriplectic structure.** J-limb + M-limb
   accounts for ALL dynamics (CF01). np.random adds energy with no
   entropy production — unaccounted third term. N=1000 coupled nonlinear
   oscillators with tachyonic instability produce deterministic chaos.

3. **kT is measured, not injected.** Equipartition (CF06 §4.3):
   kT = ½·Var(φ̇) over the active set.

4. **Constants table citations are fabricated.** CFs derive STRUCTURE
   (equation forms, relationships), not numbers. The numbers are free
   parameter choices that need honest labeling.

5. **D ≠ γ.** D is diffusion (0.05), γ is damping (0.5). Related by
   D = c²/γ = 2Ja²/γ. Cannot be chosen independently.

6. **Engineering-choice language invites coding agent errors.** When the
   physics is solved, there are no choices in the dynamics. Words like
   "propose," "candidate," "evaluate," "accept/reject," "nucleate,"
   "birth" imply decisions where none exist. The walker observes, the
   bond DOF is instantiated at the unstable vacuum, the gradient and
   telegraph integrator determine the outcome.

### MEDIUM CONFIDENCE — structurally sound, values may need tuning

7. Specific parameter values (J=0.0125, γ=0.5, ε_bond=200) are
   reasonable starting points. CFL stable, interesting dynamics. Choices.

8. WARM_THRESHOLD tied to decoherence floor. Physically motivated but
   numeric mapping may need calibration.

### REQUIRES EMPIRICAL VALIDATION (gate 16)

9. Gradient source alone drives bonds past barrier. Max barrier
   resistance ≈ 0.192·λ_bond. Domain walls provide sufficient gradient.
   Must be confirmed at runtime.

---

## Terminology Rules (applies to ALL patches below)

| BANNED (engineering) | USE THIS (physics) |
|----------------------|-------------------|
| propose / proposal | (delete — nothing is proposed) |
| candidate | walker-observed pair / unconnected pair |
| nucleate / nucleation | spinodal condensation / instantiate at unstable vacuum |
| birth (of bond) | condensation |
| death (of bond) | decoherence |
| accept / reject | condenses / decoheres |
| evaluate / select | (delete — dynamics determine outcome) |
| seed (as verb) | instantiate at ψ = 0.0 |
| spawn / create (a bond) | instantiate bond DOF |
| co-active (as bond driver) | observable (measurement condition) + gradient (force) |

**Why "co-active" is wrong:** The source term is ½(φ_j − φ_i)². Nodes
in the same state have zero source. Nodes with large DIFFERENCE have
maximum source. This is the opposite of Hebbian "fire together, wire
together." The measurement condition (CF07) that both endpoints must be
observable (|φ̇| > 0) is a prerequisite for the gauge boson to interact
with them. It is not the driving force. The gradient is the force.

---

# PATCHES BY DIRECTIVE SECTION

---

## §0.1 — Equations of Motion

### PATCH 01 — Remove η from node EOM (line 30)

**OLD:** `= D · (L_ψ φ)_{n,i} − V'(φ_{n,i}) + η_{n,i}`
**NEW:** `= D · (L_ψ φ)_{n,i} − V'(φ_{n,i})`

### PATCH 02 — Remove η description (line 41)

**OLD:**
```
- `η_i = √(2 · D · kT) · ξ_i` — fluctuation-dissipation noise, ξ ~ N(0,1).
```

**NEW:**
```
- No injected noise. The J-limb (telegraph inertia τ·φ̈) and M-limb
  (friction φ̇) fight on the same field. Their interaction with the
  tachyonic double-well and Laplacian coupling produces endogenous
  fluctuations from N coupled nonlinear oscillators on a self-modifying
  graph. kT is measured from these dynamics via equipartition (CF06 §4.3),
  not injected.
```

### PATCH 03 — Remove η from rhs pseudocode (line 48)

**OLD:** `rhs(i) = D · (L_ψ φ)_i − V'(φ_i) + η_i`
**NEW:** `rhs(i) = D · (L_ψ φ)_i − V'(φ_i)`

### PATCH 04 — New §0.1b: Bond Field Derivation (insert after line 53)

**INSERT after the node field implicit solve, before line 56:**

```markdown
#### Bond field equation — derived from extended action

The node field equation comes from varying VDM-AX-004 w.r.t. W_i.
The bond field equation comes from the same action with ψ_ij as a
dynamical degree of freedom.

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

The source term **½(φ_j − φ_i)²** falls out of the variation because
ψ_ij multiplies (W_j − W_i)² in the action. Differentiating
−½ψ(W_j−W_i)² w.r.t. ψ gives +½(W_j−W_i)².

**Physical meaning:** Bonds form where the field has large spatial
gradients — at domain walls. Nodes in the same well have
(φ_j−φ_i)² ≈ 0, exerting no force. Nodes straddling a domain wall
have (φ_j−φ_i)² ≈ 1, pushing ψ→1. This is NOT Hebbian. The source
is gradient (spatial difference), not correlation (temporal
coincidence). The mechanism is self-limiting: once the bond condenses,
Laplacian coupling D·ψ_ij(φ_j−φ_i) smooths the gradient, reducing
the source that formed the bond. Equilibrium without external regulation.

**Add M-limb damping (CF01/CF02):**

    ε_bond · ψ̈_ij + ψ̇_ij = −U'_bond(ψ_ij) + ½(φ_j − φ_i)²

J-limb: ε_bond·ψ̈ (conservative inertia). M-limb: ψ̇ (friction).

**Bond potential:** U_bond(ψ) = λ_bond · ψ²(1−ψ)² (CF03 §1.1
applied to bond DOF). Bonds prefer ψ=0 or ψ=1. Barrier at ψ=0.5.

**Bond potential derivative:** U'(ψ) = 2·λ_bond · ψ(1−ψ)(1−2ψ)

**Full bond RHS:**

    rhs_bond(i,j) = −2·λ_bond · ψ(1−ψ)(1−2ψ) + ½(φ_j − φ_i)²

**Implicit solve (dt = 1):**

    ψ_new = [rhs_bond + (2·ε_bond + 1)·ψ_curr − ε_bond·ψ_prev]
             / [ε_bond + 1]
    ψ_new = clip(ψ_new, 0.0, 1.0)

**Why bonds form without noise:** At ψ=0, U'(0) = 0. The only force
is +½(φ_j−φ_i)². Any nonzero gradient pushes ψ positive. Max barrier
resistance ≈ 0.192·λ_bond (at ψ≈0.21). For λ_bond = 1.0, the source
must exceed ~0.19, requiring |φ_j−φ_i| > 0.62. Domain walls provide
this. Away from walls, gradients are small, bonds dissolve.
```

### PATCH 05 — Replace old bond equation (lines 56–91)

**DELETE the entire block from line 56 ("Bond field equation (CF03...")
through line 91 (end of implicit solve).** This removes the invented
`ε_topo`, the activity-coupling `|φ̇_i|·|φ̇_j|`, and the noise term.

**REPLACE WITH:**

```markdown
#### Bond field equation (derived from extended action, see §0.1b):

    ε_bond · (ψ_{n+1,ij} − 2ψ_{n,ij} + ψ_{n-1,ij}) / dt²
    + (ψ_{n+1,ij} − ψ_{n,ij}) / dt
    = −U'_bond(ψ_ij) + ½(φ_j − φ_i)²

Where:
- `ε_bond` — bond telegraph inertia. Free parameter from extended
  action. Large ε_bond → slow topology.
- `U_bond(ψ) = λ_bond · ψ²(1−ψ)²` — double-well for bond bistability
  (CF03 §1.1 applied to bond DOF).
- `½(φ_j − φ_i)²` — gradient source from action variation. Bonds form
  at domain walls where the field has large spatial gradients. NOT
  activity coupling. NOT Hebbian.
- No noise term. Fluctuations in (φ_j − φ_i)² come from node dynamics.

Bond potential derivative:

    U'_bond(ψ) = 2·λ_bond · ψ(1−ψ)(1−2ψ)

Full RHS:

    rhs_bond(i,j) = −2·λ_bond · ψ(1−ψ)(1−2ψ) + ½(φ_j − φ_i)²

Implicit solve (dt = 1):

    ψ_new(i,j) = [rhs_bond + (2·ε_bond + 1)·ψ_curr − ε_bond·ψ_prev]
                  / [ε_bond + 1]
    ψ_new(i,j) = clip(ψ_new(i,j), 0.0, 1.0)
```

### PATCH 06 — Replace bond decoherence callout (lines 93–94)

**OLD:**
```
> **Bond Decoherence and Nucleation (CF07):**
> Structures physically cease to exist in the observable M-limb when
> they become indistinguishable from background thermal noise. Therefore,
> when a bond's strength falls below the emergent thermal noise floor
> (**$\psi_{ij} < \sqrt{2 \cdot \varepsilon_{topo} \cdot kT}$**), the
> edge is lost to decoherence and removed from the adjacency list. When
> a candidate edge is proposed, it must be nucleated strictly at
> **$\psi_{ij} = 0.0$**. The continuous metriplectic integration and
> thermodynamic forces will naturally lift the bond out of the vacuum
> if favored, requiring no artificial numerical seeding.
```

**NEW:**
```
> **Bond Decoherence and Spinodal Condensation (CF07, §0.1b):**
> Structures physically cease to exist in the observable M-limb when
> they become indistinguishable from background thermal noise. When a
> bond's strength falls below the emergent decoherence floor
> (**$\psi_{ij} < \sqrt{2 \cdot kT / \varepsilon_{bond}}$**, where kT
> is measured from active-set φ̇ variance via equipartition), the edge
> is removed from the adjacency list. When a walker (gauge boson, CF09)
> encounters an unconnected pair with both endpoints observable
> (|φ̇| > 0, CF07 measurement condition), a bond DOF is instantiated
> at the unstable vacuum **$\psi_{ij} = 0.0$**. The gradient source
> ½(φ_j − φ_i)² from the action variation tilts the double-well. At
> domain walls where ½(Δφ)² exceeds the barrier (~0.192·λ_bond), the
> ψ=0 minimum ceases to exist and the bond condenses via spinodal
> decomposition toward ψ=1. Away from domain walls, the source is
> insufficient and ψ relaxes back to zero, where it is swept by the
> decoherence floor. No noise. No seeding. The gradient decides.
```

### PATCH 07 — Replace "Candidate edge proposal" section (lines 96–108)

**DELETE lines 96–108 entirely (header, h_causal formula, BFS
discussion, walker-assisted proposal paragraph).**

**REPLACE WITH:**
```markdown
#### Bond DOF instantiation (replaces TOPO_PERIOD + 2-hop scan)

A bond DOF can only come into existence between nodes that a walker
has connected through traversal. The walker IS the causal cone (CF09:
gauge boson transport). If a walker has not traversed a path between
nodes i and j, no bond DOF exists on edge (i,j).

**Conditions for bond DOF instantiation:**
- Walker has visited both i and j during the same traversal event
- Both endpoints are observable: |φ̇_i| > 0, |φ̇_j| > 0 (CF07
  measurement condition — the gauge boson can only interact with
  nodes that have detectable dynamics)
- Edge (i,j) does not already carry a bond DOF

When all three conditions are met, the bond DOF is instantiated at
ψ_ij = 0.0 (unstable vacuum). The telegraph integrator and gradient
source ½(φ_j − φ_i)² determine whether the bond condenses or
decoheres. There is no evaluation step, no scoring, no acceptance
criterion. The walker observes; the dynamics decide.

**Observable ≠ co-active ≠ Hebbian.** The observability condition is a
measurement prerequisite (can the gauge boson see this node?), not a
force law. The force is the gradient source from the action variation.
Nodes in the same state (both φ≈1) are observable but have zero
gradient — no bond formation force. Nodes straddling a domain wall
have maximum gradient — maximum force. Bonds form at structure
boundaries, not between correlated oscillators.

**Cost:** O(N_walkers · h · k̄) per tick, where h is hops per walker
and k̄ is mean degree. For W=768, h=3, k̄~20: ~46,000 pair checks.
Only active-set nodes participate.
```

---

## §0.2 — Constants

### PATCH 08 — Replace constants table (lines 110–124)

**DELETE the entire §0.2 block from line 110 through line 124.**

**REPLACE WITH:**
```markdown
### 0.2 Parameters and CF Constraints

#### Free parameters (micro-parameters of the discrete action)

These are independent choices. Different values = different physics.
They are constrained by CF-derived relationships but not determined
by them. Analogous to choosing N and k_init — initial conditions
for a specific run.

| Name | Symbol | Value | Role |
|------|--------|-------|------|
| Nearest-neighbor coupling | J | 0.0125 | Interaction strength in action (VDM-AX-004) |
| GL barrier height (nodes) | λ | 1.0 | Double-well depth: V(φ) = λ·φ²(1−φ)² |
| M-limb damping | γ | 0.5 | Friction coefficient from dissipative bracket |
| Bond telegraph inertia | ε_bond | 200.0 | Bond mass in extended action (sets timescale separation) |
| GL barrier height (bonds) | λ_bond | 1.0 | Bond double-well: U(ψ) = λ_bond·ψ²(1−ψ)² |
| Debt throttle exponent | β_debt | 0.1 | Exponential friction per unit debt |

#### CF-derived quantities (computed, not independently chosen)

Any valid parameter choice must satisfy these. You choose J and γ;
everything else follows.

| Quantity | Expression | Value | Source |
|----------|-----------|-------|--------|
| Wave speed² | c² = 2Ja² | 0.025 | VDM-AX-C02, VDM-E-014 |
| Diffusion coefficient | D = c²/γ | 0.05 | VDM-E-050 |
| Telegraph relaxation | τ = 1/γ | 2.0 | CF04 §2.1 (Cattaneo) |
| Signal speed | c = √(D/τ) | 0.158 hops/tick | CF04 §3.1 |
| Bond relaxation | τ_bond = ε_bond·Δt² | 200 ticks | Extended action (§0.1b) |
| Effective temperature | kT = ½·Var(φ̇) | measured | CF06 §4.3 (equipartition) |
| Decoherence floor | η = √(2·kT/ε_bond) | measured (dynamic) | CF07 §4.1 |

Note: The old table listed `D (= γ) = 0.05`. D ≠ γ. D is diffusion
(0.05), γ is damping (0.5). The relationship D = c²/γ = 2Ja²/γ
connects them. Choosing J and γ determines D, τ, c, and everything
else. They cannot be chosen independently.

#### Why these specific numbers

- τ = 2.0 → telegraph oscillations ring ~2 ticks before damping
  dominates (underdamped regime, interesting dynamics)
- c ≈ 0.16 hops/tick → information crosses 10 hops in ~63 ticks
  (walker budget of 3 hops/tick is ~19× faster, consistent with CF09)
- τ_bond = 200 → bonds change ~100× slower than field (timescale
  separation for topology vs activity)
- D = 0.05 → CFL number D·Δt/a² = 0.05 (stable, well within CFL < 0.5)

These are chosen for the N=1000 runtime. Different N or deployment
target may need different values. The CF relationships must still hold.
```

---

## §0.4 — Compute/Memory/Scaling

### PATCH 09 — Fix "candidate pair" in scaling description (line 149)

**OLD:** `...draw O(s) alias samples per node, score every candidate pair, symmetrize...`
**NEW:** `...draw O(s) alias samples per node, score every pair, symmetrize...`

### PATCH 10 — Fix cost table "birth/death" + "candidates" (line 169)

**OLD:**
```
| Edge birth/death bookkeeping | O(N_events) | Sparse: only edges crossing the emergent noise floor or new candidates |
```

**NEW:**
```
| Edge condensation/decoherence | O(N_events) | Sparse: only edges crossing the decoherence floor or newly instantiated bond DOFs |
```

### PATCH 11 — Fix "Candidate edge proposal" cost line (line 173)

**OLD:**
```
**Candidate edge proposal: O(N_active · w)** where w is the mean walker
trail length per node. Walker trails provide a natural candidate list
of reachable nodes within the causal cone, eliminating the need for BFS
graph-distance computation. Evaluated every tick but only for active
nodes (|φ̇| > kT). Bounded by walker budget.
```

**NEW:**
```
**Bond DOF instantiation: O(N_active · w)** where w is the mean walker
trail length per node. Walker traversal histories define the set of
reachable pairs within the causal cone, eliminating BFS graph-distance
computation. Active-set nodes only (|φ̇| > 0). Bounded by walker budget.
```

### PATCH 12 — Remove h_causal from state arrays (line 143)

**OLD:** `All state arrays (phi_curr, phi_prev, debt, adj, psi_curr, psi_prev, h_causal) MUST be stored...`
**NEW:** `All state arrays (phi_curr, phi_prev, debt, adj, psi_curr, psi_prev) MUST be stored...`

### PATCH 13 — Remove h_causal from memory cost table (line 192)

**DELETE this row:**
```
| `h_causal` | N | int32 | 4 MB |
```

### PATCH 14 — Fix comparison table (line 390)

**OLD:** `| v3 (global rebuild) | O(N · 64) | Every node, every tick, 64 candidates |`
**NEW:** `| v3 (global rebuild) | O(N · 64) | Every node, every tick, 64 samples |`

### PATCH 15 — Fix elimination note (lines 409–410)

**OLD:**
```
- **_propose_new_edges via BFS:** Eliminated. Walker trails provide the
  candidate set directly. No graph-distance computation needed.
```

**NEW:**
```
- **_propose_new_edges via BFS:** Eliminated. Walker traversal history
  determines which pairs can instantiate bond DOFs. No graph-distance
  computation needed.
```

---

## §0.5 — Topology and Manifold Structure

### PATCH 16 — Fix bond decoherence text (line 233)

**OLD:**
```
1. **Bond death (decoherence):** When ψ_ij drops below the thermal noise floor √(2 · ε_topo · kT), the edge is removed from the adjacency list (CF07).
```

**NEW:**
```
1. **Bond decoherence:** When ψ_ij drops below the decoherence floor √(2 · kT / ε_bond), the edge is removed from the adjacency list (CF07).
```

### PATCH 17 — Fix bond "birth (nucleation)" (line 234)

**OLD:**
```
2. **Bond birth (nucleation):** Candidate edges are proposed between co-active nodes within each other's causal cone (measured in graph hops via `h_causal`). New bonds are nucleated at ψ_ij = 0.0 and must be lifted by the metriplectic dynamics (CF07).
```

**NEW:**
```
2. **Bond condensation:** When a walker (gauge boson, CF09) encounters an unconnected pair with both endpoints observable (|φ̇| > 0), a bond DOF is instantiated at the unstable vacuum ψ = 0.0. The gradient source ½(φ_j − φ_i)² drives spinodal condensation at domain walls (§0.1b). Away from domain walls, the bond decoheres.
```

---

## §0.6 — Walker-Gated Computation

### PATCH 18 — Typo "principlef" (line 242)

**OLD:** `### The principlef`
**NEW:** `### The principle`

### PATCH 19 — Zone 1 "Edge proposals evaluated" (line 286)

**OLD:**
```
of this node and its neighbors are updated. Edge proposals evaluated. Events
emitted to bus. This is where reality is being actively constructed.
```

**NEW:**
```
of this node and its neighbors are updated. Walker-observed pairs checked
for bond DOF instantiation. Events emitted to bus. This is where reality
is being actively constructed.
```

### PATCH 20 — Zone 2 description (lines 291–298)

**OLD:**
```
**ZONE 2 — WARM (walker trail decaying, above threshold)**
Reduced-frequency update. The node was recently visited; its state is still
evolving from the last interaction. Bond fields continue their telegraph
relaxation. Node field continues toward equilibrium. Update frequency scales
with trail heat: every tick while heat > WARM_HIGH, every Nth tick as heat
decays toward WARM_LOW.

Cost: O(k̄) per warm node, but executed less frequently.
```

**NEW:**
```
**ZONE 2 — WARM (neighbor of hot node, or trail score above decoherence floor)**
Full physics step, same equations as Zone 1. These nodes are in the
compute set because the Laplacian coupling requires their neighbors'
state to be current. The warm set is the boundary layer around the
active set — it exists because physics is local, not because of a
scheduling policy.

Cost: O(k̄) per warm node, every tick it remains in the compute set.
```

---

## §2 — Void_Equations.py

### PATCH 21 — Replace constants block (lines 487–496)

**OLD:**
```python
# --- Material constants (from CF chain) ---
TAU       = 2.0      # Telegraph relaxation time (CF04 §2.1)
BETA      = 0.1      # Debt throttle exponent (CF03 §7.2)
LAMBDA    = 1.0      # Double-well barrier height (CF03 §1.1)
GAMMA     = 0.05     # Diffusion coefficient D = γ (CF04 §6.1)
KT_EFF    = 0.001    # Effective temperature (CF06 §4.3)
EPS_TOPO  = 0.01     # Structural coupling constant (CF02 §4.1)

# Emergent bond noise floor (CF07)
ETA_BOND_FLOOR = float(np.sqrt(2.0 * EPS_TOPO * KT_EFF))  # sqrt(2·ε_topo·kT)
```

**NEW:**
```python
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
```

### PATCH 22 — Replace bond_potential_derivative + add bond_gradient_source (§2)

**OLD:**
```python
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
```

**NEW:**
```python
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
```

Also add `bond_gradient_source` to the adapter `__all__` list in §3.

### PATCH 23 — Replace klein_gordon_rhs (§2)

**OLD:**
```python
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
```

**NEW:**
```python
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
```

---

## §4.1 — sparse_connectome.__init__

### PATCH 24 — Replace constants import block (lines 618–627)

**OLD:**
```python
# --- Material constants (from CF chain, not tuning knobs) ---
from .void_dynamics_adapter import TAU, BETA, LAMBDA, GAMMA, KT_EFF, EPS_TOPO, ETA_BOND_FLOOR
self.tau = TAU
self.beta = BETA
self.lam = LAMBDA
self.D = GAMMA
self.kT = KT_EFF
self.eps_topo = EPS_TOPO
```

**NEW:**
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
```

Also change `self.beta` → `self.beta_debt` in all subsequent uses.

### PATCH 25 — WARM_THRESHOLD from physics (lines 637–638)

**OLD:**
```python
# Warm threshold for trail-heat gating (TODO NO HARDCODING, LET THE DYNAMICS MANAGE THIS)
self.WARM_THRESHOLD = 0.05
```

**NEW:**
```python
# Zone 2→3 boundary: same decoherence floor as bonds (CF07).
self.WARM_THRESHOLD = float(bond_decoherence_floor(self.kT))
```

### PATCH 26 — No self.rng; deterministic seed for ICs only (§4.1)

There is no RNG in the physics path. Do not initialize self.rng.

```python
# Tick counter
self._tick = 0

# Deterministic seed for initial conditions (NOT for physics noise).
self._seed = getattr(self, '_seed', 42)
```

---

## §4.3 — step()

### PATCH 27 — Fix step() signature mismatch (lines 685–693)

The §4.3 header says `def step(self, tick: int):` but the body uses
`walker_events` and `trail_scores`.

**OLD (header):** `def step(self, tick: int):`
**NEW:** `def step(self, tick: int, walker_events: list = None, trail_scores: dict = None):`

### PATCH 28 — Remove noise from node computation (lines 812–813)

**OLD:**
```python
        # Noise
        eta = np.sqrt(2.0 * self.D * self.kT) * self.rng.standard_normal()
        rhs[i] = self.D * lap - dV + eta
```

**NEW:**
```python
        rhs[i] = self.D * lap - dV
```

### PATCH 29 — Replace bond update block (lines 823–848)

**OLD:**
```python
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
```

**NEW:**
```python
    # --- Step 3: Bond field update (computed nodes only) ---
    # Bond telegraph: ε_bond·ψ̈ + ψ̇ = −U'(ψ) + ½(φ_j − φ_i)²
    # Source term from action variation (§0.1b). No noise.
    from .void_dynamics_adapter import bond_gradient_source

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
```

### PATCH 30 — Add kT measurement (insert after Step 6, ~line 860)

**INSERT between Step 6 (field history) and Step 7 (debt):**

```python
    # --- Step 6b: Measure effective temperature from dynamics ---
    # Equipartition: kT = ½·Var(φ̇) over the active set.
    # The system's own temperature, not a forcing parameter.
    if len(compute_list) > 10:
        phi_dot_active = phi_new[compute_list] - self.phi_curr[compute_list]
        measured_kT = 0.5 * float(np.var(phi_dot_active))
        self.kT = max(measured_kT, 1e-15)
```

### PATCH 31 — Fix step() comment + call for bond instantiation (lines 851–852)

**OLD:**
```python
    # --- Step 5: Edge birth from walker trails ---
    self._propose_from_trails(walker_events, phi_dot_abs)
```

**NEW:**
```python
    # --- Step 5: Bond DOF instantiation from walker observation ---
    self._instantiate_walker_observed_bonds(walker_events, phi_dot_abs)
```

---

## §4.5 — _remove_dead_edges

### PATCH 32 — Use dynamic decoherence floor

**OLD:**
```python
    from .void_dynamics_adapter import ETA_BOND_FLOOR
    nodes = range(self.N) if compute_nodes is None else compute_nodes
    for i in nodes:
        i = int(i)
        if self.adj[i].size == 0:
            continue
        alive = self.psi_curr[i] >= ETA_BOND_FLOOR
```

**NEW:**
```python
    from .void_dynamics_adapter import bond_decoherence_floor
    eta_floor = bond_decoherence_floor(self.kT)
    nodes = range(self.N) if compute_nodes is None else compute_nodes
    for i in nodes:
        i = int(i)
        if self.adj[i].size == 0:
            continue
        alive = self.psi_curr[i] >= eta_floor
```

---

## §4.6 — Bond DOF instantiation method (complete rewrite)

### PATCH 33 — Replace entire _propose_from_trails section (lines 937–1052)

**DELETE lines 937–1052 entirely** (header, old method, explanatory paragraphs).

**REPLACE WITH:**

```markdown
### 4.6 — `_instantiate_walker_observed_bonds()` — Bond DOF instantiation

This replaces `_propose_new_edges()` entirely. No BFS. No h_causal.
Walker traversal IS the causal cone. When a walker encounters an
unconnected pair with both endpoints observable, a bond DOF is
instantiated at the unstable vacuum ψ = 0.0. The telegraph integrator
and gradient source determine whether the bond condenses or decoheres.
```

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

```markdown
### Why 1-hop ego-network, not 2-hop scan:

The walker is the gauge boson (CF09). Its observation cone is the set
of nodes it has physically visited or can directly see from its current
position. At node i, the walker sees i and adj(i). It does NOT see
adj(adj(i)) — those nodes are behind a corner the walker hasn't turned.

Triangle completion within the 1-hop ego-network is the correct
operation: the walker observes that j and k are both observable and both
coupled to i, but not to each other. The shortcut j ↔ k is a bond DOF
placed at the unstable vacuum. The gradient source and telegraph
integrator determine whether it condenses or decoheres. Cost: O(k̄) per
touch, linear in mean degree.
```

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

## §6.1 — main.py

### PATCH 34a — Remove misplaced step_connectome (lines 1323–1332)

**DELETE the code block at lines 1323–1332.** Replace §6.1 with:

```markdown
### 6.1 Time variable

DELETE: `t = float(step) * dt_physics` and any float time computation.
The integer `step` counter IS the physics time. No conversion needed.
```

---

## §4.7 — Reward formula

### PATCH 34b — Remove magic number (line 1115)

**OLD:**
```python
    raw = float(-dH_dt) + 0.1 * float(fisher_speed)
```

**NEW:**
```python
    # Scale Fisher speed using measured kT as energy-information bridge.
    raw = float(-dH_dt) + self.kT * float(fisher_speed)
```

---

## Stimulus decay

### PATCH 34c — Remove magic number (lines 755, 870)

**OLD:**
```python
            self._stim *= getattr(self, "_stim_decay", 0.90)
```

**NEW:**
```python
            # Stimulus decays at telegraph rate: exp(−1/τ). CF04 §2.1.
            self._stim *= getattr(self, "_stim_decay", float(np.exp(-1.0 / self.tau)))
```

---

## §9.3 — Output nodes

### PATCH 34d — Output/input node disjointness (after PORTS block, ~line 1501)

**INSERT:**
```markdown
**Disjointness constraint:** Output node indices MUST NOT overlap with
UTE input node indices. Sensory cortex and motor cortex are anatomically
disjoint. Enforced at init:

```python
assert set(output_nodes).isdisjoint(set(ute_input_nodes)), \
    "Output and input regions must not overlap (disjoint anatomy)."
```
```

### PATCH 34e — SpeechOutputAdapter arbitrary `< 2` (line 1545)

**OLD:**
```python
        if np.sum(active_mask) < 2:
            return None  # silence — default state
```

**NEW:**
```python
        if not np.any(active_mask):
            return None  # silence — no node above thermal noise floor
```

---

## §11 — Eliminated Proxies Checklist

### PATCH 34f — Double checkbox (line 1705)

**OLD:** `- [ ] - [ ] `h_causal` as a stored state array`
**NEW:** `- [ ] `h_causal` as a stored state array`

### PATCH 34g — r_causal stale ref (line 1703)

**OLD:** `- [ ] `r_causal` as a float Euclidean radius (replaced by `h_causal` integer hops)`
**NEW:** `- [ ] `r_causal` as a float Euclidean radius (replaced by walker trail reachability)`

---

## §12 — Validation Gates

### PATCH 34h — Fix walker table (line 1196)

**OLD:**
```
| SentinelScout | Monitor structural integrity | Same — bond death/birth provides richer structural signal |
```

**NEW:**
```
| SentinelScout | Monitor structural integrity | Same — bond condensation/decoherence provides richer structural signal |
```

### PATCH 34i — Fix gate 8 (line 1727)

**OLD:**
```
8. **Bond locality:** Every bond created during the run was proposed by a walker event
```

**NEW:**
```
8. **Bond locality:** Every bond DOF instantiated during the run was observed by a walker traversal event
```

### PATCH 34j — Gate 15 testable (lines 1742–1743)

**OLD:**
```
15. **Developmental silence:** At tick 0 with randomized initial bonds,
    the output nodes are not yet coherently driven but should be left for the model to route signal to in order to learn.
```

**NEW:**
```
15. **Developmental silence:** At tick 0 with randomized initial bonds,
    the speech adapter returns None for ≥ 90% of the first 1000 ticks.
    Coherent output must be earned through bond development.
```

### PATCH 35a — Add gate 16: bond condensation validation (§12)

**INSERT after gate 15:**

```
16. **Bond condensation from gradients:** With noise removed and source
    term = ½(φ_j − φ_i)², bonds must condense at domain walls. At tick
    50000, count(ψ > 0.5) > 0. If zero bonds survive, the ratio
    λ_bond / max((φ_j−φ_i)²) is too high — domain wall gradients
    are not overcoming the barrier.
```

---

## Appendix — CF Traceability Table

### PATCH 35b — Replace traceability table (lines 1765–1776)

**OLD:**
```
| v3 Mechanism | v4 Replacement | CF Source |
|---|---|---|
| `TOPO_PERIOD = 50` (cron timer) | Bond field ψ with τ_bond = τ/ε_topo ≈ 200 (natural timescale) | CF02 §4.1: M-limb coupling ε sets dissipative timescale |
...
```

**NEW:**
```
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
```

---

# Summary

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
| **Total** | **35** | |

**The three key physics corrections:**

1. **Bond source ½(φ_j − φ_i)²** replaces the invented `ε·|φ̇_i|·|φ̇_j|`.
   Falls out of the action. Bonds form at domain walls (spatial gradients),
   not between correlated oscillators (Hebbian). Self-limiting: bond
   enables Laplacian coupling → gradient relaxes → source decreases.

2. **No injected noise.** The metriplectic split IS the noise source.
   kT is measured from what the dynamics produce, not injected.

3. **No engineering-choice language.** The walker observes. The bond DOF
   is instantiated at the unstable vacuum. The gradient source and
   telegraph integrator determine condensation or decoherence. There is
   nothing to propose, evaluate, accept, or reject.

---

**END OF CONSOLIDATED PATCH SET**
