# Contract-Driven Audit System for Prometheus_VDM

## Overview

The Contract-Driven Audit System provides forensic methodological validation of VDM experimental artifacts. This system is **strictly contract-driven**: it does not contain hard-coded "pass/fail" standards. Instead, it dynamically extracts success criteria from cryptographic pre-registration and gate-specification files unique to each experimental run.

## Architecture

### Core Principles

1. **Dynamic Contract Extraction**: The auditor parses `gate_results` blocks from log files to extract the pre-registered success criteria (`metric`, `operator`, `threshold`) for each experimental run.

2. **Model-Blind Auditing**: Results are evaluated solely against the pre-registered contracts. The auditor has no knowledge of what values are "good" or "bad" outside of what the contract specifies.

3. **Provenance as Primary Firewall**: Every audit verifies cryptographic hashes:
   - `git_commit`: Git repository state at experiment time
   - `salted_sha256`: Salted hash of the experimental configuration
   - `tree_hash`: Manifest tree hash for reproducibility

4. **Hostile to Hard-Coding**: The system identifies and reports any instance where runner scripts use hard-coded numeric standards instead of dynamic pre-registration lookups.

### Directory Structure

```
Derivation/code/
├── physics/{domain}/          # Runner scripts for each domain
│   ├── run_*.py              # Main experimental runners
│   └── *_gates.py            # Gate evaluation logic (should be contract-driven)
├── outputs/
│   ├── logs/{domain}/        # Experimental run logs
│   │   ├── *.json           # Passed run artifacts
│   │   └── failed_runs/     # Failed run artifacts
│   └── figures/{domain}/     # Paired visualization outputs
└── tests/                    # Test suites
```

## Gate Results Schema

Each experimental run produces a JSON artifact with the following structure:

```json
{
  "gate_metrics": {
    "metric_name": <measured_value>,
    ...
  },
  "gate_results": {
    "status": "PASSED" | "FAILED" | "PENDING_IMPLEMENTATION",
    "gates": {
      "metric_name": {
        "metric": "metric_name",
        "value": <measured_value>,
        "operator": ">=" | "<=" | "==" | ">" | "<",
        "threshold": <pre_registered_threshold>,
        "unit": "dimensionless" | ...,
        "passed": true | false | null
      },
      ...
    },
    "failed_gates": ["metric_name", ...],
    "missing_keys": ["metric_name", ...]
  },
  "git_commit": "...",
  "salted_hash": "...",
  "tree_hash": "...",
  "provenance_ok": true | false
}
```

## Usage

### Command-Line Interface

```bash
# Audit all domains
python tools/audit_contract_driven.py

# Audit specific domain
python tools/audit_contract_driven.py --domain metriplectic

# Verbose output with debugging information
python tools/audit_contract_driven.py --domain cosmology --verbose

# JSON output format
python tools/audit_contract_driven.py --json

# Save report to file
python tools/audit_contract_driven.py --output audit_report.txt
```

### Exit Codes

- `0`: All audited runs either passed their contracts or have no contract violations
- `1`: One or more runs failed their pre-registered gate contracts

## Audit Workflow

### 1. Contract Discovery

For each domain in `Derivation/code/outputs/logs/{domain}`:
- Scan all `*.json` files in main directory (passed runs)
- Scan all `*.json` files in `failed_runs/` subdirectory

### 2. Provenance Verification

For each run, verify:
- `git_commit` hash is present
- `salted_hash` matches expected format
- `provenance_ok` flag is `true`
- No provenance-related errors in gate outcomes

### 3. Contract Extraction

Extract the pre-registered contract from `gate_results`:
- For each metric in `gates`, extract:
  - `operator`: The comparison operator (e.g., `>=`, `<=`)
  - `threshold`: The numeric threshold value
  - `unit`: The measurement unit

### 4. The Confrontation

Compare measured `gate_metrics` against pre-registered thresholds:
- Apply the operator to compare `value` vs `threshold`
- **ANY** deviation is a FAIL, even by `10^-18`
- For `==` operator, use machine epsilon tolerance (`1e-15`)

### 5. Status Determination

Overall run status:
- **PASSED**: All metrics pass their contracts
- **FAILED**: One or more metrics violate their contracts
- **COMPROMISED**: Provenance verification failed
- **INCOMPLETE**: No contract found or metrics missing
- **CONTRADICTION**: Invalid operator or comparison error

### 6. Failure Analysis

For runs in `failed_runs/`:
- Identify which specific gates were violated
- Extract error messages and gate outcomes
- Report the exact threshold violation

## Report Format

### Text Report

