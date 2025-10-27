# vdm_nexus/tests

Test suites for the Nexus desktop application. Tests mirror the Clean Architecture layout and validate contracts without duplicating physics code or data.

## Layout (mirror of src)

- `presentation/` — QML/pane smoke and snapshot tests (render-only; no business logic)
- `application/` — use-case unit tests with mocked ports
- `domain/` — pure model tests (serialization, invariants)
- `infrastructure/` — adapter integration tests (SQLite read-only, filesystem, process)
- `plugins/` — plugin descriptor schema validation
- `schemas/` — Nexus-local JSON Schema validation
- `e2e/` — end-to-end smoke (approve → run → harvest → report), using canonical runners in place

## Rules

1. Do not copy physics runners/specs/schemas/approvals into this tree.
   - Runners, specs, schemas, approvals: `../derivation/code/physics/{domain}/`
   - Data/approvals DBs: `../derivation/code/common/data/`
2. Treat `../derivation/` as read-only. Mutations occur only by invoking approved CLI for approvals or by launching canonical runners.
3. Use constructor injection to mock ports; avoid global state in tests.
4. Keep tests deterministic: fix seeds, record commit hashes, and assert KPI thresholds match `derivation/VALIDATION_METRICS.md`.
5. File size ≤ 500 LOC; prefer small, focused cases.

## Environment

Resolve roots exactly as the app:

- CLI flags > environment variables > `.env`
- Expected env: `VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`

## Canon references

- Architecture standard: [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:129)
- Execution plan: [`VDM_Nexus/TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:129)
- KPI gates: [`derivation/VALIDATION_METRICS.md`](../../derivation/VALIDATION_METRICS.md:1)
