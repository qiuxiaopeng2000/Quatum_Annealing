# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SOQASolver import SOQA

names_FSP = ['BerkeleyDB', 'ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
# names_FSP = ['WebPortal', 'Drupal', 'E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
alternative_FSP = ['less', 'less', 'less']
# weight_FSP = [{'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4},
#               {'COST': 1 / 2, 'USED_BEFORE': 1 / 6, 'DEFECTS': 1 / 6, 'DESELECTED': 1 / 6},
#               {'COST': 1 / 6, 'USED_BEFORE': 1 / 2, 'DEFECTS': 1 / 6, 'DESELECTED': 1 / 6},
#               {'COST': 1 / 6, 'USED_BEFORE': 1 / 6, 'DEFECTS': 1 / 2, 'DESELECTED': 1 / 6},
#               {'COST': 1 / 6, 'USED_BEFORE': 1 / 6, 'DEFECTS': 1 / 6, 'DESELECTED': 1 / 2}]
weight_FSP = [{'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4},
              ]

# names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'realistic-e1', 'realistic-g1', 'realistic-m1']
names_NRP = ['ms', 'Baan', 'classic-1', 'classic-2', 'classic-3', 'classic-4', 'classic-5']
alternative_NRP = ['greater', 'greater', 'greater']
order_NRP = ['cost', 'revenue']
# weight_NRP = [{'cost': 1 / 2, 'revenue': 1 / 2},
#               {'cost': 1 / 5, 'revenue': 4 / 5},
#               {'cost': 4 / 5, 'revenue': 1 / 5}]
weight_NRP = [{'cost': 1 / 2, 'revenue': 1 / 2},
              ]

# for name in names_FSP:
#
#     for weight in weight_FSP:
#         order = order_FSP
#         result_folder = 'so-sa-{}'.format(name)
#
#         problem = Problem(name)
#         problem.vectorize(order)
#
#         # prepare the problem result folder before solving
#         problem_result = ProblemResult(name, problem, result_folder)
#         qp = QP(name, order)
#         weights = weight
#
#         # solve with SA Algorithm
#         result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.0001, L=100,
#                                     max_stay=20, sample_times=10, num_reads=1000)
#         sa_result = MethodResult('sa', problem_result.path, qp)
#         sa_result.add(result1)
#
#         # solve with cplex
#         result = SOQA.solve(problem=qp, weights=weights, sample_times=10, num_reads=100)
#         so_result = MethodResult('soqp', problem_result.path, qp)
#         so_result.add(result)
#
#         # dump the results
#         problem_result.add(sa_result)
#         problem_result.add(so_result)
#         problem_result.dump()
#
#         # compare
#         scores = problem_result.statistical_analysis(method1="sa", method2="soqp", weights=weights, alternative='greater')
#         table = Visualizer.tabulate_single_problem(
#             name, ['sa', 'soqp'], ['statistic', 'p_value', 'mean', 'std', 'max', 'min', 'time'],
#             scores, {'statistic': 8, 'p_value': 8, 'mean': 8, 'std': 8, 'max': 8, 'min': 8, 'time': 8}
#         )
#         Visualizer.tabluate(table, 'so-sa-compare-{}.csv'.format(name))


for name in names_NRP:
    for weight in weight_NRP:
        order = order_NRP
        result_folder = 'so-sa-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        weights = weight

        # solve with SA Algorithm
        result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.0001, L=300,
                                    max_stay=50, sample_times=10, num_reads=1000)
        sa_result = MethodResult('sa', problem_result.path, qp)
        sa_result.add(result1)

        # solve with cplex
        result = SOQA.solve(problem=qp, weights=weights, sample_times=10, num_reads=1000)
        so_result = MethodResult('soqp', problem_result.path, qp)
        so_result.add(result)

        # dump the results
        problem_result.add(sa_result)
        problem_result.add(so_result)
        problem_result.dump()

        # compare
        scores = problem_result.statistical_analysis(method1="sa", method2="soqp", weights=weights, alternative='greater')
        table = Visualizer.tabulate_single_problem(
            name, ['soqp', 'sa'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores, {'time': 6, 'statistic': 8, 'p_value': 8, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table, 'so-sa-compare-{}.csv'.format(name))
