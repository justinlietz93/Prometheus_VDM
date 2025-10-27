# vdm_nexus/infrastructure

Adapters that connect Nexus ports to external systems (SQLite approvals DB, filesystem artifact store, Python runner processes, markdown loader, telemetry sources).

## Canonical storage policy (do not relocate)

Infrastructure reads canonical assets in place and never duplicates/moves them:

- Data and approvals DBs (canonical, read-only from adapters):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative root: `../derivation/code/common/data/`
- Physics runners/specs/schemas/approvals (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../derivation/code/physics/{domain}/`
- Experiment outputs (enumerated in place):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../derivation/code/outputs/(figures|logs)/{domain}/`

Root resolution policy (must match app): CLI flags > env (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`.

## Subdirectories (planned)

- `data/` — SQLite repositories (`SqliteApprovalRepo`, `SqliteResultsRepo`)
- `runners/` — process management for Python experiments (`PythonRunnerService`, `ProcessMonitor`)
- `catalog/` — schema/spec discovery (`SchemaCatalog`, `DerivationScanner`)
- `docs/` — markdown/commit readers
- Other adapters (e.g., REST/WebSocket) live in dedicated folders.

## Guidelines

1. Adhere to port interfaces defined in `../application/ports/`.
2. Use dependency injection; no singletons or hidden globals.
3. Treat `../derivation/` as read-only; write only via launching approved runners or calling the canonical approval CLI.
4. Keep file size ≤ 500 LOC and mirror test coverage under `../tests/infrastructure/`.

## Canon References

- [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:31)
- [`VDM_Nexus/TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:129)
