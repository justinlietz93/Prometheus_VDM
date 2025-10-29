# TODO

**IMPORTANT!** READ THIS ENTIRE HEADER.

Hierarchical execution plan for the Nexus desktop program. Phases contain Tasks; Tasks enumerate Steps with checkable items. Each Task concludes with explicit validation requirements referencing canonical anchors.

Begin the task by following the instructions below:

- [DONE] **Set up your environment**, install all required packages, and immediately review the required documentation if necessary and perform your agent memory updates.
  - Created a Python virtual environment, installed dependencies from `requirements.txt`, and reviewed `docs/ARCHITECTURE.md` plus `VDM_Nexus/NEXUS_ARCHITECTURE.md` for current standards.

- [DONE] Once that's been done, **review the repository** and all the working directories.
  - Surveyed repository root layout (Derivation/, VDM_Nexus/, docs/, tools/, etc.) to understand current assets and pending Nexus GUI scope.

- [STARTED] **Check items off as you work on them**. Issues should be prioritized by impact on usability. Mark item CHECKBOX as [DONE], [STARTED], [RETRYING], [DEBUGGING], [NOT STARTED], as you go and document your work under each item as you work.
  - Tracking this directive by updating checklist entries as progress continues; initial housekeeping items updated accordingly.

- [NOT STARTED] **You should not remain stagnant on an issue for too long**, if you get stuck on an item and it's marked [RETRYING] or [DEBUGGING], put an x# next to it, where # is the number of times you've attempted resolving it, for example [DEBUGGING x2].

- [NOT STARTED] **If you hit x3 then move on** unless it's blocking anything else or if it would introduce significant technical debt if not addressed immediately. If it is a blocker like that, state this clearly in your response including "BLOCKER PREVENTING FURTHER DEVELOPMENT"

- [NOT STARTED] I**f tests fail** because of any missing packages or installations, **you need to install those and try to run the tests again.** Same thing if you run into errors for missing packages.

- [STARTED] **Mention which items you updated** on the checklist in your response, and your ETA or number of sessions until completion of the checklist.
  - Logging this response plan to ensure reporting includes checklist deltas and session estimates.

## HIGH PRIORITY

**Date:** October 5, 2025 at 2:32 AM CDT

---

### Preamble

Each step is sequentially ordered by priority, ensuring a structured flow from proving the **metriplectic agency** to scaling and testing it across **complex systems**. This takes into account the full roadmap, from the **T7 Robustness validation** to **agency field integration** and beyond.

#### Key Definitions

- **CEG:** **Counterfactual Echo Gain** - Metric measuring the ability of the system to improve the accuracy of an echo based on model awareness of its own internal rules.
- **SMAE:** **Self-Model-Assisted Echo** - The methodology of testing the ability of a system to leverage its own self-model for improving echo precision.
- **T7 Robustness:** Test of the consistency, reproducibility, and generalization of the **CEG** across a range of environments, perturbations, and conditions.

#### Notes on Precedence

- This checklist follows the priority progression laid out by the **NotebookLM** analysis and your **existing framework**. Each proposal builds upon previous validated elements, ensuring **disciplined integration** into VDM's full architecture. The roadmap carefully separates exploration and calibration (D-Tier) from core validation (T1–T4).

**Run Preflight Metriplectic Split Certification** (before any main task)

- **J‑only limb**: Time‑reversal check (Δt, -Δt), Noether drift ≤ ( 1e^{-8} )
- **M‑only limb**: H‑theorem check (ΔΣ ≤ 0)
- **A4 degeneracies**: Test skew symmetry (J) and PSD (M) for random vectors (≤ ( 1e^{-12} ))
- **Strang composition**: Verify Strang defect slope within expected range (p ∈ [2.8, 3.2])

#### **Reproducibility & Robustness (Ongoing)**

- **Artifacts ledger:** Every figure, figure data (CSV), and model configuration (commit hash) will be available on GitHub or Zenodo for external verification
- **Ablations:** Conduct and **publish failure modes** for any run that does not pass the preflight gates or fails to show positive CEG, per the testing specification
- **Versioning:** Ensure all code is versioned properly for audit by other researchers or teams

---

## **Tier 1: Immediate Action - Validating Metriplectic Core (T4)**

-[] **Execute CEG Test (Counterfactual Echo Gain)**

    -[] Test if internal J/M knowledge improves echo fidelity: **CEG > 0** (under strict gates)
    -[] Ensure **conservation drift** is within bounds (J) and **entropy monotonicity** is enforced (M)
    3. **Test Strang‑Defect Composition (J–M–J)**

    -[] Check and confirm **composition quality** via Strang defect and JMJ residuals
    -[] Ensure Strang defect slope ≈ 3, with an R² ≥ 0.9999

-[] **Formalize Dirac Transition (J to fermions)**

    -[] Implement lattice QFT techniques for the **J‑limb** → Dirac fermions
    -[] Test **gauge covariance** (≤ 1e‑12) and **dispersion error** (≤ 3%)
    -[] Confirm correct Fermionic behavior in lattice (staggered/Wilson fermions)

