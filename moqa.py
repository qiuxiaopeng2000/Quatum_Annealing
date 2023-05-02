# Load the project path
# from project_path import PROJECT_PATH
# import sys
# sys.path.append(PROJECT_PATH)
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import MOQASolver


names_FSP = ['ERS', 'WebPortal', 'Drupal', 'E-Shop']
# names_FSP = ['E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

# names_NRP = ['rp', 'ms', 'Baan', 'classic-1']
names_NRP = ['Baan']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder = 'moqa_'

for name in names_NRP:
    # result_folder = 'moqa-{}'.format(name)
    problem = QP(name, order_NRP, offset_flag=True)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('moqa', problem_result.path, problem)
    for _ in range(1):
        result = MOQASolver.solve(problem=problem, sample_times=20, num_reads=300)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

# for name in names_FSP:
#     problem = QP(name, order_FSP, offset_flag=True)
#     problem_result = ProblemResult(name, problem, result_folder)
#     moqa_method_result = MethodResult('moqa', problem_result.path, problem)
#     for _ in range(1):
#         result = MOQASolver.solve(problem=problem, sample_times=20, num_reads=300)
#         moqa_method_result.add(result)

#     # add result to method result, problem result
#     problem_result.add(moqa_method_result)

#     # dump result to result/given_path folder
#     problem_result.dump()


