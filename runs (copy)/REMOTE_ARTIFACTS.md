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
| 2026-02-04_141359 | 2026-02-04T14:13:59 | zip_bundle | 133.17 MiB | 4dad6e496dac975382966473a9600dcca42a1603ae3cf7bcce8f5278fffc6693 | https://drive.google.com/file/d/14B8B8-soHow0P3ydUfP2FRkMSeSOUPan/view?usp=drive_link | Originally: runs/20260204_141359.zip |
| 2026-02-04_130222 | 2026-02-04T13:02:22 | zip_bundle | 226.63 MiB | b922a7fa8621a802d51442a83c90f81b1782a3690260b720a3d01098cdfcbda3 | https://drive.google.com/file/d/1mkZzVx2Vo9lvTSM4BxgbS5ou7KwmSOUW/view?usp=drive_link | Originally: runs/20260204_130222.zip |
| archived |  | drive_folder |  |  | https://drive.google.com/drive/folders/1u6agtXhAhITwQqK4kXsyL8lny5dsZYUd?usp=drive_link | Originally: runs/archived.zip (now hosted as a Drive folder) |

## Details

### 2026-02-04_141359

- Title: Run bundle (2026-02-04 14:13:59)
- kind: zip_bundle
- created_at: 2026-02-04T14:13:59
- source_commit: 3d696c658ddf140580bd479eedf68707d888d36f
- bytes: 139639702 (133.17 MiB)
- sha256: 4dad6e496dac975382966473a9600dcca42a1603ae3cf7bcce8f5278fffc6693
- url: https://drive.google.com/file/d/14B8B8-soHow0P3ydUfP2FRkMSeSOUPan/view?usp=drive_link
- notes: Originally: runs/20260204_141359.zip

### 2026-02-04_130222

- Title: Run bundle (2026-02-04 13:02:22)
- kind: zip_bundle
- created_at: 2026-02-04T13:02:22
- source_commit: 3d696c658ddf140580bd479eedf68707d888d36f
- bytes: 237640319 (226.63 MiB)
- sha256: b922a7fa8621a802d51442a83c90f81b1782a3690260b720a3d01098cdfcbda3
- url: https://drive.google.com/file/d/1mkZzVx2Vo9lvTSM4BxgbS5ou7KwmSOUW/view?usp=drive_link
- notes: Originally: runs/20260204_130222.zip

### archived

- Title: Archived runs (folder)
- kind: drive_folder
- url: https://drive.google.com/drive/folders/1u6agtXhAhITwQqK4kXsyL8lny5dsZYUd?usp=drive_link
- notes: Originally: runs/archived.zip (now hosted as a Drive folder)
