"""Finite regressions for the attempted closure, not an escaping-orbit test.

Ordinary orbit sources <= 30,000,000; the separate fresh-handoff fixture has a
5,000,000,000,000 source cap. Odd-cofactor audit <= 10,001; paths <= 64 steps.
Separate supplier primality certificates are <= 200,000,000,000.
Large CRT residues are only modular certificates, never presumed prime.
"""

from functools import lru_cache
from math import gcd, isqrt
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize

SOURCE_CAP = 30_000_000
FRESH_SOURCE_CAP = 5_000_000_000_000
ODD_BOUND = 10_001
BRIDGE_PRIME_BOUND = 1000
SUPPLIER_CAP = 200_000_000_000
STEP_CAP = 64


def valuation(n, p):
    if n < 1 or p < 2:
        raise ValueError("Valuations require a positive integer and p >= 2")
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


@lru_cache(None)
def checked_sum(n, *, source_cap=SOURCE_CAP):
    if type(n) is not int or n < 1:
        raise ValueError("Aliquot sources must be positive integers")
    if type(source_cap) is not int or not 1 <= source_cap <= FRESH_SOURCE_CAP:
        raise ValueError("Source cap outside the declared verification budgets")
    if n > source_cap:
        raise ComputationLimit("Orbit-source budget exceeded; unresolved")
    actual = aliquot_sum(n)
    independent = sum(
        d + (n // d if d*d != n else 0)
        for d in range(1, isqrt(n) + 1) if n % d == 0
    ) - n
    if actual != independent:
        raise ArithmeticError("Independent divisor-pair sum disagrees")
    return actual


@lru_cache(None)
def checked_prime(n):
    if type(n) is not int or n < 2:
        raise ValueError("Prime candidates must be integers >= 2")
    if n > SUPPLIER_CAP:
        raise ComputationLimit("Supplier-primality budget exceeded; unresolved")
    actual = factorize(n) == [(n, 1)]
    independent = all(n % d for d in range(2, isqrt(n) + 1))
    if actual != independent:
        raise ArithmeticError("Independent exhaustive primality check disagrees")
    return actual


def verify_path(path, *, source_cap=SOURCE_CAP):
    if not 1 <= len(path)-1 <= STEP_CAP:
        raise ComputationLimit("Path length outside the finite verification budget")
    for source, target in zip(path, path[1:]):
        if checked_sum(source, source_cap=source_cap) != target:
            raise ArithmeticError("Named orbit edge is incorrect")


def entry(n, bridge):
    """X0 for bridge=160, Y for bridge=12; zero is never evaluated."""
    if n <= 4 or n % 8 != 4:
        return False
    target = checked_sum(n)
    return target < n and target % bridge == 0


def crt_pair(a, m, b, n):
    if m < 1 or n < 2 or gcd(m, n) != 1:
        raise ValueError("Expected coprime positive CRT moduli")
    modulus = m*n
    return (a + m*((b-a)*pow(m, -1, n) % n)) % modulus, modulus


def supply_two_shape(factors):
    """Classify v2(sigma(odd u))=2 from its exact odd exponents."""
    odd = [(p, e) for p, e in factors if e % 2]
    if len(odd) == 1:
        p, e = odd[0]
        return ((p % 8 == 3 and e % 4 == 1)
                or (p % 4 == 1 and e % 8 == 3))
    if len(odd) == 2:
        return all(p % 4 == 1 and e % 4 == 1 for p, e in odd)
    return False


class ReturnClosureTests(unittest.TestCase):
    def test_entry_signature_and_complete_supply_two_classification(self):
        members = 0
        for u in range(1, ODD_BOUND + 1, 2):
            sigma = u + checked_sum(u)
            factors = factorize(u)
            self.assertEqual(supply_two_shape(factors), valuation(sigma, 2) == 2)
            if not entry(4*u, 160):
                continue
            members += 1
            self.assertEqual(gcd(u, 105), 1)
            self.assertEqual(valuation(sigma, 2), 2)
            self.assertLessEqual(sum(e % 2 for _, e in factors), 2)
            self.assertEqual(sigma % 160, (92*u) % 160)
            self.assertLess(7*sigma, 8*u)
        self.assertGreater(members, 0)

    def test_clean_bridge_guard_and_old_supply_failure(self):
        for v in range(1, 1001, 2):
            if gcd(v, 160) != 1:
                continue
            sigma = v + checked_sum(v)
            target = checked_sum(160*v)
            self.assertEqual(target, 378*sigma - 160*v)
            self.assertEqual(valuation(target, 2) == 2, valuation(sigma, 2) == 1)
            odd = [(p, e) for p, e in factorize(v) if e % 2]
            shape = (len(odd) == 1 and odd[0][0] % 4 == 1
                     and odd[0][1] % 4 == 1)
            self.assertEqual(shape, valuation(sigma, 2) == 1)
        verify_path([2764, 2080, 3212, 3004])
        self.assertEqual(13 + checked_sum(13), 14)
        self.assertEqual(803 + checked_sum(803), 888)
        self.assertEqual(valuation(888, 2), 3)
        self.assertTrue(entry(2764, 160))
        self.assertFalse(entry(3212, 160))

    def test_full_composite_entry_really_renews_once(self):
        path = [7700684, 5775520, 7869524, 6961600, 11148600]
        verify_path(path)
        self.assertTrue(checked_prime(1925171))
        self.assertEqual(factorize(1967381), [(13, 1), (151337, 1)])
        self.assertTrue(entry(path[0], 160))
        self.assertTrue(entry(path[2], 160))
        self.assertFalse(entry(path[4], 160))
        self.assertEqual(valuation(path[4], 2), 3)
        for start, middle, end in (path[:3], path[2:]):
            self.assertLess(middle, start)
            self.assertEqual(middle % 160, 0)
            self.assertGreater(320*end, 327*start)
        # Guard loss is not a classification of the orbit's eventual fate.

    def test_actual_prime_entry_with_abundant_retained_bridge(self):
        path = [11261644, 8446240, 13326560]
        verify_path(path)
        p = path[0] // 4
        self.assertEqual(p, 2815411)
        self.assertTrue(checked_prime(p))
        self.assertEqual(p % 160, 51)
        self.assertTrue(entry(path[0], 160))
        self.assertEqual(factorize(path[1]), [(2, 5), (5, 1), (11, 1), (4799, 1)])
        self.assertEqual((4799 + 1) % (2**6 * 5**2), 0)
        for value in path[1:]:
            self.assertEqual(valuation(value, 2), 5)
            self.assertEqual(valuation(value, 5), 1)
            self.assertFalse(entry(value, 160))
            self.assertGreaterEqual(80*checked_sum(value), 109*value)
        self.assertGreater(320*path[2], 327*path[0])

    def test_two_level_relay_and_reduced_crt_certificate(self):
        suppliers = [4799, 110545924799]
        D = 2**6 * 5**2
        self.assertEqual(suppliers[1] + 1, 3*D*suppliers[0]**2)
        residue, modulus = 1011, 1600  # Fix v2(3p+7)=5, v5(3p+7)=1.
        lower = []
        for r in suppliers:
            self.assertTrue(checked_prime(r))
            self.assertEqual(gcd(r, 21*modulus), 1)
            self.assertEqual((r+1) % D, 0)
            for previous in lower:
                self.assertEqual((r+1) % previous**2, 0)
                self.assertGreater(r, previous)
            local = (r-7)*pow(3, -1, r*r) % (r*r)
            residue, modulus = crt_pair(residue, modulus, local, r*r)
            lower.append(r)
        self.assertEqual(gcd(residue, modulus), 1)
        self.assertEqual(residue % 1600, 1011)
        m = 3*residue + 7
        self.assertEqual(valuation(m, 2), 5)
        self.assertEqual(valuation(m, 5), 1)
        for r in suppliers:
            self.assertEqual(m % (r*r), r)
        # This large least residue is NOT declared prime or used as an orbit.
        # Prime existence in the progression is a Dirichlet input to the proof.
        self.assertGreater(m, SOURCE_CAP)
        with self.assertRaises(ComputationLimit):
            checked_sum(m)
        # The induction's two remaining supplier levels each cover all lower
        # locked exponents. These are certificate premises, not computed edges.
        for count in (2, 1):
            top = suppliers[count-1]
            required = [(2, 5), (5, 1), *((r, 1) for r in suppliers[:count-1])]
            for p, exponent in required:
                self.assertEqual((top+1) % p**(exponent+1), 0)

    def test_one_relay_step_does_not_supply_its_replacement(self):
        path = [767840, 1046560, 1517792]
        verify_path(path)
        self.assertEqual(path[0], 160*4799)
        self.assertEqual(path[1], 160*31*211)
        self.assertEqual(path[2], 32*47431)
        self.assertNotEqual(path[1] % 4799, 0)
        self.assertEqual(31*211 + checked_sum(31*211), 6784)
        self.assertNotEqual(6784 % 5, 0)
        self.assertNotEqual(path[2] % 5, 0)
        self.assertTrue(all(a < b for a, b in zip(path, path[1:])))
        for source in path[:-1]:
            target = checked_sum(source)
            for p, _ in factorize(source + target):
                if source % p:
                    self.assertNotEqual(target % p, 0)

    def test_genuinely_fresh_supplier_renews_the_guard_once(self):
        path = [2200539647840, 2998235270560, 4098260524640]
        verify_path(path, source_cap=FRESH_SOURCE_CAP)
        q, r = 13753372799, 2399
        self.assertTrue(checked_prime(q))
        self.assertTrue(checked_prime(r))
        self.assertEqual(path[0], 160*q)
        self.assertEqual(q % 800, 799)
        self.assertEqual((r+1) % 800, 0)
        self.assertEqual(gcd(r, 160*218*378), 1)
        self.assertEqual(path[1], 218*q + 378)
        self.assertNotEqual(path[0] % r, 0)
        self.assertEqual(path[1] % (r*r), r)
        residue, modulus = crt_pair(799, 800, (r-378)*pow(218, -1, r*r) % (r*r), r*r)
        self.assertEqual((residue, modulus), (4545051199, 4604160800))
        self.assertEqual(gcd(residue, modulus), 1)
        self.assertEqual(q, residue + 2*modulus)
        cofactors = [value // 160 for value in path]
        self.assertEqual(cofactors, [13753372799, 18738970441, 25614128279])
        self.assertEqual(factorize(cofactors[1]), [(743, 1), (2399, 1), (10513, 1)])
        self.assertTrue(checked_prime(cofactors[2]))
        sigmas = [u + checked_sum(u, source_cap=FRESH_SOURCE_CAP) for u in cofactors]
        self.assertEqual(sigmas, [13753372800, 18773798400, 25614128280])
        self.assertEqual([sigma % 800 for sigma in sigmas], [0, 0, 280])
        self.assertEqual([u % 10 for u in cofactors], [9, 1, 9])
        for value in path:
            self.assertEqual(valuation(value, 2), 5)
            self.assertEqual(valuation(value, 5), 1)
        for source, target in zip(path, path[1:]):
            self.assertGreaterEqual(80*target, 109*source)
        # The last term retains the core and residue phase, not the full Z guard.
        # No eventual termination, escape, or absence of a later return is inferred.

    def test_twelve_bridge_has_actual_composite_entry_families(self):
        found = 0
        for p in range(31, BRIDGE_PRIME_BOUND + 1, 36):
            if not checked_prime(p):
                continue
            found += 1
            source = 52*p
            middle = checked_sum(source)
            target = checked_sum(middle)
            self.assertTrue(entry(source, 12))
            self.assertEqual(middle, 46*p + 98)
            self.assertEqual(middle % 12, 0)
            v = middle // 12
            self.assertEqual(v % 6, 1)
            self.assertEqual(v, (23*p + 49) // 6)
            self.assertGreater(target, source)
            self.assertGreaterEqual(3*target, 4*middle)
            if checked_prime(v):
                self.assertFalse(entry(target, 12))
        self.assertGreater(found, 0)

    def test_no_clean_prime_twelve_bridge_renews_the_class(self):
        for v in range(5, BRIDGE_PRIME_BOUND + 1, 2):
            if not checked_prime(v):
                continue
            # This check does not assert that every bridge has a Y predecessor.
            target = checked_sum(12*v)
            w = 4*v + 7
            self.assertEqual(target, 4*w)
            self.assertFalse(entry(target, 12))
            if v % 3 == 1:
                self.assertEqual(w % 3, 2)
                self.assertEqual((w + checked_sum(w)) % 3, 0)
            else:
                self.assertEqual(w % 3, 0)
                self.assertGreater(checked_sum(target), target)

    def test_twelve_bridge_variable_time_return_counterexample(self):
        path = [1612, 1524, 2060, 2308, 1738, 1142, 574, 434, 334,
                170, 154, 134, 70, 74, 40, 50, 43, 1, 0]
        verify_path(path)
        self.assertTrue(entry(path[0], 12))
        self.assertTrue(checked_prime(31))
        self.assertEqual(403 + checked_sum(403), 448)
        self.assertEqual(path[1], 12*127)
        self.assertTrue(checked_prime(127))
        self.assertGreater(path[2], path[0])
        self.assertGreater(checked_sum(path[2]), path[2])
        self.assertFalse(any(n > path[0] and entry(n, 12) for n in path[1:]))
        self.assertEqual(path[-1], 0)

    def test_domains_and_budgets_do_not_classify_unknown_orbits(self):
        for n in (0, -1, 1.5):
            with self.assertRaises(ValueError):
                checked_sum(n)
        with self.assertRaises(ComputationLimit):
            checked_sum(SOURCE_CAP + 1)
        with self.assertRaises(ComputationLimit):
            checked_sum(FRESH_SOURCE_CAP + 1, source_cap=FRESH_SOURCE_CAP)
        with self.assertRaises(ValueError):
            checked_sum(1, source_cap=FRESH_SOURCE_CAP + 1)
        with self.assertRaises(ComputationLimit):
            checked_prime(SUPPLIER_CAP + 1)
        with self.assertRaises(ComputationLimit):
            verify_path([6] * (STEP_CAP + 2))
        with self.assertRaises(ValueError):
            crt_pair(1, 6, 2, 9)
        with self.assertRaises(ValueError):
            verify_path([0, 0])
        self.assertFalse(entry(0, 160))
        self.assertFalse(entry(0, 12))
        verify_path([1, 0])


if __name__ == "__main__":
    unittest.main()
