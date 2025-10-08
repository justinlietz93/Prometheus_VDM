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
import json
import os
import sys
from pathlib import Path
import getpass
from .approval import (
    ensure_db,
    upsert_approval,
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
    sub = p.add_subparsers(dest="cmd", required=False)

    # approve (default/back-compat)
    p_appr = sub.add_parser("approve", help="Approve a tag for a domain (default)")
    p_appr.add_argument("domain", help="Physics domain name (e.g., metriplectic)")
    p_appr.add_argument("tag", help="Tag to approve (e.g., KG-dispersion-v1)")
    p.add_argument(
        "--manifest",
        help="Path to APPROVAL.json (default: Derivation/code/physics/<domain>/APPROVAL.json)",
    )
    p.add_argument("--approver", default=os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz"))
    p.add_argument("--approved-at", dest="approved_at", help="Override ISO-8601 UTC timestamp")
    p.add_argument("--schema", help="Optional schema path to set if missing")
    p.add_argument("--script", help="Run script name (stem or filename) to include in approval HMAC (policy: domain:script:tag)")
    p.add_argument("--dry-run", action="store_true", help="Do not write changes, just print what would change")
    # Approvals DB (required)
    p.add_argument("--db", dest="db_path", required=False, help="Path to approvals DB (SQLite). Defaults to Derivation/code/common/data/approval.db if present, else requires this flag.")
    p.add_argument("--password-prompt", action="store_true", help="Prompt for a password to derive the expected key (never echoes). Required unless VDM_APPROVAL_DB_PASSWORD is set.")

    # set-domain-key
    p_dk = sub.add_parser("set-domain-key", help="Set or update a domain approval key (prioritized over tag secrets)")
    p_dk.add_argument("domain", help="Physics domain name")
    p_dk.add_argument("domain_key", help="Domain approval key (secret); stored in DB")

    # set-tag-secret
    p_ts = sub.add_parser("set-tag-secret", help="Set or update a tag/run secret (fallback if domain key missing)")
    p_ts.add_argument("domain", help="Physics domain name")
    p_ts.add_argument("tag", help="Tag name")
    p_ts.add_argument("tag_secret", help="Tag/run secret (secret); stored in DB")

    # check
    p_ck = sub.add_parser("check", help="Check if a domain:tag has an expected key configured in DB (uses policy domain:script:tag when --script provided)")
    p_ck.add_argument("domain", help="Physics domain name")
    p_ck.add_argument("tag", help="Tag name")
    p_ck.add_argument("--script", help="Run script name (stem or filename) to include in approval HMAC computation")
    args = p.parse_args(argv)

    cmd = args.cmd or "approve"

    # Require password before any DB access
    password = os.getenv("VDM_APPROVAL_DB_PASSWORD")
    if not password and args.password_prompt:
        password = getpass.getpass("Password (won't echo): ")
    if not password:
        print("ERROR: A password is required. Use --password-prompt or set VDM_APPROVAL_DB_PASSWORD.", file=sys.stderr)
        return 3

    # Verify admin password in DB before any other DB operation
    # Resolve DB path: flag > env > default bundled location
    from .approval import DEFAULT_DB_PATH
    dbp: Path
    if args.db_path:
        dbp = Path(args.db_path)
        print(f"[approve_tag] Using approvals DB from --db: {dbp}", file=sys.stderr)
    elif os.getenv("VDM_APPROVAL_DB"):
        dbp = Path(os.getenv("VDM_APPROVAL_DB"))
        print(f"[approve_tag] Using approvals DB from environment VDM_APPROVAL_DB: {dbp}", file=sys.stderr)
    else:
        # Fall back to default path and create on first use
        dbp = DEFAULT_DB_PATH
        print(f"[approve_tag] Using approvals DB at default path: {dbp} (will create if missing)", file=sys.stderr)
    if not ensure_admin_verified(dbp, password):
        print("ERROR: Admin password did not match the stored database password.", file=sys.stderr)
        return 3
    if cmd == "set-domain-key":
        domain = args.domain.strip()
        dkey = args.domain_key
        try:
            ensure_db(dbp)
            set_domain_key(dbp, domain, dkey)
            print(f"Domain key set for '{domain}' in {dbp}")
            return 0
        except Exception as e:
            print(f"ERROR: Failed setting domain key: {e}", file=sys.stderr)
            return 8

    if cmd == "set-tag-secret":
        domain = args.domain.strip()
        tag = args.tag.strip()
        secret = args.tag_secret
        try:
            ensure_db(dbp)
            set_tag_secret(dbp, domain, tag, secret)
            print(f"Tag secret set for '{domain}:{tag}' in {dbp}")
            return 0
        except Exception as e:
            print(f"ERROR: Failed setting tag secret: {e}", file=sys.stderr)
            return 9

    if cmd == "check":
        from .approval import db_get_expected_key, db_get_domain_key, db_get_tag_secret, compute_expected_key
        domain = args.domain.strip()
        tag = args.tag.strip()
        script = (args.script.strip() if getattr(args, "script", None) else None)
        exp = db_get_expected_key(dbp, domain, tag)
        dkey = db_get_domain_key(dbp, domain)
        tsecret = db_get_tag_secret(dbp, domain, tag)
        derived = None
        if tsecret:
            derived = compute_expected_key(tsecret, domain, tag, script)
        elif dkey:
            derived = compute_expected_key(dkey, domain, tag, script)
        print(json.dumps({
            "domain": domain,
            "tag": tag,
            "db_expected_key_exists": bool(exp),
            "has_domain_key": bool(dkey),
            "has_tag_secret": bool(tsecret),
            "derived_from_priority": "tag_secret" if tsecret else ("domain_key" if dkey else None),
            "script": script,
            "match": (exp == derived) if exp and derived else None,
        }, indent=2))
        return 0

    # Default: approve flow
    domain = args.domain.strip()
    tag = args.tag.strip()

    default_manifest = Path("Derivation") / "code" / "physics" / domain.lower() / "APPROVAL.json"
    manifest_path = Path(args.manifest) if args.manifest else default_manifest
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    # Derive the approval key from domain_key or tag_secret in DB (admin password only gates CLI usage)
    from .approval import db_get_domain_key, db_get_tag_secret, compute_expected_key
    dkey = db_get_domain_key(dbp, domain)
    tsecret = db_get_tag_secret(dbp, domain, tag)
    script = (args.script.strip() if getattr(args, "script", None) else None)
    if tsecret:
        approval_key = compute_expected_key(tsecret, domain, tag, script)
    elif dkey:
        approval_key = compute_expected_key(dkey, domain, tag, script)
    else:
        print(
            "ERROR: No domain key or tag secret found in the approvals DB for this domain/tag.\n"
            "Use 'set-domain-key' or 'set-tag-secret' first, then re-run 'approve'.",
            file=sys.stderr,
        )
        return 10

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
        schema_path = args.schema
        if not Path(schema_path).exists():
            print(f"ERROR: Provided --schema does not exist: {schema_path}", file=sys.stderr)
            return 5
        entry["schema"] = schema_path

    if not entry.get("schema"):
        print(
            "ERROR: No schema set for this tag in manifest and --schema not provided. Refusing to approve without a schema.",
            file=sys.stderr,
        )
        return 6

    entry["approved_by"] = approver
    entry["approved_at"] = approved_at
    entry["approval_key"] = approval_key

    after = json.dumps(data, sort_keys=True)
    if before == after:
        print("No changes needed; manifest already reflects this approval.")
        try:
            ensure_db(dbp)
            upsert_approval(dbp, ApprovalRecord(domain=domain, tag=tag, expected_key=approval_key, approved_by=approver, approved_at=approved_at))
            print(f"DB updated: {dbp} -> ({domain}, {tag})")
        except Exception as e:
            print(f"WARNING: Failed to write approvals DB: {e}")
        return 0

    print("Will apply changes:")
    print(f"  pre_registered: {data.get('pre_registered')}")
    print(f"  allowed_tags includes: {tag}")
    print(f"  approvals['{tag}'].approved_by: {approver}")
    print(f"  approvals['{tag}'].approved_at: {approved_at}")
    print(f"  approvals['{tag}'].approval_key: <hex {len(approval_key)} chars>")
    print(f"  approvals['{tag}'].schema: {entry.get('schema')}")
    if script:
        print(f"  approval message scope: domain:{script}:{tag}")

    if args.dry_run:
        print("Dry-run mode: no file was written.")
        return 0

    try:
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"ERROR: Failed to write manifest: {e}", file=sys.stderr)
        return 7

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
