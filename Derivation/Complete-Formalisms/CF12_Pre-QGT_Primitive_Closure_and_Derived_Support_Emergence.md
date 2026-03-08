# CF12: Complete Formalism — Pre-QGT Primitive Closure and Derived Support Emergence in VDM

**Date:** 2026-03-07
**Status:** Draft for canon integration and theorem-execution pairing
**Gap Module:** Pre-QGT primitive closure / derived support emergence (assign on merge)
**Proposer:** Justin K. Lietz
**License:** See LICENSE

---

## Executive Summary

This document formalizes the strongest currently closed VDM chain beneath the QGT: a local normalized admissible state-family with local (U(1)) redundancy, quotient/projection of the self-parallel phase direction, induced QGT, induced (g/\Omega) split, scalar-generated horizontal law, a telegraph–Kähler constitutive family with an entropy-bearing reservoir, and a derived-support theorem built from the retarded horizontal propagator. The document follows the house CF structure, which requires a derivation-owned written CF, explicit generator/evolution law, constructive mapping/decomposition, worked example specification, and a gate-driven validation section paired 1:1 with a future notebook.  

The mainline uses CF09’s state-bundle/QGT construction as the first stable geometric record of meaningful local variation, CF01’s QGT (\to) (J/M) map with degeneracy checks, CF02’s contact/GENERIC bridge, and CF11’s entropy-bearing reservoir logic and telegraph speed pressure. CF11 is explicit that the dynamical law is scalar-generated and that dissipation enters through (M) and (\Sigma), not through a covariant Lagrangian trick.   

**Contributions**

* Defines the primitive representative object and the phase/ray quotient bridge to induced geometry.
* States the induced-QGT theorem and the induced (Q \mapsto (g,\Omega)\mapsto (J,M)) map.
* Closes the primitive law at the representation-class level and adopts the scalar-generated horizontal law as the mainline class.
* Narrows the constitutive closure to a telegraph–Kähler conservative density plus an entropy-bearing reservoir family.
* States a derived-support theorem in retarded-propagator form, with explicit execution gates and falsifiers.
* Gives a canonical executable worked example using (s(u)=k_B\log u) as a representative specialization of the theorem-grade constitutive family.

---

## Canon Registries and Policies

This draft follows the house CF template: the written CF owns the derivation, registries remain authoritative for symbols/equations/validation metrics, and every measurable claim must map to explicit observables and gates. The template also requires a 1:1 notebook pairing and an acceptance checklist.  

**Registry discipline**

* Equations registry: 00_EQUATIONS
* Algorithms registry: 00_ALGORITHMS
* Validation metrics: 00_VALIDATION_METRICS
* Symbols and units: SYMBOLS / UNITS_NORMALIZATION
* I/O helper: io_paths
* Results standards and proposal template: house writeup templates 

**Policy note for this draft**
The house template discourages duplicating canonical formulas and prefers anchor-only references. Here, formulas are stated because this document is the derivation vehicle intended to seed the next canonical anchor set. Before merge, the finalized formulas should be registered and cross-linked into the equations canon. This is consistent with the template’s requirement that new derived identities introduced here later be registered as canonical anchors. 

---

## Read Me First

This CF treats the pre-QGT primitive closure as a theorem-bearing derived-limit module in the same sense that CF09 treats Berry/gauge emergence: a derivation is written in the CF, then paired with a decisive gate suite in the notebook and runner artifacts. CF09 explicitly frames its deliverable as “a publishable derivation plus a decisive gate suite,” and this draft adopts the same contract style. 

This document does **not** reopen whether support, bonds, J/M, or the QGT are deepest. Those questions are treated as already triaged for this module. The purpose here is narrower: close the pre-QGT primitive, close the constitutive family strongly enough for theorem-grade use, and state the derived-support theorem strongly enough that runtime assembly can be conditioned on passing explicit gates rather than on hand-inserted adjacency.

---

