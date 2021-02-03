from dataclasses import dataclass

from models.entity import Entity
from utils.time_utils import hour_to_sec

DEFAULT_VELOCITY = 20 / hour_to_sec(1)


@dataclass
class Vehicle(Entity):
    """Class that represents a motorized Vehicle"""

    capacity: int
    start: str
    end: str
    vehicle_id: str
