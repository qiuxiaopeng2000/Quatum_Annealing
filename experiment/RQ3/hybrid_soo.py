# Load the project path
# from project_path import PROJECT_PATH
# import sys
# sys.path.append(PROJECT_PATH)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import HybridSolver

names_FSP = ['eCos', 'uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder = 'hysoo'

# for name in names_NRP:
#     # result_folder = 'hysoo-{}'.format(name)
#     problem = QP(name, order_NRP)
#     problem_result = ProblemResult(name, problem, result_folder)
#     moqa_method_result = MethodResult('hysoo', problem_result.path, problem)
#     for _ in range(30):
#         result = HybridSolver.single_solve(problem=problem, num_reads=30, weights=weight_NRP, sub_size=100,
#                                            t_max=100, t_min=1e-3, alpha=0.98)
#         moqa_method_result.add(result)
#
#     # add result to method result, problem result
#     problem_result.add(moqa_method_result)
#
#     # dump result to result/given_path folder
#     problem_result.dump()

for name in names_FSP:
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('hysoo', problem_result.path, problem)
    for i in range(30):
        result = HybridSolver.single_solve(problem=problem, num_reads=30, weights=weight_FSP, sub_size=100,
                                           t_max=100, t_min=1e-3, alpha=0.98)
        print(i)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()


