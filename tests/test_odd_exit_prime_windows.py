"""Two fixed arithmetic examples; neither tests GRH nor samples prime windows."""

from itertools import product
from math import gcd, prod
import unittest

from aliquot import aliquot_sum
from aliquot.two_adic import _divisor_pair_sum


def quadratic(p):
    return 7 * p**2 + 13 * p + 13


class OddExitPrimeWindowTests(unittest.TestCase):
    def test_rough_quadratic_drops_below_seed(self):
        p = 659
        self.assertEqual(_divisor_pair_sum(p), 1)
        self.assertEqual(p % 12, 11)
        for q in (2, 3, 5, 7, 11):
            self.assertEqual(p % q, 1 if q == 7 else q - 1)
            self.assertNotEqual(quadratic(p) % q, 0)
        n0, n1, n2 = 7_817_058, 9_145_641, 3_068_119
        self.assertEqual((n0, n1), (18 * p**2, 3 * quadratic(p)))
        for n, successor in ((n0, n1), (n1, n2)):
            self.assertEqual(aliquot_sum(n), successor)
            self.assertEqual(_divisor_pair_sum(n), successor)
        self.assertLess(7 * n0, 18 * n2)
        self.assertLess(n2, n0)

    def checked_edge(self, n, factors):
        # The huge seed is already factored by construction. Check the
        # certificate, then enumerate divisors rather than trial-factoring n.
        self.assertEqual(prod(q**e for q, e in factors), n)
        for q, _ in factors:
            self.assertEqual(_divisor_pair_sum(q), 1)
        powers = [[q**k for k in range(e + 1)] for q, e in factors]
        return sum(prod(choice) for choice in product(*powers)) - n

    def test_one_exact_prime_link_preserves_abundant_divisor(self):
        d, r, p = 8_085, 711_479, 51_342_010_523
        self.assertEqual(_divisor_pair_sum(d), 8_331)
        self.assertEqual((p % (4 * d), p % 12), (29_063, 11))
        self.assertEqual(((r + 1) % (4 * d), r % 13), (0, 2))
        n0 = 18 * p**2
        n1 = self.checked_edge(n0, [(2, 1), (3, 2), (p, 2)])
        self.assertEqual(n1, 3 * quadratic(p))
        self.assertEqual(gcd(n1, r**2), r)  # divisible once, not twice
        n2 = self.checked_edge(n1, [(3, 1), (5, 1), (7, 2), (11, 2), (59, 1),
                                    (r, 1), (14_827_851_587, 1)])
        self.assertEqual(n2, aliquot_sum(n1))
        self.assertEqual((n1 % d, n2 % d, (n1 + n2) % (r + 1)), (0, 0, 0))
        self.assertEqual((n1 % 4, n2 % 4), (1, 3))
        self.assertLess(n0, n1)
        self.assertLess(n1, n2)
