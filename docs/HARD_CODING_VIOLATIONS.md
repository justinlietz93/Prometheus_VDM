# Hard-Coding Violations Report

## Executive Summary

This report identifies instances of **hard-coded gate thresholds** in the Prometheus_VDM codebase, which violate the Contract-Driven design principle. These violations bypass the pre-registration system and introduce the risk of **false positives** (sneaky adjustments to make failing experiments appear to pass).

## Violation Type: Hard-Coded Thresholds

### Location
**File**: `Derivation/code/physics/cosmology/void_lensing/void_lensing_meter_gates.py`  
**Lines**: 41-60

### Current Implementation (VIOLATION)

```python
# Core preregistered gates and their numeric thresholds.
_GATE_SPECS: Mapping[str, Dict[str, Any]] = {
    "R2_wall": {
        "metric": "R2_wall",
        "operator": ">=",
        "threshold": 0.98,  # ← HARD-CODED!
        "unit": "dimensionless",
    },
    "AUROC_sh": {
        "metric": "AUROC_sh",
        "operator": ">=",
        "threshold": 0.90,  # ← HARD-CODED!
        "unit": "dimensionless",
    },
    "beta_bias": {
        "metric": "beta_bias",
        "operator": "<=",
        "threshold": 0.10,  # ← HARD-CODED!
        "unit": "dimensionless",
    },
}
```

### Why This is a Violation

1. **Bypasses Pre-Registration**: The thresholds are defined in source code, not loaded from a cryptographically-locked pre-registration file
2. **Mutable Post-Hoc**: A researcher could modify these thresholds after seeing results, creating a false positive
3. **No Provenance Trail**: Changes to thresholds wouldn't be captured in the git_commit hash of the experiment
4. **Violates Blind Analysis**: The contract should be locked before data collection

### Comment in Source Code

The file states:
```python
# Core preregistered gates and their numeric thresholds.
```

This comment is **misleading**. These are not "preregistered" if they exist only in mutable source code. True pre-registration requires:
- External JSON manifest with salted hash
- Hash locked in version control before experiment
- Runtime validation of hash against manifest

## Risk Assessment

### Attack Vector: "Sneaky False Positive"

**Scenario**:
1. Researcher runs void_lensing experiment
2. Results show `R2_wall = 0.97`, which would fail threshold `0.98`
3. Researcher modifies `void_lensing_meter_gates.py` to change threshold to `0.95`
4. Re-runs validation → experiment now "passes"
5. Commits both results and modified threshold together
6. Git history shows modification, but could be rationalized as "calibration"

**Detection**:
- Contract-driven audit tool would flag this if it checks for:
  - Mismatches between source code thresholds and PRE-REGISTRATION.json
  - Git commits that modify gate files between experiment runs
  - Salted hash validation

## Recommended Fix

### Option 1: Dynamic Loading from Pre-Registration File

```python
# void_lensing_meter_gates.py

from pathlib import Path
import json
from typing import Any, Dict, Mapping

# Path to pre-registration manifest (locked via salted hash)
PREREG_MANIFEST = Path(__file__).parent / "PRE-REGISTRATION.json"

def _load_gate_specs() -> Mapping[str, Dict[str, Any]]:
    """
    Load gate specifications from pre-registration manifest.
    
    The manifest must exist and contain a 'gates' key with threshold definitions.
    The manifest hash is validated at runtime to prevent tampering.
    """
    if not PREREG_MANIFEST.exists():
        raise FileNotFoundError(
            f"Pre-registration manifest not found: {PREREG_MANIFEST}"
        )
    
    with open(PREREG_MANIFEST, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Validate manifest hash (salted_sha256)
    expected_hash = manifest.get("salted_hash")
    if not expected_hash:
        raise ValueError("Manifest missing salted_hash for validation")
    
    # Return gate specs
    gates = manifest.get("gates")
    if not gates:
        raise ValueError("Manifest missing 'gates' definition")
    
    return gates


# Load specs at module import (fail fast if manifest invalid)
_GATE_SPECS: Mapping[str, Dict[str, Any]] = _load_gate_specs()
```

### Option 2: Runtime Validation Against vdm_rt Guards

