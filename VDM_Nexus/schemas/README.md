# vdm_nexus/schemas

Nexus-local JSON Schemas for GUI configuration only. Do not duplicate or move physics experiment schemas here.

## Canonical storage policy (do not relocate)

Nexus reads canonical physics assets in place. This folder must not contain copies of physics schemas/specs/approvals.

- Data and approvals DBs (canonical, read-only):
  - Windows: C:\git\Prometheus_VDM\derivation\code\common\data\approval.db
  - Windows: C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db
  - Repo-relative: ../derivation/code/common/data/

- Physics runners, specs, schemas, approvals (canonical, read-only):
  - Windows: C:\git\Prometheus_VDM\derivation\code\physics\{domain}\
  - Repo-relative: ../derivation/code/physics/{domain}/

- Experiment outputs (enumerated in place):
  - Windows: C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\
  - Repo-relative: ../derivation/code/outputs/(figures|logs)/{domain}/

Root resolution policy (must match app/infrastructure): CLI flags > environment (VDM_REPO_ROOT, VDM_APPROVAL_DB, VDM_APPROVAL_ADMIN_DB) > .env.

## Scope

- GUI settings, plugin descriptor schemas, report/export configuration.
- Validation for Nexus-specific JSON files used by presentation/application layers.

## Out of Scope (remain canonical)

- Physics experiment schemas/specs/approvals live under ../derivation/code/physics/{domain}/schemas and must be read in place.
- Approval databases and policy are under ../derivation/code/common/data/ and ../derivation/code/common/authorization/README.md.

## Rules

1. Keep Nexus schemas minimal and versioned (e.g., gui-config-v1.schema.json).
2. Reference canonical physics schemas via relative paths into ../derivation/... when needed for cross-check, but never copy their content.
3. Add schema tests under ../tests/schemas/ to validate example documents.
4. Document each schema’s purpose and version in its $id and $comment.

## References

- Architecture standard: [VDM_Nexus/NEXUS_ARCHITECTURE.md](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:31)
- Execution plan: [VDM_Nexus/TODO_CHECKLIST.md](../../VDM_Nexus/TODO_CHECKLIST.md:94)
