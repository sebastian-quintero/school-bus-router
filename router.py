import logging
from typing import Dict, List, Any

from models.depot import Depot
from models.rider import Rider
from models.route import Route
from models.vehicle import Vehicle
from optimization_model.optimization_model_builder import \
    OptimizationModelBuilder
from problem.problem import Problem
from problem.problem_builder import ProblemBuilder


class Router:
    """Class that creates Routes using different services"""

    def __init__(
            self,
            problem_builder: ProblemBuilder,
            optimization_model_builder: OptimizationModelBuilder
    ):
        self._problem_builder = problem_builder
        self._optimization_model_builder = optimization_model_builder

    def route(
            self,
            riders: Dict[str, Rider],
            vehicles: Dict[str, Vehicle],
            depots: Dict[str, Depot]
    ) -> List[Dict[str, Any]]:
        """Method that orchestrates the services and returns the Routes"""

        problem = self._problem_builder.build(riders, vehicles, depots)
        model = self._optimization_model_builder.build(problem)
        solution = model.solve()
        routes = self._parse_routes(problem, solution)

        return routes

    @staticmethod
    def _parse_routes(
            problem: Problem,
            solution: List[List[int]]
    ) -> List[Dict[str, Any]]:
        """Method that parses the optimizer's response to the Routes"""

        routes = []
        for vehicle_ix, solution_stops in enumerate(solution):
            if len(solution_stops) > 1:
                route = Route(
                    stops=[
                        problem.stops[stop_ix]
                        for stop_ix in solution_stops
                    ],
                    vehicle_id=list(problem.vehicles.keys())[vehicle_ix]
                )
                route_dict = route.to_dict()
                routes.append(route_dict)

        logging.info(
            f'Obtained {len(routes)} routes from '
            f'the OptimizationModel solution.'
        )

        return routes
