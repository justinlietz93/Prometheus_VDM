# Resolution Conjecture Milestones - Void Dynamics Model

**Generated on:** November 3, 2025 at 12:22 AM CST

---

* **Milestone ID:** EBN-A8-Def
* **Objective:** Establish single-source, repository-canonical definitions of E_exc, α, α_I, β_E, N(L), tubular neighborhoods, and diameter/gap conditions, with unit tests on analytic shapes and synthetic segmentations.
* **Due Date:** 11-03-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** BN-1.1..1.5 basic implementations
* **Notes:**
  * **Relation:** Extends existing A8 proposal (Derivation/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md) and VALIDATION_METRICS.md; uses spectral gradients, RESULTS harness.
  * **Axioms:** A0, A4, A5, A6, A7
  * **Deliverables:** [detectors.py](Derivation/code/physics/hierarchy/detectors.py), [depth_tracker.py](Derivation/code/physics/hierarchy/depth_tracker.py), [tubular_energy.py](Derivation/code/physics/hierarchy/tubular_energy.py), [info_proxy.py](Derivation/code/physics/hierarchy/info_proxy.py), [area_law.py](Derivation/code/physics/hierarchy/area_law.py); prereg [A8_validation.v1.yml](Derivation/experiments/prereg/A8_validation.v1.yml)
  * **Estimated Effort:** 1–2 weeks

* **Milestone ID:** EBN-A8-Bridge-AI-Physics
* **Objective:** Define a read-only ETL comparator from `fum_rt` boundary artifacts (e.g., stable boundary sets, `cut_strength` EWMAs, churn, B1 cycle hits) to physics-bench tubular integrals and hierarchy depth N(L) after bench-native meters exist; not a dependency for A8 validation PASS.
* **Due Date:** 11-04-2025
* **Owner:** Justin K. Lietz
* **Status:** In progress
* **Dependencies:** Bench-native A8 meters present; runtime snapshots optional via read-only ETL.
* **Notes:**
  * **Relation:** Read-only ETL; no coupling of runtime to physics bench; avoids detector duplication.
  * **Evidence:** runtime boundary observer present; bench-side ETL comparator spec drafted; delivery pending bench-native meters
  * **Axioms:** A2 (locality), A7
  * **Estimated Effort:** 1 week

* **Milestone ID:** EBN-A8-UQ
* **Objective:** Add bootstrap CIs and power analysis for α, α_I, β_E, N(L) slopes; preregister ε-tube and segmentation parameter ladders; publish sensitivity envelopes; add grid-invariance gate (slope drift ≤ 0.05 with CI overlap) and anisotropy/morphometry controls; include FDR control for multiple gates and dual model selection ΔAIC/ΔBIC between area-law and volume-law.
* **Due Date:** 11-05-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** RESULTS infra
* **Notes:**
  * **Relation:** Extends existing RESULTS discipline.
  * **Stop/go:** If grid-invariance fails, auto-spawn deconvolution and Minkowski-morphometry tasks before reruns.
  * **Axioms:** A7
  * **Estimated Effort:** 1 week

* **Milestone ID:** EBN-A8-Replicate
* **Objective:** Replicate A8 metrics across distinct integrators (where applicable) and CPU/GPU + precisions; record drift bounds as prereg gates.
* **Due Date:** 11-06-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** CI jobs; existing tests.
* **Notes:**
  * **Relation:** Formalizes cross-code replication gate (G7-like).
  * **Axioms:** A7; supports A2 by locality invariance checks
  * **Estimated Effort:** 2–4 weeks

* **Milestone ID:** EBN-Energy-Cal
* **Objective:** Harmonize discrete energy density and tubular procedure; validate against analytic perimeters/areas; eliminate definition drift.
* **Due Date:** 11-07-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** EBN-A8-Def
* **Notes:**
  * **Relation:** Supports BN-1.3/1.5; backs G2/G3 confidence.
  * **Axioms:** A7
  * **Estimated Effort:** 1 week

