"""
Test suite for contract-driven audit system.

Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.
"""

import json
import tempfile
from pathlib import Path
import pytest

import sys
# Add tools directory to path
tools_dir = Path(__file__).resolve().parents[3] / "tools"
sys.path.insert(0, str(tools_dir))

from audit_contract_driven import (
    ContractDrivenAuditor,
    AuditResult,
    RunAudit,
    DomainAudit
)


@pytest.fixture
def temp_repo():
    """Create a temporary repository structure for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        logs_root = repo_root / "Derivation" / "code" / "outputs" / "logs"
        logs_root.mkdir(parents=True)
        
        figures_root = repo_root / "Derivation" / "code" / "outputs" / "figures"
        figures_root.mkdir(parents=True)
        
        yield repo_root


def create_run_artifact(
    path: Path,
    gate_metrics: dict,
    gates: dict,
    git_commit: str = "abc123",
    provenance_ok: bool = True,
    status: str = "PASSED"
):
    """Helper to create a mock run artifact."""
    artifact = {
        "gate_metrics": gate_metrics,
        "gate_results": {
            "status": status,
            "gates": gates,
            "failed_gates": [
                k for k, v in gates.items()
                if v.get("passed") is False
            ]
        },
        "git_commit": git_commit,
        "salted_hash": "test_hash_123",
        "tree_hash": "test_tree_123",
        "provenance_ok": provenance_ok
    }
    
    with open(path, 'w') as f:
        json.dump(artifact, f)


class TestContractDrivenAuditor:
    """Test the main auditor class."""
    
    def test_auditor_initialization(self, temp_repo):
        """Test auditor can be initialized with repo root."""
        auditor = ContractDrivenAuditor(temp_repo)
        assert auditor.repo_root == temp_repo
        assert auditor.logs_root.exists()
    
    def test_audit_passed_run(self, temp_repo):
        """Test auditing a run that passes all gates."""
        # Create domain
        domain_path = temp_repo / "Derivation" / "code" / "outputs" / "logs" / "test_domain"
        domain_path.mkdir(parents=True)
        
        # Create passing run
        run_file = domain_path / "test_run_passed.json"
        create_run_artifact(
            run_file,
            gate_metrics={
                "R2_wall": 0.99,
                "beta_bias": 0.05
            },
            gates={
                "R2_wall": {
                    "metric": "R2_wall",
                    "value": 0.99,
                    "operator": ">=",
                    "threshold": 0.98,
                    "passed": True
                },
                "beta_bias": {
                    "metric": "beta_bias",
                    "value": 0.05,
                    "operator": "<=",
                    "threshold": 0.1,
                    "passed": True
                }
            },
            status="PASSED"
        )
        
        # Audit
        auditor = ContractDrivenAuditor(temp_repo)
        run_audit = auditor.audit_run(run_file, "test_domain", is_failed=False)
        
        assert run_audit is not None
        assert run_audit.overall_status == "PASSED"
        assert run_audit.provenance_status == "VERIFIED"
        assert len(run_audit.metric_audits) == 2
        assert all(a.status == "PASS" for a in run_audit.metric_audits)
    
    def test_audit_failed_run(self, temp_repo):
        """Test auditing a run that fails gates."""
        # Create domain
        domain_path = temp_repo / "Derivation" / "code" / "outputs" / "logs" / "test_domain"
        domain_path.mkdir(parents=True)
        
        # Create failing run
        run_file = domain_path / "test_run_failed.json"
        create_run_artifact(
            run_file,
            gate_metrics={
                "R2_wall": 0.95,  # Below threshold
                "beta_bias": 0.15  # Above threshold
            },
            gates={
                "R2_wall": {
                    "metric": "R2_wall",
                    "value": 0.95,
                    "operator": ">=",
                    "threshold": 0.98,
                    "passed": False
                },
                "beta_bias": {
                    "metric": "beta_bias",
                    "value": 0.15,
                    "operator": "<=",
                    "threshold": 0.1,
                    "passed": False
                }
            },
            status="FAILED"
        )
        
        # Audit
        auditor = ContractDrivenAuditor(temp_repo)
        run_audit = auditor.audit_run(run_file, "test_domain", is_failed=True)
        
        assert run_audit is not None
        assert run_audit.overall_status == "FAILED"
        assert len(run_audit.metric_audits) == 2
        assert all(a.status == "FAIL" for a in run_audit.metric_audits)
    
    def test_audit_compromised_provenance(self, temp_repo):
        """Test auditing a run with compromised provenance."""
        # Create domain
        domain_path = temp_repo / "Derivation" / "code" / "outputs" / "logs" / "test_domain"
        domain_path.mkdir(parents=True)
        
        # Create run with bad provenance
        run_file = domain_path / "test_run_compromised.json"
        create_run_artifact(
            run_file,
            gate_metrics={"R2_wall": 0.99},
            gates={
                "R2_wall": {
                    "metric": "R2_wall",
                    "value": 0.99,
                    "operator": ">=",
                    "threshold": 0.98,
                    "passed": True
                }
            },
            provenance_ok=False
        )
        
        # Audit
        auditor = ContractDrivenAuditor(temp_repo)
        run_audit = auditor.audit_run(run_file, "test_domain", is_failed=False)
        
        assert run_audit is not None
        assert run_audit.overall_status == "COMPROMISED"
        assert run_audit.provenance_status == "MISMATCH"
    
    def test_audit_no_contract(self, temp_repo):
        """Test auditing a run with no gate contract."""
        # Create domain
        domain_path = temp_repo / "Derivation" / "code" / "outputs" / "logs" / "test_domain"
        domain_path.mkdir(parents=True)
        
        # Create run without gate_results
        run_file = domain_path / "test_run_no_contract.json"
        with open(run_file, 'w') as f:
            json.dump({
                "git_commit": "abc123",
                "some_data": {"value": 123}
            }, f)
        
        # Audit
        auditor = ContractDrivenAuditor(temp_repo)
        run_audit = auditor.audit_run(run_file, "test_domain", is_failed=False)
        
        assert run_audit is not None
        assert run_audit.overall_status == "INCOMPLETE"
        assert len(run_audit.metric_audits) == 0
    
    def test_audit_domain(self, temp_repo):
        """Test auditing an entire domain."""
        # Create domain
        domain_path = temp_repo / "Derivation" / "code" / "outputs" / "logs" / "test_domain"
        domain_path.mkdir(parents=True)
        failed_path = domain_path / "failed_runs"
        failed_path.mkdir()
        
        # Create passed run
        create_run_artifact(
            domain_path / "passed_1.json",
            gate_metrics={"R2_wall": 0.99},
            gates={
                "R2_wall": {
                    "metric": "R2_wall",
                    "value": 0.99,
                    "operator": ">=",
                    "threshold": 0.98,
                    "passed": True
                }
            }
        )
        
        # Create failed run
        create_run_artifact(
            failed_path / "failed_1.json",
            gate_metrics={"R2_wall": 0.95},
            gates={
                "R2_wall": {
                    "metric": "R2_wall",
                    "value": 0.95,
                    "operator": ">=",
                    "threshold": 0.98,
                    "passed": False
                }
            },
            status="FAILED"
        )
        
        # Audit
        auditor = ContractDrivenAuditor(temp_repo)
        domain_audit = auditor.audit_domain("test_domain")
        
        assert domain_audit.domain == "test_domain"
        assert len(domain_audit.passed_runs) == 1
        assert len(domain_audit.failed_runs) == 1
        assert domain_audit.summary["total_runs"] == 2
    
    def test_metric_audit_operators(self, temp_repo):
        """Test all supported comparison operators."""
        auditor = ContractDrivenAuditor(temp_repo)
        
        # Test >=
        result = auditor._audit_metric("test_gte", 
            {"operator": ">=", "threshold": 0.5}, 0.6)
        assert result.status == "PASS"
        
        result = auditor._audit_metric("test_gte", 
            {"operator": ">=", "threshold": 0.5}, 0.4)
        assert result.status == "FAIL"
        
        # Test <=
        result = auditor._audit_metric("test_lte", 
            {"operator": "<=", "threshold": 0.5}, 0.4)
        assert result.status == "PASS"
        
        result = auditor._audit_metric("test_lte", 
            {"operator": "<=", "threshold": 0.5}, 0.6)
        assert result.status == "FAIL"
        
        # Test ==
        result = auditor._audit_metric("test_eq", 
            {"operator": "==", "threshold": 0.5}, 0.5)
        assert result.status == "PASS"
        
        result = auditor._audit_metric("test_eq", 
            {"operator": "==", "threshold": 0.5}, 0.6)
        assert result.status == "FAIL"
    
    def test_report_formatting(self, temp_repo):
        """Test report generation in different formats."""
        # Create simple domain
        domain_path = temp_repo / "Derivation" / "code" / "outputs" / "logs" / "test_domain"
        domain_path.mkdir(parents=True)
        
        create_run_artifact(
            domain_path / "test.json",
            gate_metrics={"R2_wall": 0.99},
            gates={
                "R2_wall": {
                    "metric": "R2_wall",
                    "value": 0.99,
                    "operator": ">=",
                    "threshold": 0.98,
                    "passed": True
                }
            }
        )
        
        # Audit
        auditor = ContractDrivenAuditor(temp_repo)
        domain_audits = auditor.audit_all_domains()
        
        # Text report
        text_report = auditor.format_report(domain_audits, format="text")
        assert "CONTRACT-DRIVEN AUDIT REPORT" in text_report
        assert "test_domain" in text_report
        
        # JSON report
        json_report = auditor.format_report(domain_audits, format="json")
        data = json.loads(json_report)
        assert "test_domain" in data
        assert data["test_domain"]["summary"]["total_runs"] == 1


class TestAuditResult:
    """Test the AuditResult dataclass."""
    
    def test_audit_result_creation(self):
        """Test creating an audit result."""
        result = AuditResult(
            metric="R2_wall",
            value=0.99,
            operator=">=",
            threshold=0.98,
            passed=True,
            status="PASS",
            details="R2_wall: 0.99 >= 0.98 → PASS"
        )
        
        assert result.metric == "R2_wall"
        assert result.passed is True
        assert result.status == "PASS"


class TestRunAudit:
    """Test the RunAudit dataclass."""
    
    def test_run_audit_creation(self, temp_repo):
        """Test creating a run audit."""
        run_file = temp_repo / "test.json"
        run_audit = RunAudit(
            run_file=run_file,
            domain="test_domain",
            git_commit="abc123"
        )
        
        assert run_audit.domain == "test_domain"
        assert run_audit.git_commit == "abc123"
        assert run_audit.overall_status == "PENDING"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
