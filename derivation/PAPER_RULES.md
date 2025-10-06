# Terminology & Framing

* **Never introduce custom terminology before defining it.** Give the standard term first, then your label in parentheses.
* **Always define key words once, plainly.** E.g., “training = offline parameter optimization; here we do online adaptation.”
* **Prefer mainstream language over in-house metaphors.** Map “walkers (tracer probes)”, “scoreboard (budgeted gate)”, “memory steering (slow bias field).”
* **State scope in the first paragraph.** Say what the note *does* and *does not* claim.

# Claims & Novelty

* **Never imply novelty for classical results.** If it’s known, say “we reuse X as a QC invariant.”
* **Always separate architecture from kernels.** Your system is new; the math blocks can be standard.
* **Make each claim falsifiable.** Attach a metric, a threshold, and a pass/fail outcome.

# Math & Invariants

* **Prove tiny lemmas in one line when possible.** Box the derivative that equals zero.
* **Never mix dissipative RD with “least action” language.** Use “gradient flow / entropy increase / Onsager.”
* **Use dimensionless groups early.** Declare rescalings and drop tildes cleanly.

# Evidence & Reproducibility

* **Always pair every figure with its CSV/JSON.** Same folder, same basename.
* **Emit a contradiction report on failure.** Include gate name, seed, and cell pointer.
* **Pin one artifact path in the text.** Readers need a single click target to the proof.

# Runtime & Scaling

* **Never claim scaling without a log–log slope.** Report β ± CI for step-time vs active sites.
* **Always report P50/P95/P99 latency and jitter.** Show stability over hours.
* **Quantify “no dense scans.”** Log fraction of cells touched per tick; enforce a budget.

# Citations & Prior Art

* **Cite lineage at first use.** Logistic → Verhulst; fronts → Fisher–KPP; gradient flow → Onsager/JKO/AGS; RD patterns → Turing/Murray.
* **Keep related work minimal but present.** Four bullets beat zero citations.
* **Never bury citations in an appendix.** Put them where skepticism arises.

# Naming & Jargon

* **Focus on clarity and masterful communication over convoluted complexity.**
* **Avoid anthropomorphism.** Replace “wants to output” with “emits when threshold crossed.”
* **Explain metaphors or drop them.** If you say “particle-like,” back it with lifetime/velocity/dispersion metrics.

# Figures & LaTeX/Notebooks

* **Never let floats roam.** Use `[!htbp]` and `\FloatBarrier` (or `[H]` sparingly).
* **Caption with numbers, not vibes.** Include R², slope, RMSE right in the caption.
* **One figure = one claim.** Don’t overload panels with multiple unlinked points.

# Thread/Etiquette (r/LLMPhysics survival)

* **Lead with a test, not a thesis.** “Here’s the gate; here’s the artifact path.”
* **Don’t debate venues; debate thresholds.** Invite tighter gates, not opinions.
* **Never reply defensively.** One factual clarification; then point to the artifact.

# Scope & Boundaries

* **State what is *not* in scope.** E.g., “No claim about novelty of logistic; this note is QC-only.”
* **Distinguish adaptation from training in one line.** Then don’t re-litigate it.
* **Avoid sweeping generalizations.** Keep statements bounded by your artifacts.

# Security/Integrity

* **Log seeds, commits, and environment.** Provenance kills plagiarism accusations.
* **Disclose assistance roles.** “Equations expressed in standard RD form; architecture and tests specified by author.”
* **Never fabricate certainty.** “PROVEN” only after gates pass and artifacts exist.

# Posting Flow (do this every time)

* **Open with TL;DR + one artifact path.** Then details.
* **Include a boxed lemma or boxed gate.** Visual anchors calm skeptics.
* **End with a single invitation.** “Propose a tighter threshold; I’ll run and post the result.”

# Preflight Checklist (print this)

* Title reflects purpose (QC/architecture), not novelty.
* Plain-language definitions appear before any custom names.
* Lemma/proof for any invariant in ≤3 lines.
* Each figure has CSV/JSON + seed + commit.
* Gates: names, thresholds, pass/fail JSON, contradiction report.
* Minimal citations added at first skeptical touchpoints.
* Runtime claims include β slope, P50/95/99, jitter, active-site fraction.
* No anthropomorphism; metaphors quantified or removed.
* Floats anchored; captions numeric.
* OP text leads with artifact path; replies focus on thresholds.

Stick to these and you won’t get blindsided by “made-up jargon” or “unmotivated equations” again; the conversation will be forced onto your tests and artifacts where you’re strongest.

