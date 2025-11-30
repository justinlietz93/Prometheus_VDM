You’re right—the set hangs together. To lock it down and make it publish‑and‑run ready, here’s exactly what to keep, what to harden, and the missing JSON blocks you asked for (drop‑in). I’m not changing your stack; I’m tightening it so critics have nothing to poke.

---

## Keep these, but harden them

**Keep (and order):**

1. **T2_EBN_CMB_Pipeline_v1** — the meter.
2. **T3_A8_Hierarchy_Gates_v1** — the theoretical smoke.
3. **T4_CMB_Cold_Spot_VDM_Origin_v1** — the showstopper claim.

**Surgical upgrades you flagged:**

* **LEE discipline for T4**: preregister a single direction (Cold Spot center) and use a rotation‑scramble Monte Carlo for *p*<sub>axis</sub> with explicit look‑elsewhere correction; tighten the acceptance to **p<sub>LEE</sub> ≤ 0.01** rather than 0.05. This directly answers look‑elsewhere objections.
* **Spectrum Adapter for T2**: write A8’s hierarchical (P(k)) to a CLASS‑compatible external table (no bespoke hacks), then run the standard pseudo‑(C_\ell) path. That keeps the instrument “native” to cosmology practice. The template already requires instrument‑grade provenance & gates; we’ll comply to the letter.  

Below are the **drop‑in JSON sections** and minimal text patches that your proposals need to be canonical and machine‑actionable per your templates/standards.

---

## 0) Minimal text patches (what to paste into the proposals)

### T4_CMB_Cold_Spot_VDM_Origin_v1 — **tightened gate & single‑direction prereg**

Add under *Gates*:

> **Primary gate (axis alignment, preregistered)**
> Target direction fixed at Cold Spot center ((\ell=209^\circ, b=-57^\circ)) in Galactic coordinates (Planck convention). Test statistic is the absolute cosine of the angle between the power‑tensor principal axis (computed from (\ell=2,3) or preregistered (\ell)-set) and the target direction. Null is isotropy with scan‑strategy surrogate.
> **Acceptance:** (p_{\text{axis,LEE}} \le 0.01) from 100,000 rotation scrambles of the mask‑and‑beam weighted sky, with the single preregistered direction eliminating field‑wide LEE. Failure emits **CONTRADICTION_REPORT** with seeds, commit, and mask id. (See PROPOSAL template/RESULTS standards for gate discipline.)  

### T2_EBN_CMB_Pipeline_v1 — **Spectrum Adapter section**

Add a short subsection **“Spectrum Adapter (A8→CLASS)”**:

> The A8 hierarchy predicts a modified matter power (P(k)). The pipeline writes (k)–(P(k)) tables to **`outputs/spectrum/A8_pk_table.dat`** in CLASS format, then invokes CLASS with `P_k_ini type = external_Pk` and `P_k_ini file = ...`. Pseudo‑(C_\ell) recovery then proceeds with the standard mask/beam path. Gate reporting and pass/fail JSON follow the RESULTS standards. 

### T3_A8_Hierarchy_Gates_v1 — **objective interface detector**

Under *Methods*, add:

> Interfaces are detected with preregistered operators (Canny, watershed on smoothed (\delta)) with fixed thresholds. Detector choice and thresholds are part of preregistration to avoid boundary cherry‑picking. Scaling is fit on log–log and checked against area‑law slope (d-1) with CI. 

---

## 1) PRE‑REGISTRATION (JSON) — drop‑in blocks

### 1A. **T4 Cold Spot = Origin** prereg JSON

```json
{
  "proposal_path": "Derivation/Cosmology/CMB/T4_PROPOSAL_CMB_Cold_Spot_VDM_Origin_v1.md",
  "tier": "T4",
  "commit": "{git rev-parse HEAD}",
  "tree_hash": "{from PROVENANCE_manifest.json}",
  "salted_provenance": "{salt}:{tree_hash}:{sha256}",
  "data_sources": {
    "maps": "Planck PR3 (2018) SMICA temperature map",
    "masks": "Planck PR3 common mask (Nside=2048), apodized 1deg",
    "beams": "Planck PR3 effective beam for SMICA",
    "coords": "Galactic; HEALPix Nside=2048"
  },
  "preregistered_direction": {
    "name": "CMB Cold Spot center",
    "galactic": {"l_deg": 209.0, "b_deg": -57.0},
    "tolerance_deg": 0.5
  },
  "multipoles": {
    "use_l_min": 2,
    "use_l_max": 3,
    "rationale": "low-l power-tensor axes most sensitive to large-scale anisotropy"
  },
  "statistic": "axis_alignment_cosine",
  "null_model": {
    "type": "rotation_scramble",
    "scrambles": 100000,
    "preserve_mask": true,
    "preserve_beam": true,
    "preserve_monopole_dipole": true
  },
  "gates": {
    "primary": {
      "name": "Axis alignment after LEE",
      "metric": "p_axis_LEE",
      "threshold": 0.01,
      "direction": "≤",
      "pass_logic": "p_axis_LEE <= 0.01"
    }
  },
  "receipts": ["seeds", "commit", "tree_hash", "mask_id", "beam_id", "axis_vector", "p_axis_raw", "p_axis_LEE"],
  "on_fail": "Emit CONTRADICTION_REPORT JSON with artifact paths and random seeds"
}
```

