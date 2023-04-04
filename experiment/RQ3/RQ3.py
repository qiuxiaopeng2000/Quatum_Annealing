import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer

names_FSP = ['E-shop', 'eCos', 'Freebsd']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

result_folder = 'hymoo'

# compare CQHA with NSGA-II
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving

    problem_result = ProblemResult(name, problem, result_folder)

    hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hy_result_folder)

    ga_result = MethodResult('ga', problem_result.path, problem)
    ga_result.load()
    qa_result = MethodResult('moqa', problem_result.path, problem)
    qa_result.load()
    hy_result = MethodResult('hybrid', hy_problem_result.path, problem)
    hy_result.load()

    problem_result.add(ga_result)
    problem_result.add(qa_result)
    problem_result.add(hy_result)

    # compare
    scores_hy = problem_result.average_compare(union_method='moqa', average_method='hybrid')
    table_hy = Visualizer.tabulate_single_problem(
        name, ['moqa', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_hy, 'ea-hy-compare-{}.csv'.format(name))

for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hy_result_folder)

    ga_result = MethodResult('ga', hy_problem_result.path, problem)
    ga_result.load()
    hy_result = MethodResult('hybrid', hy_problem_result.path, problem)
    hy_result.load()

    hy_problem_result.add(ga_result)
    hy_problem_result.add(hy_result)

    # compare
    scores_hybrid = hy_problem_result.average_compare(union_method='hybrid', average_method='ga')
    table_hybrid = Visualizer.tabulate_single_problem(
        name, ['hybrid', 'ga'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_hybrid, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_hybrid, 'hybrid-ga-compare-{}.csv'.format(name))

'''++++++++++++++++++++++++++++++++++++++++++++++'''

# compare Hybrid with SA
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    result_folder = 'hy-sa-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    sa_result = MethodResult('sa', problem_result.path, problem)
    sa_result.load()
    hy_result = MethodResult('hybrid', problem_result.path, problem)
    hy_result.load()

    problem_result.add(sa_result)
    problem_result.add(hy_result)

    # compare
    scores = problem_result.statistical_analysis(method1="hybrid", method2="sa", weights=weight_NRP)
    table = Visualizer.tabulate_single_problem(
        name, ['hybrid', 'sa'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'hybrid-sa-compare-{}.csv'.format(name))


for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'hy-sa-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    sa_result = MethodResult('sa', problem_result.path, problem)
    sa_result.load()
    hy_result = MethodResult('hybrid', problem_result.path, problem)
    hy_result.load()

    problem_result.add(sa_result)
    problem_result.add(hy_result)

    # compare
    scores = problem_result.statistical_analysis(method1="hybrid", method2="sa", weights=weight_FSP)
    table = Visualizer.tabulate_single_problem(
        name, ['hybrid', 'sa'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'hybrid-sa-compare-{}.csv'.format(name))

