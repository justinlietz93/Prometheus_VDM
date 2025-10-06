<!-- DOC-GUARD: REFERENCE -->
<!-- markdownlint-disable MD033 -->
# VDM Roadmap (Compiled from Repository Evidence)

**Scope:** Milestones and tasks already recorded in this repository (docs, comments, logs, exported issues).  
**Rules:** Planning-only. Link to canonical math/specs (SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS/BC_IC/VALIDATION/DATA_PRODUCTS/SCHEMAS). Do not duplicate canon here.

---

## Near-Term Milestones

## <a id="ms-frw-balance"></a>FRW Continuity Residual Validation (Gravity)

**Status:** Done • **Priority:** P1  
**Source:** derivation/cosmology/PROPOSAL_FRW_Balance_v1.md; derivation/code/physics/cosmology/run_frw_balance.py  

**Goal (verbatim/condensed from source):** Validate FRW energy continuity with source bookkeeping by measuring the RMS residual of the continuity equation under controlled scenarios (e.g., dust) with causal sourcing gates.

**Acceptance criteria (links only, no formulas):**

- Metrics/KPIs: RMS continuity residual ≤ tolerance (double precision scale)  
- Data products to produce: `DATA_PRODUCTS.md` entry for cosmology/FRW residuals (add upon standardization)

**Dependencies:** Axiomatic bookkeeping and units normalization  
**Risks/Constraints:**

- Requires causal source kernel consistency across channels  
- Tight numerical tolerances can mask discretization artifacts if grids are too coarse

**Deliverables:**

- derivation/cosmology/PROPOSAL_FRW_Balance_v1.md  
- derivation/code/physics/cosmology/run_frw_balance.py  
- Tagged artifacts: `derivation/code/outputs/{logs,figures}/cosmology/FRW-balance-v1/*`

**Target timeframe (if stated):** ✓ Completed — RMS ≈ O(10⁻¹⁵) in baseline dust sanity test (PASS)

## <a id="ms-axiomatic-foundation"></a>Axiomatic Foundation Development

**Status:** In progress • **Priority:** P1  
**Source:** derivation/axiomatic_theory_development.md:79-150 • 77f055f

**Goal (verbatim/condensed from source):** Establish rigorous axiomatic foundation for VDM, deriving continuum dynamics from discrete action principle. Phases I-III completed (axioms, continuum limit, symmetries). Phase IV (validation) and Phase V (extensions) in progress.

**Acceptance criteria (links only, no formulas):**

- Equations referenced: `EQUATIONS.md#vdm-e-008` (RD canonical)
- Data products to produce: `DATA_PRODUCTS.md#data-rd-front-speed`, `DATA_PRODUCTS.md#data-rd-dispersion`
- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-rd-front-speed-rel-err`, `VALIDATION_METRICS.md#kpi-rd-dispersion-med-rel-err`

**Dependencies:** None (foundational work)  
**Risks/Constraints:**

- Tachyonic root detection requires careful numerical handling
- EFT/KG branch quarantined pending complete discrete action derivation

**Deliverables:**

- derivation/foundations/void_dynamics_theory.md
- derivation/foundations/discrete_to_continuum.md
- derivation/foundations/symmetry_analysis.md
- derivation/foundations/continuum_stack.md

**Target timeframe (if stated):** Phases I-III ✓ completed; Phase IV-V ongoing

---

### <a id="task-discrete-action"></a>Discrete Action Formulation

**Source:** derivation/axiomatic_theory_development.md:91-97 • 77f055f  
**Description:** Apply discrete Euler-Lagrange equations rigorously to derive second-order time dynamics naturally (no "promotion")  
**Linked canon:** symbols → `SYMBOLS.md#sym-W`, equations → `EQUATIONS.md#vdm-e-001`, constants → `CONSTANTS.md#const-J`  
**Exit criteria:** Second-order time dynamics derived from variational principle without hand-waving  
**Owner (if present):** — • **Status:** ✓ Completed

---

### <a id="task-spatial-interaction"></a>Spatial Interaction Derivation

**Source:** derivation/axiomatic_theory_development.md:99-106 • 77f055f  
**Description:** Derive exact spatial kinetic prefactor $c_{\text{lat}} a^2 (\nabla\phi)^2$ from discrete interaction energy via Taylor expansion on cubic lattice  
**Linked canon:** symbols → `SYMBOLS.md#sym-J`, equations → `EQUATIONS.md#vdm-e-002`, constants → `CONSTANTS.md#const-c-lat`  
**Exit criteria:** Exact value $c_{\text{lat}} = 2$ for 3D cubic lattice; Lorentz invariance condition $c^2 = 2J a^2$  
**Owner (if present):** — • **Status:** ✓ Completed

---

### <a id="task-continuum-mapping"></a>Rigorous Continuum Mapping

**Source:** derivation/axiomatic_theory_development.md:110-116 • 77f055f  
**Description:** Define scaling limits with fixed wave speed; establish field redefinition; derive continuum action from discrete limit  
**Linked canon:** symbols → `SYMBOLS.md#sym-phi`, equations → `EQUATIONS.md#vdm-e-008`, `EQUATIONS.md#vdm-e-010`  
**Exit criteria:** Continuum action derived with proper scaling; connection to both RD and Klein-Gordon forms established  
**Owner (if present):** — • **Status:** ✓ Completed

---

### <a id="task-potential-analysis"></a>Potential Function Analysis

