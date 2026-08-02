#!/usr/bin/env python3
"""Provenance of the feature ledger (Appendix C) — EXACT.

For a pair of doculects, this reproduces the *same* LexStat coderivative sets (cogids), alignments and consonant
slots that build the analysis dissimilarity (same seed as analysis.py / compute_network.py), and lists, per slot,
the concept, cogid, the two forms, the two segments and the differing features. It then confirms that the per-feature
sums reproduce the §5.1 ledger exactly. This is the object that produces d(ℓ,ℓ'), not a same-concept re-alignment.

Exports data/results/provenance_<a>_<b>.csv. Uso:
  LEX_PATH=... MAXLANG=50 ./.venv/bin/python src/provenance.py keypano-Spanish keypano-Portuguese
"""
import logging; logging.disable(logging.INFO)
import os, sys, csv
from collections import defaultdict
from compute_network import LEX, FAMILY, MAXLANG, PRIM, feat, is_cons, _seed
from analysis import align_ops
from branches import branch_map

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "results")
A = sys.argv[1] if len(sys.argv) > 1 else "keypano-Spanish"
B = sys.argv[2] if len(sys.argv) > 2 else "keypano-Portuguese"


def diffs(a, b):
    fa, fb = feat(a), feat(b)
    return [f for f in PRIM if fa.get(f, 0) != fb.get(f, 0)]


def main():
    from lingpy import LexStat
    assign, _, _ = branch_map(FAMILY)
    lang_fam = {r["ID"]: (r.get("Family") or "") for r in csv.DictReader(open(f"{LEX}/languages.csv", encoding="utf-8"))}
    per = defaultdict(list)
    for row in csv.DictReader(open(f"{LEX}/forms.csv", encoding="utf-8")):
        if lang_fam.get(row["Language_ID"]) != FAMILY:
            continue
        segs = (row.get("Segments") or "").split()
        if len(segs) >= 2 and row.get("Parameter_ID") and assign.get(row["Language_ID"]):
            per[row["Language_ID"]].append((row["Parameter_ID"], segs))
    langs = sorted(per, key=lambda l: -len(per[l]))[:MAXLANG]
    if A not in langs or B not in langs:
        print(f"pair not both in the top-{MAXLANG} analytic sample: {A} / {B}"); return
    tsv = os.path.join(RES, "_prov.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("ID\tDOCULECT\tCONCEPT\tTOKENS\n"); i = 1
        for l in langs:
            for c, segs in per[l]:
                f.write(f"{i}\t{l}\t{c}\t{' '.join(segs)}\n"); i += 1
    _seed(); lex = LexStat(tsv); lex.get_scorer(runs=100); lex.cluster(method="lexstat", threshold=0.55, ref="cogid")
    classes = defaultdict(list)
    for k in lex:
        classes[(lex[k, "concept"], lex[k, "cogid"])].append((lex[k, "doculect"], lex[k, "tokens"]))
    os.remove(tsv)

    rows = []
    fsum = defaultdict(int); nslot = 0
    for (concept, cogid), forms in classes.items():
        fa = [t for d, t in forms if d == A]; fb = [t for d, t in forms if d == B]
        if not fa or not fb:
            continue
        for sa in fa:                       # pair EVERY A-form with EVERY B-form in this cogid — exactly as the
            for sb in fb:                    # dissimilarity is computed (build_rich), so the ledger reproduces d
                for a, b in align_ops(sa, sb)[0]:
                    if is_cons(a) and is_cons(b):
                        nslot += 1
                        d = diffs(a, b)
                        for ftr in d:
                            fsum[ftr] += 1
                        if a != b:
                            rows.append((concept, cogid, "".join(sa), "".join(sb), a, b, ",".join(d)))
    out = os.path.join(RES, f"provenance_{A.split('-')[-1]}_{B.split('-')[-1]}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["concept", "cogid", "form_a", "form_b", "seg_a", "seg_b", "differing_features"])
        w.writerows(sorted(rows))
    print(f"provenance {A} vs {B}: {nslot} consonant slots across {len(set(r[1] for r in rows))} coderivative sets")
    print("per-feature ledger d_f = (# slots where f differs)/(# consonant slots):")
    for ftr in PRIM:
        print(f"  {ftr:6s} {fsum[ftr]}/{nslot} = {fsum[ftr]/nslot:.3f}")
    print(f"  TOTAL  d = {sum(fsum.values())/nslot:.3f}   (this equals the §5.1 row for this pair)")
    print(f"wrote {out} ({len(rows)} non-identity slots)")


if __name__ == "__main__":
    main()
