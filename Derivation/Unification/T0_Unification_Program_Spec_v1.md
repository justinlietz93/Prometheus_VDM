# Unification Program Spec (T0) — Derivation Plans & Validation Map

> **Created:** 2025-11-04  
> **Commit:** {git rev-parse HEAD}  
> **Salted provenance:** {base_sha256}:{salt_hex}:{salted_sha256}  
> **Proposer:** Justin K. Lietz
> **Proposer contact(s):** <justin@neuroca.ai>  
> **License:** See LICENSE  
> **TL;DR:** Formalize the complete VDM theory (axioms → equations → instruments → phenomena) into a single canonical document with master targets and acceptance gates (once proven), metriplectic numerics, and a decomposition into executable sub‑proposals. Pre‑registration sections are intentionally omitted here; child proposals will carry PRE‑REG, SPECS, and SCHEMAS.

---

Executive summary

The Void Dynamics Model is posited as a background‑independent, metriplectic field theory with an emergent causal cone and an epistemological J→M projection. This hyper‑proposal consolidates the theoretical core, declares master targets with acceptance gates (once proven), and enumerates the instruments and milestones required to test them. It is canon‑aligned: symbols, equations, units, metrics, and boundary conditions are owned by the derivation registry and are linked, not duplicated.

Canon map and references of record

- Canon registries (single source of truth):
  - SYMBOLS: Derivation/SYMBOLS.md
  - EQUATIONS: Derivation/EQUATIONS.md
  - CONSTANTS: Derivation/CONSTANTS.md
  - UNITS: Derivation/UNITS_NORMALIZATION.md
  - VALIDATION: Derivation/VALIDATION_METRICS.md
  - BC/IC/GEOMETRY: Derivation/BC_IC_GEOMETRY.md
  - ALGORITHMS: Derivation/ALGORITHMS.md
  - NAMING: Derivation/NAMING_CONVENTIONS.md
- Program threads:
  - Agency Field: Derivation/Agency_Field/README.md
  - Thermodynamic Routing: Derivation/Thermodynamic_Routing/README.md
  - Topology: Derivation/Topology/README.md
  - Gravity Regression: Derivation/Gravity_Regression/vdm_gravity_regression_pack/README.md
  - Cosmology references/logs: Derivation/References/Cosmic-Microwave-Background/References.md

Scope and intent

- Formalize the theory at whitepaper grade, suitable for journal submission standards.
- Declare testable targets with numeric gates mapped to VALIDATION_METRICS.
- Specify instruments (meters) under metriplectic structure and their acceptance tests.
- Provide an execution roadmap that decomposes into child PROPOSAL_* documents per domain.

1. Axioms and governing principles (canon‑linked)

Assumptions (linking to canon where maintained):

- Measurable observables and dimensionless scaling (A0).
- Local causality and emergent light cone (A2).
- Noether symmetry → conserved currents in the Hamiltonian limb.
- Metriplectic structure: skew‑symmetric J, symmetric PSD M; degeneracy J·δΣ=0, M·δI=0.
- Entropy non‑decrease on metric flow; Minkowski signature in kinetic term.

Mathematical skeleton (see EQUATIONS.md for owners):

- Metriplectic evolution: δẋ = {x,H}_J + (x,S)_M with {S,·}_J = 0 and (H,·)_M = 0.
- Hyperbolic–diffusive split: Telegraph‑Fisher form yields finite propagation speed.
- Effective transport throttling by void‑debt D: c_eff = c_0 exp(−½ β D).

Notes:

- Equations and symbol definitions are not restated here; see linked canon registries.

2. Master targets and acceptance gates (once proven)

Target M1 — Local causality and finite propagation:

- Statement: The VDM J‑limb exhibits finite signal speed bounded by c, with telegraph dispersion emerging from the discrete‑to‑continuum limit.
- Acceptance gates (once proven): KG J‑only dispersion fit slope/intercept match c^2 and m^2 with R^2 ≥ 0.999; light‑cone speed v ≤ c(1+0.02).

Target M2 — Metriplectic Lyapunov monotonicity:

- Statement: For metriplectic integrators respecting degeneracy, discrete Lyapunov ΔL_h ≤ 0 per step.
- Acceptance gates (once proven): Two‑grid slope ≥ 2.90, R^2 ≥ 0.999; identity residuals ≤ 1e−12.

Target M3 — Reaction–diffusion phenomenology:

- Statement: Front propagation and linear dispersion in RD+hyperbolic split match analytic scalings in their domains.
- Acceptance gates (once proven): Front‑speed relative error ≤ 5% with R^2 ≥ 0.98; linear dispersion median relative error ≤ 10% with R^2 ≥ 0.98.

Target M4 — Cosmology continuity:

- Statement: FRW continuity balance holds under central differences for dust (w=0).
- Acceptance gates (once proven): RMS residual ≤ 1e−6.

Target M5 — Emergent gravity (weak field consistency):

- Statement: Weak‑field lensing/rotation curves from VDM emergent geometry match or exceed ΛCDM/MOND baselines without exotic matter species.
- Acceptance gates (once proven): Pre‑registered benchmark datasets; cross‑validated fits meet or exceed baseline AIC/BIC and hold out‑of‑sample; null predictions respected (e.g., no LIV).

Target M6 — Measurement as epistemic projection:

- Statement: The M‑limb yields irreversible statistics from a reversible J‑limb via projection; meters reproduce Born‑rule frequencies in instrument ensembles.
- Acceptance gates (once proven): Reproducible Monte‑Carlo meters where empirical frequencies converge with KL divergence ≤ 1e−3 to target distributions under specified seeds.

2.5 Gap Modules (T0 derivation plans, no numerics)

