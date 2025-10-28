# VDM Nexus — Architecture Standards (v2)

**Purpose.** Provide enforceable guardrails so that `physics_nexus` integrates with the canonical `derivation/` tree without duplicating sources, weakening approvals, or breaking provenance.

**Scope.** Applies to the Qt/QML desktop client, any helper CLIs, and supporting services that ship with Nexus. Physics runners under `derivation/code/physics/` remain authoritative and unmodified.

## 1. Canon Commitments

| Canon source | Obligations | Nexus enforcement |
| --- | --- | --- |
| [VDM-AX-A0](../derivation/AXIOMS.md#vdm-ax-a0)–[VDM-AX-A7](../derivation/AXIOMS.md#vdm-ax-a7) | Cite axioms instead of paraphrasing; preserve metriplectic split and measurability claims. | UI copy references anchors; toggles for law branches are reporting-only until gates pass. |
| [VDM-E-033](../derivation/EQUATIONS.md#vdm-e-033), [VDM-E-035](../derivation/EQUATIONS.md#vdm-e-035), [VDM-E-090](../derivation/EQUATIONS.md#vdm-e-090)–[VDM-E-097](../derivation/EQUATIONS.md#vdm-e-097) | Display physics metrics using canonical formulas. | KPI panels pull values from runner JSON; tooltips link to equation anchors. |
| [VDM-A-013](../derivation/ALGORITHMS.md#vdm-a-013)–[VDM-A-021](../derivation/ALGORITHMS.md#vdm-a-021) | Respect metriplectic integrator and QC algorithms. | Launch dialogues expose only approved algorithm variants; diagnostics re-use existing helper scripts. |
| [Validation metrics index](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err) | Use repository KPI definitions; thresholds are sourced from the active run's spec/schema. | Pass/fail badges resolve using thresholds from spec/schema; tooltips link to anchors; Nexus never edits thresholds. |
| RESULTS/PROPOSAL standards | Follow whitepaper-grade report templates and artifact policy (PNG + CSV + JSON). | Report exporter wraps `[RESULTS_PAPER_STANDARDS](../derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)` and enforces artifact lists. |

## 2. Governance & Approvals

1. Approvals remain in `[approval.db](../derivation/code/common/data/approval.db)` (read-only) and `[approval_admin.db](../derivation/code/common/data/approval_admin.db)` (admin writes).
2. All write operations shell to `[approve_tag.py](../derivation/code/common/authorization/approve_tag.py)`; Nexus never stores admin passwords.
3. Launch requests validate preregistration (proposal, schema, spec, approver, script HMAC). Failures block execution or route runs through quarantine using `[io_paths.py](../derivation/code/common/io_paths.py)` helpers.
4. When approvals mismatch, the UI displays the “guilty field” emitted by `common.authorization` and offers remediation instructions.
5. Artifacts from unapproved runs are tagged `engineering_only` and stored under `../derivation/code/outputs/failed_runs/`.

## 3. Directory & Dependency Guardrails

### 3.1 Directory integration

- Read runners, specs, schemas, approvals, and README files **in place** under `../derivation/code/physics/{domain}/`.
- Consume figures and logs directly from `../derivation/code/outputs/(figures|logs)/{domain}/` without copying or renaming.
- Keep Nexus sources under `physics_nexus/` with subdirectories `presentation/`, `application/`, `domain/`, `infrastructure/`, `plugins/`, `resources/`, `schemas/`, `scripts/`, and `tests/`.
- Use constructor injection and repository pattern throughout `application/`; no Qt, DB, or Python imports leak into business logic.
- Enforce ≤500 LOC per source file and mirror test tree structure in `tests/`.
- Canon Markdown (AXIOMS/EQUATIONS/VALIDATION_METRICS/etc.) is accessed only via the Markdown viewer for read‑only views; Nexus never derives thresholds, gates, or configuration from Markdown.

### 3.2 Dependency flow

```
presentation → application → ports ← infrastructure
                      ↓
                   domain
```

- Each port (e.g., `IApprovalRepo`, `IRunnerService`) is defined in `application/ports/` and implemented by infrastructure adapters (SQLite, filesystem, process).
- `presentation/` (QML) binds to application use cases only.
- Domain models remain plain structs with serialization handled by adapters.

### 3.3 Agent memory boundary (external‑agent‑only)

- Memory KG‑Lite belongs to external agents/tools only. VDM Nexus must not vendor, build, or reference any in‑repo implementation or path named "memory_kg_lite".
- Nexus may define pure ports (interfaces) for read‑only consumption of KG‑Lite artifacts or services. Implementations must live outside VDM_Nexus (e.g., an external microservice) and be configured via plugins/resources; no Nexus‑local adapters are permitted.
- If KG‑Lite artifacts exist in the repository, they must reside under memory‑bank/ (e.g., memory‑bank/MEMORY_GRAPH_CONTEXT) and are consumed read‑only; Nexus must not write or mutate these files.
- CI guard: [nexus_static_policy_check.py](VDM_Nexus/scripts/nexus_static_policy_check.py:1) fails when "memory_kg_lite" appears in any VDM_Nexus path or source literal (external‑agent‑only enforcement).

## 4. Execution Pipeline

1. **Discover.** `DerivationScanner` enumerates domains, runners, specs, and schemas; caches metadata but never writes to derivation; it does not parse Markdown canon to infer configuration (Markdown is viewer‑only).
2. **Sanity.** Nexus runs smoke RPCs (`ListDomains`, `ListPendingApprovals`, `SchemaCatalog`) during startup or CI, matching the CI requirements.
3. **Approve.** From the Approvals pane, the GUI lists pending items and triggers approval via [approve_tag.py](../derivation/code/common/authorization/approve_tag.py); Nexus presents the CLI password prompt without storing secrets, records receipts (approver, timestamp, HMAC), and refreshes DB status. Schema/proposal parity and HMAC IDs are shown alongside each entry.
4. **Launch.** `IRunnerService` invokes the runner script with `--spec` path and inherited environment variables (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`, optionally `VDM_NEXUS=1`). Default compute target is CPU/AMD; CUDA is unsupported.
5. **Monitor.** `ProcessMonitor` streams stdout/stderr and telemetry without truncation; logs are read-only mirrors of runner output.
6. **Harvest.** On completion, Nexus reads JSON/CSV/PNG artifacts, computes SHA-256 hashes, and attaches commit + seed metadata.
7. **Report.** Exporter assembles RESULTS-grade bundles, ensuring references to proposals, approvals, KPI gates, and artifacts are intact.

## 5. Interface & Plugin Contracts

| Contract | Responsibility | Notes |
| --- | --- | --- |
| `IApprovalRepo` | Read approval manifests, request status, submit CLI-backed updates. | No caching of secrets; admin writes are CLI-only. |
| `IRunnerService` | Launch Python scripts with deterministic environments; enforce policy flags. | Fails fast on missing approvals; surfaces CLI stderr. |
| `ISchemaCatalog` | Validate JSON schemas/specs co-located with runners and expose gating thresholds to the UI. | Resurfaces validation errors verbatim; thresholds are read from spec/schema, not from `VALIDATION_METRICS.md`. |
| `IArtifactStore` | Enumerate outputs via `io_paths`; verify hashes. | Never deletes or relocates artifacts. |
| Physics plugin descriptors (`plugins/physics/*.nexus.json`) | Provide discoverable entries (domain, scripts, tags). | Treated as cache; canonical data stays in derivation. |
| Viz plugin descriptors (`plugins/viz/*.json`) | Map artifact types to viewers/exporters. | Operate on canonical artifacts only. |

## 6. UI & Reporting Standards

- Dark theme QML shell with panes: Dashboard; Experiments; Approvals; Artifacts; Viz; Experiment Browser (Configs/Specs); Schema Viewer; Proposal/Results Viewer.
- Experiment Browser (read-only): lists per-domain experiments; opens config/spec JSON with a pretty/JSON-path viewer; displays repository path and commit hash; never writes to derivation.
- Schema Viewer (read-only): opens JSON Schemas co-located with runners; validates selected specs against their schema on demand; displays validation errors verbatim; no inference from Markdown canon.
- Proposal/Results Viewer (read-only): renders PROPOSAL_*and RESULTS_* Markdown with commit and salted-hash banners; links remain in-viewer; never used for gating or thresholds.
- Approvals pane (actionable): lists pending approvals from approvals DB; "Approve"/"Revoke" actions shell to [approve_tag.py](../derivation/code/common/authorization/approve_tag.py); Nexus never stores admin passwords; receipts (approver, timestamp, HMAC) are shown; DB status refreshes after completion.
- Results History pane (read-only DB-backed): aggregates per-domain results from per-experiment tables (SQLite, WAL) using [results_db.py](../derivation/code/common/data/results_db.py); filters by domain/script/tag/batch/status/time; opens row details (params_json, metrics_json, artifacts_json) with JSON viewers; never mutates DB.
- Dashboard shows active experiments, pending approvals, and counts of `PROPOSAL_*` without matching RESULTS.
- KPI tables link each metric to the corresponding anchor in `VALIDATION_METRICS.md`.
- Markdown viewer renders canon docs read-only with displayed commit hashes; viewer‑only (never used to drive thresholds, gates, or any numeric configuration).
- Report exports comply with `[RESULTS_PAPER_STANDARDS](../derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)` and include artifact manifests (PNG + CSV + JSON paths and hashes).

## 7. Build & Runtime Profile

- Toolchain: C++20, Qt 6, CMake; Python 3 runners spawned via `QProcess`.
- Supported platforms: Linux (primary), macOS, Windows—matching CI targets.
- Environment resolution order: CLI flag overrides → environment variables → `.env` file.
- Optional `gui_mode` flag may be passed to runners to emit lightweight `run-manifest.json` sidecars; default behaviour remains unchanged.
- Logging integrates with existing runtime telemetry; Nexus adds no external network services.
- Results DB root discovery for Results History: Nexus resolves per-domain SQLite paths via the canonical helper (read-only) and optionally honors `VDM_RESULTS_DB_ROOT` to point to a network share. Examples:
  - Windows UNC: `\\192.168.0.238\vdm_results`
  - Linux mount: `//192.168.0.238/vdm_results` or `/mnt/vdm_results`
  Nexus opens read-only connections with WAL enabled; the GUI performs no writes or copies.
- Approvals DB over network: `VDM_APPROVAL_DB` and `VDM_APPROVAL_ADMIN_DB` may reference network paths on `192.168.0.238`; writes occur only via CLI prompts; Nexus never stores secrets.

## 8. Validation & Metrics Exposure

Note: Thresholds are sourced from the active run's spec or schema; [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err) anchors provide definitions only.

| Domain | KPI anchors | Nexus presentation rule |
| --- | --- | --- |
| Reaction–Diffusion | [Front speed](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err), [Dispersion error](../derivation/VALIDATION_METRICS.md#kpi-dispersion-med-rel-err), [R² front fit](../derivation/VALIDATION_METRICS.md#kpi-r2-front-fit) | Display relative error, gate threshold, and R² with pass/fail badges. |
| Klein–Gordon (J-only) | [Energy oscillation slope](../derivation/VALIDATION_METRICS.md#kpi-kg-energy-osc-slope), [Time reversal error](../derivation/VALIDATION_METRICS.md#kpi-kg-reversal-sup), [Fine-step amplitude](../derivation/VALIDATION_METRICS.md#kpi-kg-rel-amp-fine) | Show log–log fit plots and residuals; enforce R² ≥ 0.999 gate. |
| Thermodynamic routing / Wave flux meter | [Flux balance](../derivation/VALIDATION_METRICS.md#kpi-taylor-green-nu-rel-err) analogue, [Dispersion gate reuse](../derivation/VALIDATION_METRICS.md#kpi-dispersion-med-rel-err) | Report prereg gates, absorber efficiency, and symmetry metrics; annotate geometry BCs. |
| Tachyonic condensation | [Spectrum coverage](../derivation/VALIDATION_METRICS.md#kpi-tube-cov-phys), [Condensation curvature](../derivation/VALIDATION_METRICS.md#kpi-tube-curvature-ok), [Finite fraction](../derivation/VALIDATION_METRICS.md#kpi-tube-finite-fraction) | Provide admissible coverage heatmaps and quadratic fit summaries. |
| Runtime observability | [Connectome entropy](../derivation/VALIDATION_METRICS.md#kpi-connectome-entropy), [Complexity cycles](../derivation/VALIDATION_METRICS.md#kpi-complexity-cycles), [B1 spike detector](../derivation/VALIDATION_METRICS.md#kpi-b1-spike-z) | Expose telemetry streams with thresholds; no GUI-side recalculation. |

## 9. Continuous Integration & Audit

- CI executes smoke commands (`ListDomains`, `ListPendingApprovals`, `SchemaCatalog`) and verifies Nexus builds on all supported platforms.
- Documentation lint ensures every physics-facing label links to its canonical anchor.
- Provenance check: exported reports include commit hash, seed, deterministic flags, and artifact hashes.
- Optional golden-run parity harness compares telemetry metrics against approved baselines.

## 10. Release Readiness Checklist

1. Discoverability: all approved domains, specs, and schemas appear in the catalog with matching timestamps.
2. Approval flow: GUI audit trail demonstrates CLI-backed approval changes plus DB status before/after.
3. Execution: sample run produces ≥1 PNG, ≥1 CSV, ≥1 JSON via `io_paths`, all hashed, all linked to gates.
4. Reporting: exported RESULTS bundle cites proposals, approvals, KPI anchors, and artifact manifests.
5. Quarantine discipline: failed gates route to `failed_runs/` with contradiction reports when required.
6. Security: approval password prompts occur only through CLI; environment origin logged in telemetry.
7. Regression: unit/integration tests cover ports, adapters, and UI smoke flows; no outer→inner dependencies.

## 11. Future Hooks (Non-blocking)

- `IPhysicsEngine` interface may bind to C++ metriplectic backends (Eigen/OpenMP baseline, HIP/ROCm optional) once validated; GUI switches remain read-only until corresponding gates graduate.
- CanonSync-style indexing of markdown canon is permitted only if it remains read-only, stores commit + salted hash, and offers purge controls to avoid stale copies.

## 12. Viewport & In‑Situ Visualization

This section defines the AMD/ROCm‑friendly, precision‑first visualization pathway that preserves runner primacy and canon gates while enabling a game‑like 3D viewport.

### 12.1 Stack (diagram in words)

Runners (unchanged) → In‑situ adapter → Viewport(s) → Artifacts & Reports

- Runners: scripts under `../derivation/code/physics/*` remain the single source of truth. Nexus never forks equations, thresholds, or gates; UI is read‑only.
- In‑situ adapter: a tiny library called when `--gui_mode` is present or `VDM_NEXUS=1` is set. It publishes fields per step as VTK XML datasets (ImageData / StructuredGrid / UnstructuredGrid) with metadata (commit, seed, Δt, units).
- Viewport(s):
  - Desktop: Qt 6 + VTK (QQuickVTK / QVTKOpenGLNativeWidget) provides a 3D viewport with orbit/pan/fly, time scrubber, slices, isosurfaces, streamlines, volume rendering, and probe cursors.
  - Remote/Web (optional): mirror via vtk.js or ParaView Live (Catalyst 2).
- Artifacts & Reports: PNG/CSV/JSON are harvested strictly from runners. Pass/fail gating uses thresholds from the active run's spec/schema; anchors in [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-kg-energy-osc-slope) are for definitions only. The GUI never “recalculates physics,” only renders/annotates and hyperlinks KPI cards to anchors.

### 12.2 Minimal data contract (stable)

On every publish (per step or per N frames), the adapter writes/streams:

```json
{
  "schema": "vdm.run-manifest.v1",
  "repo_commit": "<git-hash>",
  "seed": 12345,
  "dt": 0.0005,
  "t": 1.234,
  "domain": "kg_rd_metriplectic",
  "experiment_schema": "Derivation/code/physics/thermo_routing/schemas/thermo-routing-v2-prereg-biased-main.schema.json",
  "spec_path": "Derivation/code/physics/thermo_routing/specs/tr_v2_prereg_biased_main.json",
  "fields": [
    {"name":"phi_J","kind":"scalar","topology":"image","grid":[Nx,Ny,Nz],"spacing":[dx,dy,dz]},
    {"name":"phi_M","kind":"scalar","topology":"image"},
    {"name":"u","kind":"vector","topology":"image"},
    {"name":"mesh","kind":"unstructured","cells":"tet"},
    {"name":"particles","kind":"points","attribs":["x","v","mass"]}
  ],
  "kpis": {"front_speed_rel_err": 0.031, "kg_energy_osc_slope": -1.98}
}
```

- Datasets: `.vti/.vtu/.vtp` (VTK XML) or XDMF/HDF5.
- Manifest: co‑located with canonical outputs; read‑only to the GUI; provenance (SHA‑256 + file sizes) recorded.

### 12.3 Viewport features (precision‑first, game‑nice)

- Navigation: fly/turn/orbit; scale bar; world axes; unit banners.
- Exploration: iso‑value slider, orthogonal/oblique slices, clipping box, streamlines (RK4) from seeds, particle trails, tensor glyphs.
- Time: real‑time + stepper; loop/record MP4; jump‑to‑gate‑event when KPI crosses thresholds from the active run's spec/schema.
- Metrics overlay: KPI cards hyperlink to canon anchors; pass/fail badges mirror thresholds verbatim. No GUI‑side edits of metrics or thresholds.

### 12.4 Clean Architecture seams (viewport alignment)

- `IRunnerService`: spawns runner with `--spec ... --gui_mode` and env `{VDM_REPO_ROOT, VDM_APPROVAL_DB, VDM_APPROVAL_ADMIN_DB, VDM_NEXUS=1}`; fails fast without approvals.
- `IArtifactStore`: enumerates artifacts via `../derivation/code/common/io_paths.py`, computes hashes, and surfaces canonical paths to the UI.
- `IMarkdownReader`: renders canon docs read‑only with visible commit hashes.
- `ISchemaCatalog`: validates run manifests and summary JSONs against schemas; resolves thresholds only from the spec/schema indicated by the manifest; never from Markdown canon.

### 12.5 Visualization plugins

- `plugins/viz/volume.viz.json`: maps scalar fields to volume/iso/slice views.
- `plugins/viz/flow.viz.json`: seeds and streamlines for vector fields.
- `plugins/viz/tensor.viz.json`: tensor glyphs; `plugins/viz/particles.viz.json`: point sprites + trails.
- Plugins operate on canonical artifacts only (no copies/renames).
Example descriptor:

```json
{
  "id": "viz.volume.v1",
  "matches": {"kind":"scalar","topology":"image"},
  "controls": {"iso": true, "volume": true, "slice": ["X","Y","Z"]},
  "overlays": {"kpis":["front_speed_rel_err","kg_energy_osc_slope"]}
}
```

### 12.6 In‑situ coupling modes (both ROCm‑friendly)

- File‑coupled (fastest to ship): adapter writes VTK/XDMF every N steps; viewport watches the directory and hot‑reloads.
- Socket‑coupled (Catalyst 2 / Ascent): adapter streams arrays; ParaView/vtk.js attaches for true live flythrough. Enable per‑run; runner math unchanged.

### 12.7 Runner‑side emission example (Python)

```python
if os.getenv("VDM_NEXUS") == "1" or args.gui_mode:
    from vdm_nexus_adapter import Publisher  # minimal lib shipped with Nexus
    pub = Publisher(out_dir=io_paths.step_dir(run_tag))
    pub.publish_grid("phi_J", phiJ_array, spacing=(dx,dy,dz))
    pub.publish_grid("phi_M", phiM_array, spacing=(dx,dy,dz))
    pub.publish_vector("u", u_array)
    pub.publish_particles("particles", X, V, mass)
    pub.publish_kpis({"front_speed_rel_err": fs_err, "kg_energy_osc_slope": slope})
```

### 12.8 QML hook (conceptual)

```qml
QVTKOpenGLNativeWidget {
  id: viewport
  anchors.fill: parent
  Component.onCompleted: VizController.attach(viewport, manifestPath)
}
```

### 12.9 ROCm/AMD profile

- Desktop path uses Qt 6 + VTK OpenGL2 backend; acceleration via VTK‑m; optional Ascent/HIP backends when validated.
- CUDA is unsupported in Nexus; AMD/ROCm is the preferred GPU path. KPI definitions link to [VALIDATION_METRICS.md](../derivation/VALIDATION_METRICS.md#kpi-dispersion-med-rel-err) anchors; pass/fail thresholds are sourced from the run's spec/schema.

---

Adhering to these standards keeps Nexus in lockstep with the Void Dynamics Model canon while delivering reproducible, policy-compliant experiment orchestration.
