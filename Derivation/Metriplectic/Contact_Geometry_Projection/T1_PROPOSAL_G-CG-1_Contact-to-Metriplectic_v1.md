# G‑CG‑1 — **Contact Geometry Projection → Metriplectic Split** (T1, paper‑only)

> **Path:** `Derivation/Metriplectic/Contact_Geometry_Projection/T1_PROPOSAL_G-CG-1_Contact-to-Metriplectic_v1.md`
> Provenance fields as above.

## 1. Tier / Title / Date

* **Tier:** T1 (Proto‑model)
* **Title:** Contact Hamiltonian flows projecting to (J\oplus M) with A4 degeneracies
* **Date:** {YYYY‑MM‑DD}

## 3. Abstract

Specify a **contact manifold** ((\mathcal M,\eta)) with Reeb vector (R) and **contact Hamiltonian** (H_c) whose flow decomposes into a symplectic part (on (\ker\eta)) and a metric/dissipative part (along (R)), yielding a metriplectic pair ((J,M)) that satisfies **A4** degeneracies. Provide explicit (\eta), (R), projection maps, and a proof sketch of the degeneracy conditions.

## 5. Intellectual Merit and Procedure

1. **Data:** define (\eta = d\Sigma - p_i,dX^i) (or equivalent), compute **Reeb** (R) via (\eta(R)=1), (d\eta(R,\cdot)=0).
2. **Splitting:** decompose the contact vector field (X_{H_c}) into (X_{\parallel}\propto R) and (X_{\perp}\in\ker\eta).
3. **Projections → brackets:** define (J) from the symplectic form (d\eta|_{\ker\eta}); define (M) from a Riemannian structure induced along (R) (or via a metric on the contact distribution plus a Rayleigh dissipation functional).
4. **Degeneracies:** prove (J\cdot\delta\Sigma=0) (Casimir of (J) from (\eta)-structure) and (M\cdot\delta\mathcal I=0) (choose (\mathcal I) orthogonal in the metric direction).
5. **Minimal example:** a 1‑DOF contact system with explicit (\eta), (H_c), (R), (J), (M).

## 5.1 Mathematical Setup & Diagnostics

* **Objects:** ((\mathcal M,\eta,R,H_c)), projections (P_{\perp}, P_{\parallel}), brackets ({\cdot,\cdot}_J), ((\cdot,\cdot)_M).
* **Diagnostics:** verify (J^\top=-J), (M^\top=M\ge0), and the two degeneracies on chosen functionals (\Sigma,\mathcal I).

## 6. Gates

* **G‑CG‑1.1:** Reeb construction fully specified; **PASS** = ( \eta(R)=1,, d\eta(R,\cdot)=0) shown.
* **G‑CG‑1.2:** Projection formulas yield explicit (J,M); **PASS** = closed forms given.
* **G‑CG‑1.3:** **A4** degeneracies proved; **PASS** = identities established.  

## 7. Risks / Kill‑Plans

* Inconsistent metric choice along (R) (breaks PSD): **kill**.
* Dependence on coordinates (non‑invariant degeneracy): **kill**; restate invariantly in contact data.

## 9. Canon Anchors

* **A4**, **A2** context; **EQUATIONS.md** for metriplectic master.
