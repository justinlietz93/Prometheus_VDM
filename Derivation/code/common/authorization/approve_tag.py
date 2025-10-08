#!/usr/bin/env python3
"""
Approve a tag for a physics domain by updating the domain APPROVAL.json manifest and the local approvals DB.

DB-only flow (minimal files):
 - Prompts for your admin password and verifies it against the local SQLite DB (VDM_APPROVAL_DB).
 - Derives approval_key = HMAC-SHA256(password, f"{domain}:{tag}").
 - Stamps approved_by and approved_at in the manifest, and upserts the expected key into the DB.
 - Ensures pre_registered=true and allowed_tags contains the tag.
 - Optionally sets the schema path if missing (with --schema).

No environment secrets or key files are used. Password must be entered manually via prompt (or VDM_APPROVAL_DB_PASSWORD for automation you control).

Usage example:
    export VDM_APPROVAL_DB=/secure/vdm_approvals.sqlite3
    python3 Derivation/code/common/approve_tag.py metriplectic KG-dispersion-v1 --password-prompt --db "$VDM_APPROVAL_DB"
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path
import getpass
from .approval import (
    ensure_db,
    upsert_approval,
    compute_expected_key,
    ApprovalRecord,
    ensure_admin_verified,
    set_domain_key,
    set_tag_secret,
)  # type: ignore


# Legacy helpers removed: DB-only flow derives key from password; no secret files.


def _iso_utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("domain", help="Physics domain name (e.g., metriplectic)")
    p.add_argument("tag", help="Tag to approve (e.g., KG-dispersion-v1)")
    p.add_argument(
        "--manifest",
        help="Path to APPROVAL.json (default: Derivation/code/physics/<domain>/APPROVAL.json)",
    )
    p.add_argument("--approver", default=os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz"))
    p.add_argument("--approved-at", dest="approved_at", help="Override ISO-8601 UTC timestamp")
    p.add_argument("--schema", help="Optional schema path to set if missing")
    p.add_argument("--dry-run", action="store_true", help="Do not write changes, just print what would change")
    # Approvals DB (required)
    p.add_argument("--db", dest="db_path", required=True, help="Path to approvals DB (SQLite). Required.")
    p.add_argument("--password-prompt", action="store_true", help="Prompt for a password to derive the expected key (never echoes). Required unless VDM_APPROVAL_DB_PASSWORD is set.")
    args = p.parse_args(argv)

    domain = args.domain.strip()
    tag = args.tag.strip()

    default_manifest = Path("Derivation") / "code" / "physics" / domain.lower() / "APPROVAL.json"
    manifest_path = Path(args.manifest) if args.manifest else default_manifest
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    # Require password before any DB access
    password = os.getenv("VDM_APPROVAL_DB_PASSWORD")
    if not password and args.password_prompt:
        password = getpass.getpass("Password (won't echo): ")
    if not password:
        print("ERROR: A password is required. Use --password-prompt or set VDM_APPROVAL_DB_PASSWORD.", file=sys.stderr)
        return 3

    # Verify admin password in DB before any other DB operation
    dbp = Path(args.db_path)
    if not ensure_admin_verified(dbp, password):
        print("ERROR: Admin password did not match the stored database password.", file=sys.stderr)
        return 3

    # Derive the approval key from password
    approval_key = compute_expected_key(password, domain, tag)

    approved_at = args.approved_at or _iso_utc_now()
    approver = args.approver

    # Load manifest
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: Failed to read manifest JSON: {e}", file=sys.stderr)
        return 4

    # Mutations
    before = json.dumps(data, sort_keys=True)
    data["pre_registered"] = True
    allowed = set(data.get("allowed_tags", []) or [])
    if tag not in allowed:
        allowed.add(tag)
        data["allowed_tags"] = sorted(allowed)

    approvals = data.setdefault("approvals", {})
    entry = approvals.setdefault(tag, {})
    if args.schema and not entry.get("schema"):
        # Only set schema if missing and user provided one
        schema_path = args.schema
        # sanity: schema should exist
        if not Path(schema_path).exists():
            print(f"ERROR: Provided --schema does not exist: {schema_path}", file=sys.stderr)
            return 5
        entry["schema"] = schema_path

    # Require schema to exist in entry to avoid approving without a schema
    if not entry.get("schema"):
        print(
            "ERROR: No schema set for this tag in manifest and --schema not provided. "
            "Refusing to approve without a schema.",
            file=sys.stderr,
        )
        return 6

    entry["approved_by"] = approver
    entry["approved_at"] = approved_at
    entry["approval_key"] = approval_key

    after = json.dumps(data, sort_keys=True)
    if before == after:
        print("No changes needed; manifest already reflects this approval.")
        # Still proceed to DB write if requested
        if args.db_path:
            try:
                ensure_db(dbp)
                upsert_approval(dbp, ApprovalRecord(domain=domain, tag=tag, expected_key=approval_key, approved_by=approver, approved_at=approved_at))
                print(f"DB updated: {dbp} -> ({domain}, {tag})")
            except Exception as e:
                print(f"WARNING: Failed to write approvals DB: {e}")
        return 0

    # Print a summary of changes
    print("Will apply changes:")
    print(f"  pre_registered: {data.get('pre_registered')}")
    print(f"  allowed_tags includes: {tag}")
    print(f"  approvals['{tag}'].approved_by: {approver}")
    print(f"  approvals['{tag}'].approved_at: {approved_at}")
    print(f"  approvals['{tag}'].approval_key: <hex {len(approval_key)} chars>")
    print(f"  approvals['{tag}'].schema: {entry.get('schema')}")

    if args.dry_run:
        print("Dry-run mode: no file was written.")
        return 0

    try:
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"ERROR: Failed to write manifest: {e}", file=sys.stderr)
        return 7

    # Optional: write to approvals DB as authoritative source
    if args.db_path:
        try:
            ensure_db(dbp)
            upsert_approval(dbp, ApprovalRecord(domain=domain, tag=tag, expected_key=approval_key, approved_by=approver, approved_at=approved_at))
            print(f"DB updated: {dbp} -> ({domain}, {tag})")
        except Exception as e:
            print(f"WARNING: Failed to write approvals DB: {e}")

    print(f"Updated manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
