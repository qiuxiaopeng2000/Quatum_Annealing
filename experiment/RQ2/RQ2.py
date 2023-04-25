import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer

# names_FSP = ['ERS', 'WebPortal', 'Drupal']
names_FSP = ['ERS', 'WebPortal', 'Drupal']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['rp', 'ms', 'Baan']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

nsgaii_result_folder = 'nsgaii'
moqa_result_folder = 'moqa'

# compare MOQA with NSGA-II
for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    nsgaii_problem_result = ProblemResult(name, problem, nsgaii_result_folder)
    moqa_problem_result = ProblemResult(name, problem, moqa_result_folder)

    ga_result = MethodResult('nsgaii', nsgaii_problem_result.path, problem)
    ga_result.load(evaluate=True)
    qa_result = MethodResult('moqa', moqa_problem_result.path, problem)
    qa_result.load(evaluate=True)

    moqa_problem_result.add(ga_result)
    moqa_problem_result.add(qa_result)

    # compare
    scores_ga = moqa_problem_result.average_compare(union_method='moqa', average_method='nsgaii')
    table_ga = Visualizer.tabulate_single_problem(
        name, ['moqa', 'nsgaii'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores_ga, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4, 'tts': 4}
    )
    Visualizer.tabluate(table_ga, 'moqa-nsgaii-compare-{}.csv'.format(name))


for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    # prepare the problem result folder before solving
    nsgaii_problem_result = ProblemResult(name, problem, nsgaii_result_folder)
    moqa_problem_result = ProblemResult(name, problem, moqa_result_folder)

    ga_result = MethodResult('nsgaii', nsgaii_problem_result.path, problem)
    ga_result.load(evaluate=True)
    qa_result = MethodResult('moqa', moqa_problem_result.path, problem)
    qa_result.load(evaluate=True)

    moqa_problem_result.add(ga_result)
    moqa_problem_result.add(qa_result)

    # compare
    scores_ga = moqa_problem_result.average_compare(union_method='moqa', average_method='nsgaii')
    table_ga = Visualizer.tabulate_single_problem(
        name, ['moqa', 'nsgaii'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores_ga, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4, 'tts': 4}
    )
    Visualizer.tabluate(table_ga, 'moqa-nsgaii-compare-{}.csv'.format(name))