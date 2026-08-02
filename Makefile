VENV=./.venv/bin/python

# Immutable per-experiment configuration (the paper's exact settings).
IE_MAXLANG=50
AN_MAXLANG=45
ND_MAXLANG=45
SLUGS?=ie an nd

.PHONY: figure compute compute-ie compute-an compute-nd compute-family analysis controls manifest compare paper clean

# Redraw the point cloud from the bundled results (no corpus needed).
figure:
	$(VENV) src/build_figure.py

# Reproduce the paper's main Indo-European field (n=50). Requires LEX_PATH=/path/to/lexibank.
compute: compute-ie

compute-ie:
	LEX_PATH=$${LEX_PATH} FAMILY="Indo-European" SLUG=ie MAXLANG=$(IE_MAXLANG) $(VENV) src/compute_network.py
	SLUG=ie $(VENV) src/build_figure.py

compute-an:
	LEX_PATH=$${LEX_PATH} FAMILY="Austronesian" SLUG=an MAXLANG=$(AN_MAXLANG) $(VENV) src/compute_network.py

compute-nd:
	LEX_PATH=$${LEX_PATH} FAMILY="Nakh-Daghestanian" SLUG=nd MAXLANG=$(ND_MAXLANG) $(VENV) src/compute_network.py

# Build any family's cloud on its OWN field (SLUG/FAMILY/MAXLANG env).
compute-family:
	LEX_PATH=$${LEX_PATH} FAMILY=$${FAMILY} SLUG=$${SLUG} MAXLANG=$${MAXLANG} $(VENV) src/compute_network.py

# Full analysis at the paper's n=50: label-permutation significance, MDS diagnostics, baselines, coverage.
analysis:
	LEX_PATH=$${LEX_PATH} MAXLANG=$(IE_MAXLANG) $(VENV) src/analysis.py

# Robustness controls (concept-permuted ablation, subsampling, sensitivity) at the paper's n=50.
controls:
	LEX_PATH=$${LEX_PATH} MAXLANG=$(IE_MAXLANG) $(VENV) src/controls.py

# Doculect manifests (Appendix A): FAMILY/MAXLANG env, defaults to IE at n=50.
manifest:
	LEX_PATH=$${LEX_PATH} MAXLANG=$(IE_MAXLANG) $(VENV) src/manifest.py

# Abstract structural comparison of separate fields (never a shared space). Default: the paper's three.
compare:
	$(VENV) src/structure_compare.py $(SLUGS)

# Build the paper PDF (docs/paper.en.pdf). Needs xelatex + matplotlib for the figures.
paper:
	SLUG=ie $(VENV) src/build_figure_pdf.py
	$(VENV) src/structure_compare.py $(SLUGS)
	bash docs/build-paper.sh

clean:
	rm -f data/results/_tn_*.tsv

manifest-ie:
	LEX_PATH=$${LEX_PATH} FAMILY="Indo-European" MAXLANG=$(IE_MAXLANG) $(VENV) src/manifest.py
manifest-an:
	LEX_PATH=$${LEX_PATH} FAMILY="Austronesian" MAXLANG=$(AN_MAXLANG) $(VENV) src/manifest.py
manifest-nd:
	LEX_PATH=$${LEX_PATH} FAMILY="Nakh-Daghestanian" MAXLANG=$(ND_MAXLANG) $(VENV) src/manifest.py
manifest-all: manifest-ie manifest-an manifest-nd
