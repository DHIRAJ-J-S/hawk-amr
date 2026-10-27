# HAWK software architecture

## Scope

This repository is a software-only reference simulator. It represents the HAWK concept from the SIH deck: a warehouse AMR that can use an aerial QR/RFID scan workflow and a front forklift workflow. It does not implement the sensing, control, autonomy, or safety systems required on a physical robot.

## Components

```text
JSON mission -> CLI/parser -> Task model -> HAWKRobot simulator
                                      |-- A* route planner on warehouse grid
                                      |-- inventory scan (simulated records)
                                      `-- pallet move (simulated load limit)
```

- `hawk_amr.models`: task, attachment, inventory, route, and result data structures.
- `hawk_amr.navigation`: warehouse grid validation, deterministic A* path planning, and ASCII map rendering.
- `hawk_amr.robot`: attachment/load validation, simulated task execution, and robot position tracking between tasks.
- `hawk_amr.cli`: reads a JSON mission, executes tasks in order, and prints JSON results. `--show-map` draws the route over the configured static map.
- `data/`: example tasks and inventory records; values are fabricated for demonstration.
- `tests/`: standard-library unit tests for validation and task behavior.

## Task flow

1. The mission JSON defines a grid, blocked cells, named stations, inventory records, and an ordered task list.
2. A task states its operation and required attachment. The simulator validates the attachment and required fields before changing its position.
3. A* finds a shortest four-direction path from the robot's current cell to the target. A pallet move plans a leg to pickup and another leg to drop-off.
4. A scan returns matching records from the in-memory sample dataset. A pallet move checks the supplied load against a configured example limit.
5. The CLI reports the route, distance in grid steps, and result. No physical command is emitted.

## Proposed hardware integration boundary

The SIH concept names LiDAR, camera, IMU, wheel encoders, a drone dock, QR/RFID scanning, forklift actuator and load sensing, motor drivers, battery management, Wi-Fi, ROS 2 navigation, and a dashboard. None is integrated in this reference. A future system should separate ROS 2 adapters and hardware drivers from task policy, validate timestamps and sensor health, and require a safety controller to gate motion and lifting. The simulator's validation is not a substitute for collision avoidance, a safety-rated stop, a risk assessment, or supervised commissioning.

## Data contracts

Tasks use `operation` values `inventory_scan` or `pallet_move`. Scans include a `location` station; pallet moves include `load_kg`, `pickup_station`, and `dropoff_station` when a map is configured. `attachment` must be `drone` for scans or `forklift` for pallet moves. Warehouse positions are `[x, y]`; movement is limited to adjacent horizontal or vertical cells. Invalid map coordinates, blocked destinations, unknown stations, and unreachable routes fail with a clear error. See `data/sample_tasks.json`.

## Known gaps

- The map is static and grid-based; there is no localization, live obstacle detection, or fleet coordination.
- No real QR/RFID sensor integration or persistence layer.
- No real drone launch, landing, interlocks, payload control, or flight authorization.
- No physical forklift or motor control, braking model, or safety-rated subsystem.
- No validated performance, payload, battery, or operating-area claims.

Treat all outputs as simulated examples. Do not connect this reference to actuators.
