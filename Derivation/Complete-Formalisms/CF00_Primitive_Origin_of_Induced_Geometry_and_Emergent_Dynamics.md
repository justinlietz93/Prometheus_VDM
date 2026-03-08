# CF00: Complete Formalism — Primitive Origin of Induced Geometry and Emergent Dynamics in VDM

**Date:** 2026-03-08  
**Status:** Complete Formalism  
**Role in canon:** Current root formalism for this branch of VDM physics  
**Proposer:** Justin K. Lietz  
**License:** See LICENSE

---

## Executive Summary

This document is the current bedrock formalism for the branch of VDM physics that previously began effectively at the induced-geometry and engine layer. It begins earlier. It begins from the primitive representative ontology currently justified in this branch: a local normalized representative state-family on a carrier domain $\mathcal{M}$ with local $U(1)$ redundancy and no primitive adjacency, support graph, bond set, or gauge connection inserted by hand.

From that starting point, this document derives quotient-physical local variation, derives the quantum geometric tensor from projected variation, derives the induced metric and curvature sectors from that tensor, derives the reversible and irreversible dynamical architecture from those induced sectors, narrows the constitutive sector to a theorem-grade equivalence class under reservoir-coordinate conjugacy, derives locality-bearing support from the nonlinear solution operator and its Fréchet derivative, proves observable-independence and non-circularity of that support relation, proves local overlap-cover and gauge-hosting sufficiency of derived support neighborhoods, and states the strongest honest runtime theorem that follows: a sufficient admissibility theorem on a finite validation horizon.

CF00 is physically first for this branch even though CF01 was historically first. CF01 is therefore downstream. CF11 is downstream. Neither is load-bearing for the derivation carried here. They remain relevant as provenance, downstream placement, and consistency witnesses only.

CF00 does not merely stop at the deepest layer previously formalized. It answers the root question directly: what is the correct primitive bedrock of this branch, and is anything deeper mathematically forced beneath it? The answer carried here is that the carrier domain $\mathcal{M}$ is the present terminal primitive of this branch. A deeper substrate is not mathematically forced by any theorem in this formalism. Asking for one, without a theorem that requires it, is additional metaphysics rather than unfinished formal burden. This document therefore treats $\mathcal{M}$ as the terminal carrier of the present branch while making explicit what is already encoded in $\mathcal{M}$ and what is still induced later from quotient-physical variation.

---

## 1. Root Status, Ontological Finality, and Notation Convention

### 1.1 Root status

CF00 is the root source of truth for the derivation it presents. Any downstream document in this branch that uses induced geometry, scalar-generated mixed dynamics, constitutive reservoir closure, or support-derived locality inherits those structures from CF00.

This document is not a scope-limited repair memo. It is not a legal defense of a pre-existing engine. It is the current root derivation for the branch.

### 1.2 Notation convention

Two different kinds of objects must not share the same symbol.

- $\mathcal{M}$ denotes the **carrier domain**: the primitive ontological arena on which the representative state-family is defined.
- $M$ denotes the **dissipative symmetric operator or sector** in the emergent dynamical split $J \oplus M$.

This distinction is ontological, not cosmetic.

- $\mathcal{M}$ is a carrier arena.
- $M$ is an emergent operator on quotient cotangent data.

No statement in this document uses plain $M$ for the carrier domain. All carrier-domain quantities use $\mathcal{M}$ and derived notation such as $d_{\mathcal{M}}$ for the carrier-domain distance.

### 1.3 The root question

The root question for this branch is:

> Is the carrier domain $\mathcal{M}$ only a placeholder for a deeper substrate, or is it the correct terminal primitive bedrock of the present branch?

The answer of CF00 is:

> $\mathcal{M}$ is terminal **for the present branch and present formal reach** because no theorem carried here requires a deeper substrate beneath it. All later structures in the branch are induced from quotient-physical representative variation on $\mathcal{M}$, and no contradiction or incompleteness in that derivation forces a deeper primitive layer.

This is stronger than agnosticism. It is not the claim that nothing deeper could ever exist. It is the claim that no deeper layer is mathematically forced by the present formalism. Therefore CF00 is complete as a root formalism for this branch unless and until a theorem demonstrates that some further pre-$\mathcal{M}$ substrate is necessary.

### 1.4 Root-finality theorem

**Theorem 1.4.1 (Terminality of the carrier domain within this branch).**  
Within the branch formalized here, the carrier domain $\mathcal{M}$ is the terminal primitive arena. A deeper substrate beneath $\mathcal{M}$ is not mathematically forced by any theorem of CF00.

**Proof.**  
The derivation carried in CF00 begins with the representative state-family on $\mathcal{M}$ and then derives, in strict order, quotient-physical variation, induced geometry, the mixed dynamical architecture, constitutive closure, derived support, and runtime admissibility. At no point does the derivation require any additional pre-$\mathcal{M}$ object, relation, or law in order for the next step to exist. In particular:

1. the quotient construction uses only representative redundancy on $\mathcal{M}$;
2. the quantum geometric tensor is induced from projected variation on $\mathcal{M}$;
3. the metric and curvature sectors are induced from that tensor;
4. the mixed dynamical architecture is built from those induced sectors;
5. the constitutive sector is narrowed without introducing a deeper substrate;
6. the support relation is derived from the nonlinear solution operator of the law on $\mathcal{M}$;
7. local gauge-hosting is derived from support neighborhoods and representative continuity on $\mathcal{M}$.

