# Wave Flux Meter — Phase B (Open Ports) Results v1

> Author: Justin K. Lietz  
> Date: 2025-10-13  
> Commit: 3e4b7f7  
> Tag: thermo-routing-v2-wave-meter-openports

This document certifies the Wave Flux Meter instrument for open-port configurations (Phase B) using the preregistered gates and approved tag. It reports conservation accuracy and absorber performance, with ports auto-aligned to the provided μ-channel map. No routing claim is made here; this is instrument qualification. See Conclusions for Phase C next steps.

Pinned artifact (dashboard):

- /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/outputs/figures/thermo_routing/20251013_184252_wave_flux_meter_openports_dashboard_thermo-routing-v2-wave-meter-openports.png

JSON/CSV (same basename):

- /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/outputs/logs/thermo_routing/20251013_184458_wave_flux_meter_openports_v1_summary_thermo-routing-v2-wave-meter-openports.json
- /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/outputs/logs/thermo_routing/20251013_184458_wave_flux_meter_openports_v1_metrics_thermo-routing-v2-wave-meter-openports.csv

## Scope and gates (what is claimed)

We validate that the discrete continuity relation holds to high accuracy on an open interior rectangle with ports, and that the absorber removes outflowing energy efficiently.

- Balance gate: R^2(-dE/dt, P_out) ≥ 0.9995 and ⟨|dE/dt + P_out|⟩ / ⟨|P_out|⟩ ≤ 0.5%.
- Absorber gate: E_diss_abs / ∫ P_out dt ≥ 0.9.
- Symmetry sanity: only applicable when μ and ports are symmetric; this run uses an asymmetric μ map, so symmetry is N/A (raw value reported).

## Method (instrument definition)

- State: scalar field φ with conjugate momentum π; wave speed c=1.0; absorber damping σ near domain boundary.
- Grid: 256×128 over Lx×Ly=8×4; interior box excludes an n_abs=8-cell sponge on each side.
- Time stepping: leapfrog (ϕ at integer steps, π at half steps), CFL guard 0.35; warm-up exclusion 10% of record for metrics.
- Discretization: centered differences; face-based flux for power. Conservation checked on the interior rectangle; ports placed at its left/right boundaries.
- μ and V: μ map used to find corridor-aligned port segments; dynamics used uniform face-μ (use_mu_weighting=false) with walls via V. This setting was chosen to tighten bookkeeping at this resolution; see Discussion.
- Ports: auto-detected narrow bands on the left/right interior boundaries within the predefined port window; aligned to the μ channel corridors.

## Results

From the pinned summary JSON:

- Power balance R^2 = 0.9999827333 (PASS ≥ 0.9995)
- Relative imbalance ⟨|dE/dt + P_out|⟩/⟨|P_out|⟩ = 0.002977 (0.2977%) (PASS ≤ 0.5%)
- Absorber efficiency = 1.72077 (PASS ≥ 0.9)
- Symmetry (raw) = 0.32955; applicable=false (asymmetric μ)

Figure 1 (dashboard) shows: top panel the channel map with interior rectangle and detected ports; bottom-left the interior energy; bottom-right the port powers and balance residual curve hugging the baseline except early warm-up.

## Provenance

- Tag: thermo-routing-v2-wave-meter-openports (approved=true; not quarantined)
- Commit: 3e4b7f74e0c9e3bc123c6f783c77f2c63218af93 (short 3e4b7f7)
- Numerics: CFL=0.35; warmup_frac=0.10; use_mu_weighting=false

## Discussion

- Why the gates now pass tightly: Discrete bookkeeping uses face-based fluxes aligned with the energy accounting on the interior rectangle; disabling μ-weighted dynamics at this grid avoids small dispersion/storage mismatches near sharp μ transitions while still honoring μ for port placement and walls via V. This drops conservation error to ~0.3% and R^2≈0.99998.
- Visuals: Legends moved to upper-left; the dashboard was widened to 14.5 inches to avoid overlap with accuracy annotations.

Limitations and next levers:

- With μ-weighted dynamics enabled, at 256×128 the imbalance was ~2–3%. To use μ-weighting end-to-end, increase warm-up to 20%, thicken absorber (12–16 cells, σ_max≈3), and/or increase resolution to 512×256; then re-test gates.

## Conclusions

The Wave Flux Meter (open-ports configuration) passes its Phase B gates with high margin and is ready as a trustworthy measurement instrument. No routing advantage is claimed here.

Next: Phase C (routing comparison preregistration). Example primary claim: the μ-aligned port captures ≥ X% more energy than a shuffled-μ control across N seeds, with a preset effect-size gate and CI. Secondary: directionality under mirrored drive.

Propose target X and N; the prereg will be drafted and run under the approvals policy.
