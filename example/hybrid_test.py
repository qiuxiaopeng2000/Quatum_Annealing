# Put this file at Nen/ (Project Root Path)
import sys
import os


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, QP
from nen.Solver.LeapHybridSolver import LeapHybridSolver


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
result = LeapHybridSolver.solve(problem=qp, sample_times=1, num_reads=100)
sa_result = MethodResult('sa', problem_result.path, qp)
sa_result.add(result)

# dump the results
problem_result.add(sa_result)
problem_result.dump()
print(sa_result.results[0].elapsed)
