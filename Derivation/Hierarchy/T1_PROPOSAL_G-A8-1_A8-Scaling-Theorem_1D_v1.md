# G‑A8‑1 — **A8 Scaling Theorem (1D Existence)** (T1, paper‑only)

> **Path:** `Derivation/Hierarchy/T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md`

## 1. Tier / Title / Date

* **Tier:** T1 (Proto‑model)
* **Title:** A8 in 1D: existence of $(N(L)=\Theta(\log(L/\lambda)))$ with boundary‑law energy
* **Author:** Justin K. Lietz
* **Date:** 2025-11-04

### 3. Abstract

Formulate and prove (in 1D) that finite‑energy configurations under a **tachyonic potential** (V''(0)<0) on large domains with stated BCs/regularity yield **logarithmic hierarchy depth** (N(L)=\Theta(\log(L/\lambda))) and **boundary‑law** excess energy (E_{\mathrm{exc}}(L)=\Theta(L^{d-1})) (constant in 1D). Provide a precise energy functional, assumptions, lemmas, and a proof outline. Include a **joint discriminator**: show ER/BA nulls can match (\log)-depth but fail the boundary‑law energy under the same estimator.

### 4. Background

* **Canon:** A8 scaling sits under A0–A7, with local causality A2 and metriplectic structure A4 as context; meters are defined in EQUATIONS/VALIDATION docs (no compute here). 

### 5. Intellectual Merit and Procedure (paper‑only)

1. **Energy & domain.** Define (E[\phi]=\int_0^L \frac{c^2}{2}(\partial_x\phi)^2+V(\phi),dx) with (V''(0)<0); BCs, function class (H^1).
2. **Pulled‑front tail lemma.** Prove an exponential tail bound ( |\phi(x)-\phi_\star|\le C e^{-x/\lambda}) for interface profiles (linearization at the unstable origin).
3. **Interface counting.** Show a minimal energy per interface (e_\star>0) and spacing constraints that imply (N(L)=\Theta(\log(L/\lambda))) to maintain finiteness of (E) as (L\to\infty).
4. **Boundary‑law energy.** Establish (E_{\mathrm{exc}}(L)=N(L)e_\star=\Theta(1)) in 1D (codimension‑1).
5. **Discriminator vs nulls.** Prove ER/BA constructions can reproduce (\log)-depth but not boundary‑law energy under identical estimators.

### 6. Gates

* **G‑A8‑1.1:** Theorem statement with all assumptions and constants declared. **PASS** = formal statement present.
* **G‑A8‑1.2:** Lemmas (tail, interface energy, spacing) proved or rigorously cited; **PASS**.
* **G‑A8‑1.3:** Joint discriminator formalized; **PASS** = nulls fail boundary‑law under same metric.

### 7. Risks / Kill‑Plans

* Edge‑case BCs making (e_\star=0): **kill** or restate theorem domain.
* Non‑generic potentials: add a structural condition (V\in\mathcal V) (e.g., double‑well w/ unstable origin).

### 9. Canon Anchors

* **Axioms A0–A7, esp. A2/A4**; meters live in **EQUATIONS.md** (reference only).
