<!-- White Paper Proposal based on Templates/PROPOSAL_PAPER_TEMPLATE.md -->

# T1 (Proto-model) - Causal DAG Audits via Transfer Entropy (TE/MTE) for Locality-Constrained Transport

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  
> Define and validate a TE/MTE-based causality meter that reconstructs the Causal DAG from simulation time series and gates it against VDM’s locality cone and adjacency under Telegraph–Fisher transport.

Practical Provenance pattern (see template):

- Pre-register salted hashes and tag before any artifact-writing run; store base_sha256, salt_hex, salted_sha256 in PRE-REGISTRATION.json; tag must be included in run logs and figure/CSV/JSON artifacts.

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Principal Investigator, approval authority

---

## 3. Abstract

Proposed is a T1 instrument (meter) that infers directed causal structure from time series using Transfer Entropy (TE) and Multiscale Transfer Entropy (MTE), then audits the result against VDM’s explicit locality constraints. The defining meter equation
$$
TE_{X \to Y} \;=\; I\!\big( Y_{t+1}\,;\, X_t^{(k)} \,\big\vert\, Y_t^{(l)} \big)
$$
is registered in [VDM-E-111](Derivation/EQUATIONS.md#vdm-e-111) with context in [causality.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/causality.md:21-24). Acceptance gates require: (i) adjacency recovery matching the grid’s local stencil, (ii) delay structure consistent with the transport cone from Telegraph–Fisher calibration ([VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105)), and (iii) near-zero TE outside the cone (acausal pairs). The instrument produces machine-auditable PNG/CSV/JSON artifacts routed through the io helper for regression and reproducibility.

---

## 4. Background & Scientific Rationale

Canon anchors and program context:

- Meter definition: [VDM-E-111](Derivation/EQUATIONS.md#vdm-e-111).  
- Locality and finite speed (Telegraph–Fisher): [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105), with audits/specs in [audits/2025-11-04_A8_Bridges_Status.md](audits/2025-11-04_A8_Bridges_Status.md:104-118).  
- J-only baselines (cones/dispersion): [RESULTS_KG_Jonly_Locality_and_Dispersion.md](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md) and related proposals (KG/RD split, Strang diagnostics).  
- Causality collection justification and gate sketch: [PRIVATE causality note](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/causality.md).

Scientific need:

- Beyond visual front-arrival timing, a data-driven causal audit quantifies information flow and validates that the discretization preserves intended locality across scales and parameter regimes.  
- TE/MTE captures nonlinear, lagged dependencies robust to moderate noise; imposing cone consistency ties statistical causality to mechanistic constraints (c from TF or calibrated cones).

Assumptions and limitations:

- Stationarity approximations are applied window-wise; estimator bias is controlled by surrogate testing and permutation baselines.  
- The DAG audit targets grid-local causality; long-range physical couplings (if present) must be predeclared (e.g., periodic wrap, external forcing) to avoid false flags.

---

## 5. Intellectual Merit and Procedure

- Importance: Establishes a standardized, quantitative meter to certify A2 locality in simulated transports.  
- Broader impacts: Enables regression tests on solver changes; bridges statistical causality and mechanistic cones for policy-aware acceptance.  
- Approach: Compute TE/MTE on simulated fields (or subsets), threshold edges by significance, compare the inferred adjacency and lag spectrum to the known stencil and cone-delay predictions from TF calibration.

---

## 5.1 Experimental Setup and Diagnostics

Known parameters (unit normalization per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)):

- Spatial grid: $N$, $\Delta x$; temporal: $T$, $\Delta t$; seeds $S$.  
- Transport regime knobs for context (when using TF calibration runs): $(D,\tau)$ or equivalent cone-calibration references; alternatively $(c,m)$ for J-baseline.  
- TE parameters: embedding $(k,l)$, delay sweep $\Delta\ell \in [0,\Delta\ell_{\max}]$, estimator (discrete binning vs kNN), significance surrogate count $N_{\text{perm}}$.

Diagnostics (minimum set per run):

- Adjacency recovery metrics: precision/recall/F1 comparing inferred edges to stencil adjacency (e.g., 1D nearest neighbors or 2D 4-/8-stencil).  
- Cone-delay consistency: inferred lag $\widehat{\Delta\ell}$ vs predicted $d/c$ with $d=\text{grid distance}$, $c=\sqrt{D/\tau}$ (or measured cone slope).  
- Acausal suppression: TE outside cone below threshold (surrogate-based q-value control).  
- Robustness: per-seed variance; stability of edge set vs $(k,l,\Delta\ell_{\max})$ scan.

New tools/scripts (commit before runs):

- TE/MTE meter: Derivation/code/physics/causality/te_meter.py  
- Audit runner: Derivation/code/physics/causality/run_causal_dag_audit.py  
- Viz/report: Derivation/code/physics/causality/report_causal_dag.py

Required parameters and defaults (example T1):

- $(N,\Delta x,\Delta t,T)=(256,1.0,5\times 10^{-3},50)$; seeds $=10$; TE embedding $(k,l)=(2,2)$; $\Delta\ell_{\max}=10$; kNN estimator $k=5$; $N_{\text{perm}}=200$; FDR q=0.05.

### 5.1.1 Pre-Run Config Requirements

Approvals and preregistration are mandatory (see [authorization/README.md](Derivation/code/common/authorization/README.md)).

Required config and metadata:

- Approvals: Derivation/code/physics/causality/APPROVAL.json  
- Schemas dir: Derivation/code/physics/causality/schemas/  
  - causal-dag-audit.v1.schema.json  
- Specs dir: Derivation/code/physics/causality/specs/  
  - causal-dag-audit-run.v1.json

PRE-REGISTRATION.json (minimum keys; fill at prereg):

```json
{
  "proposal_title": "T1 - Causal DAG Audits via Transfer Entropy",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Inferred DAG edges match local stencil with F1 ≥ 0.98 across seeds.", "direction": "increase" },
    { "id": "H2", "statement": "Inferred delays agree with cone prediction d/c within ±1 grid timestep or ≤5% relative error.", "direction": "no-change" },
    { "id": "H3", "statement": "Acausal TE outside the cone is not significant under FDR q≤0.05.", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["Δt","N","estimator","Δℓ_max","k","q"],
    "dependent": ["precision","recall","F1","delay_error","acausal_TE_rate"],
    "controls": ["seed","stencil_kind","boundary_condition","transport_regime"]
  },
  "pass_fail": [
    { "metric": "F1", "operator": ">=", "threshold": 0.98, "unit": "-" },
    { "metric": "delay_error", "operator": "<=", "threshold": 0.05, "unit": "relative" },
    { "metric": "acausal_TE_rate", "operator": "<=", "threshold": 0.01, "unit": "-" }
  ],
  "spec_refs": ["Derivation/code/physics/causality/specs/causal-dag-audit-run.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

Specs (example):

```json
{
  "run_name": "causal-dag-audit-baseline",
  "version": "1.0.0",
  "tag": "causal-dag-audit.v1",
  "schema_ref": "Derivation/code/physics/causality/schemas/causal-dag-audit.v1.schema.json",
  "parameters": {
    "N": 256, "dx": 1.0, "dt": 0.005, "T": 50,
    "embedding_k": 2, "embedding_l": 2, "lag_max": 10,
    "estimator": "knn", "knn_k": 5, "surrogates": 200, "fdr_q": 0.05,
    "stencil": "1D-nearest", "periodic": true
  },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

Schemas (skeleton):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "causal-dag-audit.v1.schema.json",
  "title": "Causal DAG Audit - TE/MTE Meter v1",
  "type": "object",
  "properties": {
    "N": { "type": "integer", "minimum": 8 },
    "dx": { "type": "number", "exclusiveMinimum": 0 },
    "dt": { "type": "number", "exclusiveMinimum": 0 },
    "T": { "type": "number", "exclusiveMinimum": 0 },
    "embedding_k": { "type": "integer", "minimum": 1 },
    "embedding_l": { "type": "integer", "minimum": 1 },
    "lag_max": { "type": "integer", "minimum": 1 },
    "estimator": { "type": "string", "enum": ["discrete","knn"] },
    "knn_k": { "type": "integer", "minimum": 2 },
    "surrogates": { "type": "integer", "minimum": 20 },
    "fdr_q": { "type": "number", "exclusiveMinimum": 0, "maximum": 0.25 },
    "stencil": { "type": "string" },
    "periodic": { "type": "boolean" }
  },
  "required": ["N","dx","dt","T","embedding_k","embedding_l","lag_max","estimator","surrogates","fdr_q"]
}
```

---

## 5.2 Experimental runplan

Plan:

1) Generate/ingest simulation time series for target regimes (KG J-only cones, TF causal runs, or metriplectic compositions with declared parameters).  
2) Compute TE grid pairwise within a neighborhood (and negative control pairs at larger distances); apply surrogate-based FDR q control.  
3) Build directed edge set; compute adjacency metrics (precision/recall/F1) vs the known stencil; compute delay errors vs cone predictions ($d/c$ or measured slope).  
4) Sweep $(\Delta t,N,\Delta\ell_{\max},k)$; record per-seed variability.

Success (pass gates):

- F1 ≥ 0.98 for local adjacency; delay errors ≤ 1 step or ≤ 5% relative; acausal TE rate ≤ 0.01 at FDR q ≤ 0.05.

Failure actions:

- Route artifacts to failed_runs/ with contradiction JSON containing commit/tag, seeds, metrics, and diffs; no narrative claims are made.

Artifacts and routing:

- Figures (DAG plots, PR curves, delay histograms): Derivation/code/outputs/figures/causality/causal_dag_audit/  
- Logs (CSV metrics, JSON run log): Derivation/code/outputs/logs/causality/causal_dag_audit/  
- All via [io_paths.py](Derivation/code/common/io_paths.py); record seeds and commit/tag in JSON.

Compute budget:

- TE computations scale as O(N_pairs × lag_max); for 1D nearest-neighbor bands at N=256 and lag_max=10, per-run minutes on CPU; seed × sweep multiplies linearly.

---

## 6. Personnel

- Justin K. Lietz — design, approvals, and review; ensures adherence to authorization and artifact policies; signs prereg tags; reviews metrics vs [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md).

---

## 7. References

- TE meter definition: [VDM-E-111](Derivation/EQUATIONS.md#vdm-e-111); background [causality.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/causality.md:21-24)  
- TF locality references: [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105); [audits/2025-11-04_A8_Bridges_Status.md](audits/2025-11-04_A8_Bridges_Status.md:104-118)  
- Authorization & results standards: [authorization/README.md](Derivation/code/common/authorization/README.md), [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---
