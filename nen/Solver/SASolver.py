from typing import Dict, List
import random
from math import exp
from datetime import datetime
from jmetal.core.solution import BinarySolution
from nen.Problem import Problem
from nen.Result import Result


class SASolver:
    """ [summary] Simulated Annealing Solver.
    """
    @staticmethod
    def randomSolution(problem: Problem) -> BinarySolution:
        """randomSolution [summary] generate a random solution.
        """
        random.seed(datetime.now())
        # random variables
        variables = []
        for _ in range(problem.variables_num):
            variables.append(bool(random.randint(0, 1)))
        solution = problem._empty_solution()
        solution.variables = [variables]
        # evaluate solution
        solution = problem.evaluate_solution(solution)
        while solution.constraints[0] > 0:  # For problems that are not easy to solve, this operator will be very time-consuming.
            # random variables
            variables = []
            for _ in range(problem.variables_num):
                variables.append(bool(random.randint(0, 1)))
            solution = problem._empty_solution()
            solution.variables = [variables]
            # evaluate solution
            solution = problem.evaluate_solution(solution)
        return solution

    @staticmethod
    def randomNeighbor(solution: BinarySolution, problem: Problem) -> BinarySolution:
        """randomNeighbor [summary] random flip a variable and get a neighbour solution.
        """
        position = random.randint(0, len(solution.variables[0]) - 1)
        solution.variables[0][position] = not solution.variables[0][position]
        return problem.evaluate_solution(solution)

    @staticmethod
    def fitness(solution: BinarySolution, weights_list: List[float]) -> float:
        """fitness [summary] give the fitness according the weights.
        """
        f = 0.0
        for ind, obj in enumerate(solution.objectives):
            f += (weights_list[ind] * obj)
        return f

    @staticmethod
    def compare(s1: BinarySolution, s2: BinarySolution, weights_list: List[float]) -> float:
        """compare [summary] return f(s1) - f(s2), constrains are more important.
        """
        if s1.constraints[0] < s2.constraints[0]:
            return float('-inf')
        elif s1.constraints[0] > s2.constraints[0]:
            return float('inf')
        else:
            return SASolver.fitness(s1, weights_list) - SASolver.fitness(s2, weights_list)

    @staticmethod
    def solve(problem: Problem, weights: Dict[str, float],
              t_max: float, t_min: float, alpha: float) -> Result:
        """ [summary] solve weighted sum objective with given weights, return a single result.
            t from t_max to t_min, updates with t = t * alpha.
        """
        # check arguments
        assert t_min < t_max
        assert 0 <= alpha <= 1
        # prepare weights list
        w = [weights[obj] for obj in problem.objectives_order]
        # annealing
        s = SASolver.randomSolution(problem)
        t = t_max
        while t > t_min:
            sn = SASolver.randomNeighbor(s, problem)
            d = SASolver.compare(sn, s, w)
            if (d <= 0) or (random.random() < exp((-d) / t)):
                s = sn
            t *= alpha
        # return result
        result = Result(problem)
        result.add(s)
        return result
