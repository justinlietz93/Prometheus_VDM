# CF12: Complete Formalism — Pre-QGT Primitive Closure and Derived Support Emergence in VDM

**Date:** 2026-03-07  
**Status:** Completed Formalism within scope  
**Gap Module:** Pre-QGT primitive closure / derived support emergence  
**Proposer:** Justin K. Lietz  
**License:** See LICENSE

---

## Executive Summary

This document gives the full reference derivation for the pre-QGT primitive layer of VDM. Within the scope claimed here, the formalism proves the following chain.

1. The primitive carrier is a local normalized representative state-family on a carrier domain $M$ with local $U(1)$ redundancy.
2. Physical local variation is obtained by quotienting the self-parallel phase direction.
3. The quantum geometric tensor $Q$ is induced from projected local variation and is not primitive.
4. The metric sector $g$ and curvature sector $\Omega$ are induced from the real and imaginary parts of $Q$.
5. The surviving horizontal law class is scalar-generated:
   $$
   \bar\chi = \Omega^\sharp d\mathcal I + g^\sharp d\Sigma.
   $$
6. The constitutive sector is theorem-grade only up to reservoir-coordinate equivalence:
   $$
   \mathcal I[\psi,u]
   =
   \int_M \left(
   \frac{\tau}{2}\,|D_t\psi_\perp|_g^2
   +
   \frac{D}{2}\sum_{i=1}^d |D_i\psi_\perp|_g^2
   +
   V([\psi])
   +
   u
   \right) d\mu,
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
7. Locality-bearing support is derived from the nonlinear solution operator of the law and its Fréchet derivative, not inserted as primitive adjacency.
8. Observable-independence, non-circularity, and local gauge-hosting sufficiency follow as theorem-level consequences.
9. A runtime architecture is admissible within scope if it faithfully discretizes the primitive carrier and closed law, recomputes support from the discrete retarded propagator rather than hard-coding adjacency, and preserves the formal structures within bounded residuals on a finite validation horizon.

This CF is self-supporting. It carries its own theorem statements, proofs, constitutive reasoning, and support/evidence logic. The paired CFN is only the executable realization, numerical witness, and figure generator for a formalism already complete in this document.

---

## Canon Registries and Policy Discipline

This document is the derivation-owned source of truth for the present module. The role of canon registries is to stabilize symbols, equations, algorithms, and validation metrics once this formalism is accepted. The role of the paired CFN is to instantiate and compute the formalism written here; it does not supply missing derivation.

Equations are written explicitly in this document because the present task is a full derivation-owned Completed Formalism rather than a bridge memo. Internal canon dependencies and external mathematical background are listed later in dedicated sections.

---

## Read Me First

This CF is about the pre-QGT primitive layer only. It does **not** claim that the effective Hilbert-fiber language is the final micro-ontology. It does **not** claim that support, adjacency, or graph structure are primitive. It does **not** claim that the worked-example entropy specialization is uniquely forced. It does **not** claim necessity for the runtime admissibility theorem. It proves only what is required to close the present derivation within scope.

The proof-bearing chain is organized in the following order.

1. Primitive representative carrier and local $U(1)$ redundancy.
2. Projected variation and quotient structure.
3. Induced QGT.
4. Metric/curvature split.
5. Tangent decomposition.
6. Scalar-generated law closure.
7. Constitutive narrowing and reservoir-coordinate equivalence.
8. Derived support from the law.
9. Observable-independence, non-circularity, and gauge-hosting sufficiency.
10. Runtime admissibility within scope.

No theorem below depends on an object that has not yet been defined or derived.

---

## 1. Foundations and Primitive Setting

### 1.1 Carrier domain and representative family

Let $M$ be a connected $C^1$ carrier domain of effective local coordinates. The role of $M$ is primitive in the limited sense that it is the domain on which the state-family is defined. No support graph, neighborhood graph, or adjacency structure on $M$ is taken as primitive.

Let $\pi: \mathcal H \to M$ be an effective complex Hilbert bundle. The adjective *effective* means only that each fiber $\mathcal H_x$ carries the minimum inner-product structure needed to define normalization, overlap, admissible local variation, and local phase redundancy. No stronger ontological claim is made.

A primitive representative section is a $C^1$ map
$$
\psi : M \to \mathbb S(\mathcal H),
\qquad
x \mapsto |\psi(x)\rangle,
$$
with fiberwise normalization
$$
\langle \psi(x),\psi(x)\rangle_x = 1
\qquad
\text{for all } x\in M.
$$

