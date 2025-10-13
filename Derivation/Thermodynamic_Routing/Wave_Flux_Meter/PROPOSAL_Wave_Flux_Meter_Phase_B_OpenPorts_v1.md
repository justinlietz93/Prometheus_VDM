# Proposal: Wave Flux Meter — Phase B (Open-Ports with Absorber) v1

Author: Justin K. Lietz  
Date: 2025-10-13

## Abstract

Extend the certified A-phase Wave Flux Meter to an open-port configuration with a static absorber/sponge surrounding a rectangular interior. We open two opposing ports (left/right) and audit power accounting, symmetry null, and absorber efficiency using the same J-only dynamics and Poynting-analog flux. Approval and io_paths policies apply; execution is default-denied until this tag is approved.

## Motivation and Background

The A-phase certified the instrument in a closed box. For routing, we must validate that the instrument correctly handles open boundaries with controlled absorption and clean power ledgers. A simple damping sponge (\(\sigma(x,y)\)) is sufficient to mimic port openings with minimal reflections.

## Hypotheses and KPIs

- H1 (Power balance): The mean relative balance error satisfies  
  $$\frac{\langle\,|\,\tfrac{\mathrm{d}E_{\text{in}}}{\mathrm{d}t} + P_{\text{out}}\,|\,\rangle}{\langle\,|P_{\text{out}}|\,\rangle} \le 0.1,$$  
  where \(E_{\text{in}}\) is interior energy and \(P_{\text{out}}=P_L+P_R\) is the net outward flux through both ports.
- H2 (Symmetry null): For symmetric initial conditions,  
  $$\frac{\langle\,|P_L - P_R|\,\rangle}{\langle\,|P_L + P_R|\,\rangle} \le 0.05.$$
- H3 (Absorber efficiency): The time-integrated dissipation inside the absorber matches the energy inflow from the interior with efficiency  
  $$\eta_{\text{abs}} = \frac{\int \sigma\,\pi^2\,\mathrm{d}A\,\mathrm{d}t}{\int P_{\text{out}}\,\mathrm{d}t} \ge 0.9.$$

KPIs (JSON): power_balance_rel.mean_abs, symmetry_null_rel.mean_abs, absorber_efficiency.value. Gates are the thresholds above.

## Methods

- Dynamics: J-only scalar wave with leapfrog; damping term \(-\sigma\,\pi\) in the momentum update.
- Geometry: interior rectangle of size \([n_{\text{abs}}, N_x-n_{\text{abs}}-1]\times[n_{\text{abs}}, N_y-n_{\text{abs}}-1]\) with absorber elsewhere. Two vertical ports sample flux on the interior boundary at indices \(i_{\text{left}}=n_{\text{abs}}\) and \(i_{\text{right}}=N_x-n_{\text{abs}}-1\), between rows \([j_0,j_1)\).
- Initial condition: symmetric central Gaussian pulse with outward momentum.
- Measurements: time series of \(E_{\text{in}}\), \(P_L\), \(P_R\), instantaneous absorber dissipation \(Q=\int \sigma\pi^2\,\mathrm{d}A\); compute mean relative balance error and symmetry metric.
- IO policy: use common.io_paths to write 1 PNG + 1 CSV + 1 JSON; failed_runs routing on unapproved or gate failure.

## Specification

- Grid: \(N_x=128\), \(N_y=64\), \(L_x=8\), \(L_y=4\), \(a=L_x/N_x\).
- Time: \(\Delta t=2.5\times10^{-4}\), \(T=2.0\).
- Absorber: thickness \(n_{\text{abs}}=8\), \(\sigma_{\max}=4.0\), power 2.
- Ports: height_frac=0.5, center_frac=0.5.
- Tag: thermo-routing-v2-wave-meter-openports.
- Schema: `Derivation/code/physics/thermo_routing/schemas/wave-flux-meter-openports-summary-v1.schema.json`

## Approvals and Compliance

- Script: `run_wave_flux_meter_openports_v1.py`  
- Domain: thermo_routing  
- Tag: thermo-routing-v2-wave-meter-openports  
- Approval key policy: HMAC(domain:script:tag) with tag_secret priority.
- Compliance receipts in JSON: approvals, quarantine flag, probe-limit, absorber_static.

## Artifacts

- Figure: `code/outputs/figures/thermo_routing/*_wave_flux_meter_openports_timeseries_thermo-routing-v2-wave-meter-openports.png`
- CSV: `code/outputs/logs/thermo_routing/*_wave_flux_meter_openports_v1_metrics_thermo-routing-v2-wave-meter-openports.csv`
- JSON: `code/outputs/logs/thermo_routing/*_wave_flux_meter_openports_v1_summary_thermo-routing-v2-wave-meter-openports.json`

## Risks and Mitigations

- Reflection from sponge edge if \(\sigma\) grows too sharply → use polynomial ramp (power=2) and tune \(\sigma_{\max}\).
- Discrete sampling of port flux can miss edge currents → use interior-boundary indices and window averaging across rows.

## Timeline

- Approval, then single-seed pilot run (v1); if gates pass, proceed to Phase C (routing KPIs).
