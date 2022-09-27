# Load the project path
from project_path import PROJECT_PATH
import sys
from nen import QP, ProblemResult, MethodResult, Quadratic
from nen.Solver import RQAWSOSolver, EmbeddingSampler, SolverUtil
sys.path.append(PROJECT_PATH)

max_reverse_loop = 100

problem = QP('ms', ['cost', 'revenue'])
weights = {'cost': 1/2, 'revenue': 1/2}
# vectorize record the num of objective, if you want to
# solve single-problem with wso, you must vectorize problem with one objective
problem.vectorize(['cost', 'revenue'])

wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)

# anneal_schedule = [[0.0, 1.0], [10.0, 0.5], [20, 1.0]]
anneal_schedule = [[[0.0, 1.0], [t, 0.5], [20, 1.0]] for t in (5, 10, 15)]
result = RQAWSOSolver.solve(problem=problem, weights=weights,
                            penalty=penalty, num_reads=100,
                            max_reverse_loop=max_reverse_loop,
                            anneal_schedule=anneal_schedule)

# add result to method result, problem result
problem_result = ProblemResult('ms', problem)
moqa_method_result = MethodResult('rqawso', problem_result.path, problem)
moqa_method_result.add(result)
problem_result.add(moqa_method_result)

# dump result to result/given_path folder
problem_result.dump()
