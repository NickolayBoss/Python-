import itertools
from pathlib import Path
import random
import subprocess
import sys
import unittest

from problems.p013_correct_brackets.solution import first_bracket_error
from problems.p013_correct_brackets.baseline_reduction import first_bracket_error_reduction


class CorrectBracketsTests(unittest.TestCase):
    def test_boundary_and_priority(self):
        cases = {'': None, '()[]{}': None, '{[()]}': None,
                 ')': 1, '](': 1, '(': 1, '([': 1, '([]': 1,
                 '([)]': 3, '([)': 3, '([]{': 1, '()()[': 5,
                 '())': 3, '{]': 2, '[()]': None, '([]){}[': 7}
        for sequence, expected in cases.items():
            with self.subTest(sequence=sequence):
                self.assertEqual(first_bracket_error(sequence), expected)

    def test_exhaustive(self):
        for size in range(7):
            for symbols in itertools.product('()[]{}', repeat=size):
                sequence = ''.join(symbols)
                self.assertEqual(first_bracket_error(sequence),
                                 first_bracket_error_reduction(sequence), sequence)

    def test_random(self):
        rng = random.Random(13013)
        for _ in range(1000):
            sequence = ''.join(rng.choices('()[]{}', k=rng.randrange(100)))
            self.assertEqual(first_bracket_error(sequence),
                             first_bracket_error_reduction(sequence), sequence)

    def test_limits(self):
        self.assertIsNone(first_bracket_error('(' * 100_000 + ')' * 100_000))
        self.assertIsNone(first_bracket_error('()' * 100_000))
        self.assertEqual(first_bracket_error('(' * 200_000), 1)
        self.assertEqual(first_bracket_error('()' * 99_999 + '(]'), 200_000)
        self.assertEqual(first_bracket_error(']' * 200_000), 1)
        self.assertEqual(first_bracket_error('()' * 99_999 + '[{'), 199_999)

    def test_cli(self):
        root = Path(__file__).resolve().parents[1] / 'problems/p013_correct_brackets'
        cases = [(b'\n', b'Success\n'), (b'\r\n', b'Success\n'),
                 (b'([)]\r\n', b'3\n'), (b'([])', b'Success\n'),
                 (b'([', b'1\n'), (b')', b'1\n')]
        for example in sorted((root / 'examples').glob('*.in')):
            cases.append((example.read_bytes(), example.with_suffix('.out').read_bytes()))
        for data, expected in cases:
            with self.subTest(data=data):
                result = subprocess.run([sys.executable, str(root / 'solution.py')],
                                        input=data, capture_output=True, check=True)
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, b'')
