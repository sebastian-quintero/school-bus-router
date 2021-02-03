from dataclasses import dataclass

from models.entity import Entity
from models.location import Location


@dataclass
class Rider(Entity):
    """Class that represents a Rider to be routed"""

    location: Location
    rider_id: str
