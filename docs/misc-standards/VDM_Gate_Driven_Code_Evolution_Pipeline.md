
# **VDM Gate-Driven Code Evolution Pipeline (G-Evolve)**

**Date:** 2025-11-09
**Author:** Justin K. Lietz
**Commit:** c2d71627c286029ae90267e4051411fa1fb3973e
**Version:** 1.0-Spec — Draft for implementation
**Purpose:** Autonomous, strictly-bounded system that evolves code for VDM solvers and instruments
**Goal:** Achieve optimal numerical accuracy, physical fidelity, and performance *without* allowing information leakage, gate tampering, or overfitting

---

## **1. System Overview**

### **1.1 Core Principle**

The system evolves *code* (not parameters) under a closed-box contract:

* The agent proposes code patches.
* A detached **Verifier** runs immutable tests and measures metrics.
* Only anonymized, aggregate feedback (the **Scorecard**) returns to the agent.
* Hard gates (physics, stability, performance, reproducibility) define admissibility.
* Passing candidates emit full **Provenance Receipts** and can be human-reviewed.

### **1.2 High-Level Diagram**

```text
         ┌────────────────────────────────────────────────────────┐
         │                     Controller (Agent)                 │
         │  - Mutate / generate code                              │
         │  - Maintain candidate population                       │
         │  - Use aggregates from Scorecards for guidance         │
         └──────────────┬─────────────────────────────────────────┘
                        │
        Read-only Gate Specs (JSON)
                        │
                        ▼
         ┌────────────────────────────────────────────────────────┐
         │                    Evaluator Harness                   │
         │  Container C (Candidate): runs proposed code            │
         │  Container V (Verifier): holds tests & gold truths      │
         │  - Executes cascade (selection, hold-out, replay)       │
         │  - Computes metrics, applies hard gates                 │
         │  - Returns blinded Scorecard                            │
         └────────────────────────────────────────────────────────┘
                        │
                        ▼
         ┌────────────────────────────────────────────────────────┐
         │                    Program Database                    │
         │  - Stores candidates, diffs, scorecards, provenance     │
         │  - Handles selection, archiving, audits                │
         └────────────────────────────────────────────────────────┘
```

---

## **2. Core Components**

### **2.1 Controller**

| Responsibility        | Details                                                                         |
| --------------------- | ------------------------------------------------------------------------------- |
| Code Evolution        | Generates candidate code patches (diff-based, search/replace blocks).           |
| Prompt Assembly       | Uses previous Scorecards and aggregate hints (not labels).                      |
| Population Management | MAP-Elites or NSGA-II across objectives (accuracy, runtime, size).              |
| Security              | Read-only access to gate JSONs; no filesystem/network beyond allowed workspace. |
| Interfaces            | `submit_candidate(code_id, diff)`, `receive_scorecard(candidate_id, scorecard)` |

### **2.2 Evaluator Harness**

Two isolated containers:

* **Container C (Candidate):** runs user code on streamed inputs; cannot see tests or expected outputs.
* **Container V (Verifier):** owns gold data and computes metrics.

Evaluation cascade:

1. **Selection Set:** visible thresholds; aggregate metrics returned.
2. **Hidden Hold-out Set:** unseen data, same metrics returned only if selection passes.
3. **Cold Replay:** re-run in fresh container with fixed seed; must reproduce.

### **2.3 Program Database**

* Stores source, diffs, metrics, gates, provenance receipts, artifacts.
* Deduplicates by hash; keeps top-K per Pareto front.
* Provides audit trail for all experiments.

### **2.4 Gate Registry**

* Versioned JSON definitions for each benchmark or instrument.
* Defines hard/soft gates, resource budgets, allow-lists, and prohibited methods.

### **2.5 Provenance Recorder**

* Captures container digest, compiler hashes, seeds, timing, hardware info, gate verdicts.
* Emits immutable `provenance.json` in each artifact bundle.

---

## **3. Evaluation Contracts**

### **3.1 Scorecard Schema**

```json
{
  "candidate_id": "uuid",
  "evaluation_id": "uuid",
  "hard_gates": {
    "pass": true,
    "violations": []
  },
  "metrics": {
    "pass_rate": 1.0,
    "runtime_p95_ms": 63.2,
    "memory_mb": 228,
    "error_quantiles": {"q50": 1.2e-5, "q90": 4.1e-5, "q99": 2.3e-4}
  },
  "properties": {
    "linearity": {"violations": 0},
    "parseval": {"violations": 0}
  },
  "hints": ["focus_runtime"],
  "timestamp": "2025-11-09T14:32:00Z"
}
```

Returned to agent only; never exposes per-case data or labels.

### **3.2 Gate Schema Example**

```json
{
  "$schema": "https://vdm.local/schema/gate.v1.json",
  "name": "fft-transform-bench",
  "version": "1.0.0",
  "policy": {
    "network": "deny",
    "syscalls_allow": ["read","write","fstat","mmap","munmap","brk","exit"],
    "max_cpu_seconds": 30,
    "max_memory_mb": 512
  },
  "hard_gates": [
    {"metric": "unit_pass_rate", "op": ">=", "value": 1.0},
    {"metric": "holdout_pass", "op": "==", "value": true},
    {"metric": "mutation_score", "op": ">=", "value": 0.85},
    {"metric": "wall_time_ms", "op": "<=", "value": 500},
    {"metric": "max_rss_mb", "op": "<=", "value": 256}
  ],
  "soft_objectives": [
    {"metric": "avg_latency_ms", "goal": "min"},
    {"metric": "cyclomatic_complexity", "goal": "min"}
  ],
  "hidden_holdouts": {
    "seed_count": 100,
    "distribution": "private"
  }
}
```

---

