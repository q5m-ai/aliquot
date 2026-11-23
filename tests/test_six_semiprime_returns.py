"""Exact finite witnesses, not a test of an asymptotic or an infinite orbit."""

from collections import Counter
from math import gcd, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum


class SixSemiprimeReturnTests(unittest.TestCase):
    def check_step(self, p, q, output):
        u = p * q
        self.assertLess(3, p)
        self.assertLess(p, q)
        self.assertEqual(factorize(u), [(p, 1), (q, 1)])
        self.assertEqual((p + 2) * (q + 2) - 2, output)
        self.assertEqual(aliquot_sum(6 * u), 6 * output)
        self.assertEqual(_divisor_pair_sum(6 * u), 6 * output)
        self.assertGreater(output, u)
        self.assertEqual(gcd(output, 6), 1)
        self.assertNotEqual(output % q, 0)
        self.assertEqual(output % p == 0, (q + 1) % p == 0)

    def test_uninterrupted_visit_spends_exactly_two_factors_of_five(self):
        p = 5
        partners = (19, 29, 43)
        shifted = tuple(q + p + 1 for q in partners)
        self.assertEqual(shifted, (5**2, 5 * 7, 7**2))
        for a, b in zip(shifted, shifted[1:]):
            self.assertEqual(p * b, (p + 2) * a)
        start, end = p * partners[0], 313
        for q, output in zip(partners, (145, 215, end)):
            self.check_step(p, q, output)
        self.assertEqual(factorize(end), [(end, 1)])
        k = len(partners)  # includes the source which exits
        self.assertLessEqual(p**k, 2 * start)
        self.assertLess(p**k * end, (p + 4)**k * start)
        # Retaining the divisor alone is not another semiprime transition.
        self.check_step(5, 59, 425)
        self.assertEqual(factorize(425), [(5, 2), (17, 1)])

    def test_three_separate_visits_on_one_actual_orbit(self):
        pairs = ((11, 337), (5, 881), (37, 167), (11, 599),
                 (73, 107), (11, 743), (23, 421), (97, 109))
        cofactors = [p*q for p, q in pairs] + [10_987]
        self.assertEqual(cofactors[0], 3707)
        for (p, q), u, v in zip(pairs, cofactors, cofactors[1:]):
            self.check_step(p, q, v)
            self.assertEqual(gcd(u, v), 1)
        self.assertEqual([i for i, (p, _) in enumerate(pairs) if p == 11],
                         [0, 3, 5])
        self.assertEqual(factorize(cofactors[-1]), [(10_987, 1)])

    def test_alternating_returns_and_the_two_exceptional_subgroups(self):
        self.check_step(11, 1663, 23 * 941)
        self.check_step(23, 941, 11 * 2143)
        self.assertEqual(factorize(2143), [(2143, 1)])
        # One round spends exactly one factor of 253 from 3*1663+71.
        shifts = (3 * 1663 + 71, 3 * 941 + 37, 3 * 2143 + 71)
        self.assertEqual(shifts, (253 * 20, 143 * 20, 325 * 20))
        self.assertNotEqual(shifts[-1] % 253, 0)
        for r, order in ((37, 3), (71, 10)):
            ratio = 325 * pow(253, -1, r) % r
            subgroup = {pow(ratio, j, r) for j in range(r - 1)}
            self.assertEqual(len(subgroup), order)
            self.assertLess(order, r - 1)
        # Check the local avoidance statement on integer forms, without
        # treating primality of a family of linear forms as a theorem.
        for h in (1, 3, 12):
            forms = [(253**(h-j) * 325**j, 71) for j in range(h + 1)]
            forms += [(143 * 253**(h-j-1) * 325**j, 37) for j in range(h)]
            self.assertTrue(all((2*c - d) % 3 == 0 for c, d in forms))
            for r in (2, 3, 5, 11, 13, 23, 37, 71):
                self.assertTrue(any(all((c*z + (2*c - d)//3) % r for c, d in forms)
                                    for z in range(r)))

    def test_exact_residue_fractions_combine_at_fixed_modulus(self):
        probes = (5, 7, 11)
        modulus = prod(probes)
        units = [a for a in range(modulus) if gcd(a, modulus) == 1]
        masks = Counter()
        for a in units:
            for b in units:
                v = (a + 2) * (b + 2) - 2
                masks[tuple(v % r == 0 for r in probes)] += 1
        self.assertEqual(len(masks), 2**len(probes))
        for mask, count in masks.items():
            self.assertEqual(count, prod(r - 3 if hit else (r - 1)**2 - (r - 3)
                                         for r, hit in zip(probes, mask)))
        # One actual prime pair hitting all three probes; multiplicities differ.
        self.check_step(37, 541, 21_175)
        self.assertEqual(factorize(21_175), [(5, 2), (7, 1), (11, 2)])
