<!-- White Paper Proposal based on Templates/PROPOSAL_PAPER_TEMPLATE.md -->

# T1 (Proto-model) - Telegraph–Fisher (TF) Causality Instrument: Finite-Speed Transport and Cone Gates

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  
> Calibrate and validate the finite propagation speed $c=\sqrt{D/\tau}$ and cone consistency for Telegraph–Fisher transport with dispersion and cone gates, producing PNG/CSV/JSON artifacts via the io helper.

Practical Provenance pattern (see template):

- Pre-register salted hashes and tag before any artifact-writing run; store base_sha256, salt_hex, salted_sha256 in PRE-REGISTRATION.json; tag must be included in run logs and captions.

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Principal Investigator, approval authority

---

## 3. Abstract

Proposed is a T1 instrument to certify finite-speed transport in the hyperbolic–diffusive regime (“Telegraph–Fisher”, TF). The instrument estimates and validates the characteristic speed
$$
c \;=\; \sqrt{\frac{D}{\tau}}
$$
as registered in [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105), with acceptance gates: (i) dispersion fits with $R^2\ge 0.999$ matching predicted slope/intercept; (ii) locality cone with measured $v\le c(1+0.02)$; (iii) CFL/stability envelope checks. The design is compatible with metriplectic compositions (J⊕M), but this proposal limits scope to TF causality meters and cones. Artifacts (PNG/CSV/JSON) are routed with deterministic seeds and commit hashes via the io helper for regression and reproducibility.

---

## 4. Background & Scientific Rationale

Canon anchors and audits:

- TF speed and cone summary (spec-level): [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105); program text in [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:326-333).  
- Causality envelope and cone-dominance audits: [audits/2025-11-04_A8_Bridges_Status.md](audits/2025-11-04_A8_Bridges_Status.md:104-118).  
- J-only baselines for cones/dispersion: [RESULTS_KG_Jonly_Locality_and_Dispersion.md](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md).  
- Canon gates: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md) (KG J-only dispersion $R^2\ge 0.999$, cone $v\le c(1+0.02)$; two-grid, identity residuals for composition checks).

Motivation:

- Resolve causality rigor by replacing parabolic instantaneous-propagation models with TF-type propagation that admits a finite cone and analytically trackable dispersion.  
- Provide standardized, machine-auditable meters for cone measurement, $c$ estimation, and regression against predicted $c=\sqrt{D/\tau}$.

Assumptions and limitations:

- Analysis is conducted under regimes where TF reduction is valid (moment closure with finite $\tau$ and diffusivity $D$).  
- Scope excludes phenomenon claims (T2+); the instrument certifies meters and gates to be used upstream of physics claims.

---

## 5. Intellectual Merit and Procedure

- Importance: Establishes a reproducible meter for finite-speed transport and light-cone analogs in VDM, foundational for locality-centric gates and for J⊕M compositions.  
- Broader impacts: Enables change-impact assessments (CFL tuning, discretization variants) and supports causality audits (e.g., TE-based DAG using TF cone for delay prediction).  
- Approach: Simulate TF PDE configurations; estimate $c$ from fronts and dispersion; fit to $c=\sqrt{D/\tau}$; validate cones and regression against gate thresholds.

---

## 5.1 Experimental Setup and Diagnostics

Known parameters and normalization (per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)):

- Grid: $N$, $\Delta x$; time: $T$, $\Delta t$; seeds.  
- TF parameters: $\{D,\tau\}$; optional reaction term $f(u)$ for TF–Fisher variants (kept smooth, bounded).  
- Boundary/IC: periodic or reflecting; localized IC for front measurements; broadband small-amplitude IC for dispersion.

Diagnostics (minimum set per run):

- $c$ from fronts: front position vs time regression (quantile threshold or centroid methods) $\Rightarrow$ $\widehat{c}_{\text{front}}$.  
- Dispersion fits: $\omega(k)$ or phase/group-velocity estimation; regression $R^2$ against analytic target; residual plots.  
- Cone check: measured leading-edge speed $v$ vs cone bound $c(1+0.02)$.  
- Stability/CFL envelope: runs across $(\Delta t,\Delta x)$ grid with acceptance region logged; flag violations.

New meter scripts (commit before runs):

- TF simulator: Derivation/code/physics/metriplectic/tf/sim_tf.py  
- Front/cone meter: Derivation/code/physics/metriplectic/tf/meter_cone.py  
- Dispersion meter: Derivation/code/physics/metriplectic/tf/meter_dispersion.py  
- Runner: Derivation/code/physics/metriplectic/tf/run_tf_causality.py

Required parameters and defaults (example T1 set):  

- $(N,\Delta x,\Delta t,T)=(1024,0.5,1\times 10^{-3},50)$; seeds $=10$; $(D,\tau)=(1.0,1.0)$ giving $c=1$; IC: compact bump (front) and broadband small-amplitude (dispersion).

