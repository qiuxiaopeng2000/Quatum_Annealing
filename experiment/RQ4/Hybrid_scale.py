import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP, LP
from nen.Solver.HybridSolver import HybridSolver
from nen.Solver.GASolver import GASolver

names_NRP = ['classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

names_FSP = ['eCos', 'Freebsd', 'Fiasco']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

rates = [0.3, 0.5, 0.7]

for name in names_NRP:
    for rate in rates:
        order = order_NRP
        result_folder = 'HY-GA-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        lp = LP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.solve(problem=qp, sample_times=10, num_reads=100, maxEvaluations=20000, seed=1,
                                        sub_size=100, rate=rate, annealing_time=40)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()


for name in names_FSP:
    for rate in rates:
        order = order_FSP
        result_folder = 'HY-GA-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        lp = LP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.solve(problem=qp, sample_times=10, num_reads=100, maxEvaluations=20000, seed=1,
                                        sub_size=100, rate=rate, annealing_time=40)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()

'''++++++++++++++++++++++++++++++++++++++++++++++++++++'''

# compare Hybrid with SA
for name in names_NRP:
    for rate in rates:
        order = order_NRP
        result_folder = 'hy-sa-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        lp = LP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.single_solve(problem=qp, weights=weight_NRP[0], sample_times=30, num_reads=1000, t_max=100,
                                               t_min=0.0001, L=300, max_stay=150, sub_size=100, rate=rate)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()


for name in names_FSP:
    for rate in rates:
        order = order_FSP
        result_folder = 'HY-GA-{}'.format(name)

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, result_folder)
        qp = QP(name, order)
        lp = LP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.single_solve(problem=qp, weights=weight_FSP[0], sample_times=30, num_reads=1000,
                                               t_max=100,  t_min=0.0001, L=300, max_stay=150, sub_size=100, rate=rate)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()
