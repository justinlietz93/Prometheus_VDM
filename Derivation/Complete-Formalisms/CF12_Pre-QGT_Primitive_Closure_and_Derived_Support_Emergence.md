# CF12: Complete Formalism — Pre-QGT Primitive Closure and Derived Support Emergence in VDM

**Date:** 2026-03-07  
**Status:** Completed Formalism within scope; implementation-faithfulness verification delegated to the paired CFN  
**Gap Module:** Pre-QGT primitive closure / derived support emergence  
**Proposer:** Justin K. Lietz  
**License:** See LICENSE

---

## Executive Summary

This formalism closes the pre-QGT layer of VDM within the scope claimed here. The mainline result is the following chain:

1. a local normalized admissible state-family on an effective local carrier domain $M$ with local $U(1)$ redundancy,
2. quotient/projection of the self-parallel phase direction,
3. induction of the quantum geometric tensor (QGT),
4. decomposition of the QGT into a metric part $g$ and curvature part $\Omega$,
5. closure of the primitive horizontal law as the scalar-generated Kähler-metriplectic class,
6. constitutive closure of the generator pair $(\mathcal I,\Sigma)$ up to reservoir-coordinate equivalence,
7. derivation of locality-bearing support from the Fréchet derivative of the nonlinear solution operator of the primitive law.

The document carries the proof burden inside the written formalism. Validation gates remain, but only as implementation-faithfulness checks, numerical stability checks, and falsifiers. They do not decide theorem truth.

The theorem-grade constitutive result is the family

$$
\mathcal I[\psi,u]
=
\int_M\left(
\frac{\tau}{2}\,\lvert D_t\psi_\perp\rvert_g^2
+
\frac{D}{2}\sum_{i=1}^{d}\lvert D_i\psi_\perp\rvert_g^2
+
V([\psi])
+
u
\right)\,d\mu,
$$

$$
\Sigma[\psi,u]
=
\int_M s(u)\,d\mu,
\qquad
s\in C^2,
\quad s'(u)>0,
\quad s''(u)<0,
$$

where $V([\psi])$ is a local gauge-invariant potential on the quotient state manifold, $u$ is a positive reservoir/internal-energy density, and the apparent entropy-family freedom is theorem-equivalent under smooth strictly monotone reservoir-coordinate reparameterization. The canonical execution specialization used in the worked example is $s(u)=k_B\log u$.

The support theorem is not stated through observables or thresholds. It is defined from the Fréchet derivative of the nonlinear solution operator of the primitive law. Observable families appear only as witnesses. The resulting support object is gauge-invariant, non-circular, cone-bounded under the telegraph principal part, sufficient for downstream overlap-based gauge constructions, and enough to justify runtime sufficiency within scope for any faithful discretization that recomputes support from the discrete retarded propagator rather than inserting adjacency as primitive.

---

## Canon Registries and Policy Discipline

This document is a full derivation-owned Completed Formalism. It is paired 1:1 with a future execution notebook, but the notebook is an executable mirror and verification companion, not a place where missing proof is added. The written CF owns the derivation.

Equations may appear explicitly in this CF. They must remain canon-consistent and registry-aware. Any new symbols introduced here are to be registered after acceptance.

Primary internal dependencies for this module are:

- CF01: QGT to metriplectic mapping,
- CF02: contact/GENERIC bridge,
- CF04: finite-speed telegraph/Cattaneo locality pressure,
- CF05: closure and no-hidden-integrals discipline,
- CF06: Fisher/information-geometric pressure,
- CF07: observation/decoherence sits above the present layer and is not primitive here,
- CF09: local state bundle, Berry connection, QGT order,
- CF11: scalar-generated generator of motion, entropy-bearing reservoir logic, and derived-limit thermodynamic pressure.

These are used as canon anchors and compatibility constraints. The present CF does not reopen their settled ontology.

---

## Read Me First

