# 1. **T2 (Instrument)** — **Water‑Displacement Meters for Interfacial Hierarchies**

> **Created Date:** 2025‑11‑24  
> **Provenance:** `{git rev-parse HEAD}` → `HEAD_SHA_HERE`; salted provenance: `base_sha256=…`, `salt_hex=…`, `salted_sha256=…` (to be inserted by prereg script).  
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)  
> **License:** (Repository `LICENSE`)  
> **Short summary (TL;DR):** Proposed is a **T2 instrument** that turns **binding‑site water thermodynamics** (free energy of water displacement from cavities) into **A8‑compatible meters** for interfacial hierarchy and “void dryness”, calibrated against the supramolecular host–guest benchmarks in *Thermodynamics of Water Displacement from Binding Sites and its Contributions to Supramolecular and Biomolecular Affinity*.

***Practical Provenance pattern.***  
Follow the canonical steps in the template (salted hashes, signed prereg tag, push before runs; section **5.1.1** repeats exact artifacts and required keys).

---

## 2. List of proposers and associated institutions/companies

**Justin K. Lietz** — Neuroca, Inc. (PI, implementer, approver).

---

## 3. Abstract

This proposal introduces **water‑displacement meters** that quantify how much of a binding event’s free energy is carried by **removal of structured water** from cavities and pockets. Using the host–guest systems and thermodynamic cycles of *Thermodynamics of Water Displacement from Binding Sites and its Contributions to Supramolecular and Biomolecular Affinity* as calibration data, the meters estimate (i) the free energy of displacing water from a site, $\Delta G_{\rm disp}^{\rm H_2O}$, (ii) its contribution to binding, $\Delta G_{\rm bind}^{\rm (water)}$, and (iii) a **“void dryness” index** that can be used as an A8 boundary‑law observable. Gates require reproduction of literature values for $\Delta G_{\rm disp}^{\rm H_2O}$ and its correlation with binding affinity to within predeclared tolerances. The instrument is **T2 only**: no new A8 or cosmological claim is made here; the meters simply become certified tools for later hierarchy and packing studies (e.g., protein packing, surface condensation, and A8 interface scaling).

---

## 4. Background & Scientific Rationale

### A8 program context

A8 (Infinity Resolution) asserts that finite excess energy in tachyonic systems forces **hierarchical interfaces** with boundary‑law excess energy and logarithmic depth. CF3 A8 formalizes this in continuum terms and motivates meters that can “see” where energy and information concentrate along interfaces and voids. Existing T2 instruments (STIV macrostate meters; protein‑packing meters) operationalize area‑law vs volume‑law and packing fraction for large‑scale interfaces and folded proteins.

However, **molecular‑scale hydration** is a critical missing bridge: voids and pockets in biomolecules host structured water whose removal or retention carries a large fraction of binding free energy and effective “interfacial tension.” The thermodynamic cost of displacing these waters is a direct probe of **local boundary energetics**, and therefore a natural A8 observable.

### Water displacement as an interfacial meter

The attached reference paper develops a rigorous thermodynamic cycle for **water displacement from binding cavities**, using supramolecular cages and cucurbituril hosts as model systems. It computes the free energy cost of removing waters from a cavity, $\Delta G_{\rm disp}^{\rm H_2O}$, and decomposes binding affinities into host–guest and water terms. Key findings include:

* Water in certain cavities is **unfavorable** (high free energy); displacing it strongly stabilizes guest binding.
* In other cavities, cavity waters are **favorable**; displacing them carries a penalty that must be compensated by specific interactions.
* A significant fraction of the variation in binding free energies across hosts and guests can be attributed to **differences in water‑displacement free energy**, not just direct host–guest contacts.:contentReference[oaicite:3]{index=3}

This structure is almost tailor‑made for A8:

* Cavities and pockets are **finite‑scale voids** with well‑defined surfaces.
* The water network inside them acts as a **microscopic boundary layer** with measurable energy and entropy.
* The free energy of clearing that layer can be treated as a **“void chemical potential”** and used as a meter for how “resolved” or “dry” a hierarchy level is.

### Repository‑local context

This T2 proposal sits in the A8 ladder alongside:

* **CF3_A8_Scaling_Hierarchical_Interfaces.md** — formal A8 scaling framework and hierarchy definitions.:contentReference[oaicite:4]{index=4}  
* **T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md** — protein packing meters and 0.55 packing fraction instruments.:contentReference[oaicite:5]{index=5}  
* **T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md** — STIV macrostate meters for boundary‑law and hierarchy observables.  

