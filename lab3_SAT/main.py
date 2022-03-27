import os

from sat import solve_x3c
from utils.dimacs import *

x3c_graphs_names = [
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

    # X3C -> SAT
    x3c_dir = "x3c"
    for name in x3c_graphs_names:
        x3c_filename = os.path.join(x3c_dir, name)
        n, sets = loadX3C(x3c_filename)

        satisfiable = True if name.split(".")[1] == "yes" else False

        print(name)
        result = solve_x3c(n, sets)
        print(f"result: {result}, truth: {satisfiable}")
        print()
