"""Small fixed witnesses. Integer coefficients throughout, including roots of unity."""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import isqrt, lcm, prod
import unittest

from aliquot import aliquot_sum, factorize


SOURCES = (12, 16)
Q = prod(SOURCES)
PROBE = 383


def proper(n):
    return [d for d in range(1, n) if n % d == 0]


def coefficients_at_prime_root(coeffs):
    """Eliminate z^(p-1) using Phi_p = 1+...+z^(p-1), for p prime."""
    return [v - coeffs[-1] for v in coeffs[:-1]]


class AlpogeOrbitLiftTests(unittest.TestCase):
    def test_reading_a_theta_coefficient_as_an_index_is_not_linear(self):
        # Square the two-square series to compute the four-square coefficients.
        rng = range(-isqrt(33), isqrt(33) + 1)
        pairs = Counter(x*x + y*y for x, y in product(rng, repeat=2))
        a = {}
        for n in (9, 15, 33):
            four_squares = sum(v * pairs[n - k] for k, v in pairs.items())
            self.assertEqual(four_squares, 8 * (n + aliquot_sum(n)))
            a[n] = four_squares // 8
        self.assertEqual(a[a[15] - 15], 13)
        self.assertEqual(2 * a[2 * a[15] - 15], 96)

    def test_paired_gauss_gain_sees_exact_orbit(self):
        q = PROBE
        self.assertEqual(factorize(q), [(q, 1)])
        self.assertGreater(q, Q)
        self.assertEqual((q + 1) % lcm(8, Q), 0)
        self.assertEqual(tuple(map(aliquot_sum, SOURCES)), (16, 15))
        squares = {a * a % q for a in range(1, q)}
        xi = [0] + [1 if a in squares else -1 for a in range(1, q)]
        for char, gain in ((xi, q), ([0] + [1] * (q - 1), 1)):
            # Coefficients of |sum char(a) z^a|^2 at z a primitive q-th root.
            corr = [sum(char[a] * char[(a - k) % q] for a in range(q)) for k in range(q)]
            eigenvalue, *rest = coefficients_at_prime_root(corr)
            self.assertEqual(eigenvalue, gain)
            self.assertFalse(any(rest))
            lifted = prod(Fraction(eigenvalue * sum(d * char[d] for d in proper(n)), n)
                          for n in SOURCES)
            self.assertEqual(lifted, gain**2 * Fraction(15, 12))

    def test_trace_requires_full_denominator(self):
        q, b = PROBE, (PROBE - 1) // 2
        self.assertEqual(factorize(b), [(b, 1)])
        # 2 generates the squares here; extend each of their b characters oddly.
        logs = {pow(2, k, q): k for k in range(b)}
        self.assertEqual(len(logs), b)
        self.assertNotIn(q - 1, logs)
        words = [prod(ds) for ds in product(*(proper(n) for n in SOURCES))]
        self.assertEqual(words.count(1), 1)
        self.assertLess(max(words), q)
        self.assertEqual(sum(words), 240)
        trace = [0] * b
        for k in range(b):
            for w in words:
                trace[(k * logs[w]) % b] += w
        constant, *rest = coefficients_at_prime_root(trace)
        self.assertFalse(any(rest))
        self.assertEqual(constant, b)
        self.assertEqual(Fraction(q**2 * constant, Q).denominator, Q)

    def test_archive_polynomial_before_and_after_translation(self):
        # F_xi: every divisor in this block has xi(d)=1.
        grade = Counter()
        for ds in product(*(proper(n) for n in SOURCES)):
            w = prod(ds)
            grade[sum(e for _, e in factorize(w))] += w
        self.assertEqual([grade[i] for i in range(6)], [1, 7, 24, 48, 80, 80])
        # PP with lambda=3, e=1, c=4. Build coefficients of the operator
        # polynomial, then apply it by dilation, not by zeroing known grades.
        pp = [1, 1, 1]
        for i in range(1, 6):
            out = [0] * (len(pp) + 3)
            for k, a in enumerate(pp):
                out[k + 3] += a
                out[k] -= 4**(3 * i) * a
            pp = out
        scalar = sum(pp)
        self.assertEqual(scalar % 3**12, 0)
        self.assertNotEqual(scalar % 3**13, 0)
        for shift, retained in ((0, 1), (1, 240)):
            for z in range(-2, 4):  # six points determine a polynomial of degree <=5
                value = sum(a * sum(v * (shift + 4**k * z)**i for i, v in grade.items())
                            for k, a in enumerate(pp))
                self.assertEqual(value, scalar * retained)
