#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


VDM Nexus — Static Policy Check (Task 0.3.1)

Purpose:
- Enforce: "zero write operations under ../Derivation/" from Nexus scope
- Static source scan only (no execution). Read-only across the repo.

What it checks:
- In VDM_Nexus/**/*.{cpp,cxx,cc,c,hxx,hh,h}:
  - std::ofstream(...) (assumed write)
  - std::fstream(..., std::ios::out...) or flags with out/app
  - fopen(..., mode) where mode contains 'w' or 'a'
  - QFile::open(QIODevice::WriteOnly|ReadWrite|Append)
- In VDM_Nexus/**/*.py:
  - open(path, mode) where mode includes 'w', 'a', '+'
  - Path.write_text / Path.write_bytes
- For any of the above, flag as violation ONLY if the literal path argument contains:
  - "../derivation" or "/Derivation/" (case-insensitive)
- Prohibited identifiers in Nexus tree:
  - "memory_kg_lite" in file paths or string literals (memory KG‑Lite is external‑agent‑only per NEXUS §3)

Exit codes:
- 0 = PASS (no violations)
- 1 = FAIL (violations found)

Usage:
  python VDM_Nexus/scripts/nexus_static_policy_check.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple


CPP_EXTS = {".cpp", ".cxx", ".cc", ".c", ".hxx", ".hh", ".h"}
PY_EXTS = {".py"}

DERIV_PATTERNS = (
    "../derivation",
    "/Derivation/",
)

# Prohibited identifiers (external-agent-only; must not appear in VDM_Nexus tree)
PROHIBITED_IDENTIFIERS = {
    "memory_kg_lite": "Memory KG-Lite belongs to external agents only (not in VDM Nexus)"
}
RE_PROHIBITED = re.compile(r"memory_kg_lite", re.IGNORECASE)

# Regex patterns for quick, simple static scan
RE_CPP_OFSTREAM = re.compile(r"""std::ofstream\s*\(\s*(".*?"|'.*?')""")
RE_CPP_FSTREAM = re.compile(r"""std::fstream\s*\(\s*(".*?"|'.*?')\s*,\s*[^)]*\b(std::ios::out|std::ios::app)\b""")
RE_CPP_FOPEN = re.compile(r"""fopen\s*\(\s*(".*?"|'.*?')\s*,\s*(".*?"|'.*?')\s*\)""")
RE_CPP_QFILE_OPEN = re.compile(r"""\.open\s*\(\s*QIODevice::(WriteOnly|ReadWrite|Append)\b""")

RE_PY_OPEN = re.compile(r"""open\s*\(\s*(".*?"|'.*?')\s*,\s*(".*?"|'.*?')\s*\)""")
RE_PY_WRITE_TEXT = re.compile(r"""\.write_text\s*\(""")
RE_PY_WRITE_BYTES = re.compile(r"""\.write_bytes\s*\(""")
# Additional prohibited literals in Nexus tree (external-agent-only semantics)
RE_ACCEPTANCE = re.compile(r"acceptance_test", re.IGNORECASE)


def literal_points_to_derivation(lit: str) -> bool:
    s = lit.strip().strip("'\"").lower()
    return any(p in s for p in DERIV_PATTERNS)


def scan_cpp_text(text: str, file: Path) -> List[Tuple[int, str]]:
    violations: List[Tuple[int, str]] = []
    for m in RE_CPP_OFSTREAM.finditer(text):
        lit = m.group(1)
        if literal_points_to_derivation(lit):
            ln = text[: m.start()].count("\n") + 1
            violations.append((ln, f"std::ofstream with derivation path {lit}"))
    for m in RE_CPP_FSTREAM.finditer(text):
        lit = m.group(1)
        if literal_points_to_derivation(lit):
            ln = text[: m.start()].count("\n") + 1
            violations.append((ln, f"std::fstream (out/app) with derivation path {lit}"))
    for m in RE_CPP_FOPEN.finditer(text):
        lit, mode = m.group(1), m.group(2)
        if ("w" in mode or "a" in mode or "+" in mode) and literal_points_to_derivation(lit):
            ln = text[: m.start()].count("\n") + 1
            violations.append((ln, f"fopen write/append with derivation path {lit}, mode={mode}"))
    # QFile::open check doesn't include path literal; only flags the write intent.
    # We only consider it a violation if the same file contains a nearby literal that targets derivation.
    # Simple heuristic: if any string literal on the same line references derivation when open(WriteOnly) is present.
    for m in RE_CPP_QFILE_OPEN.finditer(text):
        ln = text[: m.start()].count("\n") + 1
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        for qlit in re.findall(r"(['\"]).*?\1", line):
            if literal_points_to_derivation(qlit):
                violations.append((ln, f"QFile::open(Write*) with derivation path {qlit}"))
                break
    return violations


