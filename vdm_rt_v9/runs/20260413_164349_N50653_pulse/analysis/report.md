# Run Analysis: run_log.h5

## Dataset
- H5 path: /home/justin/git/Prometheus_VDM/vdm_rt_v9/runs/20260413_164349_N50653_pulse/run_log.h5
- Nodes: 50653
- Lattice: 37 x 37 x 37 cubic
- Stimulus: pulse (amp=0.0)
- Summary ticks: 0 to 999 (1000 samples)
- Snapshot cadence: every 50 ticks (21 snapshots)

## Executive Findings
- The run shows a real symmetry-breaking event: phi starts near the unstable midpoint and settles into a binary 90/10 split. The positive-phase occupancy grows from 0.9916 at t=0 to 0.9916 at t=999.
- The settled geometry is a z-oriented slab, not a fragmented foam. The final positive planes are contiguous with thickness 37 out of 37 and x/y occupancy is flat to machine precision.
- That slab is not fully unbiased evidence of isotropic emergence. In this run the pulse itself is planar in index space, so the initial condition already favors z-oriented walls on the cubic lattice.
- The early transient is violent but short: walkers peak at 154383 on tick 1, kT peaks at 0.00200617 on tick 2, and active nodes peak at 14580 on tick 1.
- After the transient, the system is not broadband-critical. For ticks >= 200, n_active locks into a narrow period-2.50 oscillation with lag-5 autocorrelation 0.927 and CV 0.1167.
- Persistent topological growth is absent in the logged snapshots: max degree stays 26, final persistent new edges are 0, and the final graph is a pruned subset of the original lattice.

## Stimulus Geometry
- The pulse logic injects 1013 nodes per sign.
- Positive region bounds: [0, 0, 0] to [36, 27, 0]; z slices [0].
- Negative region bounds: [0, 0, 12] to [36, 36, 13]; z slices [12, 13].
- This means the default pulse is a plane-plus-plane fragment, not a point-like or spherical perturbation. The final slab should therefore be interpreted as phase separation under a biased seed, not as spontaneous isotropic cosmogenesis.

## Cosmogenesis Signatures
- Strong evidence for phase separation: final low/high well occupancy is 0.008/0.992, with middle occupancy 0.000 and bimodality coefficient 1.000.
- Macrostate lock occurs by snapshot tick 0, and full observation of the lattice is present by snapshot tick None.
- Interface energy localization is sharp: final cross-phase bond psi mean is 1.000, versus 0.521 inside domains.
- The final undirected interface count is 3764, while the positive domain volume increases fivefold relative to the first snapshot. That is compatible with low-perimeter coarsening rather than branching hierarchy growth inside this seeded geometry.
- Bond maturation continues after the slab geometry freezes: bonds_total stabilizes near tick 358, while n_condensed_bonds does not settle within 1 percent of final until tick 849.

## Cognition-Like Proxies
- The only durable dynamical structure is an interface oscillator. By snapshot tick 50, 100 percent of above-threshold active nodes are on the phase interface, and this remains true through the end of the run.
- The late-time active fraction is only 0.0124 of nodes on average, so the activity is sparse and spatially localized rather than globally distributed.
- There is persistent oscillation, but not the kind of broadband or avalanche-rich variability usually used as a brain-like criticality proxy. The late-time walker CV is 0.7874 and the dominant activity frequency is 0.40000 cycles per tick.
- The topology also stays simple: the largest condensed-bond component contains 0.115 of nodes, and there are no persistent new long-range edges in the snapshots.

## Limits
- This is one run at one system size, so CF03 scaling laws across L cannot be tested here.
- The log stores periodic snapshots rather than full per-tick fields, so a strict first-arrival causal-cone test is not possible from this artifact alone.
- Human cognition is not directly measurable in this dataset. The report only evaluates generic proxies such as persistence, localization, periodicity, and topological complexity.

## Suggested Improvements
- Replace the index-range pulse with coordinate-defined compact regions, such as spheres or small cubes, so the initial condition does not pre-impose z-oriented slabs on the cubic lattice.
- Increase logging density during the transient, for example snapshots every 1 to 5 ticks through tick 200, or log first-arrival maps explicitly. The current 50-tick spacing is too coarse for a clean CF04 cone test.
- If the goal is cosmogenesis rather than seeded domain growth, run a size sweep over multiple lattice lengths and compare slab thickness, interface box counts, and lock times against CF03 scaling predictions.
- If the goal is cognition-like complexity, use structured recurrent stimulation such as the sensory mode or a task-like input schedule. The single pulse in this run collapses to a narrow deterministic limit cycle instead of maintaining rich, multi-scale dynamics.
- Instrument bond instantiation and bond lifetime directly. In the current snapshots the graph only loses edges and never retains new ones, so claims about emergent long-range topology are not supported here.