* **Milestone ID:** EBN-TF-IMEX
* **Objective:** Implement Telegraph-Fisher dynamics with IMEX or Strang-partitioned J⊕M; verify ⟨J,δΣ⟩=0, ⟨M,δI⟩=0 per step (bounds logged/gated).
* **Due Date:** 11-08-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** KG J-only runner; RD DG M-step; structure checks
* **Notes:**
  * **Relation:** Extends BN-2.1 using metriplectic structure checks already validated.
  * **Deliverables:** [telegraph_fisher.py](Derivation/code/physics/causality/telegraph_fisher.py), [cone_slack.py](Derivation/code/physics/causality/cone_slack.py), [kappa_collapse.py](Derivation/code/physics/causality/kappa_collapse.py); prereg [telegraph_fisher_cone.v1.yml](Derivation/experiments/prereg/telegraph_fisher_cone.v1.yml)
  * **Axioms:** A4, A5, A7
  * **Estimated Effort:** 2–3 weeks

* **Milestone ID:** EBN-TF-Stability
* **Objective:** Document Δt–Δx–τ stability envelopes; dispersion error charting; provide admissible ladders to avoid cone artifacts.
* **Due Date:** 11-09-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** EBN-TF-IMEX
* **Notes:**
  * **Relation:** Precondition BN-2.2 cone testing.
  * **Axioms:** A7
  * **Estimated Effort:** 1 week

* **Milestone ID:** EBN-TF-Calibration
* **Objective:** Calibrate τ by matching TF c=√(D/τ) to J-limb c_J from KG dispersion/locality; define a reproducible κ=rτ sweep.
* **Due Date:** 11-10-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** KG dispersion/locality RESULTS
* **Notes:**
  * **Relation:** Tightens BN-2.3; ties to proven KG diagnostics.
  * **Axioms:** A6, A7, A4
  * **Estimated Effort:** 1 week

* **Milestone ID:** EBN-Cones-Arrival
* **Objective:** Replace naïve thresholds with matched-filter or hysteresis front-tracking; reduce noise sensitivity in cone slack.
* **Due Date:** 11-11-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** BN-2.2
* **Notes:**
  * **Relation:** Supports BN-2.2.
  * **Axioms:** A7
  * **Estimated Effort:** 3–5 days

* **Milestone ID:** EBN-Cosmo-TDA
* **Objective:** Add Betti curves/persistence and DisPerSE-like skeletonization; classify codimensions; compute N and boundary fingerprints robustly.
* **Due Date:** 11-12-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** BN-3.1/3.3 prototypes
* **Notes:**
  * **Relation:** Extends BN-3.1/3.3; maps directly to A8 predictions.
  * **Axioms:** A7; A6 via nondimensionalization
  * **Estimated Effort:** 3–4 weeks

* **Milestone ID:** EBN-Cosmo-Obs
* **Objective:** Incorporate survey masks, completeness, fiber collisions, and Redshift-Space Distortions (RSD) (Kaiser + FoG) into P(k), ξ(r), void statistics, and boundary metrics; publish corrections and uncertainties.
* **Due Date:** 11-13-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** BN-3.3
* **Notes:**
  * **Relation:** Makes BN-3.3 publication-grade.
  * **Axioms:** A7
  * **Estimated Effort:** 3 weeks

* **Milestone ID:** EBN-Units
* **Objective:** Map (λ, r, D, τ) to comoving units/redshift using FRW baseline; document re-scaling recipes for VDT↔cosmology.
* **Due Date:** 11-14-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** FRW QC results
* **Notes:**
  * **Relation:** Supports BN-3.1..3.3 and CT-5/6 links.
  * **Axioms:** A6, A7
  * **Estimated Effort:** 1 week

* **Milestone ID:** EBN-CMB-ISW+Lens
* **Objective:** Include Integrated Sachs-Wolfe (ISW)/Rees–Sciama (RS) and lensing with priors; produce ΔT and θ distributions; compare to Planck with Bayes factors; define falsification windows.
* **Due Date:** 11-15-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** EBN-Units
* **Notes:**
  * **Relation:** Extends BN-3.2.
  * **Axioms:** A7
  * **Estimated Effort:** 3–4 weeks

