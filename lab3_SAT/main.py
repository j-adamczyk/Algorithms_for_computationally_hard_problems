import os

from sat import solve_x3c
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


x3c_names = [
    "10.no.x3c",
    "10.yes.x3c",
    "50.no.x3c",
    "50.yes.x3c",
    "100.no.x3c",
    "200.no.x3c",
    "200.yes.x3c",
    "350.no.x3c",
    "350.yes.x3c",
    "500.no.x3c",
    "500.yes.x3c",
    "600.no.x3c",
    "600.yes.x3c",
]


if __name__ == "__main__":
    # calc_sat_probs_and_plot()

    # Vertex Cover -> SAT
    """
    graph_dir = "graphs"
    solution_dir = "graphs_solutions"
    for name in graph_names:
        graph_filename = os.path.join(graph_dir, name)
        solution_filename = os.path.join(solution_dir, f"{name}.sol")

        G: List[Set[int]] = loadGraph(graph_filename)
        G_edge_list: List[Tuple[int, int]] = edgeList(G)

        print(name)
        for k in range(1, len(G)):
            solution = solve_vertex_cover(G, k)
            if not solution or not isVC(G_edge_list, solution):
                continue

            print("solution k:", k)
            print("VC:", isVC(G_edge_list, solution), "\n")
            print()
            saveSolution(solution_filename, solution)
            break
            """

    # X3C -> SAT
    x3c_dir = "x3c"
    for name in x3c_names:
        x3c_filename = os.path.join(x3c_dir, name)
        n, sets = loadX3C(x3c_filename)

        satisfiable = True if name.split(".")[1] == "yes" else False

        print(name)
        result = solve_x3c(n, sets)
        print(f"result: {result}, truth: {satisfiable}")
        print()
