import logging
from typing import List

from ortools.constraint_solver.pywrapcp import RoutingIndexManager, \
    RoutingModel, DefaultRoutingSearchParameters
from ortools.constraint_solver.routing_parameters_pb2 import \
    RoutingSearchParameters

from constraints.constraint import Constraint
from optimization_model.optimization_model import OptimizationModel
from problem.problem import Problem

LOCAL_SEARCH_METAHEURISTIC = {
    'AUTOMATIC': 6,
    'GREEDY_DESCENT': 1,
    'GUIDED_LOCAL_SEARCH': 2,
    'SIMULATED_ANNEALING': 3,
    'TABU_SEARCH': 4
}
FIRST_SOLUTION_STRATEGY = {
    'AUTOMATIC': 15,
    'PATH_CHEAPEST_ARC': 3,
    'PATH_MOST_CONSTRAINED_ARC': 4,
    'EVALUATOR_STRATEGY': 5,
    'SAVINGS': 10,
    'SWEEP': 11,
    'CHRISTOFIDES': 13,
    'ALL_UNPERFORMED': 6,
    'BEST_INSERTION': 7,
    'PARALLEL_CHEAPEST_INSERTION': 8,
    'LOCAL_CHEAPEST_INSERTION': 9,
    'GLOBAL_CHEAPEST_ARC': 1,
    'LOCAL_CHEAPEST_ARC': 2,
    'FIRST_UNBOUND_MIN_VALUE': 12
}


class OptimizationModelBuilder:
    """A class to build an Optimization Model"""

    def __init__(self, constraints: List[Constraint]):
        self._constraints = constraints

    def build(self, problem: Problem) -> OptimizationModel:
        """Method to build an Opt. Model from the Problem"""

        manager = RoutingIndexManager(
            len(problem.stops),  # Number of locations
            len(problem.vehicles),  # Number of vehicles
            problem.starts,  # Start list of Vehicles
            problem.ends  # End list of Vehicles
        )
        solver = RoutingModel(manager)
        search_parameters = self._build_search_parameters(problem)
        self._apply_constraints(problem, manager, solver)
        self._set_objective_function(problem, manager, solver)

        return OptimizationModel(
            manager=manager,
            solver=solver,
            search_parameters=search_parameters
        )

    def _apply_constraints(
            self,
            problem: Problem,
            manager: RoutingIndexManager,
            solver: RoutingModel
    ):
        """Method to apply the Constraints to the Optimization Model"""

        for constraint in self._constraints:
            constraint.problem = problem
            constraint.manager = manager
            constraint.apply(solver)

        logging.info(
            f'Applied {len(self._constraints)} constraints to '
            f'the OptimizationModel.'
        )

    @staticmethod
    def _set_objective_function(
            problem: Problem,
            manager: RoutingIndexManager,
            solver: RoutingModel
    ):
        """Method to set the objective function of the Optimization Model"""

        def _time_callback(from_index: int, to_index: int):
            """Callback to obtain the complete time between Stops"""

            origin = manager.IndexToNode(from_index)
            destination = manager.IndexToNode(to_index)
            travelling_time = problem.estimations[(origin, destination)]
            service_time = problem.stops[destination].service_time

            return travelling_time + service_time

        callback_index = solver.RegisterTransitCallback(_time_callback)
        solver.SetArcCostEvaluatorOfAllVehicles(callback_index)
        logging.info('Set the objective function to the OptimizationModel.')

    @staticmethod
    def _build_search_parameters(problem: Problem) -> RoutingSearchParameters:
        """Method to set the heuristic search parameters to the solver"""

        search_parameters = DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            FIRST_SOLUTION_STRATEGY[problem.params.FIRST_SOLUTION_STRATEGY]
        )
        search_parameters.local_search_metaheuristic = (
            LOCAL_SEARCH_METAHEURISTIC[problem.params.SEARCH_METAHEURISTIC]
        )
        search_parameters.time_limit.seconds = (
            problem.params.SEARCH_TIME_LIMIT
        )
        search_parameters.solution_limit = (
            problem.params.SEARCH_SOLUTIONS_LIMIT
        )
        logging.info('Built the search parameters for the OptimizationModel.')

        return search_parameters
