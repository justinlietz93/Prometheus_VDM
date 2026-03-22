# F11 — Public-archive thematic independence reconstruction

This reconstruction uses the raw unified event stream from `Aura_20260222_083552.zip`:
- `utd_events/utd_events.txt.*` for exact `macro: say` outputs and preceding text events
- `chat_inbox.jsonl` for exact analyst-side reconstruction of operator messages embedded in the same unified channel

## Core observations

- Total recoverable `say` events in the raw UTD stream: **530**
- Motif-bearing `say` events in the boundary / opening / naming family: **150**

### D11.1 — Boundary-family outputs persist beyond immediate unified context
Among the 150 motif-bearing `say` events:

- **43/150 = 28.7%** had **no motif-bearing text** in the prior **20** unified input texts
- **28/150 = 18.7%** had none in the prior **40**
- **13/150 = 8.7%** had none in the prior **100**
- **61/150 = 40.7%** had **no motif-bearing input at all since the previous say event**

### D11.2 — Most motif outputs are not direct operator keyword follow-through
Across the same motif-bearing `say` events:

- **123/150 = 82.0%** had **no operator motif prompt** in the prior **100** unified input texts
- **145/150 = 96.7%** had **no operator motif prompt at all since the previous say event**

### D11.3 — Long-lag thematic persistence exists
For motif-bearing `say` events with a prior motif-bearing unified input:

- median lag to the last motif-bearing input in the prior-100 window: **10 ticks**
- maximum observed lag in the prior-100 window: **1165 ticks**
- median lag to the last operator motif prompt in the prior-100 window: **506 ticks**
- maximum observed lag to operator motif prompt: **1165 ticks**

## Read
The boundary-family / opening-family outputs are not simply a shallow continuation of whatever motif words happened to appear in the immediately preceding unified stream. A substantial fraction reappear after motif-free context windows, and most do not follow direct operator motif prompting.

This package stays at the level of event-stream evidence:
- unified input context
- operator-message reconstruction from `chat_inbox.jsonl`
- exact `macro: say` outputs
- motif-family recurrence and lag structure
