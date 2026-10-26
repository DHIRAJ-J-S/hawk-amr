"""Safe-by-default simulated task behavior for the HAWK concept."""

from .models import InventoryRecord, Task, TaskResult


class TaskValidationError(ValueError):
    """Raised when a task is malformed or incompatible with its attachment."""


class HAWKRobot:
    """A deterministic simulator. This class never communicates with hardware."""

    def __init__(self, inventory: list[InventoryRecord], max_load_kg: float = 100.0):
        if max_load_kg <= 0:
            raise ValueError("max_load_kg must be positive")
        self._inventory = tuple(inventory)
        self.max_load_kg = float(max_load_kg)

    def execute(self, task: Task) -> TaskResult:
        if not task.task_id:
            raise TaskValidationError("task_id must not be empty")
        if task.operation == "inventory_scan":
            if task.attachment != "drone":
                raise TaskValidationError("inventory_scan requires the drone attachment")
            if not task.location:
                raise TaskValidationError("inventory_scan requires a location")
            found = tuple(item for item in self._inventory if item.location == task.location)
            return TaskResult(task.task_id, "simulated", f"Found {len(found)} sample record(s)", found)
        if task.operation == "pallet_move":
            if task.attachment != "forklift":
                raise TaskValidationError("pallet_move requires the forklift attachment")
            if task.load_kg is None or task.load_kg <= 0:
                raise TaskValidationError("pallet_move requires a positive load_kg")
            if task.load_kg > self.max_load_kg:
                raise TaskValidationError(
                    f"load_kg exceeds simulated limit of {self.max_load_kg:g} kg"
                )
            return TaskResult(task.task_id, "simulated", "Pallet move accepted by simulator", load_kg=task.load_kg)
        raise TaskValidationError(f"unsupported operation: {task.operation}")
