from typing import Dict, List, Tuple, Union


def _basic_dpll_recursion_helper():
    pass


def solve(formula: List[List[int]], values: Dict[int, int]) -> Union[List[int], str]:
    """
    if CNF jest spełniona przez V:
    return V

    v = zmienna występująca w CNF

    if solve( CNF-z-v-ustawionym-na-1, V-z-v-ustawionym-na-1 ):
    return V
    if solve( CNF-z-v-ustawionym-na-0, V-z-v-ustawionym-na-0 ):
    return V

    return "UNSAT"
    """


def basic_dpll_solve(formula: List[List[int]]) -> Tuple[bool, int]:
    """
    Basic DPLL (Davis, Putnam, Logemann, Loveland) solver implementation for
    checking SAT formulas satisfiability.

    :param formula: list of clauses in CNF form
    :returns: tuple: whether formula is satisfiable or not, and number of
    recurrent calls to the solver procedure
    """
