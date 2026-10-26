"""Bounded regressions for the symbolic-dynamics report, not proof review."""

import importlib.util
import json
from fractions import Fraction
from math import gcd
from pathlib import Path
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize

ROOT = Path(__file__).resolve().parents[1]
APPROACH = ROOT / "research" / "approaches" / "symbolic-dynamics"
SPEC = importlib.util.spec_from_file_location("symbolic_dynamics_checks", APPROACH / "verify.py")
checks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checks)


class SymbolicDynamicsTests(unittest.TestCase):
    def test_evidence_reproduction(self):
        expected = json.loads((APPROACH / "evidence.json").read_text())
        self.assertEqual(checks.build_evidence(), expected)
        self.assertEqual(expected["unresolved_checks"], 0)
        self.assertEqual(expected["unitary_cofactors_checked"], 266)
        self.assertEqual(expected["local_classification_cases"], 1848)
        self.assertEqual(expected["moduli_checked"], 258)
        self.assertEqual(expected["largest_modular_period"], 162)

    def test_independent_pair_algorithm(self):
        # Inclusive 1..300, with 1 and square divisors handled explicitly.
        sums = checks.proper_divisor_sieve(300)
        for n in range(1, 301):
            self.assertEqual(checks.pair_sum(n), sums[n], n)
        for invalid in (0, -1, True, checks.PAIR_SOURCE_CAP + 1):
            with self.assertRaises(ValueError):
                checks.pair_sum(invalid)

    def test_composite_core_identity_and_overlap_guard(self):
        for u in (1, 7, 17, 37, 77, 211, 3847, 7697):
            actual = checks.core120_step(u)
            self.assertEqual(actual, checks.pair_sum(120 * u))
            self.assertEqual(actual, aliquot_sum(120 * u, max_work=checks.MAX_WORK))
        for invalid in (0, 2, 3, 5, 425):
            with self.assertRaises(ValueError):
                checks.core120_step(invalid)

    def test_composite_correction_resets_the_prime_trap(self):
        trace = (840, 2040, 4440, 9240, 25320, 51000)
        for source, target in zip(trace, trace[1:]):
            self.assertEqual(checks.pair_sum(source), target)
        self.assertEqual(factorize(77, max_work=checks.MAX_WORK), [(7, 1), (11, 1)])
        delta = checks.pair_sum(77) - 1
        self.assertEqual(delta, 18)
        self.assertEqual(2 * 77 + 3 + 3 * delta, 211)
        self.assertNotEqual(211 % 7, 0)
        self.assertEqual(checks.pair_sum(211), 1)
        self.assertEqual(gcd(425, 120), 5)

    def test_fixed_small_prime_filter_is_not_primality(self):
        self.assertEqual(checks.pair_sum(3847), 1)
        self.assertEqual(3847 % 2310, checks.core120_residue(2310))
        self.assertEqual(checks.residue_cycle(2310), [1537, 767])
        self.assertEqual(2 * 3847 + 3, 7697)
        self.assertEqual(7697, 43 * 179)
        self.assertEqual(gcd(7697, 2310), 1)
        self.assertEqual(checks.pair_sum(923640), 1927560)
        self.assertNotEqual(1927560, 120 * (2 * 7697 + 3))

    def test_affine_criterion_examples(self):
        self.assertEqual(checks.affine_unit_survivors(4, 5, 3), [])
        self.assertEqual(checks.affine_unit_survivors(6, 9, 3), [])
        self.assertEqual(checks.affine_unit_survivors(1, 2, 3), [])
        self.assertEqual(checks.affine_unit_survivors(3, 4, 2), [1])
        self.assertEqual(checks.affine_unit_survivors(2, 3, 3), [1, 2])
        for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
            self.assertTrue(checks.affine_unit_survivors(2, 3, prime))

    def test_profinite_residue_compatibility(self):
        # All divisibility pairs with 1 <= small <= large <= 128.
        for large in range(1, 129):
            for small in range(1, large + 1):
                if large % small == 0:
                    self.assertEqual(
                        checks.core120_residue(large) % small,
                        checks.core120_residue(small),
                    )
        for modulus in checks.NAMED_MODULI:
            states = checks.residue_cycle(modulus)
            self.assertTrue(all(gcd(x, modulus) == 1 for x in states))
            self.assertEqual((2 * states[-1] + 3) % modulus, states[0])

    def test_seed_dependent_composite_certificate(self):
        # Formal affine values only, not continued aliquot orbits.
        # Inclusive primes 7..199; order search <= p-1, no factoring huge values.
        for p in range(7, 200):
            if checks.pair_sum(p) != 1:
                continue
            order = next(h for h in range(1, p) if pow(2, h, p) == 1)
            formal_value = 2**order * (p + 3) - 3
            self.assertGreater(formal_value, p)
            self.assertEqual(formal_value % p, 0)

    def test_periodic_schedule_allows_amicable_cycle(self):
        slope = Fraction(22, 20) * Fraction(3, 4)
        prime_intercept = (Fraction(3, 4) * 42 + 7) / 20
        self.assertEqual(slope, Fraction(33, 40))
        self.assertEqual(prime_intercept, Fraction(77, 40))
        self.assertEqual(prime_intercept / (1 - slope), 11)
        self.assertEqual(checks.pair_sum(220), 284)
        self.assertEqual(checks.pair_sum(284), 220)

    def test_factorization_failure_is_unresolved(self):
        with self.assertRaises(ComputationLimit):
            checks.is_prime(101, max_work=1)
        record = checks.arithmetic_record(101, max_work=1)
        self.assertEqual(record["status"], "unresolved")
        self.assertEqual(record["pair_sum"], "1")
        self.assertNotIn("factors", record)
        self.assertNotIn("s", record)

    def test_modular_budget_is_unresolved(self):
        with self.assertRaises(ComputationLimit):
            checks.residue_cycle(9, step_cap=1)


if __name__ == "__main__":
    unittest.main()
