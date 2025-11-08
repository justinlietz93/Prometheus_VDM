# oq021 runner

**What it checks (near-equilibrium):**

* **Entropy production** (\sigma=X^\top L X) non-negativity (A5, local) — from the **entropy balance** formulation and linear laws in de Groot & Mazur Ch. III–IV, §1–2 (eqs. for (J_s), (\sigma)) .
* **Onsager–Casimir reciprocity** (L = E,L^\top E) with parity (E=\mathrm{diag}(\epsilon_j)) — near-equilibrium reciprocity in isotropic media; see Ch. IV–VI (properties/transformations; presence/absence of magnetic field) .
* **Curie principle** zeroes **vector↔tensor** cross-couplings in isotropic media (masking those entries in (L)) — de Groot & Mazur Ch. IV–VI (Curie’s principle and its tensorial bookkeeping) .
* **Boundary entropy flux (J_s)** logging at walls/corners (OQ‑021) via BoundaryEntropyFluxMonitor; artifacts JSON/CSV/PNG are routed with io_paths.
  All sit cleanly alongside GENERIC’s J/M split and degeneracy constraints (§1.2, §2) in Öttinger, i.e., this runner **does not** alter your reversible/dissipative structure; it only audits the **near-equilibrium** limit and exposes violations early .

---

### 2) Result schema (machine-auditable)

**Path**: `Derivation/code/physics/fluid_dynamics/schemas/oq021_lit_gates.schema.json`

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "title":"OQ-021 LIT Gate Report",
  "type":"object",
  "properties":{
    "tag":{"type":"string"},
    "dims":{"type":"object","properties":{"Ny":{"type":"integer"},"Nx":{"type":"integer"}},"required":["Ny","Nx"]},
    "coeffs":{"type":"object","properties":{"kappa":{"type":"number"},"eta":{"type":"number"},"zeta":{"type":"number"}},"required":["kappa","eta","zeta"]},
    "sigma":{"type":"object","properties":{"min":{"type":"number"},"max":{"type":"number"},"any_negative":{"type":"boolean"}},"required":["min","max","any_negative"]},
    "onsager":{"type":"object","properties":{"residual_fro":{"type":"number"},"residual_linf":{"type":"number"},"tolerance_fro":{"type":"number"}},"required":["residual_fro","tolerance_fro"]},
    "curie":{"type":"object","properties":{"violations":{"type":"integer"}},"required":["violations"]},
    "entropy_monitor":{"type":"object"},
    "gates":{
      "type":"object",
      "properties":{
        "sigma_nonnegative":{"type":"boolean"},
        "onsager_within_tol":{"type":"boolean"},
        "curie_zero_cross":{"type":"boolean"},
        "PASS":{"type":"boolean"}
      },
      "required":["sigma_nonnegative","onsager_within_tol","curie_zero_cross","PASS"]
    }
  },
  "required":["tag","dims","coeffs","sigma","onsager","curie","gates"]
}
```

---

### 3) CLI usage (example)

```bash
python oq021_lit_runner.py \
  --T-npy code/outputs/fields/T.npy \
  --vx-npy code/outputs/fields/vx.npy \
  --vy-npy code/outputs/fields/vy.npy \
  --dx 1.0e-3 --dy 1.0e-3 \
  --kappa 0.6 --eta 1.0 --zeta 0.2 \
  --outdir code/outputs/fluids/oq021/lit/ --tag oq021-corner-l1 \
  --onsager_tol_fro 1e-10 --sigma_tol 0
```

Artifacts:

* `oq021-corner-l1__lit_gates.json` (validates against `oq021_lit_gates.schema.json`)
* `oq021-corner-l1__sigma.csv`
* `oq021-corner-l1__sigma.png`

---

### 4) Where this sits in the VDM picture

* **GENERIC split preserved**: the runner never edits your (J, M) objects; it *audits* the **near-equilibrium projection** in the de Groot/Mazur sense (forces/fluxes, Curie, Onsager). The J/M degeneracy and entropy-monotonicity remain enforced by your `validate_generic_structure` and `EntropyMonitor` paths (Öttinger §§1.2–2; Hydrodynamics) .
* **Curie/Onsager gates** are classic *sanity constraints* that flush unit mistakes and hidden symmetry leaks early (de Groot & Mazur Ch. IV–VI) .
* For **autocorrelation/binning/fit** discipline in later data reductions (not part of this runner), you can mirror the correlated-fit/SVD and jackknife/bootstrap patterns from lattice data analysis (see standard practice in lattice texts, e.g., Monte Carlo diagnostics, covariance truncation, jackknife/bootstrap) .

---

### 5) Minimal wiring steps

1. Drop `oq021_lit_runner.py` and the schema file into the paths above.
2. Ensure `Derivation/code/common/instrument_helpers/lit_tools.py` is importable, e.g. `from instrument_helpers.lit_tools import ...` (sys.path adds `Derivation/code/common`).
3. Add a CI step that:

   * runs the CLI,
   * validates the JSON against the schema, and
   * fails the job if `"gates"."PASS" == false`.
4. (Optional) register this as a **pre-publish** audit in your OQ-021 workflow so results won’t promote unless LIT gates pass.

---

If you want, I can also add a one-liner wrapper that **compares** `void_gain={0.0,0.5}` runs: same L, same grids, and produces a small table: [(\sigma_{\min}), Onsager residual, Curie violations] per setting — it’s a tidy way to prove the regularizer doesn’t break near-equilibrium structure while it tames corners out of equilibrium.
