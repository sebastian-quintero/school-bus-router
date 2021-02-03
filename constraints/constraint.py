from dataclasses import dataclass
from typing import Optional

from ortools.constraint_solver.pywrapcp import RoutingIndexManager, \
    RoutingModel

from problem.problem import Problem


@dataclass
class Constraint:
    """Class that represents an Opt. Constraint to add to the Opt. Model"""

    problem: Optional[Problem] = None,
    manager: Optional[RoutingIndexManager] = None

    def _callback(self, *args):
        """Method to return a callback for the Constraint's quantity"""

        pass

    def apply(self, solver: RoutingModel):
        """Method where the constraint is applied to the solver"""

        pass