## 1. Foundations and Setting

### 1.1 Definitions

Let (M) denote an effective local domain of coarse coordinates. CF09 already uses precisely this language: “effective 3+1D spacetime (or a coarse-grained lattice approximation)” together with a normalized local low-energy state (|\psi(x)\rangle) at each (x\in M). 

Let (\pi:\mathcal H\to M) be an **effective Hilbert bundle**, meaning only the minimal local complex inner-product structure needed to define normalization, overlaps, admissible local variation, and local phase redundancy. This is **not** claimed as final micro-ontology.

A **primitive representative section** is a (C^1) section
[
\psi:M\to \mathbb S(\mathcal H),\qquad x\mapsto |\psi(x)\rangle,
]
with fiberwise normalization
[
\langle\psi(x),\psi(x)\rangle_x=1.
]

A **local admissible state-family** is the pair ((\psi,T^{\mathrm{adm}}*\psi)), where (T^{\mathrm{adm}}*\psi) is the distinguished admissible tangent class of local variations:

* local in (x),
* regular enough for projected derivatives and induced bilinear forms,
* preserved by the primitive law up to the redundancy class below.

A **reservoir field** is a local scalar (u:M\to \mathbb R_{>0}), interpreted as internal-energy / bath density. CF11’s derived-limit proxy makes this reservoir coordinate mandatory if one wants irreversible dynamics without violating energy degeneracy. 

### 1.2 Structural Forms and Identities

The primitive representative is redundant under local phase:
[
|\psi(x)\rangle \sim e^{i\Lambda(x)}|\psi(x)\rangle,
\qquad \Lambda\in C^1(M,\mathbb R).
]
CF09 identifies this as a (U(1)) principal-bundle structure over (M). 

Define the vertical/self-parallel projector
[
P_\parallel := |\psi\rangle\langle\psi|,
\qquad
P_\perp := 1 - |\psi\rangle\langle\psi|.
]

For any admissible local variation (v),
[
v=v_\parallel+v_\perp,
\qquad
v_\parallel=P_\parallel v,
\qquad
v_\perp=P_\perp v.
]

The induced QGT is
[
Q_{\mu\nu}
==========

## \langle \partial_\mu\psi|\partial_\nu\psi\rangle

\langle \partial_\mu\psi|\psi\rangle\langle\psi|\partial_\nu\psi\rangle,
]
with
[
g_{\mu\nu}=\mathrm{Re},Q_{\mu\nu},
\qquad
\Omega_{\mu\nu}=-2,\mathrm{Im},Q_{\mu\nu}.
]
This is exactly the CF09 construction and exactly what the CF01 witness computes and splits.  

### 1.3 Equilibrium / Constraint Manifolds

The primary constraint manifold is the unit-sphere bundle:
[
\mathbb S(\mathcal H)={,\psi:\langle\psi,\psi\rangle=1,}.
]

The physical state space for geometry is the quotient by local phase:
[
\mathbb P(\mathcal H)=\mathbb S(\mathcal H)/U(1).
]

The entropy-bearing sector requires
[
u>0,
\qquad
s'(u)>0,
\qquad
s''(u)<0
]
for the theorem-grade constitutive family adopted below.

The later notebook must verify:

* normalization preservation,
* quotient consistency,
* projected-variation correctness,
* strict positivity and concavity of the entropy specialization used in the worked example.

---

## 2. Generators and Evolution Law

### 2.1 Generator Definitions

The primitive representative evolution is written as
[
\dot\psi=-i,\alpha[\psi]\psi+\chi[\psi],
\qquad
\langle\psi,\chi[\psi]\rangle=0.
]

This decomposition is not a conjecture here; it is the accepted representation-class closure for norm-preserving admissible representative evolution.

### 2.2 Tangent Decomposition Derivation

