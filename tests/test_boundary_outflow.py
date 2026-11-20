"""Small exact excursion regressions, not an asymptotic or escape experiment.

Orbit sources are capped at 100,000. The separate semiprime check uses primes
through 499 and product sources below 250,000. Every computed aliquot edge is
checked by an independent divisor-pair sum; a cap breach fails as unresolved.
"""

from functools import lru_cache
from itertools import combinations
from math import isqrt
import unittest

from aliquot import aliquot_sum

SEED_BOUND = 1000
DEPTH = 4
ORBIT_SOURCE_CAP = 100000
ARITHMETIC_SOURCE_CAP = 250000


@lru_cache(None)
def checked_sum(n):
    if not 1 <= n <= ARITHMETIC_SOURCE_CAP:
        raise ValueError('Arithmetic source outside the explicit positive-source cap')
    actual = aliquot_sum(n)
    independent = sum(d + (n//d if d*d != n else 0)
                      for d in range(1, isqrt(n)+1) if n % d == 0) - n
    if actual != independent:
        raise ArithmeticError('Independent divisor-pair sum disagrees')
    return actual


def prefix(seed, depth):
    path = [seed]
    for _ in range(depth):
        source = path[-1]
        if source == 0:
            break
        if not 1 <= source <= ORBIT_SOURCE_CAP:
            raise ValueError('Orbit source outside the explicit positive-source cap')
        path.append(checked_sum(source))
    return path


def grows(path, depth):
    return len(path) > depth and all(a < b for a, b in zip(path[:depth], path[1:depth+1]))


def excursion_state(path, fence, depth):
    """Classify a verified immediate exit; absence after the horizon is unknown."""
    if depth < 1 or len(path) < 2 or not 1 <= path[0] <= fence < path[1]:
        raise ValueError('Expected an immediate exit and a positive observation horizon')
    seen = {path[0]}
    for value in path[1:depth+1]:
        if value <= fence:
            return 'returned'
        if value in seen:
            return 'cycle_outside'
        seen.add(value)
    if len(path) <= depth:
        raise ValueError('Incomplete prefix is unresolved, not still-open verification')
    return 'still_open'


def crossings(path, fence):
    outward = sum(a <= fence < b for a, b in zip(path, path[1:]))
    inward = sum(b <= fence < a for a, b in zip(path, path[1:]))
    return outward, inward


def first_passage(seed, fence, ceiling, step=checked_sum):
    """Resolve one finite-band stage, not the fate of its subsequent orbit."""
    if not 1 <= seed <= fence < ceiling:
        raise ValueError('Expected a seed inside two increasing integer fences')
    path = [seed]
    seen = {seed}
    for _ in range(ceiling-fence+1):
        value = step(path[-1])
        path.append(value)
        if len(path) == 2 and value <= fence:
            raise ValueError('Expected an immediate exit')
        if value > ceiling:
            return 'reached_next_fence', path
        if value <= fence:
            return 'returned', path
        if value in seen:
            return 'cycle_in_band', path
        seen.add(value)
    raise ArithmeticError('Finite band exhausted without a decision')


class BoundaryOutflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = {n: prefix(n, DEPTH) for n in range(1, SEED_BOUND+1)}

    def test_exact_table_and_nested_open_sets(self):
        expected = {
            (15, 2): (1, 1, 0, 0),
            (100, 2): (7, 3, 0, 4),
            (100, 4): (7, 5, 0, 2),
            (1000, 2): (65, 10, 0, 55),
            (1000, 4): (65, 22, 0, 43),
        }
        for fence in (15, 100, 1000):
            exits = {n for n in range(1, fence+1) if checked_sum(n) > fence}
            previous_open = exits
            for depth in range(1, DEPTH+1):
                groups = {state: set() for state in ('returned', 'cycle_outside', 'still_open')}
                for n in exits:
                    groups[excursion_state(self.paths[n], fence, depth)].add(n)
                self.assertEqual(sum(map(len, groups.values())), len(exits))
                self.assertEqual(set.union(*groups.values()), exits)
                self.assertLessEqual(groups['still_open'], previous_open)
                previous_open = groups['still_open']
                if (fence, depth) in expected:
                    row = (len(exits), *(len(group) for group in groups.values()))
                    self.assertEqual(row, expected[fence, depth])

    def test_complete_first_passage_stages_have_bounded_sources(self):
        expected = {15: (0, 1, 0, 2), 100: (3, 4, 0, 5), 1000: (43, 22, 0, 8)}
        for fence, row in expected.items():
            counts = {state: 0 for state in ('reached_next_fence', 'returned', 'cycle_in_band')}
            longest = 0
            exits = [n for n in range(1, fence+1) if checked_sum(n) > fence]
            for seed in exits:
                state, path = first_passage(seed, fence, 2*fence)
                counts[state] += 1
                longest = max(longest, len(path)-1)
                self.assertLessEqual(len(path)-1, fence+1)
                self.assertTrue(all(1 <= source <= 2*fence for source in path[:-1]))
                self.assertTrue(all(fence < value <= 2*fence for value in path[1:-1]))
                self.assertEqual(len(path[:-1]), len(set(path[:-1])))
                if state == 'reached_next_fence':
                    self.assertGreater(path[-1], 2*fence)
                elif state == 'returned':
                    self.assertLessEqual(path[-1], fence)
                else:
                    self.assertIn(path[-1], path[1:-1])
            self.assertEqual((*counts.values(), longest), row)
            self.assertEqual(sum(counts.values()), len(exits))
        # An overshooting target is accepted, not factorized or iterated.
        self.assertEqual(first_passage(840, 1000, 2000),
                         ('reached_next_fence', [840, 2040]))
        # Landing exactly on the upper fence is not yet success. Evaluate that
        # source, then accept the later overshoot without evaluating its target.
        self.assertEqual(first_passage(24, 24, 36),
                         ('reached_next_fence', [24, 36, 55]))

    def test_quick_closure_is_charged_to_a_growth_exception(self):
        for fence in (15, 100, 174, 1000):
            abundant = {n for n in range(1, fence+1) if checked_sum(n) > n}
            exits = {n for n in abundant if checked_sum(n) > fence}
            lower_bound = fence//12 - fence//16
            self.assertGreaterEqual(len(exits), lower_bound)
            for depth in range(1, DEPTH+1):
                exceptions = {n for n in abundant if not grows(self.paths[n], depth)}
                closed = {n for n in exits
                          if excursion_state(self.paths[n], fence, depth) != 'still_open'}
                self.assertLessEqual(closed, exceptions)
                self.assertGreaterEqual(len(exits-closed), lower_bound-len(exceptions))

    def test_every_cutoff_internal_edge_balance(self):
        for fence in range(1, SEED_BOUND+1):
            exits = sum(checked_sum(n) > fence for n in range(1, fence+1))
            # Include zero as an incoming target, but never as an outgoing source.
            inside_incoming = sum(0 <= checked_sum(n) <= fence for n in range(1, fence+1))
            self.assertEqual(inside_incoming, fence-exits)
            witnesses = range(fence//16+1, fence//12+1)
            self.assertTrue(all(12*t <= fence < checked_sum(12*t) for t in witnesses))
            self.assertGreaterEqual(exits, len(witnesses))

    def test_labelled_balance_for_all_small_prefixes(self):
        for fence in (15, 100, 174, 1000):
            total_outward = total_inward = total_outside = 0
            for seed in range(1, fence+1):
                path = self.paths[seed]
                outward, inward = crossings(path, fence)
                outside = int(path[-1] > fence)
                self.assertEqual(outward-inward, outside)
                total_outward += outward
                total_inward += inward
                total_outside += outside
            self.assertEqual(total_outward-total_inward, total_outside)
        self.assertEqual(prefix(12, 10), [12, 16, 15, 9, 4, 3, 1, 0])
        self.assertEqual(crossings(prefix(12, 10), 15), (1, 1))
        # A return resolves the excursion, not necessarily the entire orbit.
        self.assertEqual(prefix(220, 4), [220, 284, 220, 284, 220])
        self.assertEqual(crossings(prefix(220, 4), 220), (2, 2))

    def test_two_exits_can_share_one_return_edge(self):
        fence = 174
        paths = [prefix(seed, 7) for seed in (126, 174)]
        common_tail = [186, 198, 270, 450, 759, 393, 135]
        for path in paths:
            self.assertEqual(path[1:], common_tail)
            self.assertEqual(excursion_state(path, fence, 7), 'returned')
            self.assertEqual(crossings(path, fence), (1, 1))
        unique_edges = {edge for path in paths for edge in zip(path, path[1:])}
        outward_edges = {edge for edge in unique_edges if edge[0] <= fence < edge[1]}
        inward_edges = {edge for edge in unique_edges if edge[1] <= fence < edge[0]}
        self.assertEqual(outward_edges, {(126, 186), (174, 186)})
        self.assertEqual(inward_edges, {(393, 135)})
        self.assertEqual(sum(crossings(path, fence)[1] for path in paths), 2)

    def test_outside_cycle_and_censored_prefix_are_not_escape(self):
        # TOY map: double odd numbers; fix even numbers. This is NOT s(n).
        toy = [3, 6, 6]
        self.assertEqual(excursion_state(toy, 5, 1), 'still_open')
        self.assertEqual(excursion_state(toy, 5, 2), 'cycle_outside')
        self.assertEqual(crossings(toy, 5), (1, 0))
        self.assertEqual(first_passage(3, 5, 10, lambda n: 2*n if n % 2 else n),
                         ('cycle_in_band', toy))
        with self.assertRaises(ValueError):
            excursion_state([3, 6], 5, 2)
        with self.assertRaises(ValueError):
            checked_sum(0)
        with self.assertRaises(ValueError):
            checked_sum(ARITHMETIC_SOURCE_CAP+1)
        with self.assertRaises(ValueError):
            prefix(ORBIT_SOURCE_CAP+1, 1)
        self.assertEqual(prefix(1, 4), [1, 0])

    def test_finite_inverse_ceiling_for_nonprime_sources(self):
        for source in range(2, 10001):
            target = checked_sum(source)
            if target >= 2:
                self.assertLessEqual(source, (target-1)**2)
        # The excluded prime-to-1 sources do not satisfy a finite inverse ceiling.
        self.assertEqual(checked_sum(997), 1)
        self.assertEqual(checked_sum(49), 8)  # Equality for a prime square.
        self.assertEqual(49, (8-1)**2)

    def test_distinct_semiprime_inflow_bound(self):
        for fence in (15, 100, 1000):
            primes = [p for p in range(2, (fence-1)//2+1) if checked_sum(p) == 1]
            sources = set()
            outside = set()
            for p, q in combinations(primes, 2):
                source = p*q
                self.assertNotIn(source, sources)
                sources.add(source)
                target = checked_sum(source)
                self.assertEqual(target, p+q+1)
                self.assertLessEqual(target, fence)
                self.assertLessEqual(source, (fence-1)**2)
                if source > fence:
                    outside.add(source)
            pair_count = len(primes)*(len(primes)-1)//2
            self.assertEqual(len(sources), pair_count)
            self.assertGreaterEqual(len(outside), pair_count-fence)
            if fence == 1000:
                self.assertEqual(len(primes), 95)
                self.assertEqual(pair_count-fence, 3465)
                self.assertGreater(len(outside), fence)  # A finite check, not PNT.


if __name__ == '__main__':
    unittest.main()
