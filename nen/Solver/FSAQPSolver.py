from typing import Dict, List

import numpy as np

from nen.Problem import QP
from nen.Result import Result
from nen.Solver.EmbeddingSampler import EmbeddingSampler
from nen.Term import Quadratic, Constraint
from nen.Solver.MetaSolver import SolverUtil
from sko.SA import SA
from nen.Solver.SASolver import SASolver


class FSAQPSolver:
    """ [summary] Fast Simulated Annealing Quadratic Programming Solver.
    """

    @staticmethod
    def solve(problem: QP, weights: Dict[str, float], t_max: float, t_min: float,
              L: int = 300, max_stay: int = 150, sample_times: int = 1, num_reads: int = 1000) -> Result:
        print("start Simulated Annealing to solve single-problem!!!")
        result = Result(problem)
        for _ in range(sample_times):
            res = FSAQPSolver.solve_once(problem, weights, t_max, t_min, L, max_stay, num_reads)
            result.solution_list.append(res.single)
            result.elapsed += res.elapsed
        print("Simulated Annealing end!!!")
        return result

    @staticmethod
    def quadratic_to_fitness(H: Quadratic):
        """quadratic_to_fitness [summary] convert Quadratic function to fitness function,
        return fitness function and variable order.
        """
        # prepare the variable list and dict
        variables: List[str] = []
        variables_map: Dict[str, int] = {}
        # indexize variables
        for k in H.linear:
            if k not in variables_map:
                variables_map[k] = len(variables)
                variables.append(k)
        for (k1, k2) in H.quadratic:
            if k1 not in variables_map:
                variables_map[k1] = len(variables)
                variables.append(k1)
            if k2 not in variables_map:
                variables_map[k2] = len(variables)
                variables.append(k2)

        def F(x: List[bool]) -> float:
            fitness: float = H.constant
            x = np.array(x).flatten().tolist()
            for k, v in H.linear.items():
                # temp = x[variables_map[k]]
                if bool(x[variables_map[k]]):
                    fitness += v
            for (k1, k2), v in H.quadratic.items():
                if bool(x[variables_map[k1]]) and bool(x[variables_map[k2]]):
                    fitness += v
            return fitness

        return F, variables

    @staticmethod
    def solve_once(problem: QP, weights: Dict[str, float], t_max: float, t_min: float,
                   L: int = 300, max_stay: int = 150, num_reads: int = 1000) -> Result:
        """
        t_max: initial temperature
        t_min: end temperature
        L: num of iteration under every temperature
        max_stay: stop if best_y stay unchanged over max_stay_counter times
        """
        # check arguments
        assert t_min < t_max
        # modelling
        wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
        penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
        H = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
        # sample with sko.SA (default = FSA)
        fitness, variables = FSAQPSolver.quadratic_to_fitness(H)
        start = SolverUtil.time()
        x0 = SASolver.randomSolution(problem).variables
        sampler = SA(func=fitness, T_max=t_max, T_min=t_min, L=L, max_stay_counter=max_stay, x0=x0, num_reads=num_reads)
        best_x, _ = sampler.run()
        end = SolverUtil.time()
        # restore the result
        # shape = best_x.shape
        # print(shape)
        best_x = np.array(best_x).flatten().tolist()
        values: Dict[str, bool] = {}
        for ind, val in enumerate(best_x):
            values[variables[ind]] = bool(val)
        result = Result(problem)
        result.add(problem.evaluate(values))
        result.elapsed = end - start
        return result

