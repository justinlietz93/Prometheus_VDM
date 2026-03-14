# CF000: Complete Formalism — Primitive Distinguishability and the Origin of Differentiability in VDM

Date: 2026-03-14  
Version: v20  
Status: Review Draft — HRDAP exact-fork / non-finality guardrails integrated  
Gap Module: Root formalization beneath CF00  
Proposer: Justin K. Lietz  
License: See LICENSE

---

### Completion Standard for CF Canon

A document may carry the status **Completed Formalism** only if it is a **closed, theorem-grade formal specification within its declared scope, assumptions, and domain of validity**.

This means:

- all central objects are defined or explicitly imported with hypotheses verified,
- all theorem-bearing claims have explicit hypotheses, conclusions, and auditable proofs,
- all essential derivation, validation logic, and failure conditions are present in this document,
- no core burden is outsourced to canon links, notebooks, figures, or code,
- any claim that is heuristic, conjectural, programmatic, or only partially established is labeled as such,
- if any essential proof burden is missing, this document is **not** a Completed Formalism.

“Completed” does **not** mean universally maximal or beyond all future strengthening. It means the claimed result is closed **at the level stated in the document**.

---

## Root Rule of This Document

This CF is the root written source of truth for the pre-differential layer of this branch of VDM.

The root claim of this document is the **single fundamental primitive bifurcation law**:

> the only logically admissible primitive origin is one primitive condition whose content bears two mutually unreconcilable terminal poles, absolute nullity and absolute undifferentiated totality; neither isolated pole can terminate the burden without collapse; unresolved pole-opposition is therefore constitutive of the admissible origin; every admissible articulation stands under that same undischarged burden.

This rule is not used here as a loose metaphor, a one-time split, or a dynamical picture. It is the manuscript basis. The paper must therefore stop reading as a sequence of mostly separate burden modules and instead show how the lowest-resolution invariant-bearing differentiated degree at origin, the valid character/admission split, and RRP are more articulated determinations of one undischarged primitive invariant.

### Consequence of this rule

For this document:

- the primitive tension must be treated as **derived from the only admissible origin**, not inserted as an extra unexplained assumption,
- the origin must be treated as **one primitive condition**, not as two externally separated things,
- the two poles must be treated as **logically distinct but primitively undifferentiated in being**,
- the poles are not primitively apart,
- any admissible settlement short of terminal discharge is not final resolution,
- any articulation named elsewhere in the manuscript must be tested as an invariant-bearing articulation of the undischarged primitive burden, not as an independent primitive.

---

## Relationship to Canon and External Documents

Canon documents, proposal artifacts, hypothesis notes, and later CFs may be cited for provenance, naming, alignment, and program integration. They may not be used to outsource root derivation that belongs here.

For the present manuscript:

- **H000** captures the proposal-grade primitive bifurcation hypothesis,
- the doctrinal note on the **single fundamental primitive bifurcation law** records the intended root law in compact form,
- **A8** is not the primitive generator here; it is a later-regime candidate expression of the undischarged primitive invariant burden under added burden,
- **CF00** remains downstream of any legitimate pre-carrier and pre-differential closure obtained here.

No later canon object — manifold, chart, overlap class, support family, QGT, or $J\oplus M$ split — may be used to prepay burden at the root layer.

---

## Relationship to the CFN

No paired CFN is required for the present stage because the present burden is still theorem-hygiene and dependency-order work rather than executable realization. If a later CFN is built, it may only instantiate, test, or illustrate constructions already formalized here. It may not supply missing root logic.

---


## Executive Summary

This manuscript keeps the primitive bifurcation invariant as the root basis, treats the admissible primitive origin as fixed in-body rather than by a detachable added existence premise, preserves closure of the lowest-resolution positive articulation after origin, preserves the valid character/admission split for higher-resolution-degree claims, and installs an explicit theorem-hygiene guardrail for the live HRDAP burden: a semantic budget, a blocked-import list, and an unlocked-definitions ledger so the manuscript cannot quietly prove higher-resolution-degree admission with meanings that only become legal after that burden closes. The current package still does not license the lowest-resolution degree as exhaustively complete, and it still does not prove admission of a genuinely higher-resolution differentiated degree.

The doctrinal correction is now explicit. The invariant belongs to every admissible degree. A higher-resolution degree does not introduce a new invariant; it is a more articulated determination under the same undischarged primitive invariant. If a higher-resolution differentiated degree is admitted, the lower-resolution degree is no longer sufficient as the sole determination of the state. This is not time and not causality. It is a dependence-ranked clarification rule.

The theorem-spine naming correction is therefore as follows. The lowest-resolution positive articulation after origin is written
$$
\mathrm{Deg}_{\min}(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x).
$$
The next live burden is phrased as the question whether the current root package closes **increased resolution by admissible degrees of invariant-bearing articulation** by admitting a genuinely higher-resolution differentiated degree under the undischarged primitive invariant.

The character/admission split is preserved, and renamed safely:

1. **HRDCL — Higher-Resolution Degree Character Lemma.** If a lowest-resolution invariant-bearing differentiated degree after origin admits a genuinely higher-resolution differentiated degree under the undischarged primitive invariant, then the lower-resolution degree is no longer sufficient as the sole determination of the state and an additional internal determination is present. This still does **not** earn apartness, nodehood, metric structure, or completed boundaries.
2. **HRDAP — Higher-Resolution Degree Admission Principle.** The present package does **not** yet prove that such a genuinely higher-resolution differentiated degree is admitted.

The dependency verdict is therefore cleaner while changing nothing essential in the frame. **The admissible primitive origin is fixed in-body, not by a detachable added premise. The lowest-resolution positive articulation after origin closes directly from the Section 3 forced-origin derivation together with PB5. The character/admission split remains valid.** What changes is only that the split is now stated in fully pre-geometric, dependence-ranked language.

Principal deliverables of this CF:

- primitive bifurcation invariant frame preserved without reopening the architecture,
- closure of the lowest-resolution positive articulation after origin preserved,
- valid character/admission split preserved,
- retirement of spatial theorem-spine language such as **“widening,”**
- retirement of sequence-heavy theorem-spine language where dependence-ranked wording is sufficient,
- proof of the **Higher-Resolution Degree Character Lemma** in dependence-ranked language,
- isolation of **HRDAP** as the exact remaining admission burden,
- explicit statement that higher-resolution degrees clarify lower-resolution ones without creating a new invariant,
- explicit statement that the lowest-resolution degree is not licensed as exhaustively complete by the present package,
- an explicit **semantic budget / blocked imports / unlocked definitions** mechanism for the HRDAP scope,
- updated theorem inventory, open-burden inventory, migration delta, contamination audit, and appendix crosswalk.

## Read Me First: Writing Rules for This CF

1. This document must be self-contained at the level required to understand, test, and reuse the root formalism.
2. Every theorem-bearing section must expose its proof burden directly.
3. The primitive bifurcation invariant is the root basis; no section may silently revert to a modular burden stack that forgets the primitive bifurcation invariant.
4. No section may use words such as “emerges,” “reactivates,” “propagates,” or “branches” without specifying exactly what is proved, what is added, and what stays blocked.
5. Distinguish clearly between:
   - adopted root law,
   - proved theorem,
   - required extra principle,
   - blocked downstream target,
   - working interpretation.
