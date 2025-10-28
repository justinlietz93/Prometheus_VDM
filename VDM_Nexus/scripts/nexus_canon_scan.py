#!/usr/bin/env python3
"""
VDM Nexus — Canon Scan (Phase 1 · Task 1.1)

Purpose (read-only):
- Index canonical anchors from Derivation:
  * EQUATIONS.md → VDM-E-###
  * AXIOMS.md    → VDM-AX-A0…A7
  * VALIDATION_METRICS.md → kpi-*
- Scan Nexus Markdown for references to Derivation without anchors and flag issues.
- Validate that referenced anchors exist in the indexed canon sets.

Outputs:
- JSON index for downstream UI wiring (provenance banners, anchor menus)
- Optional GitHub Actions annotations (warnings) for missing/invalid anchors
- Non-fatal exit unless --strict is provided

Usage:
  # Build an index (JSON)
  python3 VDM_Nexus/scripts/nexus_canon_scan.py index --json

  # Scan Nexus Markdown for anchor hygiene (warn-only)
  python3 VDM_Nexus/scripts/nexus_canon_scan.py scan --root VDM_Nexus --gha

  # Strict mode (treat findings as errors, nonzero exit)
  python3 VDM_Nexus/scripts/nexus_canon_scan.py scan --root VDM_Nexus --gha --strict

Notes:
- This tool is repository-root relative. Run from repo root.
- Read-only: does not modify any files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


RE_EQ_ID = re.compile(r"\bVDM-E-(\d{3})\b", re.IGNORECASE)
RE_AX_ID = re.compile(r"\bVDM-AX-A([0-7])\b", re.IGNORECASE)
RE_KPI_ID = re.compile(r"\bkpi-[a-z0-9-]+\b", re.IGNORECASE)

DERIVATION_EQ = "Derivation/EQUATIONS.md"
DERIVATION_AX = "Derivation/AXIOMS.md"
DERIVATION_KPI = "Derivation/VALIDATION_METRICS.md"

# Link detection in Markdown lines for Derivation refs
RE_LINK_EQ_WITH_ANCHOR = re.compile(
    r"\((?:\.\./)?Derivation/EQUATIONS\.md#(vdm-e-\d{3})\)", re.IGNORECASE
)
RE_LINK_EQ_NO_ANCHOR = re.compile(
    r"\((?:\.\./)?Derivation/EQUATIONS\.md\)(?!#)", re.IGNORECASE
)

RE_LINK_AX_WITH_ANCHOR = re.compile(
    r"\((?:\.\./)?Derivation/AXIOMS\.md#(vdm-ax-a[0-7])\)", re.IGNORECASE
)
RE_LINK_AX_NO_ANCHOR = re.compile(
    r"\((?:\.\./)?Derivation/AXIOMS\.md\)(?!#)", re.IGNORECASE
)

RE_LINK_KPI_WITH_ANCHOR = re.compile(
    r"\((?:\.\./)?Derivation/VALIDATION_METRICS\.md#(kpi-[a-z0-9-]+)\)", re.IGNORECASE
)
RE_LINK_KPI_NO_ANCHOR = re.compile(
    r"\((?:\.\./)?Derivation/VALIDATION_METRICS\.md\)(?!#)", re.IGNORECASE
)


@dataclass
class Finding:
    file: str
    line: int
    col: int
    level: str  # "warning" or "error"
    code: str
    message: str

    def gha(self) -> str:
        return f"::{self.level} file={self.file},line={self.line},col={self.col}::{self.code}: {self.message}"


def run_git(args: List[str]) -> str:
    try:
        out = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode("utf-8", errors="ignore").strip()
        return out
    except Exception:
        return ""


def repo_head() -> str:
    return run_git(["git", "rev-parse", "HEAD"])


def file_last_commit(path: str) -> str:
    return run_git(["git", "log", "-n", "1", "--pretty=%H", "--", path])


def sha256_of_file(path: Path) -> Optional[str]:
    try:
        import hashlib

        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def unique(seq: List[str]) -> List[str]:
    s: Set[str] = set()
    out: List[str] = []
    for item in seq:
        key = item.lower()
        if key not in s:
            s.add(key)
            out.append(item)
    return out


def collect_ids_from_file(path: Path) -> Dict[str, List[str]]:
    text = read_text_safe(path)
    eq = [f"VDM-E-{m}" for m in RE_EQ_ID.findall(text)]
    ax = [f"VDM-AX-A{m}" for m in RE_AX_ID.findall(text)]
    kpi = [m.group(0).lower() for m in RE_KPI_ID.finditer(text)]
    return {"equations": unique(eq), "axioms": unique(ax), "kpis": unique(kpi)}


def build_index(repo_root: Path) -> Dict[str, object]:
    eq_p = repo_root / DERIVATION_EQ
    ax_p = repo_root / DERIVATION_AX
    kpi_p = repo_root / DERIVATION_KPI

    eq_ids = collect_ids_from_file(eq_p)["equations"] if eq_p.exists() else []
    ax_ids = collect_ids_from_file(ax_p)["axioms"] if ax_p.exists() else []
    # KPI anchors are not always explicitly labeled; scan file for 'kpi-' tokens
    kpi_ids = collect_ids_from_file(kpi_p)["kpis"] if kpi_p.exists() else []

    def entry(path: Path, _id: str, kind: str) -> Dict[str, object]:
        anchor = _id.lower()
        if kind == "equation":
            href = f"{DERIVATION_EQ}#{anchor}"
        elif kind == "axiom":
            href = f"{DERIVATION_AX}#{anchor}"
        else:
            href = f"{DERIVATION_KPI}#{anchor}"
        return {
            "id": _id,
            "kind": kind,
            "href": href,
            "path": str(path),
            "file_last_commit": file_last_commit(str(path)),
        }

    index = {
        "repo_head": repo_head(),
        "equations": [entry(eq_p, _id, "equation") for _id in eq_ids],
        "axioms": [entry(ax_p, _id, "axiom") for _id in ax_ids],
        "kpis": [entry(kpi_p, _id, "kpi") for _id in kpi_ids],
    }

    # Add file hashes/sizes for provenance banners when files exist
    for key, path in [("equations_md", eq_p), ("axioms_md", ax_p), ("valid_metrics_md", kpi_p)]:
        if path.exists():
            index[key] = {
                "sha256": sha256_of_file(path),
                "size_bytes": path.stat().st_size,
                "path": str(path),
                "last_commit": file_last_commit(str(path)),
            }
        else:
            index[key] = {"missing": True, "path": str(path)}

    return index


def walk_md(root: Path) -> List[Path]:
    out: List[Path] = []
    for p in root.rglob("*.md"):
        if p.is_file():
            out.append(p)
    return out


def scan_line_for_findings(md_rel_path: str, line_no: int, line: str, strict: bool, known_eq: Set[str], known_ax: Set[str], known_kpi: Set[str]) -> List[Finding]:
    f: List[Finding] = []

    # Missing anchors
    if RE_LINK_EQ_NO_ANCHOR.search(line):
        f.append(Finding(md_rel_path, line_no, 1, "error" if strict else "warning", "MD_MISSING_ANCHOR_EQ",
                         "Link to Derivation/EQUATIONS.md missing #vdm-e-### anchor"))
    if RE_LINK_AX_NO_ANCHOR.search(line):
        f.append(Finding(md_rel_path, line_no, 1, "error" if strict else "warning", "MD_MISSING_ANCHOR_AX",
                         "Link to Derivation/AXIOMS.md missing #vdm-ax-a# anchor"))
    if RE_LINK_KPI_NO_ANCHOR.search(line):
        f.append(Finding(md_rel_path, line_no, 1, "error" if strict else "warning", "MD_MISSING_ANCHOR_KPI",
                         "Link to Derivation/VALIDATION_METRICS.md missing #kpi-* anchor"))

    # Invalid anchors (present but not found in index)
    for m in RE_LINK_EQ_WITH_ANCHOR.finditer(line):
        anchor = m.group(1).lower().upper()  # normalize to VDM-E-###
        # transform to canonical form VDM-E-###
        anchor_norm = "VDM-E-" + anchor.split("-")[-1]
        if anchor_norm not in known_eq:
            f.append(Finding(md_rel_path, line_no, m.start(1) + 1, "error" if strict else "warning", "MD_INVALID_ANCHOR_EQ",
                             f"Unknown equation anchor '{m.group(1)}' (not in canon index)"))
    for m in RE_LINK_AX_WITH_ANCHOR.finditer(line):
        anchor = m.group(1).lower()
        # canonical form VDM-AX-A#
        anchor_norm = "VDM-AX-" + anchor.split("-")[-1].upper()
        if anchor_norm not in known_ax:
            f.append(Finding(md_rel_path, line_no, m.start(1) + 1, "error" if strict else "warning", "MD_INVALID_ANCHOR_AX",
                             f"Unknown axiom anchor '{m.group(1)}' (not in canon index)"))
    for m in RE_LINK_KPI_WITH_ANCHOR.finditer(line):
        anchor = m.group(1).lower()
        if anchor not in known_kpi:
            f.append(Finding(md_rel_path, line_no, m.start(1) + 1, "error" if strict else "warning", "MD_INVALID_ANCHOR_KPI",
                             f"Unknown KPI anchor '{anchor}' (not found in VALIDATION_METRICS.md)"))

    return f


def scan_nexus_markdown(repo_root: Path, root: Path, strict: bool) -> Tuple[List[Finding], Dict[str, int]]:
    index = build_index(repo_root)
    known_eq = set([e["id"] for e in index.get("equations", [])])
    known_ax = set([e["id"] for e in index.get("axioms", [])])
    known_kpi = set([e["id"].lower() for e in index.get("kpis", [])])

    totals = {"files": 0, "lines": 0}
    findings: List[Finding] = []

    for md in walk_md(root):
        rel = os.path.relpath(str(md), str(repo_root))
        totals["files"] += 1
        try:
            lines = md.read_text(encoding="utf-8", errors="ignore").splitlines(True)
        except Exception as e:
            findings.append(Finding(rel, 1, 1, "error" if strict else "warning", "MD_IO", f"Failed to read markdown: {e}"))
            continue

        for i, raw in enumerate(lines, start=1):
            line = raw.rstrip("\n\r")
            totals["lines"] += 1
            findings.extend(
                scan_line_for_findings(rel, i, line, strict, known_eq, known_ax, known_kpi)
            )

    return findings, totals


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Nexus canon indexer and anchor hygiene scanner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_index = sub.add_parser("index", help="Build a canon anchor index")
    ap_index.add_argument("--json", action="store_true", help="Emit JSON to stdout")

    ap_scan = sub.add_parser("scan", help="Scan Nexus Markdown for anchor hygiene")
    ap_scan.add_argument("--root", default="VDM_Nexus", help="Nexus root to scan (Markdown files)")
    ap_scan.add_argument("--gha", action="store_true", help="Emit GitHub Actions annotations")
    ap_scan.add_argument("--strict", action="store_true", help="Treat findings as errors (nonzero exit)")

    args = ap.parse_args(argv)
    repo_root = Path(".").resolve()

    if args.cmd == "index":
        idx = build_index(repo_root)
        if args.json:
            print(json.dumps(idx, indent=2, sort_keys=True))
        else:
            print("== VDM Nexus — Canon Anchor Index ==")
            print(f"Repo HEAD: {idx.get('repo_head','')}")
            print(f"EQUATIONS: {len(idx.get('equations', []))} entries")
            print(f"AXIOMS:    {len(idx.get('axioms', []))} entries")
            print(f"KPI:       {len(idx.get('kpis', []))} entries")
        return 0

    if args.cmd == "scan":
        root = Path(args.root)
        if not root.is_dir():
            print(f"::warning ::Scan root not found: {root}")
            return 0
        findings, totals = scan_nexus_markdown(repo_root, root, args.strict)
        # Emit
        errors = 0
        warnings = 0
        for f in findings:
            if args.gha:
                print(f.gha())
            if f.level == "error":
                errors += 1
            else:
                warnings += 1
        print(f"::notice ::Nexus Canon Scan — files={totals['files']} lines={totals['lines']} warnings={warnings} errors={errors}")
        return 1 if (args.strict and errors > 0) else 0

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))