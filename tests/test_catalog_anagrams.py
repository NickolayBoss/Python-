import itertools
from pathlib import Path
import random
import subprocess
import sys
import unittest

from problems.p012_catalog_anagrams.solution import anagram_key, group_anagrams
from problems.p012_catalog_anagrams.baseline_sorting import group_anagrams_sorting


class CatalogAnagramsTests(unittest.TestCase):
    def test_order_and_duplicates(self):
        self.assertEqual(group_anagrams(["ba", "x", "ab", "", "x", ""]),
                         [[1, 3], [2, 5], [4, 6]])

    def test_counts_and_sum_collisions(self):
        self.assertEqual(group_anagrams(["ab", "aab", "ad", "bc", "baa"]),
                         [[1], [2, 5], [3], [4]])

    def test_unicode_and_significant_characters(self):
        names = ["кот", "ток", "A", "a", " ab", "ba ", "ab", "é", "e\u0301", "😀а", "а😀"]
        self.assertEqual(group_anagrams(names),
                         [[1, 2], [3], [4], [5, 6], [7], [8], [9], [10, 11]])
        self.assertNotEqual(anagram_key("ß"), anagram_key("ss"))
        self.assertEqual(anagram_key(""), ())

    def test_exhaustive_catalogs(self):
        words = ["", "a", "b", "ab", "ba", "aa", "aab"]
        for size in range(5):
            for names in itertools.product(words, repeat=size):
                self.assertEqual(group_anagrams(names), group_anagrams_sorting(names), names)

    def test_random_catalogs(self):
        rng = random.Random(12012)
        for _ in range(1000):
            names = ["".join(rng.choices("abАа 😀", k=rng.randrange(20)))
                     for _ in range(rng.randrange(30))]
            self.assertEqual(group_anagrams(iter(names)), group_anagrams_sorting(names))

    def test_limits(self):
        self.assertEqual(group_anagrams("" for _ in range(200_000)),
                         [list(range(1, 200_001))])
        name = "а" * 50_000 + "б" * 50_000
        self.assertEqual(group_anagrams([name, name[::-1]]), [[1, 2]])
        self.assertEqual(group_anagrams([chr(i) for i in range(0x1000, 0x1000 + 10_000)]),
                         [[i] for i in range(1, 10_001)])

    def test_cli(self):
        root = Path(__file__).resolve().parents[1] / "problems/p012_catalog_anagrams"
        cases = [(b"0\n", b"0\n"), (b"1\n\n", b"1\n1 1\n"),
                 (b"3\r\nab\r\nba\r\n ab", b"2\n2 1 2\n1 3\n"),
                 (b"2\n ab\nba \n", b"1\n2 1 2\n")]
        for example in (root / "examples").glob("*.in"):
            cases.append((example.read_bytes(), example.with_suffix(".out").read_bytes()))
        for input_data, expected in cases:
            with self.subTest(input_data=input_data):
                result = subprocess.run([sys.executable, str(root / "solution.py")],
                                        input=input_data, capture_output=True, check=True)
                self.assertEqual(result.stdout.replace(b"\r\n", b"\n"), expected)
