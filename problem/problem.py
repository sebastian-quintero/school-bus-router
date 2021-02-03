import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

from models.depot import Depot
from models.params import Params
from models.rider import Rider
from models.stop import Stop
from models.vehicle import Vehicle


@dataclass
class Problem:
    """A class that defines a VRP (Vehicle Routing Problem)"""

    depots: Dict[str, Depot]
    ends: List[int]
    estimations: Dict[Tuple, float]
    params: Params
    riders: Dict[str, Rider]
    starts: List[int]
    stops: List[Stop]
    vehicles: Dict[str, Vehicle]

    def __post_init__(self):
        """Procedures to be completed after the Problem is instantiated"""

        logging.info(
            f'Instantiated a Problem with: '
            f'{len(self.depots)} depots, '
            f'{len(self.ends)} end locations, '
            f'{len(self.estimations)} estimations, '
            f'{len(self.riders)} riders, '
            f'{len(self.starts)} start locations, '
            f'{len(self.stops)} stops, '
            f'{len(self.vehicles)} vehicles.'
        )
