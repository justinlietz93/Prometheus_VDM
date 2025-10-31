# vdm_nexus/plugins

Declarative plugin descriptors that extend Nexus with physics domain catalogs and visualization exporters.

## Canonical storage policy (do not relocate)

Plugins only describe where canonical assets live. They never copy or move canonical files. Nexus reads everything in place:

- Data and approvals DBs (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative: `../Derivation/code/common/data/`
- Physics runners/specs/schemas/approvals (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../Derivation/code/physics/{domain}/`
- Experiment outputs (enumerated in place):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../Derivation/code/outputs/(figures|logs)/{domain}/`

Root resolution policy (must match app): CLI flags > environment (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`.

## Layout

- `physics/` — JSON descriptors listing domains, runner scripts, available tags, schema/spec directories pointing into `../Derivation/code/physics/{domain}/`.
- `viz/` — visualization plugin configs (e.g., Matplotlib, VTK, report exporters) describing how to render artifacts found under `../Derivation/code/outputs/(figures|logs)/{domain}/`.

## Authoring Rules

1. Plugins are descriptive only; no executable logic belongs here.
2. Paths must remain relative to the Nexus root and point to canonical locations under `../Derivation/` exactly as listed above (do not embed copies).
3. Keep descriptors schema-valid; additions require updating plugin tests under `../tests/plugins/`.
4. Treat plugin content as cacheable metadata—do not duplicate canonical spec/schema files or approval manifests.

## References

- Architecture standard: [`NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:31)
- Execution plan: [`TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:129)
