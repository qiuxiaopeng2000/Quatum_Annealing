from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.problems.functional import FunctionalProblem
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination

from nen.Problem import PymooProblem
from nen.Problem import Problem
from nen.Result import Result


class GASolver:

    @staticmethod
    def solve(problem: Problem, populationSize: int, maxEvaluations: int, iterations: int,
              seed: int, crossoverProbability: float, mutationProbability: int,
              verbose: bool = False):
        """
        seed : integer
            The random seed to be used.
        verbose : bool
            Whether output should be printed or not.
        """
        termination = DefaultMultiObjectiveTermination(
            xtol=1e-8,
            cvtol=1e-6,
            ftol=0.0025,
            period=30,
            n_max_gen=iterations,
            n_max_evals=maxEvaluations
        )
        pro = PymooProblem(problem)
        alg = NSGA2(pop_size=populationSize,
                    n_offsprings=10,
                    sampling=FloatRandomSampling(),
                    crossover=crossoverProbability,
                    mutation=mutationProbability,
                    eliminate_duplicates=True)
        res = minimize(pro, alg, termination, seed=seed, verbose=verbose)
        result = Result(problem)
        result.elapsed = res.exec_time
        print(res.X)
        result.add(res.X)

