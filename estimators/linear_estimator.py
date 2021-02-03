import logging
from typing import List, Dict, Tuple

from haversine import haversine

from estimators.estimator import Estimator
from models.stop import Stop
from models.vehicle import DEFAULT_VELOCITY


class LinearEstimator(Estimator):
    """Class that estimates the linear-distance-based time between Stops"""

    def estimate(self, stops: List[Stop]) -> Dict[Tuple, float]:
        """"
        Method that:
        1) obtains the paths to estimate, and
        2) calculates the linear time by dividing the linear distance by the
        default velocity.
        """

        paths = self._build_paths(num_stops=len(stops))
        estimations = {}

        for origin_ix, destination_ix in paths:
            origin = stops[origin_ix].location.coordinates
            destination = stops[destination_ix].location.coordinates
            estimations[(origin_ix, destination_ix)] = (
                haversine(origin, destination) / DEFAULT_VELOCITY
                if origin != destination
                else 0.
            )

        logging.info(f'Estimated {len(paths)} paths with the LinearEstimator.')

        return estimations
