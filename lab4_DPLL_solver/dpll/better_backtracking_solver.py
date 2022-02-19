from typing import Dict, List, Optional, Tuple, Union


_recurrence_counter = 0


def _simplify_clause(clause: List[int], values: Dict[int, int]) -> Optional[List[int]]:
    """
    Simplifies a single SAT formula clause (an alternative of variables), i.e.
    removes False variables and returns satisfied formula if any variable is True.

    For clauses we assume that:
    - None clause is satisfied (since it's a lack of clause)
    - [] clause is not satisfied (since it's an empty alternative, similar to
      sum of zeroes being zero)

    :param clause: clause, list of integers representing variables
    :param values: values of variables
    :return: one of:
    - None if clause is satisfied
    - simplified clause otherwise
    """
    simplified_clause = []
    for variable in clause:
        if variable not in values:
            # if variable does not have value yet, add it to the simplified clause
            simplified_clause.append(variable)
        elif values[variable] == 1:
            # if variable is True (1), formula is satisfied
            return None
        else:
            # if variable is False (0), skip it
            continue

    return simplified_clause


def _simplify_formula(
    formula: List[List[int]], values: Dict[int, int]
) -> Optional[List[List[int]]]:
    """
    Simplifies a SAT formula, i.e. simplifies each clause in the formula.

    For formulas we assume that:
    - None formula is not satisfied
    - [] formula is satisfied (since it's an empty conjunction, similar to
      product of ones being one)

    :param formula: list of clauses in CNF form
    :param values: values of variables
    :return: simplified formula
    """
    simplified_formula = []
    for clause in formula:
        simplified_clause = _simplify_clause(clause, values)
        if simplified_clause == []:
            # empty clauses are not satisfied, therefore formula cannot be satisfied
            return None
        elif simplified_clause is not None:
            # add simplified clause to the formula
            simplified_formula.append(simplified_clause)
        else:
            # None clauses are satisfied and therefore removed
            continue

    return simplified_formula


def _solve(
    formula: List[List[int]], values: Dict[int, int]
) -> Union[Dict[int, int], str]:
    """
    Helper function for DPLL solver.

    For clauses we assume that:
    - None clause is satisfied (since it's a lack of clause)
    - [] clause is not satisfied (since it's an empty alternative, similar to
      sum of zeroes being zero)

    For formulas we assume that:
    - None formula is not satisfied
    - [] formula is satisfied (since it's an empty conjunction, similar to
      product of ones being one)

    :param formula: list of clauses in CNF form
    :param values: dictionary of values of clause variables, mapping variable
    number (starting from 1) to either -1 (False) or 1 (True)
    :return: values
    """
    global _recurrence_counter
    _recurrence_counter += 1
    formula = _simplify_formula(formula, values)
    if formula == []:
        # empty formulas are satisfied
        return values
    elif formula is None:
        # None formulas are unsatisfiable
        return "UNSAT"

    # evaluate formulas from the shortest to the longest
    formula.sort(key=len)

    # try to satisfy the first, shortest formula
    for variable in formula[0]:
        values[variable] = 1
        values[-variable] = -1
        values_copy = values.copy()
        result = _solve(formula, values_copy)
        if result != "UNSAT":
            return result

        # if the previous value didn't work, the negative must (or the formula
        # is unsatisfiable)
        values[variable] = -1
        values[-variable] = 1

    # if all values didn't work, we try to take negatives and go forward
    values_copy = values.copy()
    return _solve(formula, values_copy)


def better_backtracking_dpll_solve(
    formula: List[List[int]],
) -> Tuple[Union[Dict[int, int], str], int]:
    """
    DPLL (Davis, Putnam, Logemann, Loveland) solver implementation for
    checking SAT formulas satisfiability, upgraded with better values generation
    and smarter evaluation order.

    Instead of naive checking x=1 and then x=0, we check:
    - x=1
    - x=0, y=1,
    - x=0, y=0, z=1,
    - ...
    - x=0, y=0, z=0, …, a=1

    Additionally, we check the formulas from the shortest to the longest. This
    way we potentially eliminate the unsatisfiable values fast.

    :param formula: list of clauses in CNF form
    :returns: tuple of:
    - list of values if formula is satisfiable, "UNSAT" otherwise
    - number of recurrent calls to the solver procedure
    """
    global _recurrence_counter
    _recurrence_counter = 0

    result = _solve(formula, values=dict())
    return result, _recurrence_counter
