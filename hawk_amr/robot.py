"""Simulated task behavior for the HAWK concept."""

import math

from .models import InventoryRecord, Task, TaskResult
from .navigation import AStarPlanner, Position


class TaskValidationError(ValueError):
    """Raised when a task is malformed or incompatible with its attachment."""


class HAWKRobot:
    """A deterministic simulator. This class never communicates with hardware."""

    def __init__(
        self,
        inventory: list[InventoryRecord],
        max_load_kg: float = 100.0,
        planner: AStarPlanner | None = None,
    ):
        if not math.isfinite(max_load_kg) or max_load_kg <= 0:
            raise ValueError("max_load_kg must be a finite positive number")
        self._inventory = tuple(inventory)
        self.max_load_kg = float(max_load_kg)
        self.planner = planner
        self.position: Position | None = planner.warehouse.start if planner else None

    def execute(self, task: Task) -> TaskResult:
        if not task.task_id:
            raise TaskValidationError("task_id must not be empty")
        if task.operation == "inventory_scan":
            if task.attachment != "drone":
                raise TaskValidationError("inventory_scan requires the drone attachment")
            if not task.location:
                raise TaskValidationError("inventory_scan requires a location")
            found = tuple(item for item in self._inventory if item.location == task.location)
            route = self._route_to_station(task.location)
            self._update_position(route)
            return TaskResult(
                task.task_id,
                "simulated",
                f"Found {len(found)} sample record(s)",
                records=found,
                route=route,
                distance_cells=max(0, len(route) - 1),
            )
        if task.operation == "pallet_move":
            if task.attachment != "forklift":
                raise TaskValidationError("pallet_move requires the forklift attachment")
            if task.load_kg is None or not math.isfinite(task.load_kg) or task.load_kg <= 0:
                raise TaskValidationError("pallet_move requires a finite positive load_kg")
            if task.load_kg > self.max_load_kg:
                raise TaskValidationError(
                    f"load_kg exceeds simulated limit of {self.max_load_kg:g} kg"
                )
            route = self._route_pallet_move(task)
            self._update_position(route)
            return TaskResult(
                task.task_id,
                "simulated",
                "Pallet move accepted by simulator",
                load_kg=task.load_kg,
                route=route,
                distance_cells=max(0, len(route) - 1),
            )
        raise TaskValidationError(f"unsupported operation: {task.operation}")

    def _route_to_station(self, station: str) -> tuple[Position, ...]:
        if self.planner is None or self.position is None:
            return ()
        return self.planner.find_path(self.position, self.planner.warehouse.station(station))

    def _route_pallet_move(self, task: Task) -> tuple[Position, ...]:
        if self.planner is None or self.position is None:
            return ()
        if not task.pickup_station or not task.dropoff_station:
            raise TaskValidationError(
                "mapped pallet_move requires pickup_station and dropoff_station"
            )
        pickup = self.planner.warehouse.station(task.pickup_station)
        dropoff = self.planner.warehouse.station(task.dropoff_station)
        to_pickup = self.planner.find_path(self.position, pickup)
        to_dropoff = self.planner.find_path(pickup, dropoff)
        return to_pickup + to_dropoff[1:]

    def _update_position(self, route: tuple[Position, ...]) -> None:
        if route and self.planner is not None:
            self.position = route[-1]
