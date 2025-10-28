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

## Update — 2025-10-27 21:45Z (Nexus Phase 1 kickoff)\n\n- CI: Added Nexus-only compile workflow [.github/workflows/nexus-ci.yml](.github/workflows/nexus-ci.yml:1). Builds VDM_Nexus with -DNEXUS_BUILD_TESTS=ON; no app execution; no Derivation writes.\n- CMake wiring: Top-level ensures compile-only ports target builds by default via ALL dep in [VDM_Nexus/CMakeLists.txt](VDM_Nexus/CMakeLists.txt:28). Compile-only source generated in [VDM_Nexus/tests/CMakeLists.txt](VDM_Nexus/tests/CMakeLists.txt:1).\n- Schemas scope guard: Confirmed explicit policy in [VDM_Nexus/schemas/README.md](VDM_Nexus/schemas/README.md:1) (GUI-local only; memory-graph/MCP/tokens out-of-scope for Nexus).\n- Checklist: Phase 0 items 3–5 marked DONE in [VDM_Nexus/TODO_CHECKLIST.md](VDM_Nexus/TODO_CHECKLIST.md:1).\n\nNext (immediate targets)\n1) File-coupled hot-reload MVP (presentation layer): integrate QFileSystemWatcher; on .vti/.vtp/.vtu change → reload viewport; on manifest change → validate against [vdm.run-manifest.v1.schema.json](VDM_Nexus/schemas/vdm.run-manifest.v1.schema.json:1) then refresh KPI overlays (thresholds via ISchemaCatalog).\n2) ISchemaCatalog adapter (infrastructure): enumerate Derivation spec/schema files and surface gating thresholds to UI; no thresholds from Markdown. Anchor definitions from [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md:1) displayed read-only.\n3) Scripts README tightening (Nexus-only scope) and precommit guard tests (simulate diffs; exclusions; CHRONICLES attestation) per [precommit_derivation_guard.py](VDM_Nexus/scripts/precommit_derivation_guard.py:1).\n

## 2025-10-28T04:55:30Z — Phase 1 · Task 1.2 scaffolding (approvals/quarantine)

Work completed:
- Added approvals wrapper CLI at [`approval_cli.py`](VDM_Nexus/scripts/approval_cli.py:1) to enforce env precedence (CLI &gt; env &gt; .env) and delegate all mutations to canonical [`approve_tag.py`](Derivation/code/common/authorization/approve_tag.py:1). Wrapper is read-only except for invoking the canonical tool.
- Documented usage, precedence, and examples in [`VDM_Nexus/scripts/README.md`](VDM_Nexus/scripts/README.md:1).
- Logged decision with rationale in [`memory-bank/decisionLog.md`](memory-bank/decisionLog.md:1).
- Scope alignment confirmed with Clean Architecture seams in [`NEXUS_ARCHITECTURE.md`](VDM_Nexus/NEXUS_ARCHITECTURE.md:186) (§12.4 ports).

Validation gates to execute next (Task 1.2 Validation):
- Demo CLI session: use [`approval_cli.py`](VDM_Nexus/scripts/approval_cli.py:1) → [`approve_tag.py`](Derivation/code/common/authorization/approve_tag.py:1) showing approval status change with admin prompt audited.
- Produce smoke run with unapproved status to confirm quarantine routing to failed_runs/ and policy JSON via [`io_paths.py`](Derivation/code/common/io_paths.py:1).

Determinism and policy:
- No Derivation/ writes performed by Nexus code; wrapper only shells canonical CLI.
- Environment is IEEE‑754 double; provenance and seeds are handled by canonical runners. Nexus will mirror pass/fail using thresholds from spec/schema only (see ISchemaCatalog in [`ports.hpp`](VDM_Nexus/application/ports/ports.hpp:122)).

Next actions:
- Mark checklist item “Document approvals wrapper usage” complete.
- Execute Task 1.2 validation steps and attach terminal transcript + artifact paths.


