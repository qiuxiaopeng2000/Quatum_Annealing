# Load the project path
from project_path import PROJECT_PATH
import sys
sys.path.append(PROJECT_PATH)

from nen import LP, ProblemResult, MethodResult
from nen.Solver import ExactECSolver

# load problem
problem = LP('ms', ['cost', 'revenue'])
# solve with ExactECSolver and get the result
result = ExactECSolver.solve(problem)

# add result to method result, problem result
problem_result = ProblemResult('ms', problem)
exact_method_result = MethodResult('exact-ec', problem_result.path, problem)
exact_method_result.add(result)
problem_result.add(exact_method_result)

# dump result to result/given_path folder
problem_result.dump()
