from __future__ import annotations

import os
import re
from typing import Iterable, Tuple

"""
Guard: deny any scheduler/cadence constructs in core/ and runtime/.

Policy (void-faithful, emergent-only):
- No files named 'scheduler.py' in core/cortex/void_walkers.
- No imports of 'scheduler' anywhere in fum_rt/core or fum_rt/runtime.
- Deny tokens (case-insensitive): STRUCT_EVERY | cron | schedule | scheduler | every <number>
  The 'every <number>' pattern forbids cron-like cadence gates while allowing
  incidental prose (e.g., "every tick") that contains no explicit numeric cadence.

Scope:
- Scans fum_rt/core/** and fum_rt/runtime/** .py sources only (excludes tests and docs).
"""

HERE = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FUM_ROOT = os.path.join(REPO_ROOT, "fum_rt")

CORE_DIR = os.path.join(FUM_ROOT, "core")
RUNTIME_DIR = os.path.join(FUM_ROOT, "runtime")

DENY_FILE = os.path.join(CORE_DIR, "cortex", "void_walkers", "scheduler.py")

# Denylist tokens and patterns
RE_IMPORT_SCHED = re.compile(r"(?i)^\s*(from\s+[\w\.]+\s+import\s+scheduler\b|import\s+scheduler\b)", re.M)
RE_DENY_TOKENS = re.compile(
    r"(?is)\b(STRUCT_EVERY|cron|schedule|scheduler)\b|every\s+\d+",
    re.IGNORECASE,
)


def _iter_py_files(root_dirs: Iterable[str]) -> Iterable[str]:
    for root in root_dirs:
        if not os.path.isdir(root):
            continue
        for r, _dirs, files in os.walk(root):
            for fn in files:
                if fn.endswith(".py"):
                    yield os.path.join(r, fn)


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _first_match_text(src: str, pat: re.Pattern) -> Tuple[int, str]:
    m = pat.search(src)
    if not m:
        return (-1, "")
    # Extract offending line
    start = src.rfind("\n", 0, m.start()) + 1
    end = src.find("\n", m.end())
    if end == -1:
        end = len(src)
    line = src[start:end]
    # Compute 1-based line number
    line_no = src.count("\n", 0, start) + 1
    return (line_no, line.strip())


def test_no_scheduler_file_present() -> None:
    assert not os.path.exists(DENY_FILE), f"Forbidden scheduler file present: {DENY_FILE}"


def test_no_scheduler_imports_or_tokens() -> None:
    offenders = []
    for path in _iter_py_files([CORE_DIR, RUNTIME_DIR]):
        try:
            src = _read(path)
        except Exception:
            continue
        # Specific import pattern
        ln1, line1 = _first_match_text(src, RE_IMPORT_SCHED)
        # General deny tokens
        ln2, line2 = _first_match_text(src, RE_DENY_TOKENS)

        if ln1 != -1:
            offenders.append((path, ln1, line1))
        if ln2 != -1:
            offenders.append((path, ln2, line2))

    msg_lines = ["Found forbidden scheduler/cadence constructs:"]
    for p, ln, txt in offenders:
        msg_lines.append(f"- {p}:{ln}: {txt}")
    assert not offenders, "\n".join(msg_lines)