# Product Context

## Overview

VDM Nexus is a desktop application that provides a precision-first, read-only viewport and orchestration surface for the Void Dynamics Model (VDM) runners. Physics runners under `derivation/code/physics/*` remain the single source of truth; the GUI never recalculates physics nor duplicates canon. Visualization occurs via a Qt 6 + VTK 3D viewport, consuming canonical artifacts in place (VTK XML or XDMF/HDF5) and a minimal JSON run-manifest indicating the experiment schema and spec used for KPI thresholds.

Authoritative architecture references:
- Viewport & in-situ visualization: [VDM_Nexus/NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:129)
- Minimal in-situ data contract: [VDM_Nexus/NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:144)
- ROCm/AMD profile and policy: [VDM_Nexus/NEXUS_ARCHITECTURE.md](VDM_Nexus/NEXUS_ARCHITECTURE.md:231)

## Core Features

- 3D Viewport (Qt 6 + VTK)
  - Navigation: fly/turn/orbit, scale bar, world axes, unit banners
  - Exploration: iso-values, orthogonal/oblique slices, clipping, streamlines (RK4) from seeded points, particle sprites/trails, tensor glyphs, probe cursors
  - Time: stepper and real-time play, loop/record MP4, jump-to-gate event navigation
  - KPI overlays: pass/fail badges computed strictly from thresholds in the active run’s spec/schema; KPI definitions link to [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1)

- In-situ coupling modes
  - File-coupled hot-reload (first to ship): watch canonical output directories; reload .vti/.vtu/.vtp and run-manifest.json as they appear
  - Socket-coupled (optional): ParaView Catalyst 2 / Ascent live streaming for true flythrough

- Canon and approvals discipline
  - Canon Markdown is read-only with visible commit hashes; the GUI cites anchors (AXIOMS/EQUATIONS/VALIDATION_METRICS) without duplicating formulas or thresholds
  - All approval writes are CLI-backed via [approve_tag.py](derivation/code/common/authorization/approve_tag.py:1); GUI stores no secrets
  - Artifacts are enumerated via [io_paths.py](derivation/code/common/io_paths.py:1) in place; no copies or renames

- Results History and Reporting
  - Read-only aggregation of per-domain SQLite results (WAL) with filter and detail views (never mutates DB)
  - Export RESULTS-grade bundles per standards with artifact manifests and provenance

## Technical Stack

- Languages/build: C++20, CMake
- UI/Render: Qt 6 (Widgets), VTK 9 (OpenGL2 pipeline; VTK-m optional)
- Data formats: VTK XML (.vti ImageData, .vtu UnstructuredGrid, .vtp PolyData), XDMF/HDF5, JSON manifests and logs
- Runners: Python 3; all physics code and metrics live under `derivation/`
- JSON Schemas: manifest and GUI-local plugin/config schemas validated prior to trust
- OS: Linux (primary, ROCm-friendly), macOS and Windows as secondary
- GPU: AMD ROCm path preferred; CUDA unsupported in Nexus (see [ROCm profile](VDM_Nexus/NEXUS_ARCHITECTURE.md:231))

Executable scaffold (current):
- Build script: [CMakeLists.txt](VDM_Nexus/vdm_nexus/CMakeLists.txt:1)
- App entry: [src/main.cpp](VDM_Nexus/vdm_nexus/src/main.cpp:1)
- Viewport window: [src/ViewportWindow.h](VDM_Nexus/vdm_nexus/src/ViewportWindow.h:1), [src/ViewportWindow.cpp](VDM_Nexus/vdm_nexus/src/ViewportWindow.cpp:1)
- Manifest schema: [schemas/vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1)

## Minimal Data Contract (GUI-mode publish)

- JSON manifest (schema v1) fields include:
  - schema: "vdm.run-manifest.v1"
  - repo_commit, seed, dt, t, domain
  - experiment_schema (JSON Schema path for spec), spec_path (spec JSON path)
  - fields[] descriptors (name, kind, topology, grid/spacing as applicable)
  - kpis{} values emitted by runner
