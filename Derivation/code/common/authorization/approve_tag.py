#!/usr/bin/env python3
"""
Approve a tag for a physics domain by updating the domain APPROVAL.json manifest and the local approvals DB.

DB-only flow (minimal files):
 - Prompts for your admin password (always manual, never from env) and verifies it against the local SQLite DB (VDM_APPROVAL_DB).
 - Computes approval_key = HMAC-SHA256(secret, f"{domain}:{script}:{tag}") where secret priority is:
     1) tag_secret (preferred)
     2) domain_key (fallback)
 - Stamps approved_by and approved_at in the manifest, and upserts the expected key into the DB.
 - Ensures pre_registered=true and allowed_tags contains the tag.
 - Optionally sets the schema path if missing (with --schema).

Notes:
 - The admin password gates DB access/verification; it is NOT used as the approval HMAC secret.
 - No environment secrets or key files are used; secrets live in the approvals DB.
 - The password is ALWAYS entered interactively; environment variables are ignored by design.
 - Read-only commands (check, exempt list) do not require a password; write operations do.

Usage examples:
    export VDM_APPROVAL_DB=/secure/vdm_approvals.sqlite3
    # Approve a tag (script-scoped HMAC) - provide --script to scope the approval key
    python3 Derivation/code/common/authorization/approve_tag.py approve metriplectic KG-dispersion-v1 \
        --script run_metriplectic.py --db "$VDM_APPROVAL_DB"

    # Exempt management (scripts that skip approval checks)
    python3 Derivation/code/common/authorization/approve_tag.py exempt list --db "$VDM_APPROVAL_DB"
    python3 Derivation/code/common/authorization/approve_tag.py exempt add Derivation/code/physics/metriplectic/run_metriplectic.py \
        --noted-by "Justin K. Lietz" --db "$VDM_APPROVAL_DB"
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
    ensure_public_db,
    upsert_approval,
    ApprovalRecord,
    ensure_admin_verified,
    set_domain_key,
    set_tag_secret,
    DEFAULT_DB_PATH,
    get_admin_db_path,
    get_approval_db_path,
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
    p_appr.add_argument(
        "--manifest",
        help="Path to APPROVAL.json (default: Derivation/code/physics/<domain>/APPROVAL.json)",
    )
    p_appr.add_argument("--approver", default=os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz"))
    p_appr.add_argument("--approved-at", dest="approved_at", help="Override ISO-8601 UTC timestamp")
    p_appr.add_argument("--schema", help="Optional schema path to set if missing")
    p_appr.add_argument("--script", help="Run script name (stem or filename) to include in approval HMAC (policy: domain:script:tag)")
    p_appr.add_argument("--dry-run", action="store_true", help="Do not write changes, just print what would change")
    # Approvals DB can also be passed after subcommand
    p_appr.add_argument("--db", dest="db_path", required=False, help="Path to approvals DB (SQLite). Defaults to Derivation/code/common/data/approval.db if present, else requires this flag.")

    # Approvals DB (top-level, applies when passed before subcommand)
    p.add_argument("--db", dest="db_path", required=False, help="Path to approvals DB (SQLite). Defaults to Derivation/code/common/data/approval.db if present, else requires this flag.")


    # set-domain-key
    p_dk = sub.add_parser("set-domain-key", help="Set or update a domain approval key (fallback when no tag_secret is set)")
    p_dk.add_argument("domain", help="Physics domain name")
    p_dk.add_argument("domain_key", help="Domain approval key (secret); stored in DB")

    # set-tag-secret
    p_ts = sub.add_parser("set-tag-secret", help="Set or update a tag/run secret (preferred over domain_key)")
    p_ts.add_argument("domain", help="Physics domain name")
    p_ts.add_argument("tag", help="Tag name")
    p_ts.add_argument("tag_secret", help="Tag/run secret (secret); stored in DB")

    # check
    p_ck = sub.add_parser("check", help="Check if a domain:tag has an expected key configured in DB (uses policy domain:script:tag when --script provided)")
    p_ck.add_argument("domain", help="Physics domain name")
    p_ck.add_argument("tag", help="Tag name")
    p_ck.add_argument("--script", help="Run script name (stem or filename) to include in approval HMAC computation")

    # exempt management
    p_ex = sub.add_parser("exempt", help="Manage script-based enforcement exemptions in approvals DB")
    ex_sub = p_ex.add_subparsers(dest="ex_cmd", required=True)
    p_ex_list = ex_sub.add_parser("list", help="List all exempt scripts")
    p_ex_add = ex_sub.add_parser("add", help="Add one or more scripts to exemptions (normalized relative path)")
    p_ex_add.add_argument("scripts", nargs="+", help="Script paths (relative to Derivation/code) or absolute")
    p_ex_add.add_argument("--noted-by", dest="noted_by", default=os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz"))
    p_ex_rm = ex_sub.add_parser("remove", help="Remove one or more scripts from exemptions")
    p_ex_rm.add_argument("scripts", nargs="+", help="Script paths to remove")
    p_ex_snap = ex_sub.add_parser("snapshot", help="Scan Derivation/code/physics for existing scripts and add them as exempt")

    # status (read-only)
    p_st = sub.add_parser("status", help="Show initialization status of approvals (public) DB and admin DB")
    args = p.parse_args(argv)

    cmd = args.cmd or "approve"

    # Verify admin password in DB before any other DB operation
    # Resolve DB path: flag > helper (env/.env w/ repairs) > default bundled location
    dbp: Path
    if args.db_path:
        dbp = Path(args.db_path)
        print(f"[approve_tag] Using approvals DB from --db: {dbp}", file=sys.stderr)
    else:
        resolved = get_approval_db_path()
        if resolved:
            dbp = resolved
            print(f"[approve_tag] Using approvals DB resolved by helper: {dbp}", file=sys.stderr)
        else:
            # Fall back to default path and create on first use
            dbp = DEFAULT_DB_PATH
            print(f"[approve_tag] Using approvals DB at default path: {dbp} (will create if missing)", file=sys.stderr)
    # Determine if this command mutates the approvals DB (requires admin verification)
    write_ops = (
        (cmd in {"approve", "set-domain-key", "set-tag-secret"}) or
        (cmd == "exempt" and getattr(args, "ex_cmd", None) in {"add", "remove", "snapshot"})
    )
    if write_ops:
        # Resolve admin DB path (may differ from public approvals DB)
        admin_db = get_admin_db_path()
        if not admin_db:
            admin_db = dbp
        try:
            password = getpass.getpass("Admin password for approvals DB (won't echo): ")
        except Exception as e:
            print(f"ERROR: Unable to read password: {e}", file=sys.stderr)
            return 3
        if not password:
            print("ERROR: A password is required.", file=sys.stderr)
            return 3
        if not ensure_admin_verified(admin_db, password):
            print("ERROR: Admin password did not match the stored database password.", file=sys.stderr)
            return 3
    if cmd == "set-domain-key":
        domain = args.domain.strip()
        dkey = args.domain_key
        try:
            ensure_public_db(dbp)
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
            ensure_public_db(dbp)
            set_tag_secret(dbp, domain, tag, secret)
            print(f"Tag secret set for '{domain}:{tag}' in {dbp}")
            return 0
        except Exception as e:
            print(f"ERROR: Failed setting tag secret: {e}", file=sys.stderr)
            return 9

    if cmd == "status":
        # Read-only status of DB initialization (no password required)
        import sqlite3  # local import to keep dependencies tight
        from .approval import get_admin_db_path

        def _tables_at(path: Path) -> set[str]:
            if not path.exists():
                return set()
            try:
                with sqlite3.connect(str(path)) as conn:
                    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    return {r[0] for r in cur.fetchall()}
            except Exception:
                return set()

        admin_path = get_admin_db_path() or dbp
        public_expected = {"approvals", "domain_keys", "tag_secrets", "exempt_scripts"}
        admin_expected = {"admin"}
        public_present = _tables_at(dbp)
        admin_present = _tables_at(admin_path)
        out = {
            "public_db": {
                "path": str(dbp),
                "exists": Path(dbp).exists(),
                "tables_present": sorted(public_present),
                "tables_missing": sorted(public_expected - public_present),
            },
            "admin_db": {
                "path": str(admin_path),
                "exists": Path(admin_path).exists(),
                "tables_present": sorted(admin_present),
                "tables_missing": sorted(admin_expected - admin_present),
            },
        }
        print(json.dumps(out, indent=2))
        return 0

    if cmd == "exempt":
        from .approval import db_list_exempt_scripts, db_upsert_exempt_scripts, db_remove_exempt_scripts, _normalize_rel_script
        # list
        if args.ex_cmd == "list":
            ex = sorted(db_list_exempt_scripts(dbp))
            print(json.dumps({"exempt_scripts": ex, "count": len(ex)}, indent=2))
            return 0
        # add
        if args.ex_cmd == "add":
            scripts = []
            for s in args.scripts:
                pth = Path(s)
                if not pth.is_absolute():
                    pth = Path("Derivation") / "code" / pth
                scripts.append(_normalize_rel_script(pth))
            n = db_upsert_exempt_scripts(dbp, scripts, noted_by=getattr(args, "noted_by", None))
            print(json.dumps({"added": n, "scripts": scripts}, indent=2))
            return 0
        # remove
        if args.ex_cmd == "remove":
            scripts = [s.lower() for s in args.scripts]
            n = db_remove_exempt_scripts(dbp, scripts)
            print(json.dumps({"removed": n, "scripts": scripts}, indent=2))
            return 0
        # snapshot existing scripts
        if args.ex_cmd == "snapshot":
            code_root = Path("Derivation") / "code"
            physics = code_root / "physics"
            if not physics.exists():
                print("ERROR: No physics directory found to snapshot.", file=sys.stderr)
                return 11
            scripts: list[str] = []
            for d in physics.glob("**/*.py"):
                scripts.append(_normalize_rel_script(d))
            n = db_upsert_exempt_scripts(dbp, scripts, noted_by=os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz"))
            print(json.dumps({"snapshotted": n, "total_seen": len(scripts)}, indent=2))
            return 0

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
            ensure_public_db(dbp)
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
        ensure_public_db(dbp)
        upsert_approval(dbp, ApprovalRecord(domain=domain, tag=tag, expected_key=approval_key, approved_by=approver, approved_at=approved_at))
        print(f"DB updated: {dbp} -> ({domain}, {tag})")
    except Exception as e:
        print(f"WARNING: Failed to write approvals DB: {e}")

    print(f"Updated manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
