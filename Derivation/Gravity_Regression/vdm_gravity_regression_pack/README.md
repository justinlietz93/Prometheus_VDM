
# VDM Gravity Regression Pack (Precession & Connectome Sanity)

This mini-pack helps you **verify and quantify** the GR-like orbital behaviour you observed earlier
(e.g., **perihelion precession**) and **catch substrate regressions** (e.g., accidental ring-lattice forcing).

**What you get**

- `specs/gravity_regression_spec.md` - the concise test contract.
- `scripts/compute_precession.py` - post-processes a simple CSV of `(t, x, y)` coordinates and reports precession per orbit.
- `scripts/graph_checks.py` - sanity-checks a connectome edgelist for “ring lattice” symptoms; emits metrics + a plot.
- `templates/orbit_log_example.csv` - format example for the orbital track exported from your runtime.
- `templates/edgelist_example.csv` - format example for connectome edgelist.
- `outputs/` - where figures and CSV reports are written.

## Quickstart

1) **Export an orbit track** from your runtime (one “test particle” is enough): write a CSV with columns
`time,x,y` sampled evenly in time. Save it as `orbit_log.csv` (or point the script at your file).

2) **Run precession analysis**:
```bash
python scripts/compute_precession.py --orbit templates/orbit_log_example.csv --out outputs
```

It will produce:
- `outputs/orbit_plot.png` (trajectory + perihelia markers)
- `outputs/precession_report.csv` (per-orbit angle, delta, period)
- `outputs/precession_summary.txt` (median/mean precession per orbit, sign, stability flags)

3) **Export the connectome** as a weighted or unweighted edgelist `src,dst[,w]` (directed or undirected).

4) **Run graph sanity**:
```bash
python scripts/graph_checks.py --edgelist templates/edgelist_example.csv --out outputs
```

It will produce:
- `outputs/connectome_metrics.json` (degree stats, clustering, assortativity, cycle-basis size, ring-lattice suspicion)
- `outputs/connectome_layout.png` (quick layout for visual inspection)

## File formats

- Orbit log: CSV with header `time,x,y` (floats). Time should be strictly increasing.
- Edgelist: CSV with header `src,dst` or `src,dst,w` (strings for ids; weight optional).

---

### Notes
- The pack is a **package** and **post-processing only**; it does not run your VDM. You can swap in any logs you export. Make sure to move code and derivations to their correct locations when solved and remove these artifacts.
- The ring-lattice detector is **heuristic**; it’s a fast tripwire to catch obvious misconfigurations.
- All plots use standard Matplotlib / NetworkX; no GPU or internet required.
