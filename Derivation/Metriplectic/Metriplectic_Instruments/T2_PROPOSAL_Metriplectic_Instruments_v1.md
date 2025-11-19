# 1. T2 (Instrument) — Metriplectic Instruments: Identity, KG, RD, and FRW Meters (EBN series)

> Created Date:  2025-11-18  
> Commit: dd6a53e0c38ed9c4a20bedf3e34ec2287ad40e85  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI), Neuroca (compute & instrumentation).

## 3. Abstract

Proposed in this document is the meter suite that turns VDM derivations into machine‑auditable numbers: (i) **KG J‑only dispersion/locality meter**, (ii) **RD meter** (front‑speed & dispersion), (iii) **Metriplectic identity meter** (degeneracy and Lyapunov monotonicity), and (iv) **FRW continuity meter**. Each meter has fixed acceptance gates; runs emit PNG+CSV+JSON artifacts with provenance. This proposal formalizes the meters as reusable T2 instruments.

## 4. Background & Scientific Rationale

Meters operationalize Axiom A4 and A2 claims and gate numerics (discretization = instrument). Prior QC runs for KG, FRW, and metriplectic structure motivate consolidation into a single T2 package.

## 5. Intellectual Merit and Procedure

(1) Importance: establishes standardized instruments for all downstream T3–T7 phenomena.  
(2) Broader impacts: reproducible physics meters with explicit gates.  
(3) Approach: deterministic seeds, double precision, artifact routing, AMD ROCm where applicable.

## 5.1 Experimental Setup and Diagnostics

This section answers the canonical 5.1 questions for the **meter suite as a whole**, then itemizes per‑meter details.

### 5.1.a Known required parameters (keys and units)

All meters share a small set of simulation parameters; specific subsets apply per meter.

- **KG J‑only meter (locality & dispersion).**
  - $N$ — grid size (points per dimension), dimensionless.
  - $\Delta t$ — time step [simulation time units; see [`00_UNITS_NORMALIZATION.md`](Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md:1)].
  - $c$ — J‑limb wave speed [$\text{length}/\text{time}$ in normalized units].
  - $m$ — mass parameter (code units; mass scale in the Klein–Gordon branch).
  - `seeds` — list of integer RNG seeds (dimensionless).
- **RD meter (front speed & dispersion).**
  - $D$ — diffusion coefficient [$\text{length}^2/\text{time}$].
  - $r$ — reaction/growth rate [$1/\text{time}$].
  - $\lambda$ — (optional) reaction–diffusion length scale [$\text{length}$].
  - `seeds` — integer RNG seeds (dimensionless).
- **Identity (metriplectic) meter.**
  - Same state/discretization parameters as KG/RD meters (grid, $\Delta t$) plus any Lyapunov functional coefficients listed in the schema.
- **FRW meter.**
  - Cosmological background parameters $(\Omega_b,\Omega_c,H_0,\dots)$ as defined in the FRW balance domain, plus solver tolerances and time grid; this meter is treated as a client of the FRW domain but its **QC metrics** live in this suite.

Defaults and parameter ranges are specified in the `meters-ebn.v1.json` spec (see §5.1.1), with units governed by [`00_UNITS_NORMALIZATION.md`](Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md:1).

### 5.1.b Diagnostics needed (list and count)

Per **meter** and per **tag** (e.g., `meters-ebn.v1`), the minimal diagnostics and artifact counts are:

- **KG J‑only meter**
  - 1 PNG: dispersion curve $\omega^2(k^2)$ with residuals.
  - 1 CSV: table of $(k,\omega,\omega_{\text{fit}},\text{residual})$.
  - 1 JSON: run log with metrics:
    - $v/c$, $R^2_{\text{disp}}$, Noether drift statistics, CFL.
- **RD meter**
  - 1 PNG: front‑position vs. time with fitted $c_{\text{front}}$, plus dispersion panel.
  - 1 CSV: $(x_{\text{front}}(t), c_{\text{front}}, k, \sigma(k))$.
  - 1 JSON: metrics:
    - relative front‑speed error, $R^2$ on front fit, dispersion medians.
