# G‑CL‑1 — **Closure/Integrability Test (no hidden invariants)** (T1, paper‑only)

> **Path:** `Derivation/Closure/T1_PROPOSAL_G-CL-1_Closure-NoHiddenIntegrals_v1.md`

## 1. Tier / Title / Date

* **Tier:** T1 (Proto‑model)
* **Title:** Darboux/Kowalevski‑style non‑integrability for UMSL class under A4 degeneracies
* **Date:** {YYYY‑MM‑DD}

## 3. Abstract

For a restricted yet nontrivial UMSL class ( \partial_t q = J,\delta\mathcal I + M,\delta\Sigma ), apply **Darboux**/**Kowalevski** methods (or differential Galois/ziglin‑type criteria) to show **no analytic first integrals** exist beyond those forced by **A4** degeneracies. Alternatively, register a **counterexample search protocol**. Paper‑only.

## 5. Intellectual Merit and Procedure (paper‑only)

1. **Class definition.** Fix analytic potentials (V), polynomial (J(q)), and PSD (M(q)) structures satisfying A4; state regularity and domain.
2. **Normal forms.** Reduce near equilibria; compute resonance conditions; set up Kowalevski exponents.
3. **Non‑integrability criteria.** Apply chosen criterion to exclude additional first integrals; isolate the A4‑forced Casimirs.
4. **Fallback protocol.** If proof stalls, define an automated search over polynomial invariants of bounded degree with termination and logging (paper protocol only).

## 6. Gates

* **G‑CL‑1.1:** Theorem statement (restricted class + assumptions). **PASS**.
* **G‑CL‑1.2:** Criterion applied, concluding “no extra first integrals” beyond A4 Casimirs. **PASS** = derivation written.
* **G‑CL‑1.3 (Fallback):** Counterexample search protocol fully specified (space, degree, termination). **PASS**.

## 7. Risks / Kill‑Plans

* Class too broad: shrink scope until proofs close; **kill** if only heuristic arguments remain.
* Hidden symmetry: if discovered, document and reclassify as admissible Casimir (align with **A4**).

## 9. Canon Anchors

* **A4 (Dual Generators, degeneracies)**; **A2** context; equations registry for notation.
