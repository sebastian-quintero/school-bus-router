import argparse

from constraints.capacity_constraint import CapacityConstraint
from estimators.linear_estimator import LinearEstimator
from optimization_model.optimization_model_builder import \
    OptimizationModelBuilder
from problem.problem_builder import ProblemBuilder
from router import Router
from utils.file_utils import read_entities, write_routes
from utils.logging_utils import configure_logs

"""Main method to execute the Router"""

# CLI parsing
parser = argparse.ArgumentParser(description='Route some school buses.')
parser.add_argument(
    '--input-dir',
    type=str,
    help='Directory for reading the Input. Default is ./input',
    default='./input'
)
parser.add_argument(
    '--output-dir',
    type=str,
    help='Directory for reading the Output. Default is ./output',
    default='./output',
)
args = parser.parse_args()
input_dir = args.input_dir
output_dir = args.output_dir

# Method execution
configure_logs()
riders, vehicles, depots, params = read_entities(input_dir)
estimator = LinearEstimator()
problem_builder = ProblemBuilder(params=params, estimator=estimator)
optimization_model_builder = OptimizationModelBuilder(
    constraints=[CapacityConstraint()]
)
router = Router(
    problem_builder=problem_builder,
    optimization_model_builder=optimization_model_builder
)
routes = router.route(riders, vehicles, depots)
write_routes(output_dir, routes)