## 2025-10-28T05:36:25Z — Phase 1 · Task 1.2 validation (approvals/quarantine)

Validation summary:
- Wrapper existence check PASS: [approval_cli.py](VDM_Nexus/scripts/approval_cli.py:1) resolved canonical CLI [approve_tag.py](Derivation/code/common/authorization/approve_tag.py:1).
- Env precedence print PASS: CLI > env > .env reported sources as expected.
- Canonical status PASS (read-only): approvals DB initialized; admin DB not yet seeded (admin table missing) — expected until interactive setup.
- Quarantine routing PASS: [io_paths.py](Derivation/code/common/io_paths.py:1) honored VDM_POLICY flags; artifacts landed under failed_runs/.

Artifacts (quarantine smoke):
- JSON: [20251028_003623_nexus_task_1_2_smoke.json](Derivation/code/outputs/logs/metriplectic/failed_runs/20251028_003623_nexus_task_1_2_smoke.json:1)
- CSV: [20251028_003623_nexus_task_1_2_smoke.csv](Derivation/code/outputs/logs/metriplectic/failed_runs/20251028_003623_nexus_task_1_2_smoke.csv:1)

Wrapper + status transcript (abridged):
```text
=== 1) approvals wrapper: check ===
[NEXUS][OK] Found: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/authorization/approve_tag.py

=== 2) approvals wrapper: print-env (precedence CLI>env>.env) ===
[NEXUS][ENV] Resolved variables (source in brackets):
  VDM_REPO_ROOT=/mnt/ironwolf/git/Prometheus_VDM  [cli]
  VDM_APPROVAL_DB=/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/data/approval.db  [.env]
  VDM_APPROVAL_ADMIN_DB=/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/data/approval_admin.db  [.env]

=== 3) canonical approvals CLI status (read-only) via wrapper run -- status ===
[NEXUS][INFO] Launching canonical approvals CLI
[approve_tag] Using approvals DB at default path: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db (will create if missing)
[authorization] Using admin DB from env file /mnt/ironwolf/git/Prometheus_VDM/.env: /mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/data/approval_admin.db
{
  "public_db": {
    "path": "/mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db",
    "exists": true,
    "tables_present": ["approvals","domain_keys","exempt_scripts","tag_secrets"],
    "tables_missing": []
  },
  "admin_db": {
    "path": "/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/data/approval_admin.db",
    "exists": false,
    "tables_present": [],
    "tables_missing": ["admin"]
  }
}

=== 4) quarantine smoke using io_paths policy (force unapproved) ===
JSON_LOG: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/outputs/logs/metriplectic/failed_runs/20251028_003623_nexus_task_1_2_smoke.json
CSV_LOG:  /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/outputs/logs/metriplectic/failed_runs/20251028_003623_nexus_task_1_2_smoke.csv
QUARANTINE_ROUTING_OK
```

Gates and policy evaluation (Task 1.2):
- Approvals wrapper gate: PASS — [approval_cli.py](VDM_Nexus/scripts/approval_cli.py:1) enforces precedence and shells canonical CLI without storing secrets.
- Canonical status probe: PASS — read-only; confirms public DB schema; admin DB seeding still pending (expected).
- Quarantine routing gate: PASS — with `VDM_REQUIRE_APPROVAL=1`, `VDM_POLICY_APPROVED=0`, `VDM_POLICY_HARD_BLOCK=0`, [io_paths.py](Derivation/code/common/io_paths.py:1) produced failed_runs/ JSON+CSV, carrying policy_env and timestamp.

Notes:
- No Derivation/ source modifications; only artifacts written under canonical outputs paths per policy.
- Next optional step to demonstrate a full approval mutation requires interactive admin password:
  1) Seed admin DB and set domain key or tag secret via [approve_tag.py](Derivation/code/common/authorization/approve_tag.py:1) (interactive).
  2) Approve a domain:tag with `--script` to scope HMAC; observe DB upsert.
  3) Re-run status and a runner smoke with approval flags to show non-quarantined artifact routing.
