"""Finite regressions for RECOVERY.md, not proofs of its universal assertions."""

from fractions import Fraction
from math import gcd, isqrt
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.research import divisor_sieve


def divisor_pair_sum(n):
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            total += d
            if d != n // d:
                total += n // d
    return total - n


def affine_period(cores):
    """Exact formal coefficients; prime/coprimality guards remain separate."""
    a, b = Fraction(1), Fraction(0)
    for core in cores:
        proper = aliquot_sum(core)
        ratio = Fraction(proper, core)
        a, b = ratio * a, ratio * b + proper + core
    return a, b / cores[0]


class RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sums = divisor_sieve(25_000)
        cls.primes = [q for q in range(2, 5001) if cls.sums[q] == 1]

    def test_divisibility_inequality_without_coprimality(self):
        # Every d <= 100 and multiple m <= 10,000, including overlapping factors.
        for d in range(1, 101):
            for m in range(d, 10_001, d):
                self.assertGreaterEqual(self.sums[m] * d, self.sums[d] * m)
        self.assertNotEqual(gcd(160, 640 // 160), 1)
        self.assertGreaterEqual(Fraction(self.sums[640], 640), Fraction(218, 160))

    def test_deficient_prime_sources_and_reduced_progressions(self):
        # Proven primes q <= 5,000; the largest second-step source is 15,007.
        for q in self.primes:
            if q <= 7:
                continue
            self.assertEqual(self.sums[4 * q], 3 * q + 7)
            self.assertLess(3 * q + 7, 4 * q)
        for d in (20, 160, 320, 880):
            self.assertEqual(gcd(d, 21), 1)
            residue = (-7 * pow(3, -1, d)) % d
            self.assertEqual(gcd(residue, d), 1)
            r = Fraction(self.sums[d], d)
            self.assertGreater(r, 1)
            count = 0
            for q in self.primes:
                if q <= 7 or q % d != residue:
                    continue
                count += 1
                n, middle = 4 * q, 3 * q + 7
                following = self.sums[middle]
                self.assertEqual(middle % d, 0)
                self.assertGreater(following, middle)
                self.assertGreaterEqual(Fraction(following, middle), r)
                self.assertGreater(Fraction(following, n), 3 * r / 4)
            self.assertGreater(count, 0, f"No finite witness for d={d}")
        self.assertEqual((-7 * pow(3, -1, 160)) % 160, 51)
        self.assertEqual(3 * Fraction(self.sums[160], 160) / 4, Fraction(327, 320))

    def test_profitable_block_does_not_regenerate_and_terminates(self):
        path = [844, 640, 890, 730, 602, 454, 230, 202, 104, 106,
                56, 64, 63, 41, 1, 0]
        self.assertEqual(factorize(211), [(211, 1)])
        self.assertEqual(211 % 160, 51)
        self.assertLess(path[1], path[0])
        self.assertGreater(path[2], path[0])
        self.assertNotEqual(path[2] % 4, 0)  # Outside every four-times-prime class.
        self.assertEqual(len(path) - 1, 15)
        for n, following in zip(path, path[1:]):
            self.assertGreater(n, 0)  # Never evaluate s(0).
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(divisor_pair_sum(n), following)

    def test_conditional_abundant_deficient_abundant_excursion(self):
        # One exact witness, not an infinitude claim for simultaneous primes.
        p, q = 31, 131
        self.assertEqual(q, 4 * p + 7)
        self.assertEqual(p % 5, 1)
        for prime in (p, q):
            self.assertEqual(factorize(prime), [(prime, 1)])
        path = [12 * p, 4 * q, 12 * p + 28]
        self.assertEqual(path, [372, 524, 400])
        for n, following in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(divisor_pair_sum(n), following)
        self.assertGreater(self.sums[372], 372)
        self.assertLess(self.sums[524], 524)
        self.assertGreater(self.sums[400], 400)
        self.assertGreater(400, 372)
        self.assertEqual(400 % 20, 0)
        self.assertNotEqual(400 % 12, 0)

    def test_composite_recovery_class_and_exact_transport(self):
        # Every odd u in 3..5,000 satisfying the present-factorization entry guard.
        entries = composite_entries = unitary_bridges = 0
        for u in range(3, 5001, 2):
            sigma_u = u + self.sums[u]
            if 7 * sigma_u >= 8 * u or (sigma_u - 92 * u) % 160:
                continue
            entries += 1
            composite_entries += self.sums[u] != 1
            n = 4 * u
            middle = self.sums[n]
            self.assertEqual(middle, 3 * u + 7 * self.sums[u])
            self.assertLess(middle, n)
            self.assertEqual(middle % 160, 0)
            following = aliquot_sum(middle)
            self.assertEqual(following, divisor_pair_sum(middle))
            self.assertGreater(Fraction(following, n), Fraction(327, 320))
            v = middle // 160
            if v <= 1 or gcd(v, 160) != 1:
                continue
            self.assertEqual(following, 218 * v + 378 * self.sums[v])
            sigma_v = v + self.sums[v]
            self.assertEqual(following % 8 == 4, sigma_v % 4 == 2)
            if sigma_v % 4 != 2:
                continue
            unitary_bridges += 1
            w = following // 4
            self.assertEqual(w % 2, 1)
            self.assertEqual(w, Fraction(109 * v + 189 * self.sums[v], 2))
            correction = (Fraction(763, 320) * (self.sums[u] - 1)
                          + Fraction(189, 2) * (self.sums[v] - 1))
            self.assertEqual(w + 4429, Fraction(327, 320) * (u + 4429) + correction)
        self.assertGreater(entries, 0)
        self.assertGreater(composite_entries, 0)
        self.assertGreater(unitary_bridges, 0)

    def test_deficient_composite_endpoint_loses_the_renewal_congruence(self):
        path = [2764, 2080, 3212, 3004]
        for n, following in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(divisor_pair_sum(n), following)
        self.assertEqual(factorize(691), [(691, 1)])
        self.assertEqual(factorize(803), [(11, 1), (73, 1)])
        self.assertEqual(803 + self.sums[803], 888)
        self.assertLess(7 * 888, 8 * 803)
        self.assertNotEqual((888 - 92 * 803) % 160, 0)
        self.assertNotEqual(3004 % 160, 0)
        self.assertEqual(691 + 4429, 5120)
        self.assertEqual(Fraction(327, 320) * 5120, 803 + 4429)
        self.assertEqual(5120 % 320, 0)
        self.assertNotEqual(5120 % (320 ** 2), 0)

    def test_recovery_into_an_abundant_perfect_core(self):
        # Four named terms only, all sources below 14 million.
        d, core, p = 230945, 6466460, 6466457
        self.assertEqual(d, 5 * 11 * 13 * 17 * 19)
        self.assertEqual(core, 28 * d)
        self.assertEqual(gcd(d, 42), 1)
        self.assertEqual(p, core - 3)
        self.assertEqual(factorize(p), [(p, 1)])
        self.assertEqual(p % (core ** 2), core - 3)
        self.assertGreater(Fraction(aliquot_sum(core) + core, core), 3)
        path = [12932914, 6466460, 13854820, 19397084]
        for n, following in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(divisor_pair_sum(n), following)
        self.assertLess(path[1], path[0])
        self.assertGreater(path[2], path[0])
        self.assertGreater(path[3], path[2])
        self.assertEqual(path[0] % 4, 2)
        self.assertEqual(path[2] % 8, 4)
        self.assertEqual(path[2] % 28, 0)
        self.assertGreater(path[2], 28)
        self.assertEqual(path[2], 28 * (d + 2 * aliquot_sum(d)))

    def test_affine_step_requires_prime_and_coprime_cofactor(self):
        # Every core 2..60 and prime cofactor <=97 coprime to it.
        for core in range(2, 61):
            proper = self.sums[core]
            for p in self.primes:
                if p > 97:
                    break
                if gcd(core, p) != 1:
                    continue
                self.assertEqual(self.sums[core * p], proper * p + proper + core)
        self.assertNotEqual(self.sums[4 * 2], self.sums[4] * 2 + self.sums[4] + 4)
        self.assertNotEqual(self.sums[6 * 25], self.sums[6] * 25 + self.sums[6] + 6)

    def test_affine_composition_preserves_the_amicable_exception(self):
        a, c = affine_period((20, 4))
        self.assertEqual((a, c), (Fraction(33, 40), Fraction(77, 40)))
        self.assertEqual(c / (1 - a), 11)
        self.assertEqual(a * 11 + c, 11)
        for n, core, p, following in [(220, 20, 11, 284), (284, 4, 71, 220)]:
            self.assertEqual(n, core * p)
            self.assertEqual(gcd(core, p), 1)
            self.assertEqual(factorize(p), [(p, 1)])
            self.assertEqual(aliquot_sum(n), following)
            self.assertEqual(divisor_pair_sum(n), following)
        # Even a profitable formal block need not return to the chosen core.
        self.assertEqual(affine_period((12, 4)), (Fraction(1), Fraction(7, 3)))

    def test_denominator_budget_has_a_finite_exact_endpoint(self):
        a, c = affine_period((84,))
        self.assertEqual((a, c), (Fraction(5, 3), Fraction(8, 3)))
        shift = c / (a - 1)
        self.assertEqual(shift, 4)
        cofactors = [23, 41, 71, 121]
        for p, following in zip(cofactors, cofactors[1:]):
            self.assertEqual(factorize(p), [(p, 1)])
            self.assertEqual(a * p + c, following)
            self.assertEqual(aliquot_sum(84 * p), 84 * following)
        y0 = cofactors[0] + shift
        self.assertEqual(y0, 27)
        for j in range(4):
            self.assertEqual((a ** j * y0).denominator, 1)
        self.assertNotEqual((a ** 4 * y0).denominator, 1)
        self.assertNotEqual((a * 121 + c).denominator, 1)
        self.assertEqual(factorize(121), [(11, 2)])
        # A composite cofactor invalidates the affine formula before that next use.
        self.assertNotEqual(aliquot_sum(84 * 121), 84 * (a * 121 + c))

    def test_nonexpansive_graph_weights_and_scaled_prime_gap(self):
        # Named cores 4,8 with all four edges; weights 4,7 and step bound H=15.
        cores, weights = (4, 8), (4, 7)
        h = 15
        for i, core in enumerate(cores):
            for j, next_core in enumerate(cores):
                a = Fraction(self.sums[core], next_core)
                b = Fraction(self.sums[core] + core, next_core)
                self.assertLessEqual(weights[j] * a, weights[i])
                self.assertLessEqual(weights[j] * b, h)
        # One exact CRT gap of length H+1 in the union {4p,7p : p prime}.
        gap_primes = [p for p in self.primes if gcd(p, 28) == 1][:h + 1]
        self.assertEqual(len(gap_primes), h + 1)
        z, modulus = 0, 1
        for r, prime in enumerate(gap_primes, 1):
            z += modulus * (((-r - z) * pow(modulus, -1, prime)) % prime)
            modulus *= prime
        threshold = max(weights) * max(gap_primes)
        if z <= threshold:
            z += ((threshold - z) // modulus + 1) * modulus
        for r, prime in enumerate(gap_primes, 1):
            value = z + r
            self.assertEqual(value % prime, 0)
            for weight in weights:
                self.assertEqual(gcd(weight, prime), 1)
                self.assertGreater(value, weight * prime)
                if value % weight == 0:
                    cofactor = value // weight
                    self.assertEqual(cofactor % prime, 0)
                    self.assertGreater(cofactor, prime)  # Proven composite, not a PRP test.

    def test_affine_modular_trap_is_only_a_finite_illustration(self):
        # A,C in 1..8, primes p <=31 not dividing A; at most p iterations each.
        for a in range(1, 9):
            for c in range(1, 9):
                for p in self.primes:
                    if p > 31:
                        break
                    if a % p == 0:
                        continue
                    x = p
                    for _ in range(p):
                        x = a * x + c
                        if x % p == 0:
                            break
                    else:
                        self.fail(f"No modular return for {(a, c, p)}")
                    self.assertGreater(x, p)
                    self.assertEqual(x % p, 0)


if __name__ == "__main__":
    unittest.main()