This document is about the pre-QGT primitive closure only. It does **not** claim that the effective Hilbert fiber is the final micro-ontology, and it does **not** claim that non-abelian gauge structure, cosmological mode decomposition, or measurement/decoherence are primitive here. It claims only what is needed to close the pre-QGT primitive and its derived-support consequence within scope.

The core theorem burden carried here is:

- representative-first primitive closure,
- quotient closure,
- induced QGT closure,
- scalar-generated law closure,
- constitutive equivalence closure,
- support theorem closure,
- runtime sufficiency corollary within bounded implementation assumptions.

---

## 1. Foundations and Setting

### 1.1 Primitive Carrier Domain

Let $M$ be a connected $C^1$ effective local carrier domain of coarse coordinates. The role of $M$ is primitive in the limited sense that it is the domain on which the local state-family is defined. What is **not** primitive is any locality-bearing support relation on $M$ such as fixed adjacency or graph edges.

Let $\pi:\mathcal H\to M$ be an effective complex Hilbert bundle. The adjective *effective* means only that each fiber $\mathcal H_x$ carries the minimal inner-product structure required to define normalization, overlap, local variation, and local phase redundancy. No stronger ontological claim is made.

A primitive representative section is a $C^1$ section

$$
\psi:M\to \mathbb S(\mathcal H),
\qquad
x\mapsto \lvert\psi(x)\rangle,
$$

with fiberwise normalization

$$
\langle \psi(x),\psi(x)\rangle_x = 1
\qquad \forall x\in M.
$$

A local admissible state-family is the pair $(\psi,T^{\mathrm{adm}}_\psi)$, where $T^{\mathrm{adm}}_\psi$ is the distinguished class of local admissible tangent variations satisfying:

1. locality in $x$,
2. regularity sufficient to define projected derivatives and the induced QGT,
3. closure under the primitive law modulo the redundancy class below.

A reservoir field is a scalar function

$$
u:M\to \mathbb R_{>0},$$

interpreted as internal-energy / bath density.

### 1.2 Local $U(1)$ Redundancy

The primitive representative is redundant under local phase:

$$
\lvert\psi(x)\rangle \sim e^{i\Lambda(x)}\lvert\psi(x)\rangle,
\qquad
\Lambda\in C^1(M,\mathbb R).
$$

This is the local $U(1)$ principal-bundle redundancy already fixed by the state-bundle order inherited from CF09. The physical quotient state space is therefore the projective bundle

$$
\mathbb P(\mathcal H)=\mathbb S(\mathcal H)/U(1).
$$

Define the vertical and horizontal projectors by

$$
P_\parallel := \lvert\psi\rangle\langle\psi\rvert,
\qquad
P_\perp := 1-\lvert\psi\rangle\langle\psi\rvert.
$$

For any admissible local variation $v\in T^{\mathrm{adm}}_\psi$,

$$
v=v_\parallel + v_\perp,
\qquad
v_\parallel = P_\parallel v,
\qquad
v_\perp = P_\perp v.
$$

The vertical part is pure phase/self-parallel redundancy. The horizontal part is the physically meaningful local variation class. This quotient/projection is theorem-grade in the present CF and is not left to later execution.

### 1.3 Primitive Representative Theorem

**Theorem 1 (Primitive Representative Setting).**  
Given $(M,\pi:\mathcal H\to M,\psi,T^{\mathrm{adm}}_\psi)$ as above, the normalized representative section together with local $U(1)$ redundancy is sufficient data to define physically meaningful local variation after quotienting the vertical phase direction. No primitive support graph, bond field, or adjacency structure is required.

**Proof.**  
Normalization places $\psi$ on the unit-sphere bundle. Local phase redundancy identifies vertical motion as gauge/self-parallel re-representation. The only physically meaningful variation class is therefore the quotient of admissible tangent variation by the vertical line generated by $\psi$. This uses only the primitive local carrier domain and the representative-state structure; no support relation enters. $\square$

---

## 2. Generators and Evolution Law

### 2.1 Tangent Decomposition

