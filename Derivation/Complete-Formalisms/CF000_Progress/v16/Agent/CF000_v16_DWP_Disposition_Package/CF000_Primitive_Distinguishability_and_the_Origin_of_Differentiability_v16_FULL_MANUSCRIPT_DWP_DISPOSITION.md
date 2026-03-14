# CF000: Complete Formalism — Primitive Distinguishability and the Origin of Differentiability in VDM

Date: 2026-03-14  
Status: Review Draft — v16 DWP disposition integrated  
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

## Governing Rule of This Document

This CF is the root written source of truth for the pre-differential layer of this branch of VDM.

The controlling claim of this version is the **single fundamental primitive bifurcation law**:

> the only logically admissible primitive origin is one primitive condition whose content carries two mutually unreconcilable terminal poles, absolute nullity and absolute undifferentiated totality; neither pole can globally win without collapse; therefore unresolved pole-opposition is the permanent invariant of the system, later differentiations do not discharge it, and all later articulation is a transformed expression of that same undischarged burden.

This rule is not used here as a loose metaphor, a one-time split, or a dynamical picture. It is the manuscript spine. The paper must therefore stop reading as a sequence of mostly separate burden modules and instead show, stage by stage, how the first invariant-bearing differentiated degree, the v16 widening split, and RRP are only increasingly articulated forms of one still-live primitive invariant.

### Consequence of this rule

For this document:

- the primitive tension must be treated as **derived from the only admissible origin**, not inserted as an extra unexplained assumption,
- the origin must be treated as **one primitive condition**, not as two externally separated things,
- the two poles must be treated as **logically distinct but primitively undifferentiated in being**,
- there is initially **no prior space, time, location, direction, metric, locality, or value framework** in which the poles could stand apart,
- local stability may occur, but only as **local settlement**; it may never be described as global resolution,
- any later articulation must be tested as an expression of the same invariant, not as a fresh independent engine.

---

## Relationship to Canon and External Documents

Canon documents, proposal artifacts, hypothesis notes, and later CFs may be cited for provenance, naming, alignment, and program integration. They may not be used to outsource root derivation that belongs here.

For the present manuscript:

- **H000** captures the proposal-grade primitive bifurcation hypothesis,
- the doctrinal note on the **single fundamental primitive bifurcation law** records the intended root engine in compact form,
- **A8** is not the primitive generator here; it is a later-regime candidate expression of the same invariant burden under additional structure,
- **CF00** remains downstream of any legitimate pre-carrier and pre-differential closure obtained here.

No later canon object — manifold, chart, overlap class, support family, QGT, or $J\oplus M$ split — may be used to prepay burden at the root layer.

---

## Relationship to the CFN

No paired CFN is required for the present stage because the present burden is still theorem-hygiene and dependency-order work rather than executable realization. If a later CFN is built, it may only instantiate, test, or illustrate constructions already formalized here. It may not supply missing root logic.

---


## Executive Summary

v13 remains frozen as the governing frame of CF000. v15 correctly closed the first positive articulation once sharpened origin-scoped existence was admitted, but it left two issues alive: its preferred phrase **"distinction of change"** still risked temporal or causal over-reading, and its coarse statement of **DWP** still compressed two different questions into one slogan. The v16 pass keeps the v13/v15 frame and performs only the narrower disposition required by the audit package.

The naming correction is straightforward. The first positive articulation is now stated as the **first invariant-bearing differentiated degree**. Formally this is still the first-layer shorthand
$$
\mathrm{Deg}_1(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x),
$$
but the manuscript now refuses to describe that first degree as a “change” in the theorem spine, because that wording can suggest time, event sequence, or causal transition. The relevant degree is a primitive articulated degree of invariant carriage, not later smoothness and not a temporal episode.

The v16 mathematical result is **Outcome C** for DWP. The old coarse DWP claim was too blunt. It conflated:

1. the **character** of genuine widening, and
2. the **availability** of genuine widening.

These are not the same burden.

What v16 proves is the **Widening Character Lemma**: if a first invariant-bearing differentiated degree is genuinely widened under the same unresolved invariant, then that widened articulation is already plurality-bearing in the weak internal sense of carrying more than one internally distinct determination. Otherwise no new degree of variation would have been introduced, and the alleged widening would collapse into mere restatement of the first degree. What v16 does **not** prove is that such genuine widening actually occurs from the present package alone. That remaining burden is isolated as the **Widening Availability Principle (WAP)**.

The dependency verdict is therefore sharper than v15. **BEP remains off the first-articulation critical path. E1 remains the correct explicit origin-scoped existence premise. The first positive articulation still closes directly once E1 is admitted. But coarse DWP is retired from the theorem spine and split into proved character plus open availability.** Multiplicity is therefore no longer blocked because “widening” is undefined; it is blocked because the existence of widening is not yet proved. Apartness and RRP remain parked downstream.

Principal deliverables of this CF in v16:

- v13 invariant frame preserved without reopening the architecture,
- v15 first positive articulation preserved but renamed more safely as the **first invariant-bearing differentiated degree**,
- retirement of the risky theorem-spine phrase **"distinction of change"**,
- proof of the **Widening Character Lemma**,
- isolation of **WAP** as the exact remaining plurality-availability burden,
- explicit verdict that **BEP is not on the first-articulation critical path**,
- retention of sharpened **E1** as the correct existence premise,
- downstream parking of apartness and RRP under the corrected widening split,
- updated theorem inventory, open-burden inventory, migration delta, contamination audit, and appendix crosswalk.

