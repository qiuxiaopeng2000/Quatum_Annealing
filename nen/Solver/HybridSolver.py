import random
from typing import Dict, List, Tuple

import numpy as np
from dimod import BinaryQuadraticModel
# from dwave.system import DWaveSampler
from hybrid import State, min_sample, EnergyImpactDecomposer
from jmetal.core.solution import BinarySolution

from nen.Solver import MOQASolver, JarSolver, SASolver, QAWSOSolver
from nen.Solver.GASolver import GASolver
from nen.Solver.SAQPSolver import SAQPSolver
from nen.Term import Constraint, Quadratic
from nen.Problem import QP
from nen.Result import Result, MethodResult, ProblemResult
from nen.Solver.MetaSolver import SolverUtil
from nen.Solver.EmbeddingSampler import EmbeddingSampler, SampleSet
from dwave.system import DWaveSampler
from nen.DescribedProblem import DescribedProblem
import dwavebinarycsp


class HybridSolver:
    """ [summary] HybridSolver, stands for Multi-Objective Quantum Annealling with HybridSolver,
    hybrid—quantum-classical hybrid; typically one or more classical algorithms run on the problem
    while outsourcing to a quantum processing unit (QPU) parts of the problem where it benefits most.

    The Quantum Annealling Solver is implemeneted with D-Wave Leap,
    make sure the environment is configured successfully accordingly.
    """

    @staticmethod
    def solve(problem: QP, num_reads: int, sub_size: int, maxEvaluations: int,
              sample_times: int = 1, rate: float = 1.0, **parameters) -> Result:
        """solve [summary] solve multi-objective qp, results are recorded in result.
        """
        print("{} start Hybrid Solver to solve multi-objective problem!!!".format(problem.name))
        # scale objectives and get the basic
        basic_weights = SolverUtil.scaled_weights(problem.objectives)
        # sample for sample_times times
        samplesets: List[SampleSet] = []
        elapseds: List[float] = []
        solution_list: List[BinarySolution] = []
        t = 0
        for _ in range(sample_times):
            # generate random weights and calculate weighted sum obejctive
            weights = MOQASolver.random_normalized_weights(basic_weights)
            wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.objectives, weights))
            # calculate the penalty and add constraints to objective with penalty
            penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
            objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
            qubo = Constraint.quadratic_to_qubo_dict(objective)
            # convert qubo to bqm
            bqm = BinaryQuadraticModel.from_qubo(qubo)

            '''Decomposer'''
            s1 = SolverUtil.time()
            states = HybridSolver.Decomposer(sub_size=sub_size, bqm=bqm, variables_num=bqm.num_variables)
            length = len(states)
            states = states[:int(length * rate)]
            e1 = SolverUtil.time()
            '''Sampler'''
            subsamplesets, runtime = HybridSolver.Sampler(states=states, num_reads=num_reads, **parameters)
            '''Composer'''
            s2 = SolverUtil.time()
            HybridSolver.Composer(problem=problem, subsamplesets=subsamplesets, num_reads=num_reads,
                                  solution_list=solution_list)
            e2 = SolverUtil.time()
            t += e1 - s1 + e2 - s2 + runtime
            elapseds.append(t)
        '''NSGA-II'''
        HybridSolver.NSGAII(populationSize=num_reads * sample_times, maxEvaluations=maxEvaluations, problem=problem,
                            time=e2-s1, solution_list=solution_list)
        '''Selection'''
        # solution_list.sort(key=lambda x: (x.constraints[0], np.dot(x.objectives, list(weights.values()))))
        solution_list.sort(key=lambda x: x.objectives)
        # solution_list.sort(key=lambda x: np.dot(x.objectives, list(weights.values())))
        solution_list = solution_list[:sample_times * num_reads]

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
        result.info['num_reads'] = num_reads
        result.iterations = sample_times
        result.total_num_anneals = num_reads * sample_times
        print("{} Hybrid Solver end!!!".format(problem.name))
        return result

    @staticmethod
    def single_solve(problem: QP, weights: Dict[str, float], num_reads: int, sub_size: int, t_max: float,
                     t_min: float, alpha: float, rate: float = 1.0, **parameters) -> Result:
        print("{} start Hybrid Solver to solve single-objective problem!!!".format(problem.name))
        # sample for sample_times times
        samplesets: List[SampleSet] = []
        solution_list: List[BinarySolution] = []

        # generate random weights and calculate weighted sum obejctive
        wso = Quadratic(linear=SolverUtil.weighted_sum_objective(problem.offset_objectives, weights))
        # calculate the penalty and add constraints to objective with penalty
        penalty = EmbeddingSampler.calculate_penalty(wso, problem.constraint_sum)
        objective = Constraint.quadratic_weighted_add(1, penalty, wso, problem.constraint_sum)
        qubo = Constraint.quadratic_to_qubo_dict(objective)
        # convert qubo to bqm
        bqm = BinaryQuadraticModel.from_qubo(qubo)

        '''Decomposer'''
        s1 = SolverUtil.time()
        states = HybridSolver.Decomposer(sub_size=sub_size, bqm=bqm, variables_num=bqm.num_variables)
        length = int(len(states) * rate)
        states = states[:length]
        e1 = SolverUtil.time()
        '''Sampler'''
        subsamplesets, runtime = HybridSolver.Sampler(states=states, num_reads=num_reads, **parameters)
        '''Composer'''
        s2 = SolverUtil.time()
        HybridSolver.Composer(problem=problem, subsamplesets=subsamplesets, num_reads=num_reads, 
                              solution_list=solution_list)
        e2 = SolverUtil.time()
        '''SA'''
        # x0 = QAWSOSolver.best_solution(solution_list, problem, weights)
        t = e1 - s1 + e2 - s2 + runtime
        HybridSolver.SA(t_max=t_max, t_min=t_min, num_reads=num_reads, weight=weights,
                        time=e2-s1, problem=problem, solution_list=solution_list, alpha=alpha)
        '''Selection'''
        # solution_list.sort(key=lambda x: (x.constraints[0], np.dot(x.objectives, list(weights.values()))))
        # solution_ = []
        # solution_ += solution_list
        # solution_.sort(key=lambda x: np.dot(x.objectives, list(weights.values())))
        # solution_list.sort(key=lambda x: x.objectives[1] if x.objectives[1] < 0 else x.objectives)
        w = []
        for k, v in weights.items():
            w.append(v)
        solution_list.sort(key=lambda x: sum([x.objectives[i] * w[i] for i in range(problem.objectives_num)]))
        solution_list = solution_list[:num_reads]

        # put samples into result
        result = Result(problem)
        # dp = DescribedProblem()
        # dp.load(problem.name)
        for solution in solution_list:
            result.wso_add(solution)
        # add into method result
        result.elapsed = t
        for sampleset in samplesets:
            if 'solving info' not in result.info:
                result.info['solving info'] = [sampleset.info]
            else:
                result.info['solving info'].append(sampleset.info)
        # storage parameters
        print("{} Hybrid Solver end!!!".format(problem.name))
        return result

    @staticmethod
    def Decomposer(sub_size: int, bqm: BinaryQuadraticModel, variables_num: int) -> List[State]:
        """Decomposer [summary]
        State is a dict subclass and usually contains at least three keys:
        samples: SampleSet, problem: BinaryQuadraticModel and subproblem: BinaryQuadraticModel.
        """
        length = variables_num
        if length < sub_size:
            sub_size = 20
        decomposer = EnergyImpactDecomposer(size=sub_size, rolling=True, rolling_history=1.0, traversal='pfs')
        state0 = State.from_sample(min_sample(bqm), bqm)

        states = []
        while length > 0:
            state0 = decomposer.run(state0).result()
            states.append(state0)
            length -= sub_size
        return states

    @staticmethod
    def Sampler(states: List[State], num_reads: int, **parameters) -> Tuple[List[SampleSet], float]:
        elapseds = 0.0
        subsamplesets = []
        for state in states:
            pro_bqm = state.subproblem

            qubo, offset = pro_bqm.to_qubo()
            sampler = EmbeddingSampler()
            sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads, answer_mode='raw', **parameters)
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
            # assert len(subsampleset.record) == num_reads
            for subsample in subsampleset.record:
                for var in subsampleset.variables:
                    if var not in problem.variables:
                        continue
                    values_array[var].append(subsample[0][var_index[var]])
        for var in problem.variables:
            if len(values_array[var]) == 0:
                values_array[var] += [0.0 for _ in range(len(subsamplesets[0].record))]
        pos = 0
        while pos < num_reads:
            values = {var: bool(values_array[var][pos]) for var in problem.variables}
            solution = problem.evaluate(values)
            solution_list.append(solution)
            pos += 1
        return True

    @staticmethod
    def NSGAII(populationSize: int, maxEvaluations: int, problem: QP,
               time: float, solution_list: List[BinarySolution]):
        result = GASolver.solve(populationSize=populationSize, maxEvaluations=maxEvaluations, crossoverProbability=0.8,
                                mutationProbability=(1 / problem.variables_num), seed=1,
                                problem=problem, exec_time=time)
        for solution in result.solution_list:
            solution_list.append(solution)

    @staticmethod
    def SA(t_max: float, t_min: float, num_reads: int, alpha: float,
           time: float, problem: QP, solution_list: List[BinarySolution], weight: Dict[str, float]):
        result = SASolver.solve(problem=problem, num_reads=num_reads, weights=weight,
                                t_max=t_max, t_min=t_min, alpha=alpha, exec_time=time)
        for solution in result.solution_list:
            solution_list.append(solution)

