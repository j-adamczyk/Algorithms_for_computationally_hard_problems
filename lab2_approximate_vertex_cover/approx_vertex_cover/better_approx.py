from typing import Set

from approx_vertex_cover.types import EdgeList


def _remove_neighbors_of_vertices(G: EdgeList, u: int, v: int) -> EdgeList:
    G = [
        edge
        for edge in G
        if edge[0] != u and edge[1] != u and edge[0] != v and edge[1] != v
    ]
    return G


def better_approximation(graph: EdgeList, k: int) -> Set[int]:
    """
    Upgraded approximation algorithm for the Vertex Cover problem. It just
    takes any edge and adds it's ends to the solution (removing their
    neighbors), yielding surprisingly good 2-approximation.
    Approximation factor: 2
    :param graph: graphs represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graphs
    :return: set of vertices that approximate the cover; this may NOT be the
    vertex cover for given k
    """
    solution = set()

    while len(solution) < k - 1 and graph:
        u, v = graph.pop()
        graph = _remove_neighbors_of_vertices(graph, u, v)
        solution.add(u)
        solution.add(v)

    return solution
