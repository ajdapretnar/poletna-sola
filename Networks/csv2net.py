import sys
import csv
import networkx as nx
import os

G = nx.DiGraph()

with open(sys.argv[1], newline='') as f:
    reader = csv.reader(f)
    next(reader)
    G.add_weighted_edges_from(reader)

nx.write_pajek(G, os.path.splitext(sys.argv[1])[0] + '.net')
