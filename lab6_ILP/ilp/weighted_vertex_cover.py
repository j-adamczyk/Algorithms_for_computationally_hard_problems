from typing import Optional, Set, Tuple, Union

from pulp import *

from ilp.types import VertexSets


def weighted_vertex_cover_solver(
    graph: VertexSets, neighbors_weight: Union[int, float] = 0
) -> Optional[Tuple[Set[int], int]]:
    """
    Solve weighted vertex cover problem through reduction to an ILP problem
    and using an ILP solver.

    Denote:
    - V = {v_1, v_2, ..., v_n} (n = |V|)

    Steps for reduction:
    1. For every vertex v_i create variable x_i for i in [1, n]. It's binary,
       since either x_i is in the vertex cover or it it's not
    2. Assign weight to each vertex with degree > 0:
       w_i = degree(x_i) ^ neighbors_weight
       For neighbors weight 0 every vertex has weight 1 (regular vertex cover),
       for weight 1 weight is the number of neighbors
    3. Objective: minimize w_1 * x_1 + w_2 * x_2 + ... + w_n * x_n
    4. For every edge (v_i, v_j) at least one vertex has to be in the solution:
       x_i + x_j >= 1

    :param graph: graph as list of sets of neighbors
    :param neighbors_weight: weights of neighbors, default 0
    :return: solved vertex cover and minimal k found or None, if some problem
    occurred
    """
    model = LpProblem("vertex_cover", LpMinimize)

    # weighting scheme
    neighbors_weight = max(0, neighbors_weight)
    neighbors_weight = min(neighbors_weight, 1)
    weight = lambda neighbors_count: neighbors_count ** neighbors_weight

    # objective
    variables = {
        v: LpVariable(str(v), cat="Binary") * weight(len(neighbors))
        for v, neighbors in enumerate(graph)
        if neighbors
    }  # ignore degree 0 vertices

    model += sum(variables.values())

    # constraints
    for v, neighbors in enumerate(graph):
        for u in neighbors:
            if v < u:
                model += variables[u] + variables[v] >= 1

    model.solve()
    if LpStatus[model.status] == "Optimal":
        result = set()
        for var in model.variables():
            if var.varValue:  # value is 0 or 1
                # we only care about vertices numbers
                result.add(int(var.name))
        return result, len(result), round(value(model.objective), 2)
    else:
        return None
