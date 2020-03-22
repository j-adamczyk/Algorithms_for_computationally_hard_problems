from copy import copy
from itertools import combinations
from utils.dimacs import *

G = loadGraph("graphs/e5")
V = len(G)
for v in range(V):
    s = "{0}:".format(v)
    for u in G[v]:
        s += " {0}".format(u)
    print(s)


def brute_force(graph, k):
    """
    Brute force solution for the Vertex Cover problem. Checks all possible
    subsets of k vertices and checks if they create a solution (cover all
    n vertices of the graph).
    Time complexity: O(n^k)
    :param graph: graph represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graph
    :return: set of vertices that create the cover if the solution exists,
    otherwise None
    """
    V = len(graph) - 1  # -1 for the 0-th "vertex"
    for solution in combinations(range(1, len(graph)), k):
        cover = set(solution)
        for vertex in solution:
            incident_vertices = graph[vertex]
            cover |= incident_vertices
            if len(cover) == V:
                return solution
    return None


def _simple_rec_helper(G, k, solution):
    # if G is empty, then all needed vertices have been chosen
    if not G:
        return solution

    # if G is not empty, but k is 0, then we "used up" all k vertices,
    # therefore solution does not exist
    if k == 0:
        return None

    edge = G.pop()
    u, v = edge
    # take first vertex from edge, remove all edges incident with that vertex
    G_without_u = [(a, b) for (a, b) in G
                   if not (a == u or b == u)]
    solution_copy = copy(solution)
    solution_copy.add(u)
    possible_sol_1 = _simple_rec_helper(G_without_u, k - 1, solution_copy)
    if possible_sol_1:
        return possible_sol_1

    # take second vertex from edge, remove all edges incident with that vertex
    G_without_v = [(a, b) for (a, b) in G
                   if not (a == v or b == v)]
    solution.add(v)
    possible_sol_2 = _simple_rec_helper(G_without_v, k - 1, solution)
    return possible_sol_2


def simple_recursion(graph, k):
    """
    Simple recursive solution of the VC problem. It's based on the observation
    that for every edge e={u,v} at least one vertex (u or v) has to be chosen.
    Time complexity: O(2^k)
    :param graph: graph represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graph
    :return: set of vertices that create the cover if the solution exists,
    otherwise None
    """
    solution = set()
    # add all "single" vertices to the solution - they have to be there
    # and the edge representation used below would not "see" them
    # start iteration from 1 because of "nonexistent" 0-th vertex
    for vertex in range(1, len(graph)):
        if not graph[vertex]:  # vertex does not have any incident edges
            solution.add(vertex)
            k -= 1

    graph = edgeList(graph)  # convert graph to list of edges representation
    return _simple_rec_helper(graph, k, solution)