**Source:** derivation/axiomatic_theory_development.md:118-125 • 77f055f  
**Description:** Add quartic stabilization to potential; determine parameter constraints for global minimum existence; calculate vacuum solutions  
**Linked canon:** symbols → `SYMBOLS.md#sym-V`, constants → `CONSTANTS.md#const-alpha`, `CONSTANTS.md#const-beta`, `CONSTANTS.md#const-lambda`  
**Exit criteria:** Bounded-below potential with controlled vacuum structure; effective mass $m_{\text{eff}}^2 = V''(v)$ calculated  
**Owner (if present):** — • **Status:** ✓ Completed

---

### <a id="task-symmetry-analysis"></a>Symmetry Analysis and Conservation Laws

**Source:** derivation/axiomatic_theory_development.md:136-149 • 77f055f  
**Description:** Apply Noether's theorem to derive conserved currents; analyze symmetry breaking patterns  
**Linked canon:** equations → `EQUATIONS.md#vdm-e-020` (energy conservation), algorithms → TODO: add anchor (see derivation/foundations/symmetry_analysis.md)  
**Exit criteria:** Complete conservation law framework; energy, momentum conservation verified  
**Owner (if present):** — • **Status:** ✓ Completed

---

## <a id="ms-rd-validation"></a>RD Canonical Validation

**Status:** Done • **Priority:** P1  
**Source:** derivation/reaction_diffusion/rd_validation_plan.md:1-99 • 77f055f; derivation/VDM_Overview.md:35 • 77f055f

**Goal (verbatim/condensed from source):** Establish reproducible numeric checks for the RD canonical model with front speed and linear dispersion validation

**Acceptance criteria (links only, no formulas):**

- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-rd-front-speed-rel-err` (≤ 0.05), `VALIDATION_METRICS.md#kpi-rd-front-speed-r2` (≥ 0.98)
- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-rd-dispersion-med-rel-err` (≤ 0.10), `VALIDATION_METRICS.md#kpi-rd-dispersion-r2-array` (≥ 0.98)
- Equations referenced: `EQUATIONS.md#vdm-e-008` (RD dynamics), `EQUATIONS.md#vdm-e-033` (front speed)
- Data products to produce: `DATA_PRODUCTS.md#data-rd-front-speed`, `DATA_PRODUCTS.md#data-rd-dispersion`

**Dependencies:** #ms-axiomatic-foundation  
**Risks/Constraints:**

- Front speed sensitivity to level choice and fit window
- Dispersion fit method comparison (windowed DFT vs rFFT)

**Deliverables:**

- derivation/code/physics/rd_front_speed_experiment.py
- derivation/code/physics/rd_dispersion_experiment.py
- derivation/reaction_diffusion/rd_front_speed_validation.md
- derivation/reaction_diffusion/rd_dispersion_validation.md

**Target timeframe (if stated):** ✓ Completed - validated with rel_err ≈ 0.047, R² ≈ 0.999996 (front speed); rel_err ≈ 1.45×10⁻³, R² ≈ 0.99995 (dispersion)

---

### <a id="task-front-speed"></a>Fisher-KPP Front Speed Validation

**Source:** derivation/reaction_diffusion/rd_validation_plan.md:24-40 • 77f055f  
**Description:** Validate theoretical front speed $c_{th} = 2\sqrt{D r}$ against measured front position tracking with Neumann BCs  
**Linked canon:** equations → `EQUATIONS.md#vdm-e-033`, constants → `CONSTANTS.md#const-D`, `CONSTANTS.md#const-r`  
**Exit criteria:** rel_err ≤ 0.05, R² ≥ 0.98, cross-check gradient-based speed  
**Owner (if present):** — • **Status:** ✓ Proven

---

### <a id="task-dispersion"></a>Linear Dispersion Validation

**Source:** derivation/reaction_diffusion/rd_validation_plan.md:42-57 • 77f055f  
**Description:** Validate per-mode growth rate $\sigma(m)$ via linear fit of log|Û_m(t)| against discrete and continuum theory  
**Linked canon:** equations → TODO: add anchor (see derivation/reaction_diffusion/rd_dispersion_validation.md), constants → `CONSTANTS.md#const-D`, `CONSTANTS.md#const-r`  
**Exit criteria:** median relative error ≤ 0.10 over good modes (R²_mode ≥ 0.95); R²_array ≥ 0.98  
**Owner (if present):** — • **Status:** ✓ Proven

---

## <a id="ms-memory-steering"></a>Memory Steering Mechanism

**Status:** In progress • **Priority:** P2  
**Source:** derivation/memory_steering/memory_steering_acceptance_verification.md:1-108 • 77f055f; OPEN_QUESTIONS.md#oq-004 • 77f055f

**Goal (verbatim/condensed from source):** Define quantitative acceptance criteria and reproducible verification protocol for memory steering mechanism; validate fixed-point convergence, boundedness, and canonical void target convergence

**Acceptance criteria (links only, no formulas):**

- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-mem-steering-drift-abs` (≤ 0.02)
- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-mem-steering-target-abs` (|M_final - 0.6| ≤ 0.02)
- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-mem-steering-snr-db` (≥ 3 dB improvement)
- Equations referenced: TODO: add anchor (see derivation/memory_steering/memory_steering.md)
- Data products to produce: `DATA_PRODUCTS.md#data-memory-steering-acceptance`

**Dependencies:** #ms-rd-validation (RD baseline must be proven)  
**Risks/Constraints:**

- Coupling memory-steering overlays to RD baseline (see OQ-003)
- Memory-steering update formula verification pending

**Deliverables:**

- derivation/memory_steering/memory_steering.md
- derivation/memory_steering/memory_steering_acceptance_verification.md
- derivation/code/physics/memory_steering/memory_steering_acceptance.py
- derivation/code/physics/memory_steering/memory_steering_experiments.py

**Target timeframe (if stated):** Acceptance harness defined; validation in progress

