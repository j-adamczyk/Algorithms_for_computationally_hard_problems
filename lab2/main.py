from os import getcwd
from os.path import join
from utils.dimacs import *

graph_names = [
    "e5",
    "e10",
    "e20",
    "e40",
    "e150",
    "s25",
    "s50",
    "s500",
    "b20",
    "b30",
    "b100",
    "k330_a",
    "k330_b",
    "k330_c",
    "m20",
    "m30",
    "m40",
    "m50",
    "m100",
    "p20",
    "p35",
    "p60",
    "p150",
    "r30_01",
    "r30_05",
    "r50_001",
    "r50_01",
    "r50_05",
    "r100_005"]

graph_dir = join(getcwd(), "graphs")
exact_solution_dir = join(getcwd(), "exact_solutions")
approx_solurion_dir = join(getcwd(), "approx_solutions")
for name in graph_names:
    graph_filename = join(graph_dir, name)
    exact_solution_filename = join(exact_solution_dir, name + ".sol")
    G = loadGraph(graph_filename)
    G_edge_list = edgeList(G)
    print(name)
    for k in range(1, len(G)):
        solution = optimized_recursion(G, k)
        if not solution:
            continue

        print("solution k:", k)
        print("VC:", isVC(G_edge_list, solution))
        print()
        saveSolution(solution_filename, solution)
        break