* **Milestone ID:** BN-4.1
* **Objective:** Operationalize "Measurement = Boundary Formation" with a metriplectic-consistent information functional and falsifiable gates that tie M-production to information registration under a controlled protocol (e.g., T4 CEG Assisted-Echo).
* **Due Date:** 11-16-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** A8 info/energy metrics; RESULTS harness; EBN-Info-Functional; T4 proposal
* **Notes:**
  * **Relation:** This is a "sharpened" version of the existing BN-4.1. The details are fleshed out by EBN-Info-Functional and EBN-T4-ΔΣΔI-Gates.
  * **Axioms:** A4, A5, A6, A7
  * **Estimated Effort:** Requires 3–4 weeks research + 1–2 weeks implementation for the EBNs that make it actionable.

* **Milestone ID:** EBN-Info-Functional
* **Objective:** Define I_info[φ] aligned with Σ/I and A4 degeneracy; candidate implementations: spectral-entropy changes per M-step with calibration to Σ; calibrated log(1+|∇φ|²/σ²) tied to Σ/I; mutual information across partition bands (coarse-grained).
* **Due Date:** 11-17-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** A8 info/energy metrics; RESULTS harness
* **Notes:**
  * **Relation:** Extends BN-1.4 and BN-4.1; leverages ΔΣ logging and spectral diagnostics used in RESULTS.
  * **Axioms:** A4, A5, A6, A7
  * **Estimated Effort:** 3–4 weeks research + 1–2 weeks implementation

* **Milestone ID:** EBN-T4-ΔΣΔI-Gates
* **Objective:** In the T4 CEG protocol, preregister gates: corr(ΔΣ, ΔI_info) ≥ threshold (with refinement stability), echo-quality sensitivity under M vs J-only, and boundary-proximal info capture (α_I in ε-tubes) during controlled "measurement" windows.
* **Due Date:** 11-18-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** EBN-Info-Functional; T4 proposal (Derivation/Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md)
* **Notes:**
  * **Relation:** Makes CT-7 falsifiable with your existing T4 plan.
  * **Axioms:** A5, A7
  * **Estimated Effort:** 1–2 weeks

* **Milestone ID:** BN-4.2
* **Objective:** Operationalize "Horizon as Hierarchical Boundary" with a precise path: weak-field Einstein–Skyrme post-processing from T5, and a near-term analogue-horizon experiment in the Wave Flux Meter.
* **Due Date:** 11-19-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** T5 RESULTS; units mapping; two independent solvers for replication; EBN-Info-Functional; Wave Flux Meter RESULTS (A/B phases)
* **Notes:**
  * **Relation:** This is a "sharpened" version of the existing BN-4.2, directly anchored to T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md. The details are fleshed out by EBN-GR-Weak, EBN-Analog-Horizon, and EBN-GR-Covariant-Notes.
  * **Axioms:** A0–A2, A4, A5, A6, A7

* **Milestone ID:** EBN-GR-Weak
* **Objective:** Consume T5 ε(x) and f(x) to form Tμν[U] (hedgehog), solve weak-field Poisson/linearized GR for Φ(r) under spherical symmetry; compute v_circ(r), Σ_lens(R), and validate with tight replication gates.
* **Due Date:** 11-20-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** T5 RESULTS; units mapping; two independent solvers for replication
* **Notes:**
  * **Relation:** Directly extends your T5 proposal; leverages FRW QC, Gravity_Regression/ namespace, and UNITS_NORMALIZATION.md.
  * **Axioms:** A0–A2, A6, A7 (A4 unaffected—post-processing T5 outputs)
  * **Estimated Effort:** 4–6 weeks

