# Put this file at Nen/ (Project Root Path)
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP, LP
from nen.Solver.MOQASolver import MOQASolver
from nen.Solver.GASolver import GASolver

# names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'realistic-e1', 'realistic-g1', 'realistic-m1']
names_NRP = ['rp', 'ms', 'Baan', 'classic-1']
order_NRP = ['cost', 'revenue']
# names_FSP = ['BerkeleyDB', 'ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
names_FSP = ['Amazon']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']

for name in names_FSP:
    order = order_FSP
    result_folder = 'QA-GA-{}'.format(name)

    problem = Problem(name)
    problem.vectorize(order)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)
    qp = QP(name, order)
    lp = LP(name, order)

    # solve with NSGA-II
    ga_result = MethodResult('ga', problem_result.path, lp)
    for _ in range(3):
        result1 = GASolver.solve(populationSize=100, maxEvaluations=50000, crossoverProbability=0.8, iterations=10,
                                 mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
        ga_result.add(result1)

    # solve with cplex
    qp_result = MethodResult('moqa', problem_result.path, qp)
    for _ in range(3):
        result = MOQASolver.solve(qp, num_reads=100, sample_times=10)
        qp_result.add(result)

    # dump the results
    problem_result.add(ga_result)
    problem_result.add(qp_result)
    problem_result.dump()

    # compare
    scores = problem_result.union_average_compare(union_method='moqa', average_method='ga')
    table = Visualizer.tabulate_single_problem(
        name, ['moqa', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores, {'elapsed time': 4, 'found': 3, 'front': 3, 'igd': 2, 'hv': 2, 'spacing': 2, 'tts': 6}
    )
    Visualizer.tabluate(table, 'qa-ga-compare-{}.csv'.format(name))

for name in names_NRP:
    order = order_NRP
    result_folder = 'QA-GA-{}'.format(name)

    problem = Problem(name)
    problem.vectorize(order)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)
    qp = QP(name, order)
    lp = LP(name, order)

    # solve with NSGA-II
    ga_result = MethodResult('ga', problem_result.path, lp)
    for _ in range(3):
        result1 = GASolver.solve(populationSize=100, maxEvaluations=20000, crossoverProbability=0.8, iterations=10,
                                 mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
        ga_result.add(result1)

    # solve with cplex
    qp_result = MethodResult('moqa', problem_result.path, qp)
    for _ in range(3):
        result = MOQASolver.solve(qp, num_reads=100, sample_times=10)
        qp_result.add(result)

    # dump the results
    problem_result.add(ga_result)
    problem_result.add(qp_result)
    problem_result.dump()

    # compare
    scores = problem_result.union_average_compare(union_method='moqa', average_method='ga')
    table = Visualizer.tabulate_single_problem(
        name, ['moqa', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores, {'elapsed time': 4, 'found': 3, 'front': 3, 'igd': 2, 'hv': 2, 'spacing': 2, 'tts': 6}
    )
    Visualizer.tabluate(table, 'qa-ga-compare-{}.csv'.format(name))
