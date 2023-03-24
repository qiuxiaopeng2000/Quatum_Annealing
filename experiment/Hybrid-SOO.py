# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver.HybridSolver import HybridSolver
from nen.Solver.SOQASolver import SOQA

# names_FSP = ['BerkeleyDB', 'ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
names_FSP = ['ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
alternative_FSP = ['less', 'less', 'less']
weight_FSP = [{'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}]

names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'realistic-e1', 'realistic-g1', 'realistic-m1']
alternative_NRP = ['greater', 'greater', 'greater']
order_NRP = ['cost', 'revenue']
weight_NRP = [{'cost': 1 / 2, 'revenue': 1 / 2}]

for name in names_FSP:
    for weight in weight_FSP:
        order = order_FSP
        result_folder = 'hy-soqa-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        weights = weight

        # solve with SOQA Algorithm
        result1 = SOQA.solve(problem=qp, weights=weights, sample_times=5, num_reads=100)
        sa_result = MethodResult('soqa', problem_result.path, qp)
        sa_result.add(result1)

        # solve with cplex
        result = HybridSolver.single_solve(problem=qp, weights=weights, sample_times=5, num_reads=100)
        so_result = MethodResult('hybrid', problem_result.path, qp)
        so_result.add(result)

        # dump the results
        problem_result.add(sa_result)
        problem_result.add(so_result)
        problem_result.dump()

        # compare
        scores = problem_result.statistical_analysis(method1="soqa", method2="hybrid", weights=weights, alternative='greater')
        table = Visualizer.tabulate_single_problem(
            name, ['soqa', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores, {'time': 6, 'statistic': 8, 'p_value': 8, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table, 'hy-soqa-compare-{}.csv'.format(name))

for name in names_NRP:
    for weight in weight_NRP:
        order = order_NRP
        result_folder = 'hy-soqa-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        weights = weight

        # solve with SOQA Algorithm
        result1 = SOQA.solve(problem=qp, weights=weights, sample_times=10, num_reads=100)
        sa_result = MethodResult('soqa', problem_result.path, qp)
        sa_result.add(result1)

        # solve with cplex
        result = HybridSolver.single_solve(problem=qp, weights=weights, sample_times=10, num_reads=100)
        so_result = MethodResult('hybrid', problem_result.path, qp)
        so_result.add(result)

        # dump the results
        problem_result.add(sa_result)
        problem_result.add(so_result)
        problem_result.dump()

        # compare
        scores = problem_result.statistical_analysis(method1="soqa", method2="hybrid", weights=weights, alternative='greater')
        table = Visualizer.tabulate_single_problem(
            name, ['soqa', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores, {'time': 6, 'statistic': 8, 'p_value': 8, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table, 'hy-soqa-compare-{}.csv'.format(name))
