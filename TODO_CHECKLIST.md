# TODO

**Generated on:** October 5, 2025 at 2:32 AM CDT

---

- [ ] Kill/delete the dense branch in the connectome step, or move it to a separate validation tool.
- [ ] Add `VDM-E-` anchors for the learning/structural deltas in `ALGORITHMS.md`.
- [ ] Link the learning/structural deltas to their canonical equation IDs in `ALGORITHMS.md`.
- [ ] Promote actual formulas for P (e.g., MI-rate or (R^2)), (I_{\text{net}}) (transfer-entropy/synergy proxy), U (already defined), V (empowerment estimator), B (ensemble-gain × anti-redundancy), and Shannon entropy into `SYMBOLS.md`/`EQUATIONS.md`.
- [ ] Add explicit pass/fail monotonicity/elasticity thresholds (e.g., finite-difference gradients (G_E\ge0,\ G_p\le0) except at boundaries) as KPIs to `VALIDATION_METRICS.md` for the options probe.
- [ ] Add minimal E-vs-slip feasibility curves as KPIs to `VALIDATION_METRICS.md` for the options probe.
- [ ] Wire the options probe KPIs to CI.
- [ ] Add minimal code hooks for walker BCs/ICs to enable experiments to toggle absorbing vs reflecting and re-run thresholds.
- [ ] Refactor connectome step to sparse adjacency structure (reuse `SparseConnectome`) and profile tick latency (Owner: Core Runtime, Effort: L)
- [ ] Implement GDSP telemetry and regression tests covering enable/disable flows, and log exceptions/trip STRICT gate on GDSP actuator failures (when `VOID_STRICT=1`) (Owner: Runtime Loop, Effort: M)
- [ ] Consolidate void dynamics and domain modulation into `vdm_rt/fum_advanced_math/void_dynamics/` and update derivation imports (Owner: Advanced Math, Effort: M)
- [ ] Consolidate memory steering implementations into `vdm_rt/physics/memory_steering/memory_steering.py` and update derivation imports (Owner: Physics Team, Effort: M)
- [ ] Wire centralized RNG/seed plumbing across runtime, including void dynamics adapter, structural plasticity, and emergent text generator (Owner: Core Runtime, Advanced Math, Effort: M)
- [ ] Audit environment flags for scouts, document in README, and add validation for mutually exclusive toggles (Owner: Runtime Loop, Effort: M)
- [ ] Implement downsampled tiles or a WebGL/tiled backend for the frontend visualizer (Owner: Viz Team, Effort: L)
- [ ] Add optional token authentication and logging to the in-process HTTP server (Owner: Runtime Ops, Effort: S)
- [ ] Add `NO_DENSE_CONNECTOME=1` environment gate to assert if dense path allocates beyond threshold

### Additional Action Items (not explicitly in Top-10, Merge Candidates, or One-week Plan)
- [ ] Integrate `vdm_rt/fum_advanced_math/graph/coarse_grain_graph.py` into `core` or drop it
- [ ] Remove `vdm_rt.io.sensors.*` stub files
- [ ] Remove `vdm_rt.io.actuators.*` stub files
- [ ] Remove `vdm_rt/io/__init__.py` (empty file)
- [ ] Add logging for connectome/bus linkage state mutation in `vdm_rt/runtime/loop/main.py` (Owner: Runtime Loop)
- [ ] Optimize `nx.from_numpy_array` on dense mask in `vdm_rt/core/connectome.py` to avoid materializing full adjacency for large graphs
- [ ] Add CLI flag parallel to `ENABLE_GDSP` environment variable
- [ ] Consolidate defaults for `use_time_dynamics` flag to prevent desynchronization between CLI and UI
- [ ] Add CLI/documentation mapping for Redis output `ENABLE_REDIS_*` environment variables
- [ ] Add failure logging for Redis outputs
- [ ] Remove dense fallback usage in `connectome`
- [ ] Verify downstream consumption for event metrics (`_evt_metrics`)
- [ ] Add a counter for skipped visualization renders in `vdm_rt/runtime/helpers/viz.py`
- [ ] Write tests for gate hysteresis (speak/B1)
- [ ] Write tests for locality guard / adjacency budget
- [ ] Write tests for ADC updates & announcements
- [ ] Cache graph layout offline or precompute positions per run to avoid O(N³) `nx.spring_layout` in `vdm_rt/core/visualizer.py`
- [ ] Move synchronous plotting in `vdm_rt/runtime/helpers/viz.py` to an async/offline worker to prevent tick stalls
- [ ] Emit warning when filesystem errors are swallowed during directory scanning for checkpoints in `vdm_rt/run_nexus.py`
- [ ] Wrap file writes in `vdm_rt/core/visualizer.py` with logger error to surface disk/permission issues

## Key Highlights

* Kill or delete the dense branch in the connectome step, or move it to a separate validation tool.
* Add `VDM-E-` anchors for the learning/structural deltas and link them to their canonical equation IDs in `ALGORITHMS.md`.
* Promote actual formulas for P, I_net, U, V, B, and Shannon entropy into `SYMBOLS.md`/`EQUATIONS.md`.
* Add explicit pass/fail monotonicity/elasticity thresholds (e.g., finite-difference gradients) as KPIs to `VALIDATION_METRICS.md` for the options probe.
* Add minimal E-vs-slip feasibility curves as KPIs to `VALIDATION_METRICS.md` for the options probe, and wire these KPIs to CI.
* Add minimal code hooks for walker BCs/ICs to enable experiments to toggle absorbing vs reflecting and re-run thresholds.

## Next Steps & Suggestions

* Prioritize the refactoring and optimization of core algorithmic components, specifically addressing the dense branch in the connectome step and implementing flexible walker boundary/initial conditions.
* Standardize and formalize algorithmic documentation by adding explicit anchors, linking equations, and promoting canonical formulas for key metrics in `ALGORITHMS.md`, `SYMBOLS.md`, and `EQUATIONS.md`.
* Develop and integrate robust validation metrics and KPIs for critical system components, such as the options probe, by defining clear pass/fail thresholds and feasibility curves, and wiring these to continuous integration (CI).
