Here’s the clean, falsifiable way to sequence your public drops from where you are right now.

# Classification

Axiom-core → Derived-limit (RD & fluids) → Runtime-only (memory steering runners behind a shim)

# Objective recap

Publish the next two pieces that (1) strengthen your “methodological spine” and (2) showcase the uniquely VDM bits-without outrunning your acceptance gates.

# Recommendation (order matters)

**1) Memory Steering - “Acceptance & Verification” (next preprint).**
Why this first: it’s your differentiator and you already defined how it must behave inside the event-driven, sparse-only organism. Bake the checks right into the paper: no dense ops; all structure edits go walker→event→scoreboard→actuator; budgets enforced; physics guards pass (Q_FUM drift ≈ 0; RD regime unchanged by steering). The architecture and tests are already spelled out; turn them into figures and CLI recipes.    

**2) Fluid Dynamics - “Methods Note: LBM→NS Taylor-Green benchmark.”**
You’ve already got a crisp, low-risk physics validation (ν_fit ≈ 0.0999 vs ν_th = 0.1). Package it as a short, reproducible note (setup, acceptance gate, log/figure, CLI). This keeps the “validated-methods” drumbeat going right after the RD baseline. 

**3) Gravity / dark sector - hold for a scoped hypothesis note.**
Keep it quarantined as future work with falsifiable observables, not a full derivation yet. Your published scope policy already draws a clear line between canonical RD claims and quarantined second-order/EFT content; mirror that for gravity until you’ve locked (1) and (2). 

# Why this sequence is defensible (and fast to prove)

* Your **RD methods baseline already passed** hard gates (Fisher-KPP front speed; linear dispersion) and packaged the local logarithmic invariant *as QA*, not as headline theory. That establishes your style: “claim → script → tolerance → PASS.”   
* The **Zenodo record** already bundles the artifacts (paper, methods note, figures), so your next DOI can mirror that structure with minimal ceremony. 
* You have **runtime/architecture tests ready** to cite for the memory-steering piece: “no dense,” event-driven compliance, budget checks, plus physics validation harnesses.  

# Action plan (≤7 bullets; risk-reduction order)

1. **Harden the public/private boundary** before publishing steering/fluid runners: route any public runner that touches classified primitives (e.g., `memory_steering_experiments.py`, `lbm2d.py`) through a tiny `void_runtime_api` shim; add a CI grep to block forbidden imports; keep the “friendly error path.”  
2. **Memory Steering preprint** (“Acceptance & Verification”):
   • Figures: (a) event flow (walker→event→scoreboard→actuator), (b) Q_FUM drift under steering (line ~0 within tolerance), (c) engram retention/decay step-response, (d) budget ablation (steering shuts off cleanly).
   • CLI: `vdm.ms_step --budget ... --no-dense-check --qfum-check`.
   • Gates: Q_FUM conservation, RD regime intact, event-driven & budget compliance all PASS.   
3. **Fluid Dynamics methods note**: ship the Taylor-Green viscous decay benchmark with its single decisive metric (|ν_fit/ν_th - 1| ≤ 1%). Include reproducible seeds/logs. 
4. **Link both to the RD baseline** runners/figures to emphasize continuity of method (front speed, dispersion, invariant-as-QA). 
5. **Provenance bundle**: in each preprint, add “Reproducibility & Outputs” (figures/logs layout; filenames; CLI) exactly as your baseline does. 
6. **Scope page refresh**: pin RD as canonical; stamp fluids note as “Methods/Validation,” memory steering as “Runtime-physics acceptance,” and park gravity in “Quarantined hypothesis.” 
7. **Cut the DOI pair** (steering; fluids), then circle back to a short “Gravity: falsifiable router hypothesis” outline with explicit non-claims and measurable signals.

# Verification (gates to include in each paper)

* **Axiom gates (physics)**
  • RD regime intact: front-speed rel-error ≤ 5% (mirrors baseline); dispersion array-R² ≥ 0.98. 
  • H-theorem style monotonic: memory metric behaves monotonically under intended steering windows (define metric + tolerance).
  • **Q_FUM conservation** (or bounded drift within numeric tolerance) before/after steering steps. 
* **Architecture gates (runtime)**
  • **No dense ops**; **event-driven only**; **budget compliance** (publish the tests). 
* **Reproducibility**
  • Figures/logs/CLI schema identical to RD baseline’s reproducibility section. 

# Assumptions/Risks

* **Boundary leaks** from public runners; kill-method: shim + CI “content-police” grep you already drafted. 
* **Metric ambiguity** for memory steering; kill-method: pick a single decisive metric (e.g., engram retention half-life under fixed budget), publish its tolerance and a pass/fail plot.
* **Scope creep** into EFT/gravity; kill-method: keep the quarantine banner active per current policy. 

# Next steps (concrete)

* Implement the `void_runtime_api` shim and CI grep; update the two public runners to import only through the shim. 
* Draft “Memory Steering - Acceptance & Verification” with embedded tests and four figures listed above; include Q_FUM drift panel. 
* Draft “LBM→NS Taylor-Green Methods Note” with the ν_fit vs ν_th figure and a 1-metric acceptance gate. 
* Ship both as Zenodo DOIs mirroring your RD baseline bundle layout (paper + runner + logs/figures). 

If you want a template, I can spin the memory-steering preprint skeleton with sections for gates, runners, and CI badges wired to your existing layout so it looks like a sibling to the RD baseline rather than a new genre. The meta-story stays consistent: “VDM makes claims by passing physics-style gates.”
