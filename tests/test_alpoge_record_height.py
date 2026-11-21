"""Exact fixed-orbit checks; no sampling of seeds or asymptotic estimates."""

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations
from math import gcd, isqrt, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum


def determinant(rows):
    """Cofactor expansion for the small sparse integer witness matrices."""
    @cache
    def minor(cols):
        if not cols:
            return 1
        row = rows[len(rows) - len(cols)]
        return sum((-1)**i * row[c] * minor(cols[:i] + cols[i + 1:])
                   for i, c in enumerate(cols) if row[c])
    return minor(tuple(range(len(rows))))


class AlpogeRecordHeightTests(unittest.TestCase):
    def test_determinant_contracts_but_orbit_channel_does_not(self):
        # For these single-source blocks 23 = -1 mod lcm(8,n), 23 > n.
        q = 23
        H = sorted({a*a % q for a in range(1, q)})
        self.assertEqual(len(H), 11)
        self.assertNotIn(q - 1, H)
        for n, energy, det in ((6, Fraction(7, 18), 610374),
                               (12, Fraction(11, 24), 568377232)):
            divs = [d for d in range(1, n) if n % d == 0]
            self.assertTrue(set(divs) <= set(H))
            # n*K_n on the odd space in square coordinates. The row sum is
            # the eigenvalue on xi; the squared row norm gives the mean square.
            rows = [[sum(d for d in divs if d*x % q == y) for y in H] for x in H]
            self.assertEqual({sum(row) for row in rows}, {aliquot_sum(n)})
            self.assertGreaterEqual(aliquot_sum(n), n)
            self.assertEqual({Fraction(sum(a*a for a in row), n*n) for row in rows},
                             {energy})
            self.assertEqual(determinant(rows), det)
            self.assertLessEqual(Fraction(det, n**len(H))**2, energy**len(H))
            self.assertLess(energy, Fraction(3, 4))

    def test_reversing_translations_gives_the_full_euler_factors(self):
        q = 383
        for n in (12, 16):
            # Both sides as exact coefficient vectors in the group algebra.
            left = Counter({1: Fraction(1)})
            for d in range(1, n):
                if n % d == 0:
                    left[d * pow(n, -1, q) % q] += Fraction(d, n)
            right = {1: Fraction(1)}
            for p, e in factorize(n):
                out = Counter()
                for x, v in right.items():
                    for k in range(e + 1):
                        out[x * pow(p, -k, q) % q] += v / p**k
                right = out
            self.assertEqual(left, right)
            self.assertEqual(sum(left.values()), 1 + Fraction(aliquot_sum(n), n))

    def test_first_crossing_requires_odd_prime_reuse(self):
        path = (276, 396, 696, 1104, 1872, 3770, 3790, 3050, 2716, 2772,
                5964, 10164, 19628, 19684, 22876, 26404)
        seed, bound = path[0], 25_000
        primes = [p for p in range(3, bound, 2)
                  if all(p % d for d in range(3, isqrt(p) + 1, 2))]
        # Compute the no-reuse fence from seed and threshold, not the path.
        e_odd = Fraction(prod(primes), prod(p - 1 for p in primes))
        self.assertLess(e_odd, Fraction(19, 2))
        self.assertEqual(seed * Fraction(19, 2)**2, 24909)
        self.assertLess(seed * e_odd**2, bound)

        peak = seed
        counts, records = Counter(), []
        for j, (n, successor) in enumerate(zip(path, path[1:])):
            self.assertLess(n, bound)
            self.assertEqual(aliquot_sum(n), successor)
            self.assertEqual(_divisor_pair_sum(n), successor)
            if successor > peak:
                counts.update(p for p, _ in factorize(n) if p != 2)
                records.append(j)
                peak = successor
        self.assertGreaterEqual(peak, bound)
        self.assertEqual(records, [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14])
        self.assertEqual(counts[3], 8)  # once per source, not per exponent
        self.assertLessEqual(Fraction(peak, seed),
                             prod(Fraction(p, p - 1)**(2*c) for p, c in counts.items()))

    def test_clean_six_can_use_fresh_primes_until_exit(self):
        u = (47, 49, 65, 103, 105)
        self.assertTrue(all(gcd(a, b) == 1 for a, b in combinations(u[:-1], 2)))
        counts = Counter()
        for a, b in zip(u, u[1:]):
            self.assertEqual(gcd(a, 6), 1)
            self.assertEqual(_divisor_pair_sum(6*a), 6*b)
            self.assertEqual(a + 2*aliquot_sum(a), b)
            self.assertLessEqual(Fraction(b, a), (1 + Fraction(aliquot_sum(a), a))**2)
            counts.update(p for p, _ in factorize(a))
        self.assertEqual(counts, Counter([5, 7, 13, 47, 103]))
        self.assertLess(Fraction(u[-1], u[0]), prod(Fraction(p, p - 1)**2 for p in counts))
        self.assertEqual(gcd(u[-1], 6), 3)