## Read Me First: Writing Rules for This CF

1. This document must be self-contained at the level required to understand, test, and reuse the root formalism.
2. Every theorem-bearing section must expose its proof burden directly.
3. The primitive bifurcation invariant is the controlling frame; no section may silently revert to a modular burden stack that forgets the global invariant.
4. No section may use words such as “emerges,” “reactivates,” “propagates,” or “branches” without specifying exactly what is proved, what is added, and what remains blocked.
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

CF00 begins with a differentiable carrier $\mathcal M$ and lawful local variation on it. CF000 exists because that is already too late for an absolute root account.

The root question of this document is:

> What is the earliest admissible primitive law from which distinguishability, recursive articulation, and eventually carrier-like structure could be earned without primitive geometry, metric, locality, time, causality, valuation, parameterization, or differentiability?

### 1.2 Rewrite stance

This rewrite adopts the following stance.

1. The old v10 staircase is retained only as failure-audit material.
2. The v12 pass is retained as contamination cleanup, not as final governing architecture.
3. The present manuscript is rebuilt so that the primitive unresolved pole-opposition is the permanent invariant of the whole system.
4. The first invariant-bearing differentiated degree, widening, and RRP must appear as downstream expressions of that invariant, not as mostly separate modules.
5. No graph, tree, branch map, frontier object, locality language, or carrier language may appear before it is honestly earned.

### 1.3 Primitive versus forbidden structure

#### Primitive in this rewrite

The primitive package of the present draft contains only:

- two distinguished terminal pole marks,
- their non-identity,
- their sterility for realized differentiated structure,
- their opposition,
- an origin-candidate predicate,
- a non-vacuousness predicate,
- a realizability predicate,
- a flatness predicate,
- and the governing root law that realizable origin under unresolved pole-opposition cannot remain perfectly self-coincident.

#### Forbidden as primitive

The following are forbidden at root level:

