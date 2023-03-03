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
result_folder = 'sa'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
qp = QP(name, order)
weights = {'cost': 1/2, 'revenue': 1/2}

# solve with Genetic Algorithm
result = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.01, L=10, max_stay=5, sample_times=1)
sa_result = MethodResult('sa', problem_result.path, qp)
sa_result.add(result)

# dump the results
problem_result.add(sa_result)
problem_result.dump()
print(sa_result.results[0].elapsed)


