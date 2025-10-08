#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import json
import sys
import os
import hmac
import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone


# --- Module-level DB + admin helpers (single-file design) ---

@dataclass
class ApprovalRecord:
    domain: str
    tag: str
    expected_key: str
    approved_by: str
    approved_at: str


def _iso_now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS approvals (
  domain TEXT NOT NULL,
  tag TEXT NOT NULL,
  expected_key TEXT NOT NULL,
  approved_by TEXT NOT NULL,
  approved_at TEXT NOT NULL,
  PRIMARY KEY(domain, tag)
);
CREATE TABLE IF NOT EXISTS admin (
  id INTEGER PRIMARY KEY CHECK(id = 1),
  password_scheme TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  salt TEXT NOT NULL,
  iterations INTEGER NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS domain_keys (
  domain TEXT PRIMARY KEY,
  domain_key TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tag_secrets (
  domain TEXT NOT NULL,
  tag TEXT NOT NULL,
  tag_secret TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY(domain, tag)
);
"""

# Default approvals DB path fallback (when VDM_APPROVAL_DB is unset)
DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "approval.db"


def _read_env_file(path: Path) -> dict:
    env: dict[str, str] = {}
    try:
        if not path.exists():
            return env
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k:
                env[k] = v
    except Exception:
        return {}
    return env


def _approval_db_path() -> Optional[Path]:
    # 1) OS environment
    env = os.getenv("VDM_APPROVAL_DB")
    if env:
        p = Path(env)
        print(f"[authorization] Using approvals DB from environment variable VDM_APPROVAL_DB: {p}", file=sys.stderr)
        return p
    # 2) .env files (search upward: code -> Derivation -> repo root)
    try:
        code_dir = Path(__file__).resolve().parents[2]
        deriv_dir = Path(__file__).resolve().parents[3]
        repo_root = deriv_dir.parent
        for candidate in [code_dir / ".env", deriv_dir / ".env", repo_root / ".env"]:
            envs = _read_env_file(candidate)
            if "VDM_APPROVAL_DB" in envs:
                p = Path(envs["VDM_APPROVAL_DB"]).expanduser()
                print(f"[authorization] Using approvals DB from env file {candidate}: {p}", file=sys.stderr)
                return p
    except Exception as e:
        print(f"[authorization] Warning: failed scanning .env files for VDM_APPROVAL_DB: {e}", file=sys.stderr)
    # 3) default path if present
    if DEFAULT_DB_PATH.exists():
        print(f"[authorization] Using approvals DB at default path: {DEFAULT_DB_PATH}", file=sys.stderr)
        return DEFAULT_DB_PATH
    return None


def ensure_db(dbp: Path) -> None:
    dbp.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(dbp)) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    try:
        os.chmod(dbp, 0o600)
    except Exception as _e:
        _ = _e


def db_get_expected_key(dbp: Path, domain: str, tag: str) -> Optional[str]:
    if not dbp.exists():
        return None
    try:
        with sqlite3.connect(str(dbp)) as conn:
            cur = conn.execute(
                "SELECT expected_key FROM approvals WHERE domain=? AND tag=?",
                (domain, tag),
            )
            row = cur.fetchone()
            return row[0] if row else None
    except Exception:
        return None


def db_get_domain_key(dbp: Path, domain: str) -> Optional[str]:
    if not dbp.exists():
        return None
    try:
        with sqlite3.connect(str(dbp)) as conn:
            cur = conn.execute("SELECT domain_key FROM domain_keys WHERE domain=?", (domain,))
            row = cur.fetchone()
            return row[0] if row else None
    except Exception:
        return None


def db_get_tag_secret(dbp: Path, domain: str, tag: str) -> Optional[str]:
    if not dbp.exists():
        return None
    try:
        with sqlite3.connect(str(dbp)) as conn:
            cur = conn.execute("SELECT tag_secret FROM tag_secrets WHERE domain=? AND tag=?", (domain, tag))
            row = cur.fetchone()
            return row[0] if row else None
    except Exception:
        return None


def compute_expected_key(secret: str, domain: str, tag: str, script: Optional[str] = None) -> str:
    """Compute HMAC approval key with policy message domain:script:tag.

    If script is None, falls back to domain:tag for backward compatibility.
    """
    if script:
        msg = f"{domain}:{script}:{tag}".encode("utf-8")
    else:
        msg = f"{domain}:{tag}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


def upsert_approval(dbp: Path, rec: ApprovalRecord) -> None:
    ensure_db(dbp)
    with sqlite3.connect(str(dbp)) as conn:
        conn.execute(
            """
            INSERT INTO approvals(domain, tag, expected_key, approved_by, approved_at)
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(domain, tag) DO UPDATE SET
              expected_key=excluded.expected_key,
              approved_by=excluded.approved_by,
              approved_at=excluded.approved_at
            """,
            (rec.domain, rec.tag, rec.expected_key, rec.approved_by, rec.approved_at),
        )
        conn.commit()


def set_domain_key(dbp: Path, domain: str, domain_key: str) -> None:
    ensure_db(dbp)
    with sqlite3.connect(str(dbp)) as conn:
        conn.execute("DELETE FROM domain_keys WHERE domain=?", (domain,))
        conn.execute(
            "INSERT INTO domain_keys(domain, domain_key, created_at) VALUES (?, ?, ?)",
            (domain, domain_key, _iso_now_utc()),
        )
        conn.commit()


def set_tag_secret(dbp: Path, domain: str, tag: str, tag_secret: str) -> None:
    ensure_db(dbp)
    with sqlite3.connect(str(dbp)) as conn:
        conn.execute(
            """
            INSERT INTO tag_secrets(domain, tag, tag_secret, created_at)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(domain, tag) DO UPDATE SET tag_secret=excluded.tag_secret, created_at=excluded.created_at
            """,
            (domain, tag, tag_secret, _iso_now_utc()),
        )
        conn.commit()


# Admin password (PBKDF2-SHA256)
def _pbkdf2(password: str, salt: bytes, iterations: int = 100_000, dklen: int = 32) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen)


def _rand_salt(n: int = 16) -> bytes:
    return os.urandom(n)


def set_admin_password(dbp: Path, password: str, iterations: int = 100_000) -> None:
    ensure_db(dbp)
    salt = _rand_salt()
    digest = _pbkdf2(password, salt, iterations=iterations)
    with sqlite3.connect(str(dbp)) as conn:
        conn.execute("DELETE FROM admin WHERE id=1")
        conn.execute(
            """
            INSERT INTO admin(id, password_scheme, password_hash, salt, iterations, created_at)
            VALUES (1, ?, ?, ?, ?, ?)
            """,
            ('pbkdf2_sha256', digest.hex(), salt.hex(), iterations, _iso_now_utc()),
        )
        conn.commit()


def verify_admin_password(dbp: Path, password: str) -> bool:
    if not dbp.exists():
        return False
    try:
        with sqlite3.connect(str(dbp)) as conn:
            cur = conn.execute("SELECT password_scheme, password_hash, salt, iterations FROM admin WHERE id=1")
            row = cur.fetchone()
            if not row:
                return False
            scheme, hash_hex, salt_hex, iterations = row
            if scheme != 'pbkdf2_sha256':
                return False
            salt = bytes.fromhex(salt_hex)
            calc = _pbkdf2(password, salt, iterations=int(iterations))
            return hmac.compare_digest(calc.hex(), hash_hex)
    except Exception:
        return False


def ensure_admin_verified(dbp: Path, password: str) -> bool:
    ensure_db(dbp)
    with sqlite3.connect(str(dbp)) as conn:
        cur = conn.execute("SELECT COUNT(1) FROM admin WHERE id=1")
        exists = bool(cur.fetchone()[0])
    if not exists:
        set_admin_password(dbp, password)
        return True
    return verify_admin_password(dbp, password)


def check_tag_approval(domain: str, tag: str, allow_unapproved: bool, code_root: Path) -> Tuple[bool, bool, Optional[str]]:
    """
    Enforce proposal-based tag approval with cryptographic approval keys.

    Manifest location priority (case-insensitive domain):
      1) Derivation/code/physics/<domain>/APPROVAL.json
      2) Derivation/<domain>/APPROVAL.json (writings fallback)

    Required for approval:
      - pre_registered = true
                        details.append(
                            "Approval entry missing 'approval_key' — use approve_tag.py to set a domain key or tag secret, then run 'approve' to stamp the manifest."
                        )
      - proposal file exists
      - schema file exists and contains {"tag": "<tag>"}
      - approved_by matches VDM_APPROVER_NAME (default: "Justin K. Lietz")
      - approval_key matches either:
          a) HMAC-SHA256(VDM_APPROVAL_SECRET or VDM_APPROVAL_SECRET_FILE, f"{domain}:{tag}")
          b) The first line of the file at VDM_APPROVAL_KEY_FILE (exact match)

    Returns (approved, engineering_only, proposal_path)
    """
    derivation_dir = code_root.parent  # Derivation/

    # Resolve code domain directory
    code_domain_dir = code_root / "physics" / domain
    if not code_domain_dir.exists() and (code_root / "physics").exists():
        for d in (code_root / "physics").iterdir():
            if d.is_dir() and d.name.lower() == domain.lower():
                code_domain_dir = d
                break

    # Resolve writings domain directory (fallback)
    domain_dir = derivation_dir / domain
    if not domain_dir.exists() and derivation_dir.exists():
        for d in derivation_dir.iterdir():
            if d.is_dir() and d.name.lower() == domain.lower():
                domain_dir = d
                break

    apath = (code_domain_dir / "APPROVAL.json") if (code_domain_dir / "APPROVAL.json").exists() else (domain_dir / "APPROVAL.json")
    approved = False
    proposal: Optional[str] = None

    # (DB helpers provided at module scope)

    def _resolve_path(p: str | Path, base_dir: Optional[Path] = None) -> Path:
        if isinstance(p, Path):
            cand = p
        else:
            cand = Path(p)
        if cand.is_absolute():
            return cand
        repo_root = derivation_dir.parent
        search_bases = [b for b in [base_dir, repo_root, derivation_dir, code_root] if b is not None]
        for base in search_bases:
            trial = (base / cand).resolve()
            if trial.exists():
                return trial
        for dname in ("Derivation", "derivation"):
            trial = (derivation_dir.parent / dname / cand.name).resolve()
            if trial.exists():
                return trial
        return (derivation_dir.parent / cand).resolve()

    def _find_schema_path(tag_: str, manifest: Dict[str, Any]) -> Optional[Path]:
        approvals = manifest.get("approvals", {}) or {}
        if isinstance(approvals, dict):
            entry = approvals.get(tag_)
            if isinstance(entry, dict) and entry.get("schema"):
                return _resolve_path(entry["schema"], base_dir=apath.parent)  # type: ignore[arg-type]
        schemas = manifest.get("schemas", {}) or {}
        if isinstance(schemas, dict) and schemas.get(tag_):
            return _resolve_path(schemas[tag_], base_dir=apath.parent)  # type: ignore[index]
        schema_dir = manifest.get("schema_dir")
        if schema_dir:
            base = _resolve_path(schema_dir, base_dir=apath.parent)
            for nm in (f"{tag_}.schema.json", f"{tag_}.json"):
                cand = base / nm
                if cand.exists():
                    return cand
        for d in (derivation_dir / domain / "schemas", derivation_dir / domain / "SCHEMAS"):
            for nm in (f"{tag_}.schema.json", f"{tag_}.json"):
                cand = d / nm
                if cand.exists():
                    return cand
        return None

    def _validate_schema(tag_: str, schema_path: Path) -> bool:
        try:
            with schema_path.open("r", encoding="utf-8") as fs:
                sdata = json.load(fs)
        except Exception:
            return False
        tag_in_file = sdata.get("tag") or ((sdata.get("metadata") or {}).get("tag") if isinstance(sdata.get("metadata"), dict) else None)
        if str(tag_in_file) != str(tag_):
            return False
        if not ("$schema" in sdata or "type" in sdata):
            return False
        return True

    def _get_expected_key_from_db(domain_: str, tag_: str) -> Optional[str]:
        p = _approval_db_path()
        if not p:
            return None
        return db_get_expected_key(p, domain_, tag_)

    def _compute_expected_from_domain_or_tag(domain_: str, tag_: str, script_: Optional[str]) -> Optional[str]:
        p = _approval_db_path()
        if not p:
            return None
        tsecret = db_get_tag_secret(p, domain_, tag_)
        if tsecret:
            return compute_expected_key(tsecret, domain_, tag_, script_)
        dkey = db_get_domain_key(p, domain_)
        if dkey:
            return compute_expected_key(dkey, domain_, tag_, script_)
        return None

    try:
        if apath.exists():
            with apath.open("r", encoding="utf-8") as f:
                adata: Dict[str, Any] = json.load(f)
            allowed = set(adata.get("allowed_tags", []))
            proposal = adata.get("proposal")
            proposal_path = _resolve_path(proposal, base_dir=apath.parent) if proposal else None
            has_proposal = bool(proposal_path and proposal_path.exists())
            schema_path = _find_schema_path(tag, adata)
            has_schema = bool(schema_path and schema_path.exists())
            schema_valid = bool(schema_path and has_schema and _validate_schema(tag, schema_path))
            approver_expected = os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz")
            approvals = adata.get("approvals", {}) or {}
            appr_entry = approvals.get(tag) if isinstance(approvals, dict) else None
            approved_by_ok = False
            if isinstance(appr_entry, dict):
                who = str(appr_entry.get("approved_by", "")).strip()
                approved_by_ok = (who.lower() == approver_expected.lower()) or (approver_expected.lower() in who.lower())
            approval_key_ok = False
            if isinstance(appr_entry, dict):
                have_key = str(appr_entry.get("approval_key", "")).strip()
                # DB-only strict mode: require DB and match; compute expected by priority (tag secret first, then domain key, then stored expected)
                # Determine run script name from env or argv
                script_name: Optional[str] = os.getenv("VDM_RUN_SCRIPT")
                if not script_name:
                    try:
                        argv0 = sys.argv[0]
                        if argv0:
                            script_name = Path(argv0).stem or Path(argv0).name
                    except Exception:
                        script_name = None
                expected = _compute_expected_from_domain_or_tag(domain, tag, script_name)
                if expected is None:
                    expected = _get_expected_key_from_db(domain, tag)
                approval_key_ok = bool(have_key and expected and (have_key == expected))

            approved = bool(
                adata.get("pre_registered", False)
                and (tag in allowed)
                and has_proposal
                and has_schema
                and schema_valid
                and approved_by_ok
                and approval_key_ok
            )

            if proposal_path:
                os.environ["VDM_POLICY_PROPOSAL"] = str(proposal_path)
            if schema_path:
                os.environ["VDM_POLICY_SCHEMA"] = str(schema_path)
            if appr_entry and isinstance(appr_entry, dict):
                if appr_entry.get("approved_by"):
                    os.environ["VDM_POLICY_APPROVED_BY"] = str(appr_entry.get("approved_by"))
                if appr_entry.get("approved_at"):
                    os.environ["VDM_POLICY_APPROVED_AT"] = str(appr_entry.get("approved_at"))
                if appr_entry.get("approval_key"):
                    os.environ["VDM_POLICY_APPROVAL_KEY_PRESENT"] = "1"
    except Exception:
        approved = False

    if not approved and not allow_unapproved:
        details: list[str] = []
        if not apath.exists():
            details.append(f"Missing approval manifest: {apath}")
        else:
            try:
                with apath.open("r", encoding="utf-8") as f:
                    _adata = json.load(f)
                if tag not in set(_adata.get("allowed_tags", [])):
                    details.append(f"Tag '{tag}' not listed in allowed_tags")
                prop = _adata.get("proposal")
                if not prop:
                    details.append("Field 'proposal' missing in manifest")
                else:
                    pth = (_resolve_path(prop, base_dir=apath.parent))
                    if not pth.exists():
                        details.append(f"Proposal not found at: {pth}")
                sch_path = _find_schema_path(tag, _adata)
                if not sch_path:
                    details.append("Schema path for tag not declared or discoverable (see approvals/schemas/schema_dir)")
                else:
                    if not sch_path.exists():
                        details.append(f"Schema file missing: {sch_path}")
                    else:
                        try:
                            with sch_path.open("r", encoding="utf-8") as fs:
                                sdata = json.load(fs)
                            if str(sdata.get("tag") or ((sdata.get("metadata") or {}).get("tag"))) != str(tag):
                                details.append("Schema 'tag' does not match requested tag")
                        except Exception as e:
                            details.append(f"Schema is not valid JSON: {e}")
                appr = _adata.get("approvals", {}).get(tag) if isinstance(_adata.get("approvals", {}), dict) else None
                if not (isinstance(appr, dict) and str(appr.get("approved_by", "")).strip()):
                    exp = os.getenv("VDM_APPROVER_NAME", "Justin K. Lietz")
                    details.append(f"Approval entry missing or lacks 'approved_by' (expected approver: {exp})")
                if not (isinstance(appr, dict) and str(appr.get("approval_key", "")).strip()):
                    details.append("Approval entry missing 'approval_key' — use approve_tag.py to set a domain key or tag secret, then run 'approve --script <run_script>' to stamp the manifest.")
                else:
                    have_key = str(appr.get("approval_key")).strip()
                    script_name: Optional[str] = os.getenv("VDM_RUN_SCRIPT")
                    if not script_name:
                        try:
                            argv0 = sys.argv[0]
                            if argv0:
                                script_name = Path(argv0).stem or Path(argv0).name
                        except Exception:
                            script_name = None
                    expected = _compute_expected_from_domain_or_tag(domain, tag, script_name)
                    if expected is None:
                        expected = _get_expected_key_from_db(domain, tag)
                    if _approval_db_path() is None:
                        details.append("No approvals DB found (set VDM_APPROVAL_DB or create common/data/approval.db)")
                    elif expected is None:
                        details.append("No DB record or keys for this tag/domain in VDM_APPROVAL_DB; approval denied")
                    elif have_key != expected:
                        details.append("approval_key mismatch against approval DB (VDM_APPROVAL_DB) using policy message 'domain:script:tag'")
            except Exception as e:
                details.append(f"Failed to parse manifest: {e}")

        print(
            (
                f"ERROR: tag '{tag}' is not approved for domain '{domain}'.\n" +
                "\n".join(f" - {d}" for d in details) +
                f"\nTo proceed, create/update {apath} with:\n" +
                "{\n  \"pre_registered\": true,\n  \"proposal\": \"Derivation/<domain>/PROPOSAL_<slug>.md\",\n  \"allowed_tags\": [\"<tag>\"],\n  \"approvals\": {\n    \"<tag>\": {\n      \"schema\": \"Derivation/<domain>/schemas/<tag>.schema.json\",\n      \"approved_by\": \"Justin K. Lietz\",\n      \"approved_at\": \"YYYY-MM-DD\",\n      \"approval_key\": \"<computed via approve_tag.py --script <run_script>>\"\n    }\n  }\n}\n" +
                "Or run with --allow-unapproved to quarantine artifacts (engineering-only)."
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    engineering_only = not approved
    os.environ["VDM_POLICY_APPROVED"] = "1" if approved else "0"
    os.environ["VDM_POLICY_ENGINEERING"] = "1" if engineering_only else "0"
    os.environ["VDM_POLICY_TAG"] = str(tag)
    os.environ["VDM_POLICY_DOMAIN"] = str(domain)
    if proposal:
        os.environ["VDM_POLICY_PROPOSAL"] = str(proposal)
    return approved, engineering_only, proposal
