from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination

from nen.Problem import PymooProblem, QP
from nen.Problem import Problem
from nen.Result import Result


class GASolver:
    """ [summary] GASolver, stands for Multi-Objective Genetic Algorithm Solver,
        it adopts random weighted sum of objectives and use Genetic Algorithm to solve problem for several times.

        The Genetic Algorithm Solver is implemented with 'pymoo' python package,
        make sure the environment is configured successfully accordingly.
        """
    @staticmethod
    def solve(problem: Problem, populationSize: int, maxEvaluations: int,
              seed: int, crossoverProbability: float, mutationProbability: int,
              verbose: bool = False, iterations: int = 1) -> Result:
        """
        seed : integer
            The random seed to be used.
        verbose : bool
            Whether output should be printed or not.
        populationSize : integer
            Equivalent to 'num_reads' in QA
        Returns
        --------
        res.X: Design space values are
        res.F: Objective spaces values
        res.G: Constraint values
        res.CV: Aggregated constraint violation
        res.algorithm: Algorithm object which has been iterated over
        res.opt: The solutions as a Population-Pareto object.
                If the least feasible solution should be returned when no feasible solution was found,
                the flag return_least_infeasible can be enabled
        res.pop: The final Population. The values from the final population can be extracted by using the 'get' method.
                example: res.pop.get('X')
        res.history: The history of the algorithm. (only if save_history has been enabled during the algorithm initialization)
        res.time: The time required to run the algorithm
        """
        print("{} start Genetic Algorithm to solve multi-objective problem!!!".format(problem.name))
        result = Result(problem)
        termination = DefaultMultiObjectiveTermination(
            n_max_evals=maxEvaluations
        )
        pro = PymooProblem(problem)
        alg = NSGA2(pop_size=populationSize,
                    # n_offsprings=10,
                    sampling=BinaryRandomSampling(),
                    # crossover=SBX(prob=crossoverProbability, eta=15),
                    crossover=TwoPointCrossover(),
                    # mutation=PolynomialMutation(eta=20, prob=mutationProbability),
                    mutation=BitflipMutation(),
                    eliminate_duplicates=True)

        for _ in range(iterations):
            res = minimize(pro, alg, termination, seed=seed, verbose=verbose)
            # return_least_infeasible=True

            result.elapsed += res.exec_time
            for sol in res.pop:
                val = list(sol.X.flatten())
                values = problem.convert_to_BinarySolution(val)
                solution = problem.evaluate(values)
                result.add(solution)
        result.iterations = iterations
        result.total_num_anneals = populationSize * iterations
        print("Genetic Algorithm end!!!")
        return result