An admissible local state-family is a pair $(\psi,T^{\mathrm{adm}}_\psi)$ where $T^{\mathrm{adm}}_\psi$ is the class of local admissible tangent variations satisfying:

1. locality in $x$,
2. regularity sufficient to define projected derivatives and induced bilinear forms,
3. closure under the primitive law modulo the local redundancy described next.

A reservoir field is the positive scalar field
$$
 u : M \to \mathbb R_{>0}.
$$
It is interpreted as local internal-energy or bath density.

### 1.2 Local phase redundancy

The primitive representative is redundant under local phase:
$$
|\psi(x)\rangle \sim e^{i\Lambda(x)} |\psi(x)\rangle,
\qquad
\Lambda \in C^1(M,\mathbb R).
$$
This is the only primitive gauge redundancy assumed here.

Define the vertical and horizontal projectors
$$
P_\parallel := |\psi\rangle\langle\psi|,
\qquad
P_\perp := 1 - |\psi\rangle\langle\psi|.
$$
For any admissible local variation $v \in T^{\mathrm{adm}}_\psi$,
$$
v = v_\parallel + v_\perp,
\qquad
v_\parallel = P_\parallel v,
\qquad
v_\perp = P_\perp v.
$$
The vertical part $v_\parallel$ is pure self-parallel phase motion. The horizontal part $v_\perp$ is the physically meaningful local variation class.

### 1.3 Primitive representative theorem

**Theorem 1 (Primitive representative setting).**  
Given $(M,\pi:\mathcal H\to M,\psi,T^{\mathrm{adm}}_\psi)$ as above, the normalized representative section together with local $U(1)$ redundancy is sufficient data to define physically meaningful local variation after quotienting the self-parallel phase direction. No primitive support relation, bond field, adjacency graph, or gauge-holonomy object is required.

**Proof.**  
Normalization places each representative on the unit sphere of its fiber. Local phase redundancy identifies the one-dimensional self-parallel line generated by $|\psi\rangle$ as gauge redundancy. Quotienting by that line leaves the horizontal variation class $P_\perp v$ as the unique physically meaningful local tangent content. This construction uses only the primitive carrier domain, fiberwise inner product, and phase redundancy. It does not use adjacency, links, loops, or support. $\square$

---

## 2. Projected Variation and Induced Geometry

### 2.1 Projected local derivatives

Let $x^\mu$ be a local coordinate chart on $M$. The raw derivative $\partial_\mu |\psi\rangle$ contains both physical and pure-phase components. The projected derivative is
$$
|\partial_\mu \psi\rangle_\perp
:=
P_\perp |\partial_\mu \psi\rangle
=
|\partial_\mu \psi\rangle - |\psi\rangle\langle \psi | \partial_\mu \psi\rangle.
$$
This is the gauge-invariant physical local variation class.

### 2.2 Induced quantum geometric tensor

Define the quantum geometric tensor by
$$
Q_{\mu\nu}
=
\langle \partial_\mu \psi \mid \partial_\nu \psi \rangle
-
\langle \partial_\mu \psi \mid \psi \rangle
\langle \psi \mid \partial_\nu \psi \rangle.
$$
Equivalently,
$$
Q_{\mu\nu}
=
\langle \partial_\mu \psi \mid P_\perp \partial_\nu \psi \rangle.
$$
So $Q$ depends only on projected local variation.

### 2.3 QGT theorem

**Theorem 2 (Induced QGT).**  
The tensor $Q_{\mu\nu}$ is invariant under local $U(1)$ re-representation, depends only on projected local variation, and is therefore the first gauge-invariant bilinear geometric object induced by the primitive representative family.

**Proof.**  
Under the local phase change $|\psi\rangle \mapsto e^{i\Lambda}|\psi\rangle$ one has
$$
|\partial_\mu \psi\rangle
\mapsto
 e^{i\Lambda}
\left(
|\partial_\mu \psi\rangle + i(\partial_\mu \Lambda)|\psi\rangle
\right).
$$
The extra term is vertical, because it is proportional to $|\psi\rangle$. Applying $P_\perp$ removes that vertical component. Hence the projected derivative is invariant up to the common phase factor, and the bilinear form built from projected derivatives is invariant. Therefore $Q_{\mu\nu}$ depends only on the quotient-physical local variation class and is gauge-invariant. $\square$

### 2.4 Metric/curvature split

