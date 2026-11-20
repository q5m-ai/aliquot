"""Exact finite regressions for a blocked coalescence proof strategy.

These do not prove the universal CRT/Dirichlet argument or classify an
unresolved orbit. No probable-prime tests, floating-point arithmetic, or
iteration at zero are used.
"""

from math import gcd, isqrt
import unittest

from aliquot import aliquot_sum, factorize


def divisor_pair_sum(n):
    """Independent proper-divisor enumeration for these small examples."""
    if n == 1:
        return 0
    total = 1
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            total += d
            if d != n // d:
                total += n // d
    return total


class CoalescenceTests(unittest.TestCase):
    def checked_sum(self, n):
        self.assertGreater(n, 0)
        result = aliquot_sum(n)
        self.assertEqual(result, divisor_pair_sum(n))
        return result

    def test_merger_before_numerical_descent(self):
        for path in ([56, 64, 63, 41, 1, 0], [48, 76, 64]):
            for source, target in zip(path, path[1:]):
                self.assertEqual(self.checked_sum(source), target)
        self.assertLess(48, 56)
        self.assertGreater(64, 56)

    def test_prime_guarded_smaller_shared_successor(self):
        for p, q in ((29, 7), (43, 11), (71, 19), (113, 31)):
            self.assertEqual(factorize(p), [(p, 1)])
            self.assertEqual(factorize(q), [(q, 1)])
            self.assertEqual(gcd(q, 18), 1)
            self.assertEqual(7 * q, 2 * p - 9)
            self.assertLess(18 * q, 6 * p)
            self.assertEqual(self.checked_sum(6 * p), 6 * p + 12)
            self.assertEqual(self.checked_sum(18 * q), 6 * p + 12)

    def test_composite_cofactor_correction(self):
        # All coprime cofactors 2..250, not a claim of orbit invariance.
        for q in range(2, 251):
            if gcd(q, 18) != 1:
                continue
            correction = 39 * (self.checked_sum(q) - 1)
            self.assertEqual(self.checked_sum(18 * q), 21 * q + 39 + correction)
            self.assertEqual(correction == 0, factorize(q) == [(q, 1)])
        self.assertEqual(factorize(35), [(5, 1), (7, 1)])
        self.assertEqual(self.checked_sum(762), 774)
        self.assertEqual(self.checked_sum(630), 1242)
        self.assertEqual(1242 - 774, 39 * (self.checked_sum(35) - 1))

    def test_failed_template_on_a_prime_progression(self):
        # Only primes 22 < p <= 5,000 with p=22 mod 35 are enumerated.
        checked = 0
        for p in range(57, 5001, 35):
            if factorize(p) != [(p, 1)]:
                continue
            t = (p - 22) // 35
            q = 5 + 10 * t
            self.assertEqual(7 * q, 2 * p - 9)
            self.assertGreater(q, 5)
            self.assertEqual(q % 5, 0)
            self.assertEqual(gcd(q, 18), 1)
            self.assertNotEqual(self.checked_sum(18 * q), self.checked_sum(6 * p))
            checked += 1
        self.assertGreater(checked, 0)

    def test_abundant_records_have_no_smaller_shared_successor(self):
        # Complete finite source range 1..1,200, checking t=1..100.
        # Unboundedness of these records is proved in the note, not inferred
        # from this test. Nothing here classifies their eventual orbits.
        sums = [0] + [self.checked_sum(n) for n in range(1, 1201)]
        for t in range(1, 101):
            bound = 12 * t
            record = max(range(1, bound + 1), key=sums.__getitem__)
            self.assertGreaterEqual(sums[bound], 16 * t)
            self.assertGreaterEqual(sums[record], sums[bound])
            self.assertLessEqual(record, bound)
            self.assertGreater(sums[record], record)
            self.assertTrue(all(sums[m] < sums[record] for m in range(1, record)))

    def test_finite_examples_of_crt_palette_obstruction(self):
        # C=6; d=18 uses ell=5, d=20 uses ell=13. The two forbidden
        # cofactor-prime residues give p=57 mod 65. d=11 has beta=0.
        # All tested primes satisfy 57 < p <=10,000. This finite check
        # does not establish the existence of infinitely many such primes.
        c, a = 6, self.checked_sum(6)
        traps = {18: 5, 20: 13}
        integral_cases = {d: 0 for d in traps}
        checked = 0
        for d, ell in traps.items():
            b = self.checked_sum(d)
            beta = c + a - (d + b)
            self.assertEqual(gcd(a * b * beta, ell), 1)
            self.assertEqual((a * 57 + beta) % ell, 0)
            self.assertNotEqual(57 % ell, 0)
        self.assertEqual(gcd(57, 65), 1)
        for p in range(122, 10_001, 65):
            if factorize(p) != [(p, 1)]:
                continue
            target = self.checked_sum(c * p)
            self.assertEqual(target, a * p + c + a)
            for d in (c, 11, 18, 20):
                b = self.checked_sum(d)
                beta = c + a - (d + b)
                numerator = a * p + beta
                if numerator % b:
                    continue  # No integer cofactor candidate at this core.
                q = numerator // b
                if d == c:
                    self.assertEqual(q, p)  # The original node, no reduction.
                    continue
                if d == 11:
                    self.assertEqual(beta, 0)
                    self.assertEqual(q, 6 * p)
                else:
                    ell = traps[d]
                    self.assertGreater(q, ell)
                    self.assertEqual(q % ell, 0)
                    integral_cases[d] += 1
                self.assertNotEqual(factorize(q), [(q, 1)])
                if gcd(d, q) == 1:
                    self.assertNotEqual(self.checked_sum(d * q), target)
            checked += 1
        self.assertGreater(checked, 0)
        self.assertTrue(all(count > 0 for count in integral_cases.values()))


if __name__ == "__main__":
    unittest.main()