---

### <a id="task-mem-acceptance"></a>Memory Steering Acceptance Tests

**Source:** derivation/memory_steering/memory_steering_acceptance_verification.md:55-108 • 77f055f  
**Description:** Run acceptance harness with fixed parameters (g=0.12, λ=0.08) and verify all acceptance checks pass  
**Linked canon:** equations → TODO: add anchor (see derivation/memory_steering/memory_steering.md:108), constants → TODO: add anchor (see derivation/memory_steering/memory_steering.md)  
**Exit criteria:** All acceptance checks pass; drift ≤ 0.02, target convergence verified, SNR improvement ≥ 3 dB  
**Owner (if present):** — • **Status:** In progress

---

## <a id="ms-fluids-sector"></a>LBM Fluids Sector Validation

**Status:** In progress • **Priority:** P2  
**Source:** derivation/fluid_dynamics/BENCHMARKS_FLUIDS.md:1-98 • 77f055f

**Goal (verbatim/condensed from source):** Define falsifiable acceptance thresholds for the fluids sector (LBM→NS) to certify reduction to Navier-Stokes; validate Taylor-Green vortex and lid-driven cavity benchmarks

**Acceptance criteria (links only, no formulas):**

- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-taylor-green-visc-rel-err` (≤ 0.05 at baseline grid ≥ 256²)
- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-lid-cavity-div-max` (≤ 1e-6 for double precision)
- Equations referenced: TODO: add anchor (see derivation/fluid_dynamics/fluids_limit.md)
- Data products to produce: TODO: add anchor (see derivation/code/outputs/figures/fluid_dynamics/)

**Dependencies:** None (parallel track to RD sector)  
**Risks/Constraints:**

- LBM→NS reduction validation does not change RD sector's canonical status
- Void-walker announcers must pass non-interference test

**Deliverables:**

- derivation/fluid_dynamics/BENCHMARKS_FLUIDS.md
- derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py
- derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py
- derivation/code/tests/fluid_dynamics/test_walkers_noninterference.py

**Target timeframe (if stated):** Benchmarks defined; validation in progress

---

### <a id="task-taylor-green"></a>Taylor-Green Vortex Benchmark

**Source:** derivation/fluid_dynamics/BENCHMARKS_FLUIDS.md:16-23 • 77f055f  
**Description:** Fit viscous decay E(t) = E₀ exp(-2 ν k² t) and verify |ν_fit - ν_th| / ν_th ≤ 5% at baseline grid ≥ 256²  
**Linked canon:** equations → TODO: add anchor (see derivation/fluid_dynamics/fluids_limit.md), constants → TODO: add anchor (see BENCHMARKS_FLUIDS.md)  
**Exit criteria:** Viscosity fit within 5% tolerance; refinement shows order-consistent error decrease  
**Owner (if present):** — • **Status:** In progress

---

### <a id="task-lid-cavity"></a>Lid-Driven Cavity Benchmark

**Source:** derivation/fluid_dynamics/BENCHMARKS_FLUIDS.md:25-32 • 77f055f  
**Description:** Monitor divergence norm and verify max_t ‖∇·v‖₂ ≤ 1e-6 (double precision)  
**Linked canon:** equations → TODO: add anchor (see derivation/fluid_dynamics/fluids_limit.md)  
**Exit criteria:** Divergence below threshold; centerline profiles converge with grid  
**Owner (if present):** — • **Status:** In progress

---

### <a id="task-walkers-noninterference"></a>Void-Walker Non-Interference Test

**Source:** derivation/fluid_dynamics/BENCHMARKS_FLUIDS.md:91-96 • 77f055f  
**Description:** Ensure read-only walker usage does not alter flow fields; verify max |Δu| = 0 and |Δv| = 0 at end of matched runs  
**Linked canon:** algorithms → TODO: add anchor (see derivation/code/physics/fluid_dynamics/telemetry/walkers.py)  
**Exit criteria:** Zero field difference between runs with/without walkers  
**Owner (if present):** — • **Status:** In progress

---

## Mid-Term Milestones

## <a id="ms-dark-photon-portal"></a>Dark Photon Portal Program (Decoherence Portals)

**Status:** Planned • **Priority:** P2  
**Source:** derivation/dark_photons/PROPOSAL_Decoherence_Portals.md; derivation/dark_photons/Observable-Signatures-of-Void-Dynamics-via-Dark-Photon-Portals.md  

**Goal (verbatim/condensed from source):** Operationalize dark‑photon (A′) kinetic‑mixing as a VDM portal with acceptance‑gated analyses: detector noise budget, Fisher sensitivity for ε, and EFT scale ladder tied to VDM partitions and causal sourcing.

**Acceptance criteria (links only, no formulas):**

- Data products: Noise‑budget SNR vs integration plots and JSON/CSV sidecars; Fisher quick‑estimate JSON for σ(ε); EFT ladder figure  
- Validation gates: annotated regime split (quantum‑ vs thermal‑limited), finite‑difference Fisher cross‑check consistency

**Dependencies:** Units and EFT normalization; background cosmology partition discipline  
**Risks/Constraints:**

- Feeble mixing requires careful treatment of systematics; astrophysical production stories must respect small‑source late‑time bounds

**Deliverables:**

- derivation/dark_photons/PROPOSAL_Decoherence_Portals.md  
- derivation/dark_photons/Observable-Signatures-of-Void-Dynamics-via-Dark-Photon-Portals.md  
- derivation/dark_photons/Noise_Budget.md, fisher_example.csv, noise_budget.csv (schemas)  
- Tagged artifacts: `derivation/code/outputs/{logs,figures}/dark_photons/*` (upon execution)

