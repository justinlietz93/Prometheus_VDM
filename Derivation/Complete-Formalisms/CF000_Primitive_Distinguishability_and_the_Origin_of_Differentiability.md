# CF000: Complete Formalism — Primitive Distinguishability and the Origin of Differentiability in VDM

Date: 2026-03-08  
Status: Theorem-bearing draft pass  
Gap Module: Root formalization beneath CF00  
Proposer: Justin K. Lietz  
License: See LICENSE

---

## Completion Standard for CF Canon

A document may carry the status **Completed Formalism** only if it is a **closed, theorem-grade formal specification within its declared scope, assumptions, and domain of validity**.

This means:

- all central objects are defined or explicitly imported with hypotheses verified;
- all theorem-bearing claims have explicit hypotheses, conclusions, and auditable proofs;
- all essential derivation, validation logic, and failure conditions are present in this document;
- no core burden is outsourced to canon links, notebooks, figures, or code;
- any claim that is heuristic, conjectural, programmatic, or only partially established is labeled as such;
- if any essential proof burden is missing, the document is **not** a Completed Formalism.

“Completed” does **not** mean universally maximal or beyond all future strengthening. It means the claimed result is closed **at the level stated in the document**.

---

## Governing Rule of This Document

This document is the root written source of truth for the pre-differential layer of this branch of VDM.

This document is not a bridge memo, not a philosophical appendix, and not a patch beneath CF00. It must contain the actual derivation burden required to answer the following root question:

**Why is differentiability available to law at all?**

If differentiability is derived, this document must carry that derivation. If differentiability is instead forced as the deepest accessible primitive, this document must prove that no weaker structure suffices for this branch. If neither conclusion can be supported, this document is incomplete.

The paired CFN may instantiate, compute, visualize, and numerically witness claims already formalized here. It may not carry missing derivation, missing proof burden, or missing evidentiary logic.

---

## Relationship to Downstream Canon

CF000 sits beneath CF00.

- CF000 addresses the pre-differential question.
- CF00 begins only after a differentiable carrier, lawful local variation, and the representational geometry built on that carrier are available.
- CF01 remains a downstream effective engine formalism.
- CF11 remains a downstream derived-limit module.
- Later CFs remain downstream of the differentiable layer made possible by CF000.

Accordingly, this document does not borrow its core derivation from CF00 or any later CF. It may mention downstream consequences, but it must earn the layer on which they depend.

---

## Executive Summary

