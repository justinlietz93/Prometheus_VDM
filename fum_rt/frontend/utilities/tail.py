import os
import json
from typing import Any, Tuple, List


def _parse_jsonl_line(line: str) -> Any:
    try:
        return json.loads(line)
    except Exception:
        return None


def _env_int(name: str, default: int) -> int:
    try:
        v = int(os.environ.get(name, str(default)))
        return v
    except Exception:
        return default


def tail_jsonl_bytes(path: str, last_size: int) -> Tuple[List[Any], int]:
    """
    Tail a JSONL file by byte offset with bounded IO and parse work.

    Inputs:
    - path: file path to JSONL
    - last_size: previous file size (bytes) to resume from

    Returns:
    - (records, new_size)
      records: list of parsed JSON objects appended since last_size (possibly truncated to most recent window)
      new_size: new file size to store for the next call

    Environment (all optional):
    - FUM_UI_TAIL_CAP_BYTES         (default 1_048_576)  - initial/rotation cap window
    - FUM_UI_TAIL_MAX_DELTA_BYTES   (default 131_072)    - max bytes read per tick even if more appended
    - FUM_UI_TAIL_MAX_LINES         (default 600)        - max lines parsed per tick from the new chunk

    Notes:
    - These bounds are UI-only to avoid lag on very large or fast-growing files; older appended
      records may be skipped when the per-tick delta exceeds caps. Core runtime is unaffected.
    """
    if not os.path.exists(path):
        return [], 0
    try:
        size = os.path.getsize(path)
    except Exception:
        return [], last_size

    cap = _env_int("FUM_UI_TAIL_CAP_BYTES", 1_048_576)
    max_delta = _env_int("FUM_UI_TAIL_MAX_DELTA_BYTES", 131_072)
    max_lines = _env_int("FUM_UI_TAIL_MAX_LINES", 600)

    # Establish start offset
    start = last_size if 0 <= last_size <= size else 0

    # Initial read or file rotation: only read the tail cap window
    if (last_size <= 0 or last_size > size) and size > cap:
        start = max(0, size - cap)

    # Always bound per-tick delta to avoid huge reads when many bytes were appended
    delta = size - start
    if delta <= 0:
        return [], size
    if max_delta > 0 and delta > max_delta:
        start = size - max_delta
        delta = max_delta

    try:
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(delta)
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return [], size

    # Split once; then optionally keep only the last K lines to bound JSON parsing work
    lines = text.splitlines()
    if max_lines > 0 and len(lines) > max_lines:
        lines = lines[-max_lines:]

    recs: List[Any] = []
    for s in lines:
        s = s.strip()
        if not s:
            continue
        obj = _parse_jsonl_line(s)
        if obj is not None:
            recs.append(obj)
    return recs, size

def tail_jsonl_bytes_config(path: str, last_size: int, cap: int, max_delta: int, max_lines: int) -> Tuple[List[Any], int]:
    """
    Tail a JSONL file by byte offset using explicit per-call caps (no env vars).

    Args:
        path: JSONL file path
        last_size: previous file size in bytes (seek start)
        cap: initial/rotation cap (bytes)
        max_delta: maximum bytes to read this call
        max_lines: maximum lines to parse from the read chunk

    Returns:
        (records, new_size)
    """
    if not os.path.exists(path):
        return [], 0

    # Sanitize inputs
    try:
        cap = int(cap)
    except Exception:
        cap = 1_048_576
    try:
        max_delta = int(max_delta)
    except Exception:
        max_delta = 131_072
    try:
        max_lines = int(max_lines)
    except Exception:
        max_lines = 600
    cap = max(1024, cap)
    max_delta = max(4096, max_delta)
    max_lines = max(1, max_lines)

    try:
        size = os.path.getsize(path)
    except Exception:
        return [], last_size

    start = last_size if 0 <= last_size <= size else 0

    # Initial read or file rotation: read only tail cap window
    if (last_size <= 0 or last_size > size) and size > cap:
        start = max(0, size - cap)

    delta = size - start
    if delta <= 0:
        return [], size
    if max_delta > 0 and delta > max_delta:
        start = size - max_delta
        delta = max_delta

    try:
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(delta)
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return [], size

    lines = text.splitlines()
    if max_lines > 0 and len(lines) > max_lines:
        lines = lines[-max_lines:]

    recs: List[Any] = []
    for s in lines:
        s = s.strip()
        if not s:
            continue
        obj = _parse_jsonl_line(s)
        if obj is not None:
            recs.append(obj)
    return recs, size