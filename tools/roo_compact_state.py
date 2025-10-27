#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
# Row-level compact for VS Code state: caps taskHistory by count + bytes AND
# caps the entire JSON row by bytes, with aggressive scrubbing of long strings
# and message-like arrays. Safe: backs up DB, archives pruned tasks.

import argparse, json, os, sqlite3, sys, time, shutil
from pathlib import Path
from typing import Any, List, Tuple

MESSAGE_KEYS = {"messages","chunks","diffs","edits","logs","history","items","toolCalls","outputs","events"}
TRIM_MARK = " …[trimmed]… "

def backup_db(db: Path) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    bak = db.with_name(f"{db.name}.bak.{ts}")
    shutil.copy2(db, bak)
    return bak

def decode(b):
    if isinstance(b, (bytes, bytearray)): return b.decode("utf-8", "ignore")
    return "" if b is None else str(b)

def bsize(obj: Any) -> int:
    try:
        return len(json.dumps(obj, ensure_ascii=False, separators=(',',':')).encode('utf-8'))
    except Exception:
        return 0

def find_taskhist_nodes(root: Any):
    out = []
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == 'taskHistory' and isinstance(v, list):
                    out.append((node, k))
                walk(v)
        elif isinstance(node, list):
            for v in node: walk(v)
    walk(root)
    return out

def truncate_str(s: Any, max_chars: int) -> Any:
    if not isinstance(s, str): return s
    if len(s) <= max_chars: return s
    head = max_chars // 2 - len(TRIM_MARK)//2
    head = max(0, head)
    tail = max_chars - head - len(TRIM_MARK)
    tail = max(0, tail)
    return s[:head] + TRIM_MARK + s[-tail:]

def scrub_node_inplace(node: Any, max_str: int, msg_keep: int):
    # Trim long strings and clip known message-like arrays anywhere in the row
    if isinstance(node, dict):
        for k in list(node.keys()):
            v = node[k]
            if isinstance(v, str):
                node[k] = truncate_str(v, max_str)
            elif isinstance(v, list):
                if k in MESSAGE_KEYS and len(v) > msg_keep:
                    node[k] = v[-msg_keep:]
                for i in range(len(node[k])):
                    scrub_node_inplace(node[k][i], max_str, msg_keep)
            elif isinstance(v, dict):
                scrub_node_inplace(v, max_str, msg_keep)
    elif isinstance(node, list):
        for i in range(len(node)):
            scrub_node_inplace(node[i], max_str, msg_keep)

def shrink_taskhistory(parent: dict, key: str, keep: int, max_bytes_for_parent: int,
                       max_str: int, msg_keep: int) -> Tuple[bool, List[Any]]:
    changed = False
    pruned = []
    arr = parent.get(key, [])
    if not isinstance(arr, list): return False, pruned
    # cap by count first
    if len(arr) > keep:
        pruned.extend(arr[:-keep]); parent[key] = arr[-keep:]; arr = parent[key]; changed = True
    # scrub inside tasks
    scrub_node_inplace(arr, max_str, msg_keep)
    # enforce parent budget
    guard = 0
    while bsize(parent) > max_bytes_for_parent and len(arr) > 1 and guard < 200:
        pruned.append(arr.pop(0)); changed = True; guard += 1
    return changed, pruned

def largest_taskhistory(nodes: List[Tuple[dict,str]]) -> Tuple[int,int]:
    max_len, idx = 0, -1
    for i,(parent,k) in enumerate(nodes):
        arr = parent.get(k, [])
        if isinstance(arr, list) and len(arr) > max_len:
            max_len, idx = len(arr), i
    return idx, max_len

