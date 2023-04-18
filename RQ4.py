import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from nen import Problem, ProblemResult, MethodResult, Visualizer

names_FSP = ['eCos']
order_FSP = ['COST', 'USED_BEFORE', 'DEFECTS', 'DESELECTED']
weight_FSP = {'COST': 1 / 4, 'USED_BEFORE': 1 / 4, 'DEFECTS': 1 / 4, 'DESELECTED': 1 / 4}

names_NRP = ['classic-2']
order_NRP = ['cost', 'revenue']
weight_NRP = {'cost': 1 / 2, 'revenue': 1 / 2}

rates = [0.3, 0.5, 0.7, 0.9]

hymoo_result_folder = 'hymoo'
hysoo_result_folder = 'hysoo'

# compare CQHA with NSGA-II
for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    # hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hymoo_result_folder)

    hy_result = MethodResult('hymoo', hy_problem_result.path, problem)
    hy_result.load()
    hy_problem_result.add(hy_result)
    methods = []
    for rate in rates:
        methods.append('hybrid{}'.format(rate))
    for method in methods:
        hy_result = MethodResult(method, hy_problem_result.path, problem)
        hy_result.load()
        hy_problem_result.add(hy_result)
    methods.append('hymoo')

    # compare
    scores_hy = hy_problem_result.average_list_compare(methods=methods)
    table_hy = Visualizer.tabulate_single_problem(
        name, [method for method in methods], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores_hy, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4, 'tts': 4}
    )
    Visualizer.tabluate(table_hy, 'hy-moo-{}-compare.csv'.format( name))

for name in names_FSP:
    problem = Problem(name)
    problem.vectorize(order_FSP)

    # prepare the problem result folder before solving
    # hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hymoo_result_folder)

    hy_result = MethodResult('hymoo', hy_problem_result.path, problem)
    hy_result.load()
    hy_problem_result.add(hy_result)
    methods = []
    for rate in rates:
        methods.append('hybrid{}'.format(rate))
    for method in methods:
        hy_result = MethodResult(method, hy_problem_result.path, problem)
        hy_result.load()
        hy_problem_result.add(hy_result)
    methods.append('hymoo')
    # compare
    scores_hy = hy_problem_result.average_list_compare(methods=methods)
    table_hy = Visualizer.tabulate_single_problem(
        name, [method for method in methods], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing', 'tts'],
        scores_hy, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4, 'tts': 4}
    )
    Visualizer.tabluate(table_hy, 'hy-moo-{}-compare.csv'.format(name))

'''++++++++++++++++++++++++++++++++++++++++++++++'''

# compare Hybrid with SA
# for name in names_NRP:
#     problem = Problem(name)
#     problem.vectorize(order_NRP)

#     # prepare the problem result folder before solving
#     # hy_result_folder = 'HY-GA-{}'.format(name)
#     hy_problem_result = ProblemResult(name, problem, hysoo_result_folder)

#     hy_result = MethodResult('hysoo', hy_problem_result.path, problem)
#     hy_result.load(single_flag=True)
#     hy_problem_result.add(hy_result)
#     methods = []
#     for rate in rates:
#         methods.append('hybrid{}'.format(rate))
#     for method in methods:
#         hy_result = MethodResult(method, hy_problem_result.path, problem)
#         hy_result.load()
#         hy_problem_result.add(hy_result)
#     methods.append('hysoo')

#     # compare
#     scores_hy = hy_problem_result.statistical_list_analysis(methods=methods, weights=weight_NRP)
#     table_hy = Visualizer.tabulate_single_problem(
#         name, [method for method in methods], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
#         scores_hy, {'time': 4, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
#     )
#     Visualizer.tabluate(table_hy, 'hy-soo-{}-compare.csv'.format(name))

# for name in names_FSP:
#     problem = Problem(name)
#     problem.vectorize(order_FSP)

#     # prepare the problem result folder before solving
#     # hy_result_folder = 'HY-GA-{}'.format(name)
#     hy_problem_result = ProblemResult(name, problem, hysoo_result_folder)

#     hy_result = MethodResult('hysoo', hy_problem_result.path, problem)
#     hy_result.load(single_flag=True)
#     hy_problem_result.add(hy_result)
#     methods = []
#     for rate in rates:
#         methods.append('hybrid{}'.format(rate))
#     for method in methods:
#         hy_result = MethodResult(method, hy_problem_result.path, problem)
#         hy_result.load()
#         hy_problem_result.add(hy_result)
#     methods.append('hysoo')
#     # compare
#     scores_hy = hy_problem_result.statistical_list_analysis(methods=methods, weights=weight_FSP)
#     table_hy = Visualizer.tabulate_single_problem(
#         name, [method for method in methods], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
#         scores_hy, {'time': 4, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
#     )
#     Visualizer.tabluate(table_hy, 'hy-soo-compare-{}.csv'.format(name))
