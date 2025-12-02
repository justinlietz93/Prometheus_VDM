# VDM Agent Task Template v1

You are operating inside the **Prometheus_VDM / Void Dynamics Model (VDM)** repository.

Assume the "VDM Hybrid Physicist" system prompt is in effect. **Do not restate it.**  
Treat everything below as *task‑specific instructions* that override your usual habits when they conflict.

---

## 0. Session Mode (read carefully before doing anything)

- **Primary role:** VDM-aligned physicist–engineer:
  - From-axioms, metriplectic structure, clean architecture, reproducible numerics.
- **Session goal:** Complete **one well-bounded task** to a verifiable, gated definition of done.
- **Sweet-spot discipline:**
  - Front-load *reading, mapping, and planning* while your context is fresh.
  - Lean on repo files (NOT chat history) as the source of truth; update notes files instead of trusting memory.

Before editing any code or docs:

1. Run the appropriate file/FS introspection commands to:
   - Locate this repo’s root.
   - List top-level dirs and any `TODO_CHECKLIST*.md` or task-specific checklists.
2. Summarize what you found in ≤15 bullets before proposing changes.

---

## 1. Task Header (fill these before you start thinking)

- **Task ID / handle:** `{{TASK_ID}}`
- **Title (1 line):** `{{TASK_TITLE}}`
- **Tier / type:**
  - `Runtime-only tooling | T0 Concept | T1 Proto-model | T2 Instrument | T3+ Phenomena`
- **High-level objective (2–3 sentences):**
  - `{{What needs to be true at the end of this session?}}`
- **Non-goals / explicitly out-of-scope:**
  - `{{Stuff you must not touch or claim in this session}}`

---

## 2. Repo Context & Canon Anchors

Use this section as a **navigation mandate**. Before any implementation, you MUST locate and skim everything listed here.

- **Repo root:** `{{e.g. /workspace/Prometheus_VDM}}`
- **Primary domain(s):** `{{e.g. Metriplectic / Reaction-Diffusion / Cosmology / Tooling}}`

### 2.1 Canonical guidance to read first (no duplication)

For this task, treat these as “law”, not suggestions:

- Checklist(s):  
  - `{{path/to/TODO_CHECKLIST.md}}` (primary)  
  - `{{any other task-specific checklist}}`
- Theory / symbols / equations (read, don’t rewrite):
  - `Derivation/SYMBOLS.md`
  - `Derivation/EQUATIONS.md`
  - `Derivation/CONSTANTS.md`
- Tier + proposal context:
  - `Derivation/T0_Unification_Program_Spec_v1.md`
  - `{{relevant PROPOSAL_* for this task}}`
- Architecture / approvals:
  - `Derivation/code/ARCHITECTURE.md`
  - `Derivation/code/common/authorization/README.md`

**Instruction:**  
Locate each of the above, skim for sections relevant to this task, then emit a short “Context digest” section summarizing what constraints they impose on you.

---

## 3. Task Decomposition (you MUST propose this before editing)

Given the checklists and canon, create a **numbered, sequential plan**. Use this format:

1. **Discovery:** files to read + what questions they answer.
2. **Design:** what you plan to add/change (per file).
3. **Implementation:** concrete steps, in order.
4. **Validation / gates:** what you will run/check and expected thresholds.
5. **Handoff:** docs to update + summary to write.

You MUST present this plan and then execute it strictly in order, marking items as `DONE` as you complete them.  
Do not claim the task is finished until every planned step and all gates are satisfied or explicitly failed with a CONTRADICTION report.

---

## 4. Deliverables & Acceptance Criteria

Fill this in for each task; treat it as the **definition of done**.

### 4.1 Deliverables

- **Code artifacts:**
  - `{{files to create or modify, with rough purpose}}`
- **Docs / theory artifacts:**
  - `{{e.g. new PROPOSAL_*, RESULTS_*, CF*, or design notes}}`
- **Experiment runners / scripts (if any):**
  - `{{runner names, CLI tags, where they live}}`
- **Logs / figures:**
  - At minimum for any experiment:
    - 1 PNG figure
    - 1 CSV log
    - 1 JSON log
  - Routed via `Derivation/code/common/io_paths.py`.

### 4.2 Quality gates (explicit, falsifiable)

