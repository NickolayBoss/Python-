import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path

from problems.p010_log_summary.baseline_bruteforce import BruteLogSummary
from problems.p010_log_summary.solution import LogSummary


class LogSummaryTests(unittest.TestCase):
    def test_small_logs_against_reference(self):
        for size in range(5):
            for codes in product(range(3), repeat=size):
                values = [code - 1 for code in codes]
                for limit in range(4):
                    actual = LogSummary(codes, values, limit)
                    expected = BruteLogSummary(codes, values, limit)
                    self.assertEqual(actual.longest, expected.longest)
                    for left in range(size + 1):
                        for right in range(left, size + 1):
                            self.assertEqual(actual.range_sum(left, right), expected.range_sum(left, right))
                            for code in range(4):
                                self.assertEqual(actual.frequency(left, right, code),
                                                 expected.frequency(left, right, code))

    def test_large_log(self):
        size = 200_000
        summary = LogSummary([0, 1] * (size // 2), [10**9] * size, 1)
        self.assertEqual(summary.longest, 1)
        self.assertEqual(summary.range_sum(0, size), size * 10**9)
        self.assertEqual(summary.frequency(1, size, 0), size // 2 - 1)

    def test_cli_example(self):
        root = Path(__file__).resolve().parents[1] / "problems" / "p010_log_summary"
        result = subprocess.run(
            [sys.executable, str(root / "solution.py")],
            input=(root / "examples/01.in").read_text(),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout, (root / "examples/01.out").read_text())