**Target timeframe (if stated):** To be scheduled after FRW and A6 baselines

## <a id="ms-eft-validation"></a>EFT/KG Branch Validation (Quarantined)

**Status:** Planned • **Priority:** P3  
**Source:** derivation/VDM_Overview.md:48 • 77f055f; derivation/foundations/continuum_stack.md:38 • 77f055f; OPEN_QUESTIONS.md#oq-002 • 77f055f

**Goal (verbatim/condensed from source):** Establish quantitative criteria for when second-order EFT branch becomes necessary; validate tachyonic condensation mechanism and finite-tube mode analysis. Currently quarantined as [PLAUSIBLE]/[FUTURE WORK] pending complete discrete action derivation.

**Acceptance criteria (links only, no formulas):**

- Equations referenced: `EQUATIONS.md#vdm-e-010` (EFT/KG quarantined)
- Data products to produce: TODO: add anchor (see derivation/tachyon_condensation/)
- Units/normalization context: `UNITS_NORMALIZATION.md#eft-normalization`

**Dependencies:** #ms-axiomatic-foundation (complete discrete action with second-order time dynamics)  
**Risks/Constraints:**

- Quantitative criteria for EFT branch necessity undefined
- Scale separation analysis required
- Fast transient characterization needed

**Deliverables:**

- derivation/effective_field_theory/effective_field_theory_approach.md
- derivation/effective_field_theory/kinetic_term_derivation.md
- derivation/tachyon_condensation/finite_tube_mode_analysis.md

**Target timeframe (if stated):** Future work; retained for research purposes

---

### <a id="task-eft-criteria"></a>EFT Branch Necessity Criteria

**Source:** OPEN_QUESTIONS.md#oq-002:68-89 • 77f055f  
**Description:** Define quantitative criteria for boundary between RD (canonical) and EFT/KG (quarantined) branches  
**Linked canon:** equations → `EQUATIONS.md#vdm-e-008`, `EQUATIONS.md#vdm-e-010`, symbols → `SYMBOLS.md#sym-c`  
**Exit criteria:** Quantitative criteria established; scale separation analysis complete  
**Owner (if present):** — • **Status:** Open

---

### <a id="task-tachyon-condensation"></a>Tachyon Condensation Analysis

**Source:** derivation/tachyon_condensation/DELETE_AFTER_SOLVING/TODO_tachyonic_condensation.md:1-466 • 77f055f  
**Description:** Analyze finite-tube solutions, mode spectra, and radius selection mechanism via Bessel matching  
**Linked canon:** equations → TODO: add anchor (see derivation/tachyon_condensation/finite_tube_mode_analysis.md), constants → TODO: add anchor (see CONSTANTS.md)  
**Exit criteria:** κ>0 tachyonic branches identified; energy landscape E(R) mapped; radius selection mechanism established  
**Owner (if present):** — • **Status:** Planned

---

## <a id="ms-qfum-invariant"></a>Q_FUM Logistic Invariant Validation

**Status:** Done • **Priority:** P2  
**Source:** derivation/conservation_law/discrete_conservation.md • 77f055f; agent-onboarding/VDM_Overview_20250826.md:35 • 77f055f

**Goal (verbatim/condensed from source):** Validate logarithmic first integral Q(W,t) = ln(W/(r - u W)) - r t for autonomous on-site logistic ODE numerically

**Acceptance criteria (links only, no formulas):**

- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-qfum-drift-abs` (ΔQ ≤ 10⁻⁸)
- Equations referenced: TODO: add anchor (see derivation/conservation_law/discrete_conservation.md)
- Data products to produce: `DATA_PRODUCTS.md#data-qfum-validation`

**Dependencies:** #ms-rd-validation  
**Risks/Constraints:** Convergence must be consistent with time-stepper's order  

**Deliverables:**

- derivation/conservation_law/discrete_conservation.md
- derivation/code/physics/conservation_law/qfum_validate.py

**Target timeframe (if stated):** ✓ Completed - numerically proven

---

## <a id="ms-agency-field"></a>Agency Field Framework

**Status:** In progress • **Priority:** P2  
**Source:** derivation/AGENCY_FIELD.md:1-158 • 77f055f; OPEN_QUESTIONS.md#oq-018, #oq-019 • 77f055f

**Goal (verbatim/condensed from source):** Develop agency field metric operational proxies; establish scientific significance of agency "smoke tests"

**Acceptance criteria (links only, no formulas):**

- Equations referenced: TODO: add anchor (see derivation/AGENCY_FIELD.md)
- Data products to produce: TODO: add anchor (see derivation/agency_field/)

**Dependencies:** #ms-rd-validation  
**Risks/Constraints:**

- Operational proxies for agency field metrics undefined
- Scientific significance of "smoke tests" needs rigorous validation

**Deliverables:**

- derivation/AGENCY_FIELD.md
- derivation/agency_field/ (scripts and figures)

**Target timeframe (if stated):** In progress

---

## Long-Term / Research Threads

## <a id="ms-quantum-gravity-bridge"></a>Quantum Gravity Bridge (Observational Thread)

**Status:** Planned • **Priority:** P3  
**Source:** derivation/speculations/Bridging-Quantum-Gravity-and-Astrophysical-Observations.md  

**Goal (verbatim/condensed from source):** Leverage public astrophysical and HEP datasets (Planck, DES, LHC/NA64, etc.) to confront VDM’s gravitational and portal predictions; aim to connect quantum‑scale narratives to GR‑scale observables without new experimental builds.

**Acceptance criteria (links only, no formulas):**