The primitive representative evolution is constrained by normalization. Let $t\mapsto \psi(t)$ be any admissible trajectory. Then

$$
\langle\psi,\psi\rangle = 1.
$$

Differentiate:

$$
\frac{d}{dt}\langle\psi,\psi\rangle
=
\langle\dot\psi,\psi\rangle + \langle\psi,\dot\psi\rangle
=
2\,\operatorname{Re}\langle\psi,\dot\psi\rangle
=
0.
$$

Hence $\langle\psi,\dot\psi\rangle$ is purely imaginary. Therefore there exists a real scalar functional $\alpha[\psi]$ such that

$$
\langle\psi,\dot\psi\rangle = -i\,\alpha[\psi].
$$

Define

$$
\chi[\psi] := \dot\psi + i\,\alpha[\psi]\psi.
$$

Then

$$
\langle\psi,\chi[\psi]\rangle
=
\langle\psi,\dot\psi\rangle + i\alpha[\psi]\langle\psi,\psi\rangle
=
-i\alpha[\psi]+i\alpha[\psi]
=0.
$$

So every admissible norm-preserving representative evolution decomposes uniquely as

$$
\dot\psi = -i\,\alpha[\psi]\psi + \chi[\psi],
\qquad
\langle\psi,\chi[\psi]\rangle = 0.
$$

The vertical term is pure gauge/self-parallel motion. The horizontal term is the physical evolution class.

### 2.2 Tangent Decomposition Theorem

**Theorem 2 (Unique Vertical/Horizontal Decomposition).**  
Every admissible norm-preserving representative evolution admits a unique decomposition

$$
\dot\psi = -i\,\alpha[\psi]\psi + \chi[\psi],
\qquad
\langle\psi,\chi[\psi]\rangle=0,
$$

with $\alpha[\psi]\in\mathbb R$ and $\chi[\psi]\in T^{\mathrm{adm}}_\psi\cap\operatorname{im}P_\perp$.

**Proof.**  
Existence was derived above. For uniqueness, suppose

$$
\dot\psi = -i\alpha\psi + \chi = -i\alpha'\psi + \chi',
\qquad
\langle\psi,\chi\rangle = \langle\psi,\chi'\rangle = 0.
$$

Take inner product with $\psi$ to obtain $-i\alpha=-i\alpha'$, hence $\alpha=\alpha'$, hence $\chi=\chi'$. $\square$

### 2.3 Scalar-Generated Horizontal Law Class

The surviving horizontal law class on the quotient/projective state manifold is the scalar-generated Kähler-metriplectic class

$$
\bar\chi = \Omega^\sharp d\mathcal I + g^\sharp d\Sigma.
$$

This is the only class retained after eliminating:

- pure Hamiltonian horizontal flow as too narrow for generic dissipative closure,
- pure gradient flow as too narrow for generic Berry/holonomy closure,
- arbitrary horizontal vector fields as too broad to satisfy closure/no-hidden-integrals discipline.

### 2.4 Scalar-Generated Law Theorem

**Theorem 3 (Scalar-Generated Horizontal Closure).**  
Let $(g,\Omega)$ be the induced metric-curvature pair from the QGT on the quotient state manifold. Then the physically admissible local horizontal law class compatible with the present scope is

$$
\bar\chi = \Omega^\sharp d\mathcal I + g^\sharp d\Sigma,
$$

where $\mathcal I$ is the invariant-generating scalar and $\Sigma$ is the entropy-generating scalar.

**Proof.**  
The reversible sector must be compatible with the antisymmetric curvature/symplectic structure; the only local scalar-generated vector field class of that form is $\Omega^\sharp d\mathcal I$. The irreversible sector must be compatible with the metric sector and entropy production; the only local scalar-generated gradient class of that form is $g^\sharp d\Sigma$. Pure Hamiltonian or pure gradient special cases fail to provide the generic combined structure required by the accepted law closure. Arbitrary horizontal vector fields violate closure discipline because they are not automatically generated by invariant/entropy functionals and therefore are not auditable under no-hidden-integrals pressure. $\square$

