from typing import List, Set

import pycosat


def solve_x3c(n: int, sets: List[Set[int]]) -> bool:
    """
    Solve Exact 3-set Cover (X3C) problem through reduction to a SAT problem
    and using a SAT solver.

    Denote:
    - N = {1, 2, ..., 3k}, n = |N|
    - *S = {S1, S2, ..., Sm}, where |Si| = 3 and m <= 3k

    Steps for reduction:
    1. For every element N_j create variable x_j for j in [1, n]
    2. For every variable add clause with sets containing this variable, e.g.:
       (Sa or Sb or Sc); there can be 1, 2 or 3 such sets (ensures that at
       least one set is chosen)
    3. For every variable add exclusivity clauses (makes sure that at most one
       set is chosen, e.g. (~Sa or ~Sb) and (~Sb or ~Sc) and (~Sa or ~Sc)

    :param n: number of variables, it has to be a multiple of 3
    :param sets: list of sets with variables, where each set has exactly 3
    elements and each variable is contained in at most 3 sets
    :return: whether k sets (n // 3) can be selected such that each element
    is contained in exactly one of those sets
    """
    formula = []

    # maps variable to sets in which this variable is used
    variable_to_sets = [[] for _ in range(n + 1)]
    for set_num, vars_set in enumerate(sets):
        set_num += 1  # numerate from 1, not from 0, due to pycosat requirements
        for var_num in vars_set:
            variable_to_sets[var_num].append(set_num)

    # inclusion clauses - at least one set
    inclusion_clauses = variable_to_sets[1:]
    formula.extend(inclusion_clauses)

    # exclusivity clauses - at most one set
    for sets in variable_to_sets[1:]:
        exclusivity_clauses = [[-s1, -s2] for s1 in sets for s2 in sets if s1 != s2]
        formula.extend(exclusivity_clauses)

    result = pycosat.solve(formula)
    return result != "UNSAT"
