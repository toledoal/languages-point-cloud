# A Point Cloud of Languages

### A reconstruction-free dissimilarity from inferred consonantal correspondences, and the branch structure legible in it — Indo-European, with an Austronesian contrast

**Alejandro Toledo Martínez** — Independent researcher (ORCID: 0009-0000-1277-9697)

**Preprint · draft · License: CC BY 4.0**

**Repository (code, data, figures):** https://github.com/toledoal/languages-point-cloud

*Companion to the pilot* "Additive Structure of Phonological Correspondences" (https://github.com/toledoal/phonological-correspondences).

---

## Abstract

We define a **dissimilarity** between two documented language systems that uses no reconstruction, no family
tree, and no branch labels. From concept-aligned wordlists we detect coderivative sets statistically (LexStat),
align each language pair, and average — over aligned consonant slots — the number of primary phonological features
that differ. Embedding this dissimilarity (classical MDS) and joining nearest neighbours yields a point cloud in
which, on 50 Indo-European doculects, a system's nearest neighbour shares its branch **97.7%** of the time
(silhouette **+0.34**). A label-permutation test on the fixed matrix puts both figures far above chance
(**p ≈ 0.0001**; chance purity 0.16), and the result is robust to macro-averaging, to removing 15 near-duplicate
systems, and to the distance threshold, and is uncorrelated with coverage. We are deliberately careful about what
this shows. Branch recovery is **not** a novelty of the method: a plain edit distance on consonant skeletons
matches our purity, and an unfiltered all-concept baseline matches or beats it — evidence that the branch signal
is generic lexical-phonological similarity rather than an artefact of the coderivation filter. The contribution is
instead **representational**: a reconstruction-free, feature-decomposable dissimilarity — the system-level face of
the operator repertoire studied in the pilot — whose geometry makes branch structure legible without positing
ancestors. Built as a **separate field**, Austronesian (45 doculects) reproduces the method with a markedly weaker,
higher-dimensional signal (purity 0.80, silhouette +0.13); comparing the two clouds' *abstract structure* — never a
shared space — suggests that these signatures may fingerprint how a family diversified. Cross-branch proximities
are rare and only marginally interpretable as areal contact; we do not claim to identify contact.

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
reconstruction-free, feature-decomposable *representation* and its geometry, and (§7) the comparison of that
geometry's abstract shape across families held in separate fields.

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
**the drawn network uses $k=3$**. The plane is only a projection: on the Indo-European sample the first two MDS
axes carry **27.5%** of the variance (eigenvalues 38.2, 28.9, 26.0, 17.3, 13.0, …), and the Gram matrix has
**6.7%** negative inertia — so $D$ is only *approximately* Euclidean and the 2-D figure is a rough, lossy shadow.
All statistics below use the **full** matrix, not the plane.

## 4. Results (Indo-European, 50 doculects, 4 creoles)

Branch assignment (for scoring only) follows Glottolog.

**Significance.** A label-permutation test on the fixed matrix (10,000 permutations of branch labels over the 46
non-creole systems) gives purity $0.977$ against a null of $0.155\pm0.067$ (**p ≈ 0.0001**) and silhouette
$+0.338$ against $-0.190\pm0.035$ (**p ≈ 0.0001**). The geometry aligns with branches far beyond chance.

**Purity, honestly.**

| Denominator | purity |
|---|---:|
| All doculects (multi-member branches) | 0.958 (46/48) |
| Multi-branch, creoles excluded | 0.977 (43/44), Wilson 95% [0.88, 1.00] |
| Macro-average by branch | 0.935 |
| After collapsing near-duplicate pairs ($d<1.3$; **15 dropped**) | 0.966 (28/29) |

That purity stays at 0.966 after removing fifteen near-twin systems (dialect pairs, doculect variants) shows the
result is not manufactured by a handful of near-identical pairs. The Wilson interval is wide and the observations
are not independent (mutual neighbours; small clusters) — the honest statement is "far above chance", not "a
precise 0.98".

**Coverage is not the driver.** Per pair, the median count of consonant slots is 676 (range 144–7227) over a
median 236 shared concepts; `corr(d, #slots) = +0.01`.

Systems that are near-twins remain each other's nearest neighbour (e.g. Spanish–Portuguese, Croatian–Serbo-
Croatian, Armenian E.–W.), and singleton branches sit next to their plausible relatives rather than far from
everything (Armenian nearest Greek/Indo-Iranian) — being alone in the sample is a fact of sampling, not isolation.

![Indo-European doculects placed by the consonantal-correspondence dissimilarity (classical MDS; the plane shows 27.5% of the variance, so central overlaps are partly projection). Nodes coloured by branch — colours added after layout. Solid links join same-branch nearest neighbours; dashed links join the few cross-branch nearest neighbours.](figure-network-ie.pdf|w=0.98)

## 5. Baselines — what the representation does and does not add

On the multi-branch non-creole set (n = 44):

| Method | purity | silhouette |
|---|---:|---:|
| Per-language **marginal** profile | 0.477 | −0.104 |
| **Edit distance** on consonant skeletons | 0.977 | +0.205 |
| **All-concept** dissimilarity, no LexStat filter | 1.000 | +0.324 |
| **Ours** (pairwise feature dissimilarity) | 0.977 | +0.338 |

Three honest readings. (i) **Branch recovery is generic**: a plain edit distance matches our purity, and an
unfiltered all-concept dissimilarity matches or beats it. Recovering branches is easy lexical-phonological
similarity; we claim no purity novelty. (ii) But **our dissimilarity separates the branches more cleanly than edit
distance** (silhouette +0.34 vs +0.21) — the feature representation buys margin, not just parity. (iii) **The
result is not a double-dipping artefact**: removing the similarity-based coderivation filter (the all-concept
baseline) *strengthens* the structure, so the signal is not manufactured by LexStat's selection; the marginal
baseline (0.477) confirms the pairwise comparison keeps information a per-language profile discards.

