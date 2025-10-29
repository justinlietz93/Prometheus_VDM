#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Lightweight results database helper.

Contract:
 - One SQLite database per physics domain under Derivation/code/outputs/databases/<domain>.sqlite3
 - One table per experiment script (table name = sanitized script stem, e.g., kg_light_cone)
 - Rows keyed by (tag, batch) where batch is incremental per tag within that table
 - Stores params/metrics/artifacts as JSON text; status and timestamps for lifecycle
 - Marks preflight rows explicitly to avoid confusion with first-class experiments

Minimal API:
 - get_db_path(domain) -> Path
 - ensure_table(db_path, experiment) -> table_name
 - begin_run(domain, experiment, tag, params=None, engineering_only=False) -> RunHandle
 - log_metrics(handle, metrics)
 - add_artifacts(handle, artifacts)
 - end_run_success(handle, metrics=None)
 - end_run_failed(handle, metrics=None, error_message=None)

Notes:
 - Table column 'batch' increments per tag within the same table; (tag, batch) is UNIQUE.
 - A convenience 'run_slug' is stored as f"{experiment}_{tag}_b{batch:03d}" for consistent artifact naming.
 - Caller should use io_paths for files; you can reference file paths in artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import sqlite3
import os
from typing import Any, Dict, Optional


# Local outputs root (aligned with common.io_paths)
# File lives in Derivation/code/common/data/, so parents[2] is Derivation/code
CODE_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = CODE_ROOT / "outputs"
DB_DIR = OUTPUTS / "databases"


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_db_path(domain: str) -> Path:
    """Return the per-domain results DB path and ensure parent directories exist."""
    safe_domain = _sanitize_identifier(domain)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return DB_DIR / f"{safe_domain}.sqlite3"


def _sanitize_identifier(name: str) -> str:
    """Sanitize arbitrary names to safe SQLite identifier tokens (letters, digits, underscore).
    Lowercases and replaces non [a-zA-Z0-9_] with underscores; trims leading digits with a prefix.
    """
    s = re.sub(r"[^0-9a-zA-Z_]", "_", str(name).strip())
    if not s:
        s = "_"
    if s[0].isdigit():
        s = f"t_{s}"
    return s.lower()


def _assert_safe_identifier(name: str) -> None:
    """Raise ValueError if name isn't a safe identifier (lowercase letters, digits, underscore)."""
    if not re.fullmatch(r"[a-z0-9_]+", name):
        raise ValueError(f"Unsafe identifier: {name!r}")


def _ensure_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")


def ensure_table(db_path: Path, experiment: str, variant: Optional[str] = None) -> str:
    """Create a table for the experiment (and optional variant) if it doesn't exist.
    Returns the table name. The table has a UNIQUE(tag, batch) constraint to enforce
    incremental batches per tag.
    - variant allows creating sibling tables like run_xyz_preflight while resolving
      the actual script path to run_xyz.py.
    """
    _ensure_db(db_path)
    base = Path(experiment).stem if experiment.endswith(".py") else experiment
    table = _sanitize_identifier(base)
    if variant:
        table = f"{table}_{_sanitize_identifier(variant)}"
    _assert_safe_identifier(table)
    ddl = f"""
    CREATE TABLE IF NOT EXISTS "{table}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT NOT NULL,
        batch INTEGER NOT NULL,
        run_script TEXT NOT NULL,
        run_slug TEXT NOT NULL,
        engineering_only INTEGER NOT NULL,
        preflight INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        error_message TEXT,
        params_json TEXT,
        metrics_json TEXT,
        artifacts_json TEXT,
        row_hash TEXT NOT NULL,
        UNIQUE(tag, batch)
    );
    """
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(ddl)
        # Migration: ensure 'preflight' column exists for older tables
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(f'PRAGMA table_info("{table}")')  # nosec B608
            cols = {str(r[1]).lower() for r in cur.fetchall()}  # name at index 1
        except Exception as _e:
            cols = set()
        if "preflight" not in cols:
            conn.execute(f'ALTER TABLE "{table}" ADD COLUMN preflight INTEGER NOT NULL DEFAULT 0')  # nosec B608
        conn.commit()
    return table


