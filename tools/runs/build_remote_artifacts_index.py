#!/usr/bin/env python3
"""Build a human-friendly remote artifacts index for large run data.

Source of truth: runs/REMOTE_ARTIFACTS.json
Generated output: runs/REMOTE_ARTIFACTS.md

This is intentionally lightweight and stdlib-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO_ROOT / "runs"
SRC_JSON = RUNS_DIR / "REMOTE_ARTIFACTS.json"
OUT_MD = RUNS_DIR / "REMOTE_ARTIFACTS.md"


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
    data = _load_json(SRC_JSON)
    md = build_markdown(data)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