- Data products: Comparative goodness‑of‑fit metrics (χ², residual analyses) across cosmology and particle datasets; reproducible pipelines  
- Algorithms/Tools: CLASS/CAMB integration for FRW perturbations; ROOT/likelihood scaffolds for exclusions

**Dependencies:** EFT/KG quarantined thread; FRW/units normalization  
**Risks/Constraints:**

- Cross‑domain systematics and prior choices can dominate; requires disciplined partition mapping and small‑source consistency

**Deliverables:**

- derivation/speculations/Bridging-Quantum-Gravity-and-Astrophysical-Observations.md  
- Forthcoming proposal(s) to scope concrete dataset tests and gate thresholds

**Target timeframe (if stated):** Future work; follow‑on after dark‑photon portal scoping

## <a id="ms-utoe-framework"></a>UTOE Framework Development

**Status:** Planned • **Priority:** P3  
**Source:** derivation/axiomatic_theory_development.md:1-75 • 77f055f

**Goal (verbatim/condensed from source):** Develop Unified Theory of Everything (UTOE) claim: every observed regime appears as exact identity, corollary, or regime theorem of RD axioms with explicitly stated conditions. No external EFT, no training, no extra postulates.

**Acceptance criteria (links only, no formulas):**

- Equations referenced: `EQUATIONS.md#vdm-e-008` (RD canonical foundation)
- BC/IC/Geometry referenced: `BC_IC_GEOMETRY.md` (domain specifications)

**Dependencies:** #ms-axiomatic-foundation, #ms-rd-validation, #ms-eft-validation  
**Risks/Constraints:**

- Extremely ambitious scope
- Requires bridging to multiple physical regimes
- Parameter determination method from first principles needed

**Deliverables:**

- derivation/axiomatic_theory_development.md (comprehensive theory document)

**Target timeframe (if stated):** Long-term research program

---

### <a id="task-cosmological-applications"></a>Cosmological Applications

**Source:** derivation/axiomatic_theory_development.md:192-197 • 77f055f; OPEN_QUESTIONS.md#oq-025 • 77f055f  
**Description:** Establish connection to void dynamics in cosmological contexts; analyze FRW metric coupling; study dark matter and dark energy implications  
**Linked canon:** equations → TODO: add anchor (see derivation/supporting_work/), constants → TODO: add anchor (see CONSTANTS.md)  
**Exit criteria:** Complete cosmological framework with observational connections; observational tests defined  
**Owner (if present):** — • **Status:** Planned

---

### <a id="task-quantum-renormalization"></a>Quantum Renormalization Program

**Source:** OPEN_QUESTIONS.md#oq-024:234-244 • 77f055f  
**Description:** Complete quantum renormalization program for discrete lattice structure  
**Linked canon:** equations → TODO: add anchor (see derivation/foundations/discrete_to_continuum.md)  
**Exit criteria:** Renormalization group analysis complete; UV/IR behavior characterized  
**Owner (if present):** — • **Status:** Open

---

### <a id="task-lattice-scale"></a>Lattice Scale Parameter Determination

**Source:** OPEN_QUESTIONS.md#oq-027:256-267 • 77f055f  
**Description:** Determine lattice scale parameter from first principles (currently 20 orders of magnitude uncertainty)  
**Linked canon:** constants → `CONSTANTS.md#const-a`, units → `UNITS_NORMALIZATION.md#lattice-units`  
**Exit criteria:** Lattice scale determined from physical principles; uncertainty reduced  
**Owner (if present):** — • **Status:** Open

---

## <a id="ms-discrete-action-recast"></a>Discrete Action Recast

**Status:** Open • **Priority:** P2  
**Source:** OPEN_QUESTIONS.md#oq-014:93-117 • 77f055f; derivation/foundations/void_dynamics_theory.md:20 • 77f055f

**Goal (verbatim/condensed from source):** Recast discrete model into discrete action and take to continuum via variational limit so that ∂_t² term appears from first principles rather than assumption

**Acceptance criteria (links only, no formulas):**

- Equations referenced: `EQUATIONS.md#vdm-e-001` (discrete action)
- Validation metrics: TODO: add anchor (see derivation/foundations/void_dynamics_theory.md)

**Dependencies:** #ms-axiomatic-foundation  
**Risks/Constraints:**

- Requires sophisticated field theory machinery
- Connection to Lagrangian formalism must be rigorous

**Deliverables:**

- Updated derivation/foundations/void_dynamics_theory.md with complete discrete action derivation

**Target timeframe (if stated):** Mid-term research goal

---

## <a id="ms-kinetic-normalization"></a>Kinetic Normalization from Discrete Action

**Status:** Open • **Priority:** P2  
**Source:** OPEN_QUESTIONS.md#oq-015:119-142 • 77f055f

**Goal (verbatim/condensed from source):** Derive kinetic normalization c² = κ a² with κ = 2J per-edge from discrete action via continuum limit

**Acceptance criteria (links only, no formulas):**

- Equations referenced: `EQUATIONS.md#vdm-e-002` (kinetic term)
- Constants referenced: `CONSTANTS.md#const-J`, `CONSTANTS.md#const-c-lat`

**Dependencies:** #ms-discrete-action-recast  
**Risks/Constraints:**

- Requires completion of discrete action formulation
- Must reconcile with existing RD normalization

**Deliverables:**

- derivation/effective_field_theory/kinetic_term_derivation.md (updated with rigorous derivation)

**Target timeframe (if stated):** Follows #ms-discrete-action-recast

---

## <a id="ms-conserved-quantity"></a>True Conserved Quantity Discovery

**Status:** Open • **Priority:** P2  
**Source:** OPEN_QUESTIONS.md#oq-011:177-184 • 77f055f

