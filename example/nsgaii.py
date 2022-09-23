# Put this file at Nen/ (Project Root Path)
from nen import Problem, ProblemResult, MethodResult
from nen.Solver import JarSolver

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
    problem=name, objectiveOrder=order, iterations=1,
    populationSize=500, maxEvaluations=100000,
    crossoverProbability=0.8, mutationProbability=(1 / problem.variables_num),
    resultFolder=result_folder, methodName='ea'
)

# load results
ea_result = MethodResult('ea', problem_result.path, problem)
ea_result.load()

problem_result.add(ea_result)
problem_result.dump()