Therefore every load-bearing object in the branch is generated without appealing to anything beneath $\mathcal{M}$. Since no theorem here fails in the absence of a deeper substrate, none is mathematically required. Asking for one would therefore add ontological content not forced by the formalism. That would be additional metaphysics, not unfinished derivation. Hence $\mathcal{M}$ is terminal within the present branch. $\square$

### 1.5 What is and is not already present in $\mathcal{M}$

The theorem above does **not** say that all spacetime-bearing structure is primitive in $\mathcal{M}$. It says something more precise.

Primitive in $\mathcal{M}$:
- carrier-domain locality in the minimal sense that fields are defined pointwise on $\mathcal{M}$,
- the local differential structure needed to define representative variation,
- the carrier-domain distance $d_{\mathcal{M}}$ used only to express cone bounds once the law is derived.

Not primitive in $\mathcal{M}$:
- quotient geometry,
- metric and curvature as physical geometry,
- the reversible/irreversible dynamical split,
- locality-bearing support,
- support neighborhoods,
- overlap-based gauge structures,
- bond or link variables,
- holonomy observables.

Thus $\mathcal{M}$ is terminal as the primitive carrier arena, but not as already-formed physical spacetime metric or connection structure. Those later structures are induced or derived from the primitive representative ontology.

### 1.6 Falsification path for root finality

CF00 would fail as a root formalism if any theorem in the branch required one of the following as an indispensable primitive beneath $\mathcal{M}$:

- a pre-carrier adjacency or support graph,
- a deeper pre-$\mathcal{M}$ state substrate needed to define projected variation,
- a deeper pre-$\mathcal{M}$ tensor needed to define the QGT,
- a primitive $J$-sector or $M$-sector that could not be induced from quotient geometry,
- or a pre-carrier relation required to derive support.

If any such requirement were proved, then $\mathcal{M}$ would no longer be terminal and CF00 would cease to be the true root of the branch.

---

## 2. Primitive Ontology and Representative Structure

### 2.1 Carrier domain

Let $\mathcal{M}$ be a connected $C^1$ carrier domain. The role of $\mathcal{M}$ is primitive. It is the arena on which the representative state-family is defined.

No primitive support relation on $\mathcal{M}$ is assumed. No adjacency graph, neighbor graph, bond graph, or locality-bearing edge set is part of the primitive ontology.

The only primitive spatial structure used here is:

1. the local differential structure of $\mathcal{M}$,
2. and, when a cone statement is later made, a carrier-domain distance $d_{\mathcal{M}}$ used only to measure that cone.

The distance $d_{\mathcal{M}}$ does not define support. It only measures the region in which a support relation generated by the law must lie.

### 2.2 Effective Hilbert-bundle language

Let
$$
\pi:\mathcal{H}\to \mathcal{M}
$$
be an effective complex Hilbert bundle. The word *effective* is used literally: each fiber $\mathcal{H}_x$ carries only the minimum inner-product structure needed to define normalization, overlap, projected variation, and local phase redundancy.

This is a carrier language. It is not a claim that the effective Hilbert bundle is the final micro-ontology of the universe.

### 2.3 Primitive representative state-family

A primitive representative section is a $C^1$ map
$$
\psi:\mathcal{M}\to \mathbb{S}(\mathcal{H}),
\qquad
x\mapsto |\psi(x)\rangle,
$$
with fiberwise normalization
$$
\langle \psi(x),\psi(x)\rangle_x = 1
\qquad
\text{for all } x\in \mathcal{M}.
$$

The primitive state at this branch level is therefore:

- the local normalized representative state-family,
- together with its admissible local variation class.

### 2.4 Local $U(1)$ redundancy

The representative is redundant under local phase:
$$
|\psi(x)\rangle \sim e^{i\Lambda(x)}|\psi(x)\rangle,
\qquad
\Lambda\in C^1(\mathcal{M},\mathbb{R}).
$$

This redundancy is primitive. It means the representative itself is not the physical object. The physical object is the quotient-physical content that survives removal of the self-parallel phase direction.

### 2.5 Primitive theorem

**Theorem 2.5.1 (Primitive representative ontology).**  
The primitive object of this branch is the local normalized representative state-family on $\mathcal{M}$ together with local $U(1)$ redundancy. Primitive support, adjacency, gauge connection, holonomy, bond structure, observable structure, and spacetime-bearing locality relations are forbidden as primitive insertions.

**Proof.**  
The primitive data listed above are exactly the data needed to define local representative variation and representative redundancy. Any stronger relational structure such as support graphs, holonomies, constitutive bonds, or gauge link variables would add relational content not yet earned from the representative ontology. Because the purpose of CF00 is to derive those structures, they cannot be inserted primitively without circularity. Therefore the primitive ontology is exhausted by the representative state-family, the carrier arena $\mathcal{M}$, the fiberwise inner-product structure, and the local $U(1)$ redundancy. $\square$

### 2.6 Falsification path for primitive ontology

The primitive ontology theorem fails if any downstream derivation truly requires a primitive insertion of:

- support or adjacency,
- constitutive bond/link structure,
- gauge connection or Wilson data,
- or metric/curvature geometry.

If such a primitive insertion were necessary, the claimed primitive ontology would be too shallow.

---

## 3. Quotient-Physical Local Variation

### 3.1 Vertical and horizontal projectors

Define the rank-one projector onto the representative line by
$$
P_\parallel := |\psi\rangle\langle\psi|,
$$
and the complementary projector by
$$
P_\perp := 1 - |\psi\rangle\langle\psi|.
$$

For any admissible local variation $v$ of the representative field,
$$
v = v_\parallel + v_\perp,
\qquad
v_\parallel = P_\parallel v,
\qquad
v_\perp = P_\perp v.
$$

