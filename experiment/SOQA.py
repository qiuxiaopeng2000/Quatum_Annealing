# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SOQASolver import SOQA

names = ['ms', 'rp', 'Baan']
for name in names:
    order = ['cost', 'revenue']
    result_folder = 'so-sa-{}'.format(name)

    problem = Problem(name)
    problem.vectorize(order)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)
    qp = QP(name, order)
    weights = {'cost': 1 / 2, 'revenue': 1 / 2}

    # solve with Genetic Algorithm
    result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.001, L=1,
                                max_stay=20, sample_times=10, num_reads=100)
    sa_result = MethodResult('sa', problem_result.path, qp)
    sa_result.add(result1)

    # solve with cplex
    result = SOQA.solve(problem=qp, weights=weights, sample_times=10, step_count=1, num_reads=100)
    so_result = MethodResult('soqp', problem_result.path, qp)
    so_result.add(result)

    # dump the results
    problem_result.add(sa_result)
    problem_result.add(so_result)
    problem_result.dump()

    # compare
    scores = problem_result.statistical_analysis(method1="sa", method2="soqp", weights=weights)
    table = Visualizer.tabulate_single_problem(
        name, ['sa', 'soqp'], ['statistic', 'p_value', 'mean', 'std', 'max', 'min', 'time'],
        scores, {'statistic': 8, 'p_value': 8, 'mean': 8, 'std': 8, 'max': 8, 'min': 8, 'time': 8}
    )
    Visualizer.tabluate(table, 'so-sa-compare-{}.csv'.format(name))
