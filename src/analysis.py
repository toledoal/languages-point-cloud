#!/usr/bin/env python3
"""PAPER "Point Cloud" · analysis v2 — the numbers the adversarial review requires (kept faithful to our objective:
reconstruction-free, tree-free, discover-then-contrast; branch signal legible in the distribution).

Produces, from one real LexStat pass (rich per-pair stats incl. gaps) plus a no-LexStat all-concept baseline:
  1. Valid significance: LABEL-PERMUTATION test on the fixed dissimilarity (10k) → empirical p for purity & silhouette.
     (Replaces the invalid "4.4σ from 3 permutations".)
  2. MDS diagnostics: eigenvalue spectrum, negative inertia, %variance in 2D (is the plane a faithful shadow?).
  3. Purity done honestly: Wilson CI; all doculects; multi-branch only; macro-by-branch; near-duplicate dedup.
  4. Coverage: per-pair #concepts, #sets, cons-cons slots, gaps, %discarded; correlation d↔coverage; d_change/d_cov.
  5. Full cross-branch nearest-neighbour table + residual proximity (closer than the branch baseline).
  6. Baselines: (a) marginal per-language profile; (b) all-same-concept-pairs distance WITHOUT LexStat selection
     (the double-dipping control); (c) normalized edit distance on consonant skeletons.
Caches the rich pass in data/db/_av2.pkl. Uso: ./.venv/bin/python src/analysis_v2.py
"""
import logging; logging.disable(logging.INFO)
import os, csv, math, random, pickle
from collections import defaultdict, Counter
import numpy as np
from branches import branch_map
from compute_network import feat, is_cons, cost, LEX, FAMILY, MAXLANG, PRIM, _seed, cache_path

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
CACHE = cache_path("_av2")
MINSLOT = 40
DEDUP_D = 1.3           # collapse near-duplicate systems below this dissimilarity
CREOLE_MARK = ("creole", "jamaic", "negerhol", "sranan", "papiam", "krio", "pidgin", "saramacc", "seychelles")
B_PERM = 10000


def fdcount(a, b):
    fa, fb = feat(a), feat(b)
    if fa is None or fb is None:
        return None
    return sum(1 for k in PRIM if fa.get(k, 0) != fb.get(k, 0)), \
        np.array([1 if fa.get(f, 0) != fb.get(f, 0) else 0 for f in PRIM])


