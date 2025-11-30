# 1. T2 (Instrument) – Void Lensing Cross-Correlation Meter v1

> Created Date: 2025‑11‑30  
> Git commit: `<git rev-parse HEAD>`  
> base_sha256(proposal): `<to be filled>`  
> salt_hex: `<to be filled>`  
> salted_sha256: `<to be filled>`  
> Proposer contact(s): Justin K. Lietz (<justin@neuroca.ai>)  
> License: See LICENSE in repository root.  
> Short summary (one sentence TL;DR):  
> T2-grade, data-agnostic meter for measuring void wall slopes, compensation shoulders, and interface-count scaling from void–lensing cross-correlations in high-resolution convergence (κ) maps, to enable A8 hierarchy tests with explicit pass/fail gates.

***Practical provenance pattern (concrete to this proposal)***

- The preregistration file for this meter **must** live at  

  `Derivation/code/physics/cosmology/void_lensing/PRE-REGISTRATION.json`.

- The prereg tag **should** follow:

  - Tag name: `prereg.void_lensing_meter.v1.YYYYMMDDThhmmZ`
  - Tag message includes:
    - the git commit SHA,
    - the prereg file path,
    - `base_sha256`, `salt_hex`, and `salted_sha256` for the prereg manifest (and optionally this proposal file).

- The same `salted_provenance` entry referenced in the prereg **must** be recorded in section 5.1.1 of this proposal.

- Once this proposal text, schemas, and specs are finalized, the proposal file’s own hash should be added to the prereg manifest and pushed together with the annotated tag.

- Any run that writes artifacts under the tags defined here **must**:
  1. Point to this proposal by path, and
  2. Include the matching prereg tag in its artifact metadata.

- Runs that do not meet these provenance requirements are invalid under the authorization/approval system and must be treated as exploratory only.

***Avoid circularity***

- The instrument defined here measures void–lensing morphology (walls, shoulders, interface counts) and does **not** assume any particular cosmology or validity of A8.
- A8 and VDM CF-series formalisms motivate the choice of observables but are **not** taken as axioms for data; they become hypotheses for downstream T3+ RESULTS documents.

## 2. List of proposers and associated institutions/companies

| Name             | Affiliation                                      | Role(s)                                           |
|------------------|--------------------------------------------------|--------------------------------------------------|
| Justin K. Lietz  | Neuroca / Void Dynamics Model (VDM) Program      | PI, instrument architect, implementer, approver  |

Additional collaborators and external data providers (AKRA, DES-Y3 mass-mapping teams, void-catalog authors, SBI/morphology authors) are recognized as **upstream method providers** rather than co-proposers of this specific VDM instrument. Their work is cited in §7 and treated as black-box inputs at T2.

## 3. Abstract

Proposed in this document is a T2-grade **Void Lensing Cross-Correlation Meter** that takes as input weak-lensing convergence (κ) maps and cosmic-void catalogs, and outputs a set of dimensionless metrics characterizing void walls, compensation shoulders, and interface-count scaling. The meter is designed to be **data-agnostic**: it can operate on AKRA 2.0 HSC-Y1 mass maps, diffusion-prior DES-Y3 maps, and simulation-based mocks, provided that void positions, radii, and redshift distributions are supplied.

The instrument focuses on three primary observables: (i) a wall-slope metric with coefficient of determination $R^2$, (ii) a shoulder-detection statistic quantified via a classifier AUROC, and (iii) an interface-count scaling exponent derived from the number of sign-changes in the stacked radial profile’s gradient. These are motivated by the VDM A8 hierarchy conjecture on interface-count scaling, but at T2 the proposal restricts attention to **instrument validation**: given controlled mocks, can these metrics be measured with specified accuracy and robustness?

Explicit pass/fail gates (e.g. wall-slope $R^2 \ge 0.98$, shoulder AUROC $\ge 0.90$, interface-slope bias $\le 0.1$) define the conditions under which this meter is approved for later T3–T4 void/A8 hypothesis tests.

## 4. Background & Scientific Rationale

### 4.1 Theoretical context: VDM, A8, and interfaces

