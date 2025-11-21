# CHRONICLES

<!-- Change Attestation Policy (Required) -->
<!-- This section defines the mandatory template for documenting any change under Derivation/. -->
<!-- The only bypass for Derivation edits without canon updates is explicit documentation here. -->

## Change Attestation — 2025-11-20 — CF9 Gauge Emergence and H006 Hypothesis

Dependency-Chain-Reviewed: true
Change-Type: canon-impacting
Summary: Created CF9 complete formalism deriving U(1) electromagnetic gauge field from Berry connection; created H006 hypothesis with Weinberg-Witten defense; extends matter emergence program (CF8 spinors → CF9 gauge bosons).

Paths-Changed:
- Derivation/Complete-Formalisms/CF9_Gauge_Emergence_Berry_Connection.md (NEW)
- Derivation/Gauge/H006_HYPOTHESIS_Gauge_Emergence_Weinberg_Witten_Defense.md (NEW)
- Derivation/Gauge/T6_PROPOSAL_Gauge_Emergence_v1.md (NEW)
- Derivation/Gauge/RED_TEAM_RESPONSE_Gauge_Emergence.md (NEW)
- Derivation/Gauge/T1_PROPOSAL_Gauge_Emergence.md (UPDATED)
- Derivation/z.CANONICAL_Hypotheses/00_HYPOTHESES.md (H006 entry added)
- Derivation/z.CANONICAL_Complete_Formalisms/00_COMPLETE_FORMALISMS.md (CF9 entry added)
- Derivation/z.CANONICAL_Chronicles/00_CHRONICLES.md (this entry)

Canon-Docs-Updated:
- Derivation/z.CANONICAL_Hypotheses/00_HYPOTHESES.md#h006
- Derivation/z.CANONICAL_Complete_Formalisms/00_COMPLETE_FORMALISMS.md (CF9 appended)

Dependency-Notes:
- Reviewed dependencies: CF1 (Berry connection foundation), CF8 (emergent spinor wavefunctions), AXIOMS.md (VDM-AX-004, A2, A3, A4)
- Upstream/downstream links:
  - CF1 §2.1 provides Berry connection $A_\mu = i\langle\psi|\partial_\mu\psi\rangle$
  - CF8 provides emergent spinor states $|\psi\rangle$ from domain walls
  - CF9 derives Maxwell action $S = -\frac{1}{4g^2}\int F_{\mu\nu}F^{\mu\nu}$ from Berry curvature
  - H006 defines 4 predictions (P1-P4) with experiments E1-E6
- Risk mitigation: Compatibility with Weinberg-Witten via geometric gauge fields (connection, not state)

Approval/PR:
- PR: copilot/evaluate-ninomiya-theorem (extends Nielsen-Ninomiya defense to gauge sector)
- Approval: pending principal researcher review for E1-E6 execution

---

## Change Attestation — TEMPLATE

Dependency-Chain-Reviewed: true
Change-Type: [pivot|minor-correction|file-shuffle|canon-impacting]
Summary: <one-line description of the change and rationale>
Paths-Changed:

- Derivation/path/to/changed/file.ext
- Derivation/another/changed/path.md
Canon-Docs-Updated:  # list canon docs if Change-Type is canon-impacting
- Derivation/EQUATIONS.md#<anchor>
- Derivation/VALIDATION_METRICS.md#<anchor>
- Derivation/ROADMAP.md#<anchor>
Dependency-Notes:
- Reviewed dependencies: <list related canon docs/registries touched or verified unchanged>
- Upstream/downstream links: <anchors/paths to impacted sections>
Approval/PR:
- PR: <url or owner/number>
- Approval: <reference to approve_tag.py record or admin note>

Guidance:

- All Derivation/ changes MUST add a Change Attestation entry in this file.
- For canon-impacting changes (proposals/experiments/code/results), you MUST also:
  - Update at least one canonical ALL-CAPS doc (e.g., EQUATIONS, VALIDATION_METRICS, ROADMAP, etc.).
  - Include the exact line "Dependency-Chain-Reviewed: true" in the attestation above.
- For non-canon housekeeping (e.g., minor corrections, file shuffles), an attestation entry is still required; canon updates may not be needed if scope is strictly non-canonical.

---

Date (UTC): 2025-08-20

Scope: Tier-0 correctness fixes (numerics, stability narrative) and unification to a single canonical model class (reaction-diffusion, RD). EFT/KG material retained as an active, KPI-gated branch with explicit acceptance criteria and provenance. Unapproved runs remain quarantined by IO policy.

---

## 2025-10-09 - Addendum (Provenance-Preserving Updates)

This section appends new corrections and policy clarifications without modifying prior entries. All earlier “before → after” notes remain untouched for historical fidelity.

### Policy Clarifications

- EFT/KG is an active branch with explicit KPIs and acceptance gates; only unapproved runs are quarantined by IO policy. Any “quarantined” label previously attached to EFT/KG in narrative files should be understood as referring to unapproved execution, not the research branch itself.
- The tachyonic tube RESULTS adopt the physically admissible spectrum coverage $\mathrm{cov}_{\mathrm{phys}}$ as the primary KPI (gate $\ge 0.95$). The raw coverage $\mathrm{cov}_{\mathrm{raw}}$ is reported for transparency only.

### Canonical Mappings and Normalizations

