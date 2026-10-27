import unittest

from hawk_amr.navigation import AStarPlanner, NoRouteError, WarehouseMap


class AStarPlannerTests(unittest.TestCase):
    def setUp(self):
        self.warehouse = WarehouseMap(
            width=5,
            height=4,
            start=(0, 0),
            obstacles=frozenset({(1, 0), (1, 1), (1, 2)}),
            stations={"goal": (2, 0)},
        )
        self.planner = AStarPlanner(self.warehouse)

    def test_route_goes_around_obstacle_and_is_shortest(self):
        route = self.planner.find_path((0, 0), (2, 0))
        self.assertEqual(route[0], (0, 0))
        self.assertEqual(route[-1], (2, 0))
        self.assertEqual(len(route) - 1, 8)
        self.assertTrue(all(cell not in self.warehouse.obstacles for cell in route))

    def test_start_equal_to_goal_returns_single_cell(self):
        self.assertEqual(self.planner.find_path((0, 0), (0, 0)), ((0, 0),))

    def test_fully_blocked_destination_reports_no_route(self):
        warehouse = WarehouseMap(
            width=3,
            height=3,
            start=(0, 0),
            obstacles=frozenset({(1, 0), (0, 1), (2, 1), (1, 2)}),
            stations={"goal": (1, 1)},
        )
        with self.assertRaises(NoRouteError):
            AStarPlanner(warehouse).find_path((0, 0), (1, 1))

    def test_out_of_bounds_position_is_rejected(self):
        with self.assertRaises(ValueError):
            self.planner.find_path((0, 0), (5, 0))


if __name__ == "__main__":
    unittest.main()
