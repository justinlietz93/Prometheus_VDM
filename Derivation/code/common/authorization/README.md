# authorization/ — approval gate and CLI (DB-only)

Purpose

- Enforce proposal + schema + per-tag approval before experiments run.
- Provide a password-gated CLI to stamp approvals and update a local SQLite DB you control.

Contents

- `approval.py`: runtime gate with SQLite helpers (admin password PBKDF2, expected-key retrieval, checks)
- `approve_tag.py`: CLI that prompts for your password, stamps the manifest, and upserts the DB

What it is not

- Not mixed with other common utilities (kept isolated by design).
- Not a place for experiment code or plotting.

Usage (high level)

- Set `VDM_APPROVAL_DB` to your local DB path.
- Approve a tag: run `approve_tag.py <domain> <tag> --password-prompt --db "$VDM_APPROVAL_DB"`.
- In runners: `from common.authorization.approval import check_tag_approval` and pass its result to routing/plotting.

Policy

- DB-only verification: runtime compares the manifest's `approval_key` to the expected key from the DB.
- Keys are derived as `HMAC-SHA256(password, f"{domain}:{tag}")`; password is never stored in the repo.
- Approval requires: `pre_registered=true`, tag in `allowed_tags`, existing `proposal`, tag-matching JSON schema, approver name match, and approval key match.

Security

- Admin password is stored as PBKDF2-SHA256 hash with salt in the DB.
- All DB writes are password-gated; no environment secret fallbacks.

Ownership

- Maintainers: core devs. Keep this package to the two files above plus `__init__.py` for imports.
