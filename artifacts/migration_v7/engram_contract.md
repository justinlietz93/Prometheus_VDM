# Engram Contract (v7 sparse-only)

## Save
- API: `save_checkpoint(run_dir, step, connectome, fmt='h5', adc=None)`
- File: `state_<step>.h5`

## Load
- API: `load_engram(path, connectome, adc=None)`
- Connectome type: `vdm_rt.core.sparse_connectome.Connectome`

## Resume guarantee
- Resume rehydrates sparse physics state and continues ticking from restored state.
- Verified in smoke run (checkpoint at 10, resumed through 15).