- Discrete → continuum diffusion mapping is reaffirmed as $D = J a^{2}$ (site Laplacian) or $D = (J/z) a^{2}$ (neighbor-average form). The damping parameter $\gamma$ does not appear in the definition of $D$.
- Kinetic normalization from the discrete action remains $c^{2} = 2 J a^{2}$ (per-site) or $c^{2} = \kappa a^{2}$ with $\kappa=2J$ (per-edge).

### KPIs, Schemas, and Registries

- Validation metrics: `VALIDATION_METRICS.md` updated previously to include tube KPIs (kpi-tube-cov-phys primary; kpi-tube-cov-raw transparency; condensation gates).
- Output schemas added for auditable summaries:
  - `code/physics/tachyonic_condensation/schemas/tube-spectrum-summary-v1.schema.json`
  - `code/physics/tachyonic_condensation/schemas/tube-condensation-summary-v1.schema.json`
- `SCHEMAS.md` extended with sections for the above.
- `METRICS.md` remains deprecated as a metrics source; `VALIDATION_METRICS.md` is canonical.

### RESULTS and Overview

- Tube RESULTS v1 documented with explicit gates and artifact paths; provenance is pinned in the RESULTS file. Canon registries (`EQUATIONS.md`, `ALGORITHMS.md`, `CANON_PROGRESS.md`) reflect PROVEN status.
- `OVERVIEW.md` aligned to the canonical diffusion mapping and kinetic normalization; phrasing updated to present EFT/KG as an active, KPI-gated branch.

Provenance Note: The above reflect repository state as of 2025-10-09; earlier entries below remain as originally logged to preserve history.

## Summary (before → after)

- [Derivation/VDM_Overview.md](VDM_Overview.md)
  - Before: Mixed RD/EFT claims; no explicit canonical model.
  - After: Canonical RD banner + mapping (D = J a² or (J/z) a²; r = α - β; u = α), stability note, EFT scoped to future work.

- [Derivation/code/computational_proofs/FUM_theory_and_results.md](code/computational_proofs/FUM_theory_and_results.md)
  - Before: Fixed numerical claim “m_eff ≈ 0.387”.
  - After: m_eff = √(α-β) (parameter‑dependent), added RD model‑class note; removed fixed numeric.

- [Derivation/discrete_to_continuum.md](discrete_to_continuum.md)
  - Before: Objective stated convergence to KG; D mapping not explicit.
  - After: Objective states RD mapping as primary; explicit D mapping (D = J a² or (J/z) a²); EFT derivation referenced to EFT docs as an active, KPI-gated branch.

- [Derivation/memory_steering.md](memory_steering.md)
  - Before: Hardwired EFT vacuum/mass invariants in main text.
  - After: RD is canonical; EFT invariants referenced only to EFT doc; removed back‑solving (α,β) from (v,m_eff) in RD narrative.

- [Derivation/symmetry_analysis.md](symmetry_analysis.md)
  - Before: Text implied “false/true vacuum” using EFT values in a general context.
  - After: Clarified RD vs EFT contexts; RD fixed point W* = r/u (r>0) vs EFT vacuum v = 1 - β/α as future‑work.

- [Derivation/effective_field_theory_approach.md](effective_field_theory_approach.md)
  - Before: No scope banner.
  - After: Policy banner updated; note m_eff = √(α-β) is parameter‑dependent and unitized via τ; EFT is active with KPI gates.

- [Derivation/code/computational_proofs/void_dynamics_theory.md](code/computational_proofs/void_dynamics_theory.md)
  - Before: No scope note; mixed RD/EFT implications.
  - After: Scope note at top; references discrete‑action derivation for c² = 2 J a².

- [Derivation/support/references/Suggestions.md](support/references/Suggestions.md)
  - Before: Implied fixed m_eff; mixed normalization constraint Ja² = 1/2.
  - After: Header note: RD canonical; EFT mass parameter‑dependent; lattice normalization c² = 2 J a² (per‑site); do not impose Ja² = 1/2.

- [Derivation/fum_voxtrium_mapping.md](fum_voxtrium_mapping.md)
  - Before: Referred to EFT EOM as dimensionless default.
  - After: RD mapping made canonical; EFT equation kept for EFT context only.

- New: [METRICS.md](Prometheus_VDM/METRICS.md)
  - Metrics skeleton for RD dynamics, SIE/TDA system metrics, reproducibility pointers.

## Numeric Corrections

- m_eff is not a universal constant; it is m_eff = √(α-β).
  - Example calibrations:
    - α = 0.25, β = 0.10 → m_eff ≈ 0.387
    - α = 1.0,  β = 0.40 → m_eff ≈ 0.7746

All fixed-number statements were replaced with parameter‑dependent forms and example mappings.

## Stability Narrative Corrections

- For RD (canonical): φ = 0 is dynamically unstable for r > 0; homogeneous fixed point φ* = r/u is stable.
- EFT “tachyonic” language retained only in EFT sections; where used, potential boundedness via λ φ⁴ is explicit.

## Kinetic/Lattice Normalization

- Adopted discrete‑action derivation already present in [Derivation/kinetic_term_derivation.md](kinetic_term_derivation.md) with c² = 2 J a² (per‑site convention) or c² = κ a² (per‑edge, κ = 2J). No microscopic constraint ties J to a; c can be set by units.

## Edit Log (file, change)

