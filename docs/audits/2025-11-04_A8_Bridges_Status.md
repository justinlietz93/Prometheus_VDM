# A8 Bridges Status — What exists vs. what is missing (Derivation-ready, no compute)

Metadata

- Scope: PRIVATE/Axiom-8 status notes and code-crawler mappings for A8 bridges
- Sources scanned:
  - PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/*.md (informal blueprints)
  - PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/*.md (mapped summaries)
  - Canon anchors: Derivation/AXIOMS.md, Derivation/EQUATIONS.md, Derivation/VALIDATION_METRICS.md
- Generated UTC: 2025-11-04T20:51:00Z
- Assembler: VDM research assistant
- File: PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/code_crawler_results/A8_Bridges_Status.md

High-level counts

Formalism (bridges/theory)

- Complete: 0
- Partial: 7
- Missing: 0

Hard numerical RESULTS / Logs (instrument-grade artifacts relevant to A8)

- Complete: 4  (KG J-only: dispersion, energy oscillation; RD: front-speed, linear dispersion)
- Partial: 2   (Metriplectic assisted-echo T4 prereg; Cosmology FRW continuity)
- Missing: 2   (Causality DAG audit for cone dominance; Networks/Topology null-comparator runs)

Notes:

- “Complete” (formalism) = written derivation + registered canon equation/definition + prereg schema + passing RESULTS.
- “Partial” (formalism) = strong plan and/or partial formal elements exist, but at least one of: lemma/theorem, canon equation/definition, admissible discretization, or prereg/RESULTS is missing.
- “Complete” (results) = PNG/CSV/JSON artifacts in canon paths, with provenance, meeting gates.

Domain breakdown and strength assessment

- Metriplectic (assisted echo / CEG)
  - Strength: Full instrument framework exists (echo metrics and gates), prereg schema present; rich figures/logs exist.
    - Runners/instruments: [assisted_echo.py](../../../../../../Derivation/code/physics/metriplectic/assisted_echo.py), [echo_gates.py](../../../../../../Derivation/code/physics/metriplectic/echo_gates.py)
    - Artifacts (examples visible): figures in Derivation/code/outputs/figures/metriplectic/ (20251104_…_assisted_echo_*.png)
  - Gap: G4 Strang defect gate failing; G5 outcome below tol in current plots; needs parameter/commutator resolution ladder before heavier ensembles.

- Causality (cones and DAG audits)
  - Strength: Clean KPI framing and audit plan using TE/MTE; cone-dominance gate specified; A2 boundaries crisp.
    - Plan: [causality.md](../../T8-A8_Insights/Collections/causality.md)
    - Proposal: [PROPOSAL_Metriplectic_Causal_Dominance_v1.md](../../../../../../Derivation/Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md)
    - Axiom: [AXIOMS.md#vdm-ax-a2](../../../../../../Derivation/AXIOMS.md#vdm-ax-a2)
  - Gap: TF canon equation + short lemma to KG cone; discretization envelope for operator-split scheme; prereg + stub RESULTS run.

- Klein–Gordon J-only (instruments)
  - Strength: Dispersion, light-cone, and energy-oscillation instruments are proven and compliant; serve as causal baselines for A8.
    - Runners: [run_kg_dispersion.py](../../../../../../Derivation/code/physics/metriplectic/run_kg_dispersion.py), [run_kg_energy_oscillation.py](../../../../../../Derivation/code/physics/metriplectic/run_kg_energy_oscillation.py)
  - Gap: None for baseline; these are trusted meters.

- Reaction–Diffusion controls
  - Strength: Front-speed and linear dispersion validation with PASS gating and artifacts; reliable null/baseline for A8 numerics.
    - Example logs: Derivation/code/outputs/logs/reaction_diffusion/*.json; figures under …/figures/reaction_diffusion/
  - Gap: None for baseline; instrumentation is sound.

- Cosmology
  - Strength: FRW continuity instrument exists with passing figures; pipeline thinking to ISW is correct.
    - FRW results: Derivation/code/outputs/figures/cosmology/*FRW-balance-v1.png
    - Plan to ISW: [Cosmology.md](../../T8-A8_Insights/Collections/Cosmology.md)
  - Gap: Weak-field Poisson → ISW ΔT/T needs canon equation block + minimal IO schema and toy RESULTS.

- Networks / Topology (null comparators)
  - Strength: Sharp warning that log-depth alone is non-unique; explicit ER/BA nulls designated.
    - Rationale: [Complex-Networks.md](../../T8-A8_Insights/Collections/Complex-Networks.md), [VDM-Mapping.md](../VDM-Mapping.md)
  - Gap: Boundary-law energy estimator E_exc(L) needs canonical definition; null-model failure argument to be formalized; prereg harness to bind the joint gate.

- Quantum foundations (QGT and Schrödingerization)
  - Strength: Two convergent formalisms laid out (projection via QGT, lifting via KvN) that together close the conceptual loop “quantum ↔ metriplectic.”
    - QGT path: [quantum-geometry.md](../../T8-A8_Insights/Collections/quantum-geometry.md)
    - KvN path: [schrodingerization.md](../../T8-A8_Insights/Collections/schrodingerization.md)
  - Gap: Need a compact constructive bracket + degeneracy derivation (QGT→{·,·}\_Ω and (·,·)\_g) and one explicit H_KvN + projection map check.

- Closure / Integrability (no hidden invariants beyond A4)
  - Strength: Correct instrument choice (Darboux/Kowalevski) and precise target: only A4-forced invariants survive.
    - Plan: [Closure.md](../../T8-A8_Insights/Collections/Closure.md)
  - Gap: Theorem box for a restricted UMSL class with assumptions and proof sketch.

- Entropy-as-a-Driver / MEP
  - Strength: Clear physics rationale to compare hierarchy-on vs ablation with \dot{Σ} meter; aligns with metriplectic H-theorem numerics.
    - Plan: [Entropy-as-a-Driver.md](../../T8-A8_Insights/Collections/Entropy-as-a-Driver.md)
  - Gap: Gate definition (statistic, windowing, tolerances) and a minimal \dot{Σ} meter wired to the DG M-step.

Bridges by topic — what you have vs what is missing

1) Telegraph–Fisher causality bridge (finite-speed, cone-dominance)

Have (informal plans and canon context)

- Instrument/plan to audit causality via Transfer Entropy and MTE:
  - [causality.md](../../T8-A8_Insights/Collections/causality.md)
  - Runner reference (codebase): [run_causality_dag_audit.py](../../../../../../Derivation/code/physics/causality/run_causality_dag_audit.py)
- Cone dominance proposal and gates (inside/outside L² tail, scaling collapse; red-team telegraphized proxy):
  - [PROPOSAL_Metriplectic_Causal_Dominance_v1.md](../../../../../../Derivation/Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md)
- Axiom boundary for cones (hyperbolic J-only vs parabolic RD):
  - [AXIOMS.md (A2)](../../../../../../Derivation/AXIOMS.md#vdm-ax-a2)
- Parabolic causal solution (retarded kernel) already anchored as equation:
  - [EQUATIONS.md · VDM-E-004](../../../../../../Derivation/EQUATIONS.md#vdm-e-004)

Missing or partial (to finish the bridge)

- Canon PDE entry for Telegrapher TF (VDM-E-xxx): τ φ_tt + φ_t = D ∇²φ + f(φ), with a unit-consistent map to c_TF = √(D/τ), and a short lemma c_TF ≤ c_J under the calibration used for KG (assumptions: linear regime, BC/IC class, f smooth).
- Discretization envelope for JMJ/IMEX composition: inequalities on (Δx, Δt, τ, D) that ensure the cone-dominance gate holds with a declared buffer δ and tolerance ε_tail; connect directly to the cone-slack KPI in the proposal.
- Prereg schema + one RESULTS stub (no heavy grid): JSON/CSV/PNG through io_paths, logging pass/fail of the cone L²-tail ratio and scaling collapse across a small seed set.

2) Closure / Integrability (no hidden invariants beyond A4)

Have

- Plan to adapt Darboux/Kowalevski methods; explicit target of “no analytic first integrals except those forced by A4”:
  - [Closure.md](../../T8-A8_Insights/Collections/Closure.md)
- Canon targets to cite while proving:
  - A4 degeneracies and metriplectic split: [AXIOMS.md](../../../../../../Derivation/AXIOMS.md), [EQUATIONS.md · VDM-E-042 (metriplectic flow)](../../../../../../Derivation/EQUATIONS.md#vdm-e-042)

Missing or partial

- Theorem box for a restricted but nontrivial UMSL class: assumptions (analyticity, polynomial degree, domain/BC), statement (“no nontrivial analytic first integrals beyond Σ- and I-induced trivialities”), proof sketch referencing Darboux polynomials/Kowalevski exponents.
- Mapping notes: how A4 degeneracies appear as the only surviving invariants under those assumptions.

3) QGT → Metriplectic (top‑down projection: quantum → classical J/M)

Have

- Precise QGT object and mapping intuition (Q = g − iΩ/2), with pointer to real data for g and Ω:
  - [quantum-geometry.md](../../T8-A8_Insights/Collections/quantum-geometry.md)
- Program impact called out: derive (not guess) I and Σ; aligns to EBN-Info-Functional and covariant notes.

Missing or partial

- Constructive brackets and degeneracies:
  - Exhibit a Poisson bracket {·,·}\_Ω from Ω and a metric bracket (·,·)\_g from g such that Jᵀ = −J, Mᵀ = M ⪰ 0, and the A4 degeneracies J·δΣ = 0, M·δI = 0 hold.
  - Provide one minimal toy example (2D parameterization) carrying the algebra into the classical limit and verifying positivity/antisymmetry and both degeneracies explicitly.
- A short note on conditions (regularity/geometry) under which the projection preserves those bracket properties.

4) Schrödingerization / Koopman–von Neumann lifting (bottom‑up unification)

Have

- Unified Hamiltonian “lift” plan to encode J ⊕ M as a single reversible KvN flow:
  - [schrodingerization.md](../../T8-A8_Insights/Collections/schrodingerization.md)

Missing or partial

- One explicit H\_KvN for a minimal metriplectic PDE (e.g., KG + linearized metric dissipation), with projection map Π such that Π(ψ) recovers ẋ = J∇I + M∇Σ exactly.
- Check that energy conservation along the lifted Hamiltonian flow corresponds to the classical J-branch conservation, and that monotone Σ arises under projection.
- Show how A4 degeneracies correspond to symmetries/invariants in the lifted system (Noether shadow) in two lines.

5) A8 joint discriminator: log-depth and boundary-law energy (null comparators)

Have

- Network-theory nulls and the “log-depth is not unique” warning:
  - [Complex-Networks.md](../../T8-A8_Insights/Collections/Complex-Networks.md)
  - Consolidated mapping: [VDM-Mapping.md](../VDM-Mapping.md)
- Formal A8 setting and predictions (depth and boundary-law energy) to cite:
  - [T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md](../../../../../../Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md)
- Mainstream null hypothesis (Sen’s tachyon condensation) vs. your “reorganization” claim:
  - [complete-formalism.md](../../T8-A8_Insights/Collections/complete-formalism.md)

Missing or partial

- Measurement definition for E\_exc(L): windowing, units, and estimator details used in the boundary-law test; record as canon.
- Short lemma/argument why ER and BA nulls can reproduce log-depth but generically fail the boundary-law energy scaling under the same estimator and normalization (state the precise failure mode).
- Prereg schema that binds the joint gate (both must pass on VDM; nulls must fail boundary-law) and logs pass/fail as CSV/JSON with seed details.

6) Cosmology bridge (weak-field Poisson → ISW ΔT/T)

Have

- Planning note that “Beyond the Cosmological Standard Model” provides the equations to execute ISW and weak-field post-processing:
  - [Cosmology.md](../../T8-A8_Insights/Collections/Cosmology.md)

Missing or partial

- Canon snippet (equation block) for the exact weak-field Poisson linkage to your φ-field energy density and the ISW line-of-sight integral; fix units and conventions.
- IO schema for a minimal instrument (no heavy sky maps): accept Φ(t, x), integrate along straight rays for a toy box, produce ΔT/T PNG + CSV + JSON with provenance.

7) Entropy-as-a-Driver / MEP gate

Have

- Conceptual derivation and motivation for a MEP-based discriminator:
  - [Entropy-as-a-Driver.md](../../T8-A8_Insights/Collections/Entropy-as-a-Driver.md)
  - Aggregate mapping: [VDM-Mapping.md](../VDM-Mapping.md)

Missing or partial

- Explicit gate definition (G-MEP): statistic, time-windowing, and pass criterion comparing hierarchy-on vs. ablation runs; declare units and thresholds; list control baselines.
- Minimal meter: definition of \dot{Σ}(t) computed consistently with your discrete gradient M-step and the Lyapunov functional already in canon.

Notes on canon anchors to use while formalizing

- Axioms and degeneracies: [AXIOMS.md](../../../../../../Derivation/AXIOMS.md)
- Metriplectic flow: [EQUATIONS.md · VDM-E-042](../../../../../../Derivation/EQUATIONS.md#vdm-e-042)
- Agency/retarded kernel (parabolic causal): [EQUATIONS.md · VDM-E-004](../../../../../../Derivation/EQUATIONS.md#vdm-e-004)
- Validation thresholds: [VALIDATION_METRICS.md](../../../../../../Derivation/VALIDATION_METRICS.md)

Summary

- You already have strong informal blueprints for TF causality/DAG audits, closure, QGT mapping, KvN lifting, A8 joint discriminator, cosmology ISW linkage, and MEP logic.
- None of the missing pieces require heavy compute. Each bridge can be closed by adding: (i) a short lemma/theorem or bracket construction, (ii) a canon equation or measurement definition with units, (iii) a discretization/admissibility paragraph where relevant, and (iv) a lightweight prereg/RESULTS stub that routes artifacts via io_paths.
