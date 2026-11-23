"""Bounded arithmetic for the 276 frontier and the Hankel indexing convention."""

from fractions import Fraction
from itertools import product
from math import factorial, gcd, isqrt, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.certified import CertifiedFactorizer, verify_certificates, verify_factor_product
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

    def test_minimum_height_before_the_first_drop(self):
        # These are LOWER bounds, not computed values of n[2164] or n[2166].
        self.assertEqual((11 * (A-D), 7 * 313_566), (9 * 313_566, 6 * 365_827))
        self.assertGreater(365_827 * C, 123 * 10**213)
        self.assertGreater(49 * 313_566 * C, 36 * 2 * FRONTIER)
        for d, ratio in ((12, Fraction(4, 3)), (18, Fraction(7, 6))):
            self.assertEqual(Fraction(_divisor_pair_sum(d), d), ratio)
        # Losing six is not itself the drop; test both the exit and retained cases.
        for x, y in ((24, 36), (36, 55), (55, 17), (6*7, 54), (6*25, 222)):
            self.assertEqual(aliquot_sum(x), y)
            self.assertEqual(_divisor_pair_sum(x), y)
            if x % 6 == 0 and gcd(x//6, 6) == 1:
                self.assertEqual(y, 6*(x//6 + 2*_divisor_pair_sum(x//6)))

    def test_even_three_exponent_is_enough_not_necessary(self):
        # A fully specified comparison U with an odd-power prime -1 modulo 9.
        # Its residue mod 3 is the one needed for the second supplying prime.
        u = 17 * 53
        sig = u + _divisor_pair_sum(u)
        self.assertEqual((u % 3, 17 % 9, sig % 27), (1, 8, 0))
        self.assertEqual((20*sig - 9*u) % 27, 18)
        # Actual comparison from the partially factored starting shape, not 276.
        v = 864_212_542_407
        self.assertTrue(v % 3**4 == 0 and v % 3**5 != 0)
        self.assertEqual((v//3**4) % 8, 7)
        self.assertEqual((3*v + aliquot_sum(3*v)) % 8, 0)
        # v3(V) odd and 2 || sigma(3V) do not themselves force failure.
        path = (1962, 2328, 3552, 6024)
        self.assertEqual((path[0]//6) % 40, 7)
        self.assertEqual((981 + _divisor_pair_sum(981)) % 4, 2)
        for source, target in zip(path, path[1:]):
            self.assertEqual(_divisor_pair_sum(source), target)
            self.assertGreater(target, source)

    def check_factored_path(self, path, factors):
        engine = CertifiedFactorizer(max_work=600_000, max_bits=128)
        primes = {p for fs in factors for p, _ in fs}
        for p in sorted(primes):
            self.assertEqual(engine.factor(p), ((p, 1),))
        self.assertTrue(primes <= verify_certificates(engine.export_certificates()))
        for source, target, fs in zip(path[:-1], path[1:], factors, strict=True):
            verify_factor_product(fs, source)
            self.assertEqual(len({p for p, _ in fs}), len(fs))
            powers = [[p**j for j in range(e+1)] for p, e in fs]
            self.assertEqual(sum(prod(v) for v in product(*powers)) - source, target)

    def test_composite_frontier_control_that_loses_three_then_falls(self):
        p, r = 50_534_167_632_757_103, 11_018_450_976_700_873
        q, l = 1_121_145_820_747_798_016_134_949, 163_500_432_192_387_210_686_347
        f, g = 705_644_834_009, 15_002_806_616_341
        c = 1009 * p
        self.assertEqual(c, 50_988_975_141_451_916_927)
        self.assertEqual((c % 201_600, gcd(c, D*factorial(1000))), (C % 201_600, 1))
        path = (D*c, 54*13**2*19**4*r, 18*q, 144*l, 4*f*g, 31_759_958_953_481_174_835_975_664)
        factors = (((2, 1), (3, 3), (41, 1), (89, 1), (1009, 1), (p, 1)),
                   ((2, 1), (3, 3), (13, 2), (19, 4), (r, 1)),
                   ((2, 1), (3, 2), (q, 1)), ((2, 4), (3, 2), (l, 1)),
                   ((2, 2), (f, 1), (g, 1)))
        self.check_factored_path(path, factors)
        self.assertEqual(7*q + 13, 48*l)
        self.assertEqual(path[4], 42_346_611_937_828_287_567_764_276)
        self.assertEqual([y > x for x, y in zip(path, path[1:])], [True]*4 + [False])
        self.assertEqual((gcd(path[4], 6), path[4] > 2*path[0]), (2, True))

    def test_square_then_prime_at_the_six_v_stage_only(self):
        v, z = 626_248_946_367, 12_198_452_524_207
        y = (6 * 390_764)**2
        self.assertEqual(v % 40, 7)
        self.check_factored_path((6*v, y, z, 1), (
            ((2, 1), (3, 4), (11, 2), (191_689_301, 1)),
            ((2, 6), (3, 2), (11, 2), (83, 2), (107, 2)), ((z, 1),)))

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

    def test_first_failed_prediction_and_next_odd_leading_order(self):
        prefix = [276, 396, 696, 1104]
        for x, y in zip(prefix, prefix[1:]):
            self.assertEqual(_divisor_pair_sum(x), y)
        # Crossing 718 decides every height bit needed for a size-360 matrix.
        bits = [record_bit(276, m) for m in range(719)]
        self.assertEqual([i for i, b in enumerate(bits) if b], prefix[:-1])
        powers = (37, 157, 277)
        errors = [sum(bits[i+j] for j in powers) % 2 for i in range(360)]
        self.assertEqual(errors, [0]*359 + [1])
        self.assertEqual(359 + max(powers), 636)  # predicted record, actual zero
        # Direct elimination, independent of the polynomial-discrepancy identity.
        self.assertEqual([n for n in range(275, 360) if hankel_mod_two(bits, n)], [276, 359])

    def test_prime_exclusions_and_forced_jump_in_a_recurrence(self):
        # A formal binary recurrence, NOT the record word of 276.
        def bit(n):
            return int(gcd(n, 6) == 1)
        self.assertTrue(all(bit(n) ^ bit(n+2) ^ bit(n+4) == 0 for n in range(6)))
        sums = (0, 3, 4, 7)  # CRT subset sums for rejected primes 2 and 3
        minor = [[bit(1+s-t) for t in sums] for s in sums]
        self.assertEqual(minor, [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]])
        accepted = (5, 7, 11, 13, 17, 19, 23, 29, 31)
        d = prod(accepted)
        self.assertLessEqual(prod(Fraction(p+1, p) for p in accepted[:-1]), 2)
        self.assertGreater(prod(Fraction(p+1, p) for p in accepted), 2)
        m = 5*d
        self.assertEqual((bit(m), bit(m+4)), (1, 1))
        self.assertEqual(aliquot_sum(m), _divisor_pair_sum(m))
        self.assertGreater(aliquot_sum(m), m+4)  # if m is a record, m+4 cannot be

    def test_stride_18_fence_and_zero_tail_control(self):
        self.assertEqual(Fraction(_divisor_pair_sum(18), 18), Fraction(7, 6))
        k = 10**215
        self.assertTrue((A * Fraction(1001, 1000)**69 - D)*C < k < 11*(A-D)*C//9)
        self.assertLess(24*(k+1), 25*k)
        # A genuine orbit with one last odd determinant and no more records.
        for x, y in zip((18, 21, 11, 1), (21, 11, 1, 0)):
            self.assertEqual(_divisor_pair_sum(x), y)
        bits = [record_bit(18, m) for m in range(51)]
        self.assertEqual([m for m, b in enumerate(bits) if b], [18, 21])
        self.assertEqual(hankel_mod_two(bits, 21), 1)
        self.assertTrue(all(hankel_mod_two(bits, n) == 0 for n in range(22, 26)))