def _find_case_insensitive_dir(base: Path, name: str) -> Optional[Path]:
    if (base / name).exists():
        return base / name
    lower = name.lower()
    if base.exists():
        for d in base.iterdir():
            if d.is_dir() and d.name.lower() == lower:
                return d
    return None


def _resolve_experiment_script(domain: str, experiment: str) -> Path:
    """Resolve the experiment script path.
    Accepts absolute/relative paths; otherwise, searches Derivation/code/physics/<domain> for <experiment>[.py].
    """
    p = Path(experiment)
    # If it's a direct path (absolute or relative) and exists, use it
    if p.exists():
        return p.resolve()
    # Search under code/physics/<domain>
    physics_dir = CODE_ROOT / "physics"
    domain_dir = _find_case_insensitive_dir(physics_dir, domain)
    if domain_dir is None:
        raise FileNotFoundError(f"Domain directory not found under {physics_dir}: {domain}")
    # Candidate filenames
    candidates: list[Path] = []
    if p.suffix == ".py":
        candidates.append(domain_dir / p.name)
    else:
        candidates.append(domain_dir / f"{p.name}.py")
    # Also search by stem match
    if domain_dir.exists():
        for f in domain_dir.glob("*.py"):
            if f.stem == p.name:
                candidates.append(f)
    for c in candidates:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError(f"Experiment script not found for '{experiment}' in domain '{domain}'. Tried: {', '.join(str(c) for c in candidates)}")


def _find_manifest_path(domain: str) -> Optional[Path]:
    """Locate the approval manifest for a domain. Prefer code path, then writings fallback.
    Checks for APPROVAL.json primarily, then APPROVALS.json as a fallback.
    """
    physics_dir = CODE_ROOT / "physics"
    domain_dir_code = _find_case_insensitive_dir(physics_dir, domain)
    derivation_dir = CODE_ROOT.parent
    domain_dir_writing = _find_case_insensitive_dir(derivation_dir, domain)
    names = ("APPROVAL.json", "APPROVALS.json")
    for d in [domain_dir_code, domain_dir_writing]:
        if d is None:
            continue
        for nm in names:
            cand = d / nm
            if cand.exists():
                return cand
    return None