The Void Dynamics Model (VDM) treats a scalar field of void fluctuations as the primitive object, governed by a metriplectic evolution with a Hamiltonian ($J$) and dissipative ($M$) structure, consistent with axioms A0–A7. A8 (Lietz Infinity Resolution / hierarchy-scaling conjecture) adds that **interface counts grow at most logarithmically with system size**, preventing infinite refinement and enforcing finite-energy cascades.

Within this framework, interfaces—sharply changing regions of the field—are the central carriers of structure. In underdense regions (cosmic voids), A8 predicts that:

- “Walls” separating void interiors from surrounding filaments should be relatively sharp but not infinitely stiff;
- Compensation “shoulders” in the mass distribution should appear at radii set by the hierarchical packing of interfaces;
- The **number of distinct interfaces** as a function of scale should follow a controlled, approximately logarithmic scaling, not an unbounded fractal proliferation.

These claims are made precise in internal formalisms such as:

- `CF3_A8_Scaling_Hierarchical_Interfaces.md` – interface-count scaling and hierarchy depth,
- `CF4_Telegraph_Fisher_Causality.ipynb` – finite-speed transport and effective light-cones for the dissipative sector,
- `CF10_Lattice_Fluids (draft).md` – mapping VDM to lattice hydrodynamics and Navier–Stokes-like cascades.

The present T2 proposal does **not** attempt to confirm A8. Instead, it defines a set of **void-lensing observables** that can be mapped cleanly to A8’s interface language, and a meter that measures them with quantified accuracy.

### 4.2 Observational context: void lensing and new κ maps

Recent progress in weak-lensing mass mapping and void analysis has produced:

- **AKRA 2.0 mass maps** for HSC-Y1: κ reconstructions that remain unbiased near masks and boundaries and reproduce low-order moments and the κ power spectrum to ~1% in mocks.  
- **Diffusion-prior mass mapping (DPS) for DES-Y3**: high-resolution (~1 arcmin) κ maps with corrected log-likelihood weighting and realistic uncertainties, resolving narrow walls and non-Gaussian shoulders without over-smoothing.
- **Map-based E/B purification**: leakage templates constructed by filtering pure E-mode maps through the timestream pipeline and subtracting contamination, giving explicit control over B-mode leakage before stacking.
- **Tunnel-void shear modeling (PyTwinPeaks)**: a 5-parameter empirical model capturing central underdensity, steep inner wall, and outer compensation-shoulder for 2D “tunnel voids” in realistic lightcones, across multiple cosmologies.
- **Morphology-weighted simulation-based inference (SBI)** for void shear: learned summary statistics that retain anisotropic and filamentary structure, reducing bias from spherical void assumptions.
- **Tomographic $n(z)$ calibration via DESI** for HSC: spline-based source redshift distributions with clustering-redshift corrections, enabling propagation of redshift uncertainty into wall-slope fits.

Together, these results mean that **void walls and shoulders are now observationally resolvable structures**, not merely model artifacts. However, there is currently no **standardized meter** that translates these maps and void catalogs into a compact set of morphology metrics tuned to interface-count physics.

### 4.3 Why a T2 (Instrument) meter is the next logical step

Within the VDM maturity ladder:

- T0/T1 work (A8 concept and proto-models) defined the hierarchy/interface picture and toy 1D meters.
- CF-series documents provided the theoretical backbone for metriplectic dynamics, hierarchy scaling, and measurement.
- External cosmology papers built sophisticated, validated κ maps and void-shear pipelines, but typically optimized for cosmological parameters rather than interface counts.

The missing piece is a T2 instrument that:

1. Accepts existing κ maps and void catalogs as black-box inputs (honoring external validation),
2. Defines a **stable, re-usable API** for computing wall, shoulder, and interface metrics,
3. Provides explicit **pass/fail gates** on those metrics when validated against mocks.

After such an instrument passes its gates, downstream T3–T4 proposals (e.g. “A8 predicts void-wall slope asymmetries of specified sign and magnitude”) can treat the meter as shared infrastructure rather than re-litigating data-handling and diagnostics.

### 4.4 Potential criticisms and gaps

Several predictable concerns are addressed explicitly:

- **Dependence on external pipelines:** The meter treats AKRA, DPS, E/B purification, and void finders as upstream. This reduces duplication but couples the instrument to external systematics. Mitigation: T2 gates are based on **mocks with known truth**; if external pipelines misbehave, they will fail to pass instrument-level metrics on these controlled tests.