def align_ops(s, t):
    """Needleman–Wunsch by feature cost; return (aligned_pairs, n_gap)."""
    n, m = len(s), len(t)
    D = [[0.0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        D[i][0] = i
    for j in range(1, m+1):
        D[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            D[i][j] = min(D[i-1][j-1]+cost(s[i-1], t[j-1]), D[i-1][j]+1, D[i][j-1]+1)
    pairs, gap, i, j = [], 0, n, m
    while i > 0 and j > 0:
        if abs(D[i][j]-(D[i-1][j-1]+cost(s[i-1], t[j-1]))) < 1e-9:
            pairs.append((s[i-1], t[j-1])); i -= 1; j -= 1
        elif abs(D[i][j]-(D[i-1][j]+1)) < 1e-9:
            gap += 1; i -= 1
        else:
            gap += 1; j -= 1
    gap += i + j
    return pairs[::-1], gap


def skeleton(segs):
    return [x for x in segs if is_cons(x)]


def lev(a, b):
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 0.0
    d = list(range(m+1))
    for i in range(1, n+1):
        prev, d[0] = d[0], i
        for j in range(1, m+1):
            cur = d[j]
            d[j] = min(d[j]+1, d[j-1]+1, prev+(a[i-1] != b[j-1]))
            prev = cur
    return d[m]/max(n, m)


def load_forms():
    assign, _, _ = branch_map(FAMILY)
    lang_fam, name, gcode = {}, {}, {}
    for r in csv.DictReader(open(f"{LEX}/languages.csv", encoding="utf-8")):
        lang_fam[r["ID"]] = r.get("Family") or ""; name[r["ID"]] = r.get("Name") or r["ID"]
        gcode[r["ID"]] = r.get("Glottocode", "")
    per = defaultdict(list)
    for row in csv.DictReader(open(f"{LEX}/forms.csv", encoding="utf-8")):
        if lang_fam.get(row["Language_ID"]) != FAMILY:
            continue
        segs = (row.get("Segments") or "").split()
        if len(segs) >= 2 and row.get("Parameter_ID") and assign.get(row["Language_ID"]):
            per[row["Language_ID"]].append((row["Parameter_ID"], segs))
    langs = sorted(per, key=lambda l: -len(per[l]))[:MAXLANG]
    return per, langs, assign, name, gcode


def build_rich(per, langs):
    """One real LexStat pass. Per pair: SUMF(12), n_cc, n_gap, n_concepts, n_sets. Also all-concept baseline."""
    from lingpy import LexStat
    tsv = os.path.join(RES, "_av2.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("ID\tDOCULECT\tCONCEPT\tTOKENS\n"); i = 1
        for l in langs:
            for c, segs in per[l]:
                f.write(f"{i}\t{l}\t{c}\t{' '.join(segs)}\n"); i += 1
    _seed(); lex = LexStat(tsv); lex.get_scorer(runs=100); lex.cluster(method="lexstat", threshold=0.55, ref="cogid")
    classes = defaultdict(list)
    for k in lex:
        classes[(lex[k, "concept"], lex[k, "cogid"])].append((lex[k, "doculect"], lex[k, "tokens"]))
    SUMF = defaultdict(lambda: np.zeros(len(PRIM))); NCC = defaultdict(int)
    NGAP = defaultdict(int); NSET = defaultdict(int); CONC = defaultdict(set)
    for (concept, _), forms in classes.items():
        for x in range(len(forms)):
            for y in range(x+1, len(forms)):
                la, sa = forms[x]; lb, sb = forms[y]
                if la == lb:
                    continue
                pair = tuple(sorted((la, lb))); NSET[pair] += 1; CONC[pair].add(concept)
                pairs, gap = align_ops(sa, sb); NGAP[pair] += gap
                for a, b in pairs:
                    if is_cons(a) and is_cons(b):
                        r = fdcount(a, b)
                        if r:
                            SUMF[pair] += r[1]; NCC[pair] += 1
    os.remove(tsv)
    return ({k: v for k, v in SUMF.items()}, dict(NCC), dict(NGAP), dict(NSET),
            {k: len(v) for k, v in CONC.items()})


def build_allconcept(per, langs):
    """No-LexStat baseline: align EVERY same-concept cross-language form pair (no coderivation filter)."""
    byc = defaultdict(lambda: defaultdict(list))
    for l in langs:
        for c, segs in per[l]:
            byc[c][l].append(segs)
    SUMF = defaultdict(lambda: np.zeros(len(PRIM))); NCC = defaultdict(int)
    LEVs = defaultdict(list)
    for c, ld in byc.items():
        ls = list(ld)
        for x in range(len(ls)):
            for y in range(x+1, len(ls)):
                la, lb = ls[x], ls[y]; pair = tuple(sorted((la, lb)))
                for sa in ld[la][:1]:
                    for sb in ld[lb][:1]:
                        pairs, _ = align_ops(sa, sb)
                        for a, b in pairs:
                            if is_cons(a) and is_cons(b):
                                r = fdcount(a, b)
                                if r:
                                    SUMF[pair] += r[1]; NCC[pair] += 1
                        LEVs[pair].append(lev(skeleton(sa), skeleton(sb)))
    return {k: v for k, v in SUMF.items()}, dict(NCC), {k: float(np.mean(v)) for k, v in LEVs.items()}


def dmatrix(SUMF, NCC, langs, minslot=MINSLOT):
    """MAXIMUM complete observed submatrix (max clique of the observed-pair graph) — NO imputation."""
    from compute_network import max_cliques
    keep = [l for l in langs if any(NCC.get(tuple(sorted((l, o))), 0) >= minslot for o in langs if o != l)]

    def build(ls):
        m = len(ls); M = np.full((m, m), np.nan)
        for i in range(m):
            M[i, i] = 0.0
        for i in range(m):
            for j in range(i+1, m):
                p = tuple(sorted((ls[i], ls[j])))
                if NCC.get(p, 0) >= minslot:
                    M[i, j] = M[j, i] = SUMF[p].sum()/NCC[p]
        return M
    _, cliques = max_cliques(keep, lambda a, b: NCC.get(tuple(sorted((a, b))), 0) >= minslot)
    chosen = cliques[0]
    keep = [l for l in keep if l in chosen]
    idx = {l: i for i, l in enumerate(keep)}
    return build(keep), keep, idx


def valmatrix(M, keep):
    """Dense matrix from a pair→value dict over `keep`. NO imputation: undefined pairs are an error (the caller
    must pass a keep-set on which every pair is observed, e.g. a max clique)."""
    n = len(keep); D = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            v = M.get(tuple(sorted((keep[i], keep[j]))))
            if v is None or (isinstance(v, float) and np.isnan(v)):
                raise ValueError(f"undefined baseline pair ({keep[i]},{keep[j]}): pass a complete observed submatrix")
            D[i, j] = D[j, i] = v
    return D


def silhouette(D, labels):
    n = len(labels); s = []
    for i in range(n):
        same = [D[i, j] for j in range(n) if j != i and labels[j] == labels[i]]
        if not same:
            continue
        a = np.mean(same); oth = defaultdict(list)
        for j in range(n):
            if labels[j] != labels[i]:
                oth[labels[j]].append(D[i, j])
        if not oth:
            continue
        b = min(np.mean(v) for v in oth.values()); den = max(a, b)
        s.append((b-a)/den if den > 0 else 0.0)
    return float(np.mean(s)) if s else float("nan")


def nn_purity(D, labels):
    """fraction of items (whose label appears >1) whose nearest neighbour shares the label. Returns (p,k,hit)."""
    n = len(labels); cnt = Counter(labels)
    multi = [i for i in range(n) if cnt[labels[i]] > 1]
    if not multi:
        return float("nan"), 0, 0
    hit = 0
    for i in multi:
        j = min((k for k in range(n) if k != i), key=lambda k: D[i, k])
        if labels[j] == labels[i]:
            hit += 1
    return hit/len(multi), len(multi), hit


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    half = (z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/d
    return (c-half, c+half)


def perm_test(D, labels, statfn, seed=0, B=B_PERM):
    obs = statfn(D, labels); rng = random.Random(seed); ge = 0; nulls = []
    lab = list(labels)
    for _ in range(B):
        rng.shuffle(lab); v = statfn(D, lab); nulls.append(v)
        if v >= obs - 1e-12:
            ge += 1
    return obs, (ge+1)/(B+1), float(np.mean(nulls)), float(np.std(nulls)), float(np.percentile(nulls, 95))


def mds_diag(D):
    n = D.shape[0]; J = np.eye(n)-np.ones((n, n))/n
    Bm = -0.5*J@(D**2)@J
    w = np.sort(np.linalg.eigvalsh(Bm))[::-1]
    pos = w[w > 0].sum(); neg = -w[w < 0].sum()
    return w, pos, neg, (w[0]+w[1])/pos if pos > 0 else float("nan"), neg/(pos+neg) if pos+neg > 0 else float("nan")


def dedup(D, keep, thr=DEDUP_D):
    """greedily drop one of each near-duplicate pair (d<thr); keep the earlier index."""
    n = len(keep); drop = set()
    for i in range(n):
        if i in drop:
            continue
        for j in range(i+1, n):
            if j not in drop and D[i, j] < thr:
                drop.add(j)
    keepidx = [i for i in range(n) if i not in drop]
    return keepidx, [keep[i] for i in drop]


def main():
    per, langs, assign, name, gcode = load_forms()
    if os.path.exists(CACHE):
        d = pickle.load(open(CACHE, "rb"))
        rich, allc = d["rich"], d["allc"]; print("(cache)")
    else:
        print("rich LexStat pass ..."); rich = build_rich(per, langs)
        print("all-concept baseline (no LexStat) ..."); allc = build_allconcept(per, langs)
        pickle.dump({"rich": rich, "allc": allc}, open(CACHE, "wb"))
    SUMF, NCC, NGAP, NSET, NCONC = rich
    aSUMF, aNCC, aLEV = allc

    D, keep, idx = dmatrix(SUMF, NCC, langs)
    n = len(keep)
    creole = {l for l in keep if any(m in name[l].lower() for m in CREOLE_MARK)}
    nc = [i for i in range(n) if keep[i] not in creole]           # non-creole indices
    lab_nc = [assign[keep[i]] for i in nc]
    Dnc = D[np.ix_(nc, nc)]
    print(f"\n=== ANALYSIS v2 · {FAMILY} · {n} doculects ({len(creole)} creoles) ===")

    # 1 — significance by label permutation (valid)
    op, pp, mp, sp, q95 = perm_test(Dnc, lab_nc, nn_purity_stat := (lambda D, L: nn_purity(D, L)[0]))
    os_, ps_, ms_, ss_, q95s = perm_test(Dnc, lab_nc, silhouette)
    print(f"[1] label-permutation test ({B_PERM}x, non-creole n={len(nc)}):")
    print(f"    purity     obs={op:.3f}  null={mp:.3f}±{sp:.3f}  p={pp:.4f}")
    print(f"    silhouette obs={os_:+.3f} null={ms_:+.3f}±{ss_:.3f}  p={ps_:.4f}")

    # 2 — MDS diagnostics
    w, pos, neg, var2, negfrac = mds_diag(D)
    print(f"[2] MDS diagnostics: top eigvals {np.round(w[:5],2)} ; %var in 2D = {100*var2:.1f}% ; "
          f"negative inertia = {100*negfrac:.1f}% of |eigen| (euclidean-ish if small)")

    # 3 — purity done honestly
    p_all, k_all, h_all = nn_purity(D, [assign[keep[i]] for i in range(n)])
    p_nc, k_nc, h_nc = nn_purity(Dnc, lab_nc)
    lo, hi = wilson(h_nc, k_nc)
    # macro by branch
    br = defaultdict(list)
    for i in nc:
        br[assign[keep[i]]].append(i)
    macro = []
    for b, ids in br.items():
        if len(ids) > 1:   # neighbours restricted to the non-creole universe `nc`, same as the headline metric
            hitb = sum(1 for i in ids if assign[keep[min((k for k in nc if k != i), key=lambda k: D[i, k])]] == b)
            macro.append(hitb/len(ids))
    keepidx, dropped = dedup(Dnc, [keep[i] for i in nc])
    lab_dd = [lab_nc[i] for i in keepidx]
    p_dd, k_dd, h_dd = nn_purity(Dnc[np.ix_(keepidx, keepidx)], lab_dd)
    print(f"[3] purity:  all-doculects={p_all:.3f} ({h_all}/{k_all})   "
          f"multi-branch non-creole={p_nc:.3f} ({h_nc}/{k_nc}) Wilson95 [{lo:.2f},{hi:.2f}]")
    print(f"    macro-by-branch mean={np.mean(macro):.3f}   "
          f"after near-dup dedup (d<{DEDUP_D}: dropped {len(dropped)})={p_dd:.3f} ({h_dd}/{k_dd})")

    # 3b — metadata control: ONE doculect per Glottocode. Representative by COVERAGE (total observed consonant
    # slots, a pre-D metadata quantity — NOT the outcome variable D), and we also enumerate ALL 2^k choices.
    cov = {i: sum(NCC.get(tuple(sorted((keep[i], keep[j]))), 0) for j in nc if j != i) for i in nc}
    gc_group = defaultdict(list)
    for i in nc:
        gc_group[gcode.get(keep[i], keep[i])].append(i)
    dup_gc = {g: [keep[i] for i in ids] for g, ids in gc_group.items() if len(ids) > 1}
    groups = list(gc_group.values())
    reps = [max(ids, key=lambda i: cov[i]) for ids in groups]     # coverage-based representative (metadata rule)
    p_gc, k_gc, h_gc = nn_purity(D[np.ix_(reps, reps)], [assign[keep[i]] for i in reps])
    # enumerate all combinations of representatives across duplicated glottocodes (2^k)
    import itertools
    dup_groups = [ids for ids in groups if len(ids) > 1]
    fixed = [ids[0] for ids in groups if len(ids) == 1]
    combo_p = []
    for choice in itertools.product(*dup_groups):
        sel = fixed + list(choice)
        pp3, _, _ = nn_purity(D[np.ix_(sel, sel)], [assign[keep[i]] for i in sel])
        combo_p.append(pp3)
    print(f"    ONE-per-Glottocode ({len(reps)} reps; collapsed {sum(len(v)-1 for v in dup_gc.values())} duplicates "
          f"across {len(dup_gc)} glottocodes): purity={p_gc:.3f} ({h_gc}/{k_gc}); "
          f"all {len(combo_p)} representative choices give purity in [{min(combo_p):.3f}, {max(combo_p):.3f}]")
    if dup_gc:
        print("    duplicate glottocodes: " + "; ".join(f"{g}:{len(v)}" for g, v in list(dup_gc.items())[:12]))

    # 3c — leave-one-dataset-out: drop each source dataset in turn, repurify on the rest (non-creole)
    dsof = {i: keep[i].split("-")[0] for i in nc}
    datasets = sorted(set(dsof.values()))
    lodo = []
    for ds in datasets:
        sub = [i for i in nc if dsof[i] != ds]
        if len(sub) >= 6:
            pp2, kk2, _ = nn_purity(D[np.ix_(sub, sub)], [assign[keep[i]] for i in sub])
            lodo.append(pp2)
    print(f"    leave-one-dataset-out ({len(datasets)} datasets): purity range [{min(lodo):.3f}, {max(lodo):.3f}]")

    # 3d — branch-cut sensitivity: relabel with several TF_BRANCH_MAXFRAC and repurify the SAME matrix
    print("    branch-cut sensitivity (TF_BRANCH_MAXFRAC):", end=" ")
    for mf in (0.25, 0.33, 0.5, 0.67):
        a2, _, _ = branch_map(FAMILY, maxfrac=mf)
        idx_nc = [i for i in nc if keep[i] in a2]
        pmf, kmf, _ = nn_purity(D[np.ix_(idx_nc, idx_nc)], [a2[keep[i]] for i in idx_nc])
        print(f"{mf}:{pmf:.3f}(n={kmf})", end="  ")
    print()

    # 4 — coverage (and export the full per-pair table for the reproducibility materials)
    covd = []
    pair_rows = []
    for i in range(n):
        for j in range(i+1, n):
            p = tuple(sorted((keep[i], keep[j])))
            cc = NCC.get(p, 0); gp = NGAP.get(p, 0)
            if cc >= MINSLOT:
                covd.append((D[i, j], cc, gp, NCONC.get(p, 0), NSET.get(p, 0)))
                pair_rows.append((keep[i], keep[j], round(float(D[i, j]), 4), NSET.get(p, 0),
                                  NCONC.get(p, 0), cc, gp, round(gp/(gp+cc), 4) if (gp+cc) else 0))
    with open(os.path.join(RES, "pair_stats_ie.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["doculect_a", "doculect_b", "d", "n_coderivative_sets", "n_shared_concepts",
                     "n_consonant_slots", "n_gaps", "gap_slot_ratio"])
        wr.writerows(pair_rows)
    covd = np.array(covd)
    r = np.corrcoef(covd[:, 0], covd[:, 1])[0, 1]
    print(f"[4] coverage per pair: cons-cons slots median={np.median(covd[:,1]):.0f} "
          f"[{covd[:,1].min():.0f}-{covd[:,1].max():.0f}]  gaps median={np.median(covd[:,2]):.0f}  "
          f"concepts median={np.median(covd[:,3]):.0f}")
    print(f"    corr(d, #slots) = {r:+.2f}   (near 0 ⇒ distance not driven by coverage)")

    # 5 — cross-branch nearest neighbours (full) + residual
    print("[5] ALL cross-branch nearest neighbours (obs d vs nearest same-branch d = residual):")
    for i in range(n):
        j = min((k for k in range(n) if k != i), key=lambda k: D[i, k])
        if assign[keep[j]] != assign[keep[i]]:
            same = [D[i, k] for k in range(n) if k != i and assign[keep[k]] == assign[keep[i]]]
            sb = min(same) if same else float("nan")
            tag = "creole" if keep[i] in creole else ("singleton" if sum(1 for l in keep if assign[l] == assign[keep[i]]) == 1 else "")
            print(f"    {name[keep[i]][:16]:16s}[{assign[keep[i]][:5]:5s}]→{name[keep[j]][:14]:14s}"
                  f"[{assign[keep[j]][:5]:5s}] d={D[i,j]:.2f} sameBr={sb:.2f} {tag}")

    # 6 — baselines
    Dm = None
    # marginal profile
    prof = np.zeros((n, len(PRIM)))
    for i in range(n):
        tot = 0
        for k2 in range(n):
            if k2 == i:
                continue
            p = tuple(sorted((keep[i], keep[k2])))
            if p in SUMF:
                prof[i] += SUMF[p]; tot += NCC.get(p, 0)
        if tot:
            prof[i] /= tot
    Dprof = np.array([[np.sqrt(((prof[i]-prof[j])**2).sum()) for j in range(n)] for i in range(n)])
    Dall, kall, _ = dmatrix(aSUMF, aNCC, langs)
    Dedit = valmatrix(aLEV, kall)
    # align kall to keep order for fair purity (use each matrix's own keep)
    for tag, Dx, kx in [("marginal profile", Dprof, keep),
                        ("all-concept (no LexStat)", Dall, kall),
                        ("edit-dist skeleton", Dedit, kall)]:
        ncx = [ii for ii, l in enumerate(kx) if l not in creole]
        labx = [assign[kx[ii]] for ii in ncx]
        px, kx2, hx = nn_purity(Dx[np.ix_(ncx, ncx)], labx)
        sx = silhouette(Dx[np.ix_(ncx, ncx)], labx)
        print(f"[6] baseline {tag:26s} purity={px:.3f} ({hx}/{kx2})  silhouette={sx:+.3f}")
    print(f"[6] OURS (pairwise feature dissimilarity)   purity={p_nc:.3f} ({h_nc}/{k_nc})  silhouette={os_:+.3f}")

    print("\nReadout: [1] gives a VALID p (label permutation on the fixed matrix). [6] shows what the pairwise "
          "feature dissimilarity adds over edit distance / marginal profile / no-LexStat selection. [3]-[5] make "
          "the purity and areal claims honest. Nothing here needs branch labels to BUILD the map.")


if __name__ == "__main__":
    main()
