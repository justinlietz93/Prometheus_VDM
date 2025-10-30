#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import json
import sys
import os
import hmac
import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
import re


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


SCHEMA_SQL_PUBLIC = """
CREATE TABLE IF NOT EXISTS approvals (
  domain TEXT NOT NULL,
  tag TEXT NOT NULL,
  expected_key TEXT NOT NULL,
  approved_by TEXT NOT NULL,
  approved_at TEXT NOT NULL,
  PRIMARY KEY(domain, tag)
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
CREATE TABLE IF NOT EXISTS exempt_scripts (
    script TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    noted_by TEXT
);
"""

SCHEMA_SQL_ADMIN = """
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    password_scheme TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    iterations INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
"""

# Default approvals DB path fallback (when VDM_APPROVAL_DB is unset)
DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "approval.db"
# Default admin DB path (separate file) fallback
DEFAULT_ADMIN_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "approval_admin.db"


def _read_env_file(path: Path) -> dict:
    """Parse a simple .env file.

    - Supports lines like: KEY=value, KEY="value with spaces", export KEY=value
    - Strips inline comments starting with # when not inside quotes
    - Trims surrounding single/double quotes
    """
    env: dict[str, str] = {}
    try:
        if not path.exists():
            return env
        text = path.read_text(encoding="utf-8")
        for raw in text.splitlines():
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            # Drop leading 'export '
            if s.lower().startswith("export "):
                s = s[7:].lstrip()
            if "=" not in s:
                continue
            # Remove inline comments outside quotes
            in_single = False
            in_double = False
            cut_idx = None
            for i, ch in enumerate(s):
                if ch == "'" and not in_double:
                    in_single = not in_single
                elif ch == '"' and not in_single:
                    in_double = not in_double
                elif ch == "#" and not in_single and not in_double:
                    cut_idx = i
                    break
            if cut_idx is not None:
                s = s[:cut_idx].rstrip()
            if "=" not in s:
                continue
            k, v = s.split("=", 1)
            k = k.strip()
            v = v.strip()
            # Trim surrounding quotes if present
            if (len(v) >= 2) and ((v[0] == v[-1]) and v[0] in ('"', "'")):
                v = v[1:-1]
            if k:
                env[k] = v
    except Exception as e:
        print(f"[authorization] Warning: failed reading env file {path}: {e}", file=sys.stderr)
        return env
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
        # No env variable found anywhere; inform user where to set it
        checked_paths = ", ".join(str(x) for x in [code_dir / ".env", deriv_dir / ".env", repo_root / ".env"])
        print(
            "[authorization] No VDM_APPROVAL_DB found in environment or .env files. "
            f"You can set it globally (export VDM_APPROVAL_DB=/path/to/approval.db) or add it to one of: {checked_paths}",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"[authorization] Warning: failed scanning .env files for VDM_APPROVAL_DB: {e}", file=sys.stderr)
    # 3) default path if present
    if DEFAULT_DB_PATH.exists():
        print(f"[authorization] Using approvals DB at default path: {DEFAULT_DB_PATH}", file=sys.stderr)
        return DEFAULT_DB_PATH
    return None


def _approval_admin_db_path() -> Optional[Path]:
    # 1) OS environment
    env = os.getenv("VDM_APPROVAL_ADMIN_DB")
    if env:
        p = Path(env)
        print(f"[authorization] Using admin DB from environment variable VDM_APPROVAL_ADMIN_DB: {p}", file=sys.stderr)
        return p
    # 2) .env files (search upward: code -> Derivation -> repo root)
    try:
        code_dir = Path(__file__).resolve().parents[2]
        deriv_dir = Path(__file__).resolve().parents[3]
        repo_root = deriv_dir.parent
        for candidate in [code_dir / ".env", deriv_dir / ".env", repo_root / ".env"]:
            envs = _read_env_file(candidate)
            if "VDM_APPROVAL_ADMIN_DB" in envs:
                p = Path(envs["VDM_APPROVAL_ADMIN_DB"]).expanduser()
                print(f"[authorization] Using admin DB from env file {candidate}: {p}", file=sys.stderr)
                return p
    except Exception as e:
        print(f"[authorization] Warning: failed scanning .env files for VDM_APPROVAL_ADMIN_DB: {e}", file=sys.stderr)
    # 3) default admin path if present; else fall back to approvals DB path
    if DEFAULT_ADMIN_DB_PATH.exists():
        print(f"[authorization] Using admin DB at default path: {DEFAULT_ADMIN_DB_PATH}", file=sys.stderr)
        return DEFAULT_ADMIN_DB_PATH
    # fallback to the approvals DB file for backward compatibility
    return _approval_db_path()


