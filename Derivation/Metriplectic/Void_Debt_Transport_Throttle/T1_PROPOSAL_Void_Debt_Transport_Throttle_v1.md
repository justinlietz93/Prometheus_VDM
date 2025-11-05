<!-- White Paper Proposal based on Templates/PROPOSAL_PAPER_TEMPLATE.md -->

# T1 (Proto-model) - Void-Debt Transport Throttling Instrument: $c_{\mathrm{eff}}=c_0 \exp(-\tfrac{1}{2}\beta D)$ Gates

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  
> Define and validate a metriplectic instrument that estimates void-debt $D$ from boundary concentration and verifies the transport throttling law $c_{\mathrm{eff}}=c_0\,\exp(-\tfrac{1}{2}\beta D)$ with reproducible gates and artifacts.

Practical Provenance pattern (see template):

- Pre-register salted hashes and tag before any artifact-writing run; store base_sha256, salt_hex, salted_sha256 in PRE-REGISTRATION.json; tag must be included in run logs and figure/CSV/JSON artifacts.

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Principal Investigator, approval authority

---

## 3. Abstract

Proposed is a T1 metriplectic instrument to quantify “void-debt” $D$—a boundary concentration measure—and to validate the effective transport throttling law
$$
c_{\mathrm{eff}} \;=\; c_0 \,\exp\!\big(-\tfrac{1}{2}\,\beta\, D\big),
$$
as compiled in [VDM-E-106](Derivation/EQUATIONS.md#vdm-e-106), with supportive context in the Unification hyper‑proposal (effective speed throttling notes). The instrument specifies a data-driven estimator $\widehat{D}$ from interface statistics, calibrates $\beta$, and gates attenuation consistency across seeds and parameter sweeps. Artifacts are routed via the io helper (PNG/CSV/JSON) with deterministic provenance. This instrument makes no phenomenon claim (≤T2); it standardizes meters and gates for downstream physics proposals.

---

## 4. Background & Scientific Rationale

Canon anchors:

- Throttling law (spec-level): [VDM-E-106](Derivation/EQUATIONS.md#vdm-e-106); references in [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:52-56,330-331).  
- Related A8 hierarchy and area-law context used for $D$ estimation (interface statistics): [VDM-E-107](Derivation/EQUATIONS.md#vdm-e-107), [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113).  
- Metriplectic gates and identity/degeneracy baselines: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [VDM-E-101](Derivation/EQUATIONS.md#vdm-e-101), [VDM-E-099](Derivation/EQUATIONS.md#vdm-e-099).

Rationale:

- Boundary concentration reduces effective transport channels; a scalar $D$ constructed from codimension‑1 measures provides a macroscopic throttling control.  
- A standardized instrument for $(D,\beta)$ linking and $c_{\mathrm{eff}}$ verification improves reproducibility of locality and rate‑limiting analysis across domains (RD, TF, metriplectic compositions).

Assumptions and limitations:

- $D$ estimation relies on interface detection and scale aggregation; estimator families are compared (count‑based, perimeter‑normalized, multiscale/structure tensor proxies).  
- Calibration uses controlled regimes where $c_0$ is known (e.g., J‑only $c_0=c$) or measured independently (TF cones); uncertainty bands are reported.

---

## 5. Intellectual Merit and Procedure

- Importance: Introduces a machine‑auditable throttling meter connecting boundary statistics to effective speed suppression, enabling cross‑runner regression and policy checks.  
- Broader impacts: Bridges hierarchy measurements (A8) with transport cones (TF) and metriplectic diagnostics; clarifies rate limiting in coupled J⊕M evolutions.  
- Approach: Construct $\widehat{D}$ from simulation fields; estimate $c_{\mathrm{eff}}$ by cones/dispersion; fit $c_{\mathrm{eff}}/c_0$ vs $D$ to $\exp(-\tfrac{1}{2}\beta D)$; test attenuation gates and residuals across seeds and grids.

---

## 5.1 Experimental Setup and Diagnostics

Normalization and parameters (per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)):

- Spatial grid: $N$, $\Delta x$; temporal: $\Delta t$, $T$; seeds $S$.  
- Transport regime: select either J‑only baselines (for $c_0$) or TF (for $c_0=\sqrt{D/\tau}$); optionally metriplectic compositions for stress‑tests.  
- Boundary detector settings: threshold $\theta$, scale pyramid levels $L_s$, morphological kernel sizes.

Diagnostics (minimum set per run):

- Void‑debt estimator(s): $\widehat{D}_{\text{count}}$, $\widehat{D}_{\text{per}}$, $\widehat{D}_{\text{ms}}$ with normalization to $[0,1]$ or unit‑consistent scaling; consistency checks among estimators reported.  
- Effective speed: $\widehat{c}_{\mathrm{eff}}$ from fronts/cones and/or dispersion fits; independent $\widehat{c}_0$ from J‑only or TF baseline.  
- Attenuation fit: regression of $\ln(\widehat{c}_{\mathrm{eff}}/c_0)$ vs $D$ to slope $-\tfrac{1}{2}\beta$; $R^2$, confidence intervals.  
- Gate metrics: relative error bands on predicted vs measured $c_{\mathrm{eff}}$, monotonicity of attenuation with increasing $D$.

New tools/scripts (commit before runs):

- Debt estimation: Derivation/code/physics/metriplectic/void_debt/debt_estimator.py  
- Cone/dispersion meters (reuse TF/KG meters where applicable):  
  - Derivation/code/physics/metriplectic/tf/meter_cone.py  
  - Derivation/code/physics/metriplectic/tf/meter_dispersion.py  
- Runner: Derivation/code/physics/metriplectic/void_debt/run_void_debt_throttle.py

Required parameters and defaults (example T1 set):

- $(N,\Delta x,\Delta t,T)=(512,1.0,2\times 10^{-3},60)$; seeds $=10$.  
- Detector: $\theta=1.5\,\sigma_{\text{bg}}$, $L_s=4$, kernel=(3,3).  
- Baselines: select (J‑only with $(c,m)=(1.0,0.5)$ and small amplitude) and TF with $(D,\tau)=(1.0,1.0)$.

### 5.1.1 Pre-Run Config Requirements

Approvals/prereg are mandatory (see [authorization/README.md](Derivation/code/common/authorization/README.md)).

Required config and metadata:

- Approvals: Derivation/code/physics/metriplectic/APPROVAL.json  
- Schemas: Derivation/code/physics/metriplectic/schemas/  
  - void-debt-throttle.v1.schema.json  
- Specs: Derivation/code/physics/metriplectic/specs/  
  - void-debt-throttle-run.v1.json

PRE-REGISTRATION.json (minimum keys; fill at prereg):

```json
{
  "proposal_title": "T1 - Void-Debt Transport Throttling Instrument",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "ln(c_eff/c0) is linear in D with slope -β/2 within stated CI.", "direction": "decrease" },
    { "id": "H2", "statement": "Attenuation c_eff ≤ c0 holds monotonically with increasing D across seeds.", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["Δt","N","detector_kind","θ","L_s"],
    "dependent": ["beta_hat","R2_logfit","monotonic_violations","rel_error_ceff"],
    "controls": ["seed","transport_regime","ic_kind","bc_kind"]
  },
  "pass_fail": [
    { "metric": "R2_logfit", "operator": ">=", "threshold": 0.98, "unit": "-" },
    { "metric": "monotonic_violations", "operator": "<=", "threshold": 0, "unit": "-" },
    { "metric": "rel_error_ceff", "operator": "<=", "threshold": 0.05, "unit": "-" }
  ],
  "spec_refs": ["Derivation/code/physics/metriplectic/specs/void-debt-throttle-run.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

Specs (example):

```json
{
  "run_name": "void-debt-throttle-baseline",
  "version": "1.0.0",
  "tag": "void-debt-throttle.v1",
  "schema_ref": "Derivation/code/physics/metriplectic/schemas/void-debt-throttle.v1.schema.json",
  "parameters": {
    "N": 512, "dx": 1.0, "dt": 0.002, "T": 60,
    "detector": "perimeter", "theta": 1.5, "levels": 4,
    "regime": "TF", "D": 1.0, "tau": 1.0,
    "ic_kind": "random-bands", "bc_kind": "periodic"
  },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

Schemas (skeleton):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "void-debt-throttle.v1.schema.json",
  "title": "Void-Debt Throttling - v1",
  "type": "object",
  "properties": {
    "N": { "type": "integer", "minimum": 64 },
    "dx": { "type": "number", "exclusiveMinimum": 0 },
    "dt": { "type": "number", "exclusiveMinimum": 0 },
    "T": { "type": "number", "exclusiveMinimum": 0 },
    "detector": { "type": "string", "enum": ["count","perimeter","multiscale"] },
    "theta": { "type": "number", "exclusiveMinimum": 0 },
    "levels": { "type": "integer", "minimum": 1 },
    "regime": { "type": "string", "enum": ["J-only","TF","JM"] },
    "D": { "type": "number", "exclusiveMinimum": 0 },
    "tau": { "type": "number", "exclusiveMinimum": 0 },
    "ic_kind": { "type": "string" },
    "bc_kind": { "type": "string", "enum": ["periodic","reflecting"] }
  },
  "required": ["N","dx","dt","T","detector","theta","levels","regime","ic_kind","bc_kind"]
}
```

---

## 5.2 Experimental runplan

Plan:

1) For selected regimes (J‑only for $c_0$ or TF for $c_0=\sqrt{D/\tau}$), run seed sweeps over grids and detector variants to compute $\widehat{D}$ and $\widehat{c}_{\mathrm{eff}}$.  
2) Fit $\ln(\widehat{c}_{\mathrm{eff}}/c_0)$ vs $\widehat{D}$; extract $\widehat{\beta}$ and CI; compute $R^2$ and residuals.  
3) Record monotonicity violations and relative errors against predicted attenuation; report per‑seed dispersion.

Success (pass gates):

- $R^2_{\log\text{-fit}}\ge 0.98$; zero monotonicity violations; median relative error of $c_{\mathrm{eff}}$ predictions ≤ 5%.

Failure actions:

- Route artifacts to failed_runs/ with contradiction JSON including commit/tag, seeds, metrics, and diffs; no narrative claims are made.

Artifacts and routing:

- Figures (attenuation curves, log‑fits, cone overlays): Derivation/code/outputs/figures/metriplectic/void_debt_throttle/  
- Logs (CSV metrics, JSON run logs): Derivation/code/outputs/logs/metriplectic/void_debt_throttle/  
- All via [io_paths.py](Derivation/code/common/io_paths.py); seeds and commit/tag recorded.

Compute budget:

- Comparable to TF cones and dispersion; minutes per seed at $(N=512,T=60)$; detector scans increase runtime linearly.

---

## 6. Personnel

- Justin K. Lietz — design, approvals, and review; ensures adherence to authorization and artifact policies; signs prereg tags; reviews metrics vs [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md).

---

## 7. References

- Throttling law and spec references: [VDM-E-106](Derivation/EQUATIONS.md#vdm-e-106); [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:52-56,330-331)  
- A8 hierarchy/area-law context: [VDM-E-107](Derivation/EQUATIONS.md#vdm-e-107), [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113)  
- Authorization & results standards: [authorization/README.md](Derivation/code/common/authorization/README.md), [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---
