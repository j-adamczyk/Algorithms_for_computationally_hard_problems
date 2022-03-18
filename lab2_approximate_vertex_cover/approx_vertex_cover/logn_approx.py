from typing import Dict, Set

from approx_vertex_cover.types import EdgeList
from utils.dimacs import isVC


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


def logn_approx(graph: EdgeList) -> Set[int]:
    """
    Approximation algorithm for the Vertex Cover problem, which follows
    the intuitive approach that we can add the highest degree vertex to the
    solution, until we get the solution. Each time we remove the edges of the
    selected vertex.

    Approximation factor: log(n) (for graph with n vertices)

    :param graph: graphs represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graphs
    :return: set of vertices that approximate the cover; this may NOT be the
    vertex cover for given k
    """
    solution = set()
    original_graph = graph.copy()

    while not isVC(original_graph, solution):
        u = _get_highest_degree_vertex(graph)
        graph = [edge for edge in graph if u not in edge]
        solution.add(u)

    return solution
