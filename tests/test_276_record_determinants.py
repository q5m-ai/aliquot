"""Bounded arithmetic for the 276 frontier and the Hankel indexing convention."""

from fractions import Fraction
from math import factorial, gcd, isqrt, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum


# Separate decimal fields from FactorDB's row 2162 and its remaining-cofactor field.
FRONTIER = int(
    "663794681153746999196731890055148811593408713676931896342703588592299586"
    "045282019842870918786678296761814689316893738132115742241327609778569226"
    "81054039015071929567302762304410477445787467582388823154028545135207242"
)
C = int(
    "3368729541090643804983262233464007447973613844873440193369586739097975"
    "0212908763427974732741932254233113825671005437214260413418253991950030"
    "4105036661688210224666155632503600227751112874494191147362311483334527"
)
D = 2 * 3**3 * 41 * 89
A = 453_600


def record_bit(seed, m):
    """No knowledge of an infinite tail: stop as soon as m is reached or passed."""
    x, seen = seed, set()
    while 0 < x < m and x not in seen:
        seen.add(x)
        x = aliquot_sum(x)
    return int(x > 0 and x == m)


def hankel_mod_two(bits, n):
    """Gaussian elimination on a leading (n+1)-square, using packed rows."""
    rows = [sum(bits[i+j] << j for j in range(n+1)) for i in range(n+1)]
    for col in range(n+1):
        pivot = next((i for i in range(col, n+1) if rows[i] >> col & 1), None)
        if pivot is None:
            return 0
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for i in range(col+1, n+1):
            if rows[i] >> col & 1:
                rows[i] ^= rows[col]
    return 1


class Fixed276RecordTests(unittest.TestCase):
    def test_partial_factorization_and_divisor_pairing(self):
        self.assertEqual(D * C, FRONTIER)
        self.assertEqual((len(str(FRONTIER)), len(str(C))), (215, 210))
        self.assertEqual(gcd(C, D), 1)
        self.assertEqual(D + _divisor_pair_sum(D), A)
        self.assertEqual(54 + aliquot_sum(54), 120)
        self.assertEqual(C % 201_600, 179_327)
        for d in range(1, 24):
            if gcd(d, 24) == 1:
                self.assertEqual((d + C*pow(d, -1, 24)) % 24, 0)
        # U = 8400 sigma(C) - 3649 C, with 24 | sigma(C).
        u = -3649 * C % 201_600
        self.assertEqual(u, 29_377)
        self.assertEqual(gcd(u, 210), 1)
        self.assertNotIn(u % 5, {d*d % 5 for d in range(5)})
        self.assertEqual((-9*u) % 40, 7)  # 20 sigma(U) is 0 modulo 40
        self.assertNotIn(3*7 % 8, {d*d % 8 for d in range(8)})

    def test_decimal_crossing_without_a_value_for_sigma_c(self):
        ten = 10**215
        self.assertEqual(gcd(C, factorial(1000)), 1)
        self.assertGreater(1001**70, C)
        self.assertLess((A * Fraction(1001, 1000)**69 - D) * C, ten)
        self.assertGreater(11 * (A-D) * C, 9 * ten)
        # U < 10^214; primes above 150 make at most 98 Euler factors.
        self.assertGreater(151**99, 10**214)
        small = [p for p in range(11, 151) if all(p % i for i in range(2, isqrt(p)+1))]
        bound = prod(Fraction(p, p-1) for p in small) * Fraction(151, 150)**98
        self.assertLess(bound, 4)
        self.assertLess(Fraction(20, 9) * bound - 1, 8)
        gap = (A-2*D) * C
        self.assertTrue(2 * 10**214 < gap < FRONTIER)
        self.assertEqual(gap % 4, 0)

    def test_same_input_residues_different_second_cofactor(self):
        for c, u, v in ((4_614_527, 21_962_333_377, 290_719_006_007),
                        (16_307_327, 77_617_642_177, 864_212_542_407)):
            with self.subTest(c=c):
                self.assertEqual(c % 201_600, C % 201_600)
                self.assertEqual(gcd(c, factorial(1000) * D), 1)
                self.assertEqual(len(factorize(c)), 2)
                self.assertEqual(8400*(c + _divisor_pair_sum(c)) - 3649*c, u)
                self.assertEqual(aliquot_sum(D*c), 54*u)
                self.assertEqual(20*(u + _divisor_pair_sum(u)) - 9*u, v)
                self.assertEqual(aliquot_sum(54*u), 6*v)
                self.assertEqual(v % 40, 7)
        self.assertEqual((290_719_006_007 % 3, 864_212_542_407 % 3), (2, 0))

    def test_terminating_control_for_second_image_residue(self):
        path = [522, 648, 1167, 393, 135, 105, 87, 33, 15, 9, 4, 3, 1, 0]
        self.assertEqual((path[0]//6) % 40, 7)
        for source, target in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(source), target)
            self.assertEqual(_divisor_pair_sum(source), target)

    def test_record_bits_and_leading_hankel_on_resolved_seeds(self):
        for seed, expected in ((1, {1}), (6, {6}), (12, {12, 16}), (220, {220, 284})):
            self.assertEqual({m for m in range(max(expected)+3) if record_bit(seed, m)}, expected)
        # Shift the origin to 10: the last record on the orbit of 12 has index 6.
        bits = [record_bit(12, 10+j) for j in range(17)]
        self.assertEqual([hankel_mod_two(bits, n) for n in (2, 6, 7, 8)], [1, 1, 0, 0])
        # The 1872 -> 3770 jump in the real orbit of 276 skips (1872, 2*1872].
        prefix = [276, 396, 696, 1104, 1872, 3770]
        for x, y in zip(prefix, prefix[1:]):
            self.assertEqual(_divisor_pair_sum(x), y)
        self.assertGreater(prefix[-1], 2*prefix[-2])
        # Scale the same triangular-minor check down, but use actual record bits.
        r, g = 396, 7
        bits = [record_bit(276, m) for m in range(r-g, r+g+1)]
        self.assertEqual(bits[g:], [1] + [0]*g)
        self.assertEqual(hankel_mod_two(bits, g), 1)
