# VDM Nexus TODO Checklist

Hierarchical execution plan for the Nexus desktop program. Phases contain Tasks; Tasks enumerate Steps with checkable items. Each Task concludes with explicit validation requirements referencing canonical anchors. Architecture document located at C:\git\Prometheus_VDM\VDM_Nexus\NEXUS_ARCHITECTURE.md

Begin the task by following the instructions below:

- Set up your environment, install all required packages, and immediately review the available AGENTS.md and ARCHITECTURE STANDARDS documents.

- Once that's been done, review the repository and all the working directories.

- Check items off as you work on them. Issues should be prioritized by impact on usability. Mark items as [DONE], [STARTED], [RETRYING], [DEBUGGING], [NOT STARTED], as you go and document your work under each item as you work.

- You should not remain stagnant on an issue for too long, if you get stuck on an item and it's marked [RETRYING] or [DEBUGGING], put an x# next to it, where # is the number of times you've attempted resolving it, for example [DEBUGGING x2].

- If you hit x3 then move on unless it's blocking anything else or if it would introduce significant technical debt if not addressed immediately. If it is a blocker like that, state this clearly in your response including "BLOCKER PREVENTING FURTHER DEVELOPMENT"

- If tests fail because of any missing packages or installations, you need to install those and try to run the tests again. Same thing if you run into errors for missing packages.

- Mention which items you updated on the checklist in your response, and your ETA or number of sessions until completion of the checklist.


## Phase 0 — Project Bootstrapping

### Task 0.1 — Align repository baseline
- [ ] Step 0.1.1 — Create `physics_nexus/` top-level directory and place [`NEXUS_ARCHITECTURE.md`](VDM_Nexus/NEXUS_ARCHITECTURE.md:1) under version control.
- [ ] Step 0.1.2 — Mirror canonical linting/build configurations (clang-format, CMake presets) from existing runtime packages.
- [ ] Step 0.1.3 — Document repo pointers (`VDM_REPO_ROOT`, approvals DB paths) in CONTRIBUTING notes.

**Validation:**  
- [ ] Diff against origin `main` shows architecture doc added without modifying canonical derivation files.  
- [ ] CI lint job passes with Nexus directory included.

