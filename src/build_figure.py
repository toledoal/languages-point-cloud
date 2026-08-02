#!/usr/bin/env python3
"""Genera la nube de puntos / red de sistemas (HTML autocontenido) desde los CSV de exp2."""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
SLUG = os.environ.get("SLUG", "ie")
OUT = os.path.join(HERE, "..", "docs", f"figure-network-{SLUG}.html")

nodes = list(csv.DictReader(open(os.path.join(RES, f"network_coords_{SLUG}.csv"), encoding="utf-8")))
edges = list(csv.DictReader(open(os.path.join(RES, f"network_edges_{SLUG}.csv"), encoding="utf-8")))

# vecinos por nodo (para el tooltip)
nbr = {}
for e in edges:
    nbr.setdefault(e["src"], []).append([e["dst"], float(e["dist"])])
for k in nbr:
    nbr[k] = sorted(nbr[k], key=lambda z: z[1])[:3]

# orden fijo de ramas (por tamaño) → color Okabe–Ito (CVD-safe)
order = ["Germanic", "Balto-Slavic", "Indo-Iranian", "Italic", "Graeco-Phrygian", "Armenic", "Albanian", "Celtic"]
OKABE = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9", "#F0E442", "#8A8F98"]
color = {b: OKABE[i] for i, b in enumerate(order)}
counts = {}
for n in nodes:
    counts[n["branch"]] = counts.get(n["branch"], 0) + 1

data = {
    "nodes": [{"name": n["name"], "branch": n["branch"], "x": float(n["x"]), "y": float(n["y"]),
               "nbr": nbr.get(n["name"], [])} for n in nodes],
    "edges": [{"s": e["src"], "d": e["dst"], "w": float(e["dist"])} for e in edges],
    "color": color, "order": order, "counts": counts,
}

