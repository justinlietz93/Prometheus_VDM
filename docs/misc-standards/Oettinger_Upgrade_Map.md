# Öttinger → VDM Upgrade Map (GENERIC discipline)

Source reference (do not duplicate content):

- Book: [Beyond Equilibrium Thermodynamics — Hans Christian Öttinger (Wiley, 1998)](../Derivation/References/Thermodynamics/Beyond Equilibrium Thermodynamics -- Hans Christian Öttinger -- 1_ Auflage, 1998 -- John Wiley & Sons, Ltd.pdf)

Purpose:

- This navigator maps Öttinger’s GENERIC formalism (E,S,L,M) to canonical VDM anchors across EQUATIONS, VALIDATION_METRICS, ALGORITHMS, and RESULTS standards.
- It records where axioms A4/A5 are enforced via testable gates and where extended hydrodynamics (corner regularization, OQ‑021) plugs in.
- No equations or numbers are re-stated here; follow the anchors.

---

## 1) Canon equations added (GENERIC, entropy, structure)

- GENERIC evolution and properties
  - Evolution law: [VDM-E-140](../Derivation/EQUATIONS.md#vdm-e-140)
  - Poisson bracket and Jacobi identity + residual definition: [VDM-E-141](../Derivation/EQUATIONS.md#vdm-e-141)
  - Degeneracy conditions (Casimirs): [VDM-E-142](../Derivation/EQUATIONS.md#vdm-e-142)
  - Entropy production (H‑theorem), discrete monitor: [VDM-E-143](../Derivation/EQUATIONS.md#vdm-e-143)

- Extended hydrodynamics structural variable c (void‑debt as internal variable)
  - Entropy functional and chemical potential μ_c: [VDM-E-144](../Derivation/EQUATIONS.md#vdm-e-144)
  - Metric blocks for c‑relaxation and viscous coupling; entropy production density split: [VDM-E-145](../Derivation/EQUATIONS.md#vdm-e-145)
  - Curie principle compliance (scalarization of couplings): [VDM-E-146](../Derivation/EQUATIONS.md#vdm-e-146)

- Scale program (RG blocking)
  - RG blocking operator and rescaling: [VDM-E-136](../Derivation/EQUATIONS.md#vdm-e-136)

Context pointers:

- Contact/GENERIC program in this repo: [CF2_Contact_to_Metriplectic_Evolution.md](../Derivation/Complete-Formalisms/CF2_Contact_to_Metriplectic_Evolution.md)

---

## 2) Validation metrics (KPIs) introduced

GENERIC structure gates:

- Poisson–Jacobi residual (unit test): [kpi-poisson-jacobi-resid](../Derivation/VALIDATION_METRICS.md#kpi-poisson-jacobi-resid)
- Degeneracy residuals (Casimirs): [kpi-degeneracy-resid](../Derivation/VALIDATION_METRICS.md#kpi-degeneracy-resid)
- Entropy non-negativity (H‑theorem monitor): [kpi-entropy-prod-nonneg](../Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg)
- Curie principle compliance (audit): [kpi-curie-compliance](../Derivation/VALIDATION_METRICS.md#kpi-curie-compliance)

Corner regularization (OQ‑021) gates:

- Corner stress boundedness: [kpi-corner-stress-bound](../Derivation/VALIDATION_METRICS.md#kpi-corner-stress-bound)
- Corner velocity cap + scaling collapse envelope: [kpi-corner-velocity-cap](../Derivation/VALIDATION_METRICS.md#kpi-corner-velocity-cap)
- Corner entropy non‑divergence (σ, ΔΣ): [kpi-corner-entropy-nondiv](../Derivation/VALIDATION_METRICS.md#kpi-corner-entropy-nondiv)

RG/scale program:

- RG blocking collapse envelope: [kpi-rg-collapse](../Derivation/VALIDATION_METRICS.md#kpi-rg-collapse)

HMC context (J‑flow sampler QC — DeGrand & DeTar, already present but related to A4):

- Acceptance vs stepsize slope: [kpi-hmc-acceptance-vs-stepsize](../Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize)
- ΔH histogram diagnostics: [kpi-hmc-deltaH-hist](../Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist)

---

## 3) Algorithms/pseudocode stubs (adapters and runners)

GENERIC conformance and audits:

- VDM‑GENERIC adapter (constructor + gates): [VDM-A-037](../Derivation/ALGORITHMS.md#vdm-a-037)
- Hydrodynamic Poisson construction cookbook skeleton: [VDM-A-038](../Derivation/ALGORITHMS.md#vdm-a-038)
- Poisson–Jacobi identity tester (unit-test harness): [VDM-A-039](../Derivation/ALGORITHMS.md#vdm-a-039)
- Entropy production monitor (σ(t), ΔΣ): [VDM-A-040](../Derivation/ALGORITHMS.md#vdm-a-040)
- Curie compliance linter (tensorial scalarization): [VDM-A-041](../Derivation/ALGORITHMS.md#vdm-a-041)

OQ‑021 corner test runner:

- Corner regularization runner skeleton (c‑field): [VDM-A-042](../Derivation/ALGORITHMS.md#vdm-a-042)

RG utility:

- Blocking operator (field/observable) for scale collapse: [VDM-A-036](../Derivation/ALGORITHMS.md#vdm-a-036)

---

## 4) RESULTS authoring requirements (when using GENERIC/dissipation)

Authoring standards now require:

- GENERIC block declaration (E,S,L,M) and enforcement artifacts:
  - See “GENERIC metriplectic diagnostics” section in [RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
  - Explicit KPI artifacts for Jacobi residual, degeneracy residuals, entropy monitor, Curie audit
- For OQ‑021: figures + CSV/JSON for corner stress, velocity collapse envelope, and entropy non‑divergence

---

## 5) Axiom cross-links (A4, A5)

- A4 (Dual generators, metriplectic split) now references GENERIC anchors and KPI gates:
  - See in-place additions in [AXIOMS.md](../Derivation/AXIOMS.md) under A4 notes linking to:
    - [VDM-E-140](../Derivation/EQUATIONS.md#vdm-e-140) … [VDM-E-146](../Derivation/EQUATIONS.md#vdm-e-146)
    - [kpi-poisson-jacobi-resid](../Derivation/VALIDATION_METRICS.md#kpi-poisson-jacobi-resid), [kpi-degeneracy-resid](../Derivation/VALIDATION_METRICS.md#kpi-degeneracy-resid), [kpi-entropy-prod-nonneg](../Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg), [kpi-curie-compliance](../Derivation/VALIDATION_METRICS.md#kpi-curie-compliance)

- A5 (Entropy law) note tightened to require per‑step and cumulative non‑negativity with artifacts:
  - See modified A5 note in [AXIOMS.md](../Derivation/AXIOMS.md#vdm-ax-a5) referencing [VDM-E-143](../Derivation/EQUATIONS.md#vdm-e-143) and [kpi-entropy-prod-nonneg](../Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg)
  - For corner work, A5 note points to OQ‑021 KPIs; c‑field definitions at [VDM-E-144](../Derivation/EQUATIONS.md#vdm-e-144), [VDM-E-145](../Derivation/EQUATIONS.md#vdm-e-145)

---

## 6) Operationalization notes

- Construction discipline:
  - Build L(q) by variable taxonomy (scalars/vectors/tensors) and verify antisymmetry and Jacobi via [VDM-A-039](../Derivation/ALGORITHMS.md#vdm-a-039).
  - Build M(q) to be symmetric PSD, respecting [VDM-E-146](../Derivation/EQUATIONS.md#vdm-e-146) (Curie), and enforce [VDM-E-142](../Derivation/EQUATIONS.md#vdm-e-142) (M∇E=0).

- Monitors and gates:
  - Always run the entropy monitor [VDM-A-040](../Derivation/ALGORITHMS.md#vdm-a-040) and record σ(t), ΔΣ artifacts; gate per [kpi-entropy-prod-nonneg](../Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg).
  - For extended hydrodynamics with c, use corner KPIs and report Λ, De_c, Pe_c (dimensionless groups) in Results “Variables.”

- Scale program:
  - Use [VDM-A-036](../Derivation/ALGORITHMS.md#vdm-a-036) and [VDM-E-136](../Derivation/EQUATIONS.md#vdm-e-136) for blocking/collapse; gate per [kpi-rg-collapse](../Derivation/VALIDATION_METRICS.md#kpi-rg-collapse).

---

## 7) Scope, risks, and non-goals

- Scope:
  - These anchors assert and test the GENERIC structure at the instrument level (T2). They do not introduce new physics claims beyond standard non-equilibrium thermodynamics.

- Risks:
  - Jacobi residual tests rely on a basis of functionals; ensure the basis is rich (localized probes + linear forms).
  - Entropy monitor depends on discretization details (DG vs continuous); declare the method and tolerance.

- Non-goals:
  - No duplication of the book’s derivations; this document is a routing map only.
  - No new constants or units are defined here; link to canonical registries when needed.

---

## 8) Quick checklist for new metriplectic modules

1) Define (E,S,L,M).  
2) Run VDM‑GENERIC adapter [VDM-A-037](../Derivation/ALGORITHMS.md#vdm-a-037).  
3) Pass Jacobi residual [kpi-poisson-jacobi-resid](../Derivation/VALIDATION_METRICS.md#kpi-poisson-jacobi-resid).  
4) Pass degeneracy residuals [kpi-degeneracy-resid](../Derivation/VALIDATION_METRICS.md#kpi-degeneracy-resid).  
5) Run entropy monitor [VDM-A-040](../Derivation/ALGORITHMS.md#vdm-a-040) and pass [kpi-entropy-prod-nonneg](../Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg).  
6) Curie audit [kpi-curie-compliance](../Derivation/VALIDATION_METRICS.md#kpi-curie-compliance).  
7) If applicable: RG collapse [kpi-rg-collapse](../Derivation/VALIDATION_METRICS.md#kpi-rg-collapse), or OQ‑021 corner KPIs.  
8) Author Results to the GENERIC section in [RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md).