### Task 0.2 — Provision toolchain & environment
- [ ] Step 0.2.1 — Install Qt 6.x, CMake ≥3.23, compiler (Clang/MSVC/GCC matching CI targets) with C++20 support.
- [ ] Step 0.2.2 — Set up Python 3.11 environment with repo `requirements.txt`; enable `poetry`/`pip-tools` lock if applicable.
- [ ] Step 0.2.3 — Configure deterministic environment variables (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`) per canon execution policy.

**Validation:**  
- [ ] Run `cmake -S physics_nexus -B build` succeeds on Linux/macOS/Windows.  
- [ ] `python -m pip check` passes under the project venv and matches seeds requirements.

### Task 0.3 — Wire canon ingestion scaffolding
- [ ] Step 0.3.1 — Add Nexus configuration file referencing anchors in [AXIOMS](../derivation/AXIOMS.md), [EQUATIONS](../derivation/EQUATIONS.md), and [VALIDATION_METRICS](../derivation/VALIDATION_METRICS.md).
- [ ] Step 0.3.2 — Set up repository-relative path resolver for `../derivation/` tree with guard rails against writes.
- [ ] Step 0.3.3 — Draft `CanonSync` CLI skeleton (read-only) for future indexing per standards.

**Validation:**  
- [ ] Static analysis (clang-tidy/flake8) shows zero write operations under `../derivation/`.  
- [ ] Manual run of resolver prints located canon files with correct commit hash metadata.

## Phase 1 — Canon & Policy Alignment

### Task 1.1 — Map canonical sources into Nexus surfaces
- [ ] Step 1.1.1 — Inventory all UI text and ensure every physics reference cites [VDM-AX-A0…A7](../derivation/AXIOMS.md#vdm-ax-a0) and relevant equations ([VDM-E-033](../derivation/EQUATIONS.md#vdm-e-033), [VDM-E-090](../derivation/EQUATIONS.md#vdm-e-090), etc.).
- [ ] Step 1.1.2 — Link KPI displays to the authoritative entries in [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err); remove duplicated thresholds.
- [ ] Step 1.1.3 — Ensure Markdown viewer overlays commit hashes on canon documents for provenance.

**Validation:**  
- [ ] Automated content scan finds zero physics claims without canon anchors.  
- [ ] Sample dashboard screenshot demonstrates hyperlink routing to canon files.

### Task 1.2 — Enforce approvals and quarantine policy
- [ ] Step 1.2.1 — Wrap all approval mutations through `[approve_tag.py](../derivation/code/common/authorization/approve_tag.py)`; no inline SQL.
- [ ] Step 1.2.2 — Apply environment precedence (CLI > env > `.env`) for approval DB discovery.
- [ ] Step 1.2.3 — Pipe unapproved runs through `[io_paths.py](../derivation/code/common/io_paths.py)` quarantine helpers with policy receipts (`engineering_only=true`).

**Validation:**  
- [ ] Demonstrated CLI session shows approval status change with admin password prompt logged.  
- [ ] Engineering smoke run produces artifacts under `failed_runs/` with correct policy JSON.

### Task 1.3 — Surface experiment roadmap context
- [ ] Step 1.3.1 — Ingest Tier ladder status from [`VDM-Progress-Findings.md`](../derivation/VDM-Progress-Findings.md) to tag experiments by maturity (T0–T9).
- [ ] Step 1.3.2 — Map proposed experiments (e.g., quantum gravity bridge, agency field probes, intelligence model substrate) to dashboard cards.
- [ ] Step 1.3.3 — Flag missing RESULTS for approved proposals and display prerequisites (e.g., missing T5 pilots, robustness sweeps).

**Validation:**  
- [ ] Dashboard panel shows accurate counts per Tier with links to proposals/results.  
- [ ] Cross-reference check verifies no approved proposal lacks a roadmap entry in Nexus.

## Phase 2 — Software Architecture Scaffold

### Task 2.1 — Implement Clean Architecture seams
- [ ] Step 2.1.1 — Define ports in `application/ports/` (`IApprovalRepo`, `IRunnerService`, `ISchemaCatalog`, `IArtifactStore`, `IMarkdownReader`).
- [ ] Step 2.1.2 — Create domain models (Experiment, Approval, RunnerSpec, Gate, Artifact, NexusSettings) with serialization tests.
- [ ] Step 2.1.3 — Build infrastructure adapters (SQLite repos, filesystem artifact store, runner service, markdown reader) that operate on derivation resources in place.

**Validation:**  
- [ ] Dependency analysis confirms `presentation → application → ports ← infrastructure` with no back edges.  
- [ ] Unit tests stub each port and prove adapters honour constructor injection.

### Task 2.2 — Configure plugin descriptors and schemas
- [ ] Step 2.2.1 — Author `plugins/physics/{domain}.nexus.json` descriptors referencing runner scripts, schemas, specs.
- [ ] Step 2.2.2 — Register visualization plugins (PNG viewer, VTK preview, report exporter) with configuration schemas.
- [ ] Step 2.2.3 — Provide Nexus-local JSON Schemas for GUI configuration without duplicating physics schemas.

**Validation:**  
- [ ] SchemaCatalog smoke test lists all domains/tags with timestamps matching on-disk specs.  
- [ ] JSON Schema validation passes for all plugin descriptors.

### Task 2.3 — Add experiment taxonomy support
- [ ] Step 2.3.1 — Classify experiments by domain: Reaction–Diffusion, Metriplectic, Thermodynamic Routing, Wave Flux Meter, Tachyonic Tubes, Memory Steering, Agency Field, Quantum Echoes, Quantum Gravity, Intelligence Model.
- [ ] Step 2.3.2 — Encode instrument vs phenomenon metadata (Tiers T2–T6) for filtering.
- [ ] Step 2.3.3 — Prepare hooks for cross-experiment dependencies (e.g., wave meter Phase C requires Phase A/B certification).

**Validation:**  
- [ ] Taxonomy filters return correct experiment sets; manual spot-check vs `VDM-Progress-Findings.md` entries.  
- [ ] Dependency chip UI blocks downstream runs when prerequisite tiers incomplete.

## Phase 3 — Execution & Artifact Flow

### Task 3.1 — Implement run pipeline and telemetry
- [ ] Step 3.1.1 — Integrate `DerivationScanner` with filesystem watchers for live domain/spec changes.
- [ ] Step 3.1.2 — Launch Python runners via `IRunnerService` with deterministic env (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`, optional `VDM_NEXUS=1`).
- [ ] Step 3.1.3 — Stream stdout/stderr and structured telemetry into the UI, tagging seeds and commit hashes.

