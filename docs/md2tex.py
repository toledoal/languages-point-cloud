#!/usr/bin/env python3
"""Minimal, tailored Markdown→LaTeX converter for the endolinguistics paper pipeline (MD→TeX→PDF).
Handles the subset used in docs/endolinguistic-structure.md: title/subtitle/author front matter, ##/### headings,
booktabs tables, blockquote callouts (Insight/Hypothesis/Question/generic) as tcolorbox, $$ math blocks, - / N.
lists, and inline **bold** *italic* `code` $math$. Emits a full xelatex-ready .tex (Unicode class symbols OK).
Usage: python3 docs/md2tex.py docs/endolinguistic-structure.md docs/paper/endolinguistic-structure.tex
"""
import sys, re, os

SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}
def esc(t):
    # escape LaTeX specials in plain text; protect $...$ math and `code` first
    parts = re.split(r"(\$[^$]*\$|`[^`]*`)", t)
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:  # math or code span
            if p.startswith("`"):
                _tt = p[1:-1].replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("#", r"\#").replace("&", r"\&").replace("%", r"\%").replace("{", r"\{").replace("}", r"\}")
                # insert break opportunities so long paths/ids don't overflow the margin
                _tt = _tt.replace("/", r"/\allowbreak ").replace(r"\_", r"\_\allowbreak ").replace(".", r".\allowbreak ")
                out.append(r"\texttt{" + _tt + "}")
            else:
                out.append(p)  # keep math verbatim
        else:
            p = re.sub(r"\\([*_#`~\[\]\\{}&%])", r"\1", p)  # de-escapar escapes markdown (\* \_ …) → literal
            for k, v in SPECIAL.items():
                p = p.replace(k, v)
            out.append(p)
    return "".join(out)

def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"\\emph{\1}", t)
    t = t.replace("→", r"$\to$").replace("↦", r"$\mapsto$").replace("≠", r"$\neq$").replace("≈", r"$\approx$")
    t = t.replace("≥", r"$\geq$").replace("≤", r"$\leq$").replace("×", r"$\times$").replace("↑", r"$\uparrow$").replace("↓", r"$\downarrow$")
    t = t.replace("↔", r"$\leftrightarrow$").replace("⊕", r"$\oplus$").replace("⊖", r"$\ominus$")
    t = t.replace("Ϻ", r"{\uni Ϻ}")   # San (U+03FA) via Arial fallback (STIX lacks it)
    t = t.replace("∘", r"$\circ$").replace("∝", r"$\propto$").replace("★", r"$\star$").replace("∅", r"$\emptyset$")
    t = t.replace("⟶", r"$\longrightarrow$").replace("⟷", r"$\longleftrightarrow$")
    t = t.replace("𝒞", r"$\mathcal{C}$").replace("𝒬", r"$\mathcal{Q}$")
    t = t.replace("Ϻ", r"{\uni Ϻ}")   # re-run in case a mapping reintroduced it (no-op otherwise)
    return t

def _rawlen(cell):
    return len(re.sub(r"\*\*|\*|`", "", cell))
def table(rows):
    header = rows[0]; align = rows[1]; body = rows[2:]
    cols = [c.strip() for c in header.strip("|").split("|")]
    ncol = len(cols)
    aligns = []
    for a in align.strip("|").split("|"):
        a = a.strip()
        aligns.append("r" if a.endswith(":") and not a.startswith(":") else ("c" if a.startswith(":") and a.endswith(":") else "l"))
    while len(aligns) < ncol: aligns.append("l")
    # per-column max visible length → wide columns wrap
    colmax = [0] * ncol
    for r in [header] + body:
        cs = [c.strip() for c in r.strip("|").split("|")]
        for i in range(min(ncol, len(cs))): colmax[i] = max(colmax[i], _rawlen(cs[i]))
    # longest single (unbreakable) word per column — a p{} column must be at least this wide
    colword = [1] * ncol
    for r in [header] + body:
        cs = [c.strip() for c in r.strip("|").split("|")]
        for i in range(min(ncol, len(cs))):
            for w in re.sub(r"\*\*|\*|`", "", cs[i]).split():
                colword[i] = max(colword[i], len(w))
    LONG = 18
    wide = any(m > LONG for m in colmax)
    hdr = " & ".join(inline(c) for c in cols) + r" \\"
    body_tex = []
    for r in body:
        cells = [c.strip() for c in r.strip("|").split("|")]
        body_tex.append(" & ".join(inline(c) for c in cells) + r" \\")
    if wide:  # longtable with proportional p{} widths -> breaks across pages (repeating header)
        cw = [min(m, 60) for m in colmax]   # cap so a very long wrapping column doesn't starve the others
        tot = sum(cw) or 1
        # leave room for inter-column padding (2*ncol*\tabcolsep) so the table fits \linewidth.
        # with \tabcolsep=3pt and ncol columns, padding ~ 6pt*ncol; budget the p{} widths below 1.0 accordingly.
        avail = max(0.55, 0.94 - 0.018 * ncol)
        # proportional widths, then raise any column to fit its longest word (≈82 small chars per full line),
        # then reclaim the overshoot from the columns that still have slack above their floor.
        prop = [avail * cw[i] / tot for i in range(ncol)]
        floor = [min(0.40, colword[i] / 82.0) for i in range(ncol)]
        wdt = [max(prop[i], floor[i]) for i in range(ncol)]
        excess = sum(wdt) - avail
        if excess > 0:
            slack = [max(0.0, wdt[i] - floor[i]) for i in range(ncol)]
            ts = sum(slack) or 1.0
            wdt = [wdt[i] - excess * slack[i] / ts for i in range(ncol)]
        spec = "".join(r">{\RaggedRight\arraybackslash}p{%.3f\linewidth}" % max(0.05, wdt[i])
                       for i in range(ncol))
        out = [r"{\small\setlength{\tabcolsep}{3pt}\begin{longtable}{" + spec + "}", r"\toprule",
               hdr, r"\midrule", r"\endhead"] + body_tex + [r"\bottomrule", r"\end{longtable}}"]
    else:
        out = [r"\begin{center}\small", r"\begin{tabular}{" + "".join(aligns) + "}", r"\toprule",
               hdr, r"\midrule"] + body_tex + [r"\bottomrule", r"\end{tabular}", r"\end{center}"]
    return "\n".join(out)

