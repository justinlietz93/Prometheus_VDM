#!/usr/bin/env python3
"""
VDM Nexus — License Header Audit

Goal:
- Scan ALL code files in the repository and report files that do NOT contain a license header
  or a close variation, based on multiple regex heuristics (names, company, "All Rights Reserved",
  "See LICENSE", etc.).

Output:
- JSON printed to stdout with top-level metadata (metrics, repo head, patterns used) and
  an "items" array listing missing-header filepaths with small snippets for review.

Usage:
  python VDM_Nexus/scripts/nexus_license_check.py
  python VDM_Nexus/scripts/nexus_license_check.py --json-out license_audit.json
  python VDM_Nexus/scripts/nexus_license_check.py --root . --max-lines 100 --extra-pattern "Justin Lietz"

Notes:
- Read-only scan. Large/binary files are skipped safely.
- "Code files" are determined by extension and common build-file names; see CODE_EXTS and SPECIAL_FILENAMES.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import ast
from collections import defaultdict
from pathlib import Path
from typing import Iterable, List, Dict, Any, Tuple, Optional

# Heuristic code extensions (expand as needed)
CODE_EXTS = {
    ".py", ".pyw",
    ".cpp", ".cxx", ".cc", ".c",
    ".hpp", ".hh", ".h", ".hxx",
    ".java", ".kt", ".scala",
    ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".go", ".rs", ".rb", ".php", ".swift",
    ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
    ".cmake", ".mak", ".mk",
    ".yml", ".yaml",  # CI/config scripts sometimes carry headers
    ".proto",
}

# Special code-ish filenames lacking extensions that often deserve headers
SPECIAL_FILENAMES = {
    "CMakeLists.txt",
    "Makefile",
    "Dockerfile",
    "Justfile",
    "Procfile",
}

# Directories to ignore (repo-local)
IGNORE_DIRS = {
    ".git", ".idea", ".vscode", ".venv", "venv", "node_modules", "dist", "build", "out", "__pycache__", ".cache",
    "VDM_Nexus/build",
    "Derivation/code/outputs",  # artifacts
    "runs", "outputs",
}

# Default license-related regex patterns (case-insensitive)
DEFAULT_PATTERNS = [
    r"copyright\s*©\s*20\d{2}\s*justin\s*k\.?\s*lietz",              # year + name
    r"copyright\s*\(c\)\s*20\d{2}\s*justin\s*k\.?\s*lietz",          # (c) form
    r"justin\s*k\.?\s*lietz",                                        # name alone
    r"neuroca,\s*inc\.?",                                            # company
    r"all\s*rights\s*reserved",                                      # rights statement
    r"see\s+license\s+file",                                         # pointer to license
    r"void\s+dynamics\s+model",                                      # project reference (looser)
]
 
BINARY_SNIFF_BYTES = 2048

# Standard license header to insert for Python files lacking any module docstring
HEADER_BLOCK = """\"\"\"
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
\"\"\"
"""

# Content-only insertion for existing module docstrings that lack keywords.
# Inserted immediately after the opening triple-quote, followed by a blank line.
DOCSTRING_CONTENT = (
    "Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.\n"
    "\n"
    "This research is protected under a dual-license to foster open academic\n"
    "research while ensuring commercial applications are aligned with the project's ethical principles.\n"
    "\n"
    "Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.\n"
    "See LICENSE file for full terms.\n"
)


def is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:BINARY_SNIFF_BYTES]
    except Exception:
        return True
    # Treat presence of null byte as binary
    return b"\x00" in chunk


def is_code_file(path: Path) -> bool:
    if path.name in SPECIAL_FILENAMES:
        return True
    return path.suffix.lower() in CODE_EXTS


def should_skip(path: Path, repo_root: Path) -> bool:
    # Skip ignored directories by prefix
    try:
        rel = path.relative_to(repo_root).as_posix()
    except Exception:
        return True
    parts = rel.split("/")
    # If any prefix directory matches ignore
    accum = []
    for p in parts[:-1]:
        accum.append(p)
        if "/".join(accum) in IGNORE_DIRS:
            return True
        if p in IGNORE_DIRS:
            return True
    # Skip obviously large files
    try:
        if path.stat().st_size > 8_000_000:  # 8 MB guard
            return True
    except Exception:
        return True
    return False


def git_rev_head() -> str:
    try:
        cp = subprocess.run(["git", "rev-parse", "HEAD"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return (cp.stdout or "").strip() if cp.returncode == 0 else ""
    except Exception:
        return ""


def gather_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if should_skip(p, root):
            continue
        if is_binary(p):
            continue
        if is_code_file(p):
            yield p


def file_has_header(path: Path, patterns: List[re.Pattern], max_lines: int) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            # Only scan the first N lines for a header
            lines = []
            for i, line in enumerate(fh):
                if i >= max_lines:
                    break
                lines.append(line)
            head = "".join(lines)
            for rgx in patterns:
                if rgx.search(head):
                    return True
            return False
    except Exception:
        # On any read issue, treat as "no header" to ensure manual review
        return False


def extract_module_docstring_py(path: Path) -> Optional[str]:
    """
    Extract the module-level docstring for a Python file.
    Returns the raw docstring (no cleaning) or None if absent/unparseable.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        mod = ast.parse(text)
        return ast.get_docstring(mod, clean=False)
    except Exception:
        return None


