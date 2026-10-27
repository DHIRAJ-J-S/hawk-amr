import unittest

from hawk_amr.models import InventoryRecord, Task
from hawk_amr.navigation import AStarPlanner, WarehouseMap
from hawk_amr.robot import HAWKRobot, TaskValidationError


class HAWKRobotTests(unittest.TestCase):
    def setUp(self):
        self.inventory = [
            InventoryRecord("BOX-1", "A-01", 3, "qr"),
            InventoryRecord("PART-2", "B-02", 5, "rfid"),
        ]
        self.robot = HAWKRobot(self.inventory, max_load_kg=50)

    def test_scan_returns_records_for_requested_location(self):
        result = self.robot.execute(Task("scan-1", "inventory_scan", "drone", location="A-01"))
        self.assertEqual([row.sku for row in result.records], ["BOX-1"])
        self.assertEqual(result.status, "simulated")

    def test_scan_with_no_match_returns_empty_list(self):
        result = self.robot.execute(Task("scan-empty", "inventory_scan", "drone", location="Z-99"))
        self.assertEqual(result.records, ())

    def test_scan_requires_drone(self):
        with self.assertRaises(TaskValidationError):
            self.robot.execute(Task("bad-scan", "inventory_scan", "forklift", location="A-01"))

    def test_pallet_move_within_limit_is_accepted_by_simulator(self):
        result = self.robot.execute(Task("move-1", "pallet_move", "forklift", load_kg=50))
        self.assertEqual(result.load_kg, 50)

    def test_pallet_move_over_limit_is_rejected(self):
        with self.assertRaises(TaskValidationError):
            self.robot.execute(Task("move-heavy", "pallet_move", "forklift", load_kg=50.1))

    def test_pallet_move_requires_positive_load(self):
        with self.assertRaises(TaskValidationError):
            self.robot.execute(Task("move-zero", "pallet_move", "forklift", load_kg=0))

    def test_unknown_operation_is_rejected(self):
        with self.assertRaises(TaskValidationError):
            self.robot.execute(Task("unknown", "unknown", "drone"))

    def test_mapped_scan_plans_route_and_updates_robot_position(self):
        warehouse = WarehouseMap(
            width=4,
            height=3,
            start=(0, 0),
            obstacles=frozenset({(1, 0)}),
            stations={"A-01": (3, 0)},
        )
        robot = HAWKRobot(self.inventory, planner=AStarPlanner(warehouse))
        result = robot.execute(Task("scan-route", "inventory_scan", "drone", location="A-01"))
        self.assertEqual(result.route[0], (0, 0))
        self.assertEqual(result.route[-1], (3, 0))
        self.assertEqual(result.distance_cells, len(result.route) - 1)
        self.assertEqual(robot.position, (3, 0))

    def test_mapped_pallet_move_routes_through_pickup_and_dropoff(self):
        warehouse = WarehouseMap(
            width=5,
            height=3,
            start=(0, 0),
            obstacles=frozenset(),
            stations={"receiving": (1, 1), "shipping": (4, 2)},
        )
        robot = HAWKRobot(self.inventory, planner=AStarPlanner(warehouse))
        task = Task(
            "move-route", "pallet_move", "forklift", load_kg=20,
            pickup_station="receiving", dropoff_station="shipping",
        )
        result = robot.execute(task)
        self.assertEqual(result.route[0], (0, 0))
        self.assertIn((1, 1), result.route)
        self.assertEqual(result.route[-1], (4, 2))
        self.assertEqual(robot.position, (4, 2))


if __name__ == "__main__":
    unittest.main()
