# Load the project path
# from project_path import PROJECT_PATH
# import sys
# sys.path.append(PROJECT_PATH)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import MOQASolver


names_FSP = ['E-Shop', 'uClinux']
# names_FSP = ['E-shop', 'eCos', 'Freebsd']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-1']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}


for name in names_FSP:
    result_folder = 'moqa-{}'.format(name)
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('moqa', problem_result.path, problem)
    for _ in range(3):
        result = MOQASolver.solve(problem=problem, sample_times=10, num_reads=100)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

for name in names_NRP:
    result_folder = 'moqa-{}'.format(name)
    problem = QP(name, order_NRP)
    problem_result = ProblemResult(name, problem, result_folder)
    moqa_method_result = MethodResult('moqa', problem_result.path, problem)
    for _ in range(3):
        result = MOQASolver.solve(problem=problem, sample_times=10, num_reads=100)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()