def process_db(db: Path, keep: int, node_max_bytes: int, row_max_bytes: int,
               max_str: int, msg_keep: int, ext_filters: List[str],
               scan_only: bool, verbose: bool):
    con = sqlite3.connect(str(db))
    con.text_factory = bytes
    cur = con.cursor()
    try:
        rows = cur.execute("SELECT key, value FROM ItemTable").fetchall()
    except sqlite3.OperationalError:
        con.close(); return (0,0,0,0,0)
    changed_rows = archived = candidates = bytes_saved = updates_applied = 0
    archive_path = db.with_name("roo-taskHistory-archive.jsonl")
    did_backup = False
    for key_b, val_b in rows:
        key = decode(key_b); val = decode(val_b)
        if ext_filters:
            if not any(f.lower() in key.lower() for f in ext_filters) and '"taskHistory"' not in val:
                continue
        else:
            if '"taskHistory"' not in val:
                continue
        try:
            obj = json.loads(val)
        except Exception:
            continue
        nodes = find_taskhist_nodes(obj)
        if not nodes: continue
        candidates += 1
        before = bsize(obj)
        total_pruned = []
        changed = False

        # Global scrub first (affects whole row, not only taskHistory)
        scrub_node_inplace(obj, max_str, msg_keep)

        # Per-node compaction
        for parent,k in nodes:
            ch, pruned = shrink_taskhistory(parent, k, keep, node_max_bytes, max_str, msg_keep)
            if ch: changed = True; total_pruned.extend(pruned)

        # Row-level budget: if still large, drop oldest across the largest taskHistory arrays
        guard = 0
        while bsize(obj) > row_max_bytes and guard < 400:
            idx, ln = largest_taskhistory(nodes)
            if idx == -1 or ln <= 1:  # no more to drop; tighten scrubs
                # increase scrubbing aggressiveness
                if msg_keep > 5:
                    msg_keep = max(5, msg_keep - 5)
                elif max_str > 2000:
                    max_str = max(2000, max_str - 1000)
                else:
                    break
                scrub_node_inplace(obj, max_str, msg_keep)
            else:
                parent,k = nodes[idx]
                arr = parent.get(k, [])
                if isinstance(arr, list) and len(arr) > 1:
                    total_pruned.append(arr.pop(0)); changed = True
            guard += 1

        after = bsize(obj)
        if changed and after <= before:
            changed_rows += 1
            bytes_saved += (before - after)
            archived += len(total_pruned)
            if verbose:
                print(f"[+] {db} key={key} pruned_tasks={len(total_pruned)} bytes_saved={before-after} final={after}")
            if not scan_only:
                if not did_backup:
                    backup_db(db); did_backup = True
                new_text = json.dumps(obj, ensure_ascii=False, separators=(',',':'))
                cur.execute("UPDATE ItemTable SET value=? WHERE key=?", (new_text, key))
                updates_applied += cur.rowcount
                with open(archive_path, "ab") as f:
                    for item in total_pruned:
                        f.write((json.dumps(item, ensure_ascii=False)+"\n").encode('utf-8'))

    if not scan_only and changed_rows:
        con.commit()
        try: cur.execute("VACUUM")
        except Exception: pass
    con.close()
    return (candidates, changed_rows, archived, bytes_saved, updates_applied)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="Path to state.vscdb")
    ap.add_argument("--keep", type=int, default=20, help="Keep last N tasks")
    ap.add_argument("--node-max-bytes", type=int, default=180000, help="Target max bytes for the parent object holding taskHistory")
    ap.add_argument("--row-max-bytes", type=int, default=220000, help="Target max bytes for the entire JSON row")
    ap.add_argument("--max-str", type=int, default=6000, help="Max chars for any string field")
    ap.add_argument("--messages-keep", type=int, default=15, help="Keep last K items in message-like arrays")
    ap.add_argument("--ext-substr", type=str, default="", help="Comma-separated substr filters (optional)")
    ap.add_argument("--scan-only", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    ext_filters = [s.strip() for s in args.ext_substr.split(",") if s.strip()]
    cand, changed, arch, saved, applied = process_db(Path(args.db).expanduser(),
                                                     args.keep, args.node_max_bytes, args.row_max_bytes,
                                                     args.max_str, args.messages_keep,
                                                     ext_filters, args.scan_only, args.verbose)
    mode = "SCAN" if args.scan_only else "COMPACT"
    print(f"[{mode}] candidates={cand} rows_changed={changed} items_archived={arch} bytes_saved={saved} updates_applied={applied}")

if __name__ == "__main__":
    main()
