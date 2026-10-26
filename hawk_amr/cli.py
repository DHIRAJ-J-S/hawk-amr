"""Command-line entry point for the HAWK concept simulator."""

import json
import sys
from pathlib import Path

from .models import InventoryRecord, Task
from .robot import HAWKRobot


def load_tasks(path: Path) -> tuple[HAWKRobot, list[Task]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    inventory = [InventoryRecord(**item) for item in payload.get("inventory", [])]
    limits = payload.get("simulated_limits", {})
    robot = HAWKRobot(inventory, max_load_kg=limits.get("max_load_kg", 100.0))
    tasks = [Task(task_id=item["id"], **{k: v for k, v in item.items() if k != "id"})
             for item in payload["tasks"]]
    return robot, tasks


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m hawk_amr.cli <tasks.json>", file=sys.stderr)
        return 2
    try:
        robot, tasks = load_tasks(Path(sys.argv[1]))
        for task in tasks:
            result = robot.execute(task)
            print(json.dumps({
                "task_id": result.task_id,
                "status": result.status,
                "message": result.message,
                "records": [record.__dict__ for record in result.records],
                "load_kg": result.load_kg,
            }))
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
