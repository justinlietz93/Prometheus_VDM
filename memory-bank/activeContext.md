# Active Context

## Current Goals

- Current focus: CEG (Metriplectic Assisted‑Echo) T4 experiment. Avoid Qualia T3 edits; do not touch approvals (human-only). Ensure prereg/spec/runner alignment and enable preflight → approval → main run flow.

## Current Focus — Nexus desktop build (2025-10-27 10:03:00)

- Platform: Linux (Ubuntu 25.04) on host prometheus-ai; ROCm 6.4.3; GPUs: Instinct MI100 + RX 7900. CPU path first; VTK-m optional later.
- Source scaffold added:
  - [CMakeLists.txt](VDM_Nexus/vdm_nexus/CMakeLists.txt:1) links Qt6::Widgets and VTK modules (CommonCore, CommonColor, CommonDataModel, FiltersCore, FiltersGeometry, FiltersSources, InteractionStyle, InteractionWidgets, RenderingCore, RenderingOpenGL2, RenderingAnnotation, RenderingFreeType, RenderingVolumeOpenGL2, IOXML, GUISupportQt); vtk_module_autoinit configured.
  - [src/main.cpp](VDM_Nexus/vdm_nexus/src/main.cpp:1) creates QApplication, sets OpenGL 3.2 core profile via QSurfaceFormat, constructs [ViewportWindow.h](VDM_Nexus/vdm_nexus/src/ViewportWindow.h:1); optional argv[1] opens a dataset.
  - [src/ViewportWindow.cpp](VDM_Nexus/vdm_nexus/src/ViewportWindow.cpp:1) provides QVTKOpenGLNativeWidget viewport with orientation axes; default cube; readers:
    • .vti ImageData → vtkSmartVolumeMapper + transfer functions;
    • .vtp PolyData → vtkPolyDataMapper;
    • .vtu UnstructuredGrid → vtkDataSetSurfaceFilter → vtkPolyDataMapper;
    • .json manifest placeholder (no-op for now).
  - Manifest schema present: [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1).
- Canon discipline:
  - KPI thresholds resolved from the run’s spec/schema referenced by manifest experiment_schema/spec_path; anchors in [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1) used for definitions only.
  - GUI is a read-only lens; no physics recomputation.
- Approvals and IO policy (read-only within GUI):
  - CLI writes always via [approve_tag.py](derivation/code/common/authorization/approve_tag.py:1); approvals DBs discovered from env (VDM_APPROVAL_DB, VDM_APPROVAL_ADMIN_DB).
  - Artifacts enumerated via [io_paths.py](derivation/code/common/io_paths.py:1); no copies/renames.

## Linux build handoff (ROCm-friendly; CPU path)

1) Install dependencies:
   - sudo apt update
   - sudo apt install -y build-essential cmake qt6-base-dev qt6-base-dev-tools libqt6opengl6-dev libvtk9-dev
2) Build:
   - cd /mnt/ironwolf/git/Prometheus_VDM
   - cmake -S [vdm_nexus](VDM_Nexus/vdm_nexus/CMakeLists.txt:1) -B VDM_Nexus/build -DCMAKE_BUILD_TYPE=Release
   - cmake --build VDM_Nexus/build -j 32
3) Run:
   - ./VDM_Nexus/build/vdm_nexus /path/to/sample.{vti|vtp|vtu}
Notes:
   - If VTK version differs, adjust find_package(VTK 9.x) in [CMakeLists.txt](VDM_Nexus/vdm_nexus/CMakeLists.txt:19).
   - VTK-m/ROCm acceleration can be enabled once VTK is built with Accelerators; code unchanged until then.

## Next steps (ordered)

1) File‑coupled hot‑reload: watch step/output dirs; reload .vti/.vtu/.vtp on change; load run-manifest.json and validate against [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1). Status: NOT STARTED.
2) ISchemaCatalog adapter: validate manifests/specs and expose gating thresholds to UI from experiment schema/spec. Status: NOT STARTED.
3) Viz controls: iso-values, orthogonal/oblique slices, streamlines (RK4), particle sprites; probe cursor; scale bar/world axes polish. Status: NOT STARTED.
4) KPI overlay cards: values from runner JSON; hyperlinks to anchors in [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1); pass/fail from spec/schema thresholds only. Status: NOT STARTED.
5) Approvals and Results History panes (read-only DB access). Status: NOT STARTED.

## Current Blockers

- None (proceed to Linux install/build).
