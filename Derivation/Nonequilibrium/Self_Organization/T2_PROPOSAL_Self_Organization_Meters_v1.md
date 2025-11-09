<!-- DOC-GUARD: T2 INSTRUMENT PROPOSAL -->
# T2 (Instrument) — Self-Organization Onset Meters (Nicolis–Prigogine)

**Created:** 2025-11-08
**Commit:** 8f94aeaa9e44c36ac3920e27e31b294b4e09381d
**Salted provenance (auto via stamp_proposal.py):** base_sha256=<to-fill>, salt_hex=<to-fill>, salted_sha256=<to-fill>
**Contact:** Justin K. Lietz <justin@neuroca.ai>
**License:** [LICENSE](../../LICENSE)

> Notation and MathJax: inline math uses `$...$`; block math uses `$$...$$` with blank lines above and below. All inequalities and derivatives are expressed in MathJax for standard and unambiguous parsing.

**Short summary (one sentence TL;DR):** This proposal certifies a meters-first, non-phenomenological stack for self-organization onset diagnostics. It validates Excess-Entropy-Production (EEP) trend, leading-eigenvalue bifurcation cards with branch classification, localized-structure detection, and branch-stability overlays against canonical gates. Artifacts are emitted with PNG+CSV+JSON sidecars and contradiction routing on failure.

## 1. Tier Grade

Tier: T2 (Instrument). This document certifies meters only. No phenomenon claims (T3+) are made here.

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Principal Investigator (PI), implementer, approver (Neuroca / Prometheus VDM)

## 3. Abstract

This T2 instrument proposal certifies meters for the onset of self-organization in open nonequilibrium systems, with emphasis on excess-entropy-production trends, leading-eigenvalue bifurcation diagnostics, localized structure detection, and branch-stability overlays. The instruments are defined against canonical anchors and enforced by machine-checkable KPIs and JSON Schemas. Artifacts (PNG/CSV/JSON) are routed via io_paths with full provenance and contradiction handling. No phenomena claims are made at T2.

## 4. Background & Scientific Rationale

Lattice field methods (DeGrand & DeTar) emphasize meters-first exactness: symplectic/reversible proposals, acceptance diagnostics, and statistically sound error bars with autocorrelation awareness. VDM’s nonequilibrium meters adopt the same discipline: (i) EEP trend conformity near steady state, (ii) linear stability via leading eigenvalues with explicit sign changes in $\Re(\lambda_1)$ across control ladders, (iii) morphology-aware yet report-only localized structure detection at T2, and (iv) scale-program consistency for branch overlays. Prior T2 instruments in VDM (e.g., entropy meters) inform JSON/CSV/PNG sidecar discipline and contradiction routing.

## 5. Intellectual Merit and Procedure

- Importance: Instruments quantify onset without conflating it with phenomena claims, enabling reproducible T3+ work later.
- Broader impacts: Establishes cross-domain meters and CI discipline for nonequilibrium claims within VDM’s canon.
- Clarity: KPIs map 1:1 to anchors; CSV/JSON schemas support automated validation in CI.
- Rigor: Double precision, deterministic seeds, CI smoke and nightly preset ladders; contradiction routing on any gate failure.

### 5.1 Experimental Setup and Diagnostics

- Required parameters (units in canon):
  - Control grid: $\beta$ ladder (dimensionless), $N$ (grid size), $\Delta t$ (time step), BC tag, threshold $\theta$ (fraction of P95), eigen tolerance $\varepsilon_{\text{eig}}$.
- Diagnostics and counts:
  - EEP panel (1 per $\beta$): PNG+CSV+JSON; leading eigen card (1 per $\beta$): JSON (+ optional eigenmode PNG); localized overlay (>=1): PNG+JSON; branch-stability overlay (1): PNG.
- New instrument helpers to be provided in code:
  - ExcessEntropyMonitor, Bifurcation card generator, LocalizedStructureDetector, BranchClassifier, artifact writers bound to io_paths.