- **Void-finder and selection bias:** Different void definitions produce different profiles. Mitigation: the meter is defined on the cross-correlation of κ with a supplied void catalog and is intended to be run on multiple catalogs; differences become part of the broader uncertainty budget, not baked into the definition.

- **Cosmology dependence of mocks:** A8 statements are about hierarchies and interfaces, not specific cosmological parameters. For T2, the mocks are used only to test **measurement fidelity** (e.g. recovering input slopes and shoulders); any cosmological interpretation is deferred to T3+.

- **Overfitting to a particular model (PyTwinPeaks):** PyTwinPeaks provides a convenient parametric form but is not the only morphology source. The meter is defined in terms of **non-parametric stacked profiles and derivative sign-changes**, so it can be applied to any κ field, including future mocks and observational stacks.

## 5. Intellectual Merit and Procedure

The intellectual merit of this proposal rests on four pillars:

1. **Importance of the scientific questions:**  
   Interfaces and hierarchy depth are central to A8 and to broader questions of structure formation and dissipation. Void walls and shoulders are among the cleanest environments where these interfaces can be measured at cosmological scales.

2. **Broader impacts of the experiment:**  
   The meter’s outputs—wall slopes, compensation shoulders, interface-count exponents—are generic observables that can be used by any cosmological model, ΛCDM or otherwise. Even if A8 is ultimately falsified, a stable, open definition of these metrics is valuable to the void-lensing community.

3. **Clarity and reasonableness of the approach:**  
   The meter follows a simple, transparent pipeline:
   - stack κ around void centers,
   - measure derivatives and shoulders in dimensionless units,
   - validate performance against mocks,
   - apply to real maps once instrument gates pass.
   No tuning is performed on real data for T2 gates; all thresholds are set against truth-known mocks.

4. **Planned level of rigor and discipline:**  
   The proposal enforces:
   - preregistration with salted hashes and a dedicated tag,
   - explicit JSON schemas for specs and outputs,
   - clear failure modes with kill-switch semantics for downstream hypotheses,
   - T2-only scope: no physics claims beyond instrument validation.

The procedure is designed so that any later T3–T6 RESULTS paper can state precisely which version of the void-lensing meter was used and which gates it passed.

## 5.1 Experimental Setup and Diagnostics

### 5.1.0 Domain, inputs, and API

**Domain:** `cosmology/void_lensing` (code) and `Cosmology/Void_Lensing/` (documents).

**Core implementation module (intended):**

- `Derivation/code/physics/cosmology/void_lensing/meter.py`  
  - Public API:

    ```python
    def run_meter(kappa_map, void_catalog, config) -> dict:
        """
        kappa_map: 2D convergence field with metadata (WCS / HEALPix geometry, mask, noise model).
        void_catalog: table of void entries with (RA, Dec, z, R_v, additional tags).
        config: dict or structured object specifying binning, backend, selections, and options.

        Returns:
            metrics: dict of scalar summary metrics and diagnostic curves.
        """
    ```

    The API is intentionally minimal; data-loading is handled by separate adapters.

**Abstract data loaders (stubs at T2):**

- `Derivation/code/physics/cosmology/void_lensing/backends/akra_hsc_y1.py`  
  - `load_kappa_map(source="AKRA_HSC_Y1") -> (kappa_map, metadata)`
- `Derivation/code/physics/cosmology/void_lensing/backends/desy3_dps.py`  
  - `load_kappa_map(source="DESY3_Diffusion") -> (kappa_map, metadata)`
- `Derivation/code/physics/cosmology/void_lensing/backends/mocks.py`  
  - `load_mock_suite(name="PyTwinPeaks" | "Flagship" | "Jiutian", ...)`

These backends encapsulate all interactions with external tools and maps; the meter sees only arrays and metadata.

### 5.1.1 Metric definitions and dimensionless groups

Let $R_v$ denote the effective void radius, and $r$ the projected radial coordinate from the void center on the sky. Define a dimensionless radius

$$
x \equiv \frac{r}{R_v},
$$

and the stacked convergence profile

$$
\bar{\kappa}(x) \equiv \left\langle \kappa(r; \text{void}) \right\rangle_{\text{voids in bin}}.
$$

