from copy import copy
from utils.dimacs import edgeList


def _better_recursion_helper(G, k, solution):
    # safety measure for cases when we remove too many neighbors
    if k < 0:
        return None

    # if G is empty, then all needed vertices have been chosen
    if not G:
        return solution

    # if G is not empty, but k is 0, then we "used up" all k vertices,
    # therefore solution does not exist
    if k == 0:
        return None

    # G contains only edges, so degrees of degree 1 or higher, so we can
    # pop any edge
    u, v = G.pop()

    # take vertex u, remove all his neighbors
    G_copy = [edge for edge in G if edge[0] != u and edge[1] != u]
    solution_copy = copy(solution)
    solution_copy.add(u)

    possible_sol_1 = _better_recursion_helper(G_copy, k - 1, solution_copy)
    if possible_sol_1:
        return possible_sol_1

    # take neighbors of u, remove all of their neighbors
    G = set(G)
    neighbors = {edge[1] if edge[0] == u
                 else edge[0]
                 for edge in G
                 if edge[1] == u}
    neighbors.add(v)
    neighbors_edges = {edge for edge in G
                       if edge[0] in neighbors or edge[1] in neighbors}
    G -= neighbors_edges
    G = list(G)

    solution |= neighbors
    possible_sol_2 = _better_recursion_helper(G, k - len(neighbors), solution)
    return possible_sol_2


def better_recursion(graph, k, solution=None):
    """
    Upgraded version of recursive solution based on an observation that for
    any given vertex v we have to either add v to the solution, or all of his
    neighbors (otherwise we wouldn't cover v).
    Time complexity: O(1.618^k)
    :param graph: graph represented as an edge list
    :param k: this many vertices have to cover the graphs
    :param solution: if a graph kernel was precomputed for the "graph"
    parameter, pass the partial solution as this argument
    :return: set of vertices that create the cover if the solution exists,
    otherwise None
    """
    if not solution:
        solution = set()

    return _better_recursion_helper(graph, k, solution)
