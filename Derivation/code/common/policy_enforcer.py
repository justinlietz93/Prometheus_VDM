#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


@dataclass
class Violation:
    path: Path
    reason: str


IO_IMPORT_PATTERNS = [
    re.compile(r"from\s+common\.io_paths\s+import\s+(figure_path|log_path|write_log)"),
    re.compile(r"import\s+common\.io_paths(\s+as\s+\w+)?"),
]

APPROVAL_IMPORT_PATTERNS = [
    re.compile(r"from\s+common\.approval\s+import\s+check_tag_approval"),
    re.compile(r"import\s+common\.approval(\s+as\s+\w+)?"),
]


def _has_any(patterns: List[re.Pattern[str]], text: str) -> bool:
    return any(p.search(text) for p in patterns)


def _should_check_io(text: str) -> bool:
    # Only enforce io_paths if the script emits artifacts (heuristic)
    return ("matplotlib" in text) or ("figure_path(" in text) or ("write_log(" in text)


def _should_check_approval(text: str) -> bool:
    # Only enforce approval if the script is a runnable CLI (heuristic: argparse) or uses tags
    return ("argparse" in text) or ("--tag" in text)


def scan(paths: Iterable[Path]) -> List[Violation]:
    violations: List[Violation] = []
    for p in paths:
        if not p.suffix == ".py":
            continue
        if p.name.startswith("__"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            violations.append(Violation(p, f"unreadable file: {e}"))
            continue
        if _should_check_io(text) and not _has_any(IO_IMPORT_PATTERNS, text):
            violations.append(Violation(p, "missing common.io_paths import for artifact emission"))
        if _should_check_approval(text) and not _has_any(APPROVAL_IMPORT_PATTERNS, text):
            violations.append(Violation(p, "missing common.approval import for tag-based approval"))
    return violations


def scan_physics_roots(repo_root: Path) -> List[Violation]:
    # Support both Derivation/ and derivation/ layouts
    candidates = [
        repo_root / "Derivation" / "code" / "physics",
        repo_root / "derivation" / "code" / "physics",
    ]
    violations: List[Violation] = []
    for root in candidates:
        if root.is_dir():
            files = list(root.rglob("*.py"))
            violations.extend(scan(files))
    return violations


def main() -> None:
    import sys
    repo_root = Path(__file__).resolve().parents[3]
    v = scan_physics_roots(repo_root)
    if v:
        for viol in v:
            print(f"POLICY VIOLATION: {viol.path} :: {viol.reason}")
        sys.exit(1)
    print("Policy enforcement passed: all relevant physics scripts import approval and io_paths.")


if __name__ == "__main__":
    main()
