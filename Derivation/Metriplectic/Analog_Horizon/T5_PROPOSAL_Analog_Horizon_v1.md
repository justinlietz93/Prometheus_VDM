# T5 (Pilot) - Analog Horizon — Telegraph‑Fisher Causality & Causal Dominance Meter

> Created Date:  2025-11-18  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI), partner lab (to be named).

## 3. Abstract

Proposed in this document is a laboratory analog experiment where transport obeys **Telegraph–Fisher (TF)** dynamics with tunable diffusion (D) and relaxation (τ), enabling an **independent** sweep of J‑like and M‑like knobs. The objective is to measure cone arrival times and verify **Causal Dominance**: operational signal speed of the full metriplectic system is bounded by the J‑limb c, with TF speed $c_{\mathrm{TF}}=\sqrt{D/\tau}$ calibrated to c within tolerance.

## 4. Background & Scientific Rationale

M‑limb parabolic models lack strict cones; TF regularization restores finite speed. This test checks whether the bound $v_{\rm max}\le c$ persists when dissipation is strong and independently tunable.

## 5. Intellectual Merit and Procedure

(1) Importance: direct falsifier for S4; (2) Impacts: tests emergent SR enforcement; (3) Approach: pulsed excitation, cone‑front timing, independent (D,τ) control, Born‑rule meter convergence in ensembles.

## 5.1 Experimental Setup and Diagnostics

- **Platform:** any medium realizing TF dynamics (electrical/acoustic meta‑lattice, BEC phononics).  
- **Knobs:** D via coupling; τ via relaxation network; J‑limb c from wave branch.  
- **Diagnostics:** cone slope (front arrival) and slack; TF dispersion; reproducibility across pulses.  
- **Acceptance (gates):** (G1) |c_TF/c_J − 1| ≤ 0.02; (G2) cone‑slack ≤ 2%; (G3) reproducibility across runs (Jaccard ≥ 0.7 of detected fronts).

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
    { "id": "H_CONE", "statement": "Operational cone slack ≤ 2% under J⊕M coupling.", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["D", "τ", "pulse width", "pulse energy", "lattice size"],
    "dependent": ["c_TF/c_J", "cone_slack", "arrival_speed"],
    "controls": ["temperature", "boundary conditions", "sampling rate"]
  },
  "pass_fail": [
    { "metric": "c_TF/c_J", "operator": "between", "threshold": [0.98, 1.02], "unit": "" },
    { "metric": "cone_slack", "operator": "<=", "threshold": 0.02, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/causality/specs/analog-horizon.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Experimental runplan

Pulse → record field/video → estimate cone front → fit slopes with bootstrap CI. Failure: CONTRADICTION_REPORT, including calibration logs for (D,τ,c_J).
