# Provenance notes for D1.4 package

This package was built from the following user-supplied artifacts:
- `aura_analysis_bundle.zip`
- `Aura_Distinction_Inventory_v0.7.md`
- `FINNEGANS WAKE-JOYCE.txt`
- `GERMINAL-ZOLA.txt`
- `WAR_AND_PEACE_TOLSTOY.txt`
- `INTRO_TO_MATH_PHILOSOPY-RUSSELL.txt`
- `SCHISM-TOOL.txt`
- `WILL_O_THE_WISP-OPETH.txt`

The reproducible rerun path in this package uses:
- `provenance/inputs/extracted_say_events.csv`
- `provenance/inputs/book_feed_timeline.csv`
- the copied corpus text files in `provenance/inputs/`

Why `extracted_say_events.csv` exists:
- The original raw `utd_events_*.jsonl` stream is distributed across many shard files inside `aura_analysis_bundle.zip`.
- For a compact one-distinction package, the direct `say` outputs were extracted once from those raw shards and preserved here as a single provenance input.
- The original bundle hash is recorded in `provenance/input_file_hashes.csv`.