- Datasets: .vti/.vtu/.vtp or XDMF/HDF5 located alongside canonical outputs
- GUI treats manifest as read-only and validates against [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1)
- KPI definitions link to canon anchors; pass/fail thresholds are resolved exclusively from the experiment spec/schema referenced in the manifest (never from Markdown canon). Reference: [NEXUS_ARCHITECTURE §12.2](VDM_Nexus/NEXUS_ARCHITECTURE.md:144)

## Clean Architecture seams (ports/adapters)

- IRunnerService: spawn approved runners with `--spec ...` and `VDM_NEXUS=1` when GUI mode is on; fail fast without approvals. Reference: [NEXUS_ARCHITECTURE §12.4](VDM_Nexus/NEXUS_ARCHITECTURE.md:179)
- IArtifactStore: enumerate artifacts via io_paths, compute hashes, surface canonical paths
- IMarkdownReader: render canon Markdown read-only with visible commit hashes
- ISchemaCatalog: validate JSON schemas/specs and surface thresholds to UI strictly from spec/schema (never from canon Markdown)

## Environment and Paths

- Environment resolution order: CLI flags → env vars → .env
- Networked DB paths (example host 192.168.0.238):
  - VDM_APPROVAL_DB, VDM_APPROVAL_ADMIN_DB (read-only in GUI; writes via CLI only)
  - VDM_RESULTS_DB_ROOT for Results History (read-only, WAL)
- Repository root detection: VDM_REPO_ROOT points to the local clone hosting `derivation/`

## Build profile (Linux ROCm server, CPU path first)

Dependencies:
- sudo apt update
- sudo apt install -y build-essential cmake qt6-base-dev qt6-base-dev-tools libqt6opengl6-dev libvtk9-dev

Build:
- cd /mnt/ironwolf/git/Prometheus_VDM
- cmake -S [vdm_nexus](VDM_Nexus/vdm_nexus/CMakeLists.txt:1) -B VDM_Nexus/build -DCMAKE_BUILD_TYPE=Release
- cmake --build VDM_Nexus/build -j 32

Run:
- ./VDM_Nexus/build/vdm_nexus /path/to/sample.{vti|vtp|vtu}

Notes:
- For VTK-m/ROCm acceleration, build VTK with Accelerators; link additional modules; GUI code remains unchanged until validated
- Windows is supported as CPU-only secondary; configure CMake with Qt/VTK install prefixes or vcpkg toolchain

## Policy and Canon Discipline

- Approvals required prior to runs; unapproved runs must route artifacts to failed/quarantine paths with policy receipts (engineering_only)
- GUI never duplicates canon nor derives thresholds from Markdown; GUI overlays cite anchors only (AXIOMS/EQUATIONS/VALIDATION_METRICS)
- Artifact minimum per run: ≥1 PNG figure + ≥1 CSV log + ≥1 JSON log; provenance and hashes included in reporting
- KPI gates and thresholds are spec/schema-owned; see definitions in [VALIDATION_METRICS.md](derivation/VALIDATION_METRICS.md:1), thresholds in the referenced schema/spec

## Current Status (2025-10-27)

- Completed:
  - CMake target and Qt+VTK wiring with required VTK modules (RenderingOpenGL2, IOXML, InteractionStyle/Widgets, RenderingFreeType/Annotation, VolumeOpenGL2)
  - QVTKOpenGLNativeWidget viewport MVP: volume rendering (.vti), surface rendering (.vtp/.vtu), default cube, orientation axes
  - Manifest JSON Schema drafted and placed under schemas/
- In progress:
  - Switching builds to Linux ROCm server (CPU path first)
- Next (ordered):
  1) File-coupled hot-reload for datasets and manifest (with JSON Schema validation)
  2) ISchemaCatalog thresholds adapter and KPI card overlays (links to canon anchors)
  3) Viz controls (iso/slice/streamlines/particles/tensors) and probe cursor with unit banners
  4) Approvals pane (CLI-backed) and Results History (read-only DB aggregation)
  5) Report exporter bundles per RESULTS standards with artifact manifests and hashes