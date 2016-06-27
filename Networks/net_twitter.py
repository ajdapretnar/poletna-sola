import Orange
import re
import networkx as nx
import os
import itertools as it
import csv

G = nx.read_pajek(os.path.join("data", "stormofswords.net"))
G_nodes = G.nodes(data=1)
G_nodes_dict = dict(G_nodes)


# TODO: include in Orange Python script module.
meta = Orange.data.Table(os.path.join("data", "stormofswords.data.csv"))
datapath = os.path.join("data", "twitter_got_2016-06-20_2016-06-27_dump.tab")
data = Orange.data.Table(datapath)

nodes = dict()
edges = dict()

for row in data:
    text = str(row["text"])
    mentions = dict()
    for name in G_nodes_dict:
        # TODO: respect overlapping names like Jon Snow and the other Jon
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

# Construct a graph and write a data file
graphpath = os.path.splitext(datapath)[0] + '.net'
metapath  = os.path.splitext(datapath)[0] + '.data.csv'

header = ["label 0", "degree", "popularity", "id"]
writer = csv.DictWriter(open(metapath, "w"), fieldnames=header)
writer.writeheader()

H = nx.Graph()
for name in sorted(nodes, key=lambda nm: int(G_nodes_dict[nm]["id"])):
    degree = len([e for e in edges.keys() if name in e])
    popularity = nodes.get(name, 0)
    idn = int(G_nodes_dict[name]["id"])
    H.add_node(idn)
    wrow = {
        "id":         idn,
        "degree":     degree,
        "label 0":    name,
        "popularity": popularity,
    }
    writer.writerow(wrow)

for (node1, node2), w in edges.items():
    idn1 = int(G_nodes_dict[node1]["id"])
    idn2 = int(G_nodes_dict[node2]["id"])
    H.add_edge(idn1, idn2, weight=w)


# Write a network file
nx.write_pajek(H, graphpath)






