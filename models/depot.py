from dataclasses import dataclass

from models.entity import Entity
from models.location import Location


@dataclass
class Depot(Entity):
    """"Class that represents a Depot where Vehicles depart or arrive"""

    depot_id: str
    location: Location
