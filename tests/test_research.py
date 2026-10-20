import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from aliquot import aliquot_sum, factorize
from aliquot.research import DEFAULT_BOUND, MAX_BOUND, analyze_six, divisor_sieve, scan_six

ROOT = Path(__file__).resolve().parents[1]


class ResearchTests(unittest.TestCase):
    def test_exit_criterion_including_exponent_traps(self):
        cases = {
            "retained": [6, 30, 42, 54, 2250, 126, 1170],
            "exitsToOdd": [18, 450], "exitsToMultipleOfFour": [90, 56250],
        }
        for prediction, values in cases.items():
            for n in values:
                total, _, predicted = analyze_six(n)
                self.assertEqual(predicted, prediction)
                self.assertEqual(total, aliquot_sum(n))
                if prediction == "retained":
                    self.assertEqual(total % 12, 6)
                elif prediction == "exitsToOdd":
                    self.assertEqual(total % 2, 1)
                else:
                    self.assertEqual(total % 4, 0)

    def test_growth_can_end_in_termination(self):
        sequence = [30, 42, 54, 66, 78, 90, 144, 259, 45, 33, 15, 9, 4, 3, 1, 0]
        for n, following in zip(sequence, sequence[1:]):
            self.assertEqual(aliquot_sum(n), following)
        self.assertEqual(analyze_six(438)[0], 450)
        self.assertEqual(analyze_six(450)[0], 759)

    def test_divisibility_class_escape_witnesses(self):
        for d in [2, 3, 4, 6, 9, 28]:
            p = factorize(d)[0][0]
            witness = d ** (p * (p - 1))
            self.assertEqual(witness % d, 0)
            self.assertEqual(aliquot_sum(witness) % p, 1)

    def test_inclusive_bounds(self):
        self.assertEqual(scan_six(5)["candidates"], 0)
        self.assertEqual(scan_six(5)["firstExamples"], {})
        self.assertEqual(scan_six(6)["counts"], dict(retained=1, exitsToOdd=0, exitsToMultipleOfFour=0))
        self.assertEqual(scan_six(17)["candidates"], 1)
        self.assertEqual(scan_six(18)["counts"]["exitsToOdd"], 1)
        self.assertEqual(scan_six(89)["counts"]["exitsToMultipleOfFour"], 0)
        self.assertEqual(scan_six(90)["counts"]["exitsToMultipleOfFour"], 1)

    def test_invalid_bounds_and_class_membership(self):
        for bound in [0, -1, 1.5, float("nan"), float("inf"), MAX_BOUND + 1, "100", True]:
            for operation in [scan_six, divisor_sieve]:
                with self.assertRaises(ValueError):
                    operation(bound)
        for n in [0, 1, 12, 28, True]:
            with self.assertRaises(ValueError):
                analyze_six(n)

    def test_mismatches_fail_closed(self):
        with patch("aliquot.research.analyze_six", return_value=(99, [], "retained")):
            with self.assertRaises(ArithmeticError):
                scan_six(6)

    def test_committed_report_and_third_algorithm(self):
        expected = json.loads((ROOT / "research/results/driver-six-100000.json").read_text())
        self.assertEqual(scan_six(DEFAULT_BOUND), expected)
        # Independent divisor-pair enumeration: neither factoring nor the sieve.
        from math import isqrt
        counts = dict(retained=0, exitsToOdd=0, exitsToMultipleOfFour=0)
        for n in range(6, DEFAULT_BOUND + 1, 12):
            total = 1
            for d in range(2, isqrt(n) + 1):
                if n % d == 0:
                    total += d
                    if n // d != d:
                        total += n // d
            key = ("exitsToOdd" if total % 2 else
                   "exitsToMultipleOfFour" if total % 4 == 0 else "retained")
            counts[key] += 1
        self.assertEqual(counts, expected["counts"])

    def cli(self, *args):
        return subprocess.run([sys.executable, "-m", "aliquot", *args], cwd=ROOT,
                              capture_output=True, text=True, timeout=30)

    def test_cli_success(self):
        result = self.cli("scan-six", "--bound", "90")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), scan_six(90))
        n = 2 ** 200
        result = self.cli("sum", str(n))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["sum"], str(n - 1))

    def test_cli_failures_never_emit_partial_reports(self):
        for args in [[], ["scan-six", "--bound", "0"], ["scan-six", "--bound", "1000001"],
                     ["scan-six", "--bound", "1e3"], ["scan-six", "--bound", "1.5"],
                     ["sum", "0"], ["sum", "-1"], ["sum", "true"],
                     ["sum", "999983", "--max-work", "10"],
                     ["sum", "9" * 5000]]:
            result = self.cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr)
