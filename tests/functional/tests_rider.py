import unittest
from typing import Dict, Any

from models.rider import Rider
from tests.data.test_riders import test_riders


class TestsRider(unittest.TestCase):
    """Tests for the Rider class"""

    def _assert_rider_fields(self, rider_dict: Dict[str, Any]):
        """Auxiliary method to assert fields in the Rider are correct"""

        rider = Rider.from_dict(rider_dict)
        self.assertEqual(
            rider.location.lat, rider_dict['lat'],
            msg='Latitude for the Rider is not obtained correctly.'
        )
        self.assertEqual(
            rider.location.lng, rider_dict['lng'],
            msg='Longitude for the Rider is not obtained correctly.'
        )
        self.assertEqual(
            rider.rider_id, rider_dict['rider_id'],
            msg='The Rider is instantiated with incorrect rider_id.'
        )

    def test_from_dict(self):
        """Asserts that a Rider is correctly instantiated from a Dict (JSON)"""

        rider_dict = test_riders[0]
        self._assert_rider_fields(rider_dict)

    def test_from_dict_extra_data(self):
        """
        Asserts that a Rider is correctly instantiated from a Dict (JSON)
        that has extra input
        """

        rider_dict = test_riders[0]
        rider_dict['extra_field'] = 'extra_value'
        self._assert_rider_fields(rider_dict)