Define
$$
g_{\mu\nu} := \operatorname{Re} Q_{\mu\nu},
\qquad
\Omega_{\mu\nu} := -2\,\operatorname{Im} Q_{\mu\nu}.
$$
Then
$$
Q_{\mu\nu} = g_{\mu\nu} - \frac{i}{2}\Omega_{\mu\nu}.
$$
The real part $g$ is the induced metric sector. The imaginary part $\Omega$ is the induced curvature/symplectic sector.

### 2.5 Metric/curvature theorem

**Theorem 3 (Metric/curvature split).**  
The real and imaginary parts of the induced QGT define the induced metric sector $g$ and curvature sector $\Omega$ on the quotient state manifold. Neither is primitive; both are induced from projected variation.

**Proof.**  
By Theorem 2, $Q$ is the gauge-invariant Hermitian bilinear form induced from projected variation. Every Hermitian bilinear form decomposes uniquely into a real symmetric part and an imaginary antisymmetric part. Applying this decomposition to $Q$ defines $g$ and $\Omega$. Since $Q$ itself is induced from projected variation, so are $g$ and $\Omega$. $\square$

---

## 3. Tangent Decomposition and Scalar-Generated Law Closure

### 3.1 Tangent decomposition

Let $t\mapsto \psi(t)$ be an admissible representative trajectory. Since
$$
\langle \psi,\psi\rangle = 1,
$$
differentiating gives
$$
\frac{d}{dt}\langle \psi,\psi\rangle
=
\langle \dot\psi,\psi\rangle + \langle \psi,\dot\psi\rangle
=
2\,\operatorname{Re}\langle \psi,\dot\psi\rangle
=
0.
$$
Hence $\langle \psi,\dot\psi\rangle$ is purely imaginary. Therefore there exists a real scalar functional $\alpha[\psi]$ such that
$$
\langle \psi,\dot\psi\rangle = -i\,\alpha[\psi].
$$
Define
$$
\chi[\psi] := \dot\psi + i\,\alpha[\psi]\psi.
$$
Then
$$
\langle \psi,\chi[\psi]\rangle
=
\langle \psi,\dot\psi\rangle + i\alpha[\psi]\langle \psi,\psi\rangle
=
-i\alpha[\psi] + i\alpha[\psi]
=
0.
$$
Therefore
$$
\dot\psi = -i\,\alpha[\psi]\psi + \chi[\psi],
\qquad
\langle \psi,\chi[\psi]\rangle = 0.
$$

### 3.2 Tangent decomposition theorem

**Theorem 4 (Unique vertical/horizontal decomposition).**  
Every admissible norm-preserving representative evolution admits a unique decomposition
$$
\dot\psi = -i\,\alpha[\psi]\psi + \chi[\psi],
\qquad
\langle \psi,\chi[\psi]\rangle = 0,
$$
with $\alpha[\psi]\in \mathbb R$ and $\chi[\psi]$ horizontal.

**Proof.**  
Existence was derived above. For uniqueness, suppose
$$
\dot\psi = -i\alpha\psi + \chi = -i\alpha'\psi + \chi',
\qquad
\langle \psi,\chi\rangle = \langle \psi,\chi'\rangle = 0.
$$
Taking inner product with $\psi$ gives
$$
-i\alpha = \langle \psi,\dot\psi\rangle = -i\alpha'.
$$
Hence $\alpha=\alpha'$, and therefore $\chi=\chi'$. $\square$

### 3.3 Scalar-generated horizontal law

At the quotient level, the surviving horizontal law class is
$$
\bar\chi = \Omega^\sharp d\mathcal I + g^\sharp d\Sigma.
$$
This law uses only induced geometric objects already derived in Section 2.

### 3.4 Scalar-generated law theorem

**Theorem 5 (Scalar-generated horizontal closure).**  
Within the present scope, the physically admissible local horizontal law class is the scalar-generated Kähler-metriplectic class
$$
\bar\chi = \Omega^\sharp d\mathcal I + g^\sharp d\Sigma,
$$
where $\mathcal I$ is the invariant-generating scalar and $\Sigma$ is the entropy-generating scalar.

