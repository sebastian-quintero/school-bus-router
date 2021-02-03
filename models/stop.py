from dataclasses import dataclass
from statistics import mean
from typing import Dict, Optional, Any

from models.location import Location
from models.rider import Rider


@dataclass
class Stop:
    """Class that defines a physical Stop"""

    riders: Optional[Dict[str, Rider]] = None
    demand: int = 0
    depot_id: Optional[str] = None
    location: Optional[Location] = None
    service_time: float = 0

    def __post_init__(self):
        """Procedures to be completed after the Stop is instantiated"""

        self.demand = len(self.riders) if not self.depot_id else self.demand
        if self.location is None:
            lat = mean([rider.location.lat for rider in self.riders.values()])
            lng = mean([rider.location.lng for rider in self.riders.values()])
            self.location = Location(lat=lat, lng=lng)

    def to_dict(self) -> Dict[str, Any]:
        """Method to parse the Stop to a Dict (JSON) for dumping"""

        return {
            'location': self.location.coordinates,
            'riders': (
                [rider_id for rider_id in self.riders.keys()]
                if self.riders is not None
                else self.riders
            ),
            'depot_id': self.depot_id
        }
