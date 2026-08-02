#!/usr/bin/env python3
"""System point cloud — reconstruction-free pairwise distance between language systems, MDS layout, and a
nearest-neighbour network, computed from phonological correspondences alone.

Distance d(ℓ,ℓ') = mean, over aligned consonant slots between statistically detected coderivative sets of the two
languages, of the number of primary phonological features that differ (identity = 0). It is PAIRWISE (it keeps the
information a per-language marginal profile discards), reconstruction-free, and family-tree-free. We then embed the
distance matrix with classical MDS and connect each system to its k nearest neighbours. Branch labels are used
ONLY afterwards, to colour and score the picture (neighbour purity, silhouette) — never to build it.

Requires a Lexibank-style CLDF lexicon (forms.csv, languages.csv) pointed at by $LEX_PATH. Outputs (bundled in the
repo so the figure reproduces without the corpus): data/results/network_{coords,edges,dist}_<slug>.csv (slug ie/an).

Usage:  LEX_PATH=/path/to/lexibank FAMILY="Indo-European" ./.venv/bin/python src/compute_network.py
"""
import logging; logging.disable(logging.INFO)
import os, csv, math
from collections import defaultdict
import numpy as np
import panphon
from branches import branch_map

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
LEX = os.environ.get("LEX_PATH", os.path.join(HERE, "..", "..", "..", "data", "lexicon", "lexibank"))
FAMILY = os.environ.get("FAMILY", "Indo-European")
SLUG = os.environ.get("SLUG") or {"Indo-European": "ie", "Austronesian": "an"}.get(FAMILY, FAMILY.split("-")[0].lower())
MAXLANG = int(os.environ.get("MAXLANG", "28"))
MINSLOT = int(os.environ.get("MINSLOT", "40"))
KNN = int(os.environ.get("KNN", "3"))
THR = float(os.environ.get("THR", "0.55"))
PRIM = ["cont", "voi", "nas", "ant", "cor", "lab", "back", "round", "strid", "hi", "lo", "son"]
CREOLE_MARK = ("creole", "jamaic", "negerhol", "sranan", "papiam", "krio", "pidgin", "saramacc", "seychelles")
FT = panphon.FeatureTable(); _vc = {}


def feat(ph):
    if ph not in _vc:
        v = FT.word_to_vector_list(ph.replace("g", "ɡ"), numeric=True)
        _vc[ph] = dict(zip(FT.names, v[0])) if len(v) == 1 else None
    return _vc[ph]


def is_cons(ph):
    f = feat(ph); return f is not None and f.get("syl", 0) != 1


def fd(a, b):
    fa, fb = feat(a), feat(b)
    if fa is None or fb is None:
        return None
    return sum(1 for k in PRIM if fa.get(k, 0) != fb.get(k, 0))


def cost(a, b):
    if a == b:
        return 0.0
    fa, fb = feat(a), feat(b)
    if fa is None or fb is None:
        return 1.0
    return sum(1 for k in FT.names if fa.get(k, 0) != fb.get(k, 0)) / len(FT.names)


