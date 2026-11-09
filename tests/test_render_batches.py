"""Перебор разбиений, свойства предиката, границы и запуск CLI."""

from itertools import product
from pathlib import Path
import random
import subprocess
import sys
import unittest

from problems.p003_render_batches.baseline_bruteforce import minimum_time_bruteforce
from problems.p003_render_batches.solution import can_finish, minimum_time, solve

PROBLEM = Path(__file__).resolve().parents[1] / "problems" / "p003_render_batches"


class RenderBatchTests(unittest.TestCase):
    def test_examples_and_cli(self):
        for source in sorted((PROBLEM / "examples").glob("*.in")):
            with self.subTest(example=source.name):
                expected = source.with_suffix(".out").read_text().strip()
                self.assertEqual(solve(source.read_bytes()), expected)
                result = subprocess.run([sys.executable, str(PROBLEM / "solution.py")], input=source.read_bytes(), capture_output=True, check=True)
                self.assertEqual(result.stdout.decode().strip(), expected)
                self.assertEqual(result.stderr, b"")

    def test_single_job(self):
        self.assertEqual(minimum_time([9], 1), 9)

    def test_one_worker(self):
        self.assertEqual(minimum_time([4, 1, 6], 1), 11)

    def test_worker_for_each_job(self):
        self.assertEqual(minimum_time([4, 1, 6], 3), 6)

    def test_equality_does_not_create_extra_block(self):
        self.assertTrue(can_finish([2, 3, 5], 2, 5))
        self.assertEqual(minimum_time([2, 3, 5], 2), 5)

    def test_job_larger_than_limit(self):
        self.assertFalse(can_finish([9], 1, 8))
        self.assertFalse(can_finish([1, 9], 2, 8))

    def test_order_must_be_preserved(self):
        # Перестановка позволила бы [8, 1] | [1, 8], но она запрещена.
        self.assertEqual(minimum_time([8, 8, 1, 1], 2), 10)

    def test_equal_durations(self):
        self.assertEqual(minimum_time([5, 5, 5, 5], 3), 10)

    def test_large_integer_sum(self):
        self.assertEqual(minimum_time([10**9] * 5, 2), 3 * 10**9)

    def test_inputs_unchanged(self):
        data = [7, 2, 5, 10, 8]
        minimum_time(data, 2)
        can_finish(data, 2, 18)
        self.assertEqual(data, [7, 2, 5, 10, 8])
        self.assertEqual(minimum_time(tuple(data), 2), 18)

    def test_exhaustive_small_arrays(self):
        for count in range(1, 7):
            for data in product(range(1, 4), repeat=count):
                for workers in range(1, count + 1):
                    self.assertEqual(minimum_time(data, workers), minimum_time_bruteforce(data, workers), (data, workers))

    def test_random_differential_and_boundary(self):
        rng = random.Random(20261111)
        for _ in range(1000):
            count = rng.randint(1, 10)
            data = [rng.randint(1, 50) for _ in range(count)]
            workers = rng.randint(1, count)
            answer = minimum_time(data, workers)
            self.assertEqual(answer, minimum_time_bruteforce(data, workers), (data, workers))
            self.assertTrue(can_finish(data, workers, answer))
            self.assertFalse(can_finish(data, workers, answer - 1))

    def test_predicate_monotonicity(self):
        data = [3, 1, 4, 1, 5]
        for workers in range(1, len(data) + 1):
            results = [can_finish(data, workers, limit) for limit in range(sum(data) + 2)]
            self.assertEqual(results, sorted(results))

    def test_more_workers_never_worsen_answer(self):
        data = [7, 2, 5, 10, 8]
        results = [minimum_time(data, workers) for workers in range(1, len(data) + 1)]
        self.assertEqual(results, sorted(results, reverse=True))

    def test_large_input(self):
        data = [10**9] * 200000
        self.assertEqual(minimum_time(data, 3), 66667 * 10**9)


if __name__ == "__main__":
    unittest.main()