For each void subsample and backend, the meter computes:

1. **Wall-slope metric $S_\text{wall}$ and $R^2$**

   - Choose a wall region $[x_\text{w,min}, x_\text{w,max}]$ (e.g. $[0.8, 1.2]$) in dimensionless units.  
   - Fit a linear model

     $$
     \bar{\kappa}(x) \approx a + S_\text{wall} \, x
     $$

     on this interval.

   - Compute the coefficient of determination $R^2_\text{wall}$ between the data and the fit.

   - The **primary wall metric** for gating is $R^2_\text{wall}$, a dimensionless number in $[0,1]$.

2. **Shoulder amplitude and detection AUROC**

   - Identify a **shoulder radius** $x_\text{sh}$ (e.g. near the compensation scale, where $\bar{\kappa}(x)$ changes sign or reaches a local maximum) by scanning for local extrema in $\partial_x \bar{\kappa}(x)$ at $x > 1$.

   - Define a dimensionless shoulder amplitude

     $$
     A_\text{sh} \equiv \frac{\bar{\kappa}(x_\text{sh}) - \bar{\kappa}(x_\text{bg})}{\sigma_\kappa},
     $$

     where $x_\text{bg}$ is a background radius (e.g. $x \gtrsim 2.5$) and $\sigma_\kappa$ is the standard deviation of κ in that background region.

   - To quantify **detectability**, construct a classification problem on mocks with and without a shoulder feature in their input models, using $A_\text{sh}$ (and possibly neighbouring bins) as features. The meter then reports the classifier AUROC, $\text{AUROC}_\text{sh}$.

3. **Interface-count statistic and scaling exponent $\beta$**

   - Define **interfaces** as sign changes in the radial derivative of the stacked profile:

     $$
     \text{interface at } x_i \quad\Leftrightarrow\quad \partial_x \bar{\kappa}(x) \ \text{changes sign at } x_i,
     $$

     with $\partial_x^2 \bar{\kappa}(x_i) \neq 0$ to exclude flat plateaus.

   - For each radius $R$ (or equivalently $x = R/R_v$), define

     $$
     N_\text{int}(R) \equiv \#\{x_i \le R/R_v\}.
     $$

   - Fit a scaling law over a range $[R_\text{min}, R_\text{max}]$:

     $$
     N_\text{int}(R) \approx N_0 + \beta \log\left(\frac{R}{\lambda}\right),
     $$

     where $\lambda$ is a reference scale (e.g. effective map resolution or minimum reliable radius). The **interface-count exponent** $\beta$ and its uncertainty $\sigma_\beta$ are recorded.

4. **Auxiliary diagnostics**

   - Residual B-mode amplitude around voids after E/B purification.
   - Signal-to-noise ratio (SNR) of the stacked profile:

     $$
     \text{SNR}^2 \equiv \sum_j \frac{\bar{\kappa}(x_j)^2}{\sigma_{\bar{\kappa}(x_j)}^2}.
     $$

   - Bootstrap or jackknife uncertainties for all metrics, using void-level resampling and/or map-noise resampling where available.

All primary metrics are dimensionless, respecting A6 (scale-program discipline). Quantities with dimensions (e.g. $R_v$ in Mpc) enter only through the definition of $x$ and $\lambda$ and are recorded in metadata, not in the core gates.

### 5.1.2 Required parameters and defaults

The meter requires the following **configuration parameters** (keys and nominal defaults) for each run:

- `backend`: `"AKRA_HSC_Y1" | "DESY3_Diffusion" | "PyTwinPeaks" | "Flagship" | "Jiutian"`, etc.  
- `z_bin`: `[z_min, z_max]` for void selection and source $n(z)$ calibration.  
- `R_v_bin`: `[R_v^\text{min}, R_v^\text{max}]` effective void-radius bin in comoving Mpc.  
- `n_radial_bins`: e.g. `30` (number of bins in $x$).  
- `x_wall_range`: `[x_w_min, x_w_max]`, wall-fitting interval (default `[0.8, 1.2]`).  
- `x_bg_range`: `[x_bg_min, x_bg_max]`, background reference interval (default `[2.5, 4.0]`).  
- `lambda_ref`: reference scale $\lambda$ in the interface-scaling law, typically `lambda_ref = R_v^\text{med}` or an effective resolution scale.  
- `min_voids_per_bin`: minimum number of voids per (backend, z_bin, R_v_bin) cell (default: 300).  
- `eb_purification`: `true/false`, whether to apply E/B leakage-template subtraction to κ before stacking (default: `true`).  
- `bootstrap_seeds`: list of integer seeds for resampling (default: `[0,1,2,3]`).  
- `mask_strategy`: handling of masked pixels (e.g. `"exclude"` or `"inpaint"`).