This is the mainline law-class statement. It is theorem-grade in this CF.

---

## 3. Induced Geometry from Projected Variation

### 3.1 Induced QGT

For any admissible local chart on $M$, define the QGT by

$$
Q_{\mu\nu}
=
\langle \partial_\mu \psi \mid \partial_\nu \psi\rangle
-
\langle \partial_\mu \psi \mid \psi\rangle
\langle \psi \mid \partial_\nu \psi\rangle.
$$

The subtraction term is exactly the removal of the vertical/self-parallel phase component. Therefore $Q$ is the first gauge-invariant bilinear record of physically meaningful local difference.

### 3.2 Induced QGT Theorem

**Theorem 4 (Induced QGT).**  
The bilinear form $Q_{\mu\nu}$ defined above is invariant under local $U(1)$ re-representation, depends only on projected local variation, and is therefore a tensorial object on the quotient state manifold.

**Proof.**  
Under $\psi\mapsto e^{i\Lambda}\psi$, the raw derivatives acquire vertical phase pieces. The subtraction term removes exactly the contribution from the vertical/self-parallel line. Therefore the result depends only on the horizontal quotient class and is independent of representative choice. $\square$

### 3.3 Metric/Curvature Split

The induced QGT splits as

$$
Q_{\mu\nu}=g_{\mu\nu}-\frac{i}{2}\Omega_{\mu\nu},
$$

with

$$
g_{\mu\nu}=\operatorname{Re}Q_{\mu\nu},
\qquad
\Omega_{\mu\nu}=-2\,\operatorname{Im}Q_{\mu\nu}.
$$

Here $g$ is the induced quantum metric and $\Omega$ is the induced Berry-curvature/symplectic sector.

### 3.4 QGT-to-Metriplectic Map

Once $(g,\Omega)$ are induced, the downstream metriplectic operators are obtained on the admissible leaf by the standard map

$$
M \sim g^{-1},
\qquad
J \sim \Omega^{+},
$$

with pseudo-inverse/regularized inverse on singular leaves as needed. The resulting degeneracy conditions are

$$
J\,\delta\Sigma = 0,
\qquad
M\,\delta\mathcal I = 0.
$$

These are structure identities in the formalism. The paired notebook only measures their residuals for a given implementation.

---

## 4. Constitutive Equivalence and Narrowing

### 4.1 Surviving Constitutive Family

The theorem-grade constitutive family is

$$
\mathcal I[\psi,u]
=
\int_M\left(
\frac{\tau}{2}\,\lvert D_t\psi_\perp\rvert_g^2
+
\frac{D}{2}\sum_{i=1}^{d}\lvert D_i\psi_\perp\rvert_g^2
+
V([\psi])
+
u
\right)\,d\mu,
$$

$$
\Sigma[\psi,u]
=
\int_M s(u)\,d\mu,
\qquad
s\in C^2,
\quad s'(u)>0,
\quad s''(u)<0.
$$

Here:
- $D_t\psi_\perp$ and $D_i\psi_\perp$ are the projected time and space derivatives of the representative section,
- $\tau$ and $D$ are the telegraph/Cattaneo constitutive parameters,
- $V([\psi])$ is a local gauge-invariant potential,
- $u$ is the reservoir/internal-energy density.

### 4.2 Why this Family Survives

The conservative density is fixed to the telegraph–Kähler local quadratic form because:

1. finite-speed propagation in scope requires a telegraph/Cattaneo principal part,
2. the conservative sector must be local and gauge invariant,
3. the carrier remains the projected state-family, not a primitive graph.

The entropy family survives because the theorem-level constraints only require:

$$
s'(u)>0,
\qquad s''(u)<0,
$$

so that the reservoir entropy is strictly monotone and strictly concave, making it a valid local thermodynamic/Fisher-type scalar.

### 4.3 Constitutive Equivalence under Reservoir Reparameterization

