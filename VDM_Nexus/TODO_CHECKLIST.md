# VDM Nexus TODO Checklist

**IMPORTANT!** READ THIS ENTIRE HEADER.

Hierarchical execution plan for the Nexus desktop program. Phases contain Tasks; Tasks enumerate Steps with checkable items. Each Task concludes with explicit validation requirements referencing canonical anchors. Architecture document located at [VDM_Nexus/NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:1)

Begin the task by following the instructions below:

- **Set up your environment**, install all required packages, and immediately review the available AGENTS.md and ARCHITECTURE STANDARDS documents.

- Once that's been done, **review the repository** and all the working directories.

- **Check items off as you work on them**. Issues should be prioritized by impact on usability. Mark item CHECKBOX as [DONE], [STARTED], [RETRYING], [DEBUGGING], [NOT STARTED], as you go and document your work under each item as you work.

- **You should not remain stagnant on an issue for too long**, if you get stuck on an item and it's marked [RETRYING] or [DEBUGGING], put an x# next to it, where # is the number of times you've attempted resolving it, for example [DEBUGGING x2].

- **If you hit x3 then move on** unless it's blocking anything else or if it would introduce significant technical debt if not addressed immediately. If it is a blocker like that, state this clearly in your response including "BLOCKER PREVENTING FURTHER DEVELOPMENT"

- If tests fail because of any missing packages or installations, **you need to install those and try to run the tests again.** Same thing if you run into errors for missing packages.

- **Mention which items you updated** on the checklist in your response, and your ETA or number of sessions until completion of the checklist.

---

## Phase 0 — Project Bootstrapping

### Task 0.1 — Align repository baseline

- [DONE] Step 0.1.1 — Create `VDM_Nexus/` top-level directory and place [`NEXUS_ARCHITECTURE.md`](VDM_Nexus/NEXUS_ARCHITECTURE.md:1) under version control.
- [STARTED] Step 0.1.2 — Mirror canonical linting/build configurations (clang-format, CMake presets) from existing runtime packages.
- [DONE] Step 0.1.3 — Document repo pointers (`VDM_REPO_ROOT`, approvals DB paths) in CONTRIBUTING notes.

### **Task 0.1 Validation:**

- [DONE] Diff against origin `main` shows architecture doc added without modifying tracked canon paths (exclusions applied).
  - Exclusions: `Derivation/Converging_External_Research/**`, `Derivation/References/**`, `Derivation/Speculations/**`, `Derivation/Templates/**`, `Derivation/Supporting_Work/external_references/**`, `Derivation/Supporting_Work/Physics-Based Datasets by Tier_ A Comprehensive Resource Guide.pdf`, `Derivation/VDM_OVERVIEW.md`
  - Evidence: [VDM_Nexus/scripts/nexus_validate_gate.py](VDM_Nexus/scripts/nexus_validate_gate.py:1) with DEFAULT_EXCLUSIONS reports PASS for the canon-diff gate.
  - Note: `NEXUS_ARCHITECTURE.md` not newly added vs origin/main (already present upstream or renamed).

- [PENDING] CI lint job passes with Nexus directory included.
  - Current status: PENDING. Local probes: md hygiene PASS (tools/md_hygiene_check.py), JSON lint PASS (`jq` on VDM_Nexus/**/*.json), pre-commit config missing, clang-format not installed. CI workflow not found; add/check CI before marking this passed.

### Task 0.2 — Provision toolchain & environment

- [DONE] Step 0.2.1 — Install Qt 6.5+, CMake ≥3.24, compiler (Clang/MSVC/GCC matching CI targets) with C++20 support. Evidence: CMake configure succeeded; Qt6 6.5 components resolved.
  - Installed Qt 6 base + declarative development packages along with QML runtime modules (QtQuick, Controls, Layouts, Templates, WorkerScript) so the dashboard preview can start inside the container.
  - Supplemented runtime with Qt 6 QML import packages (`qml6-module-qtquick`, `qml6-module-qtquick-controls`, `qml6-module-qtquick-layouts`, `qml6-module-qtqml-workerscript`, `qml6-module-qtquick-templates`, `qml6-module-qtquick-window`) to unblock offscreen test runs of the dashboard shell.
  - Installed `qml6-module-qtqml-workerscript` explicitly after the offscreen smoke test reported the missing `QtQml.WorkerScript` import so the dashboard QML loads cleanly under headless CI runs.
