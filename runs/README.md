# runs/ (Run Data)

This folder is intentionally **not** treated like a normal source-controlled directory.

## Policy (practical)

- **Raw run directories** (e.g. `runs/20260204_141359/`) are typically large and change frequently.
  - They are ignored by default via the repo `.gitignore`.
- **Run bundles and logs should live off-repo** (Google Drive / NAS / S3 / Release assets).
  - The repo should keep only a small **index + checksums + metadata** so runs are discoverable and verifiable.
  - If a rare curated `.zip` must be versioned, it should be treated as an explicit exception and tracked via Git LFS.

## Where the data lives

- In-repo: documentation + indexes
  - `runs/REMOTE_ARTIFACTS.md` (human-friendly index)
  - `runs/REMOTE_ARTIFACTS.json` (machine-friendly source of truth)
- Off-repo: large artifacts (zips, logs, state files)
  - Google Drive folder(s) / other artifact store

## Recommended workflow

1) Keep the full run output locally in a run directory:

- `runs/<run_id>/...`

2) Upload the heavy artifacts to your artifact store (e.g. Google Drive) and record them in `runs/REMOTE_ARTIFACTS.json`:

- Drive link (ideally a folder link)
- SHA256 checksum (so integrity is verifiable)
- Size and short notes (what’s included)

3) Optionally create a *small* curated artifact zip that contains only what you actually need to share:

- minimal logs/metrics
- a small number of representative states
- a README/manifest inside the zip describing: seed(s), config, commit hash, and what’s included

4) If you need to publish multi‑GB bundles repeatedly:

- Keep the bundles off-repo and commit only:
  - a manifest JSON with checksums + download URL(s)
  - the run config

## Helpful commands

- See what git will ignore:
  - `git check-ignore -v runs/<file>`

- Confirm LFS is tracking the zips:
  - `git lfs ls-files --size | grep '^.* runs/'`

- If a push is taking forever:
  - check if you accidentally staged a multi‑GB zip (`git status`)
  - unstage it: `git restore --staged runs/<bigfile>.zip`

## Updating the remote index

- Edit `runs/REMOTE_ARTIFACTS.json`, then regenerate `runs/REMOTE_ARTIFACTS.md`:
  - `python tools/runs/build_remote_artifacts_index.py`
