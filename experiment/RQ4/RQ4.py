import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer

names_FSP = ['eCos', 'Freebsd', 'Fiasco']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

rates = [0.3, 0.5, 0.7]

# compare CQHA with NSGA-II
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hy_result_folder)

    hy_result = MethodResult('hybrid', hy_problem_result.path, problem)
    hy_result.load()
    for rate in rates:
        hy_result = MethodResult('hybrid{}'.format(rate), hy_problem_result.path, problem)
        hy_result.load()
        hy_problem_result.add(hy_result)

    # compare
    for rate in rates:
        scores_hy = hy_problem_result.average_compare(union_method='hybrid', average_method='hybrid{}'.format(rate))
        table_hy = Visualizer.tabulate_single_problem(
            name, ['hybrid', 'hybrid{}'.format(rate)], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table_hy, 'hy-{}-compare-{}.csv'.format(rate, name))

for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hy_result_folder)

    hy_result = MethodResult('hybrid', hy_problem_result.path, problem)
    hy_result.load()
    for rate in rates:
        hy_result = MethodResult('hybrid{}'.format(rate), hy_problem_result.path, problem)
        hy_result.load()
        hy_problem_result.add(hy_result)

    # compare
    for rate in rates:
        scores_hy = hy_problem_result.average_compare(union_method='hybrid', average_method='hybrid{}'.format(rate))
        table_hy = Visualizer.tabulate_single_problem(
            name, ['hybrid', 'hybrid{}'.format(rate)], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table_hy, 'hy-{}-compare-{}.csv'.format(rate, name))

'''++++++++++++++++++++++++++++++++++++++++++++++'''

# compare Hybrid with SA
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    result_folder = 'hy-sa-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    hy_result = MethodResult('hybrid', problem_result.path, problem)
    hy_result.load()
    for rate in rates:
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
        hy_result.load()
        problem_result.add(hy_result)

    problem_result.add(hy_result)

    # compare
    for rate in rates:
        scores_hy = problem_result.average_compare(union_method='hybrid', average_method='hybrid{}'.format(rate))
        table_hy = Visualizer.tabulate_single_problem(
            name, ['hybrid', 'hybrid{}'.format(rate)], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table_hy, 'hy-{}-compare-{}.csv'.format(rate, name))


for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'hy-sa-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    hy_result = MethodResult('hybrid', problem_result.path, problem)
    hy_result.load()
    for rate in rates:
        hy_result = MethodResult('hybrid{}'.format(rate), problem_result.path, problem)
        hy_result.load()
        problem_result.add(hy_result)

    problem_result.add(hy_result)

    # compare
    for rate in rates:
        scores_hy = problem_result.average_compare(union_method='hybrid', average_method='hybrid{}'.format(rate))
        table_hy = Visualizer.tabulate_single_problem(
            name, ['hybrid', 'hybrid{}'.format(rate)], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
            scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
        )
        Visualizer.tabluate(table_hy, 'hy-{}-compare-{}.csv'.format(rate, name))

