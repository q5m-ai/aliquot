"""Targeted finite regressions; no test proves the imported density theorem."""

from functools import lru_cache
from math import isqrt
import unittest

from aliquot import aliquot_sum

BOUND = 1000
DEPTH = 4
SOURCE_CAP = 100000


@lru_cache(None)
def checked_sum(n):
    if not 1 <= n <= SOURCE_CAP:
        raise ValueError('Regression source outside the explicit positive-source cap')
    actual = aliquot_sum(n)
    independent = sum(d+(n//d if d*d != n else 0)
                      for d in range(1, isqrt(n)+1) if n % d == 0)-n
    if actual != independent:
        raise ArithmeticError('Independent divisor-pair sum disagrees')
    return actual


def prefix(n, depth, function=checked_sum):
    path = [n]
    for _ in range(depth):
        if path[-1] == 0:
            break
        path.append(function(path[-1]))
    return path


def grows(path, depth):
    return len(path) > depth and all(path[j] < path[j+1] for j in range(depth))


def split_two(n):
    k, odd = 0, n
    while odd % 2 == 0:
        k, odd = k+1, odd//2
    return k, odd


def funnel(n, escaping=False):
    k, odd = split_two(n)
    if k < odd:
        return 2*n
    return 1 << n.bit_length() if escaping else 1


def fast_merger(n):
    return 2*n+1 if n % 2 == 0 else 1 << n.bit_length()


class AncestryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = {n: prefix(n, DEPTH) for n in range(1, BOUND+1)}

    def population(self, bound):
        abundant = {n for n in range(1, bound+1) if checked_sum(n) > n}
        outflow = {n for n in abundant if checked_sum(n) > bound}
        downward = {n for n in abundant if checked_sum(n) <= bound and checked_sum(n) not in abundant}
        inside = abundant-outflow-downward
        roots = abundant-{checked_sum(n) for n in inside}
        return abundant, outflow, downward, inside, roots

    def test_exact_root_accounting_and_boundary_bound_at_every_cutoff(self):
        for bound in range(1, BOUND+1):
            a, b, d, u, roots = self.population(bound)
            self.assertEqual(len(roots), len(b)+len(d)+len(u)-len({checked_sum(n) for n in u}))
            self.assertGreaterEqual(len(roots), len(b))
            boundary_sources = {12*t for t in range(bound//16+1, bound//12+1)}
            self.assertLessEqual(boundary_sources, b)
            self.assertEqual(len(boundary_sources), bound//12-bound//16)
            self.assertGreaterEqual(len(roots), len(boundary_sources))
            self.assertTrue(all(not grows(self.paths[n], 2) for n in d))

    def test_minimum_path_charge_and_two_independent_depth_budgets(self):
        for bound in (100, 400, 1000):
            a, _, _, _, roots = self.population(bound)
            exceptions = {h: {n for n in a if not grows(self.paths[n], h)}
                          for h in range(1, DEPTH+1)}
            for h in range(1, DEPTH+1):
                witnesses = {}
                for m in range(1, bound+1):
                    for n in self.paths[m][1:h+1]:
                        if m < n <= bound and n in a:
                            witnesses.setdefault(n, self.paths[m][:self.paths[m].index(n)+1])
                deeper_roots = a-set(witnesses)
                self.assertLessEqual(deeper_roots, roots)
                charges = {}
                for n in roots-deeper_roots:
                    path = witnesses[n]
                    self.assertEqual(len(path), len(set(path)))
                    self.assertTrue(all(value > 0 for value in path))
                    minimum = min(path)
                    suffix = path[path.index(minimum):]
                    length = len(suffix)-1
                    self.assertLess(minimum, n)
                    self.assertGreater(checked_sum(minimum), minimum)
                    self.assertGreaterEqual(length, 2)
                    self.assertLessEqual(length, h)
                    self.assertGreater(suffix[-2], n)
                    self.assertIn(minimum, exceptions[length])
                    self.assertEqual(self.paths[minimum][:length+1], suffix)
                    charges[n] = (minimum, length)
                self.assertEqual(len(set(charges.values())), len(charges))
                budget = sum(len(exceptions[length]) for length in range(2, h+1))
                self.assertLessEqual(len(roots-deeper_roots), budget)
                self.assertLessEqual(budget, (h-1)*len(exceptions[h]))
                for k in range(1, DEPTH+1):
                    survivors = {n for n in deeper_roots if grows(self.paths[n], k)}
                    self.assertLessEqual(len(roots)-len(survivors), budget+len(exceptions[k]))

    def test_named_indirect_ancestor_is_not_censored_at_target(self):
        self.assertEqual(prefix(372, 2), [372, 524, 400])
        self.assertGreater(checked_sum(400), 400)
        self.assertTrue(all(checked_sum(m) != 400 for m in range(1, 400)))
        self.assertGreater(524, 400)
        self.assertGreater(524, 372)
        self.assertEqual(prefix(400, 2), [400, 561, 303])

    def test_growing_coalescence_does_not_supply_an_ancestry_charge(self):
        self.assertEqual(prefix(174, 2), [174, 186, 198])
        self.assertEqual(prefix(126, 2), [126, 186, 198])
        self.assertTrue(all(checked_sum(m) != 174 for m in range(1, 174)))
        self.assertEqual(prefix(56, 1), [56, 64])
        self.assertEqual(prefix(48, 2), [48, 76, 64])
        self.assertTrue(all(checked_sum(m) != 56 for m in range(1, 56)))

    def test_zero_cycles_and_noninitial_minimum(self):
        self.assertEqual(prefix(1, 4), [1, 0])
        self.assertFalse(grows(prefix(1, 4), 4))
        self.assertEqual(prefix(220, 2), [220, 284, 220])
        self.assertFalse(grows(prefix(220, 2), 2))
        self.assertEqual(prefix(28, 2), [28, 28, 28])
        with self.assertRaises(ValueError):
            checked_sum(0)
        with self.assertRaises(ValueError):
            checked_sum(SOURCE_CAP+1)
        # Explicit TOY functional graph, not an aliquot claim: the initial
        # witness is deficient, while the suffix minimum is abundant.
        f = {1: 1, 2: 7, 3: 2, 4: 4, 5: 9, 7: 5}
        path = prefix(3, 3, f.__getitem__)
        self.assertEqual(path, [3, 2, 7, 5])
        self.assertTrue(all(f[m] != 5 for m in range(1, 5)))
        self.assertEqual(path[path.index(min(path)):], [2, 7, 5])
        self.assertLess(f[3], 3)
        self.assertGreater(f[2], 2)

    def test_sparse_funnel_countermodels_have_opposite_global_destinations(self):
        for n in range(1, 201):
            k, odd = split_two(n)
            steps = max(0, odd-k)+1
            cyclic = prefix(n, steps, funnel)
            escaping = prefix(n, steps, lambda x: funnel(x, True))
            self.assertEqual(cyclic[-1], 1)
            self.assertEqual(escaping[-1] & (escaping[-1]-1), 0)
            self.assertTrue(grows(escaping, steps))
        self.assertEqual(prefix(1, 4, funnel), [1, 2, 1, 2, 1])
        for n in range(3, 32, 2):
            doubling = [n*2**j for j in range(n+1)]
            self.assertEqual(prefix(n, n, funnel), doubling)
            self.assertEqual(prefix(n, n, lambda x: funnel(x, True)), doubling)
            self.assertEqual(funnel(doubling[-1]), 1)
        for n in range(1, 1001):
            self.assertTrue(funnel(n) == 1 or funnel(n) % 2 == 0)
            self.assertEqual(funnel(n, True) % 2, 0)

    def test_every_large_fast_merger_has_a_bounded_smaller_coalescence(self):
        for n in range(5, 1001):
            self.assertGreater(fast_merger(n), n)
            k = n.bit_length()-1
            if n % 2:
                k = fast_merger(n).bit_length()-1
                m, i, j = 2**(k-2), 1, 2
            elif n == 2**k:
                m, i, j = 2**(k-1)+1, 1, 2
            else:
                m, i, j = 2**k, 2, 2
            self.assertLess(m, n)
            self.assertIn(i, (1, 2))
            self.assertIn(j, (1, 2))
            self.assertEqual(prefix(n, i, fast_merger)[-1], prefix(m, j, fast_merger)[-1])
        bound = 1000
        actual_image = {fast_merger(n) for n in range(1, bound+1) if fast_merger(n) <= bound}
        expected_image = set(range(5, bound+1, 4)) | {2**k for k in range(1, bound.bit_length())}
        self.assertEqual(actual_image, expected_image)


if __name__ == '__main__':
    unittest.main()
