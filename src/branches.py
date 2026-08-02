#!/usr/bin/env python3
"""Mapeo lengua → RAMA (subgrupo genealógico) por familia, GENERAL vía la clasificación de Glottolog.

Motivación (revisión peer §6): el "álgebra IE" podría ser la SUPERPOSICIÓN de álgebras de rama dominada por las
ramas mejor muestreadas. Para probarlo hay que particionar cada familia en sus ramas. El campo Subgroup de
Lexibank está vacío, así que usamos la clasificación de Glottolog (ruta de glottocodes desde la raíz de la
familia hasta cada lengua) cacheada en data/glottolog_classification.csv.

Corte de árbol POR TAMAÑO: descender desde la raíz de la familia por la ruta de cada lengua hasta el primer nodo
que cubra ≤ MAXFRAC de la familia (rompe los mega-clados tipo Malayo-Polynesian, conserva enteras las ramas
pequeñas). Es family-general y reproducible; el nivel efectivo lo fija el propio muestreo, no una decisión ad hoc.

Config por env: TF_BRANCH_MAXFRAC (default 0.5). Familias conocidas → glottocode raíz en FAMILY_ROOT.
"""
import os, csv
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
LEX = os.environ.get("LEX_PATH", os.path.abspath(os.path.join(HERE, "..", "..", "data", "lexicon", "lexibank")))

# glottocode de la raíz de cada familia (Glottolog). Ampliable.
FAMILY_ROOT = {
    "Indo-European": "indo1319",
    "Austronesian": "aust1307",
    "Nakh-Daghestanian": "nakh1245",
    "Sino-Tibetan": "sino1245",
    "Atlantic-Congo": "atla1278",
    "Afro-Asiatic": "afro1255",
    "Turkic": "turk1311",
    "Uralic": "ural1272",
    "Dravidian": "drav1251",
}


def _load_tables():
    names, paths = {}, {}
    gl = os.path.join(DATA, "glottolog_languages.csv")
    cl = os.path.join(DATA, "glottolog_classification.csv")
    for r in csv.DictReader(open(gl, encoding="utf-8")):
        names[r["Glottocode"]] = r["Name"]
    for r in csv.DictReader(open(cl, encoding="utf-8")):
        paths[r["Glottocode"]] = r["Path"]
    return names, paths


def branch_map(family, maxfrac=None):
    """→ (assign: lang_ID→branch_name, counts: Counter(branch_name→#langs), names_ok: bool).

    Solo asigna lenguas con clasificación en Glottolog. Las ramas se nombran con el nombre Glottolog del nodo.
    """
    maxfrac = float(os.environ.get("TF_BRANCH_MAXFRAC", maxfrac if maxfrac is not None else 0.5))
    code = FAMILY_ROOT.get(family)
    names, paths = _load_tables()
    langs = [r for r in csv.DictReader(open(f"{LEX}/languages.csv", encoding="utf-8"))
             if r.get("Family") == family and paths.get(r["Glottocode"])]
    if not code or not langs:
        return {}, Counter(), False
    # cobertura de cada nodo por las lenguas muestreadas de la familia
    cov = Counter()
    for r in langs:
        for gc in paths[r["Glottocode"]].split("/"):
            cov[gc] += 1
    T = len(langs)

    def branch_of(gc):
        parts = paths[gc].split("/")
        if code in parts:
            parts = parts[parts.index(code):]
        chosen = parts[0]
        for p in parts:                      # baja hasta el primer nodo suficientemente pequeño
            chosen = p
            if cov[p] <= maxfrac * T:
                break
        return chosen

    assign, counts = {}, Counter()
    for r in langs:
        b = names.get(branch_of(r["Glottocode"]), branch_of(r["Glottocode"]))
        assign[r["ID"]] = b
        counts[b] += 1
    return assign, counts, True


if __name__ == "__main__":
    fam = os.environ.get("TF_FAMILY", "Indo-European")
    assign, counts, ok = branch_map(fam)
    print(f"{fam}: {len(assign)} lenguas clasificadas → {len(counts)} ramas")
    for b, n in counts.most_common():
        print(f"  {n:4}  {b}")
