import operator
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


def _unit_propagation_with_fixed_sign(
    formula: List[List[int]], values: Dict[int, int]
) -> Optional[List[List[int]]]:
    """
    Simplifies a SAT formula with unit propagation and fixed sign variable evaluation.

    If there is a clause with a single variable, it has to be True. Setting
    this may change the rest of formula, so we continue as long as there are
    any changes. In this process we may reduce the formula to the empty one
    (satisfied) or detect unsatisfiability.

    If there is a variable that has a fixed sign (non-negated / negated) in the
    entire formula, we can set a value to it.

    For formulas we assume that:
    - None formula is not satisfied
    - [] formula is satisfied (since it's an empty conjunction, similar to
      product of ones being one)

    :param formula: list of clauses in CNF form
    :param values: values of variables
    :return: simplified formula
    """
    change = True
    while change:
        change = False

        # unit propagation
        for clause in formula:
            if len(clause) == 1 and clause[0] not in values:
                variable = clause[0]
                values[variable] = 1
                values[-variable] = -1
                change = True

        # fixed value variable evaluation
        all_variables = set()
        for clause in formula:
            all_variables |= set(clause)

        for variable in all_variables:
            if -variable not in all_variables:
                values[variable] = 1
                values[-variable] = -1
                change = True

        formula = _simplify_formula(formula, values)
        if formula is None:
            return None

    return formula


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
    formula = _unit_propagation_with_fixed_sign(formula, values)
    if formula == []:
        # empty formulas are satisfied
        return values
    elif formula is None:
        # None formulas are unsatisfiable
        return "UNSAT"

    # evaluate formulas from the shortest to the longest
    formula.sort(key=len)

    # check variables from the most common (is in the most clauses) to the least common
    first_clause_variable_counts = {v: 1 for v in formula[0]}
    for clause in formula[1:]:
        for v in clause:
            if v in first_clause_variable_counts:
                first_clause_variable_counts[v] += 1

    # we have tuples (v, count); sort them descending by count and select variables only
    first_clause_variables = [
        v
        for v, count in sorted(
            first_clause_variable_counts.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )
    ]

    # try to satisfy the first, shortest formula
    for variable in first_clause_variables:
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


def full_dpll_solve(formula: List[List[int]]) -> Tuple[Union[Dict[int, int], str], int]:
    """
    Full DPLL (Davis, Putnam, Logemann, Loveland) solver implementation for
    checking SAT formulas satisfiability, upgraded with:
    - better values generation
    - smarter evaluation order
    - unit propagation
    - fixed sign variable elimination
    -

    Variables with the same sign in the entire formula can be evaluated immediately
    as a part of simplification.

    :param formula: list of clauses in CNF form
    :returns: tuple of:
    - list of values if formula is satisfiable, "UNSAT" otherwise
    - number of recurrent calls to the solver procedure
    """
    global _recurrence_counter
    _recurrence_counter = 0

    result = _solve(formula, values=dict())
    return result, _recurrence_counter
