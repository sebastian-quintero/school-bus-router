from dataclasses import dataclass
from typing import Tuple

from geohash import encode


@dataclass
class Location:
    """Class that defines a physical Location"""

    lat: float
    lng: float
    geohash: str = ''

    @property
    def coordinates(self) -> Tuple[float, float]:
        """Method that returns the Location's coordinates"""

        return self.lat, self.lng

    def __post_init__(self):
        """Method to process initialized information for the class"""

        if not bool(self.geohash):
            self.geohash = encode(self.lat, self.lng)

    def extract_geohash(self, precision: int = 12) -> str:
        """Method to extract the geohash to a desired precision"""

        return self.geohash[0:precision]
