import matplotlib.pyplot as plt
from numpy import linspace
import pycosat
import random


def get_random_variable(max_var):
    sign = [1, -1]
    variable_number = range(1, max_var + 1)
    var = random.choice(sign) * random.choice(variable_number)
    return var


def get_random_clause(size, max_var):
    clause = [get_random_variable(max_var)
              for _ in range(size)]
    return clause


def get_random_formula(clause_no, clause_size, max_var):
    # clause_no = a * n
    # clause_size = 3
    # max_var = n
    formula = [get_random_clause(clause_size, max_var)
               for _ in range(clause_no)]
    return formula


def is_satisfiable(SAT_formula):
    sol = pycosat.solve(SAT_formula)
    if sol == "UNSAT":
        return False
    else:
        return True


def plot(x, y):
    plt.scatter(x, y)
    plt.title("Results for k=3 (SAT-3CNF), 10 variables, 100 repeats")
    plt.xlabel("a value (there are a * n clauses)")
    plt.ylabel("Satisfiability probability")
    plt.savefig("plot.png")
    plt.show()


def calc_sat_probs_and_plot():
    """
    Calculate probability of random formula being satisfiable based on it's 
    size n (number of variables). The result is plotted and shown.
    Conclusion: probability sharply decreases with number of variables, which
    makes sense, since this problem is hard.
    """
    k = 3  # SAT-3CNF
    n = 10  # number of variables: x_1, x_2, ..., x_n
    repeats = 100  # average probability for each one

    max_var = n

    sat_prob = []  # probability of formula being satisfiable
    for a in linspace(1, 10, 90):
        a = round(a, 1)  # scaling factor for number of clauses

        clause_no = int(a * n)
        satisfiable_count = 0
        for _ in range(repeats):
            formula = get_random_formula(clause_no, k, max_var)
            satisfiable_count += is_satisfiable(formula)

        probability = satisfiable_count / repeats
        sat_prob.append((a, probability))

    x, y = zip(*sat_prob)
    plot(x, y)
