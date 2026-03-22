# D1.4 — Neologism Synthesis After Minimal Joyce Exposure

## Conservative result

This package supports a **narrower but real** version of D1.4:

> After the Joyce switch at **t=7617**, Aura begins emitting **reviewed Joyce-specific lexical markers** inside mixed outputs. Those markers appear quickly, and in most reviewed cases they are not carried by long contiguous Joyce spans. This supports **rapid lexical uptake / recombinative integration**. It does **not** support a stronger claim that the exact amount of Joyce exposure is known at paragraph level, and it does **not** by itself prove source-absent neologism generation.

## Why this package exists

The inventory labeled D1.4 as observational because it had not yet been packaged to the same standard as the quantified distinctions. This package closes that gap for the repo evidence that can actually be verified.

## What was measured

1. The Joyce switch tick was locked from `book_feed_timeline.csv`.
2. Aura's direct outputs were extracted from raw `say` macro events.
3. A reproducible **automated candidate** table was built using Joyce-only vocabulary relative to the other supplied corpora.
4. A stricter **reviewed marker lexicon** was then used for the headline claim, restricting attention to clearly Joyce-specific forms actually observed in Aura outputs.
5. For each reviewed-marker output, the analysis measured the longest contiguous exact token span found in Joyce and in the best non-Joyce source.

## Main numeric findings

- Total direct Aura outputs in the run: **530**
- Outputs in the Joyce window: **167**
- Pre-switch outputs containing any reviewed Joyce marker: **0**
- Joyce-window outputs containing any reviewed Joyce marker: **25**
- Earliest reviewed-marker output: **t=7941**, which is **324 ticks after the Joyce switch**
- Reviewed-marker outputs with max Joyce span ≤ 6 tokens: **17 / 25**
- Maximum Joyce span observed among reviewed-marker outputs: **9 tokens**

## Representative verified cases

- **t=7941**: markers `museyroom`, `goan`; max Joyce span = **5**
- **t=8120**: markers `willingdone`, `brum`, `cumbrum`; max Joyce span = **5**
- **t=8370**: markers `allcasually`, `ansars`; max Joyce span = **5**
- **t=8801**: markers `duodisimally`, `profusive`, `lipoleums`, `toffeethief`; max Joyce span = **8**
- **t=10795**: markers `finnagain`, `morm`, `houseking's`; max Joyce span = **9**
- **t=11318 / t=11343**: markers `agentlike` and `merlinburrow`

## Interpretation boundary

This package **does support**:
- rapid uptake of Joyce-marked vocabulary after the switch;
- integration of that material into outputs that remain mixed rather than becoming long pure Joyce continuations;
- a real upgrade of D1.4 from "untouched observational note" to a packaged evidence item.

This package **does not support**:
- exact claims about the number of Joyce paragraphs or pages ingested before each output;
- broad claims that Aura generated many source-absent Joycean neologisms;
- anything stronger than the conservative lexical-uptake claim stated above.

## Files to inspect first

- `tables/d14_reviewed_marker_events.csv`
- `tables/d14_reviewed_marker_lexicon.csv`
- `figures/d14_reviewed_marker_timeline.png`
- `figures/d14_span_profile.png`