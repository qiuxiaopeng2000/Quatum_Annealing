# Put this file at Nen/ (Project Root Path)
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP, LP
from nen.Solver.HybridSolver import HybridSolver
from nen.Solver.GASolver import GASolver


name = 'ms'
order = ['cost', 'revenue']
result_folder = 'HY-GA-example'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
qp = QP(name, order)
lp = LP(name, order)

# solve with NSGA-II
result1 = GASolver.solve(iterations=100, populationSize=10, maxEvaluations=10000, crossoverProbability=0.8,
                         mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
ga_result = MethodResult('ga', problem_result.path, lp)
ga_result.add(result1)


# solve with cplex
result = HybridSolver.solve(qp, sample_times=50, num_reads=10)
qp_result = MethodResult('hy', problem_result.path, qp)
qp_result.add(result)

# dump the results
problem_result.add(ga_result)
problem_result.add(qp_result)
problem_result.dump()

# compare
scores = problem_result.union_average_compare(union_method='hy', average_method='ga')
table = Visualizer.tabulate_single_problem(
    name, ['hy', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
    scores, {'elapsed time': 2, 'found': 2, 'front': 2, 'igd': 2, 'hv': 2, 'spacing': 2, 'tts': 6}
)
Visualizer.tabluate(table, 'hy-ga-compare-example.csv')
