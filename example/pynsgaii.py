# Put this file at Nen/ (Project Root Path)
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, LP
from nen.Solver.GASolver import GASolver


name = 'rp'
order = ['cost', 'revenue']
result_folder = 'GA'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
lp = LP(name, order)

# solve with NSGA-II
result = GASolver.solve(iterations=1000, populationSize=100, maxEvaluations=100000, crossoverProbability=0.8,
                        mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
ga_result = MethodResult('ga', problem_result.path, lp)
ga_result.add(result)
problem_result.add(ga_result)

# dump the results
problem_result.dump()




