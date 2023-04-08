import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, QP, LP
from nen.Solver.HybridSolver import HybridSolver
from nen.Solver.GASolver import GASolver

names_NRP = ['classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

names_FSP = ['uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

rates = [0.3, 0.5, 0.7]

hymoo_result_folder = 'hymoo'
hysoo_result_folder = 'hysoo'

for name in names_NRP:
    for rate in rates:
        problem = QP(name, order_NRP)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, hymoo_result_folder)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
        for _ in range(3):
            result = HybridSolver.solve(problem=problem, num_reads=100, sample_times=10, sub_size=100,
                                        maxEvaluations=20000, annealing_time=20, rate=rate)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()


for name in names_FSP:
    for rate in rates:
        order = order_FSP

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, hymoo_result_folder)
        qp = QP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.solve(problem=qp, sample_times=10, num_reads=100, sub_size=100,
                                        maxEvaluations=50000, annealing_time=20, rate=rate)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()

'''++++++++++++++++++++++++++++++++++++++++++++++++++++'''

# compare Hybrid with SA
# for name in names_NRP:
#     for rate in rates:
#         order = order_NRP
#
#         problem = Problem(name)
#         problem.vectorize(order)
#
#         # prepare the problem result folder before solving
#         problem_result = ProblemResult(name, problem, hysoo_result_folder)
#         qp = QP(name, order)
#         lp = LP(name, order)
#
#         # solve with cplex
#         hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
#         for _ in range(15):
#             result = HybridSolver.single_solve(problem=qp, weights=weight_NRP, num_reads=30, t_max=100,
#                                                t_min=1e-3, sub_size=100, rate=rate, alpha=0.98)
#             hy_result.add(result)
#
#         # dump the results
#         problem_result.add(hy_result)
#         problem_result.dump()
#
#
# for name in names_FSP:
#     for rate in rates:
#         order = order_FSP
#
#         problem = Problem(name)
#         problem.vectorize(order)
#
#         # prepare the problem result folder before solving
#         problem_result = ProblemResult(name, problem, hysoo_result_folder)
#         qp = QP(name, order)
#         lp = LP(name, order)
#
#         # solve with cplex
#         hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
#         for _ in range(15):
#             result = HybridSolver.single_solve(problem=qp, weights=weight_FSP, num_reads=30, sub_size=100,
#                                                t_max=100,  t_min=0.0001, rate=rate, alpha=0.98)
#             hy_result.add(result)
#
#         # dump the results
#         problem_result.add(hy_result)
#         problem_result.dump()