**Goal (verbatim/condensed from source):** Discover true conserved quantity of FUM beyond trivial energy/momentum conservation

**Acceptance criteria (links only, no formulas):**

- Equations referenced: `EQUATIONS.md#vdm-e-020` (energy conservation)
- Validation metrics: TODO: add anchor (see derivation/foundations/symmetry_analysis.md)

**Dependencies:** #ms-axiomatic-foundation, #ms-discrete-action-recast  
**Risks/Constraints:**

- May require identification of new symmetries
- Connection to Noether's theorem needs exploration

**Deliverables:**

- Updated derivation/foundations/symmetry_analysis.md with new conserved quantities

**Target timeframe (if stated):** Long-term research

---

### <a id="task-noether-analysis"></a>Symmetry Analysis via Noether's Theorem

**Source:** OPEN_QUESTIONS.md#oq-012:186-196 • 77f055f  
**Description:** Apply Noether's theorem systematically to identify all continuous symmetries and corresponding conserved currents  
**Linked canon:** equations → `EQUATIONS.md#vdm-e-020`, algorithms → TODO: add anchor (see derivation/foundations/symmetry_analysis.md)  
**Exit criteria:** Complete catalog of symmetries and conserved quantities; connection to physical observables established  
**Owner (if present):** — • **Status:** Open

---

### <a id="task-info-theoretic-conservation"></a>Information-Theoretic Conserved Quantity

**Source:** OPEN_QUESTIONS.md#oq-013:198-207 • 77f055f  
**Description:** Investigate information-theoretic conserved quantity potentially underlying FUM dynamics  
**Linked canon:** equations → TODO: add anchor (see derivation/foundations/)  
**Exit criteria:** Information-theoretic quantity identified and proven conserved; connection to entropy established  
**Owner (if present):** — • **Status:** Open

---

## Engineering/Infra Tasks that Impact Theory

## <a id="ms-gdsp-wiring"></a>GDSP Runtime Wiring

**Status:** Planned • **Priority:** P1  
**Source:** PLANNED.md:40-79 • 77f055f

**Goal (verbatim/condensed from source):** Wire existing walker→bus→metrics→arbiter→GDSP path so structural edits actually fire, with emergent budgets (no static knobs), keeping everything sparse

**Acceptance criteria (links only, no formulas):**

- Algorithms referenced: TODO: add anchor (see fum_rt/core/neuroplasticity/gdsp.py)
- Data products to produce: TODO: add anchor (see fum_rt/runtime/)
- Validation metrics: Firing path tag→actuation latency ≤ 2 ticks

**Dependencies:** Existing infrastructure (bus, metrics, scoreboard)  
**Risks/Constraints:**

- Structural ops already exist; task is wiring them through arbiter
- Budget gate must enforce: edges_touched ≤ budget_prune + 2·budget_bridge + budget_grow
- Safety rails: abort if class min-degree floors/E-I checks would breach

**Deliverables:**

- fum_rt/core/proprioception/events.py (add TagEvent)
- fum_rt/core/neuroplasticity/gdsp.py (expose tick wrapper)
- fum_rt/core/substrate/growth_arbiter.py (derive budgets; call GDSP)
- fum_rt/runtime/orchestrator.py (bus→metrics→arbiter)

**Target timeframe (if stated):** Next sprint/phase

---

### <a id="task-tag-event"></a>Add TagEvent to Event Schema

**Source:** PLANNED.md:50-51 • 77f055f  
**Description:** Add TagEvent(kind="tag.*", …) to existing event types; fold into incremental reducers (EWMA/CMS/UF) for scoreboard  
**Linked canon:** schemas → `SCHEMAS.md` (events schema)  
**Exit criteria:** TagEvent integrated; scoreboard operational  
**Owner (if present):** — • **Status:** Planned

---

### <a id="task-gdsp-tick"></a>GDSP Tick Interface

**Source:** PLANNED.md:52 • 77f055f  
**Description:** Expose tick(scoreboard, budgets, territory) that calls existing sparse edit routines (prune/grow/bridge/cull) under budgets  
**Linked canon:** algorithms → TODO: add anchor (see fum_rt/core/neuroplasticity/gdsp.py)  
**Exit criteria:** GDSP tick callable; sparse operations working under budget constraints  
**Owner (if present):** — • **Status:** Planned

---

### <a id="task-emergent-budgets"></a>Emergent Budget Computation

**Source:** PLANNED.md:53 • 77f055f  
**Description:** Compute emergent budgets per territory from void-debt/SIE, fragmentation (UF components), backlog EWMA  
**Linked canon:** algorithms → TODO: add anchor (see fum_rt/core/substrate/growth_arbiter.py)  
**Exit criteria:** Budgets computed from signals; no static knobs; env knobs debug-only  
**Owner (if present):** — • **Status:** Planned

---

## <a id="ms-heterogeneous-computing"></a>Heterogeneous Computing Implementation

**Status:** Planned • **Priority:** P2  
**Source:** plans/reports/AI-Report-rewriter-2025-08-25 (2).md:60-91 • 77f055f

**Goal (verbatim/condensed from source):** Establish system where distinct neuron classes are managed and allocated to hardware best suited for their computational profile (MI100 for integrators, 7900 XTX for messengers)

**Acceptance criteria (links only, no formulas):**

- Data products to produce: TODO: add anchor (see fum_rt/core/connectome.py neuron type vectors)

**Dependencies:** None (infrastructure work)  
**Risks/Constraints:**

- Requires GPU-native frameworks (ROCm/HIP for AMD)
- Partition kernels must operate on type-specific subsets
- GrowthArbiter must handle class-specific growth commands

**Deliverables:**

