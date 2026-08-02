#!/usr/bin/env python3
"""Compare the ABSTRACT STRUCTURE of two (or more) point clouds built as SEPARATE FIELDS.

Methodological guardrail: two families must never share a distance space — embedding them together would assert a
direct relation we do not claim. So we NEVER align coordinates (no Procrustes, no shared MDS). We compare only
scale-free STRUCTURAL SIGNATURES of each independently-built dissimilarity matrix:
  · eigen-spectrum of the MDS Gram matrix → intrinsic dimensionality (participation ratio; %var in 2D; dims to 80%)
  · branch separation: mean within-branch / mean between-branch dissimilarity; silhouette; nearest-neighbour purity
  · the distribution of off-diagonal dissimilarity, normalised by its own median (shape, not position)
Then a figure overlays these signatures — an "abstraction of the clouds", coincidences of STRUCTURE only.

Reads data/results/network_{dist,coords}_<slug>.csv for each slug. Uso: ./.venv/bin/python src/structure_compare.py ie an
"""
import sys, os, csv
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
OUTDIR = os.path.join(HERE, "..", "docs", "figures")
os.makedirs(OUTDIR, exist_ok=True)
LABELS = {"ie": "Indo-European", "ie50": "Indo-European (dense)", "an": "Austronesian", "nd": "Nakh-Daghestanian"}


def load(slug):
    D = np.loadtxt(os.path.join(RES, f"network_dist_{slug}.csv"), delimiter=",", skiprows=1)
    rows = list(csv.DictReader(open(os.path.join(RES, f"network_coords_{slug}.csv"), encoding="utf-8")))
    branch = [r["branch"] for r in rows]
    return D, branch


def gram_eig(D):
    n = D.shape[0]; J = np.eye(n)-np.ones((n, n))/n
    B = -0.5*J@(D**2)@J
    w = np.sort(np.linalg.eigvalsh(B))[::-1]
    return w


def signatures(D, branch):
    n = D.shape[0]
    off = D[~np.eye(n, dtype=bool)]
    w = gram_eig(D); pos = w[w > 0]
    var2 = (w[0]+w[1])/pos.sum()
    pr = (pos.sum()**2)/(pos**2).sum()                 # participation ratio = effective dimensionality
    cum = np.cumsum(pos)/pos.sum(); dim80 = int(np.searchsorted(cum, 0.80))+1
    # separation
    win, bet = [], []
    for i in range(n):
        for j in range(i+1, n):
            (win if branch[i] == branch[j] else bet).append(D[i, j])
    win, bet = np.array(win), np.array(bet)
    ratio = win.mean()/bet.mean()
    # silhouette + purity
    sil = silhouette(D, branch); pur = purity(D, branch)
    return {"n": n, "median_d": float(np.median(off)), "var2": float(var2), "pr": float(pr),
            "dim80": dim80, "within": float(win.mean()), "between": float(bet.mean()),
            "ratio": float(ratio), "silhouette": sil, "purity": pur, "eig": w, "off_norm": off/np.median(off)}


def silhouette(D, labels):
    n = len(labels); s = []
    for i in range(n):
        same = [D[i, j] for j in range(n) if j != i and labels[j] == labels[i]]
        if not same:
            continue
        a = np.mean(same); oth = defaultdict(list)
        for j in range(n):
            if labels[j] != labels[i]:
                oth[labels[j]].append(D[i, j])
        if not oth:
            continue
        b = min(np.mean(v) for v in oth.values()); den = max(a, b)
        s.append((b-a)/den if den > 0 else 0.0)
    return float(np.mean(s)) if s else float("nan")


def purity(D, labels):
    n = len(labels); from_ = defaultdict(int)
    for l in labels:
        from_[l] += 1
    multi = [i for i in range(n) if from_[labels[i]] > 1]
    if not multi:
        return float("nan")
    return sum(1 for i in multi if labels[min((j for j in range(n) if j != i), key=lambda j: D[i, j])] == labels[i])/len(multi)


def main():
    slugs = sys.argv[1:] or ["ie", "an"]
    sig = {}
    for s in slugs:
        D, br = load(s); sig[s] = signatures(D, br)
    print("=== abstract structural comparison (SEPARATE fields; no shared space, no coordinate alignment) ===")
    hdr = ["family", "n", "median d", "%var 2D", "eff.dim(PR)", "dims→80%", "within/between", "silhouette", "purity"]
    print("  ".join(f"{h:>14}" for h in hdr))
    for s in slugs:
        g = sig[s]
        print("  ".join(str(x) for x in [
            f"{LABELS.get(s, s):>14}", f"{g['n']:>14}", f"{g['median_d']:>14.2f}", f"{100*g['var2']:>13.1f}%",
            f"{g['pr']:>14.1f}", f"{g['dim80']:>14}", f"{g['ratio']:>14.2f}", f"{g['silhouette']:>+14.3f}",
            f"{g['purity']:>14.2f}"]))

    # figure: (A) normalized scree overlay  (B) within/between + silhouette bars  (C) normalized dissimilarity dist
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.2))
    col = {"ie": "#0072B2", "ie50": "#332288", "an": "#D55E00", "nd": "#117733"}
    for s in slugs:
        w = sig[s]["eig"]; w = w[w > 0][:15]
        ax[0].plot(range(1, len(w)+1), w/w[0], "o-", ms=4, color=col.get(s, None), label=LABELS.get(s, s))
    ax[0].set_title("(A) Normalised MDS spectrum\n(shape of the geometry, scale-free)", fontsize=9)
    ax[0].set_xlabel("component"); ax[0].set_ylabel("eigenvalue / λ₁"); ax[0].legend(fontsize=8, frameon=False)

    x = np.arange(len(slugs)); wd = 0.35
    ax[1].bar(x-wd/2, [sig[s]["ratio"] for s in slugs], wd, color="#999933", label="within/between (↓ = separated)")
    ax[1].bar(x+wd/2, [sig[s]["silhouette"] for s in slugs], wd, color="#117733", label="silhouette (↑ = separated)")
    ax[1].axhline(1.0, color="#999933", lw=0.7, ls=":"); ax[1].axhline(0.0, color="#117733", lw=0.7, ls=":")
    ax[1].set_xticks(x); ax[1].set_xticklabels([LABELS.get(s, s) for s in slugs], fontsize=8)
    ax[1].set_title("(B) Branch separation\n(each in its own field)", fontsize=9); ax[1].legend(fontsize=7.5, frameon=False)

    for s in slugs:
        ax[2].hist(sig[s]["off_norm"], bins=40, histtype="step", density=True, color=col.get(s, None), label=LABELS.get(s, s))
    ax[2].set_title("(C) Dissimilarity distribution\n(each normalised by its own median)", fontsize=9)
    ax[2].set_xlabel("d / median(d)"); ax[2].set_ylabel("density"); ax[2].legend(fontsize=8, frameon=False)
    fig.suptitle("Abstract comparison of independently-built language clouds — structure only, never a shared space",
                 fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = os.path.join(OUTDIR, "figure-structure-compare.pdf")
    fig.savefig(out, bbox_inches="tight"); fig.savefig(out.replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
