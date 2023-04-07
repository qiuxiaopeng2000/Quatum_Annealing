# Load the project path
# from project_path import PROJECT_PATH
# import sys
# sys.path.append(PROJECT_PATH)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import HybridSolver

names_FSP = ['eCos']
# names_FSP = ['E-Shop', 'eCos', 'uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}


for name in names_FSP:
    result_folder = 'hymoo'
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('hymoo-{}'.format(name), problem_result.path, problem)
    for _ in range(1):
        result = HybridSolver.solve(problem=problem, num_reads=100, sample_times=10, sub_size=100,
                                    maxEvaluations=50000, annealing_time=20)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

# for name in names_NRP:
#     result_folder = 'hymoo'.format(name)
#     problem = QP(name, order_NRP)
#     problem_result = ProblemResult(name, problem, result_folder)
#     moqa_method_result = MethodResult('hymoo-{}'.format(name), problem_result.path, problem)
#     for _ in range(1):
#         result = HybridSolver.solve(problem=problem, num_reads=100, sample_times=10, sub_size=100, maxEvaluations=200000,
#                                     order=order_NRP, problem_result=problem_result, result_folder=result_folder, annealing_time=30
#                                     )
#         moqa_method_result.add(result)
#
#     # add result to method result, problem result
#     problem_result.add(moqa_method_result)
#
#     # dump result to result/given_path folder
#     problem_result.dump()
