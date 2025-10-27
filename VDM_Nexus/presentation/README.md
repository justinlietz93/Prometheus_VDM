# vdm_nexus/presentation

Qt/QML presentation layer for the Nexus desktop application. Responsible for rendering dashboards, experiment browsers, approvals UI, telemetry charts, and Markdown views.

## Canonical storage policy (do not relocate)

Presentation only displays information sourced from canonical locations. It must not copy, cache, or write physics assets.

- Data and approvals DBs (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative: `../derivation/code/common/data/`
- Physics runners/specs/schemas/approvals (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../derivation/code/physics/{domain}/`
- Experiment outputs (enumerated and rendered in place):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../derivation/code/outputs/(figures|logs)/{domain}/`

Root resolution policy (match app/infrastructure): CLI flags > env (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`.

## Structure (planned)

- `qml/` — QML components (Shell, Dashboard, Experiments, Approvals, ResultsBrowser, VizWorkbench, MarkdownViewer)
- `styles/` — shared themes (dark theme, typography, Markdown CSS)
- Additional resources (icons, fonts) live under `../resources/`.

## Guidelines

1. Presentation code should bind only to application use cases via exposed context properties or controllers.
2. No business logic here—delegate to `application/` services.
3. Keep QML files organized by pane; enforce consistent naming (e.g., `Dashboard.qml`, `DashboardMetrics.qml`).
4. Follow Qt best practices (signal-slot, property bindings) and respect dark-mode accessibility.
5. Do not persist or transform artifacts; render directly from canonical paths.

## References

- [`VDM_Nexus/NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:31)
- [`VDM_Nexus/TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:115)