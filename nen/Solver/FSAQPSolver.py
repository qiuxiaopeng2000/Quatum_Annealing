from typing import Callable, Dict, List, Tuple
from nen.Problem import QP
from nen.Result import Result
from nen.Solver.EmbeddingSampler import EmbeddingSampler
from nen.Term import Quadratic, Constraint
from nen.Solver.MetaSolver import SolverUtil
from sko.SA import SA


class FSAQPSolver:
    """ [summary] Fast Simulated Annealing Quadratic Programming Solver.
    """
    @staticmethod
    def quadratic_to_fitness(H: Quadratic) -> Tuple[Callable[[List[bool]], float], List[str]]:
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
            for k, v in H.linear.items():
                if bool(x[variables_map[k]]):
                    fitness += v
            for (k1, k2), v in H.quadratic.items():
                if bool(x[variables_map[k1]]) and bool(x[variables_map[k2]]):
                    fitness += v
            return fitness

        return F, variables

    @staticmethod
    def solve(problem: QP, weights: Dict[str, float],
              t_max: float, t_min: float, L: int = 300, max_stay: int = 150) -> Result:
        # check arguments
        assert t_min < t_max
        # modelling
        wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
        penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
        H = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
        # sample with sko.SA (default = FSA)
        fitness, variables = FSAQPSolver.quadratic_to_fitness(H)
        start = SolverUtil.time()
        sampler = SA(func=fitness, T_max=t_max, T_min=t_min, L=L, max_stay_counter=max_stay)
        best_x, _ = sampler.run()
        end = SolverUtil.time()
        # restore the result
        values: Dict[str, bool] = {}
        for ind, val in enumerate(best_x):
            values[variables[ind]] = bool(val)
        result = Result(problem)
        result.add(problem.evaluate(values))
        result.elapsed = end - start
        return result
