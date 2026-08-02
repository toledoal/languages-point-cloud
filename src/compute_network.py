#!/usr/bin/env python3
"""System point cloud — a reconstruction-free pairwise DISSIMILARITY between language systems, MDS layout, and a
nearest-neighbour network. The input is concept-aligned lexical data (NOT "phonology alone"): coderivative sets
are detected statistically with LexStat, and only then is phonology compared.

Dissimilarity d(ℓ,ℓ') = mean, over aligned consonant slots between coderivative sets of the two languages, of the
number of primary phonological features that differ (identity = 0). It is PAIRWISE (keeps information a marginal
profile discards), reconstruction-free and family-tree-free (family membership only delimits the field; no branch
labels enter d). Undefined pairs are NEVER imputed: the analysis matrix is the MAXIMUM observed clique (exact
Bron–Kerbosch). We embed with classical MDS and connect each system to its k nearest neighbours; branch labels are
used ONLY afterwards, to colour and score (purity, silhouette), never to build.

Requires a Lexibank-style CLDF lexicon (forms.csv, languages.csv) pointed at by $LEX_PATH. Outputs (bundled so the
figure reproduces without the corpus): data/results/network_{coords,edges,dist}_<slug>.csv (slug ie/an/nd).

Usage:  LEX_PATH=/path/to/lexibank FAMILY="Indo-European" ./.venv/bin/python src/compute_network.py
"""
import logging; logging.disable(logging.INFO)
import os, csv, math, random
from collections import defaultdict
import numpy as np
import panphon
from branches import branch_map

SEED = int(os.environ.get("SEED", "20260802"))


def _seed():
    """Seed the RNGs LexStat's get_scorer draws from, so runs are reproducible."""
    random.seed(SEED); np.random.seed(SEED)


def cache_path(prefix):
    """Cache filename keyed by the FULL config (family, maxlang, threshold, seed, corpus path) so a run with any
    different configuration cannot silently reuse a stale cache."""
    import hashlib
    cfg = "|".join(str(x) for x in (FAMILY, MAXLANG, os.environ.get("THR", "0.55"), SEED, os.path.realpath(LEX)))
    h = hashlib.md5(cfg.encode()).hexdigest()[:10]
    return os.path.join(HERE, "..", "data", "db", f"{prefix}_{MAXLANG}_{h}.pkl")

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
LEX = os.environ.get("LEX_PATH", os.path.join(HERE, "..", "..", "..", "data", "lexicon", "lexibank"))
FAMILY = os.environ.get("FAMILY", "Indo-European")
SLUG = os.environ.get("SLUG") or {"Indo-European": "ie", "Austronesian": "an", "Nakh-Daghestanian": "nd"}.get(FAMILY, FAMILY.split("-")[0].lower())
MAXLANG = int(os.environ.get("MAXLANG", "50"))
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


def max_cliques(cand, observed):
    """All MAXIMUM cliques of the observed-distance graph over `cand` (Bron–Kerbosch w/ pivot + size bound).
    `observed(a,b)` → True if the pair's distance is defined. Returns (best_size, list_of_cliques)."""
    import itertools
    adj = {u: set() for u in cand}
    for a, b in itertools.combinations(cand, 2):
        if observed(a, b):
            adj[a].add(b); adj[b].add(a)
    best = [0]; found = []

    def bk(R, P, X):
        if not P and not X:
            if len(R) > best[0]:
                best[0] = len(R); found.clear(); found.append(set(R))
            elif len(R) == best[0]:
                found.append(set(R))
            return
        if len(R) + len(P) < best[0]:
            return
        pivot = max(P | X, key=lambda u: len(adj[u] & P))
        for v in list(P - adj[pivot]):
            bk(R | {v}, P & adj[v], X & adj[v])
            P = P - {v}; X = X | {v}
    bk(set(), set(cand), set())
    return best[0], found


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
    _seed(); lex = LexStat(tsv); lex.get_scorer(runs=100); lex.cluster(method="lexstat", threshold=THR, ref="cogid")
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

    def build_D(ls):
        m = len(ls); M = np.full((m, m), np.nan)
        for i in range(m):
            M[i, i] = 0.0
        for i in range(m):
            for j in range(i+1, m):
                p = tuple(sorted((ls[i], ls[j])))
                if NS.get(p, 0) >= MINSLOT:
                    M[i, j] = M[j, i] = SUM[p]/NS[p]
        return M

    # NO global-mean imputation (it manufactures equidistance / flatness). Main analysis uses the MAXIMUM
    # complete observed submatrix: the maximum clique of the graph whose edges are observed (>=MINSLOT) pairs.
    n_all = len(keep)
    Dfull = build_D(keep)
    miss_before = int(np.isnan(Dfull[np.triu_indices(n_all, 1)]).sum())
    total_before = n_all*(n_all-1)//2
    observed = lambda a, b: NS.get(tuple(sorted((a, b))), 0) >= MINSLOT
    size, cliques = max_cliques(keep, observed)
    chosen = cliques[0]
    keep = [l for l in keep if l in chosen]           # preserve deterministic input order
    n = len(keep); idx = {l: i for i, l in enumerate(keep)}
    Dm = build_D(keep)
    labels = [assign[l] for l in keep]
    print(f"missingness: {miss_before}/{total_before} pairs unobserved (<{MINSLOT} slots) among {n_all} doculects")
    print(f"maximum complete submatrix (max clique): {n}/{n_all} doculects; "
          f"{len(cliques)} maximum clique(s) of size {size}; 0 imputed values")
    print(f"kept: {', '.join(name.get(l, l) for l in keep)}")

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
