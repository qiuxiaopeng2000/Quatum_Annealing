import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer

names_FSP = ['E-Shop', 'eCos', 'uClinux']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-1', 'classic-2', 'classic-3']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

hymoo_result_folder = 'hymoo'
nsgaii_result_folder = 'nsgaii'
moqa_result_folder = 'moqa'

hysoo_result_folder = 'hysoo'
sa_result_folder = 'sa'
soqa_result_folder = 'soqa'

# compare CQHA with NSGA-II
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving

    hymoo_problem_result = ProblemResult(name, problem, hymoo_result_folder)
    nsgaii_problem_result = ProblemResult(name, problem, nsgaii_result_folder)
    moqa_problem_result = ProblemResult(name, problem, moqa_result_folder)

    hysoo_problem_reuslt = ProblemResult(name, problem, hysoo_result_folder)
    sa_problem_result = ProblemResult(name, problem, sa_result_folder)
    soqa_problem_result = ProblemResult(name, problem, soqa_result_folder)

    # ga_result = MethodResult('ga', nsgaii_problem_result.path, problem)
    # ga_result.load()
    # qa_result = MethodResult('moqa', moqa_problem_result.path, problem)
    # qa_result.load()
    hy_result = MethodResult('hymoo-{}'.format(name), hymoo_problem_result.path, problem)
    hy_result.load(evaluate=True, single_flag=False)

    # hymoo_problem_result.add(ga_result)
    # hymoo_problem_result.add(qa_result)
    hymoo_problem_result.add(hy_result)

    # compare
    scores_hy = hymoo_problem_result.average_compare(union_method='moqa', average_method='hymoo-{}'.format(name))
    table_hy = Visualizer.tabulate_single_problem(
        name, ['moqa', 'hymoo-{}'.format(name)], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_hy, 'ea-hy-compare-{}.csv'.format(name))

for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving

    hymoo_problem_result = ProblemResult(name, problem, hymoo_result_folder)
    # nsgaii_problem_result = ProblemResult(name, problem, nsgaii_result_folder)
    # moqa_problem_result = ProblemResult(name, problem, moqa_result_folder)
    #
    # hysoo_problem_reuslt = ProblemResult(name, problem, hysoo_result_folder)
    # sa_problem_result = ProblemResult(name, problem, sa_result_folder)
    # soqa_problem_result = ProblemResult(name, problem, soqa_result_folder)

    # ga_result = MethodResult('ga', nsgaii_problem_result.path, problem)
    # ga_result.load()
    # qa_result = MethodResult('moqa', moqa_problem_result.path, problem)
    # qa_result.load()
    hy_result = MethodResult('hymoo-{}'.format(name), hymoo_problem_result.path, problem)
    hy_result.load(evaluate=True, single_flag=False)

    # hymoo_problem_result.add(ga_result)
    # hymoo_problem_result.add(qa_result)
    hymoo_problem_result.add(hy_result)

    # compare
    scores_hy = hymoo_problem_result.average_compare(union_method='moqa', average_method='hymoo-{}'.format(name))
    table_hy = Visualizer.tabulate_single_problem(
        name, ['moqa', 'hymoo-{}'.format(name)], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_hy, 'ea-hy-compare-{}.csv'.format(name))

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