- [Derivation/VDM_Overview.md](VDM_Overview.md): Replace overview with RD canonical banner; corrected mapping (r = α - β, u = α); EFT scoped.
- [Derivation/code/computational_proofs/FUM_theory_and_results.md](code/computational_proofs/FUM_theory_and_results.md): Insert RD note; replace fixed m_eff numeric with param‑dependent form.  
- [Derivation/discrete_to_continuum.md](discrete_to_continuum.md): Update objective to RD; add D mapping text; keep EFT derivation as future work.  
- [Derivation/memory_steering.md](memory_steering.md): Align with RD canonical; restrict EFT formulas to EFT doc; remove back‑solve in RD section.  
- [Derivation/symmetry_analysis.md](symmetry_analysis.md): Clarify RD vs EFT contexts in interpretations.  
- [Derivation/effective_field_theory_approach.md](effective_field_theory_approach.md): Add policy banner (active, KPI‑gated); retain IO quarantine for unapproved runs.  
- [Derivation/code/computational_proofs/void_dynamics_theory.md](code/computational_proofs/void_dynamics_theory.md): Add scope note at top.  
- [Derivation/support/references/Suggestions.md](support/references/Suggestions.md): Insert header note; prevent hard constraints on Ja².  
- [Derivation/fum_voxtrium_mapping.md](fum_voxtrium_mapping.md): Make RD canonical; EFT references scoped.  
- [METRICS.md](Prometheus_VDM/METRICS.md): New file with metrics skeleton.
- [Derivation/rd_front_speed_validation.md](rd_front_speed_validation.md:1): Add reproducible CLI, output routing, acceptance criteria, representative PASS metrics.
- [Derivation/code/physics/rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1): Set defaults (N=1024, cfl=0.2, level=0.1, x0=-60, fit 0.6-0.9); route outputs to Derivation/code/outputs/{figures,logs}; robust tracking and fit.
- New: [Derivation/code/physics/rd_front_speed_sweep.py](code/physics/rd_front_speed_sweep.py:1): Sweep runner producing CSV summary under Derivation/code/outputs/logs/.
- New: [Derivation/code/physics/rd_dispersion_experiment.py](code/physics/rd_dispersion_experiment.py:1): Linear dispersion validation script with periodic BC; logs/figure auto-routing; acceptance criteria.

## Status Tags

- [ERROR FIXED]: Incorrect fixed mass number claims replaced with parameter‑dependent expression.
- [PROVEN]: Lattice → continuum kinetic normalization via discrete action (already present) is internally consistent.
- [PROVEN]: RD front speed c_front = 2√(Dr) validated. Defaults: N=1024, cfl=0.2, level=0.1, x0=-60, fit window 0.6-0.9. Representative run: c_meas≈0.953, c_th=1.0, rel_err≈0.047, R²≈0.999996.
- [PROVEN]: RD dispersion σ(k) = r - D k² validated via linearized periodic evolution. Defaults (N=1024, L=200, D=1.0, r=0.25, T=10, cfl=0.2, seed=42, m_max=64) → med_rel_err≈0.00145, R²_array≈0.99995 [PASS]; grid refinement (N=2048, m_max=128) → med_rel_err≈0.00130, R²_array≈0.9928 [PASS].

## Change Log — Equations (2025-11-05T02:53:05Z, 393ed61)

- VDM-E-121 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-122 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-123 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-124 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-128 • a48f2d2 • Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md added
- VDM-E-129 • a48f2d2 • Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md added
- VDM-E-095 • 393ed61 • [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md:14) added
- VDM-E-098 • 393ed61 • [Derivation/SYMBOLS.md](Derivation/SYMBOLS.md:215-216) added
- VDM-E-099 • 393ed61 • [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:168-170) added
- VDM-E-100 • 393ed61 • [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:145-148) added
- VDM-E-101 • 393ed61 • [Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md:26) added
- VDM-E-102 • 393ed61 • [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:140-148) added
- VDM-E-103 • 393ed61 • [Derivation/Agency_Field/Agency_Field.md](Derivation/Agency_Field/Agency_Field.md:259-263) added
- VDM-E-048 • 393ed61 • [Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md](Derivation/Thermodynamic_Routing/Wave_Flux_Meter/RESULTS_Wave_Flux_Meter_A_Phase_v1.md:33-35) additional location noted
- VDM-E-105 • cbc3dd1 • Derivation/Transport/Telegraph_From_Relaxation/T1_PROPOSAL_Telegraph_From_Relaxation_v1.md added
- VDM-E-115 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-116 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-117 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-118 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-119 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-120 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added

## Change Log - Proposals (2025-11-05 a48f2d2)

- 2025-11-05 • proposals index updated • comprehensive extraction with tier, research questions, setup, diagnostics, gates, methods, personnel, references

## Symbols (2025-11-05 a48f2d2, cbc3dd1)

- 2025-11-05 • added A8 and RB-Gate symbol rows; telegraph speed symbols • sources

## Change Log — Constants (2025-11-05 b745e83)

- Updated header and metadata in [`CONSTANTS.md`](Derivation/CONSTANTS.md) to maintenance template (date/commit fields).
- Added RB-Gate spec defaults extracted verbatim from [`T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md`](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:199-211 • a48f2d2):
  g=9.81, alpha=2.0e-4, nu=1.0e-6, kappa=1.4e-7, H=[0.01,0.02], Lx_over_H=8.0, DeltaT=[1.0,2.0], BC=[rigid,free], Pr=[0.1,1.0,7.0], Nx=512, Nz=128, epsilon_noise=1e-6, t_warmup=50.0, t_avg=50.0, dt_max=1e-3.
