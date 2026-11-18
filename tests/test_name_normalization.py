import subprocess
import sys
import unittest
from pathlib import Path

from problems.p011_name_normalization.solution import names_match, normalize_name


class NameNormalizationTests(unittest.TestCase):
    def test_collapses_unicode_whitespace(self):
        self.assertEqual(normalize_name("\r\n\t СЕВЕР\u00a0\u2003ВЕТЕР\v\f"), "север ветер")

    def test_empty_and_whitespace_only(self):
        self.assertEqual(normalize_name(""), "")
        self.assertTrue(names_match("", "\t\u00a0"))
        self.assertFalse(names_match(" ", "А"))

    def test_unicode_casefold(self):
        self.assertTrue(names_match("Straße", "STRASSE"))
        self.assertTrue(names_match("Σ", "ς"))

    def test_preserves_word_boundaries_and_punctuation(self):
        self.assertFalse(names_match("А Б", "АБ"))
        self.assertFalse(names_match("А-Б", "А Б"))
        self.assertTrue(names_match("А-Б", "а-б"))

    def test_keeps_distinct_unicode_sequences(self):
        self.assertFalse(names_match("é", "e\u0301"))
        self.assertFalse(names_match("A\u200bB", "AB"))

    def test_maximum_length(self):
        self.assertTrue(names_match("ẞ" * 100_000 + " " * 100_000, "s" * 200_000))

    def test_cli_examples_and_line_boundaries(self):
        root = Path(__file__).resolve().parents[1] / "problems" / "p011_name_normalization"
        examples = root / "examples"
        cases = [
            ((examples / "01.in").read_bytes(), (examples / "01.out").read_bytes()),
            ((examples / "02.in").read_bytes(), (examples / "02.out").read_bytes()),
            (b"\n\t\n", b"YES\n"),
            (b"\nName\n", b"NO\n"),
            (b"\tName\r\nNAME", b"YES\n"),
            (b"\n\n", b"YES\n"),
        ]
        for input_data, expected in cases:
            with self.subTest(input_data=input_data):
                result = subprocess.run(
                    [sys.executable, str(root / "solution.py")],
                    input=input_data,
                    capture_output=True,
                    check=True,
                )
                self.assertEqual(result.stdout.replace(b"\r\n", b"\n"), expected)
