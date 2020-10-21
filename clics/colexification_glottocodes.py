# This needs:
#  - clics3-network.gml
#  - clics3.sqlite
#  - data-human-animal-plant.tsv

import igraph
import sqlite3
import csv
import pathlib

OUTFILE = "out.txt"

if pathlib.Path(OUTFILE).exists():
    pathlib.Path(OUTFILE).unlink()

conc_ids = set()
conc_targets = set()

with open("data-human-animal-plant.tsv") as csvf:
    reader = csv.DictReader(csvf, delimiter="\t")

    for row in reader:
        if row["CONCEPTICON_ID_a"]:
            conc_ids.add(row["CONCEPTICON_ID_a"])
        if row["CONCEPTICON_ID_COLEXI"]:
            conc_targets.add(row["CONCEPTICON_ID_COLEXI"])


concepticon_ids = list(conc_ids)
colexification_targets = list(conc_targets)

graph = igraph.read("network-3-families.gml")
clics_db_conn = sqlite3.connect("clics.sqlite")
clics_db_cursor = clics_db_conn.cursor()

# This holds mappings between Concepticon IDs and the internal
# graph IDs, e.g. {525: 484}, meaning that Concepticon ID 525 is
# internally represented as node with the ID 484.
mapping_sources = {}

# As above, just for the target nodes.
mapping_targets = {}

# Populate the mappings for source and targets.
for node in graph.vs:
    if node["ID"] in concepticon_ids:
        mapping_sources[int(node["ID"])] = int(node["id"])
    if node["ID"] in colexification_targets:
        mapping_targets[int(node["ID"])] = int(node["id"])

for edge in graph.es:
    with open(OUTFILE, "a") as f:
        if edge.source in mapping_sources.values() and edge.target in mapping_targets.values():
            print("Source: ", [k for k, v in mapping_sources.items() if v == edge.source], file=f)
            print("Target: ", [k for k, v in mapping_targets.items() if v == edge.target], file=f)

            # Lookup languages:
            languages = edge["languages"].split(";")  # Edge annotations are separated by ";"
            for language in languages:
                # remove dataset name from language
                lang = language.split("-", 1)[-1]

                print(
                    clics_db_cursor.execute(
                        "SELECT Glottocode FROM LanguageTable WHERE ID = '%s'" % lang
                    ).fetchone()[0],
                    file=f,
                )

            print(" ---------------------- ", file=f)
