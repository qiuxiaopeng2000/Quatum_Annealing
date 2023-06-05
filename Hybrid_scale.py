import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, QP, LP
from nen.Solver.HybridSolver import HybridSolver
from nen.Solver.GASolver import GASolver

names_NRP = ['classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

# names_FSP = ['uClinux', 'eCos']
names_FSP = ['eCos']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

# rates = [0.9]
rates = [0.5, 0.7, 0.9]

hymoo_result_folder = 'hymoo'
hysoo_result_folder = 'hysoo'

# for name in names_NRP:
#     problem = QP(name, order_NRP)
#     # solve with cplex
#     for _ in range(1):
#         problem_result = ProblemResult(name, problem, hymoo_result_folder)
#         results = HybridSolver.solve_rates(problem=problem, num_reads=500, sample_times=10, sub_size=200, 
#                                     maxEvaluations=500000, populationSize=500, 
#                                     objectiveOrder=order_NRP, resultFolder=hymoo_result_folder, 
#                                     problem_result_path=problem_result.path,
#                                     annealing_time=20, rates=rates)
#         for rate in rates:
#             problem_result = ProblemResult(name, problem, hymoo_result_folder)
#             hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
#             hy_result.add(results[rate])
#             # dump the results
#             problem_result.add(hy_result)
#             problem_result.dump()


for name in names_FSP:
    problem = QP(name, order_FSP)
    # solve with cplex
    for _ in range(1):
        problem_result = ProblemResult(name, problem, hymoo_result_folder)
        results = HybridSolver.solve_rates(problem=problem, num_reads=500, sample_times=10, sub_size=200, 
                                    maxEvaluations=2000000, populationSize=500, 
                                    objectiveOrder=order_FSP, resultFolder=hymoo_result_folder, 
                                    problem_result_path=problem_result.path,
                                    annealing_time=20, rates=rates)
        for rate in rates:
            problem_result = ProblemResult(name, problem, hymoo_result_folder)
            hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
            hy_result.add(results[rate])
            # dump the results
            problem_result.add(hy_result)
            problem_result.dump()

'''++++++++++++++++++++++++++++++++++++++++++++++++++++'''

# # compare Hybrid with SA
# for name in names_NRP:
#     for rate in rates:
#         problem = QP(name, order_NRP)

#         # solve with cplex
#         hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
#         for _ in range(1):
#             results = HybridSolver.single_solve_rate(problem=problem, num_reads=200, sample_times=50, sub_size=100, 
#                                                maxEvaluations=500000, populationSize=500, weights=weight_NRP, 
#                                                objectiveOrder=order_NRP, resultFolder=hysoo_result_folder, 
#                                                problem_result_path=problem_result.path, rates=rates
#                                                )
#             for rate in rates:
#                 problem_result = ProblemResult(name, problem, hymoo_result_folder)
#                 hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
#                 hy_result.add(results[rate])
#                 # dump the results
#                 problem_result.add(hy_result)
#                 problem_result.dump()


# for name in names_FSP:
#     for rate in rates:
#         problem = QP(name, order_FSP)

#         for _ in range(1):
#             results = HybridSolver.single_solve_rate(problem=problem, num_reads=200, sample_times=50, sub_size=100, 
#                                                maxEvaluations=2000000, populationSize=500, weights=weight_FSP, 
#                                                objectiveOrder=order_FSP, resultFolder=hysoo_result_folder, 
#                                                problem_result_path=problem_result.path, rate=rate 
#                                                )
#             for rate in rates:
#                 problem_result = ProblemResult(name, problem, hymoo_result_folder)
#                 hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
#                 hy_result.add(results[rate])
#                 # dump the results
#                 problem_result.add(hy_result)
#                 problem_result.dump()
