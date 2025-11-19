# 1. T5 (Pilot) — Analog Horizon — Telegraph‑Fisher Causality & Causal Dominance Meter

> Created Date:  2025-11-18
> Commit: eae2bb4479795aaa5d079a878060eff29cae69e1
> Salted provenance: {salted_hash}
> Proposer contact(s):  (<justin@neuroca.ai>)
> License: See LICENSE
> Short summary (one sentence TL;DR):  T5 pilot using a Wave Flux Meter–based analog horizon with Telegraph–Fisher dynamics to test causal dominance ($v_{\max} \le c_J$) and A8 boundary‑encoding signatures under controlled $M$‑limb injections.

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI), partner lab (to be named).

## 3. Abstract

Proposed in this document is a laboratory analog experiment where transport obeys **Telegraph–Fisher (TF)** dynamics with tunable diffusion (D) and relaxation (τ), enabling an **independent** sweep of J‑like and M‑like knobs. The objective is to measure cone arrival times and verify **Causal Dominance**: operational signal speed of the full metriplectic system is bounded by the J‑limb c, with TF speed $c_{\mathrm{TF}}=\sqrt{D/\tau}$ calibrated to c within tolerance.

## 4. Background & Scientific Rationale

M‑limb parabolic models lack strict cones; TF regularization restores finite speed. This test checks whether the bound $v_{\rm max}\le c$ persists when dissipation is strong and independently tunable.

## 5. Intellectual Merit and Procedure

(1) Importance: direct falsifier for S4; (2) Impacts: tests emergent SR enforcement; (3) Approach: pulsed excitation, cone‑front timing, independent (D,τ) control, Born‑rule meter convergence in ensembles.

## 5.1 Experimental Setup and Diagnostics

- **Platform:** Wave Flux Meter–based analog horizon geometry: a 2D scalar-wave/phonon medium with open ports and absorbing sponge (as in the Wave Flux Meter Phase B instrument), modified so that the effective propagation speed and channel map define a codimension‑1 “horizon” surface. Implementations may be electrical/acoustic meta‑lattices or BEC phononics, but must reproduce the Wave Flux Meter energy/flux meters and balance diagnostics.
- **Knobs:** D via coupling network; τ via local relaxation elements; J‑limb wave speed c_J from the reversible branch; M‑limb control via tunable damping/projection consistent with metriplectic structure.
- **Diagnostics:** (i) cone slope and slack (TF front arrival) vs J‑only light cone; (ii) TF dispersion; (iii) Wave Flux Meter power‑balance metrics (R²_balance, relative imbalance, absorber efficiency) at the horizon; (iv) A8 observables — α/α_I ratio and ΔΣ–ΔI correlation measured on bands straddling the horizon boundary.
- **Acceptance (gates):**
  - (G1) $|c_{TF}/c_{J} − 1| ≤ 0.02$.
  - (G2) cone‑slack ≤ 2%.
  - (G3) reproducibility across runs (Jaccard ≥ 0.7 of detected fronts).
  - (G4) Wave Flux Meter balance gates remain in PASS regime in the analog‑horizon configuration: R²(−dE/dt, P_out) ≥ 0.9995; relative imbalance ≤ 0.5%; absorber efficiency ≥ 0.9 (matching Phase B open‑ports standards in [`VDM_Code_Standards_Technical_Summary.md`](docs/misc-standards/VDM_Code_Standards_Technical_Summary.md:183-199)).
  - (G5) ΔΣ–ΔI correlation at the horizon is positive and above a preregistered minimum (see `deltaSigmaDeltaI_corr` gate in PRE‑REG), indicating boundary‑encoded information consistent with the EBN‑Analog‑Horizon milestone.

### 5.1.1 Pre-Run Config Requirements

- **Approvals (causality domain):**
  - `Derivation/code/physics/causality/APPROVAL.json` — analog‑horizon runner approval manifest (must reference this proposal path and allowed tags).
  - `Derivation/code/physics/causality/PRE-REGISTRATION.json` — preregistration manifest including salted provenance, hypotheses, variables, pass/fail metrics, and spec references for analog‑horizon runs.
- **Schemas (causality domain):**
  - `Derivation/code/physics/causality/schemas/analog-horizon.schema.json` — JSON Schema for `analog-horizon.v1` run specs and summary logs (includes TF parameters, cone metrics, ΔΣ–ΔI metrics, and Wave Flux Meter balance fields).
- **Specs (causality domain):**
  - `Derivation/code/physics/causality/specs/analog-horizon.v1.json` — spec files referenced in `spec_refs` below; define grids, TF parameters (D, τ), pulse shapes, seeds, and measurement windows.
