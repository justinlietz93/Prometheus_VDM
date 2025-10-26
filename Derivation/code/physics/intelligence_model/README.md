# Intelligence Model (physics-native) — Code Domain

This is the runtime/code counterpart to `Derivation/Intelligence_Model/`.

Structure

- modules/ — reusable components (fields, operators, meters, agent glue)
- runners/ — CLI entrypoints for experiments (policy-aware; approvals-first)
- tests/ — unit and smoke tests for modules and runners
- schemas/ — JSON Schemas for summaries (already present)
- specs/ — JSON specs for runs (already present)
- docs/ — code-level docs, design notes
- notebooks/ — scratch exploration (do not substitute RESULTS)

Standards

- Use `Derivation/code/common/io_paths.py` for all artifacts (PNG, CSV, JSON), with tag routing and quarantine defaults.
- Enforce approvals via `Derivation/code/common/authorization` before producing non-quarantine artifacts.
- Emit one PNG + one CSV + one JSON minimum per run, same basename.
- Summaries must validate against a schema in `schemas/`.
- Keep runners additive; prefer new entrypoints over modifying canonical ones.

Domain slug and outputs

- Domain slug: `intelligence_model`.
- Figures path: `Derivation/code/outputs/figures/intelligence_model/`
- Logs path: `Derivation/code/outputs/logs/intelligence_model/`

Next steps

- Add a `runners/run_im_substrate_v1.py` for the substrate-only real-time run (no agents), mirroring the Wave Flux Meter discipline.
- Add schema/spec stubs for `intelligence-model-v1` and wire approvals.
