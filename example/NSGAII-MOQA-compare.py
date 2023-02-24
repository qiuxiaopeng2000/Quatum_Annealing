# Put this file at Nen/ (Project Root Path)
import sys
# import os
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
from os import path
from pathlib import Path
ROOT_DIR = path.dirname(Path(__file__).parent.parent)
sys.path.append(ROOT_DIR)

from nen import Problem, ProblemResult, MethodResult, Visualizer, QP
from nen.Solver import JarSolver, MOQASolver

name = 'ms'
order = ['cost', 'revenue']
result_folder = 'ms-ea-example'

problem = Problem(name)
problem.vectorize(order)

# prepare the problem result folder before solving
problem_result = ProblemResult(name, problem, result_folder)

# solve with NSGA-II
JarSolver.solve(
    solver_name='NSGAII', config_name='tmp_config',
    problem=name, objectiveOrder=order, iterations=10,
    populationSize=500, maxEvaluations=100000,
    crossoverProbability=0.8, mutationProbability=(1 / problem.variables_num),
    resultFolder=result_folder, methodName='ga'
)
# load results
ea_result = MethodResult('ga', problem_result.path, problem)
ea_result.load()

# solve with cplex
qp = QP(name, order)
result = MOQASolver.solve(qp, sample_times=10, num_reads=100)
ex_result = MethodResult('moqp', problem_result.path, qp)
ex_result.add(result)

# dump the results
problem_result.add(ea_result)
problem_result.add(ex_result)
problem_result.dump()

# compare
scores = problem_result.union_average_compare(union_method='moqp', average_method='ga')
table = Visualizer.tabulate_single_problem(
    name, ['moqa', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
    scores, {'elapsed time': 2, 'found': 2, 'front': 2, 'igd': 2, 'hv': 0, 'spacing': 2, 'tts': 6}
)
Visualizer.tabluate(table, 'compare-example.csv')
