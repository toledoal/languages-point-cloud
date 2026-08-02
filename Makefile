VENV=./.venv/bin/python

.PHONY: figure compute clean

# Redraw the point cloud from the bundled results (no corpus needed).
figure:
	$(VENV) src/build_figure.py

# Recompute distances from a Lexibank CLDF lexicon, then redraw.
# Requires LEX_PATH=/path/to/lexibank (dir with forms.csv, languages.csv).
compute:
	$(VENV) src/compute_network.py
	$(VENV) src/build_figure.py

clean:
	rm -f data/results/_tn.tsv

# Build the paper PDF (docs/paper.en.pdf). Needs xelatex + matplotlib for the figure.
paper:
	$(VENV) src/build_figure_pdf.py
	bash docs/build-paper.sh