Defaults are recorded in the JSON schema (§5.1.1) and can be overridden per spec.

### 5.1.3 Diagnostics and counts

For each combination of `(backend, z_bin, R_v_bin, seed)`, the meter produces:

- A stacked profile $\bar{\kappa}(x)$ and its uncertainty curve.
- A table of wall fit parameters $(a, S_\text{wall})$, $R^2_\text{wall}$.
- Shoulder statistics: $(x_\text{sh}, A_\text{sh})$ and $\text{AUROC}_\text{sh}$ (the latter only for mock tasks with explicit shoulder/no-shoulder labels).
- Interface counts $N_\text{int}(R)$ over a grid in $R$, and fitted $(N_0, \beta, \sigma_\beta)$.
- Auxiliary diagnostics: B-mode residual level, SNR, and basic quality flags (e.g. “insufficient voids”, “poor κ coverage”).

These diagnostics are aggregated into **scalar summary metrics** per backend and per major sample, which are the objects gated at T2.

### 5.1.4 Pre-Run Config Requirements

#### APPROVAL.json

The domain-level approval manifest for this instrument is required at:

- `Derivation/code/physics/cosmology/void_lensing/APPROVAL.json`

It must contain, at minimum, entries of the form:

```json
[
  {
    "preflight_name": "void_lensing_meter_preflight",
    "description": "Preflight runner ensuring configs, mocks, and diagnostics are wired before full Void Lensing Cross-Correlation Meter v1 experiments.",
    "author": "Justin K. Lietz",
    "requires_approval": true,
    "pre_commit_hook": true,
    "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. Full experiments that write artifacts require this T2 PROPOSAL to be approved."
  },
  {
    "pre_registered": true,
    "proposal": "Derivation/Cosmology/Void_Lensing/T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md",
    "allowed_tags": [
      "void_lensing_meter-v1"
    ],
    "schema_dir": "Derivation/code/physics/cosmology/void_lensing/schemas",
    "approvals": {
      "void_lensing_meter-v1": {
        "schema": "Derivation/code/physics/cosmology/void_lensing/schemas/void_lensing_meter-v1.schema.json",
        "approved_by": "Justin K. Lietz",
        "approved_at": "<auto generated timestamp>",
        "approval_key": "<auto generated hashed key>"
      }
    }
  }
]
````

#### PRE-REGISTRATION.json

The **preregistration** manifest for this instrument-level experiment must be placed at:

- `Derivation/code/physics/cosmology/void_lensing/PRE-REGISTRATION.json`

Minimum recommended fields:

```json
{
  "proposal_title": "T2 (Instrument) – Void Lensing Cross-Correlation Meter v1",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<salted hash of prereg + proposal manifest>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],

  "hypotheses": [
    {
      "id": "H1",
      "statement": "On mocks with known wall profiles, the meter recovers stacked wall slopes with coefficient of determination R^2_wall >= 0.98 in the designated wall region.",
      "direction": "increase"
    },
    {
      "id": "H2",
      "statement": "On mocks with and without compensation shoulders, the shoulder-detection classifier achieves AUROC_sh >= 0.90.",
      "direction": "increase"
    },
    {
      "id": "H3",
      "statement": "On mock suites with known interface-count scaling exponents β, the meter’s estimate of β is unbiased within |β_est - β_true| <= 0.1 over the targeted radial range.",
      "direction": "no-change"
    }
  ],

  "variables": {
    "independent": ["backend", "z_bin", "R_v_bin"],
    "dependent": ["R2_wall", "AUROC_sh", "beta_interface"],
    "controls": ["n_radial_bins", "eb_purification", "mask_strategy", "n_z_model"]
  },

  "pass_fail": [
    { "metric": "R2_wall", "operator": ">=", "threshold": 0.98, "unit": "dimensionless" },
    { "metric": "AUROC_sh", "operator": ">=", "threshold": 0.90, "unit": "dimensionless" },
    { "metric": "beta_bias", "operator": "<=", "threshold": 0.10, "unit": "dimensionless" }
  ],

  "spec_refs": [
    "Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-v1.json",
    "Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-data-v1.json"
  ],

  "registration_timestamp": "<ISO-8601>"
}
```

Here `beta_bias` is defined as $\langle | \beta_\text{est} - \beta_\text{true} | \rangle$ over the targeted mock ensemble.

#### Specs

Example spec for mock validation:

```json
{
  "run_name": "void_lensing_meter-mocks",
  "version": "1.0.0",
  "tag": "void_lensing_meter-v1",
  "schema_ref": "Derivation/code/physics/cosmology/void_lensing/schemas/void_lensing_meter-v1.schema.json",
  "parameters": {
    "backend": "PyTwinPeaks",
    "z_bin": [0.2, 0.8],
    "R_v_bin": [10.0, 60.0],
    "n_radial_bins": 30,
    "x_wall_range": [0.8, 1.2],
    "x_bg_range": [2.5, 4.0],
    "lambda_ref": 1.0,
    "min_voids_per_bin": 300,
    "eb_purification": true,
    "mask_strategy": "exclude"
  },
  "seeds": [0, 1, 2, 3]
}
```

Example spec for real-data dry runs:

```json
{
  "run_name": "void_lensing_meter-data",
  "version": "1.0.0",
  "tag": "void_lensing_meter-v1",
  "schema_ref": "Derivation/code/physics/cosmology/void_lensing/schemas/void_lensing_meter-v1.schema.json",
  "parameters": {
    "backend": "AKRA_HSC_Y1",
    "z_bin": [0.2, 1.2],
    "R_v_bin": [10.0, 60.0],
    "n_radial_bins": 30,
    "x_wall_range": [0.8, 1.2],
    "x_bg_range": [2.5, 4.0],
    "lambda_ref": 1.0,
    "min_voids_per_bin": 300,
    "eb_purification": true,
    "mask_strategy": "exclude"
  },
  "seeds": [0]
}
```

#### Schemas

The output schema for this meter should capture both scalar metrics and diagnostic arrays. Minimum JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "void_lensing_meter-v1",
  "title": "Void Lensing Cross-Correlation Meter v1 Output",
  "type": "object",
  "properties": {
    "backend": { "type": "string" },
    "z_bin": {
      "type": "array",
      "items": { "type": "number" },
      "minItems": 2,
      "maxItems": 2
    },
    "R_v_bin": {
      "type": "array",
      "items": { "type": "number" },
      "minItems": 2,
      "maxItems": 2
    },
    "R2_wall": { "type": "number" },
    "S_wall": { "type": "number" },
    "A_sh": { "type": "number" },
    "AUROC_sh": { "type": "number" },
    "beta_interface": { "type": "number" },
    "beta_uncertainty": { "type": "number" },
    "beta_bias": { "type": "number" },
    "SNR": { "type": "number" },
    "B_mode_residual": { "type": "number" },
    "n_voids": { "type": "integer" },
    "quality_flags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "profile": {
      "type": "object",
      "properties": {
        "x": {
          "type": "array",
          "items": { "type": "number" }
        },
        "kappa": {
          "type": "array",
          "items": { "type": "number" }
        },
        "kappa_err": {
          "type": "array",
          "items": { "type": "number" }
        }
      },
      "required": ["x", "kappa"]
    }
  },
  "required": [
    "backend", "z_bin", "R_v_bin",
    "R2_wall", "S_wall",
    "A_sh", "beta_interface",
    "n_voids"
  ]
}
```