#### 5.1.1 Pre-Run Config Requirements

- Files and paths (domain: self_org):
  - APPROVAL manifest: Derivation/code/physics/self_org/APPROVAL.json
  - Preregistration manifest: Derivation/code/physics/self_org/PRE-REGISTRATION.json
  - Schemas: Derivation/code/physics/self_org/schemas/
    - prereg_self_org_t2.schema.json (manifest)
    - eep_monitor_panel.schema.json
    - bifurcation_card.schema.json
    - localized_report.schema.json
    - branch_stability_overlay.schema.json
  - Specs: Derivation/code/physics/self_org/specs/
    - self_org_onset_meters.v1.json

- APPROVAL.json required fields (template-aligned):
  - pre_registered = true; proposal path; allowed_tags; schema_dir; approvals map with schema refs, approver, timestamps, approval_key.

- PRE-REGISTRATION.json minimum keys (salted provenance per stamp tool):
  - proposal_title, tier_grade="T2", commit, salted_provenance, contact[], variables {independent, dependent, controls}, pass_fail[], spec_refs[], registration_timestamp.
  - Salted provenance: compute base_sha256, salt_hex, salted_sha256 using [Derivation/code/common/provenance/stamp_proposal.py](../../Derivation/code/common/provenance/stamp_proposal.py). Record values in PRE-REGISTRATION.json and reference tag message.
  - Create annotated, signed tag prereg.self_org_onset_meters.v1.YYYYMMDDThhmmZ containing commit, prereg path, salted provenance.

- Cross-reference:
  - This proposal embeds a full prereg example (Section 16) and JSON Schemas (Section 17). CI must validate manifests and outputs against these schemas prior to acceptance.

### 5.2 Experimental runplan

- Cartesian product:
  - $N \in \{64, 128, 256\}$; seeds $S \in \{0,\dots,4\}$; $\beta$ ladder of 7–11 points bracketing onset; $w_{\text{tail}} \in \{3,5,7\}$; $BC \in \{\text{No-flux}, \text{Dirichlet}\}$.
- Runtime budget (indicative; finalize in spec):
  - CI smoke: $N=64$, $S=\{0\}$, 7-point $\beta$ ladder, $\Delta t$ per CFL → target < 60 s.
  - Nightly: full ladders and grids → target < 15 min per grid.
- Success actions:
  - All gates pass; publish artifacts under io_paths; update RESULTS with instrument section per standards.
- Failure actions:
  - Emit CONTRADICTION_REPORT.json; route artifacts to failed_runs/; open issue with JSON excerpts and environment.

## 6. Personnel

- Justin K. Lietz — Principal Investigator (PI), implementer, approver

## Appendix A — Canon map (anchors; no duplication)