Given
[
\langle\psi,\psi\rangle=1,
]
differentiate in time:
[
\frac{d}{dt}\langle\psi,\psi\rangle
===================================

# \langle\dot\psi,\psi\rangle+\langle\psi,\dot\psi\rangle

2,\mathrm{Re},\langle\psi,\dot\psi\rangle
=0.
]
Hence (\langle\psi,\dot\psi\rangle) is purely imaginary, so there exists a real scalar functional (\alpha[\psi]) such that
[
\langle\psi,\dot\psi\rangle=-,i,\alpha[\psi].
]
Define
[
\chi[\psi]:=\dot\psi+i,\alpha[\psi]\psi.
]
Then
[
\langle\psi,\chi[\psi]\rangle
=============================

# \langle\psi,\dot\psi\rangle+i,\alpha[\psi]\langle\psi,\psi\rangle

-,i,\alpha[\psi]+i,\alpha[\psi]=0.
]
Therefore
[
\dot\psi=-i,\alpha[\psi]\psi+\chi[\psi],
\qquad
\langle\psi,\chi[\psi]\rangle=0.
]
Uniqueness follows immediately by taking the inner product with (\psi).

This closes the primitive law at the representation-class level: the only remaining law freedom is the horizontal subclass (\chi), not the existence of the decomposition.

### 2.3 Scalar-Generated Horizontal Law

On the quotient/projective state manifold induced by the QGT, the surviving law class is
[
\bar\chi
========

\Omega^\sharp d\mathcal I
+
g^\sharp d\Sigma.
]
This is the local scalar-generated Kähler-metriplectic class.

This form is not chosen ad hoc. It is the only surviving class after eliminating:

* pure Hamiltonian limits as too narrow for generic dissipative closure,
* pure gradient limits as too narrow for generic Berry/holonomy closure,
* arbitrary horizontal vector fields as too broad for CF05 closure and CF11 scalar-generator discipline.

CF11 already states the axiom-core law in scalar-generator form, with degeneracy and entropy production,
[
\partial_t q = J(q),\frac{\delta\mathcal I}{\delta q}+M(q),\frac{\delta\Sigma}{\delta q},
\qquad
J,\delta\Sigma=0,\quad M,\delta\mathcal I=0,\quad \dot\Sigma\ge 0,
]
and explicitly says dissipation enters through (M) and (\Sigma), not through a dissipative covariant Lagrangian. 

### 2.4 Constitutive Family

The theorem-grade constitutive family adopted here is:
[
\mathcal I[\psi,u]
==================

\int_M\Big(
\frac{\tau}{2},|D_t\psi_\perp|*g^2
+
\frac{D}{2}\sum*{i=1}^{d}|D_i\psi_\perp|_g^2
+
V([\psi])
+
u
\Big),d\mu,
]
[
\Sigma[\psi,u]
==============

\int_M s(u),d\mu,
\qquad
s\in C^2,\quad s'(u)>0,\quad s''(u)<0.
]

Interpretation:

* (D_t\psi_\perp) and (D_i\psi_\perp) are projected local derivatives of the representative section;
* (g) is the induced quantum metric;
* (V([\psi])) is a local gauge-invariant potential on the quotient state manifold;
* (u) is the local internal-energy / bath density.

This family is the narrowest constitutive class that survives:

* CF04 finite-speed/telegraph pressure through the ((\tau,D)) principal part, 
* CF01/CF11 degeneracy and entropy-production pressure, 
* CF05 no-hidden-integrals pressure, 
* CF06/Fisher information-geometric pressure through strict concavity of (s),
* CF09’s state-bundle / gauge-order pressure. 

### 2.5 Worked-Example Specialization

The canonical executable specialization used in the worked example is
[
s(u)=k_B\log u,
\qquad u>0,
]
together with a bounded-below local symmetry-breaking potential (V([\psi])) on the quotient state manifold.

This specialization is **not** claimed as the unique theorem-grade constitutive law. It is the canonical worked example inside the surviving family.

---

## 3. Domain Identities and Thermodynamic/Geometric Relations

