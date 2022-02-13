from copy import copy, deepcopy
from typing import Dict, List, Optional, Set, Tuple

from vertex_cover.types import EdgeList


def _check_solution(G: EdgeList, k: int) -> str:
    # safety measure for cases when we remove too many neighbors
    if k < 0:
        return "None"

    # if G is empty, then all needed vertices have been chosen
    if not G:
        return "solution"

    # if G is not empty, but k is 0, then we "used up" all k vertices,
    # therefore solution does not exist
    if k == 0:
        return "None"

    # if none of the above happen, we should not yet finish
    return "continue"


def _get_neighbor_of_vertex(G: EdgeList, u: int) -> int:
    for edge in G:
        # return the neighbor after finding the edge with u
        if edge[0] == u:
            return edge[1]
        elif edge[1] == u:
            return edge[0]


def _get_neighbors_of_vertex(G: Set[Tuple[int, int]], u: int) -> Set[int]:
    neighbors = set()
    for edge in G:
        if edge[0] == u:
            neighbors.add(edge[1])
        elif edge[1] == u:
            neighbors.add(edge[0])
    return neighbors


def _remove_neighbors_of_vertex(G: EdgeList, u: int) -> EdgeList:
    G = [edge for edge in G if edge[0] != u and edge[1] != u]
    return G


def _get_vertices_degrees(G: List[Tuple[int, int]]) -> Dict[int, int]:
    degrees = dict()
    for edge in G:
        u, v = edge
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1
    return degrees


def _remove_degree_1_vertices(
    G: EdgeList, k: int, solution: Set[int], degrees: Dict[int, int]
) -> Tuple[EdgeList, int]:
    # while graph contains at least one vertex with degree 1, remove them (add
    # their only neighbor to the solution, remove his edges)
    # it may create new vertices, hence the loop
    while True:
        set_of_degrees = set(degrees.values())
        if 1 not in set_of_degrees:  # no more vertices of degree 1
            break

        for u, degree in degrees.items():
            if degree == 1:
                v = _get_neighbor_of_vertex(G, u)
                if not v:  # may happen if we removed all neighbors already
                    continue
                solution.add(v)
                k -= 1
                G = _remove_neighbors_of_vertex(G, v)
        degrees = _get_vertices_degrees(G)
    return G, k


def _get_highest_degree_vertex(degrees: Dict[int, int]) -> int:
    max_degree = -1
    best_vertex = -1
    for u, degree in degrees.items():
        if degree > max_degree:
            max_degree = degree
            best_vertex = u
    return best_vertex


def _optimized_recursion_helper(
    G: EdgeList, k: int, solution: Set[int]
) -> Optional[Set[int]]:
    # check is we can finish with this solution
    check = _check_solution(G, k)
    if check == "None":
        return None
    elif check == "solution":
        return solution
    # else - continue

    # calculate degrees of vertices, remove degree 1 vertices
    degrees = _get_vertices_degrees(G)
    G, k = _remove_degree_1_vertices(G, k, solution, degrees)

    # check if the solution can still exist
    check = _check_solution(G, k)
    if check == "None":
        return None
    elif check == "solution":
        return solution
    # else - continue

    # take vertex of the highest degree as u
    u = _get_highest_degree_vertex(degrees)
    G_copy = deepcopy(G)
    G_copy = _remove_neighbors_of_vertex(G_copy, u)
    solution_copy = copy(solution)
    solution_copy.add(u)
    k_copy = k - 1

    possible_sol_1 = _optimized_recursion_helper(G_copy, k_copy, solution_copy)
    if possible_sol_1:
        return possible_sol_1

    # take neighbors of u, remove all of their neighbors
    G = set(G)
    neighbors = _get_neighbors_of_vertex(G, u)
    neighbors_edges = {
        edge for edge in G if edge[0] in neighbors or edge[1] in neighbors
    }
    G -= neighbors_edges
    G = list(G)

    solution |= neighbors
    possible_sol_2 = _optimized_recursion_helper(G, k - len(neighbors), solution)
    return possible_sol_2


def optimized_recursion(graph: EdgeList, k: int, solution: Optional[Set[int]] = None):
    """
    Even more upgraded version of recursive solution. It's very similar to the
    upgraded version (better_recursion), but makes use of the following
    observations:
    1. If there is any vertex of degree 1, it does not need to be chosen as v.
       Instead, it's only neighbor can be instantaneously added to the
       solution. Then we remove this neighbor's neighbors (including the
       vertex v).
    2. The v can be chosen in a smart way - the bigger the degree, the better,
       since then we get remove neighbors at once. Therefore, the v with the
       largest degree should be removed first.
    3. If we have only vertices of degree 2, they create a cycle and a single
       usage of observation 2. will "cut" the cycle, allowing us to use the
       observation 1 for the rest of the vertices.
    Time complexity: O(1.47^k)

    :param graph: graphs represented as a list of edges
    :param k: this many vertices have to cover the graph
    :param solution: if a graph kernel was precomputed for the "graph"
    parameter, pass the partial solution as this argument
    :return: set of vertices that create the cover if the solution exists,
    otherwise None
    """
    if not solution:
        solution = set()

    return _optimized_recursion_helper(graph, k, solution)
