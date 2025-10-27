# vdm_nexus

VDM Nexus desktop application scaffold. This directory mirrors the Clean Architecture layout defined in [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../VDM_Nexus/NEXUS_ARCHITECTURE.md:23) and strictly reads canonical physics assets in place (no relocation or duplication).

## Canonical storage policy (do not relocate)

Nexus does not move or copy canonical files. It resolves and reads them in place:

- Data and approvals DBs (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative: `../derivation/code/common/data/`

- Physics runners, specs, schemas, approvals (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../derivation/code/physics/{domain}/`

- Experiment outputs (enumerated in place):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../derivation/code/outputs/(figures|logs)/{domain}/`

Root resolution policy (must match app/infrastructure): CLI flags > env (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`.

## Nexus local database (non‑canonical; reporting/config only)

Nexus MAY maintain its own local SQLite database for:
- Reporting/search indices (e.g., FTS over canon Markdown, artifact manifests)
- Analysis caches (e.g., derived gate summaries, visualization state)
- Nexus‑local configuration (GUI/session settings, plugin cache)

This database is derivative only and must never be treated as a source of truth for physics or approvals.

- Default location (repo‑relative): `vdm_nexus/data/nexus.db` (create `data/` as needed)
- Windows absolute example: `C:\git\Prometheus_VDM\vdm_nexus\data\nexus.db`
- Override via `VDM_NEXUS_DB` (CLI flag > env > `.env`)
- Required provenance columns on ingested rows:
  - `source_path` (relative to repo), `commit`, `salted_hash`, `ingested_utc`
- Guardrails:
  - No writes back to `../derivation/`
  - No approvals or policy decisions sourced from this DB (read the canonical DBs directly)
  - Provide purge/refresh commands; stale caches must be discardable at any time

Recommended tables (illustrative; define schemas under `vdm_nexus/schemas/`):
- `canon_docs(doc_id, path, title, type, commit, salted_hash, updated_utc, fts)`
- `artifacts(run_id, domain, tag, type, path, sha256, commit, seeded, updated_utc)`
- `kpi_cache(run_id, kpis_json, gate_matrix_json, commit, updated_utc)`
- `gui_config(key, value_json, updated_utc)`
- `plugin_cache(key, value_json, updated_utc)`

## Build Requirements

- CMake ≥ 3.24
- Qt 6.5 (Core, Gui, Qml, Quick, Widgets)
- C++20 compiler (Clang/LLVM 15+, MSVC 2022, or GCC 12+)
- Python 3.11 (for runner integration; see repository root `requirements.txt`)

## Quick Start

```bash
cmake -S vdm_nexus -B build -G "Ninja" -DQt6_DIR=/path/to/Qt/6.5/gcc_64/lib/cmake/Qt6
cmake --build build
cmake --install build --prefix install
```

If Qt is installed via the official online installer, replace `Qt6_DIR` with the matching toolchain path. On Windows/MSVC, use the Visual Studio generator and the Qt MSVC directory.

## Directory Layout

```
vdm_nexus/
  CMakeLists.txt          # root build script with Qt wiring
  .clang-format           # coding style aligned to repo standards
  presentation/           # QML/Qt Quick UI
  application/            # use cases and ports
  domain/                 # plain data models
  infrastructure/         # adapters (SQLite, filesystem, runners)
  plugins/                # physics & viz descriptors
  resources/              # qrc assets
  schemas/                # Nexus-specific JSON schemas (GUI/config only)
  scripts/                # helper CLIs (e.g., read-only canon sync)
  tests/                  # unit/integration tests mirroring source tree
  data/                   # Nexus local database (reporting/config caches) [optional]
```

## Pending Tasks

Refer to [`VDM_Nexus/TODO_CHECKLIST.md`](../VDM_Nexus/TODO_CHECKLIST.md:1) for the phased execution plan (currently executing Phase 0). Update the checklist and documentation as new components are implemented.
