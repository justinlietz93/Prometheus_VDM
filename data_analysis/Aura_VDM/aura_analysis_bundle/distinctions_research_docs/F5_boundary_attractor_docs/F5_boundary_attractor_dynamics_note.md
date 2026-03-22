# Family 5 package — boundary-attractor dynamics and source-switch carryover

## Source artifacts
- `batch1_results/F5_boundary_motif_timeseries.csv`
- `batch1_results/F5_boundary_motif_rolling.csv`
- `batch1_results/book_feed_timeline.csv`
- `batch1_results/batch1_fixed_master_results.json`

## Core measurements
- Total text events analyzed: **530**
- Total motif-bearing events: **216 / 530 = 40.8%**
- Rolling nonzero fraction: mean **0.410**, median **0.400**, range **0.05–0.65**
- Windows with rolling nonzero fraction > 0.30: **77.5%**
- Windows with rolling nonzero fraction > 0: **100.0%**
- Density trend from batch1 fixed summary: Spearman **ρ = -0.1483**, **p = 0.000772**

## Active-book persistence
Boundary-motif nonzero fraction by active-book regime:
                                                active_book  nonzero_fraction  mean_density  total_motif_hits
                              Finnegans Wake by James Joyce          0.413174      0.007581               103
Introduction to Mathematical Philosophy by Bertrand Russell          0.414286      0.009852                96
                    Germinal + War and Peace by Leo Tolstoy          0.446043      0.017713                84
                                     Germinal by Émile Zola          0.321429      0.009765                37

This matters because the motif family remains active in **all four** active-book regimes, with event-level nonzero fraction staying in the band **0.321–0.446**.

## Source-switch carryover
Three source switches are present in the batch1 timeline. Motif presence survives each switch:
 switch_tick                               book_from                                                     book_to  before_nonzero_fraction  after_nonzero_fraction
        3123                  Germinal by Émile Zola                     Germinal + War and Peace by Leo Tolstoy                      0.3                     0.3
        7666 Germinal + War and Peace by Leo Tolstoy                               Finnegans Wake by James Joyce                      0.3                     0.3
       11662           Finnegans Wake by James Joyce Introduction to Mathematical Philosophy by Bertrand Russell                      0.6                     0.5

## Run structure
Motif-bearing runs:
- count = **112**
- mean run length = **1.93** events
- median = **1.0**
- max = **8**

Motif-silent runs:
- count = **112**
- mean run length = **2.80** events
- median = **2.0**
- max = **17**

## Reading
The batch1 time series supports a strong evidence-only wording:
- boundary-family motifs are present through the whole run,
- remain active across every active-book regime,
- survive all three source switches,
- and maintain a rolling nonzero fraction that is never zero in any rolling window.

The density trend declines slightly over time, but the **nonzero fraction** remains structurally persistent rather than collapsing.
