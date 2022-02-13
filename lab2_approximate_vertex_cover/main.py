import os

from approx_vertex_cover import better_approximation, simple_approximation
from approx_vertex_cover.types import EdgeList, VertexSets
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
    "k330_d",
    "k330_e",
    "k330_f",
    "f30",
    "f35",
    "f40",
    "f56",
    "m20",
    "m30",
    "m40",
    "m50",
    "m100",
    "p20",
    "p35",
    "p60",
    "p150",
    "p200",
    "r30_01",
    "r30_05",
    "r50_001",
    "r50_01",
    "r50_05",
    "r100_005",
    "r100_01",
    "r200_001",
    "r200_005",
]

if __name__ == "__main__":
    graph_dir = "graphs"
    solution_dir = "solutions"
    for name in graph_names:
        graph_filename = os.path.join(graph_dir, name)
        solution_filename = os.path.join(solution_dir, f"{name}.sol")

        G: VertexSets = loadGraph(graph_filename)
        G_edge_list: EdgeList = edgeList(G)

        print(name)
        for k in range(1, len(G)):
            solution = better_approximation(G_edge_list, k)
            if not solution or not isVC(G_edge_list, solution):
                continue

            print("solution k:", k)
            print("VC:", isVC(G_edge_list, solution))
            print()
            saveSolution(solution_filename, solution)
            break
