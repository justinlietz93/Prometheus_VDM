# Progress (Updated: 2025-10-30)

## Done

- Added proposal stamping helper (Derivation/code/common/provenance/stamp_proposal.py) and integrated canonical Salted Provenance header insertion
- Made provenance gate opt-in per-domain via require_provenance in APPROVAL.json; updated approval.py to enforce only when true
- Added unit tests for approval gating and provenance checks (Derivation/code/common/authorization/tests/test_approval_provenance.py)
- Prepared CEG T4 prereg/spec/proposal with salted provenance (metriplectic): PRE-REGISTRATION.echo_spec-v1.json stamped; proposal has matching header; assisted_echo.v1.json exists; runner assisted_echo.py present; preflight tests present

## Doing

- CEG Assisted‑Echo T4: align spec tag with allowed_tags; run preflight tests; prepare for human approvals; after approval, run main assisted_echo with artifact logging

## Next

- PI runs approve_tag.py to set tag secret/domain key and approve echo_spec-v1 (or chosen tag) with script scope
- Decide tag alignment: change spec tag to echo_spec-v1 or add/approve assisted-echo-t4-prereg
- Run main assisted_echo.py with approved tag; publish artifacts per RESULTS; compute CEG median and gate ledgers
- Documentation/runbook updates: authorization/README.md add provenance header and stamping workflow; update proposal templates
