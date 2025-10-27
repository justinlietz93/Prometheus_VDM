# Progress (Updated: 2025-10-27)

## Done

- Scaffolded Nexus desktop MVP (Qt 6 + VTK) with CPU baseline:
  - Build script wiring Qt/VTK and vtk_module_autoinit: [CMakeLists.txt](VDM_Nexus/vdm_nexus/CMakeLists.txt:1)
  - App entry sets OpenGL 3.2 core format and launches window: [src/main.cpp](VDM_Nexus/vdm_nexus/src/main.cpp:1)
  - Viewport window (QVTKOpenGLNativeWidget) with default cube and orientation axes: [src/ViewportWindow.h](VDM_Nexus/vdm_nexus/src/ViewportWindow.h:1), [src/ViewportWindow.cpp](VDM_Nexus/vdm_nexus/src/ViewportWindow.cpp:1)
  - Dataset preview:
    - .vti (ImageData) — vtkSmartVolumeMapper with transfer functions
    - .vtp (PolyData), .vtu (UnstructuredGrid) — surface pipeline via vtkDataSetSurfaceFilter
- Codified ROCm/Linux-first stance and file-coupled in‑situ path per architecture:
  - Viewport & in‑situ stack: [NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:133)
  - Minimal run-manifest contract: [NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:144), schema stub: [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1)
  - ROCm/AMD profile: [NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:231)
- Memory Bank updated for handoff:
  - Active context (Linux ROCm build plan and next steps): [activeContext.md](memory-bank/activeContext.md:1)
  - Product context (Nexus overview, features, tech stack, data contract, build/run steps): [productContext.md](memory-bank/productContext.md:1)
  - Decision log entries for Linux primary build, viewport scaffold, file‑coupled path, and next ports: [decisionLog.md](memory-bank/decisionLog.md:1)

## Doing

- Switching execution to Linux ROCm server (prometheus-ai; ROCm 6.4.3; MI100 + RX 7900):
  1) sudo apt update && sudo apt install -y build-essential cmake qt6-base-dev qt6-base-dev-tools libqt6opengl6-dev libvtk9-dev
  2) cd /mnt/ironwolf/git/Prometheus_VDM
  3) cmake -S [vdm_nexus](VDM_Nexus/vdm_nexus/CMakeLists.txt:1) -B VDM_Nexus/build -DCMAKE_BUILD_TYPE=Release
  4) cmake --build VDM_Nexus/build -j 32
  5) ./VDM_Nexus/build/vdm_nexus /path/to/sample.{vti|vtp|vtu}
- Verifying on-sample datasets render correctly (volume, surface) with stable OpenGL context.

## Next

1) Implement file‑coupled hot‑reload for .vti/.vtu/.vtp and run‑manifest.json with JSON Schema validation against [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1).
2) Add ISchemaCatalog adapter: validate spec/schema indicated by run‑manifest; surface KPI thresholds for overlay; never derive from Markdown canon.
3) Add viz controls and meters in viewport:
   - Iso‑values, orthogonal/oblique slices, clipping box
   - Streamlines (RK4) with seed management; particle sprites/trails; tensor glyphs
   - Probe cursor; scale bar; world axes; unit banners
4) KPI overlay cards: values from runner JSON; hyperlinks to [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1); pass/fail computed with thresholds from spec/schema only.
5) Approvals (CLI-backed via [approve_tag.py](derivation/code/common/authorization/approve_tag.py:1)) and read‑only Results History (SQLite WAL) panes.
6) Report exporter: RESULTS-standard bundles with artifact manifests and provenance receipts.

## Notes

- GUI remains a read‑only lens; runners are authoritative. Artifacts enumerated in place via [io_paths.py](derivation/code/common/io_paths.py:1).
- Thresholds: definitions via [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1); thresholds exclusively from the experiment spec/schema referenced by the run‑manifest.
