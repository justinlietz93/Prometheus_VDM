# Non‑Equilibrium Thermodynamics (LIT) Standard for VDM

Version: 1.0  
Owner: VDM Canon  
Status: Adopted (misc‑standards)

## 1. Scope

This standard codifies the use of classical Linear Irreversible Thermodynamics (LIT) in the Void Dynamics Model (VDM) to:

- constrain the metric (dissipative) limb M in the A4 split,
- enforce Curie tensor‑rank selection rules (isotropic media),
- assess Onsager–Casimir reciprocity in the near‑equilibrium regime,
- instrument entropy production, including boundary entropy flux for wall/corner domains.

The standard does not alter VDM’s reversible/dissipative structure; it specifies near‑equilibrium auditing requirements and artifact outputs that operationalize A4/A5 gates with falsifiable checks.

## 2. Classification

- Axiom‑core linkage: A4 (dual generators), A5 (entropy non‑decrease).
- Runtime standard: implementation guidance for meters/instruments and runners.
- Canon discipline: equations and symbols are anchored to the derivation registry; this document does not duplicate canonical equations.

References (anchors):

- GENERIC structure: [VDM‑E‑140](Derivation/EQUATIONS.md#vdm-e-140) … [VDM‑E‑145](Derivation/EQUATIONS.md#vdm-e-145)
- Curie principle scalarization: [VDM‑E‑146](Derivation/EQUATIONS.md#vdm-e-146)
- KPIs: [kpi‑entropy‑prod‑nonneg](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg), [kpi‑curie‑compliance](Derivation/VALIDATION_METRICS.md#kpi-curie-compliance), [kpi‑curie‑violations](Derivation/VALIDATION_METRICS.md#kpi-curie-violations), [kpi‑onsager‑resid](Derivation/VALIDATION_METRICS.md#kpi-onsager-resid)

## 3. Objectives

VDM integrations shall:

1) reduce to the classical near‑equilibrium limit with force–flux structure J = L X,  
2) certify non‑negative entropy production (local density and integrated),  
3) enforce Curie selection rules for isotropic media via explicit masks,  
4) quantify Onsager–Casimir reciprocity residuals under declared parities,  
5) account for boundary entropy flux in wall/corner domains (e.g., OQ‑021).

## 4. Normative Requirements (MUST/SHALL)

R1. Force–flux structure  

