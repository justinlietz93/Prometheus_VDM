#!/usr/bin/env python3

"""
Script: extract_say_texts.py
Purpose: Extract text from 'say' macro events in JSONL logs to CSV/JSONL/text for analysis.

Usage examples:
  python3 tools/extract_say_texts.py runs/20250818_212345/utd_events.jsonl --out outputs/say_texts.csv --format csv --include-why
  python3 tools/extract_say_texts.py "runs/*/utd_events.jsonl" --format text > outputs/say_texts.txt

Input: JSONL where each line is a JSON object with fields like:
  {"type":"macro","macro":"say","args":{"text":"..."}, "why": {...}, "score": 0.5}

This script streams the input(s) to handle large files; no full-file load.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import os
import sys
import glob
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Tuple


@dataclass
class SayRecord:
    source_path: str
    line_no: int
    text: str
    t: Optional[float] = None
    phase: Optional[int] = None
    score: Optional[float] = None
    why: Optional[Dict] = None


def _open_read(path: str):
    if path.endswith(".gz"):
        return io.TextIOWrapper(gzip.open(path, "rb"), encoding="utf-8")
    return open(path, "r", encoding="utf-8")


def _flatten_why(why: Optional[Dict], prefix: str = "") -> Dict[str, Optional[float]]:
    """Flatten a 'why' object into a single-level dict.
    - prefix="" yields keys like 't', 'phase', 'b1_z', 'cohesion_components', 'vt_entropy', ...
    - prefix="why." yields 'why.t', 'why.phase', 'why.b1_z', 'why.vt_entropy', ...
    - nested dicts are flattened one level: e.g., why.something.sub -> "something.sub"
    """
    if not isinstance(why, dict):
        return {}
    out: Dict[str, Optional[float]] = {}

    def add(k: str, v):
        out[f"{prefix}{k}"] = v

    for k, v in why.items():
        if isinstance(v, (int, float, str, bool)) or v is None:
            add(k, v)
        elif isinstance(v, dict):
            for k2, v2 in v.items():
                if isinstance(v2, (int, float, str, bool)) or v2 is None:
                    add(f"{k}.{k2}", v2)
    return out


def iter_jsonl(paths: List[str]) -> Iterator[Tuple[str, int, Dict]]:
    for path in paths:
        with _open_read(path) as fh:
            for i, line in enumerate(fh, start=1):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception as e:
                    sys.stderr.write(f"[warn] {path}:{i}: JSON parse error: {e}\n")
                    continue
                yield path, i, obj


def extract_say_records(paths: List[str]) -> Iterator[SayRecord]:
    for path, line_no, obj in iter_jsonl(paths):
        try:
            if obj.get("type") != "macro" or obj.get("macro") != "say":
                continue
            args = obj.get("args") or {}
            text = args.get("text")
            if not isinstance(text, str):
                continue
            # Support 'why' at top-level or inside args (as in provided example)
            why = obj.get("why")
            if not isinstance(why, dict):
                why = args.get("why")
            t = None
            phase = None
            if isinstance(why, dict):
                t = why.get("t")
                phase = why.get("phase")
            score = obj.get("score")
            yield SayRecord(
                source_path=path,
                line_no=line_no,
                text=text,
                t=t,
                phase=phase,
                score=score,
                why=why if isinstance(why, dict) else None,
            )
        except Exception as e:
            sys.stderr.write(f"[warn] {path}:{line_no}: extraction error: {e}\n")
            continue


def _records_to_rows(
    records: Iterable[SayRecord],
    include_why: bool,
    include_source: bool,
    why_as: str,
    flat_why_keys: List[str],
    why_prefix: str,
) -> Tuple[List[str], Iterator[List]]:
    # Header (avoid duplicate t/phase if coming from flattened why without prefix)
    base_fields: List[str] = []
    if include_source:
        base_fields += ["source_path", "line_no"]

    if include_why and why_as == "flat" and why_prefix == "":
        # 't' and 'phase' will be provided by flattened why keys
        base_fields += ["score", "text"]
    else:
        base_fields += ["t", "phase", "score", "text"]

    if include_why:
        if why_as == "json":
            base_fields += ["why_json"]
        else:
            base_fields += flat_why_keys

    def row_iter():
        for r in records:
            row: List = []
            if include_source:
                row += [r.source_path, r.line_no]
            if include_why and why_as == "flat" and why_prefix == "":
                row += [r.score, r.text]
            else:
                row += [r.t, r.phase, r.score, r.text]

            if include_why:
                if why_as == "json":
                    row += [
                        json.dumps(r.why, ensure_ascii=False, separators=(",", ":"))
                        if r.why is not None
                        else None
                    ]
                else:
                    flat = _flatten_why(r.why, prefix=why_prefix) if isinstance(r.why, dict) else {}
                    row += [flat.get(k) for k in flat_why_keys]
            yield row

    return base_fields, row_iter()


def write_csv(
    records: Iterable[SayRecord],
    out_fh: io.TextIOBase,
    include_why: bool,
    include_source: bool,
    why_as: str,
    flat_why_keys: List[str],
    why_prefix: str,
) -> None:
    header, rows = _records_to_rows(
        records,
        include_why=include_why,
        include_source=include_source,
        why_as=why_as,
        flat_why_keys=flat_why_keys,
        why_prefix=why_prefix,
    )
    writer = csv.writer(out_fh)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)


def write_jsonl(
    records: Iterable[SayRecord],
    out_fh: io.TextIOBase,
    include_why: bool,
    include_source: bool,
    why_as: str,
    why_prefix: str,
) -> None:
    for r in records:
        obj = {
            "text": r.text,
            "t": r.t,
            "phase": r.phase,
            "score": r.score,
        }
        if include_source:
            obj["source_path"] = r.source_path
            obj["line_no"] = r.line_no
        if include_why:
            obj["why"] = r.why
            if why_as == "flat" and isinstance(r.why, dict):
                obj["why_flat"] = _flatten_why(r.why, prefix=why_prefix)
        out_fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def write_text(records: Iterable[SayRecord], out_fh: io.TextIOBase, dedupe: bool) -> None:
    seen = set()
    for r in records:
        s = r.text.replace("\r\n", "\n").replace("\r", "\n")
        if dedupe:
            key = s.strip()
            if key in seen:
                continue
            seen.add(key)
        out_fh.write(s + "\n")


def _collect_from_directory(dir_path: str, pattern: str, recursive: bool) -> List[str]:
    """Collect matching files from a directory."""
    if recursive:
        pat = os.path.join(dir_path, "**", pattern)
        matches = glob.glob(pat, recursive=True)
    else:
        pat = os.path.join(dir_path, pattern)
        matches = glob.glob(pat)
    return sorted(p for p in matches if os.path.isfile(p))
    
    
def discover_flat_why_keys(paths: List[str], why_prefix: str) -> List[str]:
    """Scan inputs to determine the union of flattened 'why' keys present in 'say' macros."""
    keys = set()
    for path, i, obj in iter_jsonl(paths):
        try:
            if obj.get("type") == "macro" and obj.get("macro") == "say":
                # try top-level then args.why
                why = obj.get("why")
                if not isinstance(why, dict):
                    args = obj.get("args") or {}
                    why = args.get("why")
                if isinstance(why, dict):
                    flat = _flatten_why(why, prefix=why_prefix)
                    for k in flat.keys():
                        keys.add(k)
        except Exception:
            continue
    return sorted(keys)
    
def _expand_inputs(inputs: List[str], pattern: str, recursive: bool) -> List[str]:
    """Expand inputs into a deduplicated, sorted list of files.
    - Files/globs are expanded with glob.
    - Directories are scanned for files matching 'pattern'.
    - Directory paths discovered via globs are also scanned.
    """
    seen = set()
    expanded: List[str] = []
    for inp in inputs:
        if os.path.isdir(inp):
            for p in _collect_from_directory(inp, pattern, recursive):
                if p not in seen:
                    expanded.append(p)
                    seen.add(p)
            continue

        matches = glob.glob(inp)
        if matches:
            for p in sorted(matches):
                if os.path.isdir(p):
                    for q in _collect_from_directory(p, pattern, recursive):
                        if q not in seen:
                            expanded.append(q)
                            seen.add(q)
                else:
                    if p not in seen:
                        expanded.append(p)
                        seen.add(p)
        else:
            if inp not in seen:
                expanded.append(inp)
                seen.add(inp)
    return expanded


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract text from 'say' macro events in JSONL logs.")
    p.add_argument("inputs", nargs="+", help="Input JSONL file(s) or directories. Globs supported. .gz supported.")
    p.add_argument("--out", "-o", default="-", help="Output file path. '-' for stdout.")
    p.add_argument("--format", "-f", choices=["csv", "jsonl", "text"], default="csv", help="Output format.")

    # Why handling (defaults to including all why fields as flat columns, without prefix)
    p.add_argument("--include-why", dest="include_why", action="store_true", help="Include the 'why' object in output (default).")
    p.add_argument("--no-why", dest="include_why", action="store_false", help="Disable including 'why' in the output.")
    p.set_defaults(include_why=True)

    p.add_argument(
        "--why-as",
        choices=["json", "flat"],
        default="flat",
        help="How to include 'why': 'json' as single column (CSV) or raw 'why' (JSONL); "
             "'flat' expands fields into columns and adds why_flat to JSONL.",
    )
    p.add_argument(
        "--why-prefix",
        default="",
        help="Column prefix for flattened 'why' keys (e.g., 'why.'). Default '' (no prefix).",
    )

    # Other options
    p.add_argument("--include-source", action="store_true", help="Include source file and line number in output.")
    p.add_argument("--dedupe", action="store_true", help="For format=text, deduplicate identical lines after stripping.")
    p.add_argument("--pattern", "-p", default="utd_events*.jsonl", help="If an input is a directory, match files with this pattern.")
    p.add_argument("--recursive", "-R", action="store_true", help="Recurse into subdirectories for directory inputs.")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    input_paths = _expand_inputs(args.inputs, pattern=args.pattern, recursive=args.recursive)
    if not input_paths:
        sys.stderr.write("No input files.\n")
        return 2

    records = extract_say_records(input_paths)

    if args.out == "-" or args.out == "":
        out_fh = sys.stdout
        close_out = False
    else:
        out_fh = open(args.out, "w", encoding="utf-8", newline="")
        close_out = True

    try:
        if args.format == "csv":
            flat_keys: List[str] = []
            if args.include_why and args.why_as == "flat":
                # Second streaming pass to discover union of flat why keys (with chosen prefix)
                flat_keys = discover_flat_why_keys(input_paths, args.why_prefix)
            write_csv(
                records,
                out_fh,
                include_why=args.include_why,
                include_source=args.include_source,
                why_as=args.why_as,
                flat_why_keys=flat_keys,
                why_prefix=args.why_prefix,
            )
        elif args.format == "jsonl":
            write_jsonl(
                records,
                out_fh,
                include_why=args.include_why,
                include_source=args.include_source,
                why_as=args.why_as,
                why_prefix=args.why_prefix,
            )
        else:
            write_text(records, out_fh, dedupe=args.dedupe)
    finally:
        if close_out:
            out_fh.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())