CF000 begins beneath differentiability. It excludes absolute nullity and absolute undifferentiated sameness as viable roots for a falsifiable physical branch, then identifies the weakest surviving primitive residue as a nonempty distinction-bearing multiplicity $({\mathcal B},\#)$ with primitive apartness and no imported metric, valuation, parameter, derivative, topology, locality, transformation, or comparison.

The branch then asks what additional structure is needed if primitive distinction is to support law rather than one-shot separation. A no-go theorem shows that primitive distinction together with sharpenability does **not** force a unique or canonical refinement/compatibility regime. Refinement/compatibility is therefore introduced explicitly as the first minimal added branch structure $R$.

A second no-go theorem shows that $R$ alone does **not** force stable realized distinction contents or a realized carrier. The realization/decisiveness layer $S$ is then introduced as the next minimal added branch structure. Under $R+S$, realized contents and a realized carrier regime exist, but that regime is not forced to be unique or canonical.

A third no-go theorem shows that locality/cover is **not** forced from the solved $R+S$ layer. Locality/cover is therefore introduced explicitly as the next minimal added branch structure $C$.

The present pass addresses the next live theorem burden: whether the solved layer $R+S+C+T+D+A$, together with conditional and non-canonical realized-carrier existence, explicit cover discipline, explicitly added lawful transformation, explicit readout discipline, and explicit stable-comparison discipline, forces a valuation representation. The answer is no. A no-go theorem shows that branch-usable valuation representation is not forced from the solved pre-valuation layer. It must be introduced explicitly as the next minimal added branch structure $V$.

Principal deliverables of this pass:

- theorem-grade separation between forced structure, minimal added branch structure, and conditional theorem under explicit assumptions;
- no-go theorem that refinement/compatibility is not forced from primitive distinction plus sharpenability;
- no-go theorem that realized contents/carrier are not forced from $R$ alone;
- conditional theorem that $R+S$ yields a nonempty realized-carrier regime;
- theorem that the resulting realized-carrier regime is not canonical;
- no-go theorem that locality/cover is not forced from the solved $R+S$ layer;
- explicit introduction of locality/cover as the next minimal added branch structure $C$;
- no-go theorem that lawful transformation is not forced from the solved $R+S+C$ layer;
- explicit introduction of lawful transformation as the next minimal added branch structure $T$;
- no-go theorem that distinguishers/signatures are not forced from the solved $R+S+C+T$ layer;
- explicit introduction of distinguishers/signatures as the next minimal added branch structure $D$;
- no-go theorem that stable comparison algebra is not forced from the solved $R+S+C+T+D$ layer;
- explicit introduction of stable comparison algebra as the next minimal added branch structure $A$;
- no-go theorem that valuation representation is not forced from the solved $R+S+C+T+D+A$ layer;
- explicit introduction of valuation representation as the next minimal added branch structure $V$.

---

## Read Me First: Writing Rules for CF Documents

1. This document must be self-contained at the level required to understand, test, and reuse the formalism.
2. Every theorem-bearing section must expose its proof burden directly.
3. No section may hide essential logic behind phrases such as “it follows,” “similarly,” “by standard arguments,” or “left to the notebook.”
4. All dependency order must be honest. No theorem may use objects that have not yet been defined or derived.
5. Distinguish clearly between:
   - forced from prior layer,
   - minimal added branch structure,
   - conditional theorem under explicit assumptions.
6. If a statement is not theorem-grade, label it accordingly.
7. If a section is incomplete, mark the document incomplete.

---

## State of Closure

### Settled results

- Absolute nullity is not a viable root for a falsifiable law-bearing branch.
- Absolute undifferentiated sameness is not a viable root for a falsifiable law-bearing branch.
- The weakest surviving residue is a nonempty distinction-bearing multiplicity $({\mathcal B},\#)$ with nontrivial apartness and no imported metric, valuation, parameterization, continuity, locality, transformation, readout, or differentiability.
- A direct leap from primitive distinction to differentiability is illegitimate.
- Refinement/compatibility is **not** forced from primitive distinction alone.
- Refinement/compatibility has been reclassified as the first minimal added branch structure $R$.
- Refinement/compatibility alone does **not** force stable realized distinction contents or a realized carrier.
- Under the explicitly added realization/decisiveness layer $S$, stable realized distinction contents do exist.
- Under $R+S$, a realized carrier regime exists.
- Under $R+S$, the realized carrier regime is **not** forced to be unique or canonical.
- Locality/cover is **not** forced from the solved $R+S$ layer.
- Locality/cover has been reclassified as the next minimal added branch structure $C$.
- Lawful transformation is **not** forced from the solved $R+S+C$ layer.
- Lawful transformation has been reclassified as the next minimal added branch structure $T$.
- Distinguishers/signatures are **not** forced from the solved $R+S+C+T$ layer.
- Distinguishers/signatures have been reclassified as the next minimal added branch structure $D$.
- Stable comparison algebra is **not** forced from the solved $R+S+C+T+D$ layer.
- Stable comparison algebra has been reclassified as the next minimal added branch structure $A$.
- Valuation representation is **not** forced from the solved $R+S+C+T+D+A$ layer.
- Valuation representation has been reclassified as the next minimal added branch structure $V$.

### Provisional results

- It remains open whether a weaker added structure than $S$ would already suffice for realized contents/carrier.
- It remains open whether a weaker added structure than $C$ would already suffice for branch-usable locality.
- It remains open whether a weaker added structure than $T$ would already suffice for branch-usable lawful transformation.
- It remains open whether a weaker added structure than $D$ would already suffice for branch-usable readout/discrimination.
- It remains open whether a weaker added structure than $A$ would already suffice for branch-usable stable comparison.
- It remains open whether a weaker added structure than $V$ would already suffice for branch-usable valuation.
- Parameterization and differentiability may later be needed for one route to a differentiable branch.

These are not yet earned in the present pass.

### Rejected routes

- Primitive import of differentiable carriers, coordinates, metric, distance, derivatives, scalar probes, quotients, matrices, continuity, or chart structure.
- Treating refinement/compatibility as already theorem-grade from the nullity/sameness exclusions alone.
- Treating realized contents or a realized carrier as already forced from refinement/compatibility alone.
- Treating locality/cover as already theorem-grade from the solved $R+S$ layer.
- Treating lawful transformation as already theorem-grade from the solved $R+S+C$ layer.
- Treating distinguishers/signatures as already theorem-grade from the solved $R+S+C+T$ layer.
- Treating stable comparison algebra as already theorem-grade from the solved $R+S+C+T+D$ layer.
- Treating valuation as already theorem-grade from the solved $R+S+C+T+D+A$ layer.
- Treating the carrier regime produced under $R+S$ as already unique or canonical.

### Live theorem target

Determine whether a parameterization layer is forced from the solved $R+S+C+T+D+A+V$ layer, or whether parameterization must itself be introduced explicitly as the next minimal branch structure.

### Forbidden regressions

The document may not proceed upward to parameterization or differentiability until the valuation question is settled and written into the document.

---

## 1. Scope, Ontology, and Primitive Commitments

### 1.1 Root burden inherited from CF00

CF00 begins from a differentiable carrier $\mathcal M$, a local representative state-family, and local redundancy. That is already too late for an absolute first-principles account. CF000 therefore asks what must be in place before any differentiable carrier, local coordinate, or lawful local derivative can even make sense.

### 1.2 Primitive versus forbidden structure

At CF000 depth, the following are forbidden as primitive:

- differentiable manifold structure;
- local coordinates;
- tangent spaces or cotangent spaces;
- metric distance;
- point-set neighborhoods in the geometric sense;
- local derivatives, limits, or difference quotients;
- scalar-valued probes or observables;
- real parameters or small-parameter update families;
- support graphs or adjacency graphs;
- gauge connection, QGT, metric/curvature split, $J \oplus M$, constitutive fields.

If any of these appear before they are earned, the root has not moved beneath CF00.

### 1.3 What counts as a viable root for this branch

A viable root for this branch must support:

1. nontrivial distinction;
2. law rather than vacuity;
3. the possibility of falsification;
4. a route to stable comparison;
5. and, if possible, a route to differentiability.

The branch does not begin by assuming these are numerical or geometric.

### 1.4 Primitive notation convention

To prevent later overload:

- $\mathcal B$ denotes the primitive distinction-bearing bearer class.
- $\#$ denotes primitive apartness.
- $\widehat{\mathcal B}$ denotes an admissibly enriched bearer class once added branch structure is introduced.
- $\mathcal M_0^{(R)}$ denotes the candidate realized-carrier regime relative to $R$.
- $\mathcal M_0^{(R+S)}$ denotes the realized-carrier regime obtained conditionally under $R+S$.
- $\mathcal M_0$ denotes a generic realized pre-differential carrier placeholder.
- $\mathcal M$ denotes the downstream differentiable carrier earned only after later passes.
- $M$ is reserved for the dissipative symmetric operator or sector only after the later emergent split appears downstream of CF000.

No other use of plain $M$ is allowed in this document.

### 1.5 Epistemic status convention for this document

Every major layer in the derivation is labeled as one of:

- **forced from prior layer**,
- **minimal added branch structure**,
- **conditional theorem under explicit assumptions**.

If a layer is not forced from the prior layer, it is not allowed to be described as theorem-grade from that prior layer.

### 1.6 Primitive commitment of the present pass

The present pass commits only to:

1. the primitive distinction-bearing residue $({\mathcal B},\#)$,
2. the first added sharpenability discipline $L1$,
3. the explicitly added refinement/compatibility structure $R$,
4. the explicitly added realization/decisiveness layer $S$,
5. the explicitly added locality/cover structure $C$,
6. the explicitly added lawful-transformation structure $T$,
7. the explicitly added distinguisher/signature structure $D$,
8. the explicitly added stable-comparison structure $A$,
9. the explicitly added valuation-representation structure $V$.

The present pass does **not** yet commit to parameterization or differentiability.

---

## 2. Mathematical Setting and Definitions

### 2.1 Primitive bearer class and apartness

The primitive substrate at the present deepest justified level is
$$
(\mathcal B, \#),
$$
where $\mathcal B$ is a nonempty bearer class and $\#$ is a primitive nontrivial apartness relation.

### 2.2 Minimal primitive laws

The primitive relation satisfies only the weakest laws presently forced:

1. **Nonempty bearer**
   $$
   \mathcal B \neq \varnothing.
   $$

2. **Nontrivial extension**
   $$
   \exists a,b\in\mathcal B\text{ such that }a\# b.
   $$

3. **Irreflexivity**
   $$
   \neg(a\# a).
   $$

4. **Symmetry**
   $$
   a\# b \Rightarrow b\# a.
   $$

No order, topology, metric, process, comparison algebra, or valuation is yet assumed.

### 2.3 Primitive interpretation

An element of $\mathcal B$ is not yet:

- a point,
- a coordinate,
- a neighborhood,
- a state in phase space,
- a value,
- a measurable response,
- or a dynamical state.

It is only a bearer of possible nontrivial distinction.

Likewise, $a\# b$ does not yet mean metric separation, measurable difference, process difference, or local variation. It means only that $a$ and $b$ are primitively not the same in a nontrivial way.

### 2.4 First added branch commitment: sharpenability

The current pass tests whether pure distinction alone can support lawful continuation of the branch. To ask that question, the branch introduces exactly one minimal additional principle.

**Principle $L1$ (Sharpenability discipline).**  
If a distinction is to remain meaningful in a law-bearing continuation of the branch, then it must admit admissible sharpening without erasing already-witnessed distinction content.

$L1$ is not claimed to be forced from pure apartness. It is the first **minimal added branch commitment** required to test whether law-bearing continuation is possible.

### 2.5 First explicit added branch structure: refinement/compatibility

Since primitive distinction together with $L1$ does not force a unique global refinement/compatibility regime, the branch introduces refinement/compatibility explicitly.

**Added Branch Structure $R$.**  
A continuation of this branch beyond primitive distinguishability must specify:

1. an admissibly enriched bearer class $\widehat{\mathcal B}$ containing $\mathcal B$,
2. a refinement preorder $\preceq$ on $\widehat{\mathcal B}$,
3. a compatibility relation $\bowtie$ on $\widehat{\mathcal B}$,
4. preservation of apartness under sharpening,
5. stability of compatibility under sharpening.

At minimum, the added structure must satisfy:

- **R1 (reflexive refinement)**
  $$
  x \preceq x.
  $$

- **R2 (transitive refinement)**
  $$
  x \preceq y \land y \preceq z \Rightarrow x \preceq z.
  $$

- **R3 (apartness persistence)**
  $$
  x \preceq y \land y\# z \Rightarrow x\# z.
  $$

- **R4 (compatibility symmetry)**
  $$
  x \bowtie y \Rightarrow y \bowtie x.
  $$

- **R5 (refinement monotonicity of compatibility)**
  $$
  x' \preceq x \land x \bowtie y
  \Rightarrow
  \exists y' \preceq y \text{ such that } x' \bowtie y'.
  $$

$R$ is not theorem-grade from the prior layer. It is the first **minimal added branch structure**.

### 2.6 Candidate realized distinction content relative to $R$

A set $X \subseteq \widehat{\mathcal B}$ is called an **$R$-candidate realized distinction content** if it satisfies the following minimal conditions.

1. **Nonemptiness**
   $$
   X \neq \varnothing.
   $$

2. **Refinement saturation**
   $$
   x\in X \land y \preceq x \Rightarrow y \in X.
   $$

3. **Finite coherence**
   For every finite subset $F \subseteq X$, there exists $z\in X$ such that
   $$
   z \preceq f
   \qquad
   \text{for all } f\in F.
   $$

4. **Decisiveness**
   For every $b\in \widehat{\mathcal B}$, either:
   - there exists $x\in X$ with $x \bowtie b$, or
   - there exists $x\in X$ with $x \# b$.

The class of all such $R$-candidate realized contents, if nonempty, is denoted
$$
\mathcal M_0^{(R)}.
$$

This definition is not yet a theorem of existence. It is the weakest honest candidate notion of realized content available at this stage.

### 2.7 Candidate added branch structure: realization/decisiveness layer $S$

Since $R$ alone does not force realized contents, the branch introduces the next candidate added structure.

**Candidate Added Branch Structure $S$.**  
A continuation of the branch beyond $R$ must, at minimum, specify a principle strong enough to guarantee that coherent refinement content can settle into decisive realized contents. The weakest presently credible candidate consists of the following.

- **S1 (finite coherent extension)**  
  Every finite pairwise compatible family admits an admissible common refinement.

- **S2 (branch existence)**  
  Every admissible bearer lies on at least one nonempty refinement thread compatible with $R$.

- **S3 (decisive separation)**  
  Every sufficiently stable refinement thread decides every bearer by eventual compatibility or eventual apartness.

- **S4 (realization closure)**  
  Every nonempty coherent refinement thread extends to a decisive coherent content.

$S$ is **not** forced from $R$. It is introduced only as the current best **minimal added branch structure** candidate if the branch is to continue toward realization.

### 2.8 Candidate realized distinction content relative to $R+S$

Given $R+S$, a set $X\subseteq \widehat{\mathcal B}$ is called an **$(R+S)$-realized distinction content** if:

1. $X$ is nonempty,
2. $X$ is refinement-saturated,
3. $X$ is finitely coherent,
4. $X$ is decisive,
5. $X$ contains at least one refinement thread guaranteed by S2,
6. $X$ is admitted by S4 as a realization closure of some coherent thread.

The class of all such contents is denoted
$$
\mathcal M_0^{(R+S)}.
$$

At this stage $\mathcal M_0^{(R+S)}$ is a candidate realized-carrier regime. Its existence and non-canonicity have been established by the previous pass.

### 2.9 Candidate locality/cover discipline relative to $R+S$

At the present stage the branch has realized contents and a realized-carrier regime, but it does not yet have a theorem-grade notion of locality. The next candidate layer is a pre-metric cover discipline.

A **cover/locality discipline** on a realized-carrier regime $\mathcal M_0^{(R+S)}$ is a relation
$$
X \triangleleft \mathcal U,
$$
where $X \in \mathcal M_0^{(R+S)}$ and $\mathcal U \subseteq \mathcal M_0^{(R+S)}$, satisfying the following minimal clauses.

- **C1 (self-coverage)** If $X \in \mathcal U$, then $X \triangleleft \mathcal U$.
- **C2 (upward stability)** If $X \triangleleft \mathcal U$ and $\mathcal U \subseteq \mathcal V$, then $X \triangleleft \mathcal V$.
- **C3 (refinement compatibility)** If $Y$ is a realized-content sharpening of $X$ and $X \triangleleft \mathcal U$, then $Y$ is covered by a sharpening-compatible family subordinate to $\mathcal U$.
- **C4 (patch compatibility)** If $X \triangleleft \mathcal U$ and each $U \in \mathcal U$ is itself covered by a family $\mathcal V_U$, then $X$ is covered by the union of the $\mathcal V_U$ whenever the patching relations are coherent.

This cover relation is weaker than metric distance, coordinate neighborhoods, valuation, parameterization, or differentiability. It is only a pre-metric discipline of localizability and patchability on realized contents.

### 2.10 Status of locality/cover

At this stage, locality/cover is not assumed primitive. Nor is it forced by the prior layer unless proved below. The previous pass established a no-go theorem: locality/cover is not forced from the solved $R+S$ layer and must be introduced explicitly as the next minimal added branch structure $C$.

### 2.11 Candidate lawful-transformation discipline relative to $R+S+C$

At the present stage the branch has:

- primitive distinguishability,
- explicit refinement/compatibility,
- conditional and non-canonical realized contents,
- and an explicit cover/locality discipline.

It still does not yet have a theorem-grade notion of transformation.

A **lawful-transformation discipline** on a realized-carrier regime $\mathcal M_0^{(R+S)}$ equipped with cover $C$ is a class $\mathfrak T$ of partial endomorphisms
$$
\tau : \operatorname{Dom}(\tau) \to \mathcal M_0^{(R+S)}
$$
with $\operatorname{Dom}(\tau) \subseteq \mathcal M_0^{(R+S)}$, satisfying the following minimal clauses.

- **T1 (identity act)** There exists an identity transformation $\mathrm{id}$ on $\mathcal M_0^{(R+S)}$.
- **T2 (admissible composability)** If $\tau,\sigma \in \mathfrak T$ and the image of $\sigma$ lies in the domain of $\tau$, then the composite $\tau\circ\sigma$ is again in $\mathfrak T$.
- **T3 (realized-content preservation)** If $X \in \operatorname{Dom}(\tau)$, then $\tau(X)$ is again a realized distinction content.
- **T4 (cover respect)** If $X \triangleleft \mathcal U$, then whenever $\tau$ is defined on all members of $\mathcal U$, the image $\tau(X)$ is covered by the image family $\tau[\mathcal U]$ or by a cover-refinement subordinate to it.
- **T5 (nontriviality)** At least one $\tau \in \mathfrak T$ is not equal to the identity on its full domain.

This structure is weaker than distinguishers/signatures, comparison algebra, valuation, parameterization, or differentiability. It supplies only admissible process-like movement on realized contents with composition and cover respect.

### 2.12 Status of lawful transformation

At this stage, lawful transformation is not assumed primitive. The previous pass established a no-go theorem: branch-usable lawful transformation is not forced from the solved $R+S+C$ layer and must be introduced explicitly as the next minimal added branch structure $T$.

### 2.13 Candidate distinguisher/signature discipline relative to $R+S+C+T$

At the present stage the branch has:

- primitive distinguishability,
- explicit refinement/compatibility,
- conditional and non-canonical realized contents,
- an explicit cover/locality discipline,
- and an explicitly added lawful-transformation discipline.

It still does not yet have a theorem-grade notion of readout, discrimination, or signature-bearing outcome.

A **distinguisher/signature discipline** on a realized-carrier regime $\mathcal M_0^{(R+S)}$ equipped with cover $C$ and lawful transformations $T$ consists of:

1. a nonempty signature class $\mathfrak{Sig}$;
2. an event domain
   $$
   \mathcal E_T := \{(X,\tau) : X\in \operatorname{Dom}(\tau),\; \tau\in \mathfrak T\};
   $$
3. a nonempty class $\mathfrak D$ of partial readout acts
   $$
   \delta : \operatorname{Dom}(\delta) \to \mathfrak{Sig},
   \qquad
   \operatorname{Dom}(\delta) \subseteq \mathcal E_T,
   $$
   satisfying the following minimal clauses.

- **D1 (event admissibility)** Each distinguisher is defined only on admissible transformation-events in $\mathcal E_T$.
- **D2 (extensional event identity)** If two admissible event descriptions coincide in the solved layer, then every distinguisher defined on both assigns the same signature to them.
- **D3 (repeatable readout)** Whenever the same admissible event is presented again to the same distinguisher, the same signature is returned.
- **D4 (branch-usable nontriviality)** At least one distinguisher separates at least one pair of admissible events not already identified by solved-layer equality.

This structure is weaker than comparison algebra, valuation, parameterization, or differentiability. It supplies only readout-level discrimination and outcome identity. It does not yet order signatures, compose signatures, or assign numerical value.

### 2.14 Status of distinguishers/signatures

At this stage, distinguishers/signatures are not assumed primitive. Nor are they forced by the prior layer unless proved below. The theorem target solved by the previous pass was:

> determine whether the solved layer $R+S+C+T$ forces a branch-usable distinguisher/signature discipline, or whether such a discipline must be introduced explicitly as the next minimal added branch structure.

The answer was negative, and the branch now proceeds to the comparison-algebra question.


### 2.15 Candidate stable-comparison algebra relative to $R+S+C+T+D$

At the present stage the branch has:

- primitive distinguishability,
- explicit refinement/compatibility,
- conditional and non-canonical realized contents,
- an explicit cover/locality discipline,
- an explicitly added lawful-transformation discipline,
- and an explicitly added distinguisher/signature discipline.

It still does not yet have a theorem-grade notion of stable comparison.

A **stable comparison algebra** on a solved layer $(R+S+C+T+D)$ consists of:

1. a nonempty class $\mathfrak C$ of comparison classes,
2. a surjective class-forming map
   $$
   q : \mathfrak{Sig} \to \mathfrak C,
   $$
3. a preorder
   $$
   \sqsubseteq\; \subseteq \mathfrak C \times \mathfrak C,
   $$
4. a partial binary operation
   $$
   \odot : \operatorname{Dom}(\odot) \subseteq \mathfrak C \times \mathfrak C \to \mathfrak C,
   $$
   satisfying the following minimal clauses.

- **A1 (signature class identity)** If two signatures are identified by the solved readout layer as the same signature, then they determine the same comparison class.
- **A2 (preorder discipline)** $\sqsubseteq$ is reflexive and transitive on $\mathfrak C$.
- **A3 (branch-usable nontriviality)** At least one pair of comparison classes is not identified by mutual preorder collapse.
- **A4 (comparison stability under admissible readout reuse)** If the same admissible event is presented again to the same distinguisher and yields the same signature, then its comparison class is preserved.
- **A5 (partial composition respect)** Whenever comparison composition is declared on a pair $(c_1,c_2)$, the class $c_1 \odot c_2$ depends only on the comparison classes and not on hidden presentation choices of the underlying signatures.

This structure is weaker than valuation, parameterization, or differentiability. It does not yet assign numbers, select coordinates, or impose first-order smooth structure. It supplies only stable comparison-class identity, a comparison relation, and optional class-level composition.

### 2.16 Status of stable comparison algebra

At this stage, stable comparison algebra is not assumed primitive. The previous pass established by no-go theorem that it is not forced by the prior layer and must therefore be introduced explicitly as the next minimal added branch structure $A$ if the branch is to continue toward valuation, parameterization, or differentiability.


### 2.17 Candidate valuation representation relative to $R+S+C+T+D+A$

At the present stage the branch has:

- primitive distinguishability,
- explicit refinement/compatibility,
- conditional and non-canonical realized contents,
- an explicit cover/locality discipline,
- an explicitly added lawful-transformation discipline,
- an explicitly added distinguisher/signature discipline,
- and an explicitly added stable-comparison algebra.

It still does not yet have a theorem-grade notion of valuation.

A **valuation representation** on a solved layer $(R+S+C+T+D+A)$ consists of:

1. an ordered composition regime
   $$
   (\mathbb V, \leq_{\mathbb V}, \oplus, 0_{\mathbb V}),
   $$
   where $\leq_{\mathbb V}$ is a preorder on $\mathbb V$, $\oplus$ is an associative binary operation on $\mathbb V$ with neutral element $0_{\mathbb V}$, and $\oplus$ is monotone in each argument with respect to $\leq_{\mathbb V}$;
2. a map
   $$
   
u : \mathfrak C 	o \mathbb V,
   $$
   satisfying the following minimal clauses.

- **V1 (class identity respect)** If $c_1=c_2$ in $\mathfrak C$, then $
u(c_1)=
u(c_2)$.
- **V2 (order preservation)** If $c_1 \sqsubseteq c_2$, then
  $$
  
u(c_1) \leq_{\mathbb V} 
u(c_2).
  $$
- **V3 (strict noncollapse of strict comparison)** If
  $$
  c_1 \sqsubseteq c_2
  \qquad	ext{and}\qquad
  
eg(c_2 \sqsubseteq c_1),
  $$
  then
  $$
  
u(c_1) <_{\mathbb V} 
u(c_2),
  $$
  where $x <_{\mathbb V} y$ abbreviates $x \leq_{\mathbb V} y$ and $
eg(y \leq_{\mathbb V} x)$.
- **V4 (comparison-composition respect)** Whenever $c_1 \odot c_2$ is defined,
  $$
  
u(c_1 \odot c_2) = 
u(c_1) \oplus 
u(c_2).
  $$
- **V5 (neutral normalization when available)** If $\mathfrak C$ contains a comparison class $e_{\mathfrak C}$ acting as a neutral element for all comparison compositions on which it is defined, then
  $$
  
u(e_{\mathfrak C}) = 0_{\mathbb V}.
  $$

This structure is weaker than parameterization or differentiability. It assigns order-compatible values to stable comparison classes, but it does not yet supply coordinates, update parameters, chart transitions, or derivatives.

### 2.18 Status of valuation representation

At this stage, valuation representation is not assumed primitive. The theorem target of the present pass is therefore:

> determine whether the solved layer $R+S+C+T+D+A$ forces a branch-usable valuation representation, or whether such a representation must be introduced explicitly as the next minimal added branch structure.


## 3. Foundational Construction

### 3.1 Nullity exclusion

**Theorem 3.1.1 (Nullity exclusion).**  
Absolute nullity is not a viable root for this branch.

**Proof.**  
A physical branch of theory must at minimum permit a difference between success and failure of a statement, between one admissible state and another, and between a law and the absence of law. Absolute nullity supports none of these because it contains no bearer, no distinction, and no possible witness structure. Therefore nullity cannot serve as the root of a falsifiable formal branch. This is a theorem about formal-role viability, not a universal metaphysical theorem about all possible notions of nothing. $\square$

### 3.2 Undifferentiated sameness exclusion

**Theorem 3.2.1 (Undifferentiated sameness exclusion).**  
Absolute undifferentiated sameness is not a viable root for this branch.

**Proof.**  
If all admissible presentations are undifferentiated, then no nontrivial comparison can be made. Comparison, persistence, lawful separation, and falsification all collapse, because there is no content by which one state could fail to match another. Thus absolute undifferentiated sameness is as unusable for this branch as nullity, although for a different reason: it has bearer-like content but no nontrivial distinction. $\square$

### 3.3 Weakest surviving primitive

**Theorem 3.3.1 (Weakest surviving primitive).**  
For this branch, once nullity and absolute undifferentiated sameness are excluded, the weakest surviving primitive is a distinction-bearing multiplicity $({\mathcal B},\#)$ satisfying nonempty bearer, nontrivial extension, irreflexivity, and symmetry.

**Proof.**  
Nullity excludes bearer and relation altogether. Undifferentiated sameness excludes nontrivial distinction. Therefore any surviving root must contain at least a nonempty bearer class and at least one nontrivial distinction relation on it. Any stronger primitive package — order, cover, metric, value, update, or process — adds content not forced by those two exclusions alone. Hence $({\mathcal B},\#)$ is the weakest currently justified root. $\square$

### 3.4 First branch fork: can pure distinguishability support law?

Pure apartness is enough to exclude nullity and sameness. It is not enough by itself to support law.

If the branch is to support law rather than one-shot distinction, then distinctions must be:

1. revisitably meaningful,
2. sharpenable without erasure of already-witnessed content,
3. and stably reusable in later comparison contexts.

Principle $L1$ expresses this demand, but $L1$ itself does not yet define a stable global refinement or compatibility regime. The first live theorem target was therefore whether $L1$ together with pure apartness is enough to force such a regime. That question has already been resolved negatively.

### 3.5 No-go theorem for forcing refinement/compatibility

**Theorem 3.5.1 (No-go theorem for refinement forcing).**  
Primitive distinction-bearing multiplicity $({\mathcal B},\#)$ together with the sharpenability discipline $L1$ does **not** force a unique or canonical stable refinement/compatibility regime. Therefore refinement/compatibility is not theorem-grade from the prior layer. It must be introduced explicitly as the first minimal added branch structure if the branch is to continue toward law.

**Hypotheses.**

1. $({\mathcal B},\#)$ satisfies the laws of Section 2.2.
2. Principle $L1$ holds: physically meaningful distinction admits admissible sharpening without erasing already-witnessed distinction content.
3. No further primitive assumptions are added regarding order, compatibility, locality, value, process, or comparison.

**Conclusion.**

Under these hypotheses alone, there is no unique forced global refinement preorder or compatibility relation. More strongly, there exist distinct non-isomorphic sharpenability realizations compatible with the same primitive substrate and with $L1$, but yielding inequivalent refinement/compatibility structures. Hence refinement/compatibility is not forced from the prior layer.

**Proof.**

Fix a primitive substrate with two distinguishable bearers,
$$
a,b \in \mathcal B,
\qquad
 a\# b.
$$
By $L1$, if this distinction is to remain meaningful in a law-bearing continuation, then there must exist some admissible sharpening witness for $a$ and some admissible sharpening witness for $b$ preserving the already-witnessed distinction content.

Now consider two distinct enrichments of the same primitive substrate.

#### Realization R1: branchwise sharpening without global comparability

Adjoin sharpened witnesses $a_1$ and $b_1$ with the intended reading that $a_1$ sharpens $a$ and $b_1$ sharpens $b$. Define the only nontrivial sharpening facts to be
$$
a_1 \preceq a,
\qquad
b_1 \preceq b,
$$
and include reflexive closure. Introduce no further cross-comparability and no compatibility relation beyond identity-level admissibility.

This realizes $L1$: both $a$ and $b$ admit sharpenings preserving their witnessed distinction. But it yields only a sparse branchwise refinement structure.

#### Realization R2: iterated sharpening with compatible coarsenings

Adjoin an infinite descending sharpening chain for each bearer,
$$
\cdots \preceq a_2 \preceq a_1 \preceq a,
\qquad
\cdots \preceq b_2 \preceq b_1 \preceq b,
$$
again preserving $a\# b$ along each chain. Now also adjoin a coarse compatibility token $c$ that is not itself apart from either $a$ or $b$, and stipulate that certain admissible comparison contexts may pass through $c$ as a common coarse context without identifying $a$ and $b$ or making them refinements of one another.

This also realizes $L1$. It yields a much richer sharpening and compatibility regime than R1.

The two realizations are not isomorphic as refinement/compatibility structures:

- R1 has only isolated one-step branchwise refinement.
- R2 has infinite branchwise refinement and an additional compatibility organization through coarse context tokens.

Yet both respect the same primitive substrate $({\mathcal B},\#)$ and the same sharpenability discipline $L1$. Therefore $L1$ does not determine a unique global refinement/compatibility regime. Since no uniqueness, canonicity, or forcing theorem follows from the prior layer alone, refinement/compatibility is not theorem-grade from primitive distinction plus $L1$.

Hence the branch must add refinement/compatibility explicitly if it wishes to continue beyond pure distinguishability. $\square$

### 3.6 What Theorem 3.5.1 does and does not prove

**What it proves.**

- Primitive distinction plus sharpenability is insufficient to force a unique stable refinement/compatibility regime.
- Any continuation of the branch that needs such a regime must add it explicitly.

**What it does not prove.**

- It does not show that refinement is impossible.
- It does not show that cover, locality, lawful transformation, valuation, or differentiability are impossible.
- It does not show that all refinement systems are equally good.
- It does not identify the unique best added refinement system.

It proves only the no-go result needed here: refinement/compatibility is **not forced** from the prior layer.

### 3.7 No-go theorem for realized-carrier forcing from $R$

**Theorem 3.7.1 (No-go theorem for realized-carrier forcing from $R$).**  
The explicitly added refinement/compatibility structure $R$ is **not** sufficient, by itself, to force stable realized distinction contents or a realized carrier layer. More precisely:

1. there exist $R$-models for which $\mathcal M_0^{(R)} = \varnothing$;
2. there exist $R$-models for which $\mathcal M_0^{(R)} \neq \varnothing$ and contains multiple inequivalent candidate realized contents;
3. therefore neither the existence nor the canonicity of a realized carrier is forced from $R$ alone.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\#)$ satisfies Section 2.2.
2. The branch has adopted the first added structure $R$ of Section 2.5.
3. No additional structure beyond $R$ is assumed regarding realization closure, sharpness, decisiveness, localization, or maximal extension.

**Conclusion.**

Under these hypotheses alone, $R$ does not force stable realized distinction contents and does not force a canonical realized carrier layer.

**Proof.**

We use the definition of $R$-candidate realized distinction content from Section 2.6.

#### Model A: an $R$-model with no realized contents

Let
$$
\widehat{\mathcal B}_A = \{a,b,c\},
$$
with primitive apartness given only by
$$
a \# b,
$$
and no apartness involving $c$ except irreflexive triviality. Let refinement be reflexive only,
$$
x \preceq x,
$$
for all $x \in \widehat{\mathcal B}_A$, and let compatibility be identity only,
$$
x \bowtie y \iff x=y.
$$

This satisfies the axioms of $R$.

Now test candidate realized contents.

A singleton such as $\{a\}$ is nonempty, refinement-saturated, and finitely coherent. But it fails decisiveness for $c$: there is no $x\in\{a\}$ with $x \bowtie c$, because compatibility is identity only and $a\neq c$; there is also no $x\in\{a\}$ with $x\# c$, because no apartness between $a$ and $c$ has been stipulated. The same failure occurs for $\{b\}$ and $\{c\}$.

Any larger subset containing both $a$ and $b$ fails finite coherence, because there is no $z$ with $z\preceq a$ and $z\preceq b$ under reflexive-only refinement. Any subset containing $c$ fails decisiveness against at least one of $a$ or $b$. Therefore
$$
\mathcal M_0^{(R)} = \varnothing
$$
in Model A.

So $R$ does not force existence of realized contents.

#### Model B: an $R$-model with multiple realized contents

Let
$$
\widehat{\mathcal B}_B = \{a,b\},
$$
with primitive apartness
$$
a \# b,
$$
refinement again reflexive only, and compatibility identity only.

This also satisfies $R$. Now both singleton sets $\{a\}$ and $\{b\}$ are $R$-candidate realized contents, so
$$
\mathcal M_0^{(R)} = \{\{a\},\{b\}\}.
$$
Thus even when realized contents exist, they need not be unique or canonical.

Since there is at least one $R$-model with no realized contents and at least one $R$-model with multiple inequivalent realized contents, neither existence nor canonicity of a realized carrier is forced by $R$ alone. $\square$

### 3.8 What Theorem 3.7.1 does and does not prove

**What it proves.**

- $R$ is sufficient to make the realization question meaningful.
- $R$ is insufficient to force realized contents.
- $R$ is insufficient to force a canonical realized carrier.

**What it does not prove.**

- It does not show that realized contents are impossible.
- It does not show that no carrier can be earned.
- It does not show that every realization discipline beyond $R$ is equally good.
- It does not yet identify the unique best realization discipline.

The theorem establishes only the no-go result required here: realization is not forced from $R$ alone.

### 3.9 Conditional realization theorem from $R+S$

**Theorem 3.9.1 (Conditional existence of realized contents under $R+S$).**  
Assume the primitive substrate $({\mathcal B},\#)$ of Section 2.2, the minimal added structure $R$ of Section 2.5, and the realization layer $S$ of Section 2.7. Then:

1. for every admissible bearer $b\in \widehat{\mathcal B}$, there exists at least one $(R+S)$-realized distinction content $X$ with some element of $X$ refining $b$;
2. therefore $\mathcal M_0^{(R+S)} \neq \varnothing$;
3. hence a realized carrier regime exists under the explicit assumptions $R+S$.

**Epistemic status.**  
This theorem is **conditional under explicit assumptions**. It is not forced from primitive distinction alone and not forced from $R$ alone. The role of $S$ is exactly to supply the missing realization/decisiveness content.

**Proof.**

Fix any admissible bearer $b\in\widehat{\mathcal B}$.

By S2, there exists a nonempty refinement thread $T_b$ compatible with $R$ and lying beneath or through $b$. By the meaning of a refinement thread, every finite subset of $T_b$ is pairwise compatible and ordered by refinement.

By S1, every finite pairwise compatible subset of $T_b$ admits an admissible common refinement. Therefore $T_b$ is finitely coherent in the sense required for realization.

By S3, the thread $T_b$ is decisive with respect to every bearer in $\widehat{\mathcal B}$: for each $c\in\widehat{\mathcal B}$, the thread eventually produces a refinement stage that is either compatible with $c$ or apart from $c$.

By S4, every nonempty coherent refinement thread extends to a decisive coherent content. Apply S4 to $T_b$. Then there exists a decisive coherent content $X_b$ extending $T_b$.

Because $T_b$ is nonempty, $X_b$ is nonempty. Because $X_b$ extends a refinement thread and is required by S4 to be coherent, it is refinement-saturated and finitely coherent. Because S4 yields a decisive coherent content, $X_b$ is decisive. Therefore $X_b$ satisfies the definition of an $(R+S)$-realized distinction content.

Since $b$ was arbitrary, every admissible bearer lies on at least one realized distinction content. Hence $\mathcal M_0^{(R+S)}$ is nonempty. Therefore a realized carrier regime exists under $R+S$. $\square$

### 3.10 Non-canonicity theorem for the realized carrier under $R+S$

**Theorem 3.10.1 (Non-canonicity under $R+S$).**  
The assumptions $R+S$ are sufficient to force existence of a realized carrier regime, but they do **not** force that regime to be unique or canonical.

**Hypotheses.**

1. $({\mathcal B},\#)$ satisfies Section 2.2.
2. $R$ and $S$ hold.
3. No additional structure is assumed concerning maximality, uniqueness of decisive closures, localization, or choice principles that would select one realized extension over all others.

**Conclusion.**

Under these hypotheses, realized contents exist, but there may be multiple inequivalent realized contents and multiple inequivalent carrier regimes. Therefore the realized carrier under $R+S$ is generally non-canonical.

**Proof.**

We construct an explicit model satisfying $R+S$ with more than one realized distinction content.

Let
$$
\widehat{\mathcal B}_C = \{a_0,a_1,b_0,b_1\},
$$
with apartness relations
$$
a_0 \# b_0,
\qquad
 a_1 \# b_1,
$$
and no cross apartness between the $a$-chain and the $b$-chain beyond those stated. Let refinement be generated by
$$
a_1 \preceq a_0,
\qquad
b_1 \preceq b_0,
$$
with reflexive and transitive closure. Let compatibility be identity together with compatibility along each chain.

Now choose refinement threads
$$
T_a = \{a_1,a_0\},
\qquad
T_b = \{b_1,b_0\}.
$$
These are nonempty, coherent refinement threads. By S3, assume each thread decisively separates itself from the opposite branch. By S4, each extends to a decisive coherent content, say
$$
X_a \supseteq T_a,
\qquad
X_b \supseteq T_b.
$$
Then both $X_a$ and $X_b$ are realized distinction contents. They are inequivalent because one is anchored on the $a$-branch and the other on the $b$-branch, and the primitive apartness relations forbid their identification.

Thus the realized carrier regime contains at least two inequivalent realized contents. Therefore existence does not imply uniqueness, and $R+S$ does not force a canonical realized carrier. $\square$

### 3.11 What Theorems 3.9.1 and 3.10.1 do and do not prove

**What they prove.**

- $S$ improves on $R$ in a theorem-bearing way: under $R+S$, realized contents exist.
- Under $R+S$, a realized carrier regime exists.
- Under $R+S$, that regime is generally non-canonical.

**What they do not prove.**

- They do not show that $S$ is forced from $R$.
- They do not show that $S$ is the unique weakest realization principle.
- They do not show that a weaker structure than $S$ could not suffice.
- They do not yet derive locality, lawful transformation, stable comparison, valuation, parameterization, or differentiability.

So the correct status is:

- $S$ is a **minimal added branch structure candidate**,
- existence of realized contents/carrier is a **conditional theorem under $R+S$**,
- canonicity is **not** obtained.

### 3.12 No-go theorem for forcing locality/cover from $R+S$

**Theorem 3.12.1 (No-go theorem for forcing locality/cover from $R+S$).**  
The solved layer consisting of primitive distinguishability, the added refinement/compatibility structure $R$, and the added realization/decisiveness layer $S$ is **not** sufficient to force a unique or canonical cover/locality discipline on the realized-carrier regime $\mathcal M_0^{(R+S)}$. More strongly:

1. there exist $R+S$-models with the same realized-carrier regime that admit inequivalent cover/locality structures satisfying C1--C4;
2. there exist $R+S$-models in which no branch-usable cover discipline is determined unless further locality data are stipulated;
3. therefore locality/cover is not theorem-grade from the solved $R+S$ layer and must be introduced explicitly as the next minimal added branch structure if the branch is to proceed toward law-bearing locality.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\#)$ satisfies Section 2.2.
2. The added branch structures $R$ and $S$ satisfy Sections 2.5 and 2.7.
3. The conditional existence and non-canonicity results of Theorems 3.9.1 and 3.10.1 hold.
4. No additional locality axioms, gluing rules, or cover-selection principles are assumed beyond $R+S$.

**Conclusion.**

Under these hypotheses alone, no unique or canonical cover/locality discipline is forced on $\mathcal M_0^{(R+S)}$. If the branch wishes to continue toward locality before metric geometry, it must add locality/cover explicitly.

**Proof.**

Fix any $R+S$-model with a non-canonical realized-carrier regime, as provided by Theorem 3.10.1. Let
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\}
$$
be a realized-carrier regime with two inequivalent realized contents.

We now define two distinct cover disciplines on the same realized-carrier regime.

#### Locality realization C-discrete

Define a cover relation $\triangleleft_d$ by
$$
X \triangleleft_d \mathcal U
\quad\text{if and only if}\quad
X \in \mathcal U.
$$
This is the discrete cover discipline. It satisfies:

- C1, because membership implies self-coverage;
- C2, because if $X\in\mathcal U$ and $\mathcal U\subseteq\mathcal V$, then $X\in\mathcal V$;
- C3, because any realized-content sharpening of $X$ is covered only by families containing that sharpening;
- C4, because patching is trivial: every cover is already by explicit membership.

So $\triangleleft_d$ is a valid cover/locality discipline.

#### Locality realization C-indiscrete

Define a cover relation $\triangleleft_i$ by
$$
X \triangleleft_i \mathcal U
\quad\text{if and only if}\quad
\mathcal U \neq \varnothing.
$$
This is the indiscrete cover discipline. It also satisfies:

- C1, trivially, if $X\in\mathcal U$ then $\mathcal U\neq\varnothing$;
- C2, because any superset of a nonempty family is nonempty;
- C3, because every realized-content sharpening is covered by every nonempty family;
- C4, because unions of nonempty patch families remain nonempty whenever patching is coherent.

So $\triangleleft_i$ is also a valid cover/locality discipline.

But $\triangleleft_d$ and $\triangleleft_i$ are inequivalent. In the discrete discipline, a realized content is covered only by families that explicitly contain it. In the indiscrete discipline, every realized content is covered by every nonempty family. These yield different locality behavior on the same realized-carrier regime. Therefore the solved layer $R+S$ does not force a unique or canonical cover relation.

To prove the stronger claim that some $R+S$-models do not determine a branch-usable cover discipline without further data, note that $R+S$ by itself specifies realized contents and decisiveness but says nothing about which families should count as localizing, how patching should respect branch intent, or which coverings are too coarse to be physically usable. Hence branch-usable locality is underdetermined until further cover data are added.

Therefore locality/cover is not theorem-grade from $R+S$ and must be introduced explicitly as the next minimal added branch structure. $\square$

### 3.13 Explicit introduction of locality/cover as the next added branch structure

Since locality/cover is not forced from the solved layer, the branch now introduces it explicitly.

**Added Branch Structure $C$.**  
A continuation of the branch beyond realized-carrier existence must specify a pre-metric cover/locality discipline on $\mathcal M_0^{(R+S)}$ satisfying C1--C4 together with any extra gluing or locality-selection principles needed for the intended branch continuation.

$C$ is not forced from the prior layer. It is the next **minimal added branch structure** required if the branch wishes to continue toward pre-metric locality.

### 3.14 What Theorem 3.12.1 does and does not prove

**What it proves.**

- The solved $R+S$ layer does not force a unique or canonical locality/cover discipline.
- The branch cannot treat locality as theorem-grade from realized-carrier existence alone.
- Any continuation toward locality must add locality/cover explicitly.

**What it does not prove.**

- It does not show that locality is impossible.
- It does not show that every cover discipline is equally good.
- It does not show that C1--C4 are uniquely minimal in all imaginable branches.
- It does not derive lawful transformation, comparison, valuation, parameterization, or differentiability.

So the correct status is:

- locality/cover is **not forced from $R+S$**,
- locality/cover is the next **minimal added branch structure** $C$,
- no upward climb beyond locality is licensed until later passes settle the next staircase question.

### 3.15 No-go theorem for forcing lawful transformation from $R+S+C$

The present pass addresses the next live question: whether the solved layer $R+S+C$, together with conditional and non-canonical realized-carrier existence and explicit cover discipline, forces a branch-usable lawful-transformation layer.

**Theorem 3.15.1 (No-go theorem for forcing lawful transformation from $R+S+C$).**  
The solved layer consisting of primitive distinguishability, the added refinement/compatibility structure $R$, the added realization/decisiveness layer $S$, and the explicitly added locality/cover structure $C$ is **not** sufficient to force a unique or canonical branch-usable lawful-transformation discipline on the realized-carrier regime $\mathcal M_0^{(R+S)}$. More strongly:

1. there exist $R+S+C$-models with the same realized-carrier regime and the same cover discipline that admit inequivalent lawful-transformation disciplines satisfying T1--T5;
2. there exist $R+S+C$-models in which no nontrivial branch-usable transformation layer is determined unless further process data are stipulated;
3. therefore lawful transformation is not theorem-grade from the solved $R+S+C$ layer and must be introduced explicitly as the next minimal added branch structure if the branch is to proceed toward comparison, valuation, and differentiability.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\#)$ satisfies Section 2.2.
2. The added branch structures $R$, $S$, and $C$ satisfy Sections 2.5, 2.7, and 2.9.
3. The conditional existence and non-canonicity results of Theorems 3.9.1 and 3.10.1 hold.
4. The no-go result for forced locality from $R+S$ and the explicit addition of $C$ hold as in Theorem 3.12.1 and Section 3.13.
5. No additional process axioms, sequential-order axioms, composition-selection principles, or persistence principles are assumed beyond $R+S+C$.

**Conclusion.**

Under these hypotheses alone, no unique or canonical branch-usable lawful-transformation discipline is forced on $\mathcal M_0^{(R+S)}$. If the branch wishes to continue toward distinguishers, comparison, valuation, and differentiability, it must add lawful transformation explicitly.

**Proof.**

Fix any $R+S+C$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\}
$$
and a fixed cover discipline $\triangleleft$ satisfying C1--C4. The existence of such a model is guaranteed by the previous pass.

We define two distinct lawful-transformation disciplines on the same solved pre-transformation layer.

#### Transformation realization T-id

Let
$$
\mathfrak T_{\mathrm{id}} = \{\mathrm{id}\},
$$
where $\mathrm{id}$ is the identity transformation on $\mathcal M_0^{(R+S)}$.

This satisfies T1. It satisfies T2 because $\mathrm{id}\circ\mathrm{id}=\mathrm{id}$. It satisfies T3 because the identity preserves realized contents. It satisfies T4 because if $X \triangleleft \mathcal U$, then $\mathrm{id}(X)=X$ is covered by $\mathrm{id}[\mathcal U]=\mathcal U$ under the same cover. However, it fails T5, the nontriviality clause. Therefore $\mathfrak T_{\mathrm{id}}$ is not yet branch-usable in the sense required by Section 2.11.

This shows that the solved pre-transformation layer does not itself guarantee nontrivial process content.

#### Transformation realization T-swap

Now define a nontrivial involution $\sigma$ on the same carrier regime by
$$
\sigma(X_a)=X_b,
\qquad
\sigma(X_b)=X_a.
$$
Let
$$
\mathfrak T_{\mathrm{swap}} = \{\mathrm{id},\sigma\}.
$$
Then:

- T1 holds because $\mathrm{id}\in\mathfrak T_{\mathrm{swap}}$.
- T2 holds because $\sigma\circ\sigma=\mathrm{id}$ and compositions with identity stay in $\mathfrak T_{\mathrm{swap}}$.
- T3 holds because $\sigma$ maps realized contents to realized contents.
- T4 holds provided the chosen cover discipline treats $X_a$ and $X_b$ symmetrically or admits image covers subordinate to the original cover families.
- T5 holds because $\sigma$ is non-identity.

Thus $\mathfrak T_{\mathrm{swap}}$ is a branch-usable lawful-transformation discipline on the same realized carrier and same cover discipline.

The two disciplines are inequivalent:

- $\mathfrak T_{\mathrm{id}}$ contains no nontrivial transformation,
- $\mathfrak T_{\mathrm{swap}}$ contains a nontrivial involution.

Therefore the solved layer $R+S+C$ does not force a unique transformation discipline. More strongly, it does not even force existence of a nontrivial branch-usable transformation discipline, because the identity-only realization is still compatible with the prior solved layer until one explicitly demands nontrivial process content.

To prove the stronger claim that some $R+S+C$-models do not determine a branch-usable transformation layer without further data, observe that $R+S+C$ specifies distinction, refinement, realization, and local cover, but says nothing about:

- which realized contents may act on which others,
- whether non-identity acts exist,
- whether acts compose sequentially,
- whether transformation should preserve or permute cover families,
- or what counts as admissible process rather than arbitrary correspondence.

Hence branch-usable transformation is underdetermined until further process data are added. Therefore lawful transformation is not theorem-grade from the solved $R+S+C$ layer and must be introduced explicitly as the next minimal added branch structure. $\square$

### 3.16 Explicit introduction of lawful transformation as the next added branch structure

Since lawful transformation is not forced from the solved layer, the branch now introduces it explicitly.

**Added Branch Structure $T$.**  
A continuation of the branch beyond realized-carrier existence and explicit locality must specify a lawful-transformation discipline $\mathfrak T$ on $\mathcal M_0^{(R+S)}$ satisfying T1--T5 together with any extra compositional, persistence, or admissibility principles required for the intended branch continuation.

$T$ is not forced from the prior layer. It is the next **minimal added branch structure** required if the branch wishes to continue toward distinguishers, stable comparison, valuation, parameterization, or differentiability.

### 3.17 What Theorem 3.15.1 does and does not prove

**What it proves.**

- The solved $R+S+C$ layer does not force a unique or canonical lawful-transformation discipline.
- The branch cannot treat transformation as theorem-grade from realized-carrier existence plus cover alone.
- Any continuation toward comparison, valuation, or differentiability must add lawful transformation explicitly.

**What it does not prove.**

- It does not show that lawful transformation is impossible.
- It does not show that every transformation discipline is equally good.
- It does not show that T1--T5 are uniquely minimal in all imaginable branches.
- It does not derive distinguishers/signatures, stable comparison, valuation, parameterization, or differentiability.

So the correct status is:

- lawful transformation is **not forced from $R+S+C$**,
- lawful transformation is the next **minimal added branch structure** $T$,
- no upward climb beyond transformation is licensed until later passes settle the next staircase question.

### 3.18 No-go theorem for forcing distinguishers/signatures from $R+S+C+T$

**Theorem 3.18.1 (No-go theorem for forcing distinguishers/signatures from $R+S+C+T$).**  
The solved layer consisting of primitive distinguishability, the added refinement/compatibility structure $R$, the added realization/decisiveness layer $S$, the explicitly added locality/cover structure $C$, and the explicitly added lawful-transformation structure $T$ is **not** sufficient to force a unique or canonical branch-usable distinguisher/signature discipline on the event domain $\mathcal E_T$. More strongly:

1. there exist $R+S+C+T$-models with the same realized-carrier regime, the same cover discipline, and the same lawful-transformation discipline that admit inequivalent distinguisher/signature layers satisfying D1--D4;
2. there exist $R+S+C+T$-models in which no branch-usable nontrivial distinguisher/signature layer is determined unless further readout data are stipulated;
3. therefore distinguishers/signatures are not theorem-grade from the solved $R+S+C+T$ layer and must be introduced explicitly as the next minimal added branch structure if the branch is to proceed toward stable comparison, valuation, parameterization, and differentiability.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\#)$ satisfies Section 2.2.
2. The added branch structures $R$, $S$, $C$, and $T$ satisfy Sections 2.5, 2.7, 2.9, and 2.11.
3. The conditional existence and non-canonicity results of Theorems 3.9.1 and 3.10.1 hold.
4. The no-go results for forced locality and forced lawful transformation, together with the explicit additions of $C$ and $T$, hold as in Theorems 3.12.1 and 3.15.1 and Sections 3.13 and 3.16.
5. No additional observability axioms, outcome-identity axioms, signature-composition axioms, or readout-selection principles are assumed beyond $R+S+C+T$.

**Conclusion.**

Under these hypotheses alone, no unique or canonical branch-usable distinguisher/signature discipline is forced on $\mathcal E_T$. If the branch wishes to continue toward stable comparison, valuation, parameterization, or differentiability, it must add distinguishers/signatures explicitly.

**Proof.**

Fix any $R+S+C+T$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\},
$$
a fixed cover discipline $\triangleleft$, and a fixed lawful-transformation discipline
$$
\mathfrak T = \{\mathrm{id}, \sigma\},
$$
where
$$
\sigma(X_a)=X_b,
\qquad
\sigma(X_b)=X_a.
$$
Then the associated event domain is
$$
\mathcal E_T = \{(X_a,\mathrm{id}), (X_b,\mathrm{id}), (X_a,\sigma), (X_b,\sigma)\}.
$$
We now define three distinct readout realizations on the same solved pre-distinguisher layer.

#### Realization D-void: no branch-usable distinguisher/signature discipline determined

Take no signature class and no nontrivial readout acts. The solved layer $R+S+C+T$ does not by itself specify any codomain of outcomes, any event-to-outcome assignment, or any criterion by which two outcomes count as the same or different. Therefore nothing in the solved layer alone forces a nonempty branch-usable distinguisher/signature discipline.

This already proves that existence of a branch-usable nontrivial readout layer is not forced.

#### Realization D-trivial: constant readout discipline

Let
$$
\mathfrak{Sig}_{\mathrm{triv}} = \{\mathtt{const}\}
$$
be a singleton signature class, and let
$$
\mathfrak D_{\mathrm{triv}} = \{\delta_{\mathrm{triv}}\}
$$
with
$$
\delta_{\mathrm{triv}}(e)=\mathtt{const}
\qquad
\text{for all } e\in \mathcal E_T.
$$
Then D1, D2, and D3 hold automatically. D4 fails, because no pair of events is separated by the readout. So this realization gives a readout discipline in the weak sense of event-to-outcome assignment, but not a branch-usable nontrivial distinguisher/signature layer.

#### Realization D-separating: nontrivial readout discipline

Let
$$
\mathfrak{Sig}_{\mathrm{sep}} = \{\mathtt{stay}, \mathtt{swap}\}
$$
and let
$$
\mathfrak D_{\mathrm{sep}} = \{\delta_{\mathrm{sep}}\}
$$
with
$$
\delta_{\mathrm{sep}}(X,\mathrm{id}) = \mathtt{stay},
\qquad
\delta_{\mathrm{sep}}(X,\sigma) = \mathtt{swap}
$$
for every admissible $X$.

Then D1 holds because the distinguisher is defined on admissible events. D2 holds because equal events receive equal signatures. D3 holds because the same event always returns the same signature. D4 holds because
$$
(X_a,\mathrm{id})
\quad\text{and}\quad
(X_a,\sigma)
$$
are not identified by solved-layer equality and are assigned distinct signatures.

Thus the same solved layer admits both a trivial and a nontrivial readout regime, and even admits the complete absence of a branch-usable nontrivial readout layer unless additional readout data are stipulated.

These realizations are inequivalent:

- D-void does not determine a branch-usable distinguisher/signature layer at all;
- D-trivial determines only a constant outcome assignment;
- D-separating determines a nontrivial event-separating readout.

Yet all three are compatible with the same solved $R+S+C+T$ layer. Therefore the solved layer does not force a unique or canonical distinguisher/signature discipline. More strongly, it does not force existence of a branch-usable nontrivial distinguisher/signature layer. Distinguishers/signatures must therefore be added explicitly if the branch is to proceed upward. $\square$

### 3.19 Explicit introduction of distinguishers/signatures as the next added branch structure

Since distinguishers/signatures are not forced from the solved layer, the branch now introduces them explicitly.

**Added Branch Structure $D$.**  
A continuation of the branch beyond realized-carrier existence, explicit locality, and explicit lawful transformation must specify a distinguisher/signature discipline $(\mathfrak D, \mathfrak{Sig})$ on the event domain $\mathcal E_T$ satisfying D1--D4 together with any extra outcome-identity, readout-repeatability, or branch-adequacy principles required for the intended continuation.

$D$ is not forced from the prior layer. It is the next **minimal added branch structure** required if the branch wishes to continue toward stable comparison, valuation, parameterization, or differentiability.

### 3.20 What Theorem 3.18.1 does and does not prove

**What it proves.**

- The solved $R+S+C+T$ layer does not force a unique or canonical distinguisher/signature discipline.
- The branch cannot treat readout or signature identity as theorem-grade from realized-carrier existence, locality, and lawful transformation alone.
- Any continuation toward stable comparison, valuation, parameterization, or differentiability must add distinguishers/signatures explicitly.

**What it does not prove.**

- It does not show that distinguishers/signatures are impossible.
- It does not show that every readout discipline is equally good.
- It does not show that D1--D4 are uniquely minimal in all imaginable branches.
- It does not derive stable comparison, valuation, parameterization, or differentiability.

So the correct status is:

- distinguishers/signatures are **not forced from $R+S+C+T$**,
- distinguishers/signatures are the next **minimal added branch structure** $D$,
- no upward climb beyond readout is licensed until later passes settle the comparison-algebra question.


### 3.21 No-go theorem for forcing stable comparison algebra from $R+S+C+T+D$

**Theorem 3.21.1 (No-go theorem for forcing stable comparison algebra from $R+S+C+T+D$).**  
The solved layer consisting of primitive distinguishability, the added refinement/compatibility structure $R$, the added realization/decisiveness layer $S$, the explicitly added locality/cover structure $C$, the explicitly added lawful-transformation structure $T$, and the explicitly added distinguisher/signature structure $D$ is **not** sufficient to force a unique or canonical branch-usable stable comparison algebra. More strongly:

1. there exist $R+S+C+T+D$-models with the same realized-carrier regime, the same cover discipline, the same lawful-transformation discipline, and the same distinguisher/signature discipline that admit inequivalent stable comparison algebras satisfying A1--A5;
2. there exist $R+S+C+T+D$-models in which no branch-usable nontrivial comparison algebra is determined unless further comparison data are stipulated;
3. therefore stable comparison algebra is not theorem-grade from the solved $R+S+C+T+D$ layer and must be introduced explicitly as the next minimal added branch structure if the branch is to proceed toward valuation, parameterization, and differentiability.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\#)$ satisfies Section 2.2.
2. The added branch structures $R$, $S$, $C$, $T$, and $D$ satisfy Sections 2.5, 2.7, 2.9, 2.11, and 2.13.
3. The conditional existence and non-canonicity results of Theorems 3.9.1 and 3.10.1 hold.
4. The no-go results for forced locality, forced lawful transformation, and forced distinguishers/signatures, together with the explicit additions of $C$, $T$, and $D$, hold as in Theorems 3.12.1, 3.15.1, and 3.18.1 and Sections 3.13, 3.16, and 3.19.
5. No additional order axioms, signature-comparison axioms, class-composition axioms, or context-invariant comparison-selection principles are assumed beyond $R+S+C+T+D$.

**Conclusion.**

Under these hypotheses alone, no unique or canonical branch-usable stable comparison algebra is forced on the solved pre-comparison layer. If the branch wishes to continue toward valuation, parameterization, or differentiability, it must add stable comparison algebra explicitly.

**Proof.**

Fix any $R+S+C+T+D$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\},
$$
a fixed cover discipline $\triangleleft$, a fixed lawful-transformation discipline
$$
\mathfrak T = \{\mathrm{id}, \sigma\},
$$
with
$$
\sigma(X_a)=X_b,
\qquad
\sigma(X_b)=X_a,
$$
and a fixed nontrivial distinguisher/signature discipline
$$
\mathfrak{Sig} = \{\mathtt{stay}, \mathtt{swap}\},
\qquad
\mathfrak D = \{\delta_{\mathrm{sep}}\},
$$
where
$$
\delta_{\mathrm{sep}}(X,\mathrm{id}) = \mathtt{stay},
\qquad
\delta_{\mathrm{sep}}(X,\sigma) = \mathtt{swap}
$$
for each admissible $X$.

The solved pre-comparison layer is therefore fixed: same carrier, same cover, same transformations, same readout, same signatures.

We now define three inequivalent comparison realizations on that same solved layer.

#### Realization A-void: no branch-usable comparison algebra determined

Take no comparison-class quotient beyond raw signature identity, no comparison preorder, and no class-level composition law. The solved $R+S+C+T+D$ layer by itself does not specify:

- whether signatures are comparable,
- whether any one signature is greater, smaller, or equivalent in comparison strength to another,
- whether signatures should be grouped into coarser comparison classes,
- or whether there is any meaningful class-level composition of comparisons.

Therefore nothing in the solved layer alone forces a nonempty branch-usable stable comparison algebra.

This already proves that existence of a nontrivial comparison algebra is not forced.

#### Realization A-discrete: equality-only comparison

Let
$$
\mathfrak C_{\mathrm{disc}} = \{[\mathtt{stay}], [\mathtt{swap}]\},
$$
where each signature forms its own comparison class. Define
$$
c \sqsubseteq_{\mathrm{disc}} d
\quad\text{iff}\quad
c=d.
$$
Define partial composition only on identical pairs by
$$
[\mathtt{stay}] \odot_{\mathrm{disc}} [\mathtt{stay}] = [\mathtt{stay}],
\qquad
[\mathtt{swap}] \odot_{\mathrm{disc}} [\mathtt{swap}] = [\mathtt{swap}],
$$
and leave mixed pairs undefined.

Then A1--A5 hold:

- A1 holds because the quotient is by signature identity.
- A2 holds because equality is a reflexive and transitive preorder.
- A3 holds because the two classes are not mutually collapsed.
- A4 holds because repeated readout returns the same signature and hence the same comparison class.
- A5 holds because the declared partial composition depends only on comparison classes.

So $\mathfrak C_{\mathrm{disc}}$ is a branch-usable stable comparison algebra.

#### Realization A-flat: total comparison collapse without class collapse

Keep the same two classes
$$
\mathfrak C_{\mathrm{flat}} = \{[\mathtt{stay}], [\mathtt{swap}]\},
$$
but now define a total preorder
$$
c \sqsubseteq_{\mathrm{flat}} d
\quad\text{for all } c,d \in \mathfrak C_{\mathrm{flat}}.
$$
Define a total class composition by choosing
$$
c \odot_{\mathrm{flat}} d = [\mathtt{swap}]
\quad\text{for all } c,d \in \mathfrak C_{\mathrm{flat}}.
$$
Then A1, A2, A4, and A5 hold immediately. A3 still holds because the classes remain distinct as comparison classes even though the preorder collapses them comparison-wise.

This is a stable comparison algebra inequivalent to $\mathfrak C_{\mathrm{disc}}$.

#### Realization A-ordered: noncollapsed directional comparison

Keep the same comparison classes but define
$$
[\mathtt{stay}] \sqsubseteq_{\mathrm{ord}} [\mathtt{swap}],
$$
with reflexive closure and no converse strict relation except reflexivity. Define a partial composition by
$$
[\mathtt{stay}] \odot_{\mathrm{ord}} [\mathtt{stay}] = [\mathtt{stay}],
$$
$$
[\mathtt{stay}] \odot_{\mathrm{ord}} [\mathtt{swap}] = [\mathtt{swap}],
$$
$$
[\mathtt{swap}] \odot_{\mathrm{ord}} [\mathtt{stay}] = [\mathtt{swap}],
$$
and leave $[\mathtt{swap}] \odot_{\mathrm{ord}} [\mathtt{swap}]$ defined as either $[\mathtt{swap}]$ or undefined; either option satisfies A5 if chosen consistently.

Again A1--A5 hold, and this realization is inequivalent to both the discrete and flat comparison realizations.

These three realizations all live on the same solved $R+S+C+T+D$ layer. They share:

- the same realized contents,
- the same locality/cover,
- the same lawful transformations,
- the same event domain,
- the same signatures,
- and the same readout discipline.

Yet they yield inequivalent comparison algebras. Moreover, the A-void realization shows that no branch-usable nontrivial comparison algebra is forced unless additional comparison data are stipulated.

Therefore the solved $R+S+C+T+D$ layer does not force a unique or canonical stable comparison algebra. More strongly, it does not force existence of a branch-usable nontrivial comparison algebra. Stable comparison must therefore be added explicitly if the branch is to proceed upward. $\square$

### 3.22 Explicit introduction of stable comparison algebra as the next added branch structure

Since stable comparison algebra is not forced from the solved layer, the branch now introduces it explicitly.

**Added Branch Structure $A$.**  
A continuation of the branch beyond realized-carrier existence, explicit locality, explicit lawful transformation, and explicit distinguisher/signature discipline must specify a stable comparison algebra $(\mathfrak C, \sqsubseteq, \odot)$ satisfying A1--A5 together with any extra order, composition, or comparison-adequacy principles required for the intended continuation.

$A$ is not forced from the prior layer. It is the next **minimal added branch structure** required if the branch wishes to continue toward valuation, parameterization, or differentiability.

### 3.23 What Theorem 3.21.1 does and does not prove

**What it proves.**

- The solved $R+S+C+T+D$ layer does not force a unique or canonical stable comparison algebra.
- The branch cannot treat comparison as theorem-grade from realized-carrier existence, locality, lawful transformation, and readout alone.
- Any continuation toward valuation, parameterization, or differentiability must add stable comparison algebra explicitly.

**What it does not prove.**

- It does not show that stable comparison algebra is impossible.
- It does not show that every comparison algebra is equally good.
- It does not show that A1--A5 are uniquely minimal in all imaginable branches.
- It does not derive valuation, parameterization, or differentiability.

So the correct status is:

- stable comparison algebra is **not forced from $R+S+C+T+D$**,
- stable comparison algebra is the next **minimal added branch structure** $A$,
- no upward climb beyond comparison is licensed until later passes settle the valuation question.


### 3.24 No-go theorem for forcing valuation representation from $R+S+C+T+D+A$

**Theorem 3.24.1 (No-go theorem for forcing valuation representation from $R+S+C+T+D+A$).**  
The solved layer consisting of primitive distinguishability, the added refinement/compatibility structure $R$, the added realization/decisiveness layer $S$, the explicitly added locality/cover structure $C$, the explicitly added lawful-transformation structure $T$, the explicitly added distinguisher/signature structure $D$, and the explicitly added stable-comparison algebra structure $A$ is **not** sufficient to force a unique or canonical branch-usable valuation representation. More strongly:

1. there exist solved $R+S+C+T+D+A$ layers with the same comparison algebra that admit inequivalent valuation representations satisfying V1--V5;
2. there exist solved $R+S+C+T+D+A$ layers whose comparison algebra admits no branch-usable valuation representation satisfying V1--V5;
3. therefore valuation representation is not theorem-grade from the solved $R+S+C+T+D+A$ layer and must be introduced explicitly as the next minimal added branch structure if the branch is to proceed toward parameterization and differentiability.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\#)$ satisfies Section 2.2.
2. The added branch structures $R$, $S$, $C$, $T$, $D$, and $A$ satisfy Sections 2.5, 2.7, 2.9, 2.11, 2.13, and 2.15.
3. The conditional existence and non-canonicity results of Theorems 3.9.1 and 3.10.1 hold.
4. The no-go results for forced locality, forced lawful transformation, forced distinguishers/signatures, and forced stable comparison, together with the explicit additions of $C$, $T$, $D$, and $A$, hold as in Theorems 3.12.1, 3.15.1, 3.18.1, and 3.21.1 and Sections 3.13, 3.16, 3.19, and 3.22.
5. No additional valuation axioms, normalization axioms, representation-selection principles, or codomain-selection principles are assumed beyond $R+S+C+T+D+A$.

**Conclusion.**

Under these hypotheses alone, no unique or canonical branch-usable valuation representation is forced on the solved pre-valuation layer. More strongly, branch-usable valuation need not exist for every admissible stable-comparison algebra. If the branch wishes to continue toward parameterization or differentiability, it must add valuation explicitly.

**Proof.**

We prove non-uniqueness and non-forcing separately.

#### Part I: same comparison algebra, inequivalent valuation representations

Fix a solved $R+S+C+T+D+A$ layer whose stable comparison algebra is the sparse ordered comparison algebra
$$
\mathfrak C_{\mathrm{sp}} = \{c_0,c_1\},
$$
with preorder
$$
c_0 \sqsubseteq c_0,\qquad c_1 \sqsubseteq c_1,\qquad c_0 \sqsubseteq c_1,
$$
and no converse relation $c_1 \sqsubseteq c_0$. Let the only defined comparison compositions be
$$
c_0 \odot c_0 = c_0,\qquad
c_0 \odot c_1 = c_1,\qquad
c_1 \odot c_0 = c_1,
$$
with $c_1 \odot c_1$ left undefined.

This satisfies A1--A5.

Now define two valuation realizations on the same comparison algebra.

**Valuation realization $V_{\max}$.**  
Let
$$
\mathbb V_{\max} = \{0,1\}
$$
with the usual order $0 \leq 1$, operation
$$
x \oplus_{\max} y := \max\{x,y\},
$$
and neutral element $0$. Define
$$

u_{\max}(c_0)=0,\qquad 
u_{\max}(c_1)=1.
$$
Then:

- V1 holds by definition.
- V2 holds because $c_0 \sqsubseteq c_1$ and $0 \leq 1$.
- V3 holds because $c_0 \sqsubseteq c_1$ and not conversely, while $0<1$.
- V4 holds on every defined comparison composition:
  $$
  
u_{\max}(c_0 \odot c_0)=
u_{\max}(c_0)=0=0\oplus_{\max}0,
  $$
  $$
  
u_{\max}(c_0 \odot c_1)=
u_{\max}(c_1)=1=0\oplus_{\max}1,
  $$
  $$
  
u_{\max}(c_1 \odot c_0)=
u_{\max}(c_1)=1=1\oplus_{\max}0.
  $$
- V5 holds with $c_0$ as neutral class.

So $(\mathbb V_{\max},
u_{\max})$ is a branch-usable valuation representation.

**Valuation realization $V_{+}$.**  
Let
$$
\mathbb V_{+} = \mathbb N
$$
with the usual order, usual addition, and neutral element $0$. Define
$$

u_{+}(c_0)=0,\qquad 
u_{+}(c_1)=1.
$$
Then:

- V1 holds by definition.
- V2 holds because $0 \leq 1$.
- V3 holds because $0<1$.
- V4 holds on every defined comparison composition:
  $$
  
u_{+}(c_0 \odot c_0)=0=0+0,
  $$
  $$
  
u_{+}(c_0 \odot c_1)=1=0+1,
  $$
  $$
  
u_{+}(c_1 \odot c_0)=1=1+0.
  $$
- V5 holds with $c_0$ as neutral class.

So $(\mathbb V_{+},
u_{+})$ is also a branch-usable valuation representation.

The two valuation realizations are inequivalent as valuation regimes. One has an idempotent bounded target with operation $\max$; the other has an unbounded additive target with non-idempotent operation $+$. The solved layer and the comparison algebra are the same, yet the valuation codomain and valuation composition law are not uniquely determined. Therefore valuation representation is not uniquely or canonically forced even when existence is available.

#### Part II: some stable comparison algebras admit no branch-usable valuation representation

Now fix a solved $R+S+C+T+D+A$ layer whose stable comparison algebra is
$$
\mathfrak C_{\mathrm{bad}} = \{x,y,z\},
$$
with preorder generated by
$$
x \sqsubseteq y,
$$
and no converse relation $y \sqsubseteq x$. Let comparison composition be defined by
$$
x \odot z = y,\qquad
y \odot z = x,
$$
with all other compositions either undefined or chosen so as not to affect the argument.

This still satisfies A1--A5:

- A1 is irrelevant to the present abstract comparison layer once the classes are fixed.
- A2 holds because the preorder generated by $x \sqsubseteq y$ is reflexive and transitive.
- A3 holds because $x$ and $y$ are not mutually collapsed by the preorder.
- A4 and A5 hold because the class-level composition is well defined on the declared domain.

Assume, for contradiction, that there exists a branch-usable valuation representation
$$

u : \mathfrak C_{\mathrm{bad}} 	o \mathbb V
$$
satisfying V1--V5 into some ordered composition regime $(\mathbb V,\leq_{\mathbb V},\oplus,0_{\mathbb V})$.

From $x \sqsubseteq y$ and V2,
$$

u(x) \leq_{\mathbb V} 
u(y).
$$
Because $\oplus$ is monotone in each argument,
$$

u(x)\oplus 
u(z) \leq_{\mathbb V} 
u(y)\oplus 
u(z).
$$
By V4 and the declared comparison compositions,
$$

u(x\odot z) \leq_{\mathbb V} 
u(y\odot z),
$$
hence
$$

u(y) \leq_{\mathbb V} 
u(x).
$$
So $
u(x)$ and $
u(y)$ are mutually comparable both ways. But V3 requires strict noncollapse whenever
$$
x \sqsubseteq y
\qquad	ext{and}\qquad

eg(y \sqsubseteq x),
$$
which is exactly the present case. Therefore V3 requires
$$

u(x) <_{\mathbb V} 
u(y),
$$
contradicting $
u(y) \leq_{\mathbb V} 
u(x)$.

Hence no branch-usable valuation representation satisfying V1--V5 exists for this stable comparison algebra.

So valuation is not merely non-canonical; existence itself is not forced for all admissible solved layers. Therefore valuation representation is not theorem-grade from $R+S+C+T+D+A$ and must be added explicitly if the branch is to proceed upward. $\square$

### 3.25 Explicit introduction of valuation representation as the next added branch structure

Since valuation representation is not forced from the solved layer, the branch now introduces it explicitly.

**Added Branch Structure $V$.**  
A continuation of the branch beyond realized-carrier existence, explicit locality, explicit lawful transformation, explicit distinguisher/signature discipline, and explicit stable-comparison algebra must specify a valuation representation
$$
(\mathbb V,\leq_{\mathbb V},\oplus,0_{\mathbb V},
u)
$$
satisfying V1--V5 together with any extra completeness, normalization, comparability, or representation-adequacy principles required for the intended continuation.

$V$ is not forced from the prior layer. It is the next **minimal added branch structure** required if the branch wishes to continue toward parameterization or differentiability.

### 3.26 What Theorem 3.24.1 does and does not prove

**What it proves.**

- The solved $R+S+C+T+D+A$ layer does not force a unique or canonical valuation representation.
- The branch cannot treat valuation as theorem-grade from realized-carrier existence, locality, transformation, readout, and stable comparison alone.
- Some stable comparison algebras admit no branch-usable valuation representation satisfying V1--V5.
- Any continuation toward parameterization or differentiability must add valuation explicitly.

**What it does not prove.**

- It does not show that valuation is impossible.
- It does not show that every valuation regime is equally good.
- It does not show that V1--V5 are uniquely minimal in all imaginable branches.
- It does not derive parameterization or differentiability.

So the correct status is:

- valuation representation is **not forced from $R+S+C+T+D+A$**,
- valuation representation is the next **minimal added branch structure** $V$,
- no upward climb beyond valuation is licensed until later passes settle the parameterization question.


## 4. Main Theorems and Proofs

The main theorems of this pass are Theorems 3.1.1, 3.2.1, 3.3.1, 3.5.1, 3.7.1, 3.9.1, 3.10.1, 3.12.1, 3.15.1, 3.18.1, 3.21.1, and 3.24.1.

### 4.1 Theorem status map for this pass

- **Forced from prior layer:**
  - nullity exclusion,
  - undifferentiated sameness exclusion,
  - weakest surviving primitive.

- **Minimal added branch structure:**
  - sharpenability discipline $L1$,
  - refinement/compatibility structure $R$,
  - realization/decisiveness layer $S$,
  - locality/cover structure $C$,
  - lawful-transformation structure $T$,
  - distinguisher/signature structure $D$,
  - stable comparison algebra structure $A$,
  - valuation-representation structure $V$.

- **Conditional theorem under explicit assumptions in this pass:**
  - existence of realized contents under $R+S$,
  - existence of a realized carrier regime under $R+S$,
  - non-canonicity of that regime under $R+S$.

### 4.2 Claims deferred until later passes

The following are not yet theorem-grade and are not used in this pass:

- parameterization,
- differentiability emergence.

## 5. Validation Logic and Evidentiary Support

This section states what would count as support or falsification for the present pass.

### 5.1 What would falsify the nullity and sameness exclusions

The root exclusions would fail if one could exhibit a branch-level formalism in which:

1. absolute nullity supports distinction, law, and falsifiability, or
2. absolute undifferentiated sameness supports nontrivial distinction, law, and falsifiability.

No such construction is supplied here.

### 5.2 What would falsify Theorem 3.5.1

The no-go theorem for forced refinement would fail if one could prove either of the following from the prior layer alone:

1. primitive distinction plus sharpenability uniquely determines a stable global refinement/compatibility regime; or
2. every two sharpenability realizations over the same primitive substrate are canonically isomorphic as refinement/compatibility structures.

Either result would refute Theorem 3.5.1.

### 5.3 What would falsify Theorem 3.7.1

The no-go theorem for realized-carrier forcing from $R$ would fail if one could prove either of the following from $R$ alone:

1. every $R$-model necessarily admits at least one $R$-candidate realized content; or
2. every $R$-model with realized contents admits a canonical realized carrier independent of any further realization principle.

Either result would refute Theorem 3.7.1.

### 5.4 What would falsify Theorem 3.9.1

The conditional realization theorem under $R+S$ would fail if one could exhibit an $R+S$-model in which at least one admissible bearer lies on no realized distinction content, or equivalently if $\mathcal M_0^{(R+S)}$ were empty in some model satisfying all clauses of $S$.

### 5.5 What would falsify Theorem 3.10.1

The non-canonicity theorem under $R+S$ would fail if one could prove from $R+S$ alone that every realized-content extension is unique up to canonical isomorphism. Absent such a proof, the explicit countermodel in Theorem 3.10.1 stands.

### 5.6 What would show the added structure $R$ is too strong

The added branch structure $R$ would be too strong if one could exhibit a weaker added structure than $R$ that still suffices to support all later branch requirements:

- stable realization,
- lawful local organization,
- stable comparison,
- and the later route toward differentiability.

If such a weaker structure is found, $R$ must be weakened in a later pass.

### 5.7 What would show the candidate structure $S$ is too strong

The candidate realization layer $S$ would be too strong if one could exhibit a weaker added principle than $S$ that still guarantees:

- existence of realized contents,
- decisiveness/sharpness of those contents,
- and a realized carrier regime sufficient for later branch continuation.

If such a weaker structure is found, $S$ must be weakened before canonization.

### 5.8 What would show a weaker primitive package is sufficient

If one could derive realized contents or a realized carrier directly from primitive distinction plus sharpenability, without explicit introduction of $R$ or $S$, then both Theorems 3.5.1 and 3.7.1 would have to be revised downward and the current branch staircase would be too heavy.

### 5.9 What would show the current derivation still smuggles later structure

This pass would be defective if any proof above implicitly relied on:

- metric notions,
- topology stronger than what is stated,
- numeric valuation,
- parameterized process,
- comparison algebraic laws not explicitly introduced,
- locality stronger than the refinement/compatibility/realization/cover layer,
- or differentiated structure.

The present pass is designed to stop before those imports occur.

### 5.10 What would show that $S$ does not actually improve on $R$

If every theorem obtained under $R+S$ could already be obtained under $R$ alone, then $S$ would be redundant and its introduction would be illegitimate. The existence theorem 3.9.1 is exactly what prevents that: it gives a result not obtainable from $R$ alone.

### 5.11 What would falsify Theorem 3.12.1

The no-go theorem for forcing locality/cover from $R+S$ would fail if one could prove either of the following from the solved layer alone:

1. every $R+S$-model admits a unique canonical cover/locality discipline satisfying C1--C4; or
2. any two cover disciplines on the same realized-carrier regime that satisfy C1--C4 are canonically isomorphic and physically equivalent for branch continuation.

Either result would refute Theorem 3.12.1.

### 5.12 What would show the added structure $C$ is too strong

The locality/cover layer $C$ would be too strong if one could exhibit a weaker added structure than C1--C4 that still suffices for every later branch requirement that genuinely depends on pre-metric locality. If such a weaker layer is found, $C$ must be weakened in a later pass.

### 5.13 What would show a weaker solved package is sufficient for locality

If one could derive a branch-usable locality/cover discipline directly from the solved $R+S$ layer, without explicit addition of $C$, then Theorem 3.12.1 would fail and the current staircase would be one layer too heavy.

### 5.14 What would show that locality/cover does not improve on the solved layer

If every later theorem that appears to depend on $C$ could in fact already be proved from $R+S$ alone, then $C$ would be redundant and its introduction would be illegitimate. The role of later passes is to test that explicitly.

### 5.15 What would falsify Theorem 3.15.1

The no-go theorem for forcing lawful transformation from $R+S+C$ would fail if one could prove either of the following from the solved layer alone:

1. every $R+S+C$-model admits a unique canonical branch-usable lawful-transformation discipline satisfying T1--T5; or
2. any two lawful-transformation disciplines on the same realized-carrier regime and the same cover discipline that satisfy T1--T5 are canonically isomorphic and physically equivalent for branch continuation.

Either result would refute Theorem 3.15.1.

### 5.16 What would show the added structure $T$ is too strong

The lawful-transformation layer $T$ would be too strong if one could exhibit a weaker added structure than T1--T5 that still suffices for every later branch requirement that genuinely depends on process-like admissible action on realized contents. If such a weaker layer is found, $T$ must be weakened in a later pass.

### 5.17 What would show a weaker solved package is sufficient for transformation

If one could derive a branch-usable lawful-transformation discipline directly from the solved $R+S+C$ layer, without explicit addition of $T$, then Theorem 3.15.1 would fail and the current staircase would be one layer too heavy.

### 5.18 What would show that lawful transformation does not improve on the solved layer

If every later theorem that appears to depend on $T$ could already be proved from $R+S+C$ alone, then $T$ would be redundant and its introduction would be illegitimate. The role of later passes is to test that explicitly.

### 5.19 What would show the derivation still smuggles later structure through transformation

This pass would be defective if the proof of Theorem 3.15.1 or the definition of $T$ implicitly relied on:

- numeric parameters,
- valuation,
- scalar signatures,
- comparison algebra,
- metric continuity,
- or any differentiated notion of motion.

The present pass avoids those imports by treating transformation only as admissible composition on realized contents with cover respect.

### 5.20 What would falsify Theorem 3.18.1

The no-go theorem for forcing distinguishers/signatures from $R+S+C+T$ would fail if one could prove either of the following from the solved layer alone:

1. every $R+S+C+T$-model admits a unique canonical branch-usable distinguisher/signature discipline satisfying D1--D4; or
2. any two distinguisher/signature disciplines on the same realized-carrier regime, the same cover discipline, and the same lawful-transformation discipline that satisfy D1--D4 are canonically isomorphic and physically equivalent for branch continuation.

Either result would refute Theorem 3.18.1.

### 5.21 What would show the added structure $D$ is too strong

The distinguisher/signature layer $D$ would be too strong if one could exhibit a weaker added structure than D1--D4 that still suffices for every later branch requirement that genuinely depends on readout, event discrimination, or outcome identity. If such a weaker layer is found, $D$ must be weakened in a later pass.

### 5.22 What would show a weaker solved package is sufficient for distinguishers/signatures

If one could derive a branch-usable distinguisher/signature discipline directly from the solved $R+S+C+T$ layer, without explicit addition of $D$, then Theorem 3.18.1 would fail and the current staircase would be one layer too heavy.

### 5.23 What would show that distinguishers/signatures do not improve on the solved layer

If every later theorem that appears to depend on $D$ could already be proved from $R+S+C+T$ alone, then $D$ would be redundant and its introduction would be illegitimate. The role of later passes is to test that explicitly.

### 5.24 What would show the derivation still smuggles later structure through readout

This pass would be defective if the proof of Theorem 3.18.1 or the definition of $D$ implicitly relied on:

- ordered comparison of outcomes,
- algebra on signatures,
- valuation or scalar codomains,
- parameterized readout families,
- metric or differentiable structure,
- or any downstream comparison law not explicitly introduced.

The present pass avoids those imports by treating readout only as event-to-signature assignment with extensional identity, repeatability, and minimal nontriviality.

---


### 5.25 What would falsify Theorem 3.21.1

The no-go theorem for forcing stable comparison algebra from $R+S+C+T+D$ would fail if one could prove either of the following from the solved layer alone:

1. every $R+S+C+T+D$-model admits a unique canonical stable comparison algebra satisfying A1--A5; or
2. any two stable comparison algebras on the same realized-carrier regime, the same cover discipline, the same lawful-transformation discipline, and the same distinguisher/signature discipline that satisfy A1--A5 are canonically isomorphic and physically equivalent for branch continuation.

Either result would refute Theorem 3.21.1.

### 5.26 What would show the added structure $A$ is too strong

The stable-comparison layer $A$ would be too strong if one could exhibit a weaker added structure than A1--A5 that still suffices for every later branch requirement that genuinely depends on stable comparison. If such a weaker layer is found, $A$ must be weakened in a later pass.

### 5.27 What would show a weaker solved package is sufficient for comparison

If one could derive a branch-usable stable comparison algebra directly from the solved $R+S+C+T+D$ layer, without explicit addition of $A$, then Theorem 3.21.1 would fail and the current staircase would be one layer too heavy.

### 5.28 What would show that stable comparison algebra does not improve on the solved layer

If every later theorem that appears to depend on $A$ could already be proved from $R+S+C+T+D$ alone, then $A$ would be redundant and its introduction would be illegitimate. The role of later passes is to test that explicitly.

### 5.29 What would show the derivation still smuggles later structure through comparison

This pass would be defective if the proof of Theorem 3.21.1 or the definition of $A$ implicitly relied on:

- numeric valuation,
- parameterized process,
- metric or differentiable structure,
- order or algebraic laws stronger than A1--A5 without stating them,
- or any downstream valuation law not explicitly introduced.

The present pass avoids those imports by treating stable comparison only as class identity, preorder, and optional class-level composition on the solved pre-valuation layer.



### 5.30 What would falsify Theorem 3.24.1

The no-go theorem for forcing valuation representation from $R+S+C+T+D+A$ would fail if one could prove either of the following from the solved layer alone:

1. every $R+S+C+T+D+A$-model admits a unique canonical branch-usable valuation representation satisfying V1--V5; or
2. every stable comparison algebra allowed by the solved layer necessarily admits at least one branch-usable valuation representation satisfying V1--V5.

Either result would refute Theorem 3.24.1.

### 5.31 What would show the added structure $V$ is too strong

The valuation layer $V$ would be too strong if one could exhibit a weaker added structure than V1--V5 that still suffices for every later branch requirement that genuinely depends on value-bearing representation. If such a weaker layer is found, $V$ must be weakened in a later pass.

### 5.32 What would show a weaker solved package is sufficient for valuation

If one could derive a branch-usable valuation representation directly from the solved $R+S+C+T+D+A$ layer, without explicit addition of $V$, then Theorem 3.24.1 would fail and the current staircase would be one layer too heavy.

### 5.33 What would show that valuation does not improve on the solved layer

If every later theorem that appears to depend on $V$ could already be proved from $R+S+C+T+D+A$ alone, then $V$ would be redundant and its introduction would be illegitimate. The role of later passes is to test that explicitly.

### 5.34 What would show the derivation still smuggles later structure through valuation

This pass would be defective if the proof of Theorem 3.24.1 or the definition of $V$ implicitly relied on:

- parameterized processes,
- coordinate charts,
- metric distance,
- local derivatives,
- or differentiable structure.

The present pass avoids those imports by treating valuation only as order-compatible representation of stable comparison classes into an ordered composition regime.


## 6. Worked Example or Minimal Witnesses

Minimal witnesses suffice for the present pass.

### 6.1 Witness for Theorem 3.5.1

The proof of Theorem 3.5.1 already provides two sharpenability realizations over the same primitive substrate that are not isomorphic as refinement/compatibility structures.

### 6.2 Witnesses for Theorem 3.7.1

#### Witness A: $R$ without realized contents

Take
$$
\widehat{\mathcal B}_A = \{a,b,c\},
$$
with
$$
a\# b,
$$
refinement reflexive only, compatibility identity only, and no other apartness relations. Then $R$ holds, but no $R$-candidate realized content exists.

#### Witness B: $R$ with multiple realized contents

Take
$$
\widehat{\mathcal B}_B = \{a,b\},
$$
with
$$
a\# b,
$$
refinement reflexive only, and compatibility identity only. Then $R$ holds, and both $\{a\}$ and $\{b\}$ are $R$-candidate realized contents.

These two witnesses jointly establish that $R$ alone forces neither existence nor canonicity of a realized carrier.

### 6.3 Witness for Theorem 3.9.1

Take any $R$-model for which a refinement thread exists through each admissible bearer and augment it with $S1$ through $S4$. Then each such thread extends to a decisive coherent content. This witnesses existence of at least one realized content.

### 6.4 Witness for Theorem 3.10.1

Take the model used in the proof of Theorem 3.10.1 with two disjoint refinement branches. By S4, each branch extends to a decisive coherent content. The resulting realized carrier regime has at least two inequivalent members and is therefore non-canonical.

### 6.5 Witness for Theorem 3.12.1

Take any $R+S$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\}.
$$
Equip it once with the discrete cover discipline $\triangleleft_d$ and once with the indiscrete cover discipline $\triangleleft_i$ from the proof of Theorem 3.12.1. Both satisfy C1--C4, but they are inequivalent. This witnesses that locality/cover is not forced from $R+S$.

### 6.6 Witness for Theorem 3.15.1

Take any $R+S+C$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\}
$$
and a fixed cover discipline $\triangleleft$.

- Equip it once with the identity-only transformation family $\mathfrak T_{\mathrm{id}}$.
- Equip it again with the nontrivial involutive family $\mathfrak T_{\mathrm{swap}} = \{\mathrm{id},\sigma\}$.

These two transformation disciplines live on the same solved pre-transformation layer but are inequivalent. This witnesses that lawful transformation is not forced from $R+S+C$.

---


### 6.7 Witness for Theorem 3.18.1

Take any $R+S+C+T$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\},
$$
a fixed cover discipline $\triangleleft$, and a fixed lawful-transformation discipline
$$
\mathfrak T = \{\mathrm{id}, \sigma\}
$$
with
$$
\sigma(X_a)=X_b,
\qquad
\sigma(X_b)=X_a.
$$
On the same event domain $\mathcal E_T$, equip the solved layer in three different ways:

- with no branch-usable readout layer at all;
- with the constant readout discipline $(\mathfrak D_{\mathrm{triv}}, \mathfrak{Sig}_{\mathrm{triv}})$;
- with the separating readout discipline $(\mathfrak D_{\mathrm{sep}}, \mathfrak{Sig}_{\mathrm{sep}})$.

These three readout realizations live on the same solved pre-distinguisher layer but are inequivalent. This witnesses that distinguishers/signatures are not forced from $R+S+C+T$.


### 6.8 Witness for Theorem 3.21.1

Take any $R+S+C+T+D$-model with realized-carrier regime
$$
\mathcal M_0^{(R+S)} = \{X_a, X_b\},
$$
a fixed cover discipline $\triangleleft$, a fixed lawful-transformation discipline
$$
\mathfrak T = \{\mathrm{id}, \sigma\},
$$
and a fixed nontrivial readout discipline
$$
\mathfrak D = \{\delta_{\mathrm{sep}}\},
\qquad
\mathfrak{Sig} = \{\mathtt{stay}, \mathtt{swap}\}.
$$
On this same solved layer, equip the branch in three different ways:

- with no branch-usable comparison layer at all;
- with the equality-only comparison algebra $\mathfrak C_{\mathrm{disc}}$;
- with the flat comparison algebra $\mathfrak C_{\mathrm{flat}}$;
- with the ordered comparison algebra $\mathfrak C_{\mathrm{ord}}$.

These realizations share the same realized contents, locality, transformations, signatures, and readout acts, yet yield inequivalent comparison regimes. This witnesses that stable comparison algebra is not forced from $R+S+C+T+D$.



### 6.9 Witness for Theorem 3.24.1

Take any $R+S+C+T+D+A$-model with a solved pre-valuation layer whose stable comparison algebra is either:

1. the sparse ordered algebra
   $$
   \mathfrak C_{\mathrm{sp}} = \{c_0,c_1\}
   $$
   with
   $$
   c_0 \sqsubseteq c_1
   $$
   and defined compositions
   $$
   c_0 \odot c_0 = c_0,\qquad
   c_0 \odot c_1 = c_1,\qquad
   c_1 \odot c_0 = c_1,
   $$
   for which both the max-valued representation $(\mathbb V_{\max},
u_{\max})$ and the additive representation $(\mathbb V_{+},
u_{+})$ are valid; or

2. the bad comparison algebra
   $$
   \mathfrak C_{\mathrm{bad}} = \{x,y,z\}
   $$
   with
   $$
   x \sqsubseteq y,\qquad x\odot z = y,\qquad y\odot z = x,
   $$
   for which no valuation satisfying V1--V5 exists.

These witnesses jointly show that valuation is neither uniquely determined nor guaranteed to exist from the solved pre-valuation layer alone.


## 7. CFN Pairing and Executable Traceability

The paired CFN for the present pass may do the following:

- instantiate finite examples of primitive substrates $({\mathcal B},\#)$,
- instantiate multiple non-isomorphic sharpening realizations over the same primitive substrate,
- instantiate $R$-models with and without $R$-candidate realized contents,
- instantiate $R+S$-models with nonempty realized-carrier regimes,
- instantiate inequivalent cover disciplines on the same realized-carrier regime,
- instantiate inequivalent lawful-transformation disciplines on the same realized-carrier regime and same cover discipline,
- instantiate inequivalent readout disciplines on the same realized-carrier regime, same cover discipline, and same lawful-transformation discipline,
- verify that the witness models satisfy the stated axioms,
- and present the no-go, existence/non-canonicity, locality-underdetermination, transformation-underdetermination, and readout-underdetermination theorems graphically or combinatorially.

The CFN may **not** introduce any proof burden not already carried here.

---

## 8. Assumptions, Limits, and Open Boundaries

### 8.1 Assumptions used in the derivation

This pass uses only:

1. the branch-level exclusion of nullity and undifferentiated sameness,
2. the weakest surviving primitive $({\mathcal B},\#)$,
3. the first added sharpenability discipline $L1$,
4. the explicitly added refinement/compatibility structure $R$,
5. the explicitly added realization/decisiveness structure $S$,
6. the explicitly added locality/cover structure $C$,
7. the explicitly added lawful-transformation structure $T$ in the sense of candidate definition and no-go target,
8. the explicitly added candidate distinguisher/signature structure $D$ in the sense of candidate definition and no-go target,
9. the explicitly added candidate stable-comparison structure $A$ in the sense of candidate definition and no-go target,
10. the explicitly added candidate valuation structure $V$ in the sense of candidate definition and no-go target,
11. elementary logic about non-isomorphic realizations, existence/nonexistence witnesses, non-unique branch extension, inequivalent cover disciplines, inequivalent transformation disciplines, inequivalent readout disciplines, inequivalent comparison algebras, and inequivalent or absent valuation regimes on the same solved layer.

### 8.2 Claims established here

This pass establishes:

- the root exclusions,
- the weakest surviving primitive,
- the no-go theorem for forcing refinement/compatibility from the prior layer,
- the explicit introduction of refinement/compatibility as the first minimal added branch structure,
- the no-go theorem showing that $R$ alone does not force stable realized contents or a canonical realized carrier,
- the conditional theorem that $R+S$ yields realized contents and a realized carrier regime,
- the theorem that the resulting carrier regime is generally non-canonical,
- the no-go theorem showing that locality/cover is not forced from the solved $R+S$ layer,
- the explicit introduction of locality/cover as the next minimal added branch structure $C$,
- the no-go theorem showing that lawful transformation is not forced from the solved $R+S+C$ layer,
- the explicit introduction of lawful transformation as the next minimal added branch structure $T$,
- the no-go theorem showing that distinguishers/signatures are not forced from the solved $R+S+C+T$ layer,
- the explicit introduction of distinguishers/signatures as the next minimal added branch structure $D$,
- the no-go theorem showing that stable comparison algebra is not forced from the solved $R+S+C+T+D$ layer,
- the explicit introduction of stable comparison algebra as the next minimal added branch structure $A$,
- the no-go theorem showing that valuation representation is not forced from the solved $R+S+C+T+D+A$ layer,
- the explicit introduction of valuation representation as the next minimal added branch structure $V$.

### 8.3 Claims not established here

This pass does not establish:

- parameterization,
- differentiability.

### 8.4 Open boundary for the next pass

The next pass must determine whether a parameterization layer is forced from the solved $R+S+C+T+D+A+V$ layer, or whether it must itself be introduced explicitly as the next minimal branch structure.

No upward climb beyond parameterization is allowed before that question is settled.

## 9. Integration with Broader VDM Theory

CF000 remains the root of the branch.

CF00 remains downstream as the first differentiable-layer formalism, but the present pass does not yet reconnect to CF00 in detail. That bridge is intentionally paused until later comparison structure and the differentiability route are settled honestly.

The only downstream statement fixed here is structural and now stronger than in the previous pass:

> CF00 may not be treated as beginning from a layer already forced by primitive distinction, refinement/compatibility, realization/decisiveness, locality/cover, lawful transformation, and readout/comparison alone.

Instead, CF00 sits downstream of a branch that now explicitly contains:

1. a forced primitive distinction layer,
2. a first minimal added refinement/compatibility layer,
3. a second minimal added realization/decisiveness layer,
4. a conditional and non-canonical realized-carrier regime under $R+S$,
5. an explicitly added locality/cover layer $C$ not forced from that solved regime,
6. an explicitly added lawful-transformation layer $T$ not forced from the solved $R+S+C$ layer,
7. an explicitly added distinguisher/signature layer $D$ not forced from the solved $R+S+C+T$ layer,
8. an explicitly added stable-comparison layer $A$ not forced from the solved $R+S+C+T+D$ layer,
9. and an explicitly added valuation layer $V$ not forced from the solved $R+S+C+T+D+A$ layer.

---

## 10. References and Provenance

This pass uses the house CF template as the formal standard for completeness and theorem-bearing structure.

It also uses the current CF000 checklist as the binding solved/open state for this pass. The theorem target addressed here is exactly the live question identified there: whether the solved $R+S+C+T+D+A$ layer is sufficient to force a valuation representation. The answer given here is no. Valuation representation is therefore reclassified as the next minimal added branch structure $V$.

No external source is used here as a substitute for derivation.

---

## Appendix A. Symbol Table

- $\mathcal B$: primitive distinction-bearing bearer class.
- $\#$: primitive apartness relation.
- $L1$: sharpenability discipline.
- $\widehat{\mathcal B}$: admissibly enriched bearer class after added branch structure.
- $\preceq$: refinement preorder.
- $\bowtie$: compatibility relation in the first added branch structure.
- $R$: first minimal added branch structure consisting of refinement/compatibility.
- $\mathcal M_0^{(R)}$: class of $R$-candidate realized distinction contents, not forced to be nonempty.
- $S$: realization/decisiveness layer, introduced as the second minimal added branch structure.
- $\mathcal M_0^{(R+S)}$: realized-carrier regime obtained conditionally under $R+S$.
- $C$: locality/cover layer, introduced as the third minimal added branch structure.
- $\triangleleft$: pre-metric cover/locality relation on the realized-carrier regime.
- $T$: lawful-transformation layer, introduced as the fourth minimal added branch structure.
- $\mathfrak T$: class of lawful transformations on the realized-carrier regime.
- $\mathcal E_T$: event domain of admissible realized-content / transformation pairs.
- $D$: distinguisher/signature layer, introduced as the fifth minimal added branch structure.
- $\mathfrak D$: class of distinguishers on the event domain.
- $\mathfrak{Sig}$: signature class for readout outcomes.
- $A$: stable-comparison layer, introduced as the sixth minimal added branch structure.
- $\mathfrak C$: class of comparison classes.
- $q$: class-forming map from signatures to comparison classes.
- $\sqsubseteq$: comparison preorder on $\mathfrak C$.
- $\odot$: partial comparison composition law on $\mathfrak C$.
- $V$: valuation-representation layer, introduced as the seventh minimal added branch structure.
- $\mathbb V$: valuation carrier.
- $\leq_{\mathbb V}$: preorder on the valuation carrier.
- $\oplus$: valuation-composition law on $\mathbb V$.
- $0_{\mathbb V}$: neutral valuation element.
- $\nu$: valuation map from comparison classes to the valuation carrier.
- $\mathcal M_0$: generic placeholder for a realized pre-differential carrier, not yet canonical.
- $\mathcal M$: downstream differentiable carrier, not yet earned in this pass.

---

## Appendix B. Dependency Audit

### Primitive in this pass

- $({\mathcal B},\#)$

### Forced from prior layer in this pass

- nullity exclusion,
- undifferentiated sameness exclusion,
- weakest surviving primitive.

### Minimal added branch structure in this pass

- sharpenability discipline $L1$,
- refinement/compatibility structure $R$,
- realization/decisiveness layer $S$,
- locality/cover structure $C$,
- lawful-transformation structure $T$,
- distinguisher/signature structure $D$,
- stable comparison algebra structure $A$,
- valuation-representation structure $V$.

### Conditional theorem under explicit assumptions in this pass

- existence of realized contents under $R+S$,
- existence of a realized carrier regime under $R+S$,
- non-canonicity of that regime under $R+S$.

### Conditional or deferred beyond this pass

- parameterization,
- differentiability emergence.

### Main dependency chain of this pass

$$
\text{nullity failure and sameness failure}
\to
({\mathcal B},\#)
\to
L1
\to
\text{no-go theorem for forced refinement}
\to
R
\to
\text{no-go theorem for forced realization from }R
\to
S
\to
\text{conditional existence of non-canonical realized carrier regime}
\to
\text{no-go theorem for forced locality from the solved layer}
\to
C
\to
\text{no-go theorem for forced lawful transformation from the solved layer}
\to
T
\to
\text{no-go theorem for forced distinguishers/signatures}
\to
D
\to
\text{no-go theorem for forced stable comparison}
\to
A
\to
\text{no-go theorem for forced valuation}
\to
V.
$$

No later object is used in the proofs of this pass.

---

## Appendix C. CFN Traceability Table

| CF section | CFN segment | quantities instantiated | diagnostics emitted | claims witnessed |
|---|---|---|---|---|
| §2–§3.3 | `cf000-root-exclusions` | example substrates $({\mathcal B},\#)$ | nullity/sameness exclusion witness cases | Theorems 3.1.1–3.3.1 |
| §3.5 | `cf000-refinement-nogo` | non-isomorphic sharpening realizations | structure-comparison tables | Theorem 3.5.1 |
| §3.7 | `cf000-realization-nogo` | $R$-models with and without realized contents | realization existence/nonexistence witness tables | Theorem 3.7.1 |
| §3.9–§3.10 | `cf000-realization-S` | $R+S$-models with nonempty realized-carrier regimes and multiple branches | existence / non-canonicity witness tables | Theorems 3.9.1–3.10.1 |
| §3.12 | `cf000-locality-nogo` | same realized-carrier regime with inequivalent cover disciplines | locality underdetermination diagnostics | Theorem 3.12.1 |
| §3.15 | `cf000-transformation-nogo` | same realized-carrier regime and same cover discipline with inequivalent transformation families | transformation underdetermination diagnostics | Theorem 3.15.1 |
| §3.18 | `cf000-distinguisher-nogo` | same realized-carrier regime, same cover discipline, same transformation layer, with inequivalent readout disciplines | readout underdetermination diagnostics | Theorem 3.18.1 |
| §3.21 | `cf000-comparison-nogo` | same realized-carrier regime, same cover discipline, same transformation layer, same readout layer, with inequivalent comparison algebras | comparison underdetermination diagnostics | Theorem 3.21.1 |
| §3.24 | `cf000-valuation-nogo` | same solved pre-valuation layer with inequivalent valuation representations and with non-representable comparison algebras | valuation underdetermination diagnostics | Theorem 3.24.1 |
| §6 | `cf000-minimal-witnesses` | sparse witness structures | witness artifact diagrams | worked examples |

The CFN mirrors this pass. It does not repair or extend its theorem burden.

---

## Acceptance Checklist

- [x] The primitive ontology is stated clearly.
- [x] All derived objects used in this pass are earned in logical order.
- [x] All equations needed for understanding this pass are present in the document.
- [x] All theorem-bearing claims in this pass are stated with explicit hypotheses.
- [x] All proof-bearing claims in this pass have actual proofs.
- [x] No essential burden for this pass has been outsourced to canon links or the CFN.
- [x] Validation logic and falsification criteria for this pass are stated in the CF itself.
- [x] Minimal witness examples are specified in the CF itself.
- [x] The role of the CFN is executable realization only.
- [x] Non-theorem-grade claims are explicitly labeled.
- [x] The refinement/compatibility question is settled.
- [x] The realized-content / realized-carrier question is resolved at the level of a no-go theorem from $R$.
- [x] The realization/decisiveness layer $S$ is settled at the level of a conditional existence theorem and a non-canonicity theorem.
- [x] The locality/cover question is settled at the level of a no-go theorem from the solved $R+S$ layer.
- [x] The locality/cover layer $C$ is explicitly introduced as the next minimal added branch structure.
- [x] The lawful-transformation question is settled at the level of a no-go theorem from the solved $R+S+C$ layer.
- [x] The lawful-transformation layer $T$ is explicitly introduced as the next minimal added branch structure.
- [x] The distinguisher/signature question is settled at the level of a no-go theorem from the solved $R+S+C+T$ layer.
- [x] The distinguisher/signature layer $D$ is explicitly introduced as the next minimal added branch structure.
- [x] The stable-comparison question is settled at the level of a no-go theorem from the solved $R+S+C+T+D$ layer.
- [x] The stable-comparison layer $A$ is explicitly introduced as the next minimal added branch structure.
- [x] The valuation question is settled at the level of a no-go theorem from the solved $R+S+C+T+D+A$ layer.
- [x] The valuation layer $V$ is explicitly introduced as the next minimal added branch structure.
- [ ] The parameterization question is settled.
- [ ] The full CF000 branch is complete.

This document is **not yet a Completed Formalism** for the entire CF000 program. It is a theorem-bearing draft pass that resolves the stable-comparison question relative to the solved $R+S+C+T+D$ layer and honestly blocks premature ascent to higher layers.
