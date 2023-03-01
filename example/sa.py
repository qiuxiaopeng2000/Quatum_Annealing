# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, QP
from nen.Solver.FSAQPSolver import FSAQPSolver


name = 'ms'
order = ['cost', 'revenue']
result_folder = 'ms-ea-example'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
qp = QP(name, order)
weights = {'cost': 1/2, 'revenue': 1/2}

# solve with Genetic Algorithm
result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.01, L=300, max_stay=150)
ga_result = MethodResult('sa', problem_result.path, qp)
ga_result.add(result1)

# dump the results
problem_result.add(ga_result)
problem_result.dump()


