from functools import partial
from typing import Dict, List
from random import random

from dimod import BinaryQuadraticModel
from dwave.system import ReverseAdvanceComposite, LeapHybridBQMSampler
from dwave.system.composites import embedding

from nen.Solver import MOQASolver
from nen.Term import Constraint, Quadratic
from nen.Problem import QP
from nen.Result import Result, NDArchive
from nen.Solver.MetaSolver import SolverUtil
from nen.Solver.EmbeddingSampler import EmbeddingSampler, SampleSet


class HybridSolver:
    """ [summary] HybridSolver, stands for Multi-Objective Quantum Annealling with HybridSolver,
    hybrid—quantum-classical hybrid; typically one or more classical algorithms run on the problem
    while outsourcing to a quantum processing unit (QPU) parts of the problem where it benefits most.

    The Quantum Annealling Solver is implemeneted with D-Wave Leap,
    make sure the environment is configured successfully accordingly.
    """

    @staticmethod
    def solve(problem: QP, sample_times: int, num_reads: int, is_single: bool) -> Result:
        """solve [summary] solve qp, results are recorded in result.
        """
        # scale objectives and get the basic
        basic_weights = SolverUtil.scaled_weights(problem.objectives)
        # sample for sample_times times
        samplesets: List[SampleSet] = []
        elapseds: List[float] = []
        for _ in range(sample_times):
            # generate random weights and calculate weighted sum obejctive
            weights = MOQASolver.random_normalized_weights(basic_weights)
            wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
            # calculate the penalty and add constraints to objective with penalty
            penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
            objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
            qubo = Constraint.quadratic_to_qubo_dict(objective)
            # Solve in Hybrid-QA
            sampler = LeapHybridBQMSampler()
            sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads)
            samplesets.append(sampleset)
            elapseds.append(elapsed)
        # put samples into result
        result = Result(problem)
        if not is_single:
            for sampleset in samplesets:
                for values in EmbeddingSampler.get_values(sampleset, problem.variables):
                    solution = problem.evaluate(values)
                    result.add(solution)
        else:
            for sampleset in samplesets:
                for values in EmbeddingSampler.get_values(sampleset, problem.variables):
                    solution = problem.wso_evaluate(values)
                    result.wso_add(solution)
        # add into method result
        result.elapsed = sum(elapseds)
        for sampleset in samplesets:
            if 'solving info' not in result.info:
                result.info['solving info'] = [sampleset.info]
            else:
                result.info['solving info'].append(sampleset.info)
        # storage parameters
        result.info['sample_times'] = sample_times
        result.info['num_reads'] = num_reads
        return result

    def single_solve(problem: QP, weights: Dict[str, float], penalty: float, num_reads: int) -> Result:
        """solve [summary] solve single objective qp (applied wso technique), return Result.
        """
        # prepare wso objective
        wso = SolverUtil.weighted_sum_objective(problem.objectives, weights)
        # add constraints to objective with penalty
        objective = Constraint.quadratic_weighted_add(1, penalty, Quadratic(linear=wso), problem.constraint_sum)
        qubo = Constraint.quadratic_to_qubo_dict(objective)
        # Solve in QA
        sampler = LeapHybridBQMSampler()
        sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads)
        # get results
        result = Result(problem)
        if 'occurence' not in result.info:
            result.info['occurence'] = {}
        for values in EmbeddingSampler.get_values(sampleset, problem.variables):
            solution = problem.wso_evaluate(values, weights)
            result.wso_add(solution)
        result.elapsed = elapsed
        if 'solving info' not in result.info:
            result.info['solving info'] = [sampleset.info]
        else:
            result.info['solving info'].append(sampleset.info)
        # storage parameters
        result.info['weights'] = weights
        result.info['penalty'] = penalty
        result.info['num_reads'] = num_reads
        return result
