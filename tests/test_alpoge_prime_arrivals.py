"""Finite witnesses for large-prime arrivals and the finite-core return argument."""

from math import lcm
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum


class AlpogePrimeArrivalTests(unittest.TestCase):
    def check_path(self, path):
        for n, successor in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(n), successor)
            self.assertEqual(_divisor_pair_sum(n), successor)

    def test_three_new_primes_and_the_exponent_progression(self):
        core, e = 30 * 29, 5
        path = (14_622_090, 27_731_190, 41_133_066)
        self.assertEqual(path[0], core * 7**e)
        self.check_path(path)
        seed_primes = {p for p, _ in factorize(path[0])}
        arrivals = {p for p, _ in factorize(path[1]) if p > max(seed_primes)}
        self.assertEqual(seed_primes, {2, 3, 5, 7, 29})
        self.assertEqual(arrivals, {53, 107, 163})
        self.assertTrue(all(n % 5 == 0 and n < m for n, m in zip(path, path[1:])))
        sigma = core + _divisor_pair_sum(core)
        coeff = 7 * sigma - 6 * core
        self.assertEqual(coeff * 7**e - sigma, 6 * path[1])
        # Keep each prime at the first image when moving along the refined
        # exponent progression. No enormous integer or later iterate is needed.
        period = lcm(*(p - 1 for p in arrivals))
        for k in (0, 1, 17):
            for p in arrivals:
                self.assertEqual((coeff * pow(7, e + k*period, p) - sigma) % p, 0)

    def test_two_supplier_steps_and_an_extreme_residue_count(self):
        r1, r2 = 29, 25_229
        self.assertEqual(r2 + 1, 30 * r1**2)
        path = (153_644_610, 282_329_790, 418_629_090, 744_660_510)
        self.assertEqual(path[0], 30 * r1 * r2 * 7)
        self.assertEqual(factorize(path[0])[-1], (r2, 1))
        self.assertEqual(factorize(path[1])[-2:], [(r1, 1), (324_517, 1)])
        self.check_path(path)
        self.assertTrue(all(n % 30 == 0 and 5*m >= 7*n for n, m in zip(path, path[1:])))
        # TranslateMean with T={0}: count indices, not distinct residues.
        counts = [sum(n % 5 == u for n in path[:-1]) for u in range(5)]
        self.assertEqual(sum(counts), len(path) - 1)
        self.assertEqual(counts, [3, 0, 0, 0, 0])

    def test_return_of_prime_alone_does_not_force_return_of_term(self):
        path = (276, 396, 696, 1104)
        self.check_path(path)
        p = 23
        self.assertEqual([n % p for n in path], [0, 5, 6, 0])
        self.assertEqual((path[0] // p, path[-1] // p), (12, 48))

    def test_permutation_returns_on_a_true_cycle(self):
        # Start from 284=4*71, so the tracked starting residue is zero. After
        # two steps it returns, but the two-step permutation isn't the identity.
        self.check_path((284, 220, 284))
        p = 71
        self.assertEqual((284 // 4, 220 // 20), (p, 11))
        identity = list(range(p))
        image = identity[:]
        for t in range(1, 141):
            d = 4 if t % 2 else 20
            s = _divisor_pair_sum(d)
            image = [(s * pow(d, -1, p) * x + d + s) % p for x in image]
            self.assertEqual(sorted(image), identity)
            self.assertEqual(image[0], (220 if t % 2 else 284) % p)
            if t == 2:
                self.assertEqual(image, [31*x % p for x in identity])
            self.assertEqual(image == identity, t == 140)
