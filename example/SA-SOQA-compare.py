# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SOQASolver import SOQA

name = 'Baan'
order = ['cost', 'revenue']
result_folder = 'so-sa_-example'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)
qp = QP(name, order)
weights = {'cost': 1/2, 'revenue': 1/2}

# solve with Genetic Algorithm
result1 = FSAQPSolver.solve(problem=qp, weights=weights, t_max=100, t_min=0.0001, L=300,
                            max_stay=20, sample_times=5, num_reads=1000)
sa_result = MethodResult('sa_', problem_result.path, qp)
sa_result.add(result1)

# solve with cplex
result = SOQA.solve(problem=qp, weights=weights, sample_times=5, num_reads=100)
so_result = MethodResult('soqp', problem_result.path, qp)
so_result.add(result)

# dump the results
problem_result.add(sa_result)
problem_result.add(so_result)
problem_result.dump()

# compare
scores = problem_result.statistical_analysis(method1="sa_", method2="soqp", weights=weights, alternative='greater')
table = Visualizer.tabulate_single_problem(
    name, ['sa_', 'soqp'], ['statistic', 'p_value', 'mean', 'std', 'max', 'min', 'time'],
    scores, {'statistic': 8, 'p_value': 8, 'mean': 8, 'std': 8, 'max': 8, 'min': 8, 'time': 8}
)
Visualizer.tabluate(table, '{}-so-sa_-compare-example.csv'.format(name))
print("1")