- Added RB-Gate critical values from Appendix A in [`T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md`](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:304-308 • a48f2d2):
  Ra_c(rigid)=1707.76, k_c(rigid)=3.117, λ_c/H(rigid)≈2.015; Ra_c(free)=657.5, k_c(free)=2.221, λ_c/H(free)≈2.828; depth scaling H→2H ⇒ Ra×8 and λ_c≈×2.
- Added RB-Gate stationarity requirement (≤5% drift) from [`T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md`](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:251-252 • a48f2d2).
- Added RB-Gate margin factors for S/C gates from [`T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md`](Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md:262-265 • a48f2d2):
  Ra_subcritical_factor=0.95; Ra_supercritical_factor=1.10.
- Registered QFUM validation constants from [`qfum_validate.py`](Derivation/code/physics/conservation_law/qfum_validate.py:289-293 • b745e83):
  drift_gate (RK4)=1e-8; drift_gate (Euler)=1e-5; conv_r2_min=0.98; order_tol=0.4; expected_order (RK4=4, Euler=1).
- Paths changed:
  - [`CONSTANTS.md`](Derivation/CONSTANTS.md)
- Dependency-Chain-Reviewed: true

## Change Log

- VDM-E-105 • cbc3dd1 • Derivation/Transport/Telegraph_From_Relaxation/T1_PROPOSAL_Telegraph_From_Relaxation_v1.md added
- VDM-E-115 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-116 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-117 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-118 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-119 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-125 • HEAD • Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md added
- VDM-E-126 • HEAD • Derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py added
- VDM-E-127 • HEAD • Derivation/Conservation_Law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md added
- VDM-E-120 • a48f2d2 • Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md added
- VDM-E-121 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-122 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-123 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added
- VDM-E-124 • a48f2d2 • Derivation/Thermodynamics/Convection/T2_PROPOSAL_Rayleigh-Benard_Onset_Gate_for_Deep-M_v1.md added

## Change Log (Units 2025-11-05)

- 2025-11-05 • updated units/maps • 60c5156
- 2024-10-03 • Initial compilation from repository sources • ec0833a

## Change Log (Schemas 2025-11-05)

- 2025-10-04 • schemas compiled from repository source • 6b63a5e
- 2025-10-13 • added KG energy-oscillation summary schema (metriplectic) • 66eb296
- 2025-11-05 • added metriplectic echo config/artifacts/prereg schemas • HEAD

## Change Log (Validation Metrics 2025-11-05)

- 2025-10-03 • Initial compilation from repository code and tests • 17a0b72
- 2025-10-04 • Add tachyonic tube KPIs: cov_phys, cov_raw, residual, curvature_ok and finite_fraction

- 2025-11-05 • updated equations compilation (VDM-E-121–VDM-E-129) • HEAD

---

## Change Attestation — 2025-11-06 (Complete Formalisms Reorganization + Documentation Overhaul)

Date (UTC): 2025-11-06

Dependency-Chain-Reviewed: true
Change-Type: file-shuffle + canon-impacting
Summary: Reorganized Complete Formalisms to CF# naming convention; consolidated duplicate directories; rewrote VDM_OVERVIEW and HYPOTHESES to canonical DOC-GUARD format; added T8-A8 axiom documentation and new hypotheses (H001, H002).

Paths-Changed:

