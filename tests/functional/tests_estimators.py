import unittest

from haversine import haversine

from estimators.estimator import Estimator
from estimators.linear_estimator import LinearEstimator
from models.location import Location
from models.stop import Stop
from models.vehicle import DEFAULT_VELOCITY


class TestsEstimators(unittest.TestCase):
    """Tests for the Estimators"""

    def test_build_paths(self):
        """Asserts that paths are correctly built between stops"""

        num_stops = 3
        paths = Estimator._build_paths(num_stops)
        self.assertEqual(len(paths), 9, msg='Number of paths is incorrect.')
        self.assertTrue((0, 0) in paths, msg='Path (0, 0) not in paths.')
        self.assertTrue((0, 1) in paths, msg='Path (0, 1) not in paths.')
        self.assertTrue((0, 2) in paths, msg='Path (0, 2) not in paths.')
        self.assertTrue((1, 0) in paths, msg='Path (1, 0) not in paths.')
        self.assertTrue((1, 1) in paths, msg='Path (1, 1) not in paths.')
        self.assertTrue((1, 2) in paths, msg='Path (1, 2) not in paths.')
        self.assertTrue((2, 0) in paths, msg='Path (2, 0) not in paths.')
        self.assertTrue((2, 1) in paths, msg='Path (2, 1) not in paths.')
        self.assertTrue((2, 2) in paths, msg='Path (2, 2) not in paths.')

    def test_linear_estimator_estimate(self):
        """Asserts linear estimations are correctly calculated"""

        stop_1 = Stop(
            depot_id='depot_1',
            location=Location(lat=4.720634, lng=-74.037228)
        )
        stop_2 = Stop(
            depot_id='depot_2',
            location=Location(lat=4.708958, lng=-74.035172)
        )
        estimator = LinearEstimator()
        estimations = estimator.estimate(stops=[stop_1, stop_2])
        self.assertEqual(
            len(estimations), 4,
            msg='Number of estimations incorrect.'
        )

        expected_estimation = round(
                haversine(
                    point1=stop_1.location.coordinates,
                    point2=stop_2.location.coordinates
                ) / DEFAULT_VELOCITY
        )
        for (origin, destination), est in estimations.items():
            if origin == destination:
                self.assertEqual(
                    est, 0.,
                    msg='Same origin and destination has non-zero estimation.'
                )
            else:
                self.assertEqual(
                    round(est), expected_estimation,
                    msg='Estimated linear time differs to distance / velocity.'
                )