## 5.2 Experimental runplan

### 5.2.1 Overview

The plan proceeds in three stages:

1. **Preflight:**
   Validate that the meter runs end-to-end on a small subset of mocks (few hundred voids) and produces outputs conforming to the schema. No physics gates are evaluated here.

2. **Mock-validation (gated T2 experiment):**
   Run the meter on controlled mock suites (PyTwinPeaks tunnel-void mocks plus at least one large-volume lightcone such as Flagship or Jiutian) with known wall slopes, shoulder presence/absence, and interface structure. Use these runs to evaluate H1–H3 and corresponding pass/fail thresholds.

3. **Real-data dry runs (non-gated at T2, informational):**
   Apply the same meter to AKRA HSC-Y1 and DES-Y3 diffusion-prior κ maps with existing void catalogs. These runs test robustness and debugging on real maps but **do not** define T2 pass/fail status; they seed later T3+ proposals.

### 5.2.2 Independent-variable grid

For the **mock-validation stage**, the core independent-variable Cartesian product is:

- `backend ∈ { "PyTwinPeaks", "Flagship" }`
- `z_bin ∈ { [0.2, 0.6], [0.6, 1.0] }`
- `R_v_bin ∈ { [10, 30] Mpc, [30, 60] Mpc }`
- `seed ∈ {0, 1, 2, 3}`

