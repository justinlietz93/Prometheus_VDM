**Create/Update `derivation/BC_IC_GEOMETRY.md` (MathJax-only, canonical BC/IC & domains)**

Search the entire repository (code, tests, notebooks, configs, experiment scripts, docs, comments) and compile **all boundary conditions (BC), initial conditions (IC), and domain geometries** that are actually used. **Do not invent or infer new content.** Use only what exists in the repo.

**Output file:** `derivation/BC_IC_GEOMETRY.md`
**Canon rule:** This file is the single owner of BC/IC definitions and domain geometries. Other docs must link here. **Do not restate core field equations or constants**—link to them by anchor.

**MathJax on GitHub:**

* Inline: `$ ... $` • Display: `$$ ... $$` • Optional alignment: `$$\begin{aligned} ... \end{aligned}$$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, `\label`, numbering, or package-specific macros.
* **Always** reference both files to double check syntax: derivation/MathJax-Offiial-Docs.md, derivation/MathJax-Offiial-Docs.pdf

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Boundary/Initial Conditions & Domain Geometries (Auto-compiled)

**Scope:** Single source of truth for BC/IC and domain geometries used in this repository.  
**Rules:** Link to equations/constants/symbols by anchor; do not restate them here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only.  
```

---

### Sections to populate (only with content found in repo)

#### 1) Domain Geometries

List every domain explicitly referenced (interval, box, periodic torus, cylinder/tube, lattice, etc.).

**Table schema (append rows):**

```markdown
| Geometry ID | Dim $d$ | Domain $\Omega$ (MathJax) | Parameters (link) | Boundary sets | Source (path:lines • commit) | Notes |
|---|---:|---|---|---|---|---|
```

* **Parameters (link):** link to `CONSTANTS.md` (sizes like `$L_x,L_y,R,a$`) and `SYMBOLS.md` for symbols.
* **Boundary sets:** names like `$\partial\Omega_D$`, `$\partial\Omega_N$`, “periodic in $x$”.

Add an HTML anchor before each row: `<a id="geom-<slug>"></a>`.

---

#### 2) Boundary Conditions (by geometry and field/channel)

Record the **actual BCs applied** (Dirichlet/Neumann/Robin/Periodic/Absorbing, etc.), per field/channel if applicable.

**Entry template (repeat):**

```markdown
##### <BC Name> for <Geometry ID>  <a id="bc-<slug>"></a>
**Context:** <path:lines> • <commit> • <module/subsystem>

**Field(s):** link to symbols (e.g., `SYMBOLS.md#sym-phi_c`)  
**Type:** Dirichlet | Neumann | Robin | Periodic | Absorbing | Other (as named in repo)  
**Definition (quote from source if formula exists):**
$$
% paste exact BC form as used (e.g., \phi|_{\partial\Omega_D}=\phi_0,\quad \partial_n \phi|_{\partial\Omega_N}=0 )
$$

**Applies on:** list boundary set(s) (e.g., $\partial\Omega_D$, faces $x=0,L_x$, “all sides periodic”)  
**Parameters:** link to constants (e.g., `CONSTANTS.md#const-phi0`)  
**Implemented at:** code locations enforcing the BC (all files/lines)  
**Notes:** aliases, channel-specific variants (lifted from repo text)
```

* If the repo states “periodic in $x$”, record that text and link the geometry; no formula needed.

---

#### 3) Initial Conditions

Record **all ICs actually used** to start simulations/experiments (fields, walkers, densities, scoreboard state).

**Entry template (repeat):**

```markdown
##### <IC Name>  <a id="ic-<slug>"></a>
**Context:** <path:lines> • <commit>

**Quantity:** link to symbol(s)  
**Definition (quote from source if formula exists):**
$$
% paste exact IC from repo, e.g., \phi(\mathbf{x},0)=\phi_{\text{seed}}(\mathbf{x})
$$

**Parameters:** link to constants (e.g., kernel width, amplitude)  
**Randomization/Seeds:** literal seed or file path if present  
**Applies to Geometry:** link to `#geom-...`  
**Notes:** brief usage hints lifted from comments/docs
```

* If IC is procedural (e.g., “sampled from KDE”): link to implementation and describe in one line (no re-derivation).

---

#### 4) Lattice/Stencil & Neighbor Topology (if referenced)

Only include if the repo explicitly names them (e.g., `$a$` spacing, `$\mathrm{nbr}(i)$`, $z$-coordination).

**Table schema:**

```markdown
| ID | Stencil/Topology | Description (as named) | Parameters (link) | Source | Notes |
|---|---|---|---|---|---|
```

---

### Linking rules (anchors only; no duplication)

* **Equations:** `../derivation/EQUATIONS.md#vdm-e-...`
* **Symbols:** `../derivation/SYMBOLS.md#sym-...`
* **Constants:** `../derivation/CONSTANTS.md#const-...`
* **Units maps:** `../derivation/UNITS_NORMALIZATION.md#...`

If any required anchor is missing, write `TODO: add anchor` with the exact `path:lines`; do not create new content here.

### Ordering

* Within each section, order entries by the repository path of the first cited source (lexicographic). Keep ordering stable across runs.

### End-of-file blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: BCIC-INDEX -->
<!-- Tool-maintained list of [Geometry](#geom-...), [BC](#bc-...), and [IC](#ic-...) anchors -->
<!-- END AUTOSECTION: BCIC-INDEX -->

## Change Log
- <date> • updated BC/IC/Geometry • <commit>
```

### Validation

* Render on GitHub preview; confirm MathJax and anchors render.
* No core field equations or constant values copied here—only BC/IC formulas and geometry definitions that appear in the repo, with links for everything else.