The apparent entropy-family freedom is not a theorem-level ambiguity.

Let

$$
\sigma := s(u).
$$

Because $s\in C^2$ and $s'(u)>0$, the map $u\mapsto \sigma$ is a local $C^2$ diffeomorphism on the reservoir domain. Therefore

$$
u=s^{-1}(\sigma),
$$

and the constitutive pair may be rewritten as

$$
\mathcal I[\psi,\sigma]
=
\int_M\left(
\frac{\tau}{2}\,\lvert D_t\psi_\perp\rvert_g^2
+
\frac{D}{2}\sum_{i=1}^{d}\lvert D_i\psi_\perp\rvert_g^2
+
V([\psi])
+
s^{-1}(\sigma)
\right)\,d\mu,
$$

$$
\Sigma[\psi,\sigma]
=
\int_M \sigma\,d\mu.
$$

So the remaining family freedom is exactly a reservoir-coordinate choice. The load-bearing theorem consequences in scope are invariant under this reparameterization because:

- the QGT sector is upstream and untouched,
- the degeneracy identities are coordinate-covariant generator statements,
- entropy-production sign is preserved because $s'(u)>0$ keeps the entropy orientation fixed,
- support emergence depends on the telegraph principal part and the law itself, not on which local chart is used on the reservoir line.

### 4.4 Constitutive Equivalence Theorem

**Theorem 5 (Constitutive Equivalence Class).**  
The family

$$
\Sigma = \int_M s(u)\,d\mu,
\qquad s\in C^2,
\quad s'(u)>0,
\quad s''(u)<0,
$$

is theorem-equivalent within the scope of CF12 under smooth strictly monotone reservoir-coordinate reparameterization. Therefore the family itself, not a unique specialization, is the theorem-grade constitutive closure.

**Proof.**  
The map $u\mapsto \sigma=s(u)$ is a local diffeomorphism on the reservoir domain. Rewriting the constitutive pair in the entropy-adapted coordinate $\sigma$ leaves unchanged the theorem-level structure: scalar-generated law class, degeneracy identities, sign of entropy production, and support theorem principal part. Therefore all surviving members are equivalent as constitutive charts on the same reservoir sector. $\square$

### 4.5 Worked-Example Specialization

The canonical execution specialization used in the paired notebook is

$$
s(u)=k_B\log u,
\qquad u>0.
$$

This is a canonical executable representative of the theorem-grade family. It is **not** the uniquely forced constitutive law.

---

## 5. Derived Support from Primitive Evolution

### 5.1 Nonlinear Solution Operator

Let

$$
U_{t,t_0}:(\psi(t_0),u(t_0))\mapsto (\psi(t),u(t))
$$

be the nonlinear solution operator of the closed primitive law.

Let

$$
DU_{t,t_0}\big\rvert_{(\psi,u)}
$$

denote its Fréchet derivative on horizontal perturbations along the actual trajectory.

### 5.2 Exact Support Relation

For a compactly supported horizontal perturbation $(\delta\psi_{\perp,0},\delta u_0)$ localized near $x_0$, define

$$
(x_0,t_0)\rightsquigarrow (x,t)
\iff
\exists\,(\delta\psi_{\perp,0},\delta u_0)
\text{ localized near }x_0
\text{ such that }
\big(DU_{t,t_0}(\delta\psi_{\perp,0},\delta u_0)\big)(x)\neq 0.
$$

Then define the exact derived support set

$$
\operatorname{Supp}(t;t_0,x_0)
=
\overline{\{x\in M : (x_0,t_0)\rightsquigarrow (x,t)\}}.
$$

This definition uses only the law itself and its derivative. It does not use observables, thresholds, or preinserted adjacency.

### 5.3 Observable-Independence

Any admissible separating family of local gauge-invariant observables detects the same support, but does not define it.

