# Void Dynamics Model Runtime: Version 9

## What this is

This is the pure physics migration from the existing vdm_rt/ runtime. The existing version has successfully modeled several signatures of human cognition, as well as fundamental physics. That runtime uses mostly proxies and engineering tricks and does not entirely obey causality. This framework was originally designed to remove hand-waviness and get to the truth as honestly and rigorously as possible. Version 9 is the steady rebuilding of the existing runtime using the pure physics formalisms derived in the physics framework. This runtime will have it's own version of the falsification pipeline and tier standards that are just as rigorous, but well suited to the high efficiency requirements of a real time physics runtime that should work on everyday consumer hardware. This entire repo and all the code in it can currently run on my $200 Acer Aspire 15 laptop, and I intend to keep it that way.

## Note on Lattice Claim

VDM requires a real local discrete substrate. The current cubic-periodic lattice is the present implementation substrate for T2 validation, not yet the uniquely admitted spacetime lattice. During migration, lattice choice is a controlled physics variable that must be constrained by gates, not treated as a cosmetic engineering detail.
