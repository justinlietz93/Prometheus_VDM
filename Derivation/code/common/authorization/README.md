# authorization/ — approval gate and CLI (DB-only)

Purpose

- Enforce proposal + tag-specific schema + script-scoped approval before experiments run.
- Provide a password-gated CLI to stamp approvals and update a local SQLite DB you control.

Contents

- `approval.py`: runtime gate with SQLite helpers
  - Public DB: approvals, domain_keys, tag_secrets, exempt_scripts
  - Admin DB: admin (PBKDF2-SHA256 password hash)
- `approve_tag.py`: CLI that prompts for your password for write ops, stamps the manifest, and upserts the public DB

What it is not

- Not mixed with other common utilities (kept isolated by design).
- Not a place for experiment code or plotting.

Setup & Usage (high level)

- Public DB path (required for runtime/CLI):
  - Export `VDM_APPROVAL_DB=/path/to/approval.db` (or pass `--db` to the CLI).
- Admin DB path (optional, for admin credentials only):
  - Export `VDM_APPROVAL_ADMIN_DB=/path/to/approval_admin.db` (defaults to `approval_admin.db` or falls back to public DB).
- Bootstrap/check status (no password required):
  - `python3 -m Derivation.code.common.authorization.approve_tag status [--db "$VDM_APPROVAL_DB"]`
- Approve a tag (script-scoped HMAC):
  - Preferred: set a tag-specific secret, then approve
    - `python3 -m Derivation.code.common.authorization.approve_tag set-tag-secret <domain> <tag> <secret> [--db "$VDM_APPROVAL_DB"]`
    - `python3 -m Derivation.code.common.authorization.approve_tag approve <domain> <tag> --script <run_script.py> --schema <path> [--db "$VDM_APPROVAL_DB"]`
  - Fallback: set a domain-wide key if no tag secret exists
    - `python3 -m Derivation.code.common.authorization.approve_tag set-domain-key <domain> <domain_key> [--db "$VDM_APPROVAL_DB"]`
- Verify (read-only, no password):
  - `python3 -m Derivation.code.common.authorization.approve_tag check <domain> <tag> --script <run_script.py> [--db "$VDM_APPROVAL_DB"]`
- Exemptions (admin-gated writes):
  - `python3 -m Derivation.code.common.authorization.approve_tag exempt list [--db "$VDM_APPROVAL_DB"]`
  - `python3 -m Derivation.code.common.authorization.approve_tag exempt add Derivation/code/physics/<domain>/<script.py> [--db "$VDM_APPROVAL_DB"]`
  - `python3 -m Derivation.code.common.authorization.approve_tag exempt remove <normalized/script/path>`
  - `python3 -m Derivation.code.common.authorization.approve_tag exempt snapshot [--db "$VDM_APPROVAL_DB"]`

Policy

- Global enforcement: approvals are required for all scripts unless a script is explicitly listed in DB `exempt_scripts`.
- Approval key derivation is script-scoped:
  - `HMAC-SHA256(secret, f"{domain}:{script}:{tag}")`
  - Secret priority: `tag_secret` (preferred) > `domain_key` (fallback)
- Approval requires:
  - `pre_registered=true`, tag present in `allowed_tags`
  - `proposal` file exists
  - tag-specific JSON schema exists and contains the same tag
  - `approved_by` matches configured approver name
  - `approval_key` in manifest matches expected key derived from DB secret

Security

- Two-DB design:
  - Public DB (approval.db): freely readable by runtime; write operations gated by CLI/password
  - Admin DB (approval_admin.db): stores only the PBKDF2-SHA256 admin password record
- The admin password is entered interactively (never via environment), and is used only to authorize CLI write operations.
- Read-only CLI commands (status, check, exempt list) do not require a password.
- Public DB file permissions are set to 0600 on creation; place DBs in user-private locations.

Path discovery and logging

- Both DB paths are discovered in this order:
  - Explicit CLI flags (when provided)
  - Environment variables: `VDM_APPROVAL_DB` and `VDM_APPROVAL_ADMIN_DB`
  - Optional `.env` files in the workspace (if present)
- When a DB path is resolved, the module logs the provenance (where the path came from) at INFO level.
- On first creation, the module initializes the schema and enforces 0600 permissions.

Approval manifest fields

- Runners must carry an approval block (for example in an `APPROVAL.json` manifest alongside the run), containing at minimum:
  - `domain`: string
  - `tag`: string (must appear in the tag-specific JSON schema)
  - `approved_by`: string (your canonical approver name)
  - `approval_key`: string (hex HMAC of `domain:script:tag` using `tag_secret` or `domain_key`)
  - `pre_registered`: boolean (true)
  - `proposal`: path or identifier of the proposal document
  - `schema`: path to the JSON schema used to validate this tag
- The runtime checker compares this block to DB-derived expectations and rejects runs on any mismatch.

Related: Results logging and trust stamps

- Outside this package, results are logged per-domain into SQLite with per-experiment tables. Rows store the canonical JSON payload and a `row_hash` (SHA-256) covering the entire row for tamper-evident auditing.
- Begin-run validations integrate this approval check before any artifacts are written.

Ownership

- Maintainers: core devs. Keep this package to the two files above plus `__init__.py` for imports.
