\
# CF000 v12 — WNF Theorem Note
Date: 2026-03-13  
Scope: WNF / internal noncoincidence pass only  
Base manuscript: `CF000_Primitive_Distinguishability_and_the_Origin_of_Differentiability_v12_FULL_MANUSCRIPT_WNF_v1.md`

---

## 1. Definitions table audit note

This pass refines the early definitions table to separate the following without blur:

- **flatness** as an internal structural condition,
- **sterility** as a branch-level incapacity verdict,
- **internal noncoincidence** as a positive witness condition,
- **multiplicity** as a later and stronger burden.

New mandatory entries added or sharpened:

- internal noncoincidence,
- witness of non-flatness,
- multiplicity as downstream of witness,
- apartness as downstream of multiplicity.

No table entry in this pass defines witness structure so strongly that plurality or apartness is already hidden inside it.

---

## 2. WNF theorem or failure result

**Result:** The current primitive package PB1–PB5, together with E1, does **not** force a weakest positive witness of non-flatness.

**Why this is proved:**  
A model can satisfy PB1–PB5 and E1 with some differentiated realizable condition $r$ for which $\mathrm{Diff}(r)$ holds, while no positive witness relation is linked to that fact. Therefore the package underdetermines positive witness structure.

**Exact minimal additional principle required:**  
**WNF — Witnessed Non-Flatness Principle**

$$
\forall x\in\mathcal C,\quad \mathrm{Diff}(x) \Rightarrow \mathrm{INC}(x).
$$

Equivalent witness form:

$$
\forall x\in\mathcal C,\quad \mathrm{Diff}(x) \Rightarrow \exists w\in\mathcal W\;\mathrm{WitNF}(w,x).
$$

---

## 3. Weakest positive witness of non-flatness

**Candidate witness:** internal noncoincidence.

**Lean statement:**  
One realizable differentiated condition fails total self-coincidence in a structurally relevant sense.

**Provisional formal layer:**

$$
\mathrm{INC}(x) := \exists w\in\mathcal W\;\mathrm{WitNF}(w,x).
$$

**Strength position of this witness:**

- stronger than mere $\neg\mathrm{Flat}(x)$ because it adds a positive witness condition,
- weaker than multiplicity because it does not yet decompose into two determinations,
- weaker than apartness because it does not yet posit a relation between distinct determinations,
- not graph/tree structure because it does not use nodes, edges, ancestry, depth, or frontier language.

---

## 4. Theorem or no-go on multiplicity

**Result:** Multiplicity does **not** follow from PB1–PB5, E1, and WNF alone.

WNF yields only positive witness structure. It does not yet state that witness structure decomposes into at least two noncoincident internal determinations.

**Exact minimal additional principle required:**  
**DWP — Determination-Witness Decomposability Principle**

$$
\forall x\in\mathcal C,\quad \mathrm{INC}(x) \Rightarrow \exists a,b\;\big(\mathrm{Det}(a,x) \wedge \mathrm{Det}(b,x) \wedge a\neq b \wedge \neg\mathrm{Coinc}(a,b)\big).
$$

---

## 5. Theorem or no-go on apartness

**Result:** Apartness is **blocked** until multiplicity closes.

Reason: apartness requires at least two distinct internal determinations between which noncoincidence can be stated. Before DWP or an equivalent multiplicity-closing bridge is admitted, the manuscript has no theorem yielding such a pair.

**Derived-form note once multiplicity closes:**

$$
a \#_x b \; :\!\iff \; \mathrm{Det}(a,x) \wedge \mathrm{Det}(b,x) \wedge a\neq b \wedge \neg\mathrm{Coinc}(a,b).
$$

No primitive $(\mathcal B,\#)$ resurrection is needed.

---

## 6. Theorem or no-go on reiterability / recursive refinement

**Result:** Recursive refinement does **not** follow from PB1–PB5, E1, and WNF.

Reason: the package provides non-flat realizability together with positive witness structure, but it does not yet state when witness structure remains unresolved in a way that reactivates the same burden at a subordinate stage.

**Exact minimal additional principle required:**  
**RRP — Recursive Reapplication Principle**

> If a differentiated condition carries unresolved internal noncoincidence relative to the same pole-opposition burden, then a further differentiating resolving step is required.

This principle still has to be stated without hidden tree, graph, or temporal update structure.

---

## 7. Exact first remaining burden

At the level of the current primitive package plus E1, the **first remaining burden** is:

**WNF — Witnessed Non-Flatness Principle**

If WNF is admitted, the **next** remaining burden becomes:

**DWP — Determination-Witness Decomposability Principle**

That is the clean v12 dependency order.

---

## 8. Net manuscript consequence

This pass makes one thing much sharper:

- the first positive bridge after anti-flatness is **not** “many things,”
- it is **internal noncoincidence**,
- and plurality must still be earned one full step later.
