import unittest

from google.protobuf.duration_pb2 import Duration
from ortools.constraint_solver.pywrapcp import RoutingModel, \
    RoutingIndexManager

from constraints.capacity_constraint import CapacityConstraint
from models.depot import Depot
from models.rider import Rider
from models.stop import Stop
from models.vehicle import Vehicle
from optimization_model.optimization_model_builder import \
    OptimizationModelBuilder, \
    FIRST_SOLUTION_STRATEGY, LOCAL_SEARCH_METAHEURISTIC
from problem.problem import Problem
from tests.data.test_depots import test_depots
from tests.data.test_riders import test_riders
from tests.data.test_vehicles import test_vehicles
from tests.test_utils import parse_models, get_params


class TestsOptimizationModelBuilder(unittest.TestCase):
    """Tests for the Optimization Model Builder class"""

    # Base Problem
    riders = parse_models(model_dicts=test_riders[0:2], cls=Rider)
    vehicles = parse_models(model_dicts=test_vehicles, cls=Vehicle)
    depots = parse_models(model_dicts=test_depots, cls=Depot)
    stops = [
        Stop(
            depot_id=list(depots.values())[0].depot_id,
            location=list(depots.values())[0].location
        ),
        Stop(riders=riders)
    ]
    estimations = {
        (0, 0): 0.,
        (0, 1): 85.,
        (1, 0): 78.,
        (1, 1): 0.
    }
    params = get_params()
    problem = Problem(
        depots=depots,
        estimations=estimations,
        params=params,
        riders=riders,
        stops=stops,
        vehicles=vehicles,
        starts=[0, 1],
        ends=[0, 1]
    )

    def test_build_manager(self):
        """Asserts that a manager is built correctly from the Problem"""

        manager = RoutingIndexManager(
            len(self.problem.stops),  # Number of locations
            len(self.problem.vehicles),  # Number of vehicles
            self.problem.starts,  # Start list of Vehicles
            self.problem.ends  # End list of Vehicles
        )
        self.assertTrue(manager, msg='Opt. Manager could not be built.')
        self.assertEqual(
            manager.GetNumberOfVehicles(), len(self.vehicles),
            msg='Number of vehicles in manager is incorrect.'
        )
        self.assertEqual(
            manager.GetNumberOfIndices(),
            len(self.vehicles) * 2 +
            len(self.stops) -
            len(self.problem.depots),
            msg='Number of indices in manager is incorrect.'
        )
        solver = RoutingModel(manager)
        self.assertTrue(solver, msg='Solver could not be instantiated.')

    def test_build_search_parameters(self):
        """Asserts the heuristic search parameters are correctly created"""

        search_parameters = OptimizationModelBuilder._build_search_parameters(
            self.problem
        )
        self.assertTrue(
            search_parameters,
            msg='Search params could not be built.'
        )
        self.assertEqual(
            search_parameters.time_limit,
            Duration(seconds=self.params.SEARCH_TIME_LIMIT),
            msg='Time limit is incorrect in the search params.'
        )
        self.assertEqual(
            search_parameters.solution_limit,
            self.params.SEARCH_SOLUTIONS_LIMIT,
            msg='Solutions limit is incorrect in the search params.'
        )
        self.assertEqual(
            search_parameters.first_solution_strategy,
            FIRST_SOLUTION_STRATEGY[self.params.FIRST_SOLUTION_STRATEGY],
            msg='First solution strategy is incorrect in the search params.'
        )
        self.assertEqual(
            search_parameters.local_search_metaheuristic,
            LOCAL_SEARCH_METAHEURISTIC[self.params.SEARCH_METAHEURISTIC],
            msg='Search metaheuristic is incorrect in the search params.'
        )

    def test_apply_constraints_capacity_constraint(self):
        """Asserts constraints are read correctly by the solver"""

        model_builder = OptimizationModelBuilder(
            constraints=[CapacityConstraint()]
        )
        problem = self.problem
        manager = RoutingIndexManager(
            len(problem.stops),  # Number of locations
            len(problem.vehicles),  # Number of vehicles
            problem.starts,  # Start list of Vehicles
            problem.ends  # End list of Vehicles
        )
        solver = RoutingModel(manager)
        model_builder._apply_constraints(problem, manager, solver)
        self.assertTrue(solver, msg='Constraints added incorrectly.')
        self.assertTrue(
            solver.HasDimension('capacity_constraint'),
            msg='Capacity constraint not added.'
        )

    def test_set_objective_function(self):
        """Asserts the objective function is added to the solver"""

        model_builder = OptimizationModelBuilder(
            constraints=[CapacityConstraint()]
        )
        problem = self.problem
        manager = RoutingIndexManager(
            len(problem.stops),  # Number of locations
            len(problem.vehicles),  # Number of vehicles
            problem.starts,  # Start list of Vehicles
            problem.ends  # End list of Vehicles
        )
        solver = RoutingModel(manager)
        model_builder._set_objective_function(problem, manager, solver)
        self.assertTrue(solver, msg='Objective function set incorrectly.')

    def test_build(self):
        """Assert the Opt. model is built correctly"""

        model_builder = OptimizationModelBuilder(
            constraints=[CapacityConstraint()]
        )
        problem = self.problem
        model = model_builder.build(problem)
        self.assertTrue(model, msg='Opt. model built incorrectly.')
        self.assertEqual(
            model.manager.GetNumberOfVehicles(), len(self.vehicles),
            msg='Number of vehicles in manager is incorrect.'
        )
        self.assertEqual(
            model.manager.GetNumberOfIndices(),
            len(self.vehicles) * 2 +
            len(self.stops) -
            len(problem.depots),
            msg='Number of indices in manager is incorrect.'
        )
        self.assertTrue(model.solver, msg='Solver could not be instantiated.')
        self.assertTrue(
            model.search_parameters,
            msg='Search params could not be built.'
        )
        self.assertEqual(
            model.search_parameters.time_limit,
            Duration(seconds=self.params.SEARCH_TIME_LIMIT),
            msg='Time limit is incorrect in the search params.'
        )
        self.assertEqual(
            model.search_parameters.solution_limit,
            self.params.SEARCH_SOLUTIONS_LIMIT,
            msg='Solutions limit is incorrect in the search params.'
        )
        self.assertEqual(
            model.search_parameters.first_solution_strategy,
            FIRST_SOLUTION_STRATEGY[self.params.FIRST_SOLUTION_STRATEGY],
            msg='First solution strategy is incorrect in the search params.'
        )
        self.assertEqual(
            model.search_parameters.local_search_metaheuristic,
            LOCAL_SEARCH_METAHEURISTIC[self.params.SEARCH_METAHEURISTIC],
            msg='Search metaheuristic is incorrect in the search params.'
        )
        self.assertTrue(
            model.solver.HasDimension('capacity_constraint'),
            msg='Capacity constraint not added.'
        )