### 3.1 Primary Relations

This module relies on the following domain relations:

* phase/ray redundancy of normalized local representatives, as in CF09’s state bundle, 
* induced QGT from projected local variation, and its real/imaginary split into (g) and (\Omega), 
* QGT (\to) (J/M) mapping with structure checks, as embodied in the CF01 witness, 
* contact/GENERIC compatibility through (g,\Omega \to (L,M)), as embodied in the CF02 witness, 
* finite-speed telegraph/Cattaneo pressure (c=\sqrt{D/\tau}), imported through CF04/CF11, 
* entropy-bearing reservoir requirement for dissipative closure, imported through CF11’s derived-limit proxy. 

### 3.2 Derived Relations (Proof Sketches)

**Primitive (\to) quotient.**
Representative-level local states are not yet physical geometry because local phase choice is redundant. Projecting away the self-parallel direction yields the first physically meaningful local variation class.

**Quotient (\to) QGT.**
The projected bilinear form on local variation is the QGT. The subtraction term in the QGT is exactly the removal of the phase/self-parallel direction. CF01’s witness implements this explicitly with optional parallel-transport gauge fixing before computing (Q). 

**QGT (\to) (g,\Omega).**
The QGT is Hermitian; its real part is the metric, its imaginary part the Berry-curvature sector. The CF01 witness exposes this split as (g=\mathrm{Re}(Q)) and (\Omega=-2,\mathrm{Im}(Q)), and verifies Hermiticity of (Q) and PSD of (g). 

**((g,\Omega)\to(J,M)).**
The current witness takes (M=g^{-1}) (or pseudo-inverse/regularized inverse on singular leaves) and (J=\Omega^{+}) on nondegenerate leaves, then verifies the degeneracy conditions against supplied gradients of the invariant and entropy-like quantities. 

**Reservoir logic.**
CF11 shows why an extra reservoir coordinate is required: without it, damping drains the energy functional and breaks (M,\delta\mathcal I=0). Adding (u) allows the energy-like functional and entropy functional to coexist with a positive semidefinite metric operator and explicit entropy production. 

### 3.3 Measurement / Observable Map

The template requires every measurable statement to map to observables and gates. 

Main observables for this CF:

* (N_\psi(x,t)=\langle\psi,\psi\rangle) — normalization, dimensionless.
* (R_{U(1)}) — gauge-residual norm under local phase changes, dimensionless.
* (Q_{\mu\nu}), (g_{\mu\nu}), (\Omega_{\mu\nu}) — induced geometric observables, dimensionless in normalized units or per units registry.
* (r_J=|J\nabla\Sigma|_2), (r_M=|M\nabla\mathcal I|_2) — degeneracy residuals.
* (\dot\Sigma) — entropy-production density / integral.
* (G_R(t,t_0)) — retarded horizontal propagator.
* (\mathrm{Supp}(t;t_0,x_0)) — derived support set.
* overlap/plaquette/Wilson observables on the derived support neighborhood for downstream gauge readiness.

---

## 4. Mapping and Decomposition

### 4.1 Structure Checks

The template requires structure properties to be named and paired with gates. 

**QGT structure checks**

* (Q^\dagger=Q)
* (g) symmetric positive semidefinite
* (\Omega) antisymmetric

These are already explicit in the CF01 witness. 

**Generator structure checks**

* (J^\top=-J)
* (M^\top=M\ge 0)
* scalar-generated law form

These are already explicit in CF11 and the CF02/CF01 witnesses.  

### 4.2 Degeneracy Conditions

The degeneracy conditions are:
[
J,\delta\Sigma=0,
\qquad
M,\delta\mathcal I=0.
]
They are explicitly checked in the CF01 witness through `verify_degeneracy_J` and `verify_degeneracy_M`, and in the CF02 witness through `construct_generic_evolution` with (L\nabla S=0) and (M\nabla E=0).  

