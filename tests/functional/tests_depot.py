import unittest
from typing import Dict, Any

from models.depot import Depot
from tests.data.test_depots import test_depots


class TestsDepot(unittest.TestCase):
    """Tests for the Depot class"""

    def _assert_depot_fields(self, depot_dict: Dict[str, Any]):
        """Auxiliary method to assert fields in the Depot are correct"""

        depot = Depot.from_dict(depot_dict)
        self.assertEqual(
            depot.location.lat, depot_dict['lat'],
            msg='Latitude for the Depot is not obtained correctly.'
        )
        self.assertEqual(
            depot.location.lng, depot_dict['lng'],
            msg='Longitude for the Depot is not obtained correctly.'
        )
        self.assertEqual(
            depot.depot_id, depot_dict['depot_id'],
            msg='The Depot is instantiated with incorrect depot_id.'
        )

    def test_from_dict(self):
        """Asserts that a Depot is correctly instantiated from a Dict (JSON)"""

        depot_dict = test_depots[0]
        self._assert_depot_fields(depot_dict)

    def test_from_dict_extra_data(self):
        """
        Asserts that a Depot is correctly instantiated from a Dict (JSON)
        that has extra input
        """

        depot_dict = test_depots[0]
        depot_dict['extra_field'] = 'extra_value'
        self._assert_depot_fields(depot_dict)
