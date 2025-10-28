#!/usr/bin/env python3
"""
VDM Nexus — Derivation Change Guard
Enforce CHRONICLES + Canon update policy in pre-commit and CI.

Policy summary (per user instruction):
- If any path under Derivation/ changes (excluding reference-only paths), then:
  1) CHRONICLES.md must be updated in the same diff (loudly enforced).
     - Bypass exists only by documenting the change explicitly in Derivation/CHRONICLES.md.
  2) If the change is a "legitimate canon-impacting change" (e.g., new proposals, experiments, code, results),
     then at least one canonical ALL-CAPS doc must be updated in the same diff, at minimum:
       * Derivation/AXIOMS.md
       * Derivation/EQUATIONS.md
       * Derivation/VALIDATION_METRICS.md
       * Derivation/ROADMAP.md
       * Derivation/CANON_MAP.md
       * Derivation/SCHEMAS.md
       * Derivation/SYMBOLS.md
       * Derivation/UNITS_NORMALIZATION.md
       * Derivation/OPEN_QUESTIONS.md
       * Derivation/ALGORITHMS.md
       * Derivation/CANON_PROGRESS.md
  3) Dependency chain MUST also be updated when canon files are dependencies or have dependencies.
     - Phase 1 enforcement: require an explicit marker line in CHRONICLES for legitimate canon-impacting changes:
         "Dependency-Chain-Reviewed: true"
       This is a lightweight attestation until full graph enforcement is integrated.
     - Phase 2 (future): integrate a canonical dependency map for automatic verification.

Exit codes:
  0 = PASS
  1 = FAIL (violations found)

Usage:
  Pre-commit mode (staged changes):
    python VDM_Nexus/scripts/precommit_derivation_guard.py --mode precommit
  CI mode (compare against base, default origin/main):
    python VDM_Nexus/scripts/precommit_derivation_guard.py --mode ci --base origin/main

Notes:
- This guard is stricter than nexus_validate_gate.py (which warns non-fatally). CI/pre-commit can treat
  warnings as errors by using this guard.
- Exclusions mirror DEFAULT_EXCLUSIONS in [nexus_validate_gate.py](VDM_Nexus/scripts/nexus_validate_gate.py:53).

"""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Sequence


# Keep in sync with nexus_validate_gate.py DEFAULT_EXCLUSIONS
DEFAULT_EXCLUSIONS = [
    "Derivation/Converging_External_Research/**",
    "Derivation/References/**",
    "Derivation/Speculations/**",
    "Derivation/Templates/**",
    "Derivation/Supporting_Work/external_references/**",
    "Derivation/Supporting_Work/Physics-Based Datasets by Tier_ A Comprehensive Resource Guide.pdf",
    "Derivation/VDM_OVERVIEW.md",
]

# Canon docs considered "ALL-CAPS" registry for legitimacy checks
CANON_DOCS = [
    "Derivation/AXIOMS.md",
    "Derivation/EQUATIONS.md",
    "Derivation/VALIDATION_METRICS.md",
    "Derivation/ROADMAP.md",
    "Derivation/CANON_MAP.md",
    "Derivation/SCHEMAS.md",
    "Derivation/SYMBOLS.md",
    "Derivation/UNITS_NORMALIZATION.md",
    "Derivation/OPEN_QUESTIONS.md",
    "Derivation/ALGORITHMS.md",
    "Derivation/CANON_PROGRESS.md",
]

# Heuristics: paths that indicate a change is canon-impacting (not mere references/moves)
LEGIT_CHANGE_PATTERNS = [
    # Proposals/Results anywhere under Derivation
    "Derivation/**/PROPOSAL_*.md",
    "Derivation/**/RESULTS_*.md",
    # Physics code and configs/schemas/specs
    "Derivation/code/**",
    "Derivation/**/APPROVAL.json",
    "Derivation/**/schemas/*.json",
    "Derivation/**/specs/*.json",
    "Derivation/**/run_*.py",
]

CHRONICLES_PATH = "Derivation/CHRONICLES.md"
CHAIN_ATTESTATION_MARKER = "Dependency-Chain-Reviewed: true"