def _ensure_tag_allowed(domain: str, tag: str) -> None:
    """Validate that the tag appears in the domain's approval manifest.
    Requires allowed_tags to contain the tag and approvals[tag] to exist.
    Skipped when RESULTSDB_SKIP_APPROVAL_CHECK=1 is set.
    """
    if os.getenv("RESULTSDB_SKIP_APPROVAL_CHECK") == "1":
        return
    # If policy has already marked this run as approved, we can trust it; still attempt a lightweight check.
    mpath = _find_manifest_path(domain)
    if not mpath:
        raise FileNotFoundError(
            f"Approval manifest not found for domain '{domain}'. Expected at code or derivation domain folder (APPROVAL.json)."
        )
    try:
        data = json.loads(mpath.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Failed to parse approval manifest JSON at {mpath}: {e}")
    allowed = set(data.get("allowed_tags", []) or [])
    if tag not in allowed:
        raise ValueError(f"Tag '{tag}' not listed in allowed_tags in {mpath}")
    approvals = data.get("approvals") or {}
    if not (isinstance(approvals, dict) and tag in approvals):
        raise ValueError(f"Missing approvals entry for tag '{tag}' in {mpath}")


def _next_batch_for_tag(conn: sqlite3.Connection, table: str, tag: str) -> int:
    _assert_safe_identifier(table)
    # nosec B608: table name is sanitized and validated via _assert_safe_identifier
    cur = conn.execute(f"SELECT COALESCE(MAX(batch), 0) FROM \"{table}\" WHERE tag=?", (tag,))  # nosec B608
    last = cur.fetchone()[0] or 0
    return int(last) + 1


@dataclass(frozen=True)
class RunHandle:
    db_path: Path
    table: str
    tag: str
    batch: int


def begin_run(
    domain: str,
    experiment: str,
    tag: str,
    params: Optional[Dict[str, Any]] = None,
    engineering_only: bool = False,
    *,
    variant: Optional[str] = None,
    preflight: bool = False,
) -> RunHandle:
    """Start a run row and return a handle with (tag, batch).
    - Creates the per-domain DB and experiment table if missing
    - Computes the next batch for the tag and inserts a 'running' row
    """
    # Resolve experiment script and validate presence
    script_path = _resolve_experiment_script(domain, experiment)
    run_script = script_path.name
    # Set env to help downstream authorization policy (domain:script:tag HMAC scope)
    os.environ.setdefault("VDM_RUN_SCRIPT", Path(run_script).stem)

    # Approval enforcement: for qualifying scripts/domains, require manifest tag + full approval
    from ..authorization.approval import should_enforce_approval, check_tag_approval
    enforce = should_enforce_approval(domain, script_path)
    if enforce and not preflight:
        # First ensure tag is declared in manifest
        _ensure_tag_allowed(domain, tag)
        # Then run full approval guard (raises on failure unless engineering_only allowed)
        code_root = CODE_ROOT
        approved, eng_only_flag, _proposal = check_tag_approval(domain, tag, allow_unapproved=engineering_only, code_root=code_root)
        # If not approved and not engineering_only, check_tag_approval would have exited; if engineering_only, mark flag
        engineering_only = engineering_only or eng_only_flag

    # Enforce preflight/table-variant alignment to prevent mixups
    if preflight:
        # Default the table variant to 'preflight' if not provided
        if variant is None:
            variant = "preflight"
        elif "preflight" not in str(variant).lower():
            raise ValueError("Preflight runs must use a 'preflight' table variant (variant='preflight').")
    else:
        # Disallow writing real runs into preflight tables
        if variant is not None and "preflight" in str(variant).lower():
            raise ValueError("Real runs cannot target a preflight table variant. Omit variant or use a non-preflight variant.")

    # Prepare DB path and validate directory permissions
    db_path = get_db_path(domain)
    if not db_path.parent.exists():
        raise FileNotFoundError(f"Results DB directory missing: {db_path.parent}")
    if not os.access(db_path.parent, os.W_OK):
        raise PermissionError(f"Results DB directory not writable: {db_path.parent}")

    # Ensure table exists (creates DB if needed)
    table = ensure_table(db_path, experiment, variant=variant)
    # Verify DB file exists post-initialization
    if not db_path.exists():
        raise FileNotFoundError(f"Results DB was not created at: {db_path}")

    started_at = _iso_utc_now()
    with sqlite3.connect(str(db_path)) as conn:
        # Compute next batch for the tag
        batch = _next_batch_for_tag(conn, table, tag)
        run_slug = f"{_sanitize_identifier(Path(experiment).stem)}_{_sanitize_identifier(tag)}_b{batch:03d}"
        _assert_safe_identifier(table)
        # Build SQL separately to tag with nosec on the assignment line (Bandit B608)
        sql_insert = f'INSERT INTO "{table}" (tag, batch, run_script, run_slug, engineering_only, preflight, status, started_at, params_json, metrics_json, artifacts_json, row_hash) VALUES (?, ?, ?, ?, ?, ?, \'running\', ?, ?, ?, ?, ?)'  # nosec B608
        params_json = _canonical_json(params)
        metrics_json = _canonical_json({})
        artifacts_json = _canonical_json({})
        row_hash = _compute_row_hash_payload(
            tag=tag,
            batch=batch,
            run_script=run_script,
            run_slug=run_slug,
            engineering_only=1 if engineering_only else 0,
            preflight=1 if preflight else 0,
            status="running",
            started_at=started_at,
            finished_at=None,
            error_message=None,
            params_json=params_json,
            metrics_json=metrics_json,
            artifacts_json=artifacts_json,
        )
        conn.execute(
            sql_insert,
            (
                tag,
                batch,
                run_script,
                run_slug,
                1 if engineering_only else 0,
                1 if preflight else 0,
                started_at,
                params_json,
                metrics_json,
                artifacts_json,
                row_hash,
            ),
        )
        conn.commit()
    return RunHandle(db_path=db_path, table=table, tag=tag, batch=batch)


def begin_preflight_run(domain: str, experiment: str, tag: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> RunHandle:
    """Begin a preflight run row safely (engineering_only, preflight table).
    Policy:
    - Preflight rows use a fixed tag value 'preflight' (caller-provided tag is ignored).
    - Forces variant='preflight' and preflight=True to prevent mixups.
    - Skips manifest/approval enforcement internally via preflight flag.
    """
    fixed_tag = "preflight"
    return begin_run(
        domain,
        experiment,
        fixed_tag,
        params=params,
        engineering_only=True,
        variant="preflight",
        preflight=True,
    )


def begin_real_run(domain: str, experiment: str, tag: str, params: Optional[Dict[str, Any]] = None, *, engineering_only: bool = False) -> RunHandle:
    """Begin a real (non-preflight) run row safely (base table only)."""
    return begin_run(
        domain,
        experiment,
        tag,
        params=params,
        engineering_only=engineering_only,
        variant=None,
        preflight=False,
    )


def get_preflight_runs(domain: str, experiment: str, tag: Optional[str] = None) -> list[dict]:
    """Return only preflight rows for the given runner script.
    - Targets the 'preflight' table variant explicitly
    - Adds a defensive WHERE preflight=1 filter
    """
    db_path = get_db_path(domain)
    table = ensure_table(db_path, experiment, variant="preflight")
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        _assert_safe_identifier(table)
        if tag is None:
            sql = f"SELECT * FROM \"{table}\" WHERE preflight=1 ORDER BY tag, batch"  # nosec B608
            cur = conn.execute(sql)
        else:
            sql = f"SELECT * FROM \"{table}\" WHERE tag=? AND preflight=1 ORDER BY batch"  # nosec B608
            cur = conn.execute(sql, (tag,))
        rows = cur.fetchall()
    out: list[dict] = []
    for r in rows:
        d = {k: r[k] for k in r.keys()}
        for col in ("params_json", "metrics_json", "artifacts_json"):
            if d.get(col):
                try:
                    d[col] = json.loads(d[col])
                except Exception:
                    d[col] = d[col]
        out.append(d)
    return out


def get_latest_preflight(domain: str, experiment: str) -> Optional[dict]:
    """Return the most recent preflight row for the given runner script, or None if none exist.
    Uses the preflight table variant and selects the highest batch for the fixed tag 'preflight'.
    """
    db_path = get_db_path(domain)
    table = ensure_table(db_path, experiment, variant="preflight")
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        _assert_safe_identifier(table)
        # Prefer ordering by batch for the fixed tag; fall back to started_at if needed in the future
        sql = f"SELECT * FROM \"{table}\" WHERE preflight=1 AND tag=? ORDER BY batch DESC LIMIT 1"  # nosec B608
        cur = conn.execute(sql, ("preflight",))
        row = cur.fetchone()
        if not row:
            return None
        d = {k: row[k] for k in row.keys()}
        for col in ("params_json", "metrics_json", "artifacts_json"):
            if d.get(col):
                try:
                    d[col] = json.loads(d[col])
                except Exception:
                    d[col] = d[col]
        return d

def get_real_runs(domain: str, experiment: str, tag: Optional[str] = None) -> list[dict]:
    """Return only real (non-preflight) rows from the base table."""
    db_path = get_db_path(domain)
    table = ensure_table(db_path, experiment, variant=None)
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        _assert_safe_identifier(table)
        if tag is None:
            sql = f"SELECT * FROM \"{table}\" WHERE COALESCE(preflight,0)=0 ORDER BY tag, batch"  # nosec B608
            cur = conn.execute(sql)
        else:
            sql = f"SELECT * FROM \"{table}\" WHERE tag=? AND COALESCE(preflight,0)=0 ORDER BY batch"  # nosec B608
            cur = conn.execute(sql, (tag,))
        rows = cur.fetchall()
    out: list[dict] = []
    for r in rows:
        d = {k: r[k] for k in r.keys()}
        for col in ("params_json", "metrics_json", "artifacts_json"):
            if d.get(col):
                try:
                    d[col] = json.loads(d[col])
                except Exception:
                    d[col] = d[col]
        out.append(d)
    return out


def _merge_json(existing_json: Optional[str], new_obj: Dict[str, Any]) -> str:
    try:
        base = json.loads(existing_json) if existing_json else {}
        if not isinstance(base, dict):
            base = {"_": base}
    except Exception:
        base = {}
    base.update(new_obj or {})
    return json.dumps(base, sort_keys=True, separators=(",", ":"))


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj or {}, sort_keys=True, separators=(",", ":"))


def _compute_row_hash_payload(
    *,
    tag: str,
    batch: int,
    run_script: str,
    run_slug: str,
    engineering_only: int,
    preflight: int,
    status: str,
    started_at: Optional[str],
    finished_at: Optional[str],
    error_message: Optional[str],
    params_json: str,
    metrics_json: str,
    artifacts_json: str,
) -> str:
    import hashlib
    payload = {
        "tag": tag,
        "batch": batch,
        "run_script": run_script,
        "run_slug": run_slug,
        "engineering_only": engineering_only,
        "preflight": preflight,
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "error_message": error_message,
        "params_json": params_json or "{}",
        "metrics_json": metrics_json or "{}",
        "artifacts_json": artifacts_json or "{}",
    }
    s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def log_metrics(handle: RunHandle, metrics: Dict[str, Any]) -> None:
    with sqlite3.connect(str(handle.db_path)) as conn:
        _assert_safe_identifier(handle.table)
        sql_sel = f"SELECT run_script, run_slug, engineering_only, preflight, status, started_at, finished_at, error_message, params_json, metrics_json, artifacts_json FROM \"{handle.table}\" WHERE tag=? AND batch=?"  # nosec B608
        cur = conn.execute(sql_sel, (handle.tag, handle.batch))
        row = cur.fetchone()
        if not row:
            return
        run_script, run_slug, eng, preflight, status, started_at, finished_at, error_message, params_json, metrics_json, artifacts_json = row
        merged_metrics = _merge_json(metrics_json, metrics)
        new_hash = _compute_row_hash_payload(
            tag=handle.tag,
            batch=handle.batch,
            run_script=run_script,
            run_slug=run_slug,
            engineering_only=int(eng),
            preflight=int(preflight),
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            error_message=error_message,
            params_json=params_json or "{}",
            metrics_json=merged_metrics,
            artifacts_json=artifacts_json or "{}",
        )
        sql_upd = f"UPDATE \"{handle.table}\" SET metrics_json=?, row_hash=? WHERE tag=? AND batch=?"  # nosec B608
        conn.execute(sql_upd, (merged_metrics, new_hash, handle.tag, handle.batch))
        conn.commit()


def add_artifacts(handle: RunHandle, artifacts: Dict[str, Any]) -> None:
    with sqlite3.connect(str(handle.db_path)) as conn:
        _assert_safe_identifier(handle.table)
        sql_sel = f"SELECT run_script, run_slug, engineering_only, preflight, status, started_at, finished_at, error_message, params_json, metrics_json, artifacts_json FROM \"{handle.table}\" WHERE tag=? AND batch=?"  # nosec B608
        cur = conn.execute(sql_sel, (handle.tag, handle.batch))
        row = cur.fetchone()
        if not row:
            return
        run_script, run_slug, eng, preflight, status, started_at, finished_at, error_message, params_json, metrics_json, artifacts_json = row
        merged_artifacts = _merge_json(artifacts_json, artifacts)
        new_hash = _compute_row_hash_payload(
            tag=handle.tag,
            batch=handle.batch,
            run_script=run_script,
            run_slug=run_slug,
            engineering_only=int(eng),
            preflight=int(preflight),
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            error_message=error_message,
            params_json=params_json or "{}",
            metrics_json=metrics_json or "{}",
            artifacts_json=merged_artifacts,
        )
        sql_upd = f"UPDATE \"{handle.table}\" SET artifacts_json=?, row_hash=? WHERE tag=? AND batch=?"  # nosec B608
        conn.execute(sql_upd, (merged_artifacts, new_hash, handle.tag, handle.batch))
        conn.commit()


def end_run_success(handle: RunHandle, metrics: Optional[Dict[str, Any]] = None) -> None:
    finished_at = _iso_utc_now()
    with sqlite3.connect(str(handle.db_path)) as conn:
        _assert_safe_identifier(handle.table)
        sql_sel = f"SELECT run_script, run_slug, engineering_only, preflight, status, started_at, metrics_json, artifacts_json, params_json FROM \"{handle.table}\" WHERE tag=? AND batch=?"  # nosec B608
        cur = conn.execute(sql_sel, (handle.tag, handle.batch))
        row = cur.fetchone()
        if not row:
            return
        run_script, run_slug, eng, preflight, _status, started_at, metrics_json, artifacts_json, params_json = row
        new_metrics = _merge_json(metrics_json, metrics) if metrics else (metrics_json or "{}")
        new_hash = _compute_row_hash_payload(
            tag=handle.tag,
            batch=handle.batch,
            run_script=run_script,
            run_slug=run_slug,
            engineering_only=int(eng),
            preflight=int(preflight),
            status="success",
            started_at=started_at,
            finished_at=finished_at,
            error_message=None,
            params_json=params_json or "{}",
            metrics_json=new_metrics,
            artifacts_json=artifacts_json or "{}",
        )
        if metrics:
            sql_upd = f"UPDATE \"{handle.table}\" SET metrics_json=?, status='success', finished_at=?, row_hash=? WHERE tag=? AND batch=?"  # nosec B608
            conn.execute(sql_upd, (new_metrics, finished_at, new_hash, handle.tag, handle.batch))
        else:
            sql_upd2 = f"UPDATE \"{handle.table}\" SET status='success', finished_at=?, row_hash=? WHERE tag=? AND batch=?"  # nosec B608
            conn.execute(sql_upd2, (finished_at, new_hash, handle.tag, handle.batch))
        conn.commit()


def end_run_failed(handle: RunHandle, metrics: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None) -> None:
    finished_at = _iso_utc_now()
    with sqlite3.connect(str(handle.db_path)) as conn:
        _assert_safe_identifier(handle.table)
        sql_sel = f"SELECT run_script, run_slug, engineering_only, preflight, status, started_at, metrics_json, artifacts_json, params_json FROM \"{handle.table}\" WHERE tag=? AND batch=?"  # nosec B608
        cur = conn.execute(sql_sel, (handle.tag, handle.batch))
        row = cur.fetchone()
        if not row:
            return
        run_script, run_slug, eng, preflight, _status, started_at, metrics_json, artifacts_json, params_json = row
        new_metrics = _merge_json(metrics_json, metrics) if metrics else (metrics_json or "{}")
        new_hash = _compute_row_hash_payload(
            tag=handle.tag,
            batch=handle.batch,
            run_script=run_script,
            run_slug=run_slug,
            engineering_only=int(eng),
            preflight=int(preflight),
            status="failed",
            started_at=started_at,
            finished_at=finished_at,
            error_message=error_message,
            params_json=params_json or "{}",
            metrics_json=new_metrics,
            artifacts_json=artifacts_json or "{}",
        )
        if metrics:
            sql_upd = f"UPDATE \"{handle.table}\" SET metrics_json=?, status='failed', finished_at=?, error_message=?, row_hash=? WHERE tag=? AND batch=?"  # nosec B608
            conn.execute(sql_upd, (new_metrics, finished_at, error_message, new_hash, handle.tag, handle.batch))
        else:
            sql_upd2 = f"UPDATE \"{handle.table}\" SET status='failed', finished_at=?, error_message=?, row_hash=? WHERE tag=? AND batch=?"  # nosec B608
            conn.execute(sql_upd2, (finished_at, error_message, new_hash, handle.tag, handle.batch))
        conn.commit()


def get_runs(domain: str, experiment: str, tag: Optional[str] = None, *, variant: Optional[str] = None) -> list[dict]:
    """Fetch rows for inspection; for notebooks or quick diagnostics."""
    db_path = get_db_path(domain)
    table = ensure_table(db_path, experiment, variant=variant)
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        _assert_safe_identifier(table)
        if tag is None:
            sql_all = f"SELECT * FROM \"{table}\" ORDER BY tag, batch"  # nosec B608
            cur = conn.execute(sql_all)
            rows = cur.fetchall()
        else:
            sql_by_tag = f"SELECT * FROM \"{table}\" WHERE tag=? ORDER BY batch"  # nosec B608
            cur = conn.execute(sql_by_tag, (tag,))
            rows = cur.fetchall()
    out: list[dict] = []
    for r in rows:
        d = {k: r[k] for k in r.keys()}
        for col in ("params_json", "metrics_json", "artifacts_json"):
            if d.get(col):
                try:
                    d[col] = json.loads(d[col])
                except Exception as _e:
                    # Leave as raw JSON string if parsing fails; retain visibility into stored value
                    d[col] = d[col]
        out.append(d)
    return out
