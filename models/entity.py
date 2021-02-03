from typing import Dict, Any

from models.location import Location


class Entity:
    """Class that represents an abstract Entity with standard methods"""

    @classmethod
    def from_dict(cls, entity_dict: Dict[str, Any]):
        """Method to instantiate an Entity from a Dict (JSON)"""

        entity_attributes = cls.__dataclass_fields__.keys()
        attributes_dict = {
            k: entity_dict[k]
            for k in entity_attributes
            if k != 'location'
        }

        if 'location' in entity_attributes:
            location = Location(lat=entity_dict['lat'], lng=entity_dict['lng'])

            return cls(**{**attributes_dict, **{'location': location}})

        return cls(**attributes_dict)
