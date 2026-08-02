# A Point Cloud of Languages

### A reconstruction-free, feature-decomposable dissimilarity between language systems: an Indo-European study, with a portability check on two further families

**Alejandro Toledo Martínez** — Independent researcher (ORCID: 0009-0000-1277-9697)

**Preprint · draft · License: CC BY 4.0**

**Repository (code, data, figures):** https://github.com/toledoal/languages-point-cloud

*Companion to the pilot* "Additive Structure of Phonological Correspondences" (https://github.com/toledoal/phonological-correspondences).

---

## Abstract

We define a **dissimilarity** between two documented language systems that uses no reconstruction, no family tree,
and no branch labels. From concept-aligned wordlists we detect coderivative sets statistically (LexStat), align
each language pair, and average — over aligned consonant slots — the number of primary phonological features that
differ. All analysis matrices are **complete observed matrices with zero imputed values**. On 50 Indo-European
doculects, a system's nearest neighbour shares its Glottolog-derived branch **97.7%** of the time on the 44
systems whose branch has more than one member (creoles excluded; **95.8%** over all doculects; silhouette
**+0.34**); a label-permutation test on the fixed matrix puts both far above chance (**p < 10⁻⁴**; chance purity
0.16), and the result survives macro-averaging, removal of 15 near-duplicate systems (collapse criterion: the
dissimilarity itself, a disclosed circularity), and the minimum shared-slot threshold up to values that shrink
the sample, and shows no linear correlation with the number of retained consonant slots. We are deliberately
careful about what this shows. Branch recovery is **not** a novelty: a plain edit distance matches
our purity and an unfiltered all-concept baseline matches or beats it — so the branch signal is generic
lexical-phonological similarity, not an artefact of the coderivation filter. The claimed contribution is
**feature-level attribution**: the dissimilarity decomposes additively into per-feature components (demonstrated
on real pairs; the attribution is conditional on the chosen alignment), computed on the same correspondence
units, by construction, as the operator repertoire of the pilot study. As a portability check, the same pipeline
is run unchanged on two further families — Nakh-Daghestanian and Austronesian — each as a **separate field** (never
a shared distance space), recovering above-chance branch structure in each; we draw **no comparison between
families**, and the Austronesian field is sharply limited by corpus sparsity (a complete matrix survives for only
13 of 45 doculects). We make no areal claim.

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
with no claim of single-ancestor descent. One tension must be conceded openly: the detector we use, LexStat, was
designed and validated as an automatic *cognate* detector — a single-ancestor construct. What we take from it is
its output — clusters bound by recurrent segmental correspondence — treating that output as a correspondence
structure rather than a descent claim; our "reconstruction-free" applies to the *inputs* (no protoforms, no tree,
no labels), not to the intellectual lineage of the detector. Readers who prefer to read "coderivative" as
"statistically detected cognate" lose nothing in the mathematics; the terminological choice marks a difference of
interpretive commitment, not of computation.

Two honesty commitments frame the paper. First, the input is **not** "phonology alone": it is phonological
dissimilarity computed *within concept-matched, statistically inferred lexical correspondences*. "No
reconstruction", "no tree", and "no branch labels" are the defensible claims. Second, recovering known branches is
a **sanity check**, not the contribution — §5 shows simpler baselines do as well or better on that task. What the
representation claims instead is **feature-level attribution** (§5.1): unlike an edit distance, $d$ factors
exactly into which phonological features carry the difference.

**Relation to existing distance traditions.** The method inherits from, and should be read against, several
lines: ASJP-style normalized Levenshtein distances between wordlists (LDN/LDND), ALINE and SCA/PMI-based
alignment scoring, and phonetic-distance dialectometry. Credit where due: **ALINE is itself feature-based** (its
alignment scores decompose into feature saliences), and phonetic dialectometry has long used feature-based segment
distances; only the Levenshtein/ASJP line is genuinely feature-opaque. What our formulation adds relative to the
feature-aware lines is not the use of features but the *bookkeeping*: the final system-level dissimilarity is an
exact additive sum of per-feature, per-pair components ($d=\sum_f d_f$, §5.1) over correspondence slots within
inferred coderivative sets — so any entry of the matrix can be opened into a feature ledger tied to specific
correspondences, the unit on which the pilot's operator analysis is defined. We do not claim superior
classification (§5 shows parity); the contribution is this attribution layer, and its scope relative to ALINE-type
scoring is deliberately narrow.

## 2. A dissimilarity between systems

Let $\phi_f(x)\in\{+,-,0\}$ be primary feature $f$ of segment $x$ (panphon). For aligned segments $a,b$,
$$\mathrm{fd}(a,b)=\bigl\lvert\{f\in\text{PRIM}:\phi_f(a)\neq\phi_f(b)\}\bigr\rvert,$$
over the twelve consonantal features `cont, voi, nas, ant, cor, lab, back, round, strid, hi, lo, son`.

Coderivative sets are detected with LexStat (no etymologies, protoforms, or family labels supplied). Within each
set, each language pair is aligned by a feature-cost Needleman–Wunsch, and we average $\mathrm{fd}$ over slots
where both aligned segments are consonants:
$$d(\ell,\ell')=\operatorname{mean}\{\mathrm{fd}(a,b):(a,b)\ \text{a shared consonant slot of}\ \ell,\ell'\},$$
defined only when at least `MINSLOT` slots are observed. Observed range here $\approx[0.5,3.5]$ (theoretical
$[0,12]$).

**Missing pairs are never imputed.** If a pair has fewer than `MINSLOT` shared slots, $d$ is undefined for it; the
analysis then uses the largest **complete observed submatrix**, obtained by greedily dropping the doculect with
the most undefined pairs until none remain. (An earlier internal version filled undefined entries with the global
mean; that manufactures artificial equidistance and was removed — see §7, where its effect on Austronesian is
documented rather than hidden.) Every matrix reported in this paper has **zero imputed entries**, and each field
reports how many doculects the completeness requirement removed.

**We call $d$ a dissimilarity, not a metric.** Because each pair is computed on its own set of shared slots, the
triangle inequality and identity-of-indiscernibles are not guaranteed. It is symmetric and non-negative; that is
all we assume. Known blind spots, stated plainly: slots where a consonant corresponds to a gap or to a vowel do
not enter the average, so consonant loss, epenthesis, and consonant–vowel change are not penalized — two systems
can look close on the consonants that survive alignment even if much structure was lost. A companion indel/gap
statistic is future work; per-pair gap counts are reported in §4.

## 3. From dissimilarity to picture

We embed $D=[d(\ell,\ell')]$ with classical (Torgerson) MDS and build a $k=3$ nearest-neighbour network for
display; **purity is a $k=1$ statistic** computed on the full matrix. The plane is only a projection: on the
Indo-European analysis matrix the first two MDS axes carry **27.5%** of the positive variance, with **6.7%**
negative inertia — $D$ is only approximately Euclidean, and the 2-D figure is a lossy shadow. All statistics use
the **full** matrix. (Figures in this paper come from the bundled network matrices, which are regenerated by an
independent LexStat pass; because LexStat inference is stochastic across passes, figure-level summaries can differ
from the analysis matrix in the second decimal — e.g. 28.9% vs 27.5% variance-in-2D — and each table states which
matrix it uses.)

## 4. Results (Indo-European, 50 doculects, 4 creoles)

Branch labels (scoring only) are derived from Glottolog by a sample-dependent tree cut (nodes covering at most
half the sample); this makes "branch" a function of the sample, which is one reason the cross-family §7 is kept
exploratory. **Creole policy, stated once:** Glottolog classifies creoles under their lexifier's branch (Jamaican
Creole → Germanic), and we keep those labels wherever creoles appear; but because their genealogical status is
contested, the headline purity excludes them (they remain present in the matrix as potential neighbours, and in
the all-doculect row). All numbers in this section come from the analysis matrix (`make analysis`).

**Significance.** A label-permutation test on the fixed matrix: the matrix comprises the 46 non-creole systems;
the statistic is nearest-neighbour purity over the 44 of them whose branch has more than one member (a singleton
can never match, so the two Albanian-label singletons are excluded from the numerator and denominator but remain
as potential neighbours); the null shuffles the branch labels of all 46 systems, 10,000 times. Result: purity
$0.977$ against a null of $0.155\pm0.067$ and silhouette $+0.338$ against $-0.190\pm0.035$, with no permutation
reaching the observed values (**p < 10⁻⁴**, the resolution floor of 10,000 permutations). Caveat: label
exchangeability is an approximation — doculects within a branch often share dataset and transcription
conventions; blocked-by-source permutation is future work. (Three related "chance" figures appear in this paper
and are different quantities: 0.155 is this permutation-null mean; 0.158 is the analytic expected same-branch
probability of a random neighbour; §7's 0.16 is a separate 2,000× permutation null on the network matrix. They
agree to two decimals here, but they are not the same estimator.)

**Purity, reported at several denominators.**

| Denominator | purity |
|---|---:|
| All doculects (multi-member branches) | 0.958 (46/48) |
| Multi-branch, creoles excluded | 0.977 (43/44), Wilson 95% [0.88, 1.00] |
| Macro-average by branch | 0.935 |
| After collapsing near-duplicate pairs ($d<1.3$; 15 dropped) | 0.966 (28/29) |

The near-duplicate ablation uses $d$ itself as the collapse criterion, which is admittedly circular in a limited
sense; a metadata-based collapse (same Glottocode / documented dialect relation) is the better design and is left
as future work — the manifest (Appendix A) contains the fields needed to do it. One labelling artefact is noted
and neutralized: Glottolog splits "Albanian (Tosk)" and "Standard Albanian" into different top labels although
they are one language; as two singletons they are excluded from multi-branch purity, so the reported purity is
*conservative* — merging them would add a correct pair.

**Coverage.** Median 676 consonant slots per pair (range 144–7227), median 424 gaps, median 236 shared concepts;
within this sample, $d$ shows **no linear correlation** with the number of retained slots
(`corr(d, #slots) = +0.01`). This does not rule out subtler coverage effects (variance, gap proportion, neighbour
identity); per-pair coverage is published with the results so they can be probed.

![Indo-European doculects placed by the consonantal-correspondence dissimilarity (classical MDS of the bundled network matrix; the plane shows under a third of the variance, so central overlaps are partly projection). Nodes coloured by branch — colours added after layout. Solid links join same-branch nearest neighbours; dashed links join the few cross-branch nearest neighbours.](figure-network-ie.pdf|w=0.98)

## 5. Baselines — what the representation does and does not add

On the multi-branch non-creole set (n = 44), same corpus and concepts:

| Method | purity | silhouette |
|---|---:|---:|
| Per-language **marginal** profile | 0.477 | −0.104 |
| **Edit distance** on consonant skeletons | 0.977 | +0.205 |
| **All-concept** dissimilarity, no LexStat filter | 1.000 | +0.324 |
| **Ours** (pairwise feature dissimilarity) | 0.977 | +0.338 |

Honest readings. (i) **Branch recovery is generic**: edit distance ties our purity; the unfiltered all-concept
variant matches or beats it. (ii) **Not a double-dipping artefact**: removing the similarity-based coderivation
filter *strengthens* the structure, so the signal is not manufactured by LexStat's selection. (iii) The +0.014
silhouette edge over the all-concept baseline is **small and untested for stability** (a paired concept-bootstrap
is future work), and the baselines are not perfectly matched (the all-concept variant uses one form per concept);
we do not rest any claim on that margin. (iv) The marginal baseline (0.477) confirms that the pairwise comparison
keeps information a per-language profile discards. Why keep the LexStat-filtered variant as the main object at
all? An honest answer first: **not because of decomposability** — the feature decomposition of §5.1 is a property
of the feature-difference metric and would hold equally for the unfiltered all-concept variant computed the same
way. The filtered variant is retained for *continuity of units*: its slots are correspondences within coderivative
sets, which is — by construction, not by demonstrated result — the same unit the pilot's operator analysis is
defined on, so the two studies' quantities compose.

### 5.1 Feature-level decomposition — demonstrated, not promised

By construction $d(\ell,\ell')=\sum_f d_f(\ell,\ell')$, where $d_f$ is the fraction of aligned consonant slots on
which feature $f$ differs. Real values from the analysis matrix (`src/decompose.py`):

| Pair | cont | voi | nas | ant | cor | lab | back | round | strid | hi | lo | son | total | slots |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Spanish–Portuguese | 0.20 | 0.15 | 0.07 | 0.18 | 0.16 | 0.09 | 0.10 | 0.00 | 0.16 | 0.19 | 0.07 | 0.14 | **1.51** | 4276 |
| Persian–Hindi | 0.27 | 0.24 | 0.20 | 0.23 | 0.21 | 0.14 | 0.17 | 0.01 | 0.16 | 0.21 | 0.10 | 0.31 | **2.25** | 532 |
| Spanish–Hindi | 0.36 | 0.30 | 0.23 | 0.29 | 0.25 | 0.18 | 0.18 | 0.00 | 0.18 | 0.40 | 0.19 | 0.30 | **2.86** | 374 |

The decomposition is exact and interpretable: the close Romance pair differs mostly in continuancy and height
(lenition-type oppositions); the cross-branch pair adds weight on height (`hi` 0.40) and continuancy. One caveat
is declared: the alignment itself is optimized with a feature cost, so per-feature attribution is conditional on
the chosen alignment; a fixed-alignment sensitivity check is future work.

## 6. Cross-branch proximities — rare, and barely areal

Of the 50 systems, four have a nearest neighbour in another branch — two of which are the Albanian labelling
artefact of §4:

| System | branch | nearest neighbour | branch | $d$ | note |
|---|---|---|---|---:|---|
| Romani | Indo-Iranian | Romanian | Italic | 2.48 | **Balkan / Romania** contact |
| Irish | Celtic | Jamaican Creole | Germanic | 2.76 | likely sampling / lexical overlap / accidental proximity |
| Albanian (Tosk) ↔ Standard Albanian | (label split) | each other | — | 0.79 | same language; artefact, discounted |

Only Romani → Romanian matches a documented contact situation. The Irish case is computed on the full,
creole-inclusive matrix (not the projection), so it is a genuine proximity under this dissimilarity — most
plausibly reflecting sampling, lexical overlap, or corpus effects rather than contact. Note an asymmetry we flag
rather than hide: because the headline purity of §4 excludes creoles (per the stated policy), this one anomalous
proximity cannot lower that headline — it is visible only here. We make **no areal claim**: a proper test requires
a contact matrix defined *before* inspecting the map — deferred.

## 7. Portability check — the same pipeline on two further families

As a portability check only, we ran the identical pipeline on two further families, each on its **own field**
(never a shared distance space, which would assert a direct relation between families we do not claim). We report
each field's own scale-free structural signatures side by side; we do **not** compare the families or interpret the
differences between their signatures — the samples are not commensurable (see below), and any question about *how*
a family diversified is out of scope and belongs to future, matched-sampling work.

**A correction made and disclosed.** An earlier version of this section filled unobserved pairs with the global
mean. For Austronesian this was fatal: 52.6% of its 990 pairs were fill values, which *manufactures* a flat,
nearly-equidistant, high-dimensional geometry — exactly the "signature" we had reported. That analysis was wrong
and is withdrawn. Under the zero-imputation policy, the Austronesian corpus in Lexibank supports a complete matrix
for only **13 of 45** doculects: the corpus is too sparse in shared concepts for a large Austronesian field, and
that sparsity — not family history — dominated the earlier picture.

| Field (complete observed matrix) | n | missing pairs dropped-to-complete | eff. dim. (PR) | within/between | silhouette | purity | chance | **adj. purity** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Indo-European | 50 | 0 of 1225 | 13.3 | 0.62 | +0.33 | 0.96 | 0.16 | **0.95** |
| Nakh-Daghestanian | 45 | 0 of 990 | 9.4 | 0.68 | +0.31 | 0.98 | 0.29 | **0.97** |
| Austronesian | 13 | (32 doculects removed) | 4.9 | 0.61 | +0.22 | 0.83 | 0.64 | **0.54** |

"Chance" is each field's own 2,000× label-permutation null and *adj. purity* $=(P_{obs}-P_{null})/(1-P_{null})$ —
the comparable quantity, since branch granularity differs across samples. (This table is computed on the bundled
*network* matrices with all doculects included — hence IE purity 0.96 here versus §4's 0.977, which is the
analysis matrix with creoles excluded; the denominators are stated in each place.)

The purpose of this section is only to show that **the same pipeline runs unchanged on other families and recovers
above-chance branch structure in each** (adjusted purity 0.95 for Indo-European, 0.97 for Nakh-Daghestanian; the
Austronesian field is n=13 after the completeness requirement, too small and too coarse in branch partition to
read into, adjusted 0.54). We **make no comparison between the families and draw no conclusion from the differences
in their signatures.** The samples are not comparable — Nakh-Daghestanian is dialect-dense and largely
single-source, Indo-European mixes ancient, modern and creole doculects, Austronesian is sparse — so the numbers in
this table are not commensurable and are reported per-field, for transparency, not as a contrast. Any attempt to
relate a family's geometric signature to *how* it diversified would require matched sampling (one doculect per
Glottocode, fixed taxonomic depth, shared concept lists, equated branch-size distributions) and lies entirely
outside this paper. Figure 2 displays the three fields side by side under these caveats.

![The same pipeline on three families, each on its own complete observed matrix, shown side by side (not compared, and never in a shared space). (A) normalised MDS spectra; (B) branch separation; (C) each field's dissimilarity distribution normalised by its own median. The Austronesian field is n=13 (corpus sparsity) and is shown for transparency only.](figure-structure-compare.pdf|w=0.98)

## 8. Controls and robustness

The label-permutation test (§4) is the primary significance check. The following controls were run on the n=50
configuration with the zero-imputation policy (`make controls`; outputs in `data/results/controls_ie_n50.txt`):

- **Reproduction:** purity 0.977, silhouette +0.324 on an independent LexStat pass (matches §4 within the
  cross-pass stochasticity noted in §3).
- **Concept-permuted ablation:** shuffling which forms share a concept and rerunning the full pipeline collapses
  purity to 0.28 (range 0.20–0.38 over three reruns) and silhouette to ≈0 — toward, though not fully to, the
  chance level 0.16. The residual above chance is expected: concept-shuffling destroys coderivative structure but
  preserves each language's segment inventory and phonotactics, which carry some branch signal on their own. Three
  reruns are too few for a null tail, so this is reported **qualitatively**; significance is carried by the
  10,000× label-permutation test of §4, not by this ablation.
- **Minimum shared-slot threshold:** since the minimum observed per-pair coverage is 144 slots, thresholds below
  that are vacuous by construction; the sweep therefore extends **above** it. Purity is 0.977 at `MINSLOT`
  $\in\{20,40,100\}$ (n=50), **0.977 at 200** (n=48), and **1.000 at 400** (only 27 systems survive the
  completeness requirement). The result is not a knife-edge of the threshold. (The LexStat detection threshold
  `THR` is *not* varied here — a sweep over it, gap penalties, and alignment costs is future work.)
- **Feature subsets:** dropping stridency leaves the result unchanged (0.977/+0.323); dropping all five place
  features gives 0.955/+0.319; manner-only gives 0.932/+0.329 — mild, honest variation, no knife-edge.
- **Subsampling:** drawing 22 of 50 systems 500× keeps purity at mean 0.934, 95% CI [0.79, 1.00].

## 9. Limitations and scope

The input is concept-aligned lexical data, not phonology alone. The dissimilarity is corpus- and aligner-dependent,
is not a metric, ignores gaps and consonant–vowel correspondences, and weights concepts by their consonant count
(a concept-balanced variant is future work). The 2-D figures show under a third of the variance. Branch labels are
a sample-dependent Glottolog cut, so purity is not directly comparable across differently-sampled families —
which is why §7 is a portability check only and draws no cross-family comparison. The twelve-feature instrument was not validated
for cross-family measurement invariance (glottalization, uvularity and pharyngeal oppositions are not directly
represented — relevant for Nakh-Daghestanian). Branch recovery is not distinctive versus edit distance; the
near-duplicate collapse uses $d$ itself; the silhouette margin over the strongest baseline is untested for
stability. Direction and time are out of scope (the directed-layer paper).

## 10. Reproducibility

Pinned dependencies (`requirements.txt`, exact versions; Python 3.12.13). Each experiment's `MAXLANG` is fixed in
the `Makefile`: `LEX_PATH=… make compute` reproduces the n=50 Indo-European field; `make compute-nd` /
`make compute-an` the other fields; `make analysis` §4–§6; `make compare` §7 (all three slugs by default);
`make controls` §8; `make manifest` Appendix A; `make figure` redraws from bundled results without the corpus.
Permutation seeds are fixed in the scripts; complete observed matrices, coordinates, manifests and analysis logs
are bundled under `data/results/`. Code MIT; text, figures, data CC BY 4.0.

## 11. References

1. Toledo Martínez, A. (2026). *Additive Structure of Phonological Correspondences* (pilot study).
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
   Workshop LaTeCH*, 117–125.
9. List, J.-M., Forkel, R., Greenhill, S. J., Rzymski, C., Englisch, J., & Gray, R. D. (2022). Lexibank, a public
   repository of standardized wordlists. *Scientific Data* 9, 316.
10. Hammarström, H., Forkel, R., Haspelmath, M., & Bank, S. (2023). *Glottolog 4.8*. MPI-EVA. https://glottolog.org
11. Wichmann, S., Holman, E. W., & Brown, C. H. (2016). The ASJP database and normalized Levenshtein distances
    (LDN/LDND) for language classification. In *The Oxford Handbook of Historical Phonology* context; database at
    https://asjp.clld.org
12. Kondrak, G. (2000). A new algorithm for the alignment of phonetic sequences (ALINE). *Proc. NAACL 2000*.
13. Jäger, G. (2018). Global-scale phylogenetic linguistic inference from lexical resources (PMI distances).
    *Scientific Data* 5, 180189.
14. Nerbonne, J., & Heeringa, W. (2010). Measuring dialect differences. In *Language and Space* (pp. 550–567).
    De Gruyter.
15. Thomason, S. G., & Kaufman, T. (1988). *Language Contact, Creolization, and Genetic Linguistics*. UC Press.
16. Schuchardt, H. (1922). *Hugo Schuchardt-Brevier* (L. Spitzer, Ed.). Niemeyer.

## Appendix A — Doculect manifests

The doculects of all three fields, with Lexibank dataset, doculect ID, Glottocode, branch used for scoring, and
concept count, are in `data/results/doculect_manifest_{ie,an,nd}.csv` (regenerate with `make manifest`). Each
manifest lists the **candidate pool** (the top-`MAXLANG` doculects by form count); the analysed field can be
smaller after the completeness requirement — in particular the Austronesian manifest lists 45 candidates while the
complete-matrix field is n=13. Provenance is exposed so source/transcription confounds can be audited — e.g.
several near-twin systems share a source dataset, and most Nakh-Daghestanian doculects come from a single
segmented source, which the reader should weigh when comparing fields.