### 3.2 Why the self-parallel direction is redundant

Under local rephasing
$$
|\psi\rangle \mapsto e^{i\Lambda}|\psi\rangle,
$$
the infinitesimal variation generated by changing $\Lambda$ is proportional to $i|\psi\rangle$. This lies in the one-dimensional line spanned by $|\psi\rangle$. Therefore that direction changes only the representative chart, not the ray state. It is the local self-parallel phase direction.

### 3.3 Quotient-physical local variation theorem

**Theorem 3.3.1 (Quotient-physical local variation).**  
The physically meaningful local variation is the horizontal variation class defined by $P_\perp$. The self-parallel direction defined by $P_\parallel$ is redundant and must be quotiented out before any physical geometric or dynamical object is constructed.

**Proof.**  
The representative redundancy is exactly the local phase freedom. Infinitesimal variation in that phase direction lies in the representative line and therefore changes only the representative, not the ray state. Any local bilinear or dynamical construction that is meant to represent physical variation must therefore remove the $P_\parallel$ component. The surviving local content is exactly the horizontal class $P_\perp v$. $\square$

### 3.4 Physical state space at this layer

The physical local state at this layer is therefore not $|\psi\rangle$ itself but the quotient class of representatives under local phase. The projected local variation lives naturally on this quotient state space.

### 3.5 Falsification path for quotient construction

The quotient theorem fails if:

- the vertical direction contributes to any gauge-invariant local bilinear object,
- or the local phase direction produces distinct physical local predictions after quotienting.

Either failure would show that the phase direction is not truly redundant.

---

## 4. Induced Geometry from Projected Variation

### 4.1 Projected local derivatives

Let $x^\mu$ be local coordinates on $\mathcal{M}$. The raw derivative $\partial_\mu|\psi\rangle$ contains both physical and pure-phase content. Define the projected derivative by
$$
|\partial_\mu \psi\rangle_\perp
:=
P_\perp |\partial_\mu\psi\rangle
=
|\partial_\mu\psi\rangle
-
|\psi\rangle\langle\psi|\partial_\mu\psi\rangle.
$$

This is the quotient-physical local derivative.

### 4.2 Definition of the quantum geometric tensor

Define
$$
Q_{\mu\nu}
=
\langle \partial_\mu\psi \mid \partial_\nu\psi\rangle
-
\langle \partial_\mu\psi\mid\psi\rangle
\langle\psi\mid \partial_\nu\psi\rangle.
$$

Equivalently,
$$
Q_{\mu\nu}
=
\langle \partial_\mu\psi \mid P_\perp \partial_\nu\psi\rangle.
$$

Thus $Q_{\mu\nu}$ depends only on projected variation.

### 4.3 Gauge invariance of the QGT

Under local rephasing,
$$
|\psi\rangle \mapsto e^{i\Lambda}|\psi\rangle,
$$
one has
$$
|\partial_\mu\psi\rangle
\mapsto
e^{i\Lambda}
\left(
|\partial_\mu\psi\rangle + i(\partial_\mu\Lambda)|\psi\rangle
\right).
$$

The added term is vertical because it is proportional to $|\psi\rangle$. Applying $P_\perp$ removes it. Therefore the projected derivative is unchanged up to the common phase factor. The Hermitian bilinear form built from projected derivatives is therefore gauge-invariant.

### 4.4 Induced-QGT theorem

**Theorem 4.4.1 (Induced quantum geometric tensor).**  
The tensor $Q_{\mu\nu}$ is the first gauge-invariant bilinear geometric object induced by the primitive ontology. It is induced from quotient-physical local variation and is not primitive.

**Proof.**  
The primitive ontology supplies only local representative states and their quotient-physical local variation. The projected derivative is the first local object that survives the quotient. The Hermitian bilinear form built from those projected derivatives is exactly $Q_{\mu\nu}$. Since it is gauge-invariant and built solely from quotient-physical local variation, it is the first induced geometric object. It cannot be inserted primitively without violating the primitive ontology theorem. $\square$

### 4.5 Metric and curvature split

Define
$$
g_{\mu\nu} := \operatorname{Re} Q_{\mu\nu},
\qquad
\Omega_{\mu\nu} := -2\,\operatorname{Im} Q_{\mu\nu}.
$$

Then
$$
Q_{\mu\nu}
=
g_{\mu\nu} - \frac{i}{2}\Omega_{\mu\nu}.
$$

The tensor $g$ is real and symmetric. The tensor $\Omega$ is real and antisymmetric.

### 4.6 Induced metric/curvature theorem

**Theorem 4.6.1 (Induced metric and curvature sectors).**  
The metric sector $g$ and the curvature sector $\Omega$ are induced from the QGT and therefore from quotient-physical local variation. Neither is primitive.

**Proof.**  
Every Hermitian bilinear form decomposes uniquely into its real symmetric part and its imaginary antisymmetric part. Applying that decomposition to the induced QGT defines $g$ and $\Omega$. Since $Q$ itself is induced, gauge-invariant, and quotient-physical, the same is true of its metric and curvature sectors. $\square$

### 4.7 Falsification path for induced geometry

The induced-geometry chain fails if:

- the projected derivative is not gauge-invariant,
- the QGT depends on vertical representative content,
- the split into $g$ and $\Omega$ is not uniquely induced from $Q$,
- or later dynamics require geometric objects not earned from the induced QGT.

---

## 5. Tangent Decomposition and Emergent Dynamical Engine

### 5.1 Tangent decomposition of representative evolution

