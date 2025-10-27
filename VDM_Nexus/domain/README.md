# vdm_nexus/domain

Canonical data models for the Nexus application. These structs/classes carry experiment metadata, approvals, artifacts, KPI states, and provenance used across layers.

## Canonical storage policy (do not relocate)

Nexus does not move or duplicate canonical physics assets. It reads them in place and models them here as plain data.

- Data and approvals DBs (canonical, read-only from Nexus):
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative: `../derivation/code/common/data/` (resolved by policy: CLI flags > env > `.env`)

- Physics runners, specs, schemas, approvals (canonical, read-only from Nexus):
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../derivation/code/physics/{domain}/`

- Experiment outputs (canonical, enumerated in place):
  - Windows absolute: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../derivation/code/outputs/(figures|logs)/{domain}/`

Domain types must reflect these locations via paths/URIs but must not perform any I/O. Any writes occur only by launching approved canonical runners or using the approvals CLI; domain remains pure data.

## Rules

1. Plain data only. Keep types as POD/POJO with minimal helpers. No Qt, DB drivers, or runner imports.
2. No side effects. Serialization/persistence/orchestration belongs to `application/` or `infrastructure/`.
3. Stable interfaces. Changes here ripple to ports/adapters; update tests and docs accordingly.
4. Respect policy root resolution: CLI flags > `VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB` > `.env`.

## Typical Types

- `Experiment`, `Approval`, `RunnerSpec`, `Gate`, `Artifact`, `NexusSettings`
- Value objects for KPI summaries, telemetry snapshots, and provenance metadata

## References

- [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:23)
- [`VDM_Nexus/TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:1)
