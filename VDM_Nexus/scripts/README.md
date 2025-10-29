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

1. Scripts must be safe by default (read-only). Any write action must be a thin wrapper over canonical tools like [`approve_tag.py`](../../Derivation/code/common/authorization/approve_tag.py:1).
2. No hard-coded absolute paths. Resolve canonical roots via policy (CLI flags > env > `.env`).
3. Emit JSON/CSV logs with seeds, commit hashes, and reproducibility receipts if generating any Nexus-side outputs.
4. Keep files ≤ 500 LOC; include a short docstring pointing to linked standards.

## Approvals wrapper (approval_cli.py)

Thin shell for approvals that enforces environment precedence and never stores secrets.

- Tool: [`approval_cli.py`](VDM_Nexus/scripts/approval_cli.py:1)
- Underlying canonical CLI: [`approve_tag.py`](../../Derivation/code/common/authorization/approve_tag.py:1)
- Precedence: CLI flags > env (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`) > `.env`
- Policy: read-only wrapper; prompts and mutations occur only in the canonical CLI.

Examples:

```bash
# Verify the canonical approvals CLI is resolvable
python3 VDM_Nexus/scripts/approval_cli.py check --repo-root .

# Inspect resolved environment (shows source of each var)
python3 VDM_Nexus/scripts/approval_cli.py print-env --repo-root .

# Forward a command to approve_tag.py (args after -- are passed verbatim)
python3 VDM_Nexus/scripts/approval_cli.py run -- \
  --domain metriplectic \
  --script run_kg_energy_oscillation.py \
  --tag prereg_v1 \
  --approve
```

Notes:
- Wrapper sets VDM_NEXUS=1 in the environment (harmless hint for GUI/in-situ modes).
- Exit code mirrors the underlying approve_tag.py process.

## CanonSync skeleton (nexus_canon_sync.py)

Read-only scaffolding for Task 0.3 canon ingestion. The CLI loads
`resources/nexus_canon_config.v1.json`, resolves each anchor via
`canon_paths.CanonResolver`, and prints metadata (exists, sha256, last
commit). Use this to verify canonical anchors without writing to
`Derivation/`.

Examples:

```bash
# Emit JSON plan for downstream tooling
python3 VDM_Nexus/scripts/nexus_canon_sync.py --json

# Use an alternate repository root (e.g., when running from build trees)
python3 VDM_Nexus/scripts/nexus_canon_sync.py --repo-root ..

# Point at a custom canon config manifest
python3 VDM_Nexus/scripts/nexus_canon_sync.py --config /tmp/custom_canon.json --json
```

Notes:

- The command never writes to Derivation/. It only reads canonical
  Markdown paths listed in the config manifest.
- Future CanonSync implementations can extend this skeleton to persist
  metadata into Nexus-local caches (not in scope for Task 0.3).

## References

- Architecture: [`NEXUS_ARCHITECTURE.md`](../../VDM_Nexus/NEXUS_ARCHITECTURE.md:129)
- Checklist: [`TODO_CHECKLIST.md`](../../VDM_Nexus/TODO_CHECKLIST.md:129)
- Approvals: [`approve_tag.py`](../../Derivation/code/common/authorization/approve_tag.py:1)

## Derivation Guard (CHRONICLES + Canon)

This repo includes an enforced guard for canon discipline:

- Pre-commit hook: [precommit_derivation_guard.py](VDM_Nexus/scripts/precommit_derivation_guard.py:1) via [.pre-commit-config.yaml](.pre-commit-config.yaml)
- CI workflow: [.github/workflows/derivation-guard.yml](.github/workflows/derivation-guard.yml)
- Informational warnings (non-fatal): [nexus_validate_gate.py](VDM_Nexus/scripts/nexus_validate_gate.py:1)

What it enforces (summary):

- If any tracked path under Derivation/ changes, then:
  - Derivation/CHRONICLES.md must be updated in the same diff, documenting the change and rationale. See template at [CHRONICLES.md](Derivation/CHRONICLES.md:1).
  - If the change is canon-impacting (proposals/experiments/code/results), update at least one canonical ALL-CAPS doc (e.g., [EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-033), [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err), [ROADMAP.md](Derivation/ROADMAP.md), [CANON_MAP.md](Derivation/CANON_MAP.md), [SCHEMAS.md](Derivation/SCHEMAS.md), [SYMBOLS.md](Derivation/SYMBOLS.md), [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md), [OPEN_QUESTIONS.md](Derivation/OPEN_QUESTIONS.md), [ALGORITHMS.md](Derivation/ALGORITHMS.md), [CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md)).
  - Include the attestation marker in CHRONICLES: Dependency-Chain-Reviewed: true

Canon-impacting heuristic and overrides:

- Heuristic patterns are built into [precommit_derivation_guard.py](VDM_Nexus/scripts/precommit_derivation_guard.py:121) (e.g., PROPOSAL_/RESULTS_, Derivation/code/**, schemas/specs, run_*.py).
- Force canonical requirement for any Derivation change with --require-canon.
- Exclusions mirror DEFAULT_EXCLUSIONS in [nexus_validate_gate.py](VDM_Nexus/scripts/nexus_validate_gate.py:53).

Local usage:

- Install and enable pre-commit
  - pip install pre-commit
  - pre-commit install
- Run on staged changes (auto on commit) or explicitly:
  - pre-commit run --all-files
- CI-equivalent local check against main:
  - python VDM_Nexus/scripts/precommit_derivation_guard.py --mode ci --base origin/main

Output semantics:

- The pre-commit/CI guard is enforced (exit 1 on violation).
- The Nexus validation gate prints non-fatal warnings about CHRONICLES or missing canon doc updates:
  - chronicles_missing, canon_docs_missing
  - See implementation at [nexus_validate_gate.py](VDM_Nexus/scripts/nexus_validate_gate.py:147)

Bypass policy:

- The only bypass for Derivation edits without canon updates is to explicitly document the change in [CHRONICLES.md](Derivation/CHRONICLES.md:1) per the embedded template header. Legitimate canon-impacting changes still require updates to relevant canon registries and the dependency-chain attestation.

Notes:

- Scripts remain read-only to Derivation/. Any writes must route through canonical tools (e.g., [approve_tag.py](../../Derivation/code/common/authorization/approve_tag.py:1)).
