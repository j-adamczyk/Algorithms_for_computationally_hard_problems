from itertools import combinations


def brute_force(graph, k):
    """
    Brute force solution for the Vertex Cover problem. Checks all possible
    subsets of k vertices and checks if they create a solution (cover all
    n vertices of the graphs).
    Time complexity: O(n^k)
    :param graph: graphs represented as a list of sets (incident vertices)
    :param k: this many vertices have to cover the graphs
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