The present instrument adds a **hydration‑scale boundary meter** that can later be cross‑gated with protein packing, RD‑based interface models, and A8 scaling experiments.

---

## 5. Intellectual Merit and Procedure

**Importance.** A8’s claims about hierarchical interfaces require meters that work across scales: from macroscopic boundaries to molecular cavities. Hydration thermodynamics at binding sites is one of the few arenas where **microscopic boundary energetics** are both measurable and deeply studied. A certified water‑displacement meter provides:

* A local estimate of “void dryness” and interfacial energy per cavity.
* A way to decompose binding affinities into **geometry/void** vs **direct interaction** components.
* A testbed for A8‑style questions (e.g., how boundary energy scales with cavity size and topology) without yet making any axiom claim.

**Broader impacts.** Beyond A8, such meters are directly relevant to drug design, supramolecular chemistry, and biomolecular engineering, where understanding the **hydrophobic/hydrophilic contribution of water** is central to rational design.

**Approach.** Implement a **replayable pipeline** that:

1. Ingests host–guest systems and thermodynamic data from the reference study.
2. Defines per‑cavity meters for water occupancy, displacement free energy, and contribution to binding.
3. Calibrates and gates those meters by reproducing published results within predeclared tolerances.
4. Exports meter outputs in A8‑compatible form (JSON/CSV) so later CFN/PROPOSALs can treat them as inputs to hierarchy and packing analyses.

---

### 5.1 Experimental Setup and Diagnostics

#### 5.1.0 Systems, observables, and meters

**Systems.**  
Use the minimal host–guest set from the reference study (e.g., neutral and charged hosts with hard‑sphere or simple guests; exact list to be specified in the specs file). Coordinates and parameters are taken from the supporting information or reconstructed from the published force‑field definitions.

**Core observables.**

For each binding site / cavity (index $i$):

* $N_i^{\rm H_2O}$ — average number of waters in the cavity in the unbound state.
* $\Delta G_{{\rm disp},i}^{\rm H_2O}$ — free energy cost of displacing the cavity waters to bulk.
* $\Delta G_{{\rm bind},i}$ — binding free energy for the corresponding guest in that cavity.
* $\Delta G_{{\rm bind},i}^{\rm (water)}$ — water‑displacement contribution to binding (as defined by the thermodynamic cycle).
* $D_i$ — a **void‑dryness index**, e.g.
  \[
  D_i \equiv -\frac{\Delta G_{{\rm disp},i}^{\rm H_2O}}{k_{\rm B}T\,A_i},
  \]
  where $A_i$ is an effective cavity surface area proxy (from Voronoi tessellation or SASA), turning displacement free energy into an **energy per unit boundary**.

**Meters.**

1. **Water‑displacement free‑energy meter (WDM‑G).**  
   Computes $\Delta G_{{\rm disp},i}^{\rm H_2O}$ via the same thermodynamic cycle as in the reference (hydration + binding difference, or direct PMF if available).:contentReference[oaicite:8]{index=8}  

2. **Binding‑decomposition meter (WDM‑B).**  
   Decomposes $\Delta G_{{\rm bind},i}$ into water and direct host–guest contributions and reports the fraction explained by water displacement:
   \[
   f_i^{\rm (water)}=\frac{\Delta G_{{\rm bind},i}^{\rm (water)}}{\Delta G_{{\rm bind},i}}.
   \]

3. **Void‑dryness boundary meter (WDM‑D).**  
   Reports $D_i$ and aggregates it over cavities by size, chemistry, and topology (e.g., hydrophobic vs polar pockets).

4. **Cycle‑closure meter (WDM‑C).**  
   Checks consistency of the thermodynamic cycle: direct vs indirect routes to $\Delta G_{{\rm disp},i}^{\rm H_2O}$ must agree within a tolerance.

#### 5.1.1 Pre‑Run Config Requirements

Create the following machine‑readable artifacts before any artifact‑writing run; this mirrors the STIV and protein‑packing instruments.

* `Derivation/code/physics/a8_water/APPROVALS_WaterDisplacement.json`
* `Derivation/code/physics/a8_water/schemas/WaterDisplacement_Meters.schema.json`
* `Derivation/code/physics/a8_water/specs/WaterDisplacement_Meters.v1.json`
* `Derivation/experiments/prereg/WaterDisplacement_Meters.v1.json`

**APPROVALS_WaterDisplacement.json (template):**

