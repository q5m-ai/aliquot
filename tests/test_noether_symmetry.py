"""Finite checks for the noether-symmetry report, not a universal proof review."""

from fractions import Fraction
import importlib.util
import json
from math import gcd
from pathlib import Path
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize

DIRECTORY = Path(__file__).resolve().parents[1] / "research/approaches/noether-symmetry"
SPEC = importlib.util.spec_from_file_location("noether_symmetry_verify", DIRECTORY / "verify.py")
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


class NoetherSymmetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = verify.build_report()
        # Additive sieve, inclusive bound 84*2000; no factorization or core formulas.
        bound = 168_000
        cls.sums = [0] * (bound + 1)
        for d in range(1, bound // 2 + 1):
            for multiple in range(2 * d, bound + 1, d):
                cls.sums[multiple] += d

    def test_discrete_action_symmetry_and_auxiliary_charge(self):
        r = Fraction(5, 3)
        y = list(map(Fraction, (3, 7, 2, 13)))  # Off-shell, not an aliquot orbit.
        multipliers = [Fraction(2, 3), Fraction(-1, 4), Fraction(5, 2)]

        def action(values, momenta):
            return sum(momenta[i] * (values[i + 1] - r * values[i])
                       for i in range(3))

        scale = Fraction(7, 3)
        self.assertEqual(action(y, multipliers),
                         action([scale * x for x in y],
                                [p / scale for p in multipliers]))
        # Six formal real/rational steps only; after three steps these are NOT
        # asserted to be prime cofactors or actual aliquot transitions.
        y = [27 * r ** i for i in range(7)]
        multipliers = [r ** (-i) for i in range(6)]
        for i in range(1, 6):
            self.assertEqual(multipliers[i - 1], r * multipliers[i])
            self.assertEqual(multipliers[i - 1] * y[i], 45)
            self.assertEqual(multipliers[i] * y[i + 1], 45)

    def test_composite_correction_through_2000(self):
        # Every coprime cofactor u in 2..2000, one source sum, not an orbit census.
        self.assertEqual(self.sums[84], 140)
        guarded = 0
        for u in range(2, 2001):
            if gcd(u, 84) != 1:
                continue
            proper = self.sums[u]
            actual = self.sums[84 * u]
            self.assertEqual(aliquot_sum(84 * u, max_work=verify.MAX_WORK), actual)
            self.assertEqual(actual, 140 * u + 224 * proper)
            following = Fraction(actual, 84)
            self.assertEqual(following + 4,
                             Fraction(5, 3) * (u + 4)
                             + Fraction(8, 3) * (proper - 1))
            if following.denominator == 1 and gcd(following.numerator, 84) == 1:
                guarded += 1
                self.assertGreater(following, u)
        self.assertGreater(guarded, 0)

    def test_named_prime_branch_and_invalid_composite_continuation(self):
        cofactors = [23, 41, 71, 121]
        for i, (u, following) in enumerate(zip(cofactors, cofactors[1:])):
            self.assertEqual(factorize(u, max_work=verify.MAX_WORK), [(u, 1)])
            self.assertEqual(gcd(u, 84), 1)
            self.assertEqual(Fraction(5 * u + 8, 3), following)
            self.assertEqual(verify.valuation(u + 4, 3), 3 - i)
            # Unrolled balance has zero composite correction on this prefix.
            k = i + 1
            self.assertEqual(3 ** k * (following + 4), 5 ** k * 27)
        self.assertEqual(factorize(121), [(11, 2)])
        self.assertEqual(verify.valuation(125, 3), 0)
        self.assertEqual(aliquot_sum(84 * 121), 19628)
        self.assertNotEqual(19628 % 84, 0)
        self.assertEqual(Fraction(5 * 121 + 8, 3), Fraction(613, 3))

    def test_arbitrary_recharge_examples_one_step_each(self):
        self.assertEqual(len(self.evidence["recharges"]), 6)
        for row in self.evidence["recharges"]:
            self.assertEqual(row["status"], "witness")
            q, u, following = (int(row[key]) for key in ("q", "u", "next_u"))
            k = row["k"]
            self.assertEqual(factorize(q, max_work=verify.MAX_WORK), [(q, 1)])
            self.assertEqual(q % 70, 1)
            self.assertEqual((11 * q + 20) % (3 ** (k + 1)), 3 ** k)
            self.assertEqual(u, 5 * q)
            self.assertEqual(following, 11 * q + 16)
            self.assertEqual(gcd(u, 84), 1)
            self.assertEqual(gcd(following, 84), 1)
            self.assertEqual(verify.valuation(u + 4, 3), 0)
            self.assertEqual(verify.valuation(following + 4, 3), k)
            self.assertEqual(following % 5, 2)  # Supplying factor is not retained.
            self.assertGreater(following + 4, u + 4)
            self.assertEqual(3 * (following + 4),
                             5 * (u + 4) + 8 * (q + 5))
            self.assertEqual(verify.divisor_pair_sum(84 * u), 84 * following)

    def test_linear_log_valuation_height_has_conflicting_sign_requirements(self):
        # No floating logarithms. These exact signs imply the inequalities in
        # REPORT.md: b >= a*log(5/3)>0 on the prime edge, but an increase on refill.
        self.assertEqual(Fraction(41 + 4, 23 + 4), Fraction(5, 3))
        self.assertEqual(verify.valuation(45, 3) - verify.valuation(27, 3), -1)
        row = self.evidence["recharges"][0]
        u, following = int(row["u"]), int(row["next_u"])
        self.assertGreater(Fraction(following + 4, u + 4), 1)
        self.assertGreater(verify.valuation(following + 4, 3)
                           - verify.valuation(u + 4, 3), 0)

    def test_progression_exit_has_two_primes_larger_than_every_allowed_core(self):
        row = self.evidence["forced_exit"]
        self.assertEqual(row["status"], "witness")
        p = int(row["p"])
        following = int(row["edge"]["successor"])
        self.assertEqual(factorize(p, max_work=verify.MAX_WORK), [(p, 1)])
        self.assertEqual(p % 12, 11)
        self.assertEqual(following, 22 * p + 42)
        for ell in (23, 29):
            self.assertEqual(factorize(ell), [(ell, 1)])
            self.assertGreater(ell, 20)
            self.assertEqual(verify.valuation(following, ell), 1)
        # All cores c in 1..20 are covered: whenever c divides the successor,
        # its remaining cofactor has both forced primes and so is not prime.
        for c in range(1, 21):
            if following % c == 0:
                cofactor = following // c
                self.assertEqual(cofactor % (23 * 29), 0)
                self.assertGreaterEqual(cofactor, 23 * 29)
        self.assertEqual(verify.divisor_pair_sum(20 * p), following)

    def test_serialized_evidence_reproduces_exactly(self):
        expected = json.loads((DIRECTORY / "evidence.json").read_text())
        self.assertEqual(self.evidence, expected)
        totals = self.evidence["totals"]
        self.assertEqual(totals["checked_edges"], 11)
        self.assertEqual(totals["progression_candidates_tested"], 14)
        self.assertEqual(totals["unresolved_candidate_factorizations"], 0)
        self.assertEqual(totals["unresolved_cases"], [])
        self.assertEqual(totals["divisor_pair_candidates"], 40_455)

    def test_computation_limits_remain_unresolved(self):
        result = verify.find_prime(49, 100, 1, max_candidates=1, max_work=1)
        self.assertIsNone(result["prime"])
        self.assertEqual(result["status"], "candidate_limit")
        self.assertEqual(result["unresolved_candidates"], ["49"])
        with self.assertRaises(ComputationLimit):
            verify.checked_edge(49, 8, max_work=1)
        result = verify.find_prime(11, 12, 20, source_cap=100)
        self.assertEqual(result["status"], "source_cap")
        self.assertEqual(result["tested"], 0)
        with self.assertRaises(ComputationLimit):
            verify.checked_edge(verify.SOURCE_CAP + 1, 0)

    def test_invalid_arguments_do_not_extend_s_to_zero(self):
        for n in (0, -1):
            with self.assertRaises(ValueError):
                verify.divisor_pair_sum(n)
            with self.assertRaises(ValueError):
                verify.valuation(n, 3)
        for k in (0, 7):
            with self.assertRaises(ValueError):
                verify.recharge_progression(k)
        with self.assertRaises(ValueError):
            verify.crt_pair(1, 6, 1, 9)
        with self.assertRaises(ValueError):
            verify.find_prime(1, 2, 1, max_candidates=257)
        self.assertEqual(verify.divisor_pair_sum(1), 0)


if __name__ == "__main__":
    unittest.main()
