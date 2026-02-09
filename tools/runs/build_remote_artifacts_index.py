#!/usr/bin/env python3
"""Build a human-friendly remote artifacts index for large run data.

Source of truth: runs/REMOTE_ARTIFACTS.json
Generated output: runs/REMOTE_ARTIFACTS.md

Optionally updates REMOTE_ARTIFACTS.json by computing SHA256/bytes for entries
that include a local file path.

This is intentionally lightweight and stdlib-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO_ROOT / "runs"
SRC_JSON = RUNS_DIR / "REMOTE_ARTIFACTS.json"
OUT_MD = RUNS_DIR / "REMOTE_ARTIFACTS.md"


DEFAULT_MAX_HASH_BYTES = 1 * 1024 * 1024 * 1024  # 1 GiB


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    if data.get("schema_version") != 1:
        raise ValueError(f"Unsupported schema_version in {path}: {data.get('schema_version')}")
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError(f"Expected artifacts[] list in {path}")
    return data


def _repo_root() -> Path:
    return REPO_ROOT


def _resolve_local_path(value: str) -> Path:
    p = Path(value)
    if p.is_absolute():
        return p
    return _repo_root() / p


def _sha256_file(path: Path, chunk_bytes: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_bytes)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _get_head_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_repo_root(), stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return ""


def update_json_artifacts(
    data: dict[str, Any],
    *,
    max_hash_bytes: int,
    allow_overwrite_empty_url_only: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    """Populate bytes/sha256 from local files when possible.

    Conventions:
    - If an artifact has `local_path`, we treat it as a path to the local file.
    - If `sha256` is empty and the file exists and is <= max_hash_bytes, compute and fill it.
    - If `bytes` is null and the file exists, fill it.
    - Never overwrite a non-empty `url`.

    Returns: (updated_data, warnings)
    """

    warnings: list[str] = []
    artifacts: list[dict[str, Any]] = data.get("artifacts", [])

    head_commit = _get_head_commit()
    for a in artifacts:
        if not isinstance(a, dict):
            continue

        # Ensure url field exists; keep empty by default.
        if "url" not in a:
            a["url"] = ""
        elif allow_overwrite_empty_url_only and a.get("url") is None:
            a["url"] = ""

        local_path_val = a.get("local_path")
        if not isinstance(local_path_val, str) or not local_path_val.strip():
            continue

        local_path = _resolve_local_path(local_path_val.strip())
        if not local_path.exists():
            warnings.append(f"Missing local file for artifact id={a.get('id','')}: {local_path_val}")
            continue
        if not local_path.is_file():
            warnings.append(f"local_path is not a file for artifact id={a.get('id','')}: {local_path_val}")
            continue

        try:
            size_bytes = local_path.stat().st_size
        except OSError as e:
            warnings.append(f"Failed to stat local_path for artifact id={a.get('id','')}: {e}")
            continue

        if a.get("bytes") in (None, ""):
            a["bytes"] = int(size_bytes)

        # If the user hasn't recorded source_commit yet, keep it best-effort.
        if isinstance(a.get("source_commit"), str) and not a.get("source_commit") and head_commit:
            a["source_commit"] = head_commit

        sha_val = a.get("sha256")
        sha_empty = (sha_val is None) or (isinstance(sha_val, str) and sha_val.strip() == "")
        if sha_empty:
            if size_bytes > max_hash_bytes:
                warnings.append(
                    f"Skipped SHA256 for artifact id={a.get('id','')} ({size_bytes} bytes > max {max_hash_bytes}); "
                    f"set VDM_REMOTE_ARTIFACTS_MAX_BYTES to override."
                )
                continue
            try:
                a["sha256"] = _sha256_file(local_path)
            except Exception as e:
                warnings.append(f"Failed to hash artifact id={a.get('id','')}: {e}")

    return data, warnings


def _fmt_bytes(n: int | None) -> str:
    if n is None:
        return ""
    # Simple base-2 formatting
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(n)
    unit = units[0]
    for u in units[1:]:
        if value < 1024.0:
            break
        value /= 1024.0
        unit = u
    if unit == "B":
        return f"{int(value)} {unit}"
    return f"{value:.2f} {unit}"


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()


def build_markdown(data: dict[str, Any]) -> str:
    artifacts: list[dict[str, Any]] = data["artifacts"]

    # Sort newest-first if created_at present
    def sort_key(a: dict[str, Any]) -> str:
        v = a.get("created_at")
        return v if isinstance(v, str) else ""

    artifacts_sorted = sorted(artifacts, key=sort_key, reverse=True)

    lines: list[str] = []
    lines.append("# Remote Run Artifacts")
    lines.append("")
    lines.append("Large run outputs (zips, logs, state files) are hosted off-repo.")
    lines.append("This index provides links + integrity metadata so artifacts are still reproducible and shareable.")
    lines.append("")
    lines.append("## How to add a new artifact")
    lines.append("")
    lines.append("1) Upload the artifact (or folder) to Google Drive (or another store)")
    lines.append("2) Make it accessible to collaborators (link-sharing as needed)")
    lines.append("3) Compute SHA256 locally")
    lines.append("4) Add an entry to `runs/REMOTE_ARTIFACTS.json`")
    lines.append("5) Regenerate this file: `python tools/runs/build_remote_artifacts_index.py`")
    lines.append("")
    lines.append("## Index")
    lines.append("")
    lines.append("| id | created_at | kind | size | sha256 | url | notes |")
    lines.append("|---|---|---|---:|---|---|---|")

    for a in artifacts_sorted:
        artifact_id = _md_escape(str(a.get("id", "")))
        created_at = _md_escape(str(a.get("created_at", "")))
        kind = _md_escape(str(a.get("kind", "")))
        size_str = ""
        bytes_val = a.get("bytes")
        if isinstance(bytes_val, int):
            size_str = _fmt_bytes(bytes_val)
        sha256 = _md_escape(str(a.get("sha256", "")))
        url = str(a.get("url", "")).strip()
        url_cell = url if url else ""
        notes = _md_escape(str(a.get("notes", "")))
        lines.append(f"| {artifact_id} | {created_at} | {kind} | {size_str} | {sha256} | {url_cell} | {notes} |")

    lines.append("")
    lines.append("## Details")

    for a in artifacts_sorted:
        artifact_id = str(a.get("id", "")).strip()
        if not artifact_id:
            continue
        lines.append("")
        lines.append(f"### {artifact_id}")
        title = str(a.get("title", "")).strip()
        if title:
            lines.append("")
            lines.append(f"- Title: {title}")
        for key in ["kind", "created_at", "source_commit", "bytes", "sha256", "url", "notes"]:
            val = a.get(key)
            if val in (None, ""):
                continue
            if key == "bytes" and isinstance(val, int):
                lines.append(f"- bytes: {val} ({_fmt_bytes(val)})")
            else:
                lines.append(f"- {key}: {val}")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if not SRC_JSON.exists():
        raise SystemExit(f"Missing {SRC_JSON}")

    parser = argparse.ArgumentParser(description="Build runs/REMOTE_ARTIFACTS.md (and optionally update runs/REMOTE_ARTIFACTS.json)")
    parser.add_argument(
        "--update-json",
        action="store_true",
        help="Populate bytes/sha256 for artifacts that define local_path, leaving url untouched unless missing.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=int(os.environ.get("VDM_REMOTE_ARTIFACTS_MAX_BYTES", str(DEFAULT_MAX_HASH_BYTES))),
        help="Max bytes to hash in --update-json mode (default: env VDM_REMOTE_ARTIFACTS_MAX_BYTES or 1GiB).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write output files (REMOTE_ARTIFACTS.json if updated, and REMOTE_ARTIFACTS.md).",
    )
    args = parser.parse_args()

    data = _load_json(SRC_JSON)

    if args.update_json:
        data_before = json.dumps(data, sort_keys=True)
        data, warnings = update_json_artifacts(data, max_hash_bytes=args.max_bytes)
        data_after = json.dumps(data, sort_keys=True)
        if warnings:
            for w in warnings:
                print(f"[remote-artifacts] {w}")
        if args.write and data_after != data_before:
            SRC_JSON.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"Wrote {SRC_JSON}")

    md = build_markdown(data)
    if args.write:
        OUT_MD.write_text(md, encoding="utf-8")
        print(f"Wrote {OUT_MD}")
    else:
        print(md)


if __name__ == "__main__":
    main()
