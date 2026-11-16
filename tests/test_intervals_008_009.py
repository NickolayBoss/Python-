import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path

from problems.p008_workshop_schedule.baseline_bruteforce import brute_force as schedule_reference
from problems.p008_workshop_schedule.solution import max_meetings
from problems.p009_active_requests.baseline_bruteforce import brute_force as load_reference
from problems.p009_active_requests.solution import active_counts


class IntervalTests(unittest.TestCase):
    def test_schedule_against_subsets(self):
        intervals = [(start, end) for end in range(1, 4) for start in range(end)]
        for size in range(5):
            for meetings in product(intervals, repeat=size):
                self.assertEqual(max_meetings(meetings), schedule_reference(meetings), meetings)

    def test_load_against_direct_count(self):
        intervals = [(start, end) for end in range(4) for start in range(end + 1)]
        for size in range(4):
            for requests in product(intervals, repeat=size):
                self.assertEqual(active_counts(3, requests), load_reference(3, requests), requests)

    def test_large_schedule(self):
        self.assertEqual(max_meetings((i, i + 1) for i in reversed(range(200_000))), 200_000)

    def test_large_load(self):
        self.assertEqual(active_counts(200_000, [(0, 200_000)] * 200_000), [200_000] * 200_000)

    def test_cli_examples(self):
        root = Path(__file__).resolve().parents[1]
        for directory in ("p008_workshop_schedule", "p009_active_requests"):
            with self.subTest(directory=directory):
                folder = root / "problems" / directory
                result = subprocess.run(
                    [sys.executable, str(folder / "solution.py")],
                    input=(folder / "examples" / "01.in").read_text(),
                    text=True,
                    capture_output=True,
                    check=True,
                )
                self.assertEqual(result.stdout, (folder / "examples" / "01.out").read_text())
