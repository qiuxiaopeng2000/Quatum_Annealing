import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import SAQPSolver

names_FSP = ['ERS', 'WebPortal', 'Drupal', 'E-Shop', 'Fiasco', 'uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder = 'sa'

for name in names_FSP:
    # result_folder = 'sa-{}'.format(name)
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('sa', problem_result.path, problem)
    for _ in range(30):
        result = SAQPSolver.solve(problem=problem, num_reads=30, weights=weight_FSP, if_embed=False,
                                  t_max=100, t_min=1e-3, alpha=0.98)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

for name in names_NRP:
    # result_folder = 'sa-{}'.format(name)
    problem = QP(name, order_NRP)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('sa', problem_result.path, problem)
    for _ in range(30):
        result = SAQPSolver.solve(problem=problem, num_reads=30, weights=weight_NRP, if_embed=False,
                                  t_max=100, t_min=1e-3, alpha=0.98)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()