def scan_py_text(text: str, file: Path) -> List[Tuple[int, str]]:
    violations: List[Tuple[int, str]] = []
    for m in RE_PY_OPEN.finditer(text):
        lit, mode = m.group(1), m.group(2)
        mode_s = mode.strip("'\"")
        if any(ch in mode_s for ch in ("w", "a", "+")) and literal_points_to_derivation(lit):
            ln = text[: m.start()].count("\n") + 1
            violations.append((ln, f"open() write/append with derivation path {lit}, mode={mode}"))
    # Heuristic for Path.write_text/bytes: flag only if the same line mentions derivation in a literal
    for m in RE_PY_WRITE_TEXT.finditer(text):
        ln = text[: m.start()].count("\n") + 1
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        for qlit in re.findall(r"(['\"]).*?\1", line):
            if literal_points_to_derivation(qlit):
                violations.append((ln, f"Path.write_text targeting derivation path {qlit}"))
                break
    for m in RE_PY_WRITE_BYTES.finditer(text):
        ln = text[: m.start()].count("\n") + 1
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        for qlit in re.findall(r"(['\"]).*?\1", line):
            if literal_points_to_derivation(qlit):
                violations.append((ln, f"Path.write_bytes targeting derivation path {qlit}"))
                break
    return violations


def scan_prohibited_text(text: str, file: Path) -> List[Tuple[int, str]]:
    violations: List[Tuple[int, str]] = []
    # Allow this policy file to mention the terms
    if file.name == "nexus_static_policy_check.py":
        return violations
    for m in RE_PROHIBITED.finditer(text):
        ln = text[: m.start()].count("\n") + 1
        violations.append((ln, "Prohibited identifier 'memory_kg_lite' in source; external-agent-only"))
    for m in RE_ACCEPTANCE.finditer(text):
        ln = text[: m.start()].count("\n") + 1
        violations.append((ln, "Prohibited literal 'acceptance_test' in Nexus code; KG‑Lite acceptance rules must not be encoded in Nexus"))
    return violations


def main() -> int:
    repo = Path(".").resolve()
    nexus = repo / "VDM_Nexus"

    problems: List[Tuple[Path, int, str]] = []

    for p in nexus.rglob("*"):
        if not p.is_file():
            continue
        # Path-based prohibited identifier check
        if "memory_kg_lite" in p.as_posix().lower():
            problems.append((p, 0, "Prohibited path containing 'memory_kg_lite' (external-agent-only)"))
            continue
        ext = p.suffix.lower()
        try:
            if ext in CPP_EXTS or ext in PY_EXTS:
                text = p.read_text(encoding="utf-8", errors="ignore")
                # Source-based prohibited identifier check
                for (ln, msg) in scan_prohibited_text(text, p):
                    problems.append((p, ln, msg))
                if ext in CPP_EXTS:
                    v = scan_cpp_text(text, p)
                else:
                    v = scan_py_text(text, p)
                for (ln, msg) in v:
                    problems.append((p, ln, msg))
        except Exception as e:
            # Non-fatal; report as a warning but do not fail the policy
            print(f"[warn] Could not scan {p}: {e}")

    if not problems:
        print("Policy check: PASS — no write operations targeting ../derivation detected in VDM_Nexus/")
        return 0

    print("Policy check: FAIL — potential write operations to ../derivation detected:")
    for f, ln, msg in problems:
        print(f"  - {f}:{ln}  {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())