**Validation:**  
- [ ] Dry-run smoke profile matches baseline logs for `rd_front_speed`, `kg_energy_oscillation`, `kg_rd_metriplectic`, `wave_flux_meter`, `tachyonic_tube`, `memory_steering`.  
- [ ] Approval guard rejects mismatched HMACs with guilty-field messaging surfaced in UI.

### Task 3.2 — Harvest artifacts and generate reports
- [ ] Step 3.2.1 — Enumerate artifacts via `[io_paths.py](../derivation/code/common/io_paths.py)`; compute SHA-256 hashes per PNG/CSV/JSON.
- [ ] Step 3.2.2 — Render KPI cards referencing [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-kg-energy-osc-slope) with pass/fail badges.
- [ ] Step 3.2.3 — Assemble RESULTS bundles complying with `[RESULTS_PAPER_STANDARDS](../derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)` (figures, metrics tables, provenance block).

**Validation:**  
- [ ] Regression test verifies exported bundle includes proposal path, approval receipts, KPI matrix, artifact manifest.  
- [ ] Hash comparison confirms UI metadata equals canonical filesystem outputs.

### Task 3.3 — Domain-specific run support
- [ ] Step 3.3.1 — RD & Thermodynamic: embed wizard to select specs (`rd_front_speed`, `rd_dispersion`, `thermo-routing-v2`, `wave_flux_meter` phases) with boundary condition presets.
- [ ] Step 3.3.2 — Metriplectic: expose toggles for J-only, M-only, and J⊕M compositions with Strang defect metrics (link to [VDM-E-091](../derivation/EQUATIONS.md#vdm-e-091)).
- [ ] Step 3.3.3 — Tachyonic tubes & Quantum Echoes: support multi-seed sweeps and curvature fits referencing proposals (e.g., `PROPOSAL_False-Vacuum...`, `T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md`).
- [ ] Step 3.3.4 — Agency/Intelligence: integrate scenario loaders for energy clamp, inverted-U, options probe, and intelligence substrate prereg (tag `im-substrate-v1`).

**Validation:**  
- [ ] Launch dialogs populate only approved specs and show gating metrics for selection.  
- [ ] Domain-specific runs emit expected JSON schema (e.g., `wave-flux-meter-openports-summary-v1.schema.json`) verified by automated schema validation.

## Phase 4 — UX Implementation

### Task 4.1 — Build dashboard and document viewers
- [ ] Step 4.1.1 — Implement Dashboard panes (Active Experiments, Pending Approvals, KPI summaries, orphan proposals).
- [ ] Step 4.1.2 — Develop Artifact browser with filters by domain, tag, gate status, run timestamp.
- [ ] Step 4.1.3 — Embed Markdown viewer with math rendering, commit banners, anchor navigation.

**Validation:**  
- [ ] UX walkthrough captures each pane showing live data and canon hyperlinks.  
- [ ] Accessibility audit (keyboard navigation, contrast) meets WCAG AA.

### Task 4.2 — Implement viz and telemetry panels
- [ ] Step 4.2.1 — Integrate figure preview (PNG, SVG, MP4) with caption display citing seeds/commits.
- [ ] Step 4.2.2 — Add telemetry timelines for metrics like [Connectome entropy](../derivation/VALIDATION_METRICS.md#kpi-connectome-entropy), [Complexity cycles](../derivation/VALIDATION_METRICS.md#kpi-complexity-cycles), memory steering poles, agency C-score components.
- [ ] Step 4.2.3 — Provide log viewer for CSV/JSON outputs with schema-aware column formatting.
- [ ] Step 4.2.4 — Offer comparison overlays for multi-seed sweeps (e.g., tachyonic spectrum coverage, wave meter absorber efficiency).

**Validation:**  
- [ ] Visualization acceptance tests confirm canonical figures render identically to CLI baseline.  
- [ ] Telemetry charts match CLI metrics within tolerance (no smoothing that hides gate failures).  
- [ ] Sweep comparison view reproduces metrics from historical logs (e.g., `tube_spectrum_summary__<tag>.json`).

### Task 4.3 — Scenario guidance and notebooks
- [ ] Step 4.3.1 — Provide guided workflows for prereg experiments (e.g., Wave Flux Meter Phase C, Quantum Echo T4) with inline reference to proposal sections.
- [ ] Step 4.3.2 — Embed links to example notebooks or scripts (e.g., `simulate_inverted_u.py`, `run_vdm_causal_order.py`) for reproducibility.
- [ ] Step 4.3.3 — Display ablation/null test recommendations where proposals require them (agency field probes, false-vacuum asymmetry).

**Validation:**  
- [ ] Guided workflow triggers enumerated tasks with completion tracking.  
- [ ] Notebook launchers open sample runs with correct environment settings.  
- [ ] Ablation advisories match proposals’ “Next steps” sections.

## Phase 5 — Validation, QA, and Security

### Task 5.1 — Automated testing & quality gates
- [ ] Step 5.1.1 — Add unit tests for ports/adapters, integration tests for approval/run/report pipeline.
- [ ] Step 5.1.2 — Configure snapshot tests for UI panes using Qt test harness.
- [ ] Step 5.1.3 — Implement end-to-end smoke scenario (approve → run → harvest → export) with golden artifacts across representative domains (RD, Metriplectic, Wave Meter, Tachyonic, Agency).
- [ ] Step 5.1.4 — Validate schema compliance for all summary JSONs (`KG-energy-osc-v1`, `thermo-routing-v2`, `wave-flux-meter-openports-summary-v1`, `tube-spectrum-summary-v1`, `vdm-triad-v1`).

**Validation:**  
- [ ] Test suite passes on Linux/macOS/Windows with coverage ≥80% on `physics_nexus/`.  
- [ ] Golden-run comparison detects drift in KPI values beyond thresholds; diff reviewers escalate failures.  
- [ ] Schema validation report shows 0 violations across sample artifacts.

### Task 5.2 — Security & compliance review
- [ ] Step 5.2.1 — Conduct dependency audit (pip/Qt) and document CVE monitoring.
- [ ] Step 5.2.2 — Verify password handling: approvals CLI prompts, no secrets stored in config.
- [ ] Step 5.2.3 — Run static analysis (clang-tidy, cppcheck, bandit) with zero high/critical findings.
- [ ] Step 5.2.4 — Pen-test GUI command execution guarding (no arbitrary CLI injection) and sandbox runner environment variables.

**Validation:**  
- [ ] Security report filed with dependency list, CVE status, mitigations.  
- [ ] Static analysis artifacts archived and referenced in release checklist.  
- [ ] Pen-test logs demonstrate sanitized command arguments for runner invocation.

### Task 5.3 — Scientific QA integrations
- [ ] Step 5.3.1 — Add automatic gate verification against [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md) thresholds per domain before marking runs PASS.
- [ ] Step 5.3.2 — Integrate dataset-level regression checks (e.g., two-grid slope ≥ 2.90 for metriplectic, R² ≥ 0.999 for KG energy oscillation).
- [ ] Step 5.3.3 — Provide optional rerun triggers for robustness sweeps (T7) and out-of-sample tests (agency/information probes).

**Validation:**  
- [ ] QA pipeline flags metrics outside tolerances, blocking promotion to higher tiers.  
- [ ] Robustness sweep runner logs show aggregated metrics with gating decisions.

## Phase 6 — Deployment & Operations

### Task 6.1 — Release packaging
- [ ] Step 6.1.1 — Configure CPack/binary packaging for target platforms; include runtime dependencies (Qt libs).
- [ ] Step 6.1.2 — Generate signed artifacts (GPG/Authenticode) with provenance metadata (commit, build timestamp, builder ID).
- [ ] Step 6.1.3 — Publish release notes referencing KPI outcomes and approvals state.

**Validation:**  
- [ ] Install test on each platform verifies Nexus launches and locates derivation tree via environment vars.  
- [ ] Signature verification succeeds; SBOM generated and archived.  
- [ ] Release notes cite major experiment support additions (e.g., Wave Flux Meter Phase C, Intelligence Substrate) with links.

### Task 6.2 — Monitoring, incident response, and rollback
- [ ] Step 6.2.1 — Document telemetry endpoints (local logs, optional Prometheus) and retention policies.
- [ ] Step 6.2.2 — Define incident response flow for gate failures (quarantine, CONTRADICTION_REPORT) per Section 9 of [`NEXUS_ARCHITECTURE.md`](VDM_Nexus/NEXUS_ARCHITECTURE.md:103).
- [ ] Step 6.2.3 — Prepare rollback procedure restoring previous Nexus version and canonical config.
- [ ] Step 6.2.4 — Establish audit trail exports for regulatory review (experiment history, approvals, KPI results).

**Validation:**  
- [ ] Tabletop exercise demonstrates incident response plan including quarantine artifact routing.  
- [ ] Rollback rehearsal reinstalls prior build and reconnects to derivation without data loss.  
- [ ] Audit export verifies completeness across domains and tiers.

## Phase 7 — Physics Program Enablement

### Task 7.1 — Reaction–Diffusion & Thermodynamic Routing
- [ ] Step 7.1.1 — Provide parameter templates for front speed, dispersion, and thermo-routing v2 specs with dimensionless groups displayed.
- [ ] Step 7.1.2 — Expose RJ-fit diagnostics, no-switch invariants, bias metrics, and outflux floor gates per prereg (see `thermo-routing-v2-prereg-biased-main`.
- [ ] Step 7.1.3 — Automate Phase C wave flux meter checks (absorber efficiency, power balance, symmetry nulls).

**Validation:**  
- [ ] Example run shows RJ fit R² ≥ 0.99 and gate matrix display consistent with logs.  
- [ ] Phase C summary JSON validated against schema and displayed live.

### Task 7.2 — Metriplectic & Quantum Echoes
- [ ] Step 7.2.1 — Support J-only energy oscillation instrument certification (ΔE ~ Δt²) with log–log fit overlays.
- [ ] Step 7.2.2 — Implement controls for KG⊕RD composition (Strang splitting, degeneracy diagnostics).  
- [ ] Step 7.2.3 — Integrate quantum echo proposals (e.g., `T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md`) with echo envelopes, reversibility metrics, and entanglement proxies.

**Validation:**  
- [ ] Metriplectic run displays two-grid slope ≥ 2.90, defect/residual metrics within gates.  
- [ ] Quantum echo visualization overlays converge per proposal thresholds.

### Task 7.3 — Tachyonic, Wavefront, and Cosmology
- [ ] Step 7.3.1 — Provide spectrum coverage heatmap viewer, curvature fit dashboards, and condensation finite fraction metrics (tags `tube-spectrum-v1`, `tube-condensation-v1`).
- [ ] Step 7.3.2 — Surface FRW continuity RMS residuals and ΛCDM residuals for cosmology harness.
- [ ] Step 7.3.3 — Offer pipeline for false-vacuum metastability tests and void-debt asymmetry metrics per prereg.

**Validation:**  
- [ ] Tachyonic summary display matches coverage_phys ≥ 0.95 and curvature_ok boolean.  
- [ ] Cosmology panel shows RMS ≤1e-6 for dust scenario and reports contradiction when threshold breached.

### Task 7.4 — Agency Field & Intelligence Model
- [ ] Step 7.4.1 — Implement dashboards for agency probes (energy clamp, inverted-U, options, C-score) referencing defaults in session summary.
- [ ] Step 7.4.2 — Integrate intelligence model substrate prereg (im-substrate-v1): spec validation, approvals gating, scenario execution (probe-limit semantics).
- [ ] Step 7.4.3 — Provide ablation toggles (null experiments, randomization) suggested for agency robustness.

**Validation:**  
- [ ] Agency metrics display matches canonical defaults and compute z-scores from reference distributions.  
- [ ] Intelligence substrate run outputs required PNG+CSV+JSON with determinism receipts; gating ensures probe-limit compliance.

### Task 7.5 — Quantum Gravity & Causality
- [ ] Step 7.5.1 — Enable causal DAG audits (event DAG, Myrheim-Meyer stats, Alexandrov intervals) with UI to inspect partial orders.
- [ ] Step 7.5.2 — Hook quantum gravity bridge runners (`run_vdm_causal_order.py`, `run_vdm_myrheim_dimension.py`, `run_vdm_bd_action_proxy.py`) with gating thresholds from proposal.
- [ ] Step 7.5.3 — Provide parameter sweeps for holonomy diagnostics and causal geometry metrics.

**Validation:**  
- [ ] DAG audit viewer shows pass/fail flags per gate; schema-compliant artifacts stored.  
- [ ] Quantum gravity runs report dimension estimates and action proxies within proposal tolerance.

---
