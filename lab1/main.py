from solutions.better_recursion import better_recursion
from solutions.brute_force import brute_force
from solutions.simple_recursion import simple_recursion
from utils.dimacs import *

G = loadGraph("graphs/e5")
V = len(G)
for v in range(V):
    s = "{0}:".format(v)
    for u in G[v]:
        s += " {0}".format(u)
    print(s)

sol = better_recursion(G, 4)
print(isVC(edgeList(G), sol))