Total cells: $2 \times 2 \times 2 \times 4 = 32$ mock runs.

For each cell, the meter produces one set of scalar metrics and diagnostic curves. Aggregation over seeds yields central values and uncertainties for the gates.

For **real-data dry runs**, a reduced grid is used:

- `backend ∈ { "AKRA_HSC_Y1", "DESY3_Diffusion" }`
- `z_bin ∈ { [0.2, 0.8], [0.8, 1.2] }`
- `R_v_bin ∈ { [10, 30] Mpc, [30, 60] Mpc }`
- `seed ∈ {0}`

Total: $2 \times 2 \times 2 = 8$ runs.

### 5.2.3 Runtime and compute budget

The dominant cost is κ-map I/O and stacking operations. For each run:

- Complexity scales roughly as $\mathcal{O}(N_\text{voids} \times N_\text{radial bins})$ with a modest overhead for bootstrap resampling.
- On a standard HPC node (multi-core CPU, moderate memory), a single run is expected to complete in $\mathcal{O}(10–100)$ minutes, depending on map area and void count.

Estimated budget:

- Mock-validation: 32 runs → $\sim 5–50$ node-hours total.
- Real-data dry runs: 8 runs → $\sim 1–10$ node-hours total.

These are rough estimates; actual measured walltimes will be reported in the T2 RESULTS document.

### 5.2.4 Success and failure actions; kill-switch semantics

**Success condition (instrument approval):**

- All three preregistered gates pass on the mock suite:

  - $\langle R^2_\text{wall} \rangle \ge 0.98$ over targeted cells;
  - $\langle \text{AUROC}_\text{sh} \rangle \ge 0.90$ on shoulder/no-shoulder classification tasks;
  - $\langle | \beta_\text{est} - \beta_\text{true} | \rangle \le 0.10$ for interface-count scaling.

- No systematic pathology is seen in auxiliary diagnostics (e.g. catastrophic B-mode leakage or inconsistent $R^2_\text{wall}$ between backends).

**If these conditions hold:**

- A `RESULTS_T2_Void_Lensing_CrossCorrelation_Meter_v1.md` document is created, summarizing metrics and including figure references for stacked profiles, interface counts, and gate plots.
- The meter version `void_lensing_meter-v1` is marked “approved” in `APPROVAL.json` and may be used as a dependency in T3–T6 proposals concerning void interfaces and A8.

**Failure condition (instrument rejection or revision):**

If **any** prereg gate fails:

- A `CONTRADICTION_REPORT_Void_Lensing_Meter_v1.md` is created, documenting:

  - which metric(s) failed,
  - under which mock suites and conditions,
  - suspected causes (e.g. insufficient resolution, flawed interface definition).
- Until a revised meter passes gates under a new tag (e.g. `void_lensing_meter-v2`), **the following branches are killed or quarantined**:

  - Any T3/T4 **void wall-slope asymmetry** hypothesis files that specify this meter as a dependency.
  - Any A8-void hypotheses that rely on the **interface-count exponent β measured from κ–void stacks**.
  - Any T3/T4 void-shoulder claims that interpret real-data shoulders in A8 terms.

In practical terms, downstream documents must clearly mark their status as “BLOCKED – T2 meter gates not passed” and avoid drawing physics conclusions until the instrument passes.