- **Identity (metriplectic) meter**
  - 1 PNG: Lyapunov $L_h(t)$ curve plus two‑grid convergence plot.
  - 1 CSV: $L_h$ vs. time, per grid and per step.
  - 1 JSON: metrics:
    - $\max_t \Delta L_h$, identity residual norms, two‑grid slope.
- **FRW meter**
  - 1 PNG: FRW continuity residual vs. time.
  - 1 CSV: $(t,\rho,a,\text{residual})$.
  - 1 JSON: RMS residual and gate verdict, with references to FRW specs.

This satisfies the **minimum** “1 PNG + 1 CSV + 1 JSON” requirement per meter per tag and makes diagnostics explicitly machine‑auditable.

### 5.1.c Unplanned equipment and new tools/scripts

- **Physical equipment.**
  - No specialized physical apparatus is assumed; the meters run on standard Linux compute nodes (CPU or GPU).
- **Software tools/scripts required (paths).**
  - Meter runners and kernels live under:
    - `Derivation/code/physics/meters/` — domain code for KG, RD, identity, and FRW meters.
  - Specs and schemas for this suite live under:
    - `Derivation/code/physics/meters/specs/` — meter spec JSON (e.g., `meters-ebn.v1.json`).
    - `Derivation/code/physics/meters/schemas/` — JSON Schemas for meter specs and outputs.
  - Any new helper scripts or CLIs must be added under:
    - `Derivation/code/physics/meters/` (implementation) and
    - `Derivation/code/tests/meters/` (preflight tests), referenced in this proposal when created.

If additional external tools (e.g. plotting back‑ends beyond the existing common plotting helpers) are required, this proposal and the specs must be amended to document those dependencies explicitly before runs.

### 5.1.d Required parameters and defaults (keys and units)

At **minimum**, each spec must provide the following keys (per run or per meter configuration), with defaults documented in `meters-ebn.v1.json`:

- `N` (int, default: domain‑specific; grid points per dimension; unitless).
- `dt` (float, default: CFL‑safe value; time units).
- `c` (float, J‑limb wave speed; $\text{length}/\text{time}$).
- `m` (float, mass scale; code units; see UNITS).
- `D` (float, diffusion coefficient; $\text{length}^2/\text{time}$).
- `r` (float, reaction rate; $1/\text{time}$).
- `lambda` (float, RD length scale; $\text{length}$).
- `seeds` (array[int], at least one seed).
- `CFL`, `BCs`, `precision` (controls for stability and numeric discipline).

Each meter reuses these keys and adds meter‑specific parameters as documented in the meter schema. The APPROVAL and SPEC files in §5.1.1 enforce that these keys are present and range‑checked prior to artifact‑writing runs.

### 5.1.1 Pre-Run Config Requirements

- **Required config and metadata (meters domain):**
  - `Derivation/code/physics/meters/APPROVAL.json`
  - `Derivation/code/physics/meters/schemas/`
    - `meters-ebn.schema.json`
  - `Derivation/code/physics/meters/specs/`
    - `meters-ebn.v1.json`

These files encode the approval policy, pre‑registration manifest, schemas, and run specs for all meters in this suite.

### APPROVALS.json

The approvals manifest at `Derivation/code/physics/meters/APPROVAL.json` must, at minimum, follow this pattern (values may be extended as needed):

```json
{
  "preflight_name": "meters-ebn-preflight",
  "description": "Approval manifest stating that the preflight meter runners must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, this T2_PROPOSAL_Metriplectic_Instruments_v1.md must be reviewed and approved."
},
{
  "pre_registered": true,
  "proposal": "Derivation/Metriplectic/Metriplectic_Instruments/T2_PROPOSAL_Metriplectic_Instruments_v1.md",
  "allowed_tags": [
    "meters-ebn.v1"
  ],
  "schema_dir": "Derivation/code/physics/meters/schemas",
  "approvals": {
    "meters-ebn.v1": {
      "schema": "Derivation/code/physics/meters/schemas/meters-ebn.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto generated timestamp",
      "approval_key": "auto generated hashed key"
    }
  }
}
```

