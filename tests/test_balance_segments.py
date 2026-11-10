"""Полный перебор знаковых массивов, независимый эталон и свойства."""
from itertools import product
from pathlib import Path
import random
import subprocess
import sys
import unittest
from problems.p005_balance_segments.solution import count_segments, solve
from problems.p005_balance_segments.baseline_bruteforce import count_segments_bruteforce

ROOT = Path(__file__).resolve().parents[1] / 'problems/p005_balance_segments'


class BalanceSegmentTests(unittest.TestCase):
    def test_examples_cli(self):
        for source in sorted((ROOT / 'examples').glob('*.in')):
            expected = source.with_suffix('.out').read_text().strip()
            self.assertEqual(solve(source.read_bytes()), expected)
            result = subprocess.run([sys.executable, str(ROOT / 'solution.py')], input=source.read_bytes(), capture_output=True, check=True)
            self.assertEqual(result.stdout.decode().strip(), expected)
            self.assertEqual(result.stderr, b'')

    def test_empty_function_input(self):
        self.assertEqual(count_segments([], 0), 0)

    def test_empty_prefix_required(self):
        self.assertEqual(count_segments([3], 3), 1)

    def test_empty_segment_excluded(self):
        self.assertEqual(count_segments([1], 0), 0)

    def test_repeated_prefixes(self):
        self.assertEqual(count_segments([1, -1, 1, -1], 0), 4)

    def test_all_zero(self):
        self.assertEqual(count_segments([0] * 4, 0), 10)

    def test_negative_target(self):
        self.assertEqual(count_segments([-1, -1, 2], -2), 1)

    def test_no_match(self):
        self.assertEqual(count_segments([2, 4, 6], 1), 0)

    def test_large_prefixes(self):
        self.assertEqual(count_segments([10**9, 10**9, -10**9], 10**9), 3)

    def test_single_pass_and_no_mutation(self):
        data = [2, -1, 2, 1, -2]
        self.assertEqual(count_segments(iter(data), 3), 2)
        self.assertEqual(data, [2, -1, 2, 1, -2])

    def test_exhaustive(self):
        for count in range(8):
            for data in product((-1, 0, 1), repeat=count):
                for target in range(-3, 4):
                    self.assertEqual(count_segments(data, target), count_segments_bruteforce(data, target), (data, target))

    def test_random_differential(self):
        rng = random.Random(20261115)
        for _ in range(1000):
            data = [rng.randint(-10, 10) for _ in range(rng.randint(0, 60))]
            target = rng.randint(-30, 30)
            expected = count_segments_bruteforce(data, target)
            self.assertEqual(count_segments(data, target), expected)
            self.assertEqual(count_segments(reversed(data), target), expected)
            self.assertEqual(count_segments((-x for x in data), -target), expected)

    def test_large_zero_answer_exceeds_int32(self):
        count = 200000
        self.assertEqual(count_segments((0 for _ in range(count)), 0), count * (count + 1) // 2)

    def test_large_distinct_prefixes(self):
        self.assertEqual(count_segments((1 for _ in range(200000)), 1), 200000)


if __name__ == '__main__':
    unittest.main()
