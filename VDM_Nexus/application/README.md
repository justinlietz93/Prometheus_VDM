# vdm_nexus/application

Use-case layer for the VDM Nexus desktop client. It coordinates domain objects through ports while keeping presentation and infrastructure concerns decoupled.

## Structure

- `ports/` — interfaces that infrastructure adapters must implement (`IApprovalRepo`, `IRunnerService`, `ISchemaCatalog`, `IArtifactStore`, `IMarkdownReader`).
- `usecases/` — application services orchestrating Nexus workflows (discover, approve, launch, harvest, report).

## Canonical storage policy (do not relocate)

Nexus does not move or duplicate canonical physics assets. It reads them in place:

- Data and approvals DBs (canonical, read-only from Nexus):
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative: `../derivation/code/common/data/` (resolved by policy: CLI flags > env > .env)

- Physics runners, specs, schemas, approvals (canonical, read-only from Nexus):
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../derivation/code/physics/{domain}/`

- Experiment outputs (canonical, enumerated in place):
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../derivation/code/outputs/(figures|logs)/{domain}/`

Application logic here must respect these locations; any write flows occur only via launching approved canonical runners or approval CLI, never by writing into canon paths directly from the app.

## Guidelines

1. Business logic is framework-free; do not import Qt, database drivers, or Python runner helpers.
2. Depend only on `vdm_nexus/domain` types and the port interfaces defined under `ports/`.
3. Maintain constructor injection for all dependencies to preserve testability.
4. Keep files ≤ 500 LOC as mandated by the architecture standard.
5. Resolve roots per policy: CLI flags > environment variables (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`.

## References

- [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:23)
- [`VDM_Nexus/TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:1)