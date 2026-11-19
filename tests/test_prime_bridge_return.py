"""Exact fixed-seed arithmetic for note 19, not a conjecture test."""

from functools import cache
from math import gcd, isqrt, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.certified import CertifiedFactorizer, verify_certificates


def block(p):
    """B on a supplying prime; never round a nonintegral cofactor."""
    if p % 800 != 799:
        raise ValueError("not a supplying residue")
    return 1 + 109 * ((p + 1) // 80)


@cache
def trial_prime(p):
    if not 2 <= p < 10**15:
        raise ValueError("prime outside fixed-seed trial bounds")
    if p in (2, 3):
        return True
    if p % 2 == 0 or p % 3 == 0:
        return False
    return all(p % d and p % (d + 2) for d in range(5, isqrt(p) + 1, 6))


class PrimeBridgeReturnTests(unittest.TestCase):
    def test_minimal_split_on_the_realized_blocks(self):
        q, r, p, returned = 7847996863999, 2399, 4457230399, 14579600640799
        for prime in (q, r, p, returned):
            self.assertTrue(trial_prime(prime))
            self.assertEqual(prime % 800, 799)
        self.assertEqual(block(q), r * p)
        self.assertEqual(returned + 1, r + 1 + block(r) * (p + 1))
        h, x, y = 3271, 8009, 758269
        self.assertEqual((block(r), block(p)), (h, x * y))
        self.assertEqual(block(returned), h * x * y)
        self.assertEqual([z % 10 for z in (h, x, y)], [1, 9, 9])
        self.assertEqual(factorize(block(returned)), [(h, 1), (x, 1), (y, 1)])
        self.assertEqual([gcd(z + 1, 800) for z in (h, x, y)], [8, 10, 10])
        self.assertEqual((h + 1) * (x + 1) * (y + 1) % 800, 0)

    def test_composite_residual_loses_the_whole_proposed_block(self):
        r, v = 2399, 47 * 75377
        q, following = 12015893599, 16371655031
        self.assertTrue(trial_prime(q))
        self.assertEqual(aliquot_sum(160 * r * v), 160 * q)
        self.assertEqual(aliquot_sum(160 * q), 160 * following)
        sv = aliquot_sum(v)
        self.assertEqual(sv, 75425)
        self.assertEqual(80 * following, block(r) * (189 * (v + sv) - 80 * v)
                         + 189 * (1 - sv))
        self.assertEqual(gcd(block(r), 1 - sv), 1)
        self.assertEqual(gcd(block(r), following), 1)

    def test_complete_orbit_no_later_guard_or_prime_bridge_return(self):
        engine = CertifiedFactorizer(max_work=100_000, max_bits=64)
        n = 1_255_679_498_239_840
        path, multiples, guarded, residues = [], [], [], []
        for j in range(115):
            self.assertTrue(0 < n <= 8 * 10**15)
            path.append(n)
            factors = engine.factor(n)
            sigma = prod((p**(e + 1) - 1) // (p - 1) for p, e in factors)

            # Independent of Lucas and the geometric-series formula: proved
            # distinct bases, exact product, and enumeration of every divisor.
            self.assertEqual(len({p for p, _ in factors}), len(factors))
            self.assertEqual(prod(p**e for p, e in factors), n)
            self.assertLessEqual(prod(e + 1 for _, e in factors), 128)
            divisors = [1]
            for p, e in factors:
                self.assertGreaterEqual(e, 1)
                self.assertTrue(trial_prime(p))
                divisors = [d * p**k for d in divisors for k in range(e + 1)]
            self.assertEqual(sum(divisors), sigma, (j, n))

            if n % 160 == 0:
                multiples.append(j)
                u = n // 160
                if gcd(u, 10) == 1:
                    # Divisors of the clean cofactor are exactly the divisors
                    # of the full source that use neither 2 nor 5.
                    sigma_u = sum(d for d in divisors if gcd(d, 10) == 1)
                    self.assertEqual(sigma, 378 * sigma_u)
                    if j < 5:
                        residues.append(sigma_u % 800)
                    if sigma_u % 800 == 0:
                        guarded.append(j)
            n = sigma - n
        self.assertEqual(n, 0)
        verify_certificates(engine.export_certificates())
        self.assertEqual([x // 160 for x in path[:5]], [
            7847996863999, 2399 * 4457230399, 14579600640799,
            3271 * 8009 * 758269, 13 * 2083533274783,
        ])
        self.assertEqual(residues, [0, 0, 0, 0, 576])
        self.assertEqual(guarded, [0, 1, 2, 3])
        self.assertEqual(multiples, [0, 1, 2, 3, 4, 23, 101, 104])
        self.assertEqual((path.index(max(path)), max(path)), (6, 7520281881799528))
        self.assertEqual((path[101], path[104]), (320, 160))
        self.assertEqual(path[-4:], [40, 50, 43, 1])