- Implementations SHALL assemble near‑equilibrium forces X and use a phenomenological matrix L to compute fluxes J = L X for auditing. Construction of X and selection of basis are domain‑specific; isotropy assumptions SHALL be stated. Entropy production density and its integration SHALL follow canonical anchors; see [VDM‑E‑143](Derivation/EQUATIONS.md#vdm-e-143).

R2. Curie principle (isotropic scalarization)  

- Implementations SHALL apply a tensor‑rank mask to L (and where applicable to M/constitutive blocks) so that scalar↔vector↔tensor cross‑couplings forbidden by isotropy are zero. Compliance SHALL be recorded under [kpi‑curie‑compliance](Derivation/VALIDATION_METRICS.md#kpi-curie-compliance) with additional integer diagnostic [kpi‑curie‑violations](Derivation/VALIDATION_METRICS.md#kpi-curie-violations) = 0.

R3. Onsager–Casimir reciprocity residuals  

- Near equilibrium, implementations SHALL compute Frobenius and L∞ residual norms for L − E Lᵀ E with E = diag(ε_j), where parities ε_j ∈ {+1,−1} are explicitly declared. Residuals SHALL be logged as [kpi‑onsager‑resid‑fro] and [kpi‑onsager‑resid‑linf] per [kpi‑onsager‑resid](Derivation/VALIDATION_METRICS.md#kpi-onsager-resid). Runner‑specific tolerances MUST be stated.

R4. Entropy production non‑negativity (H‑theorem)  

- Metric‑leg audits SHALL report per‑cell entropy production density and integrated rates consistent with [kpi‑entropy‑prod‑nonneg](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg). For wall/corner domains, implementations SHALL additionally record boundary entropy flux time series.

R5. Boundary entropy flux (walls/corners)  

- For domains with physical boundaries (e.g., OQ‑021), implementations SHALL compute and log the boundary entropy flux (J_s) according to canonical entropy balance. Artifact outputs MUST include JSON and CSV time series; if available, a single‑panel PNG SHALL be produced.

R6. Artifact routing and provenance  

- All artifacts SHALL be routed using the repository I/O policy (figures to code/outputs/figures/{domain}, logs to code/outputs/logs/{domain}), include seed(s) and commit hash in JSON summaries, and adhere to CSV/JSON formatting standards specified by the canon.

R7. Scope limitation (minimum entropy production)  

- The minimum entropy production principle SHALL NOT be used as a general gate. If cited, its applicability conditions MUST be explicitly satisfied and recorded; otherwise, it is advisory only.

## 5. Implementation Guidance

Approved helper modules (reusable primitives):

- LIT helpers: [lit_tools.py](Derivation/code/common/instrument_helpers/lit_tools.py)  
  Provides:
  - build_L_isotropic_fluid(coeffs): constructs an isotropic L with heat (Fourier) and viscous blocks respecting Curie selection rules,
  - curie_mask(...) and apply_curie_zeroing(...),
  - onsager_casimir_residual(L, parity) with "fro" and "linf" norms,
  - entropy_production_density(X, L) and field integration utilities,
  - gate_report(...) returning σ extrema/negativity flag, Onsager residuals, and Curie violation count,
  - BoundaryEntropyFluxMonitor: boundary entropy flux time‑series monitor with JSON/CSV/PNG outputs,
  - write_lit_gate_artifacts(...): canonical KPI JSON writer for [kpi‑onsager‑resid‑{fro,linf}] and [kpi‑curie‑violations].

- GENERIC/meter primitives: [generic_helpers.py](Derivation/code/common/instrument_helpers/generic_helpers.py)  
  Provides structure checks, degeneracy residuals, and an entropy monitor aligned to [VDM‑E‑140..145](Derivation/EQUATIONS.md#vdm-e-140).

Runner example (OQ‑021 LIT audit):

- Code: [oq021_lit_runner.py](Derivation/code/physics/fluid_dynamics/oq021_lit_runner.py)  
- Schema: [oq021_lit_gates.schema.json](Derivation/code/physics/fluid_dynamics/schemas/oq021_lit_gates.schema.json)

## 6. Metrics and Acceptance Criteria

The following metrics SHALL be present in artifacts and SHALL conform to [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md):

M1. Entropy production non‑negativity  

- KPI: [kpi‑entropy‑prod‑nonneg](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg)  
- Gate: per‑step σ ≥ −ε; cumulative ΔΣ ≥ −ε (ε as specified by the runner; typical ε = 1e−12 in double precision).

M2. Curie compliance  

- KPI: [kpi‑curie‑compliance](Derivation/VALIDATION_METRICS.md#kpi-curie-compliance), [kpi‑curie‑violations](Derivation/VALIDATION_METRICS.md#kpi-curie-violations)  
- Gate: curie_ok = true and kpi‑curie‑violations = 0.

M3. Onsager–Casimir reciprocity  

- KPI: [kpi‑onsager‑resid](Derivation/VALIDATION_METRICS.md#kpi-onsager-resid) (fro, linf)  
- Gate: residuals ≤ declared tolerance for the near‑equilibrium regime (runner MUST declare tolerance value(s) and parity assignment).

M4. Boundary entropy flux (if applicable)  

- Output: JSON summary and CSV time series from BoundaryEntropyFluxMonitor; optional PNG time series panel. No universal sign constraint is imposed; reports SHALL include min/max/mean statistics.

## 7. Data and Artifact Requirements

- Minimum artifacts per audit/run (as applicable): 1 PNG figure, 1 CSV log, 1 JSON summary/log.  
- JSON formatting: indent=2, sort_keys=true; include seed(s), commit hash, and gate outcomes.  
- CSV formatting: header row, one record per sample; units and normalization MUST be documented.  
- Routing: via repository I/O helper policy; see io_paths in common.

## 8. Assumptions and Limits

- Local equilibrium: LIT auditing applies for small gradients and short relaxation times relative to observation.  
- Microreversibility: Onsager reciprocity auditing presumes appropriate parity assignment and regression hypothesis conditions.  
- Regularization: Near‑equilibrium LIT auditing does not supersede nonlinear regularization mechanisms (e.g., void‑debt); it complements them by certifying the small‑gradient limit.

## 9. Documentation Requirements

Authoring in RESULTS or domain READMEs SHALL:

- cite canonical anchors on first use (e.g., [VDM‑E‑146](Derivation/EQUATIONS.md#vdm-e-146) for Curie; LIT related KPIs as above),
- state parity assignments and tensor rank taxonomy used to construct the L basis,
- report declared tolerances for Onsager residuals and ε for entropy non‑negativity gates,
- include artifact path(s) for KPI JSON and boundary entropy flux outputs.

## 10. Change Log

- v1.0 (2025‑11‑08): Initial adoption. Introduces formal LIT standard for force–flux auditing, Curie/Onsager KPIs, and boundary entropy flux instrumentation for wall/corner domains. Aligns helper usage with repository instrument_helpers module paths and adds canonical KPI writers/monitors.

## 11. Bibliography (context)

- de Groot, S. R., & Mazur, P. (1984). Non‑Equilibrium Thermodynamics. Dover.  
- Öttinger, H. C. (2005). Beyond Equilibrium Thermodynamics. Wiley.  
- VDM canon anchors: [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/ALGORITHMS.md](Derivation/ALGORITHMS.md).

## T2 Instrument Certification Framework (Meters-first, no phenomena claims)

This section registers the certification plan for the four non-equilibrium meter stacks referenced in:

- [docs/misc-standards/Oettinger_Upgrade_Map.md](Oettinger_Upgrade_Map.md)
- [docs/misc-standards/DeGrand-DeTar_Upgrade_Map.md](DeGrand-DeTar_Upgrade_Map.md)
- [docs/misc-standards/Self-Organization_Upgrade_Map.md](Self-Organization_Upgrade_Map.md)

Scope: certify each meter as a T2 Instrument with falsifiable gates, datasets, runners, and artifact policy. No physics claims are made at T2; failures route to failed_runs/ with contradiction reports.

---

### A) GENERIC Structure Meter (Öttinger)

Canon anchors and KPIs:

- Evolution/structure: [VDM-E-140..146](../Derivation/EQUATIONS.md#vdm-e-140)  
- KPIs: Poisson–Jacobi residual, degeneracy residuals, entropy nonnegativity, Curie compliance  
  See [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md)

Instrument definition (what is certified):

- Correctness of the metriplectic scaffolding: bracket identity (restricted basis), degeneracies (L∇S=0, M∇E=0), non-negative entropy production, and Curie scalarization of admissible couplings.

Gates (pass/fail, hard numbers):

- Jacobi residual e_Jacobi ≤ 1e−12 (basis-restricted; histogram QQ-plot recorded)
- Degeneracy residuals g1=||L∇S||∞ ≤ 1e−12, g2=||M∇E||∞ ≤ 1e−12
- Entropy production monitor: per-step σ ≥ −1e−12 and cumulative ΔΣ ≥ −1e−12
- Curie compliance: curie_ok = true and kpi-curie-violations = 0

Datasets/benches:

- Synthetic extended-hydrodynamics blocks with known Casimirs and isotropic constitutive forms; grid-refined ladders (N∈{64,128,256})

Runner and artifacts:

- Planned runner: Derivation/code/physics/metriplectic/generic_instrument_runner.py
- Artifacts per run: PNG panels (Jacobi hist, σ(t)), CSV time series, JSON gate summary with commit+seeds

Promotion file (proposal path):

- Derivation/Metriplectic/T2_PROPOSAL_GENERIC_Structure_Meter_v1.md

---

### B) HMC Exactness Meter (DeGrand & DeTar)

Canon anchors and KPIs:

- Acceptance vs stepsize (leapfrog): [VDM-E-130](../Derivation/EQUATIONS.md#vdm-e-130), [kpi-hmc-acceptance-vs-stepsize](../Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize)
- ΔH hist diagnostics: [VDM-E-131](../Derivation/EQUATIONS.md#vdm-e-131), [kpi-hmc-deltaH-hist](../Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist)

Instrument definition:

- Quality of reversible, volume-preserving proposals plus Metropolis correction, measured via predicted scaling of 1−α(ε) and ΔH statistics.

Gates:

- Acceptance scaling: fit 1−α ≈ k ε^p on log–log; require p ∈ [3.5, 4.5], R² ≥ 0.98
- ΔH hist: |median(ΔH)| ≤ 5·MAD/√N; |skew(ΔH)| ≤ 0.5 per ε; moments JSON recorded

Datasets/benches:

- Gaussian/quadratic targets; fixed path length L; ε ladder across 5–7 points; ≥ 100 trajectories per ε

Runner and artifacts:

- Planned runner: Derivation/code/physics/hmc/hmc_instrument_runner.py
- Artifacts: Acceptance-vs-ε plot (PNG) with fit CSV/JSON; ΔH histogram panels + JSON moments per ε; commit+seeds in captions

Promotion file (proposal path):

- Derivation/MonteCarlo/T2_PROPOSAL_HMC_Exactness_Meter_v1.md

---

### C) LIT Core Meter (Near-Equilibrium — Representation/Reciprocity/Curie/Boundary)

Canon anchors and KPIs:

- Entropy production structure: [VDM-E-143](../Derivation/EQUATIONS.md#vdm-e-143)
- KPIs: representation invariance, Onsager–Casimir residuals, Curie violations, open-system entropy balance, Φ monotonicity, rotation split
  See [Derivation/VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md) and helper APIs in [Derivation/code/common/instrument_helpers/prigogine_gates.py](../Derivation/code/common/instrument_helpers/prigogine_gates.py)

Instrument definition:

- Coordinate-free correctness and isotropy of the LIT layer plus boundary-entropy accounting on conduction benches.

Gates:

- Repr invariance: max_rel(Δ_repr) ≤ 1e−12 (Haar A); ≤ 1e−10 (cond(A)≤10)
- Onsager residuals: ||L−EL^T E||_F ≤ tol_F; ||·||_∞ ≤ tol_∞ (runner-declared)
- Curie: curie_ok = true; kpi-curie-violations = 0
- Open balance closure: |production − boundary − dS/dt| ≤ ε (declared)
- Φ(T,T0) monotonic: ΔΦ ≤ 1e−12 per step
- Rotation split: ||antisym(M)||∞ ≤ 1e−12; min eig(sym(M)) ≥ −1e−12

Datasets/benches:

- 2D conduction with Dirichlet walls; synthetic L blocks for parity tests; controlled transforms for repr-invariance trials

Runner and artifacts:

- Planned runner: Derivation/code/physics/thermodynamics/lit_instrument_runner.py
- Artifacts: JSON gate summaries, Φ(t) PNG+CSV, boundary-flux JSON, optional bar charts for χ_cross

Promotion file (proposal path):

- Derivation/Thermodynamics/T2_PROPOSAL_LIT_Core_Meter_v1.md

---

### D) Self-Organization Onset Meter (Nicolis–Prigogine)

Canon anchors and KPIs:

- EEP/branch diagnostics: [VDM-E-150..153](../Derivation/EQUATIONS.md#vdm-e-150)
- KPIs: [kpi-eep-trend](../Derivation/VALIDATION_METRICS.md#kpi-eep-trend), [kpi-bifurcation-card](../Derivation/VALIDATION_METRICS.md#kpi-bifurcation-card), [kpi-localized-structure](../Derivation/VALIDATION_METRICS.md#kpi-localized-structure), [kpi-branch-classifier](../Derivation/VALIDATION_METRICS.md#kpi-branch-classifier), [kpi-branch-stability-plot](../Derivation/VALIDATION_METRICS.md#kpi-branch-stability-plot)

Instrument definition:

- Meters that indicate approach to onset and classify branches without asserting a phenomenon beyond instrument calibration.

Gates:

- EEP trend non-increasing near equilibrium: worst positive tail slope ≤ 1e−12
- Bifurcation detection: sign change in Re(λ1) with min |Re(λ1)| ≤ 1e−6
- Branch classifier consistency: thermo/hopf/dissipative label agrees with EEP trend + spectrum + mode presence
- Localized detector: report-only at T2; when used as phenomenon support later, require ≥1 component + measures
- Overlay: report-only at T2; consistency annotations recommended

Datasets/benches:

- Linear RD around homogeneous state (analytic dispersion controls); simple Schnakenberg/Turing-like toy at parameters near first bifurcation; conduction benches for Φ

Runner and artifacts:

- Planned runner: Derivation/code/physics/self_org/self_org_instrument_runner.py
- Artifacts: EEP series (PNG/CSV/JSON), bifurcation cards (JSON + optional eigenmode PNG), localized overlays (PNG/JSON), branch-stability overlay PNG

Promotion file (proposal path):

- Derivation/Nonequilibrium/T2_PROPOSAL_Self_Organization_Meters_v1.md

---

### Certification logistics (common to all)

- Determinism receipts: record seeds, commit hashes, environment summary in JSON sidecars (RESULTS standards)
- Artifact policy: each figure must have CSV/JSON with same basename; numeric captions include key metrics (slope, R², CI)
- Failure handling: emit CONTRADICTION_REPORT.json and route to failed_runs/ on any gate failure
- Approval: proposals require formal approval (see Derivation/code/ARCHITECTURE.md and authorization README)
- CI hooks: add minimal runners to CI with seed=0 smoke; nightly expanded seeds/grids

Status

- All four instruments: “Planned for T2 certification.” This document registers the certification plan. Individual T2 PROPOSAL_* files will be added in their respective domains with identical gates and artifact requirements, referencing the same canon anchors and KPIs.
