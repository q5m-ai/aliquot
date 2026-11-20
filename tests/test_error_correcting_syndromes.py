"""Finite checks only; the universal arguments are in the approach report."""

from fractions import Fraction
import importlib.util
import json
from math import gcd
from pathlib import Path
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize

ROOT = Path(__file__).resolve().parents[1]
APPROACH = ROOT / "research" / "approaches" / "error-correcting-syndromes"
SPEC = importlib.util.spec_from_file_location("error_correcting_syndromes_verify", APPROACH / "verify.py")
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


class ErrorCorrectingSyndromesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = verify.build_report()

    def test_bounded_report_and_persisted_reproduction(self):
        self.assertEqual(self.report["unresolved_arithmetic_count"], 0)
        self.assertEqual(self.report["affine_local_criterion"]["cases_checked"], 1440)
        self.assertGreater(self.report["coprime_box"]["pairs_checked"], 1900)
        persisted = json.loads((APPROACH / "evidence.json").read_text())
        self.assertEqual(persisted, verify.decimal_data(self.report))

    def test_divisor_pairs_include_one_but_not_zero(self):
        self.assertEqual(verify.divisor_pair_sum(1), 0)
        for n in range(1, 301):
            self.assertEqual(verify.divisor_pair_sum(n), aliquot_sum(n, max_work=verify.MAX_WORK))
        with self.assertRaises(ValueError):
            verify.divisor_pair_sum(0)
        self.assertIsNone(verify.divisor_sieve(10)[0])

    def test_exact_syndrome_and_coprimality_guard(self):
        for c, q in ((1, 1), (6, 5), (120, 77), (120, 637), (20, 11), (4, 71)):
            self.assertEqual(gcd(c, q), 1)
            sc = aliquot_sum(c, max_work=verify.MAX_WORK)
            sq = aliquot_sum(q, max_work=verify.MAX_WORK)
            sn = aliquot_sum(c * q, max_work=verify.MAX_WORK)
            self.assertEqual(c * sn - sc * c * q, c * (c + sc) * sq)
        for c, q, actual, invalid_formula in ((6, 9, 66, 102), (120, 425, 117480, 149880)):
            self.assertGreater(gcd(c, q), 1)
            sc = aliquot_sum(c, max_work=verify.MAX_WORK)
            sq = aliquot_sum(q, max_work=verify.MAX_WORK)
            self.assertEqual(aliquot_sum(c * q, max_work=verify.MAX_WORK), actual)
            self.assertEqual(sc * q + (c + sc) * sq, invalid_formula)
            self.assertNotEqual(actual, invalid_formula)

    def test_local_obstructions_and_crt_cycles(self):
        for a, b, modulus in ((1, 2, 3), (4, 5, 3), (6, 9, 3)):
            with self.assertRaises(ValueError):
                verify.safe_residue(a, b, modulus)
        for row in self.report["crt_residue_orbits_not_prime_orbits"]:
            self.assertTrue(row["cycle"])
            self.assertTrue(all(gcd(x, row["modulus"]) == 1
                                for x in row["prefix"] + row["cycle"]))
        self.assertEqual(verify.safe_residue(2, 3, 30), 7)
        self.assertEqual(verify.safe_residue(2, 3, 900), 397)
        self.assertEqual(factorize(397, max_work=verify.MAX_WORK), [(397, 1)])
        # A safe CRT residue itself need not be prime.
        self.assertEqual(verify.safe_residue(2, 3, 30030), 20017)
        self.assertEqual(factorize(20017, max_work=verify.MAX_WORK), [(37, 1), (541, 1)])

    def test_adaptive_own_prime_return_not_a_fixed_small_prime_sieve(self):
        for a in range(1, 11):
            for b in range(1, 11):
                for prime in verify.small_primes(29):
                    if a % prime == 0:
                        continue
                    residue = 0
                    for h in range(1, prime + 1):
                        residue = (a * residue + b) % prime
                        if residue == 0:
                            break
                    self.assertEqual(residue, 0)
                    self.assertLessEqual(h, prime)
        self.assertEqual(2 ** 3 * (7 + 3) - 3, 77)
        self.assertGreater(77, 7)
        self.assertEqual(77 % 7, 0)
        self.assertEqual(aliquot_sum(220, max_work=verify.MAX_WORK), 284)
        self.assertEqual(aliquot_sum(284, max_work=verify.MAX_WORK), 220)
        self.assertEqual(Fraction(33, 40) * 11 + Fraction(77, 40), 11)

    def test_invisible_perturbation_and_exact_valuations(self):
        multiplier = 3025
        self.assertEqual(factorize(multiplier, max_work=verify.MAX_WORK), [(5, 2), (11, 2)])
        self.assertEqual(multiplier % 6, 1)
        self.assertEqual((multiplier + aliquot_sum(multiplier, max_work=verify.MAX_WORK)) % 6, 1)
        example = self.report["invisible_abundance_example"]
        self.assertEqual(example["base_signature_n_sigma_s"], [2, 3, 1])
        self.assertEqual(example["base_signature_n_sigma_s"], example["perturbed_signature_n_sigma_s"])
        self.assertLess(example["base_abundancy"], 2)
        self.assertGreater(example["perturbed_abundancy"], 2)

        def valuation(n, p):
            exponent = 0
            while n % p == 0:
                n //= p
                exponent += 1
            return exponent

        for prime in (2, 3):
            self.assertEqual([valuation(n, prime) for n in (2, 3, 1)],
                             [valuation(n, prime) for n in (6050, 12369, 6319)])

    def test_neutral_prime_power_construction_small_parameters(self):
        # Exact geometric sums, not divisor enumeration of these large powers.
        for modulus in range(1, 13):
            phi = sum(gcd(k, modulus) == 1 for k in range(1, modulus + 1))
            exponent = modulus * phi
            for prime in verify.small_primes(13):
                if gcd(prime, modulus) != 1:
                    continue
                power = prime ** exponent
                sigma = sum(prime ** j for j in range(exponent + 1))
                self.assertEqual(power % modulus, 1 % modulus)
                self.assertEqual(sigma % modulus, 1 % modulus)
                self.assertEqual(aliquot_sum(power, max_work=verify.MAX_WORK), sigma - power)

    def test_composite_repair_does_not_force_exit_or_monotone_defect(self):
        self.assertGreater(self.report["semiprime_filter_cases"], 0)
        q = 637  # 7^2 * 13: outside the two-prime obstruction.
        self.assertEqual(factorize(q, max_work=verify.MAX_WORK), [(7, 2), (13, 1)])
        sigma = q + aliquot_sum(q, max_work=verify.MAX_WORK)
        self.assertEqual((q % 5, sigma % 5), (2, 3))
        self.assertEqual(3 * sigma - q, 1757)
        self.assertEqual((3 * sigma - q) % 5, 2)
        trace = self.report["actual_trace"]
        self.assertEqual([row["source"] for row in trace], [840, 2040, 4440, 9240, 25320, 51000])
        self.assertEqual([row["delta"] for row in trace[:5]], [0, 0, 0, 18, 0])
        self.assertFalse(trace[-1]["coprime_to_120"])
        self.assertEqual(self.report["trace_final_value"], 117480)
        self.assertEqual(self.report["trace_stop"], "step_limit")

    def test_budget_failure_stays_unresolved(self):
        self.assertEqual(verify.arithmetic_record(999983, max_work=1),
                         {"n": 999983, "status": "unresolved_factorization"})
        with self.assertRaises(ComputationLimit):
            verify.safe_residue(2, 3, 999983, max_work=1)
        self.assertEqual(verify.decimal_data(10 ** 100), "1" + "0" * 100)
        self.assertEqual(verify.decimal_data(Fraction(3, 2)),
                         {"numerator": "3", "denominator": "2"})
        self.assertIs(verify.decimal_data(True), True)


if __name__ == "__main__":
    unittest.main()
