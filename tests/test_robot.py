import unittest

from hawk_amr.models import InventoryRecord, Task
from hawk_amr.robot import HAWKRobot, TaskValidationError


class HAWKRobotTests(unittest.TestCase):
    def setUp(self):
        self.robot = HAWKRobot([
            InventoryRecord("BOX-1", "A-01", 3, "qr"),
            InventoryRecord("PART-2", "B-02", 5, "rfid"),
        ], max_load_kg=50)

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


if __name__ == "__main__":
    unittest.main()
