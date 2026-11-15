from itertools import product
from pathlib import Path
import subprocess
import sys
import unittest

from problems.p007_budget_pairs.baseline_bruteforce import count_pairs_bruteforce
from problems.p007_budget_pairs.solution import count_pairs


class BudgetPairTests(unittest.TestCase):
    def test_small_catalogs_against_bruteforce(self):
        for size in range(7):
            for prices in product(range(3), repeat=size):
                for budget in range(5):
                    self.assertEqual(
                        count_pairs(prices, budget),
                        count_pairs_bruteforce(prices, budget),
                        (prices, budget),
                    )

    def test_large_catalog_with_equal_prices(self):
        self.assertEqual(count_pairs([10] * 200_000, 20), 19_999_900_000)

    def test_example_from_command_line(self):
        root = Path(__file__).resolve().parents[1]
        folder = root / "problems" / "p007_budget_pairs"
        result = subprocess.run(
            [sys.executable, str(folder / "solution.py")],
            input=(folder / "examples" / "01.in").read_text(),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout, (folder / "examples" / "01.out").read_text())
