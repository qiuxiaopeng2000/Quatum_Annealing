from functools import partial
from typing import Dict, List
from random import random

from dimod import BinaryQuadraticModel
from dwave.system import ReverseAdvanceComposite
from dwave.system.composites import embedding

from nen.Term import Constraint, Quadratic
from nen.Problem import QP
from nen.Result import Result
from nen.Solver.MetaSolver import SolverUtil
from nen.Solver.EmbeddingSampler import EmbeddingSampler, SampleSet


class MOQASolver:
    """ [summary] MOQASolver, stands for Multi-Objective Quantum Annealling Solver,
    it adopts random weighted sum of objectives and query on QPU for serveral times.

    Note that, the elapsed time just count qpu time, it does not include the pre/post-process.

    The Quantum Annealling Solver is implemeneted with D-Wave Leap,
    make sure the environment is configured successfully accordingly.
    """

    @staticmethod
    def solve(problem: QP, sample_times: int, num_reads: int) -> Result:
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
            # Solve in QA
            sampler = EmbeddingSampler()
            sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads)
            samplesets.append(sampleset)
            elapseds.append(elapsed)

            # # reverse anneal
            # reverse_sampler = ReverseAdvanceComposite(sampler)
            # bqm = BinaryQuadraticModel.from_qubo(qubo)
            # embedding, bqm_embedded = sampler.embed(bqm)
            # last_set = sampleset
            # # select one from last set as initial state
            # selected_state = EmbeddingSampler.select_by_energy(sampleset)[0]
            # initial_state = {u: selected_state[v] for v, chain in embedding.items() for u in chain}
            # # sample
            # r_sampleset, r_elapsed = reverse_sampler.sample(bqm,
            #                                                 num_reads=num_reads,
            #                                                 reinitialize_state=True,
            #                                                 initial_state=initial_state,
            #                                                 anneal_schedules=anneal_schedule)
            # # samplesets.append(r_sampleset)
            # # compare current set and last set
            # if EmbeddingSampler.engery_compare(last_set, r_sampleset):
            #     samplesets.append(last_set)
            # else:
            #     samplesets.append(r_sampleset)

        # put samples into result
        result = Result(problem)
        for sampleset in samplesets:
            for values in EmbeddingSampler.get_values(sampleset, problem.variables):
                solution = problem.evaluate(values)
                result.add(solution)
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

    # def reverse_solve(problem: QP, sample_times: int, num_reads: int, max_reverse_loop: int, anneal_schedule) -> Result:
    #     """solve [summary] solve qp, results are recorded in result.
    #     """
    #     # scale objectives and get the basic
    #     basic_weights = SolverUtil.scaled_weights(problem.objectives)
    #     # sample for sample_times times
    #     samplesets: List[SampleSet] = []
    #     elapseds: List[float] = []
    #     for _ in range(sample_times):
    #         # generate random weights and calculate weighted sum obejctive
    #         weights = MOQASolver.random_normalized_weights(basic_weights)
    #         wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
    #         # calculate the penalty and add constraints to objective with penalty
    #         penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
    #         objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
    #         qubo = Constraint.quadratic_to_qubo_dict(objective)
    #         # Solve in QA
    #         sampler = EmbeddingSampler()
    #         sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads)
    #         # samplesets.append(sampleset)
    #
    #         # reverse anneal
    #         reverse_sampler = ReverseAdvanceComposite(sampler)
    #         bqm = BinaryQuadraticModel.from_qubo(qubo)
    #         embedding, bqm_embedded = sampler.embed(bqm)
    #         last_set = sampleset
    #         # select one from last set as initial state
    #         selected_state = EmbeddingSampler.select_by_energy(sampleset)[0]
    #         initial_state = {u: selected_state[v] for v, chain in embedding.items() for u in chain}
    #         # sample
    #         r_sampleset, r_elapsed = reverse_sampler.sample(bqm,
    #                                                         num_reads=num_reads,
    #                                                         reinitialize_state=True,
    #                                                         initial_state=initial_state,
    #                                                         anneal_schedules=anneal_schedule)
    #         # samplesets.append(r_sampleset)
    #         # compare current set and last set
    #         if EmbeddingSampler.engery_compare(last_set, r_sampleset):
    #             samplesets.append(last_set)
    #         else:
    #             samplesets.append(r_sampleset)
    #
    #     # put samples into result
    #     result = Result(problem)
    #     for sampleset in samplesets:
    #         for values in EmbeddingSampler.get_values(sampleset, problem.variables):
    #             solution = problem.evaluate(values)
    #             result.add(solution)
    #     # add into method result
    #     result.elapsed = sum([EmbeddingSampler.get_qpu_time(sampleset) for sampleset in samplesets])
    #     for sampleset in samplesets:
    #         if 'solving info' not in result.info:
    #             result.info['solving info'] = [sampleset.info]
    #         else:
    #             result.info['solving info'].append(sampleset.info)
    #     # storage parameters
    #     result.info['sample_times'] = sample_times
    #     result.info['num_reads'] = num_reads
    #     return result

    @staticmethod
    def random_normalized_weights(basic_weights: Dict[str, float]) -> Dict[str, float]:
        """random_normalized_weights [summary] get a random weights with respect to the basic one,
        it is generated as random weights which sum is 1 and multiply with the basic weights.
        """
        random_weights = {k: random() for k in basic_weights}
        sum_weights = sum(random_weights.values())
        return {k: (random_weights[k] / sum_weights) * v for k, v in basic_weights.items()}
