# The System Point Cloud

### Genealogy and areality drawn from phonological correspondences alone — a reconstruction-free distance between language systems

**Alejandro Toledo Martínez** — Independent researcher (ORCID: 0009-0000-1277-9697)

**Preprint · DRAFT · CC BY 4.0**

**Companion to** *Additive Structure of Phonological Correspondences* (the pilot). **Repository:**
https://github.com/toledoal/languages-point-cloud

---

## Abstract  ‹fill final wording›

We define a distance between two documented language *systems* that uses no reconstruction and no family tree:
across statistically detected coderivative sets, align each language pair and count, at every aligned consonant
slot, the primary phonological features that differ; average that count. Embedding the resulting distance matrix
(classical MDS) and linking each system to its nearest neighbours makes a language family **draw itself** as a
point cloud. On 28 Indo-European varieties, a system's nearest neighbour is its own branch **96%** of the time
(silhouette **+0.27** by branch), and the branch labels are used only *after* the map is built, to colour and
score it. Off-branch nearest neighbours recover **areal** structure (Albanian↔Romanian and the Balkan
*Sprachbund*; Romani↔Romanian) and **creole↔lexifier** proximity. The point cloud is thus a direct, minimal
picture of the level at which — as the pilot argued — genealogy and contact actually live: the *distribution* of
correspondences, not the flat type inventory.

---

## 1. Introduction

- The pilot's finding, in one line: the additive geometry of the correspondence *type* inventory is
  representational; genealogical signal lives one level up, in the distribution. ‹stub›
- This paper makes that "one level up" visible in its simplest possible form — a pairwise distance and its point
  cloud — and shows it already carries both genealogy and areality. ‹stub›
- Stance: **discover, then contrast.** We build the map from correspondences only and bring in branch labels,
  contact history, and the Balkan literature *afterwards*, as an external check. We say **coderivative**, not
  cognate. ‹stub›

## 2. A distance between systems (reconstruction-free)

- Coderivative sets via LexStat (statistical, no etymologies supplied). ‹stub›
- Pairwise alignment (feature-distance Needleman–Wunsch); at each slot where both segments are consonants, the
  feature-difference count $\mathrm{fd}(a,b)=\lvert\{f\in\text{PRIM}:\phi_f(a)\neq\phi_f(b)\}\rvert$ (identity 0).
- $d(\ell,\ell')=\operatorname{mean}\mathrm{fd}$ over shared consonant slots (≥ `MINSLOT`). **Pairwise** by
  construction — it keeps the information a per-language marginal profile discards (this is why the marginal
  profile of exp. 1b separates branches only weakly, and the pairwise distance separates them at 0.96). ‹stub›
- Properties: symmetric, reconstruction-free, tree-free; range ≈ $[0,4]$; identity of systems → 0. ‹stub›

## 3. From distance to picture

- Classical MDS embedding of the distance matrix (2-D for the figure; the matrix itself is the object). ‹stub›
- Nearest-neighbour network ($k=3$); same-branch vs different-branch links distinguished. ‹stub›
- Scoring (post hoc, labels only now): **nearest-neighbour purity**, **silhouette by branch**, within- vs
  between-branch distance. ‹stub›

## 4. Results (Indo-European, n = 28)

- Headline: purity **0.96** (22/23 multi-branch, creoles excluded); silhouette **+0.27**. ‹fill table›
- The clusters, with numbers: Romance (Spanish↔Portuguese 1.56), Germanic (English↔Jamaican 0.59,
  Dutch↔Negerhollands 1.29), Balto-Slavic (Croatian↔Serbo-Croatian 0.78), Indo-Iranian (Persian↔Hindi 2.47),
  Greek (Ancient↔Modern 1.97), Armenian E↔W 0.89. ‹fill›
- **Graded proximity / singletons:** Armenian (alone in its branch here) is nearest to Ancient Greek (0.20 in the
  marginal metric; nearest Indo-Iranian in the pairwise metric) — alone ≠ far. ‹fill›
- **Areality falls out:** Albanian → Romanian; Romani → Romanian; creoles beside lexifiers. Cross-reference the
  Balkan *Sprachbund* literature as external confirmation, not input. ‹fill›
- Figure 1: the point cloud (`docs/figure-network-ie.html`). ‹embed static export›

## 5. Controls and robustness  ‹stub›

- Concept-permuted null (does purity collapse when coderivative structure is destroyed?). ‹fill›
- Language-level bootstrap of purity/silhouette. ‹fill›
- Sensitivity to `MINSLOT`, `THR`, `MAXLANG`, feature subset. ‹fill›

## 6. Discussion  ‹stub›

- The point cloud as the minimal realization of the pilot's Annex A ("genealogy lives in the distribution").
- Genealogy vs areality vs creolization as *readable regions* of one geometry — the coderivative/confluence view,
  measured.
- Relation to lexical-distance phylogenetics and to phylogenetic *networks*: we place systems by their
  correspondence behaviour rather than by shared-cognate counts, and we read contact off the same map.

## 7. Limitations and scope  ‹stub›

Corpus/aligner-dependent; MDS is a 2-D shadow of a higher-dimensional distance; consonants only (vowels deferred);
one family shown (scaling is the programme's W1). Direction/time are out of scope (that is the directed-layer
paper).

## 8. Reproducibility

`make figure` redraws from bundled results; `LEX_PATH=… make compute` regenerates the distances. Seeds and
parameters in `src/compute_network.py`. Durable outputs in `data/results/`.

## References  ‹stub›

Reuse the pilot's; add: classical MDS (Torgerson); lexical-distance phylogenetics; Balkan *Sprachbund* (e.g.
Joseph; Friedman) for the *contrast* set; areal/contact linguistics (Thomason & Kaufman).
