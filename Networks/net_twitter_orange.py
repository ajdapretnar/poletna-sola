colname = "name"        # Change this to have an effect on network generation


import Orange
import re
import networkx as nx
import os
import itertools as it
import csv
import sys
import unicodedata
import orangecontrib

normalize = lambda s: unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode("utf-8")

# Important! The ordering of nodes in the graph must be the same as in the
# metafile
meta        = in_data
data        = in_object
readerhead  = list(map(str, meta.domain.variables)) + list(map(str, meta.domain.metas))
names       = [normalize(str(row[colname])) for row in meta]
print(names)

# Mine tweets for names
# Data format is retained from the structure stored by the Twitter module
nodes = dict()
edges = dict()
print("Processing tweets")
for row in data:
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

columns = list(meta.domain.variables) \
          + [Orange.data.ContinuousVariable("degree"),
             Orange.data.ContinuousVariable("popularity"),]
domain    = Orange.data.Domain(columns, metas=meta.domain.metas)
metatable = Orange.data.Table.from_domain(domain=domain)

print("nodes", nodes)
print("edges", edges)

H = nx.Graph()
for idn, row in enumerate(meta):
    name   = row[colname]
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

for (node1, node2), w in edges.items():
    idn1 = names.index(node1)
    idn2 = names.index(node2)
    H.add_edge(idn1, idn2, weight=w)

# Write a network file
out_object = orangecontrib.network.Graph(H)
out_data = metatable
