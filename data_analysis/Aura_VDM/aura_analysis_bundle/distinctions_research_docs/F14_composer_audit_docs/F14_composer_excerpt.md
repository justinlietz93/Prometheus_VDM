### D14.1 — Trigram Corpus Overlap Distribution
- **Claim:** Mean trigram overlap with corpus = 0.85, but **45 outputs (8.5%) share ZERO trigram sequences** with any source material. These are entirely novel multi-word compositions.
- **By epoch:** E1=8.4% zero, E2=7.0% zero, E3=**9.3%** zero. Novel outputs slightly increase in the late regime.
- **Source:** `F14_composer_audit.json` → D14_1_trigram

### D14.2 — LCS Fraction (Longest Common Substring)
- **Claim:** Mean LCS fraction = 0.157. **82.6% of outputs have <30% substring overlap** with any source.
- **Source:** `F14_composer_audit.json` → D14_2_lcs

### D14.3 — Best Jaccard Token Overlap
- **Claim:** Mean best Jaccard = 0.195. **93.6% of outputs have <30% word-level overlap** with ANY prior input in the entire run.
- **Source:** `F14_composer_audit.json` → D14_3_jaccard

### D14.4 — Immediate Input Decoupling
- **Claim:** Mean Jaccard between each output and its immediately preceding input = **0.038** (3.8%). Outputs share almost nothing with the last thing fed to the system.
- **Source:** `F14_composer_audit.json` → D14_4_immediate

### D14.5 — Within-Output Uniqueness
- **Claim:** Mean within-output unique word ratio = **0.860**. 86% of words in each output are unique — extremely low internal repetition.
- **Source:** `F14_composer_audit.json` → D14_5_uniqueness

### D14.6 — Self-Referential Structure at ~2.5 Hour Lag
- **Claim:** When outputs DO resemble prior outputs (TF-IDF similarity), the most similar past output is separated by a median of **3,687 ticks (~2.5 hours)**. The system's self-references reach far back in time, not to recent context.
- **Mean TF-IDF similarity to most-similar past output:** 0.254
- **Source:** `F14_composer_audit.json` → D14_6_self_ref

### D14.R — Repro summary for overlap / novelty metrics
- **Audited outputs:** 530
- **Zero trigram:** 45/530 = **8.5%**
- **LCS < 0.30:** 438/530 = **82.6%**
- **Best-all Jaccard < 0.30:** 496/530 = **93.6%**
- **Immediate-input Jaccard:** mean = **0.038**, median = 0.028
- **Within-output uniqueness:** mean = **0.860**, median = 0.857
- **Past-output linkage:** mean TF-IDF = **0.254**, median lag = **3687 ticks**
- **Repro artifacts:** `f14_composer_audit_analysis.py`, `f14_composer_audit_summary.csv`, `f14_composer_audit_quantiles.csv`, and the matching figures.

It is mentioned in the working notes that the encoder uses a cheap naive marker for temporal signal — it only marks temporal cues on unique symbols in a single input, so repeated symbols get skipped. And the decoder can't differentiate internal processing from intended output. That means the *raw outputs are a degraded signal* of a richer internal process. The composer audit metrics file likely contains evidence for how much richer. If we can show that the composer's internal state is more organized than what leaks through the decoder, that strengthens every other distinction — all the behavioral evidence is a *lower bound* on the substrate's actual organization.

