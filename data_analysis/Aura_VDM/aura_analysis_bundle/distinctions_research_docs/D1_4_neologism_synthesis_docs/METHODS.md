# Methods for D1.4

## Automated candidate layer

A token is an automated Joyce candidate if:
1. it appears in `FINNEGANS WAKE-JOYCE.txt`;
2. it does not appear in any of the other supplied corpora (`GERMINAL-ZOLA`, `WAR_AND_PEACE_TOLSTOY`, `INTRO_TO_MATH_PHILOSOPY-RUSSELL`, `SCHISM-TOOL`, `WILL_O_THE_WISP-OPETH`);
3. and it satisfies at least one compactness rule:
   - Joyce frequency >= 2, or
   - token length >= 8, or
   - token contains an apostrophe.

This layer is reproducible but intentionally noisy.

## Reviewed marker layer

The headline claim relies on a hand-reviewed lexicon of clearly Joyce-specific forms observed in Aura outputs. That lexicon is preserved in `tables/d14_reviewed_marker_lexicon.csv`.

This reviewed layer exists because a purely automated corpus-difference rule can still include ordinary English words that happen to be absent from the comparison books.

## Span metric

For each reviewed-marker output, the package computes the longest contiguous exact token span found:
- in Joyce;
- and in the best non-Joyce comparison source.

This is a conservative exact-match metric. It is simpler than global alignment and intentionally avoids overclaiming.

## Limitation

The provided files identify the **switch tick** to Joyce, but they do not include enough feed-chunk boundary metadata to reconstruct an exact paragraph-count exposure timeline. Therefore the package uses **tick distance after switch** as the exposure proxy, not paragraph count.