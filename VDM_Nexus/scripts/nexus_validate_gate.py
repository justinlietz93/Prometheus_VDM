#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


VDM Nexus — Validation Gate Tool

Scope:
- Lives under VDM_Nexus/scripts/ (Nexus-only changes; Derivation/ is read-only).
- Runs two checks required by Phase 0 · Task 0.1:
  1) Canon diff gate with explicit exclusions for reference-only paths
  2) Local lint probes for Nexus (JSON validity, optional clang-format, optional md hygiene)

Exit codes:
- 0 = all requested checks passed
- 1 = one or more checks failed

Example:
  python VDM_Nexus/scripts/nexus_validate_gate.py \
      --base origin/main \
      --check canon-diff --check lint \
      --exclude Derivation/Converging_External_Research/** \
      --exclude Derivation/References/** \
      --exclude Derivation/Speculations/** \
      --exclude Derivation/Templates/** \
      --exclude "Derivation/Supporting_Work/external_references/**" \
      --exclude "Derivation/Supporting_Work/Physics-Based Datasets by Tier_ A Comprehensive Resource Guide.pdf"

Notes:
- This tool is read-only except for reading repository state.
- It uses git to compute diffs; ensure you run it inside the repo root.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any


DEFAULT_EXCLUSIONS = [
    "Derivation/Converging_External_Research/**",
    "Derivation/References/**",
    "Derivation/Speculations/**",
    "Derivation/Templates/**",
    "Derivation/Supporting_Work/external_references/**",
    "Derivation/Supporting_Work/Physics-Based Datasets by Tier_ A Comprehensive Resource Guide.pdf",
    "Derivation/VDM_OVERVIEW.md",
]


C_CPP_EXTS = (".h", ".hpp", ".hh", ".hxx", ".c", ".cc", ".cxx", ".cpp")


def run(cmd: List[str], cwd: str | None = None, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def git_changed_files(base_ref: str) -> List[str]:
    """
    Return list of paths changed vs base_ref...HEAD (name-only).
    """
    try:
        cp = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
        lines = [ln.strip() for ln in (cp.stdout or "").splitlines() if ln.strip()]
        return lines
    except subprocess.CalledProcessError as e:
        print(f"[error] git diff failed: {e.stdout}", file=sys.stderr)
        return []


def path_matches_globs(path: str, patterns: List[str]) -> bool:
    """
    Globbing with git-like ** support using pathlib.match on Posix form.
    """
    posix = Path(path).as_posix()
    for pat in patterns:
        # Normalize to POSIX
        p = pat.replace("\\", "/")
        if Path(posix).match(p):
            return True
    return False


def canon_diff_gate(base_ref: str, exclusions: List[str]) -> Dict[str, Any]:
    """
    Policy: "tracked canon" = any change under Derivation/ EXCEPT excluded reference-only paths.
    We do not mutate Derivation here; this tool only reports status.

    Returns dict with:
      passed: bool
      changed_tracked: [paths]
      exclusions: [patterns]
      base_ref: str
    """
    changed = git_changed_files(base_ref)
    changed_tracked = []
    for f in changed:
        if not f.startswith("Derivation/"):
            continue
        if path_matches_globs(f, exclusions):
            continue
        changed_tracked.append(f)

    return {
        "passed": len(changed_tracked) == 0,
        "changed_tracked": changed_tracked,
        "exclusions": exclusions,
        "base_ref": base_ref,
    }

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

def derivation_policy_warnings(base_ref: str, changed_tracked: List[str]) -> List[Dict[str, Any]]:
    """
    Emit non-fatal warnings for Derivation/ changes:
    - chronicles_missing: CHRONICLES.md not updated alongside tracked Derivation/ changes
    - canon_docs_missing: no canonical ALL-CAPS docs updated with Derivation/ changes

    Notes:
    - This is a WARNING-ONLY path (does not flip summary['ok']). Enforcement can be done
      via pre-commit and CI workflows that call this tool and decide policy.
    """
    warnings: List[Dict[str, Any]] = []
    if not changed_tracked:
        return warnings

    changed = git_changed_files(base_ref)
    chronicles_path = "Derivation/CHRONICLES.md"

    # Minimum documentation: CHRONICLES updated when Derivation/ changes occur
    if chronicles_path not in changed:
        warnings.append({
            "code": "chronicles_missing",
            "message": "Derivation changes detected but Derivation/CHRONICLES.md was not updated. Document pivots/corrections/shuffles to bypass stricter enforcement.",
            "details": []
        })

    # Legitimate canon edits: expect at least one ALL-CAPS canon doc in the diff
    canon_changed = [p for p in changed if p in CANON_DOCS]
    if not canon_changed:
        warnings.append({
            "code": "canon_docs_missing",
            "message": "Derivation changes detected; no canonical docs updated (EQUATIONS/VALIDATION_METRICS/ROADMAP/etc.). Legitimate changes should update relevant canon files and their dependency chain.",
            "details": CANON_DOCS
        })

    return warnings


def lint_json_under_vdm_nexus(root: Path) -> Dict[str, Any]:
    """
    Validate JSON files under VDM_Nexus/ using Python's json module.
    """
    errors = []
    scanned = 0
    for p in root.rglob("*.json"):
        try:
            scanned += 1
            with p.open("r", encoding="utf-8") as fh:
                json.load(fh)
        except Exception as e:
            errors.append({"file": str(p), "error": str(e)})
    return {
        "passed": len(errors) == 0,
        "scanned": scanned,
        "errors": errors,
    }


def lint_clang_format_under_vdm_nexus(root: Path) -> Dict[str, Any]:
    """
    Dry-run clang-format on C/C++ files if clang-format is available.
    Will use -style=file when a .clang-format exists at repo root or under VDM_Nexus/.
    """
    cf = shutil.which("clang-format")
    if not cf:
        return {
            "passed": True,  # treat as neutral pass if tool absent
            "skipped": True,
            "reason": "clang-format not installed",
        }

    files = [str(p) for p in root.rglob("*") if p.suffix.lower() in C_CPP_EXTS]
    if not files:
        return {"passed": True, "skipped": True, "reason": "no C/C++ files found"}

    # Choose style
    style = "-style=LLVM"
    repo_has = run(["git", "ls-files", "--error-unmatch", ".clang-format"], check=False)
    nexus_has = run(["git", "ls-files", "--error-unmatch", "VDM_Nexus/.clang-format"], check=False)
    if repo_has.returncode == 0 or nexus_has.returncode == 0:
        style = "-style=file"

    # Run in batches to avoid argv too long
    batch_size = 64
    errors: List[str] = []
    for i in range(0, len(files), batch_size):
        batch = files[i : i + batch_size]
        try:
            run([cf, style, "-Werror", "-n", *batch])
        except subprocess.CalledProcessError as e:
            errors.append(e.stdout or "clang-format failed")

    return {"passed": len(errors) == 0, "skipped": False, "errors": errors}


def lint_md_hygiene(repo_root: Path) -> Dict[str, Any]:
    """
    Optionally invoke tools/md_hygiene_check.py if present.
    This stays read-only and is outside VDM_Nexus/, but we only read/execute it.
    """
    tool = repo_root / "tools" / "md_hygiene_check.py"
    if not tool.exists():
        return {"passed": True, "skipped": True, "reason": "tools/md_hygiene_check.py not found"}

    try:
        cp = run([sys.executable, str(tool)])
        out = (cp.stdout or "").strip()
        return {"passed": True, "skipped": False, "output": out}
    except subprocess.CalledProcessError as e:
        return {"passed": False, "skipped": False, "output": e.stdout or "md_hygiene_check failed"}


def main() -> int:
    parser = argparse.ArgumentParser(description="VDM Nexus validation gate tool")
    parser.add_argument("--base", default="origin/main", help="Base git ref for diff (default: origin/main)")
    parser.add_argument("--check", action="append", choices=["canon-diff", "lint"], help="Which checks to run; can repeat")
    parser.add_argument("--exclude", action="append", default=[], help="Glob-style exclusions under Derivation/")
    parser.add_argument("--no-md-hygiene", action="store_true", help="Skip Markdown hygiene probe")
    parser.add_argument("--no-clang", action="store_true", help="Skip clang-format probe")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON summary")
    args = parser.parse_args()

    repo_root = Path(".").resolve()
    nexus_root = repo_root / "VDM_Nexus"

    checks = args.check or ["canon-diff", "lint"]
    exclusions = args.exclude or DEFAULT_EXCLUSIONS

    summary: Dict[str, Any] = {"ok": True, "base": args.base, "checks": {}, "exclusions": exclusions, "warnings": []}

    if "canon-diff" in checks:
        cd = canon_diff_gate(args.base, exclusions)
        summary["checks"]["canon_diff"] = cd
        if not cd["passed"]:
            summary["ok"] = False
        # Non-fatal policy warnings for Derivation changes
        if cd["changed_tracked"]:
            warn = derivation_policy_warnings(args.base, cd["changed_tracked"])
            if warn:
                summary["warnings"].extend(warn)

    if "lint" in checks:
        lint_summary: Dict[str, Any] = {}
        # JSON under VDM_Nexus
        js = lint_json_under_vdm_nexus(nexus_root)
        lint_summary["json"] = js
        if not js["passed"]:
            summary["ok"] = False

        # clang-format if not disabled
        if args.no_clang:
            lint_summary["clang_format"] = {"passed": True, "skipped": True, "reason": "disabled by flag"}
        else:
            cf = lint_clang_format_under_vdm_nexus(nexus_root)
            lint_summary["clang_format"] = cf
            if not cf["passed"]:
                summary["ok"] = False

        # md hygiene if not disabled
        if args.no_md_hygiene:
            lint_summary["md_hygiene"] = {"passed": True, "skipped": True, "reason": "disabled by flag"}
        else:
            md = lint_md_hygiene(repo_root)
            lint_summary["md_hygiene"] = md
            if not md["passed"]:
                summary["ok"] = False

        summary["checks"]["lint"] = lint_summary

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        # Human-readable report
        print("== VDM Nexus Validation Gate ==")
        print(f"Base: {summary['base']}")
        if "canon_diff" in summary["checks"]:
            cd = summary["checks"]["canon_diff"]
            print(f"\n[canon-diff] exclusions:")
            for ex in exclusions:
                print(f"  - {ex}")
            if cd["passed"]:
                print("[canon-diff] PASS — no modified files under tracked canon paths")
            else:
                print("[canon-diff] FAIL — modified files under tracked canon paths:")
                for f in cd["changed_tracked"]:
                    print(f"  - {f}")
            # Loud warnings (non-fatal) for Derivation policy
            if summary.get("warnings"):
                print("\n[canon-diff] WARNINGS (non-fatal):")
                for w in summary["warnings"]:
                    print(f"  !! {w.get('code', 'policy_warning')}: {w.get('message')}")
                    details = w.get("details") or []
                    for d in details:
                        print(f"     - {d}")

        if "lint" in summary["checks"]:
            ls = summary["checks"]["lint"]
            js = ls["json"]
            print(f"\n[lint/json] scanned={js['scanned']}  status={'PASS' if js['passed'] else 'FAIL'}")
            cf = ls["clang_format"]
            if cf.get("skipped"):
                print(f"[lint/clang-format] SKIP — {cf.get('reason','')}")
            else:
                print(f"[lint/clang-format] status={'PASS' if cf['passed'] else 'FAIL'}")
                if not cf["passed"]:
                    print("  errors:")
                    for e in cf.get("errors", []):
                        print("    -", e.strip().splitlines()[-1] if isinstance(e, str) else e)
            md = ls["md_hygiene"]
            if md.get("skipped"):
                print(f"[lint/md-hygiene] SKIP — {md.get('reason','')}")
            else:
                print(f"[lint/md-hygiene] status={'PASS' if md['passed'] else 'FAIL'}")

        print(f"\nOverall: {'PASS' if summary['ok'] else 'FAIL'}")

    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())