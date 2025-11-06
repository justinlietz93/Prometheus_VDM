<!-- White Paper Proposal based on Templates/PROPOSAL_PAPER_TEMPLATE.md -->

# T1 (Proto-model) - A8 1D Scaling Instrument: Interface Hierarchy and Area-Law Energy

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  
> Establish an instrument to quantify 1D A8 hierarchy formation by testing interface-count scaling $N(L)\sim\Theta(\log L)$ and excess-energy scaling $E_{\mathrm{exc}}(L)\sim L^{\,d-1}$ under tachyonic regime conditions with machine-auditable gates.

Practical Provenance pattern (see template):

- Pre-register salted hashes and tag before any artifact-writing run; store base_sha256, salt_hex, salted_sha256 in PRE-REGISTRATION.json; tag must be included in run logs and figure/CSV/JSON artifacts.

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Principal Investigator, approval authority

---

## 3. Abstract

Proposed is a T1 instrument to measure scaling laws associated with Axiom 8 (“tachyonic genesis”) in 1D settings. Two spec-level equations are instrumented: (i) interface-count scaling
$$
N(L) \;\sim\; \Theta(\log L)
$$
[VDM-E-107](Derivation/EQUATIONS.md#vdm-e-107), and (ii) excess-energy area law
$$
E_{\mathrm{exc}}(L) \;\sim\; L^{\,d-1},
$$
with $d=1$ in the present instrument (so $E_{\mathrm{exc}}(L)\sim L^0$ up to constants) [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113), under the tachyonic regime condition $V''(0)<0$ [VDM-E-112](Derivation/EQUATIONS.md#vdm-e-112). The instrument defines interface detectors, energy accounting, regression procedures, and pass/fail gates with deterministic artifacts. This is an instrument (≤T2) and does not claim new physics; it standardizes meters required by downstream A8 proposals.

---

## 4. Background & Scientific Rationale

Canon anchors:

- Tachyonic regime condition: $V''(0)<0$ [VDM-E-112](Derivation/EQUATIONS.md#vdm-e-112).  
- Interface-count scaling: $N(L)\sim\Theta(\log L)$ [VDM-E-107](Derivation/EQUATIONS.md#vdm-e-107).  
- Energy area law: $E_{\mathrm{exc}}(L)\sim L^{\,d-1}$ [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113).  
- Program notes and context appear in the Unification spec (A8 and hierarchy passages).

Scientific rationale:

- In tachyonic regimes, interface formation concentrates energy on codimension‑1 sets, suggesting sublinear growth of interface count with system size and an area law for excess energy.  
- A rigorized instrument is required to quantify these patterns reproducibly (detectors, energy accounting, regression) and to provide clear acceptance gates pre-registered for experiments.

Assumptions and limitations:

- 1D baseline isolates interface counting and energy aggregation; higher‑D generalization is outside scope.  
- Detector definitions (thresholds and morphological choices) affect $N(L)$; the instrument reports detector sensitivity scans to avoid overfitting.

---

## 5. Intellectual Merit and Procedure

- Importance: Provides standardized meters for hierarchy detection and energy scaling that future A8 proposals can rely upon.  
- Broader impacts: Enables cross‑runner comparisons and long‑term regression testing; supports claims only when gates pass with pinned artifacts and provenance.  
- Approach: Simulate a 1D field with tachyonic potential $V(\phi)$ (ensuring $V''(0)<0$); detect interfaces; compute $E_{\mathrm{exc}}(L)$; fit the scaling relations across $L$ and detector/scenario sweeps; enforce pre-registered acceptance gates.

---

## 5.1 Experimental Setup and Diagnostics

Normalization and parameters (per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)):

- Domain length $L$, grid $N$, spacing $\Delta x=L/N$; temporal window $T$ and $\Delta t$ for dynamic relaxation when needed; seeds $S$.  
- Potential and regime: choose a smooth double‑well tachyonic potential with $V''(0)<0$ (e.g., $V(\phi)=\tfrac{1}{4}(\phi^2-1)^2 - \tfrac{\mu}{2}\phi^2$ with $\mu>0$); or a canonical tachyonic quadratic near $\phi=0$ in the limit that preserves numerics.  
- Dynamics: Variants allowed for relaxation to near‑steady profiles (e.g., gradient flow or metriplectic M‑limb step); the instrument records the path and does not claim dynamics at T2.

Detectors and energy accounting:

- Interface detector families:  
  - Threshold crossing (count transitions beyond $\pm \theta$),  
  - Total variation peaks (TV-based change-point),  
  - Multiscale structure tensor (1D analog) with scale pyramid $L_s$.  
- $N(L)$: number of detected interfaces after de‑spurious filtering (minimum spacing $\ge \lambda_{\min}$).  
- Energy: $E_{\mathrm{exc}}(L)=E[\phi;L]-E_{\min}(L)$ with $E[\phi;L]=\int_0^L \left(\tfrac{\kappa}{2}\lvert\partial_x\phi\rvert^{2}+V(\phi)\right)\,dx$; $E_{\min}(L)$ estimated from best-fit bulk phases without interfaces (instrument defines numerical approximation; constants reported).

Acceptance metrics and gates:

- Count law: Fit $N(L)$ vs $\log L$ using robust regression; slope $\hat s$ within tolerance of a positive constant and $R^2\ge 0.98$; report CI and detector sensitivity bands.  
- Area law (1D): Fit $E_{\mathrm{exc}}(L)$ vs $L^{\,0}$ (constant w.r.t. $L$) with $R^2\ge 0.98$; equivalently, linear fit of $\log E_{\mathrm{exc}}$ vs $\log L$ with slope $|\hat\alpha|\le 0.1$ (tunable in prereg).  
- Tachyonic check: Validate $V''(0)<0$ numerically from supplied potential; runs failing this check are invalid.

New tools/scripts (commit before runs):

- Detector implementations: Derivation/code/physics/axioms/a8/detectors.py  
- Energy calculator: Derivation/code/physics/axioms/a8/energy.py  
- Runner: Derivation/code/physics/axioms/a8/run_a8_scaling_1d.py  
- Report/viz: Derivation/code/physics/axioms/a8/report_scaling.py

Required parameters and defaults (example T1 set):

- $L\in\{128,256,512,1024,2048\}$; $N=L$; $\Delta t$ small for relax; seeds $=10$.  
- Detector threshold $\theta=0.5$ (in normalized units), minimum spacing $\lambda_{\min}=4\Delta x$, $L_s=4$ levels.  
- Potential coefficients $(\kappa,\mu)$ declared; numeric bounds at prereg.

### 5.1.1 Pre-Run Config Requirements

Approvals/preregistration are mandatory (see [authorization/README.md](Derivation/code/common/authorization/README.md)).

Required config and metadata:

- Approvals: Derivation/code/physics/axioms/APPROVAL.json  
- Schemas: Derivation/code/physics/axioms/schemas/  
  - a8-scaling-1d.v1.schema.json  
- Specs: Derivation/code/physics/axioms/specs/  
  - a8-scaling-1d-run.v1.json

PRE-REGISTRATION.json (minimum keys; fill at prereg):

```json
{
  "proposal_title": "T1 - A8 1D Scaling Instrument (Interfaces and Area Law)",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Interface count grows like Θ(log L) with R² ≥ 0.98 across detectors.", "direction": "increase" },
    { "id": "H2", "statement": "Excess energy follows area law with |slope(log E_exc vs log L)| ≤ 0.1 and R² ≥ 0.98.", "direction": "no-change" },
    { "id": "H3", "statement": "Tachyonic regime validation V''(0) < 0 holds for all runs.", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["L","detector_kind","θ","λ_min","L_s"],
    "dependent": ["N_slope","N_R2","alpha_energy","R2_energy"],
    "controls": ["seed","potential_kind","κ","μ"]
  },
  "pass_fail": [
    { "metric": "N_R2", "operator": ">=", "threshold": 0.98, "unit": "-" },
    { "metric": "R2_energy", "operator": ">=", "threshold": 0.98, "unit": "-" },
    { "metric": "alpha_energy_abs", "operator": "<=", "threshold": 0.1, "unit": "-" }
  ],
  "spec_refs": ["Derivation/code/physics/axioms/specs/a8-scaling-1d-run.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

Specs (example):

```json
{
  "run_name": "a8-scaling-1d-baseline",
  "version": "1.0.0",
  "tag": "a8-scaling-1d.v1",
  "schema_ref": "Derivation/code/physics/axioms/schemas/a8-scaling-1d.v1.schema.json",
  "parameters": {
    "L_list": [128,256,512,1024,2048],
    "detector": "threshold",
    "theta": 0.5,
    "lambda_min": 4,
    "levels": 4,
    "potential": "dw-tachyonic",
    "kappa": 1.0,
    "mu": 0.25
  },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

Schemas (skeleton):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "a8-scaling-1d.v1.schema.json",
  "title": "A8 1D Scaling Instrument - v1",
  "type": "object",
  "properties": {
    "L_list": { "type": "array", "items": { "type": "integer", "minimum": 32 }, "minItems": 3 },
    "detector": { "type": "string", "enum": ["threshold","tv-peak","multiscale"] },
    "theta": { "type": "number" },
    "lambda_min": { "type": "integer", "minimum": 1 },
    "levels": { "type": "integer", "minimum": 1 },
    "potential": { "type": "string", "enum": ["dw-tachyonic","custom"] },
    "kappa": { "type": "number", "exclusiveMinimum": 0 },
    "mu": { "type": "number", "exclusiveMinimum": 0 }
  },
  "required": ["L_list","detector","theta","lambda_min","levels","potential","kappa","mu"]
}
```

---

## 5.2 Experimental runplan

Plan:

1) For each $L\in L\_list$ and seed, produce relaxed profiles in tachyonic regime ($V''(0)<0$ test logged).  
2) Detect interfaces via selected detector; compute $N(L)$ and uncertainty (bootstrapping over seeds).  
3) Compute $E_{\mathrm{exc}}(L)$ via energy calculator; estimate $E_{\min}(L)$ reference; log residuals.  
4) Fit $N(L)$ vs $\log L$ and $E_{\mathrm{exc}}(L)$ vs $L$ (or $\log$-$\log$); record slopes, $R^2$, detector sensitivity.  
5) Enforce gates; produce summary figures and CSV/JSON logs.

Success (pass gates):

- $R^2\ge 0.98$ for both fits; $|\alpha_{\text{energy}}|\le 0.1$; tachyonic regime validated; detector sensitivity within reported CI bands.

Failure actions:

- Route artifacts to failed_runs/ with contradiction JSON (commit/tag, seeds, metrics, diffs); no narrative claims are made.

Artifacts and routing:

- Figures (counts vs log L, energy vs L; residuals): Derivation/code/outputs/figures/axioms/a8_scaling_1d/  
- Logs (CSV metrics, JSON runs): Derivation/code/outputs/logs/axioms/a8_scaling_1d/  
- All routed via [io_paths.py](Derivation/code/common/io_paths.py) with seeds and commit/tag recorded.

Compute budget:

- For $L\le 2048$ and 10 seeds, minutes per L on CPU for relax+detect; total scales linearly with $|L\_list|$ and detector variants.

---

## 6. Personnel

- Justin K. Lietz — design, approvals, and review; ensures adherence to authorization and artifact policies; signs prereg tags; reviews metrics vs [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md).

---

## 7. References

- Canon equations: [VDM-E-107](Derivation/EQUATIONS.md#vdm-e-107), [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113), [VDM-E-112](Derivation/EQUATIONS.md#vdm-e-112)  
- Program context: Unification hyper‑proposal A8 sections (Derivation/Unification/T0_Unification_Program_Spec_v1.md)  
- Authorization & results standards: [authorization/README.md](Derivation/code/common/authorization/README.md), [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---