- **Pre-registration manifest:** `Derivation/code/physics/meters/PRE-REGISTRATION.json` — records the proposal title, tier grade, commit, salted provenance, hypotheses, variables, pass/fail metrics, and `spec_refs` for all meters in this suite.

- **Schemas:** `Derivation/code/physics/meters/schemas/meters-ebn.schema.json` — JSON Schema for meter run specifications and outputs, keyed by tag (e.g., `meters-ebn.v1`).

- **Specs:** `Derivation/code/physics/meters/specs/meters-ebn.v1.json` — run‑spec files referenced in `spec_refs`; each spec defines parameters, seeds, and tags for KG, RD, identity, and FRW meters.

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "Metriplectic Instruments: KG, RD, Identity, FRW",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_KG", "statement": "Light-cone speed v is bounded by c within 2% under J-only dynamics.", "direction": "no-change" },
    { "id": "H_RD", "statement": "Front speed equals 2*sqrt(D*r) within 5%.", "direction": "no-change" },
    { "id": "H_ID", "statement": "Discrete Lyapunov decreases monotonically for M-step; degeneracy identities hold to 1e-12.", "direction": "no-change" },
    { "id": "H_FRW", "statement": "FRW continuity residual RMS ≤ 1e-6.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["N", "Δt", "c", "m", "D", "r", "λ", "seeds"],
    "dependent": ["v/c", "R2_disp", "rel_err_front", "ΔL_h", "RMS_FRW"],
    "controls": ["CFL", "BCs", "precision"]
  },
  "pass_fail": [
    { "metric": "v/c", "operator": "<=", "threshold": 1.02, "unit": "" },
    { "metric": "R2_disp", "operator": ">=", "threshold": 0.999, "unit": "" },
    { "metric": "rel_err_front", "operator": "<=", "threshold": 0.05, "unit": "" },
    { "metric": "ΔL_h", "operator": "<=", "threshold": 0.0, "unit": "" },
    { "metric": "RMS_FRW", "operator": "<=", "threshold": 1e-6, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/physics/meters/specs/meters-ebn.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

### Minimal spec example (meters-ebn.v1)

The file `Derivation/code/physics/meters/specs/meters-ebn.v1.json` must contain at least one spec entry of the following shape (keys as in §5.1 and the PRE‑REG `variables` block):

```json
{
  "run_name": "meters-ebn-baseline",
  "version": "1.0.0",
  "tag": "meters-ebn.v1",
  "schema_ref": "Derivation/code/physics/meters/schemas/meters-ebn.schema.json",
  "parameters": {
    "N": 1024,
    "dt": 0.05,
    "c": 1.0,
    "m": 0.5,
    "D": 1.0,
    "r": 0.25,
    "lambda": 10.0,
    "CFL": 0.2,
    "BCs": "periodic",
    "precision": "float64"
  },
  "seeds": [0, 1, 2]
}
```

This is a **minimal illustrative spec**, not a canonical choice of defaults. Actual production specs:

- Must use units and mappings consistent with [`00_UNITS_NORMALIZATION.md`](Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md:1) and the metriplectic/meter domain conventions.
- May include additional meter‑specific keys (e.g., windowing parameters, estimator options) as long as they remain compatible with `meters-ebn.schema.json`.
- Must be validated by `meters-ebn.schema.json` and the meters `APPROVAL.json` gate before any artifact‑writing runs.

## 5.2 Experimental runplan

This section describes how the resources in §5.1 are employed to answer the meter‑validation questions, along with runtime and success/failure actions.

1. **Cartesian product of independent variables.**
   - For each meter, define a Cartesian product over its independent variables in the spec:
     - KG meter: $(N, \Delta t, c, m, \text{seeds})$.
     - RD meter: $(D, r, \lambda, \text{seeds})$.
     - Identity meter: $(N, \Delta t, \text{seeds})$ (plus any Lyapunov parameters).
     - FRW meter: background parameter sets $(\Omega_b,\Omega_c,H_0,\dots)$ and time grids.
   - Exact product and ranges are declared in `meters-ebn.v1.json` and reviewed before approval.

2. **Execution plan and estimated runtime.**
   - Each spec defines the number of runs per meter and per tag. Baseline expectation:
     - KG/RD/identity meters: $\mathcal{O}(10)$–$\mathcal{O}(10^2)$ runs per meter configuration.
     - FRW meter: a smaller set of background configurations, each run to completion under FRW QC.
   - Estimated runtime per run:
     - On a single modern CPU or GPU, each meter run is expected to complete in minutes (not hours) under the baseline grid sizes; total compute budget per tag is expected to be within a **few GPU‑hours** or **tens of CPU‑hours**.
   - Actual runtime budgets and node allocations are recorded in the specs and in the JSON logs.

3. **Plan of action for successful experiments (PASS).**
   - When all gates for a given meter/tag pass:
     - Emit `T2_RESULTS_Metriplectic_Instruments_v1.md` (or meter‑specific RESULTS documents if split), with:
       - Numbered figures (PNG), CSV tables, and JSON logs per meter.
       - Explicit gate matrices (PASS/FAIL per metric) and references to specs/schemas used.
     - Tag the commit with an annotated, signed prereg tag that includes:
       - Commit SHA, proposal path, salted provenance, and spec/tag identifiers.
     - Update canonical indices (`00_PROPOSALS.md`, `00_RESULTS.md`, `00_DATA_PRODUCTS.md` entries for meter data products) to reflect the certified meter status.

4. **Plan of action for failed experiments (FAIL).**
   - If any gate fails for a meter or tag:
     - Route all artifacts via `io_paths.py` to a `failed_runs/` subdirectory in the meters domain.
     - Emit a CONTRADICTION_REPORT JSON with:
       - Commit, salted proposal hash, spec and schema references.
       - A full list of metrics that violated thresholds and any diagnostic plots.
     - No tier escalation is claimed; any theory claims that depended on the failed meter remain blocked until a revised proposal and rerun.

5. **Publication and display of results.**
   - All results are written according to [`RESULTS_PAPER_STANDARDS.md`](Derivation/Templates/RESULTS_PAPER_STANDARDS.md:1):
     - White‑paper grade write‑up for the T2 meter suite.
     - Grayscale‑safe, labeled figures for dispersion, fronts, Lyapunov curves, and FRW residuals.
     - CSV and JSON logs matching the schemas defined in `meters-ebn.schema.json`.

This runplan, plus the explicit APPROVAL/PRE‑REG/spec/schema structure in §5.1.1, completes the 5.2 requirements for the T2 meter suite.

## 6. Personnel

Justin K. Lietz will design the meters, implement and review the runners, and interpret diagnostics under the metriplectic and cosmology programs. Neuroca provides computational infrastructure, CI integration, and code review to ensure that implementations match this proposal, the tier standards, and the validation metrics.

## 7. References

- `Derivation/Unification/T0_Unification_Program_Spec_v1.md` — defines the EBN meter program (targets M1–M5) and cross-domain gates for causality, metriplectic structure, RD, FRW, and emergent gravity.
- `Derivation/TIER_STANDARDS.md` — global tier ladder and invariants for T2 instruments.
- `Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md` — single source for KPIs such as front-speed relative error, dispersion fits, metriplectic identity diagnostics, and FRW continuity residuals.
- `Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md` — prior QC results for the KG J-only meter that this T2 suite consolidates.
- `Derivation/Cosmology/PROPOSAL_FRW_Balance_v1.md` and related FRW balance work — context for the FRW continuity meter and its RMS gate.
