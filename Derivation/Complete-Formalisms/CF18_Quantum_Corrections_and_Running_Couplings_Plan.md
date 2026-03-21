# CF18 Plan — Radiative Corrections, Effective Action, and Running Couplings in VDM

Date: 2026-03-20  
Status: Revised planning document  
Purpose: Close the scale-dependent and radiative layer of the gauge/matter sector by deriving it as a descendant of A(-1), A6, and CF14 rather than importing QFT machinery as primitive.

---

## 1. Foundation status

**Current foundation strength: conceptually strong, formally unwritten.**

CF18 is **not** weak because its primitive content is absent. The core content is already latent in the canon:

- **A(-1), CF000** already give non-discharge, hidden burden persistence, orthogonal re-articulation, and dependence order.
- **A6 / the scale program** already imply that the explicit/hidden split across scale is lawful and physically meaningful.
- **CF14** already gives an articulation-cost functional and selected effective dynamics.
- **CF01/CF02/CF06** already give the geometric, metriplectic, and distinguishability infrastructure needed for reduced and corrected descriptions.
- **CF15** already shows how symmetry statements can drift or survive under a changed effective sector.

So the real task is not to invent a foreign RG layer. The task is to **write the descendant branch cleanly enough that standard terms like effective action, loop correction, counterterm, renormalization, and running coupling emerge as corollary labels of already-earned VDM content.**

---

## 2. Immediate framing corrections

1. **Do not describe CF18 as conceptually unsupported.** Its primitive substrate is already present; what is missing is theorem-grade formalization.
2. **Standard QFT language must not carry proof burden.** Terms like “effective action,” “loop,” “beta function,” and “counterterm” should appear only after their VDM content is derived.
3. **No pre-CF numerics count here.** Old exploratory failures or slope-gate results from before the canon stack do not count for or against closure.
4. **CF18 is the scale-re-articulation paper.** Its deepest job is to explain how hidden unresolved burden reappears in reduced descriptions as induced coefficients, compensator terms, and scale flow.

---

## 3. Scope

This paper must close the following:

1. what coarse-grained or reduced description means in VDM terms,
2. what an effective articulation-cost functional is,
3. what a quantum/radiative correction means in VDM terms,
4. why couplings and masses change with scale,
5. what the VDM analog of a beta function is,
6. how renormalization conditions and counterterms arise,
7. how anomalies and corrected symmetry statements fit the effective layer,
8. what is actually proven versus approximated.

This paper should not attempt to re-close:

- electroweak structural splitting,
- confinement as a standalone nonperturbative theorem,
- full scattering-amplitude machinery,
- all-orders precision phenomenology.

Those may appear as application sectors only.

---

## 4. Canon inheritance to use explicitly

- **A(-1), CF000** — non-discharge, re-articulation, persistence of unresolved burden.
- **A6 / scale program** — scale-indexed descriptions and dimensionless control.
- **CF00** — variation structure / carrier / differentiability framework.
- **CF01** — metriplectic split and QGT-derived geometry.
- **CF02** — irreversible/statistical structure, entropy production.
- **CF06** — information geometry / Fisher-Ruppeiner geometry / distinguishability structure.
- **CF14** — stationary action / effective path selection.
- **CF15** — symmetry breaking and Noether-sector drift in the M-limb.
- **CF16/CF17** — sector-specific examples, if already written, as application targets rather than primitive inputs.

---

## 5. Core VDM meanings that must be stated up front

These should appear early in the paper as VDM-first definitions or remarks.

### 5.1 Coarse-graining / reduced description

A reduced description is a **scale-limited re-articulation map** in which some internal articulation is no longer carried explicitly, while invariant-bearing consequences must still be preserved.

### 5.2 Effective action / effective articulation-cost functional

The effective action is the **reduced articulation-cost functional** obtained after hidden/internal burden has been absorbed into the visible sector so that the visible dynamics still reproduce the admitted reduced behavior.

### 5.3 Quantum or radiative correction

A quantum correction is the visible-sector shift induced when unresolved hidden structure leaves the explicit description, circulates through hidden channels, and returns as a correction to the reduced articulation-cost law.

