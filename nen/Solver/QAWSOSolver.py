from typing import Dict, List, Union
from jmetal.core.solution import BinarySolution
from nen.Term import Constraint, Quadratic
from nen.Problem import QP
from nen.Result import Result, NDArchive
from nen.Solver.MetaSolver import SolverUtil
from nen.Solver.EmbeddingSampler import EmbeddingSampler


class QAWSOSolver:
    """ [summary] QAWSOSolver, stands for Quantum Annealling Weighted Sum Objective Solver.

    The Quantum Annealling Solver is implemeneted with D-Wave Leap,
    make sure the environment is configured successfully accordingly.
    """
    @staticmethod
    def solve(problem: QP, weights: Dict[str, float], penalty: float, num_reads: int) -> Result:
        """solve [summary] solve single objective qp (applied wso technique), return Result.
        """
        print("start SOQA to solve {}".format(problem.name))
        # prepare wso objective
        wso = SolverUtil.weighted_sum_objective(problem.objectives, weights)
        # add constraints to objective with penalty
        objective = Constraint.quadratic_weighted_add(1, penalty, Quadratic(linear=wso), problem.constraint_sum)
        qubo = Constraint.quadratic_to_qubo_dict(objective)
        # Solve in QA
        sampler = EmbeddingSampler()
        sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads, answer_mode='raw')
        # get results
        result = Result(problem)
        if 'occurence' not in result.info:
            result.info['occurence'] = {}
        for values, occurrence in EmbeddingSampler.get_values_and_occurrence(sampleset, problem.variables):
            solution = problem.evaluate(values)
            result.wso_add(solution)
            key = NDArchive.bool_list_to_str(solution.variables[0])
            if key not in result.info['occurence']:
                result.info['occurence'][key] = str(occurrence)
            else:
                result.info['occurence'][key] = str(int(result.info['occurence'][key]) + occurrence)
        result.elapsed = elapsed
        if 'solving info' not in result.info:
            result.info['solving info'] = [sampleset.info]
        else:
            result.info['solving info'].append(sampleset.info)
        # storage parameters
        result.info['weights'] = weights
        result.info['penalty'] = penalty
        result.info['num_reads'] = num_reads
        print("end SOQA to solve")
        return result

    @staticmethod
    def best_solution(solution_list: List[BinarySolution],
                      problem: QP, weights: Dict[str, float]) -> Union[None, BinarySolution]:
        """best_solution [summary] get the best solution from the archive with certain weights.
        """
        best_value: float = float('inf')
        best_solution: Union[None, BinarySolution] = None
        w = [weights[s] for s in problem.objectives_order]
        for solution in solution_list:
            v = sum([solution.objectives[i] * w[i] for i in range(problem.objectives_num)])
            if best_value > v:
                best_value = v
                best_solution = solution
        return best_solution
