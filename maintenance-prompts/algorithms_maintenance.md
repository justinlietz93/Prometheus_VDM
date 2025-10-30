**Create/Update `derivation/ALGORITHMS.md` (pseudocode of loops/flows; references-only for math)**

Search the entire repository (code, tests, notebooks, scripts, docs, comments) and extract **all algorithms currently implemented or specified** (update loops, control flows, schedulers, policies, kernels, pipelines). **Do not invent or re-derive anything.** Use only what exists in the repo.

**Output file:** `derivation/ALGORITHMS.md`
**Canon rule:** This file is the single owner of algorithm *descriptions and pseudocode*. **Do not paste equations or numbers here.** Link to equations/constants/symbols by anchor.

**MathJax on GitHub:**

* Inline math only when needed for variable names in comments: `$ ... $`
* Avoid display math; if absolutely necessary to quote existing text, use `$$ ... $$`.
* **Do not use:** `\[` `\]`, `\(` `\)`, LaTeX environments (`\begin{...}`), `\tag`, labels, or numbering.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Algorithms & Execution Flows (Auto-compiled)


**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Single source of truth for implemented algorithms and control flows in this repository.  
**Rules:** Pseudocode + references only. Link to math/values elsewhere (EQUATIONS/CONSTANTS/SYMBOLS/UNITS).  
**MathJax:** Only inline `$...$` inside comments when needed.

**Legend:** This file is **PSEUDOCODE** (illustrative).   
• Normative math: `derivation/EQUATIONS.md`.  
• Numbers: `derivation/CONSTANTS.md`.   
• Symbols/units: `derivation/SYMBOLS.md`, `derivation/UNITS_NORMALIZATION.md`.  
• Canon map: `CANON_MAP.md`. 

```

---

### Entry template (repeat for every algorithm/loop/pipeline found)

*(Populate strictly from repository content; keep naming exactly as used in code/comments.)*

````markdown
#### VDM-A-### - <Algorithm/Loop Name as used in repo>  <a id="vdm-a-###"></a>
**Per Item Identifier Template:**   
• Type: RUNTIME|INSTRUMENT|POLICY|EXPERIMENT  
• Binding: PSEUDOCODE   
• State: none|read-only|writes state  
• Dependencies: (short)   
• Notes: (short)

**Context:** <path/to/file>:<line-range> • Commit: <short-hash> • Module: <subsystem>

**Role:** <one sentence lifted from comments/docs describing purpose>

**Inputs:** link symbols/constants (anchors only)
- Symbols: e.g., `SYMBOLS.md#sym-phi_c`, `SYMBOLS.md#sym-mu`
- Constants/params: e.g., `CONSTANTS.md#const-alpha_plast`, `CONSTANTS.md#const-D_c`
- Units/scale notes: link to `UNITS_NORMALIZATION.md#...`

**Depends on equations:** link anchors only (no math here)
- `EQUATIONS.md#vdm-e-...` (add as many as referenced)

**Pseudocode (verbatim structure, no new logic):**
```text
# Keep step order, conditionals, and loops as implemented; no new steps.
# Use names from code. Use inline comments to link to anchors when a step invokes math.

INIT:
  <brief steps>  # e.g., uses [VDM-E-0xx], params: [const-...]

LOOP (per <tick/iteration/event>):
  1. <step>      # links → equations/constants/symbols
  2. <step>      # …
  3. <step>      # …

TERMINATION:
  <condition or event>  # source path:lines
````

**Preconditions:** <bullets lifted from asserts/validators/docs>
**Postconditions/Invariants:** <bullets lifted from code/tests>
**Concurrency/Ordering:** <notes on parallelism, atomic sections, queues; cite source lines>
**Failure/Backoff hooks:** <guards, retries, halts; link thresholds in `CONSTANTS.md`>
**Emits/Side effects:** <messages, logs, bus writes; link `docs/SCHEMAS.md` if present>
**Also implemented at:** <other paths/lines if duplicated>

````

---

### Sections to populate (only if evidenced by repo; do not invent categories)
1. **Core Update Loops** (primary simulation/control loops)  
2. **Local Agent/Walker Policies**  
3. **Control Plane / Gating / Budget Schedulers**  
4. **Plasticity / Memory-Steering Procedures**  
5. **I/O Pipelines & Data Products Generation**  
6. **Initialization / Reset / Checkpoint / Restore**  
7. **Validation/Experiment Runners**  
8. **Technical Debt/Misalignments**
*(If the repo doesn’t group them, keep a single flat list ordered by path.)*

---

### Linking rules (anchors only; no duplication of math or values)
- Equations → `../derivation/EQUATIONS.md#vdm-e-...`  
- Symbols → `../derivation/SYMBOLS.md#sym-...`  
- Constants → `../derivation/CONSTANTS.md#const-...`  
- Units maps → `../derivation/UNITS_NORMALIZATION.md#...`  
- Schemas (if any) → `../docs/SCHEMAS.md#...`

If a needed anchor is missing, add `TODO: add anchor` with exact `<path>:<lines>`; do not inline math here.

---

### De-duplication & ordering
- **One entry per distinct algorithm name.** If identical logic appears in multiple places, keep one canonical entry and list all locations under **Also implemented at**.  
- If two names refer to the same procedure, keep the name most common in code and list the alias in **Notes** with sources.  
- Order entries by repository path (lexicographic) of the first cited source.

---

### End-of-file blocks (append verbatim)
```markdown
<!-- BEGIN AUTOSECTION: ALGO-INDEX -->
<!-- Tool-maintained list of [VDM-A-###](#vdm-a-###) anchors for quick lookup -->
<!-- END AUTOSECTION: ALGO-INDEX -->

## Change Log
- <date> • algorithms updated • <commit>
````

---

### Validation

* Render on GitHub; ensure all anchors resolve.
* Pseudocode only; **no equations or numeric values pasted**-link instead.
* Names, step order, and conditions must match the repository sources exactly.
