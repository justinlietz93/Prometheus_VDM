# Quantum domain — VDM Particle–Triad Analogy (pre-registered)

Purpose

- Hosts the preregistered Particle–Triad experiment suites (β confiners, α free waves/oscillations, announcer steering without forcing, SIE meta‑governor).
- Uses ONLY common helpers from `Derivation/code/common` for approvals, IO paths, plotting, and canonical equations.

References

- Proposal: `Derivation/Quantum/PROPOSAL_VDM_Particle-triad_Analogy_v1.md`
- Canon: `Derivation/EQUATIONS.md`
- Helpers:
  - `Derivation/code/common/authorization` (runtime approval enforcement)
  - `Derivation/code/common/io_paths.py` (artifact routing)
  - `Derivation/code/common/vdm_equations.py` (equations)
  - `Derivation/code/common/constants.py` (constants)

Files

- `schemas/vdm-triad-v1.schema.json` — summary JSON schema (tag-bound)
- `specs/vdm-triad-v1.spec.json` — minimal spec/config scaffold
- `APPROVAL.json` — manifest with allowed tag and schema pointer (approval via DB is required)
- `run_vdm_triad_prereg.py` — entrypoint enforcing approvals and emitting compliance snapshot + artifact scaffold