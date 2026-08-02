# A Point Cloud of Languages

### A reconstruction-free, feature-decomposable dissimilarity between language systems

**Author:** Alejandro Toledo Martínez — Independent researcher · ORCID
[0009-0000-1277-9697](https://orcid.org/0009-0000-1277-9697)

A methodological study. For every **pair** of documented languages in a family we compute a **dissimilarity**: the
mean number of primary phonological features that differ per aligned consonant slot, over statistically detected
coderivative sets (LexStat) in concept-aligned wordlists. No reconstruction, no family tree, and no branch labels
enter the computation; labels are consulted only afterwards, to score the resulting geometry. The input is *not*
"phonology alone" — it is phonological dissimilarity within concept-matched, inferred lexical correspondences.

This is a companion to the pilot *[Additive Structure of Phonological
Correspondences](https://github.com/toledoal/phonological-correspondences)*.

## What the paper shows (Indo-European, 50 doculects)

| Measure | Value | Meaning |
|---|---:|---|
| Nearest-neighbour purity | **0.98** (43/44, multi-member branches, creoles excluded; 0.958 over all doculects) | a system's closest system is almost always its own branch |
| Silhouette by branch | **+0.34** | branches are separated in the dissimilarity geometry |
| Label-permutation significance | **p < 10⁻⁴** | 0 of 10,000 label permutations reach the observed values |
| Branch labels used to build the map | **0** | placement is from correspondences only |

**Honesty notes, up front.** Branch recovery is *not* the contribution — a plain edit distance ties our purity and
an unfiltered all-concept baseline matches or beats it. The claimed value is **feature-level attribution**
(`src/decompose.py`: every matrix entry opens into an exact per-feature ledger, $d=\sum_f d_f$, on the same
correspondence units as the pilot's operators — a narrow claim relative to feature-aware traditions like ALINE,
which score alignments by features; ours is an additive decomposition of the final system-level dissimilarity)
plus a slightly cleaner margin (silhouette). Cross-branch proximities are rare and we make **no areal
claim**. The matrices used in analysis are **complete observed submatrices — zero imputed values** (an earlier
internal version mean-imputed missing pairs; that is removed, and the Austronesian corpus turns out to be too
sparse in Lexibank to support a large complete field — disclosed in the paper, not hidden).

Cross-family comparisons (Nakh-Daghestanian, Austronesian) are built as **separate fields** — never a shared
distance space, which would falsely assert a direct relation between families — and remain exploratory pending
matched sampling.

## Reproduce

```bash
python3.12 -m venv .venv && ./.venv/bin/pip install -r requirements.txt   # pinned versions

make figure                       # redraw the IE point cloud from bundled results (no corpus needed)
LEX_PATH=/path/to/lexibank make compute      # recompute the IE field (n=50, the paper's setting)
LEX_PATH=... make compute-nd                 # Nakh-Daghestanian field
LEX_PATH=... make compute-an                 # Austronesian field
LEX_PATH=... make analysis                   # significance, MDS diagnostics, baselines, coverage (n=50)
LEX_PATH=... make controls                   # robustness controls (n=50)
make compare                                 # abstract structural comparison (separate fields)
make manifest                                # doculect manifests (Appendix A)
```

Derived results are bundled under `data/results/` (matrices, coordinates, manifests, analysis logs) so figures
reproduce without the corpus. Each experiment's exact `MAXLANG` is fixed in the `Makefile`.

## Licence

Code MIT (`LICENSE`); text, figures, and data CC BY 4.0 (`LICENSE-docs.txt`).
