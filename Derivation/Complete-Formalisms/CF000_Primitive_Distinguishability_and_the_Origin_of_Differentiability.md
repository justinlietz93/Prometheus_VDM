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

- all central objects are defined or explicitly imported with hypotheses verified,
- all theorem-bearing claims have explicit hypotheses, conclusions, and auditable proofs,
- all essential derivation, validation logic, and failure conditions are present in this document,
- no core burden is outsourced to canon links, notebooks, figures, or code,
- any claim that is heuristic, conjectural, programmatic, or only partially established is labeled as such,
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
- CF00 begins only after a differentiable carrier and lawful local variation are available.
- CF01 remains a downstream effective engine formalism.
- CF11 remains a downstream derived-limit module.
- Later CFs remain downstream of the differentiable layer made possible by CF000.

Accordingly, this document does not borrow its core derivation from CF00 or any later CF. It may mention downstream consequences, but it must earn the layer on which they depend.

---

## Executive Summary

CF000 begins beneath differentiability. It excludes absolute nullity and absolute undifferentiated sameness as viable roots for a falsifiable physical branch, then identifies the weakest surviving primitive residue as a nonempty distinction-bearing multiplicity $({\mathcal B},\\#)$ with primitive apartness and no imported metric, valuation, parameter, derivative, or topology.

The present pass resolves the next live theorem burden: whether the explicitly added refinement/compatibility structure $R$ is sufficient to force stable realized distinction contents and a realized carrier layer. The answer is no. Refinement/compatibility is enough to make the question of realization meaningful, but it does not by itself force the existence or canonicity of realized contents. A no-go theorem is proved: there exist $R$-models in which no decisive coherent realized content exists, and there exist $R$-models in which multiple inequivalent realized-content families exist. Therefore realized contents and a realized carrier are **not** forced from $R$ alone.

The document accordingly identifies the next candidate branch structure, denoted $S$, as a realization/decisiveness layer. $S$ is not yet claimed theorem-grade. It is introduced only as the next minimal branch-candidate structure required if the branch is to continue upward toward locality, comparison, valuation, parameterization, and differentiability.

This pass therefore freezes the current root staircase as follows:

- nullity and undifferentiated sameness are excluded,
- primitive distinguishability is the weakest surviving root,
- refinement/compatibility is the first minimal added branch structure,
- realized contents/carrier are **not** yet forced from that layer,
- and the branch must not climb upward until the realization question is settled honestly.

Principal deliverables of this pass:

- exclusion of absolute nullity and absolute undifferentiated sameness as root candidates for this branch;
- identification of primitive distinguishability as the weakest surviving residue;
- explicit separation between forced structure, minimally added branch structure, and conditional theorem structure;
- no-go theorem showing that refinement/compatibility alone does not force stable realized distinction contents or a realized carrier;
- identification of realization/decisiveness as the next candidate branch structure;
- falsification criteria for the no-go theorem and for the realization candidate;
- updated dependency audit and acceptance checklist.

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
- The weakest surviving residue is a nonempty distinction-bearing multiplicity $({\mathcal B},\\#)$ with nontrivial apartness and no imported metric, valuation, parameterization, continuity, or differentiability.
- A direct leap from primitive distinction to differentiability is illegitimate.
- Refinement/compatibility is **not** forced from primitive distinction alone.
- Refinement/compatibility has been reclassified as the first minimal added branch structure.
- Refinement/compatibility alone does **not** force stable realized distinction contents or a realized carrier.

### Provisional results

- A realization/decisiveness layer $S$ is the current best candidate for the next minimal branch structure.
- A cover/locality discipline may later be needed if the branch wants pre-metric locality.
- Lawful transformation, distinguishers, stable comparison, valuation, and parameterization may later be needed for one route to differentiability.

These are not yet earned in the present pass.

### Rejected routes

- Primitive import of differentiable carriers, coordinates, metric, distance, derivatives, scalar probes, quotients, matrices, continuity, or chart structure.
- Treating refinement/compatibility as already theorem-grade from the nullity/sameness exclusions alone.
- Treating realized contents or a realized carrier as already forced from refinement/compatibility alone.
- Treating valuation as already forced at the present layer.

### Live theorem target

Determine whether a realization/decisiveness layer $S$ is enough to force stable realized distinction contents and a realized carrier, or whether still further minimal structure is required before the branch can proceed toward locality, comparison, and differentiability.

### Forbidden regressions

The document may not proceed upward to cover, lawful transformation, comparison algebra, valuation, parameterization, or differentiability until the realized-content / realized-carrier question is settled and written into the document.

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

The branch does not begin by assuming that any of these are numerical or geometric.

### 1.4 Primitive notation convention

To prevent later overload:

- $\mathcal B$ denotes the primitive distinction-bearing bearer class.
- $\\#$ denotes primitive apartness.
- $\widehat{\mathcal B}$ denotes an admissibly enriched bearer class once added branch structure is introduced.
- $\mathcal M_0$ denotes the realized pre-differential carrier of stable distinction contents, if and when such a carrier is earned later.
- $\mathcal M$ denotes the downstream differentiable carrier earned only after parameterization and differentiability results are established.
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

1. the primitive distinction-bearing residue $({\mathcal B},\\#)$,
2. the first added sharpenability discipline $L1$,
3. the explicitly added refinement/compatibility structure $R$.

The present pass does **not** yet commit to a realized carrier, locality, process, comparison algebra, valuation, parameterization, or differentiability.

---

## 2. Mathematical Setting and Definitions

### 2.1 Primitive bearer class and apartness

The primitive substrate at the present deepest justified level is
$$
(\mathcal B, \\#),
$$
where $\mathcal B$ is a nonempty bearer class and $\\#$ is a primitive nontrivial apartness relation.

### 2.2 Minimal primitive laws

The primitive relation satisfies only the weakest laws presently forced:

1. **Nonempty bearer**
   $$
   \mathcal B \neq \varnothing.
   $$

2. **Nontrivial extension**
   $$
   \exists a,b\in\mathcal B\text{ such that }a\\# b.
   $$

3. **Irreflexivity**
   $$
   \neg(a\\# a).
   $$

4. **Symmetry**
   $$
   a\\# b \Rightarrow b\\# a.
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

Likewise, $a\\# b$ does not yet mean metric separation, measurable difference, process difference, or local variation. It means only that $a$ and $b$ are primitively not the same in a nontrivial way.

### 2.4 First added branch commitment: sharpenability

The current pass tests whether pure distinction alone can support lawful continuation of the branch. To ask that question, the branch introduces exactly one minimal additional principle.

**Principle L1 (Sharpenability discipline).**  
If a distinction is to remain meaningful in a law-bearing continuation of the branch, then it must admit admissible sharpening without erasing already-witnessed distinction content.

L1 is not claimed to be forced from pure apartness. It is the first **minimal added branch commitment** required to test whether law-bearing continuation is possible.

### 2.5 First explicit added branch structure: refinement/compatibility

Since primitive distinction together with L1 does not force a unique global refinement/compatibility regime, the branch introduces refinement/compatibility explicitly.

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
  x \preceq y \land y\\# z \Rightarrow x\\# z.
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
   - there exists $x\in X$ with $x \\# b$.

The class of all such $R$-candidate realized contents, if nonempty, is denoted
$$
\mathcal M_0^{(R)}.
$$

This definition is not yet a theorem of existence. It is the weakest honest candidate notion of realized content available at this stage.

---

## 3. Foundational Construction

### 3.1 Nullity exclusion

**Theorem 3.1.1 (Nullity exclusion).**  
Absolute nullity is not a viable root for this branch.

**Proof.**  
A physical branch of theory must at minimum permit a difference between success and failure of a statement, between one admissible state and another, and between a law and the absence of law. Absolute nullity supports none of these because it contains no bearer, no distinction, and no possible witness structure. Therefore nullity cannot serve as the root of a falsifiable formal branch. This is a theorem about formal-role viability for this branch, not a universal metaphysical theorem about all possible notions of nothing. $\square$

### 3.2 Undifferentiated sameness exclusion

**Theorem 3.2.1 (Undifferentiated sameness exclusion).**  
Absolute undifferentiated sameness is not a viable root for this branch.

**Proof.**  
If all admissible presentations are undifferentiated, then no nontrivial comparison can be made. Comparison, persistence, lawful separation, and falsification all collapse because there is no content by which one state could fail to match another. Thus absolute undifferentiated sameness is as unusable for this branch as nullity, although for a different reason: it has bearer-like content but no nontrivial distinction. $\square$

### 3.3 Weakest surviving primitive

**Theorem 3.3.1 (Weakest surviving primitive).**  
For this branch, once nullity and absolute undifferentiated sameness are excluded, the weakest surviving primitive is a distinction-bearing multiplicity $({\mathcal B},\\#)$ satisfying nonempty bearer, nontrivial extension, irreflexivity, and symmetry.

**Proof.**  
Nullity excludes bearer and relation altogether. Undifferentiated sameness excludes nontrivial distinction. Therefore any surviving root must contain at least a nonempty bearer class and at least one nontrivial distinction relation on it. Any stronger primitive package — order, cover, metric, value, update, or process — adds content not forced by those two exclusions alone. Hence $({\mathcal B},\\#)$ is the weakest currently justified root. $\square$

### 3.4 First branch fork: can pure distinguishability support law?

Pure apartness is enough to exclude nullity and sameness. It is not obviously enough to support law.

If the branch is to support law rather than one-shot distinction, then distinctions must be:

1. revisitably meaningful,
2. sharpenable without erasure of already-witnessed content,
3. and stably reusable in later comparison contexts.

Principle $L1$ expresses this demand, but $L1$ itself does not yet define a stable global refinement or compatibility regime. The first live theorem target was therefore whether $L1$ together with pure apartness is enough to force such a regime. That question has already been resolved negatively.

### 3.5 No-go theorem for forcing refinement/compatibility

**Theorem 3.5.1 (No-go theorem for refinement forcing).**  
Primitive distinction-bearing multiplicity $({\mathcal B},\\#)$ together with the sharpenability discipline $L1$ does **not** force a unique or canonical stable refinement/compatibility regime. Therefore refinement/compatibility is not theorem-grade from the prior layer. It must be introduced explicitly as the first minimal added branch structure if the branch is to continue toward law.

**Hypotheses.**

1. $({\mathcal B},\\#)$ satisfies the laws of Section 2.2.
2. Principle $L1$ holds: physically meaningful distinction admits admissible sharpening without erasing already-witnessed distinction content.
3. No further primitive assumptions are added regarding order, compatibility, locality, value, process, or comparison.

**Conclusion.**

Under these hypotheses alone, there is no unique forced global refinement preorder or compatibility relation. More strongly, there exist distinct non-isomorphic sharpenability realizations compatible with the same primitive substrate and with $L1$, but yielding inequivalent refinement/compatibility structures. Hence refinement/compatibility is not forced from the prior layer.

**Proof.**

Fix a primitive substrate with two distinguishable bearers,
$$
a,b \in \mathcal B,
\qquad
 a\\# b.
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
again preserving $a\\# b$ along each chain. Now also adjoin a coarse compatibility token $c$ that is not itself apart from either $a$ or $b$, and stipulate that certain admissible comparison contexts may pass through $c$ as a common coarse context without identifying $a$ and $b$ or making them refinements of one another.

This also realizes $L1$. It yields a much richer sharpening and compatibility regime than R1.

The two realizations are not isomorphic as refinement/compatibility structures:

- R1 has only isolated one-step branchwise refinement.
- R2 has infinite branchwise refinement and an additional compatibility organization through coarse context tokens.

Yet both respect the same primitive substrate $({\mathcal B},\\#)$ and the same sharpenability discipline $L1$. Therefore $L1$ does not determine a unique global refinement/compatibility regime. Since no uniqueness, canonicity, or forcing theorem follows from the prior layer alone, refinement/compatibility is not theorem-grade from primitive distinction plus $L1$.

Hence the branch must add refinement/compatibility explicitly if it wishes to continue beyond pure distinguishability. $\square$

### 3.6 What Theorem 3.5.1 does and does not prove

**What it proves.**

- Primitive distinction plus sharpenability is insufficient to force a unique stable refinement/compatibility regime.
- Any continuation of the branch that needs such a regime must add it explicitly.

**What it does not prove.**

- It does not show that refinement is impossible.
- It does not show that cover, locality, transformation, valuation, or differentiability are impossible.
- It does not show that all refinement systems are equally good.
- It does not identify the unique best added refinement system.

It proves only the no-go result needed here: refinement/compatibility is **not forced** from the prior layer.

### 3.7 Realized-content / realized-carrier forcing theorem or no-go theorem

The present pass now addresses the next live question.

**Theorem 3.7.1 (No-go theorem for realized-carrier forcing from $R$).**  
The explicitly added refinement/compatibility structure $R$ is **not** sufficient, by itself, to force stable realized distinction contents or a realized carrier layer. More precisely:

1. there exist $R$-models for which $\mathcal M_0^{(R)} = \varnothing$;
2. there exist $R$-models for which $\mathcal M_0^{(R)} \neq \varnothing$ and contains multiple inequivalent candidate realized contents;
3. therefore neither the existence nor the canonicity of a realized carrier is forced from $R$ alone.

**Hypotheses.**

1. The primitive substrate $({\mathcal B},\\#)$ satisfies Section 2.2.
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
a \\# b,
$$
and no apartness involving $c$ except irreflexive triviality. Let refinement be reflexive only,
$$
x \preceq x,
$$
for all $x \in \widehat{\mathcal B}_A$, and let compatibility be identity only,
$$
x \bowtie y \iff x=y.
$$

This satisfies the axioms of $R$:

- reflexive refinement holds by definition;
- transitive refinement is trivial because refinement is identity only;
- apartness persistence holds vacuously beyond the primitive apartness pair;
- compatibility symmetry holds because identity is symmetric;
- refinement monotonicity of compatibility holds because if $x'\preceq x$ and $x\bowtie y$, then $x'=x$ and $y'=y$ work.

Now test candidate realized contents.

A singleton such as $\{a\}$ is nonempty, refinement-saturated, and finitely coherent. But it fails decisiveness for $c$: there is no $x\in\{a\}$ with $x\bowtie c$, because compatibility is identity only and $a\neq c$; there is also no $x\in\{a\}$ with $x\\# c$, because no apartness between $a$ and $c$ has been stipulated. The same failure occurs for $\{b\}$ and $\{c\}$.

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
a \\# b,
$$
refinement again reflexive only, and compatibility identity only.

This also satisfies $R$. Now both singleton sets $\{a\}$ and $\{b\}$ are $R$-candidate realized contents:

- they are nonempty,
- they are refinement-saturated,
- they are finitely coherent,
- and they are decisive because each sees itself by compatibility and the other by apartness.

Thus
$$
\mathcal M_0^{(R)} = \{\{a\},\{b\}\}
$$
in Model B.

So even when realized contents exist, they need not be unique or canonical.

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

### 3.9 Next candidate minimal branch structure: realization/decisiveness layer $S$

Since $R$ does not force realized contents, the next candidate branch structure is a realization/decisiveness layer $S$.

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

$S$ is **not** yet theorem-grade. It is the current best candidate for the next minimal branch structure if the branch is to continue toward a realized carrier.

---

## 4. Main Theorems and Proofs

The main theorems of this pass are Theorems 3.1.1, 3.2.1, 3.3.1, 3.5.1, and 3.7.1. No theorem stronger than those is claimed at this stage.

### 4.1 Theorem status map for this pass

- **Forced from prior layer:**
  - nullity exclusion,
  - undifferentiated sameness exclusion,
  - weakest surviving primitive $({\mathcal B},\\#)$.

- **Minimal added branch structure:**
  - sharpenability discipline $L1$,
  - refinement/compatibility structure $R$.

- **Conditional theorem under explicit assumptions:**
  - none beyond the no-go theorems in this pass.

- **Candidate next added branch structure:**
  - realization/decisiveness layer $S$.

### 4.2 Claims deferred until later passes

The following are not yet theorem-grade and are not used in this pass:

- cover/locality,
- realized carrier existence theorem,
- lawful transformation,
- distinguishers/signatures,
- comparison algebra,
- valuation representation,
- parameterization,
- differentiability emergence.

No later section of this document may rely on these as established until they are derived in later passes.

---

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

### 5.4 What would show the added structure $R$ is too strong

The added branch structure $R$ would be too strong if one could exhibit a weaker added structure than $R$ that still suffices to support all later branch requirements:

- stable realization,
- lawful local organization,
- stable comparison,
- and the later route toward differentiability.

If such a weaker structure is found, $R$ must be weakened in a later pass.

### 5.5 What would show the candidate structure $S$ is too strong

The candidate realization layer $S$ would be too strong if one could exhibit a weaker added principle than $S$ that still guarantees:

- existence of realized contents,
- decisiveness/sharpness of those contents,
- and a realized carrier layer sufficient for later branch continuation.

If such a weaker structure is found, $S$ must be weakened before canonization.

### 5.6 What would show the current derivation still smuggles later structure

This pass would be defective if any proof above implicitly relied on:

- metric notions,
- topology stronger than what is stated,
- numeric valuation,
- parameterized process,
- comparison algebraic laws not explicitly introduced,
- or differentiated locality.

The present pass is designed to stop before those imports occur.

---

## 6. Worked Example or Minimal Witnesses

Two minimal witnesses suffice for the present pass.

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
a\\# b,
$$
refinement reflexive only, compatibility identity only, and no other apartness relations. Then $R$ holds, but no $R$-candidate realized content exists.

#### Witness B: $R$ with multiple realized contents

Take
$$
\widehat{\mathcal B}_B = \{a,b\},
$$
with
$$
a\\# b,
$$
refinement reflexive only, and compatibility identity only. Then $R$ holds, and both $\{a\}$ and $\{b\}$ are $R$-candidate realized contents.

These two witnesses jointly establish that $R$ alone forces neither existence nor canonicity of a realized carrier.

---

## 7. CFN Pairing and Executable Traceability

The paired CFN for the present pass may do the following:

- instantiate finite examples of primitive substrates $({\mathcal B},\\#)$,
- instantiate multiple non-isomorphic sharpening realizations over the same primitive substrate,
- instantiate $R$-models with and without $R$-candidate realized contents,
- verify that the witness models satisfy the stated axioms,
- and present the no-go theorems graphically or combinatorially.

The CFN may **not** introduce any proof burden not already carried here.

---

## 8. Assumptions, Limits, and Open Boundaries

### 8.1 Assumptions used in the derivation

This pass uses only:

1. the branch-level exclusion of nullity and undifferentiated sameness,
2. the weakest surviving primitive $({\mathcal B},\\#)$,
3. the first added sharpenability discipline $L1$,
4. the explicitly added refinement/compatibility structure $R$,
5. elementary logic about non-isomorphic realizations and nonexistence/existence witnesses.

### 8.2 Claims established here

This pass establishes:

- the root exclusions,
- the weakest surviving primitive,
- the no-go theorem for forcing refinement/compatibility from the prior layer,
- the explicit introduction of refinement/compatibility as the first minimal added branch structure,
- the no-go theorem showing that $R$ alone does not force stable realized contents or a canonical realized carrier,
- and the identification of $S$ as the current next candidate branch structure.

### 8.3 Claims not established here

This pass does not establish:

- cover/locality,
- realized-carrier existence theorem,
- lawful transformation,
- distinguishers/signatures,
- comparison algebra,
- valuation representation,
- parameterization,
- differentiability.

### 8.4 Open boundary for the next pass

The next pass must determine whether the candidate realization/decisiveness layer $S$ is enough to force stable realized contents and a realized carrier, or whether still further minimal branch structure is required.

No upward climb beyond realization is allowed before that question is settled.

---

## 9. Integration with Broader VDM Theory

CF000 remains the root of the branch.

CF00 remains downstream as the first differentiable-layer formalism, but the present pass does not yet reconnect to CF00 in detail. That bridge is intentionally paused until the realization question is settled honestly.

The only downstream statement fixed here is structural and negative:

> CF00 may not be treated as beginning from a layer already forced by primitive distinction and refinement/compatibility alone.

Instead, CF00 sits downstream of a branch that now explicitly contains:

1. a forced primitive distinction layer,
2. a first minimal added refinement/compatibility layer,
3. and an unresolved but now sharply posed realization layer.

---

## 10. References and Provenance

This pass uses the house CF template as the formal standard for completeness and theorem-bearing structure.

It also uses the current CF000 checklist as the binding solved/open state for this pass. The theorem target addressed here is exactly the live question identified there: whether the added refinement/compatibility structure $R$ is enough to support realized contents and a realized carrier. The answer given here is no. The current checklist state therefore advances accordingly. fileciteturn122file0

No external source is used here as a substitute for derivation.

---

## Appendix A. Symbol Table

- $\mathcal B$: primitive distinction-bearing bearer class.
- $\\#$: primitive apartness relation.
- $L1$: sharpenability discipline.
- $\widehat{\mathcal B}$: admissibly enriched bearer class after added branch structure.
- $\preceq$: refinement preorder.
- $\bowtie$: compatibility relation in the first added branch structure.
- $R$: first minimal added branch structure consisting of refinement/compatibility.
- $\mathcal M_0^{(R)}$: class of $R$-candidate realized distinction contents, not yet forced to be nonempty.
- $S$: current candidate realization/decisiveness layer, not yet theorem-grade.
- $\mathcal M_0$: placeholder symbol for a realized pre-differential carrier, not yet earned in this pass.
- $\mathcal M$: downstream differentiable carrier, not yet earned in this pass.

---

## Appendix B. Dependency Audit

### Primitive in this pass

- $({\mathcal B},\\#)$

### Forced from prior layer in this pass

- nullity exclusion,
- undifferentiated sameness exclusion,
- weakest surviving primitive.

### Minimal added branch structure in this pass

- sharpenability discipline $L1$,
- refinement/compatibility structure $R$.

### Candidate next added branch structure

- realization/decisiveness layer $S$.

### Conditional or deferred beyond this pass

- cover/locality,
- realized-carrier forcing theorem,
- lawful transformation,
- distinguishers/signatures,
- comparison algebra,
- valuation,
- parameterization,
- differentiability emergence.

### Main dependency chain of this pass

$$
\text{nullity failure and sameness failure}
\to
({\mathcal B},\\#)
\to
L1
\to
\text{no-go theorem for forced refinement}
\to
R
\to
\text{no-go theorem for forced realization}
\to
S.
$$

No later object is used in the proofs of this pass.

---

## Appendix C. CFN Traceability Table

| CF section | CFN segment | quantities instantiated | diagnostics emitted | claims witnessed |
|---|---|---|---|---|
| §2–§3.3 | `cf000-root-exclusions` | example substrates $({\mathcal B},\\#)$ | nullity/sameness exclusion witness cases | Theorems 3.1.1–3.3.1 |
| §3.5 | `cf000-refinement-nogo` | non-isomorphic sharpening realizations | structure-comparison tables | Theorem 3.5.1 |
| §3.7 | `cf000-realization-nogo` | $R$-models with and without realized contents | realization existence/nonexistence witness tables | Theorem 3.7.1 |
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
- [x] The refinement/compatibility question is resolved.
- [x] The realized-content / realized-carrier question is resolved at the level of a no-go theorem from $R$.
- [ ] The realization/decisiveness layer $S$ is settled.
- [ ] The full CF000 branch is complete.

This document is **not yet a Completed Formalism** for the entire CF000 program. It is a theorem-bearing draft pass that resolves the realized-content / realized-carrier question relative to $R$ and honestly blocks premature ascent to higher layers.