### 5.1.1 Pre-Run Config Requirements

Approval discipline is mandatory (see [authorization/README.md](Derivation/code/common/authorization/README.md)).

Required config and metadata:

- Approvals: Derivation/code/physics/metriplectic/APPROVAL.json  
- Schemas: Derivation/code/physics/metriplectic/schemas/  
  - tf-causality.v1.schema.json  
- Specs: Derivation/code/physics/metriplectic/specs/  
  - tf-causality-run.v1.json

PRE-REGISTRATION.json (minimum keys; fill at prereg):

```json
{
  "proposal_title": "T1 - TF Causality Instrument (Finite Speed and Cone Gates)",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Measured cone speed v satisfies v ≤ c(1+0.02) with c=√(D/τ).", "direction": "decrease" },
    { "id": "H2", "statement": "Dispersion regression achieves R² ≥ 0.999 on approved k-band.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["Δt","Δx","D","τ"],
    "dependent": ["c_hat_front","cone_violation_rate","dispersion_R2"],
    "controls": ["seed","IC_kind","BC_kind"]
  },
  "pass_fail": [
    { "metric": "cone_violation_rate", "operator": "<=", "threshold": 0.0, "unit": "-" },
    { "metric": "dispersion_R2", "operator": ">=", "threshold": 0.999, "unit": "-" }
  ],
  "spec_refs": ["Derivation/code/physics/metriplectic/specs/tf-causality-run.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

Specs (example):

```json
{
  "run_name": "tf-causality-baseline",
  "version": "1.0.0",
  "tag": "tf-causality.v1",
  "schema_ref": "Derivation/code/physics/metriplectic/schemas/tf-causality.v1.schema.json",
  "parameters": {
    "N": 1024, "dx": 0.5, "dt": 0.001, "T": 50,
    "D": 1.0, "tau": 1.0,
    "ic_kind": "compact-bump", "bc_kind": "periodic",
    "k_band": [0.1, 2.0]
  },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

Schemas (skeleton):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tf-causality.v1.schema.json",
  "title": "Telegraph–Fisher Causality - v1",
  "type": "object",
  "properties": {
    "N": { "type": "integer", "minimum": 64 },
    "dx": { "type": "number", "exclusiveMinimum": 0 },
    "dt": { "type": "number", "exclusiveMinimum": 0 },
    "T": { "type": "number", "exclusiveMinimum": 0 },
    "D": { "type": "number", "exclusiveMinimum": 0 },
    "tau": { "type": "number", "exclusiveMinimum": 0 },
    "ic_kind": { "type": "string", "enum": ["compact-bump","broadband-small"] },
    "bc_kind": { "type": "string", "enum": ["periodic","reflecting"] },
    "k_band": { "type": "array", "items": { "type": "number" }, "minItems": 2, "maxItems": 2 }
  },
  "required": ["N","dx","dt","T","D","tau","ic_kind","bc_kind","k_band"]
}
```

---

## 5.2 Experimental runplan

Plan:

1) Generate TF runs over $(\Delta t,\Delta x)$ for fixed $(D,\tau)$; measure cone from front tracking; compute dispersion on broadband ICs over approved $k$ band.  
2) Estimate $\widehat{c}_{\text{front}}$ and compare to $c=\sqrt{D/\tau}$; register any cone violations $v>c(1+0.02)$.  
3) Fit dispersion curves; compute $R^2$; record residuals and gate outcomes.  
4) Repeat across seeds and parameter sweeps; log CFL/stability envelope.

Success (pass gates):

- Zero cone violations across seeds within measurement tolerance; dispersion $R^2\ge 0.999$.  
- Stability envelope logged without excursions during accepted runs.

Failure actions:

- Route artifacts to failed_runs/ with contradiction JSON (commit/tag, seeds, metrics, diffs); no narrative claims are made.

Artifacts and routing:

- Figures (cone plots, dispersion curves): Derivation/code/outputs/figures/metriplectic/tf_causality/  
- Logs (CSV metrics, JSON run log): Derivation/code/outputs/logs/metriplectic/tf_causality/  
- All via [io_paths.py](Derivation/code/common/io_paths.py); record seeds and commit/tag in JSON.

Compute budget:

- Front tracking and dispersion FFTs are O($N\log N$) per frame; for $(N=1024,T=50)$ runs complete in minutes per seed on CPU; sweeps scale linearly.

---

## 6. Personnel

- Justin K. Lietz — design, approvals, and review; ensures adherence to authorization and artifact policies; signs prereg tags; reviews metrics vs [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md).

---

## 7. References

- TF speed and cones: [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105); [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:326-333)  
- Audits and envelope notes: [audits/2025-11-04_A8_Bridges_Status.md](audits/2025-11-04_A8_Bridges_Status.md:104-118)  
- Authorization & results standards: [authorization/README.md](Derivation/code/common/authorization/README.md), [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---