def ensure_public_db(dbp: Path) -> None:
    dbp.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(dbp)) as conn:
        conn.executescript(SCHEMA_SQL_PUBLIC)
        conn.commit()
    try:
        os.chmod(dbp, 0o600)
    except Exception as _e:
        _ = _e


def ensure_admin_db(dbp: Path) -> None:
    dbp.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(dbp)) as conn:
        conn.executescript(SCHEMA_SQL_ADMIN)
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
    ensure_public_db(dbp)
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
    ensure_public_db(dbp)
    with sqlite3.connect(str(dbp)) as conn:
        conn.execute("DELETE FROM domain_keys WHERE domain=?", (domain,))
        conn.execute(
            "INSERT INTO domain_keys(domain, domain_key, created_at) VALUES (?, ?, ?)",
            (domain, domain_key, _iso_now_utc()),
        )
        conn.commit()


def set_tag_secret(dbp: Path, domain: str, tag: str, tag_secret: str) -> None:
    ensure_public_db(dbp)
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
    ensure_admin_db(dbp)
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
    ensure_admin_db(dbp)
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
                            "Approval entry missing 'approval_key' - use approve_tag.py to set a domain key or tag secret, then run 'approve' to stamp the manifest."
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

    def _sha256_file(p: Path, bufsize: int = 1024 * 1024) -> str:
        h = hashlib.sha256()
        with p.open('rb') as f:
            while True:
                b = f.read(bufsize)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()

    def _compute_salted(base_hex: str, salt_hex: str) -> str:
        payload = f"{base_hex}:{salt_hex}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def _find_prereg_path_for_tag(domain_dir: Path, t: str) -> Optional[Path]:
        # Look for PRE-REGISTRATION.<tag>.json first, then any PRE-REGISTRATION* containing tag, else PRE-REGISTRATION.json
        exact = domain_dir / f"PRE-REGISTRATION.{t}.json"
        if exact.exists():
            return exact
        cands: List[Path] = sorted(domain_dir.glob("PRE-REGISTRATION*.json"))
        for pth in cands:
            if t in pth.name:
                return pth
        fallback = domain_dir / "PRE-REGISTRATION.json"
        if fallback.exists():
            return fallback
        return None

    def _verify_provenance(proposal_path: Optional[Path], prereg_path: Optional[Path], details: List[str]) -> bool:
        """Hard gate: ensure proposal header and prereg salted_provenance exist and match.

        Checks:
          - prereg_path exists and is valid JSON with salted_provenance schema
          - spec file hashes (base and salted) match recomputation
          - proposal header line contains Salted Provenance with salted_sha256, salt_hex, prereg_manifest_sha256
          - header salted_sha256 and salt_hex match prereg recomputation
          - header prereg_manifest_sha256 == sha256(prereg file)
        """
        ok = True
        if prereg_path is None or not prereg_path.exists():
            details.append("Missing preregistration file for this tag (expected PRE-REGISTRATION.<tag>.json)")
            return False
        # Load prereg JSON
        try:
            pdata = json.loads(prereg_path.read_text(encoding='utf-8'))
        except Exception as e:
            details.append(f"Failed to parse preregistration JSON: {e}")
            return False
        prov = pdata.get("salted_provenance")
        if not isinstance(prov, dict):
            details.append("prereg.salted_provenance missing or not an object")
            ok = False
        else:
            schema = prov.get("schema")
            if str(schema) != "vdm.provenance.salted_hash.v1":
                details.append("prereg.salted_provenance.schema must be 'vdm.provenance.salted_hash.v1'")
                ok = False
            items = prov.get("items") if isinstance(prov, dict) else None
            if not isinstance(items, list) or len(items) == 0:
                details.append("prereg.salted_provenance.items is missing or empty")
                ok = False
            else:
                # Verify each item
                for it in items:
                    if not isinstance(it, dict):
                        details.append("prereg.salted_provenance.items contains a non-object item")
                        ok = False
                        continue
                    pth = it.get("path")
                    base_hex = it.get("base_sha256")
                    salt_hex = it.get("salt_hex")
                    salted_hex = it.get("salted_sha256")
                    if not (pth and base_hex and salt_hex and salted_hex):
                        details.append("salted_provenance item missing one of path/base_sha256/salt_hex/salted_sha256")
                        ok = False
                        continue
                    # Resolve path relative to prereg
                    spec_path = _resolve_path(str(pth), base_dir=prereg_path.parent)
                    if not spec_path.exists():
                        details.append(f"Spec referenced in prereg not found: {spec_path}")
                        ok = False
                        continue
                    recomputed_base = _sha256_file(spec_path)
                    if recomputed_base != str(base_hex):
                        details.append(
                            f"Spec base_sha256 mismatch for {spec_path.name}: prereg={base_hex} recomputed={recomputed_base}"
                        )
                        ok = False
                    recomputed_salted = _compute_salted(str(base_hex), str(salt_hex))
                    if recomputed_salted != str(salted_hex):
                        details.append(
                            f"Spec salted_sha256 mismatch for {spec_path.name}: prereg={salted_hex} recomputed={recomputed_salted}"
                        )
                        ok = False
        # Proposal header check
        if proposal_path is None or not proposal_path.exists():
            details.append("Proposal path missing; cannot verify proposal header provenance")
            ok = False
        else:
            try:
                header = proposal_path.read_text(encoding='utf-8')
            except Exception as e:
                details.append(f"Failed reading proposal file: {e}")
                ok = False
                header = ""
            # Look for a Salted Provenance header line
            m = re.search(r"Salted\s+Provenance:\s*spec\s+salted_sha256=([0-9a-fA-F]{64});\s*salt_hex=([0-9a-fA-F]+);\s*prereg_manifest_sha256=([0-9a-fA-F]{64})",
                          header)
            if not m:
                details.append("Proposal header missing 'Salted Provenance' line with salted_sha256/salt_hex/prereg_manifest_sha256")
                ok = False
            else:
                hdr_salted, hdr_salt, hdr_prereg_manifest = m.group(1).lower(), m.group(2).lower(), m.group(3).lower()
                # Compare against prereg recomputation (use first item)
                try:
                    if isinstance(prov, dict) and isinstance(prov.get("items"), list) and len(prov["items"]) > 0:
                        it0 = prov["items"][0]
                        preg_salted = str(it0.get("salted_sha256", "")).lower()
                        preg_salt = str(it0.get("salt_hex", "")).lower()
                        if hdr_salted != preg_salted:
                            details.append(f"Proposal salted_sha256 != prereg salted_sha256 ({hdr_salted} != {preg_salted})")
                            ok = False
                        if hdr_salt != preg_salt:
                            details.append(f"Proposal salt_hex != prereg salt_hex ({hdr_salt} != {preg_salt})")
                            ok = False
                except Exception:
                    pass
                # Compare prereg manifest sha against actual prereg file hash
                actual_manifest = _sha256_file(prereg_path)
                if hdr_prereg_manifest != actual_manifest:
                    details.append(
                        f"Proposal prereg_manifest_sha256 does not match actual prereg file hash ({hdr_prereg_manifest} != {actual_manifest})"
                    )
                    ok = False
        return ok

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

            # New: strong provenance hard gate (proposal header + prereg salted hashes)
            # Only enforce strict provenance when the manifest declares require_provenance = true
            require_prov = bool(adata.get("require_provenance", False))
            prereg_path = _find_prereg_path_for_tag(apath.parent, tag)
            strong_details: list[str] = []
            if require_prov:
                strong_ok = _verify_provenance(proposal_path, prereg_path, strong_details)
            else:
                strong_ok = True

            approved = bool(
                adata.get("pre_registered", False)
                and (tag in allowed)
                and has_proposal
                and has_schema
                and schema_valid
                and approved_by_ok
                and approval_key_ok
                and strong_ok
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
                    details.append("Approval entry missing 'approval_key' - use approve_tag.py to set a domain key or tag secret, then run 'approve --script <run_script>' to stamp the manifest.")
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
                # Strong provenance diagnostics (only if domain requires provenance)
                require_prov = bool(_adata.get("require_provenance", False))
                if require_prov:
                    prereg_path = _find_prereg_path_for_tag(apath.parent, tag)
                    strong_details: list[str] = []
                    _ = _verify_provenance(_resolve_path(_adata.get("proposal"), base_dir=apath.parent) if _adata.get("proposal") else None,
                                            prereg_path,
                                            strong_details)
                    for d in strong_details:
                        details.append(f"provenance: {d}")
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


# --- Enforcement policy helpers (DB-backed) ---


def _normalize_rel_script(p: Path) -> str:
    code_root = Path(__file__).resolve().parents[2]
    rel = p.resolve()
    try:
        rel = rel.relative_to(code_root)
    except Exception as e:
        print(f"[authorization] Note: could not relativize script path to code root ({code_root}): {e}", file=sys.stderr)
    return str(rel).replace("\\", "/").lower()


def db_list_exempt_scripts(dbp: Path) -> set[str]:
    if not dbp.exists():
        return set()
    try:
        with sqlite3.connect(str(dbp)) as conn:
            cur = conn.execute("SELECT script FROM exempt_scripts")
            rows = cur.fetchall()
            return {str(r[0]).lower() for r in rows}
    except Exception as e:
        print(f"[authorization] Warning: failed reading exempt scripts from DB: {e}", file=sys.stderr)
        return set()


def db_upsert_exempt_scripts(dbp: Path, scripts: list[str], noted_by: Optional[str] = None) -> int:
    ensure_public_db(dbp)
    ts = _iso_now_utc()
    count = 0
    try:
        with sqlite3.connect(str(dbp)) as conn:
            for s in scripts:
                conn.execute(
                    "INSERT OR IGNORE INTO exempt_scripts(script, created_at, noted_by) VALUES(?, ?, ?)",
                    (s.lower(), ts, noted_by),
                )
                count += conn.total_changes
            conn.commit()
    except Exception as e:
        print(f"[authorization] Failed to upsert exempt scripts: {e}", file=sys.stderr)
    return count


def db_remove_exempt_scripts(dbp: Path, scripts: list[str]) -> int:
    """Remove scripts from the exempt_scripts table. Returns number of rows affected."""
    if not dbp.exists():
        return 0
    removed = 0
    try:
        with sqlite3.connect(str(dbp)) as conn:
            for s in scripts:
                conn.execute("DELETE FROM exempt_scripts WHERE script=?", (s.lower(),))
                removed += conn.total_changes
            conn.commit()
    except Exception as e:
        print(f"[authorization] Failed to remove exempt scripts: {e}", file=sys.stderr)
    return removed


def should_enforce_approval(domain: str, script_path: Path) -> bool:
    """Return True if approval checks must be enforced for the given script.

            Policy:
                - Global default: enforce approval for all scripts in all domains.
                - Exception: if script's normalized relative path exists in DB table 'exempt_scripts', do not enforce.
    """
    dbp = _approval_db_path()
    if not dbp:
        print(f"[authorization] Warning: no approvals DB configured; safest to enforce", file=sys.stderr)
        return True
    rel = _normalize_rel_script(script_path)
    exempt = db_list_exempt_scripts(dbp)
    return rel not in exempt


# Public getters for paths
def get_approval_db_path() -> Optional[Path]:
    return _approval_db_path()


def get_admin_db_path() -> Optional[Path]:
    return _approval_admin_db_path()