### 4.3 Mapping Residuals

The paired notebook must summarize:

* QGT gauge-fixing residuals,
* Hermiticity and PSD residuals,
* degeneracy residuals,
* contact-form and GENERIC mapping residuals,
* support extraction stability metrics.

No code belongs here; the template requires these to be specified as notebook/reporter outputs rather than implemented in prose. 

---

## 5. Constructive Algorithm

The template calls for an implementation-agnostic algorithm with inputs, steps, outputs, and gate mappings. 

### Inputs

* local representative section ( \psi(x,t) ),
* reservoir field (u(x,t)),
* admissible coordinate charts on (M),
* constitutive parameters ((\tau,D)),
* chosen local potential (V([\psi])),
* entropy specialization (s(u)) for the worked example,
* gauge-fixing choice for notebook diagnostics (optional; physics must remain gauge invariant).

### Steps

1. **Primitive representative update**
   Evolve ((\psi,u)) under
   [
   \dot\psi=-i\alpha[\psi]\psi+\chi[\psi],
   \qquad
   \bar\chi=\Omega^\sharp d\mathcal I + g^\sharp d\Sigma.
   ]

2. **Projected variation construction**
   Compute horizontal local derivatives with (P_\perp).

3. **QGT construction**
   Build (Q_{\mu\nu}) from projected variation.

4. **Metric/curvature split**
   Extract (g,\Omega).

5. **Metriplectic map**
   Build (J,M) and evaluate degeneracy residuals.

6. **Retarded-propagator support extraction**
   Construct the retarded horizontal propagator (G_R(t,t_0)) along the actual trajectory and define support from its kernel support, not from inserted adjacency.

7. **Gauge-readiness check on derived support**
   On the derived support neighborhoods, evaluate overlap-based link variables and plaquette/Wilson constructions for downstream CF09 compatibility.

8. **Emit observables**
   Emit JSON/CSV/plot artifacts for normalization, gauge invariance, QGT residuals, degeneracy, entropy production, support stability, cone inclusion, and downstream gauge readiness.

### Outputs

* (Q,g,\Omega,J,M) fields / summaries,
* degeneracy residual logs,
* entropy-production logs,
* retarded-support artifacts,
* overlap/plaquette/Wilson diagnostics on derived support,
* pass/fail gate metadata.

---

## 6. Worked Example (Specification)

The template requires a minimal executable worked example specification with parameters, expected behavior, and data products. 

### Worked Example: Telegraph–Kähler + Log-Entropy Reservoir

#### Constitutive specialization

[
\mathcal I_{\mathrm{ex}}[\psi,u]
================================

\int_M\Big(
\frac{\tau}{2},|D_t\psi_\perp|*g^2
+
\frac{D}{2}\sum*{i=1}^{d}|D_i\psi_\perp|*g^2
+
V([\psi])
+
u
\Big),d\mu,
]
[
\Sigma*{\mathrm{ex}}[\psi,u]
============================

k_B\int_M \log u,d\mu,
\qquad u>0.
]

#### Parameter table

| Parameter               | Meaning                        |                       Units | Example role                        |
| ----------------------- | ------------------------------ | --------------------------: | ----------------------------------- |
| (\tau)                  | relaxation timescale           |                        time | sets telegraph damping / cone speed |
| (D)                     | transport coefficient          |             length(^2)/time | sets telegraph cone speed           |
| (k_B)                   | entropy scale                  | entropy / temperature units | entropy normalization               |
| (V) parameters          | local quotient-state potential |          per units registry | phase-structure control             |
| (u_0)                   | initial reservoir profile      |              energy density | entropy-bearing background          |
| chart resolution / grid | notebook discretization only   |          per units registry | validation sweep                    |

#### Expected qualitative behavior

