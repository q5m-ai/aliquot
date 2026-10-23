"""Reproduce previously discussed bounds; no orbit or novelty extrapolation.

The largest sieve source is one million. The handoff trace has exactly 34
transitions and a separate source cap of one billion. Large prime-cofactor
candidates are stored as decimal strings and checked with exact arithmetic.
"""

from array import array
from fractions import Fraction
from math import gcd, prod
import unittest

from aliquot import aliquot_sum, factorize
from aliquot.research import divisor_sieve
from aliquot.two_adic import _divisor_pair_sum


class SynthesisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bound = 1_000_000
        cls.sums = divisor_sieve(cls.bound)

    def test_large_prime_supply_bound_with_exact_rationals(self):
        # All n=2..10,000; cutoffs B=2,3,5,11. No floating-point logarithms.
        checked = {b: 0 for b in (2, 3, 5, 11)}
        for n in range(2, 10_001):
            factors = factorize(n)
            actual = Fraction(n + self.sums[n], n)
            for b in checked:
                small = prod(p ** e for p, e in factors if p <= b)
                count = sum(p > b for p, _ in factors)
                small_abundancy = Fraction(small + self.sums[small], small)
                upper = small_abundancy * Fraction(b + 1, b) ** count
                self.assertLessEqual(actual, upper)
                if small_abundancy < 2 and self.sums[n] > n:
                    epsilon = 2 - small_abundancy
                    self.assertGreater(epsilon, 0)
                    self.assertLess(epsilon, 2)
                    self.assertGreater(count, 0)
                    self.assertGreater((2 - epsilon) * Fraction(b + 1, b) ** count, 2)
                    checked[b] += 1
        self.assertTrue(all(count > 0 for count in checked.values()))
        # A perfect small-prime part has no positive deficiency margin.
        self.assertEqual(Fraction(6 + self.sums[6], 6), 2)
        self.assertGreater(self.sums[6 * 97], 6 * 97)

    def test_smaller_abundant_prime_cofactor_predecessors(self):
        # C <=100, prime p <=97. This checks an inequality, not an escaping seed.
        primes = [p for p in range(2, 98) if self.sums[p] == 1]
        checked = 0
        for core in range(2, 101):
            if self.sums[core] <= core:
                continue
            for p in primes:
                if gcd(core, p) != 1:
                    continue
                predecessor = core * p
                image = self.sums[core] * p + core + self.sums[core]
                self.assertEqual(image, self.sums[predecessor])
                self.assertLess(predecessor, image)
                checked += 1
        self.assertGreater(checked, 0)

    def test_handoff_continuation_is_bounded_and_not_full_compensation(self):
        terms = [29274]
        for _ in range(34):
            source = terms[-1]
            self.assertGreater(source, 0)  # No iteration at zero.
            self.assertLessEqual(source, 1_000_000_000)
            successor = aliquot_sum(source)
            self.assertEqual(successor, _divisor_pair_sum(source))
            terms.append(successor)
        self.assertEqual(len(terms), 35)
        outside = [i for i, n in enumerate(terms[:-1])
                   if n % 6 != 0 or gcd(n // 6, 6) != 1]
        deficient = [i for i, (n, following) in enumerate(zip(terms, terms[1:]))
                     if following < n]
        self.assertEqual(outside[0], 23)
        self.assertEqual(terms[23:25], [2079918, 2720394])
        self.assertEqual(factorize(terms[23]), [(2, 1), (3, 4), (37, 1), (347, 1)])
        self.assertEqual(deficient[0], 32)
        self.assertEqual(terms[32:35], [101368952, 98701648, 100848080])
        self.assertEqual(factorize(terms[32]), [(2, 3), (19, 1), (666901, 1)])
        self.assertGreater(terms[34], terms[33])  # Abundance returns.
        self.assertLess(terms[34], terms[32])  # The loss is not fully recovered.

    def test_direct_predecessors_of_four_perfect_targets(self):
        # Exhausts n<=100,000 only, hence all smaller predecessors of these P.
        expected = {6: [6, 25], 28: [28], 496: [496, 652],
                    8128: [8128, 10682, 10828]}
        for target, predecessors in expected.items():
            self.assertEqual(self.sums[target], target)
            observed = [n for n in range(1, 100_001) if self.sums[n] == target]
            self.assertEqual(observed, predecessors)
            self.assertTrue(all(n >= target for n in observed))
            for n in observed:
                self.assertEqual(aliquot_sum(n), target)
                self.assertEqual(_divisor_pair_sum(n), target)

    def test_aspiring_examples_do_not_answer_upward_final_entry(self):
        for path in ([95, 25, 6, 6], [790, 650, 652, 496, 496],
                     [608, 652, 496, 496]):
            for n, following in zip(path, path[1:]):
                self.assertEqual(aliquot_sum(n), following)
                self.assertEqual(_divisor_pair_sum(n), following)
            self.assertGreater(path[-3], path[-2])  # Final nonfixed step is downward.
        self.assertGreater(self.sums[608], 608)
        self.assertGreater(self.sums[650], 650)

    def test_reverse_basins_stay_inside_the_stated_bound(self):
        # Reverse graph includes only positive sources AND targets <=1,000,000.
        # A path leaving the bound and later returning is not represented.
        heads = array('i', [-1]) * (self.bound + 1)
        links = array('i', [-1]) * (self.bound + 1)
        for n in range(1, self.bound + 1):
            following = self.sums[n]
            if 0 < following <= self.bound:
                links[n] = heads[following]
                heads[following] = n
        expected = {6: 5329, 28: 1, 496: 13, 8128: 696}
        for target, count in expected.items():
            visited = {target}  # Counts include the perfect target itself.
            pending = [target]
            while pending:
                current = pending.pop()
                predecessor = heads[current]
                while predecessor != -1:
                    if predecessor not in visited:
                        visited.add(predecessor)
                        pending.append(predecessor)
                    predecessor = links[predecessor]
            self.assertEqual(len(visited), count)
            self.assertEqual(min(visited), target)

    def test_restricted_abundant_core_prime_predecessor_search(self):
        # n=cp, abundant c<=200,000, p prime and coprime to c. NOT all predecessors.
        abundant = [c for c in range(2, 200_001) if self.sums[c] > c]
        expected = {19: [(176, "701217811")], 31: [(104, "21753235925848603")]}
        for exponent in (2, 3, 5, 7, 13, 17, 19, 31):
            mersenne = (1 << exponent) - 1
            self.assertEqual(factorize(mersenne), [(mersenne, 1)])
            target = (1 << (exponent - 1)) * mersenne
            self.assertEqual(aliquot_sum(target), target)
            candidates = []
            for core in abundant:
                proper = self.sums[core]
                numerator = target - (core + proper)
                if numerator <= proper or numerator % proper:
                    continue
                p = numerator // proper
                if gcd(core, p) != 1:
                    continue
                candidates.append((core, str(p)))
                # A budget exception fails as unresolved; it is never accepted as prime.
                factors = factorize(p)
                self.assertNotEqual(factors, [(p, 1)])
                self.assertEqual(prod(q ** e for q, e in factors), p)
                self.assertLess(core * p, target)
                self.assertEqual(proper * p + core + proper, target)
                # Independent small proper divisors certify the two candidates composite.
                small_divisor = {19: 7, 31: 11}[exponent]
                self.assertEqual(p % small_divisor, 0)
                self.assertGreater(p, small_divisor)
            self.assertEqual(candidates, expected.get(exponent, []))


if __name__ == "__main__":
    unittest.main()