Let $t\mapsto \psi(t)$ be an admissible representative trajectory. Since
$$
\langle \psi,\psi\rangle = 1,
$$
differentiate in time:
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
\langle \psi,\dot\psi\rangle + i\,\alpha[\psi]\langle \psi,\psi\rangle
=
-i\,\alpha[\psi] + i\,\alpha[\psi]
=
0.
$$

Therefore every norm-preserving representative evolution decomposes uniquely as
$$
\dot\psi
=
-i\,\alpha[\psi]\psi + \chi[\psi],
\qquad
\langle \psi,\chi[\psi]\rangle = 0.
$$

### 5.2 Interpretation of the decomposition

The term $-i\,\alpha[\psi]\psi$ is vertical. It is pure representative phase motion. The term $\chi[\psi]$ is horizontal. It is the quotient-physical evolution class.

### 5.3 The geometric operators available for dynamics

Once the quotient geometry has been induced, there are exactly two geometric structures available at this level:

- the antisymmetric sector $\Omega$,
- the symmetric sector $g$.

On the regular quotient sectors these define bundle maps from cotangent data to tangent data:
$$
J := \Omega^\sharp,
\qquad
M := g^\sharp.
$$

This is the first appearance of plain $M$ in the document. It is the dissipative symmetric operator induced from the quotient geometry. It is not the carrier domain.

### 5.4 Why the mixed law is forced

A local quotient-physical law built only from induced geometry and scalar generators must use only the maps already earned from the induced geometry. At this level, those are precisely $J$ and $M$.

The antisymmetric operator $J$ generates the reversible sector because it acts on scalar differentials through the curvature structure. The symmetric operator $M$ generates the irreversible sector because it acts on scalar differentials through the metric structure. If both sectors are physically present and no extra primitive dynamical tensor may be inserted, then the most general scalar-generated local law is their sum.

### 5.5 Emergent engine theorem

**Theorem 5.5.1 (Emergent scalar-generated mixed dynamical architecture).**  
Let the quotient geometry be given by the induced pair $(g,\Omega)$. Suppose the horizontal law is required to satisfy all of the following:

1. it is local on $\mathcal{M}$,
2. it acts only on quotient-physical data,
3. it is generated by scalar state functionals,
4. it contains both the reversible sector carried by the antisymmetric induced geometry and the irreversible sector carried by the symmetric induced geometry,
5. it does not insert any further primitive generator tensor not already earned from the induced geometry.

Then the horizontal law must take the scalar-generated mixed form
$$
\bar\chi = J\,d\mathcal{I} + M\,d\Sigma
=
\Omega^\sharp d\mathcal{I} + g^\sharp d\Sigma,
$$
for scalar generators $\mathcal{I}$ and $\Sigma$.

**Proof.**  
Condition (2) excludes vertical representative content. Condition (5) excludes any new primitive tensor beyond the induced geometric data. Thus the only available local bundle maps from scalar differentials to quotient tangent vectors are those induced from $\Omega$ and $g$.

An antisymmetric bilinear structure acting on a scalar differential gives the reversible local transport allowed by the induced curvature sector. A symmetric bilinear structure acting on a scalar differential gives the gradient-like local transport allowed by the induced metric sector. If both sectors must appear and both must be scalar-generated, then every admissible horizontal law is the sum of one term generated by the antisymmetric operator and one term generated by the symmetric operator. No third independent primitive sector may appear by condition (5). Therefore the general scalar-generated law has the form
$$
\bar\chi = J\,d\mathcal{I} + M\,d\Sigma.
$$
Since $J=\Omega^\sharp$ and $M=g^\sharp$ on the regular quotient sectors, this is exactly
$$
\bar\chi = \Omega^\sharp d\mathcal{I} + g^\sharp d\Sigma.
$$
Thus the dynamical engine is not imported. It is forced by the induced quotient geometry under the stated conditions. $\square

### 5.6 Honest strength statement

The theorem above does not claim that no deeper pre-geometric dynamics could ever exist in some other branch. It claims that, once the primitive representative ontology of this branch is accepted, the law-bearing engine at this level is forced into the scalar-generated mixed architecture just derived.

### 5.7 Falsification path for emergent engine

The emergent-engine theorem fails if any of the following occur:

- a primitive $J$-sector or $M$-sector is needed,
- a third primitive dynamical sector is needed,
- or the induced geometry cannot generate both reversible and irreversible channels.

---

## 6. Constitutive Narrowing and Reservoir Equivalence

### 6.1 Need for a constitutive sector

The mixed law from Section 5 is structural. To obtain a concrete physical engine one must specify the invariant generator $\mathcal{I}$ and entropy generator $\Sigma$.

### 6.2 Minimal conservative/entropy-bearing form

The narrowest admissible constitutive form at this level is
$$
\mathcal{I}[\psi,u]
=
\int_{\mathcal{M}}
\left(
\frac{\tau}{2}\,|D_t\psi_\perp|_g^2
+
\frac{D}{2}\sum_{i=1}^d |D_i\psi_\perp|_g^2
+
V([\psi])
+
u
\right)d\mu,
$$
and
$$
\Sigma[\psi,u]
=
\int_{\mathcal{M}} s(u)\,d\mu,
$$
with
$$
s\in C^2,
\qquad
s'(u)>0,
\qquad
s''(u)<0.
$$

Here:

- $V([\psi])$ is a local gauge-invariant quotient potential,
- $\tau$ and $D$ determine the telegraph/Cattaneo principal part,
- $u$ is the local entropy-bearing reservoir variable,
- and $d\mu$ is the carrier-domain integration measure.

### 6.3 Why the reservoir is required

