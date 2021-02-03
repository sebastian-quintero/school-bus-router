import logging
from typing import List, Tuple, Dict

import numpy as np

from models.stop import Stop


class Estimator:
    """Class that estimates time between Stops"""

    def estimate(self, stops: List[Stop]) -> Dict[Tuple, float]:
        """Method to estimate time between stops"""

        pass

    @staticmethod
    def _build_paths(num_stops: int) -> List[Tuple[int, int]]:
        """Method to build the paths that will be estimated"""

        stops_indices = np.arange(num_stops)
        stops_indices_rep = np.arange(num_stops)
        mesh = np.array(np.meshgrid(stops_indices, stops_indices_rep))
        combinations = mesh.T.reshape(-1, 2)
        logging.info(
            f'Built {len(combinations)} paths from {num_stops} stops.'
        )

        return list(map(tuple, combinations))
