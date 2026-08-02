#!/bin/bash
set -e; cd "$(dirname "$0")"
BASE=paper.en
python3 md2tex.py $BASE.md ./$BASE.tex
INJ='\\setmonofont{Menlo}[Scale=0.85]\n\\usepackage{newunicodechar}\n\\newunicodechar{⊕}{\\ensuremath{\\oplus}}\n\\newunicodechar{⊆}{\\ensuremath{\\subseteq}}\n\\newunicodechar{∖}{\\ensuremath{\\setminus}}\n\\newunicodechar{⟨}{\\ensuremath{\\langle}}\n\\newunicodechar{⟩}{\\ensuremath{\\rangle}}\n\\newunicodechar{≤}{\\ensuremath{\\leq}}\n\\newunicodechar{≥}{\\ensuremath{\\geq}}\n\\newunicodechar{≈}{\\ensuremath{\\approx}}\n\\newunicodechar{×}{\\ensuremath{\\times}}\n\\newunicodechar{Δ}{\\ensuremath{\\Delta}}\n\\newunicodechar{Ω}{\\ensuremath{\\Omega}}\n\\newunicodechar{ρ}{\\ensuremath{\\rho}}\n\\newunicodechar{τ}{\\ensuremath{\\tau}}\n\\newunicodechar{κ}{\\ensuremath{\\kappa}}\n\\newunicodechar{σ}{\\ensuremath{\\sigma}}\n\\newunicodechar{ʲ}{\\textsuperscript{j}}\n\\newunicodechar{ˀ}{\\textsuperscript{ʔ}}\n\\newunicodechar{ⁿ}{\\textsuperscript{n}}\n'
perl -0pi -e "s/\\\\begin\{document\}/$INJ\\\\begin{document}/ unless /setmonofont/" $BASE.tex
xelatex -interaction=nonstopmode $BASE.tex >/dev/null 2>&1 || true
xelatex -interaction=nonstopmode $BASE.tex >/dev/null 2>&1 || true
rm -f $BASE.aux $BASE.out $BASE.toc
echo "→ docs/$BASE.pdf ($(($(wc -c < $BASE.pdf)/1024)) KB)"
