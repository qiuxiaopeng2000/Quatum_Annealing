from typing import List, Dict, Tuple
import copy
from numpy import matrix as Mat
from jmetal.core.solution import BinarySolution
from nen.DescribedProblem import DescribedProblem
from nen.Term import Constraint, Linear, Quadratic


class Problem:
    """ [summary] Problem is the logic problem used in this project, its name determines its described problem file.

    Note that, 'Problem' is composed by LINEAR objectives and INTEGER (coefficient) constraints.
    """
    def __init__(self, name: str = '') -> None:
        # record the name
        self.name: str = name
        # problem content
        self.variables: List[str] = []
        self.objectives: Dict[str, Dict[str, float]] = {}
        self.constraints: List[Constraint] = []
        self.variables_num: int = 0
        self.objectives_num: int = 0
        self.constraints_num: int = 0

        # evaluate all constraints or just indicate infeasible (1)
        self.violateds_count: bool = True

        # vectorized content
        self.variables_index: Dict[str, int] = {var: index for index, var in enumerate(self.variables)}
        self.objectives_order: List[str] = []
        self.objectives_index: Dict[str, int] = {}
        self.objectives_matrix: Mat = Mat([])

        # check if empty problem
        if name == '': return

        # load with described problem
        dp = DescribedProblem()
        dp.load(name)
        self.variables = dp.variables
        self.objectives = dp.objectives
        for constraint_str_list in dp.constraints:
            assert len(constraint_str_list) == 3
            left, sense, right = constraint_str_list
            if sense == '<=' or sense == '=':
                self.constraints.append(Constraint(left, sense, int(right)))
            else:
                self.constraints.append(Constraint(left, sense, right))
        self.variables_num = len(self.variables)
        self.objectives_num = len(self.objectives)
        self.constraints_num = len(self.constraints)

    def info(self) -> None:
        print('name: {}'.format(self.name))
        print('variables number: {}'.format(len(self.variables)))
        print('objectives: {}'.format(self.objectives_order))
        print('constraints number: {}'.format(len(self.constraints)))

    def clone(self, another: 'Problem') -> None:
        """clone [summary] construct from another problem type
        """
        self.name = another.name
        self.variables = copy.copy(another.variables)
        self.objectives = copy.deepcopy(another.objectives)
        self.constraints = copy.deepcopy(another.constraints)

    def vectorize_variables(self) -> None:
        """vectorize_variables [summary] index variables
        """
        for index, var in enumerate(self.variables):
            self.variables_index[var] = index

    def vectorize_objectives(self, objectives_order: List[str]) -> None:
        """vectorize_objectives [summary] make objectives a matrix (in numpy) to accelerate speed.
        """
        assert self.variables_index is not None
        # collect objectives and check if objectives order is legal
        self.objectives_index = {}
        ordered_objectives: List[List[float]] = [[0.0] * len(self.variables) for _ in range(len(objectives_order))]
        for index, objective_name in enumerate(objectives_order):
            self.objectives_index[objective_name] = index
            assert objective_name in self.objectives
            for var, coef in self.objectives[objective_name].items():
                ordered_objectives[index][self.variables_index[var]] = coef
        self.objectives_matrix = Mat(ordered_objectives).T
        # set objectives attributes
        self.objectives_order = objectives_order
        self.objectives_num = len(objectives_order)
        self.objectives = {name: self.objectives[name] for name in objectives_order}

    def vectorize(self, objectives_order: List[str] = []) -> None:
        """vectorize [summary] vectorize the variables and objectives
        """
        self.vectorize_variables()
        if len(objectives_order) == 0:
            objectives_order = list(self.objectives.keys())
        self.vectorize_objectives(objectives_order)



    def vectorize_values(self, values: Dict[str, bool]) -> Mat:
        """vectorize_values [summary] make variables value (mapping variable name to bool value)
        a vector (one-line numpy matrix).

        Note that this function ignore variables not in self.variables.
        """
        vector: List[int] = [0] * len(self.variables)
        for var, val in values.items():
            if var not in self.variables_index: continue
            if not val: continue
            vector[self.variables_index[var]] = 1
        return Mat(vector)

    def evaluate_objectives(self, values: Dict[str, bool]) -> List[float]:
        """evaluate_objectives [summary] evaluate objectives list with variables values.
        """
        obj_values: List[float] = [0.0] * len(self.objectives_index)
        for obj_name, obj_index in self.objectives_index.items():
            for var, coef in self.objectives[obj_name].items():
                if values[var]: obj_values[obj_index] += coef
        return obj_values

    def evaluate_single_objective(self, values: Dict[str, bool], weights: Dict[str, float]) -> float:
        """evaluate-single-objective [summary] evaluate single-objective
        with the sum of objectives list with variables values.
        """
        sum_obj = 0
        obj_values: List[float] = [0.0] * len(self.objectives_index)
        for obj_name, obj_index in self.objectives_index.items():
            for var, coef in self.objectives[obj_name].items():
                if values[var]:
                    obj_values[obj_index] += coef
                    sum_obj += obj_values[obj_index] * weights[obj_name]
        return sum_obj

    def evaluate_constraints(self, values: Dict[str, bool], violated_count: bool) -> int:
        """evaluate_constraints [summary] evaluate violated constriants count with variables values.
        The violated constraint would be count as a number when violated_count is True,
        otherwise it would only indicate feasible (0) or infeasible(1).
        """
        if violated_count:
            violated = 0
            for constraint in self.constraints:
                if not constraint.evaluate(values):
                    violated += 1
            return violated
        else:
            for constraint in self.constraints:
                if not constraint.evaluate(values):
                    return 1
            return 0

    def _evaluate(self, values: Dict[str, bool], violated_count: bool = True) -> Tuple[List[float], int]:
        """_evaluate [summary] evaluate a solution with variables values.
        The violated constraint would be count as a number when violated_count is True,
        otherwise it would only indicate feasible (0) or infeasible(1).

        Return (objectives values, violated)
        """
        # evaluate objectives
        obj_values = self.evaluate_objectives(values)
        # evaluate violated
        violated = self.evaluate_constraints(values, violated_count)
        return obj_values, violated

    def _wso_evaluate(self, values: Dict[str, bool], weights: Dict[str, float], violated_count: bool = True) -> Tuple[float, int]:
        """_evaluate [summary] evaluate a solution with variables values.
        The violated constraint would be count as a number when violated_count is True,
        otherwise it would only indicate feasible (0) or infeasible(1).

        Return (objective values, violated)
        """
        # evaluate objectives
        obj_value = self.evaluate_single_objective(values, weights)
        # evaluate violated
        violated = self.evaluate_constraints(values, violated_count)
        return obj_value, violated

    def _empty_solution(self) -> BinarySolution:
        """_empty_solution [summary] prepare a empty BinarySolution.
        """
        # NOTE: we use one int BinarySolution.constraint to record violated constraints num.
        solution = BinarySolution(self.variables_num, self.objectives_num, 1)
        solution.constraints[0] = 0
        return solution

    def listize_values(self, values: Dict[str, bool]) -> List[bool]:
        """listize_values [summary] make values dict a list based on variables indexing.
        """
        values_list: List[bool] = [False] * self.variables_num
        for index, var in enumerate(self.variables):
            if values[var]: values_list[index] = True
        return values_list

    def evaluate(self, values: Dict[str, bool]) -> BinarySolution:
        """evaluate [summary] evaluate a solution with variables values.
        Return a BinarySolution from jmetal.
        """
        # prepare a BinarySolution
        solution = self._empty_solution()
        # NOTE: note that jmetal use variables in this way, variables: [[True, False, True, ...]]
        solution.variables = [self.listize_values(values)]
        solution.objectives, solution.constraints[0] = self._evaluate(values, self.violateds_count)
        return solution

    def wso_evaluate(self, values: Dict[str, bool], weights: Dict[str, float]) -> BinarySolution:
        """evaluate [summary] evaluate a solution with variables values.
        Return a BinarySolution from jmetal.
        """
        # prepare a BinarySolution
        solution = self._empty_solution()
        # NOTE: note that jmetal use variables in this way, variables: [[True, False, True, ...]]
        solution.variables = [self.listize_values(values)]
        solution.objectives, solution.constraints[0] = self._wso_evaluate(values, weights, self.violateds_count)
        return solution

    def evaluate_solution(self, solution: BinarySolution) -> BinarySolution:
        """evaluate_solution [summary] evaluate a given solution and return itself.
        """
        values = {var: solution.variables[0][ind] for ind, var in enumerate(self.variables)}
        solution.objectives, solution.constraints[0] = self._evaluate(values)
        return solution

    def weighted_objectives_sum(self, objectives_weight: Dict[str, float] = {}) -> Dict[str, float]:
        """weighted_objectives_sum [summary] get weighted sum objective.
        """
        objective: Dict[str, float] = {}
        if len(objectives_weight) == 0:
            objectives_weight = {k: 1 for k in self.objectives_order}
        for obj_name, obj_weight in objectives_weight.items():
            assert obj_name in self.objectives
            for var, coef in self.objectives[obj_name].items():
                if var in objective:
                    objective[var] += (obj_weight * coef)
                else:
                    objective[var] = (obj_weight * coef)
        return objective


