"""Проверки порогов, порядка цен и независимого эталона."""
from itertools import combinations_with_replacement, product
from pathlib import Path
import random
import subprocess
import sys
import unittest

from problems.p006_trip_tariff.baseline_bruteforce import cheapest_tariffs_bruteforce
from problems.p006_trip_tariff.solution import cheapest_tariffs, solve

ROOT = Path(__file__).resolve().parents[1] / "problems/p006_trip_tariff"


class TripTariffTests(unittest.TestCase):
    def test_examples_and_cli(self):
        for source in sorted((ROOT / "examples").glob("*.in")):
            expected = source.with_suffix(".out").read_bytes()
            self.assertEqual(solve(source.read_bytes()), expected.decode().strip())
            result = subprocess.run(
                [sys.executable, str(ROOT / "solution.py")],
                input=source.read_bytes(), capture_output=True, check=True,
            )
            self.assertEqual(result.stdout, expected)

    def test_equal_threshold_and_unsorted_prices(self):
        tariffs = [(3, 100), (3, 70), (8, 90), (9, 80)]
        self.assertEqual(cheapest_tariffs(tariffs, iter([4, 3, 10, 1])), [80, 70, -1, 70])
        self.assertEqual(tariffs, [(3, 100), (3, 70), (8, 90), (9, 80)])

    def test_exhaustive_small_catalogs(self):
        for size in range(1, 5):
            for limits in combinations_with_replacement(range(1, 4), size):
                for prices in product(range(3), repeat=size):
                    tariffs = list(zip(limits, prices))
                    trips = range(1, 5)
                    self.assertEqual(
                        cheapest_tariffs(tariffs, trips),
                        cheapest_tariffs_bruteforce(tariffs, trips),
                    )

    def test_random_differential(self):
        rng = random.Random(6)
        for _ in range(1000):
            tariffs = sorted(
                ((rng.randint(1, 20), rng.randint(0, 100))
                 for _ in range(rng.randint(1, 40))),
                key=lambda tariff: tariff[0],
            )
            trips = [rng.randint(1, 22) for _ in range(30)]
            self.assertEqual(
                cheapest_tariffs(tariffs, trips),
                cheapest_tariffs_bruteforce(tariffs, trips),
            )

    def test_large_catalog_and_batch(self):
        size = 200000
        tariffs = [(limit, limit) for limit in range(1, size + 1)]
        self.assertEqual(cheapest_tariffs(tariffs, range(size, 0, -1)),
                         list(range(size, 0, -1)))
