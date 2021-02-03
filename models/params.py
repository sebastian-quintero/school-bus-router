from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Params:
    """Class to handle the Params of the project"""

    GEOHASH_PRECISION_GROUPING: int = 8
    FIRST_SOLUTION_STRATEGY: str = 'AUTOMATIC'
    SEARCH_METAHEURISTIC: str = 'AUTOMATIC'
    SEARCH_TIME_LIMIT: float = 3
    SEARCH_SOLUTIONS_LIMIT: int = 1000

    @classmethod
    def from_dict(cls, params_dict: Dict[str, Any]):
        """Method to instantiate a Params class from a Dict (JSON)"""

        entity_attributes = cls.__dataclass_fields__.keys()
        attributes_dict = {
            k: v
            for k, v in params_dict.items()
            if k in entity_attributes
        }

        return cls(**attributes_dict)