CALLOUT = [("Insight", "insightbox"), ("Hypothesis", "hypobox"), ("Question", "questionbox")]
def callout(lines):
    body = " ".join(l[2:] if l.startswith("> ") else l[1:] for l in lines).strip()
    kind = "genericbox"
    for key, env in CALLOUT:
        if body.lstrip().startswith("**" + key) or ("**" + key) in body[:12]:
            kind = env; break
    return r"\begin{" + kind + "}" + "\n" + inline(body) + "\n" + r"\end{" + kind + "}"

def convert_body(lines):
    out = []; i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "---":
            out.append(r"\medskip"); i += 1; continue
        mimg = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", ln.strip())
        if mimg:
            cap, path = mimg.group(1), mimg.group(2)
            w = "0.98"
            mw = re.search(r"\|w=([0-9.]+)$", path)
            if mw: w = mw.group(1); path = path[:mw.start()]
            out.append(r"\begin{figure}[htbp]\centering\includegraphics[width=" + w +
                       r"\linewidth]{" + path + r"}\caption{" + inline(cap) + r"}\end{figure}")
            i += 1; continue
        if ln.lstrip().startswith("```"):   # fenced block
            info = ln.lstrip()[3:].strip().lower()
            i += 1; raw = []
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                raw.append(lines[i].rstrip("\n")); i += 1
            if i < len(lines): i += 1  # skip closing fence
            if info in ("latex", "tex"):  # raw LaTeX passthrough (figures / tikz) — emit verbatim, no escaping
                out.append("\n".join(raw))
            else:                          # code -> verbatim block (preserve line breaks, no escaping)
                out.append("{\\small\\begin{verbatim}\n" + "\n".join(raw) + "\n\\end{verbatim}}")
            continue
        if ln.startswith("# ") and not ln.startswith("## "):   # part divider: newpage + large centered heading
            out.append(r"\newpage\begin{center}{\Large\bfseries " + inline(ln[2:].strip()) +
                       r"}\end{center}\vspace{0.6em}"); i += 1; continue
        if ln.startswith("## ") and not ln.startswith("### "):
            out.append(r"\section*{" + inline(ln[3:].strip()) + "}"); i += 1; continue
        if ln.startswith("### "):
            out.append(r"\subsection*{" + inline(ln[4:].strip()) + "}"); i += 1; continue
        if ln.strip().startswith("$$"):
            block = [ln]; i += 1
            if ln.strip().endswith("$$") and len(ln.strip()) > 2:  # single-line $$...$$
                inner = ln.strip()[2:-2]
                out.append(r"\[" + inner + r"\]"); continue
            while i < len(lines) and not lines[i].strip().endswith("$$"):
                block.append(lines[i]); i += 1
            if i < len(lines): block.append(lines[i]); i += 1
            inner = "\n".join(block).strip().strip("$")
            out.append(r"\[" + inner + r"\]"); continue
        if ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i]); i += 1
            out.append(callout(block)); continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i+1]):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            out.append(table(rows)); continue
        def _cont(nxt):  # indented, non-blank continuation of the current list item (not a new item)
            return nxt.strip() and re.match(r"^\s+\S", nxt) and not re.match(r"^\s*([-*]|\d+\.)\s", nxt)
        if re.match(r"^\s*[-*] ", ln):
            raw = []
            while i < len(lines):
                if re.match(r"^\s*[-*] ", lines[i]):
                    raw.append(re.sub(r"^\s*[-*] ", "", lines[i])); i += 1
                elif raw and _cont(lines[i]):
                    raw[-1] += " " + lines[i].strip(); i += 1
                else: break
            out.append(r"\begin{itemize}\setlength{\itemsep}{2pt}")
            out += [r"  \item " + inline(it) for it in raw]
            out.append(r"\end{itemize}"); continue
        if re.match(r"^\s*\d+\. ", ln):
            raw = []
            while i < len(lines):
                if re.match(r"^\s*\d+\. ", lines[i]):
                    raw.append(re.sub(r"^\s*\d+\. ", "", lines[i])); i += 1
                elif raw and _cont(lines[i]):
                    raw[-1] += " " + lines[i].strip(); i += 1
                else: break
            out.append(r"\begin{enumerate}\setlength{\itemsep}{2pt}")
            out += [r"  \item " + inline(it) for it in raw]
            out.append(r"\end{enumerate}"); continue
        if ln.strip() == "":
            out.append(""); i += 1; continue
        # párrafo de texto: juntar líneas consecutivas antes del inline (para negrita/cursiva que envuelve saltos)
        para = [ln]; i += 1
        while i < len(lines):
            nx = lines[i]
            if (nx.strip() == "" or nx.strip() == "---" or nx.startswith(("#", ">", "|"))
                    or nx.strip().startswith("$$") or re.match(r"^\s*([-*]|\d+\.)\s", nx)
                    or re.match(r"^!\[", nx.strip())):
                break
            para.append(nx); i += 1
        out.append(inline(" ".join(x.strip() for x in para)))
    return "\n".join(out)

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage{fontspec}
\setmainfont{STIX Two Text}
\newfontfamily\uni{Arial}
\usepackage{amsmath,amssymb}
\usepackage[a4paper,margin=2.4cm]{geometry}
\usepackage{booktabs}
\usepackage{array}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{ragged2e}
\newcolumntype{Y}{>{\RaggedRight\arraybackslash}X}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\graphicspath{{../figures/}{figures/}}
\usepackage{microtype}
% tolerate hard-to-break lines instead of spilling into the margin
\emergencystretch=3em
% inline code (\texttt file paths, ids) gets break points at / _ . inserted by the converter
\usepackage[dvipsnames,svgnames]{xcolor}
\usepackage[colorlinks=true,linkcolor=NavyBlue,citecolor=NavyBlue,urlcolor=NavyBlue]{hyperref}
% base-only callout boxes (no tcolorbox available): captured minipage inside \fcolorbox
\newsavebox{\cobox}
\newenvironment{callout}[1]{%
  \colorlet{cofr}{#1!65}\colorlet{cobg}{#1!7}%
  \begin{lrbox}{\cobox}\begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule-4pt}%
  \small\setlength{\parskip}{0.4em}\setlength{\parindent}{0pt}}%
  {\end{minipage}\end{lrbox}\par\medskip\noindent
   {\setlength{\fboxrule}{0.5pt}\setlength{\fboxsep}{6pt}\fcolorbox{cofr}{cobg}{\usebox{\cobox}}}\par\medskip}