**Proof.**  
The curvature sector $\Omega$ is antisymmetric and therefore generates local reversible motion from a scalar by contraction with an exact one-form $d\mathcal I$. The metric sector $g$ is symmetric and therefore generates local irreversible motion from a scalar by contraction with an exact one-form $d\Sigma$. A pure Hamiltonian law $\Omega^\sharp d\mathcal I$ omits the irreversible sector and therefore cannot realize the combined generator split required by the present closure. A pure gradient law $g^\sharp d\Sigma$ omits the curvature/holonomy sector and therefore cannot realize the combined generator split either. An arbitrary horizontal vector field not generated by scalars is too broad: it is not automatically auditable under the degeneracy and no-hidden-integrals burden. Hence the only admissible class within scope is the scalar-generated mixed class above. $\square$

---

## 4. Constitutive Closure

### 4.1 Constitutive family

The theorem-grade constitutive family is
$$
\mathcal I[\psi,u]
=
\int_M \left(
\frac{\tau}{2}|D_t\psi_\perp|_g^2
+
\frac{D}{2}\sum_{i=1}^{d}|D_i\psi_\perp|_g^2
+
V([\psi])
+
 u
\right) d\mu,
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
Here $D_t\psi_\perp$ and $D_i\psi_\perp$ are projected time and space derivatives of the representative section, $\tau$ and $D$ are telegraph/Cattaneo constitutive parameters, $V([\psi])$ is a local gauge-invariant potential on the quotient state manifold, and $u$ is the local reservoir density.

This family is the narrowest one compatible with:

1. local finite-speed telegraph propagation,
2. scalar-generated reversible/irreversible splitting,
3. entropy production with a genuine reservoir channel,
4. strict concavity of the entropy sector,
5. no-hidden-integrals discipline.

### 4.2 Reservoir-coordinate conjugacy and constitutive equivalence

Let
$$
\mathcal I[\psi,u] = \mathcal I_0[\psi] + \int_M u\,d\mu,
\qquad
\Sigma[\psi,u] = \int_M s(u)\,d\mu,
$$
where $\mathcal I_0[\psi]$ denotes the gauge-invariant conservative sector. Assume $s\in C^2(U)$ with $s'(u)>0$ on the reservoir interval $U$.

Define the reservoir-coordinate map
$$
\Phi:(\psi,u)\mapsto (\psi,\sigma),
\qquad
\sigma = s(u).
$$

**Lemma 6 (Reservoir-coordinate conjugacy).**  
On every region where $s'(u)>0$, the map $\Phi$ is a local $C^2$ diffeomorphism and the scalar-generated primitive law in $(\psi,u)$ coordinates is locally conjugate to the scalar-generated primitive law in $(\psi,\sigma)$ coordinates. The degeneracy conditions, entropy-production sign, derived-support relation, and runtime-admissibility content are preserved under this conjugacy.

**Proof.**  
Because $s'(u)>0$, the inverse function theorem gives a local inverse $u=s^{-1}(\sigma)$, so $\Phi$ is a local diffeomorphism. Write the horizontal quotient vector field in $(\psi,u)$ coordinates as
$$
X = \Omega^\sharp d\mathcal I + g^\sharp d\Sigma.
$$
The pushed-forward vector field in $(\psi,\sigma)$ coordinates is
$$
\widetilde X = T\Phi\bigl(X\circ \Phi^{-1}\bigr).
$$
Since
$$
\widetilde{\mathcal I}[\psi,\sigma]
=
\mathcal I_0[\psi] + \int_M s^{-1}(\sigma)\,d\mu,
\qquad
\widetilde{\Sigma}[\psi,\sigma] = \int_M \sigma\,d\mu,
$$
the transformed vector field has the same scalar-generated form
$$
\widetilde X
=
\widetilde\Omega^\sharp d\widetilde{\mathcal I} + \widetilde g^\sharp d\widetilde{\Sigma}.
$$
Thus the laws are conjugate.

The degeneracy statements are kernel statements. Under a local diffeomorphism, tensor fields and exact one-forms push forward covariantly. Therefore
$$
J\,d\Sigma = 0
\quad\Longleftrightarrow\quad
\widetilde J\,d\widetilde\Sigma = 0,
$$
$$
M\,d\mathcal I = 0
\quad\Longleftrightarrow\quad
\widetilde M\,d\widetilde{\mathcal I} = 0.
$$
Because $\widetilde\Sigma = \Sigma\circ \Phi^{-1}$, entropy production satisfies
$$
\frac{d}{dt}\widetilde\Sigma(\widetilde z(t))
=
\frac{d}{dt}\Sigma(z(t)),
$$
so the sign of entropy production is preserved.