**File Reorganization (S# → CF# renaming):**

- Derivation/Complete-Formalisms/CF1_QGT_to_Metriplectic_Brackets.md (renamed from S1)
- Derivation/Complete-Formalisms/CF2_Contact_to_Metriplectic_Evolution.md (renamed from S2)
- Derivation/Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md (renamed from S3)
- Derivation/Complete-Formalisms/CF4_Telegraph_Fisher_Causality.md (renamed from S4)
- Derivation/Complete-Formalisms/CF5_Integrability_Closure.md (renamed from S5)
- Derivation/Complete-Formalisms/CF6_Info_Geom_Fisher_Ruppeiner_Foundations.md (renamed from Info_Geom)
- Derivation/Complete-Formalisms/CF7_Measurement_Theory_Decoherence_Born_Rule.md (renamed from Measurement)
- Derivation/Complete-Formalisms/COMPLETION_SUMMARY.md (major simplification)

**Directory Consolidation:**

- Removed duplicate files from Derivation/Completed-Formalisms/ (typo variant directory)
- Deleted: Derivation/Completed-Formalisms/S1_QGT_to_Metriplectic_Brackets.md
- Deleted: Derivation/Completed-Formalisms/S2_Contact_to_Metriplectic_Evolution.md
- Deleted: Derivation/Completed-Formalisms/S3_A8_Scaling_Hierarchical_Interfaces.md
- Deleted: Derivation/Completed-Formalisms/S4_Telegraph_Fisher_Causality.md
- Deleted: Derivation/Completed-Formalisms/S5_Integrability_Closure.md
- Deleted: Derivation/Completed-Formalisms/S1-S5_VDM_Formalism_v1.md

**Canon Documentation Updates:**

- Derivation/VDM_OVERVIEW.md (complete rewrite to DOC-GUARD format; added canonical model banner with equation anchors)
- Derivation/HYPOTHESES.md (complete rewrite; added global gates G-J/M, G-Echo, G-H-theorem, G-Locality, G-Artifacts; added H001 entry)
- Derivation/TIER_STANDARDS.md (minor text correction at line 45)
- Derivation/Templates/HYPOTHESIS_TEMPLATE.md (formatting update: angle brackets → curly braces in predictions template)
- Derivation/Unification/T0_Unification_Program_Spec_v1.md (modifications)

**New Axiom Documentation:**

- Derivation/Axioms/T8-A8_Gaps.md (research paper analysis for A8 validation)
- Derivation/Axioms/T8-A8_Gates.md (gate specifications for A8)
- Derivation/Axioms/T8-A8_Milestones.md (milestone tracking for A8)

**New Hypotheses:**

- Derivation/Memory_Steering/Born_Meter/H002_Memory_Steering_as_a_Born_Meter.md
- Derivation/Quantum/Quantum_Gradient_Descent/H001_Quantum-Driven_Gradient_Descent.md

**New References:**

- Derivation/References/Dynamical-Systems/2412.00589v2.pdf

**Maintenance:**

- maintenance-prompts/overview_maintenance.md (new maintenance prompt file)

**Deletions:**

- Derivation/DIMENSIONLESS_CONSTANTS.md (removed; content likely migrated to CONSTANTS.md)

Canon-Docs-Updated:

- Derivation/VDM_OVERVIEW.md (full rewrite)
  - Added canonical model banner with equations: E-015 (RD PDE), E-016 (RD reaction), E-017 (RD stability), E-018 (RD front)
  - Added DOC-GUARD: REFERENCE header
  - Added provenance anchors to SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS canon files
  - Scoped EFT/KG and Metriplectic branches with equation anchors
  - Added RB-Gate and causality meter references
- Derivation/HYPOTHESES.md (full rewrite)
  - Added hypothesis status legend and tier progression (H → CF → T0-T9)
  - Added global gates applicable to all hypotheses
  - Added H001 (Quantum-Driven Gradient Descent) formal entry
  - Established hypothesis registry format with classification, owner, status, objectives
- Derivation/TIER_STANDARDS.md#L45 (minor correction)
- Derivation/Templates/HYPOTHESIS_TEMPLATE.md (template formatting update)

Dependency-Notes:

- Reviewed dependencies:
  - EQUATIONS.md: All equation anchors (E-015, E-016, E-017, E-018, E-042, E-091, E-105, E-121-124, E-125) referenced in VDM_OVERVIEW are verified as existing canonical entries
  - VALIDATION_METRICS.md: Referenced for global gates definition in HYPOTHESES.md
  - CONSTANTS.md: DIMENSIONLESS_CONSTANTS.md removal assumes content previously migrated (2025-08-20 per CHRONICLES)
  - TIER_STANDARDS.md: Referenced by hypothesis tier progression in HYPOTHESES.md
  - HYPOTHESIS_TEMPLATE.md: Template used for H001 and H002 new hypothesis files
- Upstream/downstream links:
  - Complete-Formalisms CF1-CF7 naming now referenced by COMPLETION_SUMMARY.md
  - HYPOTHESES.md global gates will apply to all future hypothesis files
  - VDM_OVERVIEW.md canonical model banner establishes RD as primary branch; all future proposals should reference this banner
  - T8-A8 axiom files support the Lietz Infinity Conjecture (T8_A8_PROPOSAL per CHRONICLES line 173-178)

Rationale:

1. **Naming consistency:** S# notation was ambiguous; CF# (Complete Formalism) makes purpose explicit and aligns with repository tier standards
2. **Directory consolidation:** Removed duplicate "Completed-Formalisms" vs "Complete-Formalisms" directories caused by naming inconsistency
3. **Documentation standardization:** VDM_OVERVIEW and HYPOTHESES rewritten to DOC-GUARD format with explicit provenance anchors, making all claims traceable to canonical sources
4. **Hypothesis formalization:** Established hypothesis registry (HYPOTHESES.md) and added first two entries (H001, H002) following template
5. **A8 axiom support:** Added T8-A8 support files (Gaps, Gates, Milestones) for ongoing Lietz Infinity Conjecture work

Approval/PR:

- PR: pending
- Approval: awaiting commit and review on nexus branch

Provenance Note: Changes prepared 2025-11-06; awaiting final review before commit.

- 2025-10-04 • conventions extracted from repository • 8e27c34

## Change Attestation — 2025-11-08 (GB Meter Canon Anchors, KPIs, Algorithms, Proposal)

Dependency-Chain-Reviewed: true  
Change-Type: canon-impacting  
Summary: Registered GB meter canon anchors (VDM-E-160..164), added validation KPIs/gates, extended ALGORITHMS with VDM-A-047..050, and created T2 proposal file for GB oscillating-load instrument. No equations duplicated; all math referenced by anchors.

Paths-Changed:

- [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md)
- [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
- [Derivation/ALGORITHMS.md](Derivation/ALGORITHMS.md)
- [Derivation/Nonequilibrium/T2_PROPOSAL_GB_Oscillating_Load_v1.md](Derivation/Nonequilibrium/T2_PROPOSAL_GB_Oscillating_Load_v1.md)

Canon-Docs-Updated:

- Equations registry anchors added:
  - [VDM-E-160](Derivation/EQUATIONS.md#vdm-e-160) — GB excess energy γ² law (anchor only)
  - [VDM-E-161](Derivation/EQUATIONS.md#vdm-e-161) — Asymmetric emission threshold p0⋆ (anchor only)
  - [VDM-E-162](Derivation/EQUATIONS.md#vdm-e-162) — Cycle-Lyapunov monotonicity for E_ex (anchor only)
  - [VDM-E-163](Derivation/EQUATIONS.md#vdm-e-163) — Moiré-contrast observable (anchor only)
  - [VDM-E-164](Derivation/EQUATIONS.md#vdm-e-164) — Dimensionless groups for GB scaling collapse (anchor only)
- Validation metrics (KPIs/gates) added:
  - [kpi-gb-gamma2-law](Derivation/VALIDATION_METRICS.md#kpi-gb-gamma2-law)
  - [kpi-gb-asym-threshold](Derivation/VALIDATION_METRICS.md#kpi-gb-asym-threshold)
  - [kpi-gb-lyapunov-cycle](Derivation/VALIDATION_METRICS.md#kpi-gb-lyapunov-cycle)
  - [kpi-gb-protocol-insensitivity](Derivation/VALIDATION_METRICS.md#kpi-gb-protocol-insensitivity)
  - [kpi-gb-dimless-collapse](Derivation/VALIDATION_METRICS.md#kpi-gb-dimless-collapse)
- Algorithms (pseudocode flows) added:
  - [VDM-A-047](Derivation/ALGORITHMS.md#vdm-a-047) — GB Relaxation Meter
  - [VDM-A-048](Derivation/ALGORITHMS.md#vdm-a-048) — Moiré Contrast Index
  - [VDM-A-049](Derivation/ALGORITHMS.md#vdm-a-049) — Emission Detector
  - [VDM-A-050](Derivation/ALGORITHMS.md#vdm-a-050) — Dimensionless Collapse

Dependency-Notes:

- Instrument helpers referenced (single responsibility; IO via io_paths):
  - [python.GBExcessEnergyGamma2Fitter()](Derivation/code/common/instrument_helpers/boundaries/gb_energy_gamma2_fitter.py:1)
  - [python.GBEmissionThresholdEstimator()](Derivation/code/common/instrument_helpers/boundaries/gb_emission_threshold.py:1)
  - [python.GBLyapunovCycleMonitor()](Derivation/code/common/instrument_helpers/boundaries/gb_cycle_lyapunov.py:1)
  - [python.GBMoireContrast()](Derivation/code/common/instrument_helpers/boundaries/gb_moire_contrast.py:1)
- IO routing: [Derivation/code/common/io_paths.py](Derivation/code/common/io_paths.py)
- Constants placeholders to preregister for gates:
  - TODO: add [CONSTANTS.md#const-gb-gamma2-A_ref](Derivation/CONSTANTS.md) (slope baseline per material/geometry)
  - TODO: add [CONSTANTS.md#const-gb-asym-threshold-ref](Derivation/CONSTANTS.md) (p0_ref per geometry/material)
  - TODO: add [CONSTANTS.md#const-gb-lyapunov-drop10](Derivation/CONSTANTS.md) (drop_10 threshold)
  - TODO: add [CONSTANTS.md#const-gb-protocol-insensitivity-thr](Derivation/CONSTANTS.md)
  - TODO: add [CONSTANTS.md#const-gb-collapse-envelope](Derivation/CONSTANTS.md) if overriding A6 default

Approval/PR:

- PR: pending
- Approval: pending (per [Derivation/code/ARCHITECTURE.md](Derivation/code/ARCHITECTURE.md))

Provenance:

- Proposal created: [Derivation/Nonequilibrium/T2_PROPOSAL_GB_Oscillating_Load_v1.md](Derivation/Nonequilibrium/T2_PROPOSAL_GB_Oscillating_Load_v1.md) (anchors only; no equations duplicated)

## Change Attestation — 2025-11-08 (DeGrand–DeTar Sampling Exactness, UQ, Scale-Program, Solver Practice)

Dependency-Chain-Reviewed: true  
Change-Type: canon-impacting  
Summary: Documentation anchors and cross-links for lattice-QCD-inspired meters and KPIs were consolidated from DeGrand &amp; DeTar into VDM canon without duplicating equations or constants. This attests the mapping and landing of: HMC/RHMC exactness gates, ΔH diagnostics, integrated autocorrelation and τ-aware binning, correlated χ² with SVD truncation, blocked jackknife/bootstrap, RG blocking and scaling collapse, and large-sparse solver practice (CG/BiCGStab, even–odd, multishift) as patterns.

Paths-Changed:

- docs/misc-standards/standard-upgrades/DeGrand-DeTar_Upgrade_Map.md
- Derivation/EQUATIONS.md#vdm-e-130
- Derivation/EQUATIONS.md#vdm-e-131
- Derivation/EQUATIONS.md#vdm-e-132
- Derivation/EQUATIONS.md#vdm-e-133
- Derivation/EQUATIONS.md#vdm-e-134
- Derivation/EQUATIONS.md#vdm-e-135
- Derivation/EQUATIONS.md#vdm-e-136
- Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize
- Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist
- Derivation/VALIDATION_METRICS.md#kpi-tau-int
- Derivation/VALIDATION_METRICS.md#kpi-binning-adequacy
- Derivation/VALIDATION_METRICS.md#kpi-correlated-chi2-svd
- Derivation/VALIDATION_METRICS.md#kpi-resample-ci-stability
- Derivation/VALIDATION_METRICS.md#kpi-rg-collapse
- Derivation/ALGORITHMS.md#vdm-a-030
- Derivation/ALGORITHMS.md#vdm-a-031
- Derivation/ALGORITHMS.md#vdm-a-032
- Derivation/ALGORITHMS.md#vdm-a-033
- Derivation/ALGORITHMS.md#vdm-a-034
- Derivation/ALGORITHMS.md#vdm-a-035
- Derivation/ALGORITHMS.md#vdm-a-036
- Derivation/Templates/RESULTS_PAPER_STANDARDS.md:140

Canon-Docs-Updated:

- HMC/RHMC acceptance and ΔH anchors: [VDM-E-130](Derivation/EQUATIONS.md:1914), [VDM-E-131](Derivation/EQUATIONS.md:1938)  
- Chain UQ anchors: [VDM-E-132](Derivation/EQUATIONS.md:1957), [VDM-E-133](Derivation/EQUATIONS.md:1981)  
- Correlated χ² + SVD: [VDM-E-134](Derivation/EQUATIONS.md:2006)  
- Blocked resampling: [VDM-E-135](Derivation/EQUATIONS.md:2034)  
- RG blocking/collapse: [VDM-E-136](Derivation/EQUATIONS.md:2055)  
- KPIs: HMC acceptance/ΔH, τ_int, τ-aware binning, correlated χ² SVD, resample CI stability, RG collapse (see VALIDATION_METRICS anchors above)  
- Algorithms/pseudocode: HMC, RHMC, CG/BiCGStab, even–odd, multishift, RG utility (see ALGORITHMS anchors above)  
- RESULTS standards: Chain sampling diagnostics section updated to require ΔH histograms, acceptance-vs-ε fits, τ_int reporting, τ-aware binning, correlated-fit cutoff sweep (see [Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md:140](Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md:140))

Dependency-Notes:

- Axiom cross-links: A4 notes reference HMC acceptance and ΔH KPIs ([Derivation/AXIOMS.md:73](Derivation/AXIOMS.md:73)); A6 references RG collapse KPI ([Derivation/AXIOMS.md:97](Derivation/AXIOMS.md:97)).  
- No equations or numeric constants duplicated; book-derived rationale is recorded in navigator file ([docs/misc-standards/DeGrand-DeTar_Upgrade_Map.md](docs/misc-standards/DeGrand-DeTar_Upgrade_Map.md)).  
- Future work: optional KPI set for solver adapters (residual norms, condition-estimate logs) may be proposed separately.

Provenance:

- Source: [Lattice Methods for Quantum Chromodynamics — DeGrand &amp; DeTar](Derivation/References/Lattice-Field-Theory_&amp;_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf)  
- Navigator: [docs/misc-standards/standard-upgrades/DeGrand-DeTar_Upgrade_Map.md](docs/misc-standards/standard-upgrades/DeGrand-DeTar_Upgrade_Map.md)

Approval/PR:

- PR: pending
- Approval: pending

## Change Log - 2025-10 - Roadmap

- 2025-10-04 • Initial roadmap compiled from repository evidence • 77f055f
- 2025-10-06 • Added milestones: FRW Continuity Residual (Gravity), Dark Photon Portal program, Quantum Gravity Bridge; backfilled Proposals Index (A6 Collapse, FRW Balance, Metriplectic variants, RD Conservation, Dark Photons)
- 2025-10-13 • Added milestone entry for KG J-only QC certification and note under Metriplectic proposals; updated header stamp

## 2025-11-15 — Ringdown Meter cleanup (pronoun normalization, instrument consolidation, gates)

Changes applied to ringdown-meter proposals to enforce third-person style, consolidate instruments, and pin acceptance gates.

- Pronoun normalization (second-person → third-person):
  - [T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md)
  - [T2_PROPOSAL_Ringdown_Meter_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md)
  - Removed duplicate after normalization: [T2_PROPOSAL_VDM_Ringdown_Meter_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_VDM_Ringdown_Meter_v1.md) (file deleted; see consolidation below)

- Instrument consolidation (per feedback):
  - Baseline meter retained: [T2_PROPOSAL_Ringdown_Meter_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md)
  - DSI meter retained as separate T2: [T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md)
  - Duplicate naming proposal removed to avoid split provenance: [T2_PROPOSAL_VDM_Ringdown_Meter_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_VDM_Ringdown_Meter_v1.md) (deleted). The APPROVALS example in baseline now points to the canonical baseline proposal path.

- Acceptance gates added:
  - Baseline Ringdown/QNM Fit (new section “5.1.2 Operational acceptance gates (baseline)”):
    - G1 Residual whiteness (FDR-controlled)
    - G2 Fit stability (±10% window; ≤5% parameter drift)
    - G3 Meter reproducibility (commit+seeds)
    - Location: [T2_PROPOSAL_Ringdown_Meter_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md)
  - DSI on residuals (new section “4.1 Operational acceptance gates (DSI residuals)”):
    - D1 Peak detection (SNR≥5, q≤0.05)
    - D2 t0 robustness (≤5%)
    - D3 Window robustness (≤5%)
    - D4 Null controls (Kerr-only/shuffled residuals within 95% band)
    - D5 Cross-detector consistency (joint 95% CI)
    - Location: [T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md](Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Discrete_Scale_Invariance_Ringdown_v1.md)

Rationale:
- Maintain a single canonical baseline instrument and a logically distinct DSI follow-on; avoid split provenance.
- Keep gates explicit with CSV/JSON/PNG artifacts and commit/seed provenance per RESULTS standards.

Provenance:
- Timestamp (UTC): 2025-11-15
- Commit: pinned at run time in proposal front-matter

## Change Attestation — 2025-11-19 (VDM Validation Phase Preregistration Lock)

Date (UTC): 2025-11-19

Dependency-Chain-Reviewed: true  
Change-Type: canon-impacting  
Summary: Lock the preregistered VDM Validation Phase by bringing six proposals to template-complete prereg status (Gap Modules + instruments) and updating canonical indices (PROPOSALS, ROADMAP) to treat them as a linked validation cluster.

Paths-Changed:

- Derivation/Axioms/A8_Hierarchy_Gates/T3_PROPOSAL_A8_Hierarchy_Gates_v1.md
- Derivation/Metriplectic/Metriplectic_Instruments/T2_PROPOSAL_Metriplectic_Instruments_v1.md
- Derivation/Metriplectic/Analog_Horizon/T5_PROPOSAL_Analog_Horizon_v1.md
- Derivation/Gravity/Gravity_Regression/T5_PROPOSAL_Gravity_Regression_v1.md
- Derivation/Spinor/T1_PROPOSAL_Spinor_Emergence_v1.md
- Derivation/Cosmology/CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md
- Derivation/z.CANONICAL_Proposals/00_PROPOSALS.md
- Derivation/z.CANONICAL_Roadmap/00_ROADMAP.md

Canon-Docs-Updated:

- Derivation/z.CANONICAL_Proposals/00_PROPOSALS.md
- Derivation/z.CANONICAL_Roadmap/00_ROADMAP.md

Dependency-Notes:

- Reviewed `z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md`, `z.CANONICAL_Schemas/00_SCHEMAS.md`, and domain code under `Derivation/code/physics/{meters,causality,cosmology}` for compatibility with the prereg manifests referenced in §5.1.1 of each proposal.
- Established cross-links from the Roadmap milestone `#ms-vdm-validation-phase` to the six prereg proposals and from `00_PROPOSALS.md` to the “VDM Validation Phase — Preregistration Lock” cluster note.
- Confirmed that each of the six proposals carries explicit PRE-REGISTRATION examples, APPPROVAL/SCHEMA/SPEC paths, and artifact standards consistent with `Templates/PROPOSAL_PAPER_TEMPLATE.md` and `Templates/RESULTS_PAPER_STANDARDS.md`.

Approval/PR:

- PR: (to be filled with GitHub URL or change request reference on publication)
- Approval: (to be recorded via `code/common/authorization/approve_tag.py` when prereg tags are stamped and domain APPROVAL.json manifests are updated)

---

## 2025-11-20 - Nielsen-Ninomiya Defense for Spinor Emergence

Dependency-Chain-Reviewed: true
Change-Type: canon-impacting
Summary: Added H005 hypothesis, CF8 complete formalism, and updated T1_PROPOSAL_Spinor_Emergence to defend against Nielsen-Ninomiya No-Go Theorem using domain-wall fermions, Ginsparg-Wilson operator, and Bravyi-Kitaev fermionization.

Paths-Changed:

- Derivation/Spinor/H005_HYPOTHESIS_Spinor_Emergence_Nielsen_Ninomiya_Defense.md (new)
- Derivation/Complete-Formalisms/CF8_Spinor_Emergence_Domain_Wall_Fermions.md (new)
- Derivation/Spinor/T1_PROPOSAL_Spinor_Emergence_v1.md (updated with Nielsen-Ninomiya defense section)
- Derivation/z.CANONICAL_Hypotheses/00_HYPOTHESES.md (added H005 entry)
- Derivation/z.CANONICAL_Complete_Formalisms/00_COMPLETE_FORMALISMS.md (added CF8 entry)

Canon-Docs-Updated:

- Derivation/z.CANONICAL_Hypotheses/00_HYPOTHESES.md#h005
- Derivation/z.CANONICAL_Complete_Formalisms/00_COMPLETE_FORMALISMS.md (added CF8)

Dependency-Notes:

- Reviewed [AXIOMS.md](../AXIOMS.md) (VDM-AX-004, A2, A3, A4) for J-limb scalar lattice foundation
- Reviewed [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md) for metriplectic structure equations
- Reviewed [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) for gate definitions
- CF8 provides full derivation from first principles: domain-wall kink profile, bound-state zero modes, Ginsparg-Wilson operator construction, Bravyi-Kitaev locality proof, and Lorentz invariance via RG flow
- H005 defines 5 decisive predictions (P1-P5) with quantitative pass/fail gates addressing the three Red Team attack vectors:
  1. P1: Ginsparg-Wilson relation verification (exact chiral symmetry)
  2. P2: Residual mass exponential suppression (finite-size effects)
  3. P3: Linear Dirac dispersion (emergent relativistic fermions)
  4. P4: Lorentz isotropy at low energy (rotational symmetry restoration)
  5. P5: Bravyi-Kitaev locality scaling (causality preservation in 3D)
- T1_PROPOSAL updated to reference H005 and CF8, demonstrating that VDM produces **Ginsparg-Wilson operators** (not naive Wilson fermions), evading Nielsen-Ninomiya via topology

Approval/PR:

- PR: copilot/evaluate-ninomiya-theorem
- Approval: (pending T1 experiment execution and gate validation)
