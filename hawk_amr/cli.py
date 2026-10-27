"""Command-line entry point for the HAWK concept simulator."""

import argparse
import json
import sys
from pathlib import Path

from .models import InventoryRecord, Task
from .navigation import AStarPlanner, WarehouseMap
from .robot import HAWKRobot


def load_tasks(path: Path) -> tuple[HAWKRobot, list[Task]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    inventory = [InventoryRecord(**item) for item in payload.get("inventory", [])]
    limits = payload.get("simulated_limits", {})
    planner = None
    if "warehouse" in payload:
        config = payload["warehouse"]
        warehouse = WarehouseMap(
            width=config["width"],
            height=config["height"],
            start=tuple(config["start"]),
            obstacles=frozenset(tuple(point) for point in config.get("obstacles", [])),
            stations={name: tuple(point) for name, point in config["stations"].items()},
        )
        planner = AStarPlanner(warehouse)
    robot = HAWKRobot(
        inventory,
        max_load_kg=limits.get("max_load_kg", 100.0),
        planner=planner,
    )
    tasks = [
        Task(task_id=item["id"], **{k: v for k, v in item.items() if k != "id"})
        for item in payload["tasks"]
    ]
    return robot, tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a HAWK warehouse mission simulation.")
    parser.add_argument("tasks", type=Path, help="path to a mission JSON file")
    parser.add_argument("--show-map", action="store_true", help="draw the map and planned mission route")
    args = parser.parse_args()
    try:
        robot, tasks = load_tasks(args.tasks)
        complete_route = []
        for task in tasks:
            result = robot.execute(task)
            if result.route:
                complete_route.extend(result.route if not complete_route else result.route[1:])
            print(json.dumps({
                "task_id": result.task_id,
                "status": result.status,
                "message": result.message,
                "records": [record.__dict__ for record in result.records],
                "load_kg": result.load_kg,
                "route": [list(point) for point in result.route],
                "distance_cells": result.distance_cells,
            }))
        if args.show_map and robot.planner is not None:
            print("\nMission route (* = traveled, S = start, E = finish, # = obstacle):")
            print(robot.planner.warehouse.render(tuple(complete_route)))
        elif args.show_map:
            print("No warehouse map is configured in this mission.", file=sys.stderr)
            return 2
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
