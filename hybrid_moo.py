# Load the project path
# from project_path import PROJECT_PATH
# import sys
# sys.path.append(PROJECT_PATH)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import HybridSolver

names_FSP = ['Amazon']
# names_FSP = ['E-Shop', 'eCos', 'uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

# names_NRP = ['classic-1', 'classic-2', 'classic-3']
names_NRP = ['Baan']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

hymoo_result_folder = 'hymoo'
hysoo_result_folder = 'hysoo'

# Multi-objective problems
for name in names_FSP:
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, hymoo_result_folder)
    moqa_method_result = MethodResult('hymoo', problem_result.path, problem)
    for _ in range(1):
        result = HybridSolver.solve(problem=problem, num_reads=100, sample_times=10, sub_size=100,
                                    maxEvaluations=50000, annealing_time=20)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

for name in names_NRP:
    problem = QP(name, order_NRP, offset_flag=True)
    problem_result = ProblemResult(name, problem, hymoo_result_folder)
    moqa_method_result = MethodResult('hymoo', problem_result.path, problem)
    for _ in range(1):
        result = HybridSolver.solve(problem=problem, num_reads=100, sample_times=10, sub_size=100,
                                    maxEvaluations=200000, annealing_time=20)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

#+++++++++++++++++++++++++++++++++++++++++++

# Single objective problems
for name in names_NRP:
    problem = QP(name, order_NRP, offset_flag=True)
    problem_result = ProblemResult(name, problem, hysoo_result_folder)
    moqa_method_result = MethodResult('hysoo', problem_result.path, problem)
    for i in range(3):
        result = HybridSolver.single_solve(problem=problem, num_reads=30, weights=weight_NRP, sub_size=100,
                                           t_max=100, t_min=1e-2, alpha=0.98)
        moqa_method_result.add(result)
    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

for name in names_FSP:
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, hysoo_result_folder)
    moqa_method_result = MethodResult('hysoo', problem_result.path, problem)
    for i in range(3):
        result = HybridSolver.single_solve(problem=problem, num_reads=30, weights=weight_FSP, sub_size=100,
                                           t_max=100, t_min=1e-2, alpha=0.98)
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()
