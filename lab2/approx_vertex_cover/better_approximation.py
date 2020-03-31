from utils.dimacs import edgeList


def _remove_neighbors_of_vertices(G, u, v):
    G = [edge
         for edge in G
         if edge[0] != u and edge[1] != u
         and edge[0] != v and edge[1] != v]
    return G


def better_approximation(graph, k):
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
    # convert graphs to edge list representation
    G = edgeList(graph)

    solution = set()

    while len(solution) < k - 1 and G:
        u, v = G.pop()
        G = _remove_neighbors_of_vertices(G, u, v)
        solution.add(u)
        solution.add(v)

    return solution