## **4. Enforcement & Anti-Cheat Rules**

| Class                      | Enforcement                                           | Method                            |
| -------------------------- | ----------------------------------------------------- | --------------------------------- |
| **Test Isolation**         | Candidate never mounts test data or expected results. | Read-only mount to Verifier only. |
| **Label Blindness**        | Only aggregated metrics returned.                     | Scorecard filtering.              |
| **Mutation Testing**       | Verify assertions fail when inverted.                 | `mutation_score >= threshold`.    |
| **Property Oracles**       | Check invariants (linearity, symmetry, conservation). | Property-based fuzzing.           |
| **Metamorphic Tests**      | Perturb inputs, expect invariant deltas.              | Randomized pairs.                 |
| **Side-Channel Hardening** | Block network, restrict syscalls, hide clocks.        | Seccomp, ROFS, monotonic timers.  |
| **Determinism**            | Require identical results across cold replays.        | Compare SHA-256 of outputs.       |
| **Provenance Integrity**   | Hash container + sources; sign receipts.              | Digital signatures.               |

---

## **5. Dataflow & Lifecycle**

1. **Initialization**

   * Load benchmark gate JSONs.
   * Initialize Program DB with seeds (baseline algorithms).
2. **Iteration Loop**

   * Controller proposes diffs → Evaluator builds & runs → Scorecard back.
   * Disqualify any candidate failing hard gates.
   * Update population via Pareto ranking on soft metrics (runtime, size).
3. **Verification**

   * Periodic hold-out revalidation.
   * Cold-replay verification before promotion.
4. **Promotion**

   * Archive candidate + receipts in Program DB.
   * Mark as “Validated” → eligible for real VDM experiment integration.
5. **Audit**

   * Independent auditor replays top candidates using receipts.
   * Compare metrics; discrepancies auto-invalidate.

---

## **6. Interface Summary**

| Interface           | Direction              | Description                               |
| ------------------- | ---------------------- | ----------------------------------------- |
| `/submit_candidate` | Controller → Evaluator | Uploads candidate code artifact.          |
| `/evaluate`         | Evaluator internal     | Runs cascade; returns Scorecard.          |
| `/scorecard`        | Evaluator → Controller | Aggregated feedback only.                 |
| `/provenance`       | Evaluator → DB         | Full receipts, immutable.                 |
| `/archive`          | DB                     | Store candidate + Scorecard + Provenance. |

---

## **7. Performance & Scaling**

* Async worker pool in Evaluator; parallel container launches via AMD ROCm stack.
* Each run capped by CPU seconds and memory budgets.
* Scheduler throttles concurrent evaluations to maintain deterministic metrics.
* Target throughput: 1 000–2 000 candidate evaluations/day on 8 GPUs.

---

## **8. Quality Gates (Software Engineering)**

| Rule                                    | Limit                                         |
| --------------------------------------- | --------------------------------------------- |
| LOC per file                            | ≤ 500                                         |
| Cyclomatic complexity                   | ≤ 15 per function                             |
| Tests mirror source tree                | Required                                      |
| Domain models                           | Plain objects, no framework deps              |
| Imports follow clean-architecture edges | Enforced                                      |
| Code coverage                           | ≥ 90 % on unit tests                          |
| Mutation score                          | ≥ 0.85                                        |
| CI checks                               | lint, static analysis, gate schema validation |

---

## **9. Deliverables**

Each “passing” candidate produces:

```text
artifact/
  code/
    src/...          # Generated source
  logs/
    build.log
    evaluator.log
    static_analysis.json
    mutation_report.json
  receipts/
    gates.verdict.json
    provenance.json
    performance.json
  reproducible/
    Dockerfile
    lockfiles/
```

---

## **10. Extension Hooks (for VDM Integration)**

| Hook                      | Purpose                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| `vdm_export_interface.py` | Converts candidate solver into VDM-compliant module.                         |
| `gate_metrics_vdm.py`     | Adds domain-specific gates (Noether drift, Lyapunov monotonicity, locality). |
| `notebook_adapter.ipynb`  | Loads top candidates into VDM experimental notebooks.                        |

---

## **11. Verification Checklist**

| Item                  | Verification Method            |
| --------------------- | ------------------------------ |
| Hard gates all green  | Automated gate JSON evaluation |
| Hold-out passes       | Hidden test replay             |
| Cold replay identical | Output hash compare            |
| Mutation ≥ threshold  | MutPy or cosmic-ray runner     |
| Property tests pass   | Hypothesis property fuzz       |
| Static analysis clean | Ruff / Bandit / Clang-tidy     |
| Provenance signed     | SHA-256 digest verified        |
| Audit re-run matches  | Independent replay             |

---

## **12. Benefits**

* **Uncheatable Optimization:** Agent can’t access test labels or modify gates.
* **Audit-Ready Science:** Every claim reproducible with receipts.
* **Scalable Evolution:** Parallel async evaluation with deterministic verification.
* **Cross-Domain Use:** Same architecture handles FFT, RD, KG, or FRW meters.
* **Human Control:** You review code, not results; gates guarantee honesty.

---

## **13. Future Enhancements**

* Reinforcement-learning-guided proposal ranking (using scorecard distributions).
* Formal verification of conservation properties via symbolic analyzers.
* Multi-agent specialization: separate “mutator,” “critic,” “architect” roles.
* Integration with experimental VDM notebooks for *in-situ* solver validation.
* Automatic report generation (RESULTS-style PDFs with gate tables).

---

**Summary:**
This specification defines an evolver that can *only* improve algorithms by actually improving them. It can’t memorize, spoof, or hack tests. Every promotion is a demonstrable, auditable gain in physical fidelity and efficiency—exactly the environment required to converge on optimal, high-precision VDM instruments.
