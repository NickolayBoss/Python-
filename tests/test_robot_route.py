"""Проверка стоимости и маршрута, включая независимый Bellman–Ford."""

from itertools import product
from pathlib import Path
import random
import subprocess
import sys
import unittest

from problems.p002_robot_route.baseline_dijkstra import minimum_cost_dijkstra
from problems.p002_robot_route.solution import find_route, solve

PROBLEM = Path(__file__).resolve().parents[1] / "problems" / "p002_robot_route"


def bellman_ford(grid, start, target):
    """Малый эталон: явный граф и полные релаксации без очереди приоритетов."""
    vertices = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] != "#"]
    distances = {v: float("inf") for v in vertices}
    distances[start] = 0
    edges = []
    for r, c in vertices:
        for nr, nc, symbol in ((r - 1, c, "U"), (r + 1, c, "D"), (r, c - 1, "L"), (r, c + 1, "R")):
            if (nr, nc) in distances:
                edges.append(((r, c), (nr, nc), int(grid[r][c] != symbol)))
    for _ in range(len(vertices) - 1):
        changed = False
        for source, destination, weight in edges:
            candidate = distances[source] + weight
            if candidate < distances[destination]:
                distances[destination] = candidate
                changed = True
        if not changed:
            break
    value = distances[target]
    return -1 if value == float("inf") else value


class RobotRouteTests(unittest.TestCase):
    def check_route(self, grid, start, target, expected):
        cost, path = find_route(grid, start, target)
        self.assertEqual(cost, expected, (grid, start, target))
        if expected == -1:
            self.assertEqual(path, [])
            return
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], target)
        self.assertEqual(len(path), len(set(path)), "Маршрут не должен содержать цикл")
        self.assertLessEqual(len(path), len(grid) * len(grid[0]))
        actual_cost = 0
        directions = {(-1, 0): "U", (1, 0): "D", (0, -1): "L", (0, 1): "R"}
        for r, c in path:
            self.assertTrue(0 <= r < len(grid) and 0 <= c < len(grid[0]))
            self.assertNotEqual(grid[r][c], "#")
        for (r, c), (nr, nc) in zip(path, path[1:]):
            self.assertIn((nr - r, nc - c), directions)
            actual_cost += grid[r][c] != directions[(nr - r, nc - c)]
        self.assertEqual(actual_cost, cost)

    def test_examples_and_cli(self):
        for source in sorted((PROBLEM / "examples").glob("*.in")):
            expected = source.with_suffix(".out").read_text().strip()
            self.assertEqual(solve(source.read_bytes()), expected)
            result = subprocess.run([sys.executable, str(PROBLEM / "solution.py")], input=source.read_bytes(), capture_output=True, check=True)
            self.assertEqual(result.stdout.decode().strip(), expected)
            self.assertEqual(result.stderr, b"")

    def test_same_start_and_target(self):
        self.check_route(["U"], (0, 0), (0, 0), 0)

    def test_direction_is_from_departure_cell(self):
        self.check_route(["RR"], (0, 0), (0, 1), 0)
        self.check_route(["RR"], (0, 1), (0, 0), 1)

    def test_cheapest_route_is_longer(self):
        grid = ["RRD", "ULL"]
        self.check_route(grid, (0, 0), (1, 0), 0)
        self.assertEqual(len(find_route(grid, (0, 0), (1, 0))[1]), 6)

    def test_unreachable(self):
        self.check_route(["R#L"], (0, 0), (0, 2), -1)

    def test_zero_cost_cycle(self):
        self.check_route(["RDR", "ULU"], (0, 0), (0, 2), 1)

    def test_improvement_after_first_discovery(self):
        # Прямой переход вниз стоит 1, обход вокруг квадрата стоит 0.
        self.check_route(["RD", "UL"], (0, 0), (1, 0), 0)

    def test_equal_cost_routes(self):
        self.check_route(["UU", "UU"], (0, 0), (1, 1), 2)

    def test_column_and_boundary_arrows(self):
        self.check_route(["U", "U", "D"], (0, 0), (2, 0), 2)
        self.check_route(["U", "U", "D"], (2, 0), (0, 0), 1)

    def test_inputs_unchanged(self):
        grid = ["RD", "UL"]
        find_route(grid, (0, 0), (1, 0))
        self.assertEqual(grid, ["RD", "UL"])

    def test_exhaustive_two_by_two(self):
        # 5^4 полей, все пары проходимых стартов и целей.
        for flat in product("UDLR#", repeat=4):
            grid = ["".join(flat[:2]), "".join(flat[2:])]
            cells = [(r, c) for r in range(2) for c in range(2) if grid[r][c] != "#"]
            for start in cells:
                for target in cells:
                    self.check_route(grid, start, target, bellman_ford(grid, start, target))

    def test_random_differential(self):
        rng = random.Random(20261110)
        for _ in range(1000):
            rows, cols = rng.randint(1, 7), rng.randint(1, 7)
            grid = ["".join(rng.choice("UDLR#") for _ in range(cols)) for _ in range(rows)]
            cells = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] != "#"]
            if not cells:
                grid[0] = "R" + grid[0][1:]
                cells = [(0, 0)]
            start, target = rng.choice(cells), rng.choice(cells)
            self.check_route(grid, start, target, minimum_cost_dijkstra(grid, start, target))

    def test_large_nonrecursive_path(self):
        size = 200000
        cost, path = find_route(["R" * size], (0, 0), (0, size - 1))
        self.assertEqual(cost, 0)
        self.assertEqual(len(path), size)
        self.assertEqual((path[0], path[-1]), ((0, 0), (0, size - 1)))


if __name__ == "__main__":
    unittest.main()
