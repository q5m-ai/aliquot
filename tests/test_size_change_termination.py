"""Finite checks for the size-change attempt, not universal proof verification."""

from fractions import Fraction
import importlib.util
import json
from math import gcd
from pathlib import Path
import unittest

from aliquot import ComputationLimit, aliquot_sum

DIRECTORY = (Path(__file__).resolve().parents[1] / "research" / "approaches"
             / "size-change-termination")
SPEC = importlib.util.spec_from_file_location("aliquot_sct_verify", DIRECTORY / "verify.py")
sct = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sct)


class SizeChangeTerminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Independent additive sieve, inclusive 1..50,000; primes 2..2,000.
        cls.sums = sct.divisor_sieve(50_000)
        cls.primes = [p for p in range(2, 2001) if cls.sums[p] == 1]

    def test_small_core_table_and_deficiency_threshold(self):
        expected = [0, 1, 1, 3, 1, 6, 1, 7, 4, 8, 1, 16, 1, 10, 9, 15, 1]
        self.assertEqual([self.sums[a] for a in range(1, 18)], expected)
        for a in range(1, 18):
            self.assertEqual(aliquot_sum(a), sct.divisor_pair_sum(a))
            if a not in (6, 12):
                self.assertLess(self.sums[a], a)
                self.assertLessEqual(Fraction(a + self.sums[a], a - self.sums[a]), 31)
        self.assertEqual(Fraction(31, 16 - 15), 31)
        self.assertEqual(17 * 31, sct.THRESHOLD)

    def test_restricted_rank_on_all_small_prime_sources(self):
        # a=1..17, prime p<=2,000; all source/successor values are in this sieve.
        observed = set()
        for a in range(1, 18):
            for p in self.primes:
                if gcd(a, p) != 1 or a * p <= sct.THRESHOLD:
                    continue
                n = a * p
                m = self.sums[n]
                self.assertEqual(sct.bounded_core(n, 17), (a, p))
                self.assertEqual(m, self.sums[a] * p + self.sums[a] + a)
                if m <= sct.THRESHOLD or sct.bounded_core(m, 17) is None:
                    continue
                before, after = sct.rank17(n), sct.rank17(m)
                self.assertLess(after, before)
                observed.add((before[0], after[0]))
        self.assertEqual(observed, {(0, 0), (1, 0), (1, 1), (2, 2)})

    def test_mod_three_barrier_is_symbolic_residue_check(self):
        # Every possible prime residue mod 3 for the six even deficient cores.
        for a in (2, 4, 8, 10, 14, 16):
            for residue in (1, 2):
                self.assertNotEqual((self.sums[a] * residue + self.sums[a] + a) % 3, 0)

    def test_rank_examples_and_phase_drop_allow_growth(self):
        self.assertEqual(sct.rank17(606), (2, 1))
        self.assertEqual(sct.rank17(618), (2, 0))
        self.assertEqual(sct.rank17(1212), (1, 3))
        self.assertEqual(sct.rank17(1644), (1, 2))
        self.assertEqual(sct.rank17(732), (1, 0))
        self.assertEqual(sct.rank17(1004), (0, 1004))
        self.assertGreater(1004, 732)
        self.assertLess(sct.rank17(1004), sct.rank17(732))
        self.assertEqual(sct.rank17(592), (0, 592))
        self.assertEqual(sct.rank17(586), (0, 586))

    def test_rank_does_not_claim_global_or_cycle_termination(self):
        for n in (0, 1, 220, 284, 496, 527, 630, 1926, 2706):
            with self.assertRaises(ValueError):
                sct.rank17(n)
        self.assertEqual(aliquot_sum(220), 284)
        self.assertEqual(aliquot_sum(284), 220)
        self.assertEqual(aliquot_sum(496), 496)
        with self.assertRaises(ValueError):
            sct.divisor_pair_sum(0)
        with self.assertRaises(ValueError):
            sct.valuation(0, 3)

    def test_prime_and_coprimality_guards_are_essential(self):
        self.assertNotEqual(aliquot_sum(18), 6 * 3 + 12)
        self.assertNotEqual(aliquot_sum(150), 6 * 25 + 12)
        self.assertIsNone(sct.bounded_core(1926, 17))
        self.assertEqual(sct.bounded_core(1926, 18), (18, 107))
        self.assertIsNone(sct.bounded_core(2706, 19))
        self.assertIsNone(sct.guarded_return(121))  # Proven composite, not prime.
        self.assertIsNone(sct.guarded_return(37))   # Prime but wrong mod-4 phase.

    def test_boundary_returns_are_actual_aliquot_blocks(self):
        # Every prime p=37..2,000 inclusive, at most one accelerated return.
        for p in self.primes:
            if p <= 31:
                continue
            result = sct.guarded_return(p)
            if result is None:
                continue
            q, path = result
            self.assertGreater(q, p)
            self.assertIn(len(path) - 1, (1, 2))
            for n, m in zip(path, path[1:]):
                self.assertEqual(aliquot_sum(n), m)
                self.assertEqual(sct.divisor_pair_sum(n), m)
            c, a, b = sct.active_budget(p)
            other, aa, bb = sct.active_budget(q)
            self.assertEqual(Fraction(q + c), Fraction(7, 6) * (p + c))
            self.assertEqual(other != c, b == 1)
            if other == c:
                self.assertEqual((aa, bb), (a - 1, b - 1))

    def test_simultaneous_budget_recharge_is_real_but_not_closed(self):
        self.assertEqual(sct.guarded_return(107), (127, (1926, 2286)))
        self.assertEqual(sct.active_budget(107), (13, 3, 1))
        self.assertEqual(sct.active_budget(127), (17, 4, 2))
        self.assertIsNone(sct.guarded_return(127))
        self.assertEqual(aliquot_sum(2286), 2706)
        self.assertEqual(2706, 6 * 11 * 41)

    def test_compressed_switch_identity_is_formal_not_a_prime_certificate(self):
        # t=1..4, u=1..100 coprime to 6, both shifts. No primality assertion.
        for t in range(1, 5):
            for u in range(1, 101):
                if gcd(u, 6) != 1:
                    continue
                for c, other, sign in ((13, 17, 1), (17, 13, -1)):
                    p = 4 * 6 ** t * u - c
                    q = 4 * 7 ** t * u - c
                    self.assertEqual(sct.valuation(p + c, 2), t + 2)
                    self.assertEqual(sct.valuation(p + c, 3), t)
                    self.assertEqual(q + c, Fraction(7, 6) ** t * (p + c))
                    self.assertEqual(q + other, 4 * (7 ** t * u + sign))

    def test_work_limit_is_unresolved_not_a_failed_guard(self):
        with self.assertRaises(ComputationLimit):
            sct.guarded_return(107, max_work=1)
        with self.assertRaises(ComputationLimit):
            sct.is_prime(97, max_work=1)
        with self.assertRaises(ComputationLimit):
            sct.rank17(606, max_work=1)

    def test_all_named_edges_by_independent_divisor_pairs(self):
        for path in sct.NAMED_PATHS.values():
            for n, m in zip(path, path[1:]):
                self.assertGreater(n, 0)
                self.assertEqual(aliquot_sum(n), m)
                self.assertEqual(sct.divisor_pair_sum(n), m)

    def test_bounded_evidence_reproduces_exactly(self):
        committed = json.loads((DIRECTORY / "evidence.json").read_text())
        self.assertEqual(sct.verify(), committed)
        self.assertEqual(committed["unresolved_count"], 0)
        self.assertEqual(committed["affine_cases"], 23327)
        self.assertEqual(committed["rank17_edges_checked"], 8459)
        self.assertEqual(committed["guarded_returns"], 124)


if __name__ == "__main__":
    unittest.main()
