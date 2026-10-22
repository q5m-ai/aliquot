from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, aliquot_sum, factorize
from aliquot.research import divisor_sieve
from aliquot.two_adic import (
    DEFAULT_BOUND, MAX_BOUND, RESIDUE_BITS, _divisor_pair_sum,
    even_step, scan_two_adic, valuation_two,
)

ROOT = Path(__file__).resolve().parents[1]


class TwoAdicTests(unittest.TestCase):
    def test_valuation_domain_and_large_exact_values(self):
        for exponent in [0, 1, 2, 20, 300, 1000]:
            self.assertEqual(valuation_two((1 << exponent) * 37), exponent)
        for invalid in [0, -2, True, 1.5, "8", float("inf")]:
            with self.assertRaises(ValueError):
                valuation_two(invalid)

    def test_all_three_branches_and_resonance(self):
        for n, a, b, successor, exponent, branch in [
            (2, 1, 0, 1, 0, "drops"),
            (12, 2, 2, 16, 4, "rises"),
            (30, 1, 3, 42, 1, "stays"),
            (10, 1, 1, 8, 3, "rises"),
            (26, 1, 1, 16, 4, "rises"),
            (2042, 1, 1, 1024, 10, "rises"),
            (2250, 1, 2, 3834, 1, "stays"),
        ]:
            with self.subTest(n=n):
                step = even_step(n)
                self.assertEqual((step.a, step.b, step.successor, step.predicted_valuation, step.branch),
                                 (a, b, successor, exponent, branch))
                self.assertEqual(step.successor, _divisor_pair_sum(n))
        step = even_step(2 ** 300)
        self.assertEqual((step.a, step.b, step.successor, step.predicted_valuation),
                         (300, 0, 2 ** 300 - 1, 0))

    def test_prime_exponent_formula_against_direct_sums(self):
        for prime in [3, 5, 7, 13, 17]:
            for exponent in range(1, 12):
                sigma = sum(prime ** k for k in range(exponent + 1))
                step = even_step(2 * prime ** exponent)
                self.assertEqual(step.b, valuation_two(sigma))
                self.assertEqual(step.sigma_odd, sigma)

    def test_exhaustive_law_against_sieve(self):
        sums = divisor_sieve(10_000)
        for n in range(2, len(sums), 2):
            step = even_step(n)
            self.assertEqual(step.successor, sums[n])
            self.assertEqual(step.b, valuation_two(sums[step.odd_part] + step.odd_part))
            self.assertEqual(step.predicted_valuation, valuation_two(sums[n]))

    def test_same_fingerprint_different_next_fingerprints(self):
        for n, first, b_next, second in [(30, 42, 5, 54), (78, 90, 1, 144), (438, 450, 0, 759)]:
            step = even_step(n)
            self.assertEqual((step.a, step.b), (1, 3))
            self.assertEqual(step.successor, first)
            following = even_step(first)
            self.assertEqual(following.b, b_next)
            self.assertEqual(following.successor, second)
            self.assertEqual(_divisor_pair_sum(n), first)
            self.assertEqual(_divisor_pair_sum(first), second)

    def test_large_reserve_can_collapse_before_exit(self):
        for n, b, middle, middle_b, final in [
            (72198, 12, 112122, 1, 130848),
            (48222, 9, 66978, 0, 80559),
        ]:
            first = even_step(n)
            second = even_step(middle)
            self.assertEqual((first.b, first.successor), (b, middle))
            self.assertEqual((second.b, second.successor), (middle_b, final))
            self.assertEqual(_divisor_pair_sum(n), middle)
            self.assertEqual(_divisor_pair_sum(middle), final)

    def test_odd_cofactor_identity_and_mod_three_table(self):
        allowed = {(2, 0, 1), (1, 0, 2), (1, 1, 1), (1, 2, 0)}
        for u in range(1, 1000, 2):
            if u % 3 == 0:
                continue
            sigma = _divisor_pair_sum(u) + u
            following = 2 * sigma - u
            self.assertEqual(aliquot_sum(6 * u), 6 * following)
            self.assertEqual(following % 2, 1)
            self.assertIn((u % 3, sigma % 3, following % 3), allowed)
            if u > 1:
                self.assertGreaterEqual(following, u + 2)
            else:
                self.assertEqual(following, 1)
        for orbit in [[5, 7, 9], [25, 37, 39], [49, 65, 103, 105]]:
            for u, following in zip(orbit, orbit[1:]):
                self.assertNotEqual(u % 3, 0)
                self.assertEqual(u + 2 * aliquot_sum(u), following)
            self.assertEqual(orbit[-1] % 3, 0)
        # The coprimality guard is essential: the scaled identity fails at u=3.
        self.assertNotEqual(aliquot_sum(18), 6 * (3 + 2 * aliquot_sum(3)))

    def test_discontinuity_family_is_only_a_finite_regression(self):
        self.assertEqual(aliquot_sum(18), 21)
        for k in range(4, 17):
            n = 18 * (1 + 2 ** k)
            self.assertEqual(n % 12, 6)
            self.assertEqual(valuation_two(n - 18), k + 1)
            self.assertEqual(aliquot_sum(n) % 2, 0)
            self.assertEqual(aliquot_sum(n), _divisor_pair_sum(n))
        # The excluded exponent really is exceptional: 1+2^3=9 is a square.
        self.assertEqual(aliquot_sum(18 * (1 + 2 ** 3)) % 2, 1)

    def test_translation_is_one_cycle_on_eligible_residues(self):
        for bits in range(2, RESIDUE_BITS + 1):
            modulus = 1 << bits
            visited, r = set(), 2
            while r not in visited:
                visited.add(r)
                r = (r + 12) % modulus
            self.assertEqual(r, 2)
            self.assertEqual(visited, set(range(2, modulus, 4)))
        # Exact finite examples of the prime-branch identity, not Dirichlet's theorem.
        for p in [5, 7, 13, 73, 853, 7681]:
            self.assertEqual(factorize(p), [(p, 1)])
            self.assertEqual(_divisor_pair_sum(6 * p), 6 * p + 12)

    def test_independent_pair_algorithm(self):
        sums = divisor_sieve(500)
        for n in range(1, 501):
            self.assertEqual(_divisor_pair_sum(n), sums[n])

    def test_bounds_and_inputs(self):
        self.assertEqual(scan_two_adic(1)["evenSources"], 0)
        self.assertEqual(scan_two_adic(5)["sixClass"]["sources"], 0)
        six = scan_two_adic(6)
        self.assertEqual(six["sixClass"]["outcomes"]["retainedThroughTwoSteps"], 1)
        self.assertFalse(six["primeBranchResidues"]["completeCoverage"])
        for n in [0, -1, True, 1.5, "2", 1, 3]:
            with self.assertRaises(ValueError):
                even_step(n)
        for bound in [0, -1, True, 1.5, "10", MAX_BOUND + 1]:
            with self.assertRaises(ValueError):
                scan_two_adic(bound)
        with self.assertRaises(ComputationLimit):
            even_step(2 * 999983, max_work=5)

    def test_mismatches_fail_closed_in_both_algorithms(self):
        broken = replace(even_step(2), b=9)
        with patch("aliquot.two_adic.even_step", return_value=broken):
            with self.assertRaises(ArithmeticError):
                scan_two_adic(2)
        with patch("aliquot.two_adic._divisor_pair_sum", return_value=999):
            with self.assertRaises(ArithmeticError):
                scan_two_adic(6)

    def test_committed_report(self):
        expected = json.loads((ROOT / "research/results/two-adic-100000.json").read_text())
        self.assertEqual(scan_two_adic(DEFAULT_BOUND), expected)
        self.assertEqual(expected["evenSources"], 50_000)
        self.assertEqual(expected["sixClass"]["secondStepsChecked"], 7821)
        self.assertEqual(expected["primeBranchResidues"]["coveredResidues"], 256)

    def test_cli_and_no_partial_json_on_failure(self):
        command = [sys.executable, "-m", "aliquot", "scan-two-adic", "--bound"]
        result = subprocess.run(command + ["90"], cwd=ROOT, text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), scan_two_adic(90))
        for bound in ["0", str(MAX_BOUND + 1), "1e3", "true"]:
            result = subprocess.run(command + [bound], cwd=ROOT, text=True, capture_output=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr)
