import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP, LP
from nen.Solver.HybridSolver import HybridSolver
from nen.Solver.GASolver import GASolver

names_FSP = ['LinuxX86']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-4']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

subsizes = [100, 500, 700, 1000]


hymoo_result_folder = 'hymoo'
hysoo_result_folder = 'hysoo'

# compare CQHA with NSGA-II
for name in names_NRP:
    for size in subsizes:
        order = order_NRP

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, hymoo_result_folder)
        qp = QP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(size), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.solve(problem=qp, sample_times=10, num_reads=100, maxEvaluations=20000, seed=1,
                                        sub_size=size, annealing_time=20)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()


for name in names_FSP:
    for size in subsizes:
        order = order_FSP

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, hymoo_result_folder)
        qp = QP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(size), problem_result.path, qp)
        for _ in range(3):
            result = HybridSolver.solve(problem=qp, sample_times=10, num_reads=100, maxEvaluations=50000, seed=1,
                                        sub_size=size, annealing_time=20)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()

'''++++++++++++++++++++++++++++++++++++++++++++++++++++'''

# compare Hybrid with SA
for name in names_NRP:
    for size in subsizes:
        order = order_NRP

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, hysoo_result_folder)
        qp = QP(name, order)
        lp = LP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(size), problem_result.path, qp)
        for _ in range(15):
            result = HybridSolver.single_solve(problem=qp, weights=weight_NRP, num_reads=30, t_max=100,
                                               t_min=1e-3, sub_size=size, alpha=0.98)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()


for name in names_FSP:
    for size in subsizes:
        order = order_FSP

        problem = Problem(name)
        problem.vectorize(order)

        # prepare the problem result folder before solving
        problem_result = ProblemResult(name, problem, hysoo_result_folder)
        qp = QP(name, order)

        # solve with cplex
        hy_result = MethodResult('hybrid{}'.format(size), problem_result.path, qp)
        for _ in range(15):
            result = HybridSolver.single_solve(problem=qp, weights=weight_FSP, num_reads=30, sub_size=size,
                                               t_max=100,  t_min=0.0001, alpha=0.98)
            hy_result.add(result)

        # dump the results
        problem_result.add(hy_result)
        problem_result.dump()
