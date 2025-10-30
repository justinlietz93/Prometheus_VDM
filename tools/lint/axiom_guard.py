#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

axiom_guard.py

Enforces two invariants for the canonical axiomatic file:
1. Hard termination: no non‑whitespace content exists after the termination marker line.
2. Tag compliance: every theorem/lemma/corollary/conjecture line contains an allowed status tag.

Exit codes:
 0 success
 1 violation(s) found

Usage:
  python tools/axiom_guard.py --file Derivation/axiomatic_theory_development.md

Integrate into CI / pre-commit to prevent accidental tail re-growth or untagged claims.
"""
from __future__ import annotations
import argparse, sys, re, pathlib

TERMINATION_PREFIX = "End of truth"
ALLOWED_TAGS = {"[THEOREM-PROVEN]","[LEMMA-PROVEN]","[COROLLARY]","[CONJECTURE]","[NUM-EVIDENCE]","[IDENTITY]","[AXIOM]","[EFT-KG]","[LIMIT-ASSUMPTIONS]"}
# Headings that must carry a tag (case-insensitive search for keywords below)
REQUIRES_TAG = re.compile(r"^(?:##+\s+)(Theorem|Lemma|Corollary|Conjecture|Identity|Derivation|Axiom)", re.IGNORECASE)
TAG_PATTERN = re.compile(r"\[(?:THEOREM-PROVEN|LEMMA-PROVEN|COROLLARY|CONJECTURE|NUM-EVIDENCE|IDENTITY|AXIOM|EFT-KG|LIMIT-ASSUMPTIONS)\]")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Path to axiomatic markdown file")
    args = ap.parse_args()
    path = pathlib.Path(args.file)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. Termination enforcement
    term_index = None
    for i,l in enumerate(lines):
        if l.startswith(TERMINATION_PREFIX):
            term_index = i
            break
    if term_index is None:
        print("[axiom-guard] ERROR: termination marker not found (prefix '", TERMINATION_PREFIX, "')")
        sys.exit(1)

    # Allowed tail lines: termination line itself and the explicit file terminates note (next line) plus optional blank line(s)
    tail = lines[term_index+1:]
    violations = []
    for t in tail:
        if t.strip() == "":
            continue
        if t.startswith("[File terminates here intentionally"):
            continue
        if t.strip().startswith("<!--"):
            continue
        violations.append(f"Unexpected content after termination marker: '{t[:80]}'")

    # 2. Tag compliance scan (only above termination)
    for i,l in enumerate(lines[:term_index]):
        if REQUIRES_TAG.search(l):
            if not TAG_PATTERN.search(l):
                violations.append(f"Line {i+1} heading missing required tag: {l.strip()}")
        # Also check that any bracketed tag-like token is one of the allowed
        for m in re.finditer(r"\[(.*?)\]", l):
            token = f"[{m.group(1)}]"
            if token.startswith("[") and token in ALLOWED_TAGS:
                continue
            # Skip markdown link constructs [text](...) by detecting '(' immediately after closing bracket
            after = l[m.end():m.end()+1]
            if after == '(':
                continue
            # If it looks like an ALLCAPS tag but not allowed, flag it
            if token.upper() == token and token not in ALLOWED_TAGS:
                violations.append(f"Unrecognized tag token {token} on line {i+1}")

    if violations:
        print("[axiom-guard] FAIL:")
        for v in violations:
            print(" -", v)
        sys.exit(1)
    else:
        print("[axiom-guard] PASS: termination + tag compliance OK")
        sys.exit(0)

if __name__ == "__main__":
    main()
