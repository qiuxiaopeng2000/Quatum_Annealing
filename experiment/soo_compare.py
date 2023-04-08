import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from nen import Problem, ProblemResult, MethodResult, Visualizer


names_FSP = ['BerkeleyDB', 'ERS', 'WebPortal', 'Drupal', 'Amazon', 'E-Shop']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['rp', 'ms', 'Baan', 'classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}


# compare SOQA with SA
for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'so-sa_-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    sa_result = MethodResult('sa_', problem_result.path, problem)
    sa_result.load()
    ex_result = MethodResult('soqp', problem_result.path, problem)
    ex_result.load()

    problem_result.add(sa_result)
    problem_result.add(ex_result)

    # compare
    scores = problem_result.statistical_analysis(method1="sa_", method2="soqp", weights=weight_FSP)
    table = Visualizer.tabulate_single_problem(
        name, ['sa_', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'so-sa_-compare-{}.csv'.format(name))

for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'so-sa_-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    sa_result = MethodResult('sa_', problem_result.path, problem)
    sa_result.load()
    ex_result = MethodResult('soqp', problem_result.path, problem)
    ex_result.load()

    problem_result.add(sa_result)
    problem_result.add(ex_result)

    # compare
    scores = problem_result.statistical_analysis(method1="sa_", method2="soqp", weights=weight_FSP)
    table = Visualizer.tabulate_single_problem(
        name, ['sa_', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'so-sa_-compare-{}.csv'.format(name))


# compare SOQA with Hybrid
for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'hy-soqa_old-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    sa_result = MethodResult('soqa_old', problem_result.path, problem)
    sa_result.load()
    ex_result = MethodResult('hybrid', problem_result.path, problem)
    ex_result.load()

    problem_result.add(sa_result)
    problem_result.add(ex_result)

    # compare
    scores = problem_result.statistical_analysis(method1="soqa_old", method2="hybrid", weights=weight_FSP)
    table = Visualizer.tabulate_single_problem(
        name, ['sa_', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'so-sa_-compare-{}.csv'.format(name))

for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    result_folder = 'hy-soqa_old-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    sa_result = MethodResult('soqa_old', problem_result.path, problem)
    sa_result.load()
    ex_result = MethodResult('hybrid', problem_result.path, problem)
    ex_result.load()

    problem_result.add(sa_result)
    problem_result.add(ex_result)

    # compare
    scores = problem_result.statistical_analysis(method1="soqa_old", method2="hybrid", weights=weight_FSP)
    table = Visualizer.tabulate_single_problem(
        name, ['sa_', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table, 'hy-soqa_old-compare-{}.csv'.format(name))
