# Contributing — vdm_nexus

Follow the Void Dynamics Model canon discipline when contributing to the Nexus desktop application.

## Canonical storage policy (do not relocate)

Nexus does not move or copy canonical assets. It must resolve and read them in place:

- Data and approvals DBs (canonical, read-only):
  - Windows: C:\git\Prometheus_VDM\derivation\code\common\data\approval.db
  - Windows: C:\git\Prometheus_VDM\derivation\code\common\data\approval_admin.db
  - Repo-relative: ../Derivation/code/common/data/

- Physics runners, specs, schemas, approvals (canonical, read-only):
  - Windows: C:\git\Prometheus_VDM\derivation\code\physics\{domain}\
  - Repo-relative: ../Derivation/code/physics/{domain}/

- Experiment outputs (enumerated in place):
  - Windows: C:\git\Prometheus_VDM\derivation\code\outputs\(figures|logs)\{domain}\
  - Repo-relative: ../Derivation/code/outputs/(figures|logs)/{domain}/

Root resolution policy (must match app/infrastructure): CLI flags > environment (VDM_REPO_ROOT, VDM_APPROVAL_DB, VDM_APPROVAL_ADMIN_DB) > .env. Treat ../Derivation/ as read-only; any writes occur only by launching approved canonical runners or using the canonical approvals CLI.

## Repository Pointers

- Canon root: ../Derivation/
- Approvals databases: ../Derivation/code/common/data/approval.db (read-only) and ../Derivation/code/common/data/approval_admin.db (admin writes via CLI only)
- Common helpers: ../Derivation/code/common/ (use io_paths.py and authorization APIs instead of duplicating logic)
- Canonical proposals/results: see Tier summaries in ../VDM_Nexus/TODO_CHECKLIST.md and the roadmap at ../VDM_Standards_Technical_Summary.md.md
- Architecture standard: ../VDM_Nexus/NEXUS_ARCHITECTURE.md

## Development Workflow

1. Work through the phased checklist: ../VDM_Nexus/TODO_CHECKLIST.md.
2. Configure and build:
   - cmake -S vdm_nexus -B build
   - cmake --build build
   - Ensure tests under vdm_nexus/tests/ pass.
3. Use .clang-format for C++ formatting; QML/JSON should follow Qt conventions (>2 spaces indentation).
4. Any run orchestration must call existing Python runners without modifying code in ../Derivation/ unless explicitly approved.
5. Update this file when new mandatory paths or policies are introduced.

## Approvals Discipline

- All experiment execution must be gated via ../Derivation/code/common/authorization/approve_tag.py.
- Unapproved runs must set --allow-unapproved and route artifacts to quarantine via io_paths.
- Record changes to approvals as part of commit messages referencing ticket/task IDs.

## Artifacts & Provenance

- Minimum artifacts per run: 1 PNG + 1 CSV + 1 JSON with seeds, commit hash, and gate outcomes.
- Use consistent paths under ../Derivation/code/outputs/(figures|logs)/{domain}.
- Include commit hash and timestamp in any generated reports.

## Communication

- Use issue tracker tags matching experiment domain (e.g., RD, Metriplectic, WaveFlux).
- Document any deviations from the architecture standard before implementation.
