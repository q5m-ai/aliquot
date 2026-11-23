"""Exact finite checks for the signed indices and split determinants, not an orbit census."""

from fractions import Fraction as F
from itertools import combinations
from math import lcm, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum


def slopes(word):
    values = [F(1)]
    for p in word:
        values.append(values[-1] * F(p + 2, p))
    return values


def affine(p, x):
    return F(p + 2, p) * x + 2 * (p + 1)


def d(n):
    def at(p):
        if p <= 3:
            return F(p)
        if p == 7:
            return F(4)
        return F(3, 2) if p % 3 == 2 else F(8, 3)
    return prod(at(p)**e for p, e in factorize(n))


class AlpogeReturnIndexTests(unittest.TestCase):
    def check_path(self, path):
        labels = []
        for u, v in zip(path, path[1:]):
            factors = factorize(u)
            self.assertEqual([e for _, e in factors], [1, 1])
            p, q = (r for r, _ in factors)
            self.assertLess(3, p)
            self.assertLess(p, q)
            labels.append(p)
            self.assertEqual(affine(p, u), v)
            self.assertEqual(aliquot_sum(6*u), 6*v)
            self.assertEqual(_divisor_pair_sum(6*u), 6*v)
        return labels

    def test_cancel_signed_indices_before_taking_denominators(self):
        w = self.check_path([77, 115, 173])
        self.assertEqual(w, [7, 5])
        s = slopes(w)
        self.assertEqual(s, [1, F(9, 7), F(9, 5)])
        modulus = lcm(*(a.denominator for a in s))
        self.assertEqual(modulus, 35)  # all prefixes, not just the endpoint
        for delta in range(-70, 71):
            x = F(77 + delta)
            formal = []
            for p in w:
                x = affine(p, x)
                formal.append(x)
            self.assertEqual(all(v.denominator == 1 for v in formal), delta % 35 == 0)
            self.assertEqual(formal[-1].denominator == 1, delta % 5 == 0)

    def test_denominator_weight_survives_prime_cancellation(self):
        c = F(507, 400)
        # A boundary case for each of the five rows of the proof, not a proof
        # by testing all primes up to a cutoff.
        for p, ratio in ((5, F(200, 147)), (7, F(49, 36)), (11, F(1936, 1521)),
                         (23, F(1587, 1250)), (13, c)):
            self.assertEqual(F(p, p+2)**2 * d(p+2)/d(p), ratio)
            self.assertGreaterEqual(ratio, c)
        word = [251, 23, 11, 13] + [5, 7]*3  # algebraic word, not a claimed orbit
        slope = slopes(word)[-1]
        self.assertEqual(slope, F(3**7, 251))
        self.assertGreaterEqual(slope.denominator, c**len(word) * slope)
        self.assertGreater(c**10, F(7, 5)**7)  # the return-lag constant exceeds 1.7

    def test_same_order_really_matters_on_an_actual_orbit(self):
        path = [235, 341, 427, 565, 803, 973, 1267]
        w = self.check_path(path)
        self.assertEqual(w[:3], [5, 11, 7])
        self.assertEqual(w[:3], w[3:])
        slope = slopes(w[:3])[-1]
        self.assertEqual(slope, F(117, 55))
        a, b = path[3] - path[0], path[6] - path[3]
        self.assertEqual((a, b), (330, 702))
        self.assertEqual(a % slope.denominator, 0)
        self.assertEqual(slope*a, b)
        path = [18_293, 21_643, 23_573, 27_883]
        w = self.check_path(path)
        self.assertEqual(w, [11, 23, 11])
        self.assertEqual(slopes(w[:2])[-1], slopes(w[1:])[-1])
        self.assertEqual(slopes(w[:2])[-1].denominator, 253)
        self.assertEqual((path[1] - path[0]) % 253, 61)  # wrong order

    def test_split_vandermonde_by_next_smaller_prime(self):
        path = [15_095, 21_145, 29_615, 41_473]
        w = self.check_path(path)
        self.assertEqual(w, [5, 5, 5])
        self.assertEqual(factorize(path[-1]), [(67, 1), (619, 1)])
        qs = [u // 5 for u in path[:-1]]
        self.assertEqual(qs, [3019, 4229, 5923])
        successors = w[1:] + [67]
        for q, r in zip(qs, successors):
            self.assertEqual(q % r, (-12 * pow(7, -1, r)) % r)
        # Independent determinant and pair products. Only the same-colour
        # pair (3019,4229) is forced to contribute a factor 5 here.
        a, b, c = qs
        det = b*c*c - b*b*c - a*(c*c - b*b) + a*a*(c-b)
        inside = b-a
        cross = (c-a)*(c-b)
        self.assertEqual(det, prod(y-x for x, y in combinations(qs, 2)))
        self.assertEqual(det, inside * cross)
        self.assertEqual(inside % 5, 0)
        self.assertNotEqual(cross % 5, 0)
        self.assertNotEqual(det % 67, 0)
