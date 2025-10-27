# vdm_nexus/scripts

Helper CLIs and utilities for the Nexus desktop application (e.g., read-only canon sync, approval status wrappers, report packagers). These scripts do not contain or execute physics simulations.

## Canonical storage policy (do not relocate)

Scripts here must only reference canonical assets in-place. They never copy, move, or re‑write canonical files. Nexus honors the existing directory layout:

- Data and approvals DBs (canonical, read-only for scripts):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval.db`
  - Windows: `C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db`
  - Repo-relative: `../derivation/code/common/data/`
- Physics runners, specs, schemas, approvals (canonical, read-only):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\physics\{domain}\`
  - Repo-relative: `../derivation/code/physics/{domain}/`
- Experiment outputs (enumerated in place):
  - Windows: `C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\`
  - Repo-relative: `../derivation/code/outputs/(figures|logs)/{domain}/`

Root resolution policy (must match app/infrastructure): CLI flags > environment (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`.

## Scope

- Read-only helpers (e.g., canon indexing, artifact hashing, report bundling).
- Thin shells around the canonical approval CLI to surface admin workflows in a controlled way.
- Developer utilities for validating Nexus configuration and environment.

## Out of Scope (remain canonical)

- Data storage: `../derivation/code/common/data/` — Nexus must only reference these, never create duplicates.
- Physics simulations and artifacts: `../derivation/code/physics/{domain}/` — Nexus reads these in place, does not copy or modify.
- Experiment outputs: `../derivation/code/outputs/(figures|logs)/{domain}/` — Nexus enumerates and displays artifacts from canonical locations.

## Rules

1. Scripts must be safe by default (read-only). Any write action must be a thin wrapper over canonical tools like [`approve_tag.py`](../../derivation/code/common/authorization/approve_tag.py:1).
2. No hard-coded absolute paths. Resolve canonical roots via policy (CLI flags > env > `.env`).
3. Emit JSON/CSV logs with seeds, commit hashes, and reproducibility receipts if generating any Nexus-side outputs.
4. Keep files ≤ 500 LOC; include a short docstring pointing to linked standards.

## References

- Architecture: [`NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:129)
- Checklist: [`TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:129)
- Approvals: [`approve_tag.py`](../../derivation/code/common/authorization/approve_tag.py:1)