-[] **Formalize Dissipative Limb as Lindblad Channel (M)**

    -[] Implement **Lindblad-compatible channel** for M (entropy engine)
    -[] Verify **complete positivity and trace preservation** (CP/TP ≤ 1e‑12)
    -[] Ensure **entropy monotonicity** (ΔS ≥ -1e‑10)

---

## **Tier 2: High Priority - Operationalizing VDM Phenomena (T4)**

-[] **Test False-Vacuum Metastability and Void-Debt Asymmetry**

    -[] Model the **pre‑Big Bang void field** by testing **vacuum metastability** and **asymmetry production**
    -[] Confirm nucleation scaling (radius ( R_c )) and net charge production (( \Delta Q_B > 0 ))

-[] **Test Thermodynamic Routing v2 (Self-Organization)**

    -[] Test if **self‑organization occurs via thermodynamic descent** (no‑switch control)
    -[] Confirm **H‑theorem** violations = 0 and significant routing bias (95% CI excludes 0)

-[] **SIE Invariant Validation**

    -[] Certify core invariant **Q** for the **Self-Improvement Engine (SIE)**
    -[] Ensure drift threshold for **SIE invariant** is ≤ ( 1e^{-6} ) to confirm computational efficiency

---

## **Tier 3: Medium Priority - Foundational Calibration and Integration (T4)**

-[] **Test Agency Field via Curvature Scaling (C(x,t))**

    -[] Measure **path curvature scaling** with transverse memory gradient
    -[] Confirm linear relationship of curvature and memory gradient scaling with **( X = \Theta|\nabla_\perp m| )**

-[] **Wave Flux Meter Certification**

    -[] Complete **Wave Flux Meter** validation for J-limb’s wave-routing capabilities
    -[] Test **controlled routing** via a frozen channel map and verified energy balance

---

## **Tier 4: Low Priority - Calibration and Simulation Enhancements (T3)**

-[] **Calibration of Psychophysical Observables to C Field**

    -[] Establish calibration link between **C Field** and **psychophysical observables**
    -[] Ensure predictive validity for higher rungs of agency testing (T6+)

-[] **Tachyonic Tube Condensation**

    -[] Test **tachyonic tube condensation** at a specific radius ( R_\star ) under varying parameters
    -[] Confirm the **core instability mechanism** for the tube condensation process

-[] **Causal DAG Audits for Void Dynamics**

    -[] Complete **geometry‑agnostic checks** on **locality** and **causality** using event precedence for acyclicity
    -[] Estimate **emergent dimension ( \hat{d} )** from network behavior

---

## **Tier 5: Exploratory / D-Tier (Post‑T7)**

-[] **Dark Photon Portal Signatures**

    -[] Conduct **quantum‑to‑classical shift experiments** based on existing **dark photon portal** model
    -[] Validate specific observable signatures from **energy exchange patterns** and **phase shifts**

-[] **Quantum Gravity Bridge: Causal Geometry and Holonomy**

    -[] Explore potential **quantum‑gravity bridge** and investigate **causal geometry holonomy** as an extension of agency dynamics

---

## **Next Milestones (Post-T7)**

-[] **Finalizing Agency Field Model (T8/T9)**

    -[] Expand **minimal agency field** to **multi‑task** models that generalize across varying task types and domains
    -[] Validate transfer learning via **SMAE** across unseen environments (test persistence, robustness)

-[] **Completing Full System Integration**

    -[] Integrate **agency field components** into real-world applications with full external validation (T9)
    -[] Develop **real‑time feedback mechanisms** for modeling **self‑aware behavior** in complex domains

---

## ON HOLD

**Date:** October 5, 2025 at 2:32 AM CDT

---