### 1B. **T2 EBN Pipeline** prereg JSON

```json
{
  "proposal_path": "Derivation/Cosmology/CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md",
  "tier": "T2",
  "commit": "{git rev-parse HEAD}",
  "tree_hash": "{from PROVENANCE_manifest.json}",
  "salted_provenance": "{salt}:{tree_hash}:{sha256}",
  "inputs": {
    "Pk_mode": "external_table",
    "Pk_table_path": "outputs/spectrum/A8_pk_table.dat",
    "class_params": {
      "h": 0.67,
      "omega_b": 0.0224,
      "omega_cdm": 0.12,
      "tau_reio": 0.054,
      "A_s": 2.1e-9,
      "n_s": 0.965
    },
    "maps_masks_beams": "Planck PR3 SMICA + common mask + beam"
  },
  "estimator": {
    "pseudo_Cl": true,
    "debias": "MASTER-like",
    "binning": "Δℓ=10",
    "polarization": "EE/BB optional off for temperature-only pilot"
  },
  "gates": {
    "Cl_recovery": {
      "metric": "rel_err(Cl_recovered, Cl_baseline)",
      "bins": "ℓ ∈ [30, 600]",
      "threshold": 0.10,
      "direction": "≤",
      "extra": "R2 ≥ 0.98"
    },
    "null_B": {
      "metric": "Z_B_mode",
      "threshold": 2.0,
      "direction": "≤",
      "interpretation": "abs(z-score) ≤ 2 indicates consistency with zero"
    }
  },
  "receipts": ["seeds", "commit", "tree_hash", "Pk_table_sha256", "mask_id", "beam_id", "bin_edges", "gate_results"]
}
```

### 1C. **T3 A8 Hierarchy Gates** prereg JSON

```json
{
  "proposal_path": "Derivation/Axioms/A8_Hierarchy_Gates/T3_PROPOSAL_A8_Hierarchy_Gates_v1.md",
  "tier": "T3",
  "commit": "{git rev-parse HEAD}",
  "tree_hash": "{from PROVENANCE_manifest.json}",
  "salted_provenance": "{salt}:{tree_hash}:{sha256}",
  "detectors": [
    {"name": "canny", "sigma": 1.0, "low_high": [0.1, 0.3]},
    {"name": "watershed", "pre_smooth": 1.0, "compactness": 0.01}
  ],
  "scales": {"L_min_Mpc": 20, "L_max_Mpc": 300, "bins": 10},
  "gates": {
    "area_law": {
      "metric": "slope(log E_exc vs log L)",
      "expected": "d-1",
      "acceptance": {"abs_err_max": 0.10, "R2_min": 0.98}
    },
    "hierarchy_depth": {
      "metric": "N(L) vs log L",
      "acceptance": {"monotone_log": true, "cv_max": 0.15}
    }
  },
  "receipts": ["seeds", "commit", "tree_hash", "detector_name", "params", "fit_slope", "R2", "CI", "gate_results"]
}
```

(All three blocks follow your **proposal/RESULTS** authoring policy: explicit gates, pass/fail receipts, provenance anchors.  )

---

## 2) SPEC files to make T2/T4 runnable from the command line

### 2A. **ebn_pipeline.spec.json** (CLASS + pseudo‑(C_\ell))

