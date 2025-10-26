You’re right—the Nexus must *plug into* your existing Derivation tree, not try to replace it. Below is a standards doc and scaffold that lock to your real layout (schemas/specs/APPROVALS right next to runners, existing SQLite DBs, and your canon rules). I’ve written this as a formal architecture standard you can drop into `physics_nexus/ARCHITECTURE_STANDARDS.md` and enforce via CI.

---

# VDM Nexus — Architecture Standards (v1)

**Scope.** This document defines how the **physics_nexus** desktop app integrates with the existing **Derivation/** canon and runner stack. It codifies directory structure, boundaries, data flow, quality gates, and approvals so the GUI can launch, monitor, validate, and publish experiments without breaking provenance.

**Alignment with canon.** All claims, data models, and gates must trace to canonical registries and rules already in the repo: **AXIOMS (A0–A7)**, equations, constants, symbols, schemas, and RESULTS/PROPOSAL authoring standards.    

---

## 0) Ground truth we must obey

* **Runner locality:** Every domain under `Derivation/code/physics/{domain}` **must** contain `schemas/`, `specs/`, `APPROVAL.json`, and `README.md`. The Nexus must read these in-place (no copying), and treat them as the single source of truth. 
* **Common helpers:** All runs route figures/logs via `Derivation/code/common/io_paths.py`; approvals are enforced by `Derivation/code/common/authorization`. Nexus must call helpers, not re-implement path or policy logic.  
* **Approval discipline (DB-backed):** A run is allowed only when the tag and script are approved per HMAC policy and the manifest matches the DB; otherwise artifacts are quarantined. The DBs already exist under `Derivation/code/common/data/` (`approval.db`, `approval_admin.db`).  
* **Artifacts & provenance:** Every successful run must emit **≥1 PNG figure**, **≥1 CSV**, **≥1 JSON** with seed + commit, and store them under `Derivation/code/outputs/(figures|logs)/{domain}`. Nexus must surface these, never relocate them.  
* **Physics gates:** Metered gates (e.g., RD dispersion/front, KG cone/Noether, tachyonic tube coverage) and thresholds come from canon. Nexus reports **pass/fail against those JSON fields**; it must not redefine physics criteria.   

---

## 1) Repository layout (integrated with your corrected structure)

```
Project_Name/
├─ Derivation/                         # existing canon (unchanged)
│  ├─ code/physics/{domain}/           # runners + schemas/specs/APPROVAL.json/README.md
│  ├─ code/outputs/figures/{domain}/   # PNGs produced by runs
│  ├─ code/outputs/logs/{domain}/      # CSV/JSON produced by runs
│  └─ code/common/                     # io_paths, authorization, data, plotting, equations
└─ physics_nexus/                      # the desktop application
   ├─ presentation/                    # Qt/QML UI (dark theme)
   │  ├─ qml/
   │  │  ├─ Shell.qml
   │  │  ├─ Dashboard.qml
   │  │  ├─ Experiments.qml
   │  │  ├─ Approvals.qml
   │  │  ├─ ResultsBrowser.qml
   │  │  ├─ VizWorkbench.qml
   │  │  └─ MarkdownViewer.qml
   │  └─ styles/dark/
   │     ├─ Theme.qml
   │     └─ Markdown.css
   ├─ application/                     # use-cases; no Qt imports
   │  ├─ usecases/
   │  │  ├─ ListDomains.cpp/.h
   │  │  ├─ ListPendingApprovals.cpp/.h
   │  │  ├─ ApproveTag.cpp/.h
   │  │  ├─ RunExperiment.cpp/.h
   │  │  ├─ StreamRunTelemetry.cpp/.h
   │  │  ├─ GenerateReport.cpp/.h
   │  │  └─ BrowseArtifacts.cpp/.h
   │  └─ ports/                        # interfaces (Dependency Inversion)
   │     ├─ IApprovalRepo.h
   │     ├─ IResultsRepo.h
   │     ├─ IRunnerService.h
   │     ├─ ISchemaCatalog.h
   │     ├─ IArtifactStore.h
   │     └─ IMarkdownReader.h
   ├─ domain/                          # POD/POJO models only
   │  ├─ Experiment.h                  # id, domain, script, spec, tag
   │  ├─ Proposal.h                    # path, metadata
   │  ├─ Approval.h                    # status, approver, key, schemaRef
   │  ├─ RunnerSpec.h                  # parsed spec (tag-scoped)
   │  ├─ Gate.h                        # name, threshold, pass/fail
   │  ├─ Metric.h                      # k/v + units
   │  ├─ Artifact.h                    # figure/log JSON/CSV paths + hash
   │  └─ NexusSettings.h               # repoRoot, env vars, db locations
   ├─ infrastructure/                  # adapters
   │  ├─ data/
   │  │  ├─ SqliteApprovalRepo.cpp/.h  # reads Derivation/code/common/data/*.db
   │  │  ├─ SqliteResultsRepo.cpp/.h   # optional read-only results index
   │  │  └─ FileArtifactStore.cpp/.h   # zero-copy into Derivation outputs/
   │  ├─ runners/
   │  │  ├─ PythonRunnerService.cpp/.h # launches {script}.py with spec/tag env
   │  │  └─ ProcessMonitor.cpp/.h      # stdout/err → live telemetry
   │  ├─ catalog/
   │  │  ├─ SchemaCatalog.cpp/.h       # reads co-located schemas/specs
   │  │  └─ DerivationScanner.cpp/.h   # scans real tree (no shadow copies)
   │  └─ docs/
   │     └─ MarkdownReader.cpp/.h      # Git-commit aware markdown loader
   ├─ plugins/
   │  ├─ physics/                      # declarative descriptors
   │  │  └─ {domain}.nexus.json
   │  └─ viz/
   │     ├─ plots/Matplotlib.json
   │     ├─ plots/VTK.json
   │     └─ exporter/Report.md.json
   ├─ resources/
   │  ├─ icons/
   │  └─ fonts/
   ├─ schemas/                         # GUI-side JSON Schemas (proposal, approval, results, runner_spec)
   ├─ scripts/                         # seeding & packaging
   ├─ CMakeLists.txt
   └─ tests/                           # mirrors application/, domain/, infrastructure/
```

*The above keeps runners, schemas, specs, and outputs living where they already live: inside `Derivation/code/`.*  

---

## 2) Dependency rule (Clean, modular monolith)

```
presentation → application → ports ← infrastructure
                      ↓
                   domain
```

* No outer→inner imports. Business logic contains **no** Qt, DB, or Python imports. Domain models are plain structs. Repository pattern and constructor injection are mandatory. (This mirrors your Clean Architecture goals and file-size discipline ≤500 LOC/file.) 

**Code-size & tests.** Enforce ≤500 LOC per file; tests mirror source tree and target **ports** and domain behavior first, then adapter integrations. 

---

## 3) Integration with canon data & approvals

**DBs.** Use the existing SQLite DBs under `Derivation/code/common/data/`:

* `approval.db` (public) and `approval_admin.db` (admin password). 

**Approval CLI & policy.** The GUI must *call* the `approve_tag.py` commands (or import the same module) to remain policy-consistent. Approval requires: (a) preregistration; (b) tag in schema; (c) proposal exists; (d) approver matches; (e) script-scoped HMAC matches DB secret. No GUI bypass.  

**Schema & spec co‑location.** Nexus only reads schemas/specs beside the runner. It must never duplicate or cache them in-app (only temporary runtime copies). 

**Artifacts.** Figures/JSON/CSV go to `Derivation/code/outputs/(figures|logs)/{domain}` via `io_paths`. The GUI consumes from there and displays pass/fail flags captured in the JSON.  

---

## 4) Data flow (run-time)

1. **Discover**: `DerivationScanner` reads domains and runner descriptors; `SchemaCatalog` resolves `schemas/` and `specs/` per tag. 
2. **Approve**: `IApprovalRepo` checks DB + manifest; UI shows missing items (proposal path, schema mismatch, HMAC) exactly as the policy emits. 
3. **Launch**: `PythonRunnerService` starts the Python script in `Derivation/code/physics/{domain}`, passing `--spec <spec.json>` and exporting `VDM_APPROVAL_DB`, `VDM_POLICY_*`. (AMD/CPU default; optional ROCm later—never CUDA.) 
4. **Stream**: `ProcessMonitor` tails stdout/err; telemetry events hit the UI.
5. **Harvest**: On completion, Nexus enumerates `io_paths`-routed outputs and ingests JSON metrics; pass/fail is rendered via the KPI gates defined by canon.  
6. **Report**: `GenerateReport` binds artifacts to RESULTS standards and embeds commit/seed/gates for export as PDF/HTML bundles. 

---

## 5) Domain models (GUI side, not physics theory)

* **Experiment**: `{domain, script, tag, specPath, schemaPath, status}`
* **Proposal**: `{path, title, authors, date}` (read-only from Derivation) 
* **Approval**: `{approved, approver, keyKind, lastChecked, manifestPath}` 
* **RunnerSpec**: tag-scoped config blob validated by schema. 
* **Gate**: `{name, threshold, value, pass}` with link to KPI anchor (cone/Noether/H-theorem/etc.). 
* **Artifact**: `{type: figure|csv|json, path, sha256}`; JSON carries canonical fields (e.g., `metrics.passed=true`). 

*Physics-facing content (A0–A7, KG/RD equations, constants, symbols) is referenced, not duplicated, by the GUI.*  

---

## 6) Plugins and descriptors

**Physics plugins** (`plugins/physics/{domain}.nexus.json`) are thin descriptors that tell Nexus where the runner lives and which tags/specs are available, e.g.:

```json
{
  "domain": "reaction_diffusion",
  "scripts": [
    {"name": "rd_dispersion_experiment.py", "tags": ["RD-dispersion-v1"]},
    {"name": "rd_front_speed_experiment.py", "tags": ["RD-front-v1"]}
  ],
  "schemaDir": "../../Derivation/code/physics/reaction_diffusion/schemas",
  "specDir":   "../../Derivation/code/physics/reaction_diffusion/specs"
}
```

This descriptor is *not* a source of truth; it’s a cacheable index. Canon remains in Derivation. 

**Viz plugins** declare exporters (static plots, VTK, report bundlers) that operate on the canonical JSON/CSV produced by runners. 

---

## 7) UI standards (dark theme)

* QML-only presentation; application logic is behind ports.
* Markdown viewer must render canon docs directly from `Derivation/` with commit awareness (show HEAD hash near the doc). 
* The **Dashboard** surfaces: Active Experiments, Pending Approvals, Success Rate, and **open PROPOSAL_** counts by domain (scan Derivation for `PROPOSAL_*.md` without matching RESULTS). 
* **Results Browser** lists artifacts by domain/date with the **metrics.passed** flags and gate breakdown. 

---

## 8) Build & runtime (cross‑platform desktop)

* **Language/tooling:** C++20, Qt 6 (QML), CMake; Python 3 runners via `QProcess` or a thin pybind11 shim only for targeted calls (no wholesale re-hosting).
* **Compute:** CPU baseline; opt-in AMD ROCm backends for heavy viz/physics add-ons later—**never** require CUDA.
* **Config:** Use env vars to find Derivation: `VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`. GUI must *honor* the same resolution order as authorization helpers (CLI flags > env > .env). 

---

## 9) Quality gates (software + physics)

**Software gates (mandatory).** Hierarchical directories; no outer→inner deps; interfaces for cross-layer calls; ≤500 LOC/file; repository pattern; tests mirror source; business logic framework-free; domain models plain objects. 

**Physics gates (report-only in GUI).**
Nexus must display pass/fail against canon gates, e.g.:

* RD: `σ(k)=r−Dk²` and `c_front=2√(Dr)` within repo tolerances. 
* KG: locality cone speed ≈ `c`, Noether drift bounds, energy-oscillation slope≈2, etc.  
* Tubes/condensation: coverage and curvature gates. 

**Approvals enforcement.** Any failed approval check must block runs (or force **quarantine** with receipts) and show “guilty field” messaging from the policy module. 

---

## 10) CI & provenance

* **Smoke suite:** `ListDomains`, `ListPendingApprovals`, and `SchemaCatalog` run on CI to ensure Derivation is discoverable.
* **Approvals dry-run:** CI calls `approve_tag status` against `VDM_APPROVAL_DB` to verify DB reachability (read-only). 
* **Doc lints:** Ensure every physics-facing screen links the exact canon anchor (AXIOM/EQUATION/CONSTANT/SYMBOL).  
* **Results integrity:** Hash artifacts and display SHA-256 in the GUI alongside commit and seed. (Matches RESULTS policy.) 

---

## 11) Minimal Nexus scaffolding (starter files)

* **CMakeLists.txt**: Qt6 + C++20 target, `physics_nexus` app, link to `application`, `domain`, and `infrastructure` libraries; add `-DQT_QML_DEBUG` for dev.
* **scripts/seed_db.py**: optional helper that only *reads* the existing approval DB and prints status (no writes). 
* **tests/**:

  * `application/ApproveTag_test.cpp` (mocks IApprovalRepo; checks error paths).
  * `infrastructure/SchemaCatalog_test.cpp` (finds co-located specs/schemas beside runners). 

---

## 12) Security & roles

* **Write operations to approvals DB** must go through the CLI with an admin password (PBKDF2-SHA256). GUI can shell to CLI, but never stores the password. 
* **Read-only** listing (status, check, exempt list) is allowed without password. 
* **Public DB** is 0600; record where the path came from (flag, env, or .env) in telemetry for audit. 

---

## 13) Long‑term physics engine hook

* **Engine port**: define `IPhysicsEngine.h` (tick, loadWorld, setLaw, enable/disableLaw, addField) with a C++ backend (Eigen/OpenMP baseline; optional HIP/ROCm later).
* **Law layers**: map to A4 split (J, M, J⊕M) so enabling/disabling laws is coherent with canon axioms and meters. GUI toggles are **reporting only** until gates pass for the corresponding branch.  

---

## 14) Standards the GUI must reflect (physics-side text, not code)

* Cite AXIOMS (A0–A7) on causality, metriplectic split, measurability. 
* Equations & limits (KG/RD), constants, symbols, and their validation meters.  
* Proposal/Results authoring: whitepaper-grade structure, explicit thresholds, figure/CSV/JSON pairing. GUI export must follow these.  
* Decision discipline and documentation rules shape how we present uncertainty and gates in the UI.  

---

## 15) Operational acceptance checklist (for each Nexus release)

1. **Discoverability:** All domains & tags listed; schema/specs co-located and readable. 
2. **Approval flow:** “Approve” button shells to `approve_tag.py`; DB shows update; `check` passes. 
3. **Run flow:** Launches runner with spec; produces artifacts via `io_paths`; UI shows pass/fail.  
4. **Reporting:** Exported report meets RESULTS standards and includes commit, seed, thresholds, and gate matrix. 
5. **No duplication:** Nexus never writes into Derivation except via runners and `io_paths`; no schema/spec copies.

---

# Implementation Blueprint (concise)

**Classification:** *Runtime‑only* (software), with *Axiom‑core references* for physics gating.

**Objective recap:** Deliver a Qt/QML desktop to approve, run, and analyze Derivation experiments, surfacing canon KPIs and provenance without breaking approvals or artifact routing.

**Action plan (risk‑reduction order):**

1. Implement `DerivationScanner` + `SchemaCatalog` (read-only). 
2. Wrap approval CLI in `IApprovalRepo` adapter (status/check/approve). 
3. Implement `PythonRunnerService` + `ProcessMonitor` with env parity. 
4. Build the Results Browser that renders gate status from JSON. 
5. Add Markdown viewer (canon docs with commit). 
6. Add “Generate Report” that conforms to RESULTS standards. 
7. Integrate viz plugins (plots/VTK) over canonical logs. 

**Verification:**

* **Software gates:** directory hierarchy, DI, ≤500 LOC/file, repo pattern, mirrored tests. 
* **Physics gates (display):** RD & KG meters and tube coverage rendered with exact thresholds from JSON.   

**Assumptions/Risks:**

* Paths to Derivation and DBs resolved like policy (flags > env > .env). Kill-plan: fail fast with explicit remediation per policy text. 
* Runners remain Python-first; heavy engines come later (AMD ROCm optional). Kill-plan: CPU-only baseline with OpenMP.

**Next steps:**

* Add `physics_nexus/schemas/` for GUI-side config schemas (not physics outputs).
* Write adapters for common figures (e.g., RD dispersion/front) to auto-wire KPI charts. 
* Create CI jobs that smoke-test approval/scan/report without executing long simulations.

---

### Why this matches your repo (and fixes earlier misalignments)

* We **do not** move runners or schemas/specs; we **read them in place** as required by your `ARCHITECTURE.md`. 
* We enforce **the same approval rules**—script-scoped HMAC and DB secrets—already documented in `authorization/README.md`. 
* We render canon KPIs and thresholds verbatim from runner JSON, instead of inventing GUI-side physics logic. 

If you want me to generate the initial `CMakeLists.txt` and header skeletons for the ports/adapters above, I’ll draft them next so you can drop them straight into `physics_nexus/` and build.
