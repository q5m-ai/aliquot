"""Finite arithmetic regressions for research/BLOCK-TRANSPORT.md.

The additive sieve checks identities, not universal proofs or orbit closure.
There is no new runtime API and no probabilistic primality testing.
"""

from math import gcd
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.research import divisor_sieve
from aliquot.two_adic import _divisor_pair_sum


class BlockTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sums = divisor_sieve(100_000)

    def s(self, n):
        self.assertGreater(n, 0)
        self.assertLess(n, len(self.sums))
        return self.sums[n]

    def t(self, n):
        return n + 2 * self.s(n)

    def prime(self, n):
        return n > 1 and self.s(n) == 1

    def test_corrected_identities_and_rigid_equality(self):
        for v in range(3, 80, 2):
            for w in range(v + 2, 80, 2):
                if gcd(v, w) != 1:
                    continue
                sv, sw = self.s(v), self.s(w)
                bridge = self.t(v * w)
                next_value = self.t(bridge)
                dv, dw = sv - 1, sw - 1
                defect = 2 * (w + 1) * dv + 2 * (v + 1) * dw + 2 * dv * dw
                shifted_product = (v + 2) * (w + 2)
                adaptive_product = self.t(v) * self.t(w)
                budget = sv * sw
                self.assertEqual(bridge + 2, adaptive_product - 2 * (budget - 1))
                self.assertEqual(bridge + 2, shifted_product + defect)
                self.assertEqual(next_value, shifted_product + defect + 2 * (self.s(bridge) - 1))
                self.assertEqual(next_value, adaptive_product + 2 * (self.s(bridge) - budget))
                self.assertEqual(next_value == shifted_product,
                                 self.prime(v) and self.prime(w) and self.prime(bridge))
                self.assertEqual(next_value == adaptive_product, self.s(bridge) == budget)
                if budget > 1 and bridge > (budget - 1) ** 2:
                    self.assertNotEqual(next_value, adaptive_product)

    def test_coprimality_is_required(self):
        # Multiplying sigma(5) by itself gives the wrong divisor sum at 25.
        self.assertNotEqual(self.t(5 * 5), self.t(5) ** 2 - 2 * self.s(5) ** 2)

    def test_prime_square_budget_obstruction(self):
        primes = [5, 7, 11, 13, 17, 19, 23]
        for q in primes:
            for r in primes:
                if q == r:
                    continue
                bridge = self.t(q * r ** 2)
                self.assertGreater(bridge, r ** 2)
                difference = self.t(bridge) - self.t(q) * self.t(r ** 2)
                if self.prime(bridge):
                    self.assertEqual(difference, -2 * r)
                else:
                    self.assertGreater(difference, 0)
                self.assertNotEqual(difference, 0)
        # The correction really has both signs; neither is a universal budget.
        self.assertEqual(self.t(self.t(5 * 7 ** 2)) - self.t(5) * self.t(7 ** 2), -14)
        self.assertEqual(self.t(self.t(5 * 13 ** 2)) - self.t(5) * self.t(13 ** 2), 374)

    def test_retained_prime_transport_on_bounded_prime_parameters(self):
        primes = [p for p in range(3, 60, 2) if self.prime(p)]
        bridges = guarded_returns = 0
        for a in primes:
            for b in primes:
                for p in primes:
                    if len({a, b, p}) != 3 or (p + 1) % a:
                        continue
                    t = (p + 1) // a
                    block = self.t(a * b)
                    h = t * block + b
                    self.assertEqual(self.t(a * p * b), a * h)
                    other = t * (a + 2) + 1
                    if not self.prime(h):
                        if gcd(a, h) == 1:
                            self.assertEqual(self.t(a * h),
                                             block * other + 2 * (a + 1) * (self.s(h) - 1))
                            self.assertGreater(self.t(a * h), block * other)
                        continue
                    bridges += 1
                    self.assertGreater(h, a)
                    self.assertEqual(self.t(a * h), block * other)
                    if (a % 3 == 1 and b % 3 == p % 3 == 2 and gcd(block, other) == 1
                            and ((self.s(block) + block) % 3 == 0
                                 or (self.s(other) + other) % 3 == 0)):
                        guarded_returns += 1
                        source, middle, target = a * p * b, a * h, block * other
                        self.assertEqual((source % 3, middle % 3, target % 3), (1, 2, 1))
                        self.assertEqual((self.s(source) + source) % 3, 0)
                        self.assertEqual((self.s(target) + target) % 3, 0)
                        for n in (source, middle, target):
                            self.assertEqual(gcd(n, 6), 1)
                        self.assertLess(source, middle)
                        self.assertLess(middle, target)
        self.assertGreater(bridges, 0)
        self.assertGreater(guarded_returns, 0)

    def test_named_composite_supplier_handoff(self):
        a, b, p = 7, 17, 41
        t = (p + 1) // a
        block = self.t(a * b)
        h, other = t * block + b, t * (a + 2) + 1
        self.assertEqual((t, block, h, other), (6, 169, 1031, 55))
        for prime in (a, b, p, h, 4877):
            self.assertEqual(factorize(prime), [(prime, 1)])
        self.assertEqual(factorize(block), [(13, 2)])
        self.assertEqual(factorize(other), [(5, 1), (11, 1)])
        self.assertEqual(gcd(block, other), 1)
        self.assertEqual((self.s(block) + block, self.s(other) + other), (183, 72))
        path = [4877, 4879, 7217, 9295]
        for source, target in zip(path, path[1:]):
            self.assertEqual(gcd(source, 6), 1)
            self.assertEqual(self.t(source), target)
            self.assertEqual(source + 2 * aliquot_sum(source), target)
            self.assertEqual(source + 2 * _divisor_pair_sum(source), target)
            self.assertEqual(aliquot_sum(6 * source), 6 * target)
            self.assertEqual(_divisor_pair_sum(6 * source), 6 * target)
        # The output supplies 3 but does NOT reenter the distinct-prime input template.
        self.assertEqual(factorize(path[-1]), [(5, 1), (11, 1), (13, 2)])
        self.assertNotEqual(sum(e for _, e in factorize(path[-1])), 3)

    def test_shifted_blocks_need_actual_factorization_and_m_is_not_closed(self):
        for path in ([53, 55, 89, 91], [263, 265, 383, 385]):
            for source, target in zip(path, path[1:]):
                self.assertEqual(self.t(source), target)
                self.assertEqual(_divisor_pair_sum(6 * source), 6 * target)
        self.assertEqual(self.t(385), 767)
        self.assertEqual((7 + 2) * (55 + 2) - 2, 511)
        self.assertEqual((self.s(385) + 385) % 3, 0)
        self.assertEqual((self.s(55) + 55) % 3, 0)
        self.assertNotEqual((self.s(91) + 91) % 3, 0)

    def test_quadratic_filter_at_semiprime_and_square_bridges(self):
        primes = [p for p in range(3, 100, 2) if self.prime(p)]
        tested = retained = 0
        for ell in [p for p in primes if p < 50]:
            roots = {a for a in range(1, ell) if a * a % ell == 2}
            for i, a in enumerate(primes):
                for b in primes[i + 1:]:
                    bridge = a * b
                    if (bridge + 2) % ell:
                        continue
                    tested += 1
                    survives = self.t(bridge) % ell == 0
                    self.assertEqual(survives, (a + b) % ell == 0)
                    self.assertEqual(survives, a % ell in roots)
                    if survives:
                        retained += 1
                        if ell % 3 == 2:
                            self.assertIn(ell % 24, (17, 23))
                    if ell in (5, 11):
                        self.assertFalse(survives)
                square = a * a
                if (square + 2) % ell == 0:
                    self.assertNotEqual(self.t(square) % ell, 0)
        self.assertGreater(tested, 0)
        self.assertGreater(retained, 0)
        for bridge, ell, target in [(253, 17, 323), (205, 23, 299)]:
            self.assertEqual((bridge + 2) % ell, 0)
            self.assertEqual(self.t(bridge), target)
            self.assertEqual(target % ell, 0)
            self.assertEqual(gcd(ell, target // ell), 1)
