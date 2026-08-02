#!/usr/bin/env python3
"""Doculect manifest (Appendix A): the exact doculects used, with provenance, so source/transcription confounds
can be audited. Replicates compute_network's top-MAXLANG selection. Uso: LEX_PATH=... FAMILY=... make manifest"""
import os, csv
from collections import defaultdict
from branches import branch_map
from compute_network import LEX, FAMILY, MAXLANG

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "data", "results")
SLUG = {"Indo-European": "ie", "Austronesian": "an"}.get(FAMILY, FAMILY.split("-")[0].lower())


def main():
    assign, _, _ = branch_map(FAMILY)
    meta = {}
    for r in csv.DictReader(open(f"{LEX}/languages.csv", encoding="utf-8")):
        meta[r["ID"]] = r
    per = defaultdict(int)
    for row in csv.DictReader(open(f"{LEX}/forms.csv", encoding="utf-8")):
        m = meta.get(row["Language_ID"])
        if m and m.get("Family") == FAMILY and assign.get(row["Language_ID"]) and len((row.get("Segments") or "").split()) >= 2:
            per[row["Language_ID"]] += 1
    langs = sorted(per, key=lambda l: -per[l])[:MAXLANG]
    out = os.path.join(RES, f"doculect_manifest_{SLUG}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "doculect_id", "glottocode", "branch", "n_concepts", "dataset"])
        for l in langs:
            m = meta[l]
            dataset = l.split("-")[0] if "-" in l else (m.get("Dataset") or "")
            w.writerow([m.get("Name") or l, l, m.get("Glottocode", ""), assign.get(l, ""), per[l], dataset])
    print(f"wrote {out} ({len(langs)} doculects)")


if __name__ == "__main__":
    main()