\newenvironment{insightbox}{\begin{callout}{NavyBlue}}{\end{callout}}
\newenvironment{hypobox}{\begin{callout}{OliveGreen}}{\end{callout}}
\newenvironment{questionbox}{\begin{callout}{Sepia}}{\end{callout}}
\newenvironment{genericbox}{\begin{callout}{black}}{\end{callout}}
\setlength{\parskip}{0.5em}\setlength{\parindent}{0pt}
\title{@@TITLE@@\\[2pt]\large @@SUBTITLE@@}
\author{@@AUTHOR@@}
\date{}
\begin{document}
\maketitle
"""

def main():
    src, dst = sys.argv[1], sys.argv[2]
    text = open(src, encoding="utf-8").read()
    lines = text.split("\n")
    # front matter
    title = subtitle = author = ""
    body_start = 0
    for j, ln in enumerate(lines):
        if ln.startswith("# ") and not title:
            title = inline(ln[2:].strip())
        elif ln.startswith("### ") and title and not subtitle:
            subtitle = inline(ln[4:].strip())
        elif ln.startswith("**") and subtitle and not author:
            author = inline(ln.strip().strip("*")).replace(r"\textbf{", "").rstrip("}")
            author = re.sub(r"\*+", "", ln).strip()
            author = inline(author)
        if ln.startswith("## "):   # first real section = Abstract
            body_start = j; break
    # recover the front-matter symbol-key blockquote (before Abstract) as a leading callout
    sk = [l for l in lines[:body_start] if l.startswith(">")]
    symkey = callout(sk) + "\n\n" if sk else ""
    body = symkey + convert_body(lines[body_start:])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        pre = (PREAMBLE.replace("@@TITLE@@", title).replace("@@SUBTITLE@@", subtitle)
               .replace("@@AUTHOR@@", author or "Alejandro Toledo Mart\\'inez"))
        f.write(pre)
        f.write(body)
        f.write("\n\\end{document}\n")
    print(f"wrote {dst} ({len(body.splitlines())} body lines)")

if __name__ == "__main__":
    main()
