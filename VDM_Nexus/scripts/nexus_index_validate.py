#!/usr/bin/env python3
"""
VDM Nexus — Roadmap Index Validation (Task 1.3 Validation)

Purpose:
- Read the generated roadmap index JSON (nexus-roadmap-index.v1.json)
- Compute key metrics independently and check internal consistency gates:
  1) summary.code_domains == len(code_domains)
  2) summary.doc_buckets == len(doc_buckets)
  3) summary.proposals_total == sum(len(b.proposals) for b in doc_buckets)
  4) summary.results_total == sum(len(b.results) for b in doc_buckets)
  5) summary.proposals_missing_results == count(not has_results) from proposal_status
- Additionally compute read-only counters for:
  - pending_approvals: sum over code_domains of allowed_tags without approved_at
  - artifacts_total: sum over code_domains.outputs of (logs_total + figures_total)
- Emit a JSON report under VDM_Nexus/reports/nexus-index-validation.v1.json
  with pass/fail booleans per gate and overall "passed" field.

Policy:
- Read-only validation; no writes to Derivation/.
- Deterministic, sorted JSON output (indent=2, sort_keys=True).

References:
- Index builder: [nexus_roadmap_index.py](../scripts/nexus_roadmap_index.py:1)
- Architecture: [NEXUS_ARCHITECTURE.md](../NEXUS_ARCHITECTURE.md:1)
- Checklist: [TODO_CHECKLIST.md](../TODO_CHECKLIST.md:1)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def compute_pending_approvals(index: Dict[str, Any]) -> int:
    pending = 0
    for cd in index.get("code_domains", []):
        approvals = cd.get("approvals", {}) or {}
        allowed = approvals.get("allowed_tags", []) or []
        approved_map = approvals.get("approvals", {}) or {}
        for tag in allowed:
            meta = approved_map.get(tag) or {}
            approved_at = (meta.get("approved_at") or "").strip()
            if not approved_at:
                pending += 1
    return pending


def compute_artifact_totals(index: Dict[str, Any]) -> int:
    logs = 0
    figs = 0
    for cd in index.get("code_domains", []):
        outputs = cd.get("outputs", {}) or {}
        logs += int(outputs.get("logs_total") or 0)
        figs += int(outputs.get("figures_total") or 0)
    return logs + figs


def validate_index(index: Dict[str, Any]) -> Dict[str, Any]:
    # Derived metrics
    n_code_domains = len(index.get("code_domains", []))
    n_doc_buckets = len(index.get("doc_buckets", []))
    proposals_total = sum(len(b.get("proposals", [])) for b in index.get("doc_buckets", []))
    results_total = sum(len(b.get("results", [])) for b in index.get("doc_buckets", []))
    props_missing = sum(1 for row in index.get("proposal_status", []) if not bool(row.get("has_results", False)))

    # Reported summary (may be missing keys)
    summary = index.get("summary", {}) or {}
    rep_code_domains = int(summary.get("code_domains") or 0)
    rep_doc_buckets = int(summary.get("doc_buckets") or 0)
    rep_proposals_total = int(summary.get("proposals_total") or 0)
    rep_results_total = int(summary.get("results_total") or 0)
    rep_proposals_missing = int(summary.get("proposals_missing_results") or 0)

    # Gates
    gates = {
        "g1_code_domains_count_match": (rep_code_domains == n_code_domains),
        "g2_doc_buckets_count_match": (rep_doc_buckets == n_doc_buckets),
        "g3_proposals_total_match": (rep_proposals_total == proposals_total),
        "g4_results_total_match": (rep_results_total == results_total),
        "g5_proposals_missing_results_match": (rep_proposals_missing == props_missing),
    }

    computed = {
        "code_domains": n_code_domains,
        "doc_buckets": n_doc_buckets,
        "proposals_total": proposals_total,
        "results_total": results_total,
        "proposals_missing_results": props_missing,
        "pending_approvals": compute_pending_approvals(index),
        "artifacts_total": compute_artifact_totals(index),
    }

    reported = {
        "code_domains": rep_code_domains,
        "doc_buckets": rep_doc_buckets,
        "proposals_total": rep_proposals_total,
        "results_total": rep_results_total,
        "proposals_missing_results": rep_proposals_missing,
    }

    passed = all(gates.values())

    return {
        "updated_utc": iso_now(),
        "repo_head": index.get("repo_head"),
        "index_set": {
            "set_id": index.get("set_id"),
            "set_version": index.get("set_version"),
        },
        "computed": computed,
        "reported": reported,
        "gates": gates,
        "passed": passed,
        "notes": [
            "Pending approvals and artifacts_total are computed for dashboard use; no corresponding summary fields in index.",
            "All gates are internal consistency checks; index should be regenerated if any fail.",
        ],
    }


def default_index_path(repo_root: Path) -> Path:
    return repo_root / "VDM_Nexus" / "reports" / "nexus-roadmap-index.v1.json"


def default_report_path(repo_root: Path) -> Path:
    return repo_root / "VDM_Nexus" / "reports" / "nexus-index-validation.v1.json"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate nexus-roadmap-index.v1.json and emit validation report")
    ap.add_argument("--repo-root", default=".", help="Path to repository root (default: .)")
    ap.add_argument("--index", help="Path to nexus-roadmap-index.v1.json (default: under VDM_Nexus/reports)")
    ap.add_argument("--out", help="Path to write validation JSON (default: VDM_Nexus/reports/nexus-index-validation.v1.json)")
    args = ap.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    index_path = Path(args.index) if args.index else default_index_path(repo_root)
    out_path = Path(args.out) if args.out else default_report_path(repo_root)

    if not index_path.exists():
        raise FileNotFoundError(f"Index JSON not found: {index_path}")

    index = read_json(index_path)
    report = validate_index(index)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write("\n")

    # Print short human summary
    print("[NEXUS][INDEX][VALIDATION]", "PASS" if report["passed"] else "FAIL")
    print("  repo_head:", report.get("repo_head"))
    print("  gates:", ", ".join([f"{k}={str(v)}" for k, v in report["gates"].items()]))
    print("  computed:", json.dumps(report["computed"], sort_keys=True))
    print("  out:", out_path.relative_to(repo_root) if str(out_path).startswith(str(repo_root)) else str(out_path))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())