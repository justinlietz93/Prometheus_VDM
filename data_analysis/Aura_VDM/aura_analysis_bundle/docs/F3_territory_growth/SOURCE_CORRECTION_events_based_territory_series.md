# Source correction: territory series is in the events files

Direct extraction from the **events** artifacts (not UTD) gives these structural ranges immediately:

| file | tick range | rows | adc_territories | adc_boundaries | phase |
|---|---:|---:|---:|---:|---:|
| `20260222_145647_events_parsed.csv.gz` | `9343–10489` | `1147` | `9–9` | `0–0` | `4–4` |
| `20260222_165807_events_parsed.csv.gz (recoverable portion)` | `12441–12930` | `490` | `9–9` | `0–0` | `4–4` |
| `20260222_200818_events_parsed.csv` | `15537–15924` | `388` | `9–9` | `0–0` | `4–4` |


## Direct observations

- In every recoverable events segment above, `adc_territories` is **exactly 9 throughout**.
- In those same segments, `adc_boundaries` is **0 throughout**.
- The segments directly recovered here cover:
  - `9343–10489`
  - `12441–12930` (recoverable portion of the compressed middle file)
  - `15537–15924`

So the corrected statement is:

> the directly extracted **events** files already show the runtime deep inside a stable 9-territory regime across all recoverable structural segments inspected here.

This replaces the earlier curated-source note for the territory series.