The irreversible sector cannot be closed on the conservative variables alone without collapsing the distinction between the invariant generator and the entropy generator. The reservoir variable is therefore not ornamental. It is the minimal additional scalar field needed to carry the irreversible channel while preserving that distinction.

### 6.4 Reservoir-coordinate conjugacy lemma

Let
$$
\mathcal{I}[\psi,u]
=
\mathcal{I}_0[\psi] + \int_{\mathcal{M}} u\,d\mu,
\qquad
\Sigma[\psi,u]
=
\int_{\mathcal{M}} s(u)\,d\mu,
$$
where $\mathcal{I}_0[\psi]$ is the conservative sector and $s'(u)>0$ on the reservoir range. Define
$$
\Phi:(\psi,u)\mapsto (\psi,\sigma),
\qquad
\sigma = s(u).
$$

**Lemma 6.4.1 (Reservoir-coordinate conjugacy).**  
On every region where $s'(u)>0$, the map $\Phi$ is a local $C^2$ diffeomorphism on the reservoir sector. In the transformed coordinates one has
$$
\widetilde{\mathcal I}[\psi,\sigma]
=
\mathcal I_0[\psi] + \int_{\mathcal M} s^{-1}(\sigma)\,d\mu,
\qquad
\widetilde{\Sigma}[\psi,\sigma]
=
\int_{\mathcal M} \sigma\,d\mu.
$$
The primitive law in $(\psi,u)$ and the primitive law in $(\psi,\sigma)$ are locally conjugate. Their degeneracy content, entropy-production sign, derived support relation, and runtime-admissibility content are the same physical content written in different reservoir charts.

**Proof.**  
Because $s'(u)>0$, the inverse function theorem gives a local inverse $u=s^{-1}(\sigma)$, so $\Phi$ is a local diffeomorphism.

Let $X$ be the primitive law vector field in $(\psi,u)$ coordinates. The transformed law is
$$
\widetilde X = T\Phi\, X\, \Phi^{-1}.
$$
Thus the two laws are dynamically conjugate.

The degeneracy statements are kernel statements for the induced symmetric and antisymmetric operators acting on the differentials of the scalar generators. Since those tensors and differentials transform covariantly under $\Phi$, the vanishing or nonvanishing of those kernel conditions is unchanged. Therefore the degeneracy content is preserved.

The transformed entropy is
$$
\widetilde{\Sigma}[\psi,\sigma]
=
\Sigma[\psi,s^{-1}(\sigma)].
$$
Hence along corresponding trajectories one has
$$
\frac{d}{dt}\widetilde{\Sigma}
=
\frac{d}{dt}\Sigma.
$$
So the sign of entropy production is unchanged.

If $U_{t,t_0}$ is the nonlinear solution operator, then
$$
\widetilde U_{t,t_0} = \Phi \circ U_{t,t_0} \circ \Phi^{-1}.
$$
Differentiating gives
$$
D\widetilde U_{t,t_0}
=
D\Phi \circ D U_{t,t_0} \circ D\Phi^{-1}.
$$
Therefore the support relation defined by nonzero propagated horizontal perturbations is preserved. Since runtime admissibility is defined only by faithful discretization of the carrier, quotient, law, and derived support relation, the runtime-admissibility content is also preserved. $\square

### 6.5 Constitutive equivalence theorem

**Theorem 6.5.1 (Theorem-grade constitutive equivalence class).**  
The entropy-bearing constitutive sector is theorem-grade at the level of the equivalence class
$$
s\in C^2,
\qquad
s'(u)>0,
\qquad
s''(u)<0,
$$
modulo smooth strictly monotone reservoir-coordinate reparameterization.

**Proof.**  
By Lemma 6.4.1, any two entropy charts related by such a reparameterization are locally conjugate, preserve the mixed law structure, preserve the degeneracy content, preserve entropy-production sign, preserve the support theorem content, and preserve runtime-admissibility content. Therefore the theorem-grade constitutive content is the equivalence class, not any one special chart. $\square

### 6.6 Canonical execution specialization

A canonical execution specialization is
$$
s(u)=k_B \log u,
\qquad
u>0.
$$

This specialization belongs to the theorem-grade equivalence class but is not uniquely forced by the theorem.

### 6.7 Falsification path for constitutive narrowing

The constitutive equivalence theorem fails if smooth strictly monotone reservoir-coordinate changes alter:

- the mixed-law structure,
- degeneracy content,
- the sign of entropy production,
- the derived support relation,
- or the runtime-admissibility content.

---

## 7. Derived Locality, Support, and Gauge-Hosting

### 7.1 Nonlinear solution operator

Let $Z$ denote the primitive state space of admissible fields $(\psi,u)$ modulo local $U(1)$ redundancy on the representative sector. Let
$$
U_{t,t_0}: Z\to Z
$$
denote the nonlinear solution operator of the closed primitive law on its interval of existence.

For each admissible trajectory $z(\cdot)$ and each pair $t\ge t_0$, let
$$
D U_{t,t_0}\big|_{z(t_0)}
$$
denote the Fréchet derivative of the solution operator at the initial state.

### 7.2 Derived support relation

A horizontal perturbation $\delta z_0$ at time $t_0$ is localized near $x_0\in \mathcal{M}$ if its support lies in an arbitrarily small neighborhood of $x_0$ in the primitive carrier domain.

Define
$$
(x_0,t_0)\rightsquigarrow (x,t)
$$
if and only if there exists a localized horizontal perturbation $\delta z_0$ near $x_0$ such that
$$
\bigl(D U_{t,t_0}\big|_{z(t_0)}\,\delta z_0\bigr)(x)\neq 0.
$$

