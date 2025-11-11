# Vendoring Rules (`third_party/README.md`)

## Purpose
Documents the process to follow if third-party code is ever **copied (vendored)** into the repository.

## Current Status
No third-party code is currently vendored. All dependencies are obtained via pip or other package managers.

## Vendoring Process
1) Place each third-party component under `third_party/<project_name>/`.
2) Include the original `LICENSE` and `NOTICE` files **verbatim**.
3) Keep original file headers intact; **do not** add Neuroca proprietary headers to third-party-only files.
4) For mixed-origin files, clearly annotate which portions are third-party and which are Neuroca modifications.
5) Update the root `NOTICE.md` to list vendored components and their licenses.
6) Respect upstream license terms, including copyleft, attribution, and notice obligations.

## Contact
Email justin@neuroca.ai with questions **before** vendoring.
