import logging
from dataclasses import dataclass
from typing import List

from ortools.constraint_solver.pywrapcp import RoutingIndexManager, \
    RoutingModel
from ortools.constraint_solver.routing_parameters_pb2 import \
    RoutingSearchParameters

SOLVER_STATUS = {
    0: 'ROUTING_NOT_SOLVED',
    1: 'ROUTING_SUCCESS',
    2: 'ROUTING_FAIL',
    3: 'ROUTING_FAIL_TIMEOUT',
    4: 'ROUTING_INVALID'
}


@dataclass
class OptimizationModel:
    """Class that represents the mathematical Opt. Model to solve the VRP"""

    manager: RoutingIndexManager
    solver: RoutingModel
    search_parameters: RoutingSearchParameters

    def __post_init__(self):
        """Procedures to be completed after the Opt. Model is instantiated"""

        logging.info(
            'Instantiated an OptimizationModel with a manager, solver and '
            'search_parameters.'
        )

    def solve(self) -> List[List[int]]:
        """Method to solve the Optimization Model using the Parameters"""

        solution = self.solver.SolveWithParameters(self.search_parameters)
        logging.info(
            f'Solved the OptimizationModel and '
            f'the solver status is: {SOLVER_STATUS[self.solver.status()]}.'
        )
        processed_solution = self._process_solution(solution)

        return processed_solution

    def _process_solution(self, solution) -> List[List[int]]:
        """Method to process the solution given by or-tools"""

        num_vehicles = self.manager.GetNumberOfVehicles()
        routes = [[]] * num_vehicles

        for vehicle_ix in range(num_vehicles):
            route = []
            model_index = self.solver.Start(vehicle_ix)
            stop_index = self.manager.IndexToNode(model_index)
            route.append(stop_index)

            while not self.solver.IsEnd(model_index):
                model_index = solution.Value(self.solver.NextVar(model_index))
                stop_index = self.manager.IndexToNode(model_index)
                route.append(stop_index)

            routes[vehicle_ix] = route

        logging.info(
            f'Processed the OptimizationModel solution and '
            f'obtained {len(routes)} routes with these '
            f'number of stops: {[len(route) for route in routes]}.'
        )

        return routes
