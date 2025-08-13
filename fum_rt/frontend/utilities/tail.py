import os
import json
from typing import Any, Tuple, List


def _parse_jsonl_line(line: str) -> Any:
    try:
        return json.loads(line)
    except Exception:
        return None


def tail_jsonl_bytes(path: str, last_size: int) -> Tuple[List[Any], int]:
    """
    Tail a JSONL file by byte offset.

    Inputs:
    - path: file path to JSONL
    - last_size: previous file size (bytes) to resume from

    Returns:
    - (records, new_size)
      records: list of parsed JSON objects appended since last_size
      new_size: new file size to store for the next call

    Notes:
    - To prevent the UI from blocking on very large files, the initial read (or a
      truncated/rotated file) is capped to the last CAP bytes. CAP is configurable
      via environment variable FUM_UI_TAIL_CAP_BYTES (default 1 MiB).
    """
    if not os.path.exists(path):
        return [], 0
    try:
        size = os.path.getsize(path)
    except Exception:
        return [], last_size

    # Cap initial/truncated reads to avoid UI stalls on very large files
    try:
        cap = int(os.environ.get("FUM_UI_TAIL_CAP_BYTES", "1048576"))
    except Exception:
        cap = 1048576

    start = last_size if 0 <= last_size <= size else 0
    if (last_size <= 0 or last_size > size) and size > cap:
        # New stream or file rotation detected: only read the tail window
        start = size - cap

    if size == start:
        return [], size

    try:
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(size - start)
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return [], size

    recs: List[Any] = []
    # Faster and simpler than char-by-char accumulation
    for s in text.splitlines():
        s = s.strip()
        if not s:
            continue
        obj = _parse_jsonl_line(s)
        if obj is not None:
            recs.append(obj)
    return recs, size