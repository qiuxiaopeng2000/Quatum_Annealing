# Load the project path
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from nen.Solver.GASolver import GASolver
from project_path import PROJECT_PATH
import sys
sys.path.append(PROJECT_PATH)

from nen import LP, ProblemResult, MethodResult, Problem, QP, Visualizer
from nen.Solver import ExactECSolver


names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
names_FSP = ['BerkeleyDB', 'ERS', 'Drupal', 'E-Shop', 'WebPortal', 'E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']

for name in names_FSP:
    order = order_FSP
    result_folder = 'EA-GA-{}'.format(name)

    problem = Problem(name)
    problem.vectorize(order)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)
    lp = LP(name, order)

    # solve with epsilon
    ea_result = MethodResult('ea', problem_result.path, lp)
    result = ExactECSolver.solve(lp)
    ea_result.add(result)

    # solve with NSGA-II
    ga_result = MethodResult('ga', problem_result.path, lp)
    result1 = GASolver.solve(populationSize=100, maxEvaluations=50000, crossoverProbability=0.8, iterations=10,
                             mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
    ga_result.add(result1)

    # dump the results
    problem_result.add(ea_result)
    problem_result.add(ga_result)
    problem_result.dump()

    # compare
    scores = problem_result.union_average_compare(union_method='ea', average_method='ga')
    table = Visualizer.tabulate_single_problem(
        name, ['ea', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores, {'elapsed time': 4, 'found': 3, 'front': 3, 'igd': 2, 'hv': 2, 'spacing': 2, 'tts': 6}
    )
    Visualizer.tabluate(table, 'ea-ga-compare-{}.csv'.format(name))

for name in names_NRP:
    order = order_NRP
    result_folder = 'EA-GA-{}'.format(name)

    problem = Problem(name)
    problem.vectorize(order)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)
    lp = LP(name, order)

    # solve with epsilon
    ea_result = MethodResult('ea', problem_result.path, lp)
    result = ExactECSolver.solve(lp)
    ea_result.add(result)

    # solve with NSGA-II
    ga_result = MethodResult('ga', problem_result.path, lp)
    result1 = GASolver.solve(populationSize=100, maxEvaluations=50000, crossoverProbability=0.8, iterations=10,
                             mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
    ga_result.add(result1)

    # dump the results
    problem_result.add(ea_result)
    problem_result.add(ga_result)
    problem_result.dump()

    # compare
    scores = problem_result.union_average_compare(union_method='ea', average_method='ga')
    table = Visualizer.tabulate_single_problem(
        name, ['ea', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores, {'elapsed time': 4, 'found': 3, 'front': 3, 'igd': 2, 'hv': 2, 'spacing': 2, 'tts': 6}
    )
    Visualizer.tabluate(table, 'ea-ga-compare-{}.csv'.format(name))
