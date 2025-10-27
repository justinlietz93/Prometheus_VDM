#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Markdown hygiene check: UTF-8 (no BOM), mojibake scan, and canonical link paths.

Usage:
  python Prometheus_VDM/tools/md_hygiene_check.py --root Prometheus_VDM/derivation

Exit codes:
  0 = all checks pass
  1 = issues found

Checks:
- Encoding: file decodes as UTF-8 and has no BOM.
- Mojibake: flags common sequences (â, Â, Ã, Ï, Î, replacement char �).
- Link targets: flags stale/moved doc paths and non-canonical prefixes per repo reorg.
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import json
from typing import List, Dict, Any, Tuple

MOJIBAKE_PATTERN = re.compile(r"[âÂÃÏÎ�]")
# Also catch the common misspelling used earlier
BAD_TYPO_PATTERN = re.compile(r"voxtrrium")

# Canonical path expectations (relative to repo root)
# Keys are filename stems or bad prefixes; values are canonical substrings that should appear in links
CANONICAL_LINK_RULES: List[Tuple[re.Pattern, str]] = [
    # Stale bare filenames (must include their topic subfolder)
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/discrete_to_continuum\.md(?:[:)#])"), "(Prometheus_VDM/derivation/foundations/discrete_to_continuum.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/kinetic_term_derivation\.md(?:[:)#])"), "(Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/fum_voxtrium_mapping\.md(?:[:)#])"), "(Prometheus_VDM/derivation/effective_field_theory/fum_voxtrium_mapping.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/effective_field_theory_approach\.md(?:[:)#])"), "(Prometheus_VDM/derivation/effective_field_theory/effective_field_theory_approach.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/symmetry_analysis\.md(?:[:)#])"), "(Prometheus_VDM/derivation/foundations/symmetry_analysis.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/discrete_conservation\.md(?:[:)#])"), "(Prometheus_VDM/derivation/conservation_law/discrete_conservation.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/rd_front_speed_validation\.md(?:[:)#])"), "(Prometheus_VDM/derivation/reaction_diffusion/rd_front_speed_validation.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/rd_dispersion_validation\.md(?:[:)#])"), "(Prometheus_VDM/derivation/reaction_diffusion/rd_dispersion_validation.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/rd_validation_plan\.md(?:[:)#])"), "(Prometheus_VDM/derivation/reaction_diffusion/rd_validation_plan.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/memory_steering\.md(?:[:)#])"), "(Prometheus_VDM/derivation/memory_steering/memory_steering.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/void_dynamics_theory\.md(?:[:)#])"), "(Prometheus_VDM/derivation/foundations/void_dynamics_theory.md"),
    # Computational proofs canonicalization
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/computational_proofs/"), "(Prometheus_VDM/derivation/code/computational_proofs/"),
    (re.compile(r"\((?:\.\./)*computational_proofs/"), "(Prometheus_VDM/derivation/code/computational_proofs/"),
    # Voxtrium source file moved to supporting_work/voxtrium (example representative)
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/voxtrium/voxtrium_message\.txt"), "(Prometheus_VDM/derivation/supporting_work/voxtrium/"),
    # Additional topical mappings
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/finite_tube_mode_analysis\.md(?:[:)#])"), "(Prometheus_VDM/derivation/tachyon_condensation/finite_tube_mode_analysis.md"),
    (re.compile(r"\((?:Prometheus_VDM/)?derivation/continuum_stack\.md(?:[:)#])"), "(Prometheus_VDM/derivation/foundations/continuum_stack.md"),
]

def list_md_files(root: str) -> List[str]:
    files: List[str] = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith(".md"):
                files.append(os.path.join(dirpath, fn))
    files.sort()
    return files

def check_utf8_no_bom(path: str) -> Dict[str, Any]:
    with open(path, "rb") as f:
        data = f.read()
    has_bom = data.startswith(b"\xef\xbb\xbf")
    ok_utf8 = True
    try:
        _ = data.decode("utf-8")
    except UnicodeDecodeError as e:
        ok_utf8 = False
    return {"ok_utf8": ok_utf8, "has_bom": has_bom}

def check_mojibake(text: str) -> List[str]:
    return [m.group(0) for m in MOJIBAKE_PATTERN.finditer(text)]

def check_bad_typo(text: str) -> List[str]:
    return [m.group(0) for m in BAD_TYPO_PATTERN.finditer(text)]

def check_links(text: str) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    for patt, expected in CANONICAL_LINK_RULES:
        for m in patt.finditer(text):
            issues.append({"bad_fragment": m.group(0), "expected_hint": expected})
    return issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Prometheus_VDM/derivation", help="root directory to scan (default: Prometheus_VDM/derivation)")
    ap.add_argument("--json", action="store_true", help="emit JSON report")
    args = ap.parse_args()

    all_md = list_md_files(args.root)
    report: Dict[str, Any] = {"root": args.root, "files_scanned": len(all_md), "issues": []}
    failures = 0

    for path in all_md:
        file_issue: Dict[str, Any] = {"path": path}
        enc = check_utf8_no_bom(path)
        with open(path, "rb") as f:
            raw = f.read()
        text = ""
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as e:
            pass

        mojibake_hits = check_mojibake(text) if text else []
        typo_hits = check_bad_typo(text) if text else []
        link_issues = check_links(text) if text else []

        problems = []
        if not enc["ok_utf8"]:
            problems.append("not_utf8")
        if enc["has_bom"]:
            problems.append("bom_present")
        if mojibake_hits:
            problems.append(f"mojibake:{','.join(sorted(set(mojibake_hits)))}")
        if typo_hits:
            problems.append(f"typo:{','.join(sorted(set(typo_hits)))}")
        if link_issues:
            problems.append(f"links:{len(link_issues)}")

        if problems:
            failures += 1
            file_issue["encoding"] = enc
            if mojibake_hits:
                file_issue["mojibake_samples"] = sorted(list(set(mojibake_hits)))[:5]
            if typo_hits:
                file_issue["typos"] = sorted(list(set(typo_hits)))[:5]
            if link_issues:
                # include first few hints
                file_issue["link_issues"] = link_issues[:10]
            file_issue["summary"] = problems
            report["issues"].append(file_issue)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"[md_hygiene_check] Scanned {report['files_scanned']} markdown files under {args.root}")
        if report["issues"]:
            print(f"[md_hygiene_check] Found issues in {len(report['issues'])} files:")
            for issue in report["issues"]:
                print(f" - {issue['path']}")
                for s in issue.get("summary", []):
                    print(f"    * {s}")
                for li in issue.get("link_issues", []) or []:
                    print(f"    * link: {li['bad_fragment']} -> EXPECT {li['expected_hint']}")
        else:
            print("[md_hygiene_check] No issues found.")

    sys.exit(0 if failures == 0 else 1)

if __name__ == "__main__":
    main()