# Prometheus_VDM — Asset Index (Proposals, RESULTS, Runners, Instruments, Runtime)

Purpose
- A living, single-page index of major assets in this repository:
  - PROPOSALS (with commit-pinned permalinks)
  - RESULTS (artifacted, with PASS/FAIL summaries)
  - RUNNERS (scripts/CLIs)
  - INSTRUMENTS (meters/diagnostics)
  - Runtime boundary stack (fum_rt)
- Update this file whenever you add a PROPOSAL_*, RESULTS_*, or new runner/meter.

Status keys
- [Present] in repo now
- [Planned] stub or pending implementation
- [Add link] add exact path and, if appropriate, a commit-pinned permalink

Last updated: 2025‑11‑02 (UTC)

---

## 0) Canon & Core References

- Axioms (A0–A7) — [Present]  
  [AXIOMS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/main/Derivation/AXIOMS.md)
- Equations & Instruments — [Present]  
  [EQUATIONS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/main/Derivation/EQUATIONS.md)
- Validation Metrics — [Present]  
  [VALIDATION_METRICS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/main/Derivation/VALIDATION_METRICS.md)
- Units/Normalization — [Present]  
  [UNITS_NORMALIZATION.md](https://github.com/justinlietz93/Prometheus_VDM/blob/main/Derivation/UNITS_NORMALIZATION.md)
- Schemas (Observation etc.) — [Present]  
  [SCHEMAS.md](https://github.com/justinlietz93/Prometheus_VDM/blob/main/Derivation/SCHEMAS.md)

---

## 1) PROPOSALS (commit‑pinned where available)

A8 (Axiom Candidate)
- T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md

Echo / Causality (Quantum Echos)
- T0_PROPOSAL_SIE_Willow-Convergence_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/Quantum/Quantum_Echos/T0_PROPOSAL_SIE_Willow-Convergence_v1.md
- T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md
- T4_PROPOSAL_SMAE_CEG_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_SMAE_CEG_v1.md
- T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/Quantum/Quantum_Echos/T4_PROPOSAL_Echo-Limited-Causality-in-Metriplectic-VDM_T4_v1.md

Foundations / Measurement / Quantum Engines
- T4_PROPOSAL_J-to_Dirac_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/Quantum/T4_PROPOSAL_J-to_Dirac_v1.md
- T4_PROPOSAL_Quantum-Resource-Engine_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/53f2e11c09a10adda3b5294dab6a57a20bc9f922/Derivation/Quantum/Quantum_Engine/T4_PROPOSAL_Quantum-Resource-Engine_v1.md

Dark Matter / GR Spine
- T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md — [Present]  
  https://github.com/justinlietz93/Prometheus_VDM/blob/main/Derivation/Dark_Matter/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md

(Add any additional PROPOSAL_* here with commit‑pinned links)

---

## 2) RESULTS (artifacted instruments and studies)

List every RESULTS_* document, with gate summaries and artifact basenames. Use one line per result and keep a consistent pattern.

Template entry (replace with actual):
- RESULTS_[SHORT_TAG].md — [RESULTS posted] | PASS/FAIL summary | PNG/CSV/JSON basenames | Seeds/commit in captions — [Add link]

Suggested categories to fill (based on canon):
- RD dispersion (σ(k)=r−Dk²) — [Add link]
- RD front speed (2√Dr) — [Add link]
- KG Noether drift bounds — [Add link]
- FRW continuity / residual QC — [Add link]
- Tachyonic tube spectrum — [Add link]
- Metriplectic structure checks (degeneracy residuals g₁,g₂) — [Add link]
- Any Echo/CEG execution results — [Add link]
- Any Cosmology pipeline results — [Add link]
- Any A8 gate runs (G1–G12) — [Add link]

---

## 3) RUNNERS (scripts/CLIs)

Record paths to actual runner scripts (and note when a path is only a proposed location inside a PROPOSAL).

Examples to populate:
- Derivation/code/.../[runner_name].py — [Present] | purpose: [short] — [Add link]
- Derivation/.../quantum/sie_willow_convergence_v1.py — [Proposed in T0 PROPOSAL] — [Add link if created]
- Any A8 runner(s) (physics bench) — [Planned] — [Add link]
- Any Telegraph–Fisher runner(s) — [Planned] — [Add link]
- Any cosmology CLI(s) — [Planned] — [Add link]

---

## 4) INSTRUMENTS / METERS (code modules or notebooks)

List concrete meter implementations (paths) once they exist. Until then, note conceptual instruments anchored in canon.

Conceptual instruments (per canon; replace with concrete paths when implemented):
- RD dispersion meter — [Add link]
- RD front‑speed meter — [Add link]
- Noether/energy drift monitors — [Add link]
- H‑theorem / discrete‑gradient Σ monitor — [Add link]
- Cone‑slack meter (telegraph/causality) — [Add link]
- κ‑collapse validator — [Add link]
- A8 hierarchy meters: boundary detector (physics bench), depth N(L), α, α_I, β_E — [Planned] — [Add link]
- Minkowski morphometry & deconvolution — [Planned] — [Add link]

---

## 5) A8 Program (Hierarchy, Area‑law, Information)

- Proposal: T8_A8_PROPOSAL… — [Present] (link above)
- Physics‑bench meters (boundary → Γ, N(L), α, α_I, β_E) — [Planned] — [Add link]
- Cross‑grid/ε invariance and morphometry/deconvolution — [Planned] — [Add link]
- RESULTS_A8_* (G1–G12) — [Missing] — [Add link]

---

## 6) Causality Program (Telegraph–Fisher)

- Proposal: Echo‑Limited Causality (T4) — [Present] (link above)
- Stepper + meters (cone‑slack, κ‑collapse) — [Planned] — [Add link]
- RESULTS_Telegraph_Fisher_* — [Missing] — [Add link]

---

## 7) Cosmology Spine

- Units/FRW QC — [Present] (link above)
- Primordial P(k) generator — [Planned] — [Add link]
- Evolution interface (CLASS/CAMB style) — [Planned] — [Add link]
- RESULTS_Cosmology_* — [Missing] — [Add link]

---

## 8) Runtime Boundary Detection (fum_rt stack)

- Event schema (boundary_probe; cut_strength) — [Present]  
  fum_rt/core/announce.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/main/fum_rt/core/announce.py
- Incremental boundary maintenance (EWMA cut_strength, churn) — [Present]  
  fum_rt/core/adc.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/main/fum_rt/core/adc.py
- Frontier scout (edge/cut/cohesion targeting) — [Present]  
  fum_rt/core/cortex/void_walkers/void_frontier_scout.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/main/fum_rt/core/cortex/void_walkers/void_frontier_scout.py
- Engine wiring & metrics exposure — [Present]  
  fum_rt/core/engine/core_engine.py  
  https://github.com/justinlietz93/Prometheus_VDM/blob/main/fum_rt/core/engine/core_engine.py

Note
- Detector is implemented and running in the runtime. The physics‑bench A8 meters are separate and currently [Planned].

---

## 9) Quick Status (high‑stakes)

- A8 gates executed: 0/12 — [Missing]
- Telegraph–Fisher stepper/meters: [Missing]
- Runtime boundary detector: [Present]
- Echo/SMAE proposals: [Present]
- Core instruments (RD/KPP/KG/FRW) referenced in canon: [Present], RESULTS links to be added here

---

## 10) Edit checklist for maintainers

- When you land a new PROPOSAL_*, add it here with a commit‑pinned permalink.
- When you post a RESULTS_*, add the doc path, PASS/FAIL summary, and artifact basenames.
- Record new runners (exact script paths) and instruments (module paths) as they are created.
- Keep the Quick Status honest (A8, TF, etc.).
