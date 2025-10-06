# Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-10-06 | Added minimal RD conservation harness run_rd_conservation.py using IO helper. | Implements initial controls: diffusion-only mass conservation and reaction-only Q-invariant convergence (RK4); logs artifacts under standardized outputs; aligns with periodic BC default for Obj-A/B. |
| 2025-10-06 | Cleaned and deduplicated rd_conservation harness file; fixed embedded duplication and trailing stray code; ensured sidecar JSON/CSV outputs and CLI are intact. | Prior patch corruption embedded a duplicate script block inside StepSpec and left stray print at EOF. The cleanup restores a single, valid module and preserves experimental artifacts per PAPER_STANDARDS. |
| 2025-10-06 | Paused Codacy CLI auto-analysis per user request to reduce CPU usage. | User reported high CPU from Codacy runs. I will skip Codacy tool invocations for this session unless explicitly asked to run them again. |
| 2025-10-06 | Implement failed_runs routing for RD harness artifacts based on pass/fail gates. | Added failed flag propagation to figure_path/log_path in q_invariant_convergence, objA_objB_sweeps, and lyapunov_monitor so failing controls and experiments write figures and logs under outputs/*/rd_conservation/failed_runs. |
