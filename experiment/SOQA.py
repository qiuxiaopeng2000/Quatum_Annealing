# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SOQASolver import SOQA

# names_FSP = ['BerkeleyDB', 'ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
names_FSP = ['ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = [{'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4},
              {'COST': 1 / 2, 'USED_BEFORE': 1 / 6, 'DEFECTS': 1 / 6, 'DESELECTED': 1 / 6},
              {'COST': 1 / 6, 'USED_BEFORE': 1 / 2, 'DEFECTS': 1 / 6, 'DESELECTED': 1 / 6},
              {'COST': 1 / 6, 'USED_BEFORE': 1 / 6, 'DEFECTS': 1 / 2, 'DESELECTED': 1 / 6},
              {'COST': 1 / 6, 'USED_BEFORE': 1 / 6, 'DEFECTS': 1 / 6, 'DESELECTED': 1 / 2}]

names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'realistic-e1', 'realistic-g1', 'realistic-m1']
order_NRP = ['cost', 'revenue']
weight_NRP = [{'cost': 1 / 2, 'revenue': 1 / 2},
              {'cost': 1 / 5, 'revenue': 4 / 5},
              {'cost': 4 / 5, 'revenue': 1 / 5}]

for name in names_FSP:
    flag = 0
    for weight in weight_FSP:
        order = order_FSP
        result_folder = 'so-sa-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        weights = weight

        # solve with Genetic Algorithm
        result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.0001, L=1,
                                    max_stay=20, sample_times=5, num_reads=100)
        sa_result = MethodResult('sa', problem_result.path, qp)
        sa_result.add(result1)

        # solve with cplex
        result = SOQA.solve(problem=qp, weights=weights, sample_times=5, step_count=1, num_reads=100)
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
        Visualizer.tabluate(table, 'so-sa-compare-{}-{}.csv'.format(name, flag))
        flag += 1

for name in names_NRP:
    flag = 0
    for weight in weight_NRP:
        order = order_NRP
        result_folder = 'so-sa-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        weights = {'cost': 1 / 2, 'revenue': 1 / 2}

        # solve with Genetic Algorithm
        result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.0001, L=1,
                                    max_stay=20, sample_times=10, num_reads=100)
        sa_result = MethodResult('sa', problem_result.path, qp)
        sa_result.add(result1)

        # solve with cplex
        result = SOQA.solve(problem=qp, weights=weights, sample_times=10, step_count=100, num_reads=100)
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
        Visualizer.tabluate(table, 'so-sa-compare-{}-{}.csv'.format(name, flag))
        flag += 1
