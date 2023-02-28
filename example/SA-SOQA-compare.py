# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP, LP
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SOQA import SOQA

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
ga_result = MethodResult('ga', problem_result.path, qp)
ga_result.add(result1)

# solve with cplex
result = SOQA.solve(qp, )
qp_result = MethodResult('moqp', problem_result.path, qp)
qp_result.add(result)

# dump the results
problem_result.add(ga_result)
problem_result.add(qp_result)
problem_result.dump()

# compare
scores = problem_result.union_average_compare(union_method='moqp', average_method='ga')
table = Visualizer.tabulate_single_problem(
    name, ['moqa', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
    scores, {'elapsed time': 2, 'found': 2, 'front': 2, 'igd': 2, 'hv': 0, 'spacing': 2, 'tts': 6}
)
Visualizer.tabluate(table, 'compare-example.csv')