Let $U_{t,t_0}$ be the nonlinear solution operator in $(\psi,u)$ coordinates. The transformed solution operator is
$$
\widetilde U_{t,t_0} = \Phi\circ U_{t,t_0}\circ \Phi^{-1}.
$$
Differentiating gives
$$
D\widetilde U_{t,t_0} = D\Phi \circ D U_{t,t_0}\circ D\Phi^{-1}.
$$
Hence a horizontal perturbation propagates nontrivially in one chart if and only if the corresponding perturbation propagates nontrivially in the other chart. Therefore the support relation is unchanged. Since the runtime-admissibility theorem depends only on the primitive carrier, quotient structure, closed law, and derived support relation, it is invariant under this reservoir-coordinate change. $\square$

**Corollary 6.1 (Theorem-grade constitutive equivalence class).**  
The entropy-bearing constitutive sector is theorem-grade at the level of the equivalence class
$$
s\in C^2(U),
\qquad
s'(u)>0,
\qquad
s''(u)<0,
$$
modulo smooth strictly monotone reservoir-coordinate reparameterization. The specialization
$$
s(u)=k_B\log u,
\qquad u>0,
$$
is therefore an execution specialization, not a uniquely forced entropy chart.

---

## 5. Derived Support from the Primitive Law

### 5.1 Nonlinear solution operator and derivative

Let $Z$ denote the primitive state space of admissible fields $(\psi,u)$ modulo the local $U(1)$ redundancy on the representative sector. Let
$$
U_{t,t_0}: Z \to Z
$$
denote the nonlinear solution operator of the closed primitive law on its interval of existence. For each admissible trajectory $z(\cdot)$ and each pair $t\ge t_0$, let
$$
D U_{t,t_0}\big|_{z(t_0)}
$$
denote the Fréchet derivative of the solution operator at the initial state.

A horizontal perturbation $\delta z_0$ at time $t_0$ is said to be localized near $x_0\in M$ if its support is contained in an arbitrarily small neighborhood of $x_0$ in the carrier domain.

Define the support relation by
$$
(x_0,t_0) \rightsquigarrow (x,t)
$$
if and only if there exists a localized horizontal perturbation $\delta z_0$ near $x_0$ such that
$$
\bigl(D U_{t,t_0}\big|_{z(t_0)}\,\delta z_0\bigr)(x) \neq 0.
$$
Define the exact derived support set by
$$
\operatorname{Supp}(t;t_0,x_0)
=
\overline{\{x\in M : (x_0,t_0) \rightsquigarrow (x,t)\}}.
$$

### 5.2 Derived support theorem

**Theorem 7 (Derived support theorem).**  
For every admissible trajectory of the closed primitive law, $\operatorname{Supp}(t;t_0,x_0)$ is the locality-bearing support relation induced by the law. It is determined by the retarded propagation of horizontal perturbations under the Fréchet derivative of the nonlinear solution operator and therefore depends on the law itself rather than on inserted adjacency, graph structure, or thresholded observable recovery.

If the principal part of the closed primitive law is of telegraph/Cattaneo type with effective characteristic speed $c_{\mathrm{eff}}$, then
$$
\operatorname{Supp}(t;t_0,x_0)
\subseteq
\{x\in M : d_M(x,x_0)\le c_{\mathrm{eff}}(t-t_0)\}
$$
for all $t\ge t_0$ within the domain of existence, where $d_M$ is the carrier-domain distance used within scope.

**Proof.**  
The definition of $\rightsquigarrow$ uses only the nonlinear law through its solution operator and the propagation of horizontal perturbations under its Fréchet derivative. No primitive adjacency, neighbor graph, support relation, or observable threshold is supplied as an input. Hence the support relation is law-induced.

Because perturbations are taken in the horizontal quotient dynamics, local $U(1)$ rephasing of the representative does not change whether a perturbation propagates nontrivially. Thus the support object is quotient-physical. If the principal part of the law is telegraph/Cattaneo type, then finite-speed propagation bounds the domain of dependence. Therefore the support relation is contained in the characteristic cone measured with respect to the carrier-domain distance $d_M$. $\square$

### 5.3 Observable-independence

**Corollary 7.1 (Observable-independence).**  
Let $\mathcal F$ be any separating family of local gauge-invariant observables on the horizontal quotient dynamics. Then $\mathcal F$ witnesses the derived support relation but does not define it. In particular, $\operatorname{Supp}(t;t_0,x_0)$ is independent of the choice of separating family.

