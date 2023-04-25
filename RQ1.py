import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from nen import Problem, ProblemResult, MethodResult, Visualizer

# names_FSP = ['BerkeleyDB', 'WebPortal', 'Drupal', 'E-Shop']
names_FSP = ['E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

# names_NRP = ['rp', 'ms', 'Baan', 'classic-1']
names_NRP = ['Baan']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder_sa = 'ga_'
result_folder_soqa = 'soqa'


# compare SOQA with GA
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    # result_folder = 'so-sa_-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder_sa)
    problem_result_soqa = ProblemResult(name, problem, result_folder_soqa)

    sa_result = MethodResult('ga', problem_result.path, problem)
    sa_result.load(evaluate=True, single_flag=True)
    soqa_result = MethodResult('soqa', problem_result_soqa.path, problem)
    soqa_result.load(evaluate=True, single_flag=True)

    problem_result.add(sa_result)
    problem_result.add(soqa_result)

    # compare
    scores = problem_result.statistical_analysis(method1="ga", method2="soqa", weights=weight_NRP)
    table = Visualizer.tabulate_single_problem(
        name, ['ga', 'soqa'], ['num', 'time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'num': 4, 'time': 6, 'statistic': 8, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'so-sa-compare-{}.csv'.format(name))


# for name in names_FSP:
#     problem = Problem(name)
#     problem.vectorize(order_FSP)

#     # prepare the problem result folder before solving

#     problem_result = ProblemResult(name, problem, result_folder_sa)
#     problem_result_soqa = ProblemResult(name, problem, result_folder_soqa)

#     sa_result = MethodResult('ga', problem_result.path, problem)
#     sa_result.load(evaluate=True, single_flag=True)
#     soqa_result = MethodResult('soqa', problem_result_soqa.path, problem)
#     soqa_result.load(evaluate=True, single_flag=True)

#     problem_result.add(sa_result)
#     problem_result.add(soqa_result)

#     # compare
#     scores = problem_result.statistical_analysis(method1="ga", method2="soqa", weights=weight_FSP)
#     table = Visualizer.tabulate_single_problem(
#         name, ['ga', 'soqa'], ['num', 'time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
#         scores, {'num': 4, 'time': 6, 'statistic': 8, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
#     )
#     Visualizer.tabluate(table, 'so-sa-compare-{}.csv'.format(name))


