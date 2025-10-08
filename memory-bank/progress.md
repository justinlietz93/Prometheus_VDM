# Progress (Updated: 2025-10-08)

## Done

- Added experiment script resolution and DB dir/file validation to results_db.begin_run
- Added manifest lookup and tag validation against allowed_tags + approvals
- Set VDM_RUN_SCRIPT based on resolved script for downstream authorization HMAC scope
- Fixed Bandit B608 warning by consolidating SQL into single-line f-string with nosec

## Doing

- Light test pass on results_db.begin_run in a dry environment to assert new validations behave as expected

## Next

- Document RESULTSDB_SKIP_APPROVAL_CHECK escape hatch and new preconditions in module docstring
- Wire results_db into an example runner showing the full lifecycle
