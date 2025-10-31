Stamping helper (Derivation/code/common/provenance/stamp_proposal.py)
---------------------------------------------------------------

Purpose
-------
Provides a small, reusable helper that ensures a proposal markdown and its
corresponding preregistration JSON contain canonical, machine‑readable salted
provenance. This is used by scaffolding and by approval gates.

API
---
Import and call the public function:

from common.provenance.stamp_proposal import stamp

res = stamp(proposal_path, prereg_path, salt_bytes=16)

Arguments
- proposal_path: path to the proposal markdown file (str or Path)
- prereg_path: path to the prereg JSON file (str or Path)
- salt_bytes: optional int, default 16 — number of random bytes used to generate the salt

Returns
-------
A dict with keys:
- proposal: canonicalized proposal path
- prereg: prereg path
- salted_sha256: the salted SHA256 for the first spec item
- salt_hex: hex salt value
- prereg_manifest: SHA256 hex of the prereg file after any updates

Header format written to proposals
-------------------------------
The stamp helper inserts or replaces a single canonical header line in the
proposal markdown. Example:

> Salted Provenance: spec salted_sha256=<64hex>; salt_hex=<hex>; prereg_manifest_sha256=<64hex>

This line is parsed by the approval gate to verify that the proposal references
the same salted provenance and prereg manifest that the prereg records.

Notes
-----
- The helper is idempotent: running it multiple times will not corrupt the files.
- Prefer importing and calling the helper directly (used by the scaffold CLI) to
  keep calls testable and avoid subprocess invocations.
