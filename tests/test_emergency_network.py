"""Граничные, исчерпывающие и воспроизводимые дифференциальные тесты."""

import itertools
from pathlib import Path
import random
import subprocess
import sys
import unittest

from problems.p001_emergency_network.baseline_bfs import analyze_network_bfs
from problems.p001_emergency_network.solution import DisjointSetUnion, analyze_network, solve

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "problems" / "p001_emergency_network"


class NetworkTests(unittest.TestCase):
    def test_examples(self):
        for source in sorted((PROBLEM / "examples").glob("*.in")):
            with self.subTest(source=source.name):
                self.assertEqual(solve(source.read_bytes()), source.with_suffix(".out").read_text().strip())

    def test_single_cell_and_equality(self):
        self.assertEqual(analyze_network([[5]], [6, 5, 0, 5]), [(0, 0), (1, 1), (1, 1), (1, 1)])

    def test_diagonals_are_not_edges(self):
        self.assertEqual(analyze_network([[5, 0], [0, 5]], [5]), [(2, 1)])

    def test_bridge_merges_components(self):
        self.assertEqual(analyze_network([[9, 3, 8]], [9, 8, 3]), [(1, 1), (2, 1), (1, 3)])

    def test_column(self):
        self.assertEqual(analyze_network([[9], [3], [8]], [8, 3]), [(2, 1), (1, 3)])

    def test_equal_values_and_cycle(self):
        self.assertEqual(analyze_network([[4, 4], [4, 4]], [5, 4, 4]), [(0, 0), (1, 4), (1, 4)])

    def test_extreme_values(self):
        self.assertEqual(analyze_network([[0, 10**9]], [10**9 + 1, 10**9, 0]), [(0, 0), (1, 1), (1, 2)])

    def test_inputs_unchanged(self):
        grid, queries = [[2, 1]], [0, 3, 1]
        analyze_network(grid, queries)
        self.assertEqual((grid, queries), ([[2, 1]], [0, 3, 1]))

    def test_duplicate_union(self):
        dsu = DisjointSetUnion(3)
        for cell in range(3):
            dsu.activate(cell)
        dsu.union(0, 1)
        dsu.union(1, 0)
        self.assertEqual((dsu.components, dsu.largest), (2, 2))
        dsu.union(2, 1)
        self.assertEqual((dsu.components, dsu.largest), (1, 3))

    def test_exhaustive_small_grids(self):
        queries = [3, 2, 1, 0, 2]
        for flat in itertools.product(range(3), repeat=6):
            grid = [list(flat[:3]), list(flat[3:])]
            self.assertEqual(analyze_network(grid, queries), analyze_network_bfs(grid, queries), grid)

    def test_random_differential(self):
        rng = random.Random(20261109)
        for case in range(1000):
            rows, cols = rng.randint(1, 7), rng.randint(1, 7)
            grid = [[rng.randint(0, 12) for _ in range(cols)] for _ in range(rows)]
            queries = [rng.randint(0, 14) for _ in range(rng.randint(1, 20))]
            self.assertEqual(analyze_network(grid, queries), analyze_network_bfs(grid, queries), f"case={case}")

    def test_monotonic_largest(self):
        grid = [[8, 1, 7], [2, 4, 3]]
        sizes = [size for _, size in analyze_network(grid, list(range(10, -1, -1)))]
        self.assertEqual(sizes, sorted(sizes))

    def test_cli(self):
        for filename in ("solution.py", "baseline_bfs.py"):
            result = subprocess.run([sys.executable, str(PROBLEM / filename)], input=(PROBLEM / "examples/01.in").read_bytes(), capture_output=True, check=True)
            self.assertEqual(result.stdout, (PROBLEM / "examples/01.out").read_bytes())
            self.assertEqual(result.stderr, b"")

    def test_large_uniform(self):
        grid = [[7] * 500 for _ in range(400)]
        self.assertEqual(analyze_network(grid, [8, 7, 0]), [(0, 0), (1, 200000), (1, 200000)])


if __name__ == "__main__":
    unittest.main()
