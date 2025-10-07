**Create/Update `derivation/CONSTANTS.md` (canonical constants & defaults, MathJax-only)**

Search the entire repository (code, tests, notebooks, configs, `.env`, CLI defaults, YAML/JSON, comments) and extract **all constants, default hyperparameters, kernel parameters, and fixed numerical values that are currently used by VDM**. **Do not invent or infer values.** Use only what exists in the repo.

**File:** `derivation/CONSTANTS.md`
**Canon rules:** This file is the single source of truth for constants. Other docs must link here; do not duplicate numbers elsewhere.

**MathJax on GitHub:** use `$...$` for inline math and `$$...$$` only if you must show a formula. No `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\tag`, or numbering.

**What counts as a “constant”:**

* Numeric defaults or fixed parameters used at runtime (e.g., diffusion coefficients, gains, caps, budgets, CFL factors, lattice spacings, sound speeds, kernel widths, thresholds).
* Values surfaced via config/CLI/env that have a default in code.
* Dimensionless reference values/ranges (e.g., recommended bands for KPIs) if they appear in repo text/config.
* Do **not** add derived equations here; just the values and their provenance.

**De-duplication policy:**

* One row per **unique constant name**. If the same constant appears in multiple files, keep one row and list all locations in **Source** (semicolon-separated).
* If multiple defaults exist for different modules, create separate rows with a scoped name like `name [module]`.

**Ordering:** sort rows by repository path of the first source (lexicographic). No custom categories.

**Top of file (insert verbatim):**

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Constants & Defaults (Auto-compiled)

**Scope:** Single source of truth for numerical constants, ranges, and defaults currently present in this repository.  
**Rules:** Other docs must link here; do not restate numbers elsewhere.  
**MathJax:** GitHub-safe `$...$` only (no equation environments or tags).  
```

**Table format (use exactly this header; append rows):**

```markdown
| Name | Meaning | Default/Value | Range/Limits | Units | Source (path:lines • commit) | Notes |
|---|---|---:|:---:|---|---|---|
```

**Row content guidance (formatting only, not content):**

* **Name:** use the project symbol or identifier. If it’s a mathematical symbol, write as `$ \alpha_{\mathrm{plast}} $`; if it’s a code identifier, use backticks (e.g., `BGK_TAU`). Add an HTML anchor: `<a id="const-alpha_plast"></a>` immediately before the row if helpful for linking.
* **Meaning:** 1 short phrase from nearby comments/docs.
* **Default/Value:** the literal numeric value as it appears (respect scientific notation). If computed from other constants at load time and there is no literal, leave blank and put the formula in **Notes**.
* **Range/Limits:** infer only from explicit code constraints (e.g., asserts, clamps, validator ranges) or documented bands; otherwise leave blank.
* **Units:** reference `derivation/UNITS_NORMALIZATION.md` terms (e.g., “LBM units”, “nondimensional”). Use MathJax for symbols if needed.
* **Source:** `path:line-start-line-end • <short-commit>`; include all occurrences if multiple apply.
* **Notes:** brief context like “applies per-channel $c$”, “budget per objective $k$”, or the literal formula if value is computed (MathJax allowed).

**End of file — append-only index block for tools:**

```markdown
<!-- BEGIN AUTOSECTION: CONSTANTS-INDEX -->
<!-- Tool-maintained list of [Name](#const-...) anchors -->
<!-- END AUTOSECTION: CONSTANTS-INDEX -->
```

**Validation:**

* Render the Markdown preview on GitHub; confirm all `$...$` inline math displays.
* Do not alter content outside this file; do not add or change values anywhere else in the repo.
* No speculative entries. If a symbol appears without a numeric value, add a row only if a concrete default/value exists; otherwise open a TODO in `SYMBOLS.md` instead of guessing.
