from typing import Dict, Set

from approx_vertex_cover.types import EdgeList


def _get_vertices_degrees(G: EdgeList) -> Dict[int, int]:
    degrees = dict()
    for edge in G:
        u, v = edge
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1
    return degrees


def _get_highest_degree_vertex(G: EdgeList) -> int:
    degrees = _get_vertices_degrees(G)
    max_degree = -1
    best_vertex = -1
    for u, degree in degrees.items():
        if degree > max_degree:
            max_degree = degree
            best_vertex = u
    return best_vertex


def _remove_neighbors_of_vertex(G: EdgeList, u: int) -> EdgeList:
    G = [edge for edge in G if edge[0] != u and edge[1] != u]
    return G


def simple_approximation(graph: EdgeList, k: int) -> Set[int]:
    """
    Simple approximation algorithm for the Vertex Cover problem. It follows
    the intuitive approach that we can add the highest degree vertex to the
    solution, until we get k vertices. Each time we remove the edges of the
    selected vertex.
    Approximation factor: log(n) (for graph with n vertices)

    :param graph: graphs represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graphs
    :return: set of vertices that approximate the cover; this may NOT be the
    vertex cover for given k
    """
    solution = set()

    while len(solution) < k and graph:
        u = _get_highest_degree_vertex(graph)
        graph = _remove_neighbors_of_vertex(graph, u)
        solution.add(u)

    return solution