class LP(Problem):
    """LP [summary] LP, short for Linear Problem.
    """
    TYPE = 'LP'

    def __init__(self, name: str, objectives_order: List[str] = []) -> None:
        super().__init__(name=name)
        # vectorize the problem
        self.vectorize(objectives_order)
        # convert all constraints in linear form
        self.constraints_lp: List[Linear] = []
        for constraint in self.constraints:
            self.constraints_lp += constraint.to_linear()

    def info(self) -> None:
        super().info()

    def get_objectives(self) -> List[Dict[str, float]]:
        return [self.objectives[obj_name] for obj_name in self.objectives_order]

    def get_constraints(self) -> List[Linear]:
        return self.constraints_lp


class QP(Problem):
    """QP [summary] QP, short for Quadratic Problem.
    """
    def __init__(self, name: str, objectives_order: List[str] = []) -> None:
        super().__init__(name=name)
        # vectorize the problem
        self.vectorize(objectives_order)
        # convert all constrains in quadratic form
        self.artificial_list: List[str] = []
        self.constraints_qp: List[Quadratic] = []
        for constraint in self.constraints:
            self.constraints_qp.append(constraint.to_quadratic(self.artificial_list))
        self.constraint_sum: Quadratic = Constraint.quadratic_sum(self.constraints_qp)

    def info(self) -> None:
        super().info()
        artificials_num = len(self.artificial_list)
        all_variables_num = len(self.variables) + len(self.artificial_list)
        print('all variables number: {} (artificial variables: {})'.format(all_variables_num, artificials_num))