6. If a section is incomplete, the CF remains incomplete.

---

## 1. Scope, Ontology, and Primitive Commitments

### 1.1 Root question

CF00 begins with a differentiable carrier $\mathcal M$ and lawful partial variation on it. CF000 exists because that is already too late for an absolute root account.

The root question of this document is:

> What is the earliest admissible primitive law from which distinguishability, recursive articulation, and eventually carrier-adjacent burden could be earned without primitive geometry, metricity, time, causality, valuation, parameterization, or differentiability?

### 1.2 Rewrite stance

This rewrite adopts the following stance.

1. Earlier staircase-style formulations are retained only as failure-audit material.
2. Earlier cleanup passes are retained only as contamination cleanup, not as root architecture.
3. The present manuscript is rebuilt so that the primitive unresolved pole-opposition is the permanent invariant of the whole system.
4. The lowest-resolution invariant-bearing differentiated degree after origin, the higher-resolution-degree split, and RRP must appear as downstream expressions of that invariant, not as mostly separate modules.
5. No graph, tree, branch map, frontier object, or carrier language may appear before it is honestly earned.

### 1.3 Primitive vocabulary versus blocked imports

#### Primitive in this rewrite

The primitive package of the present draft contains only:

- two distinguished terminal pole marks,
- their non-identity,
- their sterility for realized differentiated articulation,
- their opposition,
- an origin-candidate predicate,
- a non-vacuousness predicate,
- a realizability predicate,
- a flatness predicate,
- and the root law that the only admissible primitive origin, carrying unresolved pole-opposition internally, cannot remain perfectly self-coincident.

#### Forbidden as primitive

The following are forbidden at root level:

