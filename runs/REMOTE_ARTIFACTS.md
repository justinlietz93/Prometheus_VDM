# Remote Run Artifacts

Large run outputs (zips, logs, state files) are hosted off-repo.
This index provides links + integrity metadata so artifacts are still reproducible and shareable.

## How to add a new artifact

1) Upload the artifact (or folder) to Google Drive (or another store)
2) Make it accessible to collaborators (link-sharing as needed)
3) Compute SHA256 locally
4) Add an entry to `runs/REMOTE_ARTIFACTS.json`
5) Regenerate this file: `python tools/runs/build_remote_artifacts_index.py`

## Index

| id | created_at | kind | size | sha256 | url | notes |
|---|---|---|---:|---|---|---|
| 2026-02-04_141359 | 2026-02-04T14:13:59 | zip_bundle |  |  |  |  |

## Details

### 2026-02-04_141359

- Title: Run bundle (2026-02-04 14:13:59)
- kind: zip_bundle
- created_at: 2026-02-04T14:13:59
