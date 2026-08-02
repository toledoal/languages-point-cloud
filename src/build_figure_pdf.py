#!/usr/bin/env python3
"""Static vector figure (PDF) of the system point cloud, for the paper. Reads data/results/network_*.csv."""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
OUTDIR = os.path.join(HERE, "..", "docs", "figures")
os.makedirs(OUTDIR, exist_ok=True)

SLUG = os.environ.get("SLUG", "ie")
FAMILYLABEL = os.environ.get("FAMILYLABEL", {"ie": "Indo-European", "an": "Austronesian", "nd": "Nakh-Daghestanian"}.get(SLUG, SLUG))
nodes = list(csv.DictReader(open(os.path.join(RES, f"network_coords_{SLUG}.csv"), encoding="utf-8")))
edges = list(csv.DictReader(open(os.path.join(RES, f"network_edges_{SLUG}.csv"), encoding="utf-8")))
pos = {n["name"]: n for n in nodes}

from collections import Counter
_bc = Counter(n["branch"] for n in nodes)
order = [b for b, _ in _bc.most_common()]                       # branches present, by size (family-agnostic)
OKABE = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9", "#F0E442", "#8A8F98",
         "#117733", "#882255", "#44AA99", "#999933", "#AA4499", "#332288", "#DDCC77", "#661100"]
color = {b: OKABE[i % len(OKABE)] for i, b in enumerate(order)}

fig, ax = plt.subplots(figsize=(9.2, 6.4))
# edges first
for e in edges:
    a, b = pos.get(e["src"]), pos.get(e["dst"])
    if not a or not b:
        continue
    same = a["branch"] == b["branch"]
    ax.plot([float(a["x"]), float(b["x"])], [float(a["y"]), float(b["y"])],
            color=("#b9b0a0" if same else "#b98a5e"), lw=(0.6 if same else 0.9),
            ls=("-" if same else (0, (2, 2))), zorder=1, alpha=0.8)
# nodes + labels (disambiguate duplicate names with a short dataset suffix)
_namecount = Counter(n["name"].split(" (")[0] for n in nodes)
for n in nodes:
    x, y = float(n["x"]), float(n["y"])
    ax.scatter([x], [y], s=70, c=color.get(n["branch"], "#888"),
               edgecolors="white", linewidths=1.1, zorder=3)
    lab = n["name"].split(" (")[0]
    if _namecount[lab] > 1:
        ds = n.get("lang", "").split("-")[0][:4]
        lab = f"{lab}·{ds}" if ds else lab
    ax.annotate(lab, (x, y), xytext=(6, 3), textcoords="offset points",
                fontsize=6.5, color="#3a352b", zorder=4)

handles = [Line2D([0], [0], marker="o", ls="", markersize=7, markerfacecolor=color[b],
                  markeredgecolor="white", label=b) for b in order]
handles += [Line2D([0], [0], color="#b9b0a0", lw=1, label="nearest neighbour, same branch"),
            Line2D([0], [0], color="#b98a5e", lw=1, ls=(0, (2, 2)), label="nearest neighbour, other branch")]
ax.legend(handles=handles, loc="upper left", fontsize=7.2, frameon=False, ncol=1, handletextpad=0.5)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title(f"{FAMILYLABEL} placed by consonantal-correspondence dissimilarity (MDS)",
             fontsize=10.5, pad=10)
fig.tight_layout()
out = os.path.join(OUTDIR, f"figure-network-{SLUG}.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
print("wrote", out)
