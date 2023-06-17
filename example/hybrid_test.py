# Put this file at Nen/ (Project Root Path)
import sys
import os


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, QP
from nen.Solver.HybridSolver import HybridSolver


name = 'ms'
order = ['cost', 'revenue']
result_folder = 'test'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
qp = QP(name, order)
weights = {'cost': 1/2, 'revenue': 1/2}

# solve with Genetic Algorithm
result = HybridSolver.solve(problem=qp, sample_times=1, num_reads=1, sub_size=10)
sa_result = MethodResult('test', problem_result.path, qp)
sa_result.add(result)

# dump the results
problem_result.add(sa_result)
problem_result.dump()
print(sa_result.results[0].elapsed)