* **Milestone ID:** EBN-Analog-Horizon
* **Objective:** Extend your Wave Flux Meter geometry to create an effective horizon; measure α/α_I scaling with horizon boundary measure and ΔΣ–ΔI correlation under controlled M injections; enforce energy/flux conservation gates.
* **Due Date:** 11-21-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** Info functional (EBN-Info-Functional), wave meter conservation gates
* **Notes:**
  * **Relation:** Provides BH-information on-ramp consistent with A2/A4/A5/A7; no GR commitment required to test boundary encoding.
  * **Axioms:** A2, A4, A5, A7
  * **Estimated Effort:** 4–8 weeks

* **Milestone ID:** EBN-GR-Covariant-Notes
* **Objective:** Draft "Covariant Metriplectic Notes"—∂→∇, metric-compatibility of M, degeneracy in curved space, ∇μTμν=0 checks, and a spherical Einstein–Skyrme outline for future phases.
* **Due Date:** 11-22-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** GR-Weak results; literature cross-checks
* **Notes:**
  * **Relation:** Lays the math groundwork without overcommitting; connects to Quantum_Gravity/ notes.
  * **Axioms:** A0–A2, A4, A7
  * **Estimated Effort:** 4–8 weeks (documentation with toy checks)

* **Milestone ID:** EBN-SM-Effective
* **Objective:** Map SM gauge actions (SU(3)×SU(2)×U(1)) to transformations of Ψ that yield emergent Noether charges/currents in the J-limb; identify internal indices/fiber structure in Ψ consistent with A0 and A3; document necessary constraints.
* **Due Date:** 11-23-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** SYMBOLS.md/EQUATIONS.md to fix notation; Noether machinery in KG tests
* **Notes:**
  * **Relation:** Theoretical feasibility note; no claims of full dynamics yet.
  * **Axioms:** A0, A3, A6
  * **Estimated Effort:** 6–10 weeks (theory study)

* **Milestone ID:** EBN-RG-Bridge
* **Objective:** Connect lattice-scale VDT parameters to continuum EFT couplings via scaling/renormalization logic; identify dimensionless invariants that survive coarse-graining (A6).
* **Due Date:** 11-24-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** UNITS_NORMALIZATION.md; Collapse domain results
* **Notes:**
  * **Relation:** Supports EBN-SM-Effective and cosmology unit re-embedding.
  * **Axioms:** A6, A7
  * **Estimated Effort:** 4–8 weeks (notes + small experiments)

* **Milestone ID:** EBN-SM-Phenomenology
* **Objective:** Define operational probes for emergent quasi-particles/collective modes in VDT that could correspond to SM-like sectors (e.g., dispersion patterns, conserved charges).
* **Due Date:** 11-25-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** KG J-only instruments; metriplectic coupling QC
* **Notes:**
  * **Relation:** Sets measurable stepping stones before full SM mechanics.
  * **Axioms:** A7
  * **Estimated Effort:** 4–6 weeks

* **Milestone ID:** EBN-BranchCriteria
* **Objective:** Define discriminants (e.g., inertia-to-diffusion ratios, local κ=rτ) and a decision flow in the runners; preregister thresholds for when to apply RD vs KG vs TF regularized branches.
* **Due Date:** 11-26-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** TF calibration (EBN-TF-Calibration); KG and RD diagnostics; TF calibration.
* **Notes:**
  * **Relation:** Addresses OQ-002: Quantitative criteria for EFT branch necessity.
  * **Axioms:** A2, A6, A7
  * **Estimated Effort:** 1–2 weeks