What our representation adds over edit distance is **margin plus decomposability and provenance**: $d$ is
reconstruction-free and factors into *which features change* — the same feature-operators of the pilot — so the
point cloud is the system-level face of that operator repertoire, not an opaque string distance.

## 6. Cross-branch proximities — rare, and barely areal

Of the 50 systems, only four have a nearest neighbour in another branch, and two of those are an artefact:

| System | branch | nearest neighbour | branch | $d$ | note |
|---|---|---|---|---:|---|
| Romani | Indo-Iranian | Romanian | Italic | 2.48 | **Balkan / Romania** contact |
| Irish | Celtic | Jamaican Creole | Germanic | 2.76 | no obvious story |
| Albanian (Tosk) | Albanian | Standard Albanian | (Glottolog split) | 0.79 | same language, label artefact |
| Standard Albanian | (split) | Albanian (Tosk) | Albanian | 0.79 | same language, label artefact |

Only **one** (Romani → Romanian) matches a documented contact situation; one is a Glottolog labelling split of a
single language, and one (Irish → Jamaican Creole) has no plausible contact explanation and most likely reflects
the projection and sample. We therefore make **no areal claim**: the geometry does not, on this evidence,
independently identify contact or separate it from descent. A proper test requires a contact matrix defined
*before* inspecting the map, then asking whether residual proximity tracks it — deferred to future work.

## 7. A cross-family contrast, in separate fields

We built a second cloud for **Austronesian** (45 doculects) with the identical pipeline. Crucially, the two
families are **never placed in a shared distance space** — doing so would assert a direct relation we do not claim.
We compare only *scale-free structural signatures* of each independently-built matrix: the MDS spectrum (effective
dimensionality via the participation ratio; variance in 2-D), branch separation (within/between mean dissimilarity;
silhouette; purity), and the self-normalised dissimilarity distribution. No coordinate alignment, no Procrustes.

| Field (separate) | n | eff. dim. (PR) | var. in 2-D | within/between | silhouette | purity |
|---|---:|---:|---:|---:|---:|---:|
| Indo-European | 50 | 14.2 | 27.1% | 0.63 | +0.32 | 0.96 |
| Austronesian | 45 | 16.8 | 22.1% | 0.75 | +0.13 | 0.80 |

Indo-European's branch geometry is **sharper and lower-dimensional** (tighter within-branch relative to between,
higher silhouette, fewer effective dimensions) than Austronesian's, whose dissimilarities cluster near their median
— languages nearly equidistant, a flatter and more diffuse cloud (Figure 2). This is a statement about the *shape*
of two independent geometries, not about any relation between the families. We record, but do not test here, the
hypothesis that such a signature may fingerprint a family's mode of diversification.

![Abstract comparison of the two independently-built clouds — structure only, never a shared space. (A) normalised MDS spectra; (B) branch separation; (C) each cloud's dissimilarity distribution normalised by its own median.](figure-structure-compare.pdf|w=0.98)

## 8. Controls and robustness

The label-permutation test (§4) is the primary significance check. In addition: purity and silhouette are
**unchanged** across `MINSLOT` $\in\{20,30,40,60\}$ and across feature subsets (dropping stridency, dropping all
place features, or keeping only manner); subsampling systems keeps purity high; and a concept-permuted ablation —
shuffling which forms share a concept and rerunning the full pipeline — collapses the structure toward chance,
confirming it needs real lexical pairings (reported qualitatively, not as a σ).

## 9. Limitations and scope

The input is concept-aligned lexical data, not phonology alone; the dissimilarity is corpus- and aligner-dependent
and is not a metric; the 2-D figure shows about a quarter of the variance and $D$ is only approximately Euclidean
(6.7% negative inertia). Branch recovery is not distinctive in purity versus edit distance (though our silhouette
is higher). The areal reading is at most one case. Only consonants are used; the sample is mixed-provenance (see
the manifest, Appendix A) with near-twin pairs and creoles; source/transcription effects are not fully controlled.
Direction and time are out of scope (the directed-layer paper). The cross-family comparison (§7) is deliberately
structural; extending it to more families (e.g. Caucasian) and to a pre-registered areal test is future work.

## 10. Reproducibility

`make figure` redraws from bundled results (no corpus); `LEX_PATH=… make compute` regenerates the dissimilarity;
`make analysis` reproduces §4–§6; `make compare SLUGS="ie an"` reproduces §7; `make controls` runs §8; `make
manifest` writes Appendix A. Parameters (`MINSLOT`, `THR`, `MAXLANG`, `KNN`, feature subset) are
environment-overridable in `src/compute_network.py`; permutation seeds are fixed. Versions: panphon, LingPy
(LexStat), Lexibank, Glottolog 4.8 — pinned in `requirements.txt`. Code MIT; text, figures, data CC BY 4.0.

## 11. References

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
12. Nichols, J. (1992). *Linguistic Diversity in Space and Time*. University of Chicago Press.
13. François, A. (2014). Trees, waves and linkages: models of language diversification. In *The Routledge Handbook
    of Historical Linguistics* (pp. 161–189). Routledge.
14. Schuchardt, H. (1922). *Hugo Schuchardt-Brevier* (L. Spitzer, Ed.). Niemeyer.

## Appendix A — Doculect manifest

The doculects, with Lexibank dataset, doculect ID, Glottocode, branch used for scoring, and concept count, are in
`data/results/doculect_manifest_ie.csv` (and `_an.csv`; regenerate with `make manifest`). Provenance is exposed so
source/transcription confounds can be audited (e.g. several near-twin systems share a source dataset).
