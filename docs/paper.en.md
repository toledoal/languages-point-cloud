# The Languages Point Cloud

### Genealogy and areality drawn from phonological correspondences alone — a reconstruction-free distance between language systems

**Alejandro Toledo Martínez** — Independent researcher (ORCID: 0009-0000-1277-9697)

**Preprint · draft · License: CC BY 4.0**

**Repository (code, data, figure):** https://github.com/toledoal/languages-point-cloud

*Companion to the pilot* "Additive Structure of Phonological Correspondences" (https://github.com/toledoal/phonological-correspondences).

---

## Abstract

We define a distance between two documented language *systems* that uses no reconstruction and no family tree.
Across statistically detected coderivative sets (sets of forms bound by recurrent correspondence, not by a posited
common ancestor), we align each language pair and count, at every aligned consonant slot, the number of primary
phonological features that differ; the mean of that count is the distance. Embedding the resulting distance matrix
with classical multidimensional scaling and linking each system to its nearest neighbours makes a language family
**draw itself** as a point cloud. On 28 Indo-European varieties, a system's nearest neighbour is a member of its
own branch **96%** of the time (silhouette **+0.27** by branch), and the branch labels are consulted only
*after* the map is built — to colour and score it, never to place a point. The off-branch nearest neighbours are
not noise: they recover **areal** structure (Albanian and the Balkan *Sprachbund*; Romani in Romania) and
**creole–lexifier** proximity. The point cloud is thus a direct, minimal picture of the level at which — as the
pilot argued — genealogy and contact actually live: the *distribution* of correspondences, not the flat inventory
of correspondence types.

---

## 1. Introduction

The pilot study established two things about a family's repertoire of feature-difference operators. First, that
the repertoire has a rich additive geometry. Second — and this is the point we build on — that this geometry, read
at the level of the *type* inventory, is **representational rather than genealogical**: the operators a family
uses are largely those general phonology makes available, and the genealogical signal lives one level up, in how
those operators are *distributed* across languages, positions and contexts.

This paper makes that "one level up" visible in the simplest possible form. Instead of asking which operators a
family owns, we ask, for each *pair* of languages, **how their correspondences behave** — and turn the answer into
a single number, a distance between two systems. Laid out in a plane and joined to their neighbours, the languages
form a point cloud in which the branches appear as sub-clouds and contact appears as the links that cross between
them. Nothing genealogical is supplied to build the picture.

The stance is the programme's throughout: **discover first, contrast later.** We construct the map from
correspondences only, and bring in branch labels, contact history and the areal literature *afterwards*, as an
external check on what the geometry already shows. Consistent with that stance, we say **coderivative**, not
*cognate*: forms co-derived by recurrent correspondence, without committing to a single reconstructed ancestor. A
language, on this view, is not the linear issue of one parent but a confluence; genealogy is one legible region of
the geometry, areal contact another.

## 2. A distance between systems

Let $\phi_f(x)\in\{+,-,0\}$ be the value of primary phonological feature $f$ for segment $x$ (panphon coding). For
two aligned segments $a,b$ define the **feature-difference count**
$$\mathrm{fd}(a,b)=\bigl\lvert\{f\in\text{PRIM}:\phi_f(a)\neq\phi_f(b)\}\bigr\rvert,$$
over the twelve primary consonantal features `cont, voi, nas, ant, cor, lab, back, round, strid, hi, lo, son`;
identity gives $\mathrm{fd}=0$.

Coderivative sets are detected statistically with LexStat — no etymologies, protoforms or family labels are given
to the detector. Within each set, each language pair is aligned by a feature-distance Needleman–Wunsch. At every
slot where **both** aligned segments are consonants we record $\mathrm{fd}$. The distance between two systems is
the mean over all such shared slots,
$$d(\ell,\ell')=\operatorname{mean}\{\mathrm{fd}(a,b):(a,b)\ \text{a shared consonant slot of}\ \ell,\ell'\},$$
computed only when at least `MINSLOT` slots are available.

Three properties matter. The distance is **pairwise** — it compares $\ell$ and $\ell'$ directly, and so keeps
information that a per-language *marginal* profile discards. (In a control that marginalises to one operator
profile per language, the branches separate only weakly; the pairwise distance below separates them at 0.96. The
signal that Portuguese and Spanish are nearly the same system lives in their direct comparison, not in either
language's profile taken alone.) It is **reconstruction-free** and **tree-free**: no ancestor is posited and no
classification enters the computation. And it is symmetric, with range roughly $[0,4]$ and $d=0$ for identical
systems.

## 3. From distance to picture

The object is the distance matrix $D=[d(\ell,\ell')]$. For visualisation we embed it in two dimensions with
classical (Torgerson) multidimensional scaling; the plane is a shadow of the full matrix, which is what the
analysis actually uses. We then build a **nearest-neighbour network**: each system is linked to its $k=3$ nearest
systems, and links are drawn differently according to whether the two endpoints share a branch — a distinction
made only for display, from labels the map never used.

Scoring is post hoc. With branch labels now consulted we report **nearest-neighbour purity** (the fraction of
systems whose closest system is in the same branch), the **silhouette** by branch (positive when branches are
internally tighter than they are close to other branches), and the within- versus between-branch mean distance.

## 4. Results

We use 28 Indo-European doculects from Lexibank with sufficient data. Branch assignment (for scoring only) follows
the Glottolog classification.

| Measure | Value | Reading |
|---|---:|---|
| Nearest-neighbour purity (multi-branch, creoles excluded) | **0.96** (22/23) | a system's closest system is almost always its own branch |
| Silhouette by branch | **+0.27** | branches are separated in the distance geometry |
| Within-branch vs between-branch mean $d$ | tighter within | the distribution alone already separates |
| Branch labels used to build the map | **0** | placement is from correspondences only |

The branches emerge as clean sub-clouds, with sensible internal distances:

| Branch | Illustrative nearest pair | $d$ |
|---|---|---:|
| Italic (Romance) | Spanish – Portuguese | 1.56 |
| Germanic | English – Jamaican Creole | 0.59 |
| Germanic | Dutch – Negerhollands | 1.29 |
| Balto-Slavic | Croatian – Serbo-Croatian | 0.78 |
| Indo-Iranian | Persian – Hindi | 2.47 |
| Graeco-Phrygian | Ancient – Modern Greek | 1.97 |
| Armenic | Armenian E. – Armenian W. | 0.89 |

![Indo-European placed by phonological-correspondence distance alone (classical MDS of the distance matrix). Nodes are languages, coloured by branch (colours added after layout); solid links join same-branch nearest neighbours, dashed links join nearest neighbours in different branches — almost always areal contact or a creole beside its lexifier.](figure-network-ie.pdf|w=0.98)

Two features of the picture deserve emphasis, both anticipated by the reflection that led to this paper.

**Proximity is graded, and "alone" is not "far".** Armenian forms its own branch and has, in this sample, no
same-branch neighbour other than its Eastern/Western pair. A binary "is the neighbour same-branch?" test therefore
penalises it automatically. But the *distance* tells the real story: Armenian's nearest non-Armenian systems are
Greek and Indo-Iranian, not the Romance or Germanic systems at the far side of the cloud. A singleton branch is a
fact about the sample, not a measurement of isolation.

**Areality falls out of the same map.** The dashed, cross-branch nearest-neighbour links land exactly where
contact history predicts. Albanian's nearest neighbour is Romanian — the Balkan *Sprachbund*. Romani's nearest
Italic neighbour is Romanian, matching its long presence in Romania. Each creole sits beside its lexifier
(Jamaican Creole by English, Negerhollands by Dutch, Seychelles Creole by the Romance systems). We did not tell
the map about contact; contact is simply where the branches leak, and the leaks are systematic. This is the
confluence view made measurable: the same geometry that shows descent also shows admixture.

## 5. Controls and robustness *(planned; next computation)*

Three controls complete the argument and are the immediate next step; we state them here so the claim is
falsifiable. (i) A **concept-permuted null**: rebuild the distances after shuffling which forms share a concept,
destroying coderivative structure; purity and silhouette should collapse toward chance. (ii) A **language-level
bootstrap** of purity and silhouette, resampling doculects with replacement, to show the 0.96 is not an artefact
of the particular sample. (iii) A **sensitivity sweep** over `MINSLOT`, the LexStat threshold, `MAXLANG` and the
feature subset, to show the picture is not knife-edge. The code paths for all three already exist in the pilot's
null and sensitivity machinery.

## 6. Discussion

The point cloud is the minimal realisation of the pilot's central claim. Where the pilot argued in the abstract
that "genealogy lives in the distribution", here the distribution *is* a map one can look at, and the genealogy is
its coarse clustering. Crucially the same map carries what a family tree cannot: areal contact and creolisation
appear as legible regions and links, not as anomalies to be excised. Descent, contact and confluence are read off
one geometry rather than modelled by three separate formalisms.

The method sits beside, but is not, lexical-distance phylogenetics. Phylogenetic distances typically count shared
cognates; ours measures how systems *behave* phonologically, pair by pair, and reads contact off the same
quantity. It is closer in spirit to phylogenetic-network thinking — where reticulation is expected — than to a
strict tree, which is appropriate to a reconstruction-free, confluence-first stance.

## 7. Limitations and scope

The distance is corpus- and aligner-dependent, and the two-dimensional figure is a shadow of the full matrix.
Only consonants are used here; vowels are deliberately deferred (see §9). One family is shown; scaling to many is
the programme's separate workstream. Direction and time are out of scope — those belong to the directed-layer
paper. Branch labels are only as good as the Glottolog classification we score against, and singleton branches
limit what purity can express (hence the graded-distance reading in §4).

## 8. Reproducibility

`make figure` redraws the point cloud from the bundled results with no corpus required;
`LEX_PATH=/path/to/lexibank make compute` regenerates the distances from a Lexibank CLDF lexicon. All parameters
(`MINSLOT`, `THR`, `MAXLANG`, `KNN`, feature subset) are environment-overridable in `src/compute_network.py`, and
the derived outputs live in `data/results/`. Code is MIT; text, figures and data are CC BY 4.0.

## 9. Future work — planned expansions

Two expansions are already scoped for when they are needed.

1. **The full Indo-European cloud, minor languages and dialects included.** The present 28 doculects are a
   convenience sample. A complete run — every adequately attested Indo-European variety, down to minor languages
   and dialects — would turn the sparse cloud into a dense manifold, in which dialect continua should appear as
   local ridges and the singleton-branch problem of §4 largely dissolves (Armenian, Albanian, Celtic gain
   neighbours). This is a scaling exercise on the same pipeline, not a change of method.

2. **A word-level point cloud (with vowels).** The present cloud has one point per *language*. A second database
   would place one point per *word*: each attested form embedded by its correspondence behaviour, so that we can
   see **how words themselves group** — whether coderivative sets form tight sub-clouds, where borrowings sit,
   whether some concepts are phonologically more conservative than others. This word-level view **must include
   vowels**, which the system-level consonant skeleton deliberately omits; the operator and distance definitions
   extend to vowels directly, at the cost of the extra alignment noise vowels introduce. Together the two clouds
   — languages and words — would let the same geometry be read at two grains.

## References *(to complete)*

Reuse the pilot's reference set; add: classical MDS (Torgerson 1952); lexical-distance phylogenetics; the Balkan
*Sprachbund* (e.g. Joseph; Friedman) and contact linguistics (Thomason & Kaufman) for the areal contrast set;
panphon (Mortensen et al.) and LexStat (List) for the tooling.
