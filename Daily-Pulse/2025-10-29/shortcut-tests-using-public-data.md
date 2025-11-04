Here are a couple of high‑priority project ideas I found **for you**, with notes on feasibility, sources, gaps, and caveats — you may already have some of this, but I thought it helpful to map the terrain.

---

## 1) Rain‑/storm‑echo in taxi‑zone pickup rates (via New York City Taxi & Limousine Commission (TLC) data)

![Image](https://www.nyc.gov/assets/tlc/images/content/pages/about/taxi_zone_map_brooklyn.jpg)

![Image](https://www.researchgate.net/publication/374423317/figure/fig3/AS%3A11431281252190661%401718628593426/The-map-and-structure-of-the-NYC-taxi-zone.jpg)

![Image](https://www.researchgate.net/publication/335847885/figure/fig4/AS%3A11431281432245389%401746848309860/Heat-maps-of-NYC-Yellow-Taxi-Data-in-Manhattan-a-Heat-map-at-900-of-one-day-b-Heat_Q320.jpg)

![Image](https://miro.medium.com/1%2ABdeM6CWTpgmbtDWE4V5gzg.jpeg)

![Image](https://www.weather.gov/images/okx/Virtual%20Tour/blizz06.PNG)

![Image](https://upload.wikimedia.org/wikipedia/commons/4/4a/2025-03-04_15_58_38_The_Fort_Dix_WSR-88D_NEXRAD_radar_%28KDIX%29_at_Joint_Base_McGuire%E2%80%93Dix%E2%80%93Lakehurst_in_Manchester_Township%2C_Ocean_County%2C_New_Jersey.jpg)

**Why it's interesting:**

* The TLC publishes monthly trip records by pickup timestamp + taxi‑zone ID. ([NYC Government][1])
* The zone field (“Taxi Zone”) is explicitly included. ([Data.gov][2])
* Using NEXRAD (NEXRAD Level III) storm‐onset detections to define “intervention” (storm start) and then seeing if pickup‑rates in 15‑min blocks for each zone show a “peak echo” effect (outcome) is well‐posed.
* Analysis strategy: interrupted time‑series (ITS) via segmented regression, block bootstrap for CI, gating on effect ≥ 0.1 SD above null and controlling FDR p<0.01 — strong.
* Replication: multiple storm days *and* across months 2019–2024 (data available) gives robustness.

**Feasibility & data‐checks:**

* TLC data: the user guide indicates data from 2009 onwards, separated by year/month/type. ([NYC Government][3])
* Taxi zone metadata: yes, there are taxi‑zone lookup files. ([Medium][4])
* Storm onset detection: you’ll need to define a consistent rule (e.g., NEXRAD cell reflectivity exceed threshold at given time).
* 15‑minute bins: likely feasible (timestamp resolution is present) from the TLC pickup datetime field. ([NYC Government][5])
* Control for confounders: day/time of week, zone fixed effects, trending seasonality (detrended pickup rate) will be required.

**Gaps / caveats:**

* The data released may have delays, missing or corrupted points; ensure you inspect quality (missing timestamps, zones, etc).
* Storm‐onset timing must be synced precisely to the taxi timestamp timezone.
* Detrending method matters: you’ll need a baseline of pickup rate for each zone (maybe previous days same hour/day) to compute anomaly.
* Interference: Storms may impact traffic or reductions in demand; “echo peak” may be subtle or absent in some zones.

**Suggested next steps:**

* Download a year (e.g., 2019) of TLC pickup data for zones.
* Acquire NEXRAD Level III radar reflectivity data for same region/time period (NYC area).
* Pick a set of storm dates (e.g., heavy convective days) and mark onset times.
* For each zone, compute 15‑min pickup counts, detrend (e.g., subtract moving average), compute segmented regression (pre/post onset) and bootstrap CI.
* Gate on effect size ≥0.1 SD and p<0.01 (FDR across zones/dates).
* Replicate across months 2019–2024.

---

## 2) Aftershock diffusion vs. VDM cone in earthquakes

![Image](https://www.researchgate.net/publication/362581815/figure/fig4/AS%3A11431281091364149%401666403363321/Map-of-the-aftershock-spatial-distribution-recorded-during-the-seismic-sequence-from-July.png)

![Image](https://www.researchgate.net/publication/312060596/figure/fig1/AS%3A642422551879683%401530176880478/Map-of-the-locations-of-the-aftershocks-yellow-and-orange-dots-sized-by-magnitudes-that.png)

![Image](https://static.temblor.net/wp-content/uploads/2019/10/fig_OmoriPlot.jpg)

![Image](https://www.researchgate.net/publication/264124112/figure/fig5/AS%3A550929050988545%401508363129121/The-graphs-show-P-value-in-5a-from-modified-Omori-law-and-R-value-in-5b-based-on-the.png)

![Image](https://www.researchgate.net/publication/383092298/figure/fig1/AS%3A11431281271407077%401723614743151/Schematic-illustration-of-the-ETAS-model-aBackground-earthquakes-turquoise-and.png)

![Image](https://www.researchgate.net/publication/1835222/figure/fig1/AS%3A339911300403201%401458052577282/An-example-of-a-realization-of-the-ETAS-model-which-illustrates-the-differences-between.png)

**Why it's interesting:**

* The classical Omori’s law (aftershock rate ∼ 1/t) is a baseline: “rate ~ inverse time” in geophysics. ([U.S. Geological Survey][6])
* Many studies propose aftershock diffusion (spatial spread over time). e.g., mapping aftershock rate in region × hourly bins, seeing resurgence (“echo”) in spatially partitioned rate after partial reversal via declustering. The mapping to your VDM cone (visual/volume diffusion mapping) idea is plausible.
* Use of the United States Geological Survey (USGS) ANSS ComCat API allows automation across tectonic settings.

**Feasibility & data‐checks:**

* Aftershock catalogs: USGS provides earthquake catalog APIs (ComCat) with location, magnitude, time. (You’d still need to apply declustering to isolate aftershock sequences.)
* Aftershock diffusion literature: See e.g., “Diffusion of Earthquake Aftershock Epicenters, Omori’s Law and Generalized Continuous‐Time Random Walk Models” ([arXiv][7])
* The modified‐Omori, spatio‑temporal analogues exist. ([arXiv][8])

**Gaps / caveats:**

* Declustering is non‑trivial; the choice of method will influence residual “echo‑like” signals.
* Partitioning region × hourly bins: you’ll need to define region grid (spatial bins) and time bins, ensure sufficient data volume.
* Testing a “VDM‐predicted invariant cone metric” means you’ll need a clear mapping between VDM concept (whatever VDM means in your context) and the spatial diffusion emanating from the mainshock in time–space. The “cone” may denote distance increasing linearly (or some other function) with time; you must operationalize that.
* Aftershock rate decay may dominate any “echo” effect; you’ll need to model baseline decay (Omori) then test for residual “resurgence” above that.

**Suggested next steps:**

* Choose a set of mainshocks (M ≥ 5) across different tectonic settings (e.g., subduction zone, continental).
* For each, download the catalog from ComCat (pre and post mainshock).
* Perform declustering to isolate aftershocks vs background.
* Bin spatially and temporally (e.g., hourly × spatial shells around mainshock).
* Fit Omori (and maybe a modified‐Omori) decay model to rate versus time; quantify residuals.
* Define a “cone metric” (e.g., rate resurgence in a shell corresponding to distance = v*time, for some v) and test whether the residuals show a peak at ~2t (analogous to your storm‑echo idea).
* Bootstrap or block‐bootstrap to get CIs; test effect size, correct for multiple sequences/settings.

---

**In summary:**
Both ideas are **very doable** given open data and fit nicely into your analytical framework (unit/time‑bins, intervention, outcome, ITS/segmented regression, bootstrap CI, replication across days/months/settings). The main work will be in operationalizing your “echo‐peak at 2t” (storm case) or “echo‐resurgence after partial reversal” (earthquake case) in a robust way, choosing the right parameters (zone, time bins, spatial shells, etc) and controlling confounders/baseline trends.

If you like, I can **pull together direct links (APIs, data portals, sample download scripts, zone definitions, radar data access)** for both projects so you can hit the ground running.

[1]: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page?utm_source=chatgpt.com "TLC Trip Record Data - NYC.gov"
[2]: https://catalog.data.gov/dataset/2022-yellow-taxi-trip-data?utm_source=chatgpt.com "2022 Yellow Taxi Trip Data - Dataset - Catalog"
[3]: https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf?utm_source=chatgpt.com "[PDF] TLC Trip Records User Guide - NYC.gov"
[4]: https://medium.com/%40muhammadaris10/nyc-taxi-trip-data-analysis-45ecfdcb6f91?utm_source=chatgpt.com "NYC Taxi Trip Data Analysis - Medium"
[5]: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf?utm_source=chatgpt.com "[PDF] Data Dictionary – Yellow Taxi Trip Records March 18, 2025 - NYC.gov"
[6]: https://pubs.usgs.gov/publication/70271914?utm_source=chatgpt.com "An exploration of the relative influence of physical models ..."
[7]: https://arxiv.org/abs/cond-mat/0203505?utm_source=chatgpt.com "Diffusion of Earthquake Aftershock Epicenters, Omori's Law and Generalized Continuous-Time Random Walk Models"
[8]: https://arxiv.org/abs/2111.02955?utm_source=chatgpt.com "A spatio-temporal analogue of the Omori-Utsu law of aftershock sequences"
