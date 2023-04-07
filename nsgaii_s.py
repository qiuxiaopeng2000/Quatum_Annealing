# Put this file at Nen/ (Project Root Path)
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem
from nen.Solver import JarSolver
from nen.Solver.GASolver import GASolver
from nen import ProblemResult, MethodResult

names_FSP = ['ERS', 'WebPortal', 'Drupal', 'E-Shop', 'eCos', 'uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder = 'nsgaii'

for name in names_NRP:

    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)

    # solve with NSGA-II
    ea_result = MethodResult('nsgaii', problem_result.path, problem)
    for _ in range(30):
        result = GASolver.solve(populationSize=1000, maxEvaluations=20000, crossoverProbability=0.8,
                                mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
        ea_result.add(result)

    # load results
    problem_result.add(ea_result)
    problem_result.dump()

for name in names_FSP:
    # result_folder = 'nsgaii-{}'.format(name)
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    problem_result = ProblemResult(name, problem, result_folder)

    # solve with NSGA-II
    ea_result = MethodResult('nsgaii', problem_result.path, problem)
    for _ in range(30):
        result = GASolver.solve(populationSize=1000, maxEvaluations=50000, crossoverProbability=0.8,
                                mutationProbability=(1 / problem.variables_num), seed=1, problem=problem)
        ea_result.add(result)

    problem_result.add(ea_result)
    problem_result.dump()
