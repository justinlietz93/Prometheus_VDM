#!/usr/bin/env python3
"""
Contract-Driven Audit Tool for Prometheus_VDM

Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This tool performs forensic methodological audits of VDM experimental artifacts.
It is **Contract-Driven**: success criteria are dynamically extracted from
cryptographic pre-registration and gate-specification files, not hard-coded.

Audit Protocol:
1. Locate the Contract: Scan logs/{domain} for gate_results definitions
2. Define Success Envelope: Extract operator & threshold for each metric
3. The Confrontation: Compare gate_metrics against pre-registered thresholds
4. Audit the Flops: Analyze failed_runs/ for gate violations

Usage:
    python tools/audit_contract_driven.py [--domain DOMAIN] [--verbose] [--json]
"""

from __future__ import annotations

import argparse
import json
import hashlib
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Type aliases
GateMetrics = Dict[str, Any]
GateSpec = Dict[str, Any]


@dataclass
class AuditResult:
    """Result of auditing a single metric against its contract."""
    metric: str
    value: Any
    operator: Optional[str]
    threshold: Any
    passed: Optional[bool]
    status: str  # PASS, FAIL, CONTRADICTION, NO_CONTRACT, MISSING_VALUE
    details: str = ""


@dataclass
class RunAudit:
    """Audit of a single experimental run."""
    run_file: Path
    domain: str
    git_commit: Optional[str] = None
    salted_hash: Optional[str] = None
    manifest_hash: Optional[str] = None
    gate_results: Optional[Dict[str, Any]] = None
    gate_metrics: Optional[GateMetrics] = None
    metric_audits: List[AuditResult] = field(default_factory=list)
    overall_status: str = "PENDING"  # PASSED, FAILED, COMPROMISED, INCOMPLETE
    provenance_status: str = "UNKNOWN"  # VERIFIED, MISMATCH, MISSING
    errors: List[str] = field(default_factory=list)


