# System Patterns

## Architectural Patterns

- Pattern 1: Description

## Design Patterns

- Pattern 1: Description

## Common Idioms

- Idiom 1: Description

## Pre-registration execution guard for scientific runners

All scientific runners must default-deny execution unless a proposal is approved. Provide a CLI escape hatch --allow-unapproved for engineering-only smokes. When unapproved, stamp JSON logs with policy { pre_registered:false, engineering_only:true, quarantined:true } and route artifacts via failed/quarantine paths so they are excluded from RESULTS/KPIs. Add lightweight README notices in output domains explaining quarantine.

### Examples

- derivation/code/physics/dark_photons/run_dp_noise_budget.py: guard flag and policy block
- derivation/code/physics/dark_photons/run_dp_fisher_check.py: guard flag and policy block
- derivation/VALIDATION_METRICS.md: Status fields marked planned (pre-registered)
