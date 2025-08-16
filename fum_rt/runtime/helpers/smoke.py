"""
Runtime helper: optional one-shot smoke tests (macros and thought ledger).

- Controlled by env flags:
  - ENABLE_MACROS_TEST
  - ENABLE_THOUGHTS_TEST

Behavior:
- Mirrors legacy Nexus logic exactly; guarded and fail-soft.
"""

from __future__ import annotations

import os
from typing import Any, Dict


def maybe_smoke_tests(nx: Any, m: Dict[str, Any], step: int) -> None:
    """
    One-shot emitters test for macros and thought ledger when ENABLE_*_TEST env flags are set.
    Mirrors Nexus inline behavior and guards with booleans on nx.
    """
    # Macro smoke
    try:
        if (not getattr(nx, "_macros_smoke_done", False)) and str(os.getenv("ENABLE_MACROS_TEST", "0")).lower() in ("1", "true", "yes", "on"):
            if getattr(nx, "emitter", None):
                nx.emitter.vars({"N": "neural", "G": "global_access", "E": "experience", "B": "behavior"})
                nx.emitter.edges(["N->G", "G->B", "E->B?"])
                nx.emitter.assumptions(["no unmeasured confounding", "positivity"])
                nx.emitter.target("P(B|do(G))")
                nx.emitter.derivation("If N fixes G and G mediates B, therefore adjust on {confounders} yields effect.")
                nx.emitter.prediction_delta("Behavioral margin differs if extra-law holds.")
                nx.emitter.transfer("Circuit: signal->bus; flag->output; hidden noise.")
                nx.emitter.equation("Y = β X + U_Y")
                nx.emitter.status("macro smoke: ok")
            nx._macros_smoke_done = True
    except Exception:
        pass

    # Thought ledger smoke
    try:
        if (not getattr(nx, "_thoughts_smoke_done", False)) and str(os.getenv("ENABLE_THOUGHTS_TEST", "0")).lower() in ("1", "true", "yes", "on"):
            if getattr(nx, "thoughts", None):
                nx.thoughts.observation("vt_entropy", float(m.get("vt_entropy", 0.0)))
                nx.thoughts.motif("cycle_probe", nodes=[1, 2, 3])
                nx.thoughts.hypothesis("H0", "A ⟂ B | Z", status="tentative", conf=0.55)
                nx.thoughts.test("CI", True, vars={"A": "A", "B": "B", "Z": ["Z"]})
                nx.thoughts.derivation(["H0", "obs:vt_coverage↑"], "Identify P(Y|do(X)) via backdoor on {Z}", conf=0.6)
                nx.thoughts.revision("H0", "accepted", because=["test:CI:true"])
                nx.thoughts.plan("intervene", vars={"target": "X"}, rationale="disambiguate twins")
            nx._thoughts_smoke_done = True
    except Exception:
        pass


__all__ = ["maybe_smoke_tests"]