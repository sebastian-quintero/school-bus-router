# school-bus-router

This service routes school buses to deliver riders.
Buses depart from the school and may finish the tour at either the school or optional parking lots.
It obtains heuristic routes, solving the CVRP (Capacitated Vehicle Routing Problem).

## Set Up

This project uses Python. 
Start by creating a virtual environment (or conda environment).

Install the project requirements.

```shell
pip install -r requirements.txt
```

Run unit tests (and create a coverage report).

```shell
coverage run -m unittest discover
```

Get the coverage report.

```shell
coverage report -m
```

Perform code linting (style check).

```shell
flake8 .
```

## Usage

To run the project, pass two arguments: the input dir and output dir.

```shell
python3 main.py --input-dir ./input --output-dir ./output
```

The following input files should be set up in the input dir.

- `riders.json` => Information regarding riders: id's and drop-off location.
```json
[
    {
        "rider_id": "Forrest Gump",
        "lat": 4.720634,
        "lng": -74.037228
    },
    ...
]
```

- `depots.json` => Information regarding depots (school and optional parking lots): id's and location.
```json
[
    {
        "depot_id": "school",
        "lat": 4.809486,
        "lng": -74.070967
    },
    ...
]
```

- `vehicles.json` => Information regarding school buses: id's, capacity, start and end location.
```json
[
    {
        "capacity": 4,
        "start": "school",
        "end": "school",
        "vehicle_id": "magic_school_bus"
    },
    ...
]
```

- `params.json` => Information regarding service params. Full list in `./models/params.py`.
```json
{
    "GEOHASH_PRECISION_GROUPING": 8,
    "FIRST_SOLUTION_STRATEGY": "AUTOMATIC",
    "SEARCH_METAHEURISTIC": "AUTOMATIC",
    "SEARCH_TIME_LIMIT": 4,
    "SEARCH_SOLUTIONS_LIMIT": 3000,
    ...
}
```

Usage description.

```shell
usage: main.py [-h] [--input-dir INPUT_DIR] [--output-dir OUTPUT_DIR]

Route some school buses.

optional arguments:
  -h, --help            show this help message and exit
  --input-dir INPUT_DIR
                        Directory for reading the Input. Default is ./input
  --output-dir OUTPUT_DIR
                        Directory for reading the Output. Default is ./output
```
