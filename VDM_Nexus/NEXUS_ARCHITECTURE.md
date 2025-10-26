# VDM Nexus — Architecture Standards (v2)

**Purpose.** Provide enforceable guardrails so that `physics_nexus` integrates with the canonical `derivation/` tree without duplicating sources, weakening approvals, or breaking provenance.

**Scope.** Applies to the Qt/QML desktop client, any helper CLIs, and supporting services that ship with Nexus. Physics runners under `derivation/code/physics/` remain authoritative and unmodified.

## 1. Canon Commitments

| Canon source | Obligations | Nexus enforcement |
| --- | --- | --- |
| [VDM-AX-A0](../derivation/AXIOMS.md#vdm-ax-a0)–[VDM-AX-A7](../derivation/AXIOMS.md#vdm-ax-a7) | Cite axioms instead of paraphrasing; preserve metriplectic split and measurability claims. | UI copy references anchors; toggles for law branches are reporting-only until gates pass. |
| [VDM-E-033](../derivation/EQUATIONS.md#vdm-e-033), [VDM-E-035](../derivation/EQUATIONS.md#vdm-e-035), [VDM-E-090](../derivation/EQUATIONS.md#vdm-e-090)–[VDM-E-097](../derivation/EQUATIONS.md#vdm-e-097) | Display physics metrics using canonical formulas. | KPI panels pull values from runner JSON; tooltips link to equation anchors. |
| [VDM-A-013](../derivation/ALGORITHMS.md#vdm-a-013)–[VDM-A-021](../derivation/ALGORITHMS.md#vdm-a-021) | Respect metriplectic integrator and QC algorithms. | Launch dialogues expose only approved algorithm variants; diagnostics re-use existing helper scripts. |
| [Validation metrics index](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err) | Use repository KPIs and thresholds verbatim. | Pass/fail badges resolve directly from KPI fields; Nexus never edits thresholds. |
| RESULTS/PROPOSAL standards | Follow whitepaper-grade report templates and artifact policy (PNG + CSV + JSON). | Report exporter wraps `[RESULTS_PAPER_STANDARDS](../derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)` and enforces artifact lists. |

## 2. Governance & Approvals

1. Approvals remain in `[approval.db](../derivation/code/common/data/approval.db)` (read-only) and `[approval_admin.db](../derivation/code/common/data/approval_admin.db)` (admin writes).
2. All write operations shell to `[approve_tag.py](../derivation/code/common/authorization/approve_tag.py)`; Nexus never stores admin passwords.
3. Launch requests validate preregistration (proposal, schema, spec, approver, script HMAC). Failures block execution or route runs through quarantine using `[io_paths.py](../derivation/code/common/io_paths.py)` helpers.
4. When approvals mismatch, the UI displays the “guilty field” emitted by `common.authorization` and offers remediation instructions.
5. Artifacts from unapproved runs are tagged `engineering_only` and stored under `../derivation/code/outputs/failed_runs/`.

## 3. Directory & Dependency Guardrails

### 3.1 Directory integration

- Read runners, specs, schemas, approvals, and README files **in place** under `../derivation/code/physics/{domain}/`.
- Consume figures and logs directly from `../derivation/code/outputs/(figures|logs)/{domain}/` without copying or renaming.
- Keep Nexus sources under `physics_nexus/` with subdirectories `presentation/`, `application/`, `domain/`, `infrastructure/`, `plugins/`, `resources/`, `schemas/`, `scripts/`, and `tests/`.
- Use constructor injection and repository pattern throughout `application/`; no Qt, DB, or Python imports leak into business logic.
- Enforce ≤500 LOC per source file and mirror test tree structure in `tests/`.

### 3.2 Dependency flow

```
presentation → application → ports ← infrastructure
                      ↓
                   domain
```

- Each port (e.g., `IApprovalRepo`, `IRunnerService`) is defined in `application/ports/` and implemented by infrastructure adapters (SQLite, filesystem, process).
- `presentation/` (QML) binds to application use cases only.
- Domain models remain plain structs with serialization handled by adapters.

## 4. Execution Pipeline

1. **Discover.** `DerivationScanner` enumerates domains, runners, specs, and schemas; caches metadata but never writes to derivation.
2. **Sanity.** Nexus runs smoke RPCs (`ListDomains`, `ListPendingApprovals`, `SchemaCatalog`) during startup or CI, matching the CI requirements.
3. **Approve.** Users manage approvals via CLI wrappers; status view shows schema/proposal parity and HMAC IDs.
4. **Launch.** `IRunnerService` invokes the runner script with `--spec` path and inherited environment variables (`VDM_REPO_ROOT`, `VDM_APPROVAL_DB`, `VDM_APPROVAL_ADMIN_DB`, optionally `VDM_NEXUS=1`). Default compute target is CPU/AMD; CUDA is unsupported.
5. **Monitor.** `ProcessMonitor` streams stdout/stderr and telemetry without truncation; logs are read-only mirrors of runner output.
6. **Harvest.** On completion, Nexus reads JSON/CSV/PNG artifacts, computes SHA-256 hashes, and attaches commit + seed metadata.
7. **Report.** Exporter assembles RESULTS-grade bundles, ensuring references to proposals, approvals, KPI gates, and artifacts are intact.

## 5. Interface & Plugin Contracts

| Contract | Responsibility | Notes |
| --- | --- | --- |
| `IApprovalRepo` | Read approval manifests, request status, submit CLI-backed updates. | No caching of secrets; admin writes are CLI-only. |
| `IRunnerService` | Launch Python scripts with deterministic environments; enforce policy flags. | Fails fast on missing approvals; surfaces CLI stderr. |
| `ISchemaCatalog` | Validate JSON schemas/specs co-located with runners. | Resurfaces validation errors verbatim. |
| `IArtifactStore` | Enumerate outputs via `io_paths`; verify hashes. | Never deletes or relocates artifacts. |
| Physics plugin descriptors (`plugins/physics/*.nexus.json`) | Provide discoverable entries (domain, scripts, tags). | Treated as cache; canonical data stays in derivation. |
| Viz plugin descriptors (`plugins/viz/*.json`) | Map artifact types to viewers/exporters. | Operate on canonical artifacts only. |

## 6. UI & Reporting Standards

- Dark theme QML shell with panes for Dashboard, Experiments, Approvals, Artifacts, Viz, and Markdown viewer.
- Dashboard shows active experiments, pending approvals, and counts of `PROPOSAL_*` without matching RESULTS.
- KPI tables link each metric to the corresponding anchor in `VALIDATION_METRICS.md`.
- Markdown viewer renders canon docs read-only with displayed commit hashes.
- Report exports comply with `[RESULTS_PAPER_STANDARDS](../derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)` and include artifact manifests (PNG + CSV + JSON paths and hashes).

## 7. Build & Runtime Profile

- Toolchain: C++20, Qt 6, CMake; Python 3 runners spawned via `QProcess`.
- Supported platforms: Linux (primary), macOS, Windows—matching CI targets.
- Environment resolution order: CLI flag overrides → environment variables → `.env` file.
- Optional `gui_mode` flag may be passed to runners to emit lightweight `run-manifest.json` sidecars; default behaviour remains unchanged.
- Logging integrates with existing runtime telemetry; Nexus adds no external network services.

## 8. Validation & Metrics Exposure

| Domain | KPI anchors | Nexus presentation rule |
| --- | --- | --- |
| Reaction–Diffusion | [Front speed](../derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err), [Dispersion error](../derivation/VALIDATION_METRICS.md#kpi-dispersion-med-rel-err), [R² front fit](../derivation/VALIDATION_METRICS.md#kpi-r2-front-fit) | Display relative error, gate threshold, and R² with pass/fail badges. |
| Klein–Gordon (J-only) | [Energy oscillation slope](../derivation/VALIDATION_METRICS.md#kpi-kg-energy-osc-slope), [Time reversal error](../derivation/VALIDATION_METRICS.md#kpi-kg-reversal-sup), [Fine-step amplitude](../derivation/VALIDATION_METRICS.md#kpi-kg-rel-amp-fine) | Show log–log fit plots and residuals; enforce R² ≥ 0.999 gate. |
| Thermodynamic routing / Wave flux meter | [Flux balance](../derivation/VALIDATION_METRICS.md#kpi-taylor-green-nu-rel-err) analogue, [Dispersion gate reuse](../derivation/VALIDATION_METRICS.md#kpi-dispersion-med-rel-err) | Report prereg gates, absorber efficiency, and symmetry metrics; annotate geometry BCs. |
| Tachyonic condensation | [Spectrum coverage](../derivation/VALIDATION_METRICS.md#kpi-tube-cov-phys), [Condensation curvature](../derivation/VALIDATION_METRICS.md#kpi-tube-curvature-ok), [Finite fraction](../derivation/VALIDATION_METRICS.md#kpi-tube-finite-fraction) | Provide admissible coverage heatmaps and quadratic fit summaries. |
| Runtime observability | [Connectome entropy](../derivation/VALIDATION_METRICS.md#kpi-connectome-entropy), [Complexity cycles](../derivation/VALIDATION_METRICS.md#kpi-complexity-cycles), [B1 spike detector](../derivation/VALIDATION_METRICS.md#kpi-b1-spike-z) | Expose telemetry streams with thresholds; no GUI-side recalculation. |

## 9. Continuous Integration & Audit

- CI executes smoke commands (`ListDomains`, `ListPendingApprovals`, `SchemaCatalog`) and verifies Nexus builds on all supported platforms.
- Documentation lint ensures every physics-facing label links to its canonical anchor.
- Provenance check: exported reports include commit hash, seed, deterministic flags, and artifact hashes.
- Optional golden-run parity harness compares telemetry metrics against approved baselines.

## 10. Release Readiness Checklist

1. Discoverability: all approved domains, specs, and schemas appear in the catalog with matching timestamps.
2. Approval flow: GUI audit trail demonstrates CLI-backed approval changes plus DB status before/after.
3. Execution: sample run produces ≥1 PNG, ≥1 CSV, ≥1 JSON via `io_paths`, all hashed, all linked to gates.
4. Reporting: exported RESULTS bundle cites proposals, approvals, KPI anchors, and artifact manifests.
5. Quarantine discipline: failed gates route to `failed_runs/` with contradiction reports when required.
6. Security: approval password prompts occur only through CLI; environment origin logged in telemetry.
7. Regression: unit/integration tests cover ports, adapters, and UI smoke flows; no outer→inner dependencies.

## 11. Future Hooks (Non-blocking)

- `IPhysicsEngine` interface may bind to C++ metriplectic backends (Eigen/OpenMP baseline, HIP/ROCm optional) once validated; GUI switches remain read-only until corresponding gates graduate.
- CanonSync-style indexing of markdown canon is permitted only if it remains read-only, stores commit + salted hash, and offers purge controls to avoid stale copies.

---

Adhering to these standards keeps Nexus in lockstep with the Void Dynamics Model canon while delivering reproducible, policy-compliant experiment orchestration.
