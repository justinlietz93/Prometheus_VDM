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
