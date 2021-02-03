from typing import Dict, Any, List, Union

from models.depot import Depot
from models.params import Params
from models.rider import Rider
from models.vehicle import Vehicle


def parse_models(
        model_dicts: List[Dict[str, Any]],
        cls: Union[Rider, Depot, Vehicle]
) -> Dict[str, Union[Rider, Depot, Vehicle]]:
    """Method to obtain a Rider, Depot or Vehicle from the input"""

    return {
        model_dict[[k for k in model_dict.keys() if 'id' in k][0]]:
            cls.from_dict(model_dict)
        for model_dict in model_dicts
    }


def get_params() -> Params:
    """Method to obtain a set of Params"""

    return Params()