html = """<title>Indo-European as a point cloud</title>
<style>
:root{
  --bg:#faf8f3; --panel:#fffdf8; --ink:#1c1a17; --muted:#6b6157; --line:#e6dfd2;
  --accent:#9a5b34; --ring:#fffdf8; --edge:#cbbfa9; --edgex:#b98a5e; --shadow:0 1px 3px rgba(60,45,25,.10);
}
@media (prefers-color-scheme:dark){:root{
  --bg:#141310; --panel:#1d1b17; --ink:#efe9df; --muted:#9c9385; --line:#2c2921;
  --accent:#e0a06a; --ring:#1d1b17; --edge:#3a352b; --edgex:#7a5c3c; --shadow:0 1px 3px rgba(0,0,0,.4);
}}
:root[data-theme=light]{--bg:#faf8f3;--panel:#fffdf8;--ink:#1c1a17;--muted:#6b6157;--line:#e6dfd2;--accent:#9a5b34;--ring:#fffdf8;--edge:#cbbfa9;--edgex:#b98a5e;--shadow:0 1px 3px rgba(60,45,25,.10);}
:root[data-theme=dark]{--bg:#141310;--panel:#1d1b17;--ink:#efe9df;--muted:#9c9385;--line:#2c2921;--accent:#e0a06a;--ring:#1d1b17;--edge:#3a352b;--edgex:#7a5c3c;--shadow:0 1px 3px rgba(0,0,0,.4);}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:40px 24px 64px}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 10px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:600;font-size:clamp(28px,4.4vw,44px);
  line-height:1.08;margin:0 0 14px;text-wrap:balance;letter-spacing:-.01em}
.lede{font-size:18px;color:var(--muted);max-width:64ch;margin:0 0 28px}
.lede b{color:var(--ink);font-weight:600}
.stats{display:flex;flex-wrap:wrap;gap:14px;margin:0 0 26px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px;box-shadow:var(--shadow)}
.stat .n{font-family:Georgia,serif;font-size:24px;font-weight:600;font-variant-numeric:tabular-nums}
.stat .l{font-size:12.5px;color:var(--muted)}
.figure{background:var(--panel);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);
  padding:8px;position:relative;overflow:hidden}
svg{display:block;width:100%;height:auto;touch-action:none}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;margin:16px 2px 0;font-size:13px}
.legend span{display:inline-flex;align-items:center;gap:7px;cursor:default;color:var(--muted)}
.legend i{width:11px;height:11px;border-radius:50%;display:inline-block;box-shadow:0 0 0 1.5px var(--ring)}
.legend b{color:var(--ink);font-weight:600}
.node circle{stroke:var(--ring);stroke-width:1.5;cursor:pointer;transition:r .12s}
.node text{font-size:9px;fill:var(--muted);pointer-events:none;transition:fill .12s}
.node.hi circle{stroke:var(--ink);stroke-width:2}
.node.hi text{fill:var(--ink);font-weight:600}
.node.dim{opacity:.22}
.tip{position:absolute;pointer-events:none;background:var(--panel);border:1px solid var(--line);
  border-radius:10px;padding:9px 12px;font-size:12.5px;box-shadow:var(--shadow);max-width:230px;opacity:0;
  transition:opacity .1s;z-index:5}
.tip h4{margin:0 0 2px;font-size:13px}
.tip .br{color:var(--muted);font-size:11.5px;margin-bottom:6px}
.tip .nb{display:flex;justify-content:space-between;gap:12px;font-variant-numeric:tabular-nums}
.tip .nb .ok{color:var(--accent)}
.note{font-size:13.5px;color:var(--muted);margin:22px 0 0;max-width:70ch}
.note code{background:var(--line);padding:1px 5px;border-radius:4px;font-size:12.5px}
</style>
<div class="wrap">
<p class="eyebrow">Phonological correspondences · a point cloud of languages</p>
<h1>Indo-European draws itself as a point cloud</h1>
<p class="lede">Each point is a language. Its position comes only from <b>how its consonants correspond to every
other language's</b> — the mean number of phonological features that differ, pair by pair. No family tree, no
reconstruction, and <b>the branch colours were added last, only to check the picture</b>. The contiguity is not
imposed; it emerges.</p>
<div class="stats" id="stats"></div>
<div class="figure"><svg id="plot" viewBox="0 0 900 620" aria-label="Point cloud of Indo-European languages"></svg>
<div class="tip" id="tip"></div></div>
<div class="legend" id="legend"></div>
<p class="note">Distance = mean count of differing panphon features per aligned consonant slot, over statistically
detected coderivative sets (LexStat); layout by classical MDS (the 2-D plane shows ~27% of the variance, so central
overlaps are partly projection). Solid links join a language to its 3 nearest neighbours within the same branch;
<span style="color:var(--edgex)">dashed</span> links are nearest neighbours in a <i>different</i> branch — these are
rare and only marginally interpretable as contact (see the paper). Branch structure is legible in the dissimilarity;
we do not claim to recover a tree, direction, or contact. Data: <code>network_*_ie.csv</code>.</p>
</div>
<script>
const DATA=__DATA__;
const svg=document.getElementById('plot'),tip=document.getElementById('tip');
const W=900,H=620,P=48;
const xs=DATA.nodes.map(n=>n.x),ys=DATA.nodes.map(n=>n.y);
const xmin=Math.min(...xs),xmax=Math.max(...xs),ymin=Math.min(...ys),ymax=Math.max(...ys);
const sx=v=>P+(v-xmin)/(xmax-xmin)*(W-2*P);
const sy=v=>P+(ymax-v)/(ymax-ymin)*(H-2*P);
const pos={};DATA.nodes.forEach(n=>pos[n.name]=n);
const NS="http://www.w3.org/2000/svg";
function el(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
// edges
const eg=el('g',{});svg.appendChild(eg);
DATA.edges.forEach(e=>{const a=pos[e.s],b=pos[e.d];if(!a||!b)return;
  const same=a.branch===b.branch;
  eg.appendChild(el('line',{x1:sx(a.x),y1:sy(a.y),x2:sx(b.x),y2:sy(b.y),
    stroke:same?'var(--edge)':'var(--edgex)','stroke-width':same?1:1.2,
    'stroke-dasharray':same?'':'3,3','stroke-opacity':same?.9:.85,'data-s':e.s,'data-d':e.d}));});
// nodes
const ng=el('g',{});svg.appendChild(ng);
DATA.nodes.forEach(n=>{const g=el('g',{class:'node','data-name':n.name});
  g.appendChild(el('circle',{cx:sx(n.x),cy:sy(n.y),r:6,fill:DATA.color[n.branch]}));
  const t=el('text',{x:sx(n.x)+9,y:sy(n.y)+3});t.textContent=n.name.replace(/ \\(.*\\)/,'').slice(0,16);
  g.appendChild(t);ng.appendChild(g);
  g.addEventListener('mouseenter',ev=>show(n,g));
  g.addEventListener('mousemove',ev=>move(ev));
  g.addEventListener('mouseleave',hide);});
function show(n,g){
  document.querySelectorAll('.node').forEach(x=>x.classList.add('dim'));
  const near=new Set([n.name,...n.nbr.map(z=>z[0])]);
  document.querySelectorAll('.node').forEach(x=>{if(near.has(x.dataset.name)){x.classList.remove('dim');}});
  g.classList.add('hi');g.classList.remove('dim');
  let rows=n.nbr.map(z=>{const ok=pos[z[0]].branch===n.branch;
    return `<div class="nb"><span class="${ok?'ok':''}">${ok?'●':'○'} ${z[0].replace(/ \\(.*\\)/,'')}</span><span>${z[1].toFixed(2)}</span></div>`;}).join('');
  tip.innerHTML=`<h4>${n.name.replace(/ \\(.*\\)/,'')}</h4><div class="br">${n.branch}</div>${rows}`;
  tip.style.opacity=1;}
function move(ev){const r=svg.getBoundingClientRect();
  tip.style.left=Math.min(ev.clientX-r.left+14,r.width-240)+'px';
  tip.style.top=(ev.clientY-r.top+14)+'px';}
function hide(){tip.style.opacity=0;document.querySelectorAll('.node').forEach(x=>{x.classList.remove('dim','hi');});}
// stats
document.getElementById('stats').innerHTML=[
  ['0.98','nearest neighbour shares its branch (43/44)'],
  ['+0.34','silhouette by branch (positive = separated)'],
  ['p≈0.0001','vs a 10k label-permutation null'],
  [DATA.nodes.length,'language systems, 0 labels used to place them'],
].map(s=>`<div class="stat"><div class="n">${s[0]}</div><div class="l">${s[1]}</div></div>`).join('');
// legend
document.getElementById('legend').innerHTML=DATA.order.map(b=>
  `<span><i style="background:${DATA.color[b]}"></i><b>${b}</b> ${DATA.counts[b]||0}</span>`).join('');
</script>
"""
html = html.replace("__DATA__", json.dumps(data))

open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, len(html), "bytes")
