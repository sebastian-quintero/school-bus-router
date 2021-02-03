import unittest

from optimization_model.optimization_model_builder import \
    OptimizationModelBuilder
from problem.problem_builder import ProblemBuilder
from constraints.capacity_constraint import CapacityConstraint
from estimators.linear_estimator import LinearEstimator
from models.depot import Depot
from models.rider import Rider
from models.vehicle import Vehicle
from tests.data.test_depots import test_depots
from tests.data.test_riders import test_riders
from tests.data.test_vehicles import test_vehicles
from tests.test_utils import parse_models, get_params


class TestsOptimizationModel(unittest.TestCase):
    """Tests for the Optimization Model class"""

    def test_solve(self):
        """Asserts an Optimization Model is correctly solved"""

        riders = parse_models(model_dicts=test_riders, cls=Rider)
        vehicles = parse_models(model_dicts=test_vehicles, cls=Vehicle)
        depots = parse_models(model_dicts=test_depots, cls=Depot)
        params = get_params()
        estimator = LinearEstimator()
        problem_builder = ProblemBuilder(params=params, estimator=estimator)
        model_builder = OptimizationModelBuilder(
            constraints=[CapacityConstraint()]
        )
        problem = problem_builder.build(riders, vehicles, depots)
        model = model_builder.build(problem)
        solution = model.solve()

        self.assertTrue(solution, msg='Model could not be solved.')
        self.assertEqual(
            len(solution), len(vehicles),
            msg='Number of routes do not match number of vehicles.'
        )
        stops_in_solution = [stop for route in solution for stop in route]
        for stop_ix in range(len(problem.stops)):
            self.assertIn(
                stop_ix, stops_in_solution,
                msg=f'Stop {stop_ix} not in solution.'
            )
