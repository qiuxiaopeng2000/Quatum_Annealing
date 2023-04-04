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
    result_folder = 'QA-GA-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    ea_result_folder = 'EA-GA-{}'.format(name)
    ea_problem_result = ProblemResult(name, problem, ea_result_folder)
    hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hy_result_folder)

    ga_result = MethodResult('ga', problem_result.path, problem)
    ga_result.load()
    qa_result = MethodResult('moqp', problem_result.path, problem)
    qa_result.load()
    ea_result = MethodResult('ea', ea_problem_result.path, problem)
    ea_result.load()
    hy_result = MethodResult('hybrid', hy_problem_result.path, problem)
    hy_result.load()

    problem_result.add(ga_result)
    problem_result.add(qa_result)
    problem_result.add(ea_result)
    problem_result.add(hy_result)

    # compare
    scores_ga = problem_result.union_average_compare(union_method='ea', average_method='ga')
    table_ga = Visualizer.tabulate_single_problem(
        name, ['ea', 'ga'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_ga, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    scores_moqp = problem_result.union_average_compare(union_method='ea', average_method='moqp')
    table_moqp = Visualizer.tabulate_single_problem(
        name, ['ea', 'moqp'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_moqp, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    scores_hy = problem_result.union_average_compare(union_method='ea', average_method='hybrid')
    table_hy = Visualizer.tabulate_single_problem(
        name, ['ea', 'hybrid'], ['time', 'statistic', 'p_value', 'mean', 'std', 'max', 'min'],
        scores_hy, {'time': 6, 'statistic': 12, 'p_value': 18, 'mean': 4, 'std': 4, 'max': 4, 'min': 4}
    )
    Visualizer.tabluate(table_ga, 'ea-ga-compare-{}.csv'.format(name))
    Visualizer.tabluate(table_moqp, 'ea-moqa-compare-{}.csv'.format(name))
    Visualizer.tabluate(table_hy, 'ea-hy-compare-{}.csv'.format(name))

for name in names_NRP:
    problem = Problem(name)
    problem.vectorize(order_NRP)

    # prepare the problem result folder before solving
    result_folder = 'QA-GA-{}'.format(name)
    problem_result = ProblemResult(name, problem, result_folder)

    ea_result_folder = 'EA-GA-{}'.format(name)
    ea_problem_result = ProblemResult(name, problem, ea_result_folder)
    hy_result_folder = 'HY-GA-{}'.format(name)
    hy_problem_result = ProblemResult(name, problem, hy_result_folder)

    ga_result = MethodResult('ga', problem_result.path, problem)
    ga_result.load()
    qa_result = MethodResult('moqp', problem_result.path, problem)
    qa_result.load()
    ea_result = MethodResult('ea', ea_problem_result.path, problem)
    ea_result.load()
    hy_result = MethodResult('hybrid', hy_problem_result.path, problem)
    hy_result.load()

    problem_result.add(ga_result)
    problem_result.add(qa_result)
    problem_result.add(ea_result)
    problem_result.add(hy_result)

    # compare
    scores_ga = problem_result.union_average_compare(union_method='ea', average_method='ga')
    table_ga = Visualizer.tabulate_single_problem(
        name, ['ea', 'ga'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing'],
        scores_ga, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4}
    )
    scores_moqp = problem_result.union_average_compare(union_method='ea', average_method='moqp')
    table_moqp = Visualizer.tabulate_single_problem(
        name, ['ea', 'moqa'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing'],
        scores_moqp, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4}
    )
    scores_hy = problem_result.union_average_compare(union_method='ea', average_method='hybrid')
    table_hy = Visualizer.tabulate_single_problem(
        name, ['ea', 'hybeid'], ['elapsed time', 'found', 'front', 'igd', 'hv', 'spacing'],
        scores_hy, {'elapsed time': 4, 'found': 5, 'front': 4, 'igd': 4, 'hv': 4, 'spacing': 4}
    )
    Visualizer.tabluate(table_ga, 'ea-ga-compare-{}.csv'.format(name))
    Visualizer.tabluate(table_moqp, 'ea-moqa-compare-{}.csv'.format(name))
    Visualizer.tabluate(table_hy, 'ea-hy-compare-{}.csv'.format(name))