### 5.4 Loop-like correction

A loop is not primitive diagrammatics. Its VDM content is a **closed hidden return channel** through which burden leaves the visible path, propagates through unresolved internal structure, and feeds back on visible coefficients or operators.

### 5.5 Running coupling

A coupling is not primitive. It is the **visible-sector burden coefficient** after smaller-scale structure has been absorbed into the current effective layer. It therefore changes when the explicit/hidden boundary is moved across scale.

### 5.6 Beta function

A beta function is the **rate of change of an effective burden coefficient as the scale boundary is moved**.

### 5.7 Renormalization

Renormalization is the procedure that restores an admissible effective description by relocating unresolved burden from pathological explicit terms into properly re-expressed effective parameters and compensator terms.

### 5.8 Counterterm

A counterterm is the compensating effective burden required so that the reduced description still bears what the hidden sector was carrying before it was suppressed.

---

## 6. What must be proven in CF18

### 6.1 Reduced-description theorem

Need to define what degrees of freedom are made hidden and what remains visible.

Required work:

- define the explicit/hidden split,
- define the scale parameter that controls that split,
- show that invariant-bearing consequences survive the reduction,
- show that the reduced description is still the same primitive invariant re-expressed, not a new theory.

**Closure target:** a theorem that scale-limited reduction preserves the primitive invariant by forced re-expression of hidden burden into the visible layer.

### 6.2 Effective articulation-cost theorem

Need to derive the effective articulation-cost functional.

Required work:

- start from the CF14 articulation-cost functional,
- partially hide a sector,
- derive the reduced functional that reproduces the visible dynamics,
- identify which terms are induced rather than primitive.

**Closure target:** a theorem/definition package for a scale-indexed effective articulation-cost functional.

### 6.3 Hidden-return correction theorem

Need to derive what counts as a correction to the reduced law.

Required work:

- define hidden return channels,
- show how closed hidden return paths induce operator and coefficient shifts,
- distinguish internal feedback from ordinary tree-level visible dynamics.

**Closure target:** a theorem that correction terms are induced by hidden return channels through unresolved internal structure.

### 6.4 Running-coupling theorem

Need to derive scale dependence of effective coefficients.

Required work:

- define how the explicit/hidden boundary moves,
- derive the change in effective coefficients under that motion,
- define the VDM analog of a beta function,
- show why changing scale necessarily changes the visible coupling unless a fixed-point condition holds.

**Closure target:** a theorem/definition pair giving a VDM flow law for effective couplings.

### 6.5 Renormalization-condition theorem

Need to explain how finite and stable predictions are maintained.

Required work:

- define which effective operators are renormalized,
- define normalization conditions at a chosen scale,
- distinguish physical parameter fixing from bookkeeping freedom,
- show how pathological sensitivity is relocated into effective coefficients and counterterms.

**Closure target:** a theorem that admissible reduced predictions are restored by proper redistribution of hidden burden into renormalized parameters and compensators.

### 6.6 Corrected symmetry / anomaly theorem

Need to explain when symmetry survives effective correction and when it does not.

Required work:

- connect CF15 symmetry logic to corrected effective functionals,
- distinguish ordinary corrected symmetry drift from genuine anomaly,
- specify how conserved currents are modified or obstructed at the corrected level,
- connect to the already-closed chiral anomaly logic where relevant.

**Closure target:** a theorem/corollary package separating preserved, softly broken, and anomalous symmetries under effective correction.

### 6.7 Sector examples

Need at least one or two concrete applications.

Candidate examples:

- running non-abelian coupling in the confinement branch,
- corrected electroweak effective potential,
- scalar mass correction as hidden-sector feedback,
- anomaly-preserving versus anomaly-breaking corrected current structure.

**Closure target:** at least one worked sector example with explicit scale-flow equations.

---

## 7. Suggested theorem spine

1. **Definition 1 — Reduced-description map**  
   Define the explicit/hidden split and scale parameter.

