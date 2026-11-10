"""Границы, полный перебор, независимый эталон и большой вход."""
from itertools import product
from pathlib import Path
import random
import subprocess
import sys
import unittest
from problems.p004_event_window.solution import longest_window, solve
from problems.p004_event_window.baseline_bruteforce import longest_window_bruteforce

ROOT = Path(__file__).resolve().parents[1] / 'problems/p004_event_window'


class EventWindowTests(unittest.TestCase):
    def test_examples_cli(self):
        for source in sorted((ROOT / 'examples').glob('*.in')):
            expected = source.with_suffix('.out').read_text().strip()
            self.assertEqual(solve(source.read_bytes()), expected)
            result = subprocess.run([sys.executable, str(ROOT / 'solution.py')], input=source.read_bytes(), capture_output=True, check=True)
            self.assertEqual(result.stdout.decode().strip(), expected)
            self.assertEqual(result.stderr, b'')

    def test_empty_function_input(self):
        self.assertEqual(longest_window([], 2), (0, 0))

    def test_zero_limit(self):
        self.assertEqual(longest_window([1, 1, 1], 0), (0, 0))

    def test_single_event(self):
        self.assertEqual(longest_window([9], 1), (0, 1))

    def test_earliest_tie(self):
        self.assertEqual(longest_window([7, 7, 8, 8, 9], 1), (0, 2))

    def test_repeated_shrink(self):
        self.assertEqual(longest_window([1, 1, 2, 3, 3, 3], 2), (2, 6))

    def test_zero_keys_removed(self):
        self.assertEqual(longest_window([1, 2, 3, 3, 3, 3], 1), (2, 6))

    def test_all_types_fit(self):
        self.assertEqual(longest_window([1, 2, 1, 3], 5), (0, 4))

    def test_large_identifiers(self):
        self.assertEqual(longest_window([10**9, 1, 10**9], 1), (0, 1))

    def test_input_unchanged(self):
        data = [1, 2, 1]
        self.assertEqual(longest_window(tuple(data), 2), (0, 3))
        longest_window(data, 1)
        self.assertEqual(data, [1, 2, 1])

    def test_exhaustive(self):
        for count in range(8):
            for data in product(range(3), repeat=count):
                for limit in range(5):
                    self.assertEqual(longest_window(data, limit), longest_window_bruteforce(data, limit), (data, limit))

    def test_random_differential(self):
        rng = random.Random(20261110)
        for _ in range(1000):
            data = [rng.randint(1, 20) for _ in range(rng.randint(1, 60))]
            limit = rng.randint(0, 22)
            answer = longest_window(data, limit)
            self.assertEqual(answer, longest_window_bruteforce(data, limit))
            left, right = answer
            self.assertLessEqual(len(set(data[left:right])), limit)

    def test_answer_length_monotone_in_limit(self):
        data = [1, 2, 3, 2, 1, 4]
        sizes = [b-a for a, b in (longest_window(data, k) for k in range(6))]
        self.assertEqual(sizes, sorted(sizes))

    def test_large_input(self):
        self.assertEqual(longest_window([1, 2] * 100000, 2), (0, 200000))
        self.assertEqual(longest_window(range(200000), 1), (0, 1))


if __name__ == '__main__':
    unittest.main()
