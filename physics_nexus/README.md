# physics_nexus

VDM Nexus desktop application scaffold. This directory mirrors the Clean Architecture layout defined in [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../VDM_Nexus/NEXUS_ARCHITECTURE.md:23).

## Build Requirements

- CMake ≥ 3.24
- Qt 6.5 (Core, Gui, Qml, Quick, Widgets)
- C++20 compiler (Clang/LLVM 15+, MSVC 2022, or GCC 12+)
- Python 3.11 (for runner integration; see repository root `requirements.txt`)

## Quick Start

```bash
cmake -S physics_nexus -B build -G "Ninja" -DQt6_DIR=/path/to/Qt/6.5/gcc_64/lib/cmake/Qt6
cmake --build build
cmake --install build --prefix install
```

If Qt is installed via the official online installer, replace `Qt6_DIR` with the matching toolchain path. On Windows/MSVC, use the Visual Studio generator and the Qt MSVC directory.

## Directory Layout

```
physics_nexus/
  CMakeLists.txt          # root build script with Qt wiring
  .clang-format           # coding style aligned to repo standards
  presentation/           # QML/Qt Quick UI
  application/            # use cases and ports
  domain/                 # plain data models
  infrastructure/         # adapters (SQLite, filesystem, runners)
  plugins/                # physics & viz descriptors
  resources/              # qrc assets
  schemas/                # Nexus-specific JSON schemas
  scripts/                # helper CLIs (e.g., CanonSync)
  tests/                  # unit/integration tests mirroring source tree
```

## Pending Tasks

Refer to [`VDM_Nexus/TODO_CHECKLIST.md`](../VDM_Nexus/TODO_CHECKLIST.md) for the phased execution plan (currently executing Phase 0). Update the checklist and documentation as new components are implemented.