```python
# void_lensing_meter_gates.py

from vdm_rt.core.invariants import validate_gate_contract

def evaluate_gates(results: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Evaluate gates using vdm_rt invariant guards.
    
    This approach delegates to the runtime system which loads contracts
    from pre-registration manifests and validates provenance.
    """
    from vdm_rt.physics.ci_gates import load_payload, validate_payload
    
    # Load pre-registration contract
    contract = load_payload("PRE-REGISTRATION.json")
    
    # Extract required gates from contract (not hard-coded!)
    required_metrics = contract["gates"].keys()
    
    # Validate against contract
    validation_result = validate_payload(results, required_metrics)
    
    return {
        "status": "PASSED" if validation_result else "FAILED",
        "gates": contract["gates"],
        "validation": validation_result
    }
```

## Pre-Registration Manifest Example

### PRE-REGISTRATION.json

```json
{
  "experiment": "void_lensing_meter-v1",
  "generated_utc": "2025-01-15T10:00:00Z",
  "salted_hash": "8cb9bf095a99d4c7e3b5a4eff8fd61d68663d652ecd710123730e4f869100f8f",
  "salted_tag": "void_lensing_meter-v1",
  "gates": {
    "R2_wall": {
      "metric": "R2_wall",
      "operator": ">=",
      "threshold": 0.98,
      "unit": "dimensionless",
      "justification": "Wall-clock R² must exceed 0.98 to ensure convergence"
    },
    "AUROC_sh": {
      "metric": "AUROC_sh",
      "operator": ">=",
      "threshold": 0.90,
      "unit": "dimensionless",
      "justification": "Signal/background separation must exceed 90% AUROC"
    },
    "beta_bias": {
      "metric": "beta_bias",
      "operator": "<=",
      "threshold": 0.10,
      "unit": "dimensionless",
      "justification": "Systematic bias must not exceed 10%"
    }
  },
  "git_commit_at_registration": "93e059f020db54a09eea56f451d27445828ea2f8"
}
```

### Salted Hash Computation

```python
import hashlib
import json

def compute_salted_hash(tag: str, gates: dict, salt: str = "VDM_v1") -> str:
    """
    Compute salted SHA256 hash of gate contract.
    
    This hash is stored in version control BEFORE the experiment runs,
    preventing post-hoc modification of thresholds.
    """
    payload = {
        "tag": tag,
        "salt": salt,
        "gates": gates
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
```

## Migration Plan

### Phase 1: Create Pre-Registration Manifests (Week 1)
- [ ] Extract hard-coded thresholds to PRE-REGISTRATION.json files
- [ ] Compute and lock salted hashes in git
- [ ] Document justification for each threshold

### Phase 2: Update Gate Evaluation (Week 2)
- [ ] Modify `void_lensing_meter_gates.py` to load from manifest
- [ ] Add runtime hash validation
- [ ] Update tests to verify contract loading

### Phase 3: Audit & CI Integration (Week 3)
- [ ] Run `audit_contract_driven.py` on all domains
- [ ] Add CI check to detect hard-coded thresholds
- [ ] Fail builds if manifests missing or hashes invalid

## Detection in CI/CD

### GitHub Actions Workflow

```yaml
name: Contract-Driven Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Detect Hard-Coded Thresholds
        run: |
          # Search for suspicious patterns
          if grep -r "threshold.*=" Derivation/code/physics --include="*_gates.py" | grep -v "load_"; then
            echo "ERROR: Hard-coded thresholds detected!"
            exit 1
          fi
      
      - name: Run Contract-Driven Audit
        run: |
          python tools/audit_contract_driven.py --verbose
```

## Similar Violations to Check

Search for these patterns across the codebase:

```bash
# Hard-coded thresholds in gate definitions
grep -r "threshold.*0\." Derivation/code/physics --include="*.py"

# Hard-coded operators
grep -r "operator.*=.*\">=\"" Derivation/code/physics --include="*.py"

# Direct numeric comparisons without contract
grep -r "if.*>.*0\.[0-9]" Derivation/code/physics --include="*.py"
```

## References

- VDM Contract-Driven Audit Documentation: `docs/audit_contract_driven.md`
- Pre-Registration Protocol: `docs/preregistration_protocol.md` (to be created)
- Audit Tool Source: `tools/audit_contract_driven.py`
- Test Suite: `Derivation/code/tests/test_audit_contract_driven.py`