```
================================================================================
CONTRACT-DRIVEN AUDIT REPORT
Prometheus_VDM Experimental Artifacts
================================================================================

DOMAIN: metriplectic
--------------------------------------------------------------------------------
  Total Runs:   26
  Passed Runs:  17
  Failed Runs:  9

  Status Breakdown:
    PASSED              : 15
    FAILED              : 2
    INCOMPLETE          : 9

  Provenance Breakdown:
    VERIFIED            : 24
    MISMATCH            : 1
    MISSING             : 1

  FAILED RUNS ANALYSIS:
    File: 20251009_052916_tube_spectrum_summary.json
      Status: FAILED
      Provenance: VERIFIED
      Failed Gates:
        - R2_wall: 0.975 >= 0.98 → FAIL
        - beta_bias: 0.15 <= 0.1 → FAIL
```

### JSON Report

```json
{
  "domain": {
    "summary": {
      "total_runs": 26,
      "passed_runs": 17,
      "failed_runs": 9,
      "status_breakdown": {...},
      "provenance_breakdown": {...}
    },
    "passed_runs": [...],
    "failed_runs": [
      {
        "file": "...",
        "status": "FAILED",
        "provenance": "VERIFIED",
        "metric_audits": [
          {
            "metric": "R2_wall",
            "value": 0.975,
            "operator": ">=",
            "threshold": 0.98,
            "status": "FAIL",
            "details": "R2_wall: 0.975 >= 0.98 → FAIL"
          }
        ]
      }
    ]
  }
}
```

## Integration with CI/CD

The audit tool is designed to integrate with GitHub Actions:

```yaml
- name: Contract-Driven Audit
  run: |
    python tools/audit_contract_driven.py --verbose
  continue-on-error: false
```

Exit code `1` will fail the CI build if any gate violations are detected.

## Hard-Coding Detection

The audit system is **hostile to hard-coding**. When inspecting gate evaluation code (e.g., `*_gates.py`), watch for:

### ❌ Hard-Coded Thresholds (VIOLATION)

```python
# BAD: Hard-coded thresholds
_GATE_SPECS = {
    "R2_wall": {
        "threshold": 0.98,  # ← HARD-CODED!
        "operator": ">="
    }
}
```

### ✅ Contract-Driven Thresholds (CORRECT)

```python
# GOOD: Dynamic threshold from pre-registration
def load_gate_specs(prereg_path: Path) -> Dict[str, Any]:
    with open(prereg_path) as f:
        prereg = json.load(f)
    return prereg["gates"]
```

## Metrics

Common metrics across domains:

- **R2_wall**: Coefficient of determination for wall-clock convergence
- **beta_bias**: Systematic bias in parameter estimation
- **AUROC_sh**: Area under ROC curve for signal/background separation
- **Noether_drift**: Conservation law violation magnitude
- **metriplectic_degeneracy**: Symplectic-dissipative splitting defect

Each metric has domain-specific semantics defined in the pre-registration manifest.

## Extending the System

### Adding a New Domain

1. Create runner script in `Derivation/code/physics/{domain}/`
2. Ensure runner outputs gate_results with:
   - `gates` mapping with `operator`/`threshold` for each metric
   - `gate_metrics` with measured values
   - Provenance fields: `git_commit`, `salted_hash`, `tree_hash`
3. Logs automatically saved to `outputs/logs/{domain}/`
4. Run audit: `python tools/audit_contract_driven.py --domain {domain}`

### Pre-Registration Workflow

1. Create `PRE-REGISTRATION.json` with gate specifications
2. Compute salted hash: `sha256(tag + salt + parameters)`
3. Lock hash in version control before experiment
4. Runner loads pre-registration and validates against hash
5. Audit verifies measured values against loaded contract

## Troubleshooting

### "INCOMPLETE" Status

Runs marked INCOMPLETE have no gate_results contract. Common causes:
- Skeleton implementations (phase-1 placeholders)
- Legacy runs from before contract system
- Runs that crashed before writing gate_results

### "COMPROMISED" Status

Provenance verification failed. Possible causes:
- `git_commit` hash missing or doesn't match repository state
- `salted_hash` doesn't match pre-registration
- `provenance_ok` flag is `false`

### "MISSING" Metrics

Gate contract references a metric that wasn't measured. Causes:
- Implementation incomplete for that metric
- Metric only relevant to specific experimental configurations
- Bug in metric extraction code

## References

- VDM Pre-Registration Protocol: `docs/preregistration_protocol.md`
- Gate Evaluation API: `vdm_rt/physics/ci_gates.py`
- Metriplectic Gates Example: `Derivation/code/physics/cosmology/void_lensing/void_lensing_meter_gates.py`
