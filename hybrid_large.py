# Load the project path
# from project_path import PROJECT_PATH
# import sys
# sys.path.append(PROJECT_PATH)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import HybridSolver

# names_FSP = ['Amazon']
# names_FSP = ['E-Shop', 'eCos', 'uClinux', 'Amazon']
names_FSP = [ 'uClinux', 'eCos','Fiasco']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-2', 'classic-3', 'classic-5']
# names_NRP = ['classic-5']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

hymoo_result_folder = 'hymoo_m'
hysoo_result_folder = 'hysoo_m'

# Multi-objective problems
# for name in names_NRP:
#     problem = QP(name, order_NRP, offset_flag=True)
#     problem_result = ProblemResult(name, problem, hymoo_result_folder)
#     moqa_method_result = MethodResult('hymoo', problem_result.path, problem)
#     for _ in range(1):
#         result = HybridSolver.solve(problem=problem, num_reads=500, sample_times=20, sub_size=200, 
#                                     maxEvaluations=500000, populationSize=500, 
#                                     objectiveOrder=order_FSP, resultFolder=hymoo_result_folder, 
#                                     problem_result_path=problem_result.path,
#                                     )
#         moqa_method_result.add(result)

#     # add result to method result, problem result
#     problem_result.add(moqa_method_result)

#     # dump result to result/given_path folder
#     problem_result.dump()

for name in names_FSP:
    if name != 'Fiasco':
        continue
    problem = QP(name, order_FSP)
    problem_result = ProblemResult(name, problem, hymoo_result_folder)
    moqa_method_result = MethodResult('hymoo', problem_result.path, problem)
    for _ in range(1):
        result = HybridSolver.solve(problem=problem, num_reads=500, sample_times=10, sub_size=200, 
                                    maxEvaluations=2000000, populationSize=500, 
                                    objectiveOrder=order_FSP, resultFolder=hymoo_result_folder, 
                                    problem_result_path=problem_result.path,
                                    )
        moqa_method_result.add(result)

    # add result to method result, problem result
    problem_result.add(moqa_method_result)

    # dump result to result/given_path folder
    problem_result.dump()

#+++++++++++++++++++++++++++++++++++++++++++

# Single objective problems
# for name in names_NRP:
#     problem = QP(name, order_NRP, offset_flag=True)
#     problem_result = ProblemResult(name, problem, hysoo_result_folder)
#     moqa_method_result = MethodResult('hysoo', problem_result.path, problem)
#     for i in range(1):
#         result = HybridSolver.single_solve(problem=problem, num_reads=200, sample_times=50, sub_size=200, maxEvaluations=500000, 
#                                            populationSize=500, weights=weight_NRP, objectiveOrder=order_NRP, 
#                                            resultFolder=hysoo_result_folder, 
#                                            problem_result_path=problem_result.path
#                                            )
#         moqa_method_result.add(result)
#     # add result to method result, problem result
#     problem_result.add(moqa_method_result)

#     # dump result to result/given_path folder
#     problem_result.dump()

# for name in names_FSP:
#     problem = QP(name, order_FSP, offset_flag=True)
#     problem_result = ProblemResult(name, problem, hysoo_result_folder)
#     moqa_method_result = MethodResult('hysoo', problem_result.path, problem)
#     for i in range(1):
#         result = HybridSolver.single_solve(problem=problem, num_reads=100, sample_times=50, sub_size=200, maxEvaluations=2000000, 
#                                            populationSize=500, weights=weight_FSP, objectiveOrder=order_NRP, 
#                                            resultFolder=hysoo_result_folder, 
#                                            problem_result_path=problem_result.path
#                                            )
#         moqa_method_result.add(result)

#     # add result to method result, problem result
#     problem_result.add(moqa_method_result)

#     # dump result to result/given_path folder
#     problem_result.dump()