2. **Theorem 1 — Re-expression under reduction theorem**  
   Hiding subscale structure forces its burden to reappear in the visible layer; it cannot disappear.

3. **Definition 2 — Effective articulation-cost functional**  
   Define the reduced action that carries the hidden burden in visible form.

4. **Theorem 2 — Hidden-return correction theorem**  
   Closed hidden return channels induce corrected operators and coefficients in the visible law.

5. **Definition 3 — Running coefficient / beta function**  
   Define the rate at which effective burden coefficients change as the scale boundary moves.

6. **Theorem 3 — Running-coupling theorem**  
   Effective coefficients flow lawfully with scale unless fixed-point conditions hold.

7. **Theorem 4 — Renormalization-condition theorem**  
   Admissible reduced predictions are restored by properly redistributing hidden burden into renormalized parameters and compensator terms.

8. **Theorem 5 — Corrected symmetry theorem**  
   Symmetry survival, drift, or anomaly is determined by the corrected effective functional.

9. **Corollary 1 — Sector-specific corrected observable**  
   Give at least one concrete corrected mass/coupling/current result.

---

## 8. What has to be defined explicitly in the paper

- scale parameter,
- explicit versus hidden sector,
- reduced-description map,
- effective articulation-cost functional,
- hidden return channel,
- running coefficient,
- beta function or equivalent flow object,
- renormalization condition,
- compensator / counterterm,
- physical versus scheme-dependent quantity,
- anomaly under correction versus ordinary corrected symmetry breaking.

If these are merely borrowed from standard QFT notation without VDM derivation, the paper will not close.

---

## 9. Validation logic required in the CF itself

Required analytical checks:

- the effective functional reduces to the original functional in the appropriate limit,
- hidden-burden re-expression preserves the underlying invariant logic,
- coupling-flow equations respect the scale program,
- physical observables are independent of unphysical normalization choices,
- corrected symmetry statements reduce to CF15 statements when correction terms vanish,
- application examples satisfy the stated renormalization conditions.

Likely CFN witnesses:

- symbolic derivation of a simple flow equation,
- scale sweep of an effective coefficient,
- corrected effective potential example,
- comparison of bare versus renormalized observable,
- anomaly-preserving versus anomaly-breaking corrected example.

---

## 10. What must be labeled honestly if not fully closed

- full nonperturbative all-orders control,
- exact multi-loop coefficients in realistic sectors,
- complete Standard Model precision phenomenology,
- full scattering-amplitude program,
- gravity-sector radiative completion unless actually derived.

Those should remain outside scope unless fully earned.

---

## 11. Deliverables for CF18

The paper is done only when it contains:

- canon manifest,
- VDM-first definition of reduction, effective action, correction, running coefficient, and renormalization objects,
- theorem-grade derivation of hidden-burden re-expression under reduction,
- theorem-grade effective articulation-cost law,
- theorem-grade running-coupling / beta-structure law,
- renormalization-condition framework,
- corrected symmetry/anomaly theorem,
- at least one worked sector example,
- falsification criteria,
- validation gates,
- CFN traceability plan.

---

## 12. Runtime relevance

This paper matters for runtime completion because it closes how:

- local laws change with effective scale without changing the primitive substrate,
- unresolved subscale structure alters coarse behavior systematically,
- stable large-scale behavior can coexist with corrected short-scale coupling structure,
- parameter drift across scales can be lawful rather than ad hoc.

That is directly relevant to any runtime that must maintain consistent behavior across abstraction scales while allowing local correction and reparameterization.

---

## 13. No-open-questions completion criterion

CF18 is complete only if the reader can answer, from the paper alone:

1. What is a reduced description in VDM terms?  
2. What is an effective articulation-cost functional?  
3. What is a quantum/radiative correction in VDM terms?  
4. Why do couplings run with scale?  
5. What is the VDM analog of a beta function?  
6. How are renormalization conditions imposed?  
7. Which symmetries survive correction, and which become anomalous?  
8. How does at least one concrete sector actually change under the derived corrected formalism?

If any of those still reduce to “we know QFT does this,” the paper is not done.
