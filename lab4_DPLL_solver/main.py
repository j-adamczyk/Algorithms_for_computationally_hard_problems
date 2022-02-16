import os

from dpll import basic_dpll_solve
from utils.dimacs import loadCNF

sat_formula_names = [
    "5.no.sat",
    "5.yes.sat",
    "10.no.sat",
    "10.yes.sat",
    "100.no.sat",
    "100.yes.sat",
    "20.no.sat",
    "20.yes.sat",
    "30.no.sat",
    "30.yes.sat",
    "35.no.sat",
    "35.yes.sat",
    "40.no.sat",
    "40.yes.sat",
    "50.no.sat",
    "50.yes.sat",
    "60.no.sat",
    "60.yes.sat",
    "70.no.sat",
    "70.yes.sat",
    "80.no.sat",
    "80.yes.sat",
    "90.no.sat",
    "90.yes.sat",
    "1-FullIns_3.3.sat",
    "1-FullIns_3.4.sat",
    "1-FullIns_4.4.sat",
    "1-FullIns_4.5.sat",
    "1-Insertions_4.4.sat",
    "1-Insertions_4.5.sat",
    "r30_01.dyn.14.sat",
    "r30_01.dyn.15.sat",
    "r30_01.fast.14.sat",
    "r30_01.fast.15.sat",
    "r30_01.ins.14.sat",
    "r30_01.ins.15.sat",
    "anna.11.sat",
    "anna.15.sat",
    "anna.5.sat",
    "homer.13.sat",
    "homer.14.sat",
]

if __name__ == "__main__":
    sat_formulas_dir = "sat_formulas"
    for name in sat_formula_names:
        sat_formula_filename = os.path.join(sat_formulas_dir, name)
        n, formula = loadCNF(sat_formula_filename)

        if name != "5.yes.sat":
            continue

        satisfiable = name.split(".")[1]
        if satisfiable == "no":
            satisfiable = False
        elif satisfiable == "yes":
            satisfiable = True
        else:
            satisfiable = "unknown"

        print(name)
        result, num_recurrent_calls = basic_dpll_solve(formula)
        print(f"Result: {result}, truth: {satisfiable}")
        print(f"Number of recurrent calls:", num_recurrent_calls)
        print()
        exit()
