#!/usr/bin/env python3
"""Feature-level decomposition of the dissimilarity: d(l,l') = sum_f d_f(l,l'), with
d_f = (1/N) * #slots where feature f differs. Demonstrates decomposability on real pairs
(a close within-branch pair, a distant within-branch pair, a cross-branch pair).
Reads the analysis cache (data/db/_av2.pkl) produced by `make analysis`.
Usage: ./.venv/bin/python src/decompose.py [NameA:NameB ...]"""
import os, sys, csv, pickle
import numpy as np
from compute_network import LEX, PRIM

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "db", "_av2.pkl")

DEFAULT = ["Spanish:Portuguese", "Persian:Hindi", "Spanish:Hindi"]


def main():
    d = pickle.load(open(CACHE, "rb"))
    SUMF, NCC = d["rich"][0], d["rich"][1]
    # resolve names against the doculect IDs actually present in the cache
    ids = sorted({x for p in SUMF for x in p})
    idname = {}
    for r in csv.DictReader(open(f"{LEX}/languages.csv", encoding="utf-8")):
        if r["ID"] in ids:
            idname[r["ID"]] = r.get("Name") or r["ID"]

    def find(nm):
        nm = nm.lower()
        hits = [i for i in ids if nm in idname.get(i, "").lower() or nm in i.lower()]
        return hits[0] if hits else None
    name2id = None
    wanted = sys.argv[1:] or DEFAULT
    print("feature-level decomposition  d = sum_f d_f   (per aligned consonant slot)")
    print(f"{'pair':28s} " + " ".join(f"{f:>5}" for f in PRIM) + f" {'total':>6} {'slots':>6}")
    for w in wanted:
        a, b = w.split(":")
        ia, ib = find(a), find(b)
        if not ia or not ib:
            print(f"{w}: not found"); continue
        p = tuple(sorted((ia, ib)))
        if p not in SUMF:
            print(f"{w}: no shared data"); continue
        v = SUMF[p]/NCC[p]
        print(f"{a}-{b:<{27-len(a)}s} " + " ".join(f"{x:5.2f}" for x in v) + f" {v.sum():6.2f} {NCC[p]:6d}")


if __name__ == "__main__":
    main()