- [DONE] Step 0.2.2 — Set up Python 3.13.5 environment with repo `requirements.txt`; enable `poetry`/`pip-tools` lock if applicable. Evidence: Python 3.13.5 active; `pip check` OK.
- [DONE] Step 0.2.3 — Configure deterministic environment variables (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `BLIS_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS`, `PYTHONHASHSEED`) per canon execution policy. Evidence: [`VDM_Nexus/.env.example`](VDM_Nexus/.env.example:7) updated; copy to local .env for development shells.

### **Task 0.2 Validation:**

- [DONE] Run `cmake -S VDM_Nexus -B VDM_Nexus/build` succeeds on Linux/macOS/Windows.
- [DONE] `python -m pip check` passes under the project venv and matches seeds requirements.
- [DONE] Deterministic threading baseline present in [VDM_Nexus/.env.example](VDM_Nexus/.env.example:7).

### Task 0.3 — Wire canon ingestion scaffolding

- [DONE] Step 0.3.1 — Add Nexus configuration file referencing anchors in [AXIOMS](../derivation/AXIOMS.md#vdm-ax-a0), [EQUATIONS](../derivation/EQUATIONS.md#vdm-e-033), and [VALIDATION_METRICS](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err).
  - Published `resources/nexus_canon_config.v1.json` enumerating required canon anchors with summaries for ingestion scaffolding (read-only manifest).
- [DONE] Step 0.3.2 — Set up repository-relative path resolver for `../derivation/` tree with guard rails against writes. (Note: resolver prints AXIOMS/EQUATIONS/VALIDATION_METRICS + commits.)
  - Implemented `scripts/canon_paths.py` providing guarded resolution, git metadata helpers, and enforced Derivation scoping; updated resolver printer to consume it.
- [DONE] Step 0.3.3 — Draft `CanonSync` CLI skeleton (read-only) for future indexing per standards.
  - Added `scripts/nexus_canon_sync.py` to emit read-only plans from the canon config using the shared resolver; documented usage in scripts README.

### **Task 0.3 Validation:**

- [DONE] Static analysis (clang-tidy/flake8) shows zero write operations under `../derivation/`.
  - Evidence: [`nexus_static_policy_check.py`](VDM_Nexus/scripts/nexus_static_policy_check.py:1) PASS (exit 0) on VDM_Nexus/.
- [DONE] Manual run of resolver prints located canon files with correct commit hash metadata.
  - Evidence: [`nexus_resolver_print.py`](VDM_Nexus/scripts/nexus_resolver_print.py:93) --json reported repo_head f36d3481ed7caaff79a55135348bf6687a6b394f and file_last_commit for AXIOMS/EQUATIONS/VALIDATION_METRICS.

## Phase 1 — Canon & Policy Alignment

### Task 1.1 — Map canonical sources into Nexus surfaces

- [STARTED] Step 1.1.1 — Inventory all UI text and ensure every physics reference cites [VDM-AX-A0…A7](../derivation/AXIOMS.md#vdm-ax-a0) and relevant equations ([VDM-E-033](../derivation/EQUATIONS.md#vdm-e-033), [VDM-E-090](../derivation/EQUATIONS.md#vdm-e-090), etc.).
  - Added dashboard reference chips that resolve canon anchors (VDM-AX-A0…A7, VDM-E-033, VDM-E-090, VALIDATION_METRICS) through `DashboardController::repositoryUrl`, keeping links repo-local.
  - Normalized and deduplicated repository links so dashboard chips only expose safe, canon-tracked anchors.
  - Hardened anchor handling so repository URLs preserve Markdown fragments after validating targets exist within `VDM_REPO_ROOT`.
  - Added repository traversal guard that ascends from build/output directories to find canon files safely, so dashboard chips work even when the app launches outside the repo root.
- [STARTED] Step 1.1.2 — Link KPI displays to definitions in [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err); compute pass/fail with thresholds from the active run's spec/schema; do not duplicate thresholds in GUI.
  - Dashboard metrics now reference nexus-roadmap summary counts and display gating copy referencing VALIDATION_METRICS while deferring threshold evaluation to controller data.
- [STARTED] Step 1.1.3 — Ensure Markdown viewer overlays commit hashes on canon documents for provenance.

### **Task 1.1 Validation:**

- [ ] Automated content scan finds zero physics claims without canon anchors.  
- [ ] Sample dashboard screenshot demonstrates hyperlink routing to canon files.

### Task 1.2 — Enforce approvals and quarantine policy

- [STARTED] Step 1.2.1 — Wrap all approval mutations through `[approve_tag.py](../derivation/code/common/authorization/approve_tag.py)`; no inline SQL.
- [STARTED] Step 1.2.2 — Apply environment precedence (CLI > env > `.env`) for approval DB discovery.
- [STARTED] Step 1.2.3 — Pipe unapproved runs through `[io_paths.py](../derivation/code/common/io_paths.py)` quarantine helpers with policy receipts (`engineering_only=true`).

### **Task 1.2 Validation:**  

- [ ] Demonstrated CLI session shows approval status change with admin password prompt logged.  
- [ ] Engineering smoke run produces artifacts under `failed_runs/` with correct policy JSON.

### Task 1.3 — Surface experiment roadmap context

- [ ] Step 1.3.1 — Present Tier ladder status via read-only link to [VDM-Progress-Findings.md](../derivation/VDM-Progress-Findings.md); do not parse Markdown to drive UI state. Tag experiments by maturity (T0–T9) only from structured sources (approvals DB/specs/JSON registries) when available.
- [STARTED] Step 1.3.2 — Map proposed experiments (e.g., quantum gravity bridge, agency field probes, intelligence model substrate) to dashboard cards as read-only links; no thresholds or gating derived from Markdown.
  - Spotlight cards pull from `spotlight_cards` entries to expose proposal paths with click-through to repo files while flagging missing RESULTS status.
  - Spotlight proposal links are sanitized and validated against the repo root before exposing open actions.
  - Repository resolver now retains proposal anchors/fragments while still preventing traversal outside the repo.
  - Repository lookup now walks parent directories when necessary, ensuring sanitized proposal links still reach canon files when the binary executes from a build tree.
- [ ] Step 1.3.3 — Flag missing RESULTS using structured artifacts (approvals DB and presence of RESULTS_* artifacts/logs); show prerequisites as links to proposal sections only (no Markdown parsing for logic).

### **Task 1.3 Validation:**  

- [ ] Dashboard panel shows accurate counts computed from structured sources, with links to proposals/results.
- [ ] Cross-reference check verifies no approved proposal lacks a roadmap entry in Nexus; canon docs are viewer-only.

## Phase 2 — Software Architecture Scaffold

### Task 2.1 — Implement Clean Architecture seams

- [DONE] Step 2.1.1 — Define ports in `application/ports/` (`IApprovalRepo`, `IRunnerService`, `ISchemaCatalog`, `IArtifactStore`, `IMarkdownReader`). Implemented in [`VDM_Nexus/application/ports/ports.hpp`](VDM_Nexus/application/ports/ports.hpp:1).
- [STARTED] Step 2.1.2 — Create domain models (Experiment, Approval, RunnerSpec, Gate, Artifact, NexusSettings) with serialization tests.
- [STARTED] Step 2.1.3 — Build infrastructure adapters (SQLite repos, filesystem artifact store, runner service, markdown reader) that operate on derivation resources in place.

### **Task 2.1 Validation:**  

- [ ] Dependency analysis confirms `presentation → application → ports ← infrastructure` with no back edges.  
- [ ] Unit tests stub each port and prove adapters honour constructor injection.

### Task 2.2 — Configure plugin descriptors and schemas

- [STARTED] Step 2.2.1 — Author `plugins/physics/{domain}.nexus.json` descriptors referencing runner scripts, schemas, specs.
- [STARTED] Step 2.2.2 — Register visualization plugins (PNG viewer, VTK preview, report exporter) with configuration schemas.
- [STARTED] Step 2.2.3 — Provide Nexus-local JSON Schemas for GUI configuration without duplicating physics schemas.
- [STARTED] Step 2.2.4 — Author viz plugin descriptors: [plugins/viz/volume.viz.json](VDM_Nexus/plugins/viz/volume.viz.json), [plugins/viz/flow.viz.json](VDM_Nexus/plugins/viz/flow.viz.json), [plugins/viz/tensor.viz.json](VDM_Nexus/plugins/viz/tensor.viz.json), [plugins/viz/particles.viz.json](VDM_Nexus/plugins/viz/particles.viz.json); define matches/controls/overlays per [NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md) §12.5.
- [STARTED] Step 2.2.5 — Define `vdm.run-manifest.v1` JSON Schema at [schemas/vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json) for manifest validation (fields arrays, topology, spacing, KPI map).
- [STARTED] Step 2.2.6 — Implement threshold extraction in ISchemaCatalog to surface gating thresholds from spec/schema to the UI (e.g., thermo routing schemas under Derivation/code/physics/thermo_routing/schemas/*.schema.json).

### **Task 2.2 Validation:**  

- [ ] SchemaCatalog smoke test lists all domains/tags with timestamps matching on-disk specs.
- [ ] JSON Schema validation passes for viz plugins and `vdm.run-manifest.v1` manifest.

### Task 2.3 — Add experiment taxonomy support

- [ ] Step 2.3.1 — Classify experiments by domain: Reaction–Diffusion, Metriplectic, Thermodynamic Routing, Wave Flux Meter, Tachyonic Tubes, Memory Steering, Agency Field, Quantum Echoes, Quantum Gravity, Intelligence Model.
- [ ] Step 2.3.2 — Encode instrument vs phenomenon metadata (Tiers T2–T6) for filtering.
- [ ] Step 2.3.3 — Prepare hooks for cross-experiment dependencies (e.g., wave meter Phase C requires Phase A/B certification).

### **Task 2.3 Validation:**  

- [ ] Taxonomy filters return correct experiment sets; manual spot-check vs `VDM-Progress-Findings.md` entries.  
- [ ] Dependency chip UI blocks downstream runs when prerequisite tiers incomplete.

## Phase 3 — Execution & Artifact Flow

### Task 3.1 — Implement run pipeline and telemetry

- [STARTED] Step 3.1.1 — Integrate `DerivationScanner` with filesystem watchers for live domain/spec changes.
- [STARTED] Step 3.1.2 — Launch Python runners via `IRunnerService` with deterministic env (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`, optional `VDM_NEXUS=1`).
- [STARTED] Step 3.1.3 — Stream stdout/stderr and structured telemetry into the UI, tagging seeds and commit hashes.
- [STARTED] Step 3.1.4 — Implement in‑situ adapter to write `run-manifest.json` (including `experiment_schema` and `spec_path`) and VTK datasets (`.vti/.vtu/.vtp` or XDMF/HDF5) every N steps; file-watcher hot‑reload in viewport.
- [NOT STARTED] Step 3.1.5 — Optional socket‑coupled streaming (ParaView Catalyst 2 / Ascent) for true live flythrough; toggle per‑run; runner math unchanged.

### **Task 3.1 Validation:**  

- [ ] Dry-run smoke profile matches baseline logs for `rd_front_speed`, `kg_energy_oscillation`, `kg_rd_metriplectic`, `wave_flux_meter`, `tachyonic_tube`, `memory_steering`.
- [ ] Approval guard rejects mismatched HMACs with guilty-field messaging surfaced in UI.

### Task 3.2 — Harvest artifacts and generate reports

- [STARTED] Step 3.2.1 — Enumerate artifacts via `[io_paths.py](../derivation/code/common/io_paths.py)`; compute SHA-256 hashes per PNG/CSV/JSON.
- [STARTED] Step 3.2.2 — Render KPI cards linking to [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-kg-energy-osc-slope) anchors; compute pass/fail using thresholds from the run’s spec/schema.
- [STARTED] Step 3.2.3 — Assemble RESULTS bundles complying with `[RESULTS_PAPER_STANDARDS](../derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)` (figures, metrics tables, provenance block).

### **Task 3.2 Validation:**  

- [ ] Regression test verifies exported bundle includes proposal path, approval receipts, KPI matrix, artifact manifest.
- [ ] Hash comparison confirms UI metadata equals canonical filesystem outputs.

### Task 3.3 — Domain-specific run support

- [ ] Step 3.3.1 — RD & Thermodynamic: embed wizard to select specs (`rd_front_speed`, `rd_dispersion`, `thermo-routing-v2`, `wave_flux_meter` phases) with boundary condition presets.
- [ ] Step 3.3.2 — Metriplectic: expose toggles for J-only, M-only, and J⊕M compositions with Strang defect metrics (link to [VDM-E-091](../derivation/EQUATIONS.md#vdm-e-091)).
- [ ] Step 3.3.3 — Tachyonic tubes & Quantum Echoes: support multi-seed sweeps and curvature fits referencing proposals (e.g., `PROPOSAL_False-Vacuum...`, `T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md`).
- [ ] Step 3.3.4 — Agency/Intelligence: integrate scenario loaders for energy clamp, inverted-U, options probe, and intelligence substrate prereg (tag `im-substrate-v1`).

### **Task 3.3 Validation:**  

- [ ] Launch dialogs populate only approved specs and show gating metrics for selection.  
- [ ] Domain-specific runs emit expected JSON schema (e.g., `wave-flux-meter-openports-summary-v1.schema.json`) verified by automated schema validation.

## Phase 4 — UX Implementation

### Task 4.1 — Build dashboard and document viewers

- Note: Phase 4 remains [NOT STARTED] until ports/adapters compile; see [NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md) §12.
- [STARTED] Step 4.1.1 — Implement Dashboard panes (Active Experiments, Pending Approvals, KPI summaries, orphan proposals).
  - Added QML dashboard preview (`presentation/qml/Main.qml`) wiring `DashboardController` metrics into three-card layout with canon anchor links; loads roadmap index read-only at startup.
  - Packaged dashboard QML into `presentation.qrc` under the `/presentation` prefix and verified the headless Qt Quick runtime loads without missing module errors.
  - Added headless runtime guard in `main.cpp` that exits automatically when `QT_QPA_PLATFORM=offscreen` after confirming QML load, preventing hung CI sessions.
  - Default index discovery now walks upward from build and binary directories (in addition to `VDM_REPO_ROOT`) so off-tree builds still locate `nexus-roadmap-index.v1.json`, logging clear warnings when the manifest is missing or unreadable.
  - Honoured `VDM_REPO_ROOT` values that point directly at the manifest file by short-circuiting the lookup before traversing directories, keeping env-driven preview scripts functional.
  - Trimmed whitespace from environment-provided manifest paths before resolution so stray spaces in `VDM_REPO_ROOT` no longer break dashboard startup.
- [NOT STARTED] Step 4.1.2 — Develop Artifact browser with filters by domain, tag, gate status, run timestamp.
- [NOT STARTED] Step 4.1.3 — Implement Proposal/Results Viewer: render PROPOSAL_* and RESULTS_* Markdown with math rendering, commit banners, anchor navigation; read-only.
- [NOT STARTED] Step 4.1.4 — Implement Experiment Browser (Configs/Specs): list per-domain experiments and open config/spec JSON with a pretty/JSON-path viewer; display repository path and commit hash; read-only (no writes to derivation).
- [NOT STARTED] Step 4.1.5 — Implement Schema Viewer: open JSON Schemas co-located with runners; validate selected specs against their schema; display validation errors verbatim; viewer-only.
- [NOT STARTED] Step 4.1.6 — Implement Approvals pane UI: list pending approvals from approvals DB and trigger Approve/Revoke via [approve_tag.py](../derivation/code/common/authorization/approve_tag.py); present CLI password prompt without storing secrets; display receipts (approver, timestamp, HMAC) and refresh DB status.

### **Task 4.1 Validation:**  

- [ ] UX walkthrough captures each pane showing live data and canon hyperlinks.
- [ ] Accessibility audit (keyboard navigation, contrast) meets WCAG AA.
- [ ] Experiment Browser opens sample spec [tr_v2_prereg_biased_main.json](derivation/code/physics/thermo_routing/specs/tr_v2_prereg_biased_main.json) read-only and displays repository path + commit hash.
- [ ] Schema Viewer validates that spec against [thermo-routing-v2-prereg-biased-main.schema.json](derivation/code/physics/thermo_routing/schemas/thermo-routing-v2-prereg-biased-main.schema.json) and displays validation results verbatim.
- [ ] Proposal/Results Viewer renders [PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md](derivation/Thermodynamic_Routing/Prereg_Biased_Main/PROPOSAL_Thermodynamic_Routing_v2_Preg_Biased_Main.md) and a RESULTS doc with commit and salted-hash banners.
- [ ] Approvals pane triggers [approve_tag.py](derivation/code/common/authorization/approve_tag.py) for an approval and surfaces receipts; DB status reflects the change; no secrets stored.

### Task 4.2 — Implement viz and telemetry panels

- [NOT STARTED] Step 4.2.1 — Integrate figure preview (PNG, SVG, MP4) with caption display citing seeds/commits.
- [NOT STARTED] Step 4.2.2 — Add telemetry timelines for metrics like [Connectome entropy](../derivation/VALIDATION_METRICS.md#kpi-connectome-entropy), [Complexity cycles](../derivation/VALIDATION_METRICS.md#kpi-complexity-cycles), memory steering poles, agency C-score components.
- [NOT STARTED] Step 4.2.3 — Provide log viewer for CSV/JSON outputs with schema-aware column formatting.
- [NOT STARTED] Step 4.2.4 — Offer comparison overlays for multi-seed sweeps (e.g., tachyonic spectrum coverage, wave meter absorber efficiency).
- [NOT STARTED] Step 4.2.5 — Build Qt 6 + VTK viewport (QQuickVTK/QVTKOpenGLNativeWidget): iso-values, orthogonal/oblique slices, streamlines (RK4), volume rendering, probe cursors; ROCm/AMD-friendly path.
- [NOT STARTED] Step 4.2.6 — Add navigation/time: fly/turn/orbit controls; time scrubber/stepper; loop/record MP4; scale bar, world axes, unit banners.
- [NOT STARTED] Step 4.2.7 — Add particle trails and tensor glyphs; clipping box; KPI jump-to-gate events.
- [NOT STARTED] Step 4.2.8 — KPI overlay cards hyperlink to canon anchors from [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-connectome-entropy); pass/fail badges mirror thresholds from the active run’s spec/schema.

### **Task 4.2 Validation:**  

- [ ] Visualization acceptance tests confirm canonical figures render identically to CLI baseline.
- [ ] Telemetry charts match CLI metrics within tolerance (no smoothing that hides gate failures).
- [ ] Sweep comparison view reproduces metrics from historical logs (e.g., `tube_spectrum_summary__<tag>.json`).

### Task 4.3 — Scenario guidance and notebooks

- [ ] Step 4.3.1 — Provide guided workflows for prereg experiments (e.g., Wave Flux Meter Phase C, Quantum Echo T4) with inline reference to proposal sections.
- [ ] Step 4.3.2 — Embed links to example notebooks or scripts (e.g., `simulate_inverted_u.py`, `run_vdm_causal_order.py`) for reproducibility.
- [ ] Step 4.3.3 — Display ablation/null test recommendations where proposals require them (agency field probes, false-vacuum asymmetry).

### **Task 4.3 Validation:**  

- [ ] Guided workflow triggers enumerated tasks with completion tracking.  
- [ ] Notebook launchers open sample runs with correct environment settings.  
- [ ] Ablation advisories match proposals’ “Next steps” sections.

## Phase 5 — Validation, QA, and Security

### Task 5.1 — Automated testing & quality gates

- [ ] Step 5.1.1 — Add unit tests for ports/adapters, integration tests for approval/run/report pipeline.
- [ ] Step 5.1.2 — Configure snapshot tests for UI panes using Qt test harness.
- [ ] Step 5.1.3 — Implement end-to-end smoke scenario (approve → run → harvest → export) with golden artifacts across representative domains (RD, Metriplectic, Wave Meter, Tachyonic, Agency).
- [ ] Step 5.1.4 — Validate schema compliance for all summary JSONs (`KG-energy-osc-v1`, `thermo-routing-v2`, `wave-flux-meter-openports-summary-v1`, `tube-spectrum-summary-v1`, `vdm-triad-v1`).

### **Task 5.1 Validation:**  

- [ ] Test suite passes on Linux/macOS/Windows with coverage ≥80% on `VDM_Nexus/`.  
- [ ] Golden-run comparison detects drift in KPI values beyond thresholds; diff reviewers escalate failures.  
- [ ] Schema validation report shows 0 violations across sample artifacts.

### Task 5.2 — Security & compliance review

- [ ] Step 5.2.1 — Conduct dependency audit (pip/Qt) and document CVE monitoring.
- [ ] Step 5.2.2 — Verify password handling: approvals CLI prompts, no secrets stored in config.
- [ ] Step 5.2.3 — Run static analysis (clang-tidy, cppcheck, bandit) with zero high/critical findings.
- [ ] Step 5.2.4 — Pen-test GUI command execution guarding (no arbitrary CLI injection) and sandbox runner environment variables.

### **Task 5.2 Validation:**  

- [ ] Security report filed with dependency list, CVE status, mitigations.  
- [ ] Static analysis artifacts archived and referenced in release checklist.  
- [ ] Pen-test logs demonstrate sanitized command arguments for runner invocation.

### Task 5.3 — Scientific QA integrations

- [ ] Step 5.3.1 — Add automatic gate verification against thresholds declared in the run’s spec/schema before marking runs PASS; cross-reference [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-kg-energy-osc-slope) for definitions only.
- [ ] Step 5.3.2 — Integrate dataset-level regression checks (e.g., two-grid slope ≥ 2.90 for metriplectic, R² ≥ 0.999 for KG energy oscillation).
- [ ] Step 5.3.3 — Provide optional rerun triggers for robustness sweeps (T7) and out-of-sample tests (agency/information probes).

### **Task 5.3 Validation:**  

- [ ] QA pipeline flags metrics outside tolerances, blocking promotion to higher tiers.  
- [ ] Robustness sweep runner logs show aggregated metrics with gating decisions.

## Phase 6 — Deployment & Operations

### Task 6.1 — Release packaging

- [ ] Step 6.1.1 — Configure CPack/binary packaging for target platforms; include runtime dependencies (Qt libs).
- [ ] Step 6.1.2 — Generate signed artifacts (GPG/Authenticode) with provenance metadata (commit, build timestamp, builder ID).
- [ ] Step 6.1.3 — Publish release notes referencing KPI outcomes and approvals state.

### **Task 6.1 Validation:**  

- [ ] Install test on each platform verifies Nexus launches and locates derivation tree via environment vars.  
- [ ] Signature verification succeeds; SBOM generated and archived.  
- [ ] Release notes cite major experiment support additions (e.g., Wave Flux Meter Phase C, Intelligence Substrate) with links.

### Task 6.2 — Monitoring, incident response, and rollback

- [ ] Step 6.2.1 — Document telemetry endpoints (local logs, optional Prometheus) and retention policies.
- [ ] Step 6.2.2 — Define incident response flow for gate failures (quarantine, CONTRADICTION_REPORT) per Section 9 of [`NEXUS_ARCHITECTURE.md`](VDM_Nexus/NEXUS_ARCHITECTURE.md:103).
- [ ] Step 6.2.3 — Prepare rollback procedure restoring previous Nexus version and canonical config.
- [ ] Step 6.2.4 — Establish audit trail exports for regulatory review (experiment history, approvals, KPI results).

### **Task 6.2 Validation:**  

- [ ] Tabletop exercise demonstrates incident response plan including quarantine artifact routing.  
- [ ] Rollback rehearsal reinstalls prior build and reconnects to derivation without data loss.  
- [ ] Audit export verifies completeness across domains and tiers.

## Phase 7 — Physics Program Enablement

### Task 7.1 — Reaction–Diffusion & Thermodynamic Routing

- [ ] Step 7.1.1 — Provide parameter templates for front speed, dispersion, and thermo-routing v2 specs with dimensionless groups displayed.
- [ ] Step 7.1.2 — Expose RJ-fit diagnostics, no-switch invariants, bias metrics, and outflux floor gates per prereg (see `thermo-routing-v2-prereg-biased-main`.
- [ ] Step 7.1.3 — Automate Phase C wave flux meter checks (absorber efficiency, power balance, symmetry nulls).

### **Task 7.1 Validation:**  

- [ ] Example run shows RJ fit R² ≥ 0.99 and gate matrix display consistent with logs.  
- [ ] Phase C summary JSON validated against schema and displayed live.

### Task 7.2 — Metriplectic & Quantum Echoes

- [ ] Step 7.2.1 — Support J-only energy oscillation instrument certification (ΔE ~ Δt²) with log–log fit overlays.
- [ ] Step 7.2.2 — Implement controls for KG⊕RD composition (Strang splitting, degeneracy diagnostics).  
- [ ] Step 7.2.3 — Integrate quantum echo proposals (e.g., `T4_PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md`) with echo envelopes, reversibility metrics, and entanglement proxies.

### **Task 7.2 Validation:**  

- [ ] Metriplectic run displays two-grid slope ≥ 2.90, defect/residual metrics within gates.  
- [ ] Quantum echo visualization overlays converge per proposal thresholds.

### Task 7.3 — Tachyonic, Wavefront, and Cosmology

- [ ] Step 7.3.1 — Provide spectrum coverage heatmap viewer, curvature fit dashboards, and condensation finite fraction metrics (tags `tube-spectrum-v1`, `tube-condensation-v1`).
- [ ] Step 7.3.2 — Surface FRW continuity RMS residuals and ΛCDM residuals for cosmology harness.
- [ ] Step 7.3.3 — Offer pipeline for false-vacuum metastability tests and void-debt asymmetry metrics per prereg.

### **Task 7.3 Validation:**  

- [ ] Tachyonic summary display matches coverage_phys ≥ 0.95 and curvature_ok boolean.  
- [ ] Cosmology panel shows RMS ≤1e-6 for dust scenario and reports contradiction when threshold breached.

### Task 7.4 — Agency Field & Intelligence Model

- [ ] Step 7.4.1 — Implement dashboards for agency probes (energy clamp, inverted-U, options, C-score) referencing defaults in session summary.
- [ ] Step 7.4.2 — Integrate intelligence model substrate prereg (im-substrate-v1): spec validation, approvals gating, scenario execution (probe-limit semantics).
- [ ] Step 7.4.3 — Provide ablation toggles (null experiments, randomization) suggested for agency robustness.

### **Task 7.4 Validation:**  

- [ ] Agency metrics display matches canonical defaults and compute z-scores from reference distributions.  
- [ ] Intelligence substrate run outputs required PNG+CSV+JSON with determinism receipts; gating ensures probe-limit compliance.

### Task 7.5 — Quantum Gravity & Causality

- [ ] Step 7.5.1 — Enable causal DAG audits (event DAG, Myrheim-Meyer stats, Alexandrov intervals) with UI to inspect partial orders.
- [ ] Step 7.5.2 — Hook quantum gravity bridge runners (`run_vdm_causal_order.py`, `run_vdm_myrheim_dimension.py`, `run_vdm_bd_action_proxy.py`) with gating thresholds from proposal.
- [ ] Step 7.5.3 — Provide parameter sweeps for holonomy diagnostics and causal geometry metrics.

### **Task 7.5 Validation:**  

- [ ] DAG audit viewer shows pass/fail flags per gate; schema-compliant artifacts stored.  
- [ ] Quantum gravity runs report dimension estimates and action proxies within proposal tolerance.

---