def align(s, t):
    n, m = len(s), len(t)
    D = [[0.0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        D[i][0] = i
    for j in range(1, m+1):
        D[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            D[i][j] = min(D[i-1][j-1]+cost(s[i-1], t[j-1]), D[i-1][j]+1, D[i][j-1]+1)
    out, i, j = [], n, m
    while i > 0 and j > 0:
        if abs(D[i][j]-(D[i-1][j-1]+cost(s[i-1], t[j-1]))) < 1e-9:
            out.append((s[i-1], t[j-1])); i -= 1; j -= 1
        elif abs(D[i][j]-(D[i-1][j]+1)) < 1e-9:
            i -= 1
        else:
            j -= 1
    return out[::-1]


def mds(D):
    n = D.shape[0]; J = np.eye(n) - np.ones((n, n))/n
    B = -0.5 * J @ (D**2) @ J
    w, V = np.linalg.eigh(B); idx = np.argsort(-w)
    L = np.clip(w[idx][:2], 0, None)
    return V[:, idx][:, :2] * np.sqrt(L)


def silhouette(D, labels):
    n = len(labels); s = []
    for i in range(n):
        same = [D[i, j] for j in range(n) if j != i and labels[j] == labels[i]]
        if not same:
            continue
        a = np.mean(same)
        others = defaultdict(list)
        for j in range(n):
            if labels[j] != labels[i]:
                others[labels[j]].append(D[i, j])
        if not others:
            continue
        b = min(np.mean(v) for v in others.values())
        s.append((b-a)/max(a, b))
    return float(np.mean(s)) if s else float("nan")


def main():
    from lingpy import LexStat
    assign, _, _ = branch_map(FAMILY)
    lang_fam, name = {}, {}
    for r in csv.DictReader(open(f"{LEX}/languages.csv", encoding="utf-8")):
        lang_fam[r["ID"]] = r.get("Family") or ""; name[r["ID"]] = r.get("Name") or r["ID"]
    per = defaultdict(list)
    for row in csv.DictReader(open(f"{LEX}/forms.csv", encoding="utf-8")):
        if lang_fam.get(row["Language_ID"]) != FAMILY:
            continue
        segs = (row.get("Segments") or "").split()
        if len(segs) >= 2 and row.get("Parameter_ID") and assign.get(row["Language_ID"]):
            per[row["Language_ID"]].append((row["Parameter_ID"], segs))
    langs = sorted(per, key=lambda l: -len(per[l]))[:MAXLANG]
    tsv = os.path.join(RES, f"_tn_{SLUG}.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("ID\tDOCULECT\tCONCEPT\tTOKENS\n"); i = 1
        for l in langs:
            for c, segs in per[l]:
                f.write(f"{i}\t{l}\t{c}\t{' '.join(segs)}\n"); i += 1
    lex = LexStat(tsv); lex.get_scorer(runs=100); lex.cluster(method="lexstat", threshold=THR, ref="cogid")
    classes = defaultdict(list)
    for k in lex:
        classes[(lex[k, "concept"], lex[k, "cogid"])].append((lex[k, "doculect"], lex[k, "tokens"]))
    SUM = defaultdict(float); NS = defaultdict(int)
    for _, forms in classes.items():
        for x in range(len(forms)):
            for y in range(x+1, len(forms)):
                la, sa = forms[x]; lb, sb = forms[y]
                if la == lb:
                    continue
                pair = tuple(sorted((la, lb)))
                for a, b in align(sa, sb):
                    if is_cons(a) and is_cons(b):
                        d = fd(a, b)
                        if d is not None:
                            SUM[pair] += d; NS[pair] += 1

    keep = [l for l in langs if any(NS.get(tuple(sorted((l, o))), 0) >= MINSLOT for o in langs if o != l)]
    n = len(keep); idx = {l: i for i, l in enumerate(keep)}
    Dm = np.full((n, n), np.nan)
    for i in range(n):
        Dm[i, i] = 0.0
    for i in range(n):
        for j in range(i+1, n):
            p = tuple(sorted((keep[i], keep[j])))
            if NS.get(p, 0) >= MINSLOT:
                Dm[i, j] = Dm[j, i] = SUM[p]/NS[p]
    glob = np.nanmean(Dm[~np.eye(n, dtype=bool)])
    Dm = np.where(np.isnan(Dm), glob, Dm)
    labels = [assign[l] for l in keep]

    brc = defaultdict(int)
    for l in keep:
        brc[assign[l]] += 1
    multi = [l for l in keep if brc[assign[l]] > 1 and not any(m in name[l].lower() for m in CREOLE_MARK)]
    hit = sum(1 for l in multi if assign[keep[sorted((j for j in range(n) if j != idx[l]),
              key=lambda j: Dm[idx[l], j])[0]]] == assign[l])
    print(f"=== system point cloud · {FAMILY} · {n} languages ===")
    print(f"nearest-neighbour purity (multi-branch, no creoles) = {hit}/{len(multi)} = {hit/len(multi):.2f}")
    print(f"silhouette by branch = {silhouette(Dm, labels):+.3f}")

    edges = []
    for l in keep:
        i = idx[l]
        for j in sorted((j for j in range(n) if j != i), key=lambda j: Dm[i, j])[:KNN]:
            edges.append((name[l], name[keep[j]], round(float(Dm[i, j]), 3)))
    coords = mds(Dm)
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, f"network_coords_{SLUG}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["lang", "name", "branch", "x", "y"])
        for l in keep:
            i = idx[l]; w.writerow([l, name[l], assign[l], f"{coords[i,0]:.4f}", f"{coords[i,1]:.4f}"])
    with open(os.path.join(RES, f"network_edges_{SLUG}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["src", "dst", "dist"])
        for a, b, dd in edges:
            w.writerow([a, b, dd])
    np.savetxt(os.path.join(RES, f"network_dist_{SLUG}.csv"), Dm, fmt="%.4f", delimiter=",",
               header=",".join(name[l] for l in keep), comments="")
    os.remove(tsv)
    print(f"wrote data/results/network_{{coords,edges,dist}}_{SLUG}.csv")


if __name__ == "__main__":
    main()