```json
{
  "preflight_name": "a8_water_displacement_preflight",
  "description": "Approval manifest for A8 water-displacement meters; preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs may execute under Derivation/code/tests. Artifact-writing runs require this T2 proposal and prereg tag.",
  "pre_registered": true,
  "proposal": "Derivation/Proposals/T2_A8_PROPOSAL_Water-Displacement-Meters_v1.md",
  "allowed_tags": ["a8-water-displacement-v1"],
  "schema_dir": "Derivation/code/physics/a8_water/schemas",
  "approvals": {
    "a8-water-displacement-v1": {
      "schema": "Derivation/code/physics/a8_water/schemas/WaterDisplacement_Meters.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto",
      "approval_key": "auto"
    }
  }
}
````

**PRE‑REGISTRATION.json (minimum keys):**

```json
{
  "proposal_title": "T2 — Water-Displacement Meters for Interfacial Hierarchies",
  "tier_grade": "T2",
  "commit": "HEAD_SHA_HERE",
  "salted_provenance": "salted_sha256_here",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"Water-displacement free energies match literature values within 1 kcal/mol RMS.","direction":"no-change"},
    {"id":"H2","statement":"Across the calibration set, ΔG_bind correlates strongly with ΔG_disp^H2O.","direction":"no-change"},
    {"id":"H3","statement":"Void-dryness index D clusters by cavity type (hydrophobic vs polar/charged).","direction":"no-change"},
    {"id":"H4","statement":"Thermodynamic cycle closure error remains below 0.5 kcal/mol.","direction":"no-change"}
  ],
  "variables": {
    "independent": ["host_id","guest_id","cavity_id","temperature","forcefield","seed"],
    "dependent": ["ΔG_disp_H2O","ΔG_bind","f_water","D","cycle_error"],
    "controls": ["cutoff_scheme","thermostat","barostat","simulation_length"]
  },
  "pass_fail": [
    {"metric":"rms_error_ΔG_disp","operator":"<=","threshold":1.0,"unit":"kcal/mol"},
    {"metric":"R2_corr_ΔGbind_vs_ΔGdisp","operator":">=","threshold":0.85,"unit":""},
    {"metric":"cluster_sep_D","operator":">=","threshold":1.0,"unit":"z-score"},
    {"metric":"max_cycle_error","operator":"<=","threshold":0.5,"unit":"kcal/mol"}
  ],
  "spec_refs": ["Derivation/code/physics/a8_water/specs/WaterDisplacement_Meters.v1.json"],
  "registration_timestamp": "AUTO-UTC"
}
```

**Specs & Schemas.**
The `specs` file should list:

* host/guest IDs, temperatures, and simulation lengths,
* analysis windows and cavity definitions,
* mapping from raw logs (e.g., PMFs, occupancy counts) to meter outputs.

The schema should enforce units (kcal/mol, nm², etc.) and required keys for each meter.

#### 5.1.2 Gate definitions

1. **Gate WDM‑G1 (Free‑energy reproduction).**
   RMS difference between measured $\Delta G_{{\rm disp},i}^{\rm H_2O}$ and reference values across the calibration set must be **≤ 1.0 kcal/mol**; report RMS and max errors.

2. **Gate WDM‑G2 (Binding correlation).**
   Linear regression of $\Delta G_{{\rm bind},i}$ vs $\Delta G_{{\rm disp},i}^{\rm H_2O}$ across hosts/guests must yield **slope $s$ in [0.7,1.3]** and **$R^2\ge 0.85$**, indicating that a substantial fraction of binding variation is captured by water displacement.

3. **Gate WDM‑G3 (Void‑type separation).**
   The void‑dryness index $D_i$ must show statistically significant separation between hydrophobic and polar/charged cavities (e.g., two‑sample $t$‑test or nonparametric equivalent with $p<10^{-4}$; effect size ≥1 in z‑score units).

4. **Gate WDM‑G4 (Thermodynamic cycle closure).**
   For each cavity with both direct and indirect routes available, **cycle closure error** $|\Delta G^{\rm (direct)}*{{\rm disp},i}-\Delta G^{\rm (cycle)}*{{\rm disp},i}|$ must be ≤0.5 kcal/mol; summary max and 95th percentile must be reported.

5. **Gate WDM‑G5 (Numerical stability).**
   Across seeds and replicates, meter outputs must show coefficient of variation ≤5% for $\Delta G_{{\rm disp},i}^{\rm H_2O}$ and ≤10% for $D_i$; failures trigger grid/time‑step and sampling diagnostics.

---

### 5.2 Experimental runplan

**Scope banner:** *T2 instrument calibration only; no phenomenon claims.* A8 hierarchy and cosmology claims remain governed by the separate A8 T1/T3/T8 proposals.

**Datasets / testbeds.**

* **S1 — Literature replay.**
  Digitized or re‑extracted data from the reference paper (host/guest IDs, $\Delta G_{\rm disp}^{\rm H_2O}$, $\Delta G_{\rm bind}$, cavity classifications). This stage checks the analysis and gating code without running MD.

* **S2 — Minimal MD reproduction.**
  One or two host–guest systems with available coordinates and parameters, simulated with open‑source MD (e.g., GROMACS or OpenMM) to validate end‑to‑end reproducibility of a subset of $\Delta G_{\rm disp}^{\rm H_2O}$ values.

* **S3 — Synthetic cavities (optional stretch).**
  Simple geometric cavities (spherical, cylindrical) in explicit water to probe how $D_i$ scales with cavity size and shape; used as a bridge to CF3 and protein‑packing meters but not treated as an A8 test.

**Independent variable ladders.**

* Temperature: $T\in{280,300}$ K (if available).
* Hosts: at least one neutral hydrophobic cavity and one charged/polar cavity.
* Guests: at least one “hard sphere” guest and one interacting guest.
* Seeds: ${0..9}$ per system for S2/S3.

**Outputs & artifacts.**

* JSON/CSV tables of meter outputs for each cavity: $(N^{\rm H_2O},\Delta G_{\rm disp}^{\rm H_2O},\Delta G_{\rm bind},f^{\rm (water)},D,{\rm cycle_error})$.
* QC plots: scatter of $\Delta G_{\rm bind}$ vs $\Delta G_{\rm disp}^{\rm H_2O}$; histograms of $D$ by cavity type; cycle‑closure boxplots.
* Stored under `Derivation/code/outputs/meters/a8_water_displacement/{tag}/`.
* A T2 RESULTS paper following `RESULTS_PAPER_STANDARDS.md` that documents gates, passes/fails, and pinned artifacts.

**Success action.**
Mark the water‑displacement meters **CERTIFIED** and register them as A8 meters/gates (usable by protein‑packing, STIV, and future CFNs).

**Failure action.**
Quarantine with a CONTRADICTION_REPORT summarizing which gates failed (RMS error, correlation, separation, or cycle closure). If failure is methodological (e.g., insufficient sampling), adjust specs (longer MD, different analysis windows) and resubmit; if failure is structural (e.g., systematic bias), note this as an explicit limitation of A8 hydration meters.

---

## 6. Personnel

**Justin K. Lietz** — implement meters and analysis code; author specs/schemas and prereg; run S1–S3; publish RESULTS and PASS/FAIL manifest; file promotion PR on PASS and wire cross‑gating with existing A8 instruments.

---

## 7. References

* **VDM / A8 Canon.**
  `CF3_A8_Scaling_Hierarchical_Interfaces.md`; `T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md`; `T2_PROPOSAL_STIV_Macrostate_&_Gradient-Flow_Meters_v1.md`; `T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md`.

* **Water displacement reference.**
  *Thermodynamics of Water Displacement from Binding Sites and its Contributions to Supramolecular and Biomolecular Affinity* (core free‑energy cycles, host–guest systems, and hydration analyses).

* **Proposal and tier standards.**
  `Derivation/Templates/PROPOSAL_PAPER_TEMPLATE.md`; `Derivation/TIER_STANDARDS.md`; `Derivation/Templates/RESULTS_PAPER_STANDARDS.md`.

---

## Implementation classification, objective, and plan (VDM work‑order style)

**Classification:** Derived‑limit (Instrument).

**Objective (one‑liner):**
Certify water‑displacement meters as hydration‑scale A8 boundary‑law observables with preregistered PASS/FAIL gates.

**Action plan (≤7):**

1. Implement parsers and data structures for host–guest and hydration data (S1) plus optional MD logs (S2/S3).
2. Implement WDM‑G, WDM‑B, WDM‑D, and WDM‑C meters with unit‑checked outputs and schema validation.
3. Author **APPROVALS/SCHEMA/SPECS** and **PREREG** artifacts listed in §5.1.1 and sign the prereg tag.
4. Run S1 (literature replay) and tune only analysis parameters allowed by the prereg; lock thresholds.
5. Run S2 MD reproductions and, if feasible, S3 synthetic cavities; compute gate metrics and QC plots.
6. Publish a T2 RESULTS whitepaper with pinned artifacts and PASS/FAIL manifest; note any limitations.
7. On PASS, register the meters in the A8 registry and wire them into cross‑gating with protein‑packing and STIV instruments.

**Verification.**
Meter certification is granted only if **all** gates WDM‑G1–G5 pass under the preregistered thresholds on S1 and at least one S2 system. Any gate failure triggers explicit CONTRADICTION_REPORT logging and blocks A8‑level usage until resolved.