def insert_license_into_existing_docstring_py(path: Path) -> Tuple[int, int, int]:
    """
    Insert DOCSTRING_CONTENT into the existing module docstring after the opening
    triple-quote delimiter. Returns (insert_index_after_opening_quotes, inserted_lines, inserted_bytes).
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        mod = ast.parse(text)
    except Exception as e:
        raise RuntimeError(f"AST parse failed: {e}")

    if not mod.body or not isinstance(mod.body[0], ast.Expr):
        raise RuntimeError("No module-level docstring expression found")

    node = mod.body[0]
    if not hasattr(node, "lineno") or not hasattr(node, "col_offset"):
        raise RuntimeError("Docstring node lacks position info")

    lines = text.splitlines(True)  # keep line endings
    if node.lineno - 1 >= len(lines):
        raise RuntimeError("lineno out of range for docstring node")

    start_offset = sum(len(l) for l in lines[: node.lineno - 1]) + node.col_offset

    seg = ast.get_source_segment(text, node) if hasattr(ast, "get_source_segment") else None
    if not seg:
        seg = text[start_offset : start_offset + 4096]

    low = seg.lower()
    # Skip potential string prefixes: r, u, f, b (any order; we conservatively skip a short run)
    i = 0
    while i < len(low) and low[i] in ("r", "u", "f", "b"):
        i += 1

    idx_triple_dq = low.find('"""', i)
    idx_triple_sq = low.find("'''", i)
    if idx_triple_dq == -1 and idx_triple_sq == -1:
        raise RuntimeError("Could not locate opening triple quotes for docstring")

    qidx = idx_triple_dq if (idx_triple_dq != -1 and (idx_triple_sq == -1 or idx_triple_dq < idx_triple_sq)) else idx_triple_sq
    insert_pos = start_offset + qidx + 3

    # Insert a newline, the content, then another newline
    ins = "\n" + DOCSTRING_CONTENT + "\n"
    new_text = text[:insert_pos] + ins + text[insert_pos:]
    path.write_text(new_text, encoding="utf-8")

    inserted_lines = ins.count("\n")
    inserted_bytes = len(ins.encode("utf-8"))
    return (qidx + 3, inserted_lines, inserted_bytes)


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit repository for missing VDM license headers in code files.")
    ap.add_argument("--root", default=".", help="Repo root to scan (default: .)")
    ap.add_argument("--json-out", default="", help="Optional: write JSON results to this path")
    ap.add_argument("--max-lines", type=int, default=80, help="Number of leading lines to inspect per file (default: 80)")
    ap.add_argument("--extra-pattern", action="append", default=[], help="Additional regex (case-insensitive) to treat as header match (can repeat)")
    ap.add_argument(
        "--insert-headers",
        action="store_true",
        help="Insert the standard license docstring at line 1 for Python files with no module docstring."
    )
    args = ap.parse_args()

    repo_root = Path(args.root).resolve()
    # Use timezone-aware UTC (avoid deprecated utcnow)
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Compile regex (case-insensitive)
    patterns: List[re.Pattern] = [re.compile(pat, re.IGNORECASE) for pat in DEFAULT_PATTERNS]
    for pat in args.extra_pattern:
        patterns.append(re.compile(pat, re.IGNORECASE))

    all_files = list(gather_files(repo_root))
    scanned = len(all_files)

    missing: List[Dict[str, Any]] = []
    matched_count = 0

    # Per-root folder stats
    by_root = defaultdict(lambda: {"scanned": 0, "matched": 0, "missing": 0})

    # Track applied fixes (docstring inserts)
    fixes_applied: List[Dict[str, Any]] = []

    for p in all_files:
        try:
            rel = p.relative_to(repo_root)
        except Exception:
            rel = p
        parts = rel.parts
        root_key = parts[0] if len(parts) > 1 else "(repo-root)"

        by_root[root_key]["scanned"] += 1
        ext = p.suffix.lower()

        if ext in {".py", ".pyw"}:
            doc = extract_module_docstring_py(p)
            if doc is not None:
                # Check license keywords inside the docstring only
                has_keywords = any(rgx.search(doc) for rgx in patterns)
                if has_keywords:
                    matched_count += 1
                    by_root[root_key]["matched"] += 1
                else:
                    if args.insert_headers:
                        try:
                            inner_idx, added_lines, added_bytes = insert_license_into_existing_docstring_py(p)
                            # After insertion, treat as matched
                            matched_count += 1
                            by_root[root_key]["matched"] += 1
                            fixes_applied.append({
                                "path": str(rel),
                                "root": root_key,
                                "action": "inserted_license_into_docstring",
                                "insert_index_after_opening_quotes": inner_idx,
                                "inserted_lines": added_lines,
                                "inserted_bytes": added_bytes,
                            })
                        except Exception as e:
                            # If insertion fails, keep as missing and record error
                            missing.append({
                                "path": str(rel),
                                "reason": "no keywords found",
                                "docstring": doc,
                                "error": str(e),
                            })
                            by_root[root_key]["missing"] += 1
                    else:
                        missing.append({
                            "path": str(rel),
                            "reason": "no keywords found",
                            "docstring": doc,
                        })
                        by_root[root_key]["missing"] += 1
            else:
                # No module docstring header present at all
                if args.insert_headers:
                    try:
                        text = p.read_text(encoding="utf-8", errors="ignore")
                        lines = text.splitlines(True)  # keep line endings
                        idx = 0
                        after_shebang = False
                        after_encoding = False
                        # Preserve executable shebang at line 1
                        if len(lines) > 0 and lines[0].startswith("#!"):
                            idx = 1
                            after_shebang = True
                        # Preserve PEP 263 encoding cookie on first/second line
                        if idx < len(lines) and re.match(r"^#.*coding[:=]", lines[idx]):
                            idx += 1
                            after_encoding = True
                        new_text = "".join(lines[:idx]) + HEADER_BLOCK + "".join(lines[idx:])
                        p.write_text(new_text, encoding="utf-8")
                        added_lines = HEADER_BLOCK.count("\n")
                        added_bytes = len(HEADER_BLOCK.encode("utf-8"))
                        # Consider this now matched
                        matched_count += 1
                        by_root[root_key]["matched"] += 1
                        fixes_applied.append({
                            "path": str(rel),
                            "root": root_key,
                            "action": "inserted_license_docstring",
                            "insert_index": idx,
                            "after_shebang": after_shebang,
                            "after_encoding_cookie": after_encoding,
                            "inserted_lines": added_lines,
                            "inserted_bytes": added_bytes,
                        })
                        # do not add to missing
                    except Exception as e:
                        # If insertion fails, keep as missing
                        missing.append({
                            "path": str(rel),
                            "reason": "no docstring header found at all",
                            "docstring": None,
                            "error": str(e),
                        })
                        by_root[root_key]["missing"] += 1
                else:
                    # Report as missing (no insertion requested)
                    missing.append({
                        "path": str(rel),
                        "reason": "no docstring header found at all",
                        "docstring": None,
                    })
                    by_root[root_key]["missing"] += 1
        else:
            # Non-Python: fall back to scanning first N lines for license keywords
            ok = file_has_header(p, patterns, args.max_lines)
            if ok:
                matched_count += 1
                by_root[root_key]["matched"] += 1
            else:
                preview = ""
                try:
                    with p.open("r", encoding="utf-8", errors="ignore") as fh:
                        preview = "".join([next(fh) for _ in range(min(10, args.max_lines))])
                except Exception:
                    preview = ""
                missing.append({
                    "path": str(rel),
                    "reason": "no keywords found",
                    "preview": preview,
                })
                by_root[root_key]["missing"] += 1

    # Build per-root summary with percentages
    by_root_summary = []
    for rk in sorted(by_root.keys()):
        s = by_root[rk]
        total = max(1, s["scanned"])
        matched_pct = round(100.0 * s["matched"] / total, 2)
        missing_pct = round(100.0 * s["missing"] / total, 2)
        by_root_summary.append({
            "root": rk,
            "scanned": s["scanned"],
            "matched": s["matched"],
            "missing": s["missing"],
            "matched_pct": matched_pct,
            "missing_pct": missing_pct,
        })

    # Build fixes_by_root summary
    fixes_by_root = defaultdict(int)
    for fx in fixes_applied:
        fixes_by_root[fx.get("root", "(repo-root)")] += 1
    fixes_by_root_summary = [{"root": rk, "inserted": fixes_by_root[rk]} for rk in sorted(fixes_by_root.keys())]

    result = {
        "generated_utc": now_utc,
        "repo_head": git_rev_head(),
        "root": str(repo_root),
        "scanned_files": scanned,
        "matched_headers": matched_count,
        "missing_headers": len(missing),
        "ignore_dirs": sorted(list(IGNORE_DIRS)),
        "patterns": DEFAULT_PATTERNS + (args.extra_pattern or []),
        "by_root_summary": by_root_summary,
        "fixes_applied_count": len(fixes_applied),
        "fixes_by_root": fixes_by_root_summary,
        "fixes_applied": fixes_applied,
        "items": missing,  # only the files missing headers
    }

    # Print to stdout
    print(json.dumps(result, indent=2, sort_keys=True))

    # Optional write
    if args.json_out:
        out_path = Path(args.json_out)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        except Exception as e:
            print(f"[warn] Could not write JSON to {out_path}: {e}")

    # Non-strict exit: success even if missing files exist (tool is a reporter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())