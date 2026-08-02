#!/usr/bin/env python3
"""Provenance demo (Appendix C): for a pair of doculects, show — per concept — the aligned consonant slots and the
features that differ, i.e. WHERE each unit of the feature-difference ledger comes from. Aligns same-concept forms
directly (no cognate filter needed to illustrate the mechanism). Reads the corpus via LEX_PATH.
Usage: ./.venv/bin/python src/provenance.py keypano-Spanish keypano-Portuguese [N_CONCEPTS]"""
import os, sys, csv
from collections import defaultdict
from compute_network import LEX, PRIM, feat, is_cons, align

A = sys.argv[1] if len(sys.argv) > 1 else "keypano-Spanish"
B = sys.argv[2] if len(sys.argv) > 2 else "keypano-Portuguese"
N = int(sys.argv[3]) if len(sys.argv) > 3 else 6


def load(doc):
    out = defaultdict(list)
    for row in csv.DictReader(open(f"{LEX}/forms.csv", encoding="utf-8")):
        if row["Language_ID"] == doc and row.get("Parameter_ID"):
            segs = (row.get("Segments") or "").split()
            if len(segs) >= 2:
                out[row["Parameter_ID"]].append(segs)
    return out


def diffs(a, b):
    fa, fb = feat(a), feat(b)
    if fa is None or fb is None:
        return []
    return [f for f in PRIM if fa.get(f, 0) != fb.get(f, 0)]


fa, fb = load(A), load(B)
shared = sorted(set(fa) & set(fb))
print(f"provenance: {A}  vs  {B}   ({len(shared)} shared concepts; showing first {N} with a consonant difference)")
print(f"{'concept':22s} {'form A':16s} {'form B':16s} {'aligned Δ (cons slots)':40s}")
shown = 0
for c in shared:
    sa, sb = fa[c][0], fb[c][0]
    slots = []
    for x, y in align(sa, sb):
        if is_cons(x) and is_cons(y) and x != y:
            d = diffs(x, y)
            if d:
                slots.append(f"{x}/{y}:{{{','.join(d)}}}")
    if slots:
        print(f"{c[:22]:22s} {''.join(sa)[:16]:16s} {''.join(sb)[:16]:16s} {'  '.join(slots)}")
        shown += 1
        if shown >= N:
            break
