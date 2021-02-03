import unittest

from constraints.capacity_constraint import CapacityConstraint
from estimators.linear_estimator import LinearEstimator
from models.depot import Depot
from models.rider import Rider
from models.vehicle import Vehicle
from optimization_model.optimization_model_builder import \
    OptimizationModelBuilder
from problem.problem_builder import ProblemBuilder
from router import Router
from tests.data.test_depots import test_depots
from tests.data.test_riders import test_riders
from tests.data.test_vehicles import test_vehicles
from tests.test_utils import parse_models, get_params


class TestsRouter(unittest.TestCase):
    """Tests for the Router class"""

    def test_parse_routes(self):
        """Asserts that Routes are correctly parsed from the Opt. solution"""

        params = get_params()
        estimator = LinearEstimator()
        problem_builder = ProblemBuilder(params=params, estimator=estimator)
        model_builder = OptimizationModelBuilder(
            constraints=[CapacityConstraint()]
        )
        riders = parse_models(model_dicts=test_riders, cls=Rider)
        vehicles = parse_models(model_dicts=test_vehicles, cls=Vehicle)
        depots = parse_models(model_dicts=test_depots, cls=Depot)
        problem = problem_builder.build(riders, vehicles, depots)
        model = model_builder.build(problem)
        solution = model.solve()
        routes = Router._parse_routes(problem, solution)
        self.assertTrue(routes, msg='Routes could not be built.')

        for route in routes:
            self.assertTrue(route['vehicle_id'], msg='Route without vehicle.')
            self.assertTrue(
                len(route['stops']) > 1,
                msg='Route with single stop.'
            )

    def test_route(self):
        """Asserts the main routing method works correctly"""

        params = get_params()
        estimator = LinearEstimator()
        problem_builder = ProblemBuilder(params=params, estimator=estimator)
        model_builder = OptimizationModelBuilder(
            constraints=[CapacityConstraint()]
        )
        router = Router(
            problem_builder=problem_builder,
            optimization_model_builder=model_builder
        )
        riders = parse_models(model_dicts=test_riders, cls=Rider)
        vehicles = parse_models(model_dicts=test_vehicles, cls=Vehicle)
        depots = parse_models(model_dicts=test_depots, cls=Depot)
        routes = router.route(riders, vehicles, depots)
        self.assertTrue(routes, msg='Routes could not be built.')

        for route in routes:
            self.assertTrue(route['vehicle_id'], msg='Route without vehicle.')
            self.assertTrue(
                len(route['stops']) > 1,
                msg='Route with single stop.'
            )