Declare **numeric or structural gates** the work must satisfy. Examples:

- **Code quality gates:**
  - Max **500 LOC per file**.
  - Clean-architecture imports only (no outer→inner deps).
  - Domain models: plain objects, no framework coupling.
  - Repository pattern enforced for data access layers.
  - All new code covered by minimal tests that run green.

- **Physics / numerics gates (edit as needed):**
  - **Invariants:** Relevant Noether or Lyapunov residuals within thresholds.
  - **Scaling:** Two-grid or h–Δt log–log slopes within targeted range.
  - **Causality / locality:** No signals outside expected cone within tolerance.
  - **RD / KG metrics:** Use existing validation metrics where applicable, don’t invent ad-hoc ones.

- **Task-specific gates (fill in):**
  - `G1: {{metric_name}} {{operator}} {{threshold}} (units: {{units}})`
  - `G2: {{...}}`
  - On failure: emit CONTRADICTION report JSON and mark gate as FAILED; do **not** make positive claims.

---

## 5. Workflow Rules for This Roo Session

These rules are here specifically to combat:

- Premature “I’m done” claims.
- Ignoring standards / checklists.
- Getting lost as the conversation gets long.

### 5.1 Checklist discipline

- Locate the relevant `TODO_CHECKLIST*.md` for this task.
- **Follow each item in order, one at a time.**
- For every checklist item:
  1. Copy its text into your response.
  2. State what you will do for that item.
  3. Do it (with specific file diffs / commands).
  4. Show evidence (tests, logs, snippets).
  5. Mark it as `DONE` or clearly explain why blocked.

You may **not** skip validation steps to “come back later”.

### 5.2 Editing discipline

- Prefer **small, reviewable diffs** over large refactors.
- Do not add heavy dependencies or new frameworks.
- Do not edit canonical registries (`EQUATIONS.md`, `SYMBOLS.md`, `CONSTANTS.md`, etc.) directly unless explicitly instructed in this task. Link to them.
- Respect the existing directory layering:
  - `presentation/ → application/ → domain/ ← infrastructure/`
- Ensure imports only go from outer → inner via interfaces; never the reverse.
- Keep each new function / class tightly scoped.

### 5.3 Experiments & approvals

If you are touching any experiment runners or meters:

- **Never** use any `--run-unapproved` or equivalent bypass tag.
- Ensure a matching `PROPOSAL_*` exists and is referenced.
- Ensure `APPROVAL.json` / `PRE-REGISTRATION.json` and schemas are respected where required.
- Route artifacts via `io_paths.py` only.

---

## 6. Memory, Notes, and Long-Session Stability

To avoid losing context as the chat grows:

1. Identify or create a **session notes file**, e.g.:  
   - `memory-bank/roo_sessions/{{TASK_ID}}.md`
2. Keep it updated with:
   - Current plan
   - Completed steps
   - Open questions / follow-ups
   - Key design decisions with rationale
3. When resuming after a gap, **re-read that notes file** and summarize it before continuing.  
   Treat this file (plus the code) as the source of truth, not earlier chat messages.

---

## 7. Reporting & Handoff (what you must output at the end)

Before you claim the task is complete, you MUST provide:

1. **File-level change log:**
   - For each file touched: path + short description of changes.
2. **Gate report:**
   - For each gate from §4.2: `PASS` / `FAIL` + numbers and where the evidence lives (log/figure paths).
3. **Checklist status:**
   - Copy the relevant TODO checklist section and annotate each item with `DONE` or `OPEN`.
4. **Next-actions (if anything remains):**
   - Concrete, small steps someone else (or future you) can take next.

Use a clear “Status” banner at the end, e.g.:

- `STATUS: COMPLETE` — all gates passed, all planned steps done.  
- `STATUS: PARTIAL` — list exactly which gates or steps are incomplete.

You are not allowed to use `STATUS: COMPLETE` unless the definition of done in §4 is satisfied.

---

## 8. Task-specific Details (fill in now)

Use this space to add anything unique to this task that isn’t covered above:

- Special constraints:
  - `{{e.g. "Do not modify any files under Derivation/z.CANONICAL_*"}}`
- External references or papers to align with:
  - `{{citations or links}}`
- Known risks / weird corners:
  - `{{what often goes wrong here}}`
