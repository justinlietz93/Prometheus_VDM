#!/usr/bin/env python3
"""
Example demonstrating contract-driven audit workflow.

This script shows how to:
1. Create a pre-registration manifest
2. Run an experiment that produces gate_results
3. Audit the results against the contract
4. Detect violations

Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


def create_preregistration_manifest(
    experiment_name: str,
    gates: Dict[str, Dict[str, Any]],
    output_path: Path
) -> str:
    """
    Create a pre-registration manifest with salted hash.
    
    Args:
        experiment_name: Unique experiment identifier
        gates: Gate specifications with operator/threshold
        output_path: Where to save the manifest
    
    Returns:
        Salted hash for verification
    """
    # Compute salted hash
    salt = "VDM_v1"
    payload = {
        "tag": experiment_name,
        "salt": salt,
        "gates": gates
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    salted_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    
    # Create manifest
    manifest = {
        "experiment": experiment_name,
        "version": "1.0.0",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "salted_hash": salted_hash,
        "salted_tag": experiment_name,
        "gates": gates
    }
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✓ Pre-registration manifest created: {output_path}")
    print(f"  Salted hash: {salted_hash}")
    
    return salted_hash


def create_experiment_results(
    experiment_name: str,
    measured_metrics: Dict[str, float],
    gates: Dict[str, Dict[str, Any]],
    output_path: Path,
    salted_hash: str
) -> None:
    """
    Simulate experimental results with gate evaluation.
    
    Args:
        experiment_name: Experiment identifier
        measured_metrics: Measured values for each metric
        gates: Gate specifications (from pre-registration)
        output_path: Where to save results
        salted_hash: Expected hash for provenance
    """
    # Evaluate gates
    gate_results = {
        "status": "PENDING",
        "gates": {},
        "failed_gates": []
    }
    
    for metric_name, gate_spec in gates.items():
        measured_value = measured_metrics.get(metric_name)
        operator = gate_spec["operator"]
        threshold = gate_spec["threshold"]
        
        # Evaluate
        if measured_value is not None:
            if operator == ">=":
                passed = measured_value >= threshold
            elif operator == "<=":
                passed = measured_value <= threshold
            else:
                passed = None
            
            gate_results["gates"][metric_name] = {
                "metric": metric_name,
                "value": measured_value,
                "operator": operator,
                "threshold": threshold,
                "unit": gate_spec.get("unit"),
                "passed": passed
            }
            
            if passed is False:
                gate_results["failed_gates"].append(metric_name)
        else:
            gate_results["gates"][metric_name] = {
                "metric": metric_name,
                "value": None,
                "operator": operator,
                "threshold": threshold,
                "unit": gate_spec.get("unit"),
                "passed": None
            }
    
    # Determine overall status
    if gate_results["failed_gates"]:
        gate_results["status"] = "FAILED"
    elif any(g["passed"] is None for g in gate_results["gates"].values()):
        gate_results["status"] = "INCOMPLETE"
    else:
        gate_results["status"] = "PASSED"
    
    # Create full results artifact
    results = {
        "experiment": experiment_name,
        "gate_metrics": measured_metrics,
        "gate_results": gate_results,
        "git_commit": "abc123def456",  # Simulated
        "salted_hash": salted_hash,
        "tree_hash": "tree_abc123",
        "provenance_ok": True
    }
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    status_symbol = "✓" if gate_results["status"] == "PASSED" else "✗"
    print(f"{status_symbol} Experiment results created: {output_path}")
    print(f"  Status: {gate_results['status']}")
    if gate_results["failed_gates"]:
        print(f"  Failed gates: {', '.join(gate_results['failed_gates'])}")


def main():
    print("=" * 80)
    print("CONTRACT-DRIVEN AUDIT WORKFLOW EXAMPLE")
    print("=" * 80)
    print()
    
    # Example 1: Passing experiment
    print("Example 1: Experiment that PASSES all gates")
    print("-" * 80)
    
    gates_passing = {
        "R2_wall": {
            "metric": "R2_wall",
            "operator": ">=",
            "threshold": 0.98,
            "unit": "dimensionless"
        },
        "beta_bias": {
            "metric": "beta_bias",
            "operator": "<=",
            "threshold": 0.1,
            "unit": "dimensionless"
        }
    }
    
    manifest_path = Path("example_preregistration_pass.json")
    results_path = Path("example_results_pass.json")
    
    hash1 = create_preregistration_manifest(
        "example-experiment-v1",
        gates_passing,
        manifest_path
    )
    
    create_experiment_results(
        "example-experiment-v1",
        {"R2_wall": 0.99, "beta_bias": 0.05},  # Both pass
        gates_passing,
        results_path,
        hash1
    )
    
    print()
    
    # Example 2: Failing experiment
    print("Example 2: Experiment that FAILS gates")
    print("-" * 80)
    
    gates_failing = {
        "R2_wall": {
            "metric": "R2_wall",
            "operator": ">=",
            "threshold": 0.98,
            "unit": "dimensionless"
        },
        "beta_bias": {
            "metric": "beta_bias",
            "operator": "<=",
            "threshold": 0.1,
            "unit": "dimensionless"
        }
    }
    
    manifest_path_fail = Path("example_preregistration_fail.json")
    results_path_fail = Path("example_results_fail.json")
    
    hash2 = create_preregistration_manifest(
        "example-experiment-fail-v1",
        gates_failing,
        manifest_path_fail
    )
    
    create_experiment_results(
        "example-experiment-fail-v1",
        {"R2_wall": 0.95, "beta_bias": 0.15},  # Both fail!
        gates_failing,
        results_path_fail,
        hash2
    )
    
    print()
    print("=" * 80)
    print("AUDIT THESE RESULTS")
    print("=" * 80)
    print()
    print("To audit these example results, run:")
    print(f"  python tools/audit_contract_driven.py")
    print()
    print("The audit will verify:")
    print("  1. Provenance hashes match pre-registration")
    print("  2. Measured values compared to thresholds")
    print("  3. Pass/fail status is correctly determined")
    print()
    print("Files created:")
    print(f"  - {manifest_path} (pre-registration)")
    print(f"  - {results_path} (passed experiment)")
    print(f"  - {manifest_path_fail} (pre-registration)")
    print(f"  - {results_path_fail} (failed experiment)")
    print()


if __name__ == "__main__":
    main()
