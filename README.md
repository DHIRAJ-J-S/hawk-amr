# HAWK AMR

HAWK is a modular autonomous mobile robot concept for warehouse work. The proposed platform combines an indoor mobile robot with a drone dock for QR/RFID inventory scanning and a front forklift attachment for pallet movement. The concept also explores using the drone for disaster-response missions.

This repository contains a Python reference simulator for the warehouse workflows. It provides a small map, plans routes around blocked cells, runs inventory and pallet tasks in sequence, and prints the results. It is a software demonstration of the concept, not firmware for a physical robot.

**Repository:** [github.com/DHIRAJ-J-S/hawk-amr](https://github.com/DHIRAJ-J-S/hawk-amr)

## What is implemented

- **Warehouse map:** A rectangular grid with named stations and blocked cells that represent shelves or other obstacles.
- **A* path planning:** The planner finds a shortest route using horizontal and vertical moves. Every move costs one grid cell; diagonal travel is not allowed.
- **Mission state:** Tasks run in order. The robot's simulated position after one task becomes the starting position for the next task.
- **Inventory scan task:** A task assigned to the `drone` attachment returns the sample inventory records for its location.
- **Pallet move task:** A task assigned to the `forklift` attachment routes from the robot's current position to the pickup station, then to the drop-off station. The requested load is checked against a configurable example limit.
- **Input validation:** The simulator checks attachment/task compatibility, positive load values, map bounds, station names, and whether a route is possible.
- **Readable output:** Each task prints a JSON result with its status, message, route, distance, and any matching inventory records. The `--show-map` option draws the complete route in the terminal.

All records, obstacles, and load limits in the sample mission are demonstration data. No hardware commands are sent.

## Requirements

- Python 3.10 or newer
- Git to clone the repository
- No third-party Python packages

## Setup and run

Clone the repository and enter its directory:

```bash
git clone https://github.com/DHIRAJ-J-S/hawk-amr.git
cd hawk-amr
```

Run the sample mission and draw the map:

```bash
python -m hawk_amr.cli data/sample_tasks.json --show-map
```

The sample mission contains three tasks:

1. Scan inventory location `A-01-02` using the drone attachment.
2. Move a simulated 45 kg pallet from `receiving` to `shipping` using the forklift attachment.
3. Scan inventory location `B-03-01`.

The simulator starts at grid position `[0, 0]`. It calculates a route to each task's station, prints one JSON object per task, then renders the combined route. In the map, `S` marks the start, `E` marks the finish, `#` marks a blocked cell, and `*` marks traveled cells. The station coordinates are printed below the map.

To run the unit tests:

```bash
python -m unittest discover -s tests -v
```

The test cases cover shortest-path behavior around obstacles, unreachable destinations, out-of-bounds coordinates, scan results, attachment checks, pallet load validation, and route state across tasks.

## Mission file format

The CLI reads one JSON mission file. `data/sample_tasks.json` is the complete working example. A mission can contain:

- `inventory`: sample records with `sku`, `location`, `quantity`, and `source` (`qr` or `rfid` in the example).
- `tasks`: ordered jobs. Each task has an `id`, `operation`, and `attachment`.
- `simulated_limits.max_load_kg`: maximum load accepted by this simulation.
- `warehouse`: grid dimensions, starting position, obstacles, and named station coordinates.

Coordinates are `[x, y]`, with `[0, 0]` at the top-left. `x` increases to the right and `y` increases downward. A route may move only one cell left, right, up, or down at a time.

### Inventory scan

An inventory scan uses the drone attachment and a `location` that matches both a named warehouse station and the `location` field in the inventory records:

```json
{"id": "scan-a-01", "operation": "inventory_scan", "attachment": "drone", "location": "A-01-02"}
```

The result contains all sample records whose location matches the task. If there are no matches, the scan returns an empty `records` array.

### Pallet move

A pallet move uses the forklift attachment, a positive `load_kg`, and named pickup and drop-off stations:

```json
{
  "id": "move-pallet-01",
  "operation": "pallet_move",
  "attachment": "forklift",
  "load_kg": 45.0,
  "pickup_station": "receiving",
  "dropoff_station": "shipping"
}
```

When a warehouse map is present, the route includes a path from the robot's current position to pickup and then a path from pickup to drop-off. A load greater than `simulated_limits.max_load_kg` is rejected. This value is only a simulator setting; it is not a payload rating for a real robot.

## Architecture

```text
Mission JSON
    │
    ▼
CLI parser ──► task and inventory models
                    │
                    ▼
               HAWKRobot ──► A* planner ──► grid route
                    │
                    ├──► sample inventory lookup
                    └──► pallet load check
                    │
                    ▼
          JSON task results + optional map
```

- `hawk_amr/models.py` defines the immutable inventory, task, and task-result records.
- `hawk_amr/navigation.py` validates the warehouse map, runs A* with Manhattan distance as its heuristic, reconstructs the route, and renders the ASCII map.
- `hawk_amr/robot.py` validates tasks, returns sample scan data, checks pallet loads, and carries the simulated position between jobs.
- `hawk_amr/cli.py` loads a JSON mission, executes its tasks in order, and prints task results.
- `data/sample_tasks.json` defines the map, sample inventory, and event demonstration mission.
- `tests/` contains standard-library unit tests for the route planner and task simulator.
- `docs/ARCHITECTURE.md` describes the software structure and integration boundaries. `docs/DEMO.md` provides a short walkthrough for presenting the mission.

## Repository layout

```text
hawk-amr/
├── data/
│   ├── README.md
│   └── sample_tasks.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEMO.md
│   └── PUBLISHING.md
├── hawk_amr/
│   ├── __init__.py
│   ├── cli.py
│   ├── models.py
│   ├── navigation.py
│   └── robot.py
├── tests/
│   ├── test_navigation.py
│   └── test_robot.py
├── LICENSE
└── README.md
```

## Current boundaries

The map is static, grid-based, and supplied in the mission file. The simulator does not include ROS 2, localization, live sensor input, dynamic obstacle avoidance, QR/RFID hardware, drone flight or docking controls, motor drivers, forklift actuators, battery management, or a dashboard. Those components would need to be designed and integrated before this software could control a physical AMR.

The STEP file available with the source material was a separate drone assembly, not HAWK AMR CAD, so it is not part of this repository. The presentation decks are also not included because their embedded media redistribution rights have not been confirmed.

## License

The code and documentation are available under the [MIT License](LICENSE).
