# vdm_nexus/resources

Static assets for the Nexus GUI (icons, fonts, stylesheets, QRC manifests). These resources support presentation only and must not contain physics data, results, or schemas.

## Canonical storage policy (do not relocate)

Resources must only reference canonical assets; they must not copy or store physics data locally. Nexus reads everything in place:

- Data and approvals DBs (canonical, read-only):
  - Windows: C:\git\Prometheus_VDM\derivation\code\common\data\approval.db
  - Windows: C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db
  - Repo-relative: ../derivation/code/common/data/
- Physics runners/specs/schemas/approvals (canonical, read-only):
  - Windows: C:\git\Prometheus_VDM\derivation\code\physics\{domain}\
  - Repo-relative: ../derivation/code/physics/{domain}/
- Experiment outputs (enumerated in place):
  - Windows: C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\
  - Repo-relative: ../derivation/code/outputs/(figures|logs)/{domain}/

Root resolution policy (must match app/infrastructure): CLI flags > environment (VDM_REPO_ROOT, VDM_APPROVAL_DB, VDM_APPROVAL_ADMIN_DB) > .env.

## Scope

- App icons (SVG/PNG), font files, and theme CSS (e.g., Markdown.css used by the viewer).
- Qt resource collections (.qrc) referenced by the presentation layer.

## Out of Scope (remain canonical elsewhere)

- Data and approvals: ../derivation/code/common/data/
- Runners, specs, schemas, approvals: ../derivation/code/physics/{domain}/
- Experiment outputs (PNG/CSV/JSON): ../derivation/code/outputs/(figures|logs)/{domain}/

## Guidelines

1. Keep paths relative and referenced via the Qt resource system when possible.
2. Do not duplicate or embed physics artifacts in this folder.
3. Maintain a short manifest comment at the top of each .qrc describing included assets and intended panes.

## References

- Architecture: [VDM_Nexus/NEXUS_ARCHITECTURE.md](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:31)
- Checklist: [VDM_Nexus/TODO_CHECKLIST.md](../../VDM_Nexus/TODO_CHECKLIST.md:115)