def run(cmd: Sequence[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def path_matches_globs(path: str, patterns: Sequence[str]) -> bool:
    """
    Glob match on POSIX path using fnmatch.fnmatchcase; '*' matches across '/'.
    Treat '**' as '*' to avoid pathlib.Path.match edge cases across Python versions.
    """
    posix = Path(path).as_posix()
    for pat in patterns:
        p = pat.replace("\\", "/")
        p = p.replace("**", "*")
        if fnmatch.fnmatchcase(posix, p):
            return True
    return False


def git_changed_files_precommit() -> List[str]:
    """
    Staged files to be committed. Works during pre-commit.
    """
    try:
        cp = run(["git", "diff", "--cached", "--name-only"])
        lines = [ln.strip() for ln in (cp.stdout or "").splitlines() if ln.strip()]
        return lines
    except subprocess.CalledProcessError as e:
        print(f"[error] git diff --cached failed: {e.stdout}", file=sys.stderr)
        return []


def git_changed_files_vs_base(base_ref: str) -> List[str]:
    """
    Files changed vs base_ref...HEAD.
    """
    try:
        cp = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
        lines = [ln.strip() for ln in (cp.stdout or "").splitlines() if ln.strip()]
        return lines
    except subprocess.CalledProcessError as e:
        print(f"[error] git diff failed: {e.stdout}", file=sys.stderr)
        return []


def filter_derivation_tracked(paths: Sequence[str], exclusions: Sequence[str]) -> List[str]:
    out: List[str] = []
    for f in paths:
        if not f.startswith("Derivation/"):
            continue
        if path_matches_globs(f, exclusions):
            continue
        out.append(f)
    return out


def any_match_globs(paths: Sequence[str], patterns: Sequence[str]) -> bool:
    return any(path_matches_globs(p, patterns) for p in paths)


def read_file_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Derivation change guard (pre-commit/CI enforcement)")
    parser.add_argument("--mode", choices=["precommit", "ci"], default="precommit", help="Run mode (default: precommit)")
    parser.add_argument("--base", default="origin/main", help="Base ref for CI mode (default: origin/main)")
    parser.add_argument("--exclusion", action="append", default=[], help="Extra exclusion patterns")
    parser.add_argument("--require-canon", action="store_true", help="Require canon doc update for any Derivation change (override heuristics)")
    parser.add_argument("--no-chain-attestation", action="store_true", help="Do not enforce CHRONICLES chain attestation marker")
    args = parser.parse_args()

    exclusions = list(DEFAULT_EXCLUSIONS) + list(args.exclusion)

    if args.mode == "precommit":
        changed = git_changed_files_precommit()
    else:
        changed = git_changed_files_vs_base(args.base)

    changed_tracked = filter_derivation_tracked(changed, exclusions)
    if not changed_tracked:
        # No tracked Derivation changes — PASS
        return 0

    # 1) Enforce CHRONICLES update when Derivation changes occur
    chronicles_in_diff = (CHRONICLES_PATH in changed)
    violations: List[str] = []
    if not chronicles_in_diff:
        violations.append(
            "Derivation changes detected but Derivation/CHRONICLES.md is not in this diff.\n"
            "Action: Add an explicit entry documenting the change (pivots, DISPROVEN status, corrections, shuffles, etc.)."
        )

    # Heuristic for "legitimate canon-impacting change"
    legit_change = args.require_canon or any_match_globs(changed_tracked, LEGIT_CHANGE_PATTERNS)

    # 2) If legitimate change, require at least one canon doc updated
    if legit_change:
        canon_touched = [p for p in changed if p in CANON_DOCS]
        if not canon_touched:
            violations.append(
                "Legitimate Derivation change detected (proposals/experiments/code/results), "
                "but no canonical ALL-CAPS doc was updated in this diff.\n"
                "Action: Update at least one of the canon docs (EQUATIONS/VALIDATION_METRICS/ROADMAP/etc.) "
                "and ensure anchors/registries are consistent. If a canon file is a dependency or has dependencies, "
                "update the entire dependency chain."
            )

        # 3) Enforce chain attestation (Phase 1)
        if not args.no_chain_attestation:
            chronicles_text = read_file_text(CHRONICLES_PATH)
            if CHAIN_ATTESTATION_MARKER not in chronicles_text:
                violations.append(
                    f'Missing dependency attestation in CHRONICLES. Add a line: "{CHAIN_ATTESTATION_MARKER}"\n'
                    "Include brief notes listing the canon files reviewed/updated for dependency consistency."
                )

    if violations:
        print("== Derivation Change Guard: FAIL ==")
        print("Tracked Derivation changes (exclusions applied):")
        for f in changed_tracked:
            print(f"  - {f}")
        print("\nViolations:")
        for v in violations:
            print(f"  • {v}")
        print("\nBypass note:")
        print(f"- The only bypass for Derivation changes without canon updates is to explicitly document in {CHRONICLES_PATH}.")
        print("- For legitimate canon-impacting changes, you must also update relevant canon files and attest dependency review.")
        return 1

    print("Derivation Change Guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())