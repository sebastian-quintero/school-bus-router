import unittest
from statistics import mean

from models.location import Location
from models.rider import Rider
from models.stop import Stop
from tests.data.test_riders import test_riders
from tests.test_utils import parse_models


class TestsStop(unittest.TestCase):
    """Tests for the Stop class"""

    def test_post_init(self):
        """Assert the actions taken after the class is instantiated"""

        riders = parse_models(model_dicts=test_riders[0:2], cls=Rider)
        stop = Stop(riders=riders)

        self.assertEqual(
            stop.demand, len(riders),
            msg='Stop has demand that differs from riders.'
        )
        self.assertEqual(
            stop.location.lat,
            mean([rider.location.lat for rider in riders.values()]),
            msg='Latitude incorrectly calculated for Stop.'
        )
        self.assertEqual(
            stop.location.lng,
            mean([rider.location.lng for rider in riders.values()]),
            msg='Longitude incorrectly calculated for Stop.'
        )

    def test_to_dict(self):
        """Asserts the Stop is correctly parsed to a Dict"""

        depot_stop = Stop(
            depot_id='my_depot',
            location=Location(lat=1.23, lng=4.56)
        )
        depot_stop_dict = depot_stop.to_dict()
        self.assertEqual(
            depot_stop.depot_id, depot_stop_dict['depot_id'],
            msg='Depot stop has incorrect depot_id after parsing.'
        )
        self.assertEqual(
            depot_stop.location.coordinates, depot_stop_dict['location'],
            msg='Depot stop has incorrect location after parsing.'
        )
        self.assertIsNone(
            depot_stop_dict['riders'],
            msg='Depot stop has non-null riders.'
        )

        riders_stop = Stop(
            riders={
                'my_rider': Rider(
                    location=Location(lat=1.23, lng=4.56),
                    rider_id='my_rider'
                )
            }
        )
        riders_stop_dict = riders_stop.to_dict()
        self.assertIsNone(
            riders_stop_dict['depot_id'],
            msg='Riders stop has non-null depot_id.'
        )
        self.assertEqual(
            depot_stop.location.coordinates, riders_stop_dict['location'],
            msg='Riders stop has incorrect location after parsing.'
        )
        self.assertIsNotNone(
            riders_stop_dict['riders'],
            msg='Riders stop has null riders.'
        )
