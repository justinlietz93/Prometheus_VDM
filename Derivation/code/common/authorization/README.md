# Common utilities: approval and artifact policy

This directory contains shared utilities used by physics runners for proposal/tag approval and artifact output policy.

- `approval.py`: Enforces proposal + schema + per-tag approval using a cryptographic approval key.
- `io_paths.py`: Centralized figure/log path helpers that honor approval policy (quarantine vs. normal outputs).
- `gen_approval_key.py`: CLI to generate `approval_key` values and timestamps for manifest updates.
- `approvals_db.py`: Local SQLite approvals database support.
- `approve_tag.py`: Helper to stamp manifest and write approvals to the DB with a password prompt.

## Quick workflow

1) Create proposal and schema
   - Proposal lives under writings, e.g. `Derivation/Metriplectic/PROPOSAL_*.md`.
   - JSON Schema lives under code, e.g. `Derivation/code/physics/<domain>/schemas/<tag>.schema.json` and must include `"tag": "<tag>"`.

2) Update code-side manifest
   - Path: `Derivation/code/physics/<domain>/APPROVAL.json`
   - Ensure your tag is in `allowed_tags` and `approvals["<tag>"]` has fields below.

3) Approve the tag (DB + manifest)

- Set `VDM_APPROVAL_DB` to a local path you control (e.g., `/secure/vdm_approvals.sqlite3`).
- Run `approve_tag.py` with `--password-prompt` (your password is never echoed or stored): this writes the derived expected key to the DB and stamps the manifest.

1) Verification at runtime

- When `VDM_APPROVAL_DB` is set, the runner will only trust the DB entry for `(<domain>, <tag>)`. No fallbacks.

1) Run your script

- Runners invoke `check_tag_approval(...)`. If approved, artifacts go to standard outputs; otherwise the run is blocked (or quarantined with `--allow-unapproved`).

## Approve a tag with password (DB + manifest)

```bash
# One-time: choose your DB path
export VDM_APPROVAL_DB=/secure/vdm_approvals.sqlite3

# Approve a tag (prompts for your password; password is not stored or echoed)
python3 Derivation/code/common/approve_tag.py metriplectic KG-dispersion-v1 --password-prompt --db "$VDM_APPROVAL_DB"
```

## Manifest fields (per tag)

- File: `Derivation/code/physics/<domain>/APPROVAL.json`
- Required for approval:
  - `pre_registered`: `true`
  - `allowed_tags`: includes the tag
  - `proposal`: path to the proposal document (must exist)
  - `approvals[tag].schema`: path to the JSON schema (must exist; include `"tag": "<tag>"`)
  - `approvals[tag].approved_by`: name of the approver (default expected: `"Justin K. Lietz"`; override with `VDM_APPROVER_NAME`)
  - `approvals[tag].approved_at`: ISO 8601 UTC timestamp (generator provides this)
  - `approvals[tag].approval_key`: hex key derived from your password for this tag (HMAC-SHA256(password, "{domain}:{tag}"))

Example snippet:

```json
{
  "pre_registered": true,
  "proposal": "Derivation/Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md",
  "allowed_tags": ["KG-dispersion-v1"],
  "approvals": {
    "KG-dispersion-v1": {
      "schema": "Derivation/code/physics/metriplectic/schemas/KG-dispersion-v1.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "2025-10-08T02:11:14.839214+00:00",
      "approval_key": "<hex-from-generator>"
    }
  }
}
```

## How verification works

`approval.py` approves only if ALL checks pass:

1) `pre_registered` is true and tag is in `allowed_tags`
2) Proposal file exists
3) Schema exists and contains matching `tag`
4) `approved_by` matches expected (default: "Justin K. Lietz")
5) `approval_key` matches the entry in the approvals DB at `VDM_APPROVAL_DB`.

If any check fails and `--allow-unapproved` is not used, the run stops with a detailed error. With `--allow-unapproved`, artifacts are quarantined.

## Environment variables

- `VDM_APPROVAL_DB`: Path to the local approvals SQLite DB. If set, DB verification is required; no fallbacks.
- `VDM_APPROVER_NAME`: Expected approver name (default: `Justin K. Lietz`).
- `VDM_REQUIRE_APPROVAL`: If `"1"`, `io_paths` requires explicit approval; otherwise quarantine applies by default.
- `VDM_POLICY_HARD_BLOCK`: If `"1"`, artifact writing is blocked when unapproved.

## Quarantine vs. normal outputs

- `io_paths.py` honors policy:
  - Unapproved/quarantined: `code/outputs/(figures|logs)/<domain>/failed_runs/...`
  - Approved: `code/outputs/(figures|logs)/<domain>/...`
- Set `VDM_POLICY_HARD_BLOCK=1` to hard-block writes when unapproved.

## Security & rotation

- The secret is never stored in the repo; supply it via environment or a private file.
- To revoke a single tag without rotating the secret: remove or change the tag’s `approval_key` in the manifest.
- To rotate the secret for all tags: generate new keys per tag and update the manifest entries.

## Troubleshooting

- Missing manifest: ensure `Derivation/code/physics/<domain>/APPROVAL.json` exists (domain is case-insensitive).
- Schema issues: confirm path in manifest and that the JSON includes `"tag": "<tag>"`.
- Approver mismatch: update `approved_by` or set `VDM_APPROVER_NAME`.
- Key verification failure: provide one of `VDM_APPROVAL_SECRET`/`VDM_APPROVAL_SECRET_FILE` (HMAC) or `VDM_APPROVAL_KEY_FILE` (direct match).


If you want, we can add an `approve_tag.py` helper that generates the key + timestamp and patches the manifest for a given tag without ever writing your secret.
If you want, we can add an `approve_tag.py` helper that generates the key + timestamp and patches the manifest for a given tag without ever writing your secret.
