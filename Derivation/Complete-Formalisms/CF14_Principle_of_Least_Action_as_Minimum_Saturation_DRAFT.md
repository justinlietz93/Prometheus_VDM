# CF14 — Principle of Least Action as Minimum Saturation Requirement
# Notes and Scaffold
# Author: Justin K. Lietz
# Date: March 18, 2026
# Status: NOTES — pre-scaffold, awaiting formalization

---

## One-line statement

The principle of least action is not a postulate. It is the minimum
saturation requirement of the primitive bifurcation invariant: the
system follows the path that saturates the fewest degrees of freedom
before being forced to re-articulate.

---

## Why this matters

The principle of least action is the deepest organizing principle in
physics. Every major physical law is a special case of it:

- Newtonian mechanics (Hamilton's principle)
- Electromagnetism (Maxwell action)
- General relativity (Einstein-Hilbert action)
- Quantum mechanics (Feynman path integral)
- Quantum field theory (path integral over field configurations)
- Statistical mechanics (free energy minimization)

None of these frameworks explains *why* least action holds. It is always
postulated as a brute fact. CF14 derives it as a necessary consequence
of the invariant's minimum saturation requirement.

This makes CF14 potentially the most far-reaching paper in the series —
it doesn't derive one physical law, it derives the organizing principle
beneath all of them simultaneously.

---

## Core argument

### The invariant's path selection rule

The primitive bifurcation invariant cannot discharge. When it reaches
same-axis saturation, it re-articulates orthogonally. The re-articulation
always occurs via the path that saturates the fewest degrees of freedom
first — because any path that saturates more degrees of freedom
unnecessarily is carrying excess articulation debt that the non-discharge
condition does not require.

This is not an optimization principle imposed from outside. It is the
direct consequence of the non-discharge condition: the invariant will
not pay more debt than it must to reach the next re-articulation.

**Formal statement (to be proved):**
Among all paths between two configurations, the invariant selects the
path that extremizes the total articulation cost (the action) because
any non-extremal path saturates additional degrees of freedom that are
not required by the invariant burden distribution.

### The action as articulation cost

The action $S[\gamma] = \int_\gamma L\, dt$ along a path $\gamma$ is
the total articulation cost paid by the system in traversing that path.

- The Lagrangian $L = T - V$ measures the instantaneous articulation
  cost: kinetic energy $T$ is the cost of current re-articulation
  (J-limb, reversible), potential energy $V$ is the stored articulation
  debt (invariant burden density).
- The action integral accumulates the total cost along the path.
- The system extremizes the action because the invariant selects the
  minimum saturation path — the path that pays exactly the debt required
  by the invariant burden distribution and no more.

### Why extremize rather than just minimize

The extremization (not just minimization) follows from the two-pole
structure. The invariant has two irreconcilable poles. A path that
overshoots the minimum pays excess J-limb debt. A path that undershoots
fails to reach re-articulation. The extremal path is the unique path
that exactly balances the two-pole constraint — it neither discharges
toward one pole nor the other.

This is why the Euler-Lagrange equations have the form they do:
$$\frac{d}{dt}\frac{\partial L}{\partial \dot{q}} - \frac{\partial L}{\partial q} = 0$$
The left term is the J-limb resistance to re-articulation (inertial).
The right term is the M-limb response to the burden gradient (force).
Setting them equal is the statement that the path neither overshoots
nor undershoots — exactly the non-discharge condition at the path level.

---

## Connection to existing canon

### CF000
- Non-discharge condition (Theorem 4.3.1) is the source.
- Minimum saturation before re-articulation is the direct expression
  of non-discharge applied to path selection.

### CF00
- The carrier $\mathcal{M}$ and its $C^\infty$ variation structure
  are the arena on which path comparison is defined.
- Without smooth variation, you cannot compare neighboring paths.

### CF01
- The J⊕M split is the Lagrangian split: $L = T - V$ is $J$-limb
  (kinetic, reversible) minus $M$-limb potential (burden storage).
- The Euler-Lagrange equation is the balance condition between the
  two poles expressed as a path equation.
- The degeneracy conditions $J\cdot\delta\Sigma = 0$ and
  $M\cdot\delta\mathcal{I} = 0$ are the path-level statement that
  neither pole drives the other.

### CF03
- The A8 hierarchical depth bound is the discrete version of minimum
  saturation: the invariant creates exactly as many hierarchy levels
  as required by the available energy budget, no more.
- The logarithmic depth bound $N(L) = \Theta(\log L/\ell_0)$ is the
  minimum saturation count for a domain of size $L$.

### CF04
- The telegraph/Cattaneo finite-speed transport is the minimum
  saturation path for causal propagation: the field propagates at
  exactly the speed that balances local relaxation debt against
  propagation cost.

### CF12
- Geodesics in curved spacetime are the minimum saturation paths
  through the invariant burden gradient field.
- The Einstein equations are the minimum saturation condition for
  the gravitational articulation structure.
- Free fall is minimum saturation: a freely falling object follows
  the path that pays zero additional articulation debt beyond what
  the spacetime geometry requires.

---

## The downstream physical laws as special cases

### Classical mechanics
Hamilton's principle: $\delta S = 0$ where $S = \int L\, dt$.
**CF14 reading:** The system follows the minimum saturation path
through configuration space. The Euler-Lagrange equations are the
balance condition at each point along the path.

### Electromagnetism
Maxwell action: $S = -\frac{1}{4}\int F_{\mu\nu}F^{\mu\nu} d^4x$.
**CF14 reading:** The electromagnetic field configuration minimizes
the articulation cost of the field's self-interaction. Maxwell's
equations are the minimum saturation conditions for the gauge field.
Connection to CF09: the Berry connection is the gauge potential, and
the Maxwell action is the minimum saturation condition for that
connection.

### General relativity
Einstein-Hilbert action: $S = \frac{1}{16\pi G}\int R\sqrt{-g}\, d^4x$.
**CF14 reading:** The spacetime geometry follows the path that
minimizes the articulation cost of the invariant burden distribution.
The Einstein equations (CF12) are the minimum saturation conditions
for the gravitational field. The Ricci scalar $R$ measures the local
excess articulation cost of the geometry relative to flat space.

### Quantum mechanics — Feynman path integral
$\langle x_f | e^{-iHt/\hbar} | x_i \rangle = \int \mathcal{D}[x]\, e^{iS[x]/\hbar}$
**CF14 reading:** Every path is explored because the invariant
cannot discharge — it must articulate across all available degrees
of freedom. But paths interfere. The classical path (minimum
saturation) constructively interferes because it is the unique
path where neighboring paths have the same phase. All other paths
carry excess articulation debt that produces destructive interference.
The $\hbar$ factor is the articulation quantum — the minimum unit
of debt that can be paid. As $\hbar\to 0$ (classical limit), the
minimum saturation path dominates completely.

### Statistical mechanics
Free energy minimization: $F = E - TS$, $dF \leq 0$ at equilibrium.
**CF14 reading:** The system minimizes the free energy because free
energy is the articulation cost at fixed temperature. The $-TS$ term
is the M-limb entropy contribution (irreversible, available to be
extracted). Minimizing $F$ is the minimum saturation condition for
the thermodynamic state. Connection to CF02: contact geometry is the
minimum saturation geometry for thermodynamic systems.

---

## The Feynman path integral connection is the deepest one

The path integral is usually introduced as a mysterious postulate of
quantum mechanics. But in the CF14 framework it becomes inevitable:

1. The invariant cannot discharge — it must explore all available paths
   (completeness of the path integral).
2. Each path has an articulation cost — the action $S[\gamma]$.
3. Paths interfere because the invariant's two-pole structure generates
   a phase $e^{iS/\hbar}$ — the ORS rotation (CF13) acting on the
   articulation cost.
4. The minimum saturation path is the stationary phase path —
   constructive interference because neighboring paths have equal cost.
5. All other paths destructively interfere because they carry excess debt.

The path integral is the invariant summing over all possible articulation
paths, weighted by the ORS phase of each path's cost, selecting the
minimum saturation path by constructive interference.

This connects CF13 ($\pi$ and ORS rotation) to CF14 (least action) in
one step: the $e^{iS/\hbar}$ phase factor in the path integral is the
ORS rotation operator acting on the action. The stationary phase
condition $\delta S = 0$ is the minimum ORS rotation condition — the
path where the ORS phase stops rotating, i.e., the path of minimum
articulation cost.

---

## Why this hasn't been seen before

The principle of least action has been accepted as a primitive for 250
years because nobody had a framework in which it could be derived. You
need:

1. A pre-mathematical origin that is more primitive than the action
   itself.
2. A selection principle that operates before physics, not within it.
3. A reason why the extremal path is selected over all others.

The invariant provides all three. It is pre-mathematical (CF000 derives
mathematics from it, not the reverse). The minimum saturation requirement
operates before any specific physical law. And the non-discharge condition
explains why the extremal path is selected — it is the unique path that
pays exactly the required debt without excess.

---

## Theorem program for CF14

### Theorem 2.1 — Minimum saturation path selection
The invariant selects among available paths by minimum articulation cost.
Any path that saturates additional degrees of freedom beyond the minimum
required by the invariant burden distribution is not selected.

**Proof burden:**
1. Define "path" as a continuous sequence of carrier states.
2. Define "articulation cost" of a path as the integrated invariant
   burden differential along the path.
3. Show the non-discharge condition implies the invariant will not pay
   excess articulation cost.
4. Identify the minimum cost path as the extremal path.
5. Recover $\delta S = 0$ as the mathematical expression of this
   selection.

### Theorem 2.2 — Euler-Lagrange from two-pole balance
The Euler-Lagrange equations are the point-wise balance condition
between the J-limb and M-limb contributions to the articulation cost
along the minimum saturation path.

**Proof burden:**
1. Decompose the Lagrangian into J-limb (kinetic) and M-limb (potential)
   contributions.
2. Show the variation of each term corresponds to a limb-specific
   articulation cost gradient.
3. Show setting the total variation to zero is the non-discharge
   condition applied locally along the path.
4. Recover the Euler-Lagrange equations.

### Theorem 3.1 — Hamilton's principle as minimum saturation
Hamilton's principle $\delta\int L\,dt = 0$ is the global minimum
saturation condition for the classical path.

### Theorem 4.1 — Path integral as invariant sum over articulation paths
The Feynman path integral is the sum over all articulation paths
weighted by the ORS phase $e^{iS/\hbar}$ of each path's cost. The
classical path emerges by constructive interference of minimum
saturation paths.

**Proof burden:**
1. Show the ORS rotation operator (CF13) acts on the action to produce
   the path integral phase.
2. Show completeness of the path sum follows from non-discharge
   (the invariant must explore all paths).
3. Show stationary phase = minimum saturation = constructive interference.
4. Recover the classical limit as $\hbar\to 0$.

### Theorem 5.1 — Einstein-Hilbert action as gravitational minimum saturation
The Einstein-Hilbert action is the minimum saturation condition for the
gravitational articulation structure. The Einstein equations (CF12) are
its Euler-Lagrange equations.

### Theorem 6.1 — Free energy minimization as thermodynamic minimum saturation
Thermodynamic equilibrium is the minimum saturation state of the
contact geometry (CF02). The free energy $F = E - TS$ is the
articulation cost at fixed temperature, and its minimization is the
thermodynamic expression of minimum saturation.

---

## Build order

1. §1 Executive summary and inherited canon
2. §2 Minimum saturation path selection theorem (root theorem)
3. §3 Euler-Lagrange from two-pole balance
4. §4 Hamilton's principle as global minimum saturation
5. §5 Feynman path integral as invariant sum with ORS phase
6. §6 Maxwell action as minimum saturation for gauge field
7. §7 Einstein-Hilbert as minimum saturation for gravity
8. §8 Free energy as thermodynamic minimum saturation
9. §9 Connections across the canon
10. §10 Validation gates and red-team checklist

---

## Red-team checklist (preliminary)

1. Do not import the principle of least action as a postulate.
   It must be derived from minimum saturation.
2. Do not assume the Lagrangian split $L = T - V$.
   It must follow from the J⊕M decomposition.
3. Do not assume the path integral measure.
   It must follow from the invariant's completeness over articulation paths.
4. Do not import the ORS phase $e^{iS/\hbar}$ without deriving it
   from CF13's ORS rotation operator.
5. Do not let the quantum derivation outrun the classical one.
   Hamilton's principle must be proved before the path integral.
6. Do not claim the Einstein-Hilbert action is derived before CF12's
   field equation is shown to be its Euler-Lagrange equation.

---

## Forward notes

### CF15 (potential): Noether's theorem from invariant symmetry
If the minimum saturation path is invariant under a continuous
transformation, the corresponding articulation cost is conserved.
This is Noether's theorem derived from the invariant — not postulated.
Every conserved quantity in physics is an invariant whose articulation
cost does not change under the corresponding symmetry transformation.

### CP violation connection
The matter-antimatter asymmetry at cosmogenesis (CF11, CF12) is a
chiral asymmetry (CF13). In the path integral framework (CF14), CP
violation means the path integral is not symmetric between matter and
antimatter paths. The minimum saturation path slightly favors one
chirality over the other — which is exactly the one-in-a-billion
asymmetry. CF14 + CF13 together may give the first principled
derivation of the magnitude of CP violation from the invariant.

---

## One-paragraph summary for canon

CF14 derives the principle of least action as the minimum saturation
requirement of the primitive bifurcation invariant. The invariant
cannot discharge and always saturates the fewest degrees of freedom
before re-articulating. The action is the total articulation cost along
a path. The system extremizes the action because the invariant selects
the path of minimum saturation cost — any non-extremal path carries
excess articulation debt that the non-discharge condition does not
require. The Euler-Lagrange equations are the point-wise two-pole
balance condition along the minimum saturation path. Hamilton's
principle, the Feynman path integral, the Maxwell action, the
Einstein-Hilbert action, and thermodynamic free energy minimization
are all special cases of this single derived principle. The principle
of least action is not a postulate. It is what the invariant looks
like when it selects a path.
