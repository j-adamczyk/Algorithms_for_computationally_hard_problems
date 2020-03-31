from utils.dimacs import edgeList


def _get_vertices_degrees(G):
    degrees = dict()
    for edge in G:
        u, v = edge
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1
    return degrees


def _get_highest_degree_vertex(G):
    degrees = _get_vertices_degrees(G)
    max_degree = -1
    best_vertex = -1
    for u, degree in degrees.items():
        if degree > max_degree:
            max_degree = degree
            best_vertex = u
    return best_vertex


def _remove_neighbors_of_vertex(G, u):
    G = [edge for edge in G if edge[0] != u and edge[1] != u]
    return G


def simple_approximation(graph, k):
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
    # convert graphs to edge list representation
    G = edgeList(graph)

    solution = set()

    while len(solution) < k and G:
        u = _get_highest_degree_vertex(G)
        G = _remove_neighbors_of_vertex(G, u)
        solution.add(u)

    return solution
