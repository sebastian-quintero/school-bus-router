import unittest
from typing import Dict, Any

from models.vehicle import Vehicle
from tests.data.test_vehicles import test_vehicles


class TestsVehicle(unittest.TestCase):
    """Tests for the Vehicle class"""

    def _assert_vehicle_fields(self, vehicle_dict: Dict[str, Any]):
        """Auxiliary method to assert fields in the Vehicle are correct"""

        vehicle = Vehicle.from_dict(vehicle_dict)
        self.assertEqual(
            vehicle.capacity, vehicle_dict['capacity'],
            msg='The Vehicle is instantiated with incorrect capacity.'
        )
        self.assertEqual(
            vehicle.start, vehicle_dict['start'],
            msg='The Vehicle is instantiated with incorrect start Depot.'
        )
        self.assertEqual(
            vehicle.end, vehicle_dict['end'],
            msg='The Vehicle is instantiated with incorrect end Depot.'
        )
        self.assertEqual(
            vehicle.vehicle_id, vehicle_dict['vehicle_id'],
            msg='The Vehicle is instantiated with incorrect vehicle_id.'
        )

    def test_from_dict(self):
        """
        Asserts that a Vehicle is correctly instantiated from a Dict (JSON)
        """

        vehicle_dict = test_vehicles[0]
        self._assert_vehicle_fields(vehicle_dict)

    def test_from_dict_extra_data(self):
        """
        Asserts that a Vehicle is correctly instantiated from a Dict (JSON)
        that has extra input
        """

        vehicle_dict = test_vehicles[0]
        vehicle_dict['extra_field'] = 'extra_value'
        self._assert_vehicle_fields(vehicle_dict)
