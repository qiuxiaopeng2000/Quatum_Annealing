import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from nen import Problem, ProblemResult, MethodResult, Visualizer

names_FSP = ['ERS', 'WebPortal', 'Amazon']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['rp', 'ms', 'Baan']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder_sa = 'sa'
result_folder_soqa = 'soqa'

# compare SOQA with SA
for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving

    problem_result = ProblemResult(name, problem, result_folder_sa)
    problem_result_soqa = ProblemResult(name, problem, result_folder_soqa)

    sa_result = MethodResult('sa', problem_result.path, problem)
    sa_result.load(evaluate=True, single_flag=True)
    soqa_result = MethodResult('soqa', problem_result_soqa.path, problem)
    soqa_result.load(evaluate=True, single_flag=True)
    # print(name, " : {}".format(soqa_result.))

for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    # result_folder = 'so-sa-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder_sa)
    problem_result_soqa = ProblemResult(name, problem, result_folder_soqa)

    sa_result = MethodResult('sa', problem_result.path, problem)
    sa_result.load(evaluate=True, single_flag=True)
    soqa_result = MethodResult('soqa', problem_result_soqa.path, problem)
    soqa_result.load(evaluate=True, single_flag=True)