* **Milestone ID:** EBN-Action-Continuum
* **Objective:** Recast the discrete model into a variational action; derive ∂t² terms and c² normalization from lattice couplings; provide EFT mapping and kinetic‑term derivation; commit QA artifacts and document assumptions.
* **Due Date:** 11-27-2025
* **Owner:** Justin K. Lietz
* **Status:** Completed
* **Completed:** 2025-11-03
* **Dependencies:** Delivered (EFT derivation + kinetic term derivation + RD QA + bench‑native code); see evidence below
* **Notes:**
  * **Relation:** Addresses OQ-014: Recast discrete model into discrete action.
  * **Axioms:** A0, A4, A7
  * **Evidence (EFT derivations, RD QA, bench‑native code):**
    * [effective_field_theory_approach.md](Axiom-8/Status/Derivation/Effective_Field_Theory/effective_field_theory_approach.md)
    * [kinetic_term_derivation.md](Axiom-8/Status/Derivation/Effective_Field_Theory/kinetic_term_derivation.md)
    * [fum_voxtrium_mapping.md](Axiom-8/Status/Derivation/Effective_Field_Theory/fum_voxtrium_mapping.md)
    * [logarithmic_constant_of_motion.md](Axiom-8/Status/Derivation/Draft-Papers/RD_Methods_QA/logarithmic_constant_of_motion.md)
    * [rd_methods_QA.md](Axiom-8/Status/Derivation/Draft-Papers/RD_Methods_QA/rd_methods_QA.md)
    * [census_clocks.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/census_clocks.py)
    * [discrete_gradient.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/discrete_gradient.py)
    * [flux_core.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/flux_core.py)
    * [rd_dispersion_experiment.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py)
    * [rd_front_speed_experiment.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py)
    * [rd_front_speed_sweep.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/rd_front_speed_sweep.py)
    * [reaction_exact.py](Axiom-8/Status/Derivation/code/physics/reaction_diffusion/reaction_exact.py)
    * [run_rd_conservation.py](Axiom-8/Status/Derivation/code/physics/rd_conservation/run_rd_conservation.py)
    * [qfum_validate.py](Axiom-8/Status/Derivation/code/physics/conservation_law/qfum_validate.py)
    * [condense_tube.py](Axiom-8/Status/Derivation/code/physics/tachyonic_condensation/condense_tube.py)
    * [cylinder_modes.py](Axiom-8/Status/Derivation/code/physics/tachyonic_condensation/cylinder_modes.py)
    * [run_tachyon_tube.py](Axiom-8/Status/Derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py)

* **Milestone ID:** EBN-c2-Norm
* **Objective:** Extract c² from lattice couplings and spacing; validate against KG dispersion across grids.
* **Due Date:** 11-28-2025
* **Owner:** Justin K. Lietz
* **Status:** In progress
* **Dependencies:** EBN-Action-Continuum (Completed); KG dispersion results; EQUATIONS.md
* **Notes:**
  * **Relation:** Addresses OQ-015: Kinetic normalization c² = 2J a² from discrete action.
  * **Axioms:** A6, A7
  * **Evidence to date:**
    * Kinetic term derivation: [kinetic_term_derivation.md](Axiom-8/Status/Derivation/Effective_Field_Theory/kinetic_term_derivation.md)
    * EFT approach/mapping: [effective_field_theory_approach.md](Axiom-8/Status/Derivation/Effective_Field_Theory/effective_field_theory_approach.md), [fum_voxtrium_mapping.md](Axiom-8/Status/Derivation/Effective_Field_Theory/fum_voxtrium_mapping.md)
    * KG J-only dispersion/locality RESULTS: [RESULTS_KG_Jonly_Locality_and_Dispersion.md](Axiom-8/Status/Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md)
  * **Next action to close:** add explicit multi-grid c² validation table (slope/intercept across N ladders with CI), then mark Completed.
  * **Estimated Effort:** 1–2 weeks

* **Milestone ID:** EBN-Lattice-Scale
* **Objective:** Calibrate lattice 'a' via astrophysical anchors (Skyrme T5 R*; cosmological characteristic scales); provide prior ranges and uncertainty.
* **Due Date:** 11-29-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** T5 RESULTS; FRW; unit re-embedding (EBN-Units).
* **Notes:**
  * **Relation:** Addresses OQ-027: Lattice scale parameter (20 orders uncertainty).
  * **Axioms:** A6, A7
  * **Estimated Effort:** 2–3 weeks

