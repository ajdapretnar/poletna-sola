import Orange
import re
import networkx as nx
import os
import itertools as it
import csv
import sys
import unicodedata
import numpy as np

try:
    datapath = os.path.join("data", sys.argv[1])
    metapath = os.path.join("data", sys.argv[2])
    colname  = sys.argv[3]
    assert os.path.exists(datapath)
    assert os.path.exists(metapath)
except:
    print("Pretvorba Twitter podatkov v omrežje. Za dano datoteko .tab s Twitter " +
          "podatki in tabelo imen, poišče vse tvite kjer se pojavljajo pari imen in na tej podlagi zgradi omrežje.")
    print()
    print("Uporaba: ")
    print("\t %s <Twitter podatki> <Tabela z imeni> <Ime stolpca>" % sys.argv[0])
    print()
    print("Primer: ")
    print("\t %s twitter_got_dump.tab got.csv name" % sys.argv[0])
    print()
    quit(1)

normalize = lambda s: unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode("utf-8")

# Important! The ordering of nodes in the graph must be the same as in the
# metafile
meta        = Orange.data.Table(metapath)
data        = Orange.data.Table(datapath)
readerhead  = list(map(str, meta.domain.variables)) + list(map(str, meta.domain.metas))
names       = [normalize(str(row[colname])) for row in meta]
print()
print("Prvih 10 iskalnih nizov:")
print("\t %s" % ", ".join(names[:10]))

# Mine tweets for names
# Data format is retained from the structure stored by the Twitter module
nodes = dict()
edges = dict()
print("Iskanje nizov v podatkih Twitter ...")
for ri, row in enumerate(data):
    if ri % 10 == 0:
        sys.stdout.write("%d/%d\r" % (ri, len(data)))
        sys.stdout.flush()
    text = normalize(str(row["text"]))


    mentions = dict()
    for name in names:
        if " " in name:
            pat = name.replace(" ", "[ ]+")
        else:
            pat = "%s" % name

        m = re.search(pat, text, re.IGNORECASE)
        if m:
            mentions[name] = mentions.get(name, 0) + 1
    if len(mentions):
        for ky in mentions:
            nodes[ky] = nodes.get(ky, 0) + 1
        for ky1, ky2 in it.combinations(sorted(mentions.keys()), 2):
            edges[ky1, ky2] = edges.get((ky1, ky2), 0) + 1
print()

columns = list(meta.domain.variables) \
          + [Orange.data.ContinuousVariable("degree"),
             Orange.data.ContinuousVariable("popularity"),]
domain    = Orange.data.Domain(columns, metas=meta.domain.metas)
metatable = Orange.data.Table.from_domain(domain=domain)

print(nodes)

H = nx.Graph()
print(nodes, name)
for idn, row in enumerate(meta):
    name   = str(row[colname])
    degree = len([e for e in edges.keys() if name in e])
    popularity = nodes.get(name, 0)
    H.add_node(idn)

    # # Input data is store in order defined be metafile
    newrow = Orange.data.Instance(domain=domain)
    for ky in readerhead:
        newrow[ky] = row[ky]
    newrow["popularity"] = popularity
    newrow["degree"] = degree
    metatable.append(newrow)

D = np.zeros((len(names), len(names)))
for (node1, node2), w in edges.items():
    idn1 = names.index(node1)
    idn2 = names.index(node2)
    H.add_edge(idn1, idn2, weight=w)
    D[idn1, idn2] = D[idn2, idn1] = w

# Write a network file
# Construct a graph and write a data file
recompath = os.path.splitext(metapath)[0] + '.processed.txt'
graphpath = os.path.splitext(metapath)[0] + '.processed.net'
metapath  = os.path.splitext(metapath)[0] + '.processed.tab'
nx.write_pajek(H, graphpath)
metatable.save(metapath)
header = ",".join(names)
np.savetxt(recompath, D, delimiter=",", comments="", header=header, fmt="%d")

# Print to output
print("Narejene datoteke:")
for fname in [recompath, graphpath, metapath]:
    print("\t%s" % fname)
