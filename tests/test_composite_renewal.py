"""Bounded arithmetic for composite renewal, not an infinite-orbit certificate.

The prime-triple scan caps t at 4096 and stops at 375. Certified factorization
uses 200000 work units/call and 128 bits; failures stay unresolved. Independent
pair enumeration covers three sources <2*10^13. Larger smooth examples use
proved factors and complete divisor enumeration. The residue-refined overflow
example is checked only modulo inventory prime powers, without expanding q^E.
"""

from math import gcd, prod
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize
from aliquot.certified import CertifiedFactorizer, SMALL_PRIMES, verify_certificates
from aliquot.two_adic import _divisor_pair_sum


def sigma(n):
    return n + aliquot_sum(n)


def valuation(n, p):
    if n <= 0:
        raise ValueError("valuation requires a positive integer")
    exponent = 0
    while n % p == 0:
        n //= p
        exponent += 1
    return exponent


def cofactor_image(u):
    if gcd(u, 10) != 1:
        raise ValueError("the core must be unitary")
    numerator = 189 * sigma(u) - 80 * u
    if numerator % 80:
        raise ValueError("the cofactor image is not integral")
    return numerator // 80


def unitary(d, n):
    return n % d == 0 and gcd(d, n // d) == 1


def enumerated_aliquot(factors):
    """Sum every divisor, not the product of geometric-series sums.

    Complete trial proofs of the distinct prime bases certify completeness.
    Only the small divisor sets explicitly used below are enumerated.
    """
    assert len({p for p, _ in factors}) == len(factors)
    divisors = [1]
    for p, e in factors:
        assert factorize(p) == [(p, 1)] and e > 0
        divisors = [d * p ** j for d in divisors for j in range(e + 1)]
    n = prod(p ** e for p, e in factors)
    assert len(divisors) <= 256 and max(divisors) == n
    return sum(divisors) - n


def power_sigma_mod(q, exponent, modulus):
    """Geometric sum by doubling, independent of the q=1 specialization."""
    def pair(count):
        if count == 0:
            return 1, 0
        power, total = pair(count // 2)
        square = power * power % modulus
        doubled = total * (1 + power) % modulus
        if count % 2:
            return square * q % modulus, (doubled + square) % modulus
        return square, doubled
    return pair(exponent + 1)[1]


class CompositeRenewalTests(unittest.TestCase):
    def test_composite_map_uses_actual_divisor_sum(self):
        for r in (2399, 4799):
            self.assertEqual(factorize(r), [(r, 1)])
            k = (r + 1) // 800
            for w in (1, 3, 7, 11, 121, 143, 1653):
                self.assertEqual(gcd(w, 10 * r), 1)
                u = r * w
                v = cofactor_image(u)
                self.assertEqual(v, (1090 * k + 1) * w
                                 + 1890 * k * aliquot_sum(w))
                self.assertEqual(aliquot_sum(160 * u), 160 * v)
                self.assertEqual(gcd(v, 10), 1)
                self.assertGreater(80 * v, 109 * u)

    def test_fixed_composite_factor_and_fresh_supplier(self):
        A, p, r = 1653, 278344271, 2399
        self.assertEqual(factorize(A), [(3, 1), (19, 1), (29, 1)])
        self.assertEqual(sigma(A), 2400)
        self.assertEqual(factorize(p), [(p, 1)])
        B = 189 * sigma(A) // 80
        v = (B - A) * p + B
        self.assertEqual(v, 1118108942277)
        self.assertEqual(p % 10, 1)
        self.assertEqual(v % (r * r), r)
        self.assertEqual(gcd(A * p, r), 1)
        self.assertTrue(unitary(r, v))
        self.assertEqual(sigma(v) % 800, 0)
        self.assertEqual(cofactor_image(A * p), v)
        factors = [(2, 5), (3, 1), (5, 1), (19, 1), (29, 1), (p, 1)]
        self.assertEqual(enumerated_aliquot(factors), 160 * v)

    def test_full_prime_entry_return_and_next_guard_loss(self):
        t, r = 375, 2399
        p = 87200 * t + 2399
        q = 153536000 * t + 4223999
        Q = 285231200 * t + 7852799
        self.assertEqual((p, q, Q), (32702399, 57580223999, 106969552799))
        for prime in (r, p, q, Q):
            self.assertEqual(factorize(prime), [(prime, 1)])
            self.assertEqual(prime % 800, 799)
        cofactors = [q, r * p, Q, 145746015691]
        self.assertEqual(factorize(cofactors[-1]), [(29, 2), (3271, 1), (52981, 1)])
        for u, v in zip(cofactors, cofactors[1:]):
            self.assertEqual(gcd(u, 10), 1)
            self.assertEqual(sigma(u) % 800, 0)
            self.assertEqual(cofactor_image(u), v)
            n, following = 160 * u, 160 * v
            self.assertLess(n, 20_000_000_000_000)
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(_divisor_pair_sum(n), following)
            self.assertGreater(following, n)
        self.assertEqual(sigma(cofactors[-1]) % 800, 784)
        self.assertEqual(gcd(cofactors[-1], 10), 1)

    def test_bounded_prime_triple_search_and_independent_replay(self):
        engine = CertifiedFactorizer(max_work=200_000, max_bits=128)
        unresolved, survivors, hit = [], 0, None
        for t in range(1, 4097):
            values = (87200 * t + 2399, 153536000 * t + 4223999,
                      285231200 * t + 7852799)
            if any(x % ell == 0 for x in values for ell in SMALL_PRIMES):
                continue
            survivors += 1
            try:
                # CertifiedFactorizer returns tuples, not the trial API's lists.
                if any(engine.factor(x) != ((x, 1),) for x in values):
                    continue
            except ComputationLimit:
                unresolved.append(t)
                continue
            hit = t
            break
        verify_certificates(engine.export_certificates())
        self.assertEqual(unresolved, [])
        self.assertEqual((hit, survivors), (375, 27))

    def test_prime_bridge_endpoint_residue(self):
        for r in (2399, 4799):
            k = (r + 1) // 800
            c, e = 1090 * k + 1, 1890 * k
            self.assertEqual(gcd(c, 800), 1)
            for p in (3, 7, 11, 13, 2399, 4799):
                if p == r:
                    continue
                Q = c * p + e
                self.assertEqual(Q, cofactor_image(r * p))
                self.assertEqual((Q + 1) % 800 == 0, (p + 1) % 800 == 0)

    def test_fixed_supplier_return_consumes_an_integer_budget(self):
        for r in (2399, 4799):
            k = (r + 1) // 800
            c, e = 1090 * k + 1, 1890 * k
            a, d, b = 109 * c, 80 * r, 189 * c + 80 * r * e
            self.assertEqual(gcd(a, d), 1)
            self.assertGreater(a, d)
        r, q, Q = 2399, 57580223999, 106969552799
        a, d, b = 356539, 191920, 1088804619
        self.assertEqual(d * Q, a * q + b)
        H = (a - d) * q + b
        self.assertEqual(str(H), "9478799983296000")
        self.assertEqual(d * ((a - d) * Q + b), a * H)
        self.assertEqual([valuation(H, ell) for ell in (2, 5, r)], [9, 3, 1])
        self.assertEqual(H % d, 0)
        self.assertNotEqual(H % (d * d), 0)
        self.assertNotEqual(cofactor_image(Q) % r, 0)

    def test_composite_exchange_and_alternative_growing_phase(self):
        A, D = 9261, 30240
        self.assertEqual(sigma(A), 16000)
        self.assertEqual(sigma(D), 4 * D)
        for w in (1, 11, 13, 17, 121, 143):
            self.assertEqual(gcd(w, 10 * A), 1)
            t = 200 * sigma(w) - 49 * w
            self.assertEqual(cofactor_image(A * w), 189 * t)
            self.assertEqual(aliquot_sum(160 * A * w), D * t)
        self.assertEqual((200 * sigma(13) - 49 * 13) % 7, 0)
        path = [160 * A, D * 151, D * 457, D * 1375]
        for n, following in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(n), following)
            self.assertGreater(following, n)
        self.assertTrue(unitary(D, D * 151))
        self.assertTrue(unitary(D, D * 457))
        self.assertFalse(unitary(D, D * 1375))

    def test_actual_composite_remainder_exits_a_finite_core_union(self):
        D, q, E, H = 6, 1297, 22, 3
        self.assertEqual(factorize(q), [(q, 1)])
        self.assertEqual(q % (6 ** (H + 1)), 1)
        # Weak p=3: sigma(6)=3*4 and 6=3*2.
        self.assertEqual((4 * (E + 1) - 2) % (3 ** 3), 3 ** 2)
        n = D * q ** E
        self.assertEqual(n.bit_length(), 231)
        following = aliquot_sum(n)
        self.assertEqual(following, enumerated_aliquot([(2, 1), (3, 1), (q, E)]))
        self.assertEqual((valuation(following, 2), valuation(following, 3)), (1, H))
        self.assertTrue(unitary(6, n))
        self.assertTrue(all(not unitary(core, following) for core in (6, 18)))
        self.assertGreater(following, n)

    def test_reduced_residue_overflow_modular_certificate(self):
        D, z, E, H = 1481760, 341, 43070, 6
        q = int("342206822790000001")
        engine = CertifiedFactorizer(max_work=200_000, max_bits=128)
        self.assertEqual(engine.factor(q), ((q, 1),))
        verify_certificates(engine.export_certificates())
        self.assertEqual(q, 1 + 19 * 210 ** 7)
        self.assertEqual(factorize(z), [(11, 1), (31, 1)])
        self.assertEqual((z % 9, q % 9), (8, 1))
        self.assertEqual(gcd(z, D), 1)
        self.assertEqual(sigma(z), 384)
        self.assertEqual(valuation(sigma(z), 3), 1)
        self.assertEqual(gcd(sigma(z), 5 * 7), 1)
        SD, SZ = sigma(D), sigma(z)
        self.assertEqual(SD, 6048000)
        # These are the actual n=D*z*q^E residues, not an expanded orbit.
        expected = {2: 5, 3: 3, 5: 1, 7: H}
        for ell, exponent in expected.items():
            modulus = ell ** (H + 1)
            self.assertEqual(q % modulus, 1)
            self.assertEqual(power_sigma_mod(q, E, modulus), (E + 1) % modulus)
            following = (SD * SZ * power_sigma_mod(q, E, modulus)
                         - D * z * pow(q, E, modulus)) % modulus
            self.assertNotEqual(following, 0)
            self.assertEqual(valuation(following, ell), exponent)
        # The core has 7^3, whereas the successor has exactly 7^6.
        self.assertEqual(valuation(D, 7), 3)

    def test_non_strict_retention_for_prime_active_blocks(self):
        t, p = 2399, 15833399
        self.assertEqual(factorize(p), [(p, 1)])
        w = t * p
        self.assertEqual((valuation(w, t), valuation(sigma(w), t)), (1, 1))
        self.assertEqual((189 * sigma(w) // t - 80 * p) % t, 0)
        for r in (3, 7, 11, 13, 17, 19, 23):
            self.assertEqual(gcd(r, 10 * w), 1)
            v = cofactor_image(w * r)
            self.assertEqual(valuation(v, t), 1)
            self.assertEqual(aliquot_sum(160 * w * r), 160 * v)
            self.assertEqual(gcd(v, 10), 1)
        self.assertEqual(cofactor_image(3 * w), 245148539397)

    def test_supplied_composite_active_block_breaks_exact_retention(self):
        t, p, a, b = 2399, 15833399, 4799, 21589
        for prime in (t, p, a, b):
            self.assertEqual(factorize(prime), [(prime, 1)])
        w, R = t * p, a * b
        self.assertEqual((a % 800, a % t, b % t), (799, 1, t - 2))
        self.assertEqual(sigma(R) % 800, 0)
        self.assertEqual(aliquot_sum(R) % t, 0)
        source = w * R
        target = cofactor_image(source)
        self.assertEqual(str(source), "3935389117266691811")
        self.assertEqual(str(target), "5368212855629308189")
        self.assertEqual(valuation(target, t), 2)
        self.assertEqual(sigma(t * t) % 5, 1)
        factors = [(2, 5), (5, 1), (t, 1), (p, 1), (a, 1), (b, 1)]
        self.assertEqual(enumerated_aliquot(factors), 160 * target)
        # No claim that the whole target lacks alternative 800-supply.

    def test_finite_menu_constant_and_variable_exponents(self):
        w = 3
        for r in (2399, 4799):
            self.assertTrue(unitary(3, cofactor_image(w * r)))
        q = 15293599
        self.assertEqual(factorize(q), [(q, 1)])
        self.assertEqual(q % 800, 799)
        v = cofactor_image(q)
        self.assertEqual(factorize(v), [(11, 2), (13, 2), (1019, 1)])
        self.assertFalse(unitary(11, v))
        self.assertFalse(unitary(13, v))
        for ell in (11, 13):
            self.assertEqual((109 * q + 189) % (ell * ell), 0)

    def test_constant_zero_exponent_excludes_the_active_prime_itself(self):
        w, ell = 95959, 2399
        self.assertEqual(factorize(w), [(w, 1)])
        self.assertEqual(w % ell, ell - 1)
        self.assertEqual((valuation(w, ell), valuation(189 * sigma(w), ell)), (0, 1))
        # Constant zero holds for other active primes, but not r=ell.
        self.assertEqual(valuation(cofactor_image(w * 4799), ell), 0)
        self.assertEqual(valuation(cofactor_image(w * ell), ell), 1)


if __name__ == "__main__":
    unittest.main()
