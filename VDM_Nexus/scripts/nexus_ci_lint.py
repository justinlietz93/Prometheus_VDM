#!/usr/bin/env python3
"""
Nexus CI Lint

Read-only lint checks for the VDM Nexus directory:
- JSON validity (.json files)
- Markdown hygiene (.md files): CRLFs, trailing whitespace, tabs
- Optional long-line warnings (default warn only)

Outputs GitHub Actions annotations for inline review.

Policy:
- Errors cause nonzero exit.
- Long-line is warn-only unless --strict is set.

Scope:
- Restrict traversal to the provided --root (default: VDM_Nexus) to keep CI
  focused and Nexus-only, per scope discipline.

Usage:
  python3 VDM_Nexus/scripts/nexus_ci_lint.py --root VDM_Nexus --json --md --max-line-length 120
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Finding:
    file: str
    line: int
    column: int
    level: str  # "error" or "warning"
    code: str   # short machine code, e.g., "JSON_PARSE", "MD_TRAILING_WS"
    message: str

    def gha_annot(self) -> str:
        # GitHub Actions logging command
        # ::level file=...,line=...,col=...::message
        attrs = [f"file={self.file}"]
        if self.line > 0:
            attrs.append(f"line={self.line}")
        if self.column > 0:
            attrs.append(f"col={self.column}")
        attr_s = ",".join(attrs)
        return f"::{self.level} {attr_s}::{self.code}: {self.message}"


def is_json_file(path: str) -> bool:
    return path.lower().endswith(".json")


def is_md_file(path: str) -> bool:
    return path.lower().endswith(".md")


def walk_files(root: str) -> List[str]:
    files: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Optionally, ignore build output or external dirs under root if any arise in future
        # Currently no excludes are necessary for VDM_Nexus.
        for fn in filenames:
            files.append(os.path.join(dirpath, fn))
    return files


def lint_json_files(root: str) -> Tuple[List[Finding], List[Finding]]:
    errors: List[Finding] = []
    warnings: List[Finding] = []
    for path in walk_files(root):
        if not is_json_file(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
        except Exception as e:
            # Best-effort line/column extraction from exception string
            line = 0
            col = 0
            msg = str(e)
            # Look for patterns like: line X column Y (char Z)
            m = re.search(r"line\s+(\d+)\s+column\s+(\d+)", msg, re.IGNORECASE)
            if m:
                try:
                    line = int(m.group(1))
                    col = int(m.group(2))
                except Exception:
                    pass
            errors.append(Finding(
                file=path,
                line=line,
                column=col,
                level="error",
                code="JSON_PARSE",
                message=msg,
            ))
    return errors, warnings


def _has_crlf(s: str) -> bool:
    return "\r" in s


def _trailing_ws(s: str) -> bool:
    return bool(re.search(r"[ \t]+$", s))


def _has_tab(s: str) -> bool:
    return "\t" in s


def _long_line(s: str, limit: int) -> bool:
    # Measure visual length; here just count chars.
    return len(s) > limit


def lint_md_files(root: str, max_len: int, strict: bool) -> Tuple[List[Finding], List[Finding]]:
    errors: List[Finding] = []
    warnings: List[Finding] = []
    for path in walk_files(root):
        if not is_md_file(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines(True)  # keepends
        except Exception as e:
            errors.append(Finding(
                file=path,
                line=0,
                column=0,
                level="error",
                code="MD_IO",
                message=f"Failed to read markdown: {e}",
            ))
            continue

        # CRLF detection
        for i, raw in enumerate(lines, start=1):
            if _has_crlf(raw):
                errors.append(Finding(
                    file=path,
                    line=i,
                    column=1,
                    level="error",
                    code="MD_CRLF",
                    message="CRLF detected; use LF-only newlines.",
                ))

        # Content checks operate on line without newline
        for i, raw in enumerate(lines, start=1):
            line = raw.rstrip("\n\r")

            # Trailing whitespace handling:
            # - Exactly two spaces at EOL (no tab, not 3+) is a Markdown hard line break → warning
            # - Any other trailing whitespace (tabs or >=3 spaces) → error
            if _trailing_ws(line):
                is_two_space_hard_break = (
                    line.endswith("  ")
                    and not line.endswith("   ")
                    and ("\t" not in line)
                )
                if is_two_space_hard_break:
                    warnings.append(Finding(
                        file=path,
                        line=i,
                        column=len(line),
                        level="warning",
                        code="MD_HARD_BREAK",
                        message="Markdown hard line break (two trailing spaces).",
                    ))
                else:
                    errors.append(Finding(
                        file=path,
                        line=i,
                        column=len(line),
                        level="error",
                        code="MD_TRAILING_WS",
                        message="Trailing whitespace.",
                    ))

            # Tab check remains an error
            if _has_tab(line):
                errors.append(Finding(
                    file=path,
                    line=i,
                    column=line.find("\t") + 1,
                    level="error",
                    code="MD_TAB",
                    message="Tab character detected; use spaces.",
                ))

            # Long line (warn by default)
            if _long_line(line, max_len):
                f = Finding(
                    file=path,
                    line=i,
                    column=max_len + 1,
                    level=("error" if strict else "warning"),
                    code="MD_LONG_LINE",
                    message=f"Line length {len(line)} exceeds limit {max_len}.",
                )
                if strict:
                    errors.append(f)
                else:
                    warnings.append(f)

        # Final newline check
        if len(lines) > 0 and not lines[-1].endswith("\n"):
            warnings.append(Finding(
                file=path,
                line=len(lines),
                column=1,
                level="warning",
                code="MD_FINAL_NEWLINE",
                message="File should end with a newline.",
            ))

    return errors, warnings


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Nexus-only lint checks")
    ap.add_argument("--root", default="VDM_Nexus", help="Root directory to lint")
    ap.add_argument("--json", action="store_true", help="Enable JSON lint checks")
    ap.add_argument("--md", action="store_true", help="Enable Markdown hygiene checks")
    ap.add_argument("--max-line-length", type=int, default=120, help="Markdown long line length")
    ap.add_argument("--strict", action="store_true", help="Treat long-line warnings as errors")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        print(f"::warning ::Root path not found or not a directory: {args.root}", file=sys.stderr)
        return 0  # do not fail the job if directory missing

    all_errors: List[Finding] = []
    all_warnings: List[Finding] = []

    if args.json:
        e, w = lint_json_files(args.root)
        all_errors.extend(e)
        all_warnings.extend(w)

    if args.md:
        e, w = lint_md_files(args.root, args.max_line_length, args.strict)
        all_errors.extend(e)
        all_warnings.extend(w)

    # Emit annotations
    for f in all_warnings:
        print(f.gha_annot())
    for f in all_errors:
        print(f.gha_annot())

    # Summary
    print(f"::notice ::Nexus CI Lint — warnings={len(all_warnings)} errors={len(all_errors)}")

    return 1 if len(all_errors) > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))