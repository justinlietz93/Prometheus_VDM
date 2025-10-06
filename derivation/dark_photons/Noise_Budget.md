# Detector Noise Budget (pick one search mode)

**Goal:** Show which noise sets the floor for your chosen mode (cavity/dish or monophoton).

## Inputs

- CSV: `noise_budget.csv` with columns: `freq_Hz, integration_time_s, shot_noise, thermal_noise, amplifier_noise, total_noise, SNR`.

## Tasks

- Plot SNR vs integration time for a fixed frequency (single curve).
- Identify **quantum-limited** vs **thermal-limited** regimes.

## Acceptance gates

- [ ] CSV loads and schema validated.
- [ ] Plot saved (PNG) with annotated floor (shot or thermal).
- [ ] One-sentence conclusion: which regime dominates and why.
