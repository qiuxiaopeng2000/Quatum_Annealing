# Put this file at Nen/ (Project Root Path)
from nen import LP, Problem, ProblemResult, MethodResult, Visualizer
from nen.Solver import JarSolver, ExactECSolver

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
    resultFolder=result_folder, methodName='ea'
)
# load results
ea_result = MethodResult('ea', problem_result.path, problem)
ea_result.load()

# solve with cplex
lp = LP(name, order)
result = ExactECSolver.solve(lp)
ex_result = MethodResult('ex', problem_result.path, lp)
ex_result.add(result)

# dump the results
problem_result.add(ea_result)
problem_result.add(ex_result)
problem_result.dump()

# compare
scores = problem_result.union_average_compare(union_method='ex', average_method='ea')
table = Visualizer.tabulate_single_problem(
    name, ['ea', 'ex'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing'],
    scores, {'elapsed time': 2, 'found': 2, 'front': 2, 'igd': 2, 'hv': 0, 'spacing': 2}
)
Visualizer.tabluate(table, 'compare-example.csv')