Define the exact support set by
$$
\operatorname{Supp}(t;t_0,x_0)
=
\overline{
\left\{
x\in \mathcal{M} :
(x_0,t_0)\rightsquigarrow (x,t)
\right\}
}.
$$

### 7.3 Derived-support theorem

**Theorem 7.3.1 (Derived support from the law).**  
For every admissible trajectory of the closed primitive law, the locality-bearing support relation is the support relation induced by the retarded propagation of horizontal perturbations under the Fréchet derivative of the nonlinear solution operator. It is not primitive adjacency, not thresholded observable recovery, and not graph structure inserted by hand.

If the principal part of the closed primitive law is of telegraph/Cattaneo type with effective characteristic speed $c_{\mathrm{eff}}$, then
$$
\operatorname{Supp}(t;t_0,x_0)
\subseteq
\left\{
x\in \mathcal{M} :
d_{\mathcal{M}}(x,x_0)\le c_{\mathrm{eff}}(t-t_0)
\right\}
$$
for all $t\ge t_0$ within the domain of existence.

**Proof.**  
The support relation is defined entirely through the law via its nonlinear solution operator and the propagation of horizontal perturbations under its Fréchet derivative. Therefore support is generated by the law itself.

Because the perturbations are horizontal, representative phase redundancy does not affect whether a perturbation propagates nontrivially. So the support object is quotient-physical.

If the principal part of the law is telegraph/Cattaneo type, then the domain of dependence of perturbations is bounded by the corresponding characteristic cone measured with the carrier-domain distance $d_{\mathcal{M}}$. Therefore the derived support set lies inside that cone. $\square

### 7.4 Observable-independence corollary

**Corollary 7.4.1 (Observable-independence).**  
Let $\mathcal F$ be any separating family of local gauge-invariant observables on the horizontal quotient dynamics. Then $\mathcal F$ witnesses the derived support relation but does not define it. The support set $\operatorname{Supp}(t;t_0,x_0)$ is independent of the separating family used to detect propagated perturbations.

**Proof.**  
The support object is defined from the law itself through $D U_{t,t_0}$. Any separating witness family merely detects whether the propagated perturbation is nonzero. It does not alter the propagation. Therefore different separating witness families recover the same support object. $\square

### 7.5 Non-circularity lemma

**Lemma 7.5.1 (Non-circularity of derived support).**  
The primitive inputs of the formalism are the carrier domain $\mathcal{M}$, the representative field, the reservoir field, and the closed primitive law on those fields. No support relation, adjacency graph, or neighborhood graph on $\mathcal{M}$ is primitive. The support relation on $\mathcal{M}$ is derived from the retarded propagation of horizontal perturbations under the law.

**Proof.**  
The only primitive role of $\mathcal{M}$ is to provide the arena on which fields are defined. The support relation is a subset of $\mathcal{M}\times\mathcal{M}\times \mathbb R^2$ selected by nonzero propagation under the solution operator. Since that relation is computed from the law and is not independently specified, no primitive locality-bearing adjacency is inserted. $\square

### 7.6 Local overlap cover and loop-hosting lemma

Let $\psi:\mathcal{M}\to \mathbb S(\mathcal H)$ be continuous and normalized. For fixed $x\in \mathcal{M}$, the map
$$
y\mapsto \langle \psi(x),\psi(y)\rangle
$$
is continuous and equals $1$ at $y=x$.

**Lemma 7.6.1 (Local overlap cover and loop-hosting).**  
For every $x\in \mathcal{M}$ there exists an open neighborhood $U_x\subset \mathcal{M}$ such that
$$
\langle \psi(x),\psi(y)\rangle \neq 0
\qquad
\text{for all } y\in U_x.
$$
Hence the family $\{U_x\}_{x\in \mathcal{M}}$ is an open overlap cover on which local overlap phases
$$
\mathcal U(x,y)
=
\frac{\langle \psi(x),\psi(y)\rangle}
{|\langle \psi(x),\psi(y)\rangle|}
$$
are well-defined whenever $x$ and $y$ lie in a common overlap neighborhood.

If a support-generated neighborhood $V\subset \operatorname{Supp}(t;t_0,x_0)$ is contained in one such overlap neighborhood, then:

1. local link phases on $V$ are well-defined and gauge-covariant;
2. any sufficiently small loop in $V$ admits a discrete holonomy built from ordered products of local link phases;
3. plaquette and Wilson-loop constructions on such sufficiently small support-generated loops are well-defined.

**Proof.**  
Continuity of the overlap map and normalization at coincidence imply the existence of a neighborhood $U_x$ on which the overlap remains nonzero. The normalized overlap phase is therefore well-defined on each such neighborhood. Under local $U(1)$ rephasing, the normalized overlap phase transforms covariantly and therefore defines a local link variable.

If a support-generated neighborhood is subordinate to the overlap cover, then any sufficiently small loop in that neighborhood is covered by finitely many overlap neighborhoods. Ordered products of local link variables along the loop are therefore defined, and these products give local plaquette and Wilson-loop holonomies. $\square

### 7.7 Gauge-hosting sufficiency corollary

**Corollary 7.7.1 (Gauge-hosting sufficiency of derived support).**  
Within the scope of CF00, the derived support neighborhoods furnished by the law are sufficient to host the downstream local overlap-based connection, plaquette, and Wilson-loop machinery. Therefore gauge-holonomy structure in this branch depends on derived support and continuous representative geometry, not on inserted primitive adjacency.

**Proof.**  
By Lemma 7.6.1, each point admits an overlap neighborhood with well-defined local link phases. By Theorem 7.3.1, the law furnishes local support neighborhoods. On sufficiently fine local scales the support neighborhoods may be taken subordinate to the overlap cover. Therefore the local overlap-based gauge machinery is structurally supported on derived support. $\square

