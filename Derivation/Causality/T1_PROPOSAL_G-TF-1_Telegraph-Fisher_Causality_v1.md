# 4) G‑TF‑1 — **Telegraph–Fisher Causality Bridge (finite‑speed)** (T1, paper‑only)

> **Path:** `Derivation/Causality/T1_PROPOSAL_G-TF-1_Telegraph-Fisher_Causality_v1.md`

## 1. Tier / Title / Date

* **Tier:** T1 (Proto‑model)
* **Title:** Telegraph–Fisher bridge with admissible speed (c=\sqrt{D/\tau}) and cone‑slack inequality
* **Author:** Justin K. Lietz
* **Date:** 2025-11-04

## 3. Abstract

Derive the finite transport speed (c=\sqrt{D/\tau}) for the Telegraph–Fisher (TF) form and formalize the **cone‑slack** inequality that reconciles parabolic RD behavior with a **J‑branch** light cone (A2). State discretization constraints that preclude superluminal leakage under VDM stepper assumptions (paper‑only).

## 5. Intellectual Merit and Procedure (paper‑only)

1. **TF derivation.** From a Cattaneo/Maxwell relaxation, derive ( \tau \partial_{tt} u + \partial_t u = D\nabla^2 u + R(u) ) and its wavefront bound (c=\sqrt{D/\tau}).
2. **Cone‑slack inequality.** Prove an inclusion ( \mathcal{D}*{\text{RD}}(t)\subseteq \mathcal{C}*{J}(ct+\delta) ) with explicit slack (\delta) dependent on initial data norms.
3. **Discretization constraints.** Provide CFL‑style bounds (e.g., (\Delta t \le \min(\sqrt{\tau},\Delta x/\sqrt{D}, ; \hat c^{-1}\Delta x))) ensuring no super‑cone transport for the TF regularized RD step used within metriplectic composition.

## 6. Gates

* **G‑TF‑1.1:** Closed‑form derivation of (c=\sqrt{D/\tau}). **PASS**.
* **G‑TF‑1.2:** Cone‑slack inequality stated and proved. **PASS**.
* **G‑TF‑1.3:** Discrete admissibility conditions enumerated with justification. **PASS**.

## 7. Risks / Kill‑Plans

* Nonlinear (R(u)) breaking characteristics: restrict to small‑signal regime or provide comparison principle; **kill** if counterexample found.

## 9. Canon Anchors

* **A2 (Local causality)**; **A4** context for the JM coupling; equations registry for KG/RD instruments.
