from ortools.constraint_solver.pywrapcp import RoutingModel

from constraints.constraint import Constraint


class CapacityConstraint(Constraint):
    """Class that restricts the number of Riders assigned to each Vehicle"""

    def _callback(self, from_index: int):
        """Callback to obtain the demand at a Stop"""

        from_node = self.manager.IndexToNode(from_index)

        return self.problem.stops[from_node].demand

    def apply(self, solver: RoutingModel):
        """Vehicle's occupation is restricted based on demand"""

        callback_index = solver.RegisterUnaryTransitCallback(self._callback)
        solver.AddDimensionWithVehicleCapacity(
            evaluator_index=callback_index,
            slack_max=0,
            vehicle_capacities=[
                vehicle.capacity
                for vehicle in self.problem.vehicles.values()
            ],
            fix_start_cumul_to_zero=True,
            name='capacity_constraint'
        )
