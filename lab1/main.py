from utils.dimacs import *

G = loadGraph("graphs/e5")
V = len(G)
for v in range(V):
    s = "{0}:".format(v)
    for u in G[v]:
        s += " {0}".format(u)
    print(s)