- primitive bearer multiplicity $(\mathcal B,\#)$,
- nodes, edges, graphs, trees, branch maps, ancestry, depth, frontier, sectors,
- attenuation maps, weights, energies, valuations, metrics, or measures,
- time parameter, event sequence, propagation, causality, or irreversible arrow,
- locality, neighborhoods, covers, overlaps, patch maps, or chart language,
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

> if a statement about widening or RRP is written in a way that makes it look like an independent engine rather than a further articulation of the same invariant burden, the statement is frame-contaminated even if its low-level wording is careful.

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
| Absolute nullity | complete realized absence | distinguished pole mark $\mathbf 0$ | not the empty set; not an empty region; not a vacuum in prior space | Primitive |
| Absolute undifferentiated totality | complete homogeneous one-ness without internal noncoincidence | distinguished pole mark $\mathbf 1$ | not “one object” inside prior plurality; not a constant field on a background | Primitive |
| Origin candidate | candidate primitive condition for a realized branch | predicate $\mathrm{Orig}(x)$ on $\mathcal C$ | does not assume uniqueness, time, geometry, or support structure | Primitive |
| Sterile | cannot support realized differentiated structure while remaining what it is | predicate $\mathrm{Ster}(x)$ | does not automatically mean flat; does not assume dynamics | Primitive |
| Flat | contains no realized internal noncoincidence by which differentiated structure could be sustained | predicate $\mathrm{Flat}(x)$ | does not assume plurality, graph structure, locality, or metric sameness | Primitive |
| Non-vacuous | not complete realized absence in the root sense | predicate $\mathrm{NV}(x)$ | does not assume multiplicity or persistence | Primitive |
| Realizable | admissible as a non-vacuous realized branch-condition | predicate $\mathrm{Real}(x)$ | does not yet mean temporal persistence or dynamical stability | Primitive |
| Opposition | non-identity of the two terminal poles together with their shared sterility verdict | predicate $\mathrm{Opp}(x,y)$ | does not assume external separation, interaction law, or dynamics | Primitive |
| Primitive bifurcation invariant | one primitive origin-condition carries unresolved pole-opposition internally; it is never globally discharged | schematic shorthand $\mathrm{Inv}(x)$ | does not assume two externally situated things; does not assume time, locality, or graph structure | Governing derived shorthand |
| Local settlement | a local articulation behaves as if one pole has locally won, without global discharge of the invariant | schematic shorthand $\mathrm{LocSet}(x)$ | does not mean final resolution of the system | Derived target |
| Differentiated articulation | realizable condition that is not flat | $\mathrm{Diff}(x):=\mathrm{Real}(x)\wedge 
eg \mathrm{Flat}(x)$ | does not assume multiplicity, apartness, locality, or carrier structure | Derived |
| First invariant-bearing differentiated degree | the same invariant is now carried non-flatly rather than in primitive undifferentiated form | first-layer shorthand $\mathrm{Deg}_1(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x)$ | does not mean smoothness, charts, or manifold differentiability; does not mean event sequence or causality | Derived first positive articulation |
| Genuine widening | stronger articulation of the same invariant that introduces a new degree of variation rather than merely renaming the first degree | schematic notion used in theorem statements | does not yet assume apartness, locality, metric structure, or time | Derived target notion |
| Multiplicity | one widened articulation carries more than one internally distinct determination of the same invariant | provisional $\mathrm{Mult}(x)$ | does not assume primitive nodehood or metric separation | Open target |
| WCL | if genuine widening occurs, it is plurality-bearing | theorem-level result, not primitive law | does not assert that widening exists | Proved theorem |
| WAP | at least one origin-bearing first-degree articulation admits genuine widening under the same invariant | widening availability principle | does not define apartness or recursion | Requires one new explicit principle |
| Recursive refinement | locally unsettled articulation of the invariant reappears at higher resolution | provisional $\mathrm{Ref}(x)$ | does not assume trees, ancestry, time, or causality | Open target |
| RRP | if an invariant-bearing articulation remains locally unsettled, the same invariant must be restated at higher resolution | schematic reapplication principle | does not mean optional later reactivation | Open principle |
| Dependence order | burden order: what must be settled before what may be licensed | provisional relation $\prec_d$ | not clock time; not irreversible history; not causal propagation | Derived target |


### 2.3 Definitions table audit note

The table enforces seven distinctions the manuscript may not blur.

1. **Flatness** is an internal structural condition.
2. **Sterility** is a branch-level incapacity verdict.
3. **Differentiated articulation** is the first negative articulation of the invariant.
4. **The first invariant-bearing differentiated degree** is the first positive articulation and does **not** yet imply multiplicity.
5. **Genuine widening** is stronger than the first degree and must be kept distinct from mere restatement.
6. **Multiplicity** is stronger than the first degree and remains downstream behind widening availability.
7. **Recursive refinement** is stronger still and remains downstream behind RRP.

The table also separates **non-vacuousness** from **realizability**, separates the **first invariant-bearing differentiated degree** from smoothness in the later geometric sense, and separates **local settlement** from **global resolution**.

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

**PB5. Anti-flatness under unresolved pole-opposition**
$$
\forall x\in\mathcal C,\quad \big(\mathrm{Real}(x)\wedge \mathrm{Opp}(\mathbf 0,\mathbf 1)\big)\Rightarrow \neg \mathrm{Flat}(x)
$$

### 2.5 One-origin and no-prior-framework discipline

The manuscript adopts the following root discipline.

- There is initially no prior space, time, location, direction, metric, locality, or value framework in which the two poles could stand apart.
- Therefore the poles may not be read as two externally separated primitive things.
- Any admissible primitive origin must be read as **one primitive condition** carrying the opposition internally.

This is a governing discipline of the rewrite. It is not permission to smuggle in an unearned mediating substance.

### 2.6 Derived shorthand for the invariant

When convenient, write $\mathrm{Inv}(x)$ for the following schematic situation:

- $x$ is a realizable origin-condition,
- $x$ does not coincide with either isolated pole,
- the non-identical sterile poles remain opposed,
- that opposition is internal to the one origin-condition,
- and it is not globally discharged.

This shorthand is architectural. It does not replace proof burden.

### 2.7 First derived notion

Define
$$
\mathrm{Diff}(x) := \mathrm{Real}(x)\wedge \neg \mathrm{Flat}(x).
$$

This is the first negative articulation of the invariant. In v14 it is also recognized as the weak non-self-coincidence layer. What remains open is only the stronger witness-lift burden.

### 2.8 Status of the primitive package

**Proved or stipulated at the present layer:**

- symbolic pole distinction,
- pole sterility,
- pole opposition,
- non-vacuousness / realizability separation,
- flatness / sterility distinction,
- anti-flatness under unresolved pole-opposition.

**Not proved at the present layer:**

- that the two poles exhaust every admissible flat sterile origin candidate,
- that realizable conditions actually exist,
- that anti-flatness already carries a positive witness,
- that positive witness already yields plurality.

---

## 3. Foundational Construction: Forced Origin Architecture

### 3.1 Origin candidate

**Definition 3.1.1.**  
An **origin candidate** is any $x\in\mathcal C$ such that $\mathrm{Orig}(x)$ holds.

This says only that $x$ is being tested as a candidate root condition for a realized branch. It does not yet say that $x$ is realizable, unique, temporal, geometric, or already articulated.

### 3.2 Nullity exclusion

**Theorem 3.2.1 (Nullity exclusion).**  
Absolute nullity is not a viable realized root for a falsifiable law-bearing branch.

**Status:** Proved.

**Proof.**  
A falsifiable law-bearing branch must support at least the distinction between admissible and inadmissible structure and between realized and unrealized burden. Absolute nullity supports no realized content and no realized distinction. Therefore it cannot serve as the realized root of the present branch. $\square$

### 3.3 Undifferentiated totality exclusion

**Theorem 3.3.1 (Undifferentiated totality exclusion).**  
Absolute undifferentiated totality is not a viable realized root for a falsifiable law-bearing branch.

**Status:** Proved.

**Proof.**  
A falsifiable law-bearing branch requires some realized noncoincidence by which one admissible condition can fail to coincide with another or with itself in a structurally relevant way. Absolute undifferentiated totality contains no internal noncoincidence and therefore cannot sustain differentiated realized structure. Hence it cannot serve as the realized root of the present branch. $\square$

### 3.4 Shared sterility does not collapse the poles

**Proposition 3.4.1.**  
The poles $\mathbf 0$ and $\mathbf 1$ are not identical even though both are sterile for the present branch.

**Status:** Proved.

**Proof.**  
By PB1, $\mathbf 0\neq\mathbf 1$. By PB2, both are sterile. Distinctness and shared sterility therefore coexist. $\square$

### 3.5 Why unresolved opposition is derived rather than assumed

The manuscript now makes the following architectural claim explicit.

- Isolated nullity is excluded.
- Isolated undifferentiated totality is excluded.
- The two excluded poles are distinct.
- The primitive layer contains no prior external framework in which they could stand apart as two already-separated things.
- Therefore, if a realizable primitive origin exists at all, the only admissible reading is not that one pole wins, but that one primitive condition carries their opposition internally.

This is the reason the primitive tension is treated here as **derived from the only admissible origin** rather than inserted as a separate unexplained assumption.

**Status:** Partially proved, partially conditional.

What is proved are the exclusion theorems and the pole distinction. What remains conditional is the exhaustive inference that these are the only terminal origin possibilities. That is the role of BEP below.

### 3.6 Flat-origin bipolar classification: failure result

**Target theorem.** Every admissible flat sterile origin candidate collapses into exactly one of the two distinguished pole classes.

**Status:** Not proved.

**Theorem 3.6.1 (Flat-origin bipolar classification does not follow from PB1–PB5).**  
The present primitive package does **not** prove that every admissible flat sterile origin candidate is identical to $\mathbf 0$ or $\mathbf 1$.

**Status:** Proved.

**Proof.**  
PB1–PB5 name two distinguished poles and constrain realizable conditions relative to them. They do not impose an exhaustion principle on the class of flat sterile origin candidates. A third candidate $z\in\mathcal C$ can therefore be posited with
$$
z\neq \mathbf 0,\qquad z\neq \mathbf 1,\qquad \mathrm{Orig}(z),\qquad \mathrm{Flat}(z),\qquad \mathrm{Ster}(z),
$$
without violating PB1–PB5. Hence bipolar flat-origin classification is underdetermined by the present package. $\square$

### 3.7 Exact additional principle for bipolar exhaustion

**BEP — Bipolar Exhaustion Principle.**
$$
\forall x\in\mathcal C,\quad \big(\mathrm{Orig}(x)\wedge \mathrm{Flat}(x)\wedge \mathrm{Ster}(x)\big)\Rightarrow (x=\mathbf 0 \vee x=\mathbf 1).
$$

BEP does not by itself create the invariant. It only closes the stronger classification gap needed to justify that the two distinguished poles exhaust the flat sterile origin extremes.

**Status:** Requires one new explicit principle.

**Proposition 3.7.1 (BEP is not on the first-articulation route).**  
BEP is not required for the derivation of first differentiated articulation or for the v16 first-articulation route.

**Status:** Proved.

**Proof.**  
The derivations below use only PB3, PB5, and the sharpened existence premise E1. They do not quantify over all flat sterile origin candidates and do not invoke bipolar exhaustion. Therefore BEP is parked for the stronger classification claim and is not on the WNF critical path. $\square$

### 3.8 Existence burden recast for the first-articulation route

The old bare existence premise
$$
\exists x\in\mathcal C\;\mathrm{Real}(x)
$$
was usable for anti-flatness, but too loose for the v13 invariant route because it did not keep the first articulation chain scoped to origin-bearing realizability.

**E1 — Realizable origin existence**
$$
\exists x\in\mathcal C\;\big(\mathrm{Orig}(x)\wedge \mathrm{Real}(x)\big).
$$

This sharpened E1 is the correct existence premise for the first-articulation route.

**Status:** Requires one new explicit principle.

### 3.9 First non-flat articulation under the invariant

**Theorem 3.9.1 (Breakdown of perfect flatness).**  
Assume PB3, PB5, and E1. Then there exists at least one realizable origin-condition that is not flat.

**Status:** Requires one new explicit principle, namely E1.

**Proof.**  
By E1, choose $x$ with $\mathrm{Orig}(x)\wedge \mathrm{Real}(x)$. By PB3, $\mathrm{Opp}(\mathbf 0,\mathbf 1)$. PB5 then yields $\neg \mathrm{Flat}(x)$. $\square$

**Theorem 3.9.2 (Differentiated articulation exists).**  
Assume PB3, PB5, and E1. Then
$$
\exists x\in\mathcal C\;\big(\mathrm{Orig}(x)\wedge \mathrm{Diff}(x)\big).
$$

**Status:** Requires one new explicit principle, namely E1.

**Proof.**  
Immediate from Theorem 3.9.1 and the definition of $\mathrm{Diff}$. $\square$

### 3.10 Non-flatness does not discharge the invariant

Theorem 3.9.2 is not a discharge theorem. It does not say that the primitive burden has been solved. It says only that once realizability is admitted under unresolved pole-opposition, perfect self-coincidence fails. This is the first negative articulation of the invariant, not its exhaustion.

**Status:** Proved as architectural consequence of the governing rule.

### 3.11 Local settlement versus global non-resolution

This manuscript henceforth uses the following discipline.

- A local articulation may settle enough to support derived structure.
- Such settlement may look one-sided.
- That does **not** count as global final resolution of the primitive invariant.

Any later theorem that uses stability language must say explicitly whether it is only local settlement or something stronger.

### 3.12 Section summary

At this stage the manuscript has:

- proved exclusion of isolated nullity,
- proved exclusion of isolated undifferentiated totality,
- proved distinctness of the poles despite shared sterility,
- proved that the current package does not itself exhaust flat sterile origin by the two poles,
- isolated BEP as the exact bipolar classification burden,
- isolated E1 as the exact existence burden,
- and shown that admitted realizability yields non-flat articulation without discharging the invariant.

---


## 4. First Articulation Chain Governed by the Invariant

### 4.1 Dependency-clean stage order

The intended dependency order is now stated under the invariant frame:

1. pole distinction and exclusion of isolated pole-residence,
2. conditional forcing of one-origin internal unresolved opposition,
3. first negative articulation: non-flat realizability,
4. first positive articulation: first invariant-bearing differentiated degree,
5. widening of that first degree under the same invariant,
6. multiplicity in the weak internal sense,
7. apartness,
8. recursive refinement of the same invariant,
9. dependence order,
10. hierarchy,
11. later braking, truncation, locality, coherence, and pre-carrier burden.

The point is no longer “first anti-flatness, then maybe witness, then maybe plurality.” The point is: each stage is a more articulated expression of one undischarged primitive invariant, and v16 must separate the **character** of widening from the **availability** of widening rather than compressing both into one coarse slogan.

### 4.2 Naming disposition under the invariant

The AC invariant correction changes the diagnostic question. The manuscript must no longer ask what later object certifies the first articulation. It must ask what primitive structural difference is already earned once the same unresolved invariant is carried non-flatly.

The v16 naming verdict is therefore:

- the first positive articulation remains closed,
- the risky theorem-spine phrase **"distinction of change"** is retired,
- and the safer structural term is **first invariant-bearing differentiated degree**.

This change is not cosmetic. It prevents the first positive articulation from sounding temporal, event-like, or causal, and it keeps the theorem spine focused on invariant carriage rather than on later process language.

### 4.3 First invariant-bearing differentiated degree

**Definition 4.3.1 (First invariant-bearing differentiated degree).**  
At the present layer, write
$$
\mathrm{Deg}_1(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x).
$$
This says that the same primitive invariant now occurs in a realizable non-flat articulation rather than in primitive undifferentiated form. The definition is deliberately first-layer only. It does **not** mean smoothness, derivative structure, manifold differentiability, event sequence, or causal transition.

### 4.4 First positive articulation is already derivable

**Theorem 4.4.1 (First invariant-bearing differentiated degree exists).**  
Assume PB3, PB5, and E1. Then
$$
\exists x\in\mathcal C\;ig(\mathrm{Orig}(x)\wedge \mathrm{Deg}_1(x)ig).
$$

**Status:** Requires one new explicit principle, namely E1.

**Proof.**  
By Theorem 3.9.2, there exists $x$ with $\mathrm{Orig}(x)\wedge \mathrm{Diff}(x)$. By the governing invariant discipline already adopted in this manuscript, an origin-bearing realizable articulation produced under PB3 and PB5 stands under unresolved internal pole-opposition and so carries $\mathrm{Inv}(x)$ in the manuscript sense. Hence $\mathrm{Deg}_1(x)$ holds. Therefore such an $x$ exists. $\square$

**Corollary 4.4.2 (The first positive articulation burden closes once E1 is admitted).**  
The first positive articulation burden is not an extra witness layer above differentiated articulation. It closes directly as the first invariant-bearing differentiated degree.

**Status:** Proved.

**Proof.**  
Immediate from Theorem 4.4.1. $\square$

### 4.5 Why no second witness layer is retained on the root route

**Proposition 4.5.1 (The v14 weak/strong WNF split is not a live root dependency difference).**  
On the v16 route, the old weak/strong WNF split is not retained as a mainline dependency split for the first positive articulation.

**Status:** Proved as dependency-order disposition.

**Proof.**  
The first positive articulation is already captured by $\mathrm{Deg}_1(x)$, which closes by Theorem 4.4.1 once E1 is admitted. Any stronger requirement that the first articulation be formalized through an additional explicit witness layer is therefore not needed to state or prove that first articulation itself. Such a further requirement may matter for later burdens, but it is not on the first-articulation route. $\square$

The v14 witness language is retained only as migration crosswalk and warning against smuggling multiplicity or later-stage usability conditions into the root theorem.

### 4.6 DWP disposition under the invariant

DWP is not “plurality from nowhere.” It is the next question about the same invariant once the first degree is already earned. But the coarse v15 form of DWP,
$$
orall x\in\mathcal C,\quad \mathrm{Deg}_1(x)\Rightarrow \mathrm{Mult}(x),
$$
is too coarse. It collapses two non-equivalent claims into one line:

1. **character claim:** what genuine widening would have to look like if it occurs; and
2. **availability claim:** whether the present package already proves that such widening occurs.

These are different burdens.

**Theorem 4.6.1 (Coarse DWP should be split).**  
The manuscript must distinguish the character of widening from the availability of widening.

**Status:** Proved as dependency-order disposition.

**Proof.**  
A theorem that states only $\mathrm{Deg}_1(x)\Rightarrow \mathrm{Mult}(x)$ says neither what makes the widening genuine nor whether the present package proves the existence of such a widened articulation. The first omission is structural; the second is existential. Since these burdens can succeed or fail separately, the coarse statement conflates distinct theorem tasks and must be split. $\square$

### 4.7 Widening character versus widening availability

Call a **genuine widening** any stronger articulation of the same invariant that carries a new degree of variation rather than merely renaming the first degree.

**Theorem 4.7.1 (Widening Character Lemma).**  
If a first invariant-bearing differentiated degree is genuinely widened under the same invariant, then the widened articulation is plurality-bearing in the weak internal sense captured by $\mathrm{Mult}(x)$.

**Status:** Proved.

**Proof.**  
The AC invariant discipline states that a new degree of variation yields an increase in complexity. A genuine widening is therefore not a vacuous restatement of the first degree, but a stronger articulation carrying strictly richer internal variation under the same unresolved burden. If the widened articulation remained singular in internal determination, no new internal variation would have been introduced, and the alleged widening would collapse into mere restatement of the same first degree. That contradicts the assumption that the articulation is genuinely widened. Hence any genuine widening, if it occurs, must carry more than one internally distinct determination in the weak internal sense intended by $\mathrm{Mult}(x)$. $\square$

This theorem proves the **character** of widening. It does **not** prove the **availability** of widening.

**WAP — Widening Availability Principle**  
At least one origin-bearing first invariant-bearing differentiated degree admits genuine widening under the same unresolved invariant.

**Status:** Requires one new explicit principle.

**Theorem 4.7.2 (Availability of widening does not yet follow).**  
The current manuscript does **not** prove WAP from PB1–PB5 and E1.

**Status:** Proved as a no-go.

**Proof.**  
PB1–PB5 and E1 yield at least one origin-bearing first invariant-bearing differentiated degree by Theorem 4.4.1. They also preserve global non-discharge of the invariant and the distinction between local settlement and global resolution. But they do not yet specify that any first-degree articulation actually widens into a stronger articulation rather than remaining merely the first earned degree. To infer such widening directly would require an extra availability principle or would silently borrow recursive-restatement burden from a later stage. Therefore WAP does not follow from the present package alone. $\square$

So the live plurality bottleneck is now exact:

- **WCL is proved** (character of widening),
- **WAP is open** (availability of widening),
- and multiplicity remains unclosed only because WAP is unproved.

### 4.8 Apartness remains blocked behind widened plurality

**Theorem 4.8.1.**  
Apartness is blocked until widening availability closes and plurality is actually obtained.

**Status:** Proved.

**Proof.**  
Apartness requires at least two distinct internal determinations between which noncoincidence can be stated. The Widening Character Lemma proves only what widening would require if it occurs. Since WAP is still open, the manuscript has no theorem yet yielding an actually widened plurality-bearing articulation. Therefore apartness remains blocked. $\square$

If WAP later closes, apartness may be defined contextually rather than primitively.

### 4.9 RRP recast under the invariant

RRP is not a later optional reactivation principle. It is the claim that if a first-degree or widened articulation still leaves the invariant locally unsettled, the same invariant must be restated at higher resolution.

**Theorem 4.9.1 (Recursive refinement does not yet follow).**  
The current manuscript does **not** prove recursive refinement from PB1–PB5, E1, and the first invariant-bearing differentiated degree.

**Status:** Proved as a no-go.

**Proof.**  
PB1–PB5, E1, and the first invariant-bearing differentiated degree yield an articulated degree of invariant carriage, but they do not yet specify when that articulation remains locally unsettled in a way that requires the invariant to be restated at higher resolution. The Widening Character Lemma does not solve this, because it concerns only the form genuine widening would have, not whether higher-resolution restatement is forced. Therefore recursive refinement does not follow. $\square$

**RRP — Recursive Reapplication Principle**  
If a realizable invariant-bearing articulation remains locally unsettled relative to the same primitive invariant, then a further articulated condition is required that again stands under that invariant.

RRP is thus not a fresh engine. It is the higher-resolution restatement of the same one.

**Status:** Requires one new explicit principle.

### 4.10 Dependence order, not time

**Proposition 4.9.1.**  
Any earliest order obtained from repeated articulation of the invariant is an order of dependence, not yet an order of physical time.

**Status:** Proved.

**Proof.**  
The present root package contains no time parameter, no dynamics, no event sequence, no continuation law, and no dissipation law. Therefore any earliest order here can only mean that one burden must be settled before another later structure is licensed. $\square$

### 4.11 Hierarchy

Hierarchy is not primitive ancestry in this rewrite. It is repeated dependence/refinement under the same invariant.

**Status:** Blocked.

What is proved is only the frame discipline: hierarchy must, if later closed, be derived from repeated articulation of one invariant burden rather than from primitive tree language.

### 4.12 Exact active bite under the correct frame

The active bite is no longer best described as “find the next isolated module.”

The active bite is now sharper:

1. keep the first invariant-bearing differentiated degree closed without inflating it into multiplicity,
2. decide whether any first-degree articulation genuinely widens and, if so, under what exact availability burden,
3. decide when a locally unsettled invariant-bearing articulation forces higher-resolution restatement via RRP,
4. only after that ask the later truncation, locality, and carrier questions.

That is the first honest engine chain of the manuscript.

### 4.13 Contamination self-check for the articulation chain

At the present stage, the three top risks are:

1. **externalizing the poles** so the origin is misread as two primitive things;
2. **treating the first invariant-bearing differentiated degree as already multiplicity**, which would smuggle plurality shut;
3. **treating RRP as optional reactivation** rather than as higher-resolution restatement of the same invariant.

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

Causality is later than dependence order and likely later than mere continuation. It requires at minimum some admissible locality or propagation discipline. Therefore causality is forbidden from the primitive layer.

**Status:** Proved as staging discipline.

---

## 6. Relationship to H000, A8, CF00, and Later Canon

### 6.1 H000

H000 remains the proposal-grade hypothesis line that first stated the primitive bifurcation architecture in compact form.

**Status:** Alignment only.

### 6.2 A8

A8 is not the primitive generator in this rewrite. It is a later-regime candidate expression of the same invariant burden under additional structure: repeated articulation, braking, truncation, and interface concentration.

**Status:** Proved as reclassification discipline.

### 6.3 CF00

CF00 remains downstream of any legitimate pre-carrier and pre-differential closure achieved here. The present draft still does not license the carrier bridge.

### 6.4 Later dual split

The present root architecture suggests a plausible deep ancestor of the later conservative/dissipative split:

- one aspect opens articulation under unresolved opposition,
- another aspect closes or stabilizes locally without global discharge.

This is structurally suggestive, but it is **not** a derivation of QGT or $J\oplus M$.

**Status:** Not proved.

---


## 7. v15 to v16 Migration and Disposition

### 7.1 Global verdict on v15

v15 correctly closed the first positive articulation under the AC invariant rule, but it still carried two avoidable risks:

1. its preferred phrase **"distinction of change"** still suggested time or process more strongly than the theorem actually warranted, and
2. its coarse DWP statement still compressed widening-character and widening-availability into one slogan.

### 7.2 What v16 changes

v16 makes four narrow but important changes.

- It retires the risky theorem-spine phrase **"distinction of change"** and replaces it with **first invariant-bearing differentiated degree**.
- It preserves the v15 closure of the first positive articulation and does **not** reopen the v14 witness split.
- It splits coarse DWP into a **proved Widening Character Lemma (WCL)** and an open **Widening Availability Principle (WAP)**.
- It leaves **BEP** parked, keeps **E1** origin-scoped, and leaves apartness and RRP downstream.

### 7.3 What v16 does not change

v16 does not reopen the one-origin invariant frame, does not reopen WNF-style witness bookkeeping, does not prove widening availability, does not prove apartness, does not advance RRP, and does not move locality, frontier, coherence, pre-carrier support, or differentiability forward.

### 7.4 Net disposition outcome

The DWP pass lands as **Outcome C**:

- the first positive articulation remains closed,
- coarse DWP is too coarse and must be split,
- widening character is proved,
- widening availability remains open,
- and the manuscript is cleaner once those two burdens are separated.


## 8. Remaining Burdens Required for Actual Closure

To move this draft toward real CF closure, the next burdens are now ordered as follows.

1. **E1 derivability remains open**  
   E1 remains explicit in sharpened origin-scoped form. The question is whether realizable origin-bearing articulation is itself derivable rather than admitted.

2. **WAP — widening availability**  
   Decide whether at least one origin-bearing first invariant-bearing differentiated degree genuinely widens under the same invariant.

3. **Multiplicity after widening availability**  
   Once WAP closes, multiplicity follows by WCL and may then be used as an actual theorem-stage result rather than a merely characterized form.

4. **Apartness after multiplicity**  
   Once multiplicity closes, define apartness contextually rather than primitively.

5. **RRP — higher-resolution restatement of the same invariant**  
   Prove or admit when locally unsettled invariant-bearing articulation forces further articulation.

6. **WEP — well-founded exhaustion / truncation burden**  
   Decide whether repeated articulation yields frontier-like closure or requires one additional principle.

7. **First honest locality stage**  
   Identify exactly when “local” first becomes earned rather than intuitive leakage.

8. **Later coherence principle**  
   If locality/frontier ever closes, isolate one minimal coherence principle for any pre-carrier bridge.

9. **Differentiability status**  
   Keep this honest: either open, or name the exact burden.

10. **Later dual split**  
    Any bridge from this root to a conservative/dissipative dual structure remains downstream and unproved.

11. **BEP remains parked**  
    BEP still matters for stronger flat-origin exhaustion, but it is no longer a live blocker for the first-articulation route.


## 9. Theorem Inventory (compact)

### Proved
- Nullity exclusion
- Undifferentiated totality exclusion
- Pole non-identity with shared sterility verdict
- No-go on bipolar flat-origin classification from the current lean package
- **BEP is not required for the first-articulation route**
- Breakdown of perfect flatness from PB3, PB5, and sharpened E1
- Existence of differentiated articulation from PB3, PB5, and sharpened E1
- First invariant-bearing differentiated degree exists from PB3, PB5, and sharpened E1
- The first positive articulation burden closes directly as the first invariant-bearing differentiated degree once E1 is admitted
- Non-flatness does not discharge the invariant
- Coarse DWP must be split into character versus availability
- The **Widening Character Lemma**
- Widening availability does not follow from PB1–PB5 and E1
- Apartness is blocked until widening availability closes
- Recursive refinement does not follow from PB1–PB5, sharpened E1, and the first invariant-bearing differentiated degree
- Dependence order is earlier than time
- Reversible continuation is staged later than dependence order
- Irreversible arrow is staged later than root asymmetry
- Causality is forbidden at the primitive layer
- A8 is reclassified as late-regime expression, not primitive generator

### Requires one new explicit principle
- Realizable origin existence via sharpened E1
- Widening availability via WAP
- Recursive higher-resolution restatement via RRP
- Truncation/frontier via WEP
- Bipolar exhaustion via BEP, but only for the stronger classification claim

### Not proved
- That sharpened E1 is derivable rather than added
- That WAP is derivable rather than added
- That RRP is derivable rather than added
- That WEP is derivable rather than added
- Any constructive locality stage
- Any pre-carrier bridge
- Any differentiability result
- Any derivation of the later conservative/dissipative split

### Blocked
- Actual multiplicity as constructive result before WAP closes
- Apartness as constructive result before multiplicity closes
- Hierarchy as constructive result before RRP closes
- Boundary/domain-wall-type structure before truncation closes
- First honest locality stage before later burdens close
- Pre-carrier patchability before locality/coherence closure


## 10. Anti-Smuggling Note

Top contamination risks in the present rewrite:

1. **Externalizing the poles**  
   If the two poles are written as two ready-made things standing apart, the one-origin root is lost.

2. **Using $\mathcal C$ as hidden ontology**  
   The logical discourse domain must not secretly do the work of plurality.

3. **Treating the first invariant-bearing differentiated degree as already multiplicity**  
   The first positive articulation is still weaker than actual widened plurality.

4. **Borrowing later witness language to certify present articulation**  
   If a later-stage usability or explicit witness requirement is imported in order to state the first articulated degree, the manuscript has asked the wrong question.

5. **Treating WAP as arbitrary extra plurality rule**  
   WAP must read as the minimal availability burden for a stronger articulation of the same invariant, not as plurality from nowhere.

6. **Treating RRP as optional reactivation**  
   RRP must read as the higher-resolution restatement of the same invariant when local articulation remains unsettled.

7. **Letting local settlement sound final**  
   Stability language must never imply global discharge of the invariant unless that stronger claim is separately proved.

8. **Reading first-degree articulation language as smoothness**  
   The first-degree language names articulated carriage of the invariant, not differentiability in the later geometric sense.


## Appendix A. Primitive Block

Primitive marks and predicates of this draft:

$$
\mathbf 0,\mathbf 1\in \mathcal C
$$

$$
\mathrm{Orig}(x),\qquad \mathrm{Ster}(x),\qquad \mathrm{NV}(x),\qquad \mathrm{Real}(x),\qquad \mathrm{Flat}(x),\qquad \mathrm{Opp}(x,y)
$$

Adopted root laws:

$$
\mathbf 0
eq \mathbf 1
$$

$$
\mathrm{Ster}(\mathbf 0)\wedge \mathrm{Ster}(\mathbf 1)
$$

$$
\mathrm{Opp}(\mathbf 0,\mathbf 1)
$$

$$
orall x\in\mathcal C,\quad \mathrm{Real}(x)\Rightarrow ig(\mathrm{NV}(x)\wedge x
eq \mathbf 0 \wedge x
eq \mathbf 1ig)
$$

$$
orall x\in\mathcal C,\quad ig(\mathrm{Real}(x)\wedge \mathrm{Opp}(\mathbf 0,\mathbf 1)ig)\Rightarrow 
eg \mathrm{Flat}(x)
$$

Named added principles introduced by this draft:

- **BEP** — Bipolar Exhaustion Principle
- **E1** — Realizable origin existence
- **WAP** — Widening Availability Principle
- **RRP** — Recursive Reapplication Principle
- **WEP** — Well-founded Exhaustion Principle

Migration crosswalk only:

- the v14 weak/strong **WNF** split is retained only as historical theorem-hygiene cleanup and is not on the v16 main dependency spine,
- the coarse **DWP** slogan is retained only as migration shorthand and is resolved in v16 into **WCL + WAP**.


## Appendix B. Articulation Block

First derived shorthand:
$$
\mathrm{Diff}(x):=\mathrm{Real}(x)\wedge 
eg \mathrm{Flat}(x)
$$

First positive articulation:
$$
\mathrm{Deg}_1(x):=\mathrm{Inv}(x)\wedge \mathrm{Diff}(x)
$$

Architectural shorthand:
- $\mathrm{Inv}(x)$ — one realizable origin-condition stands under globally undischarged internal pole-opposition.
- $\mathrm{LocSet}(x)$ — one local articulation settles without globally discharging the invariant.

v16 widening split:
- **WCL** — if genuine widening occurs, it is plurality-bearing.
- **WAP** — at least one first-degree articulation genuinely widens.

Target later notions, not yet closed:

- actual multiplicity,
- apartness,
- recursive refinement,
- dependence hierarchy,
- qualitative braking,
- truncation/frontier,
- boundary-type structure,
- locality,
- coherence,
- pre-carrier support,
- differentiability bridge.

Migration warning:

- v14’s weak non-self-coincidence language is absorbed into first differentiated articulation,
- v14’s strong witness-lift language is not retained as a root bottleneck in v16,
- v15’s phrase **"distinction of change"** is retired from the theorem spine in v16 in favor of **first invariant-bearing differentiated degree**,
- v15’s coarse DWP statement is not retained as a single theorem task in v16.


## Appendix C. Acceptance Status

This document is **not** yet a Completed Formalism for the full CF000 burden.

It is a v16 DWP-disposition pass that:

- keeps the v13 primitive bifurcation frame frozen as baseline,
- preserves the v15 closure of the first positive articulation,
- replaces the risky theorem-spine phrase **"distinction of change"** with **first invariant-bearing differentiated degree**,
- splits coarse DWP into proved widening character and open widening availability,
- keeps RRP downstream,
- and names the remaining exact burdens without pretending closure.

The next serious pass should either derive **E1** or, if E1 is provisionally admitted, attack **WAP** as the exact availability burden for plurality-bearing widening.
