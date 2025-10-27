# System Patterns

## Architectural Patterns

- Pattern 1: Description

## Design Patterns

- Pattern 1: Description

## Common Idioms

- Idiom 1: Description

## Pre-registration execution guard for scientific runners

All scientific runners must default-deny execution unless a proposal is approved. Provide a CLI escape hatch --allow-unapproved for engineering-only smokes. When unapproved, stamp JSON logs with policy { pre_registered:false, engineering_only:true, quarantined:true } and route artifacts via failed/quarantine paths so they are excluded from RESULTS/KPIs. Add lightweight README notices in output domains explaining quarantine.

### Examples

- derivation/code/physics/dark_photons/run_dp_noise_budget.py: guard flag and policy block
- derivation/code/physics/dark_photons/run_dp_fisher_check.py: guard flag and policy block
- derivation/VALIDATION_METRICS.md: Status fields marked planned (pre-registered)


## Causality audit ingestion via neuron head expansion + bounded chaining

When runtime logs include per-tick arrays of top-k neuron indices (e.g., evt_*_head), construct per-neuron per-tick events with IDs like kind:neuron:tick. Chain edges across ticks for the same neuron (last-seen map) to ensure a sparse, acyclic baseline graph. Disable unbounded time-inference by default to avoid dense graphs. Optionally allow bounded cross-neuron successors with a small max_successors and time tolerance. Use iterative Kahn’s algorithm for acyclicity checks to avoid recursion limits on large graphs.

### Examples

- Derivation/code/physics/causality/run_causality_dag_audit.py head expansion path
- Derivation/code/common/causality/event_dag.py with is_acyclic via Kahn’s algorithm


## Structure-check runner pattern for algebraic invariants

Provide a tiny, policy-aware runner that samples random vectors to test operator properties (e.g., J skew-symmetry via median |<v,Jv>| and M positive semidefiniteness via counts of negative <u,Mu>). Route outputs through io_paths with quarantine on unapproved runs; pair a short RESULTS doc that defines gates and artifact paths.

### Examples

- Derivation/code/physics/metriplectic/metriplectic_structure_checks.py
- Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md


## Experiment artifact and prereg discipline enforcement

All experiments must (1) be approved before running (default-deny; --allow-unapproved routes to quarantine), (2) use common.io_paths for all artifacts, (3) produce at minimum: 1 PNG figure + 1 CSV log + 1 JSON summary, (4) never emit a RESULTS document until metrics are finalized and approved, and (5) include a compliance block in the JSON with approvals, probe-limit, frozen-map, and artifact_minimum receipts.

### Examples

- Derivation/code/physics/thermo_routing/passive_thermo_routing/run_ftmc_v1.py writes 2 figures, a CSV metrics file via log_path_by_tag(..., type='csv'), and a JSON summary; approvals enforced via common.authorization.approval.check_tag_approval; RESULTS output disabled.

## Nexus Desktop Patterns (2025-10-27 10:07:00)

- Clean Architecture ports (viewport alignment)
  - Define ports in application layer and bind adapters in infrastructure:
    - IRunnerService, IArtifactStore, IMarkdownReader, ISchemaCatalog per [NEXUS_ARCHITECTURE.md §12.4](VDM_Nexus/NEXUS_ARCHITECTURE.md:179).
  - Pattern: presentation → application → ports ← infrastructure; domain is pure data. Reference: [NEXUS_ARCHITECTURE.md §3.2](VDM_Nexus/NEXUS_ARCHITECTURE.md:36).

- Qt/VTK initialization pattern
  - Use OpenGL Core 3.2 and set default format for QVTK:
    - QSurfaceFormat fmt; fmt.setProfile(CoreProfile); fmt.setVersion(3,2); QVTKOpenGLNativeWidget::setDefaultFormat(fmt) in [main.cpp](VDM_Nexus/vdm_nexus/src/main.cpp:1).
  - Create QVTKOpenGLNativeWidget and attach vtkGenericOpenGLRenderWindow; keep orientation marker widget bound to the interactor:
    - See [ViewportWindow.cpp](VDM_Nexus/vdm_nexus/src/ViewportWindow.cpp:37).

- Dataset loader dispatch (read-only viewers)
  - Extension-based dispatch:
    - .vti (ImageData): vtkXMLImageDataReader + vtkSmartVolumeMapper + transfer functions
    - .vtu (UnstructuredGrid): vtkXMLUnstructuredGridReader → vtkDataSetSurfaceFilter → vtkPolyDataMapper
    - .vtp (PolyData): vtkXMLPolyDataReader → vtkPolyDataMapper
    - .json (run-manifest): placeholder (validate later)
  - Reference implementation: [ViewportWindow.cpp](VDM_Nexus/vdm_nexus/src/ViewportWindow.cpp:100).

- VTK module wiring (CMake)
  - Link minimal modules for viewport MVP (CPU path):
    - CommonCore, CommonColor, CommonDataModel, FiltersCore, FiltersGeometry, FiltersSources, InteractionStyle, InteractionWidgets, RenderingCore, RenderingOpenGL2, RenderingAnnotation, RenderingFreeType, RenderingVolumeOpenGL2, IOXML, GUISupportQt
  - Use vtk_module_autoinit with ${VTK_LIBRARIES}. Reference: [CMakeLists.txt](VDM_Nexus/vdm_nexus/CMakeLists.txt:19).

- File-coupled hot-reload pattern (to implement)
  - Watch canonical output directories (via QFileSystemWatcher or platform watcher).
  - On file change: if .vti/.vtp/.vtu then reload dataset into viewport; if run-manifest.json then (1) validate JSON against [schemas/vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1), (2) update overlays/controls from spec/schema thresholds resolved by ISchemaCatalog.
  - Never copy/rename artifacts; operate in place via io_paths policy.

- Manifest validation and thresholds sourcing
  - Validate run-manifest.json against GUI-local schema [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1).
  - Resolve KPI thresholds exclusively from experiment spec/schema referenced by fields experiment_schema/spec_path; never from Markdown canon (VALIDATION_METRICS is definitions-only). Architecture: [NEXUS_ARCHITECTURE.md §12.2](VDM_Nexus/NEXUS_ARCHITECTURE.md:144).

- KPI overlays (read-only, canon-linked)
  - Display KPI cards with values from runner JSON sidecars; hyperlink labels to [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1).
  - Pass/fail computation uses thresholds from spec/schema surfaced via ISchemaCatalog; GUI does not modify or cache thresholds.

- Approvals policy (GUI write discipline)
  - All modifications go through [approve_tag.py](derivation/code/common/authorization/approve_tag.py:1) (CLI-backed; interactive password); GUI stores no secrets.
  - Results History connects read-only to per-domain SQLite with WAL; no writes. Paths resolved via env precedence and io helpers.

- ROCm/AMD profile and accelerators
  - Default rendering path is VTK OpenGL2; ROCm/VTK-m accelerators optional once VTK is built with Accelerators modules.
  - CUDA is unsupported by Nexus. Policy and profile: [NEXUS_ARCHITECTURE.md §12.9](VDM_Nexus/NEXUS_ARCHITECTURE.md:231).

- QML integration hook (future)
  - QVTKOpenGLNativeWidget embedded in QML via controller attach: see conceptual hook in [NEXUS_ARCHITECTURE.md §12.8](VDM_Nexus/NEXUS_ARCHITECTURE.md:221).

- Canon and artifact discipline (recap)
  - Canon Markdown is viewer-only with visible commit hashes; no thresholds derived from Markdown; artifacts are enumerated via [io_paths.py](derivation/code/common/io_paths.py:1) with no relocation.