### 7.8 Falsification path for derived locality and gauge hosting

The support theorem or its corollaries fail if:

- support cannot be defined directly from the solution operator and its Fréchet derivative,
- different separating witness families define inequivalent support objects,
- support requires primitive adjacency,
- support violates the carrier-domain cone bound,
- or support-generated neighborhoods do not admit local overlap-based gauge constructions.

---

## 8. Runtime Admissibility

A runtime architecture is admissible relative to CF00 on a finite validation horizon if it satisfies the following sufficient conditions.

**Theorem 8.1 (Runtime admissibility).**  
Let $\mathcal R_h$ be a discretized implementation. Suppose the following hold on a finite validation horizon.

1. $\mathcal R_h$ discretizes the primitive carrier variables $(\psi,u)$ on $\mathcal{M}$ and preserves normalization and the local $U(1)$ quotient structure up to bounded residuals.
2. $\mathcal R_h$ discretizes the closed scalar-generated primitive law together with the theorem-grade constitutive equivalence class of the entropy-bearing reservoir sector.
3. $\mathcal R_h$ computes support from the discrete retarded propagator of the discretized law and does not insert adjacency, support, or neighborhood graphs as primitive ontological inputs.
4. $\mathcal R_h$ preserves, up to bounded residuals on the validation horizon,
   - induced-QGT regularity,
   - the metric/curvature split,
   - the mixed generator structure,
   - entropy-production sign,
   - cone inclusion of derived support relative to $d_{\mathcal{M}}$,
   - and the overlap-cover conditions needed for local overlap-based gauge constructions.
5. $\mathcal R_h$ introduces no undeclared conserved quantities, primitive support structures, or gauge inconsistencies beyond those allowed by the formalism.

Then $\mathcal R_h$ is an admissible runtime realization of CF00 on that validation horizon.

**Proof.**  
Sections 2 through 7 determine the ontologically load-bearing structures of this branch: primitive representative carrier, quotient structure, induced geometry, scalar-generated mixed law, constitutive equivalence class, derived support relation, and local gauge-hosting sufficiency. A runtime satisfying conditions (1) through (5) preserves exactly those structures, up to bounded residuals on the stated horizon, and does not insert structures forbidden by the primitive ontology theorem. Therefore it is an admissible realization of CF00 on that horizon. $\square

This is a theorem of admissibility. It is not a necessity claim, not an “unlock” slogan, and not a statement that every concrete implementation automatically satisfies its hypotheses.

### 8.2 Falsification path for runtime admissibility

A concrete implementation fails the admissibility theorem if it:

- inserts primitive adjacency,
- fails to preserve the quotient or induced-geometry structure,
- violates the carrier-domain cone bound,
- or introduces hidden integrals or primitive support structures not licensed by the formalism.

The executable notebook of CF00 may compute and visualize these checks, but it does not supply missing proof.

---

## 9. Validation and Falsification Inside the Formalism

Validation belongs to the formalism itself as falsification logic. It is not an external sink.

### 9.1 Primitive carrier falsifiers

The primitive carrier theorem fails if the formalism requires any primitive insertion of:

- adjacency or support graph on $\mathcal{M}$,
- holonomy or gauge data before quotient-physical variation is derived,
- constitutive bond structure before the mixed law is derived,
- or observable structure before support is derived from the law.

### 9.2 Induced geometry falsifiers

The induced-geometry chain fails if:

- projected variation is not gauge-invariant,
- the QGT depends on vertical representative content,
- the split into metric and curvature is not uniquely induced from the QGT,
- or later dynamics require geometric objects not earned from the induced QGT.

### 9.3 Mixed-law falsifiers

The emergent-engine theorem fails if:

- a primitive $J$-sector or $M$-sector is needed,
- a third primitive dynamical sector is needed,
- or the induced geometry cannot generate both reversible and irreversible channels.

### 9.4 Constitutive equivalence falsifiers

The constitutive equivalence theorem fails if reservoir-coordinate changes alter:

- the mixed-law structure,
- degeneracy content,
- the sign of entropy production,
- the derived support relation,
- or the runtime-admissibility content.

### 9.5 Derived support falsifiers

The support theorem fails if:

- support cannot be defined directly from the nonlinear solution operator and its Fréchet derivative,
- observables define different support objects rather than witnessing one,
- support requires primitive adjacency,
- support violates the $d_{\mathcal{M}}$ cone bound,
- or support-generated neighborhoods fail to admit local overlap-based gauge constructions.

### 9.6 Runtime falsifiers

A runtime realization fails admissibility if it:

- inserts primitive adjacency,
- fails to preserve the quotient or induced-geometry structure,
- violates the carrier-domain cone bound,
- or introduces hidden integrals or primitive support structures not licensed by the formalism.

---

## 10. Downstream Placement in the Canon

CF00 is the current bedrock formalism for this branch. It is physically first, even though it is historically later.

### 10.1 CF01

CF01 is reclassified as a downstream effective engine formalism. It remains historically important because it was the first successful explicit engine-layer document. It is not load-bearing for the root derivation carried here.

### 10.2 CF11

CF11 is reclassified as a downstream derived-limit module. Its scalar-generated law form and entropy-bearing reservoir logic are consistent with CF00, but they do not substitute for root derivation once CF00 exists.

### 10.3 Other CFs

Other cited CFs remain relevant as downstream modules, consistency witnesses, or provenance records. They do not carry root proof burden for this branch once CF00 is in place.

---

## 11. Internal Canon References