- fum_rt/core/connectome.py (neuron_types array)
- fum_rt/core/void_dynamics_adapter.py (type-aware kernels)
- fum_rt/core/fum_growth_arbiter.py (class-specific decisions)

**Target timeframe (if stated):** Next implementation phase

---

### <a id="task-neuron-types"></a>Define Neuron Classes

**Source:** plans/reports/AI-Report-rewriter-2025-08-25 (2).md:68-76 • 77f055f  
**Description:** Define NeuronType enumeration (INTEGRATOR, MESSENGER, etc.) in shared constants module  
**Linked canon:** schemas → `SCHEMAS.md` (if neuron type schema exists)  
**Exit criteria:** Neuron types defined; Connectome augmented with type vector  
**Owner (if present):** — • **Status:** Planned

---

### <a id="task-partition-kernels"></a>Partition GPU Kernels by Neuron Type

**Source:** plans/reports/AI-Report-rewriter-2025-08-25 (2).md:86 • 77f055f  
**Description:** Write GPU kernels to operate on subsets of neuron arrays based on type; partition data for MI100 (integrators) and 7900 XTX (messengers)  
**Linked canon:** algorithms → TODO: add anchor (see fum_rt/core/connectome.py, void_dynamics_adapter.py)  
**Exit criteria:** Type-specific kernels working; correct device allocation  
**Owner (if present):** — • **Status:** Planned

---

## <a id="ms-heterogeneous-plasticity"></a>Heterogeneous Plasticity

**Status:** Planned • **Priority:** P2  
**Source:** plans/reports/AI-Report-rewriter-2025-08-25 (2).md:93-98 • 77f055f

**Goal (verbatim/condensed from source):** Allow different neuron classes to have distinct learning parameters; enable mix of fast-adapting and slow, stable learning to prevent catastrophic forgetting

**Acceptance criteria (links only, no formulas):**

- Algorithms referenced: TODO: add anchor (see fum_rt/core/void_dynamics_adapter.py RE-VGSP)

**Dependencies:** #ms-heterogeneous-computing  
**Risks/Constraints:**

- Messenger neurons: fast-learning "scratchpad"
- Integrator neurons: stable long-term memory
- Computational cost negligible but capability increase massive

**Deliverables:**

- fum_rt/core/void_dynamics_adapter.py (class-specific learning rates)

**Target timeframe (if stated):** Follows heterogeneous computing implementation

---

## <a id="ms-physics-validation-ci"></a>Physics Validation CI Task

**Status:** Planned • **Priority:** P1  
**Source:** agent-onboarding/VDM_Overview_20250826.md:65 • 77f055f

**Goal (verbatim/condensed from source):** Establish and continuously run 'Physics Validation Task' within CI pipeline to ensure automated, ongoing verification of all established physics tests and real-time detection of critical failures like tachyonic roots

**Acceptance criteria (links only, no formulas):**

- Validation metrics: All KPIs in `VALIDATION_METRICS.md` must pass
- Data products: Aggregated validation report

**Dependencies:** #ms-rd-validation, #ms-fluids-sector, #ms-qfum-invariant  
**Risks/Constraints:**

- Must aggregate multiple test suites
- Single failure should fail entire CI run
- Tachyonic root detection requires careful handling

**Deliverables:**

- scripts/run_physics_validations.py (aggregator)
- CI configuration (.github/workflows/)

**Target timeframe (if stated):** Near-term priority for CI integration

---

## Blocked/On-Hold

## <a id="ms-vdm-fluids-corner"></a>VDM-Fluids Corner Testbed

**Status:** Blocked • **Priority:** P2  
**Source:** OPEN_QUESTIONS.md#oq-021:218-227 • 77f055f

**Goal (verbatim/condensed from source):** Implement VDM-fluids corner testbed combining RD + hyperbolic + VDM dynamics for L-bend geometry

**Acceptance criteria (links only, no formulas):**

