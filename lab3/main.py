import os
from typing import List, Set, Tuple

from pysat.solvers import Solver
from sat.satisfiability import calc_sat_probs_and_plot
from sat.vertex_cover import solve_vertex_cover
from utils.dimacs import *

# commented out the hardest graphs, since they take LONG time to calculate
graph_names = [
    "e5",
    "e10",
    "e20",
    "e40",
    # "e150",
    "s25",
    "s50",
    "s500",
    "b20",
    # "b30",
    # "b100",
    # "k330_a",
    # "k330_b",
    # "k330_c",
    # "k330_d",
    # "k330_e",
    # "k330_f",
    # "f30",
    # "f35",
    # "f40",
    # "f56",
    "m20",
    "m30",
    "m40",
    "m50",
    # "m100",
    "p20",
    "p35",
    "p60",
    # "p150",
    # "p200",
    "r30_01",
    "r30_05",
    "r50_001",
    "r50_01",
    # "r50_05",
    # "r100_005",
    # "r100_01",
    # "r200_001",
    # "r200_005"
]

if __name__ == "__main__":
    # calc_sat_probs_and_plot()

    graph_dir = "graphs"
    solution_dir = "solutions"
    for name in graph_names:
        graph_filename = os.path.join(graph_dir, name)
        solution_filename = os.path.join(solution_dir, f"{name}.sol")

        G: List[Set[int]] = loadGraph(graph_filename)
        G_edge_list: List[Tuple[int, int]] = edgeList(G)

        print(name)
        for k in range(1, len(G)):
            formula = solve_vertex_cover(G, k, return_solution=False)
            solver = Solver(name="glucose4")
            solver.append_formula(formula)
            solver.solve()
            solution = solver.get_model()
            if not solution or not isVC(G_edge_list, solution):
                continue

            print("solution k:", k)
            print("VC:", isVC(G_edge_list, solution), "\n")
            print()
            saveSolution(solution_filename, solution)
            break
