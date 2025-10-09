#!/usr/bin/env bash
# init_dark_photon_quantum_docs_v2.sh
# Robust version: uses here-docs (no multi-line arg passing). Idempotent.
# Usage:
#   ./init_dark_photon_quantum_docs_v2.sh "<TARGET_DIRECTORY>"

set -euo pipefail

TARGET_DIR="${1:-}"
if [[ -z "${TARGET_DIR}" ]]; then
  echo "Error: please provide a target directory path." >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

create_if_missing() {
  local path="$1"
  shift
  if [[ -s "$path" ]]; then
    echo "• Exists: $path"
    return
  fi
  cat > "$path" <<'EOF'
'"$@"'
EOF
  # Remove the extra quoting lines added by the function wrapper
  # We inserted the payload between lines that contain just quotes; strip them.
  # But simpler: we won't wrap "$@" and will just pass a here-doc per call.
}

# Since passing content via "$@" is messy for here-docs, define per-file creators:

create_readme() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
# Dark Photon - Quantum Bridge (target set)
**Purpose:** Give immediate, concrete targets that bridge your portal work to quantum credibility, with one artifact per document (figure + CSV). Keep everything plain-English, equation-light.

**Files created by this pack**
- Portal_Lingo.md
- Noise_Budget.md
- Decoherence_Portals.md
- Fisher_Epsilon.md
- EFT_Ladder.md
- noise_budget.csv
- fisher_example.csv

**Rhythm:** For each doc, produce **one figure + one CSV/JSON** and assert **acceptance gates** before merging.
EOF
  echo "✓ Created: $path"
}

create_portal_lingo() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
# Portal → Quantum: Lingo & Mapping
**Goal:** Speak quantum-field basics fluently using your portal (dark photon A′) as the anchor.

## What to say in 60-90s
- Field ↔ particle (ripple ↔ quantum), gauge, mixing (ε as leaky splitter), mass (dark Higgs or Stueckelberg), state & measurement (clicks vs interference).
- Visible vs invisible channels = where the **record** lands (SM vs dark).

## Deliverables
- 1-panel diagram (fields ⇄ quanta ⇄ detectors). *(PNG placeholder now)*
- 1 summary paragraph (≤120 words).

## Acceptance gates
- [ ] Diagram present and legible.
- [ ] Paragraph hits: field, quantum, gauge, mixing, mass, measurement.
EOF
  echo "✓ Created: $path"
}

create_noise_budget_md() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
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
EOF
  echo "✓ Created: $path"
}

create_decoherence_md() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
# Open Systems: Visible vs Invisible = Where the Record Goes
**Goal:** Explain missing-energy vs visible channels using open-quantum-system language.

## Picture
- System: dark photon production
- Bath A (visible): SM detectors (clicks)
- Bath B (invisible): dark sector (no direct record)

## Deliverables
- 1 box diagram (system-bath-readout) + 3 bullets on how decoherence appears.

## Acceptance gates
- [ ] Diagram present.
- [ ] 3 bullets cover: record location, reversibility (in practice), and why invisible ≠ anti-photon.
EOF
  echo "✓ Created: $path"
}

create_fisher_md() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
# Fisher Info Quick Win (ε sensitivity)
**Goal:** Show how sensitivity to mixing ε scales with counts, efficiency, and background-no heavy math.

## Inputs
- CSV: `fisher_example.csv` with columns: `bin_label, expected_signal, background, exposure, eff_signal, eff_background`.

## Tasks
- Compute a simple Fisher estimate for ε in 1-2 bins (analytic or finite-diff).
- Output a tiny JSON summary with the estimated σ(ε).

## Acceptance gates
- [ ] CSV loads and schema validated.
- [ ] σ(ε) computed and saved to JSON.
- [ ] 2-line note: how scaling with exposure & background behaves.
EOF
  echo "✓ Created: $path"
}

create_eft_ladder_md() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
# EFT Scale Ladder (what changes as you zoom)
**Goal:** One ladder figure + 5 bullets explaining assumptions at each rung.

## Rungs (edit as needed)
1. **Detector scale** (Hz-GHz): noise model, materials, coherence time.
2. **Portal scale** (m_A′, ε): decay modes, lifetime, production mechanism.
3. **Dark-sector dynamics** (α_D, dark Higgs): in/visible branching, self-interactions.
4. **SM matching** (loops, thresholds): running couplings, radiative mixings.
5. **UV completion** (≫ TeV): what breaks/extends the EFT; symmetries that protect ε.

## Acceptance gates
- [ ] Ladder graphic present.
- [ ] 5 bullets match the rungs; no undefined jargon.
EOF
  echo "✓ Created: $path"
}

create_noise_csv() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
freq_Hz,integration_time_s,shot_noise,thermal_noise,amplifier_noise,total_noise,SNR
1.0e6,1,0,0,0,0,0
EOF
  echo "✓ Created: $path"
}

create_fisher_csv() {
  local path="$1"
  if [[ -s "$path" ]]; then echo "• Exists: $path"; return; fi
  cat > "$path" <<'EOF'
bin_label,expected_signal,background,exposure,eff_signal,eff_background
bin1,10,100,1.0,0.9,1.0
bin2,5,80,1.0,0.9,1.0
EOF
  echo "✓ Created: $path"
}

# Create files
create_readme        "${TARGET_DIR}/README.md"
create_portal_lingo  "${TARGET_DIR}/Portal_Lingo.md"
create_noise_budget_md "${TARGET_DIR}/Noise_Budget.md"
create_decoherence_md  "${TARGET_DIR}/Decoherence_Portals.md"
create_fisher_md       "${TARGET_DIR}/Fisher_Epsilon.md"
create_eft_ladder_md   "${TARGET_DIR}/EFT_Ladder.md"
create_noise_csv       "${TARGET_DIR}/noise_budget.csv"
create_fisher_csv      "${TARGET_DIR}/fisher_example.csv"

echo "Done."
