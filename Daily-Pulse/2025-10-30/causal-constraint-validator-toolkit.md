Here’s a simple, rigorous VDM experiment kit you can use immediately, with a checklist, a minimal DAG workflow, and a “one‑page audit” generator.

[Download the folder](sandbox:/mnt/data/vdm_experiment_kit) → open `README.md` first.
Key script: `vdm_macro.py` (no NVIDIA deps; pure Python, AMD/ROCm‑friendly).

**What’s inside**

* **Checklist + minimal DAG template** (treat steer/pulse as the intervention node; declare backdoor adjustments and identifiability).
* **Predefined tests**: active vs sham pulses; randomized coupling; ablation falsifiers (remove memory steering; break J or M branch).
* **Power & multiplicity lock** fields + **report stub** that logs effect sizes, invariant checks, and deviations.
* **Notebook macro (script)** that:

  * Renders an ASCII DAG,
  * Computes invariant diagnostics (energy drift, entropy slope, front‑speed windows),
  * Runs ITS or DiD with block bootstrap,
  * Emits a **one‑page audit** (`reports/<name>_audit.md`) and a **prereg appendix** JSON with **PROVEN/PLAUSIBLE/NEEDS_DATA** labels.

**Quickstart**

1. Put CSV in `data/` with columns: `time, group, treated, value, energy(optional)` (an example is included).
2. Run:

```bash
python vdm_macro.py --data data/example.csv --design ITS --name run_001 --seed 42
```

3. Open `reports/run_001_audit.md` (effect size + invariant gates) and `reports/run_001_prereg.json` (tests + labels).

**What it enforces**

* Minimal DAG per experiment ✔️
* Conserved quantities & monotones (VDM‑implied) ✔️
* Identifiability/backdoor adjustments ✔️
* Interventional tests & ablations with pass/fail thresholds ✔️
* Seed control, synthetic‑data stress test hooks, and auto‑labels ✔️

If you want, I can extend this to render PNG DAGs, add formal multiple‑comparison controls (e.g., Holm), and integrate your canon folder export names next.
