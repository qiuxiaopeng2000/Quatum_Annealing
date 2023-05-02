import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from nen import Problem, QP
from nen.Solver.MetaSolver import SolverUtil
from nen.Term import Constraint, Quadratic
from nen.Solver.EmbeddingSampler import EmbeddingSampler

order_NRP = ['cost', 'revenue']
weights = [{'cost': 0.1, 'revenue': 0.9}, {'cost': 0.9, 'revenue': 0.1}]

problem = QP("temp", order_NRP)
for weight in weights:
    basic_weights = SolverUtil.scaled_weights(problem.objectives)
    for k, v in basic_weights.items():
        weight[k] *= v
    wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weight))
    penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
    objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
    qubo = Constraint.quadratic_to_qubo_dict(objective)
    print(penalty)
    print(qubo)
print(problem.variables_num, problem.constraints_num)

  