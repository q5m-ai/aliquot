"""Finite regressions for the small-gain attempt; not mathematical proof review."""

from fractions import Fraction
import importlib.util
import json
from math import gcd
from pathlib import Path
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize

DIRECTORY = Path(__file__).resolve().parents[1] / "research/approaches/small-gain-feedback"
SPEC = importlib.util.spec_from_file_location("small_gain_feedback_verify", DIRECTORY / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class SmallGainFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = VERIFY.evidence()

    def test_evidence_reproduces_exactly_and_records_limits(self):
        expected = json.loads((DIRECTORY / "evidence.json").read_text())
        self.assertEqual(self.report, expected)
        scan = self.report["scan"]
        self.assertEqual(scan["attempted_inputs"], 2000)
        self.assertEqual(scan["completed_inputs"], 2000)
        self.assertEqual(scan["unresolved_count"], 0)
        self.assertEqual(scan["guarded_20_4_20_blocks"], 211)
        self.assertEqual(scan["first_growing_block"]["values"], ["540", "1140", "2220"])
        self.assertEqual(scan["factorization_work_per_call"], 10000)
        self.assertEqual(self.report["named_transition_count"], 10)

    def test_composite_core_identity_with_independent_sieve(self):
        # Inclusive d,u=1..60; all products <=3600; only unitary splits.
        sums = VERIFY.divisor_sieve(3600)
        for d in range(1, 61):
            for u in range(1, 61):
                if gcd(d, u) == 1:
                    actual = aliquot_sum(d * u, max_work=10000)
                    self.assertEqual(actual, sums[d * u])
                    self.assertEqual(actual, sums[d] * u + (sums[d] + d) * sums[u])
        # Ordinary divisibility is not sufficient: 6*9 is not unitary.
        self.assertEqual(aliquot_sum(54), 66)
        self.assertEqual(aliquot_sum(6) * 9 + 12 * aliquot_sum(9), 102)
        self.assertEqual(VERIFY.pair_sum(1), 0)
        with self.assertRaises(ValueError):
            VERIFY.pair_sum(0)

    def test_exact_cycle_weights_and_expansive_rejection(self):
        gains = {(20, 4): Fraction(6), (4, 20): Fraction(1, 6)}
        self.assertEqual(VERIFY.cycle_weights((20, 4), gains), {20: 6, 4: 1})
        # Bare prime-core slopes; the additive/composite input is NOT included.
        bare = {(20, 4): Fraction(11, 2), (4, 20): Fraction(3, 20)}
        self.assertEqual(bare[20, 4] * bare[4, 20], Fraction(33, 40))
        self.assertEqual(VERIFY.cycle_weights((20, 4), bare), {20: 11, 4: 2})
        with self.assertRaises(ValueError):
            VERIFY.cycle_weights((20, 4), {(20, 4): Fraction(6), (4, 20): Fraction(1, 5)})
        self.assertEqual(VERIFY.cycle_weights((6,), {(6, 6): Fraction(1)}), {6: 1})
        three_cycle = {(0, 1): Fraction(2), (1, 2): Fraction(3), (2, 0): Fraction(1, 6)}
        self.assertEqual(VERIFY.cycle_weights((0, 1, 2), three_cycle), {0: 6, 1: 3, 2: 1})
        with self.assertRaises(ValueError):
            VERIFY.cycle_weights((6,), {(6, 6): Fraction(2)})

    def test_cycles_are_allowed_by_nonexpansive_full_gains(self):
        # The real amicable pair, with exact edge-dependent leakage bounds.
        gains = {(20, 4): Fraction(71, 11), (4, 20): Fraction(11, 71)}
        weights = VERIFY.cycle_weights((20, 4), gains)
        self.assertEqual(weights, {20: 71, 4: 11})
        self.assertEqual(weights[20] * 11, weights[4] * 71)
        self.assertEqual(VERIFY.pair_sum(220), 284)
        self.assertEqual(VERIFY.pair_sum(284), 220)

    def test_sharp_algebraic_common_leakage_threshold(self):
        def product(epsilon):
            return (11 + 21 * epsilon) * (3 + 7 * epsilon) / 40
        self.assertEqual(product(Fraction(1, 21)), 1)
        self.assertLess(product(Fraction(1, 22)), 1)
        self.assertGreater(product(Fraction(1, 20)), 1)
        self.assertLess(Fraction(47, 46) ** 2 - 1, Fraction(1, 21))
        self.assertGreater(self.report["scan"]["leakage_threshold_blocks"], 0)
        for p in (491, 2711):
            self.assertEqual(factorize(p, max_work=10000), [(p, 1)])
            self.assertEqual(VERIFY.pair_sum(p), 1)

    def test_supplier_guard_and_failed_regeneration(self):
        self.assertEqual(factorize(179, max_work=10000), [(179, 1)])
        self.assertEqual(factorize(199, max_work=10000), [(199, 1)])
        self.assertEqual(VERIFY.pair_sum(179), 1)
        self.assertEqual(VERIFY.pair_sum(199), 1)
        u, v, w = 179, 995, 221
        self.assertEqual(factorize(v), [(5, 1), (199, 1)])
        self.assertEqual(aliquot_sum(v) + v, 1200)
        self.assertEqual((22 * u + 42 * aliquot_sum(u)) // 4, v)
        self.assertEqual(aliquot_sum(4 * v), 20 * w)
        self.assertEqual(gcd(w, 20), 1)
        self.assertEqual(Fraction(33, 40) * u + Fraction(63, 40) * aliquot_sum(u)
                         + Fraction(7, 20) * aliquot_sum(v), w)
        self.assertGreater(w, u)
        self.assertEqual(factorize(w), [(13, 1), (17, 1)])
        next_v = aliquot_sum(20 * w) // 4
        self.assertEqual(next_v, 1541)
        self.assertNotEqual(next_v % 5, 0)  # supply guard already lost
        self.assertEqual(aliquot_sum(5828) % 20, 4)  # enlarged core loop also fails

    def test_crt_conditions_are_reduced_not_a_prime_or_orbit_assertion(self):
        # K=13*17*19 only checks the CRT algebra. No primality of the CRT
        # representative, or existence of an infinite itinerary, is inferred.
        modulus = 4 * 25 * 199**2
        self.assertEqual(modulus, 3960100)
        self.assertEqual(gcd(179, modulus), 1)
        k = 13 * 17 * 19
        target = (-21 * pow(11, -1, k)) % k
        residue = 179 + modulus * (((target - 179) * pow(modulus, -1, k)) % k)
        self.assertEqual(gcd(residue, modulus * k), 1)
        self.assertEqual(residue % modulus, 179)
        self.assertEqual(residue % k, target)
        v = (11 * residue + 21) // 2
        self.assertEqual((11 * residue + 21) % 2, 0)
        self.assertEqual(v % 2, 1)
        self.assertEqual(v % 25, 20)
        self.assertEqual(v % 199**2, 995)
        self.assertEqual(v % k, 0)

    def test_lenstra_supply_links_without_constructing_huge_seeds(self):
        # Exactly two links, exponents 2,7,8747; modular exponentiation only.
        self.assertEqual(sum(3**j for j in range(8)) % 2**3, 0)
        modulus = 3**8 * (5 - 1)
        self.assertEqual(pow(5, 8748, modulus), 1)
        self.assertEqual((pow(5, 8748, 4 * 3**8) - 1) % (4 * 3**8), 0)

    def test_budget_exhaustion_stays_unresolved(self):
        with self.assertRaises(ComputationLimit):
            aliquot_sum(199, max_work=1)
        limited = VERIFY.scan(u_bound=10, source_cap=1000, max_work=1)
        self.assertGreater(limited["unresolved_count"], 0)
        self.assertEqual(limited["attempted_inputs"],
                         limited["completed_inputs"] + limited["unresolved_count"])
        self.assertTrue(all("factorization" in case["stage"] for case in limited["unresolved"]))
        capped = VERIFY.scan(u_bound=10, source_cap=200, max_work=10000)
        self.assertEqual(capped["completed_inputs"], 3)
        self.assertEqual(capped["unresolved"], [
            {"u": "9", "stage": "second source cap", "known_successor": "366"}
        ])
        self.assertEqual(capped["max_endpoint"], "203")  # above-cap output is retained


if __name__ == "__main__":
    unittest.main()
