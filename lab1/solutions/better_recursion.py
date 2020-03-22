from copy import copy

from utils.dimacs import loadGraph


def remove_neighbors(G, neighbors):
    G_copy = copy(G)
    for v in neighbors:
        try:
            del G_copy[v]
        except KeyError:
            pass
    return G_copy


def _better_recursion_helper(G, k, solution):
    # if G is empty, then all needed vertices have been chosen
    if not G:
        return solution

    # if G is not empty, but k is 0, then we "used up" all k vertices,
    # therefore solution does not exist
    if k == 0:
        return None

    # G contains only vertices of degree 1 or higher, so we can pop any vertex
    v, v_neighbors = G.popitem()

    # take vertex v, remove all his neighbors
    G_without_v = copy(G)
    G_without_v = remove_neighbors(G_without_v, v_neighbors)

    solution_copy = copy(solution)
    solution_copy.add(v)

    possible_sol_1 = _better_recursion_helper\
        (G_without_v, k - 1, solution_copy)
    if possible_sol_1:
        return possible_sol_1

    # take neighbors of v (if possible, i. e. it's at most k of them), remove
    # all of their neighbors
    neighbors_count = len(v_neighbors)

    # check if taking neighbors is possible; if not, return no solution
    if neighbors_count > k:
        return None

    for neighbor in v_neighbors:
        G = remove_neighbors(G, neighbor)

    solution |= v_neighbors
    possible_sol_2 = _better_recursion_helper\
        (G, k - neighbors_count, solution)
    return possible_sol_2


def better_recursion(graph, k):
    """
    Upgraded version of recursive solution based on an observation that for
    any given vertex v we have to either add v to the solution, or all of his
    neighbors (otherwise we wouldn't cover v).
    Time complexity: O(1.618^k)
    :param graph: graph represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graph
    :return: set of vertices that create the cover if the solution exists,
    otherwise None
    """
    # convert graph to dictionary form:
    # vertex_index -> set_of_incident_vertices
    G = {vertex: graph[vertex] for vertex in range(1, len(graph))}

    solution = set()
    # add all "single" vertices to the solution - they have to be there
    for vertex, incident_vertices in G.items():
        if not incident_vertices:
            solution.add(vertex)
            k -= 1

    # remove selected "single" vertices from graph
    for vertex in solution:
        del G[vertex]

    return _better_recursion_helper(G, k, solution)


G = loadGraph("graphs/e5")
V = len(G)
for v in range(V):
    s = "{0}:".format(v)
    for u in G[v]:
        s += " {0}".format(u)
    print(s)

print()
print(better_recursion(G, 4))
