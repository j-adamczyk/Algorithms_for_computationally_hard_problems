from typing import Set

from approx_vertex_cover.types import EdgeList
from utils.dimacs import isVC


def two_approx(graph: EdgeList) -> Set[int]:
    """
    Approximation algorithm for the Vertex Cover problem, which just takes any
    edge and adds its ends to the solution (removing their neighbors), yielding
    surprisingly good 2-approximation.

    Approximation factor: 2

    :param graph: graphs represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graphs
    :return: set of vertices that approximate the cover; this may NOT be the
    vertex cover for given k
    """
    solution = set()
    original_graph = graph.copy()

    while not isVC(original_graph, solution):
        u, v = graph.pop()
        graph = [
            edge
            for edge in graph
            if u not in edge and v not in edge
        ]
        solution |= {u, v}

    return solution
