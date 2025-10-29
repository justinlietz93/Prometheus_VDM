#!/usr/bin/env python3
"""
Fail if tests import or call begin_run() directly.

Scope:
- Scans Derivation/code/tests/**/*.py for disallowed patterns.
- Allows conftest.py (it installs a guard shim that references begin_run).

Exit codes:
- 0: OK
- 1: Violations found; prints explicit guidance
"""
from __future__ import annotations

import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = ROOT / "Derivation" / "code" / "tests"

# Simple patterns; keep explicit and readable
CALL_PATTERNS = [
    re.compile(r"\bbegin_run\s*\("),
    re.compile(r"results_db\s*\.\s*begin_run\s*\("),
    re.compile(r"\bfrom\s+common\.data\.results_db\s+import\s+.*\bbegin_run\b"),
]

# Files to ignore
IGNORE_BASENAMES = {"conftest.py"}

# Explicit per-file whitelist (relative to TESTS_DIR)
# These files may reference begin_run for enforcement testing.
WHITELIST_RELATIVE = {
    "ci/test_preflight_guard.py",
}


def main() -> int:
    if not TESTS_DIR.exists():
        return 0
    violations: list[tuple[Path, int, str]] = []
    for py in TESTS_DIR.rglob("*.py"):
        if py.name in IGNORE_BASENAMES:
            continue
        # Skip whitelisted files
        try:
            rel = py.relative_to(TESTS_DIR).as_posix()
            if rel in WHITELIST_RELATIVE:
                continue
        except Exception as e:
            # If relative computation fails, proceed with scanning but emit a warning
            print(f"WARN: Could not compute relative path for {py}: {e}")
        try:
            text = py.read_text(encoding="utf-8")
        except Exception as e:
            print(f"WARN: Skipping unreadable file: {py} ({e})")
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            s = line.strip()
            # Skip obvious comments
            if s.startswith("#"):
                continue
            for pat in CALL_PATTERNS:
                if pat.search(line):
                    violations.append((py, i, line.rstrip()))
                    break
    if not violations:
        return 0

    print("ERROR: Forbidden begin_run() usage detected in tests.")
    print()
    for path, ln, src in violations:
        print(f" - {path}:{ln}: {src}")
    print()
    print("Guidance:")
    print("  Tests must use preflight-only DB writes.")
    print("  Replace begin_run(...) with one of:")
    print("    - common.data.results_db.begin_preflight_run(domain, runner, tag, params)")
    print("    - common.data.preflight_db.log_preflight(test_name, config=..., results=..., status=...)")
    print("  If absolutely necessary to call begin_run, pass preflight=True and variant='preflight'.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