- primitive bearer multiplicity $(\mathcal B,\#)$,
- nodes, edges, graphs, trees, branch maps, ancestry, depth, frontier, sectors,
- attenuation maps, weights, energies, valuations, metrics, or measures,
- time parameter, event sequence, propagation, causality, or irreversible arrow,
- neighborhoods, covers, overlaps, patch maps, or chart language,
- topology, metric space structure, continuity, derivatives, smoothness,
- observables, comparison algebra, valuation maps, parameterization,
- QGT, induced geometry, $J\oplus M$, or any downstream CF00 machinery.

### 1.4 Status convention

Every major claim in this document is labeled as one of:

- **Proved**
- **Requires one new explicit principle**
- **Not proved**
- **Blocked**

In addition, this draft uses the following architectural rule:

> if a statement about a genuinely higher-resolution differentiated degree or RRP is written in a way that makes it look like an independent source rather than a further articulation of the undischarged primitive invariant burden, the statement is frame-contaminated even if its low-level wording is careful.

### 1.5 Handoff target to CF00

CF000 does not need to derive QGT, metric curvature, or metriplectic evolution. It must only close enough pre-differential burden to justify a legitimate handoff point for CF00.

That handoff point is still open. The present draft does not pretend otherwise.

---

## 2. Mathematical Setting and Definitions

### 2.1 Logical domain of discourse

Let $\mathcal C$ denote the logical domain of candidate realization conditions.

This is **not** a primitive ontology of objects in the world. It is a logical range of discourse only. It is introduced so that realizability claims can be stated without presupposing points, states, branches, fields, graphs, or manifolds.


### 2.2 Definitions table

| Term | Plain-language meaning | Formal symbol / schematic definition | What it explicitly does **not** assume | Status |
|---|---|---|---|---|
| Absolute nullity | complete realized absence | distinguished pole mark $\mathbf 0$ | not the empty set; not an empty region; not a vacuum in already-given space | Primitive |
| Absolute undifferentiated totality | complete homogeneous one-ness without internal noncoincidence | distinguished pole mark $\mathbf 1$ | not “one object” inside already-given plurality; not a constant field on a background | Primitive |
| Origin candidate | candidate primitive condition for a realized branch | predicate $\mathrm{Orig}(x)$ on $\mathcal C$ | does not assume uniqueness, time, geometry, or support | Primitive |
| Sterile | cannot admit realized differentiated articulation while remaining what it is | predicate $\mathrm{Ster}(x)$ | does not automatically mean flat; does not assume dynamics | Primitive |
| Flat | contains no realized internal noncoincidence by which differentiated articulation could be sustained | predicate $\mathrm{Flat}(x)$ | does not assume plurality, graph language, or metric sameness | Primitive |
| Non-vacuous | not complete realized absence in the root sense | predicate $\mathrm{NV}(x)$ | does not assume multiplicity | Primitive |
| Realizable | admissible as a non-vacuous realized branch-condition | predicate $\mathrm{Real}(x)$ | does not yet mean anything beyond admissibility as branch-condition | Primitive |
| Opposition | non-identity of the two terminal poles together with their shared sterility verdict | predicate $\mathrm{Opp}(x,y)$ | does not assume external separation, interaction law, or dynamics | Primitive |
| Primitive bifurcation invariant | one primitive origin-condition bears unresolved pole-opposition internally and does not terminate in pole-discharge | schematic shorthand $\mathrm{Inv}(x)$ | does not assume two externally situated things; does not assume time or graph language | Derived shorthand |
| Differentiated articulation | realizable condition that is not flat | $\mathrm{Diff}(x):=\mathrm{Real}(x)\wedge \neg \mathrm{Flat}(x)$ | does not assume multiplicity, apartness, or carrier language | Derived |
| Lowest-resolution invariant-bearing differentiated degree after origin | the undischarged primitive invariant is now carried non-flatly rather than in primitive undifferentiated form, at the least articulated admitted degree after origin | shorthand $\mathrm{Deg}_{\min}(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x)$ | does not mean smoothness, charts, or manifold differentiability; does not mean event sequence or causality | Derived lowest-resolution positive articulation after origin |
| Genuinely higher-resolution differentiated degree | a higher-resolution articulation of the undischarged primitive invariant that adds an internal determination rather than merely renaming the lower one | schematic notion used in theorem statements | does not yet assume apartness, metric structure, or time | Derived target notion |
| HRDCL | if a genuinely higher-resolution differentiated degree is admitted, then the lower-resolution degree is no longer sufficient as sole determination and an additional internal determination is present | theorem-level result, not primitive law | does not assert admission of a higher-resolution differentiated degree; does not yield apartness or geometry | Proved theorem |
| HRDAP | at least one origin-bearing lowest-resolution invariant-bearing differentiated degree after origin admits a genuinely higher-resolution differentiated degree under the undischarged primitive invariant | higher-resolution degree admission principle | does not define apartness or recursion | Requires one new explicit principle |

### 2.3 Definitions table audit note

The table enforces seven distinctions the manuscript may not blur.

1. **Flatness** is an internal structural condition.
2. **Sterility** is a branch-level incapacity verdict.
3. **Differentiated articulation** is the first negative articulation of the invariant.
4. **The lowest-resolution invariant-bearing differentiated degree after origin** is the lowest-resolution positive articulation after origin and does **not** yet imply multiplicity.
5. **A genuinely higher-resolution differentiated degree** is stronger than the lowest-resolution degree and must be kept distinct from mere restatement.
6. **Multiplicity** is stronger than the lowest-resolution degree and remains downstream behind admission of a genuinely higher-resolution differentiated degree.
7. **Recursive refinement** is stronger still and remains downstream behind RRP.

The table also separates **non-vacuousness** from **realizability** and separates the **lowest-resolution invariant-bearing differentiated degree after origin** from smoothness in the later geometric sense.

### 2.4 Primitive root package

Introduce primitive predicates

$$
\mathrm{Orig}(x),\qquad \mathrm{Ster}(x),\qquad \mathrm{NV}(x),\qquad \mathrm{Real}(x),\qquad \mathrm{Flat}(x),\qquad \mathrm{Opp}(x,y).
$$

The present draft adopts the following root laws.

**PB1. Pole non-identity**
$$
\mathbf 0 \neq \mathbf 1
$$

**PB2. Pole sterility**
$$
\mathrm{Ster}(\mathbf 0)\wedge \mathrm{Ster}(\mathbf 1)
$$

**PB3. Pole opposition**
$$
\mathrm{Opp}(\mathbf 0,\mathbf 1)
$$

**PB4. Realizability implies non-vacuousness and pole exclusion**
$$
\forall x\in\mathcal C,\quad \mathrm{Real}(x)\Rightarrow \big(\mathrm{NV}(x)\wedge x\neq \mathbf 0 \wedge x\neq \mathbf 1\big)
$$

**PB5. Invariant carriage precludes flatness**
$$
\forall x\in\mathcal C,\quad \mathrm{Inv}(x)\Rightarrow \neg \mathrm{Flat}(x)
$$

### 2.5 One-origin and no-prior-apartness discipline

The manuscript adopts the following root discipline.

- There is initially no prior basis under which the two poles are primitive separate things.
- Therefore the poles may not be read as two externally separated primitive things.
- Any admissible primitive origin must be read as **one primitive condition** bearing the opposition internally.

This is a root discipline of the rewrite. It is not permission to smuggle in an unearned mediating substance.

### 2.6 Derived shorthand for the invariant

When convenient, write $\mathrm{Inv}(x)$ for the following schematic situation:

- $x$ is an admissible primitive origin-condition,
- $x$ does not coincide with either isolated pole,
- the non-identical sterile poles are opposed,
- that opposition is internal to the one origin-condition,
- and the condition does not terminate in pole-discharge.

This shorthand is mnemonic. It does not replace proof burden.

### 2.7 First derived notion

Define
$$
\mathrm{Diff}(x) := \mathrm{Real}(x)\wedge \neg \mathrm{Flat}(x).
$$

This is the first negative articulation of the invariant. It is also the weak non-self-coincidence layer. What remains open is only the stronger witness-lift burden.

### 2.8 Status of the primitive package

**Proved or stipulated at the present layer:**

- symbolic pole distinction,
- pole sterility,
- pole opposition,
- non-vacuousness / realizability separation,
- flatness / sterility distinction,
- anti-flatness under unresolved pole-opposition.

**Not proved at the present layer:**

- that the full root origin-law elimination has already been unfolded here line by line in theorem-grade detail,
- that anti-flatness already carries a positive witness,
- that positive witness already yields plurality.

---

## 3. Foundational Construction: Forced Origin Architecture

### 3.1 Origin candidate and branch-scope witness

**Definition 3.1.1.**  
An **origin candidate** is any $x\in\mathcal C$ such that $\mathrm{Orig}(x)$ holds.

This says only that $x$ is being tested as a candidate root condition for a realized branch. It does not yet say that $x$ is unique, temporal, geometric, or already articulated.

**Scope Convention 3.1.2 (The branch under study is realized).**  
This manuscript classifies the primitive origin of a realized falsifiable branch rather than the empty possibility class. Let $\omega$ denote the primitive origin-condition of the branch under study. Then
$$
\mathrm{Orig}(\omega)\wedge \mathrm{Real}(\omega).
$$
This is not a detachable added ontological principle about arbitrary worlds. It is the witness fixed by the subject matter of the manuscript itself: given that a realized branch is under study, what must its primitive origin be?

### 3.2 Nullity exclusion

**Theorem 3.2.1 (Nullity exclusion).**  
Absolute nullity is not a viable realized root for a falsifiable law-bearing branch.

**Status:** Proved.

**Proof.**  
A falsifiable law-bearing branch must support at least the distinction between admissible and inadmissible articulation and between realized and unrealized burden. Absolute nullity supports no realized content and no realized distinction. Therefore it cannot serve as the realized root of the present branch. $\square$

### 3.3 Undifferentiated totality exclusion

**Theorem 3.3.1 (Undifferentiated totality exclusion).**  
Absolute undifferentiated totality is not a viable realized root for a falsifiable law-bearing branch.

**Status:** Proved.

**Proof.**  
A falsifiable law-bearing branch requires some realized noncoincidence by which one admissible condition can fail to coincide with another or with itself in a relevant way. Absolute undifferentiated totality contains no internal noncoincidence and therefore cannot sustain differentiated realized articulation. Hence it cannot serve as the realized root of the present branch. $\square$

### 3.4 Shared sterility does not collapse the poles

**Proposition 3.4.1.**  
The poles $\mathbf 0$ and $\mathbf 1$ are not identical even though both are sterile for the present branch.

**Status:** Proved.

**Proof.**  
By PB1, $\mathbf 0\neq\mathbf 1$. By PB2, both are sterile. Distinctness and shared sterility therefore coexist. $\square$

### 3.5 Exhaustive terminal classification at the primitive layer

The root argument cannot stop at exclusion of the two named poles. It must also show why no third simpler terminal primitive outcome survives once richer imports are forbidden.

**Definition 3.5.1 (Terminal primitive pole-candidate).**  
A **terminal primitive pole-candidate** is a primitive origin-candidate considered only at terminal, flat, sterile resolution: no internal noncoincidence is available by which differentiated articulation could be admitted, and no added basis is available by which the candidate could be decomposed or separated.

**Theorem 3.5.2 (No third terminal primitive pole survives).**  
Let $t$ be any terminal primitive pole-candidate. Then exactly one of the following holds:

1. $t=\mathbf 0$ (absolute nullity), or
2. $t=\mathbf 1$ (absolute undifferentiated totality).

In particular, no third terminal primitive pole survives.

**Status:** Proved.

**Proof.**  
Because the primitive layer admits no imported geometry, metricity, plurality, or external two-thing reading, a terminal primitive pole-candidate can be classified only by the weakest root distinctions already on the page: whether any realized content is present at all, and whether any internal noncoincidence is available.

- **Case 1: no realized content is present.** Then the candidate is complete realized absence. By the meaning of $\mathbf 0$, this is absolute nullity, so $t=\mathbf 0$.
- **Case 2: realized content is present.** Then $t$ is non-vacuous. But $t$ is terminal, flat, and primitive by hypothesis. So no internal noncoincidence is available by which differentiated articulation could be admitted, and no richer articulated content may be imported to manufacture such noncoincidence from outside. Therefore the realized content, being present yet internally undifferentiated, collapses to the second primitive extreme: absolute undifferentiated totality. By the meaning of $\mathbf 1$, $t=\mathbf 1$.

There is no third case. A purported third primitive terminal pole would have to either:

- lack realized content, in which case it is Case 1 and collapses to $\mathbf 0$;
- possess realized content while remaining internally undifferentiated, in which case it is Case 2 and collapses to $\mathbf 1$; or
- possess internal noncoincidence or richer articulated content, in which case it is not a terminal flat primitive pole-candidate at all.

So no third terminal primitive pole survives. $\square$

### 3.6 The realized branch-origin cannot terminate in either pole

**Theorem 3.6.1 (The branch-origin is not nullity and not undifferentiated totality).**  
For the realized branch under study, the primitive origin-condition $\omega$ cannot coincide with either isolated terminal pole:
$$
\omega\neq \mathbf 0,\qquad \omega\neq \mathbf 1.
$$

**Status:** Proved.

**Proof.**  
By Scope Convention 3.1.2, $\omega$ is the primitive origin-condition of a realized falsifiable branch. By Theorem 3.2.1, absolute nullity cannot serve as the realized root of such a branch. Therefore $\omega\neq \mathbf 0$. By Theorem 3.3.1, absolute undifferentiated totality also cannot serve as the realized root of such a branch. Therefore $\omega\neq \mathbf 1$. Hence the realized branch-origin cannot terminate in either isolated pole. $\square$

### 3.7 Forced admissible origin theorem

This is the decisive step. Once the two isolated poles are excluded and no third terminal primitive pole survives, the realized primitive origin has only one admissible form left.

**Theorem 3.7.1 (Forced admissible origin theorem).**  
For the realized branch under study, the primitive origin-condition $\omega$ is one primitive condition bearing the opposition of $\mathbf 0$ and $\mathbf 1$ internally without terminal settlement. Equivalently,
$$
\mathrm{Inv}(\omega).
$$

**Status:** Proved.

**Proof.**  
We proceed in explicit elimination order.

1. By Theorem 3.6.1, the realized branch-origin $\omega$ is not identical to isolated nullity and is not identical to isolated undifferentiated totality.
2. By Theorem 3.5.2, there is no third terminal primitive pole. Any terminal flat primitive pole collapses to either $\mathbf 0$ or $\mathbf 1$.
3. Therefore the realized branch-origin cannot be any terminally settled primitive pole at all. If it were terminally settled, it would have to be one of the two isolated poles already excluded in Step 1.
4. By Section 2.5, the primitive layer contains no prior basis under which two primitive poles could begin as externally separate things. So the relevant primitive opposition cannot be realized as two already-distinct primitive objects.
5. By Proposition 3.4.1, the two poles are genuinely distinct even though both are sterile in isolation. So the manuscript is not allowed to collapse them into one indistinguishable extreme.
6. Since the realized branch-origin cannot terminate in either isolated pole, cannot be a third terminal primitive pole, and cannot externalize the poles into two already-separated primitive things, the only admissible primitive possibility left is that the distinction between the two terminal poles is borne internally by one primitive origin-condition without terminal settlement.
7. That is exactly the manuscript meaning of the primitive invariant shorthand $\mathrm{Inv}(\omega)$: one admissible primitive origin-condition stands under internally borne, non-discharged opposition of the two terminal poles.

Therefore $\mathrm{Inv}(\omega)$ holds. Unresolved opposition is not an added extra premise. It is the only primitive origin-form left after the stricter alternatives are eliminated. $\square$

**Corollary 3.7.2 (No simpler primitive survivor remains).**  
Relative to the inferential discipline of this manuscript, no simpler primitive survivor remains beyond:

1. isolated nullity,
2. isolated undifferentiated totality,
3. one primitive origin-condition bearing their unresolved internal opposition.

The first two are excluded for any realized falsifiable branch, so only the third remains admissible.

**Status:** Proved.

**Proof.**  
Theorem 3.5.2 exhausts the terminal primitive poles; Theorem 3.6.1 excludes both isolated poles as realized branch-origins; Theorem 3.7.1 identifies the only remaining admissible primitive form. $\square$

### 3.8 First non-flat articulation follows directly from the forced origin

**Theorem 3.8.1 (Breakdown of perfect flatness at the realized origin).**  
For the realized branch under study,
$$
\neg \mathrm{Flat}(\omega).
$$

**Status:** Proved.

**Proof.**  
By Theorem 3.7.1, the origin-condition $\omega$ stands under the internally borne opposition of the distinct poles. By Scope Convention 3.1.2, $\mathrm{Real}(\omega)$. PB5 therefore applies and yields $\neg \mathrm{Flat}(\omega)$. $\square$

**Corollary 3.8.2 (Differentiated articulation is present at the realized origin).**  
For the realized branch under study,
$$
\mathrm{Diff}(\omega).
$$

**Status:** Proved.

**Proof.**  
By Scope Convention 3.1.2, $\mathrm{Real}(\omega)$. By Theorem 3.8.1, $\neg \mathrm{Flat}(\omega)$. By the definition of $\mathrm{Diff}$, $\mathrm{Diff}(\omega)$ holds. $\square$

**Corollary 3.8.3 (Existential witness form for the present branch).**  
In witness form, the present branch therefore satisfies
$$
\exists x\in\mathcal C\;\big(\mathrm{Orig}(x)\wedge \mathrm{Inv}(x)\wedge \mathrm{Diff}(x)\big),
$$
with witness $x=\omega$.

**Status:** Proved.

**Proof.**  
Immediate from Scope Convention 3.1.2, Theorem 3.7.1, and Corollary 3.8.2. $\square$

### 3.9 Non-flatness does not discharge the invariant

Corollary 3.8.2 is not a discharge theorem. It does not say that the primitive burden has been solved. It says only that once the realized origin is forced to bear unresolved internal pole-opposition, perfect self-coincidence fails. This is the first non-flat articulation of the invariant, not its exhaustion.

**Status:** Proved as architectural consequence of the forced-origin derivation.

### 3.10 Apparent settlement does not equal terminal discharge

This manuscript henceforth uses the following discipline.

- An articulation may display one-sided settled appearance.
- Such appearance does **not** count as terminal resolution of the primitive invariant.

Any later theorem that uses settlement language must say explicitly whether it reaches terminal discharge or only a weaker non-terminal condition.

### 3.11 Section summary

At this stage the manuscript has:

- proved exclusion of isolated nullity,
- proved exclusion of isolated undifferentiated totality,
- proved distinctness of the poles despite shared sterility,
- proved exhaustive terminal classification at the primitive layer,
- proved that no third terminal primitive pole survives,
- proved that the realized branch-origin cannot terminate in either isolated pole,
- proved that the only admissible primitive origin left is one origin-condition bearing unresolved internal pole-opposition,
- proved that no simpler primitive survivor remains for a realized falsifiable branch,
- proved breakdown of perfect flatness at that realized origin,
- proved differentiated articulation at that realized origin,
- and kept terminal settlement distinct from terminal discharge.

---


## 4. Dependence-Ranked Articulation Chain Governed by the Invariant

### 4.1 Dependency-clean stage order

Under the AC invariant discipline, the articulation chain must now be read in dependence-ranked form:

1. one admissible origin-condition carries unresolved internal pole-opposition,
2. a lowest-resolution invariant-bearing differentiated degree after origin is admitted,
3. the question is whether that degree admits a genuinely higher-resolution differentiated degree under the undischarged primitive invariant,
4. if such a higher-resolution degree is admitted, the lower-resolution degree is no longer sufficient as the sole determination of the state and an additional internal determination is present,
5. only after that may the manuscript ask whether apartness, recursive restatement, truncation, or any later carrier-adjacent burden is earned.

This is not chronology. It is shared resolution dependency.

### 4.2 Naming disposition under the invariant

The theorem spine now uses only dependence-ranked, pre-geometric language.

- **lowest-resolution invariant-bearing differentiated degree after origin** replaces the riskier sequence-shaped wording that had accumulated in earlier passes,
- **genuinely higher-resolution differentiated degree** replaces spatial language such as “widening,”
- **additional internal determination** replaces prematurely stronger language such as apartness or ready-made plurality,
- **clarification of the lower-resolution degree** replaces any implication that a later degree carries a new invariant.

The invariant is already present at every admissible degree. A higher-resolution degree does not inherit a new invariant; it clarifies a lower-resolution degree by inhabiting the undischarged primitive invariant more articulately.

### 4.3 Lowest-resolution invariant-bearing differentiated degree after origin

**Definition 4.3.1 (Lowest-resolution invariant-bearing differentiated degree after origin).**  
At the present layer, write
$$
\mathrm{Deg}_{\min}(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x).
$$
This says only that the undischarged primitive invariant now occurs in a realizable non-flat articulation rather than in primitive undifferentiated form. It does **not** mean smoothness, derivative structure, manifold differentiability, event sequence, or causal transition.

### 4.4 Lowest-resolution positive articulation after origin is already derivable

**Theorem 4.4.1 (Lowest-resolution invariant-bearing differentiated degree after origin exists).**  
Assume PB5 together with the Section 3 origin-law derivation. Then
$$
\exists x\in\mathcal C\;\big(\mathrm{Orig}(x)\wedge \mathrm{Deg}_{\min}(x)\big).
$$

**Status:** Proved from PB5 together with the Section 3 origin-law derivation.

**Proof.**  
By Corollary 3.8.3, there exists $x$ with $\mathrm{Orig}(x)\wedge \mathrm{Inv}(x)\wedge \mathrm{Diff}(x)$. Hence $\mathrm{Deg}_{\min}(x)$ holds. Therefore such an $x$ exists. $\square$

**Corollary 4.4.2 (The lowest-resolution positive articulation after origin burden closes directly from the origin-law derivation).**  
The lowest-resolution positive articulation after origin burden is not an extra witness layer above differentiated articulation. It closes directly as the lowest-resolution invariant-bearing differentiated degree after origin.

**Status:** Proved.

**Proof.**  
Immediate from Theorem 4.4.1. $\square$

### 4.5 Why no second witness layer is retained on the root route

**Proposition 4.5.1 (The weak/strong WNF split is not a live root dependency difference).**  
On the present route, the old weak/strong WNF split is not retained as a mainline dependency split for the lowest-resolution positive articulation after origin.

**Status:** Proved as dependency-order disposition.

**Proof.**  
The lowest-resolution positive articulation after origin is already captured by $\mathrm{Deg}_{\min}(x)$, which closes by Theorem 4.4.1 directly from the origin-law derivation together with PB3 and PB5. Any stronger requirement that the lowest-resolution articulation be formalized through an additional explicit witness layer is therefore not needed to state or prove that articulation itself. Such a further requirement may matter for later burdens, but it is not on the present route. $\square$

The earlier witness language is retained only as migration crosswalk and warning against smuggling additional determination, apartness, or later-stage usability conditions into the root theorem.

### 4.6 Coarse higher-resolution-degree disposition under the invariant

The old coarse DWP slogan is not “plurality from nowhere.” It is the historical placeholder for the question that arises once the lowest-resolution degree is already earned. But the coarse form
$$
\forall x\in\mathcal C,\quad \mathrm{Deg}_{\min}(x)\Rightarrow \mathrm{Mult}(x),
$$
is too coarse. It collapses two non-equivalent claims into one line:

1. **character claim:** what a genuinely higher-resolution differentiated degree would have to imply if it is admitted; and
2. **admission claim:** whether the present package already proves that such a genuinely higher-resolution differentiated degree is admitted.

These are different burdens.

**Theorem 4.6.1 (Coarse DWP must be split).**  
The manuscript must distinguish the character of a genuinely higher-resolution differentiated degree from the admission of such a degree.

**Status:** Proved as dependency-order disposition.

**Proof.**  
A theorem that states only $\mathrm{Deg}_{\min}(x)\Rightarrow \mathrm{Mult}(x)$ says neither what makes the higher-resolution degree genuine nor whether the present package proves the existence of such a degree. The first omission is structural; the second is existential. Since these burdens can succeed or fail separately, the coarse statement conflates distinct theorem tasks and must be split. $\square$

### 4.7 Character versus admission of a higher-resolution differentiated degree

Call a **genuinely higher-resolution differentiated degree** any higher-resolution articulation of the undischarged primitive invariant that adds an internal determination rather than merely renaming the lower-resolution degree.

**Theorem 4.7.1 (Higher-Resolution Degree Character Lemma).**  
If a lowest-resolution invariant-bearing differentiated degree after origin admits a genuinely higher-resolution differentiated degree under the undischarged primitive invariant, then:

1. the lower-resolution degree is no longer sufficient as the sole determination of the state,
2. an additional internal determination is present, and
3. apartness, nodehood, metric structure, and completed boundaries still do **not** follow from this theorem alone.

**Status:** Proved.

**Proof.**  
The AC invariant discipline states that a new degree of variation yields an increase in complexity. A genuinely higher-resolution differentiated degree is therefore not a vacuous restatement of the lower-resolution degree, but a more articulated inhabitation of the undischarged primitive burden. If the lower-resolution degree remained sufficient as sole determination, no added internal determination would have been introduced, and the alleged higher-resolution degree would collapse into mere renaming of the lower one. That contradicts the assumption that the higher-resolution degree is genuine. Hence a genuine higher-resolution degree, if admitted, makes the lower-resolution degree insufficient as sole determination and introduces an additional internal determination. But this alone does not state external separation, contextual noncoincidence between distinct determinations, metricity, or any later carrier-adjacent burden. $\square$

**Corollary 4.7.2 (Clarification of the lower-resolution degree).**  
If a genuinely higher-resolution differentiated degree is admitted, then the lower-resolution degree is clarified rather than erased, and the live insufficiency is borne at the highest admitted articulation degree.

**Status:** Proved as doctrinal consequence of the invariant rule.

**Proof.**  
By Theorem 4.7.1, the lower-resolution degree is no longer sufficient as sole determination once a higher-resolution degree is admitted. So the lower-resolution degree is not cancelled; it is shown to have been only partially sufficient at its own articulation level. Since the invariant is without terminal discharged, the unresolvedness does not disappear; it is instead borne at the highest admitted articulation degree. $\square$

This proves the **character** of a genuinely higher-resolution differentiated degree. It does **not** prove the **admission** of such a degree.

**HRDAP — Higher-Resolution Degree Admission Principle**  
At least one origin-bearing lowest-resolution invariant-bearing differentiated degree after origin admits a genuinely higher-resolution differentiated degree under the undischarged primitive invariant.

**Status:** Requires one new explicit principle.

**Theorem 4.7.3 (Admission of a genuinely higher-resolution differentiated degree does not yet follow).**  
The current manuscript does **not** prove HRDAP from PB1–PB5 together with the Section 3 forced-origin derivation.

**Status:** Proved as a no-go.

**Proof.**  
PB1–PB5 together with the Section 3 forced-origin derivation yield at least one origin-bearing lowest-resolution invariant-bearing differentiated degree after origin by Theorem 4.4.1. They also preserve terminal non-discharge of the invariant and the distinction between apparent settlement and terminal resolution. But they do not yet specify that any such degree admits a genuinely higher-resolution differentiated degree rather than remaining only the currently admitted degree. To infer such admission directly would require an extra admission principle or would silently borrow recursive-restatement burden from a later stage. Therefore HRDAP does not follow from the present package alone. $\square$

### 4.7.4 HRDAP semantic budget and unlocked definitions

The live HRDAP burden is now protected by an explicit semantic-budget ledger. This is theorem-hygiene infrastructure, not a new structural theorem.

**Current semantic budget inside HRDAP scope (legal before HRDAP closes):**

- origin and origin-bearing realizability,
- flat / non-flat,
- differentiated articulation,
- invariant-bearing articulation,
- lowest-resolution degree after origin,
- a schematic higher-resolution differentiated degree target,
- lower-resolution degree not sufficient as sole determination,
- additional internal determination only as a **character consequence if admission occurs**,
- dependence order,
- apparent settlement / terminal non-discharge.

**Blocked imports inside HRDAP scope:**

- apartness,
- contextual noncoincidence as if already closed,
- nodehood,
- branch / tree / graph structure,
- metricity,
- boundary completion,
- carrier-like support,
- recursive refinement as though already active,
- geometric dimension language,
- any unearned external relation vocabulary.

**Unlocked definitions if HRDAP closes:**

- an actually admitted higher-resolution differentiated degree,
- stronger use of additional internal determination,
- contextual noncoincidence as a live next burden,
- apartness as a downstream candidate rather than a blocked notion,
- a cleaner attack surface for RRP.

These unlocked notions are not licensed until HRDAP is actually closed.

**Proposition 4.7.4 (HRDAP may not be proved by unlocked semantics).**  
Inside the present manuscript, HRDAP may not be argued by using any semantic notion listed above as blocked or unlocked-only.

**Status:** Proved as theorem-hygiene discipline.

**Proof.**  
The present burden is precisely whether a genuinely higher-resolution differentiated degree is admitted from the currently earned package. If the proof were allowed to use apartness, contextual noncoincidence, nodehood, metricity, recursive refinement, carrier-like support, or any other notion that becomes meaningful only after HRDAP closes, then the argument would assume the conclusion-stage semantic environment in order to prove entry into that environment. That would make the theorem circular by semantic overreach rather than by explicit formal steps. Therefore the HRDAP scope must remain bounded by the current semantic budget, and blocked or unlocked-only meanings may not be used to prove HRDAP. $\square$

So the live articulation bottleneck is now exact:

- **HRDCL is proved** (character of a genuinely higher-resolution differentiated degree),
- **HRDAP is open** (admission of a genuinely higher-resolution differentiated degree),
- and additional internal determination remains unclosed only because HRDAP is unproved.

**Theorem 4.7.5 (Exhaustive completeness of the lowest-resolution degree does not follow).**  
The current manuscript does **not** prove that an origin-bearing lowest-resolution invariant-bearing differentiated degree after origin is exhaustively complete as the sole articulation of the undischarged primitive invariant.

**Status:** Proved as a no-go.

**Proof.**  
The present package proves only that at least one origin-bearing lowest-resolution invariant-bearing differentiated degree after origin exists from the origin-law derivation together with PB3 and PB5. It also preserves the root rule that the primitive invariant is without terminal discharged and distinguishes apparent settlement from terminal resolution. No theorem in the current manuscript shows that the lowest-resolution degree exhausts the admissible articulation of that invariant, and HRDAP, RRP, and WEP all remain open. Therefore exhaustive completeness of the lowest-resolution degree does not follow from the present package. $\square$

**Proposition 4.7.6 (Exact live fork).**  
Under the current package, further progress beyond the lowest-resolution degree must take one of two explicit forms:

1. close **HRDAP** under the current semantic budget, or  
2. introduce and justify an explicit obstruction principle or no-go theorem showing why a genuinely higher-resolution differentiated degree is not admitted.

Until one of these is supplied, the manuscript may not treat the lowest-resolution degree as exhaustively complete and may not treat a genuinely higher-resolution differentiated degree as admitted.

**Status:** Proved as dependency-order disposition.

**Proof.**  
By Theorem 4.7.3, admission of a genuinely higher-resolution differentiated degree does not yet follow from the present package. By Theorem 4.7.5, exhaustive completeness of the lowest-resolution degree also does not follow. Therefore the manuscript is positioned between unproved admission and unproved completeness. The only theorem-legible ways forward are either to close admission or to state and justify an explicit obstruction to admission. Any attempt to skip that fork would either assume admission without proof or assume exhaustive completeness without proof. $\square$

### 4.8 Apartness remains blocked behind a higher-resolution differentiated degree

**Theorem 4.8.1.**  
Apartness is blocked until admission of a genuinely higher-resolution differentiated degree closes and contextual noncoincidence is actually earned.

**Status:** Proved.

**Proof.**  
Apartness requires more than the statement that a lower degree is no longer sufficient as sole determination. It requires a theorem-bearing noncoincidence relation between determinations. The Higher-Resolution Degree Character Lemma proves only what a genuinely higher-resolution differentiated degree would imply if it is admitted. Since HRDAP is still open, and since contextual noncoincidence and apartness remain explicitly blocked by the HRDAP semantic-budget ledger until admission closes, the manuscript has no theorem yet yielding an actually admitted higher-resolution degree and therefore no theorem yet yielding contextual apartness. $\square$

If HRDAP later closes, apartness may be defined contextually rather than primitively.

### 4.9 RRP recast under the invariant

RRP is not a later optional reactivation principle. It is the claim that if a lowest-resolution degree or higher-resolution degree still leaves the invariant non-exhaustive, the undischarged primitive invariant must be restated at higher resolution.

**Theorem 4.9.1 (Recursive refinement does not yet follow).**  
The current manuscript does **not** prove recursive refinement from PB1–PB5 together with the Section 3 forced-origin derivation, even once the lowest-resolution invariant-bearing differentiated degree after origin is in hand.

**Status:** Proved as a no-go.

**Proof.**  
PB1–PB5 together with the Section 3 forced-origin derivation, plus the lowest-resolution invariant-bearing differentiated degree after origin, yield an articulated degree of invariant carriage, but they do not yet specify when that articulation remains non-exhaustive in a way that requires the invariant to be restated at higher resolution. The Higher-Resolution Degree Character Lemma does not solve this, because it concerns only the form a genuinely higher-resolution differentiated degree would have, not whether higher-resolution restatement is forced. Therefore recursive refinement does not follow. $\square$

**RRP — Recursive Reapplication Principle**  
If a realizable invariant-bearing articulation is non-exhaustive relative to the undischarged primitive invariant, then a further articulated condition is required that again stands under that invariant.

RRP is thus not a fresh source. It is the higher-resolution restatement of that same one.

**Status:** Requires one new explicit principle.

### 4.10 Dependence order, not time

**Proposition 4.10.1.**  
Any order obtained from repeated articulation of the invariant is an order of dependence, not yet an order of physical time.

**Status:** Proved.

**Proof.**  
The present root package contains no time parameter, no dynamics, no event sequence, no continuation law, and no dissipation law. Therefore any admissible order here can only mean that one burden must be settled before another burden is licensed in the dependency sense, not in chronological time. $\square$

### 4.11 Repeated dependence is not yet constructive

Repeated dependence is not primitive ancestry in this rewrite. It is repeated dependence/refinement under the undischarged primitive invariant.

**Status:** Blocked.

What is proved is only the frame discipline: any later nested dependence must, if closed, be derived from repeated articulation of one invariant burden rather than from primitive tree language.

### 4.12 Exact active bite under the correct frame

The active bite is no longer best described as “find an isolated module.”

The active bite is now sharper:

1. keep the lowest-resolution invariant-bearing differentiated degree after origin closed without inflating it into apartness or ready-made plurality,
2. decide whether any lowest-resolution degree admits a genuinely higher-resolution differentiated degree and, if so, under what exact admission burden,
3. decide when a non-exhaustive invariant-bearing articulation forces higher-resolution restatement via RRP,
4. only after that ask the later truncation and carrier-family questions.

That is the first honest dependence-ranked chain of the manuscript.

### 4.13 Contamination self-check for the articulation chain

At the present stage, the three top risks are:

1. **externalizing the poles** so the origin is misread as two primitive things;
2. **treating the lowest-resolution invariant-bearing differentiated degree after origin as already apartness or ready-made plurality**, which would smuggle later burdens shut;
3. **treating RRP as optional reactivation** rather than as higher-resolution restatement of the undischarged primitive invariant,
4. **proving HRDAP by semantic scope leakage** through blocked or unlocked-only meanings,
5. **equating non-completeness of the lowest-resolution degree with actual admission of a higher-resolution degree**.

These are now the main frame-level failure modes, not just low-level notation accidents.


## 5. Time, Continuation, Arrow, and Causality

### 5.1 Dependence order

Dependence order is the earliest allowable order notion in CF000. It means only:

- this burden must be settled before that later structure may be licensed.

It does **not** mean elapsed time, reversible update, irreversible history, or causal propagation.

**Status:** Proved.

### 5.2 Reversible continuation

A lawful reversible continuation regime cannot honestly appear until a later support or pre-carrier layer exists. Before that, there is nothing yet on which a lawful continuation could act.

**Status:** Proved as staging discipline.

### 5.3 Irreversible arrow

An irreversible arrow belongs later than dependence order and later than reversible continuation. It should enter only with a genuine dissipation or entropy-producing burden, not with root asymmetry alone.

**Status:** Proved as staging discipline.

### 5.4 Causality

Causality is later than dependence order and likely later than mere continuation. It requires at minimum some further discipline not yet earned here. Therefore causality is forbidden from the primitive layer.

**Status:** Proved as staging discipline.

---

## 6. Relationship to H000, A8, CF00, and Later Canon

### 6.1 H000

H000 remains the proposal-grade hypothesis line that first stated the primitive bifurcation architecture in compact form.

**Status:** Alignment only.

### 6.2 A8

A8 is not the primitive generator in this rewrite. It is a later-regime candidate expression of the undischarged primitive invariant burden under added burden: repeated articulation, braking, truncation, and interface concentration.

**Status:** Proved as reclassification discipline.

### 6.3 CF00

CF00 remains downstream of any legitimate pre-carrier and pre-differential closure achieved here. The present draft still does not license the carrier bridge.

### 6.4 Later dual split

The present root architecture suggests a plausible deep ancestor of the later conservative/dissipative split:

- one aspect opens articulation under unresolved opposition,
- another aspect closes or stabilizes in a merely partial way without terminal discharge.

This is structurally suggestive, but it is **not** a derivation of QGT or $J\oplus M$.

**Status:** Not proved.

---


## 7. HRDAP Exact-Fork Disposition

### 7.1 Package verdict

The theorem spine is clean enough that the dominant remaining risk is no longer wording sludge in the abstract. The dominant remaining risk is semantic scope leakage inside HRDAP.

### 7.2 What this pass changes

This pass makes four narrow but important changes.

- It keeps the primitive bifurcation invariant as root basis.
- It keeps closure of the lowest-resolution positive articulation after origin.
- It keeps the valid character/admission split.
- It recasts that split entirely in pre-geometric, dependence-ranked language.

### 7.3 What this pass does not change

This pass does not reopen the one-origin invariant frame, does not reopen WNF-style witness bookkeeping, does not prove HRDAP, does not prove apartness, does not advance RRP, and does not close later carrier-family notions, coherence, pre-carrier support, or differentiability.

### 7.4 Net disposition outcome

- The theorem structure is tightened at the root and otherwise unchanged.
- The live bite remains **HRDAP**.
- The proof environment is now explicitly scope-bounded.
- Semantics that would only become meaningful after HRDAP closes are deferred rather than used illicitly inside the HRDAP argument.
- Contextual noncoincidence, apartness, and a cleaner RRP attack are now named as **unlocked only after HRDAP closure**.

### 7.5 Interpretation

This pass does not add new structural machinery. It turns the HRDAP dependency ladder into an operational proof guardrail by stating what semantics are legal now, which are blocked now, and which only become live if HRDAP closes.

The naming-cleanup pass lands as a dependency-safe recast:

- the lowest-resolution positive articulation after origin remains closed,
- the character/admission split remains valid,
- the character side is now stated as **additional internal determination** rather than spatial widening,
- the admission side remains open as **HRDAP**,
- and the theorem ladder is cleaner once spatial and sequence-heavy packaging are removed.

## 8. Remaining Burdens Required for Actual Closure

To move this draft toward real CF closure, the next burdens are now ordered as follows.

2. **HRDAP — admission of a genuinely higher-resolution differentiated degree**  
   Decide whether at least one origin-bearing lowest-resolution invariant-bearing differentiated degree after origin admits a genuinely higher-resolution differentiated degree under the undischarged primitive invariant. If not, the manuscript must supply an explicit obstruction/no-go principle rather than quietly treating the lowest-resolution degree as exhaustively complete.

3. **Additional internal determination after HRDAP**  
   Once HRDAP closes, the lower-resolution degree is no longer sufficient as sole determination and an additional internal determination is present by HRDCL.

4. **Apartness after contextual noncoincidence**  
   Only after an actually admitted higher-resolution degree exists may the manuscript ask whether contextual noncoincidence closes strongly enough for apartness.

5. **RRP — higher-resolution restatement of the undischarged primitive invariant**  
   Prove or admit when non-exhaustive invariant-bearing articulation forces further articulation.

6. **WEP — well-founded exhaustion / truncation burden**  
   Decide whether repeated articulation yields frontier-like closure or requires one additional principle.

7. **First later carrier-family notion**  
   Identify exactly when a later carrier-family notion first becomes earned rather than intuitive leakage.

8. **Later coherence principle**  
   If later carrier-family closure ever occurs, isolate one minimal coherence principle for any pre-carrier bridge.

9. **Differentiability status**  
   Keep this honest: either open, or name the exact burden.

10. **Later dual split**  
    Any bridge from this root to a conservative/dissipative dual structure remains downstream and unproved.


## 9. Theorem Inventory (compact)

### Proved
- Nullity exclusion
- Undifferentiated totality exclusion
- Pole non-identity with shared sterility verdict
- Exhaustive terminal classification at the primitive layer
- Withdrawal of the earlier artificial underdetermination bookkeeping move
- Forced admissible origin theorem
- No simpler primitive survivor remains
- Breakdown of perfect flatness from PB5 and the origin-law derivation
- Existence of differentiated articulation from PB5 and the origin-law derivation
- Lowest-resolution invariant-bearing differentiated degree after origin exists from PB5 and the origin-law derivation
- The lowest-resolution positive articulation after origin burden closes directly as the lowest-resolution invariant-bearing differentiated degree after origin from the origin-law derivation
- Non-flatness does not discharge the invariant
- Coarse DWP must be split into character versus admission
- The **Higher-Resolution Degree Character Lemma**
- Admission of a genuinely higher-resolution differentiated degree does not follow from PB1–PB5 together with the Section 3 forced-origin derivation
- Apartness is blocked until admission of a genuinely higher-resolution differentiated degree closes
- Recursive refinement does not follow from PB1–PB5 together with the Section 3 forced-origin derivation and the lowest-resolution invariant-bearing differentiated degree after origin
- Dependence order is earlier than time
- Reversible continuation is staged later than dependence order
- Irreversible arrow is staged later than root asymmetry
- Causality is forbidden at the primitive layer
- A8 is reclassified as late-regime expression, not primitive generator

### Requires one new explicit principle
- Admission of a genuinely higher-resolution differentiated degree via HRDAP
- Recursive higher-resolution restatement via RRP
- Truncation via WEP

### Not proved
- That HRDAP is derivable rather than added
- That RRP is derivable rather than added
- That WEP is derivable rather than added
- Any constructive later carrier-family notion
- Any pre-carrier bridge
- Any differentiability result in the later geometric sense
- Any derivation of the later conservative/dissipative split

### Blocked
- Actual contextual apartness before HRDAP closes
- Repeated dependence as constructive result before RRP closes
- Boundary/domain-wall-type structure before truncation closes
- First later carrier-family notion before later burdens close
- Pre-carrier patchability before later carrier-family closure / coherence closure

## 10. Anti-Smuggling Note

The present draft forbids the following contamination moves:

1. treating the two poles as though they begin externally separate,
2. treating the lowest-resolution invariant-bearing differentiated degree after origin as already apartness,
3. treating a genuinely higher-resolution differentiated degree as though it were already geometric dimension,
4. treating additional internal determination as though it were already metric separation,
5. treating apparent settlement as though it were terminal discharge,
6. borrowing time, causality, graph, tree, carrier, or completed boundaries to close a root burden,
7. treating non-completeness of the lowest-resolution degree as though it were already proof of a genuinely higher-resolution admitted degree.

## Appendix A. Primitive Block

Primitive package of the current draft:

- distinguished poles $\mathbf 0$ and $\mathbf 1$,
- predicates $\mathrm{Orig}(x),\mathrm{Ster}(x),\mathrm{Flat}(x),\mathrm{NV}(x),\mathrm{Real}(x)$,
- relation $\mathrm{Opp}(x,y)$,
- derived shorthand $\mathrm{Inv}(x)$,
- root laws PB1–PB5,
- explicit added principles only where named.

Primitive root laws used in the current draft:

$$
\mathbf 0\neq \mathbf 1,
$$

$$
\mathrm{Ster}(\mathbf 0)\wedge \mathrm{Ster}(\mathbf 1),
$$

$$
\mathrm{Opp}(\mathbf 0,\mathbf 1),
$$

$$
\forall x\in\mathcal C,\quad \mathrm{Real}(x)\Rightarrow \big(\mathrm{NV}(x)\wedge x\neq \mathbf 0 \wedge x\neq \mathbf 1\big),
$$

$$
\forall x\in\mathcal C,\quad \big(\mathrm{Real}(x)\wedge \mathrm{Opp}(\mathbf 0,\mathbf 1)\big)\Rightarrow \neg \mathrm{Flat}(x).
$$

Named added principles introduced by this draft:

- **HRDAP** — Higher-Resolution Degree Admission Principle
- **RRP** — Recursive Reapplication Principle
- **WEP** — Well-founded Exhaustion Principle

No separate detachable origin-existence premise remains on the live dependency spine.

Migration crosswalk only:

- the weak/strong **WNF** split is retained only as historical theorem-hygiene cleanup and is not on the main dependency spine,
- the coarse **DWP** slogan is retained only as migration shorthand and is resolved into **HRDCL + HRDAP**.

## Appendix B. Articulation Block

First derived shorthand:
$$
\mathrm{Diff}(x):=\mathrm{Real}(x)\wedge \neg \mathrm{Flat}(x)
$$

Lowest-resolution positive articulation after origin:
$$
\mathrm{Deg}_{\min}(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x)
$$

Architectural shorthand:
- $\mathrm{Inv}(x)$ — one admissible primitive origin-condition bears internal pole-opposition without terminal discharge.

Higher-resolution-degree split:
- **HRDCL** — if a genuinely higher-resolution differentiated degree is admitted, the lower-resolution degree is no longer sufficient as sole determination and an additional internal determination is present.
- **HRDAP** — at least one origin-bearing lowest-resolution invariant-bearing differentiated degree after origin admits a genuinely higher-resolution differentiated degree.

Target later notions, not yet closed:

- contextual apartness,
- recursive refinement,
- repeated dependence,
- qualitative braking,
- truncation,
- boundary-type structure,
- coherence,
- pre-carrier support,
- differentiability bridge.

Migration warning:

- the weak non-self-coincidence language is absorbed into differentiated articulation,
- the strong witness-lift language is not retained as a root bottleneck,
- the phrase **"distinction of change"** is retired from the theorem spine in favor of **lowest-resolution invariant-bearing differentiated degree after origin**,
- spatial wording is retired from the theorem spine in favor of **higher-resolution differentiated degree** and **additional internal determination**.

## Appendix C. Acceptance Status

This document is **not** yet a Completed Formalism for the full CF000 burden.

It is an exact-fork / non-finality guardrail pass that:

- keeps the primitive bifurcation frame frozen as baseline,
- preserves closure of the lowest-resolution positive articulation after origin,
- preserves the valid character/admission split,
- retires spatial and sequence-heavy theorem-spine wording,
- keeps RRP downstream,
- states explicitly that the lowest-resolution degree is not licensed as exhaustively complete,
- and names the remaining exact burdens without pretending closure.

The next serious pass should hostile-audit the in-body elimination proof of the admissible primitive origin, and then attack **HRDAP** as the exact admission burden for a genuinely higher-resolution differentiated degree. If that attack fails, the manuscript should not silently default to completion at the lower degree; it should state an explicit obstruction/no-go principle.
