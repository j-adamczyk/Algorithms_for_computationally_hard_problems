from typing import Optional, Set, Tuple

from pulp import *

from ilp.types import VertexSets


def approx_vertex_cover_solver(graph: VertexSets) -> Optional[Tuple[Set[int], int]]:
    """
    Solve approximate vertex cover problem through reduction to an ILP
    problem and using an ILP solver.

    Denote:
    - V = {v_1, v_2, ..., v_n} (n = |V|)

    Steps for reduction:
    1. For every vertex v_i create continuous variable x_i for i in [1, n]
    2. Objective: minimize x_1 + x_2 + ... + x_n
    3. For every edge (v_i, v_j) at least one vertex has to be in the solution:
       x_i + x_j >= 1
    4. Take those vertices to the solution that have value at least 0.5

    :param graph: graph as list of sets of neighbors
    :return: solved approximate vertex cover and minimal k found or None,
    if some problem occurred
    """
    model = LpProblem("vertex_cover", LpMinimize)

    # objective
    variables = {
        v: LpVariable(str(v), lowBound=0, upBound=1, cat="Continuous")
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
            if var.varValue >= 0.5:
                # we only care about vertices numbers
                result.add(int(var.name))
        return result, len(result)
    else:
        print(LpStatus[model.status])
        return None
