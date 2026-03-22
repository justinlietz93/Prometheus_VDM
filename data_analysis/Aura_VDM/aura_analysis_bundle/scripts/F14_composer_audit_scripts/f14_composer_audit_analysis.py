#!/usr/bin/env python3
from pathlib import Path
import zipfile, io, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path('/mnt/data/aura_research_deliverables')
ZIP_PATH = Path('/mnt/data/aura_analysis_bundle.zip')
for sub in ['tables','figures','docs','patches']:
    (ROOT/sub).mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(ZIP_PATH) as zf:
    audit = pd.read_csv(io.BytesIO(zf.read('aura_analysis_bundle/utd_audit/tables/say_event_composer_audit_metrics.csv')))

audit['within_output_uniqueness'] = audit['say_unique_tokens'] / audit['say_len_tokens']
summary = {
    'n_outputs': int(len(audit)),
    'zero_trigram_count': int((audit['tri_frac_in_corpus'] == 0).sum()),
    'zero_trigram_fraction': float((audit['tri_frac_in_corpus'] == 0).mean()),
    'lcs_lt_0_30_count': int((audit['lcs_frac_say'] < 0.30).sum()),
    'lcs_lt_0_30_fraction': float((audit['lcs_frac_say'] < 0.30).mean()),
    'best_jaccard_lt_0_30_count': int((audit['best_all_jaccard'] < 0.30).sum()),
    'best_jaccard_lt_0_30_fraction': float((audit['best_all_jaccard'] < 0.30).mean()),
    'imm_jaccard_mean': float(audit['imm_jaccard'].mean()),
    'imm_jaccard_median': float(audit['imm_jaccard'].median()),
    'uniqueness_mean': float(audit['within_output_uniqueness'].mean()),
    'uniqueness_median': float(audit['within_output_uniqueness'].median()),
    'past_tfidf_top1_sim_mean': float(audit['past_tfidf_top1_sim'].mean()),
    'past_tfidf_top1_sim_median': float(audit['past_tfidf_top1_sim'].median()),
    'past_tfidf_top1_lag_median': float(audit['past_tfidf_top1_lag'].median()),
    'past_tfidf_top1_lag_mean': float(audit['past_tfidf_top1_lag'].mean()),
}
summary_df = pd.DataFrame([summary])
summary_df.to_csv(ROOT/'tables/f14_composer_audit_summary.csv', index=False)

quantiles = pd.DataFrame({
    'metric': ['tri_frac_in_corpus','lcs_frac_say','best_all_jaccard','imm_jaccard','within_output_uniqueness','past_tfidf_top1_sim','past_tfidf_top1_lag'],
    'q05': [audit[c].quantile(0.05) for c in ['tri_frac_in_corpus','lcs_frac_say','best_all_jaccard','imm_jaccard','within_output_uniqueness','past_tfidf_top1_sim','past_tfidf_top1_lag']],
    'q25': [audit[c].quantile(0.25) for c in ['tri_frac_in_corpus','lcs_frac_say','best_all_jaccard','imm_jaccard','within_output_uniqueness','past_tfidf_top1_sim','past_tfidf_top1_lag']],
    'q50': [audit[c].quantile(0.50) for c in ['tri_frac_in_corpus','lcs_frac_say','best_all_jaccard','imm_jaccard','within_output_uniqueness','past_tfidf_top1_sim','past_tfidf_top1_lag']],
    'q75': [audit[c].quantile(0.75) for c in ['tri_frac_in_corpus','lcs_frac_say','best_all_jaccard','imm_jaccard','within_output_uniqueness','past_tfidf_top1_sim','past_tfidf_top1_lag']],
    'q95': [audit[c].quantile(0.95) for c in ['tri_frac_in_corpus','lcs_frac_say','best_all_jaccard','imm_jaccard','within_output_uniqueness','past_tfidf_top1_sim','past_tfidf_top1_lag']],
})
quantiles.to_csv(ROOT/'tables/f14_composer_audit_quantiles.csv', index=False)

# examples tables
zero_trigram_examples = audit[audit['tri_frac_in_corpus'] == 0].sort_values('t').head(25)
low_immediate_examples = audit.sort_values(['imm_jaccard','best_all_jaccard','t']).head(25)
zero_trigram_examples.to_csv(ROOT/'tables/f14_zero_trigram_examples.csv', index=False)
low_immediate_examples.to_csv(ROOT/'tables/f14_low_immediate_overlap_examples.csv', index=False)

# figures
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
axes = axes.ravel()
axes[0].hist(audit['tri_frac_in_corpus'], bins=30)
axes[0].set_title('Trigram corpus overlap')
axes[1].hist(audit['lcs_frac_say'], bins=30)
axes[1].set_title('LCS fraction vs best source')
axes[2].hist(audit['best_all_jaccard'], bins=30)
axes[2].set_title('Best-all Jaccard overlap')
axes[3].hist(audit['imm_jaccard'], bins=30)
axes[3].set_title('Immediate input Jaccard')
fig.tight_layout()
fig.savefig(ROOT/'figures/f14_overlap_distributions.png', dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8,4.5))
labels = ['zero trigram','LCS<0.30','best Jaccard<0.30']
vals = [summary['zero_trigram_fraction'], summary['lcs_lt_0_30_fraction'], summary['best_jaccard_lt_0_30_fraction']]
ax.bar(labels, vals)
ax.set_ylim(0,1)
ax.set_ylabel('Fraction of outputs')
ax.set_title('F14 — novelty / overlap thresholds')
fig.tight_layout()
fig.savefig(ROOT/'figures/f14_threshold_summary.png', dpi=180)
plt.close(fig)

(ROOT/'docs/F14_results.json').write_text(json.dumps(summary, indent=2))
print('F14 outputs written.')