Formally: let $\mathcal O$ be a separating family of local gauge-invariant observables on the quotient dynamics. Then for any horizontal perturbation state, if all members of $\mathcal O$ vanish on the propagated perturbation at $(x,t)$, then the propagated perturbation vanishes there. Conversely, if the propagated perturbation is nonzero, some member of the separating family detects it. Therefore the support extracted from the law is primary, and observable families are witnesses.

### 5.4 Non-Circularity

The primitive formalism assumes only:
- the effective carrier domain $M$,
- the local state-family on $M$,
- and the closed primitive law on that carrier.

It does **not** assume any primitive locality-bearing support relation on $M$ such as adjacency, edges, or graph neighborhoods.

Therefore there is no circularity in using $M$ while deriving support. The domain is primitive; the influence relation on that domain is derived.

### 5.5 Cone Inclusion

If the telegraph–Kähler principal part holds, then the derived support satisfies a finite-speed cone law

$$
\operatorname{Supp}(t;t_0,x_0)
\subseteq
\{x\in M : d_g(x,x_0)\le c_{\mathrm{eff}}(t-t_0)\},
$$

with

$$
c=\sqrt{D/\tau},
$$

and with any declared hierarchy throttle entering only through the effective speed factor $c_{\mathrm{eff}}$ when the model explicitly includes such throttling.

### 5.6 Gauge-Hosting Sufficiency

Because the representative section is continuous and normalized, for every $x\in M$ there exists a neighborhood $U_x$ such that

$$
\lvert\langle \psi(x),\psi(y)\rangle\rvert > 0
\qquad \forall y\in U_x.
$$

If derived support furnishes local neighborhoods inside the telegraph cone, then those neighborhoods necessarily support nonzero local overlaps. Therefore they are sufficient to host:

- overlap-based connection data,
- discrete link variables,
- plaquette holonomies,
- Wilson loops on sufficiently small support-generated loops.

This is the gauge-hosting corollary needed for downstream CF09-style overlap constructions.

### 5.7 Support Theorem

**Theorem 6 (Derived Support from the Primitive Law).**  
Let $(\psi,u)$ evolve under the closed primitive law of this formalism. Then the support relation defined through the Fréchet derivative of the nonlinear solution operator is:

1. derived from the law rather than inserted by hand,
2. invariant under representative choice because it acts on horizontal quotient perturbations,
3. observable-independent because observables are only separating witnesses,
4. non-circular because the primitive object is the local carrier domain, not a primitive support relation,
5. cone-bounded under the telegraph principal part,
6. sufficient to host downstream overlap-based gauge constructions.

**Proof.**  
Items (1) and (4) follow from the definition of support through $DU_{t,t_0}$ with no primitive adjacency input. Item (2) follows because $DU_{t,t_0}$ acts on horizontal quotient classes. Item (3) follows from the separating-family argument above. Item (5) follows from the telegraph principal symbol and finite-speed propagation. Item (6) follows from continuity and normalization of the representative section, which give nonzero local overlap on sufficiently small support neighborhoods. $\square$

---

## 6. Runtime Sufficiency within Scope

### 6.1 Faithful Discretization Assumptions

A concrete runtime lies within the scope of this formalism only if it satisfies all of the following bounded implementation-faithfulness assumptions:

1. the discrete state variables faithfully discretize the primitive representative carrier and reservoir field,
2. the discrete update law faithfully discretizes the closed scalar-generated primitive law,
3. the discrete implementation recomputes support from the discrete retarded propagator of the law and does not insert adjacency as primitive,
4. the discrete QGT and downstream $(g,\Omega,J,M)$ constructions remain inside the regime where the theorem assumptions are approximated with controlled residuals.

### 6.2 Runtime Sufficiency Corollary

**Corollary 7 (Runtime Sufficiency within Scope).**  
Any runtime satisfying the implementation-faithfulness assumptions above is ontologically sufficient within the scope of CF12.