The following internal canon modules are retained as provenance, downstream placement, or consistency witnesses. They are not load-bearing substitutes for the derivation carried here.

- **CF01** — provenance and downstream effective engine placement.
- **CF02** — provenance and downstream contact/GENERIC compatibility witness.
- **CF04** — provenance and downstream finite-speed / cone witness.
- **CF05** — provenance and downstream closure / no-hidden-integrals witness.
- **CF06** — provenance and downstream Fisher / information-geometric witness.
- **CF09** — provenance and downstream overlap/holonomy witness.
- **CF11** — provenance and downstream derived-limit reservoir/entropy witness.

Where this document reproduces, absorbs, or strengthens structures historically associated with those documents, the proof burden is carried here and not delegated back to them.

---

## 12. External Mathematical Background

The following external mathematical categories provide language and sharpening tools. They are not canon authorities.

1. **Projective Hilbert space and geometric quantum mechanics**  
   Used for representative-to-ray quotient language, vertical/horizontal decomposition, and local overlap geometry.

2. **Quantum geometric tensor, Fubini–Study, and Berry geometry**  
   Used for the gauge-invariant Hermitian bilinear form and the induced split into metric and curvature sectors.

3. **GENERIC, contact, and metriplectic structure**  
   Used for reversible/irreversible mixed-generator language and entropy-production form.

4. **Hyperbolic / telegraph propagation and differentiable nonlinear flow operators**  
   Used for the support theorem through the nonlinear solution operator and its Fréchet derivative.

---

## 13. Novel Contributions of CF00

The following are newly formalized here as root-level results.

1. The integration of the primitive representative carrier, quotient-physical variation, induced QGT, and induced metric/curvature sectors into a single dependency-clean root derivation.
2. The derivation of the scalar-generated mixed dynamical architecture from induced geometry rather than importing an engine from downstream canon.
3. The theorem-grade constitutive equivalence class under reservoir-coordinate conjugacy.
4. The support theorem formulated directly from the nonlinear solution operator and its Fréchet derivative.
5. The explicit non-circularity theorem for derived support.
6. The local overlap-cover and loop-hosting lemma proving gauge-hosting sufficiency of derived support neighborhoods.
7. The runtime admissibility theorem stated in the strongest honest form that follows from the formalism.
8. The reclassification of CF01 and CF11 as downstream documents relative to this root formalism.
9. The terminality argument for the carrier domain $\mathcal{M}$ within the present branch.

---

## 14. Explicit Non-Claims

CF00 does not claim the following.

1. It does not claim that the effective Hilbert-bundle language is final micro-ontology.
2. It does not claim necessity in the runtime admissibility theorem.
3. It does not claim a unique entropy chart; it proves only the equivalence class under reservoir-coordinate conjugacy.
4. It does not claim that every downstream extension of VDM is exhausted by this branch.

CF00 also does not claim that no deeper theory could ever exist. What it does claim is stronger and more precise: no deeper substrate beneath $\mathcal{M}$ is mathematically forced by the branch formalized here. Therefore CF00 is root-complete for this branch unless and until a theorem proves otherwise.

---

## 15. Ontological Status of the Carrier Domain $\mathcal{M}$

The question answered here is not whether deeper metaphysics can be imagined. The question is whether the formalism forces anything deeper than $\mathcal{M}$.

### 15.1 What $\mathcal{M}$ is

$\mathcal{M}$ is the primitive carrier arena of the branch. It is the connected $C^1$ domain on which the representative state-family and reservoir field live.

### 15.2 What $\mathcal{M}$ is not

$\mathcal{M}$ is not:

- a graph of primitive adjacency,
- an already-formed metric manifold carrying the induced geometry as primitive data,
- the dissipative operator $M$,
- or a placeholder whose insufficiency is already theorem-forced.

### 15.3 What is already encoded in $\mathcal{M}$

Encoded primitively in $\mathcal{M}$:

- local field carriage,
- local differentiability,
- the carrier-domain distance used only for cone statements after the law is derived.

Not encoded primitively in $\mathcal{M}$:

- quotient geometry,
- support relation,
- gauge connection,
- holonomy,
- or the mixed dynamical engine.

### 15.4 Terminality statement

Within this branch, $\mathcal{M}$ is terminal because every later load-bearing structure is induced from the representative state-family on $\mathcal{M}$ and no theorem demands anything deeper.

### 15.5 Falsifier for terminality

The claim that $\mathcal{M}$ is the correct bedrock carrier for CF00 is falsified if any theorem requires:

- a deeper substrate to define representative redundancy,
- a deeper substrate to define projected variation,
- a deeper substrate to derive the QGT,
- a deeper substrate to derive the mixed law,
- or a deeper substrate to derive support.

No such requirement is proved in this branch. Therefore the terminality claim stands.

---

## 16. CF Status Note

- **Theorem-grade content carried here:** primitive representative ontology, quotient-physical local variation, induced QGT, induced metric/curvature split, tangent decomposition, scalar-generated mixed law, constitutive equivalence under reservoir-coordinate conjugacy, derived support from the nonlinear solution operator and its Fréchet derivative, observable-independence, non-circularity, local overlap-cover / loop-hosting, gauge-hosting sufficiency, runtime admissibility, and terminality of the carrier domain $\mathcal{M}$ within this branch.
- **What remains downstream rather than missing:** executable realization, numerical witness generation, figure production, and bounded-residual checks for concrete implementations.
- **What is not left in suspense:** the root question of whether a deeper substrate is mathematically forced beneath $\mathcal{M}$. It is not.
- **Completion verdict:** CF00 is complete as the current root formalism for this branch of VDM physics.