**Proof.**  
The support object is defined from the law itself through $D U_{t,t_0}$. A separating family of local gauge-invariant observables detects whether the propagated perturbation is nonzero, but it does not alter the propagation law. Hence different separating witness families recover the same support relation. $\square$

### 5.4 Non-circularity

**Lemma 7.2 (Non-circularity of support emergence).**  
The formalism assumes as primitive only:

1. the carrier domain $M$ on which the fields are defined,
2. the local differential structure needed to write the primitive law.

It does not assume as primitive any adjacency, edge set, support relation, neighborhood graph, or locality-bearing influence structure on $M$. The support relation on $M$ is instead derived from propagation under the primitive law.

**Proof.**  
The carrier domain is the arena of fields. It is not itself a support graph. The support relation is the subset of $M\times M\times \mathbb R^2$ defined by nonzero retarded propagation of horizontal perturbations. Since that relation is built from the nonlinear solution operator and its Fréchet derivative rather than supplied independently, no primitive locality-bearing support structure is smuggled in. $\square$

### 5.5 Local overlap cover and loop-hosting sufficiency

**Lemma 7.3 (Local overlap cover and loop-hosting).**  
Let $\psi:M\to \mathbb S(\mathcal H)$ be a continuous normalized representative section. Then for every $x\in M$ there exists an open neighborhood $U_x\subset M$ such that
$$
\langle \psi(x),\psi(y)\rangle \neq 0
\qquad
\text{for all } y\in U_x.
$$
Consequently, the family $\{U_x\}_{x\in M}$ forms an open overlap cover on which local overlap phases
$$
\mathcal U(x,y)
=
\frac{\langle \psi(x),\psi(y)\rangle}{|\langle \psi(x),\psi(y)\rangle|}
$$
are well-defined whenever $x$ and $y$ lie in a common overlap neighborhood.

Suppose $V\subset \operatorname{Supp}(t;t_0,x_0)$ is a support-generated neighborhood such that $V$ is subordinate to the overlap cover, meaning every point of $V$ lies in some overlap neighborhood and every sufficiently small loop in $V$ is covered by finitely many overlap neighborhoods. Then:

1. local link phases on $V$ are well-defined and gauge-covariant,
2. any sufficiently small loop in $V$ admits a discrete holonomy built from ordered products of local link phases,
3. plaquette and Wilson-loop constructions on such sufficiently small support-generated loops are well-defined.

**Proof.**  
For fixed $x\in M$, the map
$$
y\mapsto \langle \psi(x),\psi(y)\rangle
$$
is continuous. At $y=x$ one has
$$
\langle \psi(x),\psi(x)\rangle = 1 \neq 0.
$$
Therefore there exists an open neighborhood $U_x$ on which the overlap remains nonzero. On such a neighborhood the normalized overlap phase $\mathcal U(x,y)$ is well-defined. Under local $U(1)$ rephasing, $\mathcal U(x,y)$ transforms covariantly and therefore serves as a local link variable. If $V$ is subordinate to the overlap cover, then sufficiently small loops in $V$ are covered by finitely many such overlap neighborhoods. Ordered products of the local link phases along those loops are therefore defined, yielding local plaquette and Wilson-loop holonomies. $\square$

### 5.6 Gauge-hosting sufficiency

**Corollary 7.4 (Gauge-hosting sufficiency).**  
Within the scope of this formalism, the derived support neighborhoods furnished by the retarded law are sufficient to host the downstream local overlap-based connection, plaquette, and Wilson-loop constructions. Thus the local gauge/holonomy machinery depends on derived support and continuous representative geometry, not on inserted primitive adjacency.

**Proof.**  
By Lemma 7.3 every point has an overlap neighborhood on which local link phases are well-defined. By Theorem 7 the law furnishes local support neighborhoods generated by propagation. Whenever those support neighborhoods are taken within the subordinacy condition of Lemma 7.3, they support the required overlap-based local holonomy constructions. $\square$

---

## 6. Runtime Admissibility Within Scope

**Theorem 8 (Runtime admissibility within scope).**  
Let $\mathcal R_h$ be a discretized implementation of the formalism. Suppose the following hold on a finite validation horizon.

