# Test-driven “proposal” docs and reproducible “results” papers.

Here’s a tight, battle-ready shortlist plus how to bend each to your standards (floats locked down, `cleveref`, CSV/JSON artifacts, etc.).

## Proposal (≤5 pages, physics-literate audience)

* **NSF Proposal Sample (2023)** — sane structure, modern, tested with research.gov; easy to strip down to your 7 sections. ([Overleaf][1])
* **NSF Grant Proposal (MIT-MATH)** — clean, minimal preamble, good for single-PI whitepapers (just delete the NSF-isms you don’t need). ([Overleaf][2])
* **Project Proposal (generic)** — very light scaffolding when you want zero policy baggage. ([Overleaf][3])

Map your proposal sections straight onto any of the above:

* Title/date, proposers, abstract, background/rationale, setup & diagnostics, run plan, personnel, refs (your page cap is 5 pages total).
* Keep “intellectual merit” cues explicit (importance, impact, approach, rigor).

## Results papers (preprint → journal)

* **Basic Academic Journal Article** — Overleaf’s clean vanilla article; perfect for “results + gates + artifacts.” ([Overleaf][4])
* **Preprint style for arXiv/bioRxiv** — nice figure cross-refs, toggles for single/double column & line numbers; ideal for Zenodo/arXiv drops. ([Overleaf][5])
* **REVTeX 4.2 (APS/AIP)** — if you might aim at PRX/PRL/PhysRev later, start here to avoid a big refactor. ([Overleaf][6])
* **Elsevier (elsarticle)** and **Springer Nature** — official classes when targeting those ecosystems. ([Overleaf][7])

## Snap-in changes so these match your standards

Do this in whichever template you pick (proposal or results):

1. **Lock float behavior + section barriers**
   Add:

```tex
\usepackage[section]{placeins} % \FloatBarrier
\usepackage{float}             % [H] occasionally
```

Your rules require anchored floats and numeric captions with metrics.

2. **Citations/links & cross-refs**
   Add:

```tex
\usepackage{hyperref}
\usepackage[nameinlink,capitalize]{cleveref}
```

(You want `cleveref` hyperlinks like “Figure 1A” everywhere.)

3. **Units, math, small lemmas**
   Add:

```tex
\usepackage{siunitx,amsmath,amssymb,mathtools,amsthm}
```

Prove tiny lemmas in one line and box the derivative that equals zero; keep dissipative language to Onsager/entropy.

4. **Artifact pairing & contradiction reports**
   In your Methods/Results text, for every figure include its CSV/JSON basename and seed/commit; on any failed gate, include the contradiction report. (No special package—just disciplined writing and figure folder layout.)

5. **Runtime/scaling disclosures**
   Add a small table (P50/P95/P99, jitter, active-site fraction, slope β) and cite it in captions.

6. **Minimal, on-point background**
   Use a short “Scope & larger theory → core equations → gate map” block, then push anything longer to an Appendix.  

7. **Terminology discipline**
   Standard term first, then your label in parentheses; third-person tone.

## Quick start combos

* **Proposal**: start from **NSF Proposal Sample (2023)** → delete budget sections → drop in your 7 headings → enforce 5-page cap. ([Overleaf][1])
* **Results**: start from **Preprint style (arXiv)** → add `placeins`, `siunitx`, `cleveref` → use your caption metrics/CSV pairing policy. ([Overleaf][5])  

If you want, I can draft the minimal Overleaf preamble patch as a single `preamble_vdm.tex` you can paste into any template so your float policy, cross-refs, units, and lemma/box macros are identical across “proposal” and “results.”

[1]: https://www.overleaf.com/latex/templates/nsf-proposal-sample-2023/nxjjtpzzkrnd?utm_source=chatgpt.com "NSF Proposal Sample (2023)"
[2]: https://www.overleaf.com/latex/templates/nsf-grant-proposal-latex-template-mit-math/bpdgxygqdphw?utm_source=chatgpt.com "NSF Grant Proposal LaTeX Template (MIT-MATH)"
[3]: https://www.overleaf.com/latex/templates/project-proposal-template/whgtpdghprtb?utm_source=chatgpt.com "Project Proposal Template - Overleaf, Online LaTeX Editor"
[4]: https://www.overleaf.com/latex/templates/basic-academic-journal-article-template/hqyvzjmktytm?utm_source=chatgpt.com "Basic Academic Journal Article Template"
[5]: https://www.overleaf.com/latex/templates/style-and-template-for-preprints-arxiv-bio-arxiv/fxsnsrzpnvwc?utm_source=chatgpt.com "Style and Template for Preprints (arXiv, bio-arXiv)"
[6]: https://www.overleaf.com/latex/templates/revtex-4-dot-2-template-and-sample/yydsrzvrqrzs?utm_source=chatgpt.com "RevTeX 4.2 Template and Sample"
[7]: https://www.overleaf.com/latex/templates/elsevier-article-elsarticle-template/vdzfjgjbckgz?utm_source=chatgpt.com "Elsevier Article (elsarticle) Template"
