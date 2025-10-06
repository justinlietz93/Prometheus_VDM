# Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-10-06 | Added minimal RD conservation harness run_rd_conservation.py using IO helper. | Implements initial controls: diffusion-only mass conservation and reaction-only Q-invariant convergence (RK4); logs artifacts under standardized outputs; aligns with periodic BC default for Obj-A/B. |
| 2025-10-06 | Cleaned and deduplicated rd_conservation harness file; fixed embedded duplication and trailing stray code; ensured sidecar JSON/CSV outputs and CLI are intact. | Prior patch corruption embedded a duplicate script block inside StepSpec and left stray print at EOF. The cleanup restores a single, valid module and preserves experimental artifacts per PAPER_STANDARDS. |
