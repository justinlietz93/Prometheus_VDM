
# Gravity Regression Spec - Perihelion Precession & Connectome Sanity

## Purpose
Prove whether the runtime still exhibits **GR-like perihelion precession** and ensure the **substrate** has **not** drifted
into a forced ring‑lattice or other pathological scaffold.

## Inputs
- **Orbit log**: CSV `time,x,y` for a single tracked “test particle” (or effective mass point) over multiple orbits.
- **Connectome edgelist**: CSV `src,dst[,w]` exported at the beginning and end of the run.

## Outputs
1) `precession_report.csv` - per‑orbit perihelion angle, delta angle, orbital period.
2) `precession_summary.txt` - median/mean precession per orbit; sign consistency; stability flags.
3) `connectome_metrics.json` - degree stats, clustering, assortativity, cycle basis size, ring‑lattice suspicion.
4) `connectome_layout.png` - quick visual sanity snapshot.

## Acceptance Gates
- **Precession present**: median Δθ per orbit ≠ 0 with consistent sign across ≥ 5 consecutive orbits.
- **Stability**: coefficient of variation for Δθ < 0.5 over the measured window (tunable).
- **No forced ring**: degree variance > 0; cycle‑basis size not ≈ N; ring‑lattice suspicion = false.
- **Topology breathing OK**: if your growth rules are active, degree variance and clustering evolve smoothly (no step-wise clamp).

## Procedure (TL;DR)
1. Export orbit log & edgelist(s).
2. Run `compute_precession.py` and `graph_checks.py`.
3. Inspect figures + pass/fail flags.
4. If failed, revert substrate growth to your last known good and re‑run.

## Rationale (Long)
- **Perihelion precession** is robust to small perturbations; it’s a great early‑warning signal of whether your substrate’s curvature‑like effects are intact.
- **Ring‑lattice checks** catch accidental hard‑coding that suppresses curvature & detours, erasing precession.
- Keeping the test **post‑hoc** lets you iterate on the runtime without entangling analysis with control loops.
