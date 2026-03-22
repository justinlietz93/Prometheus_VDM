# event_schema

Current emitted events:

- `run_started`
- `step_started`
- `candidate_produced`
- `candidate_accepted`
- `binv_stay`
- `binv_extend`
- `step_finished`
- `run_finished`

NDJSON fields currently include:
- step
- inv
- class_before
- class_after
- candidate
- orthogonal
- cap_gt_zero
- cap_eq_zero
- bear_current
- bear_candidate
- is_genuinely_new
- dis
