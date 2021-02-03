import json
import logging
import os
from typing import Tuple, Dict, List, Any

from models.depot import Depot
from models.params import Params
from models.rider import Rider
from models.vehicle import Vehicle
from settings import RIDERS_FILE, VEHICLES_FILE, DEPOTS_FILE, PARAMS_FILE, \
    ROUTES_FILE


def read_entities(input_dir: str) -> Tuple[
    Dict[str, Rider],
    Dict[str, Vehicle],
    Dict[str, Depot],
    Params
]:
    """Method to parse the Riders, Vehicles and Depots from JSON to Dict"""

    riders_file = RIDERS_FILE.format(input_dir=input_dir)
    with open(riders_file) as f:
        logging.info(f'Read riders from {riders_file}.')
        riders_dicts = json.load(f)
    riders = {
        r_dict['rider_id']: Rider.from_dict(r_dict)
        for r_dict in riders_dicts
    }
    logging.info(f'Successfully parsed {len(riders)} riders.')

    vehicles_file = VEHICLES_FILE.format(input_dir=input_dir)
    with open(vehicles_file) as f:
        vehicles_dicts = json.load(f)
        logging.info(f'Read vehicles from {vehicles_file}.')
    vehicles = {
        v_dict['vehicle_id']: Vehicle.from_dict(v_dict)
        for v_dict in vehicles_dicts
    }
    logging.info(f'Successfully parsed {len(vehicles)} vehicles.')

    depots_file = DEPOTS_FILE.format(input_dir=input_dir)
    with open(depots_file) as f:
        depots_dicts = json.load(f)
        logging.info(f'Read depots from {depots_file}.')
    depots = {
        d_dict['depot_id']: Depot.from_dict(d_dict)
        for d_dict in depots_dicts
    }
    logging.info(f'Successfully parsed {len(depots)} depots.')

    params_file = PARAMS_FILE.format(input_dir=input_dir)
    with open(params_file) as f:
        logging.info(f'Read params from {params_file}.')
        params_dict = json.load(f)
    params = Params.from_dict(params_dict)
    logging.info(f'Successfully parsed {len(params_dict)} params.')

    return riders, vehicles, depots, params


def write_routes(output_dir: str, routes: List[Dict[str, Any]]):
    """Method to write the Routes (result) to the output file"""

    routes_file = ROUTES_FILE.format(output_dir=output_dir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    with open(routes_file, 'w') as f:
        logging.info(f'Wrote {len(routes)} routes to {routes_file}.')
        json.dump(routes, f, indent=4)
