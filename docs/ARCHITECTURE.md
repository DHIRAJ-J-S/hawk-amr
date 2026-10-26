# HAWK software architecture

## Scope

This repository is a software-only reference simulator. It represents the HAWK concept from the SIH deck: a warehouse AMR that can use an aerial QR/RFID scan workflow and a front forklift workflow. It does not implement the sensing, control, autonomy, or safety systems required on a physical robot.

## Components

```text
JSON task file -> CLI/parser -> Task model -> HAWKRobot simulator
                                             |-- inventory scan (simulated records)
                                             `-- pallet move (simulated load limit)
```

- `hawk_amr.models`: task, attachment, inventory, and event data structures.
- `hawk_amr.robot`: validation and simulated task execution.
- `hawk_amr.cli`: reads a JSON task list, executes each task, and prints JSON results.
- `data/`: example tasks and inventory records; values are fabricated for demonstration.
- `tests/`: standard-library unit tests for validation and task behavior.

## Task flow

1. A task states its operation and required attachment.
2. The simulator checks that the attachment supports the operation.
3. A scan returns matching records from the in-memory sample dataset. A pallet move checks the supplied load against a configured limit.
4. The CLI reports a structured result. No physical command is emitted.

## Proposed hardware integration boundary

The SIH concept names LiDAR, camera, IMU, wheel encoders, a drone dock, QR/RFID scanning, forklift actuator and load sensing, motor drivers, battery management, Wi-Fi, ROS 2 navigation, and a dashboard. None is integrated in this reference. A future system should separate ROS 2 adapters and hardware drivers from task policy, validate timestamps and sensor health, and require a safety controller to gate motion and lifting. The simulator's validation is not a substitute for collision avoidance, a safety-rated stop, a risk assessment, or supervised commissioning.

## Data contracts

Tasks use `operation` values `inventory_scan` or `pallet_move`. Scans may include `location`; pallet moves include `load_kg`. `attachment` must be `drone` for scans or `forklift` for pallet moves. Invalid inputs fail with a clear error instead of silently selecting an attachment. See `data/sample_tasks.json`.

## Known gaps

- No map, localization, route planning, obstacle detection, or fleet coordination.
- No real QR/RFID sensor integration or persistence layer.
- No real drone launch, landing, interlocks, payload control, or flight authorization.
- No physical forklift or motor control, braking model, or safety-rated subsystem.
- No validated performance, payload, battery, or operating-area claims.

Treat all outputs as simulated examples. Do not connect this reference to actuators.