**Proof.**  
The primitive carrier, quotient, induced geometry, scalar-generated law, constitutive equivalence class, and derived support are theorem-grade inside the present formalism. A faithful discretization preserves that structure at the implementation level by hypothesis. Because support is recomputed from the discrete retarded propagator rather than inserted as primitive adjacency, the runtime respects the same primitive-to-support derivation carried in the formalism. Therefore no further foundational ingredient is required for runtime sufficiency within scope. $\square$

This is not loose conditional language. It is an explicit theorem with bounded implementation assumptions.

---

## 7. Validation and Falsification

Validation is subordinate to proof. The gates below do not decide theorem truth; they test whether a concrete implementation lies inside the theorem’s domain.

### 7.1 Constitutive Gates

**C-G1 Conservative-density gate**  
Measure the principal symbol of the implemented conservative density and the extracted characteristic speed $c_{\mathrm{num}}$. It validates telegraph–Kähler locality. Failure falsifies faithful implementation of the conservative sector.

**C-G2 Reservoir-degeneracy gate**  
Measure

$$
r_M = \lVert M\nabla\mathcal I\rVert_2,
\qquad
r_J = \lVert J\nabla\Sigma\rVert_2,
\qquad
\dot\Sigma.
$$

It validates exact degeneracy and entropy production. Failure falsifies faithful implementation of the generator pair.

**C-G3 Strict-concavity/Fisher gate**  
Measure $s'(u)$ and $s''(u)$ in the chosen execution specialization. It validates that the specialization remains inside the theorem-grade constitutive equivalence class. Failure falsifies the execution specialization, not the equivalence theorem itself.

**C-G4 No-hidden-integrals gate**  
Audit extra conserved quantities/Casimirs beyond the declared invariant/entropy structure. Failure falsifies implementation-faithfulness or exposes an actual contradiction with the formal closure.

### 7.2 Support Gates

**S-G1 Kernel-defined support gate**  
Compute support from the discrete retarded propagator, not from inserted adjacency. Failure falsifies runtime faithfulness to the support theorem.

**S-G2 Gauge-invariant support gate**  
Check support under multiple local representative choices. Failure falsifies discrete quotient fidelity.

**S-G3 Cone gate**  
Check support envelope against the telegraph cone. Failure falsifies faithful implementation of the principal part.

**S-G4 Separating-observable recovery gate**  
Use a separating family of local gauge-invariant observables to recover support and confirm witness consistency with the theorem-defined support object. Failure falsifies witness adequacy or implementation fidelity.

**S-G5 Gauge-structure-hosting gate**  
Construct overlap-based link variables, plaquette phases, and Wilson-loop diagnostics on the derived support neighborhoods. Failure falsifies the implementation of the support neighborhoods or the continuity assumptions at discrete resolution.

**S-G6 Runtime sufficiency gate**  
Verify that support is recomputed from primitive evolution in the implementation and not hard-coded. Failure falsifies the implementation-faithfulness assumptions of Corollary 7.

### 7.3 Falsifiers

This formalism is falsified within scope if any of the following occur:

1. the primitive representative cannot be quotiented to a gauge-invariant QGT,
2. the tangent decomposition fails for admissible norm-preserving evolution,
3. the scalar-generated law class fails to reproduce the required degeneracy structure,
4. the constitutive family fails reservoir-coordinate equivalence,
5. support cannot be defined from the law itself,
6. support depends on representative choice or fails the separating-observable witness property,
7. derived support cannot host downstream overlap-based gauge structure,
8. no faithful discretization can satisfy the implementation-faithfulness assumptions.

---

## 8. Worked Example Specification

### 8.1 Canonical Execution Specialization

The canonical execution specialization is:

$$
s(u)=k_B\log u,
\qquad u>0,
$$

with a bounded-below local gauge-invariant potential $V([\psi])$ chosen for the target phase structure.

The worked conservative density is

$$
\mathcal I_{\mathrm{ex}}[\psi,u]
=
\int_M\left(
\frac{\tau}{2}\,\lvert D_t\psi_\perp\rvert_g^2
+
\frac{D}{2}\sum_{i=1}^{d}\lvert D_i\psi_\perp\rvert_g^2
+
V([\psi])
+
u
\right)\,d\mu,
$$

