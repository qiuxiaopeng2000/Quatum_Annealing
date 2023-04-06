# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, QP
from nen.Solver.FSAQPSolver import FSAQPSolver

names = ['classic-1', 'classic-2', 'classic-3']
order = ['cost', 'revenue']
result_folder = 'temp'


for name in names:
    problem = Problem(name)
    problem.vectorize(order)
    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)
    qp = QP(name, order)
    weights = {'cost': 1 / 2, 'revenue': 1 / 2}

    # solve with Genetic Algorithm
    result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.0001, L=100,
                                max_stay=50, num_reads=20)
    sa_result = MethodResult('sa', problem_result.path, qp)
    sa_result.add(result1)

    # dump the results
    problem_result.add(sa_result)
    problem_result.dump()
