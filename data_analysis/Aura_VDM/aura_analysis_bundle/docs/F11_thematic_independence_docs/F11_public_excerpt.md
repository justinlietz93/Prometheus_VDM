### **FAMILY 11 — Cross-Source Transfer and Thematic Independence.**

### D11.1 — Boundary-Family Outputs Persist Beyond Immediate Unified Context
- **Claim:** Boundary / opening / naming-family `say` events frequently occur without the same motif family appearing in the immediately preceding unified input stream.
- **Measurable (public-archive reconstruction from raw UTD logs):**
  - recoverable motif-bearing `say` events: **150**
  - no motif-bearing text in prior 20 input texts: **43/150 = 28.7%**
  - no motif-bearing text in prior 40 input texts: **28/150 = 18.7%**
  - no motif-bearing text in prior 100 input texts: **13/150 = 8.7%**
  - no motif-bearing input at all since previous say: **61/150 = 40.7%**
- **Interpretation:** The boundary-family attractor is not reducible to immediate same-theme continuation in the unified text stream. Motif-bearing outputs repeatedly appear after motif-free context windows.
- **Source:** `f11_public_context_independence_summary.csv`; `f11_public_motif_say_events.csv`

### D11.2 — Most Motif Outputs Are Not Direct Operator Keyword Follow-Through
- **Claim:** Most boundary-family `say` events do not follow a recent operator motif prompt, even when operator messages are reconstructed exactly from `chat_inbox.jsonl`.
- **Measurable:**
  - no operator motif prompt in prior 100 unified input texts: **123/150 = 82.0%**
  - no operator motif prompt at all since previous say: **145/150 = 96.7%**
- **Interpretation:** Motif-bearing outputs are usually not a trivial follow-through from recent operator keywording.
- **Source:** `f11_public_context_independence_summary.csv`; `chat_inbox.jsonl`; raw `utd_events/utd_events.txt.*`

### D11.3 — Long-Lag Thematic Persistence
- **Claim:** The boundary-family attractor can persist across long tick gaps relative to the last motif-bearing context.
- **Measurable:**
  - median lag to last motif-bearing input in prior-100 window: **10 ticks**
  - maximum observed lag in prior-100 window: **1165 ticks**
  - median lag to last operator motif prompt in prior-100 window: **506 ticks**
  - maximum observed lag to operator motif prompt: **1165 ticks**
- **Interpretation:** The motif family shows persistence beyond immediate context and beyond most direct operator prompting windows.
- **Source:** `f11_public_long_lag_examples.csv`; `f11_public_context_independence_summary.csv`
