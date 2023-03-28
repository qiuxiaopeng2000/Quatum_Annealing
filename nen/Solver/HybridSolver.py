import random
from typing import Dict, List, Tuple

import numpy as np
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler
# from dwave.system import DWaveSampler
from hybrid import State, min_sample, EnergyImpactDecomposer, SplatComposer
from jmetal.core.solution import BinarySolution

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination

from nen.Solver import MOQASolver, SOQA
from nen.Solver.FSAQPSolver import FSAQPSolver
from nen.Solver.SA import SAFast
from nen.Term import Constraint, Quadratic
from nen.Problem import QP, PymooProblem
from nen.Result import Result
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
    def solve(problem: QP, num_reads: int, seed: float, sub_size: int, maxEvaluations: int, sample_times: int = 1) -> Result:
        """solve [summary] solve multi-objective qp, results are recorded in result.
        """
        print("{} start Hybrid Solver to solve multi-objective problem!!!".format(problem.name))
        # scale objectives and get the basic
        basic_weights = SolverUtil.scaled_weights(problem.objectives)
        # sample for sample_times times
        samplesets: List[SampleSet] = []
        elapseds: List[float] = []
        solution_list: List[BinarySolution] = []
        for _ in range(sample_times):
            solution_: List[BinarySolution] = []
            # generate random weights and calculate weighted sum obejctive
            weights = MOQASolver.random_normalized_weights(basic_weights)
            wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
            # calculate the penalty and add constraints to objective with penalty
            penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
            objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
            qubo = Constraint.quadratic_to_qubo_dict(objective)
            # convert qubo to bqm
            bqm = BinaryQuadraticModel.from_qubo(qubo)

            start = SolverUtil.time()
            '''Decomposer'''
            s1 = SolverUtil.time()
            states = HybridSolver.Decomposer(sub_size=sub_size, bqm=bqm, variables_num=bqm.num_variables)
            e1 = SolverUtil.time()
            '''Sampler'''
            subsamplesets, runtime = HybridSolver.Sampler(states=states, num_reads=num_reads)
            '''Composer'''
            s2 = SolverUtil.time()
            HybridSolver.Composer(problem=problem, subsamplesets=subsamplesets, num_reads=num_reads,
                                  solution_list=solution_)
            e2 = SolverUtil.time()
            end = SolverUtil.time()
            '''NSGA-II'''
            t = end - start
            elapseds.append(e1 - s1 + e2 - s2 + runtime)
            HybridSolver.NSGAII(populationSize=num_reads, maxEvaluations=maxEvaluations, problem=problem, seed=seed,
                                time=t, solution_list=solution_)
            '''Selection'''
            solution_.sort(key=lambda x: (x.constraints[0], np.dot(x.objectives, list(weights.values()))))
            # solution_.sort(key=lambda x: np.dot(x.objectives, list(weights.values())))
            solution_list += solution_

        # put samples into result
        result = Result(problem)
        for solution in solution_list:
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
        result.iterations = sample_times
        result.total_num_anneals = num_reads * sample_times
        print("{} Hybrid Solver end!!!".format(problem.name))
        return result

    @staticmethod
    def single_solve(problem: QP, weights: Dict[str, float], num_reads: int, sub_size: int, t_max: float,
                     t_min: float, L: int, max_stay: int, sample_times: int) -> Result:
        print("{} start Hybrid Solver to solve single-objective problem!!!".format(problem.name))
        # sample for sample_times times
        samplesets: List[SampleSet] = []
        elapseds: List[float] = []
        solution_list: List[BinarySolution] = []
        for _ in range(sample_times):
            solution_: List[BinarySolution] = []
            # generate random weights and calculate weighted sum obejctive
            wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
            # calculate the penalty and add constraints to objective with penalty
            penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
            objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
            qubo = Constraint.quadratic_to_qubo_dict(objective)
            # convert qubo to bqm
            bqm = BinaryQuadraticModel.from_qubo(qubo)

            start1 = SolverUtil.time()
            '''Decomposer'''
            s1 = SolverUtil.time()
            states = HybridSolver.Decomposer(sub_size=sub_size, bqm=bqm, variables_num=problem.variables_num)
            e1 = SolverUtil.time()
            '''Sampler'''
            subsamplesets, runtime = HybridSolver.Sampler(states=states, num_reads=num_reads)
            '''Composer'''
            s2 = SolverUtil.time()
            HybridSolver.Composer(problem=problem, subsamplesets=subsamplesets, num_reads=num_reads, solution_list=solution_)
            e2 = SolverUtil.time()
            end1 = SolverUtil.time()
            '''SA'''
            H = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
            t = end1 - start1
            elapseds.append(e1 - s1 + e2 - s2 + runtime)
            HybridSolver.SA(H=H, t_max=t_max, t_min=t_min, L=L, max_stay=max_stay, num_reads=num_reads,
                            time=t, problem=problem, solution_list=solution_)
            '''Selection'''
            solution_.sort(key=lambda x: x.objectives[0])
            solution_list.append(solution_[0])

        # put samples into result
        result = Result(problem)
        for solution in solution_list:
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
        result.iterations = sample_times
        print("{} Hybrid Solver end!!!".format(problem.name))
        return result

    @staticmethod
    def Decomposer(sub_size: int, bqm: BinaryQuadraticModel, variables_num: int) -> List[State]:
        """Decomposer [summary]
        State is a dict subclass and usually contains at least three keys:
        samples: SampleSet, problem: BinaryQuadraticModel and subproblem: BinaryQuadraticModel.
        """
        decomposer = EnergyImpactDecomposer(size=sub_size, rolling=True, rolling_history=1.0, traversal='pfs')
        state0 = State.from_sample(min_sample(bqm), bqm)
        length = variables_num
        states = []
        while length > 0:
            state0 = decomposer.run(state0).result()
            states.append(state0)
            length -= sub_size
        return states

    @staticmethod
    def Sampler(states: List[State], num_reads: int) -> Tuple[List[SampleSet], float]:
        elapseds = 0.0
        subsamplesets = []
        for state in states:
            pro_bqm = state.subproblem
            qubo, offset = pro_bqm.to_qubo()
            sampler = EmbeddingSampler()
            sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads, answer_mode='raw')
            subsamplesets.append(sampleset)
            elapseds += elapsed
        return subsamplesets, elapseds

    @staticmethod
    def Composer(problem: QP, subsamplesets: List[SampleSet], num_reads: int, solution_list: List[BinarySolution]) -> bool:
        values_array: Dict[str, List[int]] = {}
        for var in problem.variables:
            values_array[var] = []
        for subsampleset in subsamplesets:
            var_index: Dict[str, int] = {}
            for var in subsampleset.variables:
                if var not in problem.variables:
                    continue
                var_index[var] = subsampleset.variables.index(var)
            assert len(subsampleset.record) == num_reads
            for subsample in subsampleset.record:
                for var in subsampleset.variables:
                    if var not in problem.variables:
                        continue
                    values_array[var].append(subsample[0][var_index[var]])
        if len(values_array) != problem.variables_num:
            return False
        pos = 0
        while pos < num_reads:
            values = {var: bool(values_array[var][pos]) for var in problem.variables}
            solution = problem.evaluate(values)
            solution_list.append(solution)
            pos += 1
        return True

    @staticmethod
    def NSGAII(populationSize: int, maxEvaluations: int, problem: QP, seed: float,
               time: float, solution_list: List[BinarySolution]):
        t = 0
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
                    mutation=BitflipMutation())
        while t < time:
            res = minimize(pro, alg, termination, seed=seed, verbose=False,
                           return_least_infeasible=True)
            for sol in res.pop:
                val = list(sol.X.flatten())
                values = problem.convert_to_BinarySolution(val)
                solution = problem.evaluate(values)
                solution_list.append(solution)
            t += res.exec_time

    @staticmethod
    def SA(H: Quadratic, t_max: float, t_min: float, L: int, max_stay: int, num_reads: int,
           time: float, problem: QP, solution_list: List[BinarySolution]):
        fitness, variables = FSAQPSolver.quadratic_to_fitness(H)
        x0 = []
        for _ in range(len(variables)):
            x0.append(bool(random.randint(0, 1)))
        sampler = SAFast(func=fitness, T_max=t_max, T_min=t_min, L=L, max_stay_counter=max_stay, x0=x0,
                         num_reads=num_reads)
        t = 0
        while t < time:
            start2 = SolverUtil.time()
            best_x, _ = sampler.run()
            end2 = SolverUtil.time()
            # restore the result
            best_x = np.array(best_x).flatten().tolist()
            values: Dict[str, bool] = {}
            for ind, val in enumerate(best_x):
                values[variables[ind]] = bool(val)
            sol = problem.evaluate(values)
            solution_list.append(sol)
            t += (end2 - start2)
