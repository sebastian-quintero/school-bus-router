from dataclasses import dataclass, field
from typing import List, Any, Dict

from models.stop import Stop


@dataclass
class Route:
    """Class that represents a route, which is an ordered set of stops"""

    stops: List[Stop] = field(default_factory=lambda: list())
    vehicle_id: str = ''

    def to_dict(self) -> Dict[str, Any]:
        """Method to parse the Route to a Dict (JSON) for dumping"""

        return {
            'vehicle_id': self.vehicle_id,
            'stops': [stop.to_dict() for stop in self.stops]
        }
