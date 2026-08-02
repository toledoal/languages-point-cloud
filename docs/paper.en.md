# A Point Cloud of Languages

### A reconstruction-free dissimilarity from inferred consonantal correspondences, and the branch structure legible in it — an Indo-European pilot

**Alejandro Toledo Martínez** — Independent researcher (ORCID: 0009-0000-1277-9697)

**Preprint · draft · License: CC BY 4.0**

**Repository (code, data, figure):** https://github.com/toledoal/languages-point-cloud

*Companion to the pilot* "Additive Structure of Phonological Correspondences" (https://github.com/toledoal/phonological-correspondences).

---

## Abstract

We define a **dissimilarity** between two documented language systems that uses no reconstruction, no family
tree, and no branch labels. From concept-aligned wordlists we detect coderivative sets statistically (LexStat),
align each language pair, and average — over aligned consonant slots — the number of primary phonological features
that differ. Embedding this dissimilarity (classical MDS) and joining nearest neighbours yields a point cloud in
which, on 28 Indo-European doculects, a system's nearest neighbour shares its branch **95.5%** of the time
(silhouette **+0.28**). A label-permutation test on the fixed matrix puts both figures far above chance
(**p ≈ 0.0001**; chance purity 0.15), and the result is robust to macro-averaging, to removing near-duplicate
pairs, and to the distance threshold, and is uncorrelated with coverage. We are deliberately careful about what
this shows. Branch recovery is **not** a novelty of the method: a plain edit distance on consonant skeletons does
as well, and an unfiltered all-concept baseline does better — evidence that the branch signal is generic
lexical-phonological similarity rather than an artefact of the coderivation filter. The contribution is instead
**representational**: a reconstruction-free, feature-decomposable dissimilarity — the system-level face of the
operator repertoire studied in the pilot — whose geometry makes branch structure (and, more tentatively, contact)
legible without positing ancestors. Cross-branch proximities are rare and only partly interpretable as areal
contact; we do not claim to identify contact, nor to separate it causally from descent.

---

## 1. Introduction

The pilot study argued that a family's inventory of feature-difference operators, read at the level of *types*, is
representational rather than genealogical: the operators are largely those general phonology makes available, and
the genealogical signal lives one level up, in how those operators are *distributed* across languages. This paper
looks at the simplest projection of that distribution — a pairwise dissimilarity between whole systems — and asks a
deliberately modest question: **is branch structure legible in it, built without any historical apparatus?**

The stance is the programme's: **discover first, contrast later.** We construct the map from correspondences in
concept-aligned lexical data and consult branch labels, contact history, and baselines only afterwards. We say
**coderivative**, not *cognate*: operationally, an *algorithmically linked form set* (recurrent correspondence),
with no claim of single-ancestor descent. A language, on this view, is a confluence, not the linear issue of one
parent; branch structure is one legible aspect of the geometry, not the whole of it.

Two honesty commitments frame the paper. First, the input is **not** "phonology alone": it is phonological
dissimilarity computed *within concept-matched, statistically inferred lexical correspondences*. "No
reconstruction", "no tree", and "no branch labels" are the defensible claims. Second, recovering known branches is
a **sanity check**, not the contribution — §5 shows simpler baselines do as well or better. What is new is the
reconstruction-free, feature-decomposable *representation* and its geometry.

## 2. A dissimilarity between systems

Let $\phi_f(x)\in\{+,-,0\}$ be primary feature $f$ of segment $x$ (panphon). For aligned segments $a,b$,
$$\mathrm{fd}(a,b)=\bigl\lvert\{f\in\text{PRIM}:\phi_f(a)\neq\phi_f(b)\}\bigr\rvert,$$
over the twelve consonantal features `cont, voi, nas, ant, cor, lab, back, round, strid, hi, lo, son`.

Coderivative sets are detected with LexStat (no etymologies, protoforms, or family labels supplied). Within each
set, each language pair is aligned by a feature-cost Needleman–Wunsch, and we average $\mathrm{fd}$ over slots
where both aligned segments are consonants:
$$d(\ell,\ell')=\operatorname{mean}\{\mathrm{fd}(a,b):(a,b)\ \text{a shared consonant slot of}\ \ell,\ell'\},$$
requiring at least `MINSLOT` slots. Its observed range here is $\approx[0.5,3.5]$ (theoretical $[0,12]$).

**We call $d$ a dissimilarity, not a metric.** Because each pair is computed on its own set of shared slots, the
triangle inequality and identity-of-indiscernibles are not guaranteed. It is symmetric and non-negative; that is
all we assume. This matters for §3.

## 3. From dissimilarity to picture

We embed $D=[d(\ell,\ell')]$ with classical (Torgerson) MDS and build a $k=3$ nearest-neighbour network. Two
distinct objects must not be confused: **purity is a $k=1$ statistic** (is the single closest system same-branch?);
**the drawn network uses $k=3$**. The plane is only a projection: on this sample the first two MDS axes carry
**28.6%** of the variance (eigenvalues 19.7, 19.0, 13.3, 11.2, 10.3, …), with negligible negative inertia (0.3%,
so the matrix is close to Euclidean). The dissimilarity is genuinely high-dimensional; the figure is a lossy
shadow, and all statistics below use the **full** matrix, not the plane.

## 4. Results (Indo-European pilot, 28 doculects, 4 creoles)

Branch assignment (for scoring only) follows Glottolog.

**Significance.** A label-permutation test on the fixed matrix (10,000 permutations of branch labels over the 24
non-creole systems) gives purity $0.955$ against a null of $0.142\pm0.091$ (**p ≈ 0.0001**) and silhouette
$+0.283$ against $-0.147\pm0.036$ (**p ≈ 0.0001**). The geometry aligns with branches far beyond chance.

**Purity, honestly.** Reported several ways:

| Denominator | purity |
|---|---:|
| All doculects (multi-member branches) | 0.923 (24/26) |
| Multi-branch, creoles excluded | 0.955 (21/22), Wilson 95% [0.78, 0.99] |
| Macro-average by branch | 0.944 |
| After collapsing near-duplicate pairs ($d<1.3$; 2 dropped) | 0.947 (18/19) |

The headline survives macro-averaging and near-duplicate removal, so it is not merely an artefact of a few
near-twin pairs (Croatian–Serbo-Croatian, Armenian E.–W., etc.). The Wilson interval is wide and the observations
are not independent (mutual neighbours; small clusters) — the honest statement is "clearly above chance", not "a
precise 0.96".

**Coverage is not the driver.** Per pair, the median count of consonant slots is 2008 (range 312–7493) over a
median 585 shared concepts; `corr(d, #slots) = +0.00`. Two languages are not judged close merely because more
material survived alignment.

**Internal pairs** (same dissimilarity): Spanish–Portuguese 1.56, English–Jamaican Creole 0.59,
Dutch–Negerhollands 1.29, Croatian–Serbo-Croatian 0.78, Persian–Hindi 2.47, Ancient–Modern Greek 1.97, Armenian
E.–W. 0.89.

![Indo-European doculects placed by the consonantal-correspondence dissimilarity (classical MDS; the plane shows 28.6% of the variance, so overlaps in the centre are partly projection). Nodes coloured by branch — colours added after layout. Solid links join same-branch nearest neighbours; dashed links join the few cross-branch nearest neighbours.](figure-network-ie.pdf|w=0.98)

**Graded proximity.** Singleton branches are not "far from everything": Armenian's nearest non-Armenian systems
are Greek and Indo-Iranian, not the Romance/Germanic systems across the cloud. Being alone in the sample is a fact
of sampling, not a measurement of isolation.

## 5. Baselines — what the representation does and does not add

The decisive question is not whether branches are recovered, but whether *this* dissimilarity recovers something
simpler methods do not. On the multi-branch non-creole set (n = 22):

| Method | purity | silhouette |
|---|---:|---:|
| Per-language **marginal** profile | 0.364 | −0.083 |
| **Edit distance** on consonant skeletons | 0.955 | +0.213 |
| **All-concept** dissimilarity, no LexStat filter | 1.000 | +0.313 |
| **Ours** (pairwise feature dissimilarity) | 0.955 | +0.283 |

Two honest readings. (i) **Branch recovery is generic**: a plain edit distance matches us, and an unfiltered
all-concept dissimilarity beats us. Recovering branches is easy lexical-phonological similarity; we claim no
classification novelty. (ii) **The result is not a double-dipping artefact**: removing the similarity-based
coderivation filter (the all-concept baseline) *strengthens* the structure rather than destroying it, so the
signal is not manufactured by LexStat's selection. The marginal baseline (0.364) confirms the earlier point that
the **pairwise** comparison keeps information a per-language profile discards.

What our representation adds over edit distance is not accuracy but **decomposability and provenance**: $d$ is
reconstruction-free and factors into *which features change* — the same feature-operators studied in the pilot —
so the point cloud is the system-level face of that operator repertoire, not an opaque string distance.

## 6. Cross-branch proximities — rare, and only partly areal

Of the 28 systems, only **four** have a nearest neighbour in another branch:

| System | branch | nearest neighbour | branch | $d$ | same-branch $d$ | note |
|---|---|---|---|---:|---:|---|
| Albanian (Tosk) | Albanian | Romanian | Italic | 2.87 | — | singleton; **Balkan** contact |
| Romanian | Italic | English | Germanic | 2.36 | 2.56 | no obvious contact story |
| Breton | Celtic | English | Germanic | 2.58 | — | singleton; no obvious story |
| Seychelles Creole | Italic | English | Germanic | 2.50 | 2.77 | creole; English not its lexifier |

Only **one** (Albanian → Romanian) matches a documented contact area (the Balkan *Sprachbund*); the others have no
obvious contact explanation and most likely reflect the high-dimensional projection and the small sample. We
therefore make no areal claim: the geometry does **not**, on this evidence, independently identify contact or
separate it from descent. A proper test requires a contact matrix defined *before* inspecting the map, then asking
whether residual proximity (closer than the branch baseline predicts) tracks it — deferred to future work.

## 7. Controls and robustness

Beyond §4's permutation test: a **concept-permuted** ablation — shuffling which forms share a concept and rerunning
the full pipeline — collapses purity from 0.955 to $0.29$ and silhouette to $\approx 0$, i.e. the structure needs
real lexical pairings (three reruns; reported qualitatively, not as a σ). Purity and silhouette are **unchanged**
across `MINSLOT` $\in\{20,30,40,60\}$ and across feature subsets (dropping stridency, dropping all place features,
or keeping only manner). Subsampling 22 of 28 systems 500× keeps purity in [0.87, 1.00].

## 8. Limitations and scope

The input is concept-aligned lexical data, not phonology alone; the dissimilarity is corpus- and aligner-dependent
and is not a metric; the 2-D figure shows under a third of the variance. Branch recovery is not distinctive versus
edit distance. The areal reading is at most suggestive (one case). Only consonants are used; only one family is
shown, with a small, uneven, mixed-provenance sample (see the doculect manifest, Appendix A) that includes near-
twin pairs and creoles; source/transcription effects are not fully controlled. Direction and time are out of scope
(the directed-layer paper). **Ongoing extension** (respecting the same stance): a denser Indo-European sample
including minor languages and dialects, and Austronesian built as a *separate field* — the two clouds compared only
at the level of abstract structure, never embedded in a shared distance space (which would falsely assert a direct
relation between families). A first Austronesian field (40 doculects) already shows the same method with a weaker
signal (nearest-neighbour purity 0.86, silhouette +0.09), a contrast we will develop rather than merge.

## 9. Reproducibility

`make figure` redraws from bundled results (no corpus); `LEX_PATH=… make compute` regenerates the dissimilarity;
`make controls` runs §7's checks. Parameters (`MINSLOT`, `THR`, `MAXLANG`, `KNN`, feature subset) are
environment-overridable in `src/compute_network.py`; permutation seeds are fixed in the scripts. Versions:
panphon, LingPy (LexStat), Lexibank, Glottolog 4.8 — pinned in `requirements.txt`; the exact 28 doculects are
listed in Appendix A. Code MIT; text, figures, data CC BY 4.0.

## 10. References

1. Toledo Martínez, A. (2026). *Additive Structure of Phonological Correspondences: A protoform-agnostic method
   for discovering mathematical patterns in documented linguistic systems* (pilot study).
   https://github.com/toledoal/phonological-correspondences
2. Torgerson, W. S. (1952). Multidimensional scaling: I. Theory and method. *Psychometrika* 17(4), 401–419.
3. Kruskal, J. B., & Wish, M. (1978). *Multidimensional Scaling*. Sage.
4. Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis.
   *Journal of Computational and Applied Mathematics* 20, 53–65.
5. Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA* 22, 209–212.
6. Needleman, S. B., & Wunsch, C. D. (1970). A general method applicable to the search for similarities in the
   amino acid sequence of two proteins. *Journal of Molecular Biology* 48(3), 443–453.
7. Mortensen, D. R., Littell, P., Bharadwaj, A., Goyal, K., Dyer, C., & Levin, L. (2016). PanPhon: a resource for
   mapping IPA segments to articulatory feature vectors. *Proc. COLING 2016*, 3475–3484.
8. List, J.-M. (2012). LexStat: automatic detection of cognates in multilingual wordlists. *Proc. EACL 2012
   Workshop on Language Technology for Cultural Heritage*, 117–125.
9. List, J.-M., Forkel, R., Greenhill, S. J., Rzymski, C., Englisch, J., & Gray, R. D. (2022). Lexibank, a public
   repository of standardized wordlists. *Scientific Data* 9, 316.
10. Hammarström, H., Forkel, R., Haspelmath, M., & Bank, S. (2023). *Glottolog 4.8*. MPI-EVA. https://glottolog.org
11. Thomason, S. G., & Kaufman, T. (1988). *Language Contact, Creolization, and Genetic Linguistics*. UC Press.
12. Joseph, B. D. (1983). *The Synchrony and Diachrony of the Balkan Infinitive*. Cambridge University Press.
13. François, A. (2014). Trees, waves and linkages: models of language diversification. In *The Routledge Handbook
    of Historical Linguistics* (pp. 161–189). Routledge.
14. Schuchardt, H. (1922). *Hugo Schuchardt-Brevier* (L. Spitzer, Ed.). Niemeyer.

## Appendix A — Doculect manifest

The 28 doculects, with Lexibank dataset, doculect ID, Glottocode, branch used for scoring, and concept count, are
listed in `data/results/doculect_manifest_ie.csv` (regenerate with `make manifest`). It exposes provenance so
source/transcription confounds can be audited — e.g. several near-twin systems share a source (Bulgarian, Ancient
Greek, and Serbo-Croatian all come from `idssegmented`), which the reader should weigh when reading their
proximity.