* normalization preserved up to representative redundancy,
* QGT gauge invariance under local phase re-representation,
* (g) PSD and (\Omega) antisymmetric,
* (J\nabla\Sigma\approx 0), (M\nabla\mathcal I\approx 0),
* (\dot\Sigma\ge 0),
* retarded support inside telegraph cone,
* support-derived neighborhoods sufficient for overlap-based gauge readiness.

#### Data products

* QGT residual tables,
* degeneracy residual tables,
* entropy-production traces,
* support-kernel visualizations / support masks,
* cone-inclusion diagnostics,
* overlap/plaquette/Wilson diagnostics on derived support.

---

## 7. Advanced Topics (Pointers Only)

* Non-abelian gauge extensions beyond (U(1)) require additional bundle structure and are not claimed here, consistent with CF09’s own non-claims. 
* Schrödingerization/KvN lifting remains an advanced compatibility topic, not a primitive-law claim in this draft.
* Spectral J/M mode splits for cosmology remain downstream derived-limit analyses, not primitive ontology, consistent with CF11’s mode-projection language. 

---

## 8. Integration with VDM Unification

This CF sits beneath and feeds:

* CF09, by supplying the pre-QGT primitive and the derived support neighborhoods on which overlap-based connection and plaquette constructions may be built, 
* CF01/CF02, by giving the primitive route into QGT and then into (J/M) and GENERIC/contact structure,  
* CF11, by supplying the stronger pre-cosmology closure and the theorem-grade justification for the energy-like/reservoir entropy pair already used in its derived-limit proxy. 

This document should therefore be understood as a pre-QGT primitive closure module that underwrites the existing QGT/metriplectic/gauge/cosmology stack rather than replacing it.

---

## 9. Validation and Consistency

The template requires precise gates, observables, and acceptance logic. 

### 9.1 Mathematical Consistency

#### C-G1 Conservative-density gate

**Observable:** principal-symbol diagnostics of (\mathcal I); extracted characteristic speed (c_{\mathrm{num}}).
**Validates:** locality + telegraph principal part.
**Pass condition:** (c_{\mathrm{num}}) matches the declared telegraph relation (c=\sqrt{D/\tau}) within the validation tolerance band.
**Failure falsifies:** the claimed telegraph–Kähler conservative density.
Basis: CF04/CF11 finite-speed relation.  

#### C-G2 Reservoir-degeneracy gate

**Observable:** (r_M=|M\nabla\mathcal I|_2), (r_J=|J\nabla\Sigma|_2), (\dot\Sigma).
**Validates:** exact metriplectic degeneracy and entropy production.
**Pass condition:** both residuals within tolerance and (\dot\Sigma\ge 0).
**Failure falsifies:** the constitutive pair ((\mathcal I,\Sigma)).
Basis: CF01 witness, CF11 proxy.  

#### C-G3 Strict-concavity/Fisher gate

