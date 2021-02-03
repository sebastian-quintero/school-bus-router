import logging
from collections import defaultdict
from typing import List, Dict, Tuple

from estimators.estimator import Estimator
from models.depot import Depot
from models.params import Params
from models.rider import Rider
from models.stop import Stop
from models.vehicle import Vehicle
from problem.problem import Problem


class ProblemBuilder:
    """A class to build a Routing Problem"""

    def __init__(self, params: Params, estimator: Estimator):
        self._params = params
        self._estimator = estimator

    def build(
            self,
            riders: Dict[str, Rider],
            vehicles: Dict[str, Vehicle],
            depots: Dict[str, Depot]
    ) -> Problem:
        """Method to build a VRP from Riders and Vehicles"""

        starts, ends = self._build_vehicles_starts_ends(vehicles, depots)
        stops = self._build_stops(riders, depots, starts, ends)
        estimations = self._estimator.estimate(stops)

        return Problem(
            depots=depots,
            ends=ends,
            estimations=estimations,
            params=self._params,
            riders=riders,
            starts=starts,
            stops=stops,
            vehicles=vehicles
        )

    def _build_stops(
            self,
            riders: Dict[str, Rider],
            depots: Dict[str, Depot],
            starts: List[int],
            ends: List[int]
    ) -> List[Stop]:
        """Method to build Stops from locations of Riders and Depots"""

        stop_groups = defaultdict(list)
        for rider_id, rider in riders.items():
            geohash = rider.location.extract_geohash(
                precision=self._params.GEOHASH_PRECISION_GROUPING
            )
            stop_groups[geohash] += [rider_id]

        stops = [
            Stop(riders={rider_id: riders[rider_id] for rider_id in rider_ids})
            for rider_ids in stop_groups.values()
        ]
        logging.info(
            f'Built {len(stops)} rider stops from {len(riders)} riders.'
        )
        depot_stops = [
            Stop(depot_id=depot.depot_id, location=depot.location)
            for depot_ix, depot in enumerate(depots.values())
            if depot_ix in starts or depot_ix in ends
        ]
        logging.info(
            f'Built {len(depot_stops)} depot stops from {len(depots)} depots.'
        )

        return depot_stops + stops

    @staticmethod
    def _build_vehicles_starts_ends(
            vehicles: Dict[str, Vehicle],
            depots: Dict[str, Depot]
    ) -> Tuple[List[int], List[int]]:
        """Method to build lists with the start and end depots"""

        depot_keys = list(depots.keys())
        starts, ends = [None] * len(vehicles), [None] * len(vehicles)

        for vehicle_ix, vehicle in enumerate(vehicles.values()):
            starts[vehicle_ix] = depot_keys.index(vehicle.start)
            ends[vehicle_ix] = depot_keys.index(vehicle.end)

        logging.info(
            f'Built start and end locations from {len(vehicles)} vehicles and '
            f'{len(depots)} depots.'
        )

        return starts, ends