- Equations referenced: TODO: add anchor (see OPEN_QUESTIONS.md#oq-022)
- Data products to produce: TODO: add anchor (see derivation/code/outputs/vdm_fluids/)

**Dependencies:** #ms-rd-validation, #ms-eft-validation  
**Risks/Constraints:**

- Blocked by: Canonical equations for VDM-fluids undefined (see OQ-022)
- Requires bridging RD, hyperbolic, and VDM formulations

**Deliverables:**

- VDM corner testbed implementation

**Target timeframe (if stated):** Blocked until canonical equations defined

---

## <a id="ms-walker-extension-attention"></a>Extend Walkers to Attention Graphs

**Status:** Blocked • **Priority:** P3  
**Source:** OPEN_QUESTIONS.md#oq-010:167-175 • 77f055f

**Goal (verbatim/condensed from source):** Extend walkers to attention graphs with token-head-position addressing

**Acceptance criteria (links only, no formulas):**

- Algorithms referenced: TODO: add anchor (see derivation/code/obs/walker_glow.py)

**Dependencies:** Walker infrastructure, attention graph formalism  
**Risks/Constraints:**

- Blocked by: Attention graph formalism undefined
- Requires bridging to transformer architecture concepts

**Deliverables:**

- Attention-aware walker implementation

**Target timeframe (if stated):** Future work

---

## <a id="ms-memory-steering-bridges"></a>Memory-Steering System Integration

**Status:** Blocked • **Priority:** P2  
**Source:** OPEN_QUESTIONS.md#oq-005:228-248 • 77f055f

**Goal (verbatim/condensed from source):** Bridge memory-steering into host systems (LBM, RD, walkers); implement acceptance harness

**Acceptance criteria (links only, no formulas):**

- Data products to produce: `DATA_PRODUCTS.md#data-memory-steering-acceptance`
- Validation metrics: `VALIDATION_METRICS.md` (memory steering section)

**Dependencies:** #ms-memory-steering, #ms-rd-validation, #ms-fluids-sector  
**Risks/Constraints:**

- Blocked by: Memory-steering acceptance harness pending completion
- Integration points with LBM/RD/walkers need definition

**Deliverables:**

- Integrated memory-steering in multiple host systems
- Cross-system validation suite

**Target timeframe (if stated):** Follows memory-steering acceptance verification

---

<!-- BEGIN AUTOSECTION: ROADMAP-INDEX -->
<!-- Tool-maintained list of [Milestone](#ms-...) and [Task](#task-...) anchors -->

### Milestone Index

- [Axiomatic Foundation Development](#ms-axiomatic-foundation)
- [RD Canonical Validation](#ms-rd-validation)
- [Memory Steering Mechanism](#ms-memory-steering)
- [LBM Fluids Sector Validation](#ms-fluids-sector)
- [EFT/KG Branch Validation (Quarantined)](#ms-eft-validation)
- [Q_FUM Logistic Invariant Validation](#ms-qfum-invariant)
- [Agency Field Framework](#ms-agency-field)
- [UTOE Framework Development](#ms-utoe-framework)
- [Discrete Action Recast](#ms-discrete-action-recast)
- [Kinetic Normalization from Discrete Action](#ms-kinetic-normalization)
- [True Conserved Quantity Discovery](#ms-conserved-quantity)
- [GDSP Runtime Wiring](#ms-gdsp-wiring)
- [Heterogeneous Computing Implementation](#ms-heterogeneous-computing)
- [Heterogeneous Plasticity](#ms-heterogeneous-plasticity)
- [Physics Validation CI Task](#ms-physics-validation-ci)
- [VDM-Fluids Corner Testbed](#ms-vdm-fluids-corner)
- [Extend Walkers to Attention Graphs](#ms-walker-extension-attention)
- [Memory-Steering System Integration](#ms-memory-steering-bridges)
- [FRW Continuity Residual Validation (Gravity)](#ms-frw-balance)
- [Dark Photon Portal Program (Decoherence Portals)](#ms-dark-photon-portal)
- [Quantum Gravity Bridge (Observational Thread)](#ms-quantum-gravity-bridge)

### Task Index

- [Discrete Action Formulation](#task-discrete-action)
- [Spatial Interaction Derivation](#task-spatial-interaction)
- [Rigorous Continuum Mapping](#task-continuum-mapping)
- [Potential Function Analysis](#task-potential-analysis)
- [Symmetry Analysis and Conservation Laws](#task-symmetry-analysis)
- [Fisher-KPP Front Speed Validation](#task-front-speed)
- [Linear Dispersion Validation](#task-dispersion)
- [Memory Steering Acceptance Tests](#task-mem-acceptance)
- [Taylor-Green Vortex Benchmark](#task-taylor-green)
- [Lid-Driven Cavity Benchmark](#task-lid-cavity)
- [Void-Walker Non-Interference Test](#task-walkers-noninterference)
- [EFT Branch Necessity Criteria](#task-eft-criteria)
- [Tachyon Condensation Analysis](#task-tachyon-condensation)
- [Cosmological Applications](#task-cosmological-applications)
- [Quantum Renormalization Program](#task-quantum-renormalization)
- [Lattice Scale Parameter Determination](#task-lattice-scale)
- [Symmetry Analysis via Noether's Theorem](#task-noether-analysis)
- [Information-Theoretic Conserved Quantity](#task-info-theoretic-conservation)
- [Add TagEvent to Event Schema](#task-tag-event)
- [GDSP Tick Interface](#task-gdsp-tick)
- [Emergent Budget Computation](#task-emergent-budgets)
- [Define Neuron Classes](#task-neuron-types)
- [Partition GPU Kernels by Neuron Type](#task-partition-kernels)

<!-- END AUTOSECTION: ROADMAP-INDEX -->

## Proposals Index

Central list of active proposals with links to their source documents. See each proposal for scope, acceptance gates, and artifact tags.

- Collapse Physics: [PROPOSAL_A6_Collapse_v1.md](collapse/PROPOSAL_A6_Collapse_v1.md)
- Cosmology (FRW Balance): [PROPOSAL_FRW_Balance_v1.md](cosmology/PROPOSAL_FRW_Balance_v1.md)
- Metriplectic (RD + KG): [PROPOSAL_KG_plus_RD_Metriplectic.md](metriplectic/PROPOSAL_KG_plus_RD_Metriplectic.md)
- Metriplectic Variant (Symplectic + DG): [PROPOSAL_Metriplectic_SymplecticPlusDG.md](metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md)
- Conservation vs Balance (RD): [PROPOSAL_RD_Discrete_Conservation_vs_Balance.md](conservation_law/PROPOSAL_RD_Discrete_Conservation_vs_Balance.md)
- Dark Photons (Decoherence Portals): [PROPOSAL_Decoherence_Portals.md](dark_photons/PROPOSAL_Decoherence_Portals.md)
- Quantum Gravity Bridge (Observational): [PROPOSAL_Quantum_Gravity_Bridge_v1.md](speculations/PROPOSAL_Quantum_Gravity_Bridge_v1.md)

## Change Log

- 2024-10-04 • Initial roadmap compiled from repository evidence • 77f055f
- 2025-10-06 • Added milestones: FRW Continuity Residual (Gravity), Dark Photon Portal program, Quantum Gravity Bridge; backfilled Proposals Index (A6 Collapse, FRW Balance, Metriplectic variants, RD Conservation, Dark Photons)
