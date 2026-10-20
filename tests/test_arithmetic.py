import math
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize
from aliquot.research import divisor_sieve


class ArithmeticTests(unittest.TestCase):
    def test_direct_divisor_enumeration(self):
        for n in range(1, 301):
            self.assertEqual(aliquot_sum(n), sum(d for d in range(1, n) if n % d == 0))
            factors = factorize(n)
            self.assertEqual(math.prod(p ** e for p, e in factors), n)
            for p, _ in factors:
                self.assertTrue(all(p % d for d in range(2, math.isqrt(p) + 1)))
        self.assertEqual(factorize(1), [])
        self.assertEqual(factorize(999983), [(999983, 1)])
        self.assertEqual(aliquot_sum(1_000_000), 1_480_437)

    def test_independent_additive_sieve(self):
        sums = divisor_sieve(10_000)
        self.assertIsNone(sums[0])
        for n in range(1, len(sums)):
            self.assertEqual(aliquot_sum(n), sums[n], f"s({n})")

    def test_arbitrary_precision_above_old_ceiling(self):
        for e in [50, 100, 1000, 2000, 15000]:
            self.assertEqual(aliquot_sum(2 ** e), 2 ** e - 1)
        n = 2 ** 80 * 3 ** 40
        sigma = (2 ** 81 - 1) * (3 ** 41 - 1) // 2
        self.assertEqual(aliquot_sum(n), sigma - n)
        self.assertGreater(aliquot_sum(10 ** 15), 10 ** 15)

    def test_budget_is_explicit_and_never_accepts_unfactored_residual(self):
        with self.assertRaises(ComputationLimit):
            aliquot_sum(999983, max_work=10)
        with self.assertRaises(ComputationLimit):
            factorize(2 ** 100, max_work=10)  # Repeated divisions also cost work.
        self.assertEqual(aliquot_sum(4, max_work=3), 3)
        with self.assertRaises(ComputationLimit):
            aliquot_sum(4, max_work=2)

    def test_invalid_inputs_and_no_s_zero_extension(self):
        for n in [0, -1, True, False, 1.0, "12", None]:
            with self.subTest(n=n), self.assertRaises(ValueError):
                aliquot_sum(n)
        for budget in [0, -1, True, 1.5, None]:
            with self.assertRaises(ValueError):
                factorize(12, max_work=budget)