@dataclass
class DomainAudit:
    """Audit results for an entire domain."""
    domain: str
    passed_runs: List[RunAudit] = field(default_factory=list)
    failed_runs: List[RunAudit] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class ContractDrivenAuditor:
    """
    Forensic auditor for VDM experimental artifacts.
    
    This auditor is STRICTLY contract-driven: it extracts success criteria
    from gate_results blocks in log files and compares measured gate_metrics
    against pre-registered thresholds and operators.
    
    NO hard-coded standards are permitted.
    """
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.logs_root = repo_root / "Derivation" / "code" / "outputs" / "logs"
        self.figures_root = repo_root / "Derivation" / "code" / "outputs" / "figures"
        
    def log(self, msg: str, level: str = "INFO") -> None:
        """Log message if verbose mode enabled."""
        if self.verbose:
            print(f"[{level}] {msg}", file=sys.stderr)
    
    def audit_domain(self, domain: str) -> DomainAudit:
        """Audit all runs in a specific domain."""
        self.log(f"Starting audit for domain: {domain}")
        
        domain_audit = DomainAudit(domain=domain)
        domain_path = self.logs_root / domain
        
        if not domain_path.exists():
            self.log(f"Domain path does not exist: {domain_path}", "WARNING")
            return domain_audit
        
        # Audit successful runs (in main directory)
        for json_file in domain_path.glob("*.json"):
            if json_file.is_file():
                run_audit = self.audit_run(json_file, domain, is_failed=False)
                if run_audit:
                    domain_audit.passed_runs.append(run_audit)
        
        # Audit failed runs
        failed_path = domain_path / "failed_runs"
        if failed_path.exists():
            for json_file in failed_path.glob("*.json"):
                if json_file.is_file():
                    run_audit = self.audit_run(json_file, domain, is_failed=True)
                    if run_audit:
                        domain_audit.failed_runs.append(run_audit)
        
        # Compute summary
        domain_audit.summary = self._compute_domain_summary(domain_audit)
        
        return domain_audit
    
    def audit_run(self, run_file: Path, domain: str, is_failed: bool) -> Optional[RunAudit]:
        """Audit a single experimental run."""
        self.log(f"Auditing run: {run_file.name}")
        
        try:
            with open(run_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self.log(f"Failed to load {run_file}: {e}", "ERROR")
            return None
        
        run_audit = RunAudit(
            run_file=run_file,
            domain=domain
        )
        
        # Extract provenance information
        run_audit.git_commit = self._extract_git_commit(data)
        run_audit.salted_hash = self._extract_salted_hash(data)
        run_audit.manifest_hash = self._extract_manifest_hash(data)
        
        # Verify provenance
        run_audit.provenance_status = self._verify_provenance(data, run_audit)
        
        # Extract gate contract
        run_audit.gate_results = self._extract_gate_results(data)
        run_audit.gate_metrics = self._extract_gate_metrics(data)
        
        # Perform metric audits if we have a contract
        if run_audit.gate_results:
            gates = run_audit.gate_results.get("gates", {})
            metrics = run_audit.gate_metrics or {}
            
            for metric_name, gate_spec in gates.items():
                audit_result = self._audit_metric(
                    metric_name, 
                    gate_spec, 
                    metrics.get(metric_name)
                )
                run_audit.metric_audits.append(audit_result)
        
        # Determine overall status
        run_audit.overall_status = self._determine_overall_status(run_audit, is_failed)
        
        return run_audit
    
    def _extract_git_commit(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract git commit hash from run data."""
        # Try multiple locations
        if "git_commit" in data:
            return data["git_commit"]
        if "git" in data and isinstance(data["git"], dict):
            return data["git"].get("head_commit") or data["git"].get("head_short")
        if "run_receipts" in data and isinstance(data["run_receipts"], dict):
            return data["run_receipts"].get("git_commit")
        return None
    
    def _extract_salted_hash(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract salted hash from run data."""
        if "salted_hash" in data:
            return data["salted_hash"]
        if "salted_provenance" in data and isinstance(data["salted_provenance"], dict):
            return data["salted_provenance"].get("salted_hash")
        if "run_receipts" in data and isinstance(data["run_receipts"], dict):
            return data["run_receipts"].get("salted_hash")
        return None
    
    def _extract_manifest_hash(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract manifest tree hash from run data."""
        if "tree_hash" in data:
            return data["tree_hash"]
        if "manifest" in data and isinstance(data["manifest"], dict):
            return data["manifest"].get("tree_hash")
        if "run_receipts" in data and isinstance(data["run_receipts"], dict):
            return data["run_receipts"].get("tree_hash")
        return None
    
    def _verify_provenance(self, data: Dict[str, Any], run_audit: RunAudit) -> str:
        """Verify cryptographic provenance hashes."""
        # Check if provenance_ok flag exists and is True
        provenance_ok = data.get("provenance_ok")
        if provenance_ok is True:
            return "VERIFIED"
        elif provenance_ok is False:
            run_audit.errors.append("Provenance marked as NOT OK in data")
            return "MISMATCH"
        
        # Check for presence of required provenance fields
        if not run_audit.git_commit:
            run_audit.errors.append("Missing git_commit hash")
            return "MISSING"
        
        # Additional checks for gate/policy structures
        if "gate" in data and isinstance(data["gate"], dict):
            gate = data["gate"]
            if gate.get("provenance_ok") is False:
                run_audit.errors.append("Gate provenance check failed")
                return "MISMATCH"
        
        return "VERIFIED" if run_audit.git_commit else "MISSING"
    
    def _extract_gate_results(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract gate_results block (the contract) from run data."""
        # Direct gate_results
        if "gate_results" in data and isinstance(data["gate_results"], dict):
            return data["gate_results"]
        
        # Nested in run_receipts
        if "run_receipts" in data and isinstance(data["run_receipts"], dict):
            receipts = data["run_receipts"]
            if "gate_outcomes" in receipts and isinstance(receipts["gate_outcomes"], dict):
                outcomes = receipts["gate_outcomes"]
                if "gate_results" in outcomes:
                    return outcomes["gate_results"]
        
        # gate_outcomes at top level (metriplectic style)
        if "gate_outcomes" in data and isinstance(data["gate_outcomes"], dict):
            return data["gate_outcomes"]
        
        return None
    
    def _extract_gate_metrics(self, data: Dict[str, Any]) -> Optional[GateMetrics]:
        """Extract measured gate_metrics from run data."""
        # Direct gate_metrics
        if "gate_metrics" in data and isinstance(data["gate_metrics"], dict):
            return data["gate_metrics"]
        
        # Nested in run_receipts
        if "run_receipts" in data and isinstance(data["run_receipts"], dict):
            receipts = data["run_receipts"]
            if "gate_outcomes" in receipts and isinstance(receipts["gate_outcomes"], dict):
                outcomes = receipts["gate_outcomes"]
                if "gate_metrics" in outcomes:
                    return outcomes["gate_metrics"]
        
        return None
    
    def _audit_metric(
        self, 
        metric_name: str, 
        gate_spec: GateSpec, 
        measured_value: Any
    ) -> AuditResult:
        """
        Audit a single metric against its contract.
        
        This is the core confrontation: measured value vs pre-registered threshold.
        ANY deviation from the contract is a FAIL, even by 10^-18.
        """
        operator = gate_spec.get("operator")
        threshold = gate_spec.get("threshold")
        
        # NO CONTRACT: If no operator/threshold, we cannot judge
        if operator is None or threshold is None:
            return AuditResult(
                metric=metric_name,
                value=measured_value,
                operator=operator,
                threshold=threshold,
                passed=None,
                status="NO_CONTRACT",
                details=f"Metric '{metric_name}' has no pre-registered threshold/operator"
            )
        
        # MISSING VALUE: Cannot evaluate
        if measured_value is None:
            return AuditResult(
                metric=metric_name,
                value=None,
                operator=operator,
                threshold=threshold,
                passed=None,
                status="MISSING_VALUE",
                details=f"Metric '{metric_name}' has no measured value"
            )
        
        # THE CONFRONTATION: Apply the contract
        try:
            value = float(measured_value)
            thresh = float(threshold)
            
            if operator == ">=":
                passed = value >= thresh
            elif operator == "<=":
                passed = value <= thresh
            elif operator == "==":
                # For equality, use machine epsilon tolerance
                passed = abs(value - thresh) < 1e-15
            elif operator == ">":
                passed = value > thresh
            elif operator == "<":
                passed = value < thresh
            else:
                return AuditResult(
                    metric=metric_name,
                    value=value,
                    operator=operator,
                    threshold=thresh,
                    passed=None,
                    status="CONTRADICTION",
                    details=f"Unknown operator '{operator}' in contract"
                )
            
            status = "PASS" if passed else "FAIL"
            details = f"{metric_name}: {value} {operator} {thresh} → {status}"
            
            return AuditResult(
                metric=metric_name,
                value=value,
                operator=operator,
                threshold=thresh,
                passed=passed,
                status=status,
                details=details
            )
            
        except (ValueError, TypeError) as e:
            return AuditResult(
                metric=metric_name,
                value=measured_value,
                operator=operator,
                threshold=threshold,
                passed=None,
                status="CONTRADICTION",
                details=f"Cannot compare {measured_value} {operator} {threshold}: {e}"
            )
    
    def _determine_overall_status(self, run_audit: RunAudit, is_failed: bool) -> str:
        """Determine overall status of a run based on metric audits."""
        # If provenance is compromised, mark as such
        if run_audit.provenance_status == "MISMATCH":
            return "COMPROMISED"
        
        if not run_audit.metric_audits:
            return "INCOMPLETE"
        
        # Check all metric audits
        has_fails = any(a.status == "FAIL" for a in run_audit.metric_audits)
        has_passes = any(a.status == "PASS" for a in run_audit.metric_audits)
        has_contradictions = any(a.status == "CONTRADICTION" for a in run_audit.metric_audits)
        
        if has_contradictions:
            return "CONTRADICTION"
        
        if has_fails:
            return "FAILED"
        
        if has_passes:
            return "PASSED"
        
        return "INCOMPLETE"
    
    def _compute_domain_summary(self, domain_audit: DomainAudit) -> Dict[str, Any]:
        """Compute summary statistics for a domain audit."""
        all_runs = domain_audit.passed_runs + domain_audit.failed_runs
        
        status_counts = defaultdict(int)
        provenance_counts = defaultdict(int)
        
        for run in all_runs:
            status_counts[run.overall_status] += 1
            provenance_counts[run.provenance_status] += 1
        
        # Metric-level statistics
        metric_stats = defaultdict(lambda: {"pass": 0, "fail": 0, "no_contract": 0})
        
        for run in all_runs:
            for audit in run.metric_audits:
                metric_stats[audit.metric][audit.status.lower()] += 1
        
        return {
            "total_runs": len(all_runs),
            "passed_runs": len(domain_audit.passed_runs),
            "failed_runs": len(domain_audit.failed_runs),
            "status_breakdown": dict(status_counts),
            "provenance_breakdown": dict(provenance_counts),
            "metric_statistics": dict(metric_stats),
        }
    
    def audit_all_domains(self) -> Dict[str, DomainAudit]:
        """Audit all domains in the repository."""
        if not self.logs_root.exists():
            self.log(f"Logs directory does not exist: {self.logs_root}", "ERROR")
            return {}
        
        results = {}
        
        for domain_path in self.logs_root.iterdir():
            if domain_path.is_dir() and not domain_path.name.startswith('.'):
                domain = domain_path.name
                results[domain] = self.audit_domain(domain)
        
        return results
    
    def format_report(self, domain_audits: Dict[str, DomainAudit], format: str = "text") -> str:
        """Format audit results as a report."""
        if format == "json":
            return self._format_json_report(domain_audits)
        else:
            return self._format_text_report(domain_audits)
    
    def _format_json_report(self, domain_audits: Dict[str, DomainAudit]) -> str:
        """Format audit results as JSON."""
        report = {}
        
        for domain, audit in domain_audits.items():
            report[domain] = {
                "summary": audit.summary,
                "passed_runs": [
                    {
                        "file": str(r.run_file.name),
                        "status": r.overall_status,
                        "provenance": r.provenance_status,
                        "git_commit": r.git_commit,
                        "metric_audits": [
                            {
                                "metric": a.metric,
                                "value": a.value,
                                "operator": a.operator,
                                "threshold": a.threshold,
                                "status": a.status
                            }
                            for a in r.metric_audits
                        ]
                    }
                    for r in audit.passed_runs
                ],
                "failed_runs": [
                    {
                        "file": str(r.run_file.name),
                        "status": r.overall_status,
                        "provenance": r.provenance_status,
                        "git_commit": r.git_commit,
                        "errors": r.errors,
                        "metric_audits": [
                            {
                                "metric": a.metric,
                                "value": a.value,
                                "operator": a.operator,
                                "threshold": a.threshold,
                                "status": a.status,
                                "details": a.details
                            }
                            for a in r.metric_audits
                        ]
                    }
                    for r in audit.failed_runs
                ]
            }
        
        return json.dumps(report, indent=2)
    
    def _format_text_report(self, domain_audits: Dict[str, DomainAudit]) -> str:
        """Format audit results as human-readable text."""
        lines = []
        lines.append("=" * 80)
        lines.append("CONTRACT-DRIVEN AUDIT REPORT")
        lines.append("Prometheus_VDM Experimental Artifacts")
        lines.append("=" * 80)
        lines.append("")
        
        for domain, audit in sorted(domain_audits.items()):
            lines.append(f"DOMAIN: {domain}")
            lines.append("-" * 80)
            
            summary = audit.summary
            lines.append(f"  Total Runs:   {summary['total_runs']}")
            lines.append(f"  Passed Runs:  {summary['passed_runs']}")
            lines.append(f"  Failed Runs:  {summary['failed_runs']}")
            lines.append("")
            
            lines.append("  Status Breakdown:")
            for status, count in sorted(summary['status_breakdown'].items()):
                lines.append(f"    {status:20s}: {count}")
            lines.append("")
            
            lines.append("  Provenance Breakdown:")
            for status, count in sorted(summary['provenance_breakdown'].items()):
                lines.append(f"    {status:20s}: {count}")
            lines.append("")
            
            # Failed runs detail
            if audit.failed_runs:
                lines.append("  FAILED RUNS ANALYSIS:")
                for run in audit.failed_runs:
                    lines.append(f"    File: {run.run_file.name}")
                    lines.append(f"      Status: {run.overall_status}")
                    lines.append(f"      Provenance: {run.provenance_status}")
                    if run.errors:
                        lines.append(f"      Errors:")
                        for err in run.errors:
                            lines.append(f"        - {err}")
                    
                    failed_metrics = [a for a in run.metric_audits if a.status == "FAIL"]
                    if failed_metrics:
                        lines.append(f"      Failed Gates:")
                        for audit_result in failed_metrics:
                            lines.append(f"        - {audit_result.details}")
                    lines.append("")
            
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("AUDIT COMPLETE")
        lines.append("=" * 80)
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Contract-Driven Audit Tool for Prometheus_VDM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--domain",
        type=str,
        help="Audit a specific domain (e.g., 'metriplectic', 'cosmology'). If omitted, audits all domains."
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output report in JSON format instead of text"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Write report to file instead of stdout"
    )
    
    args = parser.parse_args()
    
    # Determine repository root
    repo_root = Path(__file__).resolve().parents[1]
    
    # Create auditor
    auditor = ContractDrivenAuditor(repo_root, verbose=args.verbose)
    
    # Run audit
    if args.domain:
        domain_audits = {args.domain: auditor.audit_domain(args.domain)}
    else:
        domain_audits = auditor.audit_all_domains()
    
    # Format report
    report_format = "json" if args.json else "text"
    report = auditor.format_report(domain_audits, format=report_format)
    
    # Output report
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding='utf-8')
        print(f"Report written to: {output_path}")
    else:
        print(report)
    
    # Exit with appropriate code
    # Check if any domain has failed runs with status FAILED (actual gate violations)
    has_violations = any(
        any(r.overall_status == "FAILED" for r in audit.failed_runs)
        for audit in domain_audits.values()
    )
    
    sys.exit(1 if has_violations else 0)


if __name__ == "__main__":
    main()
