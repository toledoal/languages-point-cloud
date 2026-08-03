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

import numpy as np
fig, ax = plt.subplots(figsize=(12.5, 8.6))
# edges first
for e in edges:
    a, b = pos.get(e["src"]), pos.get(e["dst"])
    if not a or not b:
        continue
    same = a["branch"] == b["branch"]
    ax.plot([float(a["x"]), float(b["x"])], [float(a["y"]), float(b["y"])],
            color=("#b9b0a0" if same else "#b98a5e"), lw=(0.6 if same else 0.9),
            ls=("-" if same else (0, (2, 2))), zorder=1, alpha=0.8)

# --- choose which nodes to label (reviewer #18: a curated subset; full labels live in the interactive figure) ---
_namecount = Counter(n["name"].split(" (")[0] for n in nodes)
xy = {n["name"]: (float(n["x"]), float(n["y"])) for n in nodes}
cross_ep = set()
for e in edges:
    a, b = pos.get(e["src"]), pos.get(e["dst"])
    if a and b and a["branch"] != b["branch"]:
        cross_ep.add(e["src"]); cross_ep.add(e["dst"])
# one anchor per branch = node closest to its branch centroid
anchor = set()
for br in order:
    members = [n["name"] for n in nodes if n["branch"] == br]
    if not members:
        continue
    cx = np.mean([xy[m][0] for m in members]); cy = np.mean([xy[m][1] for m in members])
    anchor.add(min(members, key=lambda m: (xy[m][0]-cx)**2 + (xy[m][1]-cy)**2))
to_label = set(); _dup_seen = set()          # keyed by unique doculect id (`lang`), since twins share a name
for n in nodes:
    nm = n["name"]; base = nm.split(" (")[0]
    if _namecount[base] > 1:                 # near-twins sit on the same spot → label the base name ONCE
        if base not in _dup_seen:
            _dup_seen.add(base); to_label.add(n["lang"])
    elif _bc[n["branch"]] == 1 or nm in cross_ep or nm in anchor:
        to_label.add(n["lang"])

# draw all nodes
for n in nodes:
    x, y = xy[n["name"]]
    ax.scatter([x], [y], s=70, c=color.get(n["branch"], "#888"),
               edgecolors="white", linewidths=1.1, zorder=3)
# selective labels with vertical de-collision + leader lines
xs = [xy[n["name"]][0] for n in nodes]; ys = [xy[n["name"]][1] for n in nodes]
xr = max(xs)-min(xs); yr = max(ys)-min(ys); xmid = np.mean(xs)
ygap = 0.032*yr; xgap = 0.16*xr
placed = []
for n in sorted((n for n in nodes if n["lang"] in to_label), key=lambda n: -xy[n["name"]][1]):
    x, y = xy[n["name"]]; ly = y + 0.012*yr
    while any(abs(px-x) < xgap and abs(py-ly) < ygap for px, py in placed):
        ly -= ygap
    placed.append((x, ly))
    right = x >= xmid
    dxd = 0.015*xr if right else -0.015*xr
    ax.annotate(n["name"].split(" (")[0], xy=(x, y), xytext=(x+dxd, ly), textcoords="data",
                ha=("left" if right else "right"), va="center",
                fontsize=6.8, color="#2a2620", zorder=5,
                arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.4, shrinkA=0, shrinkB=2))

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
