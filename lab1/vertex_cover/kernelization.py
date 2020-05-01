def kernelize(graph, k):
    """
    Calculates the graphs kernel suitable for the Vertex Cover problem.
    It's based on the following observations:
    1. Every vertex of degree 0 can't be in a solution
    2. For every vertex of degree 1, it's only neighbor has to be in the
       solution
    3. Every vertex of degree larger than current k has to be in the solution
    4. If the graphs kernel contains more than k^2 edges, it cannot have a
       Vertex Cover of size k
    Time complexity: O(n)
    :param graph: graphs represented as a list of edges
    :param k: this many vertices have to cover the graph
    :return: graphs kernel (subgraph equal in terms of Vertex Cover solution
    existence) if the solution may exist or None if it does not exist
    """
    solution = set()

    # convert graph to dict of sets of neighbors representation
    G = dict()
    for u, v in graph:
        if u in G:
            G[u].add(v)
        else:
            G[u] = {v}
        if v in G:
            G[v].add(u)
        else:
            G[v] = {u}

    while True:
        to_remove = None
        for v, neighbors in G.items():
            if len(neighbors) == 1:
                u = list(neighbors)[0]
                solution.add(u)
                to_remove = [u, v]
                k -= 1
                break
            elif len(neighbors) > k:
                to_remove = [v]
                solution.add(v)
                k -= 1
                break

        if to_remove:
            for v in to_remove:
                try:
                    neighbors = G[v]
                except KeyError:
                    continue

                try:
                    del G[v]
                except:
                    pass

                for u in neighbors:
                    try:
                        G[u].remove(v)
                        if not G[u]:
                            del G[u]
                    except KeyError:
                        pass
        else:
            break

    graph = set()
    for v, neighbors in G.items():
        for u in neighbors:
            graph.add((u, v)) if u < v else graph.add((v, u))

    # check if solution can exist
    if len(graph) > k * k:
        return None
    else:
        return graph, k, solution
