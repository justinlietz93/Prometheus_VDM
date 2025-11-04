Here’s a simple, plug‑and‑play way to tie your **theory milestones (T‑tiers)** to your **software deliverables (Nexus/Studio)** so both streams move in lock‑step.

---

# Dual Roadmap: T‑Tiers ⇄ Nexus/Studio

**What this is:**
A single view that shows (a) theory validation gates (T0–T6/7) and (b) the app/modules they unlock in Nexus/Studio. Each theory gate becomes a **dependency** for specific features, so code only ships once its physics/metrics are proven at the right tier.

**Key ideas (plain English):**

* **T‑tiers** = proof levels (from concept → benchmarked, reproducible, peer‑comparable).
* **Nexus/Studio** = your desktop app + services (runners, memory, viewport, agents, data IO).
* **Rule:** a module can’t graduate from “experimental” → “stable” unless its linked T‑gate is passed.

---

## 1) Minimal tier scale (use/adjust as needed)

* **T0 Concept** → coherent hypothesis, success metrics sketched
* **T1 Instrument** → runnable experiment spec + IO paths + sanity checks
* **T2 First Signal** → repeatable signal above noise; failure modes logged
* **T3 Validation** → cross‑dataset/seed stability; ablations; baselines beat
* **T4 Robustness** → perturbations, domain shift, hardware repeatability
* **T5 Benchmark** → external baselines; effect sizes with CIs; prereg log
* **T6 Result** → DOI’d package + reproduction script; third‑party rerun
* **T7 Field‑ready** → long‑horizon stability + independent confirmation

---

## 2) Dependency schema (one‑liners you can paste into a planner)

* **Nexus/Viewport · Echo Overlay** depends on **T3 Echo Witness**
* **Nexus/Runner · Metriplectic Integrator v1** depends on **T2 J/M Split Stability**
* **Nexus/MemGraph · Steering API** depends on **T3 Policy‑free Steering Metric**
* **Studio/Experiment Wizard** depends on **T2 Run‑Manifest Spec**
* **Nexus/Bench · Quantum Echo Suite** depends on **T5 External Benchmarks**
* **Studio/Publishing · DOI Packager** depends on **T6 Repro Pack Format**

---

## 3) One‑page roadmap (make a living doc)

### Q1 (Weeks 1–12)

* **T1→T2 J/M Split Stability**
  Owner: Phys‑Alpha · Metrics: energy drift < ε; split error vs Strang
  **Unblocks:** Nexus/Runner (Metriplectic v1, sandbox flag)
* **T2 Run‑Manifest Spec**
  Owner: Nexus Core · Output: `run-manifest.json` + schema tests
  **Unblocks:** Studio/Experiment Wizard (basic)

### Q2 (Weeks 13–24)

* **T3 Echo Witness**
  Owner: Phys‑Beta · Metrics: refocus curve, perturb sensitivity, ablations
  **Unblocks:** Viewport Echo Overlay + Bench viewer
* **T3 Policy‑free Steering Metric**
  Owner: ADC/SIE · Metric: steering without reward function leakage
  **Unblocks:** MemGraph Steering API (beta)

### Q3 (Weeks 25–36)

* **T4 Robust Echo (hardware/domain shift)**
  **Unblocks:** Promote Echo Overlay → stable; enable export
* **T5 External Benchmarks**
  **Unblocks:** Nexus/Bench (publishable dashboards)

### Q4 (Weeks 37–48)

* **T6 Repro Pack (DOI)**
  **Unblocks:** Studio/Publishing (DOI packager)
* **T7 Field‑ready Long‑run**
  **Unblocks:** “Stable” flags across Nexus modules

---

## 4) Status board (copy this block into `ROADMAP.md`)

```text
[ ] T1 Instrument: J/M split sanity           → Nexus/Runner (Metriplectic v1)
[ ] T2 First Signal: J/M stability            → Studio/Experiment Wizard (basic)
[ ] T3 Validation: Echo witness               → Viewport Echo Overlay (beta)
[ ] T3 Validation: Steering metric (policy‑free)
                                              → MemGraph Steering API (beta)
[ ] T4 Robustness: Echo under shift           → Viewport Echo Overlay (stable)
[ ] T5 Benchmark: External suites             → Nexus/Bench (publishable)
[ ] T6 Result: DOI repro pack                 → Studio/Publishing (DOI tool)
[ ] T7 Field‑ready: Long‑horizon stability    → Promote modules to “Stable”
```

---

## 5) Promotion rules (keep it mechanical)

* **Experimental → Beta:** linked T‑gate reached **or** provisional waiver with fallback + kill‑switch.
* **Beta → Stable:** linked T‑gate **passed** + regression suite green + perf budget met.
* **Stable → Publish:** T6 package exists, includes seeds, manifests, and rerun script.

---

## 6) What to track (short checklist)

* Each card has: **Tier, Metric, Owner, Evidence path, Nexus modules it unlocks.**
* Evidence path points to: logs, plots, manifests, seeds, DOI (when ready).
* Every Nexus PR must reference a **T‑gate ID** (e.g., `T3‑ECHO‑2025‑10‑12`).

---

## 7) Starter JSON (drop in `roadmap/dual_map.json`)

```json
{
  "tiers": {
    "T2_JM_STABILITY": {
      "metrics": ["ΔH drift < 1e-4 per 1k steps", "split error vs Strang ≤ 5%"],
      "evidence": "artifacts/T2_JM_STABILITY/",
      "unlocks": ["nexus.runner.metriplectic_v1", "studio.wizard.basic"]
    },
    "T3_ECHO_WITNESS": {
      "metrics": ["refocus peak SNR ≥ 8dB", "perturb sensitivity slope > 0"],
      "evidence": "artifacts/T3_ECHO_WITNESS/",
      "unlocks": ["viewport.overlay.echo", "nexus.bench.echo_view"]
    },
    "T3_STEERING_METRIC": {
      "metrics": ["causal steering Δ vs reward baseline", "leakage tests pass"],
      "evidence": "artifacts/T3_STEERING_METRIC/",
      "unlocks": ["memgraph.api.steering_beta"]
    },
    "T6_REPRO_PACK": {
      "metrics": ["third‑party rerun pass", "DOI registered"],
      "evidence": "artifacts/T6_REPRO_PACK/",
      "unlocks": ["studio.publish.doi_packager"]
    }
  }
}
```

---

If you want, I can convert this into a repo‑ready `ROADMAP.md` + `dual_map.json` + a lightweight Kanban template so you can paste it straight into Nexus/Studio.