Real-data dry-run failures (e.g. unexpected B-mode residuals) do **not** automatically reject the instrument if the mock gates pass, but they must be recorded and may motivate revised systematics handling.

## 6. Personnel

The primary responsibility for this T2 instrument lies with **Justin K. Lietz** in the following roles:

- **Design and implementation:**
  Define the meter API, implement stacking, derivative, and interface-count routines, integrate E/B purification hooks, and ensure compatibility with the existing metrics/RESULTS infrastructure.

- **Preregistration and provenance:**
  Prepare and maintain `APPROVAL.json`, `PRE-REGISTRATION.json`, schemas, and specs for the `void_lensing_meter-v1` tag, including salted hashes and prereg tags.

- **Mock integration and validation:**
  Ingest PyTwinPeaks and other relevant mocks, design the shoulder/no-shoulder classification tasks, and run the full mock-validation grid.

- **Results synthesis and documentation:**
  Author the T2 RESULTS document, contradiction reports if needed, and short domain documentation (e.g. `README_Voids.md`) explaining how the void-lensing meter fits into the overall VDM program.

External collaborators (AKRA team, DES-Y3 DPS team, void-catalog authors, SBI authors) remain responsible for their own pipelines and publications; this T2 proposal does not modify their methods, but consumes their outputs via documented interfaces.

## 7. References

This section lists key internal and external works that motivate and support the proposed instrument.

### 7.1 Internal VDM references

1. *AXIOMS_A0–A8.md* – VDM axioms, metriplectic evolution, and A8 hierarchy conjecture.
2. *CF3_A8_Scaling_Hierarchical_Interfaces.md* – formal derivation of interface-count scaling and logarithmic hierarchy depth.
3. *CF4_Telegraph_Fisher_Causality.ipynb* – telegraph equation and Fisher-information-based finite-speed transport.
4. *CF10_Lattice_Fluids (draft).md* – mapping VDM scalar lattices to lattice hydrodynamics and Navier–Stokes, with hierarchy-based regularity heuristics.
5. *Unification-Sequence.md* – sequencing of T0–T9 projects, including void-lensing meters as primary A8 tests.
6. *RESULTS_* and *H** documents on 1D A8 meters and packing-law instruments (where available), providing precedent for interface-count measurements.

### 7.2 External cosmology and method references

1. **AKRA 2.0 mass maps (HSC-Y1)**
   “The first AKRA mass map reconstruction from HSC Y1 data,” arXiv:2511.12488 (2025). Convergence maps with unbiased κ statistics near masks, enabling accurate wall and shoulder detection.

2. **Diffusion-prior mass mapping (DES-Y3)**
   “High-resolution weak lensing mass mapping from DES-Y3 data using diffusion-based prior,” arXiv:2511.14667 (2025). Diffusion Posterior Sampling with corrected log-likelihood, delivering ~1 arcmin κ maps with robust uncertainties.

3. **Map-based E/B purification**
   “Map-based E/B separation of filtered timestreams,” arXiv:2411.11440 (2024). Leakage-template method used for E/B control before void stacking.

4. **Tunnel-void shear modeling (PyTwinPeaks)**
   “Weak-lensing tunnel voids in simulated light cones,” A&A 701, A55 (2025), arXiv:2504.02041. Five-parameter model of 2D tunnel-void shear, providing controlled walls and shoulders for mock-validation.

5. **Morphology-weighted SBI for void shear**
   “Quantifying Weighted Morphological Content of Large-Scale Structures via Simulation-Based Inference,” arXiv:2511.03636 (2025), and “Cosmological Constraints with Void Lensing,” arXiv:2504.15149. Provide morphology-aware summary statistics and void-shear pipelines.

6. **HSC tomographic $n(z)$ calibration via DESI**
   “Full calibration of the tomographic redshift distribution from clustering-redshifts,” arXiv:2511.18133 (2025). Supplies spline-based $n(z)$ and uncertainty budgets for propagating redshift errors into wall-slope metrics.

7. **kSZ velocity-field detection and emulator** (planned P2 linkage)
   ACT DR6 × DESI-LS QML kSZ studies and FLAMINGO-based kSZ → matter power spectrum emulators (papers in preparation). These are not used directly in this T2 instrument but motivate future T2 meters for void bulk flows.