$$
\Sigma_{\mathrm{ex}}[\psi,u]
=
 k_B\int_M \log u\,d\mu.
$$

### 8.2 Parameter Table

| Parameter | Meaning | Units / role |
|---|---|---|
| $\tau$ | relaxation timescale | telegraph timescale |
| $D$ | transport coefficient | telegraph cone speed $c=\sqrt{D/\tau}$ |
| $k_B$ | entropy scale | entropy normalization |
| $V$ parameters | quotient-state potential parameters | phase-structure control |
| $u_0$ | initial reservoir profile | entropy-bearing background |
| chart resolution / grid | discretization for CFN | verification only |

### 8.3 Expected Diagnostics

The worked example is expected to show:

- normalization preserved up to representative redundancy,
- gauge invariance of the QGT,
- positive semidefinite metric sector,
- antisymmetric curvature sector,
- small degeneracy residuals,
- nonnegative entropy production,
- support inside the telegraph cone,
- viable overlap-based gauge diagnostics on derived support neighborhoods.

This worked example is not theorem-grade uniqueness. It is the canonical execution case inside the theorem-grade constitutive equivalence class.

---

## 9. Assumptions and Limitations

1. The effective Hilbert bundle is not claimed as final micro-ontology.
2. The constitutive entropy family is theorem-grade only up to reservoir-coordinate equivalence; $s(u)=k_B\log u$ is an execution specialization.
3. The support theorem is exact within the continuum law and bounded implementation assumptions; discrete implementations must still verify fidelity through the CFN gates.
4. Non-abelian gauge closure is not claimed here.
5. Cosmological mode decompositions remain downstream of the present primitive closure.

---

## 10. Notebook Pairing and Traceability

The paired CFN is a code recreation and verification mirror of this formalism. It does not decide theorem truth. Each theorem and corollary in this document maps to explicit observables and gates, and every gate listed above is a verification of implementation-faithfulness to the formalism already carried here.

---

## 11. Acceptance Checklist

- [ ] Primitive representative/quotient/QGT chain encoded exactly as written.
- [ ] Tangent decomposition reproduced exactly.
- [ ] Scalar-generated law class implemented with constitutive family restricted to the theorem-grade equivalence class.
- [ ] Support recomputed from the discrete retarded propagator rather than inserted adjacency.
- [ ] C-G1 through C-G4 passed.
- [ ] S-G1 through S-G6 passed.
- [ ] No hidden integrals or gauge inconsistencies detected.

---

## Explicit Non-Claims

This formalism does **not** claim:

- that the effective Hilbert bundle is final microscopic ontology,
- that $s(u)=k_B\log u$ is uniquely forced at theorem grade,
- that a concrete implementation is valid merely because the formalism exists,
- that non-abelian gauge structure is closed here,
- that cosmological derived-limit modules are primitive rather than downstream.

---

## CF Status Note

- **Theorem-grade content carried in the document:** primitive representative setting, $U(1)$ quotient, induced QGT, tangent decomposition, scalar-generated law class, constitutive equivalence under reservoir-coordinate reparameterization, derived support theorem, and runtime sufficiency corollary within bounded implementation-faithfulness assumptions.
- **Constitutive equivalence result used:** the family $s\in C^2$, $s'(u)>0$, $s''(u)<0$ is theorem-equivalent under smooth strictly monotone reservoir-coordinate reparameterization; $s(u)=k_B\log u$ is the canonical execution specialization.
- **CFN verification tasks that remain:** constitutive gates C-G1 through C-G4, support gates S-G1 through S-G6, numerical residual audits, and discrete propagator/support extraction checks.
- **Runtime unlock statement within scope:** a runtime is ontologically sufficient within scope iff it is a faithful discretization of the primitive carrier and closed law and recomputes support from the discrete retarded propagator rather than inserting adjacency as primitive.