- EEP near steady state: [VDM-E-150](../../Derivation/EQUATIONS.md#vdm-e-150)
- Open-system entropy balance (branch diagnostic): [VDM-E-151](../../Derivation/EQUATIONS.md#vdm-e-151)
- Leading-eigenvalue classification and critical control: [VDM-E-152](../../Derivation/EQUATIONS.md#vdm-e-152)
- Local-potential Lyapunov functional (patterned steady): [VDM-E-153](../../Derivation/EQUATIONS.md#vdm-e-153)

KPIs (gates, thresholds, and artifacts):

- EEP trend: [kpi-eep-trend](../../Derivation/VALIDATION_METRICS.md#kpi-eep-trend)
- Bifurcation card: [kpi-bifurcation-card](../../Derivation/VALIDATION_METRICS.md#kpi-bifurcation-card)
- Localized structures: [kpi-localized-structure](../../Derivation/VALIDATION_METRICS.md#kpi-localized-structure)
- Branch classifier: [kpi-branch-classifier](../../Derivation/VALIDATION_METRICS.md#kpi-branch-classifier)
- Branch-stability overlay: [kpi-branch-stability-plot](../../Derivation/VALIDATION_METRICS.md#kpi-branch-stability-plot)

Implementation helpers (instruments’ APIs; reference only):

- prigogine_gates: [Derivation/code/common/instrument_helpers/prigogine_gates.py](../../Derivation/code/common/instrument_helpers/prigogine_gates.py)

## 3. Scope & goal (meters-first)

Goal: certify the correctness and reproducibility of onset diagnostics that indicate proximity to instability and characterize branch type (thermo vs dissipative vs Hopf) without asserting a physical pattern occurrence beyond instrument calibration.

Non-goals (explicitly out-of-scope at T2):

- No claims about the existence/persistence of patterns in a target PDE beyond producing the instrument outputs and gates.
- No parameter-sweep phenomena or secondary-branch physics assertions. Those belong to T3–T6.

## 4. Variables

Independent variables (by track):

- Control parameter $\beta$ ladder (dimensionless), grid resolution $N \in \{64, 128, 256\}$, seeds $S \in \{0,\dots,4\}$
- For EEP: window size $w_{\text{tail}} \in \{3,5,7\}$ for tail-slope gate robustness; baseline computation mode {scalar, field}
- For eigen analysis: boundary conditions tag $BC \in \{\text{Dirichlet}, \text{No-flux}\}$; eigen-solver tolerance $\varepsilon_{\text{eig}} \in \{10^{-8}, 10^{-10}\}$
- For localized detector: threshold $\theta$ as fraction of field’s P95 $\in \{0.6, 0.7, 0.8\}$
- For open-system flux: conduction $\kappa$ benchmark tag; numerical derivative stencil selection

Dependent variables:

- EEP series $\delta_p \sigma^{(e)}(t)$, tail trend slope $\frac{\mathrm{d}}{\mathrm{d}t}\,\delta_p \sigma^{(e)}$
- Leading eigenvalue $\lambda_1(\beta) = \Re + i\,\Im$; classification label $L \in \{\text{thermo}, \text{dissipative}, \text{hopf}\}$
- Localized component count and measures $\{\text{area}, r_{\mathrm{eq}}, \text{bbox}, \text{peak}\}$
- Overlay arrays: controls $\{\beta_i\}$, $\{\Re(\lambda_1)_i\}$, $\{\text{EEP\_trend}_i\}$, $\{\text{boundary\_entropy\_flux}_i\}$

Controls:

- Time-step $\Delta t$ per CFL/solver stability in domain-specific runners; deterministic seed; IEEE-754 double precision
- Artifact routing via io_paths with strict basenames and provenance

## 5. Equipment / Environment

- OS: Linux; double precision only; single-threaded and/or deterministic BLAS where relevant
- Determinism receipts: record seeds, commit hash, environment summary in JSON sidecars
- No heavy dependencies added. Matplotlib optional for plots (PNG); NumPy baseline

## 6. Methods / Procedure

### 6.1 EEP meter (VDM-A-043)

- Initialize `ExcessEntropyMonitor(tol=1e-12)` and set baseline $\sigma^\star$ under identical BCs.
- Run near-equilibrium sweeps and log $\delta_p \sigma^{(e)}(t)$ and the discrete derivative for each step.
- Gate: rolling worst positive slope over tail window $\le \text{tol}$ (default $10^{-12}$).
- Artifacts: EEP time series PNG (EEP + $\mathrm{d}/\mathrm{d}t$ EEP), CSV$(t,\ \text{eep},\ \text{de\_dt})$, JSON summary with gate boolean and meta.

### 6.2 Bifurcation card + branch classifier (VDM-A-044)

- Construct the linearized operator $L(\beta)$ about the reference state including BCs.
- Compute leading eigenpair $(\lambda_1, e_1)$ per $\beta$; optional eigenmode image if 2D.
- Classify branch with `classify_branch`(EEP tail slope, $\Re\,\lambda_1$, $\Im\,\lambda_1$, `has_nontrivial_mode`).
- Gate: detect sign-change in $\Re(\lambda_1)$ across the $\beta$ ladder; $\min |\Re(\lambda_1)| \le 10^{-6}$ within tolerance band.
- Artifacts: per-$\beta$ JSON card $\{\beta, \Re, \Im, \text{branch}, \text{eigenmode\_path?}\}$; optional eigenmode PNG.

### 6.3 Localized-structure detector (VDM-A-045)

- On selected $\beta$/time slices, compute activity field $A(x)$ (e.g., $|u|$, $|\nabla u|$, $\sigma$).
- Detect connected components of super-threshold regions via `detect_localized_structures`$(A,\ \theta,\ dx,\ dy)$.
- Gate at T2: report-only. When used later for phenomena, require component count $\ge 1$ plus measures.
- Artifacts: overlay PNG with bounding boxes and JSON listing per-component metrics.

### 6.4 Branch-stability overlay (VDM-A-046)

- Collate arrays $\{\beta_i\}$, $\{\Re(\lambda_1)_i\}$, optional $\{\text{EEP\_trend}_i\}$, optional $\{\text{boundary\_entropy\_flux}_i\}$.
- Produce overlay PNG via `branch_stability_plot(...)`.
- Gate at T2: report-only; annotate where $\Re(\lambda_1)$ changes sign; optional entropy-flux curve.
- Artifacts: overlay PNG; inputs CSV/JSON if runner implements logging.

## 7. Runners & IO policy

Planned instrument runner:

- Path: Derivation/code/physics/self_org/self_org_instrument_runner.py
- CLI: seed, $\beta$-grid, $N$, $BC$, $\theta$, windows; output paths delegated to io_paths via tag

IO policy:

- Each PNG has CSV/JSON with same basename; captions include numeric values (slope, $R^2$, CI, thresholds).
- JSON includes commit, seeds, environment, parameters, and gate decisions.
- On gate failure: emit `CONTRADICTION_REPORT.json` and route all outputs to `failed_runs/`.

## 8. Acceptance gates (hard thresholds)

EEP trend gate (kpi-eep-trend):

- $\text{worst\_positive\_tail\_slope} \le 10^{-12}$ for window $\in \{3,5,7\}$; must pass for $\ge 2$ windows.

Bifurcation detection (kpi-bifurcation-card):

- Detect sign change in $\Re(\lambda_1)$ on the $\beta$ ladder; $\min |\Re(\lambda_1)| \le 10^{-6}$ within solver’s tolerance; JSON cards written per $\beta$.

Branch classifier consistency (kpi-branch-classifier):

- If $\Re(\lambda_1) < 0$ and EEP trend $\le 0$ and `has_nontrivial_mode=false` → `branch=thermo`.
- If $|\Re(\lambda_1)| \le 10^{-8}$ and $\Im(\lambda_1) \ne 0$ → `branch=hopf`.
- Else → `branch=dissipative`.
- JSON summary denotes `classification_consistent = true`.

Localized detector (kpi-localized-structure):

- Report-only (T2). JSON lists components; PNG overlay present. For future T3+ claims, require $\ge 1$ component + measures.

Branch-stability overlay (kpi-branch-stability-plot):

- Report-only (T2). PNG overlay exists with consistent units and sign conventions.

## 9. Datasets / Benches

- Linear RD about homogeneous state with analytic dispersion controls; small-amplitude noise; periodic domain for eigen tests with BC-variants where applicable; conduction benches with Dirichlet walls for $\Phi$ and boundary-flux terms.

- Grids: $N \in \{64, 128, 256\}$. $\beta$-ladders: 7–11 points covering below/near/above onset. Seeds: $S \in \{0,\dots,4\}$.

## 10. Results / Artifacts (what will be produced)

- `eep_monitor_panel__<tag>.png`, `.csv`, `.json`
- `bifurcation_card__β=<value>__<tag>.json` [+ optional eigenmode PNG]
- `localized_overlay__<tag>.png` and `localized_report__<tag>.json`
- `branch_stability__<tag>.png` [+ optional csv/json inputs]
- `CONTRADICTION_REPORT.json` on any gate failure

## 11. Determinism & provenance

- Record seeds, commit hash, environment summary in all JSON sidecars.
- Where stochastic components are used (noise/initialization), set seeds explicitly and include in JSON.

## 12. Risks & mitigations

- Noisy EEP estimates: use multiple tail windows; smooth with minimal bias (median/robust).
- Eigenvalue sensitivity: verify solver tolerance; locate sign change by bracketing $\beta$; include $\min |\Re(\lambda_1)|$ report.
- Detector threshold bias: report $\theta$ as fraction of P95; provide per-component measures to reduce arbitrariness.

## 13. Escalation path

- If T2 passes, promote to T3 (smoke) to demonstrate onset in controlled PDEs (e.g., Schnakenberg/Turing regimes) with the certified meters.
- Later T4 prereg can lock claims about onset parameters and morphology classes with ablations and CI.

## 14. Approval & policy

- Requires approval per Derivation/code/ARCHITECTURE.md and authorization README.
- Unapproved runs must be quarantined and tagged `engineering_only` with explicit warning in JSON.

## 15. References

- Mapping note: [docs/misc-standards/Self-Organization_Upgrade_Map.md](../../docs/misc-standards/Self-Organization_Upgrade_Map.md)
- Non-Equilibrium Thermodynamics framework: [docs/misc-standards/Non-Equilibrium-Thermodynamics.md](../../docs/misc-standards/Non-Equilibrium-Thermodynamics.md)

## 16. Preregistration JSON (T2 instrument)

The instrument run MUST be preregistered with a JSON manifest that declares parameters, gates, artifacts, routing, and provenance. Save alongside outputs and include the path in every sidecar.

```json
{
  "version": "1.0",
  "tier": "T2",
  "instrument_id": "self_org_onset_meters",
  "anchors": {
    "equations": ["VDM-E-150", "VDM-E-151", "VDM-E-152", "VDM-E-153"],
    "kpis": [
      "kpi-eep-trend",
      "kpi-bifurcation-card",
      "kpi-localized-structure",
      "kpi-branch-classifier",
      "kpi-branch-stability-plot"
    ],
    "docs": {
      "equations_md": "../../Derivation/EQUATIONS.md",
      "metrics_md": "../../Derivation/VALIDATION_METRICS.md",
      "schemas_md": "../../Derivation/SCHEMAS.md",
      "proposal_md": "../../Derivation/Nonequilibrium/T2_PROPOSAL_Self_Organization_Meters_v1.md"
    }
  },
  "parameters": {
    "seed": 0,
    "beta_grid": {"type": "linspace", "start": 0.1, "stop": 0.5, "num": 9},
    "N": 128,
    "BC": "No-flux",
    "theta_fraction_of_P95": 0.7,
    "w_tail_options": [3, 5, 7],
    "eig_tolerance": 1e-8,
    "dt": 1e-3
  },
  "gates": {
    "eep_trend": {"worst_positive_tail_slope_max": 1e-12, "required_windows_pass": 2},
    "bifurcation": {"min_abs_Re_lambda1_max": 1e-6, "require_sign_change": true},
    "branch_classifier": {"consistency_required": true},
    "localized_detector": {"mode": "report_only"},
    "branch_stability_overlay": {"mode": "report_only"}
  },
  "artifacts_expected": [
    "eep_monitor_panel__*.png",
    "eep_monitor_panel__*.csv",
    "eep_monitor_panel__*.json",
    "bifurcation_card__β=*_*.json",
    "localized_overlay__*.png",
    "localized_report__*.json",
    "branch_stability__*.png"
  ],
  "io_paths": {
    "figures_dir": "../../Derivation/code/outputs/figures/nonequilibrium",
    "logs_dir": "../../Derivation/code/outputs/logs/nonequilibrium"
  },
  "provenance": {
    "commit": "{git rev-parse HEAD}",
    "environment": "Linux; Python; IEEE-754 double",
    "created_at": "2025-11-08T00:00:00Z"
  },
  "contradiction_policy": {
    "on_gate_failure": "route_to_failed_runs",
    "report": "CONTRADICTION_REPORT.json"
  },
  "schema_uri": "vdm://schemas/nonequilibrium/prereg_self_org_t2.schema.json"
}
```

## 17. JSON Schemas (machine-validated)

Authoritative registry: [Derivation/SCHEMAS.md](../../Derivation/SCHEMAS.md). Below are self-contained JSON Schemas used for CI validation.

### 17.1 eep_monitor_panel.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "vdm://schemas/nonequilibrium/eep_monitor_panel.schema.json",
  "type": "object",
  "required": ["meta", "series", "gate"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["seed", "commit", "dt", "N", "BC"],
      "properties": {
        "seed": {"type": "integer"},
        "commit": {"type": "string"},
        "dt": {"type": "number"},
        "N": {"type": "integer"},
        "BC": {"type": "string"},
        "beta": {"type": "number"}
      },
      "additionalProperties": true
    },
    "series": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["t", "eep", "de_dt"],
        "properties": {
          "t": {"type": "number"},
          "eep": {"type": "number"},
          "de_dt": {"type": "number"}
        },
        "additionalProperties": false
      }
    },
    "gate": {
      "type": "object",
      "required": ["worst_positive_tail_slope", "windows", "pass"],
      "properties": {
        "worst_positive_tail_slope": {"type": "number"},
        "windows": {
          "type": "array",
          "items": {"type": "integer"}
        },
        "pass": {"type": "boolean"},
        "tolerance": {"type": "number"}
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

### 17.2 bifurcation_card.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "vdm://schemas/nonequilibrium/bifurcation_card.schema.json",
  "type": "object",
  "required": ["beta", "Re", "Im", "branch"],
  "properties": {
    "beta": {"type": "number"},
    "Re": {"type": "number"},
    "Im": {"type": "number"},
    "branch": {"type": "string", "enum": ["thermo", "dissipative", "hopf"]},
    "eigenmode_path": {"type": "string"}
  },
  "additionalProperties": false
}
```

### 17.3 localized_report.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "vdm://schemas/nonequilibrium/localized_report.schema.json",
  "type": "object",
  "required": ["meta", "components"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["beta", "theta_fraction_of_P95"],
      "properties": {
        "beta": {"type": "number"},
        "theta_fraction_of_P95": {"type": "number"}
      },
      "additionalProperties": true
    },
    "components": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["label", "area", "r_eq", "bbox", "peak"],
        "properties": {
          "label": {"type": "integer"},
          "area": {"type": "number"},
          "r_eq": {"type": "number"},
          "bbox": {
            "type": "array",
            "minItems": 4,
            "maxItems": 4,
            "items": {"type": "number"}
          },
          "peak": {"type": "number"}
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

### 17.4 branch_stability_overlay.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "vdm://schemas/nonequilibrium/branch_stability_overlay.schema.json",
  "type": "object",
  "required": ["beta", "Re_lambda1"],
  "properties": {
    "beta": {
      "type": "array",
      "items": {"type": "number"}
    },
    "Re_lambda1": {
      "type": "array",
      "items": {"type": "number"}
    },
    "eep_trend": {
      "type": "array",
      "items": {"type": "number"}
    },
    "boundary_entropy_flux": {
      "type": "array",
      "items": {"type": "number"}
    }
  },
  "additionalProperties": false
}
```
