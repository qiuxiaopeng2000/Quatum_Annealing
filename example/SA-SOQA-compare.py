# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SOQA import SOQA

name = 'ms'
order = ['cost', 'revenue']
result_folder = 'so-sa-example'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
qp = QP(name, order)
weights = {'cost': 1/2, 'revenue': 1/2}

# solve with Genetic Algorithm
result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.01, L=50, max_stay=10, sample_times=100)
sa_result = MethodResult('sa', problem_result.path, qp)
sa_result.add(result1)

# solve with cplex
result = SOQA.solve(problem=qp, weights=weights, num_reads=100, sample_times=100)
so_result = MethodResult('soqp', problem_result.path, qp)
so_result.add(result)

# dump the results
problem_result.add(sa_result)
problem_result.add(so_result)
problem_result.dump()

# compare
scores = problem_result.statistical_analysis(method1="sa", method2="soqp", weights=weights)
table = Visualizer.tabulate_single_problem(
    name, ['soqp', 'sa'], ['statistic', 'p_value', 'mean', 'std', 'max', 'min', 'time'],
    scores, {'statistic': 8, 'p_value': 8, 'mean': 8, 'std': 8, 'max': 8, 'min': 8, 'time': 8}
)
Visualizer.tabluate(table, 'so-sa-compare-example.csv')