1. $\mathcal R_h$ discretizes the primitive carrier variables $(\psi,u)$ on the carrier domain $M$ and preserves normalization and the local $U(1)$ quotient structure up to bounded residuals.
2. $\mathcal R_h$ discretizes the closed scalar-generated law together with the theorem-grade constitutive equivalence class of the entropy-bearing reservoir sector.
3. $\mathcal R_h$ computes support from the discrete retarded propagator of the discretized law and does not insert adjacency, support, or neighborhood graphs as primitive ontological inputs.
4. $\mathcal R_h$ preserves, up to bounded residuals on the validation horizon, induced-QGT regularity, the metric/curvature split, degeneracy conditions, the sign of entropy production, cone inclusion of derived support with respect to $d_M$, and the overlap-cover conditions required for downstream overlap-based gauge constructions.
5. $\mathcal R_h$ introduces no undeclared conserved quantities, primitive support structures, or gauge inconsistencies beyond those allowed by the formalism.

Then $\mathcal R_h$ is an admissible runtime realization of CF12 within scope on that validation horizon.

**Proof.**  
Theorems 1 through 7 fix the ontologically load-bearing content of the formalism: primitive carrier, quotient structure, induced geometry, closed scalar-generated law, constitutive equivalence class, and derived support. A discretization satisfying conditions (1) through (5) preserves exactly those structures up to bounded residuals on the stated horizon and recomputes support from law-generated propagation rather than inserting it primitively. Therefore the runtime lies within the ontological scope of CF12 on that horizon. $\square$

**Role of the CFN.**  
The theorem above is not a claim that every concrete code base automatically satisfies its hypotheses. The role of the CFN is only to verify whether a given implementation satisfies the bounded residual assumptions of Theorem 8 and to provide executable numerical realization, figures, and worked examples for the already-complete formalism.

---

## 7. Validation and Falsification

Validation in this CF is subordinate to proof. The gates below do not decide theorem truth. They test whether a concrete implementation or execution specialization lies inside the domain of the theorems already proved above.

### 7.1 Constitutive verification

**C-G1 Conservative-density verification.**  
Measure the principal symbol of the implemented conservative density and the extracted characteristic speed $c_{\mathrm{num}}$. This verifies faithful implementation of the telegraph–Kähler conservative sector.

**C-G2 Reservoir-degeneracy verification.**  
Measure
$$
r_M = \lVert M\nabla\mathcal I\rVert_2,
\qquad
r_J = \lVert J\nabla\Sigma\rVert_2,
\qquad
\dot\Sigma.
$$
This verifies implementation-faithfulness to the degeneracy and entropy-production structure.

**C-G3 Entropy-chart verification.**  
For a chosen execution specialization of $s(u)$, measure $s'(u)$ and $s''(u)$ to verify that the specialization lies inside the theorem-grade constitutive equivalence class.

**C-G4 No-hidden-integrals verification.**  
Audit the implementation for undeclared conserved quantities or hidden primitive relational structures.

### 7.2 Support verification

**S-G1 Propagator-defined support verification.**  
Compute support from the discrete retarded propagator and verify that no primitive adjacency is used as an ontological input.

**S-G2 Quotient support verification.**  
Check support under multiple representative choices to verify quotient consistency.

**S-G3 Cone verification.**  
Check the support envelope against the finite-speed cone defined with respect to $d_M$.

**S-G4 Witness recovery verification.**  
Use separating families of local gauge-invariant observables to recover support and confirm consistency with the theorem-defined support object.

**S-G5 Gauge-hosting verification.**  
Construct overlap-based link variables, plaquette phases, and Wilson loops on derived support neighborhoods to verify faithful realization of the overlap-cover structure.

**S-G6 Runtime admissibility verification.**  
Check that the implementation satisfies the hypotheses of Theorem 8 on the declared validation horizon.

### 7.3 Falsifiers

This formalism is falsified within scope if any of the following occur:

1. the representative carrier cannot be quotiented to a gauge-invariant projected variation class;
2. the QGT cannot be induced from projected variation;
3. the tangent decomposition fails for admissible norm-preserving evolution;
4. the scalar-generated law class fails to reproduce the required degeneracy structure;
5. the constitutive family fails reservoir-coordinate equivalence;
6. support cannot be defined from the law itself;
7. the support relation depends on representative choice;
8. derived support cannot host downstream overlap-based gauge structure under the stated subordinacy condition;
9. no faithful discretization satisfies the admissibility conditions of Theorem 8.

---

## 8. Worked Example Specification

### 8.1 Canonical execution specialization

The canonical execution specialization used in the paired notebook is
$$
s(u)=k_B\log u,
\qquad u>0.
$$

