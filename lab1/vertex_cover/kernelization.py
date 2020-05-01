from utils.dimacs import edgeList


# DOES NOT WORK YET - needs a bit of debugging


def _get_neighbor_of_vertex(G, u):
    for edge in G:
        # return the neighbor after finding the edge with u
        if edge[0] == u:
            return edge[1]
        elif edge[1] == u:
            return edge[0]


def _get_neighbors_of_vertex(G, u):
    neighbors = set()
    for edge in G:
        if edge[0] == u:
            neighbors.add(edge[1])
        elif edge[1] == u:
            neighbors.add(edge[0])
    return neighbors


def _remove_neighbors_of_vertex(G, u):
    G = [edge for edge in G if edge[0] != u and edge[1] != u]
    return G


def _get_vertices_degrees(G):
    degrees = dict()
    for edge in G:
        u, v = edge
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1
    return degrees


def _kernelize_helper(G, k, solution, prev_solution_size):
    print(G)
    # for too small k we may get negative value, then we know that such
    # kernelization is not possible
    if k < 0:
        return None

    # degree 0 vertices "handle themselves", since we use edge list for graph

    degrees = _get_vertices_degrees(G)
    G, k = _handle_degree_1_vertices(G, k, solution, degrees)
    if k < 0:
        return None

    degrees = _get_vertices_degrees(G)
    G, k = _handle_degree_above_k_vertices(G, k, solution, degrees)
    if k < 0:
        return None

    if prev_solution_size == len(solution) or k == 0:
        return G, k, solution
    else:
        return _kernelize_helper(G, k, solution, len(solution))


def kernelize(graph, k):
    """
    Calculates the graphs kernel suitable for the Vertex Cover problem.
    It's based on the following observations:
    1. Every vertex of degree 0 has to be in the solution
    2. For every vertex of degree 1, it's only neighbor has to be in the
       solution
    3. Every vertex of degree larger than current k has to be in the solution
    4. If the graphs kernel contains more than k^2 edges, it cannot have a
       Vertex Cover of size k
    Time complexity: O(n)
    :param graph: graphs represented as a list of sets (incident vertices) or
    as a dict of sets (vertex -> incident vertices)
    :param k: this many vertices have to cover the graphs
    :return: graphs kernel (subgraph equal in terms of Vertex Cover solution
    existence) if the solution may exist or None if it does not exist
    """
    solution = set()

    while True:
        changed = False
        degrees = _get_vertices_degrees(graph)
        for v in degrees:
            if degrees[v] == 1:
                u = _get_neighbor_of_vertex(graph, v)
                solution.add(u)
                k -= 1
                graph = _remove_neighbors_of_vertex(graph, u)
                changed = True
                break
            elif degrees[v] > k:
                solution.add(v)
                k -= 1
                graph = _remove_neighbors_of_vertex(graph, v)
                changed = True
                break

        if not changed:
            break

    # check if solution can exist
    if len(graph) > k * k:
        return None
    else:
        return graph, k, solution
