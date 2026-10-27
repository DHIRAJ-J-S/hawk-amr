"""Grid-based warehouse route planning for the HAWK simulator."""

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count

Position = tuple[int, int]


class NoRouteError(ValueError):
    """Raised when a route cannot be found on the configured warehouse map."""


@dataclass(frozen=True)
class WarehouseMap:
    width: int
    height: int
    start: Position
    obstacles: frozenset[Position]
    stations: dict[str, Position]

    def __post_init__(self) -> None:
        if self.width < 1 or self.height < 1:
            raise ValueError("warehouse width and height must be positive")
        self.validate_position(self.start)
        for point in self.obstacles:
            self.validate_position(point)
        for name, point in self.stations.items():
            if not name:
                raise ValueError("station names must not be empty")
            self.validate_position(point)
            if point in self.obstacles:
                raise ValueError(f"station {name!r} is placed on an obstacle")
        if self.start in self.obstacles:
            raise ValueError("warehouse start is placed on an obstacle")

    def validate_position(self, point: Position) -> None:
        x, y = point
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"position {point} is outside the warehouse map")

    def station(self, name: str) -> Position:
        try:
            return self.stations[name]
        except KeyError as exc:
            raise ValueError(f"unknown warehouse station: {name}") from exc

    def render(self, route: tuple[Position, ...] = ()) -> str:
        """Return a compact ASCII view of the map and the supplied route."""
        route_cells = set(route)
        end = route[-1] if route else None
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                point = (x, y)
                if point in self.obstacles:
                    symbol = "#"
                elif point == self.start:
                    symbol = "S"
                elif point == end and point != self.start:
                    symbol = "E"
                elif point in route_cells:
                    symbol = "*"
                else:
                    symbol = "."
                row.append(symbol)
            rows.append(" ".join(row))
        legend = ", ".join(
            f"{name}={point}" for name, point in sorted(self.stations.items())
        )
        return "\n".join(rows) + (f"\nStations: {legend}" if legend else "")


class AStarPlanner:
    """Finds shortest four-direction paths around blocked grid cells."""

    def __init__(self, warehouse: WarehouseMap):
        self.warehouse = warehouse

    def find_path(self, start: Position, goal: Position) -> tuple[Position, ...]:
        self.warehouse.validate_position(start)
        self.warehouse.validate_position(goal)
        if start in self.warehouse.obstacles or goal in self.warehouse.obstacles:
            raise NoRouteError("route start and destination must be clear cells")
        if start == goal:
            return (start,)

        sequence = count()
        frontier: list[tuple[int, int, Position]] = []
        heappush(frontier, (self._heuristic(start, goal), next(sequence), start))
        came_from: dict[Position, Position | None] = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, _, current = heappop(frontier)
            if current == goal:
                return self._reconstruct(came_from, goal)

            for neighbor in self._neighbors(current):
                new_cost = cost_so_far[current] + 1
                if new_cost >= cost_so_far.get(neighbor, 1 << 60):
                    continue
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
                priority = new_cost + self._heuristic(neighbor, goal)
                heappush(frontier, (priority, next(sequence), neighbor))

        raise NoRouteError(f"no route found from {start} to {goal}")

    def _neighbors(self, point: Position) -> tuple[Position, ...]:
        x, y = point
        candidates = ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))
        return tuple(
            candidate for candidate in candidates
            if 0 <= candidate[0] < self.warehouse.width
            and 0 <= candidate[1] < self.warehouse.height
            and candidate not in self.warehouse.obstacles
        )

    @staticmethod
    def _heuristic(start: Position, goal: Position) -> int:
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    @staticmethod
    def _reconstruct(
        came_from: dict[Position, Position | None], goal: Position
    ) -> tuple[Position, ...]:
        path = []
        current: Position | None = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        return tuple(reversed(path))