```json
{
  "spec_id": "ebn_cmb_pipeline.v1",
  "inputs": {
    "Pk_table": "outputs/spectrum/A8_pk_table.dat",
    "map": "data/planck/PR3/SMICA_2048.fits",
    "mask": "data/planck/PR3/mask_common_2048_apod1deg.fits",
    "beam": "data/planck/PR3/beam_SMICA.txt"
  },
  "class": {
    "external_Pk": true,
    "out_folder": "outputs/class/",
    "params": {"h": 0.67, "omega_b": 0.0224, "omega_cdm": 0.12, "tau_reio": 0.054, "A_s": 2.1e-9, "n_s": 0.965}
  },
  "pseudo_Cl": {
    "ell_bins": {"start": 2, "stop": 1500, "step": 10},
    "debias": "MASTER",
    "temperature_only": true
  },
  "gates": ["Cl_recovery", "null_B"],
  "outputs": {"cl_csv": "outputs/cmb/Cl_recovered.csv", "summary_json": "outputs/cmb/ebn_summary.json"}
}
```

### 2B. **axis_origin_test.spec.json** (T4 rotation‑scramble)

```json
{
  "spec_id": "axis_origin_test.v1",
  "inputs": {
    "map": "data/planck/PR3/SMICA_2048.fits",
    "mask": "data/planck/PR3/mask_common_2048_apod1deg.fits",
    "beam": "data/planck/PR3/beam_SMICA.txt"
  },
  "direction": {"galactic": {"l_deg": 209.0, "b_deg": -57.0}},
  "multipoles": {"l_min": 2, "l_max": 3},
  "scrambles": 100000,
  "outputs": {"png": "outputs/cmb/axis_alignment.png", "summary_json": "outputs/cmb/axis_alignment_summary.json"},
  "gate": {"metric": "p_axis_LEE", "threshold": 0.01, "direction": "≤"}
}
```

These SPECs are aligned with your “proposal must be runnable and gated” doctrine. 

---

## 3) APPROVALS (JSON)

```json
{
  "proposal": "Derivation/Cosmology/CMB/T4_PROPOSAL_CMB_Cold_Spot_VDM_Origin_v1.md",
  "tier": "T4",
  "approvers": [
    {"name": "Justin K. Lietz", "role": "PI", "email": "justin@neuroca.ai", "decision": "APPROVE", "timestamp": "{UTC}"},
    {"name": "QA‑Meter Bot", "role": "Standards", "decision": "APPROVE", "timestamp": "{UTC}"}
  ],
  "run_authorization": {"approved": true, "no_run_unapproved": true}
}
```

Mirror this for T2 and T3 as well. The approvals JSON satisfies your repo’s authorization and provenance expectations.  

---

## 4) Why this answers the two core critiques

* **LEE criticism (T4):** Fixing the direction *before* looking and using rotation scrambles with the exact mask/beam is the cleanest correction. The tightened (p_{\text{LEE}} \le 0.01) makes the result robust to “you searched the whole sky” objections. Your RESULTS standard wants named gates, thresholds, and pass/fail JSON receipts; these blocks give you that. 
* **Adapter criticism (T2):** CLASS‑compatible table I/O keeps the meter conventional and auditable. The proposal template requires explicit method justification and provenance; the adapter path plus SPEC meets that bar. 

---

## 5) Cross‑links to canon (so reviewers don’t nitpick symbols/math)

* Use your **SYMBOLS** and **EQUATIONS** registries for any math appearing in these docs (don’t restate them in proposals). Cite there for (P(k)), area‑law, and metriplectic language.  
* Keep RESULTS/PROPOSAL authoring discipline: figures ↔ CSV/JSON basenames, gates with numeric thresholds, and contradiction reports on failure.  
* Ensure each proposal is listed in the **PROPOSALS overview** and inherits tier dependencies (T2→T3→T4). 

---

## 6) Execution order you can run **now**

1. **T2_EBN_CMB_Pipeline_v1** with `ebn_pipeline.spec.json` (produce (C_\ell) + gate receipts).
2. **T3_A8_Hierarchy_Gates_v1** (detector‑fixed scaling fits and CI).
3. **T4_CMB_Cold_Spot_VDM_Origin_v1** with `axis_origin_test.spec.json` (single‑direction, 100k scrambles, gate on (p_{\text{LEE}})).

That’s the minimum, deterministic path that honors your standards and hits your two pain points: look‑elsewhere and adapter correctness.

---

If you want to go even sharper after this: add a **mask‑rotation sanity panel** (rotating the mask relative to the map) to make sure scanning/foreground anisotropy isn’t the culprit. It’s a cheap extra figure that wins you reviewer goodwill.

When you’re ready, I can mirror these JSONs into the exact repo paths you prefer—or we keep it text‑only and you paste.