**Observable:** (s'(u)), (s''(u)), one-dimensional Hessian statistics of the entropy sector.
**Validates:** strict monotonicity and strict concavity of the entropy-bearing family.
**Pass condition:** (s'(u)>0) and (s''(u)<0) on the tested domain.
**Failure falsifies:** the claim that the chosen specialization lies inside the theorem-grade constitutive family.

#### C-G4 No-hidden-integrals gate

**Observable:** extra-Casimir/integral search residuals from the closure witness.
**Validates:** absence of undeclared conserved structures.
**Pass condition:** no extra independent integrals beyond the declared invariant/entropy structure.
**Failure falsifies:** primitive-law closure.
Basis: CF05 closure witness. 

### 9.2 Physical Consistency

#### S-G1 Kernel-defined support gate

**Observable:** retarded horizontal propagator (G_R(t,t_0)), exact support masks.
**Validates:** support is derived from primitive evolution, not inserted by hand.
**Failure falsifies:** the main derived-support claim.

#### S-G2 Gauge-invariant support gate

**Observable:** support masks under multiple local representative/gauge choices.
**Validates:** support invariance under (U(1)) redundancy.
**Failure falsifies:** support as a physical quotient object.

#### S-G3 Cone gate

**Observable:** derived support envelope vs telegraph cone.
**Validates:** finite-speed locality of support emergence.
**Pass condition:** support remains inside the declared cone except where the chosen hierarchy throttle law explicitly modifies the effective speed.
**Failure falsifies:** the retarded-support theorem.
Basis: CF04/CF11 and spec-level speed anchors.  

#### S-G4 Separating-observable recovery gate

**Observable:** support recovered from a separating family of local gauge-invariant observables.
**Validates:** observable-independence of the theorem-grade support object.
**Failure falsifies:** support robustness.

#### S-G5 Gauge-structure-hosting gate

**Observable:** overlap-based link variables, plaquette phases, Wilson-loop residuals on derived support neighborhoods.
**Validates:** derived support is strong enough to host CF09 downstream gauge constructions.
**Failure falsifies:** support sufficiency for force-sector emergence.
Basis: CF09’s gauge deliverable and gates.  

#### S-G6 Runtime sufficiency gate

**Observable:** whether support can be recomputed from primitive evolution without pre-hard-coded adjacency.
**Validates:** runtime unlock condition.
**Failure falsifies:** honest runtime assembly from this CF.

### 9.3 Numerical Validation (Notebook Pairing)

The paired notebook must:

* sweep ((\tau,D)) and the worked-example (V)-parameters,
* compare gauge choices,
* compute QGT residuals and degeneracy residuals,
* construct (G_R) along trajectories,
* report support stability and cone inclusion,
* and emit JSON/CSV/figure artifacts for all C-G* and S-G* gates.

### 9.4 Lattice–Exactness & UQ Gates (Optional)

If the execution notebook uses stochastic sampling or large sparse solvers, adopt the optional UQ pack from the template:

* acceptance and (\Delta H) diagnostics,
* autocorrelation/binning,
* correlated fits and SVD stability,
* solver residual logging.
  These are optional execution-quality add-ons, not part of the primitive derivation itself.  

---

## Assumptions and Limitations

1. **Effective Hilbert fiber assumption.**
   This draft does **not** claim the effective Hilbert bundle is the final micro-ontology. It is the minimal pre-QGT carrier.

2. **Entropy-family non-uniqueness.**
   The theorem-grade constitutive result is the family (s\in C^2,\ s'>0,\ s''<0). The specialization (s(u)=k_B\log u) is a worked example, not a uniquely forced theorem-level statement.

3. **Support theorem execution still required.**
   This draft states the derived-support theorem as mainline, but it is not considered *validated* until the S-G* gates pass in the paired notebook and runner artifacts.

4. **Low-momentum / effective-domain scope.**
   As in CF09, the formalism is effective/derived-limit. Lorentz invariance is not assumed at the microscopic scale; only an auditable low-momentum isotropy/locality window is required. 

5. **Runtime not validated by writing alone.**
   Runtime assembly is conditionally unlocked only by gate execution, not by this document’s existence.

---

## 10. References

Internal canon references should dominate the final merged version. External references are used here only where they sharpen the representative/ray quotient, QGT/Fubini–Study geometry, or GENERIC/contact mathematics. CF09 itself explicitly adopts the same practice: standard Berry/Provost–Vallée/Wilson/Kogut results are used as mathematical tools while the claims remain VDM-gated. 

---

## Appendix A: Symbol Definitions

New symbols introduced here that should be registered if accepted:

* (P_\parallel, P_\perp): vertical/horizontal projectors on representative tangent space
* (D_t\psi_\perp, D_i\psi_\perp): projected local derivatives of the representative section
* (G_R(t,t_0)): retarded horizontal propagator
* (\mathrm{Supp}(t;t_0,x_0)): derived support set
* C-G1…C-G4, S-G1…S-G6: constitutive/support gate labels

---

## Appendix B: Notebook Pairing & Traceability

**Paired notebook:** CFx — Pre-QGT Primitive Closure and Derived Support Emergence (title to assign on notebook creation)

**1:1 mapping promise**
Every numbered section above is to have a corresponding notebook section with executable meters and commentary, matching the template requirement exactly.  

**Traceability map (initial draft)**

| CF Section | Notebook Tag | Meters / Gates               | Observables                                       |
| ---------- | ------------ | ---------------------------- | ------------------------------------------------- |
| 1.1–1.3    | `cfx-1`      | A1/A2 structural checks      | (N_\psi, R_{U(1)})                                |
| 2.2        | `cfx-2-2`    | tangent decomposition checks | (\alpha,\chi,\langle\psi,\chi\rangle)             |
| 2.4        | `cfx-2-4`    | C-G1…C-G4                    | (c_{\mathrm{num}}, r_J, r_M, \dot\Sigma)          |
| 4          | `cfx-4`      | QGT/JM/contact bridge checks | (Q,g,\Omega,J,M)                                  |
| 9.2        | `cfx-9-2`    | S-G1…S-G6                    | (G_R,\mathrm{Supp}), plaquette/Wilson diagnostics |

---

## Acceptance Checklist

* [ ] All sections completed and numbered 1:1 with the paired notebook.
* [ ] New equations/symbols proposed for registry anchoring before merge.
* [ ] All claims mapped to observables and gates.
* [ ] Worked example specified without code or plots.
* [ ] Support theorem paired with S-G* gate suite.
* [ ] Runtime unlock criteria stated explicitly.
* [ ] Provenance entry prepared for CHRONICLES after merge.

---

## Runtime Unlock Criteria

Runtime assembly is honestly justified **only if all of the following are true**:

1. the primitive representative/quotient/QGT/JM chain is implemented without hardening support or bonds as primitive;
2. the constitutive gates C-G1…C-G4 pass;
3. the support gates S-G1…S-G6 pass;
4. support is recomputed from primitive evolution / the retarded horizontal propagator, not inserted as fixed adjacency;
5. no hidden integrals, gauge inconsistencies, or cone violations appear.

If any of these fail, the runtime is **not** unlocked by this CF.

---

## Explicit Non-Claims

This CF does **not** claim:

* that the effective Hilbert fiber is the final micro-ontology;
* that (s(u)=k_B\log u) is uniquely forced at theorem grade;
* that support emergence is validated prior to execution of S-G1…S-G6;
* that runtime validity follows automatically from a written formalism;
* that non-abelian gauge structure is closed here;
* that the cosmological CF11 split is primitive rather than derived-limit bookkeeping. CF11 itself is explicit that it is a derived-limit module built on axiom-core metriplectic structure. 

---

## CF Status Note

**1. What is theorem-grade in this draft**

* primitive representative setting with local (U(1)) redundancy,
* quotient/projection of the self-parallel phase direction,
* induced QGT and its (g/\Omega) split,
* tangent decomposition of norm-preserving representative evolution,
* scalar-generated law class as the mainline structural closure.

**2. What is constitutive-family-level rather than uniquely specialized**

* the theorem-grade constitutive family
  [
  \mathcal I=\int(\text{telegraph–Kähler local density}+u),d\mu,\qquad
  \Sigma=\int s(u),d\mu,\ s'>0,\ s''<0
  ]
  is closed as a family, but the specialization (s(u)=k_B\log u) is only the worked example.

**3. What execution/validation tasks remain**

* execute C-G1…C-G4 and S-G1…S-G6,
* promote witness-level QGT→JM/contact results to notebook-verified artifacts,
* test support extraction from (G_R) without inserted adjacency,
* verify downstream overlap/plaquette/Wilson readiness on derived support.

**4. Runtime status**

* The runtime is **conditionally unlocked**, not validated.
  It becomes honestly unlocked **only if** the stated gates pass and support is derived from primitive evolution rather than hard-coded.

That is the current status of this CF draft under the closure results available so far.