* **Milestone ID:** EBN-PreReg
* **Objective:** Implement machine-readable prereg YAML for A8, TF, T4, T5, GR weak-field, analogue horizons; locked before first runs; embedded SHA and salted provenance.
* **Due Date:** 11-30-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** RESULTS/PROPOSAL templates; PROVENANCE_manifest.json
* **Notes:**
  * **Relation:** Programmatic enhancement for rigor.
  * **Axioms:** A7
  * **Estimated Effort:** 3–5 days

* **Milestone ID:** EBN-Repro
* **Objective:** Add CI jobs to run A8/TF smoke tests on multiple hardware/OS stacks; quantify drift; require PASS invariance to platform within CIs.
* **Due Date:** 12-01-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** Existing CI/test harness; conftest.py
* **Notes:**
  * **Relation:** Programmatic enhancement for rigor.
  * **Axioms:** A7
  * **Estimated Effort:** 3–5 days

* **Milestone ID:** EBN-HPC-3D
* **Objective:** Profile hotspots; implement FFT-based spectral ops and GPU acceleration where suitable; memory tiling for tubular neighborhood operations; plan target grid sizes and wallclock budgets for statistical power for A8/TF/cosmology experiments.
* **Due Date:** 12-02-2025
* **Owner:** Justin K. Lietz
* **Status:** Not started
* **Dependencies:** Stabilized A8/TF core; Derivation/code/, tools/; prior RESULTS performance
* **Notes:**

## Repository derivations survey — status corrections (2025-11-03)

Upstream instruments/results — Completed (evidence)

* KG J-only locality & dispersion: [RESULTS_KG_Jonly_Locality_and_Dispersion.md](Axiom-8/Status/Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md)
* RD dispersion validation (linear regime): [rd_dispersion_validation.md](Axiom-8/Status/Derivation/Reaction_Diffusion/rd_dispersion_validation.md)
* RD Fisher–KPP front speed (logs, PASS): [rd_front_speed_experiment_20250823T194825Z.json](Axiom-8/Status/Derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250823T194825Z.json)
* FRW continuity QC (dust): [RESULTS_FRW_Continuity_Residual_Quality_Check.md](Axiom-8/Status/Derivation/Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md)
* Tachyonic tube spectrum: [RESULTS_Tachyonic_Tube_v1.md](Axiom-8/Status/Derivation/Tachyon_Condensation/RESULTS_Tachyonic_Tube_v1.md)
* Tachyonic tube PROPOSAL: [PROPOSAL_Tachyonic_Tube_Condensation.md](Axiom-8/Status/Derivation/Tachyon_Condensation/PROPOSAL_Tachyonic_Tube_Condensation.md)
* Finite‑tube mode analysis: [finite_tube_mode_analysis.md](Axiom-8/Status/Derivation/Tachyon_Condensation/finite_tube_mode_analysis.md)
* A6 scaling collapse: [RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md](Axiom-8/Status/Derivation/Collapse/RESULTS_A6_Scaling_Collapse_Junction_Logistic_Universality.md)
* EFT derivations (upstream for kinetic normalization and mapping):
  * [kinetic_term_derivation.md](Axiom-8/Status/Derivation/Effective_Field_Theory/kinetic_term_derivation.md)
  * [effective_field_theory_approach.md](Axiom-8/Status/Derivation/Effective_Field_Theory/effective_field_theory_approach.md)
  * [fum_voxtrium_mapping.md](Axiom-8/Status/Derivation/Effective_Field_Theory/fum_voxtrium_mapping.md)

P0 items still missing for A8/TF benches (not found under Derivation/)

* Telegraph–Fisher implementation and meters:
  * Stepper for τ·φ_tt + φ_t = D∇²φ + f(φ)
  * Cone‑slack meter (arrival-time slack)
  * κ‑collapse validator with κ = r·τ
