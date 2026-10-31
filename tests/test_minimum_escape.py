"""Finite checks of minimum-seed companion attempts, not the conjecture.

Deletion/classification inputs and correction cofactors are <=2000.
The supplier/CRT example uses symbolic integers, not a huge orbit.
Root lifts use K=1..8,
with at most 10000 progression candidates per prime witness; the displayed
source values are below 1.8 billion. No orbit is continued indefinitely.
"""

from math import gcd, isqrt
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum


def valuation_three(n):
    if n <= 0:
        raise ValueError("valuation requires a positive integer")
    exponent = 0
    while n % 3 == 0:
        n //= 3
        exponent += 1
    return exponent


def trial_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


class MinimumEscapeTests(unittest.TestCase):
    def test_prime_deletion_identity_and_abundant_classification(self):
        for n in range(2, 2001):
            following = aliquot_sum(n)
            self.assertEqual(following, _divisor_pair_sum(n))
            for p, exponent in factorize(n):
                b, d = n // p, n // p ** exponent
                companion_next = aliquot_sum(b)
                correction = d + aliquot_sum(d)
                self.assertEqual(following, p * companion_next + correction)
                if correction % p:
                    self.assertNotEqual(following % p, 0)
                if following > n:
                    self.assertGreater(companion_next, 0)
                    self.assertEqual(following % companion_next == 0,
                                     exponent == 1 and companion_next == b)

    def test_unitary_companion_gcd(self):
        for d in range(2, 41):
            for p in range(2, 32):
                if not trial_prime(p) or d % p == 0:
                    continue
                self.assertEqual(gcd(aliquot_sum(d * p), aliquot_sum(d)),
                                 gcd(d, aliquot_sum(d)))

    def test_terminating_companion_errors_and_finite_growth(self):
        companion = [12, 16, 15, 9, 4, 3, 1, 0]
        for n, following in zip(companion, companion[1:]):
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(_divisor_pair_sum(n), following)
        for p, path, second_error in ((13, [156, 236, 184], -11),
                                      (17, [204, 300, 568], 313),
                                      (19, [228, 332, 256], -29)):
            for n, following in zip(path, path[1:]):
                self.assertEqual(aliquot_sum(n), following)
                self.assertEqual(_divisor_pair_sum(n), following)
            self.assertEqual(path[1] - p * companion[1], 28)
            self.assertEqual(path[2] - p * companion[2], second_error)
            self.assertEqual(second_error,
                             path[1] + aliquot_sum(path[1])
                             - p * (16 + aliquot_sum(16)) - 28)
            if p % 6 == 1:
                self.assertEqual(gcd(path[0], path[1]), 4)

        # One small illustration, not validation of the infinite family.
        p, path = 101, [1212, 1644, 2220, 4164, 5580]
        self.assertTrue(trial_prime(p))
        self.assertEqual(factorize(path[0]), [(2, 2), (3, 1), (101, 1)])
        self.assertEqual(aliquot_sum(path[0]), path[1])
        self.assertGreater(path[1], path[0])
        for n, following in zip(path[1:], path[2:]):
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(_divisor_pair_sum(n), following)
            self.assertGreater(10 * following, 13 * n)

    def test_symbolic_supplier_and_reduced_affine_entry(self):
        # D=12, A=16, B=28. The first two fresh supplier primes are 5,11.
        # e1=1 and e2=phi(5^2*(11-1))-1=99.
        self.assertEqual(pow(11, 100, 25 * 10), 1)
        self.assertEqual(((11 ** 100 - 1) // 10) % 25, 0)
        # A third link can be checked modularly without expanding 13^e3.
        phi = 40 * 11 ** 99  # phi(11^100 * (13-1))
        self.assertEqual(pow(13, phi, 11 ** 100 * 12), 1)

        modulus_one, modulus_two = 25, 11 ** 100
        a = ((5 - 28) * pow(16, -1, modulus_one)) % modulus_one
        b = ((11 ** 99 - 28) * pow(16, -1, modulus_two)) % modulus_two
        residue = a + modulus_one * (((b - a)
                  * pow(modulus_one, -1, modulus_two)) % modulus_two)
        modulus = modulus_one * modulus_two
        residue += modulus * (((1 - residue) * pow(modulus, -1, 6)) % 6)
        self.assertEqual(gcd(residue, 6 * modulus), 1)
        self.assertEqual(residue % 6, 1)
        affine = 16 * residue + 28
        self.assertEqual(affine % 25, 5)
        self.assertEqual(affine % (11 ** 100), 11 ** 99)
        # This verifies only the reduced CRT class and exact valuations.
        # Its displayed representative is not asserted prime, so no actual
        # aliquot step from 12*residue or infinite trajectory is inferred.

    def test_composite_correction_and_guard(self):
        for u in range(2, 2001):
            if gcd(u, 6) != 1:
                continue
            successor = aliquot_sum(6 * u)
            self.assertEqual(successor, _divisor_pair_sum(6 * u))
            self.assertEqual(successor % 6, 0)
            transformed = successor // 6
            correction = 2 * (aliquot_sum(u) - 1)
            self.assertEqual(transformed, u + 2 + correction)
            self.assertGreater(transformed, u)
            self.assertEqual(correction == 0, trial_prime(u))
            self.assertEqual(transformed % 2, 1)
            self.assertEqual(gcd(transformed, 6) == 1, transformed % 3 != 0)
        self.assertEqual(aliquot_sum(6), 6)  # The excluded u=1 is fixed.

    def test_prime_only_guard_exits(self):
        for p in range(5, 1001):
            if not trial_prime(p):
                continue
            self.assertEqual(aliquot_sum(6 * p), 6 * (p + 2))
            if p % 3 == 1:
                self.assertEqual((p + 2) % 3, 0)
            elif trial_prime(p + 2):
                self.assertEqual(aliquot_sum(6 * (p + 2)), 6 * (p + 4))
                self.assertEqual((p + 4) % 3, 0)
            # Composite p+2 is not declared an exit or a resolved orbit.

    def test_prime_checkpoint_budget_can_increase(self):
        examples = (
            ([1002, 1014, 1182], [(13, 2)], (1, 2)),
            ([4098, 4110, 5826], [(5, 1), (137, 1)], (2, 5)),
        )
        for path, middle_factors, budgets in examples:
            start, middle, end = (n // 6 for n in path)
            self.assertTrue(trial_prime(start))
            self.assertTrue(trial_prime(end))
            self.assertEqual(factorize(start), [(start, 1)])
            self.assertEqual(factorize(end), [(end, 1)])
            self.assertEqual(factorize(middle), middle_factors)
            for n, following in zip(path, path[1:]):
                self.assertEqual(aliquot_sum(n), following)
                self.assertEqual(_divisor_pair_sum(n), following)
                self.assertGreater(following, n)
            self.assertTrue(all(gcd(n // 6, 6) == 1 for n in path))
            actual = (valuation_three(start + 1), valuation_three(end + 1))
            self.assertEqual(actual, budgets)
            self.assertGreater(actual[1], actual[0])

    def test_actual_supply_and_tag_reset_together(self):
        # Fixed witnesses, not a search over prime tuples or an orbit claim.
        for k, length, supplier, q in ((2, 2, 17, 139),
                                      (3, 2, 53, 877),
                                      (1, 3, 5, 571)):
            self.assertTrue(trial_prime(supplier))
            self.assertTrue(trial_prime(q))
            self.assertEqual(factorize(q), [(q, 1)])
            self.assertEqual(supplier % 4, 1)
            self.assertEqual((supplier + 1) % (3 ** k), 0)
            u, r = q * q, q * q + 2 * q + 2
            self.assertEqual(r % supplier, 0)
            self.assertNotEqual(r % (supplier * supplier), 0)
            self.assertEqual(gcd(u, 6), 1)
            self.assertEqual(gcd(r, 6), 1)
            self.assertEqual(aliquot_sum(6 * u), 6 * r)
            self.assertEqual(_divisor_pair_sum(6 * u), 6 * r)
            self.assertGreater(r, u)
            sigma_u = u + aliquot_sum(u)
            sigma_r = r + aliquot_sum(r)
            self.assertEqual(sigma_u, u + _divisor_pair_sum(u))
            self.assertEqual(sigma_r, r + _divisor_pair_sum(r))
            self.assertEqual(valuation_three(u + 1), 0)
            self.assertEqual(valuation_three(sigma_u), 1)
            self.assertGreaterEqual(valuation_three(r + 1), length)
            self.assertGreaterEqual(valuation_three(sigma_r), k)
            remainder = r // supplier
            self.assertEqual(sigma_r, (supplier + 1)
                             * (remainder + aliquot_sum(remainder)))

    def test_root_lifting_and_bounded_reset_witnesses(self):
        residue, modulus = 1, 3
        observed_primes = []
        for k in range(1, 9):
            if k > 1:
                lifts = [residue + t * modulus for t in range(3)
                         if ((residue + t * modulus + 1) ** 2 + 2)
                         % (3 * modulus) == 0]
                self.assertEqual(len(lifts), 1)
                residue = lifts[0]
                modulus *= 3
            self.assertEqual(modulus, 3 ** k)
            self.assertEqual(residue % 3, 1)
            self.assertEqual(gcd(residue, modulus), 1)
            self.assertEqual(((residue + 1) ** 2 + 2) % modulus, 0)
            self.assertEqual((2 * (residue + 1)) % 3, 1)

            first = residue if residue > 3 else residue + modulus
            q = next((first + j * modulus for j in range(10000)
                      if trial_prime(first + j * modulus)), None)
            self.assertIsNotNone(q, "finite prime-witness search exhausted")
            observed_primes.append(q)
            self.assertEqual(factorize(q), [(q, 1)])
            u = q * q
            r = q * q + 2 * q + 2
            source, successor = 6 * u, 6 * r
            self.assertLess(source, 1_800_000_000)
            self.assertEqual(aliquot_sum(source), successor)
            self.assertEqual(_divisor_pair_sum(source), successor)
            self.assertEqual(gcd(u, 6), 1)
            self.assertEqual(gcd(r, 6), 1)
            self.assertGreater(successor, source)
            self.assertEqual(valuation_three(u + 1), 0)
            self.assertGreaterEqual(valuation_three(r + 1), k)
            # No assertion that r is prime or that its future stays guarded.
        self.assertEqual(observed_primes, [7, 13, 31, 139, 463, 5323, 12613, 16987])


if __name__ == "__main__":
    unittest.main()
