**Create/Update `derivation/SCHEMAS.md` (canonical structured schemas; references-only for math/values)**

Search the entire repository (code, tests, notebooks, scripts, configs, docs, comments) and compile **all structured schemas that actually exist** (messages, packets, records, state snapshots, configs, API/event payloads, file formats). **Do not invent or infer fields.** Use only what appears in the repo.

**Output file:** `derivation/SCHEMAS.md`
**Canon rule:** This file is the single owner of schema specifications. Other docs must link here. **Do not restate equations or numeric defaults**—link to anchors in the canonical files.

**MathJax on GitHub:**

* Inline only for symbol names in prose: `$ ... $`
* **No** display math or LaTeX environments here. Put formulas in `EQUATIONS.md` and link.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Schemas (Auto-compiled)

**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Single source of truth for message/record/state/config schemas used in this repository.  
**Rules:** Paste schema definitions from source; document fields. Link to equations/constants/symbols/units/algorithms.  
**MathJax:** Inline `$...$` only in descriptions (no display math or LaTeX environments).
```

---

### Schema entry template (repeat for every schema you find)

*(Populate strictly from repository content; keep names exactly as used in code/comments.)*

````markdown
#### <Schema Name as used in repo>  <a id="schema-<slug>"></a>
**Kind:** <message | record | state | config | API | event | file | other>  
**Versioning (if present):** <field name / semver / migration note>  
**Defined at:** `<path/to/file>:<line-range> • <short-commit>` (list all canonical sources)

**Definition (verbatim snippet from source):**
```<language>  <!-- e.g., json, yaml, python, protobuf, typescript, toml -->
<exact schema/model/typedef excerpt>
````

**Fields (expand from source; do not invent):**

| Field    | Type     | Required | Default             | Units/Normalization                        | Description (lifted)        | Source         |
| -------- | -------- | :------: | ------------------- | ------------------------------------------ | --------------------------- | -------------- |
| `<name>` | `<type>` |  `<Y/N>` | `<literal or link>` | link `UNITS_NORMALIZATION.md#...` or `n/a` | one line from comments/docs | `<path:lines>` |

**Producers/Consumers:** link algorithms that write/read this schema → `../derivation/ALGORITHMS.md#vdm-a-###`
**Related equations (anchors only):** `../derivation/EQUATIONS.md#vdm-e-###` (if schema fields are mathematically constrained; do not paste math)
**Related symbols/constants:** `../derivation/SYMBOLS.md#sym-...`, `../derivation/CONSTANTS.md#const-...`
**Examples (if present):** `<path/to/example artifact or test fixture>`
**Invariants/Validation rules:** copy literal constraints from asserts/validators/JSON-Schema/Pydantic (regex, ranges, enums). Link to constants for thresholds.
**Notes:** aliases, deprecations, migration guidance (lifted from repo)

````

---

### Sections to populate (only if evidenced by the repo; omit if empty)
1. **Buses & Messages** (e.g., bus packets, walker messages, scoreboard updates)  
2. **State Snapshots & Checkpoints** (substrate/graph/scoreboard/agents)  
3. **Diagnostics & Logs** (KPI traces, drift monitors, metric rows)  
4. **Configs & CLI/ENV** (runtime/config files and structured CLI schemas)  
5. **External Interfaces** (HTTP/gRPC/IPC payloads, import/export file specs)

*(If the repo doesn’t group them this way, keep a single flat list ordered by path.)*

---

### Linking rules (anchors only; no duplication)
- Equations → `../derivation/EQUATIONS.md#vdm-e-...`  
- Symbols → `../derivation/SYMBOLS.md#sym-...`  
- Constants → `../derivation/CONSTANTS.md#const-...`  
- Units → `../derivation/UNITS_NORMALIZATION.md#...`  
- Algorithms → `../derivation/ALGORITHMS.md#vdm-a-...`  
- Data products (if schema describes a stored artifact) → `../derivation/DATA_PRODUCTS.md#data-...`

If an expected anchor is missing, add: `TODO: missing anchor (see <path>:<line>)`; do not create content here.

---

### De-duplication & ordering
- **One entry per distinct schema name.** If identical schemas appear in multiple files, keep one canonical entry and list all locations in **Defined at**.  
- If two names describe the **same schema**, keep the most common name and list the alias in **Notes** with sources.  
- Order entries by repository path (lexicographic) of the first cited source.

---

### End-of-file blocks (append verbatim)
```markdown
<!-- BEGIN AUTOSECTION: SCHEMAS-INDEX -->
<!-- Tool-maintained list of [Schema](#schema-...) anchors for quick lookup -->
<!-- END AUTOSECTION: SCHEMAS-INDEX -->

## Change Log
- <date> • schemas updated • <commit>
````

---

### Validation

* Render on GitHub; ensure anchors resolve and code snippets are fenced with the correct language.
* Do not paste formulas or numeric defaults here—**link** to canonical files.
* Field tables must match the source definitions exactly (names, types, required/optional, defaults, constraints).