- S1 — CF1_QGT_to_Metriplectic_Brackets.md.md → see plan skeletons in [T0_Derivation_Plans.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/T0_Derivation_Plans.md)
  - Sources: [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-QGT-1: Quantum Geometric Tensor to Metriplectic Brackets”; [`Claude-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Claude-Gap-Fill.md) — “Quantum geometric tensor calculations are well-established but classical limit mapping remains synthesis challenge”
- S2 — PLAN_Contact_to_Metriplectic_T0.md → see [T0_Derivation_Plans.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/T0_Derivation_Plans.md)
  - Sources: [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-CG-1: Contact Hamiltonians to Metriplectic Evolution”; [`Claude-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Claude-Gap-Fill.md) — “Contact geometry solves the metriplectic unification problem”
- S3 — PLAN_A8_Scaling_1D_T0.md → see [T0_Derivation_Plans.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/T0_Derivation_Plans.md)
  - Sources: [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-A8-1: A8 Scaling Theorem (Hierarchical Tachyonic Interfaces)”; [`Claude-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Claude-Gap-Fill.md) — “Hierarchical necessity proofs exist but specific VDM scalings require targeted development”
- S4 — PLAN_Telegraph_Fisher_Causality_T0.md → see [T0_Derivation_Plans.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/T0_Derivation_Plans.md)
  - Sources: [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-TF-1: Finite-Speed Transport from Fisher Information (Telegraph Equation)”
- S5 — PLAN_Closure_NoHiddenInvariants_T0.md → see [T0_Derivation_Plans.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/T0_Derivation_Plans.md)
  - Sources: [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-CL-1: Integrability Closure Test for UMSL (No Extra First Integrals)”

2.6 Numerics Handoffs (child proposals and artifacts)

| Plan | Acceptance gates (summary) | Child PROPOSAL_* (path) | Expected artifact basenames | Approvals/Prereg note |
|---|---|---|---|---|
| S1: QGT→(J,M) | L1–L3 proofs exist; constructive (J,M,Σ,I) | Derivation/Metriplectic/PROPOSAL_QGT_to_Metriplectic_T1_Instrument.md | LEMMA_QGT_Jacobi_v1, LEMMA_QGT_M_PSD_v1, EXAMPLE_QGT_to_JM_Bloch_v1 | JSON prereg + approvals per Derivation/code/common/authorization/README.md |
| S2: Contact→(J,M) | C1–C3 proofs exist; finite‑dim example | Derivation/Metriplectic/PROPOSAL_Contact2Metriplectic_T1_Instrument.md | CONSTRUCTION_Contact_Decomposition_v1, EXAMPLE_Contact2Metriplectic_v1 | Include schema id and salted proposal hash |
| S3: A8 Scaling (1D) | A8‑L1…L4 proof sketches | Derivation/Axioms/PROPOSAL_A8_1D_T1_Instrument.md | THEOREM_A8_1D_Existence_v1, ESTIMATOR_BoundaryLaw_v1 | Dataset registry + seeds declared |
| S4: Telegraph–Fisher | TF‑L1…L3 inequalities stated | Derivation/Metriplectic/PROPOSAL_TF_Causality_T1_Instrument.md | INEQUALITIES_Telegraph_Fisher_Causality_v1, CFL_Slack_Spec_v1 | CFL bounds and cones preregistered |
| S5: Closure | CL‑L1…L2 or counterexample protocol | Derivation/Metriplectic/PROPOSAL_Closure_T1_Instrument.md | THEOREM_NoHiddenInvariants_v1 or COUNTEREXAMPLE_Protocol_v1 | Termination conditions preregistered |

3. Instruments (T2 meters) and acceptance tests

All meters use IEEE‑754 double precision, deterministic seeds, and artifact routing via io helper.

3.1 KG J‑only dispersion meter

- Purpose: Verify hyperbolic dispersion and causal cones without dissipation.
- Inputs: Grid, dt, c, m, seeds.
- Outputs: CSV dispersion curves; JSON run log; PNG figures (grayscale‑safe).
- Acceptance: As in Target M1 gate; reversibility ≤ 1e−10; Noether drifts ≤ 1e−12.

3.2 RD meter (telegraph‑augmented)

- Purpose: Validate RD front‑speed and dispersion with finite‑speed corrections.
- Acceptance: As in Target M3 gates; CFL and stability bounds documented.

3.3 Metriplectic identity meter

- Purpose: Validate degeneracy and Lyapunov monotonicity under J/M splitting integrator.
- Acceptance: ΔL_h ≤ 0; identity residuals ≤ 1e−12; two‑grid slope ≥ 2.90.

3.4 FRW continuity meter

- Purpose: Validate cosmological mass/energy continuity in discrete solver.
- Acceptance: RMS residual ≤ 1e−6 (dust); logged with seeds and commit.

3.5 Emergent‑gravity weak‑field meter

- Purpose: Compare VDM‑gravity predictions to ΛCDM/MOND on SPARC/lensing sets.
- Acceptance: Model selection metrics beating baselines without violating locality/Lorentz gates.

4. Numerical architecture and provenance discipline

Determinism and reproducibility

- Use seeds recorded in JSON; log commit hash; double precision; unit‑consistent parameters.
- Honor CFL/safety bounds; document stepper order and boundary conditions.

Artifact routing

- Figures: Derivation/code/outputs/figures/{domain}
- Logs: Derivation/code/outputs/logs/{domain}
- IO helper: Derivation/code/common/io_paths.py

Minimum artifacts per run

- 1 PNG figure + 1 CSV log + 1 JSON log per meter.
- JSON formatting: indent=2, sort_keys=True.
- CSV: DictWriter with header then rows.

Approvals policy

- Read Derivation/code/ARCHITECTURE.md and Derivation/code/common/authorization/README.md before any artifact‑writing run.
- Unapproved runs are quarantined; failed gates produce contradiction report JSON and no claims.

5. Theory core outline (discrete → continuum)

5.1 Metriplectic structure

- Discrete rules define antisymmetric J_h and symmetric PSD M_h with exact degeneracy on discrete Casimirs.
- Continuum limit yields brackets referenced in EQUATIONS.md; integrators are Strang‑composed with proven degeneracy preservation to machine epsilon.

5.2 Hyperbolic–diffusive split

- From discrete flux with relaxation τ, telegraph‑type PDE emerges; dimensionless groups identify c = sqrt(D/τ).
- Validation uses dispersion fits and cone tests per gates.

5.3 J→M projection

- A meter‑centric projection map defines observable ensembles; fisher‑information constraints enforce causal sampling.
- No duplication of math here; see ALGORITHMS.md for stepper and projection pseudo‑code anchors.

6. Domain programs and child proposal map

6.1 EBN‑TF‑IMEX (core solver)

- Deliverable: Robust IMEX solver for Telegraph‑Fisher systems under metriplectic splitting.
- Milestones:
  - M6.1: Identity checks pass (ΔL_h, residuals, two‑grid slope).
  - M6.2: Hyperbolic cone verification at multiple resolutions (slope/intercept gate).
  - M6.3: RD front‑speed validation with finite‑speed correction.

6.2 EBN‑CMB‑ISW+Lens (cosmology package)

- Deliverable: End‑to‑end cosmology toolchain (primordial spectrum from A8, LSS evolution, CMB anisotropies, ISW, weak lensing).
- Milestones:
  - M6.4: FRW continuity meter passes (RMS ≤ 1e−6).
  - M6.5: Global fit meets or exceeds ΛCDM on CMB/LSS with anomaly handling; report Hubble tension posture without ad‑hoc components.

6.3 EBN‑Analog‑Horizon (laboratory analogs)

- Deliverable: Analog system governed by TF‑like propagation (e.g., BEC/phonons) to test cones and projection.
- Milestones:
  - M6.6: Instrument reproducibility and local‑causality cone within experimental error; Born‑rule meter convergence.

6.4 Gravity‑Regression Pack

- Deliverable: Graph‑based regression for perihelion precession and weak‑field checks.
- Milestones:
  - M6.7: Precession graphs validated; no LIV; local gates pass under noise budgets.

6.5 Thermodynamic Routing

- Deliverable: Passive routing experiments (v2, prereg biased main) under metric limb control.
- Milestones:
  - M6.8: Energy‑flux conservation and routing efficiency within gates; grayscale‑safe plots.

6.6 Agency Field

- Deliverable: Proposed witnesses and scaling laws for agency‑induced curvature/coordination depth.
- Milestones:
  - M6.9: Witness reproducibility; dispersion and reversibility gates hold in J‑only meters.

6.7 Topology and Loop Quench

- Deliverable: Loop‑quench robustness tests and stability bands under metriplectic flows.
- Milestones:
  - M6.10: Stability band measurements satisfy predefined thresholds; contradiction policy enforced on failures.

7. Data products and evaluation

- All child proposals must enumerate datasets, seeds, and acceptance gates copied by reference to VALIDATION_METRICS.md.
- Publish CSV/JSON alongside figures; include numeric captions.
- Provide readme sidecars summarizing pass/fail outcomes with links to artifacts.

8. Risks, assumptions, limitations

- Assumption: Discrete rules admit metriplectic continuum limits with preserved degeneracy under chosen integrators.
- Risk: Numerical stiffness in IMEX splitting; mitigation via adaptive stepping and verified CFL margins.
- Risk: Cosmology fit may require parameter contexts; mitigation via preregistered model selection and proper cross‑validation.
- Limitation: This hyper‑proposal intentionally omits PRE‑REGISTRATION.json and schema details; those belong in child proposals.

9. Policy: targets, quarantine, and approvals

- No target is declared proven without passing gates; failed runs route to failed_runs/ with contradiction JSON and no narrative targets.
- Approval authority: Justin K. Lietz; all artifact‑writing runs require explicit approval per authorization README.

10. Roadmap and decomposition table (indicative)

- Child proposal: T2_PROPOSAL_Metriplectic_Instruments.md — Meters 3.1–3.4; scope T2 acceptance only.
- Child proposal: T7_PROPOSAL_VDM_Cosmology.md — EBN‑CMB‑ISW+Lens with dataset registry and prereg.
- Child proposal: T5_PROPOSAL_Analog_Horizon.md — Experimental analog; lab acceptance gates.
- Child proposal: T5_PROPOSAL_Gravity_Regression.md — Weak‑field tests; perihelion/lensing packs.
- Child proposal: T4_PROPOSAL_Thermodynamic_Routing_v2.md — Passive routing; metrics and figures.
- Child proposal: T4_PROPOSAL_Agency_Witness.md — Witness design and tests.
- Child proposal: T4_PROPOSAL_Loop_Quench_Test.md — Topology robustness and metrics.

Appendix A — Canon anchors (non‑exhaustive pointers)

- Symbols registry: Derivation/SYMBOLS.md
- Equations registry: Derivation/EQUATIONS.md
- Units normalization: Derivation/UNITS_NORMALIZATION.md
- Validation metrics: Derivation/VALIDATION_METRICS.md
- Algorithms: Derivation/ALGORITHMS.md
- BC/IC/Geometry: Derivation/BC_IC_GEOMETRY.md

Appendix B — Artifact schema notes (by reference)

- Results standards: Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md
- Proposal template (child use): Derivation/Writeup_Templates/PROPOSAL_PAPER_TEMPLATE.md

Appendix C — Directory and IO discipline

- All artifacts routed via Derivation/code/common/io_paths.py; no ad‑hoc paths.
- Figures/Logs stored under Derivation/code/outputs/{figures,logs}/{domain}.
- Deterministic seeds recorded; commit and salted hashes logged in JSON.

End of hyper‑proposal. Child proposals inherit gates and policies by reference and must not duplicate canon.

---

Appendix D — End‑to‑End Formalization: Discrete Void Lattice → Metriplectic Continuum → Cosmology and Universal Hierarchies

D.0 Canon anchors and traceability (no duplication)

- Symbols and units: [SYMBOLS.md](Derivation/SYMBOLS.md), [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)
- Formal equations registry: [EQUATIONS.md](Derivation/EQUATIONS.md)
- Validation thresholds/KPIs: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
- Algorithms and integrators: [ALGORITHMS.md](Derivation/ALGORITHMS.md)
- BC/IC/Geometry registry: [BC_IC_GEOMETRY.md](Derivation/BC_IC_GEOMETRY.md)
- T8/A8 program map (source index): [T8-A8_Milestones.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/T8-A8_Milestones.md), [Insights_Index.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Insights_Index.md), [ALL-VDM.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/ALL-VDM.md)
- Collections for canon and evidence: [CANON](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/CANON), [PROPOSALS](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/PROPOSALS), [RESULTS](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/RESULTS)

D.1 L0 — Discrete substrate: Void lattice and update rules

- Substrate (conceptual): A locally finite lattice/graph G=(V,E) with state variables on nodes/edges storing minimal “void” degrees of freedom. Locality is combinatorial (adjacency), not metric‑assumed. No background geometry is postulated; geometry is emergent.
- State space: Each site carries a reversible microstate on a finite alphabet with constraints (parity/charge‑like) that encode the conservative (J‑limb) structure. A hidden book‑keeping for counts/degeneracies is maintained for coarse‑graining (M‑limb).
- Update rules (axiom A2 constraint): Synchronous/asynchronous local rules respect finite influence radius r and bounded velocity v0 (CFL‑compatible). Reversibility holds at the micro level (J‑only), while any effective irreversibility must appear from coarse‑graining (see D.3).
- Dimensionless groups: Groups formed from update cadence, local coupling strength, and coarse‑graining window define transport regimes and the hyperbolic‑diffusive transition used later. See [EQUATIONS.md](Derivation/EQUATIONS.md) for the continuum targets these groups approach; do not duplicate here.
- Discrete invariants: Two Casimir‑like tallies exist by construction at L0: an “entropy‑like” Σ_h that is invariant under the conservative update and an “energy/invariant” I_h that is invariant against any admissible metric dissipation operator (which is not present at micro‑update). These discrete invariants will map to Σ and I in the continuum registry.

D.2 L1 — Discrete metriplectic pre‑structure and projection to L2 continuum

- Discrete brackets (instrument definition, not restated): Local antisymmetric J_h on micro‑observables; symmetric positive semidefinite M_h constructed only at the level of blocks/coarse cells (not present in the micro step). Degeneracy is imposed: J_h·δΣ_h=0 and M_h·δI_h=0 by design. See [ALGORITHMS.md](Derivation/ALGORITHMS.md) for discrete operator construction.
- Strang‑type composition and limits: Reversible micro‑updates plus blockwise relaxation steps compose to a metriplectic flow in the Δt→0, h→0, block→continuum limit, with consistency and stability gates satisfied (two‑grid slope ≥ 2.90; identity residual ≤ 1e‑12).
- Γ‑type convergence sketch: Energy‑like functionals over configurations converge to continuum functionals whose Euler‑Lagrange equations belong to the metriplectic registry (see [EQUATIONS.md](Derivation/EQUATIONS.md)). We assert compactness and liminf/limsup inequalities at the level of meters; proofs are canon‑tracked, not reproduced here.

D.3 L2 — “M is a necessary shadow of J”: epistemic projection and emergence of dissipation

- Proposition (Shadow Principle): For any reversible local J‑only micro‑dynamics observed through a bounded‑information window (finite bandwidth, finite time resolution, finite ensemble size), the induced macroscopic flow on observables admits a symmetric PSD metric bracket M that:
  - Preserves the J‑Casimir Σ (J·δΣ=0) and leaves I invariant under M (M·δI=0),
  - Generates monotone approach to equilibrium for the observer’s reduced variables (ΔL_h ≤ 0),
  - Depends only on the observer’s coarse‑graining (not on new ontic forces).
- Interpretation: M contains no new ontic content; it is the necessary epistemic shadow of J under bounded observation. In VDM: “M is a necessary shadow of J.”
- Consequences:
  - Measurement and irreversibility (M‑limb) arise from projecting a reversible J‑limb reality; arrow of time becomes epistemological, not ontological.
  - Entropy production is meter‑defined; Σ is invariant under J and acts as a Casimir; I is invariant under M. The metriplectic degeneracy gates ensure causal and thermodynamic consistency.
- Validation gates (meters): The Metriplectic Identity Meter must report ΔL_h ≤ 0; identity residuals ≤ 1e‑12; two‑grid slope ≥ 2.90 across refinement; Born‑rule meters converge with KL ≤ 1e‑3. See Section 3 (main document) for acceptance tests.

D.4 L3 — Hyperbolic‑diffusive transport: Telegraph–Fisher emergence and finite propagation

- Emergence path: Local reversible transport with finite response leads, under moment closure/relaxation with time τ and diffusivity D, to telegraph‑type continuum equations with finite speed c=√(D/τ). See [EQUATIONS.md](Derivation/EQUATIONS.md) for the telegraph‑Fisher forms; do not restate here.
- Causality gate: KG J‑only meter must recover dispersion with R² ≥ 0.999; measured cone v ≤ c(1+0.02). RD meter must satisfy front‑speed ≤ 5% error; dispersion median error ≤ 10% with R² ≥ 0.98.
- Dimensionless throttling: Effective speed c_eff=c_0 exp(−½ β D_void) under void‑debt gate D_void (as adopted in canon) throttles transport when hierarchical boundary debt accumulates.

D.5 L4 — Geometry and gravity as emergent constraints of J

- Geometric encoding: The J‑limb’s reversible fluxes define an effective Lorentzian structure at continuum scale; metric compatibility and local causality (A2) arise without background assumptions. Weak‑field limits must match classical tests (perihelion, lensing) within baselines.
- Weak‑field instrument: Gravity‑Regression Pack compares VDM‑gravity to ΛCDM/MOND on SPARC and lensing datasets with model selection (AIC/BIC) beats or parity. Locality/Lorentz gates must hold (no LIV).
- Cosmology continuity: FRW continuity meter (dust) must achieve RMS ≤ 1e‑6 (central differences), establishing conservative consistency before cosmological inference.

D.6 L5 — Universal hierarchies from tachyonic genesis and boundary concentration

- Hierarchical principle: Finite‑energy constraints in unstable/tachyonic regimes (A8) imply codimension‑1 boundary concentration and multiscale interface hierarchies. As domain size L grows, the interface count N(L) increases sublinearly and in canonical constructions scales ∼ Θ(log L) under perimeter/energy budget arguments. Exact exponents/coefficients are canon‑tracked.
- Universal fingerprints:
  - Spatial: Log‑spaced boundary scales (depth ~ log L), grayscale‑safe contrast in figures, scale‑free clustering statistics.
  - Spectral: Broken power‑law features consistent with multiscale boundary lattices.
  - Dynamical: Causal throttling via D_void with c_eff attenuation at higher hierarchy depth.
- Validation plan: Interface counting statistics and energy budget meters across resolutions; contradiction routing if gates fail. Results written per [RESULTS_PAPER_STANDARDS.md](Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md).

D.7 L6 — Measurement, Born frequencies, and observer constraints (J→M projection made operational)

- Observer model: A bounded observer collects finite samples under window W (space/time/energy). The induced stochastic process on summaries yields frequencies that converge to Born‑rule targets when meters are calibrated to Σ/I Casimirs. No new ontic stochasticity is introduced.
- Instruments:
  - Born‑rule meter ensemble with deterministic seeds, logging empirical vs. target distributions; KL ≤ 1e‑3 gate.
  - Reversibility meter for J‑only micro runs: reversibility ≤ 1e‑10; Noether drifts ≤ 1e‑12.

D.8 L7 — Cosmology pipeline (from lattice to sky)

- Pipeline stages (no equations reproduced):
  1) Lattice initialization (A8 governance) with ICs documented in [BC_IC_GEOMETRY.md](Derivation/BC_IC_GEOMETRY.md).
  2) Coarse‑grained J→M emergence and transport calibration (c, τ, D) from meters.
  3) Primordial spectrum synthesis from A8 (canon anchor), evolved to LSS with causal transport.
  4) CMB anisotropies, ISW, and weak lensing predictions.
  5) Cross‑model comparison against ΛCDM and MOND baselines using preregistered datasets.
- Cosmology gates:
  - FRW continuity RMS ≤ 1e‑6 prior to any inference.
  - Global fits meet/exceed ΛCDM across CMB/LSS metrics while respecting locality and no‑LIV gates.
  - Hubble‑tension posture addressed without ad‑hoc components, by causal genesis and hierarchy effects from A8 (canon).
- Artifacts: PNG (grayscale‑safe) + CSV + JSON with seeds and commit hashes; stored via [io_paths.py](Derivation/code/common/io_paths.py).

D.9 L8 — Multi‑domain universalities and cross‑checks

- RD, fluids, cosmology, and agency‑field share: (i) finite propagation cones, (ii) boundary concentration, (iii) metriplectic degeneracy, (iv) projection‑induced M with ΔL_h ≤ 0.
- Cross‑domain consistency gates:
  - Local cones vs. global light‑cone alignment,
  - Hierarchy depth vs. throttling coefficient consistency across domains,
  - Meter reproducibility (seeded) and cross‑seed robustness.

D.10 Execution crosswalk to milestones/proposals/results

- T8/A8 milestones (work breakdown and sequencing): [T8-A8_Milestones.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/T8-A8_Milestones.md)
- Insight synthesis and references: [Insights_Index.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Insights_Index.md), [ALL-VDM.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/ALL-VDM.md)
- Proposal library (child whitepapers): [PROPOSALS](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/PROPOSALS)
- Results and artifacts (evidence base): [RESULTS](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/RESULTS)

D.11 Validation matrix (targets ↔ meters ↔ gates ↔ artifacts)

- M1 (Causality/telegraph): KG J‑only meter → dispersion/cone gates → CSV/PNG/JSON logs.
- M2 (Metriplectic monotonicity): Identity meter → ΔL_h ≤ 0; two‑grid; identity residuals → logs and figure panels.
- M3 (RD): RD meter → front‑speed/dispersion gates → multi‑resolution CSV/PNG/JSON.
- M4 (FRW): FRW continuity meter → RMS ≤ 1e‑6 → cosmology precheck logs.
- M5 (Gravity weak‑field): Gravity‑Regression pack → AIC/BIC beats parity vs. ΛCDM/MOND without LIV → dataset‑specific reports.
- M6 (Projection/Born): Born‑rule meters → KL ≤ 1e‑3 → convergence plots and seed‑stratified logs.

D.12 Policy and approvals (re‑stated for emphasis)

- No target is declared proven without passing gates; failed runs → failed_runs/ with contradiction JSON and no narrative targets.
- All artifact‑writing runs require approval per [authorization/README.md](Derivation/code/common/authorization/README.md).
- Determinism and reproducibility are mandatory: IEEE‑754 doubles; seeds; commit and salted hashes in JSON sidecars.

D.13 Summary: Airtight causal chain

- L0 reversible micro‑rules (J‑only) + bounded observation ⇒ L1/L2 metriplectic flow with M as necessary shadow of J.
- Hyperbolic transport arises with finite c; RD and continuum gates validate cones and fronts.
- Geometry and gravity emerge from J without background; M imposes epistemic arrow only.
- A8 induces universal boundary hierarchies that throttle transport and imprint cosmology.
- Child proposals execute this chain with preregistered meters, datasets, gates, and artifacts, all canon‑linked.

End Appendix D.

---

Appendix E — Airtight Formalization Details and Proof Obligations (Lattice → Metriplectic → Cosmology → Hierarchies)

E.0 Purpose and scope

- This appendix expands the formal chain from the discrete void lattice to full cosmology and universal hierarchies, and states proof obligations and validation gates at each layer. Equations, symbols, units, algorithms, BC/IC, constants are owned by canon; links are provided rather than restated.
- Canon anchors:
  - Axioms: [AXIOMS.md](Derivation/AXIOMS.md)
  - Equations: [EQUATIONS.md](Derivation/EQUATIONS.md)
  - Symbols: [SYMBOLS.md](Derivation/SYMBOLS.md)
  - Units: [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)
  - Algorithms: [ALGORITHMS.md](Derivation/ALGORITHMS.md)
  - BC/IC/Geometry: [BC_IC_GEOMETRY.md](Derivation/BC_IC_GEOMETRY.md)
  - Validation metrics: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
- Program context and indices:
  - Milestones: [T8-A8_Milestones.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/T8-A8_Milestones.md)
  - Insight index: [Insights_Index.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Insights_Index.md)
  - All-VDM synthesis: [ALL-VDM.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/ALL-VDM.md)
  - Canon / Proposals / Results collections:
    - [CANON](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/CANON)
    - [PROPOSALS](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/PROPOSALS)
    - [RESULTS](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/RESULTS)

E.1 L0 — Discrete lattice axioms and action anchors

- Axiom anchors: locality, metriplectic split, measurability (see [AXIOMS.md](Derivation/AXIOMS.md#vdm-ax-a2), [Derivation/AXIOMS.md#vdm-ax-a4), (A0–A7)](Derivation/AXIOMS.md))
- Discrete action and Euler–Lagrange limit:
  - [VDM-E-075](Derivation/EQUATIONS.md#vdm-e-075) Discrete Lattice Lagrangian (per time step)
  - [VDM-E-077](Derivation/EQUATIONS.md#vdm-e-077) Continuum field equation from lattice with wave speed mapping
  - [VDM-E-080](Derivation/EQUATIONS.md#vdm-e-080) Discrete interaction energy per site
- Proof obligations (no duplication of math; provide artifacts):
  - Show ∂t² term and dispersion emerge from discrete action via variational limit (Δt→0, a→0 with scale held fixed). Artifacts: derivation notebook/figures + JSON provenance.

E.2 L1 — Metriplectic pre-structure on the lattice and integrator composition

- Discrete operators with degeneracy (by construction):
  - Antisymmetric J_h; symmetric PSD M_h; degeneracies J_h·δΣ_h=0 and M_h·δI_h=0 enforced at the operator level. Construction details in [ALGORITHMS.md](Derivation/ALGORITHMS.md).
- Strang composition and stability:
  - Integrator obligations: identity residual ≤ 1e−12; two-grid slope ≥ 2.90; ΔL_h ≤ 0 under M step. Meters: Metriplectic Identity Meter (see main Section 3) with artifacts routed via [io_paths.py](Derivation/code/common/io_paths.py).
- Gap provenance (sources for planned solution):
  - [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-CG-1: Contact Hamiltonians to Metriplectic Evolution”; “G-QGT-1: Quantum Geometric Tensor to Metriplectic Brackets”.
  - [`Claude-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Claude-Gap-Fill.md) — “Contact geometry solves the metriplectic unification problem”; “Quantum geometric tensor calculations are well-established but classical limit mapping remains synthesis challenge”.
  - [`2025-11-04_A8_Bridges_Status.md`](audits/2025-11-04_A8_Bridges_Status.md) — QGT mapping and Contact bridge gaps (instrument choice and constructive bracket notes).
  - [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-CL-1: Integrability Closure Test for UMSL (No Extra First Integrals)” (closure gap and Darboux/Kowalevski/Prelle–Singer provenance).

E.3 L2 — “M is a necessary shadow of J” (epistemic emergence of dissipation)

- Statement (Shadow Principle):
  - Under bounded observation (finite-rate sampling/window W) of a reversible, local J-only micro-dynamics, the induced macroscopic flow on observables admits a symmetric PSD metric bracket M that:
    - Preserves the J-Casimir Σ (J·δΣ=0) and leaves I invariant under M (M·δI=0),
    - Produces monotone decay of a Lyapunov functional (ΔL_h ≤ 0) for the reduced variables,
    - Depends solely on the observer’s coarse-graining, introducing no new ontic forces.
- Interpretation in VDM:
  - The M-limb is an epistemic projection of the J-limb: “M is a necessary shadow of J.” Measurement irreversibility and the arrow of time live in M; the underlying reality (J) remains reversible and locally causal.
- Proof obligations:
  - Provide the projection operator definition, sampling window specification, and show degeneracy and monotonicity gates hold numerically for representative systems (artifacts + seeds + commit). Link projection details to [ALGORITHMS.md](Derivation/ALGORITHMS.md).
- Gap provenance (sources for planned solution):
  - [`Gemini-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Gemini-Gap-Fill.md) — “The ‘Projection Mechanism’ (The M-Limb’s Formalism)” gap call-out (Part II §3.0; Item 1).
  - [`Claude-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Claude-Gap-Fill.md) — “Quantum measurement as boundary formation enjoys robust theoretical support” (decoherence/einselection, Kofler–Brukner).

E.4 L3 — Hyperbolic–diffusive transport and finite propagation

- Emergent telegraph–Fisher structure and speed bound:
  - Continuum targets and dispersion anchors in [EQUATIONS.md](Derivation/EQUATIONS.md); do not restate equations here.
- Validation gates:
  - KG J-only dispersion: slope/intercept gates (R² ≥ 0.999) and cone v ≤ c(1+0.02). RD: front-speed ≤ 5% error; dispersion median error ≤ 10% with R² ≥ 0.98 (see [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)).
- Void-debt throttling:
  - Effective transport c_eff=c_0 e^{−½ β D_void} as adopted in canon; D_void measured by boundary concentration meters. State estimator in child proposal; figures grayscale-safe.
- Gap provenance (sources for planned solution):
  - [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-TF-1: Finite-Speed Transport from Fisher Information (Telegraph Equation)” (Cattaneo/Kac/Goldstein; Fisher-information derivations).
  - [`2025-11-04_A8_Bridges_Status.md`](audits/2025-11-04_A8_Bridges_Status.md) — Telegraph–Fisher causality bridge: cone-dominance gates and discretization envelope.

E.5 L4 — Geometry and gravity from the J-limb (no background assumption)

- Emergent geometry obligation:
  - Show that linear response/propagation cones define an effective Lorentz structure consistent with A2; weak-field behavior validated by perihelion precession and lensing comparisons (Gravity-Regression pack).
- LIV null:
  - No Lorentz invariance violation; gates consistent with causal cones and dispersion. Null results are recorded outcomes.

E.6 L5 — Universal hierarchies and boundary concentration (A8 program)

- Hierarchical necessity:
  - Under tachyonic/unstable regimes, finite-energy states concentrate on codimension‑1 sets with multiscale hierarchies. Depth scales ∼ Θ(log L) in canonical constructions (see A8 documents and audits).
  - Energy and perimeter budgets, along with interface‑count statistics, must be measured by meters with CSV/JSON artifacts.
- Canon anchors to cite in child work (no duplication):
  - A8 proposal: [T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md](Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md)
  - Status/audits: [2025-11-04_A8_Bridges_Status.md](audits/2025-11-04_A8_Bridges_Status.md)
- Gap provenance (sources for planned solution):
  - [`GPT-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/GPT-Gap-Fill.md) — “G-A8-1: A8 Scaling Theorem (Hierarchical Tachyonic Interfaces)” (Γ-convergence, Kohn–Müller, Zwicknagl).
  - [`Claude-Gap-Fill.md`](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Support/Claude-Gap-Fill.md) — “Hierarchical necessity proofs exist but specific VDM scalings require targeted development”.

E.7 L6 — Measurement/Born frequencies: operational meters

- Bounded observer model:
  - Define sampling constraints and reference distributions; demonstrate convergence to Born-rule frequencies with KL ≤ 1e−3 across seeds. Reversibility meter for J-only: ≤ 1e−10 drift; Noether ≤ 1e−12 (scaled epsilon allowed).
- Artifacts:
  - Ensemble plots PNG + CSV + JSON with seeds and commit hashes.

E.8 L7 — Cosmology pipeline (from lattice to sky)

- Stages:
  1) IC/BC selection from canon ([BC_IC_GEOMETRY.md](Derivation/BC_IC_GEOMETRY.md))
  2) Transport calibration (c, τ, D) via meters
  3) Primordial spectrum synthesis under A8 (canon anchor)
  4) LSS evolution + ISW + weak lensing post‑processing
  5) Model comparison: VDM vs ΛCDM vs MOND with preregistered datasets
- Gates:
  - FRW continuity RMS ≤ 1e−6 (dust) as a precondition
  - Global fits meet/exceed ΛCDM across CMB/LSS while respecting locality/cone gates; no LIV
  - Hubble tension posture addressed without ad‑hoc additions by causal genesis/hierarchy effects
- Evidence handling:
  - PNG+CSV+JSON per dataset; report AIC/BIC and residuals; contradiction routing on failures.

E.9 L8 — Cross-domain universalities and consistency checks

- Universal fingerprints across RD, fluids, cosmology, agency:
  - Finite cones (A2), metriplectic degeneracy, boundary concentration, projection‑induced irreversibility (ΔL_h ≤ 0)
- Consistency gates:
  - Cone speeds vs. global light-cone; throttling parameters vs. hierarchy depth; cross‑seed and cross‑resolution robustness.

E.10 Validation matrix (targets ↔ meters ↔ gates ↔ artifacts) — extended

- M1 (Causality/telegraph): KG J‑only meter → dispersion/cone gates → CSV/PNG/JSON
- M2 (Metriplectic monotonicity): Identity meter → ΔL_h ≤ 0; two‑grid; identity residuals → logs/figures
- M3 (RD): RD meter → front‑speed/dispersion gates → multi‑resolution CSV/PNG/JSON
- M4 (FRW): FRW meter → RMS ≤ 1e−6 → cosmology precheck
- M5 (Weak‑field gravity): Gravity‑Regression pack → AIC/BIC beats vs ΛCDM/MOND without LIV → dataset‑specific reports
- M6 (Projection/Born): Born‑rule meters → KL ≤ 1e−3 → convergence plots/logs
- Crosswalk to milestones: see [T8-A8_Milestones.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/T8-A8_Milestones.md) for sequencing.

E.11 Proof obligations registry (to be satisfied by child proposals)

- Discrete→continuum action derivation completeness (anchors: [VDM-E-075](Derivation/EQUATIONS.md#vdm-e-075), [VDM-E-077](Derivation/EQUATIONS.md#vdm-e-077))
- Operator degeneracy at discrete and continuum levels; numerical preservation to machine‑epsilon (Identity meter)
- Data‑processing compliant projection: definition, calibration, and invariance of Σ, I under the respective limbs (link [ALGORITHMS.md](Derivation/ALGORITHMS.md))
- Boundary concentration metrics and interface‑count estimators (units/normalization in [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md))
- Cosmology FRW continuity precheck; dataset preregistration and model‑selection transparency

E.12 Policy restatement and approvals

- No claims without passing gates; failed runs → failed_runs/ with contradiction JSON; null predictions are claims.
- Approvals are required prior to artifact‑writing runs per [authorization/README.md](Derivation/code/common/authorization/README.md).

E.13 Executive synthesis

- The formal chain is now explicit and testable: L0 reversible lattice (J) → metriplectic limit with enforced degeneracy → “M is a necessary shadow of J” via bounded observation → finite‑speed transport and cones → emergent geometry/gravity without background → universal boundary hierarchies from A8 → cosmology with causal genesis fingerprints and cross‑model gates.
- All mathematical content is canon‑linked; all validation is meter‑based with unit‑consistent observables and quantitative thresholds.

End Appendix E.

---

Appendix F — Refinement: Airtight Formalization Recap and Execution Details (Lattice → Metriplectic → Cosmology → Hierarchies)

F.0 Purpose

- This appendix tightens the end-to-end formalization with explicit proof obligations, meter mappings, null hypotheses, and unit-consistent observables. It emphasizes the epistemic status of M (the necessary shadow of J) and the discrete-to-continuum chain up to cosmology and universal hierarchies. Canon is linked, not duplicated.

Canon and indices (owners of record)

- Axioms: [AXIOMS.md](Derivation/AXIOMS.md)
- Equations: [EQUATIONS.md](Derivation/EQUATIONS.md)
- Symbols/Units: [SYMBOLS.md](Derivation/SYMBOLS.md), [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)
- Algorithms/integrators: [ALGORITHMS.md](Derivation/ALGORITHMS.md)
- BC/IC/Geometry: [BC_IC_GEOMETRY.md](Derivation/BC_IC_GEOMETRY.md)
- Validation metrics: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
- Program indices: [T8-A8_Milestones.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/T8-A8_Milestones.md), [Insights_Index.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/Insights_Index.md), [ALL-VDM.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/ALL-VDM.md)

F.1 L0 Discrete lattice: substrate, invariants, dimensionless groups

- Substrate: Locally finite lattice/graph with adjacency locality; no background geometry assumed (A2 enforces finite influence radius). See axioms in [AXIOMS.md](Derivation/AXIOMS.md).
- Action anchors (no restatement): [VDM-E-075](Derivation/EQUATIONS.md#vdm-e-075), [VDM-E-077](Derivation/EQUATIONS.md#vdm-e-077), [VDM-E-080](Derivation/EQUATIONS.md#vdm-e-080).
- Discrete invariants: Construct Σ_h (entropy-like) and I_h (energy/invariant) so that micro J-only updates preserve Σ_h; any admissible M_h preserves I_h at coarse level. Unit conventions in [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md).
- Dimensionless groups: Update cadence, local coupling, and coarse-graining window define regimes and the hyperbolic–diffusive transition; observables must be reported in canon units.

Proof obligations (artifacts required)

- Provide notebooks/figures showing Euler–Lagrange discrete-to-continuum limit as Δt→0, a→0 with fixed scale; CSV/JSON logs include commit and salted provenance.

F.2 L1 Metriplectic pre-structure and composition

- Operators: Discrete J_h antisymmetric; M_h symmetric PSD. Degeneracy enforced: J_h·δΣ_h=0; M_h·δI_h=0. Operator construction in [ALGORITHMS.md](Derivation/ALGORITHMS.md).
- Composition: Reversible micro-step + metric relaxation compose (Strang) to metriplectic flow; gates: identity residual ≤ 1e−12; two-grid slope ≥ 2.90; ΔL_h ≤ 0.
- Meter: Metriplectic Identity Meter with PNG+CSV+JSON routed via [io_paths.py](Derivation/code/common/io_paths.py).

F.3 L2 “M is a necessary shadow of J”

- Statement: Under bounded observation (finite-rate sampling/window W) of a reversible local J-only dynamics, the macroscopic reduced flow on observables admits a symmetric PSD metric bracket M that introduces no new ontic forces. M preserves I; J preserves Σ; ΔL_h ≤ 0 holds. Hence “M is a necessary shadow of J.”
- Consequence: Measurement irreversibility and time’s arrow are epistemic (M-limb), while the underlying J-limb remains reversible and locally causal.
- Proof/metering: Define W (space/time/energy window), specify projection operator, demonstrate degeneracy and ΔL_h gates on representative systems with seed-reproducible logs; details in [ALGORITHMS.md](Derivation/ALGORITHMS.md).

F.4 L3 Hyperbolic–diffusive transport and causality

- Emergence: Telegraph–Fisher structure under finite response time τ and diffusivity D (anchors in [EQUATIONS.md](Derivation/EQUATIONS.md)); finite speed c=√(D/τ).
- Gates: KG J-only dispersion slope/intercept (R² ≥ 0.999) and cone v ≤ c(1+0.02). RD: front-speed ≤ 5% error; dispersion median error ≤ 10% with R² ≥ 0.98 (see [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)).
- Throttling: c_eff = c_0 e^{−½ β D_void} under void-debt D_void; estimator defined and logged with units from [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md).

F.5 L4 Geometry and gravity from J (no background)

- Effective geometry: Cones and reversible flux define a Lorentzian structure consistent with A2; weak-field matches via perihelion/lensing regression.
- Meter: Gravity-Regression Pack; model selection (AIC/BIC) meets or exceeds ΛCDM/MOND without LIV; locality gates pass.

F.6 L5 Universal hierarchies and boundary concentration (A8)

- Thesis: In tachyonic/unstable regimes (A8), finite-energy configurations concentrate on codimension-1 sets with multiscale interface hierarchies; depth scales ∼ Θ(log L) in canonical constructions (parameters tracked in canon).
- Operationalization:
  - Interface count N(L): Define windowing, counting rules, and normalization; record with units.
  - Boundary energy estimator: Units and calibration per [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md).
  - Fingerprints: Spatial (log-spaced scales), spectral (broken power laws), dynamical (c_eff attenuation).
- Gate: Joint pass on depth and boundary-law energy with preregistered nulls; contradiction routing if fail.

F.7 L7 Cosmology pipeline (from lattice to sky)

- Stages (no equations duplicated):
  1) IC/BC per [BC_IC_GEOMETRY.md](Derivation/BC_IC_GEOMETRY.md),
  2) Transport calibration (c, τ, D) via meters,
  3) Primordial spectrum from A8,
  4) LSS + ISW + weak lensing,
  5) Model comparison vs ΛCDM/MOND (datasets preregistered).
- Precondition: FRW continuity RMS ≤ 1e−6 (dust).
- Nulls and targets:
  - LIV: Null result is a positive recorded outcome (no dispersion LIV).
  - MOND vs VDM-gravity: Competing fits reported with AIC/BIC and held-out validation.
  - Hubble tension: Addressed without ad‑hoc additions, by causal genesis/hierarchy effects.
- Artifacts: PNG/CSV/JSON; seeds and commit logged; figures grayscale-safe.

F.8 Validation matrix (extended, execution-level)

- M1 Causality/telegraph: KG J-only meter → dispersion/cone gates → CSV/PNG/JSON.
- M2 Metriplectic monotonicity: Identity meter → ΔL_h ≤ 0; two-grid; identity residuals → logs/panels.
- M3 RD: RD meter → front-speed and dispersion gates → multi-resolution artifacts.
- M4 FRW: FRW meter → RMS ≤ 1e−6 → cosmology precheck.
- M5 Weak-field gravity: Gravity-Regression → AIC/BIC beats or parity without LIV → dataset reports.
- M6 Projection/Born: Born-rule meters → KL ≤ 1e−3 across seeds → convergence plots/logs.

F.9 Threat model and null hypotheses

- LIV search: Fail to detect LIV within sensitivity → supports A2 and J-limb locality.
- MOND parity tests: If MOND uniquely outperforms, VDM-gravity mapping must be revised; if VDM meets/exceeds with fewer assumptions, claim stands.
- A8 hierarchy nulls: ER/BA nulls can mimic log-depth; boundary-law energy scaling under same estimator/normalization must separate VDM from nulls (see audits and prereg in [A8_Bridges_Status.md](audits/2025-11-04_A8_Bridges_Status.md)).

F.10 Reproducibility, policy, and approvals (re‑affirmed)

- Determinism: IEEE‑754 double; seeds; commit+salted hashes in JSON sidecars.
- Routing: [io_paths.py](Derivation/code/common/io_paths.py) for all artifacts; no ad‑hoc paths.
- Policy: No target is declared proven without gates; failures → failed_runs/ with contradiction JSON; approvals required per [authorization/README.md](Derivation/code/common/authorization/README.md).

F.11 Crosswalk to milestones (concrete next steps)

- Discrete action → continuum proof artifacts (T8/A8: ms-discrete-action-recast).
- Identity/telegraph/RD meters to PASS on current runners; record seeds/commits.
- Gravity-Regression Pack: SPARC and cluster lensing comparisons with preregistered datasets.
- Cosmology pipeline: FRW precheck, ISW+Lens, global fits with null comparisons.
- A8 hierarchy meters: N(L), boundary energy scaling; joint null separation.

F.12 Executive synthesis

- The chain “L0 reversible J → metriplectic with M as necessary shadow of J → finite-speed transport → emergent geometry/gravity → universal hierarchies (A8) → cosmology with anomaly posture” is now fully specified by canon-linked claims, unit-consistent observables, and quantitative gates. Execution proceeds via meters and preregistered analyses, with approvals and contradiction policy enforcing scientific discipline.

End Appendix F.
