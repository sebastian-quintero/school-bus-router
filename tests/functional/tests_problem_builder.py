import unittest
from statistics import mean

from estimators.linear_estimator import LinearEstimator
from models.depot import Depot
from models.location import Location
from models.rider import Rider
from models.vehicle import Vehicle
from problem.problem_builder import ProblemBuilder
from tests.data.test_depots import test_depots
from tests.data.test_riders import test_riders
from tests.data.test_vehicles import test_vehicles
from tests.test_utils import get_params, parse_models


class TestsProblemBuilder(unittest.TestCase):
    """Tests for the Problem Builder class"""

    def test_build_starts_ends(self):
        """Asserts start and end locations are correctly created"""

        vehicle_1 = Vehicle(
            capacity=0,
            start='depot_1',
            end='depot_1',
            vehicle_id='vehicle_1'
        )
        vehicle_2 = Vehicle(
            capacity=0,
            start='depot_1',
            end='depot_2',
            vehicle_id='vehicle_2'
        )
        depot_1 = Depot(
            depot_id='depot_1',
            location=Location(lat=0, lng=0)
        )
        depot_2 = Depot(
            depot_id='depot_2',
            location=Location(lat=0, lng=0)
        )
        vehicles = {
            vehicle_1.vehicle_id: vehicle_1,
            vehicle_2.vehicle_id: vehicle_2
        }
        depots = {
            depot_1.depot_id: depot_1,
            depot_2.depot_id: depot_2
        }
        starts, ends = ProblemBuilder._build_vehicles_starts_ends(
            vehicles, depots
        )
        self.assertTrue(starts, msg='Empty start locations.')
        self.assertTrue(ends, msg='Empty ends locations.')
        self.assertEqual(
            len(starts),
            len(vehicles),
            msg='Starts list differs from length to vehicles list.'
        )
        self.assertEqual(
            len(starts),
            len(ends),
            msg='Starts list differs from length to ends list.'
        )
        self.assertEqual(starts, [0, 0], msg='Starts list does not match.')
        self.assertEqual(ends, [0, 1], msg='Ends list does not match.')

    def test_build_stops(self):
        """Assert that Stops are a grouping of Riders and Depots"""

        riders = parse_models(model_dicts=test_riders, cls=Rider)
        depots = parse_models(model_dicts=test_depots, cls=Depot)
        params = get_params()
        builder = ProblemBuilder(params=params, estimator=LinearEstimator())
        stops = builder._build_stops(
            riders=riders,
            depots=depots,
            starts=[0, 1],
            ends=[0, 1]
        )

        self.assertTrue(
            stops,
            msg=f'Stops could not be built from {len(riders)} riders.'
        )
        self.assertEqual(
            len(stops), len(riders) + len(depots) - 1,
            msg='Number of stops differs from expected from test input.'
        )

        for stop in stops:
            if not stop.depot_id:
                self.assertEqual(
                    stop.demand, len(stop.riders),
                    msg='Stop has a demand that differs from the Riders.'
                )
                self.assertEqual(
                    stop.location.lat,
                    mean([
                        rider.location.lat
                        for rider in stop.riders.values()
                    ]),
                    msg='Latitude incorrectly calculated for Stop.'
                )
                self.assertEqual(
                    stop.location.lng,
                    mean([
                        rider.location.lng for rider in stop.riders.values()
                    ]),
                    msg='Longitude incorrectly calculated for Stop.'
                )
                first_rider = list(stop.riders.values())[0]
                self.assertEqual(
                    stop.location.extract_geohash(
                        precision=params.GEOHASH_PRECISION_GROUPING
                    ),
                    first_rider.location.extract_geohash(
                        precision=params.GEOHASH_PRECISION_GROUPING
                    ),
                    msg='Geohash for the Stop differs to that of first Rider.'
                )

            else:
                self.assertEqual(
                    stop.demand, 0,
                    msg='Depot stop has non-zero demand.'
                )

    def test_build(self):
        """Asserts that the Problem is built correctly"""

        params = get_params()
        estimator = LinearEstimator()
        builder = ProblemBuilder(params=params, estimator=estimator)

        riders = parse_models(model_dicts=test_riders, cls=Rider)
        vehicles = parse_models(model_dicts=test_vehicles, cls=Vehicle)
        depots = parse_models(model_dicts=test_depots, cls=Depot)
        problem = builder.build(riders, vehicles, depots)

        self.assertTrue(problem, msg='Problem could not be built.')
        self.assertEqual(
            len(problem.stops), len(riders) + len(depots) - 1,
            msg='Number of stops differs from expected from test input.'
        )
        self.assertEqual(
            len(problem.estimations), (len(riders) + len(depots) - 1) ** 2,
            msg='Number of estimations incorrect.'
        )

    def test_build_stops_absent_depots(self):
        """Asserts depots are excluded if no vehicle starts or ends there"""

        params = get_params()
        estimator = LinearEstimator()
        builder = ProblemBuilder(params=params, estimator=estimator)
        rider_1 = Rider(
            location=Location(lat=1.234, lng=5.678),
            rider_id='rider_1'
        )
        rider_2 = Rider(
            location=Location(lat=5.678, lng=1.234),
            rider_id='rider_2'
        )
        depot_1 = Depot(
            depot_id='depot_1',
            location=Location(lat=0, lng=0)
        )
        depot_2 = Depot(
            depot_id='depot_2',
            location=Location(lat=0, lng=0)
        )
        riders = {
            rider_1.rider_id: rider_1,
            rider_2.rider_id: rider_2
        }
        depots = {
            depot_1.depot_id: depot_1,
            depot_2.depot_id: depot_2
        }

        # Case 1: all depots are needed
        starts = [0, 0]
        ends = [0, 1]
        stops = builder._build_stops(riders, depots, starts, ends)
        self.assertEqual(
            len(stops), 4,
            msg='Wrong number of stops when all depots are used.'
        )

        # Case 2: some depots are needed
        starts = [0, 0]
        ends = [0, 0]
        stops = builder._build_stops(riders, depots, starts, ends)
        self.assertEqual(
            len(stops), 3,
            msg='Wrong number of stops when some depots are used.'
        )