* A8 hierarchy bench‑native meters:
  * Hierarchical boundary detector (Γ_ℓ)
  * Log‑depth tracker N(L)
  * Tubular‑energy α(ε)
  * Information proxy α_I(ε) with σ sweeps and proxy concordance
  * Area‑law fits (β_E) with ΔAIC/ΔBIC vs volume‑law and grid‑invariance checks

Milestone corrections (consistency with evidence)

* EBN‑Action‑Continuum: Completed (evidence listed above; see also bench‑native RD/KG instruments).
* EBN‑A8‑Bridge‑AI‑Physics: In progress (runtime boundary observer exists; bench‑side ETL comparator pending).
* EBN‑TF‑IMEX / EBN‑TF‑Stability / EBN‑TF‑Calibration: Not started (no TF stepper/meters present); dependent on KG/RD (completed).
* EBN‑A8‑Def / EBN‑A8‑UQ / EBN‑A8‑Replicate / EBN‑Energy‑Cal: Not started (no A8 hierarchy meters present).
* Baseline dependencies satisfied for A8/TF run‑up: KG J‑only, RD dispersion/front, FRW QC, A6 collapse, tachyonic tube results, and EFT/kinetic derivations — all completed and artifacted as above.

Cone & hygiene clauses (reiterated for scheduling)

* Finite‑speed cone claims must be produced on KG (J‑only) or TF benches; RD‑only runs support front‑speed/dispersion gates, not cones.
* A5 sign convention unified across milestones and deliverables: enforce ΔΣ ≥ −tol and, where a Lyapunov F is used, ΔF ≤ +tol; log degeneracy certificates g1,g2 ≤ 1e−10 with refinement tightening in all benches.
  * **Relation:** Programmatic enhancement for scale.
  * **Axioms:** A7
  * **Estimated Effort:** 3–6 weeks

## Key Highlights

* Establishing single-source, repository-canonical definitions for core physics parameters (E_exc, α, α_I, β_E, N(L)) is a foundational step, supported by unit tests on analytic shapes and synthetic segmentations.
* A critical objective is to define a translation layer that bridges AI `fum_rt` boundary artifacts to physics-side tubular integrals and hierarchy depth, effectively wiring AI detectors to A8 meters.
* Ensuring scientific rigor involves adding bootstrap confidence intervals and power analysis for key parameters, and replicating metrics across distinct integrators, CPU/GPU, and precisions to record drift bounds.
* A major conceptual goal is to operationalize "Measurement = Boundary Formation" by defining a metriplectic-consistent information functional and establishing falsifiable gates within a controlled experimental protocol.
* The project aims to operationalize "Horizon as Hierarchical Boundary" through weak-field General Relativity calculations and the creation of an effective horizon in analogue-horizon experiments.
* Connecting the model to real-world observables includes incorporating survey masks, Redshift-Space Distortions, and other observational effects into cosmological metrics, alongside mapping parameters to comoving units.
* For theoretical consistency, the discrete model will be recast into a variational action, with `∂t²` terms and `c²` normalization derived from lattice couplings and validated against KG dispersion.
* To enhance rigor and transparency, machine-readable preregistration YAML will be implemented for key experiments, and CI jobs will be added to ensure cross-platform reproducibility within quantified drift bounds.

## Next Steps & Suggestions

* Prioritize and assign owners to foundational definition milestones like EBN-A8-Def and EBN-Info-Functional, as they are critical dependencies for numerous subsequent tasks.
* Conduct a detailed dependency analysis across all 'Not started' milestones to establish a clear critical path and sequencing plan, ensuring efficient resource allocation.
* Initiate early-stage reproducibility and preregistration efforts (EBN-PreReg, EBN-Repro) to embed scientific rigor and provide immediate, low-effort wins.
* Concurrently begin planning for computational scaling (EBN-HPC-3D) given the expected complexity of 3D experiments for A8/TF/cosmology, to avoid performance bottlenecks later.
* Develop a strategy and assign ownership for integrating real-time boundary artifacts from `fum_rt` into the physics-side tubular integrals (EBN-A8-Bridge-AI-Physics) for early empirical validation.
