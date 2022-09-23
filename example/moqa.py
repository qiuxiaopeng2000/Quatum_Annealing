# Load the project path
from project_path import PROJECT_PATH
import sys
sys.path.append(PROJECT_PATH)

from nen import QP, ProblemResult, MethodResult
from nen.Solver import MOQASolver

problem = QP('ms', ['cost', 'revenue'])
result = MOQASolver.solve(problem=problem, sample_times=10, num_reads=100)

# add result to method result, problem result
problem_result = ProblemResult('ms', problem)
moqa_method_result = MethodResult('moqa', problem_result.path, problem)
moqa_method_result.add(result)
problem_result.add(moqa_method_result)

# dump result to result/given_path folder
problem_result.dump()
