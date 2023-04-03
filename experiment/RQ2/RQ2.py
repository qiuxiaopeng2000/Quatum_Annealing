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


# compare MOQA with NSGA-II
for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'QA-GA-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    ga_result = MethodResult('ga', problem_result.path, problem)
    ga_result.load()
    qa_result = MethodResult('moqa', problem_result.path, problem)

    problem_result.add(ga_result)
    problem_result.add(qa_result)

    # compare
    scores_ga = problem_result.average_compare(union_method='moqa', average_method='ga')
    table_ga = Visualizer.tabulate_single_problem(
        name, ['moqa', 'ga'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_ga, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_ga, 'moqa-ga-compare-{}.csv'.format(name))


for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    result_folder = 'QA-GA-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    ga_result = MethodResult('ga', problem_result.path, problem)
    ga_result.load()
    qa_result = MethodResult('moqa', problem_result.path, problem)
    qa_result.load()

    problem_result.add(ga_result)

    # compare
    scores_ga = problem_result.average_compare(union_method='moqa', average_method='ga')
    table_ga = Visualizer.tabulate_single_problem(
        name, ['moqa', 'ga'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_ga, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_ga, 'moqa-ga-compare-{}.csv'.format(name))