A canonical conservative execution specialization is
$$
\mathcal I_{\mathrm{ex}}[\psi,u]
=
\int_M \left(
\frac{\tau}{2}|D_t\psi_\perp|_g^2
+
\frac{D}{2}\sum_{i=1}^{d}|D_i\psi_\perp|_g^2
+
V([\psi])
+
 u
\right) d\mu,
$$
$$
\Sigma_{\mathrm{ex}}[\psi,u]
=
 k_B\int_M \log u\,d\mu.
$$
This is an execution specialization, not a uniquely forced theorem-grade constitutive law.

### 8.2 Worked-example diagnostics

The execution case is expected to show:

- normalization preserved up to representative redundancy,
- gauge invariance of the induced QGT,
- small degeneracy residuals,
- nonnegative entropy production,
- support inside the carrier-domain cone,
- overlap-based gauge diagnostics on derived support neighborhoods.

---

## 9. Internal Canon References

The following canon documents are load-bearing for CF12.

- **CF01**: QGT to metriplectic mapping and degeneracy checks.
- **CF02**: contact/GENERIC compatibility.
- **CF04**: finite-speed / telegraph locality pressure.
- **CF05**: closure and no-hidden-integrals discipline.
- **CF06**: Fisher / information-geometric pressure.
- **CF07**: observation/decoherence layer sits above the present formal layer.
- **CF09**: representative-first local state bundle, projected variation, induced QGT, downstream overlap/holonomy machinery.
- **CF11**: scalar-generated generator form, entropy-bearing reservoir logic, derived-limit thermodynamic pressure.

---

## 10. External Mathematical Background

The following external mathematical categories are used only as background and sharpening tools.

- **Projective Hilbert space and geometric quantum mechanics**: representative-to-ray quotient, horizontal/vertical decomposition, overlap geometry.
- **Quantum geometric tensor and Fubini–Study / Berry geometry**: gauge-invariant Hermitian bilinear form, metric/curvature split, local holonomy structure.
- **GENERIC / contact / metriplectic structure**: scalar-generated reversible/irreversible splitting, degeneracy, entropy-production form.
- **Hyperbolic / telegraph propagation and differentiable solution operators**: finite-speed support cone, nonlinear solution operator, Fréchet-derivative support theorem.

---

## 11. Novel Contributions of CF12

The results newly proved or newly tightened here are:

1. the integration of the pre-QGT primitive carrier with the scalar-generated law chain in one continuous formal derivation;
2. the reservoir-coordinate conjugacy lemma showing theorem-grade constitutive equivalence;
3. the support theorem stated from the nonlinear solution operator and its Fréchet derivative;
4. the observable-independence corollary;
5. the explicit non-circularity lemma;
6. the local overlap-cover / loop-hosting lemma;
7. the gauge-hosting sufficiency corollary;
8. the runtime admissibility theorem.

---

## 12. Assumptions, Limitations, and Explicit Non-Claims

1. The effective Hilbert-bundle language is not claimed as final micro-ontology.
2. The entropy family is theorem-grade only up to reservoir-coordinate equivalence; the logarithmic entropy density is an execution specialization, not uniquely forced.
3. The support theorem is proved within the scope of local carrier-domain geometry and the closed primitive law; it does not claim more than that scope.
4. The runtime theorem is a sufficient admissibility theorem on a finite validation horizon. It is not a necessity theorem.
5. The paired CFN is only executable realization, numerical witness, and figure generation for the formalism already complete in this CF.

---

## CF Status Note

- **Theorem-grade content carried in the document:** primitive representative carrier, local $U(1)$ quotient, induced QGT, metric/curvature split, tangent decomposition, scalar-generated law closure, constitutive equivalence, derived support theorem, observable-independence, non-circularity, overlap-cover / loop-hosting lemma, gauge-hosting sufficiency, runtime admissibility.
- **Constitutive equivalence result used:** entropy-bearing constitutive freedom is theorem-grade only modulo smooth strictly monotone reservoir-coordinate reparameterization; $s(u)=k_B\log u$ is the canonical execution specialization.
- **CFN verification tasks that remain:** implementation-faithfulness checks, residual measurements, support-kernel computation, cone verification, overlap/holonomy diagnostics, worked numerical realization, and figure generation.
- **Runtime unlock statement within scope:** a runtime lies within the ontological scope of CF12 only if it satisfies the sufficient admissibility conditions of Theorem 8 on a finite validation horizon.