- **Dependencies (Wave Flux Meter instrument):**
  - `Derivation/code/physics/thermo_routing/APPROVAL.json` and associated schemas/specs for the Wave Flux Meter (`wave-flux-meter-summary-v1.schema.json`, `wfm.openports.v1*.json`) must be in PASS/approved state. Analog‑horizon runs are allowed to write artifacts only if Wave Flux Meter Phase A/B results remain certified as T2 instruments (see [`RESULTS_Wave_Flux_Meter_A_Phase_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md) and [`RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md)).

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "Analog Horizon — Telegraph-Fisher Causality",
  "tier_grade": "T5",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_TF", "statement": "c_TF matches c_J within 2% across calibrated settings.", "direction": "no-change" },
    { "id": "H_CONE", "statement": "Operational cone slack ≤ 2% under J⊕M coupling.", "direction": "decrease" },
    { "id": "H_ALPHA", "statement": "The ratio α/α_I measured at the analog horizon scales with boundary measure as predicted by the A8 hierarchy model.", "direction": "increase" },
    { "id": "H_INFO", "statement": "ΔΣ–ΔI correlation at the horizon exceeds a preregistered minimum, indicating boundary-encoded information under M injections.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["D", "τ", "pulse width", "pulse energy", "lattice size"],
    "dependent": [
      "c_TF/c_J",
      "cone_slack",
      "arrival_speed",
      "R2_balance",
      "imbalance_rel",
      "absorber_eff",
      "deltaSigmaDeltaI_corr"
    ],
    "controls": ["temperature", "boundary conditions", "sampling rate", "channel map", "horizon location"]
  },
  "pass_fail": [
    { "metric": "c_TF/c_J", "operator": "between", "threshold": [0.98, 1.02], "unit": "" },
    { "metric": "cone_slack", "operator": "<=", "threshold": 0.02, "unit": "" },
    { "metric": "R2_balance", "operator": ">=", "threshold": 0.9995, "unit": "" },
    { "metric": "imbalance_rel", "operator": "<=", "threshold": 0.005, "unit": "" },
    { "metric": "absorber_eff", "operator": ">=", "threshold": 0.9, "unit": "" },
    { "metric": "deltaSigmaDeltaI_corr", "operator": ">=", "threshold": 0.3, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/physics/causality/specs/analog-horizon.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

### Minimal spec example (analog-horizon.v1)

The file `Derivation/code/physics/causality/specs/analog-horizon.v1.json` must contain at least one spec entry of the following shape (keys and units as in §5.1 and §5.1.1):

```json
{
  "run_name": "analog-horizon-baseline",
  "version": "1.0.0",
  "tag": "analog-horizon.v1",
  "schema_ref": "Derivation/code/physics/causality/schemas/analog-horizon.schema.json",
  "parameters": {
    "D": 0.12,
    "tau": 0.8,
    "pulse_width": 12.0,
    "pulse_energy": 1.0,
    "lattice_size": [128, 128],
    "horizon_location": {
      "band": [48, 80],
      "ports": ["left", "right"]
    },
    "channel_map": "wfm-phaseB-openports-v1"
  },
  "seeds": [42, 43, 44]
}
```

This is a **minimal illustrative example**, not a canonical choice of instrument parameters. Actual production specs:

- Must use units and normalization consistent with [`00_UNITS_NORMALIZATION.md`](Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md:1) and the Wave Flux Meter / causality domain conventions.
- May include additional keys (e.g., detailed pulse shapes, hardware configuration identifiers) as long as they remain compatible with `analog-horizon.schema.json`.
- Must be validated by `analog-horizon.schema.json` and the causality `APPROVAL.json` gate before any artifact‑writing runs.

## 5.2 Experimental runplan

This section describes how the resources in §5.1 will be used, the approximate runtime and compute budget, and the success/failure actions.

1. **Instrument precheck (Wave Flux Meter).**
   - Confirm that Wave Flux Meter Phase A/B results remain in PASS state using approved specs (`wfm.openports.v1*.json`) and gates in the thermodynamic‑routing domain.
   - Rerun balance tests if the codebase or hardware has changed.
   - This step validates that the underlying meter geometry and energy/flux accounting remain within their T2 acceptance region before enabling analog‑horizon runs.

2. **TF calibration (per $(D,\tau)$ pair).**
   - For each candidate $(D,\tau)$ in the spec’s Cartesian product:
     - Run the J‑only branch to establish the reference cone.
     - Run the TF branch and measure cone fronts to calibrate $c_{\mathrm{TF}}$ to $c_J$ within the 2% gate using cone‑front timing fits with bootstrap CIs.
   - Record $(D,\tau,c_J,c_{\mathrm{TF}},\text{cone\_slack})$ in JSON/CSV.

3. **Horizon geometry configuration.**
   - Program the channel map and propagation‑speed profile so that a codimension‑1 analog horizon forms inside the Wave Flux Meter geometry.
   - Record the horizon boundary measure, associated ports, and the `horizon_location` band in the spec and logs.

4. **Pulse experiments (per spec).**
   - Inject pulsed excitations from the J‑limb side for each spec entry (combination of $(D,\tau,\text{pulse\_width},\text{pulse\_energy},\text{lattice\_size},\text{seeds})$).
   - Record field/video and Wave Flux Meter energy/flux logs.
   - Estimate cone fronts and compute:
     - $c_{\mathrm{TF}}/c_J$, cone_slack, arrival_speed.
     - Balance metrics: $R^2_{\text{balance}}$, imbalance_rel, absorber_eff.

5. **A8 information metrics.**
   - Using the same runs, compute $\alpha$, $\alpha_I$, $\Sigma$, and $I$ on bands straddling the horizon.
   - Form $\alpha/\alpha_I$ and $\Delta\Sigma$–$\Delta I$ correlation metrics.
   - Log these in JSON/CSV per RESULTS standards with explicit linkage to the A8 hierarchy program.

6. **Runtime and compute budget.**
   - Each TF calibration and pulse‑experiment configuration is expected to be $\mathcal{O}(\text{minutes})$ on a modern GPU/CPU, depending on lattice size and sampling rate.
   - The total compute budget per `analog-horizon.v1` spec is expected to remain within a few GPU‑hours or tens of CPU‑hours; exact counts (number of configs × number of seeds) are encoded in the spec and summarized in the JSON logs.

7. **Success and failure actions (gates, contradiction handling, publication).**
   - Apply the PRE‑REG pass/fail rules from the embedded PRE‑REG JSON on:
     - $c_{\mathrm{TF}}/c_J$, cone_slack, $R^2_{\text{balance}}$, imbalance_rel, absorber_eff, and deltaSigmaDeltaI_corr.
   - **On PASS:**
     - Emit `T5_RESULTS_Analog_Horizon_v1.md` (or equivalent RESULTS document) with:
       - Numbered figures and logs (PNG+CSV+JSON) via `io_paths`.
       - Clear gate matrices, linking back to specs, schemas, and PRE‑REG hypotheses.
     - Tag the commit with an annotated prereg tag containing the salted provenance and proposal path.
   - **On FAIL:**
     - Route all artifacts under the `failed_runs/` subtree for the causality domain via `io_paths.py`.
     - Emit a CONTRADICTION_REPORT JSON documenting which of $\{c_{\mathrm{TF}}/c_J,\text{cone\_slack},R^2_{\text{balance}},\text{imbalance\_rel},\text{absorber\_eff},\text{deltaSigmaDeltaI\_corr}\}$ violated the gates and summarizing the conditions under which failure occurred.

## 6. Personnel

Justin K. Lietz will design the analog‑horizon configuration, integrate the Wave Flux Meter instrumentation and TF runner, and interpret diagnostics under the A8 and causality programs. A partner laboratory (to be named) will operate the physical medium (electrical/acoustic/BEC), perform calibration and data collection according to this preregistered protocol, and return raw and reduced artifacts for audit.

## 7. References

- Wave Flux Meter instruments and results:
  - [`PROPOSAL_Wave_Flux_Meter_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_v1.md)
  - [`PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md)
  - [`PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/PROPOSAL_Wave_Flux_Meter_PhaseC_OpenPorts_v1.md)
  - [`RESULTS_Wave_Flux_Meter_A_Phase_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md)
  - [`RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md`](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_Phase_B_OpenPorts_v1.md)
- A8 milestones and gaps (EBN‑Analog‑Horizon context):
  - [`T8-A8_Milestones.md`](Derivation/Axioms/T8-A8_Milestones.md:199-219) — EBN‑Analog‑Horizon milestone (Wave Flux Meter geometry, α/α_I scaling, ΔΣ–ΔI correlation, and flux gates).
  - [`T8-A8_Gaps.md`](Derivation/Axioms/T8-A8_Gaps.md) — gap analysis and thermodynamic‑geometry guidance (including Ruppeiner‑style metrics) for horizon‑as‑boundary tests.
- Thermodynamic Routing and routing meters:
  - [`PROPOSAL_Passive_Thermodynamic_Routing_v2.md`](Derivation/Thermodynamic_Routing/Passive_Thermodynamic_Routing/PROPOSAL_Passive_Thermodynamic_Routing_v2.md)
  - Wave Flux Meter sections in [`VDM_OVERVIEW.md`](Derivation/VDM_OVERVIEW.md:158-163) and [`00_RESULTS.md`](Derivation/z.CANONICAL_Results/00_RESULTS.md:133-146).
- Standards and KPIs:
  - [`VDM_Code_Standards_Technical_Summary.md`](docs/misc-standards/VDM_Code_Standards_Technical_Summary.md) — code and meter standards, including Wave Flux Meter Phase B gates.
  - [`00_VALIDATION_METRICS.md`](Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) — global KPIs and cosmology/conservation gates reused where applicable.
