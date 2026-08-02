# The Languages Point Cloud

### Genealogy and areality drawn from phonological correspondences alone — reconstruction-free

**Author:** Alejandro Toledo Martínez — Independent researcher · ORCID
[0009-0000-1277-9697](https://orcid.org/0009-0000-1277-9697)

A short, foundational method. Take a family of documented languages. For every **pair** of languages, measure how
their consonants correspond across statistically detected coderivative sets — the mean number of phonological
features that differ, per aligned consonant slot. That single number is a **distance between two systems**,
computed **without any reconstruction and without a family tree**. Lay every language out by that distance (MDS)
and connect each to its nearest neighbours, and the family **draws itself**: tight sub-clouds that turn out to be
the branches, plus off-branch links that turn out to be **areal contact** (Balkan) or **creoles beside their
lexifier**. The branch labels are added *last*, only to colour and score the picture — never to build it.

This is a companion to the pilot *[Additive Structure of Phonological
Correspondences](https://github.com/toledoal/phonological-correspondences)*. The pilot showed the additive
geometry of the *type* inventory is representational — genealogy lives one level up, in the **distribution** of
correspondences. This repo makes that one level visible in its simplest form: a point cloud.

## The headline (Indo-European, 28 documented varieties)

| Measure | Value | Meaning |
|---|---:|---|
| Nearest-neighbour purity | **0.96** (22/23) | a system's closest system is almost always its own branch |
| Silhouette by branch | **+0.27** | branches are separated in the distance geometry |
| Branch labels used to build the map | **0** | placement is from correspondences only |

Off-branch nearest neighbours are not noise — they are the interesting cases: Albanian → Romanian (Balkan
*Sprachbund*), Romani → Romanian (contact in Romania), each creole beside its lexifier. Contiguity is graded, and
a singleton branch (Armenian, alone in the sample) is *near* its relatives (Armenian → Ancient Greek), not far
from everything: being alone in the sample is a fact of sampling, not a distance.

## Reproduce

```bash
python3.12 -m venv .venv && ./.venv/bin/pip install -r requirements.txt

# 1) redraw the figure from the bundled results (no corpus needed):
make figure          # -> docs/figure-network-ie.html  (open in a browser)

# 2) recompute the distances from a Lexibank CLDF lexicon (heavier):
LEX_PATH=/path/to/lexibank make compute
```

The derived results (`data/results/network_{coords,edges,dist}_ie.csv`) are bundled so the figure reproduces
immediately; `make compute` regenerates them from the corpus.

## What is (and is not) claimed

- **Is:** a reconstruction-free, family-tree-free distance between language *systems*, and the empirical finding
  that genealogical + areal structure is already legible in it.
- **Is not:** a claim that history does not exist, or that this distance *is* the tree. It is a measurement of the
  distribution in which such structure lives; the tree is one coarse summary of this geometry. We say
  **coderivative**, not *cognate*: co-derived by recurrent correspondence, without positing a single ancestor.

## Method (one paragraph)

Coderivative sets are detected statistically (LexStat). Within each set, every language pair is aligned by a
feature-distance Needleman–Wunsch; at each slot where both segments are consonants, we count the primary panphon
features that differ (identity = 0). The distance `d(ℓ,ℓ')` is the mean of that count over all shared slots — a
pairwise quantity that keeps information a per-language marginal profile would discard. Classical MDS embeds the
distance matrix; each node is linked to its `k=3` nearest neighbours. See `docs/paper.en.md` for the full account
and `src/compute_network.py` for the code.

## Licence

Code MIT (`LICENSE`); text, figures, and data CC BY 4.0 (`LICENSE-docs.txt`).