- [ ] Kill/delete the dense branch in the connectome step, or move it to a separate validation tool.
- [ ] Add `VDM-E-` anchors for the learning/structural deltas in `ALGORITHMS.md`.
- [ ] Link the learning/structural deltas to their canonical equation IDs in `ALGORITHMS.md`.
- [ ] Promote actual formulas for P (e.g., MI-rate or (R^2)), (I_{\text{net}}) (transfer-entropy/synergy proxy), U (already defined), V (empowerment estimator), B (ensemble-gain × anti-redundancy), and Shannon entropy into `SYMBOLS.md`/`EQUATIONS.md`.
- [ ] Add explicit pass/fail monotonicity/elasticity thresholds (e.g., finite-difference gradients (G_E\ge0,\ G_p\le0) except at boundaries) as KPIs to `VALIDATION_METRICS.md` for the options probe.
- [ ] Add minimal E-vs-slip feasibility curves as KPIs to `VALIDATION_METRICS.md` for the options probe.
- [ ] Wire the options probe KPIs to CI.
- [ ] Add minimal code hooks for walker BCs/ICs to enable experiments to toggle absorbing vs reflecting and re-run thresholds.
- [ ] Refactor connectome step to sparse adjacency structure (reuse `SparseConnectome`) and profile tick latency (Owner: Core Runtime, Effort: L)
- [ ] Implement GDSP telemetry and regression tests covering enable/disable flows, and log exceptions/trip STRICT gate on GDSP actuator failures (when `VOID_STRICT=1`) (Owner: Runtime Loop, Effort: M)
- [ ] Consolidate void dynamics and domain modulation into `vdm_rt/fum_advanced_math/void_dynamics/` and update derivation imports (Owner: Advanced Math, Effort: M)
- [ ] Consolidate memory steering implementations into `vdm_rt/physics/memory_steering/memory_steering.py` and update derivation imports (Owner: Physics Team, Effort: M)
- [ ] Wire centralized RNG/seed plumbing across runtime, including void dynamics adapter, structural plasticity, and emergent text generator (Owner: Core Runtime, Advanced Math, Effort: M)
- [ ] Audit environment flags for scouts, document in README, and add validation for mutually exclusive toggles (Owner: Runtime Loop, Effort: M)
- [ ] Implement downsampled tiles or a WebGL/tiled backend for the frontend visualizer (Owner: Viz Team, Effort: L)
- [ ] Add optional token authentication and logging to the in-process HTTP server (Owner: Runtime Ops, Effort: S)
- [ ] Add `NO_DENSE_CONNECTOME=1` environment gate to assert if dense path allocates beyond threshold

### Additional Action Items (not explicitly in Top-10, Merge Candidates, or One-week Plan)

- [ ] Integrate `vdm_rt/fum_advanced_math/graph/coarse_grain_graph.py` into `core` or drop it
- [ ] Remove `vdm_rt.io.sensors.*` stub files
- [ ] Remove `vdm_rt.io.actuators.*` stub files
- [ ] Remove `vdm_rt/io/__init__.py` (empty file)
- [ ] Add logging for connectome/bus linkage state mutation in `vdm_rt/runtime/loop/main.py` (Owner: Runtime Loop)
- [ ] Optimize `nx.from_numpy_array` on dense mask in `vdm_rt/core/connectome.py` to avoid materializing full adjacency for large graphs
- [ ] Add CLI flag parallel to `ENABLE_GDSP` environment variable
- [ ] Consolidate defaults for `use_time_dynamics` flag to prevent desynchronization between CLI and UI
- [ ] Add CLI/documentation mapping for Redis output `ENABLE_REDIS_*` environment variables
- [ ] Add failure logging for Redis outputs
- [ ] Remove dense fallback usage in `connectome`
- [ ] Verify downstream consumption for event metrics (`_evt_metrics`)
- [ ] Add a counter for skipped visualization renders in `vdm_rt/runtime/helpers/viz.py`
- [ ] Write tests for gate hysteresis (speak/B1)
- [ ] Write tests for locality guard / adjacency budget
- [ ] Write tests for ADC updates & announcements
- [ ] Cache graph layout offline or precompute positions per run to avoid O(N³) `nx.spring_layout` in `vdm_rt/core/visualizer.py`
- [ ] Move synchronous plotting in `vdm_rt/runtime/helpers/viz.py` to an async/offline worker to prevent tick stalls
- [ ] Emit warning when filesystem errors are swallowed during directory scanning for checkpoints in `vdm_rt/run_nexus.py`
- [ ] Wrap file writes in `vdm_rt/core/visualizer.py` with logger error to surface disk/permission issues

## Key Highlights

- Kill or delete the dense branch in the connectome step, or move it to a separate validation tool.
- Add `VDM-E-` anchors for the learning/structural deltas and link them to their canonical equation IDs in `ALGORITHMS.md`.
- Promote actual formulas for P, I_net, U, V, B, and Shannon entropy into `SYMBOLS.md`/`EQUATIONS.md`.
- Add explicit pass/fail monotonicity/elasticity thresholds (e.g., finite-difference gradients) as KPIs to `VALIDATION_METRICS.md` for the options probe.
- Add minimal E-vs-slip feasibility curves as KPIs to `VALIDATION_METRICS.md` for the options probe, and wire these KPIs to CI.
- Add minimal code hooks for walker BCs/ICs to enable experiments to toggle absorbing vs reflecting and re-run thresholds.

## Next Steps & Suggestions

- Prioritize the refactoring and optimization of core algorithmic components, specifically addressing the dense branch in the connectome step and implementing flexible walker boundary/initial conditions.
- Standardize and formalize algorithmic documentation by adding explicit anchors, linking equations, and promoting canonical formulas for key metrics in `ALGORITHMS.md`, `SYMBOLS.md`, and `EQUATIONS.md`.
- Develop and integrate robust validation metrics and KPIs for critical system components, such as the options probe, by defining clear pass/fail thresholds and feasibility curves, and wiring these to continuous integration (CI).
